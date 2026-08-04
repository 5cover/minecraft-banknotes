import path from 'path'
import { downloadLinks } from './markdown-links.js'
import { mkdirSync } from 'fs'

async function main(): Promise<void> {
    const outputDirectory = path.resolve(import.meta.dirname, 'inputs', 'banknotes')
    mkdirSync(outputDirectory, { recursive: true })
    const designLetters = ['a', 'b', 'c', 'd', 'e'] as const
    const values = [5, 10, 20, 50, 100, 200] as const
    const sides = ['front', 'back'] as const
    const imageUrl = (
        designLetter: (typeof designLetters)[number],
        value: (typeof values)[number],
        side: (typeof sides)[number]
    ) =>
        new URL(
            `https://www.ecb.europa.eu/euro/banknotes/future_banknotes/shared/img/banknote-design-proposal-${designLetter}-${value}-${side}.jpg`
        )

    const urls: URL[] = []
    for (const designLetter of designLetters) {
        for (const value of values) {
            for (const side of sides) {
                urls.push(imageUrl(designLetter, value, side))
            }
        }
    }
    const result = await downloadLinks(urls, {
        outputDirectory,
        concurrency: 4,
    })
    for (const download of result) {
        if (download.status === 'downloaded') {
            console.log(`Downloaded ${download.url.href}`)
            console.log(`  -> ${download.outputPath}`)
        } else {
            console.error(`Failed ${download.url.href}: ${download.error?.message}`)
        }
    }

    if (result.some(item => item.status === 'failed')) {
        process.exitCode = 1
    }
}

main().catch((error: unknown) => {
    console.error(error)
    process.exitCode = 1
})
