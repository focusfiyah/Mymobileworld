"""S1 (Omni take, 2026-10-27): Omni added a small gold key under the key ring (the real charm has no key; product_truth).
Each frame: find the ring (Hough circle in its area), paint out the gold below its bottom edge (OpenCV inpaint). Free.
  python3 tools/key_out.py clips/S1.mp4 clips/S1_nokey.mp4"""
import subprocess, sys
import cv2, numpy as np
src, dst = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); W, H = int(cap.get(3)), int(cap.get(4)); fps = cap.get(5)
out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}", "-i", "-",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
x0, x1, y0, y1 = int(W * .12), int(W * .45), int(H * .52), int(H * .80); n = 0
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
# pass 1: the ring centre per frame (Hough), radius fixed to the median (a too-small radius cut a notch into the ring)
cs, rs = [], []
for f in frames:
    roi = cv2.GaussianBlur(cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY), (5, 5), 0)
    c = cv2.HoughCircles(roi, cv2.HOUGH_GRADIENT, 1.2, 80, param1=90, param2=28, minRadius=int(W * .03), maxRadius=int(W * .075))
    if c is not None: cs.append((c[0][0][0] + x0, c[0][0][1] + y0)); rs.append(c[0][0][2])
    else: cs.append((np.nan, np.nan))
cs = np.array(cs, float); ok = ~np.isnan(cs[:, 0])
for j in range(2): cs[:, j] = np.interp(np.arange(len(cs)), np.nonzero(ok)[0], cs[ok, j])
cs = np.array([np.median(cs[max(0, i - 2):i + 3], 0) for i in range(len(cs))])
rr = float(np.median(rs))
# pass 2: paint out the key in a narrow strip under the ring's bottom edge
for i, f in enumerate(frames):
    b, g, r = [f[..., k].astype(int) for k in range(3)]
    gold = ((r > 120) & (g > 85) & (b < g * 0.8) & (r > b + 45)).astype(np.uint8) * 255
    cx, cy = cs[i]; m = np.zeros((H, W), np.uint8)
    yb = int(cy + rr * 0.92)
    band = np.zeros((H, W), np.uint8); band[yb:int(cy + rr * 3.1), int(cx - rr):int(cx + rr)] = 255
    ys, xs = np.nonzero(cv2.dilate(band & gold, np.ones((7, 7), np.uint8)))
    if len(xs):
        kx = int(np.median(xs)); m[int(cy + rr * 1.04):int(cy + rr * 3.1), kx - int(rr * 0.5):kx + int(rr * 0.5)] = 255
        sh = int(rr * 1.5); pad = np.roll(f, -sh, axis=1)
        a = cv2.GaussianBlur(cv2.dilate(m, np.ones((5, 5), np.uint8)), (11, 11), 0).astype(np.float32)[..., None] / 255
        f = (f * (1 - a) + pad * a).astype(np.uint8); n += 1
    out.stdin.write(f.tobytes())
out.stdin.close(); out.wait(); print("key painted out on", n, "frames, ring radius", round(rr, 1), "->", dst)
