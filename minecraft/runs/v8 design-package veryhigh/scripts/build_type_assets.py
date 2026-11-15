from pathlib import Path
from copy import deepcopy
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image, ImageFont, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def main():
 f=TTFont(ROOT/'assets/supplied/inputs/Minecraft.ttf',recalcTimestamp=False); cmap=f.getBestCmap()
 # Script-specific encoded glyphs use the source's exact matching capital designs.
 mapping={'Ε':'E','Υ':'Y','Ρ':'P','Е':'E','В':'B','Р':'P','О':'O'}
 for ch,src in mapping.items():
  name='uni%04X'%ord(ch); f['glyf'][name]=deepcopy(f['glyf'][cmap[ord(src)]]);f['hmtx'][name]=f['hmtx'][cmap[ord(src)]]
  f.setGlyphOrder(f.getGlyphOrder()+[name] if name not in f.getGlyphOrder() else f.getGlyphOrder())
  for t in f['cmap'].tables:
   if t.isUnicode():t.cmap[ord(ch)]=name
 # Omega: 12 rows, 12 columns, 64-unit cells and two-cell stems.
 omega=['001111111100','011111111110','110000000011','110000000011','110000000011','110000000011','110000000011','110000000011','011000000110','001100001100','111110011111','111110011111']
 pen=TTGlyphPen(None)
 for row,line in enumerate(omega):
  for col,cell in enumerate(line):
   if cell=='1':
    x=col*64;y=(11-row)*64;pen.moveTo((x,y));pen.lineTo((x,y+64));pen.lineTo((x+64,y+64));pen.lineTo((x+64,y));pen.closePath()
 name='uni03A9';f['glyf'][name]=pen.glyph();f['hmtx'][name]=(832,0)
 if name not in f.getGlyphOrder():f.setGlyphOrder(f.getGlyphOrder()+[name])
 for t in f['cmap'].tables:
  if t.isUnicode():t.cmap[0x3A9]=name
 for nid,value in [(1,'Minecraft Crafting Europe'),(3,'Minecraft-CraftingEurope-Medium-1'),(4,'Minecraft Crafting Europe Medium'),(6,'MinecraftCraftingEurope-Medium')]:
  f['name'].setName(value,nid,3,1,0x409);f['name'].setName(value,nid,1,0,0)
 f['OS/2'].recalcUnicodeRanges(f)
 out=ROOT/'assets/approved/Minecraft-Crafting-Europe.ttf';f.save(out)
 f=TTFont(out);gs=f.getGlyphSet();c=f.getBestCmap()
 def svg(text,path,group=False):
  lines=text.split('\n');parts=[];width=0
  for i,line in enumerate(lines):
   xpos=0;paths=[]
   for ch in line:
    n=c[ord(ch)];p=SVGPathPen(gs);gs[n].draw(p);paths.append(f'<path transform="translate({xpos} 768) scale(1 -1)" d="{p.getCommands()}"/>');xpos+=f['hmtx'][n][0]
   # All script lines have the same cap height. Keep natural widths; centre as one group.
   width=max(width,xpos-64);parts.append((xpos-64,paths))
  body=''.join(f'<g transform="translate({(width-w)/2} {i*1000})">'+''.join(paths)+'</g>' for i,(w,paths) in enumerate(parts))
  (ROOT/path).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {768+(len(lines)-1)*1000}">{body}</svg>')
 for n in [5,10,20,50,100,200]:svg(str(n),f'assets/derived/value-{n}.svg')
 svg('EURO\nΕΥΡΩ\nЕВРО','assets/derived/euro-scripts.svg')
 image=Image.new('RGB',(1300,610),'#eee9dd');d=ImageDraw.Draw(image);font=ImageFont.truetype(str(out),82)
 for y,t in zip([35,180,325],['EURO 0123456789','ΕΥΡΩ  Ε Υ Ρ Ω','ЕВРО  Е В Р О']):d.text((45,y),t,font=font,fill='#27352f')
 image.save(ROOT/'outputs/contacts/font-specimen.png')
 print(out)
if __name__=='__main__':main()
