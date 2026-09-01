#!/usr/bin/env node
const sharp = require('sharp');

const [src, dst, width, height] = process.argv.slice(2);
if (!src || !dst || !width || !height) {
  throw new Error('usage: rasterize_svg.js SOURCE.svg DEST.png WIDTH HEIGHT');
}
sharp(src)
  .resize(Number(width), Number(height), { fit: 'contain' })
  .png()
  .toFile(dst)
  .catch((error) => { console.error(error); process.exit(1); });
