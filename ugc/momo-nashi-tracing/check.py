"""Gate oracle: python3 check.py MODE LO HI -> CUT_OK when out/momo_MODE.mp4 is 1080x1920, silent, LO-HI s long, within
0.15 s of the planned length, has no black frames and no frozen stretch (>0.5 s)."""
import subprocess,json,sys
n,lo,hi=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]); p=f"out/momo_{n}.mp4"
pr=json.loads(subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",p],capture_output=True,text=True,check=True).stdout)
v=[s for s in pr["streams"] if s["codec_type"]=="video"][0]; a=[s for s in pr["streams"] if s["codec_type"]=="audio"]
d=float(pr["format"]["duration"]); exp=json.load(open(f"out/momo_{n}.json"))["expected"]
log=subprocess.run(["ffmpeg","-v","info","-i",p,"-vf","blackdetect=d=0.05:pix_th=0.10,freezedetect=n=0.003:d=0.5","-an","-f","null","-"],capture_output=True,text=True).stderr
bl=log.count("black_start"); fr=log.count("freeze_start")
errs=[]
if (v["width"],v["height"])!=(1080,1920): errs.append(f"size {v['width']}x{v['height']}")
if a: errs.append("has audio")
if not lo<=d<=hi: errs.append(f"duration {d:.2f} not in {lo}-{hi}")
if abs(d-exp)>0.15: errs.append(f"duration {d:.2f} vs planned {exp}")
if bl: errs.append(f"{bl} black segments")
if fr: errs.append(f"{fr} frozen stretches")
print("FAIL "+"; ".join(errs) if errs else f"CUT_OK {n} {d:.2f}s"); sys.exit(1 if errs else 0)
