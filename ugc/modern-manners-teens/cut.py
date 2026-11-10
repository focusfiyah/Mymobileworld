"""52 Modern Manners (2026-11-10): hard-cut Grace's real footage, silent (she adds music in TikTok).
SRC = Telegram copy (draft). Swap SRC to her full-quality original when it lands (same timeline)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/manners.mov")
OFF = float(os.environ.get("OFF", "0"))  # HD original runs ~0.1 s later than the Telegram copy (measured 2026-11-08)
SEGS = [(2.25,3.5),(6.5,7.8),(13.3,14.6),(15.2,16.4),(22.2,23.3),(27.6,28.7),(29.6,30.8),(32.3,33.6),(37.4,38.6),(48.3,49.6),(50.6,52.0)]
def render(name="manners", preset="veryfast"):
    f = "".join(f"[0:v]trim={a+OFF:.3f}:{b+OFF:.3f},setpts=PTS-STARTPTS,fps=30,scale=1080:-2:flags=lanczos,crop=1080:1920,setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","20","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
