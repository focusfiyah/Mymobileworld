"""Gemstone teardrop bracelet (2026-11-06): hard-cut real footage, no sound (Grace adds music in TikTok). Source = Telegram copy 464x848."""
import subprocess, sys, json, os
SRC="orig/IMG_0346.MOV"
SEGS=[(3.5,6.0),(9.0,11.0),(17.0,19.0),(22.0,24.0),(35.0,37.0),(51.0,53.0)]
def render(name="bracelet"):
    f="".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
    f+="".join(f"[v{i}]" for i in range(len(SEGS)))+f"concat=n={len(SEGS)}:v=1:a=0[out]"
    os.makedirs("out",exist_ok=True); out=f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render()
