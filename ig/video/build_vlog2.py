import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D='/home/claude/vid/vlog2'; T=D+'/b1'
import os; os.makedirs(T,exist_ok=True)
BLK='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
F=lambda s: ImageFont.truetype(BLK,s,index=3)
W,H=720,1280
def run(a): subprocess.run(['ffmpeg','-v','error','-y',*a],check=True)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def sub_png(t,p):
    im=Image.new('RGBA',(W,H),(0,0,0,0));f=F(48)
    sh=Image.new('RGBA',(W,H),(0,0,0,0));ds=ImageDraw.Draw(sh);ds.text((W/2+2,1035+3),t,font=f,anchor='mm',fill=(0,0,0,220),stroke_width=5,stroke_fill=(0,0,0,220));sh=sh.filter(ImageFilter.GaussianBlur(3));im.alpha_composite(sh)
    d=ImageDraw.Draw(im);d.text((W/2,1035),t,font=f,anchor='mm',fill='white',stroke_width=2,stroke_fill=(30,30,30,255))
    assert d.textbbox((0,0),t,font=f)[2]<W-40, t
    im.save(p)
def open_title(p):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    sh=Image.new('RGBA',(W,H),(0,0,0,0));ds=ImageDraw.Draw(sh)
    for (y,t,s) in [(560,'雪寶虎寶出國玩',72),(650,'EP.2 京都・清水寺',40)]:
        ds.text((W/2,y),t,font=F(s),anchor='mm',fill=(0,0,0,200),stroke_width=6,stroke_fill=(0,0,0,200))
    sh=sh.filter(ImageFilter.GaussianBlur(6));im.alpha_composite(sh);d=ImageDraw.Draw(im)
    d.text((W/2,560),'雪寶虎寶出國玩',font=F(72),anchor='mm',fill='white')
    d.text((W/2,650),'EP.2 京都・清水寺',font=F(40),anchor='mm',fill=(255,236,170))
    im.save(p)
def tag_png(p,t):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im);g=F(26)
    bb=d.textbbox((40,70),t,font=g,anchor='lm');d.rounded_rectangle((bb[0]-16,bb[1]-10,bb[2]+16,bb[3]+10),radius=20,fill=(0,0,0,120))
    d.text((40,70),t,font=g,anchor='lm',fill='white');im.save(p)
def end_png(p):
    im=Image.new('RGB',(W,H),(247,243,234));d=ImageDraw.Draw(im);c=(31,58,104)
    d.ellipse((W/2-110,140,W/2+110,360),fill='white',outline=c,width=6)
    d.text((W/2,240),'旅遊通',font=F(58),anchor='mm',fill=c);d.text((W/2,300),'旅平險小幫手',font=F(22),anchor='mm',fill=c)
    d.text((W/2,460),'護照錢包掉了，先別慌',font=F(46),anchor='mm',fill=c)
    d.text((W/2,540),'先到警察局拿遺失證明',font=F(34),anchor='mm',fill=(51,51,51))
    d.text((W/2,595),'補辦費用能不能申請，看你的不便險',font=F(30),anchor='mm',fill=(51,51,51))
    d.text((W/2,720),'你身邊有雪寶嗎？標記他',font=F(44),anchor='mm',fill=(232,105,46))
    d.rounded_rectangle((110,830,610,940),radius=55,fill=(6,199,85));d.text((W/2,885),'LINE 搜尋 @149ecuvk',font=F(42),anchor='mm',fill='white')
    d.text((W/2,1010),'出國前，先幫你看保障',font=F(28),anchor='mm',fill=(102,102,102))
    im.save(p)
def atempo(x):
    x=max(0.68,min(1.5,x));return f'atempo={x:.3f}'
