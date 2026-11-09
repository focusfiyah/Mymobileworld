"""Pinmoco cross-leg chair (2026-11-08): hard-cut of Grace's real footage, silent (Grace adds music in TikTok, as on the Kids Kitchen Set / outfit edits).
SRC = Telegram copy (draft); for the HD cut run SRC=orig/<her original> python3 cut.py (same timeline, check the times first if her original is trimmed differently)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/tg_786406594.mp4")
TAG = os.environ.get("TAG", "v1")
OFF = float(os.environ.get("OFFSET", "0"))  # HD original runs ~0.08 s ahead of the Telegram copy (frame match 2026-11-09)
SEGS = [
 (1.0,2.6),    # hook: nursing, sitting cross-legged on the wide seat
 (12.6,14.0),  # side angle: cross-legged at the desk with baby
 (18.2,19.6),  # baby sits on the cloud footstool between her legs
 (24.0,25.0),  # legs down, baby on the footstool
 (27.3,28.2),  # baby walks up to camera (fun beat)
 (44.0,45.0),  # chair + footstool, hand on the heart backrest
 (50.0,51.8),  # she swings the footstool around (it rolls on its own)
 (56.4,57.8),  # seat swivels
 (67.5,68.8),  # hand presses the teddy seat
 (74.0,75.4),  # hand on the heart backrest
 (82.6,83.4),  # hand presses the seat, feet on the floor for scale
 (93.5,95.7)]  # close: chair + footstool overview
def render():
    f = "".join(f"[0:v]trim={a+OFF:.3f}:{b+OFF:.3f},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/chair_{TAG}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/chair_{TAG}.json","w")); print(out)
render()
