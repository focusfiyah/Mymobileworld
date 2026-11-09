"""Gate oracle: python3 check.py NAME LO HI -> prints CUT_OK NAME when 1080x1920, no audio, length in [LO,HI] and within 0.15 s of planned, no black frames."""
import subprocess,json,sys
n,lo,hi=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]); p=f"out/knife_{n}.mp4"
pr=json.loads(subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",p],capture_output=True,text=True,check=True).stdout)
v=[s for s in pr["streams"] if s["codec_type"]=="video"][0]; a=[s for s in pr["streams"] if s["codec_type"]=="audio"]
d=float(pr["format"]["duration"]); exp=json.load(open(f"out/knife_{n}.json"))["expected"]
bl=subprocess.run(["ffmpeg","-v","info","-i",p,"-vf","blackdetect=d=0.05:pix_th=0.10","-an","-f","null","-"],capture_output=True,text=True).stderr.count("black_start")
errs=[]
if (v["width"],v["height"])!=(1080,1920): errs.append(f"size {v['width']}x{v['height']}")
if a: errs.append("has audio")
if not lo<=d<=hi: errs.append(f"duration {d:.2f} not in {lo}-{hi}")
if abs(d-exp)>0.15: errs.append(f"duration {d:.2f} vs planned {exp}")
if bl: errs.append(f"{bl} black segments")
print("FAIL "+"; ".join(errs) if errs else f"CUT_OK {n} {d:.2f}s"); sys.exit(1 if errs else 0)
