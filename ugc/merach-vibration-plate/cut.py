"""Merach vibration plate (2026-11-08): hard-cut Grace's real footage, silent (she adds music in TikTok).
SRC = Telegram copy (draft). Swap SRC to her full-quality original when it lands (same timeline)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/tg.mp4")
SEGS = [(41.8,43.2),(1.2,2.25),(3.0,4.2),(4.4,5.6),(11.4,12.6),(14.6,15.8),(19.2,20.4),
        (50.6,51.9),(44.4,45.6),(54.6,55.8),(47.2,48.4),(65.0,66.2),(71.0,72.4)]
def render(name="merach", preset="veryfast"):
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:-2:flags=lanczos,crop=1080:1920,setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","20","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
