import subprocess
exec(open('build.py').read().split("shots=json.load")[0])
BD=B; V='/home/claude/vid/v6'
def run(a): subprocess.run(['ffmpeg','-v','error','-y',*a],check=True)
def subs_overlay(subs,dur,n):
    inp=[];fc='';last='v1';ii=2
    for k,(tt,s0) in enumerate(subs):
        s1=subs[k+1][1] if k+1<len(subs) else dur
        p=f'{BD}/v7_{n}_{k}.png';sub_png(tt,p);inp+=['-i',p]
        fc+=f";[{last}][{ii}:v]overlay=0:0:enable='between(t,{s0:.2f},{s1-0.01:.2f})'[v{ii}]";last=f'v{ii}';ii+=1
    return inp,fc,last,ii
# --- A: A4 visuals, DA2 audio shifted -0.35
dA=11.8
SA=[('欸，看板全紅了。',0.11),('欸欸欸！延誤欸！延到幾點啦？',1.63),('待定。',3.96),('待定是幾點啦！',4.67),('那我的溫泉咧？我的和牛咧？',5.72),('你很重，下去。',7.51),('我訂了半年欸……',8.81),('誰叫你挑颱風天。',10.20)]
inp,fc,last,ii=subs_overlay(SA,dA,'A')
run(['-t',str(dA),'-i',V+'/g_A4.mp4','-i',BD+'/title.png',*inp,'-ss','0.35','-i',V+'/d_A2.mp4','-filter_complex',
 '[0:v]scale=720:1280,fps=24,setsar=1[v0];[v0][1:v]overlay=0:0[v1]'+fc+f';[{ii}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.2,atrim=0:{dA},afade=t=out:st={dA-0.2}:d=0.2,alimiter=limit=0.89[a]',
 '-map',f'[{last}]','-map','[a]','-t',str(dA),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',BD+'/v7_qA.mp4'])
# --- B: B2 visuals (cut before weird arm), DB3 lines placed at B2 line starts
dB=13.2
L=[(0.46,1.82,0.44),(2.14,3.92,2.35),(4.15,5.11,4.42),(5.43,6.12,5.94),(6.35,7.78,6.96),(8.04,9.41,8.96),(9.69,10.23,10.65),(10.43,11.77,11.74)]
SB=[('蛤？你怎麼點這麼多？',0.44),('延誤有不便險啊，',2.35),('吃的可以申請。',3.2),('那分我一口嘛～',4.42),('你又沒保。',5.94),('我有啊！刷卡送的！',6.96),('那你機票用哪張卡刷的？',8.96),('另一張。',10.65),('出國前先問清楚啦！',11.74)]
inp,fc,last,ii=subs_overlay(SB,dB,'B')
ainp=['-f','lavfi','-t',str(dB),'-i','anoisesrc=c=pink:a=0.02:r=48000'];bed=ii;ii+=1
mix=[f'[{bed}:a]aformat=channel_layouts=stereo,lowpass=f=2500[bed]'];labs=['[bed]']
for j,(s,e,t0) in enumerate(L):
    ainp+=['-ss',str(s-0.05),'-t',str(e-s+0.12),'-i',V+'/d_B3.mp4']
    mix.append(f'[{ii}:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.02,adelay={int((t0-0.05)*1000)}|{int((t0-0.05)*1000)},volume=1.2[l{j}]');labs.append(f'[l{j}]');ii+=1
mix.append(''.join(labs)+f'amix=inputs={len(labs)}:normalize=0:duration=first,atrim=0:{dB},afade=t=out:st={dB-0.2}:d=0.2,alimiter=limit=0.89[a]')
run(['-t',str(dB),'-i',V+'/g_B2.mp4','-i',BD+'/title.png',*inp,*ainp,'-filter_complex','[0:v]scale=720:1280,fps=24,setsar=1[v0];[v0][1:v]overlay=0:0[v1]'+fc+';'+';'.join(mix),
 '-map',f'[{last}]','-map','[a]','-t',str(dB),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',BD+'/v7_qB.mp4'])
open(BD+'/list7.txt','w').write(''.join(f"file '{p}'\n" for p in [BD+'/v7_qA.mp4',BD+'/v7_qB.mp4',BD+'/pend.mp4']))
run(['-f','concat','-safe','0','-i',BD+'/list7.txt','-c','copy','v7_nomusic.mp4'])
D=dA+dB+4.0
run(['-i','v7_nomusic.mp4','-i',V+'/bgm.wav','-filter_complex',f"[1:a]atrim=0:{D},volume='if(lt(t,{dA+dB}),0.12,0.3)':eval=frame,afade=t=out:st={D-1.2}:d=1.2[m];[0:a][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89[a]",'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','EP1_v7_final.mp4'])
print('ok')
