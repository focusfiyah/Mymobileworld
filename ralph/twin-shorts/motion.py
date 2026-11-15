"""Motion-graphics panels for the split-screen beats (Ralph 2026-11-15: "I want motion graphics when showing the product.
It looks boring"). Each anim draws the 1080x820 top panel at local time t (seconds since the beat started) from the real
kit pages (pages/*.png, rendered from the PDFs): 3D tilts (perspective warp), spring ease, soft shadows, a counter.
Never enlarges a page past its rendered size (pages are 1105 px wide; cards here are 300-560 px)."""
import math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = __file__.rsplit("/", 1)[0]
PW, PH = 1080, 820
BG = (250, 250, 248, 255)
NAVY, YEL = (27, 31, 59, 255), (255, 210, 63, 255)
_cache = {}


def bgpanel():
    """Soft warm-to-cool gradient with a faint glow behind the cards (not a flat fill)."""
    if "bg" not in _cache:
        y, x = np.mgrid[0:PH, 0:PW].astype(np.float32)
        top, bot = np.array([252, 250, 245]), np.array([236, 242, 250])
        g = top + (bot - top) * (y / PH)[..., None]
        r = np.sqrt(((x - 540) / 520) ** 2 + ((y - 430) / 380) ** 2)
        g = g + (np.clip(1 - r, 0, 1) ** 2)[..., None] * np.array([6, 6, 2])
        a = np.dstack([np.clip(g, 0, 255), np.full((PH, PW), 255)]).astype(np.uint8)
        _cache["bg"] = Image.fromarray(a, "RGBA")
    return _cache["bg"].copy()


def page(name, w):
    k = (name, w)
    if k not in _cache:
        p = Image.open(f"{HERE}/pages/{name}.png").convert("RGBA"); h = int(p.height * w / p.width)
        p = p.resize((w, h), Image.LANCZOS)
        m = Image.new("L", p.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), int(w * 0.03), fill=255)
        p.putalpha(m); _cache[k] = p
    return _cache[k]


def ease_out_back(x, s=1.4):
    x = min(max(x, 0), 1); x -= 1; return x * x * ((s + 1) * x + s) + 1


