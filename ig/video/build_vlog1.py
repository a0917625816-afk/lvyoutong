import subprocess,sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D='/home/claude/vid/vlog1'; T=D+'/build'
BLK='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
F=lambda s: ImageFont.truetype(BLK,s,index=3)
W,H=720,1280
def run(a): subprocess.run(['ffmpeg','-v','error','-y',*a],check=True)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def title_png(p,TITLE,TAG):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im);f=F(44)
    bb=d.textbbox((W/2,140),TITLE,font=f,anchor='mm');d.rounded_rectangle((bb[0]-26,bb[1]-18,bb[2]+26,bb[3]+18),radius=14,fill=(242,207,58,255))
    d.text((W/2,140),TITLE,font=f,anchor='mm',fill=(17,17,17,255))
    g=F(26);bb=d.textbbox((W/2,215),TAG,font=g,anchor='mm');d.rounded_rectangle((bb[0]-16,bb[1]-10,bb[2]+16,bb[3]+10),radius=20,fill=(0,0,0,130))
    d.text((W/2,215),TAG,font=g,anchor='mm',fill='white');im.save(p)
def sub_png(t,p):
    im=Image.new('RGBA',(W,H),(0,0,0,0));f=F(48)
    sh=Image.new('RGBA',(W,H),(0,0,0,0));ds=ImageDraw.Draw(sh);ds.text((W/2+2,1035+3),t,font=f,anchor='mm',fill=(0,0,0,220),stroke_width=5,stroke_fill=(0,0,0,220));sh=sh.filter(ImageFilter.GaussianBlur(3));im.alpha_composite(sh)
    d=ImageDraw.Draw(im);d.text((W/2,1035),t,font=f,anchor='mm',fill='white',stroke_width=2,stroke_fill=(30,30,30,255))
    assert d.textbbox((0,0),t,font=f)[2]<W-40, t
    im.save(p)
def end_png(p):
    im=Image.new('RGB',(W,H),(247,243,234));d=ImageDraw.Draw(im);c=(31,58,104)
    d.ellipse((W/2-110,140,W/2+110,360),fill='white',outline=c,width=6)
    d.text((W/2,240),'旅遊通',font=F(58),anchor='mm',fill=c);d.text((W/2,300),'旅平險小幫手',font=F(22),anchor='mm',fill=c)
    d.text((W/2,460),'冬天去日本，小心路面結冰',font=F(46),anchor='mm',fill=c)
    d.text((W/2,540),'在國外看醫生，自費可能很驚人',font=F(34),anchor='mm',fill=(51,51,51))
    d.text((W/2,595),'出發前先確認有沒有海外醫療保障',font=F(30),anchor='mm',fill=(51,51,51))
    d.text((W/2,720),'你身邊有雪寶嗎？標記他',font=F(44),anchor='mm',fill=(232,105,46))
    d.rounded_rectangle((110,830,610,940),radius=55,fill=(6,199,85));d.text((W/2,885),'LINE 搜尋 @149ecuvk',font=F(42),anchor='mm',fill='white')
    d.text((W/2,1010),'出國前，先幫你看保障',font=F(28),anchor='mm',fill=(102,102,102))
    im.save(p)
def xclip(n,src,tempo=1.12):
    out=f'{T}/{n}.wav'
    run(['-i',src,'-af',f'silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.08,areverse,silenceremove=stop_periods=-1:stop_duration=0.22:stop_threshold=-40dB:stop_silence=0.16,atempo={tempo},highpass=f=90,equalizer=f=4500:t=h:w=3000:g=4,loudnorm=I=-18:TP=-2:LRA=7,aresample=48000','-ac','2','-ar','48000',out]);return out
def hclip(n,s,e):
    out=f'{T}/{n}.wav'
    run(['-ss',str(s-0.03),'-t',str(e-s+0.08),'-i',D+'/dF.mp4','-af','afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse,lowpass=f=9000,loudnorm=I=-18:TP=-2:LRA=7,aresample=48000','-ac','2','-ar','48000',out]);return out
title_png(T+'/title.png','雪寶虎寶出國玩','岐阜・白川鄉合掌村');end_png(T+'/end.png')
X={k:xclip(k,f'{D}/{k}.wav') for k in ['w0b','w1','w2','w3b']};X['w4']=xclip('w4',D+'/w4.wav',1.3)
for k,v in X.items(): print(k,round(dur(v),2))
if len(sys.argv)>1: sys.exit()
A=[(X['w0b'],0.15,[('大家好～我們到白川鄉了！',0)]),
   (hclip('h1',0.48,1.04),3.3,[('好冷。',0)]),
   (X['w1'],4.8,[('你看那個屋頂，像不像飯糰！',0)]),
   (hclip('h2',2.88,3.80),9.3,[('……你只想到吃。',0)]),
   (X['w2'],11.0,[('等一下上展望台，',0),('拍全景給大家看！',1.3)])]
