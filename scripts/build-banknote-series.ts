#!/usr/bin/env node
import { resolve, dirname, basename } from 'node:path'
import { fileURLToPath } from 'node:url'
import { mkdir, readdir, writeFile } from 'node:fs/promises'
import sharp from 'sharp'
import { cac } from 'cac'

const denominations = [
  { value: '005', ratio: 60 / 31 },
  { value: '010', ratio: 127 / 67 },
  { value: '020', ratio: 133 / 72 },
  { value: '50', ratio: 20 / 11 },
  { value: '100', ratio: 147 / 82 },
  { value: '200', ratio: 153 / 82 },
] as const
const sides = ['recto', 'verso'] as const
const ratioTolerance = 0.005
const scriptDir = dirname(fileURLToPath(import.meta.url))
const overlayPath = resolve(scriptDir, '../commons/ai-generated-black-transparent.svg')
const sheetBackground = '#eaf3f2'

type OutputFormat = 'jpeg' | 'webp'
type Options = { maxSize: string; maxWidth: string; overlayWidth: string; format: OutputFormat }

function positiveNumber(value: string, label: string): number {
  const number = Number(value)
  if (!Number.isFinite(number) || number <= 0) throw new Error(`${label} must be a positive number`)
  return number
}

function positiveInteger(value: string, label: string): number {
  const number = Number(value)
  if (!Number.isSafeInteger(number) || number <= 0) throw new Error(`${label} must be a positive integer`)
  return number
}

function bytesFromSize(value: string): number {
  const match = /^(\d+(?:\.\d+)?)\s*(b|kb|mb)?$/i.exec(value.trim())
  if (!match) throw new Error('max-size must be a number optionally followed by B, KB, or MB')
  const unit = (match[2] ?? 'b').toLowerCase()
  return Number(match[1]) * ({ b: 1, kb: 1024, mb: 1024 * 1024 }[unit] ?? 1)
}

async function encode(image: sharp.Sharp, format: OutputFormat, quality: number): Promise<Buffer> {
  return format === 'jpeg'
    ? image.flatten({ background: '#ffffff' }).jpeg({ quality, mozjpeg: true }).toBuffer()
    : image.webp({ quality, effort: 6 }).toBuffer()
}

async function buildContactSheet(
  images: Array<{ target: string; output: Buffer }>,
  maxBytes: number,
  format: OutputFormat
): Promise<Buffer> {
  const sheetWidth = 1080
  const sheetHeight = 1080
  const px = (value: number) => value
  const columns = 3
  const left = px(28)
  const right = px(28)
  const top = px(112)
  const bottom = px(28)
  const gapX = px(14)
  const gapY = px(10)
  const cellWidth = (sheetWidth - left - right - gapX * (columns - 1)) / columns
  const cellHeight = (sheetHeight - top - bottom - gapY * 3) / 4
  const labelHeight = px(34)
  const thumbWidth = Math.floor(cellWidth)
  const thumbHeight = Math.floor(cellHeight - labelHeight)
  const labelMarkup = images
    .map(({ target }, index) => {
      const denomination = target.match(/^EUR(\d+)_/)?.[1]
      const side = target.match(/_(recto|verso)\./)?.[1]
      const column = Math.floor(index / 2) % columns
      const row = (index % 2) + Math.floor(index / 6) * 2
      const x = left + column * (cellWidth + gapX) + px(4)
      const y = top + row * (cellHeight + gapY) + px(24)
      return `<text x="${x}" y="${y}" font-family="Arial, sans-serif" font-size="${px(19)}" font-weight="700" fill="#17394a">€${Number(denomination)} · ${side?.toUpperCase()}</text>`
    })
    .join('')
  const background = Buffer.from(
    `<svg width="${sheetWidth}" height="${sheetHeight}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="${sheetBackground}"/><text x="${left}" y="${px(38)}" font-family="Arial, sans-serif" font-size="${px(15)}" letter-spacing="${px(2)}" fill="#41616d">EURO BANKNOTE SERIES</text><text x="${left}" y="${px(78)}" font-family="Arial, sans-serif" font-size="${px(31)}" font-weight="700" fill="#17394a">Six denominations · recto and verso</text>${labelMarkup}</svg>`
  )
  const composites = [] as Array<{ input: Buffer; left: number; top: number }>
  for (let index = 0; index < images.length; index += 1) {
    const column = Math.floor(index / 2) % columns
    const row = (index % 2) + Math.floor(index / 6) * 2
    const thumbnail = await sharp(images[index].output)
      .resize({ width: thumbWidth, height: thumbHeight, fit: 'contain', background: sheetBackground })
      .png()
      .toBuffer()
    composites.push({
      input: thumbnail,
      left: Math.round(left + column * (cellWidth + gapX)),
      top: Math.round(top + row * (cellHeight + gapY) + labelHeight),
    })
  }
  let quality = 88
  let output = await encode(sharp(background).composite(composites), format, quality)
  while (output.byteLength > maxBytes && quality > 20) {
    quality -= 5
    output = await encode(sharp(background).composite(composites), format, quality)
  }
  if (output.byteLength > maxBytes)
    throw new Error(`Contact sheet is still ${output.byteLength} bytes at quality 20; increase --max-size`)
  return output
}

