"""KIGO Baby Sunglasses (2026-11-10): hard-cut Grace's real footage (her HD original), silent (background audio is kids/TV, not usable; she adds music in TikTok)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/kigo.mov")
# bend hook, bend wider, lenses, lenses close, case reveal, cloth wipe, snap pouch, Kidsgo card, back in case
SEGS = [(61.4,64.2),(65.6,67.2),(53.0,54.8),(26.4,27.0),(2.4,4.2),(18.6,20.4),(38.1,39.3),(48.3,49.2),(27.3,29.0)]
GRADE = os.environ.get("GRADE", "eq=brightness=0.025:contrast=1.03")
def render(name="kigo", preset="veryfast"):
    f = "".join(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1,{GRADE}[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
