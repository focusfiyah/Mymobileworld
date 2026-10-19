"""Free fix: paste the REAL box photo (refs/real_box.jpg, white bg cut out) over the AI box in stills/S3.png, Grace's fingers kept in front.
  python3 s3paste.py [scale] [cx] [top]"""
import sys, cv2, numpy as np
sc = float(sys.argv[1]) if len(sys.argv) > 1 else 0.41
cx = int(sys.argv[2]) if len(sys.argv) > 2 else 392
top = int(sys.argv[3]) if len(sys.argv) > 3 else 400
st = cv2.imread("old/S3_v1.png"); box = cv2.imread("refs/real_box.jpg")
nw = (box.min(2) < 235).astype(np.uint8)            # not-white = box
nw = cv2.morphologyEx(nw, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
n, lab, stats, _ = cv2.connectedComponentsWithStats(nw); k = 1 + np.argmax(stats[1:, 4]); m = (lab == k).astype(np.uint8)
cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); m = np.zeros_like(m); cv2.drawContours(m, cnts, -1, 1, -1)
x, y, w, h = cv2.boundingRect(m); box, m = box[y:y+h, x:x+w], m[y:y+h, x:x+w]
box = cv2.resize(box, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA); m = cv2.resize(m.astype(np.float32), (box.shape[1], box.shape[0]), interpolation=cv2.INTER_AREA)
m = cv2.erode(m, np.ones((3, 3), np.uint8)); m = cv2.GaussianBlur(m, (0, 0), 0.8)
H, W = st.shape[:2]; bh, bw = box.shape[:2]; x0 = cx - bw // 2
full = np.zeros_like(st, np.float32); fm = np.zeros((H, W), np.float32)
full[top:top+bh, x0:x0+bw] = box; fm[top:top+bh, x0:x0+bw] = m
hsv = cv2.cvtColor(st, cv2.COLOR_BGR2HSV)

skin = (((hsv[..., 0] < 25) | (hsv[..., 0] > 165)) & (hsv[..., 1] > 35) & (hsv[..., 2] > 35)).astype(np.uint8)
skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
# Grace's fingers that overlap the box (the table is skin-hued too, so only look inside these two rects)
keep = np.zeros_like(skin)
for (xa, ya, xb, yb) in [(395, 370, 640, 548), (230, 900, 350, 1010)]:
    keep[ya:yb, xa:xb] = skin[ya:yb, xa:xb]
n, lab, stats, _ = cv2.connectedComponentsWithStats(keep)
for i in range(1, n):
    if stats[i, 4] < 400: keep[lab == i] = 0
nail = ((hsv[..., 1] < 70) & (hsv[..., 1] > 12) & (hsv[..., 2] > 170)).astype(np.uint8) & cv2.dilate(keep, np.ones((11, 11), np.uint8))
fg = cv2.morphologyEx(np.maximum(keep, nail), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
fg = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 1.2)
lumS = cv2.GaussianBlur(cv2.cvtColor(st, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 30)
a = (fm * (1 - fg))[..., None]
out = (full * 0.97 * a + st * (1 - a)).clip(0, 255).astype(np.uint8)
# fill what is left of the AI box outside the real one (its flap and bottom corner) from the surroundings
pur = np.zeros(st.shape[:2], np.uint8); r = (slice(380, 1005), slice(225, 575))
pur[r] = ((hsv[r][..., 0] > 115) & (hsv[r][..., 0] < 165) & (hsv[r][..., 1] > 60)).astype(np.uint8)
pts = cv2.findNonZero(cv2.morphologyEx(pur, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)))
ai = np.zeros_like(pur); cv2.fillConvexPoly(ai, cv2.convexHull(np.vstack([pts.reshape(-1, 2), np.array([[255, 405], [530, 405], [524, 994], [250, 990]])]).astype(np.int32)), 1); ai = cv2.dilate(ai, np.ones((9, 9), np.uint8))
rem = (ai & (fm < 0.5) & (fg < 0.3)).astype(np.uint8)
rem = cv2.dilate(rem, np.ones((5, 5), np.uint8)) & (fm < 0.9).astype(np.uint8) & (fg < 0.3).astype(np.uint8)
bgfill = cv2.inpaint(st, (ai & (fg < 0.3)).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)   # background only, never the pasted box
rm = cv2.GaussianBlur(rem.astype(np.float32), (0, 0), 1.0)[..., None]
out = (bgfill * rm + out * (1 - rm)).astype(np.uint8)
cv2.imwrite("qc/S3_rem.png", rem * 255); print("remnant px", rem.sum())
cv2.imwrite("stills/S3.png", out); cv2.imwrite("qc/S3_fg.png", (fg * 255).astype(np.uint8))
print("box", bw, bh, "at", x0, top)
