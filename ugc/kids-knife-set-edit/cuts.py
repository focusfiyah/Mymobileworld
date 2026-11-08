"""Gate oracle: python3 cuts.py TAG -> CUTS_OK when the cut has exactly len(SEGS)-1 hard scene changes (no stray or flash frames inside a shot) and mean luma is bright (YAVG >= 110)."""
import subprocess,sys,re
sys.path.insert(0,"."); from cut import SEGS
p=f"out/knife_{sys.argv[1]}.mp4"
o=subprocess.run(["ffmpeg","-v","error","-i",p,"-vf","select='gt(scene,0.22)',metadata=print:file=-","-f","null","-"],capture_output=True,text=True).stdout
n=len(re.findall("pts_time",o))
y=subprocess.run(["ffmpeg","-v","error","-i",p,"-vf","signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-","-f","null","-"],capture_output=True,text=True).stdout
ys=[float(v) for v in re.findall(r"YAVG=([\d.]+)",y)]; ya=sum(ys)/len(ys)
ok=n==len(SEGS)-1 and ya>=110
print(("CUTS_OK" if ok else "FAIL")+f" scene_changes={n} expected={len(SEGS)-1} yavg={ya:.0f} min={min(ys):.0f}"); sys.exit(0 if ok else 1)
