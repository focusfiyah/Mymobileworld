"""S7 free fix (Ralph 2026-10-26 "Yes go ahead on draw"): at its small size the pouch's claim lines, flavor bar and size
line came out garbled. Replace that band with the real print (refs/listing_front_clean.png), multiplied onto S7's own foil
so its light and colour stay the still's."""
from PIL import Image, ImageFilter
import numpy as np
S = np.asarray(Image.open('stills/r3/S7_r8_orig.png').convert('RGB')).astype(float)
R = np.asarray(Image.open('refs/listing_front_clean.png').convert('RGB')).astype(float)
X0, X1, Y0, Y1 = 126, 240, 893, 938          # S7 band: divider under "liquid" to just below the old size line (rows 939+ are clean foil, then the seam)
out = S.copy()
for y in range(Y0, Y1 + 1):                  # erase with the clean foil rows above and below, column by column
    k = (y - (Y0 - 1)) / ((Y1 + 1) - (Y0 - 1))
    out[y, X0:X1] = S[Y0 - 1, X0:X1] * (1 - k) + S[Y1 + 1, X0:X1] * k
blk = R[643:786, 313:579] / 238.0             # real print as a multiplier (foil = 1.0)
w = 231 - 137; h = round(blk.shape[0] * w / blk.shape[1])
m = np.asarray(Image.fromarray((blk.clip(0, 1) * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.3))) / 255.0
ty = Y0 + 2
out[ty:ty + h, 137:137 + w] *= m ** 1.5                # a touch darker, to sit with "liquid"
rng = np.random.default_rng(3); out[Y0:Y1 + 1, X0:X1] += rng.normal(0, 1.4, out[Y0:Y1 + 1, X0:X1].shape)
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save('stills/S7.png')
Image.fromarray(out.clip(0, 255).astype(np.uint8)).crop((105, 820, 260, 960)).resize((620, 560), Image.LANCZOS).save('/tmp/claude-0/-home-user/e4f9bc0d-8646-529d-a3d4-0b15a4703cd3/scratchpad/s7c.png')
print('block', w, h, 'rows', ty, ty + h)
