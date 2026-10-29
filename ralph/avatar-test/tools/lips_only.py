"""Free fix for MuseTalk's soft lower face (Ralph 2026-10-29): keep the REAL footage everywhere and take only the lips
from MuseTalk's output, through a soft oval mask placed from MuseTalk's own per-frame face box (work/<base>.pkl).
v2 (Ralph 2026-10-29: "clean up the lip sync overlay. I can see it"): the face box is smoothed over time (it jumped up to
10 px a frame, so the oval jittered), the lip patch is colour-matched to the real frame (LAB mean/std inside the mask)
and lightly sharpened before blending.
Usage: <musetalk venv python> lips_only.py BASE.mp4 MUSETALK.mp4 COORDS.pkl AUDIO.wav OUT.mp4"""
import pickle, subprocess, sys
import cv2, numpy as np
base, mt, pkl, audio, out = sys.argv[1:6]
raw = np.array(pickle.load(open(pkl, "rb")), float)
k = 9; pad = np.pad(raw, ((k // 2, k // 2), (0, 0)), mode="edge")
coords = np.stack([pad[i:i + k].mean(0) for i in range(len(raw))])   # centred moving average


def match(src, ref, m):
    """Colour-match src to ref inside mask m (LAB mean/std), so the lips carry the real frame's skin tone."""
    a, b = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype(np.float32), cv2.cvtColor(ref, cv2.COLOR_BGR2LAB).astype(np.float32)
    w = m[..., 0] > 0.3
    if w.sum() < 50: return src
    for c in range(3):
        sa, sb = a[..., c][w], b[..., c][w]
        a[..., c] = (a[..., c] - sa.mean()) * (sb.std() / (sa.std() + 1e-6)) + sb.mean()
    return cv2.cvtColor(np.clip(a, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
cb, cm = cv2.VideoCapture(base), cv2.VideoCapture(mt)
W, H = int(cm.get(3)), int(cm.get(4)); fps = cm.get(5) or 25
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-i", audio, "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "160k", out], stdin=subprocess.PIPE)
n = 0
while True:
    okm, fm = cm.read()
    if not okm: break
    okb, fb = cb.read()
    if not okb:                       # MuseTalk loops the base video back and forth past its end; follow it
        cb.set(cv2.CAP_PROP_POS_FRAMES, 0); okb, fb = cb.read()
    x1, y1, x2, y2 = [int(v) for v in coords[n % len(coords)]]
    w, h = x2 - x1, y2 - y1
    mask = np.zeros((H, W), np.float32)
    cv2.ellipse(mask, (x1 + w // 2, y1 + int(h * 0.80)), (int(w * 0.23), int(h * 0.12)), 0, 0, 360, 1.0, -1)
    mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=w * 0.06)[..., None]
    fm = match(fm, fb, mask)
    fm = cv2.addWeighted(fm, 1.5, cv2.GaussianBlur(fm, (0, 0), 1.6), -0.5, 0)   # light unsharp on the lips
    p.stdin.write((fm * mask + fb * (1 - mask)).astype(np.uint8).tobytes()); n += 1
p.stdin.close(); p.wait(); print("LIPS_ONLY_OK", n, "frames")