const cli = cac('build-banknote-series')
cli
  .command('<directory>', 'Validate and prepare a banknote series')
  .option('--max-size <size>', 'Maximum output size (B, KB, or MB)', { default: '1mb' })
  .option('--max-width <pixels>', 'Maximum note width in pixels; narrower notes are not resized', { default: '1080' })
  .option('--overlay-width <percent>', 'Overlay width as a percentage of note width', { default: '15' })
  .option('--format <format>', 'Output format: jpeg or webp', { default: 'jpeg' })
  .action(async (directory: string, options: Options) => {
    try {
      const inputDir = resolve(directory)
      const outputDir = resolve(inputDir, 'publish')
      const maxBytes = bytesFromSize(options.maxSize)
      const maxWidth = positiveInteger(options.maxWidth, 'max-width')
      const overlayPercent = positiveNumber(options.overlayWidth, 'overlay-width')
      const format = options.format.toLowerCase()
      if (format !== 'jpeg' && format !== 'webp') throw new Error('--format must be either jpeg or webp')
      const extension = format === 'jpeg' ? 'jpg' : 'webp'
      if (overlayPercent > 100) throw new Error('overlay-width cannot exceed 100%')

      const names = new Set(await readdir(inputDir))
      const jobs = denominations.flatMap(({ value, ratio }) =>
        sides.map(side => ({
          source: `EUR${value}_${side}.png`,
          target: `EUR${value}_${side}.${extension}`,
          ratio,
        }))
      )
      const missing = jobs.filter(({ source }) => !names.has(source)).map(({ source }) => source)
      if (missing.length) throw new Error(`Missing expected images:\n${missing.map(name => `  ${name}`).join('\n')}`)

      const validated = [] as Array<(typeof jobs)[number] & { width: number; height: number }>
      for (const job of jobs) {
        const metadata = await sharp(resolve(inputDir, job.source)).metadata()
        if (!metadata.width || !metadata.height) throw new Error(`Could not read dimensions for ${job.source}`)
        const actual = metadata.width / metadata.height
        if (Math.abs(actual - job.ratio) / job.ratio > ratioTolerance) {
          throw new Error(
            `${job.source} has ratio ${metadata.width}:${metadata.height} (${actual.toFixed(5)}); expected ${job.ratio.toFixed(5)} (within ${(ratioTolerance * 100).toFixed(1)}%)`
          )
        }
        validated.push({ ...job, width: metadata.width, height: metadata.height })
      }

      const prepared: Array<{ target: string; output: Buffer }> = []
      for (const job of validated) {
        const width = Math.min(job.width, maxWidth)
        const overlayWidth = Math.max(1, Math.round((width * overlayPercent) / 100))
        const overlay = await sharp(overlayPath).resize({ width: overlayWidth }).png().toBuffer()
        let quality = 90
        const render = () => {
          const image = sharp(resolve(inputDir, job.source))
          return (job.width > maxWidth ? image.resize({ width: maxWidth }) : image).composite([
            { input: overlay, gravity: 'southeast' },
          ])
        }
        let output = await encode(render(), format, quality)
        while (output.byteLength > maxBytes && quality > 20) {
          quality -= 5
          output = await encode(render(), format, quality)
        }
        if (output.byteLength > maxBytes)
          throw new Error(
            `${job.target} is still ${output.byteLength} bytes at quality 20; reduce --max-width or increase --max-size`
          )
        prepared.push({ target: job.target, output })
      }
      const contactSheet = await buildContactSheet(prepared, maxBytes, format)
      await mkdir(outputDir, { recursive: true })
      for (const { target, output } of prepared) {
        await writeFile(resolve(outputDir, target), output)
        console.log(`${target} (${output.byteLength} bytes)`)
      }
      await writeFile(resolve(outputDir, `contact-sheet.${extension}`), contactSheet)
      console.log(`contact-sheet.${extension} (${contactSheet.byteLength} bytes)`)
      console.log(`Prepared ${validated.length} notes in ${outputDir}`)
    } catch (error) {
      console.error(`Error: ${error instanceof Error ? error.message : String(error)}`)
      process.exitCode = 1
    }
  })
cli.help()
cli.version('1.0.0')
cli.parse()
