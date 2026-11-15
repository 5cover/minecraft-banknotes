from project import *
from build_notes import build
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

def main():
 ds=config()['designs'];expected={5:(1800,930),10:(1778,938),20:(1729,936),50:(1700,935),100:(1617,902),200:(1683,902)}
 for ident,d in ds.items():
  path=ROOT/d['export'];im=Image.open(path);assert im.size==tuple(d['size'])==expected[d['value']],ident;assert im.mode=='RGB',ident
  before=hashlib.sha256(path.read_bytes()).hexdigest();build(ident,d);after=hashlib.sha256(path.read_bytes()).hexdigest();assert before==after,f'{ident}: rebuild differs'
 old=TTFont(ROOT/'assets/supplied/inputs/Minecraft.ttf');new=TTFont(ROOT/'assets/approved/Minecraft-Crafting-Europe.ttf')
 for n in old.getGlyphOrder():
  a=RecordingPen();b=RecordingPen();old.getGlyphSet()[n].draw(a);new.getGlyphSet()[n].draw(b);assert a.value==b.value,n;assert old['hmtx'][n]==new['hmtx'][n],n
 for k,v in old.getBestCmap().items():assert new.getBestCmap()[k]==v
 for ch in 'EUROΕΥΡΩЕВРО0123456789':assert ord(ch) in new.getBestCmap()
 print('Verified twelve exact-size RGB notes; every PNG rebuilt identically; source font outlines, metrics and mappings retained; required script glyphs present.')
if __name__=='__main__':main()
