"""S5 flicker, free (BOOK: flicker added in the edit if the clip won't blink): every other 1/6 s the front lens and its
beam go dark. Mask = bright pixels inside the beam cone (lens at the tip of the cap, cone toward the upper left), feathered.
clips/S5.mp4 -> clips/S5_flicker.mp4"""
import cv2, numpy as np
cap = cv2.VideoCapture("clips/S5.mp4"); fps = cap.get(cv2.CAP_PROP_FPS)
w, h = int(cap.get(3)), int(cap.get(4))
out = cv2.VideoWriter("clips/_S5_flicker.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
cone = np.zeros((h, w), np.uint8)
cv2.fillPoly(cone, [np.array([[0.66 * w, 0.70 * h], [0.50 * w, 0.68 * h], [0.10 * w, 0.30 * h], [0.62 * w, 0.30 * h]], np.int32)], 255)
cone = cv2.GaussianBlur(cone, (0, 0), 25) / 255.0
n = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if (n / fps) % (1 / 3) < 1 / 6:   # off phase
        hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV); v = hsv[..., 2].astype(np.float32); s = hsv[..., 1].astype(np.float32)
        base = cv2.GaussianBlur(v, (0, 0), 60)              # local background level
        glow = np.clip((v - base) / 30.0, 0, 1) * np.clip(1.4 - s / 120.0, 0, 1)   # bright and whitish = beam, not blue sky
        glow = cv2.GaussianBlur(glow, (0, 0), 8) * cone
        f = (f.astype(np.float32) * (1 - 0.6 * glow[..., None])).astype(np.uint8)
    out.write(f); n += 1
out.release()
