"""Shrink the AI's seat bump into the real tub's small, low oval swell (free retouch, Ralph 2026-10-21: "the bump in the middle does not
reflect the product" ... "can the bump be fixed"). The AI drew a two-lobed pillow (S4, S5), a big dome (S6) or a lump (S7); the real seat is
a gentle single oval mound. Per frame: the bump area (an ellipse that follows the tub through the camera move via optical flow on the tub
floor, smoothed over time) is replaced by a heavily blurred copy of itself (lobes and hard highlights gone, the floor's own light kept)
plus a faint soft oval highlight, feathered in.

  python3 bump_fix.py IN OUT --ell cx,cy,len,height,angle [--frames a:b] [--sigma 3] [--glow 10] [--edge 9] [--fade f0:f1] [--keys "f,cx,cy,len,h;..."] [--static]   writes OUT + OUT_check.jpg
--ell = the bump in the FIRST frame (frame pixels, full axis lengths, angle in degrees)."""
import subprocess, sys
import cv2, numpy as np
from scipy.ndimage import gaussian_filter1d

_a = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
IN, OUT = sys.argv[1], sys.argv[2]
cx0, cy0, L0, H0, A0 = map(float, _a("--ell", "0,0,0,0,0").split(","))
SIG, GLOW = float(_a("--sigma", "3")), float(_a("--glow", "10"))
cap = cv2.VideoCapture(IN); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
a, b = map(int, _a("--frames", f"0:{len(frames)}").split(":"))

T = [np.eye(3)]
if "--static" not in sys.argv:   # follow the tub floor around the bump (the dots and rim give the flow points)
    r = max(L0, H0) * 1.6; zone = np.zeros(frames[a].shape[:2], np.uint8)
    cv2.ellipse(zone, (int(cx0), int(cy0)), (int(r), int(r * 0.8)), A0, 0, 360, 255, -1)
    prev = cv2.cvtColor(frames[a], cv2.COLOR_BGR2GRAY); pts = cv2.goodFeaturesToTrack(prev, 150, 0.004, 3, mask=zone)
    for i in range(a + 1, b):
        cur = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, pts, None, winSize=(25, 25), maxLevel=3); ok = st.ravel() == 1
        M, _ = cv2.estimateAffinePartial2D(pts[ok], nxt[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0) if ok.sum() >= 6 else (None, None)
        T.append((np.vstack([M, [0, 0, 1]]) if M is not None else np.eye(3)) @ T[-1]); pts = nxt[ok].reshape(-1, 1, 2)
        if len(pts) < 50:
            c = T[-1] @ np.array([cx0, cy0, 1]); s = np.sqrt(abs(np.linalg.det(T[-1][:2, :2]))); z = np.zeros_like(zone)
            cv2.ellipse(z, (int(c[0]), int(c[1])), (int(r * s), int(r * s * 0.8)), A0, 0, 360, 255, -1)
            new = cv2.goodFeaturesToTrack(cur, 150, 0.004, 3, mask=z)
            if new is not None: pts = np.vstack([pts, new]).astype(np.float32)
        prev = cur
T += [T[-1]] * (b - a - len(T))
P = []
for Ti in T:
    c = Ti @ np.array([cx0, cy0, 1]); s = np.sqrt(abs(np.linalg.det(Ti[:2, :2]))); rot = np.degrees(np.arctan2(Ti[1, 0], Ti[0, 0]))
    P.append([c[0], c[1], L0 * s, H0 * s, A0 + rot])
KEYS = _a("--keys", None)   # "frame,cx,cy,len,height;..." hand-set bump positions (S4 push-in: the flow drifted onto the rim); overrides the flow
if KEYS:
    K = np.array([list(map(float, k.split(","))) for k in KEYS.split(";")]); idx = np.arange(a, b)
    P = [[np.interp(i, K[:, 0], K[:, c]) for c in range(1, 5)] + [A0] for i in idx]
P = gaussian_filter1d(np.array(P, float), SIG, axis=0, mode="nearest"); np.save(OUT.replace(".mp4", "_path.npy"), P)


def fix(f, p, k=1.0):
    cx, cy, L, H, an = p; f = f.astype(np.float32); hw = f.shape[:2]
    m = np.zeros(hw, np.float32); cv2.ellipse(m, (int(cx), int(cy)), (int(L / 2), int(H / 2)), an, 0, 360, 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), max(3, H * 0.18))[..., None] * k
    soft = cv2.GaussianBlur(f, (0, 0), max(6, H * 0.35))   # lobes and specular highlights gone, the floor's light gradient kept
    g = np.zeros(hw, np.float32); cv2.ellipse(g, (int(cx), int(cy - H * 0.08)), (int(L * 0.33), int(H * 0.3)), an, 0, 360, 1, -1)
    g = cv2.GaussianBlur(g, (0, 0), max(3, H * 0.2))[..., None] * GLOW   # a faint soft oval highlight: a low swell, not a flat floor
    e = np.zeros(hw, np.float32)   # a faint shadow along the lower edge of the mound, so it reads as a shape (the real seat has a soft rim)
    cv2.ellipse(e, (int(cx), int(cy + H * 0.12)), (int(L * 0.36), int(H * 0.34)), an, 20, 160, 1, max(2, int(H * 0.06)))
    e = cv2.GaussianBlur(e, (0, 0), max(2, H * 0.07))[..., None] * float(_a("--edge", "9"))
    return np.clip(f * (1 - m) + (soft + g - e) * m, 0, 255).astype(np.uint8)


res = list(frames)
FADE = _a("--fade", None)   # f0:f1 = full retouch until f0, none from f1 (S4: the bump hides behind the rim as the camera pushes in)
def strength(i):
    if not FADE: return 1.0
    f0, f1 = map(int, FADE.split(":")); return float(np.clip((f1 - i) / max(f1 - f0, 1), 0, 1))
for j, i in enumerate(range(a, b)): res[i] = fix(frames[i], P[j], strength(i))
h, w = frames[0].shape[:2]
pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                       "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for fr in res: pr.stdin.write(fr.tobytes())
pr.stdin.close(); pr.wait()
rows = []
for i in [a, (a + b) // 2, b - 1]:
    cx, cy, L, H, _ = P[i - a]; r = int(max(L, H) * 0.9) + 20
    y0, x0 = max(0, int(cy - r)), max(0, int(cx - r)); pair = np.hstack([frames[i][y0:int(cy + r), x0:int(cx + r)], res[i][y0:int(cy + r), x0:int(cx + r)]])
    rows.append(cv2.resize(pair, (800, int(800 * pair.shape[0] / pair.shape[1]))))
cv2.imwrite(OUT.replace(".mp4", "_check.jpg"), np.vstack(rows)); print("wrote", OUT, f"({b - a} frames)")
