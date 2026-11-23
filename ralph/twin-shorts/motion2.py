"""Cinematic motion-graphics cards (round 2, Ralph 2026-11-15, style ref: an Instagram reel he sent; style only).
A 900x540 card floats over a blurred copy of the room with the presenter below it. Each card is drawn per frame from
the real kit pages (pages/*.png): light-speed burst, glossy 3D reveal on black, infinite zoom through the pages,
kinetic type with motion blur and camera shake on electric blue, particles assembling into the Voice Kit cover, and a
bundle slam for the CTA. Pages are never enlarged past their rendered size (1105 px wide)."""
import math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = __file__.rsplit("/", 1)[0]
CW, CH = 900, 540
BLUE_A, BLUE_B = np.array([46, 58, 240]), np.array([18, 24, 150])
YEL = (255, 210, 63)
_c = {}


def font(sz, f="Anton-400.ttf"): return ImageFont.truetype(f"{HERE}/fonts/{f}", sz)


def cl(x): return min(max(x, 0.0), 1.0)
def eo(x): x = cl(x); return 1 - (1 - x) ** 3
def eob(x, s=1.5): x = cl(x) - 1; return x * x * ((s + 1) * x + s) + 1
def eio(x): x = cl(x); return 3 * x * x - 2 * x ** 3


def page(name, w):
    k = (name, w)
    if k not in _c:
        p = Image.open(f"{HERE}/pages/{name}.png").convert("RGBA"); p = p.resize((w, int(p.height * w / p.width)), Image.LANCZOS)
        m = Image.new("L", p.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, p.width - 1, p.height - 1), int(w * .03), fill=255)
        p.putalpha(m); _c[k] = p
    return _c[k]


def blue_bg():
    if "blue" not in _c:
        y, x = np.mgrid[0:CH, 0:CW].astype(np.float32); r = np.sqrt(((x - CW / 2) / CW) ** 2 + ((y - CH / 2) / CH) ** 2)
        g = BLUE_A + (BLUE_B - BLUE_A) * np.clip(r * 1.6, 0, 1)[..., None]
        _c["blue"] = Image.fromarray(np.dstack([g, np.full((CH, CW), 255)]).astype(np.uint8), "RGBA")
    return _c["blue"].copy()


def black_bg(spot=(450, 220)):
    k = ("black", spot)
    if k not in _c:
        y, x = np.mgrid[0:CH, 0:CW].astype(np.float32); r = np.sqrt(((x - spot[0]) / 520) ** 2 + ((y - spot[1]) / 360) ** 2)
        v = 8 + 34 * np.clip(1 - r, 0, 1) ** 2
        _c[k] = Image.fromarray(np.dstack([v, v, v * 1.08, np.full((CH, CW), 255)]).clip(0, 255).astype(np.uint8), "RGBA")
    return _c[k].copy()


def warp(card, ry=0.0, rz=0.0, scale=1.0):
    w, h = card.size; f = 1300.0; pts = []
    for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        a = math.radians(ry); X, Z = x * math.cos(a), x * math.sin(a); k = f / (f + Z); X, Y = X * k, y * k
        b = math.radians(rz); X, Y = X * math.cos(b) - Y * math.sin(b), X * math.sin(b) + Y * math.cos(b)
        pts.append((X * scale, Y * scale))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]; ox, oy = -min(xs) + 2, -min(ys) + 2
    ow, oh = int(max(xs) - min(xs)) + 4, int(max(ys) - min(ys)) + 4
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), np.float32([(x + ox, y + oy) for x, y in pts]))
    return Image.fromarray(cv2.warpPerspective(np.array(card), M, (ow, oh), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))), (ox, oy)


def put(c, card, cx, cy, ry=0, rz=0, scale=1.0, alpha=1.0, glow=None, reflect=False):
    im, (ox, oy) = warp(card, ry, rz, scale)
    if alpha < 1: a = np.array(im); a[..., 3] = (a[..., 3] * cl(alpha)).astype(np.uint8); im = Image.fromarray(a)
    x, y = int(cx - ox), int(cy - oy)
    if glow:
        g = Image.new("RGBA", im.size, glow + (0,)); g.putalpha(Image.fromarray((np.array(im)[..., 3] * .55).astype(np.uint8)))
        g = g.filter(ImageFilter.GaussianBlur(28)); c.alpha_composite(g, (x, y))
    if reflect:   # glossy floor reflection under the card
        rf = im.transpose(Image.FLIP_TOP_BOTTOM); a = np.array(rf).astype(np.float32)
        a[..., 3] *= np.linspace(.35, 0, rf.height)[:, None] * cl(alpha); rf = Image.fromarray(a.astype(np.uint8))
        c.alpha_composite(rf, (x, y + im.height + 6))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(Image.fromarray((np.array(im)[..., 3] * .4).astype(np.uint8)))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (x + 8, y + 14)); c.alpha_composite(im, (x, y))


