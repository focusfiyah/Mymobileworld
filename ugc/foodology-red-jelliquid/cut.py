"""12 s music-only cut (no VO, no text). python3 cut.py [v1] -> out/cut_v1_raw.mp4, then ai_finish -> out/cut_v1.mp4"""
import subprocess, sys
from pathlib import Path
V = sys.argv[1] if len(sys.argv) > 1 else "v1"
# (clip, start, duration): clean windows from QC 2026-11-03 (S4 grip change after 1.8 s; S3/S6 = Wan r2)
SEG = [("clips/S1.mp4", 0.0, 2.0), ("clips/S2.mp4", 1.0, 2.0), ("clips/S3.mp4", 0.5, 2.0),
       ("clips/S4.mp4", 0.0, 1.8), ("clips/S5_seedance.mp4", 0.0, 2.0), ("clips/S6.mp4", 1.5, 2.2)]
Path("out").mkdir(exist_ok=True); parts = []
for i, (c, ss, d) in enumerate(SEG):
    o = f"out/seg{i}.mp4"; parts.append(o)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", c, "-t", str(d), "-an",
                    "-vf", "scale=1080:1920:flags=lanczos,setsar=1,fps=30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
                    "-pix_fmt", "yuv420p", "-threads", "4", o], check=True)
Path("out/list.txt").write_text("".join(f"file '{Path(p).name}'\n" for p in parts))
raw = f"out/cut_{V}_raw.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/list.txt", "-c", "copy", raw], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", raw, f"out/cut_{V}.mp4"], check=True)
print("OK", f"out/cut_{V}.mp4")
