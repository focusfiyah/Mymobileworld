"""Carousel slides (Ralph 2026-11-15), 1080x1350 PNG, same cinematic look as the videos: electric-blue or black
gradient, Anton headline, Instrument Serif subline, real kit pages or Fluent 3D icons (never enlarged past ~1.2x),
slide counter and a swipe hint. Usage: python carousel.py WEEK   (MuseTalk venv: PIL + numpy + cv2)"""
import sys, json, pathlib
sys.path.insert(0, "/home/user/Mymobileworld/ralph/twin-shorts")
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import motion2 as M

HERE = pathlib.Path(__file__).parent; TS = "/home/user/Mymobileworld/ralph/twin-shorts"
W, H = 1080, 1350; YEL = (255, 210, 63)
ICONS = {"C1": ["movie_camera", "eyes", "handshake", "star-struck", None, "package"],
         "C2": [None, "camera_with_flash", "movie_camera", "couch_and_lamp", "clapper_board", "studio_microphone", None]}
FRAMES = {("C2", 0): "twin_a.png", ("C2", 6): "twin_b.png"}   # real frames from Ralph's approved twin videos


def bg(dark):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((x - W / 2) / W) ** 2 + ((y - H * .42) / H) ** 2)
    a, b = (np.array([30, 30, 36]), np.array([6, 6, 10])) if dark else (np.array([46, 58, 240]), np.array([16, 20, 130]))
    g = a + (b - a) * np.clip(r * 1.5, 0, 1)[..., None]
    return Image.fromarray(np.dstack([g, np.full((H, W), 255)]).astype(np.uint8), "RGBA")


def wrap(d, text, f, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: out.append(cur); cur = w
    return out + [cur]


def text_block(im, lines, f, y, fill, shadow=True):
    d = ImageDraw.Draw(im)
    for ln in lines:
        w = d.textlength(ln, font=f)
        if shadow:
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text(((W - w) / 2, y + 5), ln, font=f, fill=(0, 0, 0, 170))
            im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        d.text(((W - w) / 2, y), ln, font=f, fill=fill); y += int(f.size * 1.12)
    return y


def slide(cid, i, n, s, dark):
    im = bg(dark); d = ImageDraw.Draw(im); cover = i == 0
    hf = M.font(118 if cover else 96); sf = ImageFont.truetype(f"{TS}/fonts/InstrumentSerif-Regular.ttf", 62 if cover else 56)
    icon = ICONS.get(cid, [])[i] if i < len(ICONS.get(cid, [])) else None
    frame = FRAMES.get((cid, i))
    hl = wrap(d, s["head"].upper(), hf, 940); sl = wrap(d, s["sub"], sf, 900)
    th = len(hl) * int(hf.size * 1.12) + 24 + len(sl) * int(sf.size * 1.12)
    vis = 380 if icon else (520 if (s.get("page") or s.get("bundle") or frame) else 0)
    top = max(90, (H - 120 - th - (40 + vis if vis else 0)) // 2)
    y = text_block(im, wrap(d, s["head"].upper() if not cover else s["head"].upper(), hf, 940), hf, top, (255, 255, 255, 255))
    y = text_block(im, wrap(d, s["sub"], sf, 900), sf, y + 24, YEL + (255,))
    zone_top = y + 40
    if icon:
        ic = Image.open(f"{HERE}/assets/fluent/{icon}.png").convert("RGBA"); ic = ic.resize((300, 300), Image.LANCZOS)   # 256 -> 300 = 1.17x
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((W / 2 - 230, zone_top - 30, W / 2 + 230, zone_top + 360), fill=(120, 140, 255, 90))
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(60))); im.alpha_composite(ic, ((W - 300) // 2, zone_top + 20))
    if frame:
        fr = Image.open(f"{HERE}/assets/frames/{frame}").convert("RGBA"); fw = 300; fr = fr.resize((fw, int(fr.height * fw / fr.width)), Image.LANCZOS)
        fr = fr.crop((0, 20, fw, min(fr.height, 20 + 500))); mk = Image.new("L", fr.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, fr.width - 1, fr.height - 1), 28, fill=255); fr.putalpha(mk)
        M.put(im, fr, W // 2, zone_top + 270, rz=-3, glow=(140, 160, 255))
    if s.get("page"):
        card = M.page(s["page"], 460); M.put(im, card, W // 2, zone_top + card.height // 2 + 20, ry=-12, glow=(140, 160, 255))
    if s.get("bundle"):
        for nm, dx, rz in [("H-01", -260, -10), ("V-01", 260, 10), ("K-01", 0, 0)]:
            c = M.page(nm, 300 if nm != "K-01" else 340); M.put(im, c, W // 2 + dx, zone_top + 250, rz=rz, glow=(140, 160, 255) if nm == "K-01" else None)
    small = ImageFont.truetype(f"{TS}/fonts/Figtree-800.ttf", 30)
    d.text((60, H - 80), f"{i + 1}/{n}", font=small, fill=(255, 255, 255, 170))
    if i < n - 1: d.text((W - 230, H - 80), "swipe  >", font=small, fill=(255, 255, 255, 200))
    return im.convert("RGB")


if __name__ == "__main__":
    week = sys.argv[1]; D = HERE / week
    for c in json.load(open(D / "scripts.json"))["carousel"]:
        o = D / "carousel" / c["id"]; o.mkdir(parents=True, exist_ok=True); n = len(c["slides"])
        for i, s in enumerate(c["slides"]):
            slide(c["id"], i, n, s, dark=(i % 2 == 1)).save(o / f"{c['id']}_{i + 1:02d}.png")
        print("CAROUSEL_OK", c["id"], n)
