"""Free ripple boost for the water opener (S1/S2), HEVEBLUE 2026-10-27: moving concentric rings drawn by a small radial
pixel displacement inside the water-surface ellipse only, the chrome tip masked out. Ellipse given for the first and last
frame (cx, cy, a, b) and interpolated (the clip has a slight push-in).
  python3 tools/ripple.py IN OUT cx0 cy0 a0 b0 cx1 cy1 a1 b1 [--amp 2.0] [--rings 7] [--hz 6] [--tipw 26]"""
import argparse, subprocess, numpy as np, cv2
p = argparse.ArgumentParser(); p.add_argument("inp"); p.add_argument("out")
for k in ("cx0", "cy0", "a0", "b0", "cx1", "cy1", "a1", "b1"): p.add_argument(k, type=float)
p.add_argument("--amp", type=float, default=2.0); p.add_argument("--rings", type=float, default=7); p.add_argument("--hz", type=float, default=6)
p.add_argument("--tipw", type=float, default=26)
p.add_argument("--src", type=float, nargs=4, help="ring source x0 y0 x1 y1 (the touch point on the rim, first/last frame); rings radiate from it (v2: tip on the rim, Ralph 2026-10-27)")
p.add_argument("--body", type=float, nargs=3, help="water body below the surface: half-height first frame, half-height last frame, shimmer px (Ralph 2026-10-27: 'can the water vibrate more')")
p.add_argument("--start", type=float, default=0.0, help="seconds: no rings before (the tip touches the rim at this time); fades in over 0.2 s")
A = p.parse_args()
cap = cv2.VideoCapture(A.inp); fps = cap.get(cv2.CAP_PROP_FPS); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
W, H = int(cap.get(3)), int(cap.get(4))
pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                       "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", A.out], stdin=subprocess.PIPE)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
for i in range(n):
    ok, f = cap.read()
    if not ok: break
    t = i / max(1, n - 1); cx, cy, a, b = [(1 - t) * getattr(A, k + "0") + t * getattr(A, k + "1") for k in ("cx", "cy", "a", "b")]
    dx, dy = (xx - cx) / a, (yy - cy) / b; r = np.sqrt(dx * dx + dy * dy) + 1e-6
    tsec = i / fps; on = np.clip((tsec - A.start) / 0.2, 0, 1)
    if A.src:
        sx = (1 - t) * A.src[0] + t * A.src[2]; sy = (1 - t) * A.src[1] + t * A.src[3]
        dx, dy = (xx - sx) / a, (yy - sy) / b; rs = np.sqrt(dx * dx + dy * dy) + 1e-6
        fade = np.clip((1 - r) / 0.15, 0, 1) * np.clip(1 - rs / 1.6, 0, 1) ** 0.7 * on   # inside the water, strongest at the touch point
        s = A.amp * np.sin(2 * np.pi * (A.rings * rs - A.hz * tsec)) * fade
        r = rs
    else:
        fade = np.clip(1 - r, 0, 1) ** 0.6 * np.clip((r - 0.05) / 0.1, 0, 1)
        fade *= np.clip((np.abs(xx - cx) - A.tipw) / 6, 0, 1)            # keep the chrome tip untouched
        s = A.amp * np.sin(2 * np.pi * (A.rings * r - A.hz * tsec)) * fade * on
    mx = xx + s * dx / r * (a / max(a, b)); my = yy + s * dy / r * 1.0
    if A.body:
        bb = (1 - t) * A.body[0] + t * A.body[1]
        ry = np.sqrt(((xx - cx) / (a * 0.92)) ** 2 + ((yy - (cy + bb)) / bb) ** 2)
        mb = np.clip((1 - ry) / 0.2, 0, 1) * (yy > cy) * on                      # inside the bowl, below the water line
        jit = A.body[2] * np.sin(2 * np.pi * (yy / 9.0 + 11 * tsec)) * np.sin(2 * np.pi * (xx / 23.0 - 7 * tsec))
        mx = mx + jit * mb; my = my + 0.6 * jit * mb
    g = cv2.remap(f, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    pr.stdin.write(g.tobytes())
pr.stdin.close(); pr.wait(); print("ripple ok", n, "frames")
