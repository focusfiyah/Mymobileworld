"""Free fix, automatic (2026-10-21): every AI still draws the insole logo as a red box with white letters; the real one is a
white box with red letters. Finds each red insole, the light logo cluster inside it, and swaps the colours inside the box.
  python3 insole_auto.py stills/V3S2.png ...   -> <id>_clean.png (updates it if it exists); prints boxes found"""
import sys, os, cv2, numpy as np
for src in sys.argv[1:]:
    cur = src.replace(".png", "_clean.png"); im = cv2.imread(cur if os.path.exists(cur) else src)
    b, g, r = [im[..., i].astype(int) for i in range(3)]
    red = ((r > 110) & (r > g + 60) & (r > b + 50)).astype(np.uint8)
    red = cv2.morphologyEx(red, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(red)
    light = ((im.min(2) > 150) & (im.max(2).astype(int) - im.min(2) < 60)).astype(np.uint8)
    found = []
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] < 1500: continue
        hull = np.zeros_like(red); cnt, _ = cv2.findContours((lab == k).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.fillPoly(hull, [cv2.convexHull(max(cnt, key=cv2.contourArea))], 1)
        inside = cv2.erode(hull, np.ones((9, 9), np.uint8)) & light
        cl = cv2.morphologyEx(inside, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
        m, l2, s2, _ = cv2.connectedComponentsWithStats(cl)
        if m < 2: continue
        j = 1 + int(np.argmax(s2[1:, cv2.CC_STAT_AREA]))
        if s2[j, cv2.CC_STAT_AREA] < 120: continue
        pts = np.column_stack(np.nonzero((l2 == j) & (inside > 0)))[:, ::-1].astype(np.float32)
        rect = cv2.minAreaRect(pts); box = cv2.boxPoints(rect).astype(np.int32)
        mask = np.zeros_like(red); cv2.fillPoly(mask, [box], 1); inner = cv2.erode(mask, np.ones((5, 5), np.uint8)) > 0
        redc = np.median(im[(lab == k) & ~(mask > 0)], 0); white = np.array([236, 238, 240.])
        t = np.clip((im.mean(2) / 255.0 - 0.25) / 0.45, 0, 1)[..., None]
        sw = white * (1 - t) + redc * t
        im = np.where(inner[..., None], sw, im).astype(np.uint8); found.append([int(v) for v in (*rect[0], *rect[1])])
    cv2.imwrite(cur, im); print(cur, "logo boxes (cx,cy,w,h):", found)
