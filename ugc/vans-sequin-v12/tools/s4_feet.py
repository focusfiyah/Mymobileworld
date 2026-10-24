"""S4 free fix (2026-10-24): keep round-1 S4 (right shoe, laces, logos) and take only the bare feet from the r2 edit
(same framing); the r2 shoe lost its laces. Feathered mask over the feet area. -> stills/S4_r3.png"""
import cv2, numpy as np
a = cv2.imread("stills/S4.png").astype(np.float32); b = cv2.imread("stills/S4_r2.png").astype(np.float32)
H, W = a.shape[:2]
m = np.zeros((H, W), np.float32)
cv2.rectangle(m, (int(__import__("sys").argv[1]), int(__import__("sys").argv[2])), (W, H), 1, -1)
m = cv2.GaussianBlur(m, (61, 61), 0)[..., None]
cv2.imwrite("stills/S4_r3.png", (b * m + a * (1 - m)).astype(np.uint8))
