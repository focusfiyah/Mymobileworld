"""Gate oracle: python3 check.py NAME LO HI -> CUT_OK NAME when out/NAME_v1.mp4 is 1080x1920, length in [LO,HI] and within 0.15 s of out/NAME_v1.json "expected", no black frames. Audio allowed (Grace's own sound)."""
import subprocess,json,sys
n,lo,hi=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]); p=f"out/{n}_v1.mp4"
pr=json.loads(subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",p],capture_output=True,text=True,check=True).stdout)
v=[s for s in pr["streams"] if s["codec_type"]=="video"][0]
d=float(pr["format"]["duration"]); exp=json.load(open(f"out/{n}_v1.json"))["expected"]
bl=subprocess.run(["ffmpeg","-v","info","-i",p,"-vf","blackdetect=d=0.05:pix_th=0.10","-an","-f","null","-"],capture_output=True,text=True).stderr.count("black_start")
e=[]
if (v["width"],v["height"])!=(1080,1920): e.append(f"size {v['width']}x{v['height']}")
if not lo<=d<=hi: e.append(f"duration {d:.2f} not in {lo}-{hi}")
if abs(d-exp)>0.15: e.append(f"duration {d:.2f} vs planned {exp}")
if bl: e.append(f"{bl} black segments")
print("FAIL "+"; ".join(e) if e else f"CUT_OK {n} {d:.2f}s"); sys.exit(1 if e else 0)
