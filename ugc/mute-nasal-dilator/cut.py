"""Free cut: 7 hands-only clips on the trimmed Grace B voiceover, no text overlay (Ralph has not asked for one).

  python3 cut.py   -> out/mute_nasal_dilator_r1.mp4 (720x1280, 24fps)

Windows come from shots.json (vo.py). Every shot is real clip footage at 1.0x (no holds, no Ken Burns). 
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/ugc-product-ad/scripts"))

J = json.loads(Path("shots.json").read_text())
START = {}
# shot windows (cuts on the action, every clip at 1.0x: no window longer than its clip): S3 only has 5.04 s so S4 starts 0.6 s into the S3 line
JOIN = {"S1": (0.0, 5.22), "S2": (5.22, 10.26), "S3": (10.26, 15.30), "S4": (15.30, 19.34), "S5": (19.34, 25.38), "S6": (25.38, 29.42), "S7": (29.42, 34.81)}
SRC = {"S3": "fix/S3_fixed.mp4", "S4": "fix/S4_fixed.mp4", "S7": "fix/S7_fixed.mp4"}   # real box print pasted over the AI box (boxfix.py)

Path("inserts").mkdir(exist_ok=True)
inputs, chains, labels = [], [], []
for i, s in enumerate(J["shots"]):
    s["t"] = list(JOIN.get(s["id"], s["t"])); win = s["t"][1] - s["t"][0]; st = START.get(s["id"], 0.0)
    clip_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC.get(s["id"], f"clips/{s['id']}.mp4")],
                                    capture_output=True, text=True).stdout)
    assert st + win <= clip_len + 0.05, f"{s['id']} window {win:.2f}s needs more clip than {clip_len - st:.2f}s"
    inputs += ["-i", SRC.get(s["id"], f"clips/{s['id']}.mp4")]
    chains.append(f"[{i}:v]trim=start={st}:duration={win:.3f},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[v{i}]")
    labels.append(f"[v{i}]")
n = len(J["shots"]); total = J["shots"][-1]["t"][1]
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]")
chains.append("[c0]format=yuv420p[vout]")
inputs += ["-i", "vo/voiceover_tight.mp3"]
chains.append(f"[{n}:a]apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/mute_nasal_dilator_r1.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out, total)
