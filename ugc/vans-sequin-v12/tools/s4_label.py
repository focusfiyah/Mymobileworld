"""S4 free fix (PLAYBOOK §6 Vans lesson 6): the AI drew the heel label inverted (black box, white print). Invert the
colours inside the label box only -> white label, black print, like refs/real_heel_label.jpg. stills/S4_r3.png -> stills/S4_r3fix.png"""
import cv2, numpy as np
im = cv2.imread("stills/S4_r3.png"); x0, y0, x1, y1 = 260, 680, 460, 790
win = im[y0:y1, x0:x1]
dark = (win.max(axis=2) < 80).astype(np.uint8) * 255
n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)))
k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); bx, by, bw, bh = st[k, :4]
print("label box", x0 + bx, y0 + by, bw, bh)
box = np.zeros(dark.shape, np.uint8); box[by:by + bh, bx:bx + bw] = 255
box = cv2.erode(box, np.ones((3, 3), np.uint8))
m = cv2.GaussianBlur(box.astype(np.float32) / 255, (3, 3), 0)[..., None]
inv = 255 - win.astype(np.float32)
inv = inv * 0.93 + 8                     # off-white like the real label, not paper white
im[y0:y1, x0:x1] = (inv * m + win * (1 - m)).astype(np.uint8)
cv2.imwrite("stills/S4_r3fix.png", im)
