"""House of Rameau version (Ralph 2026-10-29: HofR keeps the hook text, no captions): same VO and words as cut.py, own framing
(1.15x crops), other in-points, cooler brighter grade, hook card from frame 0 to 3.0 s. Posts only on Ralph's OK.
NovaTabz 15 s cut (2026-10-30), from ugc/heveblue-eye-cream/cut.py: clean clip windows on the Grace cloned v5 voiceover,
no text, no music (none planned in the BOOK), AI finish last. Every clip plays at 1.0x from its start.
  python3 cut.py [VO]   -> out/novatabz_v1_review.mp4 (veryfast) + out/novatabz_v1.mp4 (AI finish)
Shot windows: shots.json "t" from vo.py; S4/S5 moved by hand (S5's clip is clean only for its first 1.85 s)."""
import json, subprocess, sys
from pathlib import Path

VO = sys.argv[1] if len(sys.argv) > 1 else "vo/voiceover_paced.mp3"
HOLD = 0.4
S = json.load(open("shots.json"))["shots"]
NAME = "novatabz_hor_v1"
SRC = {"S1": 0.4, "S2": 0.8, "S3": 1.0, "S4": 0.2, "S5": 0.0, "S6": 0.3}   # S5 stays at 0: clean only 0-1.85 s
CROP = {"S1": "crop=940:1671:0:110,", "S2": "crop=940:1671:140:200,", "S3": "crop=940:1671:70:40,", "S4": "crop=940:1671:140:170,", "S5": "crop=940:1671:0:120,", "S6": "crop=940:1671:70:90,"}
starts = [s["t"][0] for s in S]
END_VO = S[-1]["t"][1]
EDIT, pos = [], 0.0
for k, s in enumerate(S):
    b = starts[k + 1] if k + 1 < len(S) else END_VO + HOLD
    d = b - pos
    clip = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"clips/{s['id']}.mp4"], capture_output=True, text=True).stdout)
    ss = SRC[s["id"]]
    assert ss + d <= clip + 0.01, f"{s['id']} needs {ss + d:.2f} s, clip is {clip:.2f} s (never stretch)"
    EDIT.append((s["id"], ss, d)); pos += d
for e in EDIT: print(e[0], f"len {e[2]:.2f}")
END = pos
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f"clips/{c}.mp4"]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920,{CROP[c]}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.025:contrast=1.04:saturation=1.04,colorbalance=bs=0.04:rs=-0.03[g];[g][{n+1}:v]overlay=0:0:enable='lt(t,3.0)'[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO, "-af", f"aresample=44100,loudnorm=I=-16:TP=-2.5:LRA=11,apad,atrim=0:{END:.3f}", "-ar", "44100", "out/_vo.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", "out/_vo.wav", "-i", "out/hor_hook.png", "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"out/{NAME}_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"out/{NAME}_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s")
