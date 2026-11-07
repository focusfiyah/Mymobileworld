"""V3 cut: 6 clips x 2.0 s (12 s), Grace's text (v3/overlay/text.png) on every frame from frame 0, silent track (Grace adds
the song in TikTok), then the AI finish. Windows avoid each clip's jumps (frame-diff checked).
  python3 v3/cut_v3.py [--review]   (--review = veryfast preset)"""
import json, subprocess, sys
from pathlib import Path
WIN = json.loads(Path("v3/windows.json").read_text())   # {"S1": [start, end], ...}
ORDER = ["S1", "S2", "S3", "S4", "S5", "S6"]
preset = "veryfast" if "--review" in sys.argv else "medium"
Path("v3/parts").mkdir(exist_ok=True)
for s in ORDER:
    a, b = WIN[s]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", f"{b - a:.3f}", "-i", f"clips/v3_{s}.mp4",
                    "-vf", "scale=1080:1920:flags=lanczos,fps=30,setsar=1", "-an", "-c:v", "libx264", "-preset", preset, "-crf", "16",
                    "-threads", "4", f"v3/parts/{s}.mp4"], check=True)
Path("v3/parts/list.txt").write_text("".join(f"file '{s}.mp4'\n" for s in ORDER))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "v3/parts/list.txt", "-i", "v3/overlay/text.png",
                "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto[v]", "-map", "[v]", "-map", "2:a", "-shortest",
                "-c:v", "libx264", "-preset", preset, "-crf", "17", "-pix_fmt", "yuv420p", "-threads", "4", "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart", "v3/cut_v3_raw.mp4"], check=True)
fin = Path(__file__).resolve().parents[3] / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"
subprocess.run(["bash", str(fin), "v3/cut_v3_raw.mp4", "v3/cut_v3.mp4"], check=True)
print("CUT_OK v3/cut_v3.mp4")
