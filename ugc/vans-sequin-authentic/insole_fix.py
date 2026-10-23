"""Free fix (2026-10-21): the AI drew the insole logo as a red box with a white outline and white VANS text; the real insole is a
solid white box with red VANS text. Inside the logo outline, swap: red -> insole-box white, white text -> insole red.
  python3 insole_fix.py stills/V1S1.png x0 y0 x1 y1   (search window around the logo) -> stills/V1S1_clean.png"""
import sys, cv2, numpy as np
src, (x0, y0, x1, y1) = sys.argv[1], map(int, sys.argv[2:6])
im = cv2.imread(src); roi = im[y0:y1, x0:x1].copy()
light = (roi.min(2) > 165).astype(np.uint8) * 255
cnts, _ = cv2.findContours(light, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if len(sys.argv) > 6:   # explicit outline corners in full-image coords: x0,y0 x1,y1 x2,y2 x3,y3
    box = np.array([[int(v) for v in a.split(",")] for a in sys.argv[6:10]]) - [x0, y0]
else:
    box = cv2.boxPoints(cv2.minAreaRect(max(cnts, key=cv2.contourArea))).astype(np.int32)
mask = np.zeros(light.shape, np.uint8); cv2.fillPoly(mask, [box], 255)
inner = cv2.erode(mask, np.ones((5, 5), np.uint8))               # inside the white outline
red = np.median(roi[(mask == 0) & (roi[:, :, 2] > roi[:, :, 1] + 40)], 0)  # insole red outside the box
white = np.array([236, 238, 240.])                                # BGR, off-white box
lum = roi.mean(2) / 255.0                                         # 0 = red bg, 1 = white text
t = np.clip((lum - 0.25) / 0.45, 0, 1)[..., None]                 # soft edges
swapped = white * (1 - t) + red * t
shade = (roi.astype(float).max(2, keepdims=True) / 255.0) ** 0.15  # keep a little of the original shading
out = roi.astype(float); m = (inner > 0)[..., None]
out = np.where(m, swapped * np.clip(shade * 1.05, 0.85, 1.0), out)
im[y0:y1, x0:x1] = np.clip(out, 0, 255).astype(np.uint8)
dst = src.replace(".png", "_clean.png"); cv2.imwrite(dst, im); print("wrote", dst, "box", box.tolist())
