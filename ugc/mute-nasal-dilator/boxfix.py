"""Paste the REAL Mute box front (refs/box_real_front.png) over the AI box in a clip (free). Per-frame SIFT+RANSAC homography
(the box moves), fits smoothed over neighbours, skin kept in front, frames without a fit left as the AI made them (motion blur).
  python3 boxfix.py CLIP OUT [--check N]   writes OUT (+ fix/<name>_check.jpg every N frames)"""
import sys, subprocess
import cv2, numpy as np
src, dst = sys.argv[1:3]
photo = cv2.imread("refs/grace_box_photo.jpg"); f = 1.92
x0, y0, x1, y1 = [int(v * f) for v in (190, 478, 503, 1388)]
REAL = photo[y0:y1, x0:x1]; REAL = cv2.resize(REAL, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_AREA)
cv2.imwrite("refs/box_real_front.png", REAL)
h0, w0 = REAL.shape[:2]
core = np.zeros((h0, w0), np.uint8); cv2.rectangle(core, (int(w0*.04), int(h0*.03)), (int(w0*.96), int(h0*.97)), 255, -1)
sift = cv2.SIFT_create(4000)
kR, dR = sift.detectAndCompute(cv2.cvtColor(REAL, cv2.COLOR_BGR2GRAY), None)
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
while True:
    ok, fr = cap.read()
    if not ok: break
    frames.append(fr)
h, w = frames[0].shape[:2]
def fit(img):
    k, d = sift.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
    if d is None or len(k) < 30: return None, 0
    m = [a for a, b in cv2.BFMatcher().knnMatch(dR, d, k=2) if a.distance < 0.75 * b.distance]
    if len(m) < 18: return None, len(m)
    H, inl = cv2.findHomography(np.float32([kR[x.queryIdx].pt for x in m]), np.float32([k[x.trainIdx].pt for x in m]), cv2.RANSAC, 3.0)
    if H is None or inl.sum() < 14: return None, 0
    return H, int(inl.sum())
C = np.float32([[0, 0], [w0, 0], [w0, h0], [0, h0]]).reshape(-1, 1, 2)
fits = [fit(fr) for fr in frames]
corners = [cv2.perspectiveTransform(C, H)[:, 0] if H is not None else None for H, n in fits]
def sane(c):
    if c is None: return False
    a = cv2.contourArea(c.astype(np.float32)); return 0.02 * w * h < a < 1.5 * w * h and cv2.isContourConvex(c.astype(np.float32).reshape(-1, 1, 2))
good = [i for i, c in enumerate(corners) if sane(c)]
print(src, "fits", len(good), "of", len(frames), "inliers", [n for H, n in fits])
Hs = {}
for i in good:   # smooth the 4 corners over +-2 good neighbours
    nb = [j for j in good if abs(j - i) <= 2]; c = np.mean([corners[j] for j in nb], axis=0)
    Hs[i] = cv2.getPerspectiveTransform(np.float32([[0, 0], [w0, 0], [w0, h0], [0, h0]]), c.astype(np.float32))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
chk = int(sys.argv[sys.argv.index("--check") + 1]) if "--check" in sys.argv else 0
name = dst.split("/")[-1].rsplit(".", 1)[0]; cks = []
for i, fr in enumerate(frames):
    out = fr
    if i in Hs:
        H = Hs[i]
        real = cv2.warpPerspective(REAL, H, (w, h), flags=cv2.INTER_LANCZOS4)
        m = cv2.warpPerspective(core, H, (w, h)).astype(np.float32) / 255
        hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)
        skin = (((hsv[..., 0] < 25) & (hsv[..., 1] > 50) & (hsv[..., 2] > 40)) | (((hsv[..., 0] > 160) | (hsv[..., 0] < 12)) & (hsv[..., 1] > 22) & (hsv[..., 2] > 110))).astype(np.uint8)
        skin = cv2.dilate(cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)), np.ones((9, 9), np.uint8))
        m = cv2.GaussianBlur(m * (1 - skin), (0, 0), 2.0)[..., None]
        pap = lambda x: cv2.GaussianBlur(x.astype(np.float32), (0, 0), 25)
        lum = np.clip(pap(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)) / (pap(cv2.cvtColor(real, cv2.COLOR_BGR2GRAY)) + 1), 0.7, 1.4)[..., None]
        out = (np.clip(real * lum, 0, 255) * m + fr * (1 - m)).astype(np.uint8)
    if chk and i % chk == 0: cks.append(cv2.resize(out, (w // 2, h // 2)))
    p.stdin.write(out.tobytes())
p.stdin.close(); p.wait()
if cks: cv2.imwrite(f"fix/{name}_check.jpg", np.hstack(cks[:6]))
