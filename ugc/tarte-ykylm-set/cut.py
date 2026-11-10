"""tarte YKYLM 8-piece set (2026-11-10): hard cut of Grace's original (1080x1920 HEVC 59.94), silent (she adds music in TikTok)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/hd.mov")
SEGS = [(0.0,0.45),(20.3,21.5),(22.8,24.0),(31.5,32.9),(38.7,39.9),(54.2,55.6),(65.0,66.2),(74.7,76.0),(96.8,98.0),(129.5,131.0)]
def render(name="tarte", preset="veryfast", crf="20"):
    ins, f = [], ""
    for i,(a,b) in enumerate(SEGS):
        ins += ["-ss",f"{a:.3f}","-t",f"{b-a:.3f}","-i",SRC]
        f += f"[{i}:v]fps=30,scale=1080:1920:flags=lanczos,setsar=1,setpts=PTS-STARTPTS[v{i}];"
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf",crf,"-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
