"""Youtheory B12B6 cut (2026-10-26): Seedance first-frame clips on Grace's voiceover, no text, AI finish last.
  python3 cut.py            -> out/youtheory_b12b6_review.mp4 (veryfast) + out/youtheory_b12b6_v1.mp4 (AI finish)
Each shot's window = its line's time in vo/words_trimmed.json (vo.py writes shots.json "t"). Every clip plays at 1.0x.
S9: a foil glare sweeps the pouch from ~1.5 s, so only its first 1.3 s is used and S8 (pouch on the desk) runs on into
the CTA line ("Tap the orange cart...") until S9 cuts in for "grab yours while they're in stock"."""
import json, subprocess
from pathlib import Path

VO = "vo/voiceover_paced.mp3"
HOLD = 0.6                      # hold the last shot a beat after the voice ends
CLIP = 4.04                     # Seedance clip length (s)
S9_MAX = 1.3                    # clean S9 footage (QC 2026-10-26)
S = json.load(open("shots.json"))["videos"][0]["shots"]
EDIT = []
for k, s in enumerate(S):
    a, b = s["t"]; d = b - a + (HOLD if k == len(S) - 1 else 0)
    EDIT.append([s["id"], 0.0, d])
s9 = EDIT[-1]; extra = s9[2] - S9_MAX; s9[2] = S9_MAX; EDIT[-2][2] += extra     # S8 takes the start of the CTA line
for c, ss, d in EDIT:
    assert ss + d <= CLIP + 1e-6, f"{c} window {d:.2f} runs past its clip"
END = sum(e[2] for e in EDIT)
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f"clips/{c}_seedance.mp4"]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", VO, "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-af", f"apad,atrim=0:{END:.3f},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/youtheory_b12b6_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/youtheory_b12b6_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/youtheory_b12b6_v1.mp4"], check=True)
for c, ss, d in EDIT: print(c, round(d, 2))
print("out/youtheory_b12b6_v1.mp4", round(END, 2), "s")
