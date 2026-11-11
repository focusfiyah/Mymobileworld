"""GALENTAL Iceberg Vanity Mirror (2026-11-11): hard-cut Grace's HD original (Mirror1.mov, 1080x1920 HEVC 59.94), silent (she adds music in TikTok)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/Mirror1.mov")
# tap: cool light flips warm at 0.75 s | warm glow on her face | pull back: mirror on its base | hand on frame, light cycles cool/white/warm | crystal edge close-up | wide end
SEGS = [(7.0,9.5),(49.0,51.75),(55.75,59.0),(66.25,69.25),(80.5,83.0),(87.25,89.0)]
# V2 (2026-11-11): timed to Grace's script (Telegram msg 438), one line -> its shots
SEGS2 = [(7.0,10.0),                               # L1 "I'm not even going to say anything. Just look." tap, light flips warm
         (49.0,51.75),                             # L2 "prettiest vanity mirror" warm glow on her face
         (55.75,63.0),                             # L3 "don't have the space for a whole setup" pull back: small mirror on a desk
         (80.5,83.0),(52.5,55.5),(66.25,69.25),(2.0,5.0),  # L4 crystal design | LED lighting | 3 light settings | touch controls
         (41.5,45.5),(30.0,32.5),(37.5,40.0),      # L5 makeup | getting ready | space looks elevated
         (86.3,89.3)]                              # L6 "orange cart" end on the whole mirror
if os.environ.get("V")=="2": SEGS = SEGS2
GRADE = os.environ.get("GRADE", "eq=brightness=0.02:contrast=1.03")
def render(name="galental", preset="veryfast"):
    os.makedirs("out/parts",exist_ok=True); parts=[]
    for i,(a,b) in enumerate(SEGS):
        p=f"out/parts/{name}_{i}.mp4"; parts.append(p)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.3f}","-i",SRC,"-t",f"{b-a:.3f}","-vf",f"fps=30,scale=1080:1920:flags=lanczos,setsar=1,{GRADE}","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-r","30","-threads","4",p],check=True)
    open("out/parts/list.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
    out=f"out/{name}_v{os.environ.get("V","1")}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","out/parts/list.txt","-c","copy","-movflags","+faststart",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v{os.environ.get("V","1")}.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
