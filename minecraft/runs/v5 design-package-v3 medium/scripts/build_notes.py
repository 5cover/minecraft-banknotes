#!/usr/bin/env python3
from pathlib import Path
import math, random, xml.etree.ElementTree as ET, yaml
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
from fontTools.svgLib.path import parse_path
from fontTools.pens.basePen import BasePen

ROOT=Path(__file__).resolve().parents[1]
CFG=yaml.safe_load((ROOT/"layout.yaml").read_text())

def box(layout,w,h):
    return (int(w*layout["x_pct"]/100),int(h*layout["y_pct"]/100),max(1,int(w*layout["width_pct"]/100)),max(1,int(h*layout["height_pct"]/100)))

def fit(im,size,cover=True):
    return ImageOps.fit(im.convert("RGB"),size,Image.Resampling.LANCZOS,centering=(.5,.5)) if cover else ImageOps.contain(im,size,Image.Resampling.LANCZOS)

def tint_alpha(im,color):
    im=im.convert("RGBA"); alpha=im.getchannel("A")
    rgb=tuple(int(color[i:i+2],16) for i in (1,3,5))
    out=Image.new("RGBA",im.size,rgb+(255,)); out.putalpha(alpha); return out

class FlatPen(BasePen):
    def __init__(self,glyphSet=None,steps=9): super().__init__(glyphSet); self.paths=[]; self.path=[]; self.steps=steps
    def _moveTo(self,p):
        if self.path: self.paths.append(self.path)
        self.path=[p]
    def _lineTo(self,p): self.path.append(p)
    def _curveToOne(self,p1,p2,p3):
        p0=self.path[-1]
        for i in range(1,self.steps+1):
            t=i/self.steps; u=1-t
            self.path.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    def _qCurveToOne(self,p1,p2):
        p0=self.path[-1]
        for i in range(1,self.steps+1):
            t=i/self.steps; u=1-t
            self.path.append((u*u*p0[0]+2*u*t*p1[0]+t*t*p2[0],u*u*p0[1]+2*u*t*p1[1]+t*t*p2[1]))
    def _closePath(self):
        if self.path: self.paths.append(self.path); self.path=[]
    def _endPath(self): self._closePath()

def map_asset(size,color):
    svg=ROOT/"assets/maps/europe_map_project.svg"; root=ET.parse(svg).getroot()
    vb=[float(x) for x in root.attrib.get("viewBox","144 110 670 540").split()]
    pad=6; out=Image.new("RGBA",size,(0,0,0,0)); d=ImageDraw.Draw(out)
    scale=min((size[0]-2*pad)/vb[2],(size[1]-2*pad)/vb[3]); ox=(size[0]-vb[2]*scale)/2-vb[0]*scale; oy=(size[1]-vb[3]*scale)/2-vb[1]*scale
    for el in root.iter():
        if el.tag.endswith("path") and el.attrib.get("d"):
            pen=FlatPen(); parse_path(el.attrib["d"],pen)
            for p in pen.paths:
                pts=[(ox+x*scale,oy+y*scale) for x,y in p]
                if len(pts)>2: d.polygon(pts,fill=color)
    return out

def flag_asset(size,palette):
    """Rasterize the supplied official flag SVG's exact star path and placements."""
    root=ET.parse(ROOT/"assets/flags/eu_flag_master.svg").getroot()
    star_d=None
    for el in root.iter():
        if el.tag.endswith("path") and el.attrib.get("id")=="a": star_d=el.attrib["d"]; break
    pen=FlatPen(steps=14); parse_path(star_d,pen)
    stars=[(0,0),(0,-400),(-100,-26.795),(-173.205,-100),(-200,-200),(-173.205,-300),(-100,-373.205),
           (100,-26.795),(173.205,-100),(200,-200),(173.205,-300),(100,-373.205)]
    w,h=size; im=Image.new("RGBA",size,(0,51,153,245)); d=ImageDraw.Draw(im)
    sx=w/900; sy=h/600
    for tx,ty in stars:
        for p in pen.paths:
            pts=[((450+tx+x)*sx,(300+ty+y)*sy) for x,y in p]
            if len(pts)>2: d.polygon(pts,fill=(255,204,0,250))
    overlay=Image.new("RGBA",size,tuple(int(palette[i:i+2],16) for i in (1,3,5))+(35,)); return Image.alpha_composite(im,overlay)

