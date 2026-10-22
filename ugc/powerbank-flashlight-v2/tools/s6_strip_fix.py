"""S6 free fix: the Kie still drew a second lit strip on the flashlight's side face (the real unit has one front panel).
Inpaint that strip with the side-face plastic. stills/S6_raw.png -> stills/S6.png"""
import cv2, numpy as np, shutil
from pathlib import Path
if not Path("stills/S6_raw.png").exists(): shutil.copy("stills/S6.png", "stills/S6_raw.png")
im = cv2.imread("stills/S6_raw.png")
m = np.zeros(im.shape[:2], np.uint8)
ox, oy = 450, 1450  # crop origin used to locate the strip
cv2.line(m, (ox + 86, oy + 160), (ox + 216, oy + 522), 255, 30)
m = cv2.dilate(m, np.ones((5, 5), np.uint8))
out = cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA)
out = cv2.GaussianBlur(out, (0, 0), 0.8) * (m[..., None] / 255.0) + out * (1 - m[..., None] / 255.0)
cv2.imwrite("stills/S6.png", out.astype(np.uint8))
cv2.imwrite("/tmp/claude-0/-home-user-Mymobileworld/53416d4d-556f-51f6-84c6-dd5be98e1d67/scratchpad/s6fix.png", out[oy:oy + 650, ox:ox + 350].astype(np.uint8))
