"""S1 free fix (2026-10-24, Ralph: the held shoe must be the RIGHT shoe): reflect ONLY the held shoe across its own long
axis (side tab moves to the outer = right side, toe and heel stay put), keep the hand on top, and put the insole logo
back unmirrored (reflect twice = a shift). Input stills/S1.png -> stills/S1_r3.png. Free, no generation."""
import cv2, numpy as np
im = cv2.imread("stills/S1.png"); H, W = im.shape[:2]
obj = cv2.imread("qc/obj.png", 0) > 0
b, g, r = [im[..., i].astype(int) for i in range(3)]
ycc = cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb)
skin = cv2.inRange(ycc, (0, 135, 85), (255, 180, 135)) > 0
crimson = (g < 60) & (r > 70) & (r > b + 25)
hand = skin & ~crimson & (np.arange(W)[None, :] > 380) & (np.arange(H)[:, None] > 560)
hand = cv2.morphologyEx(hand.astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)) > 0
shoe = obj & ~hand
# long axis of the shoe by PCA
ys, xs = np.nonzero(shoe); c = np.array([xs.mean(), ys.mean()])
cov = np.cov(np.vstack([xs - c[0], ys - c[1]])); w, v = np.linalg.eigh(cov); d = v[:, np.argmax(w)]
# reflection across the line through c with direction d: p' = c + R (p - c), R = 2 d d^T - I
R = 2 * np.outer(d, d) - np.eye(2)
M = np.hstack([R, (c - R @ c)[:, None]])          # forward map p -> p'
refl = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
rshoe = cv2.warpAffine(shoe.astype(np.uint8) * 255, M, (W, H), flags=cv2.INTER_NEAREST) > 0
# insole logo: white box inside the crimson insole, put back unmirrored at its reflected place (pure shift)
ins = (crimson & obj).astype(np.uint8) * 255
cnts, _ = cv2.findContours(ins, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
big = cv2.convexHull(np.vstack(cnts)); fill = np.zeros_like(ins); cv2.drawContours(fill, [big], -1, 255, -1)
white = (b > 170) & (g > 170) & (r > 170)
logo = ((fill > 0) & white).astype(np.uint8) * 255
logo = cv2.morphologyEx(logo, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(logo)
k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); x, y, bw, bh = st[k, :4]
print("logo box", x, y, bw, bh)
box = np.zeros((H, W), np.uint8); box[y - 6:y + bh + 6, x - 6:x + bw + 6] = 255
box = (box > 0) & (fill > 0)
bc = np.array([x + bw / 2, y + bh / 2]); t = (c + R @ (bc - c)) - bc
T = np.float32([[1, 0, t[0]], [0, 1, t[1]]])
shift = cv2.warpAffine(im, T, (W, H)); sbox = cv2.warpAffine(box.astype(np.uint8) * 255, T, (W, H)) > 0
out = im.copy()
gap = shoe & ~rshoe                                  # old shoe area the reflection does not cover: inpaint brick
out = cv2.inpaint(out, (cv2.dilate(gap.astype(np.uint8) * 255, np.ones((5, 5), np.uint8))), 7, cv2.INPAINT_TELEA)
soft = cv2.GaussianBlur(rshoe.astype(np.float32), (5, 5), 0)[..., None]
out = (refl * soft + out * (1 - soft)).astype(np.uint8)
sb = cv2.GaussianBlur(sbox.astype(np.float32), (3, 3), 0)[..., None]
out = (shift * sb + out * (1 - sb)).astype(np.uint8)
hs = cv2.GaussianBlur(hand.astype(np.float32), (3, 3), 0)[..., None]
out = (im * hs + out * (1 - hs)).astype(np.uint8)
cv2.imwrite("stills/S1_r3.png", out)
print("axis", d, "logo shift", t)
