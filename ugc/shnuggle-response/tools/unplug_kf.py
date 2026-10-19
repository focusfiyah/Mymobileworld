"""Free fix (Ralph 2026-10-16: remove the AI plug): paint out a moving object using hand-read keyframes.
python3 tools/unplug_kf.py IN OUT 'obj1kf;obj1kf;...' ['obj2...']   each kf = t:cx:cy:hw:hh (seconds, clip px).
Linear interpolation; the mask is only active between an object's first and last keyframe (+/- one frame)."""
import sys, subprocess, cv2, numpy as np
protect, rows = "--protect-yellow" in sys.argv, "--rows" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
src, dst = args[0], args[1]
objs = [[tuple(float(v) for v in k.split(":")) for k in a.split(";")] for a in args[2:]]
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); W, H = int(cap.get(3)), int(cap.get(4))

def at(kfs, t):
    if t < kfs[0][0] - 1 / fps or t > kfs[-1][0] + 1 / fps: return None
    if t <= kfs[0][0]: return kfs[0][1:]
    for a, b in zip(kfs, kfs[1:]):
        if t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0])
            return tuple(x + (y - x) * u for x, y in zip(a[1:], b[1:]))
    return kfs[-1][1:]

p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
n = 0
while True:
    ok, f = cap.read()
    if not ok: break
    t = n / fps; mask = np.zeros((H, W), np.uint8)
    for kfs in objs:
        # a keyframe given as t:cx:cy keeps the size of the keyframe before it
        full = []
        for k in kfs: full.append(k if len(k) == 5 else k + full[-1][3:5])
        e = at(full, t)
        if e: cv2.ellipse(mask, (int(e[0]), int(e[1])), (int(e[2]), int(e[3])), 0, 0, 360, 255, -1)
    if mask.any():
        soft = cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), 3)[..., None]
        m = cv2.dilate(mask, np.ones((5, 5), np.uint8)); g = f
        if protect:  # keep the yellow duck: never paint over it, and never pull its colour into the fill
            hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
            duck = cv2.dilate(cv2.inRange(hsv, (12, 90, 90), (40, 255, 255)), np.ones((7, 7), np.uint8))
            m = cv2.bitwise_or(m, duck)
            soft = soft * (1 - cv2.GaussianBlur(cv2.erode(duck, np.ones((3, 3), np.uint8)).astype(np.float32) / 255, (0, 0), 1)[..., None])
        fill = cv2.inpaint(g, m, 9, cv2.INPAINT_TELEA)
        if rows:  # continue near-horizontal edges (floor/wall line) across the hole: per-row blend of the pixels left and right of it
            fill = f.astype(np.float32).copy()
            for y in np.where(m.any(1))[0]:
                xs = np.where(m[y] > 0)[0]; a, b = max(xs[0] - 2, 0), min(xs[-1] + 2, W - 1)
                u = np.linspace(0, 1, b - a + 1)[:, None]; fill[y, a:b + 1] = f[y, a] * (1 - u) + f[y, b] * u
            fill = cv2.GaussianBlur(fill, (0, 0), 1.5).astype(np.uint8)
        f = (f * (1 - soft) + fill * soft).astype(np.uint8)
    p.stdin.write(f.tobytes()); n += 1
p.stdin.close(); p.wait(); print("wrote", dst, n, "frames")
