import { createHash } from 'node:crypto'
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import path from 'node:path'

import rehypeRaw from 'rehype-raw'
import remarkParse from 'remark-parse'
import remarkRehype from 'remark-rehype'
import { unified } from 'unified'
import { visit } from 'unist-util-visit'
import type { Element, Root } from 'hast'

export type LinkPredicate = (url: URL, index: number, allLinks: readonly URL[]) => boolean | Promise<boolean>

export interface ExtractLinksOptions {
  /**
   * Used to resolve relative links such as "./manual.pdf".
   *
   * For a local Markdown file, this could be the public URL corresponding
   * to that document, such as "https://example.com/docs/readme.md".
   */
  baseUrl?: string | URL
}

export interface DownloadOptions {
  outputDirectory: string

  /**
   * Number of downloads allowed at once.
   */
  concurrency?: number

  /**
   * Optional fetch settings, such as headers or an AbortSignal.
   */
  requestInit?: RequestInit
}

export interface DownloadResult {
  url: URL
  outputPath?: string
  status: 'downloaded' | 'failed'
  error?: Error
}

const URL_PROPERTIES_BY_TAG: Readonly<Record<string, readonly string[]>> = {
  a: ['href'],
  area: ['href'],
  audio: ['src'],
  embed: ['src'],
  iframe: ['src'],
  img: ['src', 'srcSet'],
  input: ['src'],
  link: ['href'],
  object: ['data'],
  script: ['src'],
  source: ['src', 'srcSet'],
  track: ['src'],
  video: ['src', 'poster'],
}

export async function extractLinks(markdown: string, options: ExtractLinksOptions = {}): Promise<URL[]> {
  const processor = unified().use(remarkParse).use(remarkRehype, { allowDangerousHtml: true }).use(rehypeRaw)

  const markdownTree = processor.parse(markdown)
  const htmlTree = processor.runSync(markdownTree) as Root
  const rawUrls: string[] = []

  visit(htmlTree, 'element', (node: Element) => {
    const properties = URL_PROPERTIES_BY_TAG[node.tagName]

    if (!properties) {
      return
    }

    for (const propertyName of properties) {
      const value = node.properties?.[propertyName]

      if (typeof value !== 'string') {
        continue
      }

      if (propertyName === 'srcSet') {
        rawUrls.push(...parseSrcSet(value))
      } else {
        rawUrls.push(value)
      }
    }
  })

  return rawUrls.flatMap(rawUrl => {
    try {
      return [resolveUrl(rawUrl, options.baseUrl)]
    } catch {
      return []
    }
  })
}

/**
 * Extracts URL candidates from srcset.
 *
 * Examples:
 *   image.png 1x, image@2x.png 2x
 *   small.png 480w, large.png 1080w
 */
function parseSrcSet(srcSet: string): string[] {
  return srcSet
    .split(',')
    .map(candidate => candidate.trim())
    .filter(Boolean)
    .map(candidate => {
      const whitespaceIndex = candidate.search(/\s/)

      return whitespaceIndex === -1 ? candidate : candidate.slice(0, whitespaceIndex)
    })
    .filter(Boolean)
}

function resolveUrl(rawUrl: string, baseUrl?: string | URL): URL {
  const value = rawUrl.trim()

  if (value.length === 0 || value.startsWith('#') || value.startsWith('data:') || value.startsWith('javascript:')) {
    throw new Error(`URL is not downloadable: ${value}`)
  }

  return baseUrl ? new URL(value, baseUrl) : new URL(value)
}
/**
 * Applies an async or synchronous predicate while preserving link order.
 */
export async function filterLinks(links: readonly URL[], predicate: LinkPredicate): Promise<URL[]> {
  const decisions = await Promise.all(links.map((link, index) => predicate(link, index, links)))

  return links.filter((_, index) => decisions[index])
}

