"""Free fix (2026-10-21): the AI drew a Chanel-style CC turn-lock on the black bag. Inside the clasp box, inpaint the dark
lines between the gold so it reads as a plain gold clasp (no brand).  python3 clasp_fix.py stills/V1S2.png x0 y0 x1 y1"""
import sys, os, cv2, numpy as np
src = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6]); cur = src.replace(".png", "_clean.png")
im = cv2.imread(cur if os.path.exists(cur) else src); roi = im[y0:y1, x0:x1]
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
gold = ((hsv[..., 0] > 8) & (hsv[..., 0] < 35) & (hsv[..., 1] > 50) & (hsv[..., 2] > 90)).astype(np.uint8)
area = cv2.morphologyEx(gold, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))   # the clasp's footprint
foot = cv2.dilate(area, np.ones((3, 3), np.uint8)).astype(float)
g = gold.astype(float)[..., None]; k = (15, 15)                               # smooth gold from gold pixels only
fill = cv2.GaussianBlur(roi.astype(float) * g, k, 0) / np.maximum(cv2.GaussianBlur(g, k, 0)[..., None], 1e-3)
a = cv2.GaussianBlur(foot, (5, 5), 0)[..., None]
im[y0:y1, x0:x1] = (roi * (1 - a) + fill * a).astype(np.uint8)
cv2.imwrite(cur, im); print(cur, "clasp px", int(foot.sum()))
