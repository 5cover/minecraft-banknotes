#!/usr/bin/env node
import { resolve, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdir, readdir, writeFile } from 'node:fs/promises';
import sharp from 'sharp';
import { cac } from 'cac';

const denominations = [
  { value: '005', ratio: 60 / 31 },
  { value: '010', ratio: 127 / 67 },
  { value: '020', ratio: 133 / 72 },
  { value: '50', ratio: 20 / 11 },
  { value: '100', ratio: 147 / 82 },
  { value: '200', ratio: 153 / 82 },
] as const;
const sides = ['recto', 'verso'] as const;
const ratioTolerance = 0.005;
const scriptDir = dirname(fileURLToPath(import.meta.url));
const overlayPath = resolve(scriptDir, '../commons/ai-generated-black-transparent.svg');

type Options = { maxSize: string; scale: string; overlayWidth: string };

function positiveNumber(value: string, label: string): number {
  const number = Number(value);
  if (!Number.isFinite(number) || number <= 0) throw new Error(`${label} must be a positive number`);
  return number;
}

function bytesFromSize(value: string): number {
  const match = /^(\d+(?:\.\d+)?)\s*(b|kb|mb)?$/i.exec(value.trim());
  if (!match) throw new Error('max-size must be a number optionally followed by B, KB, or MB');
  const unit = (match[2] ?? 'b').toLowerCase();
  return Number(match[1]) * ({ b: 1, kb: 1024, mb: 1024 * 1024 }[unit] ?? 1);
}

const cli = cac('build-banknote-series');
cli.command('<directory>', 'Validate and prepare a banknote series')
  .option('--max-size <size>', 'Maximum output size (B, KB, or MB)', { default: '1mb' })
  .option('--scale <percent>', 'Resize percentage; 100 skips resizing', { default: '100' })
  .option('--overlay-width <percent>', 'Overlay width as a percentage of note width', { default: '15' })
  .action(async (directory: string, options: Options) => {
    try {
      const inputDir = resolve(directory);
      const outputDir = resolve(inputDir, 'publish');
      const maxBytes = bytesFromSize(options.maxSize);
      const scale = positiveNumber(options.scale, 'scale');
      const overlayPercent = positiveNumber(options.overlayWidth, 'overlay-width');
      if (overlayPercent > 100) throw new Error('overlay-width cannot exceed 100%');

      const names = new Set(await readdir(inputDir));
      const jobs = denominations.flatMap(({ value, ratio }) => sides.map((side) => ({
        source: `EUR${value}_${side}.png`,
        target: `EUR${value}_${side}.webp`,
        ratio,
      })));
      const missing = jobs.filter(({ source }) => !names.has(source)).map(({ source }) => source);
      if (missing.length) throw new Error(`Missing expected images:\n${missing.map((name) => `  ${name}`).join('\n')}`);

      const validated = [] as Array<(typeof jobs)[number] & { width: number; height: number }>;
      for (const job of jobs) {
        const metadata = await sharp(resolve(inputDir, job.source)).metadata();
        if (!metadata.width || !metadata.height) throw new Error(`Could not read dimensions for ${job.source}`);
        const actual = metadata.width / metadata.height;
        if (Math.abs(actual - job.ratio) / job.ratio > ratioTolerance) {
          throw new Error(`${job.source} has ratio ${metadata.width}:${metadata.height} (${actual.toFixed(5)}); expected ${job.ratio.toFixed(5)} (within ${(ratioTolerance * 100).toFixed(1)}%)`);
        }
        validated.push({ ...job, width: metadata.width, height: metadata.height });
      }

      const prepared: Array<{ target: string; output: Buffer }> = [];
      for (const job of validated) {
        const width = Math.max(1, Math.round(job.width * scale / 100));
        const height = Math.max(1, Math.round(job.height * scale / 100));
        const overlayWidth = Math.max(1, Math.round(width * overlayPercent / 100));
        const overlay = await sharp(overlayPath).resize({ width: overlayWidth }).png().toBuffer();
        let quality = 90;
        let output = await sharp(resolve(inputDir, job.source))
          .resize({ width, height, fit: 'fill' })
          .composite([{ input: overlay, gravity: 'southeast' }])
          .webp({ quality, effort: 6 })
          .toBuffer();
        while (output.byteLength > maxBytes && quality > 20) {
          quality -= 5;
          output = await sharp(resolve(inputDir, job.source))
            .resize({ width, height, fit: 'fill' })
            .composite([{ input: overlay, gravity: 'southeast' }])
            .webp({ quality, effort: 6 })
            .toBuffer();
        }
        if (output.byteLength > maxBytes) throw new Error(`${job.target} is still ${output.byteLength} bytes at quality 20; reduce --scale or increase --max-size`);
        prepared.push({ target: job.target, output });
      }
      await mkdir(outputDir, { recursive: true });
      for (const { target, output } of prepared) {
        await writeFile(resolve(outputDir, target), output);
        console.log(`${target} (${output.byteLength} bytes)`);
      }
      console.log(`Prepared ${validated.length} notes in ${outputDir}`);
    } catch (error) {
      console.error(`Error: ${error instanceof Error ? error.message : String(error)}`);
      process.exitCode = 1;
    }
  });
cli.help();
cli.version('1.0.0');
cli.parse();
