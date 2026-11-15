from project import *
def main():
 for ident,d in config()['designs'].items():
  if not (ROOT/d['primary']).exists():continue
  context_design=dict(d);context_design['edge_extension']=d['context_edge_extension'];im=primary(context_design);im.alpha_composite(fixed(d,True))
  if d['side']=='recto':
   cx,cy=d['label_center'];diam=d['label_diameter_height']*im.height;r=diam/2;cx*=im.width;cy*=im.height
   ImageDraw.Draw(im).ellipse((cx-r,cy-r,cx+r,cy+r),outline='#805c8c',width=3)
  im.convert('RGB').save(ROOT/d['context'])
if __name__=='__main__':main()
