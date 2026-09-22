from PIL import Image,ImageDraw,ImageFont
from build_notes import ROOT,save_png

def main():
    im=Image.new('RGB',(1700,935),'#fff4df')
    d=ImageDraw.Draw(im)
    font=ImageFont.truetype(str(ROOT/'assets/supplied/DejaVuSans.ttf'),16)
    d.polygon([(510,100),(1640,100),(1690,830),(470,830)],fill='#e5c49b')
    def chair(x,y,label):
        d.rectangle((x-21,y-13,x+21,y+17),fill='#9a7550',outline='#4b341e',width=2)
        d.rectangle((x-20,y-27,x+20,y-15),fill='#6f4e30')
        d.line((x-18,y+17,x-22,y+29),fill='#4b341e',width=3)
        d.line((x+18,y+17,x+22,y+29),fill='#4b341e',width=3)
        d.text((x-17,y-5),label,font=font,fill='white')
    for i,x in enumerate([1000,1120,1240,1360]):
        d.ellipse((x-27,95,x+27,135),fill='#b1844b',outline='#4b341e',width=3)
        d.text((x-8,103),str(i+1),font=font,fill='white')
    for i,x in enumerate([900,1080,1260,1440]): chair(x,225,'B'+str(i+1))
    for i,x in enumerate([680,850,1020,1190,1360,1530]): chair(x,330,'W'+str(i+1))
    for row in range(4):
        for col,x in enumerate([650,830,1010,1190,1370,1550]):
            y=445+row*90+int(25*(1-((col-2.5)/2.5)**2))
            chair(x,y,str(row*6+col+1))
            if col%2==0:
                sx=x+90
                sy=y+35
                d.rectangle((sx-25,sy-12,sx+25,sy),fill='#3f3026')
                d.line((sx,sy,sx,sy+25),fill='#3f3026',width=3)
    d.rectangle((1080,815,1180,880),fill='#b5956e',outline='#4b341e',width=3)
    d.text((35,40),'LAYOUT GUIDE ONLY — NO LABELS IN FINAL',font=font,fill='#735538')
    save_png(im,ROOT/'generated/contexts/EUR050_verso_seating_proxy.png')

if __name__=='__main__': main()