def blur_text(c, txt, cx, cy, sz, t_in, t, col=(255, 255, 255), shake=0.0):
    """Kinetic type: slams in from scale 1.6 with a motion-blur trail, then holds with a decaying camera shake."""
    k = eo((t - t_in) / 0.28)
    if t < t_in: return
    f = font(sz); d = ImageDraw.Draw(Image.new("RGBA", (1, 1))); w = d.textlength(txt, font=f)
    sx = sy = 0
    if shake: amp = shake * math.exp(-(t - t_in) * 3.5); sx, sy = amp * math.sin(t * 61), amp * math.cos(t * 47)
    layer = Image.new("RGBA", (CW, CH), col + (0,)); dl = ImageDraw.Draw(layer)
    sc = 1.6 - 0.6 * k
    for j in range(5 if k < 1 else 1):   # trail copies while moving
        s2 = sc + j * 0.06 * (1 - k); al = int(255 * (1 if j == 0 else 0.25 / j) * min(1, k * 2))
        ft = font(max(8, int(sz * s2))); w2 = dl.textlength(txt, font=ft)
        dl.text((cx - w2 / 2 + sx, cy - sz * s2 * 0.62 + sy), txt, font=ft, fill=col + (al,))
    if k < 1: layer = layer.filter(ImageFilter.GaussianBlur(3 * (1 - k)))
    c.alpha_composite(layer)


def burst(t, dur):
    """Light-speed burst on electric blue that resolves into the kit cover."""
    c = blue_bg(); a = np.array(c).astype(np.float32); rng = np.random.default_rng(7)
    ang = rng.uniform(0, 2 * np.pi, 160); spd = rng.uniform(.6, 1.6, 160); off = rng.uniform(0, 1, 160)
    d = ImageDraw.Draw(c)
    for th, s, o in zip(ang, spd, off):
        r0 = ((t * s * 1.4 + o) % 1.0) * 700; r1 = r0 + 40 + 160 * s * cl(1 - t / 2.2)
        x0, y0 = 450 + r0 * math.cos(th), 270 + r0 * math.sin(th) * .6; x1, y1 = 450 + r1 * math.cos(th), 270 + r1 * math.sin(th) * .6
        d.line((x0, y0, x1, y1), fill=(255, 255, 255, int(200 * cl(1.6 - t))), width=2)
    fl = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); ImageDraw.Draw(fl).ellipse((390, 210, 510, 330), fill=(255, 255, 255, int(255 * cl(1.4 - t))))
    c.alpha_composite(fl.filter(ImageFilter.GaussianBlur(26)))
    if t > .5: put(c, page("K-01", 300), 450, 270, ry=-20 * (1 - eob((t - .5) / .7)), scale=.3 + .7 * eob((t - .5) / .7), glow=(150, 170, 255))
    return c


def reveal(t, dur):
    """Glossy 3D reveal of the guide on black with a floor reflection and a dolly, then an infinite zoom through pages."""
    c = black_bg(); z0 = 1.5
    if t < z0:
        k = eio(t / z0); put(c, page("K-01", 250), 450, 225, ry=-38 + 46 * k, scale=.92 + .12 * k, reflect=True)
        d = ImageDraw.Draw(c); f = ImageFont.truetype(f"{HERE}/fonts/Figtree-800.ttf", 30)
        a = int(255 * eo((t - .3) / .4)); d.text((60, 210), "52 pages.", font=f, fill=(255, 255, 255, a))
        d.text((60, 250), "Photo to finished video.", font=ImageFont.truetype(f"{HERE}/fonts/Figtree-800.ttf", 20), fill=(170, 170, 180, a))
    else:   # infinite zoom: each page flies from small to past the camera
        seq = ["K-02", "K-03", "K-04", "K-05", "K-06", "K-07", "K-08"]; u = (t - z0) * 2.2
        for j in range(3, -1, -1):
            ph = u - math.floor(u) + j; i = (int(math.floor(u)) - j) % len(seq)
            s = .12 * (2.6 ** ph)
            if s > 3.2: continue
            put(c, page(seq[i], 280), 450, 270, scale=s, alpha=cl(1.8 - s * .55) * cl(s * 3))
    return c


