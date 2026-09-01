#!/usr/bin/env python3
import argparse, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(name):
    with open(ROOT/name, encoding='utf-8') as f: return yaml.safe_load(f)

def rgba(hex_value, alpha=255):
    h=hex_value.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(alpha,)

def box_px(spec,w,h):
    return (round(spec['x']*w), round(spec['y']*h), round((spec['x']+spec['w'])*w), round((spec['y']+spec['h'])*h))

def cover(img,w,h):
    s=max(w/img.width,h/img.height); nw,nh=round(img.width*s),round(img.height*s)
    img=img.resize((nw,nh),Image.Resampling.LANCZOS)
    return img.crop(((nw-w)//2,(nh-h)//2,(nw-w)//2+w,(nh-h)//2+h))

def tint_white_asset(img, color):
    a=img.getchannel('A')
    out=Image.new('RGBA',img.size,color)
    out.putalpha(a); return out

def fit_asset(path, target, color=None):
    im=Image.open(path).convert('RGBA')
    if color: im=tint_white_asset(im,color)
    x0,y0,x1,y1=target; scale=min((x1-x0)/im.width,(y1-y0)/im.height)
    im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
    return im,(x0+(x1-x0-im.width)//2,y0+(y1-y0-im.height)//2)

def rasterize_svg(src, dst, w, h):
    subprocess.run([
        'node', str(ROOT/'scripts/rasterize_svg.js'), str(src), str(dst), str(w), str(h)
    ], check=True)

def pattern(draw, pattern, w, h, color):
    step=max(18,h//28); c=rgba(color,70)
    if pattern in ('strata','manuscript'):
        for y in range(step, h, step): draw.line((0,y,w,y),fill=c,width=1 if pattern=='manuscript' else 2)
    elif pattern=='signal':
        for y in range(step, h, step*2):
            draw.line((0,y,w*.25,y,w*.31,y+step,w*.46,y+step),fill=c,width=2)
    elif pattern=='conductive':
        for x in range(0,w,step): draw.line((x,0,x+h//5,h),fill=c,width=2)
    elif pattern=='lattice':
        for x in range(-h,w,step*2):
            draw.line((x,0,x+h,h),fill=c,width=1); draw.line((x+h,0,x,h),fill=c,width=1)
    elif pattern=='rings':
        for r in range(step,min(w,h),step): draw.ellipse((w//2-r,h//2-r,w//2+r,h//2+r),outline=c,width=2)

def frame_layer(code, side, w, h, pal):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    dark,dom,light=pal['dark'],pal['dominant'],pal['light']
    left=int(w*.245); right=int(w*.715)
    d.rectangle((0,0,left,h),fill=rgba(light,168)); d.rectangle((right,0,w,h),fill=rgba(light,184))
    d.rectangle((0,0,w,h),outline=rgba(dark,245),width=max(7,h//75))
    m=max(18,h//35); d.rounded_rectangle((m,m,w-m,h-m),radius=h//48,outline=rgba(dom,230),width=max(3,h//170))
    d.rounded_rectangle((m*2,m*2,w-m*2,h-m*2),radius=h//58,outline=rgba(dark,165),width=2)
    pattern(d,pal['pattern'],w,h,dom)
    d.rectangle((left-4,0,left+4,h),fill=rgba(dark,90)); d.rectangle((right-4,0,right+4,h),fill=rgba(dark,90))
    # tactile placeholder groups
    for i in range(int(code[-1])%4+2): d.rounded_rectangle((int(w*.055)+i*13,int(h*.665),int(w*.061)+i*13,int(h*.72)),radius=3,fill=rgba(dark,185))
    return im

def label_layer(w,h,pal,common):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    dia=int(common['ore_label']['diameter_h']*h); cx=int(common['ore_label']['cx']*w); cy=int(common['ore_label']['cy']*h)
    b=(cx-dia//2,cy-dia//2,cx+dia//2,cy+dia//2)
    d.ellipse(b,fill=rgba(pal['light'],242),outline=rgba(pal['dark'],235),width=max(6,h//110))
    inset=max(13,h//55); d.ellipse((b[0]+inset,b[1]+inset,b[2]-inset,b[3]-inset),outline=rgba(pal['dominant'],190),width=3)
    # clipped-looking motif remains inside inner disk
    for i in range(18):
        a=2*math.pi*i/18; r=dia*.42
        x=cx+math.cos(a)*r; y=cy+math.sin(a)*r
        d.ellipse((x-2,y-2,x+2,y+2),fill=rgba(pal['dominant'],110))
    return im,(cx,cy,dia)

def paste_asset(canvas,path,spec,w,h,color=None):
    im,pos=fit_asset(path,box_px(spec,w,h),color); canvas.alpha_composite(im,pos)

def text_layer(path,spec,w,h,color):
    layer=Image.new('RGBA',(w,h),(0,0,0,0)); paste_asset(layer,path,spec,w,h,color); return layer

def build_one(code, meta, side, layout, palettes, previews):
    w,h=meta['width'],meta['height']; pal=palettes['notes'][code]; common=layout['common']
    scene_path=ROOT/f'generated/scenes/{code}_{side}_scene.png'
    scene=cover(Image.open(scene_path).convert('RGB'),w,h).convert('RGBA')
    scene=ImageEnhance.Color(scene).enhance(.80); scene=ImageEnhance.Contrast(scene).enhance(.96)
    scene=Image.blend(scene,Image.new('RGBA',(w,h),rgba(palettes['paper'])),.08)
    layers={'scene':scene}
    if side=='recto':
        label,geom=label_layer(w,h,pal,common); layers['ore_label']=label
        cx,cy,dia=geom; size=int(common['ore_block']['size_h']*h)
        ore=Image.open(ROOT/f'assets/ore_blocks/{meta["ore"]}.webp').convert('RGBA')
        ore.thumbnail((size,size),Image.Resampling.LANCZOS)
        ol=Image.new('RGBA',(w,h),(0,0,0,0)); ol.alpha_composite(ore,(cx-ore.width//2,cy-ore.height//2)); layers['ore_block']=ol
    layers['frame']=frame_layer(code,side,w,h,pal)
    value=str(meta['value'])
    layers['main_value']=text_layer(ROOT/f'assets/type_png/{value}_master.png',common['main_value'],w,h,rgba(pal['dark']))
    layers['secondary_value']=text_layer(ROOT/f'assets/type_png/{value}_master.png',common['secondary_value'],w,h,rgba(pal['dark'],210))
    scripts=Image.new('RGBA',(w,h),(0,0,0,0)); sb=box_px(common['euro_scripts'],w,h); row=(sb[3]-sb[1])//3
    for i,name in enumerate(['euro','euro_greek','euro_cyrillic']):
        spec={'x':sb[0]/w,'y':(sb[1]+i*row)/h,'w':(sb[2]-sb[0])/w,'h':(row*.72)/h}
        paste_asset(scripts,ROOT/f'assets/type_png/{name}_master.png',spec,w,h,rgba(pal['dark']))
    layers['euro_scripts']=scripts
    flag_tmp=ROOT/'assets/flags/eu_flag_master.png'; map_tmp=ROOT/'assets/maps/europe_map_master.png'
    if not flag_tmp.exists(): rasterize_svg(ROOT/'assets/flags/eu_flag_master.svg',flag_tmp,900,600)
    if not map_tmp.exists(): rasterize_svg(ROOT/'assets/maps/europe_map_master.svg',map_tmp,670,540)
    flag=Image.new('RGBA',(w,h),(0,0,0,0)); paste_asset(flag,flag_tmp,common['flag'],w,h); layers['flag']=flag
    mp=Image.open(map_tmp).convert('RGBA'); alpha=mp.getchannel('A'); colored=Image.new('RGBA',mp.size,rgba(pal['dark'],150)); colored.putalpha(alpha.point(lambda a:int(a*.62)))
    maplayer=Image.new('RGBA',(w,h),(0,0,0,0)); target=box_px(common['map'],w,h); scale=min((target[2]-target[0])/colored.width,(target[3]-target[1])/colored.height); colored=colored.resize((round(colored.width*scale),round(colored.height*scale)),Image.Resampling.LANCZOS); maplayer.alpha_composite(colored,(target[0]+(target[2]-target[0]-colored.width)//2,target[1]+(target[3]-target[1]-colored.height)//2)); layers['map']=maplayer
    sig=Image.new('RGBA',(w,h),(0,0,0,0)); sd=ImageDraw.Draw(sig); x0,y0,x1,y1=box_px(common['signature'],w,h); sd.line((x0,y1-3,x1,y1-3),fill=rgba(pal['dark'],150),width=2); sd.arc((x0,y0,x0+(x1-x0)//2,y1),180,350,fill=rgba(pal['dark'],180),width=2); layers['signature']=sig
    serial=Image.new('RGBA',(w,h),(0,0,0,0)); serial_font=ImageFont.truetype(str(ROOT/'assets/font/Minecraft.ttf'),max(18,h//42))
    sd=ImageDraw.Draw(serial); x0,y0,x1,y1=box_px(common['serial'],w,h); sd.text((x0,y0),f'CE {code[-3:]} 2026 000001',font=serial_font,fill=rgba(pal['dark'],150),stroke_width=0); layers['serial']=serial
    overlay=Image.new('RGBA',(w,h),(0,0,0,0)); od=ImageDraw.Draw(overlay)
    for y in range(0,h,7): od.line((0,y,w,y),fill=(255,255,255,10),width=1)
    layers['print_overlay']=overlay
    out=Image.new('RGBA',(w,h),(0,0,0,0))
    for name in layout['z_order'][side]: out=Image.alpha_composite(out,layers[name])
    final_path=ROOT/f'outputs/notes/{code}_{side}.png'; temp_path=final_path.with_suffix('.tmp.png')
    out.convert('RGB').save(temp_path,quality=96)
    with Image.open(temp_path) as check:
        check.load()
        if check.size != (w,h): raise RuntimeError(f'export size mismatch for {code}_{side}: {check.size}')
    temp_path.replace(final_path)
    (ROOT/'generated/frames').mkdir(parents=True,exist_ok=True); layers['frame'].save(ROOT/f'generated/frames/{code}_{side}_frame.png')
    if side=='recto':
        (ROOT/'generated/ore_labels').mkdir(parents=True,exist_ok=True); layers['ore_label'].save(ROOT/f'generated/ore_labels/{code}_recto_label.png')
    if previews:
        d=ROOT/'outputs/layer_previews'; d.mkdir(parents=True,exist_ok=True)
        for name,im in layers.items(): im.save(d/f'{code}_{side}_{name}.png')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--layer-previews',action='store_true'); args=ap.parse_args()
    layout=load_yaml('layout.yaml'); palettes=load_yaml('palette.yaml')
    (ROOT/'outputs/notes').mkdir(parents=True,exist_ok=True)
    for code,meta in layout['notes'].items():
        for side in ('recto','verso'): build_one(code,meta,side,layout,palettes,args.layer_previews)
    print('Built 12 exact-size notes.')

if __name__=='__main__': main()
