"""Free still fixes (2026-10-24): paint out a blue wrist band (S8) and eyelash tips at the profile edge (S6_r2, S9_r2).
usage: python3 tools/paintout.py  -> stills/S8_fix.png, stills/S6_r2_fix.png, stills/S9_r2_fix.png"""
import cv2, numpy as np

def band(src, dst, box):
    im = cv2.imread(src); x0, y0, x1, y1 = box
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (95, 90, 40), (130, 255, 255)); reg = np.zeros_like(m); reg[y0:y1, x0:x1] = 255
    m = cv2.dilate(cv2.bitwise_and(m, reg), np.ones((7, 7), np.uint8))
    cv2.imwrite(dst, cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA)); return int(m.sum() / 255)

def lashes(src, dst, box, thresh=105):
    """dark thin strokes inside box = lashes; replace with the background just outside the profile"""
    im = cv2.imread(src); x0, y0, x1, y1 = box
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); m = np.zeros_like(g)
    sub = g[y0:y1, x0:x1]; m[y0:y1, x0:x1] = (sub < thresh).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    cv2.imwrite(dst, cv2.inpaint(im, m, 7, cv2.INPAINT_TELEA)); return int(m.sum() / 255)

if __name__ == "__main__":
    import sys
    print("S6", lashes("stills/S6_r2.png", "stills/S6_r2_fix.png", (498, 518, 545, 556), thresh=80))
    print("S9", lashes("stills/S9_r2.png", "stills/S9_r2_fix.png", (525, 465, 587, 509)))
    # S8 band: tried 2026-10-24, inpaint smears the wrist; needs a paid one-item edit
