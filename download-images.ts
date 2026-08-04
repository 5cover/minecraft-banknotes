import path from 'path'
import { processMarkdownFile } from './markdown-links.js'
import { mkdirSync } from 'fs'

async function main(): Promise<void> {
  const outputDirectory = path.resolve(import.meta.dirname, 'inputs', 'banknotes')
  mkdirSync(outputDirectory, { recursive: true })
  const result = await processMarkdownFile(
    path.resolve(import.meta.dirname, 'inputs', 'design-proposals.md'),
    url => url.pathname.toLowerCase().endsWith('.jpg'),
    {
      outputDirectory,
      concurrency: 4,
    }
  )
  console.log(result.allLinks.join('\n'))
  console.log(`Found: ${result.allLinks.length}`)
  console.log(`Selected: ${result.selectedLinks.length}`)

  for (const download of result.downloads) {
    if (download.status === 'downloaded') {
      console.log(`Downloaded ${download.url.href}`)
      console.log(`  -> ${download.outputPath}`)
    } else {
      console.error(`Failed ${download.url.href}: ${download.error?.message}`)
    }
  }

  if (result.downloads.some(item => item.status === 'failed')) {
    process.exitCode = 1
  }
}

main().catch((error: unknown) => {
  console.error(error)
  process.exitCode = 1
})
