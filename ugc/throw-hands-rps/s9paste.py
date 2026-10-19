"""Free fix: paste the REAL box photo (refs/real_box.jpg, white bg cut out) over the two AI boxes on the table in stills/S9.png."""
import cv2, numpy as np
st = cv2.imread("old/S9_v1.png"); H, W = st.shape[:2]
box = cv2.imread("refs/real_box.jpg")
nw = cv2.morphologyEx((box.min(2) < 235).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
n, lab, stats, _ = cv2.connectedComponentsWithStats(nw); m = (lab == 1 + np.argmax(stats[1:, 4])).astype(np.uint8)
cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); m = np.zeros_like(m); cv2.drawContours(m, cnts, -1, 1, -1)
x, y, w, h = cv2.boundingRect(m); box, m = box[y:y+h, x:x+w], m[y:y+h, x:x+w].astype(np.float32)
AI = [(208, 380, 382, 643), (408, 384, 557, 654)]      # AI box bboxes (x0 y0 x1 y1)
out = st.astype(np.float32); cover = np.zeros((H, W), np.float32); aim = np.zeros((H, W), np.uint8)
for (x0, y0, x1, y1) in AI:
    aim[y0:y1, x0:x1] = 1
    s = (y1 - y0 + 4) / h; b = cv2.resize(box, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32)
    mm = cv2.GaussianBlur(cv2.erode(cv2.resize(m, (b.shape[1], b.shape[0]), interpolation=cv2.INTER_AREA), np.ones((2, 2), np.uint8)), (0, 0), 0.7)
    bh, bw = b.shape[:2]; cx = (x0 + x1) // 2; X0, Y0 = cx - bw // 2, y1 + 2 - bh
    reg = out[Y0:Y0+bh, X0:X0+bw]
    lum = np.clip(cv2.GaussianBlur(cv2.cvtColor(st[Y0:Y0+bh, X0:X0+bw], cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 20).mean() /
                  cv2.cvtColor(b.astype(np.uint8), cv2.COLOR_BGR2GRAY)[mm > 0.5].mean(), 0.8, 1.15)
    out[Y0:Y0+bh, X0:X0+bw] = b * lum * mm[..., None] + reg * (1 - mm[..., None])
    cover[Y0:Y0+bh, X0:X0+bw] = np.maximum(cover[Y0:Y0+bh, X0:X0+bw], mm)
    print("box", bw, bh, "at", X0, Y0, "lum", round(float(lum), 2))
# what is left of the AI boxes outside the real ones: fill from the background (never from the pasted boxes)
hsv = cv2.cvtColor(st, cv2.COLOR_BGR2HSV)
aibox = aim & ((((hsv[..., 0] > 115) & (hsv[..., 0] < 165) & (hsv[..., 1] > 50)) | (hsv[..., 2] < 70))).astype(np.uint8)
aibox = cv2.dilate(cv2.morphologyEx(aibox, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)), np.ones((5, 5), np.uint8))
rem = (aibox & (cover < 0.5)).astype(np.uint8)
bg = cv2.inpaint(st, (cv2.dilate(aim, np.ones((5, 5), np.uint8)) * 255), 9, cv2.INPAINT_TELEA).astype(np.float32)
rm = cv2.GaussianBlur(rem.astype(np.float32), (0, 0), 1.0)[..., None]
out = bg * rm + out * (1 - rm); print("remnant px", rem.sum())
cv2.imwrite("stills/S9.png", out.clip(0, 255).astype(np.uint8))
o = cv2.imread("stills/S9.png")[360:670, 190:580]; cv2.imwrite("qc/S9_box_fix.png", cv2.resize(o, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4))
