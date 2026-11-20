import subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D='/home/claude/vid/v3'; B=D+'/build'
BLK='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
F=lambda s: ImageFont.truetype(BLK,s,index=3)
W,H=720,1280
TITLE='颱風天出國，雪寶又出事了'
def title_png(p):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im);f=F(46)
    bb=d.textbbox((W/2,150),TITLE,font=f,anchor='mm');d.rounded_rectangle((bb[0]-26,bb[1]-20,bb[2]+26,bb[3]+20),radius=14,fill=(242,207,58,255))
    d.text((W/2,150),TITLE,font=f,anchor='mm',fill=(17,17,17,255));im.save(p)
def sub_png(t,p):
    im=Image.new('RGBA',(W,H),(0,0,0,0));f=F(48)
    sh=Image.new('RGBA',(W,H),(0,0,0,0));ds=ImageDraw.Draw(sh);ds.text((W/2+2,1035+3),t,font=f,anchor='mm',fill=(0,0,0,220),stroke_width=5,stroke_fill=(0,0,0,220));sh=sh.filter(ImageFilter.GaussianBlur(3));im.alpha_composite(sh)
    d=ImageDraw.Draw(im);d.text((W/2,1035),t,font=f,anchor='mm',fill='white',stroke_width=2,stroke_fill=(30,30,30,255))
    w=d.textbbox((0,0),t,font=f)[2]
    assert w<W-40, f'subtitle too wide: {t} {w}'
    im.save(p)
def end_png(p):
    im=Image.new('RGB',(W,H),(247,243,234));d=ImageDraw.Draw(im)
    d.ellipse((W/2-110,140,W/2+110,360),fill='white',outline=(31,58,104),width=6)
    d.text((W/2,240),'旅遊通',font=F(58),anchor='mm',fill=(31,58,104));d.text((W/2,300),'旅平險小幫手',font=F(22),anchor='mm',fill=(31,58,104))
    d.text((W/2,460),'刷卡送的旅平險要注意',font=F(50),anchor='mm',fill=(31,58,104))
    d.text((W/2,540),'通常要用那張卡付機票才有保',font=F(36),anchor='mm',fill=(51,51,51))
    d.text((W/2,595),'出發前先確認，別像雪寶一樣',font=F(36),anchor='mm',fill=(51,51,51))
    bb=d.textbbox((W/2,720),'你身邊有雪寶嗎？標記他',font=F(44),anchor='mm');d.text((W/2,720),'你身邊有雪寶嗎？標記他',font=F(44),anchor='mm',fill=(232,105,46))
    d.rounded_rectangle((110,830,610,940),radius=55,fill=(6,199,85));d.text((W/2,885),'LINE 搜尋 @149ecuvk',font=F(42),anchor='mm',fill='white')
    d.text((W/2,1010),'出國前，先幫你看保障',font=F(28),anchor='mm',fill=(102,102,102))
    im.save(p)
shots=json.load(open(D+'/shots.json'))
title_png(B+'/title.png'); end_png(B+'/end.png')
parts=[]
for n,s in enumerate(shots):
    a,b=s['in'],s['out'];dur=b-a
    inputs=['-ss',str(a),'-t',str(dur),'-i',f"{D}/{s['file']}",'-i',B+'/title.png']
    fc='[0:v]scale=720:1280,fps=24,setsar=1[v0];[v0][1:v]overlay=0:0[v1]'
    last='v1'
    for k,(t0,t1,txt) in enumerate(s['subs']):
        p=f'{B}/s{n}_{k}.png';sub_png(txt,p);inputs+=['-i',p]
        fc+=f";[{last}][{k+2}:v]overlay=0:0:enable='between(t,{t0},{t1})'[v{k+2}]";last=f'v{k+2}'
    fc+=f";[0:a]aresample=48000,afade=t=in:d=0.04,afade=t=out:st={dur-0.06}:d=0.06[a]"
    out=f'{B}/p{n}.mp4';parts.append(out)
    subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc,'-map',f'[{last}]','-map','[a]','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',out],check=True)
# end card 4s with fade in, silent audio
out=B+'/pend.mp4';parts.append(out)
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-t','4','-i',B+'/end.png','-f','lavfi','-t','4','-i','anullsrc=r=48000:cl=stereo','-vf','fps=24,format=yuv420p,fade=t=in:d=0.4','-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-shortest',out],check=True)
open(B+'/list.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',B+'/list.txt','-c','copy','-movflags','+faststart',D+'/EP1_final.mp4'],check=True)
print('done')
