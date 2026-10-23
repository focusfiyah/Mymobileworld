"""Free fix: inpaint the small stray orange shapes at the left edge of S2 and S5 (2026-10-23 QC). Keeps *_raw.png."""
import cv2, numpy as np, shutil
from pathlib import Path
BOX = {"S2": (0, 900, 70, 1010), "S5": (45, 890, 120, 980)}
for s, (x0, y0, x1, y1) in BOX.items():
    raw = Path(f"stills/{s}_raw.png")
    if not raw.exists(): shutil.copy(f"stills/{s}.png", raw)
    im = cv2.imread(str(raw)); m = np.zeros(im.shape[:2], np.uint8); m[y0:y1, x0:x1] = 255
    cv2.imwrite(f"stills/{s}.png", cv2.inpaint(im, m, 7, cv2.INPAINT_TELEA))
