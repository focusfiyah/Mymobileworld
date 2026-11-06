"""Kids chef cooking set (2026-11-06): hard-cut real footage, silent (Grace adds music in TikTok). SRC = original; swap to the full-quality file when Grace uploads it (same timeline)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/IMG_0349.MOV")
CUTS = {"chef_set": (SRC, [
 (0.0,1.4),(4.4,5.6),(10.0,11.4),(14.8,16.0),(18.0,19.2),(22.0,23.0),
 (26.0,27.2),(28.5,29.7),(32.0,33.2),(34.5,35.5),(36.4,37.6),(40.0,41.4)])}
def render(name):
    src, segs = CUTS[name]
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1[v{i}];" for i,(a,b) in enumerate(segs))
    f += "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset","medium","-crf","23","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"segs":segs,"expected":round(sum(b-a for a,b in segs),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__":
    for n in (sys.argv[1:] or CUTS): render(n)
