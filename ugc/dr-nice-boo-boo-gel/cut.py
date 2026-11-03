"""Cut V1 (12.0 s, music only: no audio track, Ralph adds music). Windows follow shots.json line timing.
  python3 cut.py  -> out/V1_raw.mp4, out/V1.mp4 (AI finish)"""
import subprocess, json
from pathlib import Path
# (clip, start in clip, length): length = the shot's line window in shots.json
EDL = [("S1", 0.0, 2.4), ("S2_seedance", 0.5, 1.8), ("S3_seedance", 0.4, 2.1), ("S4", 0.0, 2.1), ("S5", 1.4, 2.2), ("S6", 0.3, 1.4)]
Path("out").mkdir(exist_ok=True); parts = []
for i, (c, ss, d) in enumerate(EDL):
    p = f"out/part{i}.mp4"; parts.append(p)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", f"clips/{c}.mp4", "-t", str(d), "-an",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", p], check=True)
Path("out/list.txt").write_text("".join(f"file '{Path(p).name}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/list.txt", "-c", "copy", "out/V1_raw.mp4"], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", "out/V1_raw.mp4", "out/V1.mp4"], check=True)
