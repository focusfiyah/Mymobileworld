"""Niagara topper cut (2026-10-30): each shot = its VO window from shots.json "t", trimmed from the clip's clean part,
scaled to 1080x1920 (never slowed), Grace VO over it, 1.0 s hold on S8 after the last word. Bright neutral, no text.
  python3 cut.py [--preset veryfast] -> out/niagara_topper_r1.mp4 (then ai_finish.sh -> out/niagara_topper_v1.mp4)"""
import json, subprocess, sys
S = json.load(open("shots.json"))["shots"]
SRC = {"S1": ("clips/S1_seedance.mp4", 0.0), "S2": ("clips/S2_seedance.mp4", 0.3), "S3": ("clips/S3.mp4", 0.0),
       "S4": ("clips/S4.mp4", 0.2), "S5": ("clips/S5.mp4", 0.3), "S6": ("clips/S6.mp4", 0.0),
       "S7": ("clips/S7.mp4", 0.0),   # only the first 2.3 s: the push-in after that invents navy pillows
       "S8": ("clips/S8.mp4", 0.0)}
TAIL = 1.0; preset = sys.argv[sys.argv.index("--preset") + 1] if "--preset" in sys.argv else "medium"
inp, fl = [], []
for k, s in enumerate(S):
    a, b = s["t"]; d = b - a + (TAIL if k == len(S) - 1 else 0)
    f, ss = SRC[s["id"]]
    if s["id"] == "S7": assert ss + d <= 2.35, d
    inp += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f]
    fl.append(f"[{k}:v]scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p[v{k}]")
n = len(S); vo = len(S)
f = ";".join(fl) + ";" + "".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0[v];[{vo}:a]apad=pad_dur={TAIL}[a]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *inp, "-i", "vo/voiceover_paced.mp3", "-filter_complex", f, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", preset, "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-shortest",
                "-movflags", "+faststart", "out/niagara_topper_r1.mp4"], check=True)
print("cut out/niagara_topper_r1.mp4")