XCH='highpass=f=90,equalizer=f=4500:t=h:w=3000:g=4,loudnorm=I=-18:TP=-2:LRA=7,aresample=48000'
HCH='lowpass=f=9000,loudnorm=I=-18:TP=-2:LRA=7,aresample=48000'
def fit(n,src,s0,s1,t0,t1,kind):
    # extract source span, compress inner pauses, stretch to target length
    raw=f'{T}/{n}_r.wav'
    run(['-i',src,'-af',f'atrim={max(0,s0-0.02)}:{s1+0.04},asetpts=PTS-STARTPTS,'+('silenceremove=stop_periods=-1:stop_duration=0.25:stop_threshold=-40dB:stop_silence=0.18,' if s1-s0>1.6 else '')+'afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse','-ac','1','-ar','48000',raw])
    d=dur(raw);out=f'{T}/{n}.wav'
    run(['-i',raw,'-af',atempo(d/(t1-t0))+','+(XCH if kind=='x' else HCH),'-ac','2','-ar','48000',out])
    print(n,'src',round(d,2),'target',round(t1-t0,2),'got',round(dur(out),2));return (out,t0)
dF=D+'/dF2.mp4'
A=[(fit('a1',D+'/k0.wav',0.0,3.65,0.0,2.29,'x'),[('大家好～今天在京都清水寺！',0.05)]),
   (fit('a2',D+'/dF4.mp4',0.0,0.91,3.24,4.10,'h'),[('人好多。',3.24)]),
   (fit('a3',D+'/k1.wav',0.0,3.79,4.86,7.21,'x'),[('你看下面！',4.86),('整個京都都白了！',5.9)]),
   (fit('a4',D+'/dF4.mp4',2.20,3.67,8.22,9.40,'h'),[('……你不要靠欄杆那麼近。',8.22)]),
   (fit('a5',D+'/k2.wav',0.0,1.81,10.19,11.95,'x'),[('等一下去吃抹茶冰淇淋！',10.19)])]
B=[(fit('b1',D+'/k3.wav',0.0,1.94,0.53,2.40,'x'),[('欸……我的錢包呢？',0.53)]),
   (fit('b2',D+'/dF4.mp4',4.62,5.20,3.19,3.79,'h'),[('又來了。',3.19)]),
   (fit('b3',D+'/k4.wav',0.0,2.77,4.71,6.61,'x'),[('護照……也在裡面啦……',4.71)]),
   (fit('b4',D+'/dF4.mp4',6.91,12.84,7.40,12.09,'h'),[('先去派出所拿遺失證明，',7.40),('有保不便險的話，',9.4),('補辦費用可以申請。',10.7)])]
