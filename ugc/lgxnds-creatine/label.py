"""Paste the REAL LGXNDS label (refs/crop_tub.png) over the AI tub's label (free). SIFT + RANSAC homography, label band only
(lid and anything above/below stay AI), shading carried over from the AI frame so it sits in the scene's light.

  python3 label.py still IN OUT        writes OUT + OUT_check.jpg (mask outline)
  python3 label.py video IN OUT [--ref N]   every frame, one homography fitted on frame N (locked camera)
"""
import subprocess, sys
import cv2, numpy as np

REAL = cv2.imread("refs/crop_tub.png")
BAND = np.zeros(REAL.shape[:2], np.uint8); cv2.rectangle(BAND, (22, 158), (678, 598), 255, -1)
_g = cv2.cvtColor(REAL, cv2.COLOR_BGR2HSV)
INK = cv2.dilate((((_g[..., 2] < 200) | (_g[..., 1] > 50)) & (BAND > 0)).astype(np.uint8) * 255, np.ones((11, 11), np.uint8))
CORE = np.zeros(REAL.shape[:2], np.uint8); cv2.rectangle(CORE, (188, 196), (560, 588), 255, -1)
_g = cv2.cvtColor(REAL, cv2.COLOR_BGR2HSV)  # right of x=560 only the print itself (the AI tub ends sooner than the real one)
_ink = cv2.dilate((((_g[..., 2] < 150) | (_g[..., 1] > 60))).astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
_ink[:, :560] = 0; _ink[:196] = 0; _ink[588:] = 0; _ink[:, 672:] = 0
CORE = np.maximum(CORE, _ink)  # printed block right of the
# stripes/wordmark: the homography fits it well; the AI's stripes + vertical LGXNDS stay (they render right, the cylinder edges don't fit)
sift = cv2.SIFT_create(6000)
kR, dR = sift.detectAndCompute(cv2.cvtColor(REAL, cv2.COLOR_BGR2GRAY), BAND)


def fit(img):
    k, d = sift.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
    m = [a for a, b in cv2.BFMatcher().knnMatch(dR, d, k=2) if a.distance < 0.75 * b.distance]
    if len(m) < 25: return None, len(m)
    H, inl = cv2.findHomography(np.float32([kR[x.queryIdx].pt for x in m]), np.float32([k[x.trainIdx].pt for x in m]), cv2.RANSAC, 4.0)
    return (H if H is not None and inl.sum() >= 20 else None), int(inl.sum()) if inl is not None else 0


def paste(img, H):
    h, w = img.shape[:2]
    real = cv2.warpPerspective(REAL, H, (w, h), flags=cv2.INTER_LANCZOS4)
    m = cv2.warpPerspective(CORE, H, (w, h)).astype(np.float32) / 255
    dark = cv2.morphologyEx((cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[..., 2] < 70).astype(np.uint8), cv2.MORPH_OPEN, np.ones((31, 31), np.uint8))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   # the hand always stays in front of the label
    skin = ((hsv[..., 0] < 25) & (hsv[..., 1] > 60) & (hsv[..., 2] > 40) & (hsv[..., 2] < 200)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = m * (1 - cv2.dilate(skin, np.ones((7, 7), np.uint8)).astype(np.float32))
    m = m * (1 - cv2.dilate(dark, np.ones((9, 9), np.uint8)).astype(np.float32))   # big dark occluders (the bag) stay in front
    m = cv2.GaussianBlur(m, (0, 0), 3.0)[..., None]
    shade = cv2.GaussianBlur(img.astype(np.float32), (0, 0), 25) / (cv2.GaussianBlur(real.astype(np.float32), (0, 0), 25) + 1)
    lum = np.clip(shade.mean(axis=2, keepdims=True), 0.6, 1.25)
    out = np.clip(real.astype(np.float32) * lum, 0, 255)
    return (out * m + img.astype(np.float32) * (1 - m)).astype(np.uint8), m


if __name__ == "__main__":
    mode, src, dst = sys.argv[1:4]
    if mode == "still":
        img = cv2.imread(src); H, n = fit(img); print("inliers", n)
        if H is None: sys.exit("no fit")
        out, m = paste(img, H); cv2.imwrite(dst, out)
        chk = out.copy(); cs, _ = cv2.findContours((m[..., 0] > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(chk, cs, -1, (0, 0, 255), 2); cv2.imwrite(dst.rsplit(".", 1)[0] + "_check.jpg", chk)
    else:
        cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
        while True:
            ok, f = cap.read()
            if not ok: break
            frames.append(f)
        h, w = frames[0].shape[:2]; lastH = None; bad = 0; a0 = None
        C = np.float32([[22, 158], [678, 158], [678, 598], [22, 598]]).reshape(-1, 1, 2)
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                              "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
        # ONE homography per clip (locked camera, tub never moves): per-frame SIFT fits jitter by up to 25 px and the print
        # shimmers. Fit on the frame given by --ref (default 0 = the approved still).
        ref = int(sys.argv[sys.argv.index("--ref") + 1]) if "--ref" in sys.argv else 0
        H, n = fit(frames[ref]); print("ref frame", ref, "inliers", n)
        for f in frames:
            p.stdin.write(paste(f, H)[0].tobytes())
        p.stdin.close(); p.wait(); print(f"{len(frames)} frames, {bad} without a fresh fit")
