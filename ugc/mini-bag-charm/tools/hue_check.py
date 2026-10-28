"""v8 check (Grace 2026-10-28: 'she can tell it was pasted'; Ralph: 'are you going to use the correct burgundy'):
in every pasted shot (clips/S4/S7/S8/S9_track.mp4) the charm's body keeps the listing photo's burgundy hue, and with
--sharp, it is no sharper than the footage around it (a crisp studio photo on soft AI video reads as a sticker).
  python3 tools/hue_check.py [--sharp]   -> HUE_OK / SHARP_OK or the failures"""
import colorsys, json, sys
import cv2, numpy as np
SHOTS, TOL, SHARP_MAX = ["S4", "S7", "S8L", "S9"], 8.0, 1.1


def hue(rgb):
    return colorsys.rgb_to_hsv(*(np.asarray(rgb) / 255))[0] * 360


def burg(a):
    b, g, r = [a[..., i].astype(int) for i in range(3)]
    return (r > 45) & (r < 190) & (g < r * 0.5) & (b > g * 0.9) & (b < r * 0.8)


def crisp(gray, m):
    """Edge steepness on the strongest edges in m: gradient / local contrast (7x7), independent of how bright or dark
    the edge is. A crisp studio cut-out scores higher than soft AI footage."""
    g = np.hypot(*np.gradient(gray)); k = np.ones((7, 7), np.uint8)
    con = cv2.dilate(gray, k) - cv2.erode(gray, k); v = (g / np.maximum(con, 1))[m & (con > 25)]
    gm = g[m & (con > 25)]
    return float(np.median(v[gm >= np.percentile(gm, 80)])) if len(gm) > 20 else np.nan


L = cv2.imread("refs/real/listing_burgundy_10of10.jpg")[650:1050, 300:600]
ref = hue(np.median(L[burg(L)][:, ::-1], 0))
bad = []; sharp = "--sharp" in sys.argv
for sid in SHOTS:
    q = json.load(open(f"qc/track_{sid}.json")); boxes = q.get("charm_box") or []
    cap = cv2.VideoCapture(f"clips/{sid}_track.mp4"); hs, ratios = [], []
    for i, bx in enumerate(boxes):
        ok, f = cap.read()
        if not ok: break
        if bx is None or i % 6: continue
        x0, y0, x1, y1 = bx; c = f[y0:y1 + 1, x0:x1 + 1]; m = burg(c)
        if m.sum() < 80: continue
        hs.append(hue(np.median(c[m][:, ::-1], 0)))
        if sharp:
            w, h = x1 - x0, y1 - y0; X0, Y0 = max(0, x0 - w), max(0, y0 - h // 2)
            big = cv2.cvtColor(f[Y0:y1 + h // 2, X0:x1 + w], cv2.COLOR_BGR2GRAY).astype(np.float32)
            cm = np.zeros(big.shape, np.uint8); cm[y0 - Y0:y1 - Y0 + 1, x0 - X0:x1 - X0 + 1] = burg(c)
            band = (cv2.dilate(cm, np.ones((5, 5), np.uint8)) - cv2.erode(cm, np.ones((5, 5), np.uint8))) > 0
            sur = np.ones(big.shape, bool); sur[max(0, y0 - Y0 - 8):y1 - Y0 + 9, max(0, x0 - X0 - 8):x1 - X0 + 9] = False
            bb, bg_, br = [f[Y0:y1 + h // 2, X0:x1 + w][..., k].astype(int) for k in range(3)]
            leather = (br > 60) & (br > bg_ + 10) & (bg_ > bb) & (br < 230)       # what it hangs on (same focus), not bokeh
            if (sur & leather).sum() > 400: sur &= leather
            r_ = crisp(big, band) / crisp(big, sur)
            if np.isfinite(r_): ratios.append(r_)
    d = [min(abs(x - ref), 360 - abs(x - ref)) for x in hs]
    line = f"{sid}: hue {np.median(hs):.0f} (listing {ref:.0f}), worst off {max(d):.1f} deg" if hs else f"{sid}: no charm found"
    if not hs or max(d) > TOL: bad.append(f"{sid} hue")
    if sharp and ratios:
        line += f"; sharpness charm/around {np.median(ratios):.2f}"
        if np.median(ratios) > SHARP_MAX: bad.append(f"{sid} too sharp")
    print(line)
print(("SHARP_OK" if sharp else "HUE_OK") if not bad else "FAIL: " + ", ".join(bad))
