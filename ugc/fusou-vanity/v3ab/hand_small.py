"""Small-hand paste-back for the pointing clips (free). Camera is locked: take the hand (HSV skin, blob touching the left/right frame edge) from each AI frame,
scale it about its entry point on the frame edge (so the wrist stays ON the edge, forearm shrinks off-frame), paste onto the REAL listing photo.
  python3 v3ab/hand_small.py clips/P1_raw.mp4 clips/P1.mp4 [--scale 0.55] [--side left|right]"""
import subprocess, sys
import cv2, numpy as np
src, out = sys.argv[1:3]; opt = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
s = float(opt("--scale", 0.55)); side = opt("--side", "left"); W, H = 800, 1422
base = cv2.imread("refs/base_A_916.jpg"); cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS) or 24
frames, masks = [], []
while True:
    ok, f = cap.read()
    if not ok: break
    f = cv2.resize(f, (W, H), interpolation=cv2.INTER_AREA); hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV); h_, sa, v = cv2.split(hsv)
    m = ((h_ >= 3) & (h_ <= 22) & (sa > 70) & (v < 215) & (v > 40)).astype(np.uint8); m[:560] = 0; m[1300:] = 0
    if side == "left": m[:, 450:] = 0
    else: m[:, :350] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m); col = 0 if side == "left" else W - 1
    keep = [i for i in range(1, n) if st[i, 4] > 1500 and (lab[:, col] == i).any()]
    mk = np.isin(lab, keep).astype(np.uint8)
    cs, _ = cv2.findContours(mk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(mk, cs, -1, 1, cv2.FILLED)   # fill holes (nails, knuckle gaps): no background through the hand
    mk = cv2.dilate(mk, np.ones((5, 5), np.uint8)); frames.append(f); masks.append(mk)
col = 0 if side == "left" else W - 1
ays = [np.where(m[:, col] > 0)[0].mean() for m in masks if m[:, col].any()]; ay = float(np.median(ays)); ax = float(col)
print("entry y", round(ay), "frames", len(frames), "frames without hand", sum(1 for m in masks if not m.any()))
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
T = np.float32([[s, 0, ax - s * ax], [0, s, ay - s * ay]])
prev = None
for f, m in zip(frames, masks):
    hp = cv2.warpAffine(f, T, (W, H), flags=cv2.INTER_AREA); hm = cv2.warpAffine(m * 255, T, (W, H), flags=cv2.INTER_AREA)
    hm = cv2.GaussianBlur(hm, (0, 0), 1.0).astype(np.float32)[..., None] / 255
    ff.stdin.write((hp * hm + base * (1 - hm)).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
