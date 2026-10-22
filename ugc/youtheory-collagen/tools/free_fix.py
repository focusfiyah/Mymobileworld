"""Free still fixes (OpenCV inpaint), 2026-10-22: S2 paints out a made-up branded tub print in the soft background."""
import sys, cv2, numpy as np
def inpaint(src, out, boxes, r=9):
    im = cv2.imread(src); m = np.zeros(im.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes: m[y0:y1, x0:x1] = 255
    res = cv2.inpaint(im, m, r, cv2.INPAINT_TELEA)
    res = cv2.GaussianBlur(res, (0, 0), 0) if False else res
    cv2.imwrite(out, res)
if __name__ == "__main__":
    if sys.argv[1] == "S2": inpaint("stills/orig/S2.png", "stills/S2.png", [(542, 705, 748, 915)])
