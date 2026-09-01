#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'assets/font/Minecraft.ttf'
SVG_DIR = ROOT / 'assets/type_svg'
PNG_DIR = ROOT / 'assets/type_png'

GRID = {
    'Ε': ['11111','10000','11110','10000','11111'],
    'Υ': ['10001','01010','00100','00100','00100'],
    'Ρ': ['11110','10001','11110','10000','10000'],
    'Ω': ['01110','10001','10001','10101','11011'],
    'Е': ['11111','10000','11110','10000','11111'],
    'В': ['11110','10001','11110','10001','11110'],
    'Р': ['11110','10001','11110','10000','10000'],
    'О': ['01110','10001','10001','10001','01110'],
}

def safe_name(s):
    return {'€':'euro_sign','ΕΥΡΩ':'euro_greek','ЕВРО':'euro_cyrillic'}.get(s, s.lower())

def ttf_svg(text, out_path):
    font = TTFont(FONT)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font['hmtx']
    units = font['head'].unitsPerEm
    x = 0
    paths = []
    for ch in text:
        gname = cmap.get(ord(ch), '.notdef')
        pen = SVGPathPen(glyphs)
        glyphs[gname].draw(pen)
        d = pen.getCommands()
        if d:
            paths.append(f'<path transform="translate({x} {units}) scale(1 -1)" d="{d}"/>')
        x += hmtx[gname][0]
    out_path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max(x,1)} {units}">' + ''.join(paths) + '</svg>')

def grid_svg(text, out_path):
    cell, gap = 20, 14
    x = 0
    rects = []
    for ch in text:
        rows = GRID[ch]
        for yy,row in enumerate(rows):
            for xx,val in enumerate(row):
                if val == '1': rects.append(f'<rect x="{x+xx*cell}" y="{yy*cell}" width="{cell}" height="{cell}"/>')
        x += 5*cell + gap
    out_path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x-gap} {5*cell}">' + ''.join(rects) + '</svg>')

def png_text(text, out_path):
    if text in GRID or any(ch in GRID for ch in text):
        cell, gap = 26, 16
        im = Image.new('RGBA', (len(text)*(5*cell+gap), 5*cell), (0,0,0,0))
        d = ImageDraw.Draw(im)
        x = 0
        for ch in text:
            for yy,row in enumerate(GRID[ch]):
                for xx,val in enumerate(row):
                    if val == '1': d.rectangle((x+xx*cell, yy*cell, x+(xx+1)*cell-1, (yy+1)*cell-1), fill='white')
            x += 5*cell+gap
        im = im.crop(im.getbbox())
    else:
        font = ImageFont.truetype(str(FONT), 180)
        box = font.getbbox(text, stroke_width=0)
        im = Image.new('RGBA', (box[2]-box[0]+16, box[3]-box[1]+16), (0,0,0,0))
        ImageDraw.Draw(im).text((8-box[0],8-box[1]), text, font=font, fill='white')
    im.save(out_path)

def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    for text in ['EURO','€','5','10','20','50','100','200']:
        name=safe_name(text); ttf_svg(text, SVG_DIR/f'{name}_master.svg'); png_text(text, PNG_DIR/f'{name}_master.png')
    for text in ['ΕΥΡΩ','ЕВРО']:
        name=safe_name(text); grid_svg(text, SVG_DIR/f'{name}_master.svg'); png_text(text, PNG_DIR/f'{name}_master.png')
    print(f'Built typography assets in {SVG_DIR} and {PNG_DIR}')

if __name__ == '__main__': main()
