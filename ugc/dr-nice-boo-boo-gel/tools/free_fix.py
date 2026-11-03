"""Free still fixes (2026-11-03): paint out the hookah pipes on the wall shelf that came from the real backyard photo
(S1, S2) with wall pixels from just above them; skin pixels (the child's finger) are kept. stills/orig keeps the AI originals."""
import numpy as np
from PIL import Image, ImageFilter
def fix(name, box, src_dy, keep_skin=True):
    im = np.asarray(Image.open(f"stills/orig/{name}.png").convert("RGB")).astype(float)
    x0, y0, x1, y1 = box
    top = im[y0 - 4:y0 - 1, x0:x1].mean(0); bot = im[y1 + 1:y1 + 4, x0:x1].mean(0)
    t = np.linspace(0, 1, y1 - y0)[:, None, None]
    patch = top[None] * (1 - t) + top[None] * t   # plain wall: the row above, all the way down
    patch = patch + np.random.default_rng(1).normal(0, 1.5, patch.shape)   # keep a little grain
    reg = im[y0:y1, x0:x1]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    skin = (r > 120) & (r - b > 35) & (r > g)
    skin[:70] = False
    if not keep_skin: skin[:] = False   # the finger is only in the lower part; the small lamp above is painted out
    m = Image.fromarray(((~skin) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(2))
    m = np.asarray(m).astype(float)[..., None] / 255
    # feather the left edge of the box into the original
    ramp = np.clip(np.arange(x1 - x0) / 12, 0, 1)[None, :, None]
    m = m * ramp
    im[y0:y1, x0:x1] = reg * (1 - m) + patch * m
    Image.fromarray(im.astype(np.uint8)).save(f"stills/{name}.png"); print("fixed", name)
fix("S1", (608, 500, 768, 612), 115)
fix("S2", (608, 500, 768, 612), 115)
fix("S3", (641, 150, 768, 243), 0, keep_skin=False)
