"""Christmas Cheer cut (2026-10-30): each shot = its clip from IN for the VO line's window (1.0x, never stretched), 1080x1920,
Grace's VO on top, 0.6 s tail on the end shot, then ai_finish.sh. No text, no music.  python3 cut.py [--final]"""
import json, subprocess, sys
from pathlib import Path
W = json.load(open("vo/windows.json")); win = W["windows"]; TAIL = 0.6
IN = {"S1": 0.0, "S2": 0.3, "S3": 0.0, "S4": 1.0, "S5": 0.5, "S6": 1.6, "S7": 0.0}   # picked from the frame strips
Path("out").mkdir(exist_ok=True); Path("tmp").mkdir(exist_ok=True); parts = []
for i, (a, b) in enumerate(win):
    sid = f"S{i + 1}"; d = b - a + (TAIL if i == len(win) - 1 else 0)
    src = f"clips/{sid}.mp4"
    clip_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    assert IN[sid] + d <= clip_len + 0.01, f"{sid}: needs {IN[sid] + d:.2f}s of a {clip_len:.2f}s clip (would stretch)"
    out = f"tmp/{sid}.mp4"; parts.append(out)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(IN[sid]), "-i", src, "-t", f"{d:.3f}", "-an",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", out], check=True)
Path("tmp/list.txt").write_text("".join(f"file '{Path(p).name}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "tmp/list.txt", "-i", "vo/voiceover_final.mp3",
                "-map", "0:v", "-map", "1:a", "-af", f"apad=pad_dur={TAIL}", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k", "-threads", "4", "out/cut_raw.mp4"], check=True)
fin = Path(__file__).resolve().parents[2] / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"
subprocess.run(["bash", str(fin), "out/cut_raw.mp4", "out/christmas_cheer_v1.mp4"], check=True)
print("CUT_OK out/christmas_cheer_v1.mp4")
