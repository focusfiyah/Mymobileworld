"""QC sheet for a clip: 8 frames across the clip + max frame-to-frame jump (flicker). python3 qc/sheet.py clips/X.mp4 OUT.jpg"""
import subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw
f, out = sys.argv[1], sys.argv[2]
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip().split(","))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", "scale=180:320", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 320, 180).astype(float)
jumps = np.abs(np.diff(fr.mean(axis=(1, 2))))
ts = [round(i * (d - 0.1) / 7, 2) for i in range(8)]
ims = []
for t in ts:
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", "scale=360:-1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    import io; ims.append(Image.open(io.BytesIO(p)).convert("RGB"))
W = Image.new("RGB", (360 * 4, (ims[0].height + 24) * 2), "white"); dr = ImageDraw.Draw(W)
for k, (t, im) in enumerate(zip(ts, ims)):
    x, y = 360 * (k % 4), (ims[0].height + 24) * (k // 4); W.paste(im, (x, y + 24)); dr.text((x + 4, y + 6), f"{t:.1f}s", fill="black")
W.save(out, quality=85)
print(json.dumps({"clip": f, "dur": round(d, 2), "size": [w, h], "frames": len(fr), "max_jump": round(float(jumps.max()), 2), "at_frame": int(jumps.argmax())}))
