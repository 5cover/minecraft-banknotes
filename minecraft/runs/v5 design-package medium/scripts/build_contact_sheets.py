#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/contacts'; OUT.mkdir(parents=True,exist_ok=True)
CODES=['EUR005','EUR010','EUR020','EUR050','EUR100','EUR200']

def sheet(paths,title,cols=2,gray=False):
    thumb_w=760; rows=(len(paths)+cols-1)//cols; cell_h=430
    im=Image.new('RGB',(cols*thumb_w+60,rows*cell_h+100),'#e9e4d7'); d=ImageDraw.Draw(im)
    d.text((30,25),title,fill='#242020')
    for i,p in enumerate(paths):
        src=Image.open(p).convert('RGB')
        if gray: src=ImageOps.grayscale(src).convert('RGB')
        src.thumbnail((thumb_w-40,cell_h-70),Image.Resampling.LANCZOS)
        x=30+(i%cols)*thumb_w+(thumb_w-src.width)//2; y=75+(i//cols)*cell_h
        im.paste(src,(x,y)); d.text((x,y+src.height+8),p.stem,fill='#242020')
    return im

rectos=[ROOT/f'outputs/notes/{c}_recto.png' for c in CODES]
versos=[ROOT/f'outputs/notes/{c}_verso.png' for c in CODES]
sheet(rectos,'CRAFTING EUROPE — RECTO SERIES').save(OUT/'recto_contact.png')
sheet(versos,'CRAFTING EUROPE — VERSO SERIES').save(OUT/'verso_contact.png')
paired=[p for pair in zip(rectos,versos) for p in pair]
sheet(paired,'CRAFTING EUROPE — PAIRED SERIES').save(OUT/'paired_contact.png')
sheet(paired,'CRAFTING EUROPE — GRAYSCALE CHECK',gray=True).save(OUT/'grayscale_contact.png')
print('Built four contact sheets.')
