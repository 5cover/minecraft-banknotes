from pathlib import Path
import argparse
import numpy as np
from PIL import Image,ImageOps
from build_notes import ROOT,read_layout,colorize,save_png

def isolate(key):
    note=read_layout()['notes'][key]
    src=Image.open(ROOT/f'generated/monetary_artwork/{key}_source.png').convert('RGBA')
    darkness=np.asarray(ImageOps.invert(ImageOps.grayscale(src)),dtype=float)/255
    alpha=np.asarray(src.getchannel('A'),dtype=float)/255
    mask=Image.fromarray(np.round(np.clip(np.clip((darkness-.015)/.985,0,1)*alpha*note['artwork_density_gain'],0,1)*255).astype('uint8'))
    out=colorize(mask,note['ink'],note['artwork_opacity'])
    save_png(out,ROOT/note['artwork'])
    print(key,'alpha range',out.getchannel('A').getextrema())
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('design',nargs='*');args=p.parse_args()
    for key in args.design or read_layout()['notes']: isolate(key)
