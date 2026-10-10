"""Free fix: paste the REAL Carpe Mountain Breeze label front (wordmark + badge + teal panel + UNDERARM/NET WT, refs/mb_front.png)
over the AI stick, frame by frame. Anchor = the teal panel (found by colour, position smoothed over 9 frames). The real label is
scaled from the panel size, its orange matched to the frame's orange, and only drawn over stick-coloured pixels, so fingers and
skin stay on top (never background or label through hands).
  python3 label.py IN.mp4 OUT.mp4 [--still IN.png OUT.png]"""
import subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
REF = np.asarray(Image.open("refs/mb_front.png").convert("RGB")).astype(float)
def teal(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (g > r + 25) & (b > r + 30) & (r < 110) & (abs(b - g) < 60)
def pbox(a, lim=None):
    m = teal(a)
    if lim is not None: m &= lim
    ys, xs = np.nonzero(m)
    if len(xs) < 300: return None
    cy, cx = np.median(ys), np.median(xs); k = (abs(ys - cy) < 120) & (abs(xs - cx) < 120); ys, xs = ys[k], xs[k]
    return np.array([np.percentile(xs, .5), np.percentile(ys, .5), np.percentile(xs, 99.5) + 1, np.percentile(ys, 99.5) + 1])
RP = pbox(REF.astype(np.uint8), lim=np.pad(np.ones((147, 190), bool), ((590, 980 - 737), (210, 490 - 400))))   # ref panel box
LAB = (95, 375, 425, 830)   # ref label region (x0, y0, x1, y1): wordmark top to NET WT line
ref_orange = np.median(REF[200:300, 150:350].reshape(-1, 3), axis=0)
def fix(im, box):
    a = np.asarray(im).astype(float); s = (box[2] - box[0]) / (RP[2] - RP[0])
    x0 = int(round(box[0] + (LAB[0] - RP[0]) * s)); y0 = int(round(box[1] + (LAB[1] - RP[1]) * s))
    w = int(round((LAB[2] - LAB[0]) * s)); h = int(round((LAB[3] - LAB[1]) * s))
    lab = np.asarray(Image.fromarray(REF[LAB[1]:LAB[3], LAB[0]:LAB[2]].astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(float)
    H, W = a.shape[:2]; X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    reg = a[Y0:Y1, X0:X1]; lab = lab[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    orange = (r > 150) & (r > g + 40) & (g > b)            # stick surface
    ink = (r > 150) & (g > 140) & (b > 120) & (abs(r - b) < 70)   # AI white text
    surf = orange | ink | teal(reg.astype(np.uint8))
    fo = np.median(reg[orange].reshape(-1, 3), axis=0) if orange.sum() > 50 else ref_orange
    lab = np.clip(lab * ((fo + 8) / (ref_orange + 8)), 0, 255)   # match the frame light (+8 guards the zero blue channel)
    m = Image.fromarray((surf * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    m = np.asarray(m).astype(float)[..., None] / 255
    a[Y0:Y1, X0:X1] = reg * (1 - m) + lab * m
    return Image.fromarray(a.astype(np.uint8))
if sys.argv[1] == "--still":
    im = Image.open(sys.argv[2]).convert("RGB"); fix(im, pbox(np.asarray(im))).save(sys.argv[3]); sys.exit()
src, out = sys.argv[1], sys.argv[2]; tmp = Path(tempfile.mkdtemp())
subprocess.run(["ffmpeg", "-v", "error", "-i", src, str(tmp / "f%04d.png")], check=True)
fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
frames = sorted(tmp.glob("f*.png")); B = [pbox(np.asarray(Image.open(f).convert("RGB"))) for f in frames]
ok = [i for i, b in enumerate(B) if b is not None]; arr = np.array([B[i] for i in ok]); W9 = 9
med = np.array([np.median(arr[max(0, k - 4):k + 5], axis=0) for k in range(len(arr))])
sm = np.array([med[max(0, k - 4):k + 5].mean(axis=0) for k in range(len(med))])
for k, i in enumerate(ok): fix(Image.open(frames[i]).convert("RGB"), sm[k]).save(frames[i])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", fps, "-i", str(tmp / "f%04d.png"), "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
print("label fixed", len(ok), "of", len(frames), "frames ->", out)
