"""Gate oracle: python3 check.py NAME LO HI [audio|silent] -> prints CUT_OK NAME when 1080x1920, length in [LO,HI] and within 0.15 s of planned,
no black frames, no frozen run >=0.5 s, and audio present (audio) or absent (silent) as planned. Pattern: ugc/haiti-flag/check.py."""
import subprocess,json,sys
n,lo,hi=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]); mode=sys.argv[4] if len(sys.argv)>4 else "audio"
p=f"out/{n}_v1.mp4"
pr=json.loads(subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",p],capture_output=True,text=True,check=True).stdout)
v=[s for s in pr["streams"] if s["codec_type"]=="video"][0]; a=[s for s in pr["streams"] if s["codec_type"]=="audio"]
d=float(pr["format"]["duration"]); exp=json.load(open(f"out/{n}_v1.json"))["expected"]
log=subprocess.run(["ffmpeg","-v","info","-i",p,"-vf","blackdetect=d=0.05:pix_th=0.10,freezedetect=n=0.003:d=0.5","-an","-f","null","-"],capture_output=True,text=True).stderr
errs=[]
if (v["width"],v["height"])!=(1080,1920): errs.append(f"size {v['width']}x{v['height']}")
if mode=="silent" and a: errs.append("has audio")
if mode=="audio" and not a: errs.append("no audio")
if not lo<=d<=hi: errs.append(f"duration {d:.2f} not in {lo}-{hi}")
if abs(d-exp)>0.15: errs.append(f"duration {d:.2f} vs planned {exp}")
if log.count("black_start"): errs.append(f"{log.count('black_start')} black segments")
if log.count("freeze_start"): errs.append(f"{log.count('freeze_start')} frozen runs")
print("FAIL "+"; ".join(errs) if errs else f"CUT_OK {n} {d:.2f}s"); sys.exit(1 if errs else 0)
