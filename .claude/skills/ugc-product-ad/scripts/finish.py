"""Phone-camera finish (free), run AFTER pasteback so the vanity stays the real photo (Ralph 2026-10-03: "hard to tell it's AI").

  python3 finish.py IN OUT [--glow T X Y R] [--sway PX] [--grain SIGMA]   T = second the LEDs switch on, X,Y,R = glow centre/radius
1) handheld sway, default OFF (Ralph 2026-10-03: moving a soft upscaled photo by sub-pixels makes fine lines crawl = shimmer)
2) one texture for the whole frame: 0.6 px blur (sharp AI hand meets the soft 800 px photo) + phone grain
3) LED spill: from T a soft lift (+4%, barely warmer) around the mirror, same 0.25 s smooth fade as the ring (pasteback prints T)
"""
import subprocess, sys
import cv2, numpy as np

src, out = sys.argv[1], sys.argv[2]
arg = lambda k, d: float(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
SWAY, GRAIN = arg('--sway', 0), arg('--grain', 1.3)
TB = list(map(float, sys.argv[sys.argv.index('--topblur') + 1:][:2])) if '--topblur' in sys.argv else None   # soft focus over far labels: full above Y0, gone by Y1
glow = list(map(float, sys.argv[sys.argv.index("--glow") + 1:][:4])) if "--glow" in sys.argv else None
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
w, h = int(cap.get(3)), int(cap.get(4)); n = int(cap.get(7))
rng = np.random.default_rng(abs(hash(out)) % 2**32); t = np.arange(n) / fps


def drift(amp):  # sum of slow sines = hand sway, no jitter
    return sum(amp / k * np.sin(2 * np.pi * rng.uniform(0.15, 0.6) * k * t + rng.uniform(0, 6.3)) for k in (1, 2, 3))


dx, dy, rot = drift(SWAY), drift(SWAY), drift(SWAY * 0.05)
if glow:
    T, gx, gy, R = glow
    yy, xx = np.mgrid[0:h, 0:w]; fall = np.clip(1 - np.hypot(xx - gx, yy - gy) / R, 0, 1)[..., None] ** 1.5
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                       "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
for i in range(n):
    ok, f = cap.read()
    if not ok: break
    f = f.astype(np.float32)
    if glow and t[i] >= T:
        e = min(1, (t[i] - T) / 0.25); e = e * e * (3 - 2 * e)
        k = e * fall
        f = f * (1 + 0.04 * k) + k * np.array([-1, 1, 3], np.float32)       # BGR: a touch brighter + warmer near the mirror
    if SWAY:
        M = cv2.getRotationMatrix2D((w / 2, h / 2), rot[i], 1.035); M[:, 2] += (dx[i], dy[i])
        f = cv2.warpAffine(f, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    if TB:
        wt = np.clip((TB[1] - np.arange(h)[:, None, None]) / (TB[1] - TB[0]), 0, 1); f = cv2.GaussianBlur(f, (0, 0), 4.5) * wt + f * (1 - wt)
    f = cv2.GaussianBlur(f, (0, 0), 0.6)
    g = rng.normal(0, GRAIN, (h // 2, w // 2)).astype(np.float32)
    f += cv2.resize(g, (w, h))[..., None]                                    # soft (2 px) luma grain, like a phone sensor
    ff.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); print("finished", out, n, "frames")
