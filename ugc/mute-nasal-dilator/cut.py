"""Free cut: 7 hands-only clips on the trimmed Grace B voiceover, no text overlay (Ralph has not asked for one).

  python3 cut.py   -> out/mute_nasal_dilator_r4.mp4 (720x1280, 24fps)

Windows come from shots.json (vo.py). Every shot is real clip footage at 1.0x (no holds, no Ken Burns). 
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/ugc-product-ad/scripts"))

J = json.loads(Path("shots.json").read_text())
# ordered plan: (shot id, clip start, window start, window end). S0 (dilator held up) opens on hook line 1, S1 pillow shot finishes it.
PLAN = [("S0", 0.0, 0.0, 2.6), ("S1", 0.0, 2.6, 5.16), ("S2", 0.0, 5.16, 8.5), ("S3", 0.0, 8.5, 13.24), ("S4", 0.0, 13.24, 14.74),
        ("S4b", 2.5, 14.74, 16.18), ("S5", 0.0, 16.18, 20.66), ("S6", 0.0, 20.66, 24.5), ("S7", 0.0, 24.5, 29.91)]
# S4b: same clip after the box under the tray melts away (clip 1.6-2.4 s skipped, Ralph 2026-10-10 "why does the box disappear")
SRC = {"S3": "fix/S3_fixed.mp4", "S4": "fix/S4_hybrid.mp4", "S4b": "clips/S4.mp4", "S7": "fix/S7_fixed.mp4"}   # real box print pasted over the AI box (boxfix.py)

Path("inserts").mkdir(exist_ok=True)
inputs, chains, labels = [], [], []
for i, (sid, st, t0, t1) in enumerate(PLAN):
    win = t1 - t0; src = SRC.get(sid, f"clips/{sid}.mp4")
    clip_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    assert st + win <= clip_len + 0.05, f"{sid} window {win:.2f}s needs more clip than {clip_len - st:.2f}s"
    inputs += ["-i", src]
    chains.append(f"[{i}:v]trim=start={st}:duration={win:.3f},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[v{i}]")
    labels.append(f"[v{i}]")
n = len(PLAN); total = PLAN[-1][3]
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]")
chains.append("[c0]format=yuv420p[vout]")
inputs += ["-i", "vo/voiceover_tight.mp3"]
chains.append(f"[{n}:a]apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/mute_nasal_dilator_r4.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out, total)
