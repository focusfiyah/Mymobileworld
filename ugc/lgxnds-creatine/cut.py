"""Free cut: 9 hands-only clips on the trimmed Grace B voiceover, Classic hook caption over S1.

  python3 cut.py   -> out/lgxnds_creatine.mp4 (720x1280, 24fps)

Windows come from shots.json (vo.py). Every shot is real clip footage at 1.0x (no holds, no Ken Burns). Tub clips carry
the real label (label.py) on every frame.
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/ugc-product-ad/scripts"))
from classic_caption import classic_png

J = json.loads(Path("shots.json").read_text())
START = {"S3a": 1.42}   # S3a: Seedance turns the tub for frames 10-31, so start at 1.42 s (front-on again); S3 uses its first 1.5 s only (powder sinks later)
HOOK = "the last sip shouldn't crunch"
# S6 (label line) = the real listing packshot with a slow push-in, like Beet Root's label shot: Ralph's yes 2026-10-05
# ("can the label shot use the real product photo with a slow zoom?" -> "Yes"), an exception to hard rule 6 for this shot only.
SRC = {"S6": "clips/S6_real.mp4"}

Path("inserts").mkdir(exist_ok=True)
classic_png(HOOK, 720, 1280).save("inserts/hook.png")
inputs, chains, labels = [], [], []
for i, s in enumerate(J["shots"]):
    win = s["t"][1] - s["t"][0]; st = START.get(s["id"], 0.0)
    clip_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC.get(s["id"], f"clips/{s['id']}.mp4")],
                                    capture_output=True, text=True).stdout)
    assert st + win <= clip_len + 0.05, f"{s['id']} window {win:.2f}s needs more clip than {clip_len - st:.2f}s"
    inputs += ["-i", SRC.get(s["id"], f"clips/{s['id']}.mp4")]
    chains.append(f"[{i}:v]trim=start={st}:duration={win:.3f},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[v{i}]")
    labels.append(f"[v{i}]")
n = len(J["shots"]); total = J["shots"][-1]["t"][1]; hook_end = J["shots"][0]["t"][1]
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]")
inputs += ["-i", "inserts/hook.png"]
chains.append(f"[c0][{n}:v]overlay=0:0:enable='lt(t,{hook_end})'[c1]")
chains.append("[c1]format=yuv420p[vout]")
inputs += ["-i", "vo/voiceover_tight.mp3"]
chains.append(f"[{n + 1}:a]apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/lgxnds_creatine_v2.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out, total)
