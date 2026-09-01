#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
for path in sorted((ROOT/'generated/scenes').glob('*.png')):
    with Image.open(path) as im:
        optimized=im.convert('RGB').quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.FLOYDSTEINBERG)
        optimized.save(path,optimize=True)
        optimized.close()
    print(path.name)
print('Optimized 12 scene plates as lossless indexed-colour PNGs.')
