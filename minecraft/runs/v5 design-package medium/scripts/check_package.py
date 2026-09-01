#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import yaml

ROOT=Path(__file__).resolve().parents[1]
with open(ROOT/'layout.yaml',encoding='utf-8') as f: layout=yaml.safe_load(f)
errors=[]
for code,meta in layout['notes'].items():
    for side in ('recto','verso'):
        p=ROOT/f'outputs/notes/{code}_{side}.png'
        if not p.exists(): errors.append(f'missing {p.relative_to(ROOT)}'); continue
        with Image.open(p) as im:
            if im.size != (meta['width'],meta['height']): errors.append(f'wrong size {p.name}: {im.size}')
required=[
    ROOT/'assets/font/Minecraft.ttf', ROOT/'assets/flags/eu_flag_master.svg',
    ROOT/'assets/maps/europe_map_master.svg', ROOT/'outputs/contacts/paired_contact.png'
]
for ore in ('coal','redstone','lapis','copper','emerald','gold'):
    required.append(ROOT/f'assets/ore_blocks/{ore}.webp')
for p in required:
    if not p.exists(): errors.append(f'missing {p.relative_to(ROOT)}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print('Package check passed: 12 note sizes and required shared assets are present.')
