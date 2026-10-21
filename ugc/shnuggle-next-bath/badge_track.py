"""Put the REAL grey "shnuggle" badge (refs/badge_real.png, cut from the brand's own photo) over a garbled AI badge in a moving clip (free).
Ralph OK'd the paste for S11 on 2026-10-21 ("paste"). The AI badge's letters are wrong, so text matching (label_track.py) can't lock on;
this tracks the grey pebble SHAPE instead: per frame the grey blob nearest the last position, an ellipse fit, the centre/size/angle
smoothed over time (no jitter), the real badge warped onto it with the frame's own grey level and softness, and any AI grey left
outside the real shape filled from the white tub around it.

  python3 badge_track.py IN OUT --roi x0,y0,x1,y1 [--frames a:b] [--sigma 3]    writes OUT + OUT_check.jpg (4x crops, AI vs pasted)
--roi = a box around the badge in the FIRST frame (frame pixels)."""
import subprocess, sys
import cv2, numpy as np
from scipy.ndimage import gaussian_filter1d

_a = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
IN, OUT = sys.argv[1], sys.argv[2]
X0, Y0, X1, Y1 = map(int, _a("--roi", "0,0,0,0").split(","))
SIG = float(_a("--sigma", "3"))
REAL = cv2.imread("refs/badge_real.png").astype(np.float32); RM = cv2.imread("refs/badge_real_mask.png", 0)


def ellipse(mask):
    c, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(c, key=cv2.contourArea)
    return cv2.fitEllipse(c) if len(c) >= 5 else None


(rcx, rcy), (rw, rh), rang = ellipse(RM)
cap = cv2.VideoCapture(IN); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
a, b = map(int, _a("--frames", f"0:{len(frames)}").split(":"))


VMAX = int(_a("--vmax", "198"))   # badge grey vs the white tub (S11: badge V ~187, tub 208-220)


def grey_blob(f, box, prev=None):
    x0, y0, x1, y1 = [int(v) for v in box]; x0, y0 = max(0, x0), max(0, y0)
    roi = f[y0:y1, x0:x1]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 1] < 40) & (hsv[..., 2] > 95) & (hsv[..., 2] < VMAX)).astype(np.uint8) * 255   # neutral mid-grey (badge), not the white tub
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))                          # close over the white letters
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2: return None, None
    mid = np.array([(x1 - x0) / 2, (y1 - y0) / 2]); cand = list(range(1, n))
    if prev is not None:   # the badge can only change a little between frames: area within 0.6-1.6x, pebble-shaped (wider than tall)
        cand = [i for i in cand if 0.6 * prev <= st[i, 4] <= 1.6 * prev and 1.4 <= st[i, 2] / max(st[i, 3], 1) <= 4.0]
    if not cand: return None, None
    best = min(cand, key=lambda i: np.linalg.norm(cen[i] - mid) - (0 if prev else 0.02 * st[i, 4]))
    full = np.zeros(f.shape[:2], np.uint8); full[y0:y1, x0:x1] = (lab == best).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(full, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); fill = np.zeros_like(full)
    cv2.drawContours(fill, [max(cnts, key=cv2.contourArea)], -1, 255, -1)
    e = ellipse(fill)
    return e, fill


# Find the badge ONCE (first frame), then follow the tub's own surface: optical-flow points on the tub front around the badge give a
# similarity transform per frame (the tub is rigid and the camera moves smoothly), so the badge rides along with the tub.
e0, m0 = grey_blob(frames[a], (X0, Y0, X1, Y1))
if _a("--ell", None):   # manual first-frame badge: cx,cy,length,height,angle (deg, long axis) when the auto fit catches nearby shading
    ecx, ecy, el, eh, ea = map(float, _a("--ell", None).split(","))
    m0 = np.zeros(frames[a].shape[:2], np.uint8); cv2.ellipse(m0, (int(ecx), int(ecy)), (int(el / 2), int(eh / 2)), ea, 0, 360, 255, -1); e0 = ellipse(m0)
