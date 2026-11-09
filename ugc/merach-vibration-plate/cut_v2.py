"""Merach V2 (2026-11-09): Grace's own script (research/grace_script.txt), cut from her HD original, silent so she records the VO over it.
Times are HD-file seconds. zoom = punch-in (1.0 = full frame), cy = vertical centre of the crop (0-1). Line durations estimated at ~3.3 words/s;
re-time to her real VO when she sends it. Different from V1: new windows, punch-in framing, new order, lighter grade."""
import subprocess, sys, json
SRC = "orig/hd.mov"
SHOTS = [  # (start, dur, zoom, cy, line)
 (43.4, 1.6, 1.25, 0.62, 1, "You're not lazy."),
 (2.75, 1.0, 1.15, 0.45, 2, "Your workout routine is just too complicated."),
 (3.75, 2.0, 1.15, 0.45, 3, "You need simple options to make fitness easier like this vibration plate."),
 (7.0, 2.0, 1.2, 0.45, 3, ""),
 (67.0, 1.5, 1.1, 0.5, 4, "It adds daily movement without planning an entire workout."),
 (46.1, 0.9, 1.15, 0.5, 4, ""),
 (12.7, 1.9, 1.1, 0.5, 5, "You can adjust the vibration settings,"),
 (57.0, 1.6, 1.15, 0.5, 6, "and it comes with stretching straps so you can get creative with how you use it. [PLACEHOLDER: strap shot from Grace]"),
 (8.6, 1.4, 1.0, 0.5, 6, ""),
 (63.6, 1.3, 1.1, 0.5, 6, ""),
 (45.2, 1.5, 1.0, 0.5, 7, "This might be the home fitness upgrade you've been missing."),
 (69.0, 1.3, 1.15, 0.45, 7, ""),
 (71.4, 1.4, 1.15, 0.55, 8, "It's in the orange cart!"),
]
GRADE = "eq=brightness=0.02:contrast=1.04:saturation=0.97"
def render(preset="veryfast", out="out/merachv2_v1.mp4"):
    f = ""
    for i,(a,d,z,cy,_,_) in enumerate(SHOTS):
        w, h = int(1080/z)//2*2, int(1920/z)//2*2
        y = int(min(max(0, cy*1920 - h/2), 1920-h))
        f += f"[0:v]trim={a:.3f}:{a+d:.3f},setpts=PTS-STARTPTS,fps=30,crop={w}:{h}:(iw-{w})/2:{y},scale=1080:1920:flags=lanczos,{GRADE},setsar=1[v{i}];"
    f += "".join(f"[v{i}]" for i in range(len(SHOTS))) + f"concat=n={len(SHOTS)}:v=1:a=0[out]"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","20","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    t=0; marks=[]
    for a,d,z,cy,ln,txt in SHOTS:
        if txt: marks.append((round(t,2),ln,txt))
        t+=d
    json.dump({"src":SRC,"shots":SHOTS,"expected":round(t,2),"line_starts":marks},open(out.replace(".mp4",".json"),"w"),indent=1); print(out, round(t,2))
if __name__=="__main__": render(*sys.argv[1:])
