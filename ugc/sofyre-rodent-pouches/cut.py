"""Free cut: 11 clips on the trimmed Grace B voiceover, no text overlay (Ralph has not asked for one).

  python3 cut.py   -> out/sofyre_r1_raw.mp4 (720x1280, 24fps), then ai_finish.sh -> out/sofyre_r1.mp4

Windows come from shots.json (vo.py). Real clip footage, never slower than 1.0x. Per-shot source offsets / speed-ups:
S5 starts at 2.9s (the hand pressed the pouch flat with its palm before that; only the placed pouch is used).
S6 runs 1.6-4.9s at ~1.85x so "the garage, even the car" shows the pouch on the shelf and then the car.
"""
import json, subprocess
from pathlib import Path

J = json.loads(Path("shots.json").read_text())
SRC = {"S5": (2.9, None), "S6": (1.6, 4.9)}   # (start, end of source used); end None = start + window at 1.0x
inputs, chains, labels = [], [], []
for i, s in enumerate(J["shots"]):
    t0, t1 = s["t"]; win = t1 - t0; src = f"clips/{s['id']}.mp4"
    clip_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    a, b = SRC.get(s["id"], (0.0, None)); b = b or a + win
    assert b <= clip_len + 0.05, f"{s['id']} needs {b:.2f}s of a {clip_len:.2f}s clip"
    speed = (b - a) / win; assert speed >= 0.999, f"{s['id']} would be slowed to {speed:.2f}x"
    inputs += ["-i", src]
    chains.append(f"[{i}:v]trim=start={a:.3f}:end={b:.3f},setpts=(PTS-STARTPTS)/{speed:.4f},scale=720:1280,setsar=1,fps=24,trim=duration={win:.3f}[v{i}]")
    labels.append(f"[v{i}]"); print(s["id"], f"src {a:.2f}-{b:.2f}  win {win:.2f}  speed {speed:.2f}x")
n = len(J["shots"]); total = J["shots"][-1]["t"][1]
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]")
chains.append("[c0]format=yuv420p[vout]")
inputs += ["-i", "vo/voiceover_tight.mp3"]
chains.append(f"[{n}:a]apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/sofyre_r1_raw.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-threads", "4",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out, total)
