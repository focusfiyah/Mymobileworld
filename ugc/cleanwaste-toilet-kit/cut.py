"""V1 cut: one clip per shot, cut on the voiceover word times (vo/windows.json), no text, no overlays.
  python3 cut.py            review render (veryfast) -> out/cleanwaste_v1_review.mp4
  python3 cut.py --final    + AI finish (PLAYBOOK §6: grain 6, unsharp 0.6, saturation 0.92, bitrate capped) -> out/cleanwaste_v1.mp4
Each clip is used from OFFSET[s] for its window (all windows <= 5 s, so every clip plays at 1.0x); the last shot runs TAIL s past the
last word so the video ends on a visual beat."""
import json, subprocess, sys
from pathlib import Path
W = json.load(open("vo/windows.json")); TAIL = 0.6
OFFSET = {}   # per-shot start inside its clip (s), set after QC if a clip's best window is later
Path("out").mkdir(exist_ok=True); Path("tmp").mkdir(exist_ok=True)
prev, parts = 0.0, []
for k, w in enumerate(W):
    d = w["cut"] - prev + (TAIL if k == len(W) - 1 else 0); prev = w["cut"]
    o = f"tmp/{w['id']}.mp4"; parts.append(o)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(OFFSET.get(w["id"], 0)), "-i", f"clips/{w['id']}.mp4", "-t", f"{d:.3f}",
                    "-vf", "scale=1080:1920:flags=lanczos,fps=30,setsar=1", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", o], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", o], capture_output=True, text=True).stdout)
    assert dur >= d - 0.05, f"{w['id']}: clip too short ({dur:.2f} < {d:.2f}): never stretch footage"
inputs = sum((["-i", p] for p in parts), []) + ["-i", "vo/voiceover_tight.wav"]
fc = "".join(f"[{i}:v]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[v];[{len(parts)}:a]apad=pad_dur={TAIL},afade=t=out:st={prev:.3f}:d={TAIL}[a]"
review = "out/cleanwaste_v1_review.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{prev + TAIL:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", review], check=True)
print("review", review)
if "--final" in sys.argv:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", review, "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                    "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-movflags", "+faststart", "out/cleanwaste_v1.mp4"], check=True)
    print("final out/cleanwaste_v1.mp4")
