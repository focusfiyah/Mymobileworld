"""Luvum gel mask edit (2026-11-06): hard-cut Grace's real footage, silent. SRC set by argv[1] (default orig/IMG_0347.MOV)."""
import subprocess, sys, json, os
SEGS = [(0.5,2.0),(2.5,4.0),(4.9,6.5),(9.5,11.0),(12.0,13.2),(14.3,15.8),(15.8,17.0),(19.2,20.5)]
def render(src, name="luvum", w=1080, h=1920):
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    os.makedirs("out",exist_ok=True); out=f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(sys.argv[1] if len(sys.argv)>1 else "orig/IMG_0347.MOV")