/**
 * Downloads all supplied URLs into the configured output directory.
 *
 * This function does no Markdown parsing or filtering.
 */
export async function downloadLinks(links: readonly URL[], options: DownloadOptions): Promise<DownloadResult[]> {
  const concurrency = options.concurrency ?? 4

  if (!Number.isInteger(concurrency) || concurrency < 1) {
    throw new Error('concurrency must be a positive integer')
  }

  await mkdir(options.outputDirectory, { recursive: true })

  return mapWithConcurrency(links, concurrency, async (url, index) => {
    try {
      validateDownloadProtocol(url)

      const response = await fetch(url, {
        redirect: 'follow',
        ...options.requestInit,
      })

      if (!response.ok) {
        throw new Error(`Request failed with ${response.status} ${response.statusText}`)
      }

      const data = Buffer.from(await response.arrayBuffer())
      const filename = createOutputFilename(url, index)
      const outputPath = path.join(options.outputDirectory, filename)

      await writeFile(outputPath, data)

      return {
        url,
        outputPath,
        status: 'downloaded',
      } satisfies DownloadResult
    } catch (error) {
      return {
        url,
        status: 'failed',
        error: toError(error),
      } satisfies DownloadResult
    }
  })
}

/**
 * Full pipeline:
 * 1. Read the complete Markdown document.
 * 2. Extract the complete link list.
 * 3. Filter that list.
 * 4. Download the selected files.
 */
export async function processMarkdownFile(
  markdownPath: string,
  predicate: LinkPredicate,
  downloadOptions: DownloadOptions,
  extractOptions: ExtractLinksOptions = {}
): Promise<{
  allLinks: URL[]
  selectedLinks: URL[]
  downloads: DownloadResult[]
}> {
  const markdown = await readFile(markdownPath, 'utf8')

  const allLinks = await extractLinks(markdown, extractOptions)
  const selectedLinks = await filterLinks(allLinks, predicate)
  const downloads = await downloadLinks(selectedLinks, downloadOptions)

  return {
    allLinks,
    selectedLinks,
    downloads,
  }
}

function validateDownloadProtocol(url: URL): void {
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new Error(`Unsupported protocol: ${url.protocol}`)
  }
}

function createOutputFilename(url: URL, index: number): string {
  const decodedPath = safelyDecodeURIComponent(url.pathname)
  const candidate = path.basename(decodedPath)
  const parsed = path.parse(candidate)

  const baseName = sanitizeFilename(parsed.name || 'download')
  const extension = sanitizeExtension(parsed.ext)
  const fingerprint = createHash('sha256').update(url.href).digest('hex').slice(0, 10)

  return `${baseName}-${fingerprint}${extension}`
}

function sanitizeFilename(value: string): string {
  const sanitized = value
    .replace(/[<>:"/\\|?*\u0000-\u001f]/g, '-')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^[.-]+|[.-]+$/g, '')
    .slice(0, 100)

  return sanitized || 'download'
}

function sanitizeExtension(extension: string): string {
  return /^\.[a-zA-Z0-9]{1,10}$/.test(extension) ? extension : ''
}

function safelyDecodeURIComponent(value: string): string {
  try {
    return decodeURIComponent(value)
  } catch {
    return value
  }
}

function toError(value: unknown): Error {
  return value instanceof Error ? value : new Error(String(value))
}

async function mapWithConcurrency<T, R>(
  values: readonly T[],
  concurrency: number,
  operation: (value: T, index: number) => Promise<R>
): Promise<R[]> {
  const results = new Array<R>(values.length)
  let nextIndex = 0

  async function worker(): Promise<void> {
    while (true) {
      const index = nextIndex
      nextIndex += 1

      if (index >= values.length) {
        return
      }

      results[index] = await operation(values[index], index)
    }
  }

  const workerCount = Math.min(concurrency, values.length)

  await Promise.all(Array.from({ length: workerCount }, () => worker()))

  return results
}
