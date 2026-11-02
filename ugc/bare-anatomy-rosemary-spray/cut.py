"""Bare Anatomy rosemary spray cut (2026-11-02), from earth-breeze-sheets/cut.py. Music-only video: no voiceover, no text,
a silent audio track so Grace can drop her music in. S7a dropped (REMOVED.md): the close is S7b then S7c. Every clip at 1.0x.
  python3 cut.py [--only S1,S2]  -> out/rosemary_v1_review.mp4 (veryfast) + out/rosemary_v1.mp4 (AI finish)"""
import subprocess, sys
from pathlib import Path

NAME = "rosemary_v3"
# (shot, source start in its 4 s clip, length); windows from scripts.md, S7 = S7b 0.8 s + S7c 1.2 s
EDIT = [("S1", 1.7, 2.0), ("S2", 0.8, 1.4), ("S3", 0.6, 1.6), ("S4", 0.5, 1.6), ("S5", 0.6, 1.4),
        ("S6", 0.6, 1.4), ("S7b", 0.0, 0.8), ("S7c", 0.4, 1.2)]
CROP = {}  # shot -> "crop=w:h:x:y," free fixes
only = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only")), None)
if only: EDIT = [e for e in EDIT if e[0] in only]
END = sum(d for _, _, d in EDIT)
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f"clips/{c}.mp4"]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,{CROP.get(c, '')}scale=1080:1920:flags=lanczos,eq=gamma=1.06,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-f", "lavfi", "-t", f"{END:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
                "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"out/{NAME}_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"out/{NAME}_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s")
