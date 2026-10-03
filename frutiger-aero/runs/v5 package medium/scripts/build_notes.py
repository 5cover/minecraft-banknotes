from pathlib import Path
import argparse, math, io, os
import yaml
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

def save_png(im, path):
    buf=io.BytesIO()
    im.save(buf,format='PNG')
    data=buf.getvalue()
    tmp=path.with_suffix('.tmp')
    with open(tmp,'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(path)
    with Image.open(path) as check:
        check.verify()

def read_layout():
    return yaml.safe_load((ROOT / 'layout.yaml').read_text())

def smooth(a):
    a = np.clip(a, 0, 1)
    return a * a * (3 - 2 * a)

def box_px(box, size):
    w, h = size
    return tuple(round(v * (w if i % 2 == 0 else h) / 100) for i, v in enumerate(box))

def colorize(mask, color, opacity=1):
    out = Image.new('RGBA', mask.size, color)
    out.putalpha(mask.point(lambda p: round(p * opacity)))
    return out

def place(out, asset, box, align='center'):
    x0,y0,x1,y1 = box_px(box,out.size)
    im = ImageOps.contain(asset,(x1-x0,y1-y0),Image.Resampling.LANCZOS)
    x = x0 if align=='left' else x1-im.width if align=='right' else x0+(x1-x0-im.width)//2
    out.alpha_composite(im,(x,y0+(y1-y0-im.height)//2))

def primary_layer(note):
    size = tuple(note['size'])
    source = Image.open(ROOT / note['primary']).convert('RGB')
    crop = note['crop']
    source = source.crop(tuple(round(v * (source.width if i%2==0 else source.height)) for i,v in enumerate(crop)))
    source = ImageOps.fit(source,size,Image.Resampling.LANCZOS,centering=tuple(note['centering']))
    # Palette translation changes ink hue, retaining the selected image's luminosity and geometry.
    lum = ImageOps.grayscale(source)
    return ImageOps.colorize(lum,note['shadow'],note['paper'],mid=note['mid']).convert('RGBA')

def quiet_layer(note):
    w,h = note['size']
    x=np.linspace(0,100,w)
    low,high=note['quiet_fade']
    field = smooth((x-low)/(high-low)) if note['side']=='recto' else 1-smooth((x-low)/(high-low))
    mask=Image.fromarray(np.repeat((field*note['quiet_opacity']*255).astype('uint8')[None,:],h,axis=0))
    return colorize(mask,note['paper'])

def fixed_layer(note, layout, proxies=False):
    out=Image.new('RGBA',tuple(note['size']))
    masks=layout['masks'][note['side']]
    if proxies:
        # Real-size silhouettes communicate occupancy; no planning grid or panel outlines.
        value=Image.open(ROOT/f"assets/approved/value_{note['denomination']}.png")
        place(out,colorize(value,'#575757',.6),masks['value'],note['alignment'])
        type_im=Image.open(ROOT/'assets/approved/currency_group.png')
        place(out,colorize(type_im,'#575757',.5),masks['type'])
        icon='european_flag.png' if note['side']=='recto' else 'europe_mask.png'
        im=Image.open(ROOT/'assets/approved'/icon)
        mask=im.getchannel('A') if im.mode=='RGBA' else im
        place(out,colorize(mask,'#777777',.4),masks['flag' if note['side']=='recto' else 'map'])
        return out
    value=Image.open(ROOT/f"assets/approved/value_{note['denomination']}.png")
    place(out,colorize(value,note['ink']),masks['value'],note['alignment'])
    place(out,colorize(Image.open(ROOT/'assets/approved/currency_group.png'),note['ink']),masks['type'])
    if note['side']=='recto':
        place(out,Image.open(ROOT/'assets/approved/european_flag.png'),masks['flag'])
    else:
        mask=Image.open(ROOT/'assets/approved/europe_mask.png')
        map_im=colorize(mask,note['ink'],.55)
        # Denomination-specific interior treatment always uses the same silhouette mask.
        pat=Image.new('L',mask.size)
        d=ImageDraw.Draw(pat)
        k=note['denomination']
        if k==5:
            for x in range(0,1200,70): d.line((x,0,x,1000),fill=180,width=4)
            for y in range(0,1000,70): d.line((0,y,1200,y),fill=180,width=4)
        elif k in [10,50,200]:
            for r in range(80,1500,90): d.arc((450-r,300-r//2,450+r,300+r//2),0,355,fill=210,width=5)
        elif k==20:
            for q in range(-400,1300,110): d.line((q,1000,q+650,0),fill=210,width=5)
        else:
            for j in range(20):
                points=[(x, int(j*65+25*math.sin(x/130+j))) for x in range(0,1200,4)]
                d.line(points,fill=210,width=4)
        pat=Image.fromarray((np.asarray(pat,dtype=float)*np.asarray(mask)/255).astype('uint8'))
        map_im=Image.alpha_composite(map_im,colorize(pat,note['paper'],.7))
        place(out,map_im,masks['map'])
    return out

def artwork_layer(note):
    im=Image.open(ROOT/note['artwork']).convert('RGBA')
    if im.getchannel('A').getextrema()==(255,255):
        raise ValueError(f"Artwork is opaque, not isolated: {note['artwork']}")
    return im.resize(tuple(note['size']),Image.Resampling.LANCZOS)

def build(design=None, contexts=False, layers=False):
    layout=read_layout()
    for key,note in layout['notes'].items():
        if design and key!=design: continue
        if contexts and not (ROOT/note['primary']).exists(): continue
        named={'primary':primary_layer(note),'quiet':quiet_layer(note)}
        if not contexts: named['monetary_artwork']=artwork_layer(note)
        named['fixed']=fixed_layer(note,layout,proxies=contexts)
        out=Image.new('RGBA',tuple(note['size']))
        for name,layer in named.items():
            out=Image.alpha_composite(out,layer)
            if layers:
                folder=ROOT/'outputs/layer_previews'/key
                folder.mkdir(parents=True,exist_ok=True)
                save_png(layer,folder/f'{name}.png')
        dest=ROOT/f'generated/contexts/{key}.png' if contexts else ROOT/'outputs/notes'/note['filename']
        dest.parent.mkdir(parents=True,exist_ok=True)
        save_png(out.convert('RGB'),dest)
        if Image.open(dest).size != tuple(note['size']): raise ValueError(f'Wrong output size: {dest}')
        print(dest.relative_to(ROOT))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--design')
    p.add_argument('--contexts',action='store_true')
    p.add_argument('--layers',action='store_true')
    args=p.parse_args()
    build(args.design,args.contexts,args.layers)
