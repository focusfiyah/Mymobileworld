"""Put Grace's real TikTok on the phone screen in S1 (Ralph 2026-10-21: "overlay Grace's Tiktok on it"). Free.
  python3 screen_track.py   -> clips/S1_screen.mp4 (+ qc/S1_screen_check.jpg)
The S1 still/clip shows a plain grey screen. Per frame: mask the grey (low saturation, mid-high value) blob, take its
convex hull, fit 4 corners, smooth the corners over 5 frames, warp the TikTok frame onto them, and paste only where the
pixel is screen-grey (so fingers in front of the screen stay real; the notch stays black)."""
import cv2, numpy as np, subprocess

SRC, SCR, OUT = "clips/S1.mp4", "refs/screen_grace.mp4", "clips/S1_screen.mp4"


def grey_mask(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 1] < 45) & (hsv[..., 2] > 140) & (hsv[..., 2] < 250)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    if n < 2: return None, None
    # the screen = the largest tall blob in the middle third of the frame
    cand = [(st[i, cv2.CC_STAT_AREA], i) for i in range(1, n)
            if st[i, cv2.CC_STAT_HEIGHT] > 1.5 * st[i, cv2.CC_STAT_WIDTH] and 0.2 < cen[i][0] / f.shape[1] < 0.8]
    if not cand: return None, None
    i = max(cand)[1]
    blob = (lab == i).astype(np.uint8) * 255
    blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    return blob, i


def corners(blob):
    cnt = max(cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], key=cv2.contourArea)
    hull = cv2.convexHull(cnt).reshape(-1, 2).astype(np.float32)
    s, d = hull.sum(1), np.diff(hull, axis=1).ravel()
    return np.array([hull[s.argmin()], hull[d.argmin()], hull[s.argmax()], hull[d.argmax()]], np.float32)  # tl, tr, br, bl


cap = cv2.VideoCapture(SRC); fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
scr = cv2.VideoCapture(SCR); sf = []
while True:
    ok, f = scr.read()
    if not ok: break
    sf.append(f)
masks, quads = [], []
for f in frames:
    b, _ = grey_mask(f); masks.append(b); quads.append(corners(b) if b is not None else None)
missing = [k for k, q in enumerate(quads) if q is None]
assert len(missing) < 3, f"screen not found in frames {missing}"
for k in missing: quads[k] = quads[k - 1] if k else quads[k + 1]
Q = np.array(quads)
Qs = np.array([Q[max(0, k - 2):k + 3].mean(0) for k in range(len(Q))])   # 5-frame smoothing
H, W = frames[0].shape[:2]
out = cv2.VideoWriter("clips/_s1_screen.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
for k, f in enumerate(frames):
    q = Qs[k]; c = q.mean(0); q = (c + (q - c) * 1.08).astype(np.float32)   # overfill 8%: rounded corners make the fitted quad sit inside the glass
    sw, sh = np.linalg.norm(q[1] - q[0]), np.linalg.norm(q[3] - q[0])
    s = sf[min(k, len(sf) - 1)]
    th, tw = s.shape[:2]; cw = int(th * sw / sh)                       # crop the TikTok frame to the screen's aspect
    x0 = max(0, (tw - cw) // 2); s = s[:, x0:x0 + min(cw, tw)]
    th, tw = s.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [tw, 0], [tw, th], [0, th]]), q)
    warped = cv2.warpPerspective(s, M, (W, H), flags=cv2.INTER_LINEAR)
    region = cv2.warpPerspective(np.full((th, tw), 255, np.uint8), M, (W, H))
    m = masks[k] if masks[k] is not None else region
    m = cv2.bitwise_and(cv2.dilate(m, np.ones((5, 5), np.uint8)), region)
    a = cv2.GaussianBlur(m, (5, 5), 0).astype(np.float32)[..., None] / 255
    g = (warped.astype(np.float32) * 0.95)                                # a lit screen at dusk, a touch under full white
    out.write((f * (1 - a) + g * a).astype(np.uint8))
out.release()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "clips/_s1_screen.mp4", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
                "-pix_fmt", "yuv420p", OUT], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", OUT, "-vf", "fps=2,scale=240:-1,tile=10x1", "-frames:v", "1", "qc/S1_screen_check.jpg"], check=True)
print(OUT, len(frames), "frames, screen missing in", missing)
