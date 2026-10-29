"""S5, free: the view THROUGH the detector's window (Ralph OK 2026-10-29: "Yes ok", the product's own light allowed when needed).
S2's smoke-detector push-in, seen through the red filter: the room goes red, the window's rounded shape frames it, and the tiny
pinhole lens on the detector rim shines back as a bright red pinpoint, tracked frame by frame (cv2 template match).
  python3 tools/s5_view.py -> clips/S5_view.mp4 (+ qc/S5_track.json)"""
import json, subprocess
import cv2, numpy as np

SRC, OUT, T0, T1 = "clips/S2_seedance.mp4", "clips/S5_view.mp4", 0.75, 4.04
SEED_T, SEED = 2.0, (395, 460)          # pinhole on the rim at 2.0 s, found by eye at 2x (qc/S2_f2_zoom.png)
cap = cv2.VideoCapture(SRC); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
H, W = frames[0].shape[:2]; i0, i1, iseed = int(T0 * fps), min(len(frames), int(T1 * fps)), int(SEED_T * fps)


def track(order, start):
    pos, x, y, R = {}, *start, 14
    for k in order:
        g = cv2.cvtColor(frames[k], cv2.COLOR_BGR2GRAY)
        if pos:  # search near the last point for the darkest small blob (the pinhole is the only dark dot on the rim)
            sx0, sy0 = max(0, x - 18), max(0, y - 18)
            win = cv2.GaussianBlur(g[sy0:y + 19, sx0:x + 19], (5, 5), 0)
            mv, _, mn, _ = cv2.minMaxLoc(win); x, y = sx0 + mn[0], sy0 + mn[1]
            ys_, xs_ = np.where(g[y - 8:y + 9, x - 8:x + 9] < mv + 30)   # centre of the dark hole, not its darkest edge
            if len(xs_): x, y = int(round(x - 8 + xs_.mean())), int(round(y - 8 + ys_.mean()))
        pos[k] = (int(x), int(y))
    return pos


p = track(range(iseed, i1), SEED); p.update(track(range(iseed, i0 - 1, -1), SEED))
ks = sorted(p); xs = np.array([p[k][0] for k in ks], float); ys = np.array([p[k][1] for k in ks], float)
ker = np.ones(3) / 3; xs = np.convolve(np.pad(xs, 1, mode="edge"), ker, "valid"); ys = np.convolve(np.pad(ys, 1, mode="edge"), ker, "valid")
json.dump({str(k): [round(a, 1), round(b, 1)] for k, a, b in zip(ks, xs, ys)}, open("qc/S5_track.json", "w"))
# window mask: tall rounded rectangle like the real filter window, soft edge, black outside
mask = np.zeros((H, W), np.float32); mw, mh, r = int(W * 0.84), int(H * 0.80), int(W * 0.30)
x0, y0 = (W - mw) // 2, (H - mh) // 2
cv2.rectangle(mask, (x0 + r, y0), (x0 + mw - r, y0 + mh), 1, -1); cv2.rectangle(mask, (x0, y0 + r), (x0 + mw, y0 + mh - r), 1, -1)
for cx, cy in [(x0 + r, y0 + r), (x0 + mw - r, y0 + r), (x0 + r, y0 + mh - r), (x0 + mw - r, y0 + mh - r)]: cv2.circle(mask, (cx, cy), r, 1, -1)
mask = cv2.GaussianBlur(mask, (0, 0), 9)[..., None]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
pipe = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for n, (k, px, py) in enumerate(zip(ks, xs, ys)):
    g = cv2.cvtColor(frames[k], cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    g = np.clip((g - 0.15) * 1.15, 0, 1) ** 1.25                       # the filter darkens and reddens everything
    img = np.stack([g * 0.10, g * 0.12, g * 0.95], -1)                 # BGR: deep red view
    d2 = (xx - px) ** 2 + (yy - py) ** 2; pulse = 0.85 + 0.15 * np.sin(n / fps * 2 * np.pi * 1.5)
    glow = (np.exp(-d2 / (2 * 26.0 ** 2)) * 0.9 + np.exp(-d2 / (2 * 6.0 ** 2)) * 1.0) * pulse
    core = np.exp(-d2 / (2 * 3.2 ** 2)) * pulse                        # near-white centre of the pinpoint
    img[..., 2] += glow; img[..., 1] += core * 0.75 + glow * 0.12; img[..., 0] += core * 0.65 + glow * 0.08
    img = np.clip(img, 0, 1) * mask
    pipe.stdin.write((img * 255).astype(np.uint8).tobytes())
pipe.stdin.close(); pipe.wait(); print("ok", OUT, len(ks), "frames", round(len(ks) / fps, 2), "s")
