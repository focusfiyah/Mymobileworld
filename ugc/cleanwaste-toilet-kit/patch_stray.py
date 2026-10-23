"""Free fix: remove the small made-up 'Cleanwaste' kraft box the still model added in V1S3 (garage shelf) by inpainting,
and crop V1S2 below the bathroom shelf that holds another made-up box. Originals kept in stills/v1_round2/."""
import cv2, numpy as np, shutil
from pathlib import Path
Path("stills/v1_round2").mkdir(exist_ok=True)
for s in ("V1S2", "V1S3"): shutil.copy(f"stills/{s}.png", f"stills/v1_round2/{s}.png")
im = cv2.imread("stills/v1_round2/V1S3.png"); m = np.zeros(im.shape[:2], np.uint8)
cv2.rectangle(m, (522, 770), (655, 905), 255, -1)
# per-row fill from the plain shelf right of the box (keeps the shelf's horizontal edges; inpaint smeared them), soft edge
fill = im.copy(); y0, y1, x0, x1 = 766, 910, 518, 660
for y in range(y0, y1): fill[y, x0:x1] = np.median(im[y, 668:760], axis=0)
fill = cv2.GaussianBlur(fill, (0, 0), 0.6); a = np.zeros(im.shape[:2], np.float32); a[y0:y1, x0:x1] = 1
a = cv2.GaussianBlur(a, (0, 0), 3)[..., None]
cv2.imwrite("stills/V1S3_fix.png", (fill * a + im * (1 - a)).astype(np.uint8))
im = cv2.imread("stills/v1_round2/V1S2.png")   # crop 9:16 below the shelf (shelf box ends ~y 310), toilet kept whole
c = im[340:1376, 190:190 + 583]
cv2.imwrite("stills/V1S2_fix.png", cv2.resize(c, (720, 1280), interpolation=cv2.INTER_LANCZOS4))
print(c.shape)
