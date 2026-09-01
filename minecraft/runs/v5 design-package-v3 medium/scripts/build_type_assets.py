#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = ROOT / "assets/font/Minecraft.ttf"
SVG_DIR = ROOT / "assets/type_svg"
PNG_DIR = ROOT / "assets/type_png"

PIXELS = {
    "€": ["01110", "10000", "11110", "10000", "11110", "10000", "01110"],
    "Ε": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "Υ": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Ρ": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Ω": ["01110", "10001", "10001", "10001", "10001", "10101", "01010"],
    "Е": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "В": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "Р": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "О": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
}

def render_font_png(text, filename, size=220):
    font = ImageFont.truetype(str(FONT_PATH), size)
    box = font.getbbox(text)
    im = Image.new("RGBA", (box[2] - box[0] + 24, box[3] - box[1] + 24), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((12 - box[0], 12 - box[1]), text, font=font, fill=(255, 255, 255, 255))
    im.save(PNG_DIR / filename)

def pixel_geometry(text, unit=22, gap=2):
    x = 0
    rects = []
    for ch in text:
        grid = PIXELS[ch]
        for row, line in enumerate(grid):
            for col, bit in enumerate(line):
                if bit == "1":
                    rects.append((x + col * unit, row * unit, unit, unit))
        x += (5 + gap) * unit
    return rects, max(unit, x - gap * unit), 7 * unit

def render_pixel_assets(text, stem):
    rects, w, h = pixel_geometry(text)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">', '<g fill="#000">']
    svg += [f'<rect x="{x}" y="{y}" width="{rw}" height="{rh}"/>' for x, y, rw, rh in rects]
    svg += ["</g></svg>"]
    (SVG_DIR / f"{stem}.svg").write_text("\n".join(svg), encoding="utf-8")
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x, y, rw, rh in rects:
        d.rectangle((x, y, x + rw, y + rh), fill=(255, 255, 255, 255))
    im.save(PNG_DIR / f"{stem}.png")

def outline_font_svg(text, stem):
    font = TTFont(str(FONT_PATH))
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    units = font["head"].unitsPerEm
    x = 0
    paths = []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyph_set)
        glyph_set[name].draw(pen)
        paths.append(f'<path d="{pen.getCommands()}" transform="translate({x} {units}) scale(1 -1)"/>')
        x += glyph_set[name].width
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x} {units}"><g fill="#000">{"".join(paths)}</g></svg>'
    (SVG_DIR / f"{stem}.svg").write_text(svg, encoding="utf-8")

def grouped_png():
    items = [Image.open(PNG_DIR / n).convert("RGBA") for n in ["euro_latin.png", "euro_greek.png", "euro_cyrillic.png"]]
    target_w = max(im.width for im in items)
    resized = []
    for im in items:
        scale = target_w / im.width
        resized.append(im.resize((target_w, max(1, int(im.height * scale))), Image.Resampling.NEAREST))
    gap = 18
    out = Image.new("RGBA", (target_w, sum(i.height for i in resized) + gap * 2), (0, 0, 0, 0))
    y = 0
    for im in resized:
        out.alpha_composite(im, (0, y)); y += im.height + gap
    out.save(PNG_DIR / "euro_scripts_grouped.png")
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 900"><image href="euro_latin.svg" x="0" y="0" width="1000" height="240"/><image href="euro_greek.svg" x="0" y="310" width="1000" height="240"/><image href="euro_cyrillic.svg" x="0" y="620" width="1000" height="240"/></svg>'
    (SVG_DIR / "euro_scripts_grouped.svg").write_text(svg, encoding="utf-8")

def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True); PNG_DIR.mkdir(parents=True, exist_ok=True)
    for code, text in [("005", "5"), ("010", "10"), ("020", "20"), ("050", "50"), ("100", "100"), ("200", "200")]:
        outline_font_svg(text, f"value_{code}_master")
        render_font_png(text, f"value_{code}_master.png")
    outline_font_svg("EURO", "euro_latin")
    render_font_png("EURO", "euro_latin.png")
    render_pixel_assets("ΕΥΡΩ", "euro_greek")
    render_pixel_assets("ЕВРО", "euro_cyrillic")
    render_pixel_assets("€", "euro_sign")
    grouped_png()

if __name__ == "__main__":
    main()

