"""Paste the REAL BodyJ label (refs/bottle_front.png) over the AI bottle's label in a clip where the bottle MOVES (free).
Per-frame SIFT + RANSAC homography on the label, corner paths smoothed over time (no jitter/shimmer), frames without a fit
interpolated. Only the printed middle of the label is pasted (cylinder edges stay AI); the hand stays in front; the AI
frame's light carries onto the print. Built 2026-10-17 from ugc/lgxnds-creatine/label.py (locked-camera version).

  python3 label_track.py IN OUT [--sigma 3] [--frames a:b] [--ref IMG --rect x0,y0,x1,y1] [--roi x0,y0,x1,y1] [--noskin]    writes OUT + OUT_check.jpg (mask outline on the middle frame)
"""
import subprocess, sys
import cv2, numpy as np
from scipy.ndimage import gaussian_filter1d

_a = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
REAL = cv2.imread(_a("--ref", "refs/bottle_front.png"))   # --ref refs/box_and_bottle.png --rect 328,118,606,758 = the box
X0, Y0, X1, Y1 = map(int, _a("--rect", "62,342,318,690").split(","))
BAND = np.zeros(REAL.shape[:2], np.uint8); cv2.rectangle(BAND, (X0 - 4, Y0 - 12), (X1 + 4, Y1 + 8), 255, -1)  # where SIFT looks
CORE = np.zeros(REAL.shape[:2], np.uint8); cv2.rectangle(CORE, (X0, Y0), (X1, Y1), 255, -1)                # what gets pasted
REAL_AA = cv2.GaussianBlur(REAL, (0, 0), 0.5)
sift = cv2.SIFT_create(4000)
kR, dR = sift.detectAndCompute(cv2.cvtColor(REAL, cv2.COLOR_BGR2GRAY), BAND)
C = np.float32([[X0, Y0], [X1, Y0], [X1, Y1], [X0, Y1]]).reshape(-1, 1, 2)


ROI = _a("--roi", None)   # x0,y0,x1,y1 in frame pixels: only look for the label there (S9: the box has the same print)


def fit(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); mk = None
    if ROI:
        a0, b0, a1, b1 = map(int, ROI.split(",")); mk = np.zeros(g.shape, np.uint8); mk[b0:b1, a0:a1] = 255
    k, d = sift.detectAndCompute(g, mk)
    if d is None: return None, 0
    m = [a for a, b in cv2.BFMatcher().knnMatch(dR, d, k=2) if a.distance < 0.75 * b.distance]
    if len(m) < 15: return None, len(m)
    H, inl = cv2.findHomography(np.float32([kR[x.queryIdx].pt for x in m]), np.float32([k[x.trainIdx].pt for x in m]), cv2.RANSAC, 3.0)
    n = int(inl.sum()) if inl is not None else 0
    return (H if H is not None and n >= 12 else None), n


def paste(img, H):
    h, w = img.shape[:2]
    real = cv2.warpPerspective(REAL_AA, H, (w, h), flags=cv2.INTER_LANCZOS4)
    m = cv2.warpPerspective(CORE, H, (w, h)).astype(np.float32) / 255
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   # fingers always stay in front of the label
    skin = ((hsv[..., 0] < 25) & (hsv[..., 1] > 45) & (hsv[..., 2] > 60) & (hsv[..., 2] < 245)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    if "--noskin" not in sys.argv:   # hand-free shots (Youtheory S3): coral print reads as skin, so skip the hand mask
        m = m * (1 - cv2.dilate(skin, np.ones((9, 9), np.uint8)).astype(np.float32))
    m = cv2.GaussianBlur(m, (0, 0), 2.0)[..., None]
    # paper colour per channel (text removed by a median filter): carries the scene's warm light and the bottle's
    # curve shading onto the print, so no cool grey patch shows
    pap = lambda x: cv2.GaussianBlur(cv2.medianBlur(x, 21).astype(np.float32), (0, 0), 6)
    lum = np.clip(pap(img) / (pap(real) + 1), 0.6, 1.3)
    out = np.clip(real.astype(np.float32) * lum, 0, 255)
    return (out * m + img.astype(np.float32) * (1 - m)).astype(np.uint8), m


if __name__ == "__main__":
    src, dst = sys.argv[1:3]
    sigma = float(sys.argv[sys.argv.index("--sigma") + 1]) if "--sigma" in sys.argv else 3.0
    cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
    while True:
        ok, f = cap.read()
        if not ok: break
        frames.append(f)
    a, b = 0, len(frames)
    if "--frames" in sys.argv: a, b = map(int, sys.argv[sys.argv.index("--frames") + 1].split(":"))
    pts, ok = np.zeros((len(frames), 4, 2), np.float32), np.zeros(len(frames), bool)
    for i in range(a, b):
        H, n = fit(frames[i])
        if H is not None: pts[i] = cv2.perspectiveTransform(C, H).reshape(4, 2); ok[i] = True
    idx = np.arange(a, b); good = idx[ok[a:b]]
    print(f"fits {len(good)}/{b - a}")
    if len(good) < 0.6 * (b - a): sys.exit("too few fits: label not trackable in this clip")
    for c in range(4):  # interpolate gaps, then smooth each corner path
        for xy in range(2):
            pts[a:b, c, xy] = gaussian_filter1d(np.interp(idx, good, pts[good, c, xy]), sigma, mode="nearest")
    h, w = frames[0].shape[:2]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
    for i, f in enumerate(frames):
        if a <= i < b:
            H = cv2.getPerspectiveTransform(C.reshape(4, 2), pts[i]); f, m = paste(f, H)
            if i == (a + b) // 2:
                chk = f.copy(); cs, _ = cv2.findContours((m[..., 0] > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(chk, cs, -1, (0, 0, 255), 2); cv2.imwrite(dst.rsplit(".", 1)[0] + "_check.jpg", chk)
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
