import subprocess, json
exec(open('build.py').read().split("shots=json.load")[0])
BD=B; V='/home/claude/vid/v6'; T=BD+'/v10'
import os; os.makedirs(T,exist_ok=True)
def run(a): subprocess.run(['ffmpeg','-v','error','-y',*a],check=True)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def clip(name,src,parts,male):
    # parts: list of (s,e); join with 0.15s gaps
    fs=[]
    for k,(s,e) in enumerate(parts):
        f=f'{T}/{name}_{k}.wav';run(['-ss',str(s-0.03),'-t',str(e-s+0.08),'-i',src,'-ac','2','-ar','48000',f]);fs.append(f)
    inp=[];fc=''
    for k,f in enumerate(fs): inp+=['-i',f]
    gap='anullsrc=r=48000:cl=stereo'
    seq=[]
    for k in range(len(fs)):
        seq.append(f'[{k}:a]afade=t=in:d=0.02,areverse,afade=t=in:d=0.03,areverse[s{k}]')
    chain=';'.join(seq)
    if len(fs)>1:
        inp+=['-f','lavfi','-t','0.15','-i',gap]; g=len(fs)
        cat=''.join(f'[s{k}]'+(f'[g{k}]' if k<len(fs)-1 else '') for k in range(len(fs)))
        chain+=';'+f'[{g}:a]asplit={len(fs)-1}'+''.join(f'[g{k}]' for k in range(len(fs)-1)) if len(fs)>2 else ';'+f'[{g}:a]anull[g0]'
        chain+=';'+cat+f'concat=n={2*len(fs)-1}:v=0:a=1[c]'
    else: chain+=';[s0]anull[c]'
    post='atempo=1.2,aecho=0.8:0.6:25:0.12,volume=1.1' if male else 'anull'
    out=f'{T}/{name}.wav';run([*inp,'-filter_complex',chain+f';[c]{post}[o]','-map','[o]',out]);return out

def xclip(name,src):
    out=f'{T}/{name}.wav'
    run(['-i',src,'-af','silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.08,areverse,silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-40dB:stop_silence=0.14,atempo=1.33,highpass=f=90,equalizer=f=4500:t=h:w=3000:g=4,loudnorm=I=-18:TP=-2:LRA=7,aresample=48000','-ac','2','-ar','48000',out]);return out
def hclip(name,src,s,e):
    out=f'{T}/{name}.wav'
    run(['-ss',str(s-0.03),'-t',str(e-s+0.08),'-i',src,'-af','afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse,lowpass=f=9000,loudnorm=I=-18:TP=-2:LRA=7,aresample=48000','-ac','2','-ar','48000',out]);return out
X=V+'/tts_xA.wav'; XB=V+'/tts_xB.wav'; DA=V+'/d_A2.mp4'; DB=V+'/d_B3.mp4'
A=[('H',hclip('aH1',DA,0.46,1.63),['欸，看板全紅了。']),
   ('X',xclip('aX1',V+'/x0.wav'),['欸欸欸，延誤欸？延到幾點啦？']),
   ('H',hclip('aH2',DA,4.31,4.73),['待定。']),
   ('X',xclip('aX2',V+'/x1.wav'),['待定是幾點啦……','那我的溫泉咧？我的和牛咧？']),
   ('H',hclip('aH3',DA,7.86,8.79),['你很重，下去。']),
   ('X',xclip('aX3',V+'/x2.wav'),['我訂了半年欸……']),
   ('H',hclip('aH4',DA,10.55,11.67),['誰叫你挑颱風天。'])]
Bl=[('X',xclip('bX1',V+'/x3.wav'),['蛤？你怎麼點這麼多？']),
   ('H',hclip('bH1',DB,2.14,3.92),['延誤有不便險啊，','吃的可以申請。']),
   ('X',xclip('bX2',V+'/x4.wav'),['那分我一口嘛～']),
   ('H',hclip('bH2',DB,5.43,6.12),['你又沒保。']),
   ('X',xclip('bX3',V+'/x5.wav'),['我有啊！刷卡送的！']),
   ('H',hclip('bH3',DB,8.04,9.41),['那你機票用哪張卡刷的？']),
   ('X',xclip('bX4',V+'/x6.wav'),['……另一張。']),
   ('H',hclip('bH4',DB,10.43,11.77),['出國前先問清楚啦！'])]
def scene(n,video,lines,lead,gapv,maxd):
    t=lead;place=[];subs=[]
    for w,f,txt in lines:
        d=dur(f);place.append((f,t))
        if len(txt)==1: subs.append((txt[0],t))
        else: subs.append((txt[0],t));subs.append((txt[1],t+d*0.45))
        t+=d+gapv
    D=min(maxd,t+0.4);print(n,'dur',round(D,2),'speech end',round(t,2))
    inp=['-t',str(D),'-i',video,'-i',BD+'/title.png'];fc='[0:v]scale=720:1280,fps=24,setsar=1[v0];[v0][1:v]overlay=0:0[v1]';last='v1';ii=2
    for k,(tt,s0) in enumerate(subs):
        s1=subs[k+1][1] if k+1<len(subs) else D
        p=f'{T}/s{n}_{k}.png';sub_png(tt,p);inp+=['-i',p]
        fc+=f";[{last}][{ii}:v]overlay=0:0:enable='between(t,{s0:.2f},{s1-0.01:.2f})'[v{ii}]";last=f'v{ii}';ii+=1
    inp+=['-f','lavfi','-t',str(D),'-i','anoisesrc=c=pink:a=0.016:r=48000'];bed=ii;ii+=1
    mix=[f'[{bed}:a]aformat=channel_layouts=stereo,lowpass=f=2500[bed]'];labs=['[bed]']
    for j,(f,t0) in enumerate(place):
        inp+=['-i',f];mix.append(f'[{ii}:a]adelay={int(t0*1000)}|{int(t0*1000)}[l{j}]');labs.append(f'[l{j}]');ii+=1
    mix.append(''.join(labs[1:])+f'amix=inputs={len(labs)-1}:normalize=0:duration=longest,aecho=0.85:0.7:28|47:0.13|0.08[vox]');mix.append(f'[bed][vox]amix=inputs=2:normalize=0:duration=first,atrim=0:{D},afade=t=out:st={D-0.2}:d=0.2,alimiter=limit=0.85:level=0[a]')
    out=f'{T}/q{n}.mp4'
    run([*inp,'-filter_complex',fc+';'+';'.join(mix),'-map',f'[{last}]','-map','[a]','-t',str(D),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',out])
    return out,D
qA,dA=scene('A',V+'/g_A4.mp4',A,0.12,0.2,15.0)
qB,dB=scene('B',V+'/g_B2_slow.mp4',Bl,0.25,0.18,14.85)
open(T+'/list.txt','w').write(''.join(f"file '{p}'\n" for p in [qA,qB,BD+'/pend.mp4']))
run(['-f','concat','-safe','0','-i',T+'/list.txt','-c','copy',T+'/nomusic.mp4'])
D=dA+dB+3.0
run(['-i',T+'/nomusic.mp4','-i',V+'/bgm.wav','-filter_complex',f"[0:a]volume=0.8[d];[1:a]atrim=0:{D},volume='if(lt(t,{dA+dB}),0.075,0.26)':eval=frame,afade=t=out:st={D-1.4}:d=1.4[m];[d][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85:level=0[a]",'-map','0:v','-map','[a]','-t',str(D),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','EP1_v10.mp4'])
print('ok',D)
