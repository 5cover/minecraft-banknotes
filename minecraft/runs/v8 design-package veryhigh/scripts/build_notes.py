import argparse
from project import *
def build(ident,d,preview=False):
 size=tuple(d['size']);p=primary(d);a=Image.open(ROOT/d['artwork']).convert('RGBA').resize(size,LANCZOS);f=fixed(d)
 if a.getchannel('A').getextrema()[0]==255:raise ValueError(f'{ident}: artwork is opaque')
 p.alpha_composite(a)
 # Feathered underprint keeps the grouped lettering legible over fine ornament.
 u=config()['script_underprint'];pad=u['padding_pixels'];x,y,w,h=box(d['fixed']['scripts'],size);mask=Image.new('L',size);ImageDraw.Draw(mask).rectangle((x-pad,y-pad,x+w+pad,y+h+pad),fill=u['alpha']);mask=mask.filter(ImageFilter.GaussianBlur(u['feather_pixels']));under=Image.new('RGBA',size,d['paper']);under.putalpha(mask);p.alpha_composite(under)
 p.alpha_composite(f);result=paper_finish(p,d)
 result.save(ROOT/d['export'])
 if preview:
  dest=ROOT/'outputs/layer_previews'/ident;dest.mkdir(parents=True,exist_ok=True)
  primary(d).save(dest/'01-primary.png');a.save(dest/'02-monetary-artwork.png');under.save(dest/'03-script-underprint.png');f.save(dest/'04-fixed-assets.png')
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--design');parser.add_argument('--layers',action='store_true');args=parser.parse_args()
 for ident,d in config()['designs'].items():
  if args.design and ident!=args.design:continue
  build(ident,d,args.layers)
