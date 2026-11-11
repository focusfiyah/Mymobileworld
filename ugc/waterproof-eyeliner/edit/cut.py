"""Waterproof Ultra-Fine Eyeliner (2026-11-11): hard-cut Grace's HD original (no voice in her clip, only room noise; silent, she adds music in TikTok).
Usage: python3 cut.py [name] [preset]. Fast seek per shot (-ss before each input)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/WaterproofEyeliner.mov")
# finished look smile (hook), SNAILGIRL box, pencil slides out, swatch on palm, lower lash line, finished eyes
SEGS = [(182.3,184.6),(187.0,189.0),(194.6,197.2),(23.5,26.0),(82.0,85.0),(161.0,163.5)]
GRADE = os.environ.get("GRADE", "eq=brightness=0.02:contrast=1.03")
def render(name="eyeliner", preset="veryfast"):
    ins, f = [], ""
    for i,(a,b) in enumerate(SEGS):
        ins += ["-ss", f"{a:.3f}", "-t", f"{b-a:.3f}", "-i", SRC]
        f += f"[{i}:v]setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1,{GRADE}[v{i}];"
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
