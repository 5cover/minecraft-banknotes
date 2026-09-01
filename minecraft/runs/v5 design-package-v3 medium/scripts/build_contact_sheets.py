#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
CODES=["005","010","020","050","100","200"]

def label(draw,xy,text):
    draw.text(xy,text,fill=(35,35,35),font=ImageFont.load_default())

def sheet(name,items,cols=2,thumb=(600,320)):
    rows=(len(items)+cols-1)//cols; margin=36; label_h=28
    out=Image.new("RGB",(cols*(thumb[0]+margin)+margin,rows*(thumb[1]+label_h+margin)+margin),(226,222,212)); d=ImageDraw.Draw(out)
    for i,(title,path) in enumerate(items):
        col=i%cols; row=i//cols; x=margin+col*(thumb[0]+margin); y=margin+row*(thumb[1]+label_h+margin)
        im=Image.open(path).convert("RGB"); im=ImageOps.contain(im,thumb,Image.Resampling.LANCZOS)
        out.paste(im,(x+(thumb[0]-im.width)//2,y+label_h+(thumb[1]-im.height)//2)); label(d,(x,y),title)
    out.save(ROOT/f"outputs/contacts/{name}.png",optimize=True)

def main():
    (ROOT/"outputs/contacts").mkdir(parents=True,exist_ok=True)
    rectos=[(f"€{int(c)} recto",ROOT/f"outputs/notes/EUR{c}_recto.png") for c in CODES]
    versos=[(f"€{int(c)} verso",ROOT/f"outputs/notes/EUR{c}_verso.png") for c in CODES]
    sheet("rectos_contact",rectos,2); sheet("versos_contact",versos,2)
    paired=[]
    for c in CODES: paired += [(f"€{int(c)} recto",ROOT/f"outputs/notes/EUR{c}_recto.png"),(f"€{int(c)} verso",ROOT/f"outputs/notes/EUR{c}_verso.png")]
    sheet("series_paired_contact",paired,2)

if __name__=="__main__": main()
