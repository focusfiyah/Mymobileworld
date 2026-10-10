"""Free fix: paste the REAL 'MOUNTAIN BREEZE' teal panel (refs/mb_front.png) over the AI panel, frame by frame.
The AI panel is found by its teal colour (largest teal blob); the real panel is resized to that box with a soft edge.
  python3 panel.py IN.mp4 OUT.mp4"""
import subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
def teal(a, r0=0, r1=None):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (g > r + 25) & (b > r + 30) & (r < 110) & (abs(b - g) < 60)
ref = np.asarray(Image.open("refs/mb_front.png").convert("RGB"))
sub = ref[590:760, 210:400]; ys, xs = np.nonzero(teal(sub))
REAL = Image.fromarray(sub[ys.min() + 4:ys.max() - 3, xs.min() + 4:xs.max() - 3])  # inset: drop the rounded orange corners
def box(a):
    m = teal(a); ys, xs = np.nonzero(m)
    if len(xs) < 400: return None
    cy, cx = np.median(ys), np.median(xs)          # keep the blob around the median (the panel), drop stray teal
    k = (abs(ys - cy) < 120) & (abs(xs - cx) < 120); ys, xs = ys[k], xs[k]
    return int(np.percentile(xs, 0.5)), int(np.percentile(ys, 0.5)), int(np.percentile(xs, 99.5)) + 1, int(np.percentile(ys, 99.5)) + 1
src, out = sys.argv[1], sys.argv[2]
tmp = Path(tempfile.mkdtemp())
subprocess.run(["ffmpeg", "-v", "error", "-i", src, str(tmp / "f%04d.png")], check=True)
fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
frames = sorted(tmp.glob("f*.png")); B = [box(np.asarray(Image.open(f).convert("RGB"))) for f in frames]
ok = [i for i, b in enumerate(B) if b]; arr = np.array([B[i] for i in ok], float)
W = 9   # temporal smoothing (median then mean over 9 frames) so the patch never jitters
med = np.array([np.median(arr[max(0, k - W // 2):k + W // 2 + 1], axis=0) for k in range(len(arr))])
sm = np.array([med[max(0, k - W // 2):k + W // 2 + 1].mean(axis=0) for k in range(len(med))]).round().astype(int)
n = 0
for k, i in enumerate(ok):
    im = Image.open(frames[i]).convert("RGB"); x0, y0, x1, y1 = sm[k]
    im.paste(REAL.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0)); im.save(frames[i]); n += 1
print("smoothed box jitter max:", np.abs(np.diff(sm, axis=0)).max(axis=0))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", fps, "-i", str(tmp / "f%04d.png"), "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
print("patched", n, "frames ->", out)
