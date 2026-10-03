"""Free slow push-in / pull-out on a REAL photo (Ralph 2026-10-03), one Lanczos resample per frame straight from the source photo.

  python3 kb.py SRC X0,Y0,X1,Y1 OUT DUR [--zoom 1.05] [--out-pull] [--to CX,CY]
Box = the 9:16 framing in SRC pixels at the start; zoom > 1 pushes in toward the box centre (or CX,CY in SRC pixels); --out-pull reverses it.
Smoothstep easing, monotonic (no back-and-forth = no line crawl). 24 fps, 720x1280.
"""
import subprocess, sys
import cv2, numpy as np
src, box, out, dur = sys.argv[1], list(map(float, sys.argv[2].split(","))), sys.argv[3], float(sys.argv[4])
opt = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
Z = float(opt("--zoom", 1.05)); pull = "--out-pull" in sys.argv
im = cv2.imread(src).astype(np.float32); W, H, fps = 720, 1280, 24
x0, y0, x1, y1 = box; cx, cy = map(float, opt("--to", f"{(x0 + x1) / 2},{(y0 + y1) / 2}").split(","))
n = round(dur * fps)
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                       "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / max(n - 1, 1); t = t * t * (3 - 2 * t)
    if pull: t = 1 - t
    z = 1 + (Z - 1) * t
    bw, bh = (x1 - x0) / z, (y1 - y0) / z
    bx0 = x0 + (cx - x0) * (1 - 1 / z); by0 = y0 + (cy - y0) * (1 - 1 / z)     # shrink the box toward the target point
    s = W / bw; M = np.float32([[s, 0, -bx0 * s], [0, s, -by0 * s]])
    f = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REFLECT)   # AREA/LINEAR crawl least (measured 2026-10-03)
    ff.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); print("kb", out, n, "frames")
