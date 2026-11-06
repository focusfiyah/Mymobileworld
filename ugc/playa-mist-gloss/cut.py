"""PLAYA Perfume Mist + Gloss Rinse (2026-11-06): hard-cut Grace's real footage, silent (she adds music in TikTok)."""
import subprocess, sys, json, os
CUTS = {"playa": ("orig/IMG_0348.MOV", [
  (0.2,1.2),(2.0,4.4),(6.0,7.6),(10.8,12.6),(14.0,15.2),(19.0,20.4),(20.6,22.2),(24.0,25.4)])}
def render(name, src=None):
    s, segs = CUTS[name]; src = src or s
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1[v{i}];" for i,(a,b) in enumerate(segs))
    f += "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"segs":segs,"expected":round(sum(b-a for a,b in segs),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__":
    os.makedirs("out",exist_ok=True); render("playa")
