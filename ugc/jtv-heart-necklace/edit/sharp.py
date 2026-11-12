"""python3 sharp.py SRC OUT.json -> every 0.2 s: (t, sharpness = Laplacian variance of the centre 60%, motion = mean abs diff vs previous sample, luma)."""
import cv2, sys, json, numpy as np
c = cv2.VideoCapture(sys.argv[1]); fps = c.get(5); rows = []; prev = None; i = 0
while True:
    ok, f = c.read()
    if not ok: break
    if i % 6 == 0:
        g = cv2.cvtColor(cv2.resize(f, (540, 960)), cv2.COLOR_BGR2GRAY); h, w = g.shape
        cg = g[int(h*.2):int(h*.8), int(w*.2):int(w*.8)]
        m = float(np.mean(cv2.absdiff(g, prev))) if prev is not None else 0
        rows.append((round(i/fps, 2), round(cv2.Laplacian(cg, cv2.CV_64F).var(), 1), round(m, 1), round(float(g.mean()), 1))); prev = g
    i += 1
json.dump(rows, open(sys.argv[2], "w"))
