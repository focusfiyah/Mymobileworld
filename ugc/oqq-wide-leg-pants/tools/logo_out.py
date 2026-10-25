"""Free fix: paint a faint brand logo (Apple mark Omni added) off a moving plain phone. Tracks a box around the logo by
template matching frame to frame, masks only low-saturation pixels darker than the phone's own grey (skin and the pants
are left alone) and inpaints them. usage: python3 tools/logo_out.py IN.mp4 OUT.mp4 X Y W H [--until SECONDS]"""
import sys, cv2, numpy as np
src, dst, x, y, w, h = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
until = float(sys.argv[sys.argv.index("--until") + 1]) if "--until" in sys.argv else 1e9
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
pad = 40; tpl = None; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i / fps <= until:
        if tpl is not None:   # follow the patch inside a search window
            sx, sy = max(0, x - pad), max(0, y - pad)
            win = f[sy:min(H, y + h + pad), sx:min(W, x + w + pad)]
            r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, _, _, loc = cv2.minMaxLoc(r)
            x, y = sx + loc[0], sy + loc[1]
        tpl = f[y:y + h, x:x + w].copy()
        box = f[y:y + h, x:x + w]; hsv = cv2.cvtColor(box, cv2.COLOR_BGR2HSV)
        s, v = hsv[..., 1].astype(int), hsv[..., 2].astype(int)
        phone = (s < 40) & (v > 150)
        if phone.sum() > 200:
            med = np.median(v[phone])
            hue = hsv[..., 0].astype(int)
            grey = (s < 12) | ((hue >= 70) & (hue <= 130))      # the phone is a cool grey; nails (pink) and skin stay out
            m = ((s < 45) & (v > 110) & (v < med - 8) & grey).astype("uint8") * 255
            m = cv2.dilate(m, np.ones((3, 3), np.uint8))
            f[y:y + h, x:x + w] = cv2.inpaint(box, m, 5, cv2.INPAINT_TELEA)
    out.write(f); i += 1
out.release(); print("frames", i)
