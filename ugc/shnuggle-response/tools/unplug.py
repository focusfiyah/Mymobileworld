"""Free fix: remove an AI plug drawn on top of the seat bump (real plug sits in the dotted floor). python3 tools/unplug.py ID cx cy rx ry"""
import sys, cv2, numpy as np
sid, cx, cy, rx, ry = sys.argv[1], *map(int, sys.argv[2:6])
im = cv2.imread(f"stills_raw/{sid}.png"); m = np.zeros(im.shape[:2], np.uint8)
cv2.ellipse(m, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
cv2.imwrite(f"stills/{sid}.png", cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA)); print("unplugged", sid)
