"""Paste the REAL SoFyre bag's lower print (4 icons + KEY BENEFITS + NET WT) over the AI bag (free). The AI draws 5 icons and
fake fine print there. Homography fitted per frame on the top print (SOFYRE / RODENT / mouse, which the AI keeps right),
corners smoothed over time so the print doesn't jitter. The real photo has a pouch over its lower right corner, so that
part (ACTIVE INGREDIENTS block, edge of the icon row) is filled with plain bag black / band white, never invented text.

  python3 bagfix.py frame CLIP T OUT      one frame at T seconds -> OUT + OUT_check.jpg
  python3 bagfix.py video CLIP OUT        every frame
"""
import subprocess, sys
import cv2, numpy as np

REAL = cv2.imread("refs/bag_front.jpg")
R = REAL.copy()
blk = REAL[470:575, 445:540]                               # plain bag black (polygon texture), right of the whiskers
R[575:680, 445:540] = cv2.resize(blk, (95, 105))
R[680:762, 335:540] = np.median(REAL[690:700, 120:300].reshape(-1, 3), 0)   # band white: ACTIVE INGREDIENTS block blanked
R[762:805, 445:540] = cv2.resize(blk, (95, 43))
REAL_AA = cv2.GaussianBlur(R, (0, 0), 0.6)
FIT = np.zeros(REAL.shape[:2], np.uint8); FIT[110:560, 60:520] = 255
PASTE = np.zeros(REAL.shape[:2], np.uint8); PASTE[572:800, 44:528] = 255
sift = cv2.SIFT_create(4000)
kR, dR = sift.detectAndCompute(cv2.cvtColor(REAL, cv2.COLOR_BGR2GRAY), FIT)
HAND = False
OCC = False
BANDL = np.zeros(REAL.shape[:2], np.uint8); BANDL[678:764, :] = 255            # real white band rows
BELOW = np.zeros(REAL.shape[:2], np.uint8); BELOW[764:, :] = 255
_hsv = cv2.cvtColor(R, cv2.COLOR_BGR2HSV)
INK = np.where(BANDL > 0, _hsv[..., 2] < 140, (_hsv[..., 2] > 85) | (_hsv[..., 1] > 90)).astype(np.uint8) * 255
INK[PASTE == 0] = 0; INK[:, 445:] = 0                                         # only real print, never the filled corner
INK = cv2.GaussianBlur(cv2.dilate(INK, np.ones((2, 2), np.uint8)), (0, 0), 0.7)
C = np.float32([[60, 110], [520, 110], [520, 800], [60, 800]]).reshape(-1, 1, 2)


def fit(img):
    k, d = sift.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
    if d is None: return None, 0
    m = [a for a, b in cv2.BFMatcher().knnMatch(dR, d, k=2) if a.distance < 0.75 * b.distance]
    if len(m) < 20: return None, len(m)
    H, inl = cv2.findHomography(np.float32([kR[x.queryIdx].pt for x in m]), np.float32([k[x.trainIdx].pt for x in m]), cv2.RANSAC, 3.0)
    return (H if H is not None and inl.sum() >= 15 else None), int(inl.sum()) if inl is not None else 0


