"""S1 free fix step 1: masks for the held shoe and the hand (GrabCut + skin colour). Writes qc/s1_masks.jpg."""
import cv2, numpy as np
im = cv2.imread("stills/S1.png")
H, W = im.shape[:2]
rect = (150, 270, 430, 680)                       # x, y, w, h around the held shoe + hand
mask = np.zeros((H, W), np.uint8); bg = np.zeros((1, 65), np.float64); fg = np.zeros((1, 65), np.float64)
cv2.grabCut(im, mask, rect, bg, fg, 6, cv2.GC_INIT_WITH_RECT)
obj = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); ycc = cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb)
skin = cv2.inRange(ycc, (0, 135, 85), (255, 180, 135))
hand = cv2.bitwise_and(skin, obj)
n, lab, st, _ = cv2.connectedComponentsWithStats(hand)
if n > 1:
    big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); hand = np.where(lab == big, 255, 0).astype(np.uint8)
cv2.imwrite("qc/obj.png", obj); cv2.imwrite("qc/hand.png", hand)
vis = im.copy(); vis[obj > 0] = (vis[obj > 0] * 0.5 + np.array([0, 255, 0]) * 0.5).astype(np.uint8)
vis[hand > 0] = (vis[hand > 0] * 0.5 + np.array([255, 0, 0]) * 0.5).astype(np.uint8)
cv2.imwrite("qc/s1_masks.jpg", cv2.resize(vis, (W // 2, H // 2)))
