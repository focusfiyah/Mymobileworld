"""Clip QC (free): python3 qc/clip_qc.py V1S2 ... -> qc/sheets/<id>.jpg (8 frames across the clip, first frame vs still) and
motion per second (mean abs frame diff on a 90x160 grey copy; < 0.6 = frozen, flags a still stretch)."""
import subprocess, sys, numpy as np
from pathlib import Path
from PIL import Image
Path("qc/sheets").mkdir(parents=True, exist_ok=True)
for cid in sys.argv[1:]:
    f = f"clips/{cid}.mp4"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", "scale=90:160", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 160, 90).astype(float); n = len(fr)
    d = np.abs(np.diff(fr, axis=0)).mean((1, 2)); per = [round(float(d[i:i + 24].mean()), 2) for i in range(0, len(d), 24)]
    idx = np.linspace(0, n - 1, 8).astype(int); tiles = []
    for i in idx:
        im = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", f"select=eq(n\\,{i}),scale=270:480", "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        import io; tiles.append(Image.open(io.BytesIO(im)).convert("RGB"))
    s = Image.new("RGB", (270 * 8, 480)); [s.paste(t, (k * 270, 0)) for k, t in enumerate(tiles)]
    s.save(f"qc/sheets/{cid}.jpg", quality=80)
    print(cid, f"{n} frames", "motion/s", per, "FROZEN?" if min(per) < 0.6 else "")