B=[(X['w3b'],1.35,[('這邊路好滑喔……',0),('哇啊啊！',1.75)]),
   (hclip('h3',5.72,7.62),4.25,[('哈哈哈哈，我有錄到喔。',0)]),
   (X['w4'],None,[('我的屁股……好痛喔……',0)]),
   (hclip('h4',9.37,13.12),None,[('在日本看醫生很貴欸，',0),('出國前先確認',1.6),('有沒有保海外醫療啦。',2.3)])]
def scene(n,video,lines,D_,gap=0.25,title=True,ss=0,sfx=None):
    t=0;place=[];subs=[]
    for f,t0,sb in lines:
        if t0 is not None: t=t0
        d=dur(f);place.append((f,t));subs+=[(s,t+r) for s,r in sb];t+=d+gap
    print(n,'speech end',round(t-gap,2),[(round(b,2)) for a,b in place])
    inp=['-ss',str(ss),'-t',str(D_),'-i',video,'-i',T+'/title.png'];fc=f'[0:v]scale=720:1280,fps=24,setsar=1,tpad=stop_mode=clone:stop_duration=1,trim=0:{D_}[v0];[v0][1:v]overlay=0:0'+("" if title else ":enable='lt(t,0)'")+'[v1]';last='v1';ii=2
    for k,(tt,s0) in enumerate(subs):
        s1=subs[k+1][1] if k+1<len(subs) else min(D_,s0+3.5)
        p=f'{T}/s{n}_{k}.png';sub_png(tt,p);inp+=['-i',p]
        fc+=f";[{last}][{ii}:v]overlay=0:0:enable='between(t,{s0:.2f},{s1-0.01:.2f})'[v{ii}]";last=f'v{ii}';ii+=1
    inp+=['-f','lavfi','-t',str(D_),'-i','anoisesrc=c=brown:a=0.16:r=48000'];bed=ii;ii+=1
    mix=[f'[{bed}:a]aformat=channel_layouts=stereo,highpass=f=120,lowpass=f=900,tremolo=f=0.15:d=0.6,volume=0.9[bed]'];labs=[]
    for j,(f,t0) in enumerate(place):
        inp+=['-i',f];mix.append(f'[{ii}:a]adelay={int(t0*1000)}|{int(t0*1000)}[l{j}]');labs.append(f'[l{j}]');ii+=1
    if sfx: inp+=['-i',sfx];mix.append(f'[{ii}:a]volume=1.0[sx]');labs.append('[sx]');ii+=1
    mix.append(''.join(labs)+f'amix=inputs={len(labs)}:normalize=0:duration=longest,aecho=0.9:0.6:18|60:0.10|0.05,lowpass=f=11000[vox]')
    mix.append(f'[bed][vox]amix=inputs=2:normalize=0:duration=first,atrim=0:{D_},afade=t=out:st={D_-0.25}:d=0.25,alimiter=limit=0.85:level=0[a]')
    out=f'{T}/q{n}.mp4'
    run([*inp,'-filter_complex',fc+';'+';'.join(mix),'-map',f'[{last}]','-map','[a]','-t',str(D_),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',out]);return out
qA=scene('A',D+'/A.mp4',A,14.1)
qB=scene('B',D+'/B.mp4',B,14.4,title=False,ss=1.4)
run(['-loop','1','-t','4','-i',T+'/end.png','-f','lavfi','-t','4','-i','anullsrc=r=48000:cl=stereo','-vf','fps=24,format=yuv420p,fade=t=in:d=0.4','-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-shortest',T+'/pend.mp4'])
open(T+'/list.txt','w').write(''.join(f"file '{p}'\n" for p in [qA,qB,T+'/pend.mp4']))
run(['-f','concat','-safe','0','-i',T+'/list.txt','-c','copy',T+'/nomusic.mp4'])
Dt=14.1+14.4+4.0
run(['-i',T+'/nomusic.mp4','-i','/home/claude/vid/v6/bgm.wav','-filter_complex',f"[0:a]volume=2.4[d];[1:a]aloop=loop=-1:size=2e9,atrim=0:{Dt},volume='if(lt(t,28.5),0.07,0.26)':eval=frame,afade=t=out:st={Dt-1.4}:d=1.4[m];[d][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85:level=0[a]",'-map','0:v','-map','[a]','-t',str(Dt),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',D+'/VLOG1_白川鄉_v4.mp4'])
print('ok')
