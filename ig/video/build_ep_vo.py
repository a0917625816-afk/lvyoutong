import subprocess, json, wave
import numpy as np
exec(open('build.py').read().split("shots=json.load")[0])  # reuse fonts/title/sub/end helpers
idx={"X1":[0,4.96],"X2":[5.96,3.36],"X3":[10.32,2.6],"X4":[13.92,2.36],"X5":[17.28,2.64],"X6":[20.92,1.68],"X7":[23.6,1],"H1":[25.6,1.32],"H2":[27.92,1.92],"H3":[30.84,1.56],"H4":[33.4,2.16],"H5":[36.56,2.32]}
TXT={"X1":"欸虎寶！延誤欸！延到幾點啦？！","X2":"那我的溫泉怎麼辦啦……","X3":"欸你哪來的錢吃這麼多啊？","X4":"欸欸，分我一口嘛！","X5":"哼！我也有刷卡送的好不好！","X6":"……另一張。","H1":"待定。","H2":"延誤有不便險啊。","H3":"你又沒保！","H4":"那你機票用哪張卡刷的？","H5":"出國前先問清楚啦！"}
# cut each line to its own wav
for k,(s,d) in idx.items():
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s),'-t',str(d),'-i','vo2.wav','-ar','48000','-ac','2',f'{B}/vo_{k}.wav'],check=True)
shots=[
 dict(file='S1.mp4',a=0.2,b=5.6,amb='rain',lines=[('X1',0.3)]),
 dict(file='S2.mp4',a=0.2,b=2.2,amb='rain',lines=[('H1',0.3)]),
 dict(file='S3.mp4',a=0.2,b=3.7,amb='rain',lines=[('X2',0.1)]),
 dict(file='S4.mp4',a=0.4,b=3.4,amb='room',lines=[('X3',0.3)]),
 dict(file='S5.mp4',a=0.6,b=3.9,amb='room',lines=[('H2',1.1)]),
 dict(file='S6.mp4',a=0.3,b=4.9,amb='room',lines=[('X4',0.2),('H3',2.8)]),
 dict(file='S7.mp4',a=0.2,b=3.2,amb='room',lines=[('X5',0.2)]),
 dict(file='S8.mp4',a=0.4,b=7.3,amb='room',lines=[('H4',0.3),('X6',2.7),('H5',4.55)]),
]
parts=[]
for n,s in enumerate(shots):
    dur=round(s['b']-s['a'],3)
    inp=['-ss',str(s['a']),'-t',str(dur),'-i',s['file'],'-i',B+'/title.png']
    fc='[0:v]scale=720:1280,fps=24,setsar=1[v0];[v0][1:v]overlay=0:0[v1]';last='v1';ii=2
    for (k,t0) in s['lines']:
        txt=TXT[k];d=idx[k][1]
        pieces=[(txt,t0,t0+d+0.15)] if len(txt)<=13 else [(txt[:txt.index('！',len(txt)//3)+1],t0,t0+d*0.45),(txt[txt.index('！',len(txt)//3)+1:],t0+d*0.45,t0+d+0.15)]
        for q,(tt,s0,s1) in enumerate(pieces):
            p=f'{B}/t{n}_{k}_{q}.png';sub_png(tt,p);inp+=['-i',p]
            fc+=f";[{last}][{ii}:v]overlay=0:0:enable='between(t,{s0},{s1})'[v{ii}]";last=f'v{ii}';ii+=1
    # ambience
    col='brown' if s['amb']=='rain' else 'pink'
    amp=0.06 if s['amb']=='rain' else 0.025
    inp+=['-f','lavfi','-t',str(dur),'-i',f'anoisesrc=c={col}:a={amp}:r=48000']
    amb_i=ii;ii+=1
    mix=[f'[{amb_i}:a]aformat=channel_layouts=stereo,lowpass=f=3000[amb]']
    labs=['[amb]']
    for j,(k,t0) in enumerate(s['lines']):
        inp+=['-i',f'{B}/vo_{k}.wav']
        mix.append(f'[{ii}:a]adelay={int(t0*1000)}|{int(t0*1000)},volume=1.25[l{j}]');labs.append(f'[l{j}]');ii+=1
    mix.append(''.join(labs)+f'amix=inputs={len(labs)}:normalize=0:duration=first,atrim=0:{dur},afade=t=out:st={dur-0.05}:d=0.05,alimiter=limit=0.89[a]')
    fc+=';'+';'.join(mix)
    out=f'{B}/q{n}.mp4';parts.append(out)
    subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map',f'[{last}]','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',out],check=True)
parts.append(B+'/pend.mp4')
open(B+'/list2.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',B+'/list2.txt','-c','copy','-movflags','+faststart','EP1_final_v4.mp4'],check=True)
print('ok')
