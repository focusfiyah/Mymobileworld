"""JIYU NAD+ Moisturizer (2026-11-10): hard-cut Grace's real footage (HD original), silent (she adds music in TikTok), all clips 1.0x.
Order: cream dive hook, box, 'Time is part of the formula' insert, jar logo, lid top, lid off/seal, seal peel, NAD+ label, scoop, dot, rub, absorbed, two-hand compare."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/jiyu_orig.mov")
SEGS = [(54.0,55.5),(3.0,4.2),(7.4,8.6),(26.0,27.4),(30.0,31.0),(37.4,38.6),(40.6,41.8),
        (48.4,50.0),(62.0,63.4),(66.2,67.2),(67.2,69.0),(77.0,78.6),(81.5,83.5)]
def render(name="jiyu", preset="veryfast"):
    os.makedirs("out/segs", exist_ok=True); lst=[]
    for i,(a,b) in enumerate(SEGS):
        p=f"out/segs/{name}_{i:02d}.mp4"; lst.append(p)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.3f}","-i",SRC,"-t",f"{b-a:.3f}","-vf","fps=30,scale=1080:1920:flags=lanczos,setsar=1","-an",
            "-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-threads","4",p],check=True)
    open("out/segs/list.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in lst))
    out=f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","out/segs/list.txt","-c","copy","-movflags","+faststart",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