def ease_out(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = min(max(x, 0), 1); return 3 * x * x - 2 * x ** 3


def warp(card, ry=0.0, rz=0.0, scale=1.0):
    """Rotate a card around its vertical axis (ry, degrees, 3D with perspective) and in plane (rz), then scale."""
    w, h = card.size; f = 1400.0
    pts = []
    for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        a = math.radians(ry); X, Z = x * math.cos(a), x * math.sin(a)
        k = f / (f + Z); X, Y = X * k, y * k
        b = math.radians(rz); X, Y = X * math.cos(b) - Y * math.sin(b), X * math.sin(b) + Y * math.cos(b)
        pts.append((X * scale, Y * scale))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    ox, oy = -min(xs) + 4, -min(ys) + 4; ow, oh = int(max(xs) - min(xs)) + 8, int(max(ys) - min(ys)) + 8
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), np.float32([(x + ox, y + oy) for x, y in pts]))
    out = cv2.warpPerspective(np.array(card), M, (ow, oh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return Image.fromarray(out), (ox, oy)


def place(canvas, card, cx, cy, ry=0, rz=0, scale=1.0, alpha=1.0, shadow=True):
    """Draw card centred at (cx, cy) with a soft drop shadow."""
    im, (ox, oy) = warp(card, ry, rz, scale)
    if alpha < 1: a = np.array(im); a[..., 3] = (a[..., 3] * max(alpha, 0)).astype(np.uint8); im = Image.fromarray(a)
    x, y = int(cx - ox), int(cy - oy)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sa = np.array(im)[..., 3]
        sh.putalpha(Image.fromarray((sa * 0.28 * max(alpha, 0)).astype(np.uint8)))
        sh = sh.filter(ImageFilter.GaussianBlur(16)); canvas.alpha_composite(sh, (x + 10, y + 18))
    canvas.alpha_composite(im, (x, y))


def font(sz, f="InstrumentSerif-Regular.ttf"): return ImageFont.truetype(f"{HERE}/fonts/{f}", sz)


def fan_flip(t, dur):
    """52-page guide: three pages spring in and fan out, then the front page flips through the guide like a book."""
    c = bgpanel(); names = ["K-05", "K-08", "K-01"]
    for i, n in enumerate(names):
        k = ease_out_back((t - 0.08 * i) / 0.55); side = (i - 1)
        place(c, page(n, 360), 540 + side * 230 * k, 430 + (1 - k) * 500, ry=side * -18 * k, rz=side * 7 * k, scale=0.85 + 0.15 * k, alpha=min(1, k * 1.5))
    if t > 0.9:   # flip-through on top, 6 pages a second
        seq = ["K-01", "K-02", "K-03", "K-04", "K-05", "K-06", "K-07", "K-08"]; ft = t - 0.9
        i = int(ft * 6) % len(seq); ph = (ft * 6) % 1
        place(c, page(seq[(i + 1) % len(seq)], 400), 540, 430, scale=1.0, shadow=True)
        place(c, page(seq[i], 400), 540, 430, ry=-85 * ease_in_out(ph), scale=1.0, alpha=1 - 0.4 * ph)
    return c


def counter_hooks(t, dur):
    """120 hooks: Hook Library cover swings in from the left, hook table pages slide behind it, a counter ticks to 120."""
    c = bgpanel()
    for i, n in enumerate(["H-04", "H-03"]):
        k = ease_out((t - 0.15 - 0.1 * i) / 0.6)
        place(c, page(n, 330), 700 + 60 * i - (1 - k) * 300, 420 + 20 * i, rz=6 + 4 * i, alpha=k)
    k = ease_out_back(t / 0.6)
    place(c, page("H-01", 380), 360 + (1 - k) * -500, 420, ry=25 * (1 - k) + 8, rz=-4)
    n = int(round(120 * ease_out(min(1, (t - 0.2) / 1.1)))) if t > 0.2 else 0
    d = ImageDraw.Draw(c); f = font(150); s = f"{n}"; w = d.textlength(s, font=f)
    pill = (770 - w / 2 - 30, 560, 770 + w / 2 + 30, 730)
    if t > 0.2: d.rounded_rectangle(pill, 30, fill=NAVY); d.text((770 - w / 2, 560), s, font=f, fill=YEL)
    return c


def voice_wave(t, dur):
    """Voice Kit: cover turns in on its vertical axis, an animated voice waveform grows beside it."""
    c = bgpanel()
    k = ease_out_back(t / 0.7)
    place(c, page("V-01", 380), 360, 420, ry=-70 * (1 - k) - 6, scale=0.9 + 0.1 * k)
    d = ImageDraw.Draw(c); n = 15; x0 = 600; gw = 26
    for i in range(n):
        g = ease_out((t - 0.2 - 0.03 * i) / 0.4)
        a = (0.35 + 0.65 * abs(math.sin(t * 7 + i * 0.7)) * abs(math.sin(i * 1.3 + 0.5))) * g
        h = 30 + 250 * a; x = x0 + i * gw
        d.rounded_rectangle((x, 420 - h / 2, x + 14, 420 + h / 2), 7, fill=(44, 85, 168, 255) if i % 3 else YEL)
    return c


def bundle(t, dur):
    """CTA: the three covers slide together into one bundle, gentle float."""
    c = bgpanel(); fl = 8 * math.sin(t * 2.2)
    for i, (n, dx, rz) in enumerate([("H-01", -240, -9), ("V-01", 240, 9), ("K-01", 0, 0)]):
        k = ease_out_back((t - 0.1 * i) / 0.6)
        place(c, page(n, 340 if n != "K-01" else 380), 540 + dx * k, 430 + fl * (1 if i == 2 else 0.5) + (1 - k) * 600, rz=rz * k, alpha=min(1, k * 1.4))
    return c


ANIMS = {"fan_flip": fan_flip, "counter_hooks": counter_hooks, "voice_wave": voice_wave, "bundle": bundle}


if __name__ == "__main__":   # contact sheet for a look: python motion.py OUT.png
    import sys
    tiles = []
    for name in ANIMS:
        for t in (0.15, 0.5, 1.2, 2.0):
            tiles.append(ANIMS[name](t, 2.5).convert("RGB").resize((270, 205)))
    S = Image.new("RGB", (270 * 4, 205 * len(ANIMS)), "white")
    for i, im in enumerate(tiles): S.paste(im, ((i % 4) * 270, (i // 4) * 205))
    S.save(sys.argv[1]); print("SHEET_OK")
