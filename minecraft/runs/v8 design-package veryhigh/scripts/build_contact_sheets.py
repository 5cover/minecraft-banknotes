from project import *
def main():
 ds=config()['designs'];w=800;h=450;canvas=Image.new('RGB',(w*2+90,h*6+130),'#eeeae0');draw=ImageDraw.Draw(canvas)
 draw.text((30,20),'CRAFTING EUROPE  /  RECTO + VERSO',fill='#263c35')
 for i,(ident,d) in enumerate(ds.items()):
  x=30+(i%2)*(w+30);y=65+(i//2)*h
  im=ImageOps.contain(Image.open(ROOT/d['export']),(w,420),LANCZOS);canvas.paste(im,(x,y+23));draw.text((x,y),ident+'  /  '+str(d['size'][0])+' x '+str(d['size'][1]),fill='#263c35')
 canvas.save(ROOT/'outputs/contacts/Crafting_Europe_contact_sheet.png')
if __name__=='__main__':main()
