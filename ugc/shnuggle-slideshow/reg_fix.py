"""Free fix: paint out the AI-added (R) mark next to the logo badge (the real badge has none). python3 reg_fix.py"""
import cv2, numpy as np, shutil
from pathlib import Path
SPOTS = {"S4": [(934, 2302, 11)], "S5": []}
GREY = {"S5": [(1154, 1908, 6), (1151, 1928, 6)]}
for sid in ["S1", "S2", "S3", "S4", "S5", "S6"]:
    src = Path(f"stills_raw/{sid}.png"); dst = Path(f"stills/{sid}.png")
    if not src.exists(): continue
    if sid not in SPOTS: shutil.copy(src, dst); continue
    im = cv2.imread(str(src)); m = np.zeros(im.shape[:2], np.uint8)
    for x, y, r in SPOTS[sid]: cv2.circle(m, (x, y), r, 255, -1)
    out = cv2.inpaint(im, m, 7, cv2.INPAINT_TELEA)
    for x, y, r in GREY.get(sid, []):   # small marks inside the grey badge: flat badge grey sampled just below-left of the mark (plain badge area above-left, measured from the luminance grid)
        g = np.median(im[1895:1903, 1132:1146].reshape(-1, 3), axis=0); cv2.circle(out, (x, y), r, g.tolist(), -1)
        out = np.where(cv2.circle(np.zeros(m.shape, np.uint8), (x, y), r + 2, 255, -1)[..., None] > 0, cv2.GaussianBlur(out, (5, 5), 0), out)
    cv2.imwrite(str(dst), out); print("fixed", sid)