def kinetic120(t, dur):
    """'120 HOOKS' slams in with motion blur and camera shake; hook pages drift behind on electric blue."""
    c = blue_bg()
    for i, n in enumerate(["H-03", "H-04", "H-02"]):
        put(c, page(n, 230), 160 + i * 290, 300 + 40 * math.sin(t * 1.5 + i), rz=-8 + 8 * i, alpha=.28)
    n = int(round(120 * eo((t - .1) / .5)))
    blur_text(c, f"{n}", 450, 230, 210, .1, t, shake=10)
    blur_text(c, "HOOKS", 450, 390, 96, .55, t, col=YEL, shake=6)
    return c


def particles(t, dur):
    """Orange particles swirl in and assemble into the Voice Kit cover, which then lights up; a glow waveform below."""
    c = black_bg((450, 250)); cov = page("V-01", 230); cx, cy = 450, 240
    if "pts" not in _c:
        a = np.array(cov)[..., 3]; ys, xs = np.nonzero(a[::6, ::6]); rng = np.random.default_rng(3)
        idx = rng.choice(len(xs), min(900, len(xs)), replace=False)
        tgt = np.stack([xs[idx] * 6 - cov.width / 2 + cx, ys[idx] * 6 - cov.height / 2 + cy], 1)
        st = np.stack([rng.uniform(-200, 1100, len(idx)), rng.uniform(-300, 840, len(idx))], 1); _c["pts"] = (st, tgt, rng.uniform(0, 6.28, len(idx)))
    st, tgt, ph = _c["pts"]; k = eio(cl((t - .05) / 1.0))
    sw = (1 - k) * 90; pos = st + (tgt - st) * k + np.stack([np.cos(ph + t * 4), np.sin(ph + t * 4)], 1) * sw
    lay = np.zeros((CH, CW, 4), np.uint8)
    for x, y in pos.astype(int):
        if 0 <= x < CW and 0 <= y < CH: cv2.circle(lay, (x, y), 2, (255, 140, 40, 255), -1)
    L = Image.fromarray(lay); c.alpha_composite(L.filter(ImageFilter.GaussianBlur(4))); c.alpha_composite(L)
    if t > 1.0: put(c, cov, cx, cy, alpha=eo((t - 1.0) / .45), glow=(255, 140, 40))
    d = ImageDraw.Draw(c)
    for i in range(26):
        h = (8 + 36 * abs(math.sin(t * 6 + i * .55)) * abs(math.sin(i * .9 + 1))) * eo((t - .9) / .5)
        x = 450 - 26 * 9 + i * 18; d.rounded_rectangle((x, 470 - h, x + 9, 470 + h), 4, fill=(255, 150, 60, 230))
    return c


def bundle(t, dur):
    """CTA: the three covers slam together on electric blue, 'DM me KIT' kinetic type."""
    c = blue_bg()
    for i, (n, dx, rz) in enumerate([("H-01", -230, -10), ("V-01", 230, 10), ("K-01", 0, 0)]):
        k = eob((t - .08 * i) / .45)
        put(c, page(n, 200 if n != "K-01" else 230), 450 + dx * k, 200 + (1 - k) * 500, rz=rz * k, alpha=cl(k * 1.4), glow=(140, 160, 255) if n == "K-01" else None)
    blur_text(c, "DM me KIT", 450, 470, 84, .45, t, col=YEL, shake=7)
    return c


def text_card(t, dur, a, b="", dark=False):
    """Kinetic type card for any line: big white words slam in with blur + shake, yellow second line follows."""
    c = black_bg() if dark else blue_bg()
    blur_text(c, a, 450, 230 if b else 270, 150 if len(a) <= 9 else (118 if len(a) <= 13 else 92), .05, t, shake=9)
    if b: blur_text(c, b, 450, 390, 84 if len(b) <= 14 else 64, .4, t, col=YEL, shake=6)
    return c


ANIMS = {"burst": burst, "reveal": reveal, "kinetic120": kinetic120, "particles": particles, "bundle": bundle}

if __name__ == "__main__":
    import sys
    tiles = [ANIMS[n](t, 2.5).convert("RGB").resize((300, 180)) for n in ANIMS for t in (.2, .7, 1.3, 2.2)]
    S = Image.new("RGB", (1200, 180 * len(ANIMS)))
    for i, im in enumerate(tiles): S.paste(im, ((i % 4) * 300, (i // 4) * 180))
    S.save(sys.argv[1]); print("SHEET_OK")
