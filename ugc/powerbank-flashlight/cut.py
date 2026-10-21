"""Cut r3 (2026-10-21; r2 + new S1 with Grace's TikTok on the screen): clean clip windows on the Grace voiceover, no text, AI finish last.
  python3 cut.py   -> out/powerbank_flashlight_r3.mp4 (+ out/_raw.mp4 before the finish)
Edit list = (clip, source start, length); each line's window comes from vo/words_trimmed.json (vo.py).
Windows only use clean footage (QC 2026-10-21): S8 has a second flashlight from frame 0 and is not used;
S9 turns and morphs after ~2.4 s, so only its first 2.4 s are used. Every clip plays at 1.0x."""
import json, subprocess
from pathlib import Path

VO = "vo/voiceover_paced.mp3"
END = 33.18   # voice ends 32.91; hold the last shot a beat
EDIT = [   # (clip, src_start, dur, what it covers)
    ("S1_screen", 0.00, 5.04, "line 1, phone light (pointing away) dies, Grace's TikTok on the screen (v2, Ralph 2026-10-21)"),
    ("S2", 0.00, 3.78, "line 2, parking lot"),
    ("S3", 0.00, 4.04, "line 3, on the keys"),
    ("S4", 0.50, 2.58, "line 4, thumb presses the button, beam lands in front of the lens (v2 clip, Ralph 2026-10-21)"),
    ("S5", 0.00, 2.64, "line 5, hung in the tent"),
    ("S6", 0.00, 4.22, "line 6, charging the phone"),
    ("S7", 0.00, 3.46, "line 7, on the backpack"),
    ("S4", 3.08, 1.92, "line 8a 'clocks go back November first', S4's unused lit tail at dusk"),
    ("S5", 2.64, 1.56, "line 8b 'dark before dinner', S5's unused tent tail"),
    ("S9", 0.00, 2.40, "line 9, keys in the car (clean part only)"),
    ("S7", 3.46, 1.54, "line 10 'It's in the orange cart', one product"),
]
assert abs(sum(e[2] for e in EDIT) - END) < 0.02, sum(e[2] for e in EDIT)
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d, _) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f"clips/{c}.mp4"]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", VO, "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-af", f"apad,atrim=0:{END}", "-t", f"{END}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/_raw.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the bitrate cap from PLAYBOOK §6 (BodyJ: 202 MB -> 82 MB)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/_raw.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/powerbank_flashlight_r3.mp4"], check=True)
print("out/powerbank_flashlight_r3.mp4")
