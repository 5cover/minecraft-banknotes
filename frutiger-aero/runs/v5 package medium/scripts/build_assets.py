from pathlib import Path
import json, math, shutil, xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets/approved'

def type_asset(text, name):
    font_path = ROOT / 'assets/supplied/DejaVuSans.ttf'
    font = TTFont(font_path)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    missing = [c for c in text if ord(c) not in cmap]
    if missing:
        raise ValueError(f'Missing glyphs: {missing}')
    x = 0
    paths = []
    for c in text:
        glyph = glyphs[cmap[ord(c)]]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        paths.append(f'<path transform="translate({x} 0)" d="{pen.getCommands()}"/>')
        x += glyph.width + 35
    (A / f'{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x} 2400"><g transform="translate(0 1900) scale(1 -1)">{"".join(paths)}</g></svg>')
    pil_font = ImageFont.truetype(str(font_path), 600)
    im = Image.new('L', (int(x / font['head'].unitsPerEm * 600) + 100, 850))
    d = ImageDraw.Draw(im)
    px = 0
    for c in text:
        d.text((px, 0), c, font=pil_font, fill=255)
        px += (glyphs[cmap[ord(c)]].width + 35) / font['head'].unitsPerEm * 600
    im = im.crop(im.getbbox())
    im.save(A / f'{name}.png')

def currency_group():
    ims = [Image.open(A / f'type_{n}.png') for n in range(3)]
    height = 160
    fitted = [im.resize((round(im.width * height / im.height), height), Image.Resampling.LANCZOS) for im in ims]
    width = max(im.width for im in fitted)
    group = Image.new('L', (width, 3 * height + 2 * 42))
    for i, im in enumerate(fitted):
        group.paste(im, ((width - im.width) // 2, i * (height + 42)))
    group.save(A / 'currency_group.png')
    blocks=[]
    for i in range(3):
        root=ET.fromstring((A/f'type_{i}.svg').read_text())
        vb=root.attrib['viewBox']
        body=''.join(ET.tostring(child,encoding='unicode') for child in root)
        blocks.append(f'<svg x="0" y="{i*2400}" width="6500" height="2400" viewBox="{vb}">{body}</svg>')
    (A/'currency_group.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 6500 7200">'+''.join(blocks)+'</svg>')

def map_asset():
    data = json.loads((ROOT / 'assets/supplied/natural-earth-countries.geojson').read_text())
    w, h = 1200, 1000
    im = Image.new('L', (w, h))
    d = ImageDraw.Draw(im)
    paths = []
    # A fixed equirectangular projection, fixed x/y scales corresponding to a standard parallel near 49 degrees N; no country borders.
    sx = w / 70
    sy = h / 38
    for f in data['features']:
        prop = f['properties']
        if prop['CONTINENT'] != 'Europe' and prop['ADMIN'] not in ['Cyprus', 'Northern Cyprus', 'Turkey']:
            continue
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            for n, ring in enumerate(poly):
                points = [((lon + 25) * sx, (72 - lat) * sy) for lon, lat in ring]
                d.polygon(points, fill=255 if n == 0 else 0)
                path = 'M ' + ' L '.join(f'{x:.2f} {y:.2f}' for x, y in points) + ' Z'
                paths.append(f'<path d="{path}" fill="{"black" if n == 0 else "white"}"/>')
    im.save(A / 'europe_mask.png')
    (A / 'europe.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{"".join(paths)}</svg>')

def flag_asset():
    im = Image.new('RGBA', (900, 600), '#003399')
    d = ImageDraw.Draw(im)
    star_paths = []
    for i in range(12):
        a = i * math.pi / 6 - math.pi / 2
        cx, cy = 450 + 200 * math.cos(a), 300 + 200 * math.sin(a)
        pts = []
        for j in range(10):
            ang = j * math.pi / 5 - math.pi / 2
            r = 33.333 if j % 2 == 0 else 12.732
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.polygon(pts, fill='#FFCC00')
        star_paths.append('<polygon points="' + ' '.join(f'{x:.3f},{y:.3f}' for x,y in pts) + '" fill="#FFCC00"/>')
    im.save(A / 'european_flag.png')
    (A / 'european_flag.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600"><path fill="#003399" d="M0 0H900V600H0Z"/>' + ''.join(star_paths) + '</svg>')

if __name__ == '__main__':
    A.mkdir(parents=True, exist_ok=True)
    for n in [5,10,20,50,100,200]:
        type_asset(str(n), f'value_{n}')
    for n, word in enumerate(['EURO','ΕΥΡΩ','ЕВРО']):
        type_asset(word, f'type_{n}')
    currency_group()
    map_asset()
    flag_asset()
    print('Built portable outlined lettering, currency group, geographic map and flag.')
