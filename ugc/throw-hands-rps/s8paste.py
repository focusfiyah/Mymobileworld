"""Free fix: warp the REAL box front (refs/real_box.jpg) onto the top face of the box lying on the table in stills/S8.png."""
import cv2, numpy as np
st = cv2.imread("old/S8_v1.png"); k = 0.2
box = cv2.resize(cv2.imread("refs/real_box.jpg"), None, fx=k, fy=k, interpolation=cv2.INTER_AREA)   # shrink first: warping 1600px down to ~150px aliases
src = np.float32([[333, 312], [1198, 302], [1222, 1438], [392, 1516]]) * k          # real front TL TR BR BL
dst = np.float32([[478, 350], [393, 415], [245, 352], [325, 292]])            # S8 face: top edge = the open (flap) end
H = cv2.getPerspectiveTransform(src, dst); h, w = st.shape[:2]
real = cv2.warpPerspective(box, H, (w, h), flags=cv2.INTER_LANCZOS4)
core = np.zeros(box.shape[:2], np.uint8); cv2.fillConvexPoly(core, src.astype(np.int32), 255)
core = cv2.erode(core, np.ones((3, 3), np.uint8))
m = cv2.GaussianBlur(cv2.warpPerspective(core, H, (w, h)).astype(np.float32) / 255, (0, 0), 0.7)[..., None]
pap = lambda x: cv2.GaussianBlur(x.astype(np.float32), (0, 0), 12)
lum = np.clip(pap(cv2.cvtColor(st, cv2.COLOR_BGR2GRAY)) / (pap(cv2.cvtColor(real, cv2.COLOR_BGR2GRAY)) + 1), 0.6, 1.3)[..., None]
out = (np.clip(real * lum, 0, 255) * m + st * (1 - m)).astype(np.uint8)
cv2.imwrite("stills/S8.png", out)
cv2.imwrite("qc/S8_box_fix.png", cv2.resize(out[270:480, 230:520], None, fx=3, fy=3, interpolation=cv2.INTER_LANCZOS4))
