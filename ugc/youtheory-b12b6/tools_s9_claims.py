"""S9 free fix (Ralph 2026-10-26 'A'): the two claim lines under 'liquid' came out garbled; replace them with the real
lines from the real pouch print (refs/listing_front_clean.png), drawn as ink on S9's own foil so nothing reads as a sticker."""
from PIL import Image, ImageFilter
import numpy as np
S = np.asarray(Image.open('stills/r3/S9_r5_orig.png').convert('RGB')).astype(float)
R = np.asarray(Image.open('refs/listing_front_clean.png').convert('RGB')).astype(float)
X0, X1, Y0, Y1 = 296, 500, 763, 799          # S9: below the divider (760-761), above the clean foil rows 800-803 (bar glow starts ~804)
out = S.copy()
for y in range(Y0, Y1 + 1):                  # erase: blend the clean foil rows above and below, column by column
    k = (y - (Y0 - 1)) / ((Y1 + 1) - (Y0 - 1))
    out[y, X0:X1] = S[Y0 - 1, X0:X1] * (1 - k) + S[Y1 + 1, X0:X1] * k
# real block: 'promotes brain health*' rows, the middle divider, 'helps support energy production*' rows
rows = list(range(652, 672)) + list(range(676, 685)) + list(range(688, 712))
blk = R[rows, 313:579]
lum = blk.mean(2); alpha = np.clip((236 - lum) / (236 - 150), 0, 1)
w = 490 - 301; h = round(len(rows) * w / blk.shape[1])
a = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.35))) / 255.0
ty = Y0
ink = np.array([92, 88, 84.0])
rng = np.random.default_rng(7); out[Y0:Y1 + 1, X0:X1] += rng.normal(0, 1.6, out[Y0:Y1 + 1, X0:X1].shape)
reg = out[ty:ty + h, 301:301 + w]
out[ty:ty + h, 301:301 + w] = reg * (1 - a[..., None]) + ink * a[..., None]
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save('stills/S9.png')
Image.fromarray(out.clip(0, 255).astype(np.uint8)).crop((280, 740, 520, 820)).resize((960, 320)).save('/tmp/claude-0/-home-user/e4f9bc0d-8646-529d-a3d4-0b15a4703cd3/scratchpad/s9c.png')
print('block', w, h, 'at y', ty)
