import subprocess
exec(open('build.py').read().split("shots=json.load")[0])
V='/home/claude/vid/v5'
def cut(src,s,e,out):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s),'-t',str(round(e-s,3)),'-i',src,'-ar','48000','-ac','2',out],check=True)
# (src wav, src start, src end, place time in shot, subtitle pieces[(text, rel_start)])
A=[('A',0.10,1.88,0.10,[('欸欸欸！延誤欸！',0)]),
   ('A',2.12,3.26,2.12,[('嗯，看到了。',0)]),
   ('A',3.26,4.10,3.26,[('延到幾點啦？',0)]),
   ('A',4.42,5.04,4.42,[('待定。',0)]),
   ('A',5.32,9.26,5.32,[('待定是幾點啦！',0),('那我的溫泉咧？我的和牛咧？',1.6)]),
   ('A',9.42,10.64,9.42,[('你很重，下去。',0)]),
   ('A',11.22,12.78,11.22,[('我訂了半年欸……',0)]),
   ('A',13.08,14.64,13.08,[('誰叫你挑颱風天。',0)])]
Bl=[('B',0.12,1.76,1.0,[('蛤？你怎麼點這麼多？',0)]),
   ('B',2.06,5.38,3.0,[('延誤有不便險啊，',0),('吃的可以申請。',2.1)]),
   ('B',5.38,6.36,7.7,[('那分我一口嘛～',0)]),
   ('B',6.54,7.24,9.9,[('你又沒保。',0)]),
   ('B',7.78,9.16,10.9,[('我有啊！刷卡送的！',0)]),
   ('B',9.62,11.00,12.5,[('那你機票用哪張卡刷的？',0)]),
   ('B',12.08,12.96,14.2,[('……另一張。',0)]),
   ('B',13.54,15.58,15.5,[('出國前先問清楚啦！',0)])]
def shot(n,video,vf_extra,dur,lines,amb):
    inp=['-i',video,'-i',B+'/title.png'];fc=f'[0:v]{vf_extra}scale=720:1280,fps=24,setsar=1[v0];[v0][1:v]overlay=0:0[v1]';last='v1';ii=2
    subs=[]
    for li,(w,s,e,t0,pcs) in enumerate(lines):
        for (tt,r) in pcs: subs.append([tt,t0+r])
    for k in range(len(subs)):
        s0=subs[k][1]; s1=subs[k+1][1] if k+1<len(subs) else dur
        p=f'{B}/v5_{n}_{k}.png';sub_png(subs[k][0],p);inp+=['-i',p]
        fc+=f";[{last}][{ii}:v]overlay=0:0:enable='between(t,{s0:.2f},{s1-0.01:.2f})'[v{ii}]";last=f'v{ii}';ii+=1
    col,amp=('brown',0.06) if amb=='rain' else ('pink',0.025)
    inp+=['-f','lavfi','-t',str(dur),'-i',f'anoisesrc=c={col}:a={amp}:r=48000'];ai=ii;ii+=1
    mix=[f'[{ai}:a]aformat=channel_layouts=stereo,lowpass=f=3000[amb]'];labs=['[amb]']
    for j,(w,s,e,t0,pcs) in enumerate(lines):
        f=f'{B}/v5_{n}_l{j}.wav';cut(f'{V}/ep1v5_{w}.wav',s,e,f);inp+=['-i',f]
        mix.append(f'[{ii}:a]adelay={int(t0*1000)}|{int(t0*1000)},volume=1.25[l{j}]');labs.append(f'[l{j}]');ii+=1
    mix.append(''.join(labs)+f'amix=inputs={len(labs)}:normalize=0:duration=first,atrim=0:{dur},afade=t=out:st={dur-0.05}:d=0.05,alimiter=limit=0.89[a]')
    fc+=';'+';'.join(mix);out=f'{B}/v5_q{n}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map',f'[{last}]','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',out],check=True)
    return out
# shot B: slow 11s-end by 1.63 to reach 17.6s
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{V}/ep1v5_shotB.mp4','-filter_complex',"[0:v]split[a][b];[a]trim=0:11,setpts=PTS-STARTPTS[a1];[b]trim=11,setpts=(PTS-STARTPTS)*1.63,fps=24[b1];[a1][b1]concat=n=2:v=1:a=0[v]",'-map','[v]','-an','-c:v','libx264','-crf','16','-preset','medium',f'{V}/shotB_ret.mp4'],check=True)
p1=shot(1,f'{V}/ep1v5_shotA.mp4','',15.0,A,'rain')
p2=shot(2,f'{V}/shotB_ret.mp4','',17.6,Bl,'room')
open(B+'/list5.txt','w').write(''.join(f"file '{p}'\n" for p in [p1,p2,B+'/pend.mp4']))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',B+'/list5.txt','-c','copy','-movflags','+faststart','EP1_v5.mp4'],check=True)
print('ok')
