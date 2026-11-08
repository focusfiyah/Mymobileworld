"""Gate oracle: python3 cuts.py TAG -> CUTS_OK when every planned cut shows a scene change (score >= 0.12 within 3 frames (60 fps sources round)),
no hard change (score >= 0.30) happens anywhere else (stray/flash frame), and mean luma is bright (YAVG >= 110)."""
import subprocess,sys,re,json
p=f"out/knife_{sys.argv[1]}.mp4"; segs=json.load(open(f"out/knife_{sys.argv[1]}.json"))["segs"]
b=[];t=0
for a,e in segs[:-1]: t+=e-a; b.append(round(t*30))
o=subprocess.run(["ffmpeg","-v","error","-i",p,"-vf","select='gt(scene,0.12)',metadata=print:file=-","-f","null","-"],capture_output=True,text=True).stdout
ev=[(round(float(x)*30),float(s)) for x,s in re.findall(r"pts_time:([\d.]+).*?\n.*?scene_score=([\d.]+)",o)]
missing=[x for x in b if not any(abs(f-x)<=3 for f,_ in ev)]
stray=[(f,s) for f,s in ev if s>=0.30 and not any(abs(f-x)<=3 for x in b)]
y=subprocess.run(["ffmpeg","-v","error","-i",p,"-vf","signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-","-f","null","-"],capture_output=True,text=True).stdout
ys=[float(v) for v in re.findall(r"YAVG=([\d.]+)",y)]; ya=sum(ys)/len(ys)
ok=not missing and not stray and ya>=110
print(("CUTS_OK" if ok else "FAIL")+f" cuts={len(b)} missing={missing} stray={stray} yavg={ya:.0f}"); sys.exit(0 if ok else 1)
