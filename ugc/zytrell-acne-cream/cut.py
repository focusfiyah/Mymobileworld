"""ZYTRELL cut (2026-11-02): silent 10-12 s, music added later by Ralph. No text, no VO.
Windows: clip in/out seconds per shot (S3 = Ralph's tapped trim 2.1-3.9). Each piece -> 1080x1920 30 fps,
gentle neutral grade, then concat, then ai_finish.sh (last step). Usage: python3 cut.py [v1]"""
import subprocess, sys
from pathlib import Path
V = sys.argv[1] if len(sys.argv) > 1 else "v1"
SHOTS = [("S1", 0.2, 2.4), ("S2", 0.3, 2.3), ("S3", 2.1, 3.9), ("S4", 0.3, 2.3), ("S5", 0.2, 2.6)]
out = Path("out"); seg = out / f"_seg_{V}"; seg.mkdir(parents=True, exist_ok=True)
VF = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=brightness=0.01:contrast=1.02,format=yuv420p"
parts = []
for sid, a, b in SHOTS:
    p = seg / f"{sid}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", f"clips/{sid}.mp4", "-an",
                    "-vf", VF, "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-threads", "4", str(p)], check=True)
    parts.append(p)
lst = seg / "list.txt"; lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
raw = out / f"zytrell_{V}_raw.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(raw)], check=True)
fin = out / f"zytrell_{V}.mp4"
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", str(raw), str(fin)], check=True)
print("CUT_OK", fin, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(fin)], capture_output=True, text=True).stdout.strip())
