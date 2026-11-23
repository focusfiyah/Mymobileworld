"""Free fix: recolour skin in a still toward Grace's measured skin (refs/grace_hand.png mean RGB 129,94,81), only inside
the given boxes and only on skin-hued pixels. python3 tools/skin_still.py SHOT x0,y0,x1,y1 [...]  (reads stills_raw/, writes stills/)"""
import sys, numpy as np
from PIL import Image, ImageFilter
TARGET = np.array([129.0, 94.0, 81.0])
sid, boxes = sys.argv[1], [tuple(int(v) for v in b.split(",")) for b in sys.argv[2:]]
im = Image.open(f"stills_raw/{sid}.png").convert("RGB"); a = np.asarray(im).astype(float)
hsv = np.asarray(im.convert("HSV")).astype(float)
m = ((hsv[..., 0] < 30) & (hsv[..., 1] > 35) & (hsv[..., 1] < 175) & (hsv[..., 2] > 45)).astype(np.uint8) * 255
keep = np.zeros_like(m)
for x0, y0, x1, y1 in boxes: keep[y0:y1, x0:x1] = 255
m = np.minimum(m, keep)
m = np.asarray(Image.fromarray(m).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(3))).astype(float)[..., None] / 255
mean = (a * m).sum((0, 1)) / max(m.sum(), 1)
out = a * (TARGET / mean)                       # per-channel gain keeps shading and texture
res = np.clip(a * (1 - m) + out * m, 0, 255).astype(np.uint8)
Image.fromarray(res).save(f"stills/{sid}.png")
Image.fromarray((m[..., 0] * 255).astype(np.uint8)).save(f"/tmp/claude-0/-home-user/679df154-22a8-5fd5-9314-c41206767bf2/scratchpad/mask_{sid}.png")
print(sid, "skin mean before", mean.round(), "-> target", TARGET)
