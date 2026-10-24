"""Free colour fix for S1_r2 (2026-10-24): the AI drew the original jar opaque coral with a bright lime lid; the real one
(refs/real/tp_1-1_*.jpg) is frosted pale peach with a pale pastel-green lid. Pull the jar's colours toward the real
ones inside the jar's own colour mask only (hand, rings, room untouched). -> stills/S1_r2_fix.png"""
import cv2, numpy as np
im = cv2.imread("stills/S1_r2.png"); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
H, W = im.shape[:2]; box = np.zeros((H, W), bool); box[400:900, 60:560] = True
h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
coral = box & (h >= 0) & (h <= 14) & (s > 90) & (v > 120)       # jar body
lime = box & (h >= 28) & (h <= 45) & (s > 90) & (v > 120)        # lid
for m, s_mul, v_add, h_to in ((coral, 0.62, 18, 10), (lime, 0.55, 22, 38)):
    k = cv2.GaussianBlur(m.astype(np.float32), (9, 9), 0)        # soft edge so no outline
    s2 = s * (1 - k) + s * s_mul * k; v2 = np.clip(v + v_add * k, 0, 255); h2 = h * (1 - k) + h_to * k
    s, v, h = s2, v2, h2
out = cv2.cvtColor(np.dstack([h, s, v]).clip(0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
cv2.imwrite("stills/S1_r2_fix.png", out); print("coral px", int(coral.sum()), "lime px", int(lime.sum()))
