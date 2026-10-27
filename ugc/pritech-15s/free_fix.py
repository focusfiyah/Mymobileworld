"""Free still fixes before any paid redo (Ralph's rule: crop / paint out first). Originals kept in stills/orig_r1/.
  V2S4 crop to head + buttons: drops a false PRITECH print on the handle and the blue band on the wrist
  V2S5 crop the top: her eye is out of frame        V4S4 crop the top: her lips are out of frame
  V3S3 crop the left 20%: the toilet is out of frame V4S3 paint out a false PRITECH print on the handle (cv2 inpaint)"""
import shutil
from pathlib import Path
import cv2, numpy as np
from PIL import Image

O = Path("stills/orig_r1"); O.mkdir(exist_ok=True)
CROP = {"V2S4": (150, 60, 684, 1010), "V2S5": (100, 300, 705, 1376), "V4S4": (60, 230, 705, 1376), "V3S3": (154, 142, 768, 1234)}
for sid, box in CROP.items():
    src = O / f"{sid}.png"
    if not src.exists(): shutil.copy(f"stills/{sid}.png", src)
    Image.open(src).convert("RGB").crop(box).resize((768, 1376), Image.LANCZOS).save(f"stills/{sid}.png")
    print(sid, "crop", box, "scale", round(768 / (box[2] - box[0]), 2))
sid = "V4S3"; src = O / f"{sid}.png"
if not src.exists(): shutil.copy(f"stills/{sid}.png", src)
im = cv2.imread(str(src)); x0, y0, x1, y1 = 196, 870, 262, 908
g = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
m = np.zeros(im.shape[:2], np.uint8); m[y0:y1, x0:x1] = (g > np.percentile(g, 35) + 18).astype(np.uint8) * 255
m = cv2.dilate(m, np.ones((5, 5), np.uint8))
cv2.imwrite(f"stills/{sid}.png", cv2.inpaint(im, m, 6, cv2.INPAINT_TELEA)); print(sid, "inpaint", int(m.sum() / 255), "px")