def paste(img, H):
    """Clean the AI bag's lower part to plain bag black + band white (real layout), then lay the real print's ink on it."""
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV); V, S, Hh = hsv[..., 2], hsv[..., 1], hsv[..., 0]
    region = cv2.warpPerspective(PASTE, H, (w, h)) > 0
    dark = (V < 70).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)))
    big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); hull = np.zeros((h, w), np.uint8)
    cv2.fillConvexPoly(hull, cv2.convexHull(np.argwhere(lab == big)[:, ::-1]), 1)
    hull = cv2.erode(hull, np.ones((5, 5), np.uint8)) > 0             # stay inside the bag outline
    band = cv2.warpPerspective(BANDL, H, (w, h)) > 0
    ink = cv2.warpPerspective(INK, H, (w, h), flags=cv2.INTER_LINEAR).astype(np.float32) / 255
    real = cv2.warpPerspective(REAL_AA, H, (w, h), flags=cv2.INTER_LANCZOS4).astype(np.float32)
    reg = region & hull
    blk = np.median(img[reg & (V < 70)], 0) if (reg & (V < 70)).any() else np.array([25, 25, 25])
    wht = np.median(img[reg & (V > 150) & (S < 40)], 0) if (reg & (V > 150) & (S < 40)).any() else np.array([225, 225, 225])
    bg = np.where(band[..., None], wht, blk).astype(np.float32)
    bg = cv2.GaussianBlur(bg, (0, 0), 1.0)
    top = cv2.warpPerspective(FIT, H, (w, h)) > 0
    g = np.clip(img[top].mean() / (cv2.warpPerspective(REAL, H, (w, h))[top].mean() + 1), 0.7, 1.3)
    out = bg * (1 - ink[..., None]) + np.clip(real * g, 0, 255) * ink[..., None]
    occ = np.zeros((h, w), bool)
    if OCC: occ |= (S > 70) & ((Hh < 20) | (Hh > 50))                # cinnamon / mint in front (S7 only; lime icons are hue 25-45)
    occ |= (V > 170) & (S < 40) & ~band & (cv2.warpPerspective(BELOW, H, (w, h)) > 0)   # white pouches in front of the bag foot
    if HAND: occ |= (Hh < 25) & (S > 60) & (V > 40)                  # the hand stays in front (S1 only)
    occ = cv2.dilate(cv2.morphologyEx(occ.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), np.ones((7, 7), np.uint8))
    m = (reg & (occ == 0)).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), 1.5)[..., None]
    return (out * m + img.astype(np.float32) * (1 - m)).astype(np.uint8), m


def frames_of(src):
    cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr, fps


if __name__ == "__main__":
    mode = sys.argv[1]; HAND = '--hand' in sys.argv; OCC = '--occ' in sys.argv; sys.argv = [a for a in sys.argv if a not in ('--hand', '--occ')]
    if mode == "frame":
        fr, fps = frames_of(sys.argv[2]); img = fr[min(len(fr) - 1, int(float(sys.argv[3]) * fps))]
        H, n = fit(img); print("inliers", n)
        if H is None: sys.exit("no fit")
        out, m = paste(img, H); dst = sys.argv[4]
        cv2.imwrite(dst, np.hstack([img, out]))
        chk = out.copy(); cs, _ = cv2.findContours((m[..., 0] > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(chk, cs, -1, (0, 0, 255), 2); cv2.imwrite(dst.rsplit(".", 1)[0] + "_check.jpg", chk)
    else:
        src, dst = sys.argv[2:4]
        fr, fps = frames_of(src); h, w = fr[0].shape[:2]
        corners = []
        for f in fr:
            H, n = fit(f)
            corners.append(cv2.perspectiveTransform(C, H).reshape(-1) if H is not None else None)
        ok = [i for i, c in enumerate(corners) if c is not None]
        print(f"{len(ok)}/{len(fr)} frames fitted")
        A = np.array([corners[i] for i in ok]); idx = np.arange(len(fr))
        full = np.stack([np.interp(idx, ok, A[:, j]) for j in range(8)], 1)   # fill missed frames
        k = 7; pad = np.pad(full, ((k // 2, k // 2), (0, 0)), mode="edge")
        sm = np.stack([np.convolve(pad[:, j], np.ones(k) / k, "valid") for j in range(8)], 1)   # smooth the jitter
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps),
                              "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
        for f, c in zip(fr, sm):
            H = cv2.getPerspectiveTransform(C.reshape(4, 2), c.reshape(4, 2).astype(np.float32))
            p.stdin.write(paste(f, H)[0].tobytes())
        p.stdin.close(); p.wait(); print("wrote", dst)