def scene(n,video,lines,D_,tag=None):
    place=[c for c,_ in lines];subs=[s for _,sb in lines for s in sb]
    inp=['-t',str(D_),'-i',video];fc=f'[0:v]scale=720:1280,fps=24,setsar=1,tpad=stop_mode=clone:stop_duration=1,trim=0:{D_},setpts=PTS-STARTPTS[v1]';last='v1';ii=1
    if tag: inp+=['-i',tag];fc+=f";[{last}][{ii}:v]overlay=0:0[vt]";last='vt';ii+=1
    for k,(tt,s0) in enumerate(subs):
        s1=subs[k+1][1] if k+1<len(subs) else min(D_,s0+3.0)
        p=f'{T}/s{n}_{k}.png';sub_png(tt,p);inp+=['-i',p]
        fc+=f";[{last}][{ii}:v]overlay=0:0:enable='between(t,{s0:.2f},{s1-0.01:.2f})'[v{ii}]";last=f'v{ii}';ii+=1
    inp+=['-f','lavfi','-t',str(D_),'-i','anoisesrc=c=brown:a=0.12:r=48000'];bed=ii;ii+=1
    mix=[f'[{bed}:a]aformat=channel_layouts=stereo,highpass=f=120,lowpass=f=900,tremolo=f=0.15:d=0.6[bed]'];labs=[]
    for j,(f,t0) in enumerate(place):
        inp+=['-i',f];mix.append(f'[{ii}:a]adelay={int(t0*1000)}|{int(t0*1000)}[l{j}]');labs.append(f'[l{j}]');ii+=1
    mix.append(''.join(labs)+f'amix=inputs={len(labs)}:normalize=0:duration=longest,aecho=0.9:0.6:18|60:0.10|0.05,lowpass=f=11000[vox]')
    mix.append(f'[bed][vox]amix=inputs=2:normalize=0:duration=first,atrim=0:{D_},afade=t=out:st={D_-0.2}:d=0.2,alimiter=limit=0.85:level=0[a]')
    out=f'{T}/q{n}.mp4'
    run([*inp,'-filter_complex',fc+';'+';'.join(mix),'-map',f'[{last}]','-map','[a]','-t',str(D_),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',out]);return out
# opening: bridge 2.2s + panorama 2.4s, Ken Burns, crossfade
open_title(T+'/otitle.png');tag_png(T+'/tag.png','京都・清水寺');end_png(T+'/end.png')
def kb(img,out,d,z0,z1,y0=0.5,y1=0.5):
    n=int(d*24)
    run(['-loop','1','-i',img,'-vf',f"scale=1440:-1,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*({y0}+({y1}-{y0})*on/{n})':d={n}:s=720x1280:fps=24,setsar=1",'-t',str(d),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p',out])
kb(D+'/scen/scene2.png',T+'/o1.mp4',2.6,1.0,1.12,0.6,0.45)
kb(D+'/scen/scene1.png',T+'/o2.mp4',2.8,1.12,1.0,0.5,0.5)
OD=2.6+2.8-0.5
run(['-i',T+'/o1.mp4','-i',T+'/o2.mp4','-i',T+'/otitle.png','-f','lavfi','-t',str(OD),'-i','anoisesrc=c=brown:a=0.10:r=48000','-filter_complex',
     f"[0:v][1:v]xfade=transition=fade:duration=0.5:offset=2.1[x];[x][2:v]overlay=0:0:enable='gte(t,2.3)'[v];[3:a]aformat=channel_layouts=stereo,highpass=f=120,lowpass=f=900,tremolo=f=0.15:d=0.6,afade=t=in:d=0.6[a]",
     '-map','[v]','-map','[a]','-t',str(OD),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',T+'/q0.mp4'])
qA=scene('A',D+'/A.mp4',A,12.3,tag=T+'/tag.png')
qB=scene('B',D+'/B.mp4',B,12.6)
run(['-loop','1','-t','3.5','-i',T+'/end.png','-f','lavfi','-t','3.5','-i','anullsrc=r=48000:cl=stereo','-vf','fps=24,format=yuv420p,fade=t=in:d=0.4','-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-shortest',T+'/pend.mp4'])
open(T+'/list.txt','w').write(''.join(f"file '{p}'\n" for p in [T+'/q0.mp4',qA,qB,T+'/pend.mp4']))
run(['-f','concat','-safe','0','-i',T+'/list.txt','-c','copy',T+'/nomusic.mp4'])
Dt=dur(T+'/nomusic.mp4');a0=OD;a1=OD+12.3+12.6
vol=f"if(lt(t,{a0}),1.3,if(lt(t,{a1}),0.2,1.0))"
run(['-i',T+'/nomusic.mp4','-ss','10','-i','/home/claude/vid/vlog1/bgm/jp_366769.mp3','-filter_complex',f"[0:a]volume=2.2[d];[1:a]atrim=0:{Dt},asetpts=PTS-STARTPTS,aresample=48000,volume='{vol}':eval=frame,afade=t=in:d=0.8,afade=t=out:st={Dt-1.5}:d=1.5[m];[d][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85:level=0[a]",'-map','0:v','-map','[a]','-t',str(Dt),'-c:v','libx264','-crf','21','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',D+'/VLOG2_京都_v3.mp4'])
print('ok',Dt)