assert e0 is not None, "no badge in the --roi box on the first frame"
(cx0, cy0), (w0, h0), an0 = e0; r = max(w0, h0) * float(_a("--flowr", "1.8"))   # tracking zone; smaller when a hand moves next to the tub (S10)
zone = np.zeros(frames[a].shape[:2], np.uint8); cv2.ellipse(zone, (int(cx0), int(cy0)), (int(r), int(r * 0.9)), 0, 0, 360, 255, -1)
prev = cv2.cvtColor(frames[a], cv2.COLOR_BGR2GRAY)
pts = cv2.goodFeaturesToTrack(prev, 120, 0.005, 3, mask=zone)
T = [np.eye(3)]; lost = 0
for i in range(a + 1, b):
    cur = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, pts, None, winSize=(21, 21), maxLevel=3)
    ok = st.ravel() == 1
    M_, inl = cv2.estimateAffinePartial2D(pts[ok], nxt[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0) if ok.sum() >= 6 else (None, None)
    if M_ is None: M_ = np.hstack([np.eye(2), np.zeros((2, 1))]); lost += 1
    T.append(np.vstack([M_, [0, 0, 1]]) @ T[-1])
    pts = nxt[ok].reshape(-1, 1, 2)
    if len(pts) < 40:   # refill tracking points around the badge's current position
        c = T[-1] @ np.array([cx0, cy0, 1]); z = np.zeros_like(zone); s = np.sqrt(abs(np.linalg.det(T[-1][:2, :2])))
        cv2.ellipse(z, (int(c[0]), int(c[1])), (int(r * s), int(r * s * 0.9)), 0, 0, 360, 255, -1)
        new = cv2.goodFeaturesToTrack(cur, 120, 0.005, 3, mask=z)
        if new is not None: pts = np.vstack([pts, new]).astype(np.float32)
    prev = cur
if "--static" in sys.argv:   # the tub does not move (S10: only the hand and towel move next to it): keep the first-frame badge
    T = [np.eye(3)] * len(T)
print(f"tracked {len(T)} frames ({lost} without a fit){' (static)' if '--static' in sys.argv else ''}")
P = []
for Ti in T:   # badge ellipse in each frame = first-frame ellipse moved by the tub's transform
    c = Ti @ np.array([cx0, cy0, 1]); s = np.sqrt(abs(np.linalg.det(Ti[:2, :2]))); rot = np.degrees(np.arctan2(Ti[1, 0], Ti[0, 0]))
    P.append([c[0], c[1], w0 * s, h0 * s, an0 + rot])
P = np.array(P, float); masks = []; snapped = 0; off = np.zeros(2)
for j, i in enumerate(range(a, b)):   # flow drifts over seconds: re-find the badge as the darker-than-its-surroundings oval near the
    cx, cy, w, h, an = P[j]; cx, cy = cx + off[0], cy + off[1]   # predicted spot (the AI letters morph, its grey pebble stays)
    v = cv2.cvtColor(frames[i], cv2.COLOR_BGR2HSV)[..., 2].astype(np.float32); k = int(max(w, h) * 0.7) | 1
    m = ((v < cv2.blur(v, (k, k)) - 7) & (v > 90)).astype(np.uint8) * 255
    zone = np.zeros_like(m); cv2.ellipse(zone, (int(cx), int(cy)), (int(w * 0.9), int(h * 1.2)), an, 0, 360, 255, -1); m &= zone
    m = cv2.morphologyEx(cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m); exp = np.pi / 4 * w * h
    cand = [q for q in range(1, n) if 0.55 * exp < st[q, 4] < 1.6 * exp and np.hypot(*(cen[q] - [cx, cy])) < 0.35 * w]
    if cand and "--static" not in sys.argv:   # static: nothing to correct, and the tub's side shading can pull a snap off the badge
        q = min(cand, key=lambda q: np.hypot(*(cen[q] - [cx, cy]))); off += cen[q] - [cx, cy]; cx, cy = cen[q]; snapped += 1
    P[j, :2] = cx, cy
    mk = np.zeros(m.shape, np.uint8); cv2.ellipse(mk, (int(cx), int(cy)), (int(w / 2) + 1, int(h / 2) + 1), an, 0, 360, 255, -1); masks.append(mk)
print(f"snapped to the badge in {snapped} of {len(P)} frames")
P = gaussian_filter1d(P, SIG, axis=0, mode="nearest"); np.save(OUT.replace(".mp4", "_path.npy"), P)   # for the jitter check


def paste(f, p, aimask):
    cx, cy, w, h, an = p
    # real ellipse -> target ellipse: rotate real to axis-aligned, scale axes, rotate to target, translate
    def M(cx, cy, ang, sx=1, sy=1):
        t = np.deg2rad(ang); R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
        return R, np.array([cx, cy])
    Rr, cr = M(rcx, rcy, rang); Rt, ct = M(cx, cy, an)
    S = np.diag([w / rw, h / rh]); A = Rt @ S @ Rr.T; tvec = ct - A @ cr
    W = np.hstack([A, tvec[:, None]]).astype(np.float32); H_, W_ = f.shape[:2]
    real = cv2.warpAffine(REAL, W, (W_, H_), flags=cv2.INTER_AREA if w < rw else cv2.INTER_LINEAR)
    rm = cv2.warpAffine(RM, W, (W_, H_)).astype(np.float32) / 255
    if aimask is not None and (aimask > 0).sum() > 20 and (rm > 0.5).sum() > 20:   # match the frame's grey level and softness
        fg = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32); rg = cv2.cvtColor(real.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
        sel_f, sel_r = aimask > 0, rm > 0.5   # per channel: the real pebble grey -> the frame's pebble grey, real white letters -> the frame's white
        for ch in range(3):
            fb, fl = np.percentile(f[..., ch][sel_f], 25), np.percentile(f[..., ch][sel_f], 97)
            rb, rl = np.percentile(real[..., ch][sel_r], 25), np.percentile(real[..., ch][sel_r], 97)
            real[..., ch] = fb + (real[..., ch] - rb) * (fl - fb) / max(rl - rb, 8)
    real = cv2.GaussianBlur(real, (0, 0), max(0.35, min(0.9, w / rw * 0.9)))
    out = f.astype(np.float32)
    if aimask is not None:   # AI grey outside the real shape -> white tub around it
        k = max(5, int(w * 0.08)) | 1; left = ((cv2.dilate(aimask, np.ones((k, k), np.uint8)) > 0) & (rm < 0.5)).astype(np.uint8) * 255   # AI pebble + its light outline ring
        if left.any(): out = cv2.inpaint(out.astype(np.uint8), left, 5, cv2.INPAINT_TELEA).astype(np.float32)
    al = cv2.GaussianBlur(cv2.erode(rm, np.ones((2, 2), np.uint8)), (0, 0), 0.8)[..., None]
    return np.clip(out * (1 - al) + real * al, 0, 255).astype(np.uint8)


res = list(frames)
for j, i in enumerate(range(a, b)):
    res[i] = paste(frames[i], P[j], masks[j])
h, w = frames[0].shape[:2]
pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                       "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for fr in res: pr.stdin.write(fr.tobytes())
pr.stdin.close(); pr.wait()
rows = []
for i in [a, (a + b) // 2, b - 1]:
    cx, cy = P[i - a][:2]; r = int(max(P[i - a][2:4]) * 1.3) + 8
    y0, y1, x0, x1 = max(0, int(cy - r)), int(cy + r), max(0, int(cx - 2 * r)), int(cx + 2 * r)
    pair = np.hstack([frames[i][y0:y1, x0:x1], res[i][y0:y1, x0:x1]]); rows.append(cv2.resize(pair, (800, int(800 * pair.shape[0] / pair.shape[1]))))
cv2.imwrite(OUT.replace(".mp4", "_check.jpg"), np.vstack(rows)); print("wrote", OUT)
