"""Remove the AI's own 5G badge left peeking out beside the pasted real one (free). Only pixels OUTSIDE the paste mask, inside
a box around the real badge, that are ink (dark or teal) get inpainted; thin lines inpaint cleanly (2026-10-19).
  python3 badge_fix.py IN_RAW IN_LABEL OUT"""
import sys, cv2, numpy as np
import label
raw, lab, out = sys.argv[1:4]
img = cv2.imread(raw); H, _ = label.fit(img); _, m = label.paste(img, H)
L = cv2.imread(lab); h, w = L.shape[:2]
sx = label.REAL.shape[1] / 1112
box = np.float32([[760, 220], [960, 220], [960, 470], [760, 470]]) * sx   # around the 5G badge in crop_tub_hi coords
q = cv2.perspectiveTransform(box.reshape(-1, 1, 2), H).reshape(-1, 2).astype(np.int32)
reg = np.zeros((h, w), np.uint8); cv2.fillPoly(reg, [q], 255)
hsv = cv2.cvtColor(L, cv2.COLOR_BGR2HSV)
bgv = cv2.morphologyEx(hsv[..., 2], cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))   # local paper brightness (ink closed away)
ink = (((bgv.astype(int) - hsv[..., 2]) > 9) | ((hsv[..., 1] > 24) & (hsv[..., 0] > 70) & (hsv[..., 0] < 105))).astype(np.uint8) * 255
outside = (m[..., 0] < 0.8).astype(np.uint8) * 255
edge = label._EDGE.get(H.tobytes(), w); reg[:, edge - 3:] = 0   # never touch the tub's own right edge
bad = cv2.dilate(ink & outside & reg, np.ones((3, 3), np.uint8))
# keep the REAL badge itself (its border sits on the soft mask edge)
rb = cv2.perspectiveTransform((np.float32([[828, 343], [914, 343], [914, 450], [828, 450]]) * sx).reshape(-1, 1, 2), H).reshape(-1, 2).astype(np.int32)
keep = np.zeros((h, w), np.uint8); cv2.fillPoly(keep, [rb], 255); bad[keep > 0] = 0
print("pixels", int((bad > 0).sum()))
# fill from nearby PAPER only (normalized blur over non-ink, non-pasted pixels), so no teal or black bleeds in
valid = ((ink == 0) & (outside > 0) & (bad == 0)).astype(np.float32)
num = cv2.GaussianBlur(L.astype(np.float32) * valid[..., None], (0, 0), 5); den = cv2.GaussianBlur(valid, (0, 0), 5)[..., None]
est = np.where(den > 0.02, num / np.maximum(den, 1e-3), L).clip(0, 255).astype(np.uint8)
soft = cv2.GaussianBlur(bad.astype(np.float32) / 255, (0, 0), 1.0)[..., None]
cv2.imwrite(out, (est * soft + L * (1 - soft)).astype(np.uint8))
