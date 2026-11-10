"""ili New York Double Flap Eyeglass Case (2026-11-10): hard-cut Grace's real original (1080x1920 60 fps HEVC), silent (she adds music in TikTok).
Shots: sunglasses out of front pocket (hook) / both flaps open side view = 2 pockets / magnetic snap flap opens /
eyeglasses out of back pocket / inside both compartments / leather grain close-up / closed front."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/ili.mov")
SEGS = [(26.0,28.75),(90.0,92.0),(18.5,20.3),(51.0,53.6),(86.0,88.0),(95.0,95.65),(63.0,65.0)]
def render(name="ili", preset="veryfast"):
    os.makedirs("out/seg", exist_ok=True); parts=[]
    for i,(a,b) in enumerate(SEGS):
        p=f"out/seg/{name}_{i}.mp4"; parts.append(p)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.3f}","-i",SRC,"-t",f"{b-a:.3f}","-vf","fps=30,scale=1080:1920:flags=lanczos,setsar=1",
            "-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-threads","4",p],check=True)
    open("out/seg/list.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","out/seg/list.txt","-c","copy","-movflags","+faststart",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
