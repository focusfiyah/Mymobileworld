"""COSRX Peptide Lip Care (2026-11-11): hard-cut Grace's HD original, silent (her clip has no voice; she adds music in TikTok)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/CosrxLipTintCare.mov")
# tint going on lips (hook), label close-up, swatch on hand, glossy pout, kiss, points at her lips
SEGS = [(17.5,20.0),(123.6,126.4),(142.0,144.5),(53.75,56.0),(63.0,65.5),(107.0,109.4)]
GRADE = os.environ.get("GRADE", "eq=brightness=0.02:contrast=1.03")
def render(name="cosrx", preset="veryfast"):
    os.makedirs("out/segs",exist_ok=True); parts=[]
    for i,(a,b) in enumerate(SEGS):
        p=f"out/segs/{name}_{i}.mp4"; parts.append(p)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.3f}","-i",SRC,"-t",f"{b-a:.3f}","-vf",f"fps=30,scale=1080:1920:flags=lanczos,setsar=1,{GRADE}","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-threads","4",p],check=True)
    open("out/segs/list.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","out/segs/list.txt","-c","copy","-movflags","+faststart",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
