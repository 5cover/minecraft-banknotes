from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
from build_notes import read_layout,ROOT,save_png

def main():
    notes=read_layout()['notes']
    sheet=Image.new('RGB',(1600,2820),'#f2f0e9')
    d=ImageDraw.Draw(sheet)
    font_path=ROOT/'assets/supplied/DejaVuSans.ttf'
    title=ImageFont.truetype(str(font_path),42)
    label=ImageFont.truetype(str(font_path),20)
    d.text((40,25),'LIVING SYSTEMS',font=title,fill='#283331')
    d.text((42,84),'Six interdependent civic systems • recto / verso • Version 5',font=label,fill='#59615b')
    themes=['Infrastructure','Communication','Mobility','Interpretation','Environment','Future']
    for i,(key,n) in enumerate(notes.items()):
        row,col=divmod(i,2)
        x=40+col*790; y=135+row*442
        d.text((x,y),f"€{n['denomination']}  /  {themes[row]}  /  {n['side']}",font=label,fill='#283331')
        im=Image.open(ROOT/'outputs/notes'/n['filename'])
        im=ImageOps.contain(im,(730,395),Image.Resampling.LANCZOS)
        sheet.paste(im,(x,y+34))
    folder=ROOT/'outputs/contacts';folder.mkdir(parents=True,exist_ok=True)
    save_png(sheet,folder/'Living_Systems_contact_sheet.png')
    print('Contact sheet built from final exports.')
if __name__=='__main__': main()
