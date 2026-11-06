"""Grace outfit edits (2026-11-06): hard-cut real footage, no sound (Grace adds music in TikTok)."""
import subprocess, sys, json
CUTS = {
 "kids_set": ("orig/f0bc.mov", [  # 10-piece set, 5 colours then ribbed fabric
   (0.0,0.9),(5.0,7.0),(10.0,12.0),(18.0,20.0),(21.0,23.0),(24.0,25.5),
   (29.0,31.0),(54.0,56.0),(57.0,58.8),(62.3,63.6)]),
 "sweater": ("orig/a3c3.mov", [  # striped V-neck + brown wide-leg pants
   (1.0,2.6),(7.2,9.0),(18.2,20.2),(27.0,28.6),(32.0,33.6),(52.0,53.5)]),
}
def render(name):
    src, segs = CUTS[name]
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920,setsar=1[v{i}];" for i,(a,b) in enumerate(segs))
    f += "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an",
        "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"segs":segs,"expected":round(sum(b-a for a,b in segs),2)},open(f"out/{name}_v1.json","w"))
    print(out)
if __name__=="__main__":
    import os; os.makedirs("out",exist_ok=True)
    for n in (sys.argv[1:] or CUTS): render(n)
