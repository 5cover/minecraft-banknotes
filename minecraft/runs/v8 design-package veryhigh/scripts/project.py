from pathlib import Path
from functools import cache
import yaml,subprocess,io,hashlib
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1]
LANCZOS=Image.Resampling.LANCZOS
@cache
def config():return yaml.safe_load((ROOT/'layout.yaml').read_text())
def svg(path,width=None,height=None):
 path=ROOT/path
 dimension=f'--export-width={width}' if width is not None else f'--export-height={height}'
 r=subprocess.run(['inkscape',str(path),'--export-type=png','--export-filename=-',dimension],capture_output=True,check=True)
 return Image.open(io.BytesIO(r.stdout)).convert('RGBA')
def box(b,size):return tuple(round(v*size[i%2]) for i,v in enumerate(b))
def layer(size):return Image.new('RGBA',size)
def put(im,asset,b,contain=True):
 x,y,w,h=box(b,im.size);a=ImageOps.contain(asset,(w,h),LANCZOS) if contain else asset.resize((w,h),LANCZOS);im.alpha_composite(a,(x+(w-a.width)//2,y+(h-a.height)//2))
def primary(d):
 size=tuple(d['size']);out=Image.new('RGBA',size,d['paper']);x,y,w,h=box(d['primary_box'],size)
 plate=ImageOps.fit(Image.open(ROOT/d['primary']).convert('RGBA'),(w,h),method=LANCZOS,centering=tuple(d['crop_center']))
 ex,ey=box(d['edge_extension']+[0,0],size)[:2]
 padded=Image.fromarray(np.pad(np.asarray(plate),((ey,ey),(ex,ex),(0,0)),mode='edge'))
 out.alpha_composite(padded,(x-ex,y-ey));return out
def fixed(d,proxy=False):
 size=tuple(d['size']);im=layer(size);draw=ImageDraw.Draw(im);ink=d['ink']
 for name,b in d['fixed'].items():
  x,y,w,h=box(b,size)
  if proxy:draw.rounded_rectangle((x,y,x+w,y+h),radius=2,fill='#d7c2dd90',outline='#805c8c');continue
  if name in ['value','repeat']:
   target_height=round(config()['value_cap_heights'][name]*size[1]);asset=svg(f"assets/derived/value-{d['value']}.svg",height=target_height)
  elif name=='scripts':asset=svg('assets/derived/euro-scripts.svg',w)
  elif name=='flag':asset=svg('assets/supplied/europe-flag.svg',w);asset.putalpha(asset.getchannel('A').point(lambda a:round(a*.92)))
  elif name=='map':asset=svg('assets/supplied/europe-map.svg',w)
  else:continue
  if name!='flag':
   alpha=asset.getchannel('A');asset=Image.new('RGBA',asset.size,ink);asset.putalpha(alpha.point(lambda a:round(a*(.70 if name=='map' else 1))))
  if name in ['value','repeat']:
   if asset.width>w or asset.height>h:raise ValueError(f"{d['value']} {name} does not fit its layout box")
   im.alpha_composite(asset,(x+(w-asset.width)//2,y))
  else:put(im,asset,b)
 # Recto insert remains separate from the generated shell.
 if d['side']=='recto':
  b=d['ore_box'];x,y,w,h=box(b,size)
  if proxy:draw.polygon([(x+w//2,y),(x+w,y+h//4),(x+w,y+h*3//4),(x+w//2,y+h),(x,y+h*3//4),(x,y+h//4)],fill='#c8b3d490',outline='#805c8c')
  else:
   a=Image.open(ROOT/d['ore']).convert('RGBA');a=a.crop(a.getbbox());put(im,a,b)
 if not proxy:
  # Signature placeholder and unnumbered serial reservation; neither implies issuance.
  x,y,w,h=box(d['signature_box'],size);draw.line((x,y+h,x+w,y+h),fill=ink,width=1)
  for edge in [.022,.975]:
   for i in range(d['tactile_groups']):
    yy=round(size[1]*(.37+i*.035));xx=round(size[0]*edge);draw.line((xx,yy,xx,yy+round(size[1]*.020)),fill=ink,width=3)
 return im
def paper_finish(im,d):
 a=np.asarray(im.convert('RGB')).astype(np.float32);h,w=a.shape[:2];rng=np.random.default_rng(d['texture_seed']);noise=rng.normal(0,.70,(h,w,1));a=np.clip(a+noise,0,255).astype('uint8');return Image.fromarray(a)
