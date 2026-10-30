"""House of Rameau version (Ralph 2026-10-29: HofR keeps the hook text, no captions), copied from ugc/novatabz-tablets/cut_hor.py:
same Grace VO as cut.py, own framing (1.15x crops), other in-points, cooler brighter grade, hook card "Don't buy a new mattress yet"
(modeled on @hammyk6 55.1M's opener) from frame 0 to 3.0 s, AI finish with the PLAYBOOK §6 bitrate cap. Posts only on Ralph's OK.
  python3 cut_hor.py -> out/niagara_hor_v1.mp4"""
import json, subprocess
from pathlib import Path
S = json.load(open("shots.json"))["shots"]; NAME = "niagara_hor_v1"; HOLD = 1.0
FILE = {"S1": "clips/S1_seedance.mp4", "S2": "clips/S2_seedance.mp4"}
SRC = {"S1": 0.3, "S2": 0.0, "S3": 0.4, "S4": 0.5, "S5": 0.6, "S6": 0.5, "S7": 0.0, "S8": 0.3}   # S7 stays at 0: clean only 0-2.35 s
CROP = {"S1": "crop=940:1671:140:120,", "S2": "crop=940:1671:70:0,", "S3": "crop=940:1671:0:200,", "S4": "crop=940:1671:140:60,",
        "S5": "crop=940:1671:70:150,", "S6": "crop=940:1671:0:100,", "S7": "crop=940:1671:70:120,", "S8": "crop=940:1671:140:200,"}
EDIT = []
for k, s in enumerate(S):
    d = s["t"][1] - s["t"][0] + (HOLD if k == len(S) - 1 else 0); f = FILE.get(s["id"], f"clips/{s['id']}.mp4")
    clip = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    lim = 2.35 if s["id"] == "S7" else clip + 0.01
    assert SRC[s["id"]] + d <= lim, f"{s['id']} needs {SRC[s['id']] + d:.2f} s of {lim:.2f} (never stretch)"
    EDIT.append((s["id"], f, SRC[s["id"]], d))
END = sum(e[3] for e in EDIT); inputs, chains = [], []
for i, (c, f, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920,{CROP[c]}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.025:contrast=1.04:saturation=1.04,colorbalance=bs=0.04:rs=-0.03[g];[g][{n+1}:v]overlay=0:0:enable='lt(t,3.0)'[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo/voiceover_paced.mp3", "-af", f"aresample=44100,apad,atrim=0:{END:.3f}", "-ar", "44100", "out/_vo.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", "out/_vo.wav", "-i", "out/hor_hook.png", "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"out/{NAME}_review.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"out/{NAME}_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s")
