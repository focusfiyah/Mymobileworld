"""Magnesium Night Trio cut (2026-10-30): each clip trimmed to its VO window (shots.json t, from vo.py), 1080x1920 30 fps,
Grace's paced VO on top, 0.5 s hold on the end shot, no text, no music. Then ai_finish.sh (last step).
  python3 cut.py  -> out/magnesium_trio_raw.mp4, out/magnesium_trio.mp4"""
import json, subprocess
from pathlib import Path
S = json.load(open("shots.json"))
OFF = {"S2": 1.0, "S5": 0.3, "S6": 0.6}   # where in each clip the window starts (the action the words name)
HOLD = 0.5
Path("out").mkdir(exist_ok=True); Path("out/parts").mkdir(exist_ok=True)
parts = []
for i, s in enumerate(S):
    a, b = s["t"]; d = b - a + (HOLD if i == len(S) - 1 else 0)
    o = f"out/parts/{s['id']}.mp4"; parts.append(o)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(OFF.get(s["id"], 0)), "-i", f"clips/{s['id']}.mp4", "-t", f"{d:.3f}",
                    "-vf", "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p", "-an", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "18", o], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", o], capture_output=True, text=True).stdout)
    assert dur >= d - 0.05, f"{s['id']} clip too short: {dur:.2f} < {d:.2f} (never stretch footage)"
Path("out/parts/list.txt").write_text("".join(f"file '{Path(p).name}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/parts/list.txt", "-i", "vo/voiceover_paced.mp3",
                "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
                "-af", "apad", "-shortest", "out/magnesium_trio_raw.mp4"], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", "out/magnesium_trio_raw.mp4", "out/magnesium_trio.mp4"], check=True)
print("CUT_OK out/magnesium_trio.mp4")
