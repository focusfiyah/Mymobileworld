"""Free still fixes (Ralph: free fixes first), 2026-10-30.
S4: the orange Citrus Serenity label came back reading 'MAGNESIUM LOTION with'; repaint it to the real cream layout
('MAGNESIUM CREAM' / 'HYDRATING | DEEP RELIEF', as on the brand's trio render), only on the orange label, never over the lavender jar.
S6: crop out a blue smartwatch the model added on Grace's wrist (her hand sheet has a bare wrist)."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONT = sys.argv[1] if len(sys.argv) > 1 else "Oswald.ttf"

def s4():
    im = Image.open("stills/orig/S4.png").convert("RGB"); a = np.asarray(im).astype(int)
    x0, y0, x1, y1 = 470, 795, 652, 876
    mask = np.zeros(a.shape[:2], bool)
    for y in range(y0, y1):
        row = a[y, x0:x1]
        orange = (row[:, 0] > 170) & (row[:, 0] - row[:, 2] > 70)
        idx = np.where(orange)[0]
        if not len(idx): continue
        L, R = x0 + idx.min(), x0 + idx.max()
        purple = np.where((row[:, 2] > row[:, 1] + 25) & (row[:, 2] > 120))[0]
        if len(purple): L = max(L, x0 + purple.max() + 2)
        L = 508   # the lavender jar's right edge is a straight vertical line here; white letter leftovers sit right of it
        mask[y, L:R + 1] = True
    # orange fill per row from the label's own orange pixels in that row (keeps the light falloff)
    out = a.copy()
    for y in range(y0, y1):
        row = a[y]; xs = np.where(mask[y])[0]
        if not len(xs): continue
        px = row[xs]; org = px[(px[:, 0] > 170) & (px[:, 0] - px[:, 2] > 70)]
        if len(org): out[y, xs] = np.median(org, axis=0)
    base = Image.fromarray(out.astype("uint8"))
    # text, centred on the label centre (label runs ~ x 468-650; its left part is hidden behind the lavender jar)
    txt = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    cx = 552   # jar runs x ~456-647 (lid), label centre ~552
    def fit(t, w):
        for sz in range(40, 6, -1):
            f = ImageFont.truetype(FONT, sz)
            if d.textlength(t, font=f) <= w: return f
    f1 = fit("MAGNESIUM CREAM", 156); f2 = fit("HYDRATING  |  DEEP RELIEF", 128)
    d.text((cx, 819), "MAGNESIUM CREAM", font=f1, fill=(250, 246, 240, 255), anchor="mm")
    d.text((cx, 850), "HYDRATING  |  DEEP RELIEF", font=f2, fill=(250, 240, 228, 235), anchor="mm")
    txt = txt.filter(ImageFilter.GaussianBlur(0.5))
    m = Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.8))
    base.paste(txt, (0, 0), Image.fromarray((np.asarray(txt)[:, :, 3] * (np.asarray(m) / 255)).astype("uint8")))
    sm = Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
    Image.composite(base, im, sm).save("stills/S4.png")

def s6():
    im = Image.open("stills/orig/S6.png").convert("RGB")
    c = im.crop((30, 330, 620, 1379)).resize((768, 1365), Image.LANCZOS)
    c.save("stills/S6.png")

s4(); s6(); print("FIXED S4 S6")
