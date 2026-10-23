"""Cut r1 (2026-10-23): clip windows on the Grace cloned voiceover (vo/voiceover_paced.mp3, windows from shots.json via vo.py),
no text, every clip at 1.0x, AI finish last.  python3 cut.py -> out/flashlight_v2_r1.mp4 (+ out/_raw.mp4)
S5 flicker is made free by tools/flicker.py (BOOK: "flicker added free in the edit"): the beam and lens dim every other 1/6 s,
about 3 blinks a second; the side panel stays off."""
import subprocess
from pathlib import Path

VO = "vo/voiceover_paced.mp3"
END = 22.60   # voice ends 22.11; hold the last shot a beat
EDIT = [   # (clip, src_start, dur, line)
    ("S1", 0.00, 2.02, "Who in the world made this"),
    ("S2", 0.00, 2.72, "charge my phone"),
    ("S3", 0.00, 2.22, "hang it up in my tent"),
    ("S4", 0.30, 3.20, "focused beam"),
    ("S5_flicker", 0.00, 2.72, "flickering mode (tools/flicker.py)"),
    ("S6", 0.00, 3.44, "camping gear"),
    ("S7", 2.00, 1.24, "or emergency kit (into the pouch)"),
    ("S8", 1.00, 2.56, "less than a Happy Meal (stands it on the table)"),
    ("S9", 1.00, 2.48, "orange cart (clips it to the strap)"),
]
assert abs(sum(e[2] for e in EDIT) - END) < 0.02, sum(e[2] for e in EDIT)
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d, _) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f"clips/{c}.mp4"]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,trim=duration={d:.3f},setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", VO, "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-af", f"apad,atrim=0:{END}", "-t", f"{END}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/_raw.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the bitrate cap from PLAYBOOK §6
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/_raw.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/flashlight_v2_r1.mp4"], check=True)
print("out/flashlight_v2_r1.mp4")
