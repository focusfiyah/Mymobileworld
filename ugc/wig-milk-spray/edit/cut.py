"""Wig Milk Spray (2026-11-11): hard-cut Grace's real footage (her HD original WigMilkSpray2.mov, 1080x1920 HEVC 30fps), silent like the Calmi edit (she adds sound in TikTok)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/WigMilkSpray2.mov")
# tangled wig pulled apart (messy hair at frame 0), spray + brush up to camera, spraying, brushing through, smooth shiny hair flip, final smile
SEGS = [(5.1,7.6),(28.4,31.2),(102.0,104.6),(146.4,149.2),(230.0,233.0),(551.0,553.6)]
GRADE = os.environ.get("GRADE", "eq=brightness=0.02:contrast=1.03")
def render(name="wig", preset="veryfast"):
    ins = sum((["-ss",f"{a:.3f}","-t",f"{b-a:.3f}","-i",SRC] for a,b in SEGS),[])  # one seeked input per shot (a single input with 6 trims buffers minutes of 1080p and got OOM-killed)
    f = "".join(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1,{GRADE}[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
