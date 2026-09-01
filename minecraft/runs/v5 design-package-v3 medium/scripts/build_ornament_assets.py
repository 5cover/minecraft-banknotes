#!/usr/bin/env python3
from pathlib import Path
import math, random, yaml
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load((ROOT / "layout.yaml").read_text())

def rgba(hexcolor, alpha=255):
    h = hexcolor.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)

def draw_pattern(draw, motif, w, h, ink, accent, seed):
    random.seed(seed)
    if motif == "coal":
        for y in range(24, h, 44):
            draw.line((18, y, w-18, y + random.randint(-7, 7)), fill=ink, width=2)
        for _ in range(230):
            x=random.randrange(w); y=random.choice([random.randrange(42), random.randrange(max(1,h-42),h)])
            draw.rectangle((x,y,x+random.randrange(2,6),y+random.randrange(2,5)), fill=ink)
    elif motif == "redstone":
        for base in (25, h-27):
            for x in range(20, w-80, 130):
                pts=[(x,base),(x+45,base),(x+45,base+(18 if base<100 else -18)),(x+90,base+(18 if base<100 else -18))]
                draw.line(pts, fill=accent, width=3)
                draw.ellipse((x+41,pts[2][1]-4,x+49,pts[2][1]+4), fill=accent)
    elif motif == "lapis":
        for y in list(range(25, 80, 12))+list(range(h-75,h-20,12)):
            draw.line((18,y,w-18,y), fill=ink, width=1)
        for _ in range(120):
            x=random.randrange(w); y=random.choice([random.randrange(70),random.randrange(h-70,h)])
            draw.point((x,y),fill=accent)
    elif motif == "copper":
        for y in (26,40,56,h-58,h-42,h-27):
            draw.line((18,y,w-18,y), fill=ink if y%2 else accent, width=3)
        for x in range(35,w,90):
            draw.line((x,18,x+25,68),fill=accent,width=2); draw.line((x,h-18,x+25,h-68),fill=accent,width=2)
    elif motif == "emerald":
        step=34
        for y in list(range(18,78,step))+list(range(h-75,h-12,step)):
            for x in range(20,w-20,step):
                draw.polygon([(x,y+10),(x+10,y),(x+20,y+10),(x+10,y+20)], outline=ink)
    else:
        for y in (34,h-34):
            for x in range(38,w-38,56):
                draw.polygon([(x,y-9),(x+12,y),(x,y+9),(x-12,y)], outline=accent)
        for r in (12,20,28):
            draw.arc((w/2-r,10-r/2,w/2+r,10+1.5*r),0,180,fill=ink,width=2)

def badge(motif, palette, code):
    s=480; im=Image.new("RGBA",(s,s),(0,0,0,0)); d=ImageDraw.Draw(im)
    paper=rgba(palette["paper"],244); ink=rgba(palette["ink"],210); accent=rgba(palette["accent"],130)
    d.ellipse((16,16,s-16,s-16), fill=paper, outline=ink, width=10)
    d.ellipse((34,34,s-34,s-34), outline=ink, width=3)
    if motif in ("coal","lapis","copper"):
        for k in range(48,430,20): d.line((55,k,425,k-18), fill=accent, width=1)
    elif motif == "redstone":
        for a in range(0,360,30):
            x=240+180*math.cos(math.radians(a)); y=240+180*math.sin(math.radians(a)); d.line((240,240,x,y),fill=accent,width=2)
    elif motif == "emerald":
        for y in range(70,410,36):
            for x in range(70,410,36): d.polygon([(x,y-6),(x+6,y),(x,y+6),(x-6,y)],outline=accent)
    else:
        for r in range(70,205,26): d.ellipse((240-r,240-r,240+r,240+r),outline=accent,width=2)
    d.ellipse((82,82,398,398), fill=rgba(palette["paper"],238), outline=ink, width=4)
    im.save(ROOT / f"generated/badges/EUR{code}_recto_badge.png")

def ornament(code, side, note):
    w,h=note["size"]; motif=note["motif"]; p=note["palette"]
    im=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    paper=rgba(p["paper"],190); ink=rgba(p["ink"],215); dark=rgba(p["dark"],230); accent=rgba(p["accent"],170)
    left=int(w*.18); right=int(w*.81)
    d.rectangle((0,0,left,h),fill=paper); d.rectangle((right,0,w,h),fill=paper)
    d.rectangle((8,8,w-9,h-9),outline=dark,width=8); d.rectangle((20,20,w-21,h-21),outline=ink,width=3)
    d.rectangle((31,31,w-32,h-32),outline=rgba(p["ink"],150),width=1)
    draw_pattern(d,motif,w,h,rgba(p["ink"],115),accent,int(code)+(0 if side=="recto" else 1))
    # calm windows retain institutional legibility
    d.rounded_rectangle((int(w*.825),int(h*.055),int(w*.98),int(h*.94)),radius=18,fill=rgba(p["paper"],145),outline=rgba(p["ink"],120),width=2)
    # left tactile/value field accents
    for i in range(6):
        x=int(w*.027)+i*int(w*.018); y=int(h*.92)
        d.rectangle((x,y,x+int(w*.009),y+int(h*.028)),fill=ink)
    im.save(ROOT / f"generated/ornaments/EUR{code}_{side}_ornament.png")

def main():
    (ROOT/"generated/ornaments").mkdir(parents=True,exist_ok=True); (ROOT/"generated/badges").mkdir(parents=True,exist_ok=True)
    for key,note in CFG["notes"].items():
        code=key[3:]
        badge(note["motif"],note["palette"],code)
        for side in ("recto","verso"): ornament(code,side,note)

if __name__=="__main__": main()