def print_overlay(size,seed):
    random.seed(seed); w,h=size; im=Image.new("RGBA",size,(0,0,0,0)); d=ImageDraw.Draw(im)
    for _ in range((w*h)//480):
        x=random.randrange(w); y=random.randrange(h); a=random.randrange(3,13); c=35 if random.random()<.55 else 245
        d.point((x,y),fill=(c,c,c,a))
    return im

def place(canvas,asset,b):
    x,y,w,h=b; a=ImageOps.contain(asset.convert("RGBA"),(w,h),Image.Resampling.LANCZOS); canvas.alpha_composite(a,(x+(w-a.width)//2,y+(h-a.height)//2))

def build(key,note,side):
    code=key[3:]; w,h=note["size"]; L=CFG["common_layout"]; p=note["palette"]
    scene=Image.open(ROOT/f"generated/scenes/EUR{code}_{side}_scene.png")
    scene=fit(scene,(w,h)); scene=ImageEnhance.Color(scene).enhance(.82); scene=ImageEnhance.Contrast(scene).enhance(.96)
    canvas=scene.convert("RGBA")
    stable=Image.new("RGBA",(w,h),(0,0,0,0))
    if side=="recto":
        bx=box(L["badge"],w,h); badge=Image.open(ROOT/f"generated/badges/EUR{code}_recto_badge.png"); place(canvas,badge,bx)
        place(stable,badge,bx)
        ore=Image.open(ROOT/f"assets/ore_blocks/ore_{note['motif']}_iso.webp").convert("RGBA"); place(canvas,ore,box(L["ore"],w,h))
        place(stable,ore,box(L["ore"],w,h))
    canvas.alpha_composite(Image.open(ROOT/f"generated/ornaments/EUR{code}_{side}_ornament.png").convert("RGBA"))
    val=Image.open(ROOT/f"assets/type_png/value_{code}_master.png"); val=tint_alpha(val,p["dark"]); place(canvas,val,box(L["main_value"],w,h))
    place(stable,val,box(L["main_value"],w,h))
    place(canvas,val,box(L["secondary_value"],w,h))
    place(stable,val,box(L["secondary_value"],w,h))
    scripts=tint_alpha(Image.open(ROOT/"assets/type_png/euro_scripts_grouped.png"),p["dark"]); place(canvas,scripts,box(L["euro_scripts"],w,h))
    place(stable,scripts,box(L["euro_scripts"],w,h))
    flag=flag_asset((300,200),p["ink"]); place(canvas,flag,box(L["eu_flag"],w,h)); place(stable,flag,box(L["eu_flag"],w,h))
    mb=box(L["europe_map"],w,h); m=map_asset((600,600),tuple(int(p["ink"][i:i+2],16) for i in (1,3,5))+(205,)); place(canvas,m,mb); place(stable,m,mb)
    line_color=tuple(int(p["dark"][i:i+2],16) for i in (1,3,5))+(180,)
    d=ImageDraw.Draw(canvas); sd=ImageDraw.Draw(stable); sx,sy,sw,sh=box(L["signature"],w,h)
    d.line((sx,sy+sh//2,sx+sw,sy+sh//2),fill=line_color,width=max(1,h//450)); sd.line((sx,sy+sh//2,sx+sw,sy+sh//2),fill=line_color,width=max(1,h//450))
    canvas.alpha_composite(print_overlay((w,h),int(code)+(0 if side=="recto" else 1)))
    out=ROOT/f"outputs/notes/EUR{code}_{side}.png"; canvas.convert("RGB").save(out,optimize=True)
    stable.save(ROOT/f"outputs/layer_previews/EUR{code}_{side}_stable_layers.png",optimize=True)
    return out

def main():
    (ROOT/"outputs/notes").mkdir(parents=True,exist_ok=True)
    (ROOT/"outputs/layer_previews").mkdir(parents=True,exist_ok=True)
    for key,note in CFG["notes"].items():
        for side in ("recto","verso"): print(build(key,note,side).relative_to(ROOT))

if __name__=="__main__": main()
