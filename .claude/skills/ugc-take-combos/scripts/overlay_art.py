"""Overlay art for take combos, and the still-preview sheet the client approves BEFORE any render.

    python overlay_art.py preview VIDEO SECONDS out.png a.png [b.png ...]   # composite each PNG on one real frame

All art is a full 1080x1920 transparent PNG so it overlays at 0:0. Fonts: Arial stands in for
Google's Roboto and Segoe UI Semibold for TikTok's bubble; in the cloud (no Windows fonts) Liberation
Sans (Arial's metrics) and the bundled Open Sans SemiBold (OFL) take their place.
Designs A-D were the options shown to Ralph on the Fungix job; he chose A.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
HERE = Path(__file__).parent
FONTS = {  # first file that exists wins: Windows (Ralph's PC), then the cloud stand-ins
    "arial.ttf": ["C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
    "arialbd.ttf": ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
    "seguisb.ttf": ["C:/Windows/Fonts/seguisb.ttf", str(HERE / "OpenSans-SemiBold.ttf")],
}
def font(name, size):
    for p in FONTS.get(name, [name]):
        if Path(p).exists(): return ImageFont.truetype(p, size)
    raise FileNotFoundError(f"no font for {name}; install fonts-liberation or set FONTS")
def canvas(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def wrap(d, text, f, maxw):
    rows, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur: rows.append(cur); cur = w
        else: cur = t
    return rows + ([cur] if cur else [])

def text_bubble(lines, y=850):
    """TikTok native text: one white rounded box per line, black semibold text, centred."""
    img = canvas(); d = ImageDraw.Draw(img); f = font("seguisb.ttf", 46)
    for ln in lines:
        l, t, r, b = d.textbbox((0, 0), ln, font=f); bw, bh = r - l + 52, 88; x = (W - bw) // 2
        d.rounded_rectangle((x, y, x + bw, y + bh), 20, fill=(255, 255, 255, 255))
        d.text((W // 2, y + bh // 2), ln, font=f, fill=(0, 0, 0), anchor="mm"); y += bh + 20
    return img

def card_dark(plain, hi, top=760):
    """A (approved on Fungix): a dark search-result screenshot, full-line blue highlight on the claim."""
    img = canvas(); d = ImageDraw.Draw(img); f = font("arial.ttf", 34)
    x0, cw, px, py, lh = 165, 750, 40, 24, 46
    rows = [(r, 0) for r in wrap(d, plain, f, cw - 2 * px)] + [(r, 1) for r in wrap(d, hi, f, cw - 2 * px)]
    d.rounded_rectangle((x0, top, x0 + cw, top + py * 2 + lh * len(rows)), 10, fill=(17, 20, 24, 255))
    y = top + py
    for txt, h in rows:
        if h: d.rectangle((x0 + px - 2, y + 3, x0 + px + d.textlength(txt + " ", font=f), y + lh - 3), fill=(26, 79, 214, 255))
        d.text((x0 + px, y + lh // 2), txt, font=f, fill=(255, 255, 255) if h else (232, 234, 237), anchor="lm"); y += lh
    return img

def card_light(plain, hi, top=760):
    """B: light-mode snippet, white card, soft blue selection."""
    img = canvas(); d = ImageDraw.Draw(img); f = font("arial.ttf", 34)
    x0, cw, px, py, lh = 150, 780, 38, 26, 47
    rows = [(r, 0) for r in wrap(d, plain, f, cw - 2 * px)] + [(r, 1) for r in wrap(d, hi, f, cw - 2 * px)]
    ch = py * 2 + lh * len(rows)
    d.rounded_rectangle((x0 + 5, top + 6, x0 + cw + 5, top + ch + 6), 16, fill=(0, 0, 0, 60))
    d.rounded_rectangle((x0, top, x0 + cw, top + ch), 16, fill=(255, 255, 255, 255)); y = top + py
    for txt, h in rows:
        if h: d.rectangle((x0 + px - 2, y + 4, x0 + px + d.textlength(txt + " ", font=f), y + lh - 4), fill=(197, 220, 250, 255))
        d.text((x0 + px, y + lh // 2), txt, font=f, fill=(32, 33, 36), anchor="lm"); y += lh
    return img

def card_ai_overview(body, key, top=720):
    """C: 'AI Overview' panel; only the KEY phrase is highlighted, mid-line."""
    img = canvas(); d = ImageDraw.Draw(img); f = font("arial.ttf", 33)
    x0, cw, px, py, lh = 150, 780, 36, 24, 45
    rows = wrap(d, body, f, cw - 2 * px)
    d.rounded_rectangle((x0, top, x0 + cw, top + py * 2 + 46 + lh * len(rows)), 18, fill=(255, 255, 255, 250))
    d.ellipse((x0 + px, top + py + 2, x0 + px + 26, top + py + 28), fill=(66, 133, 244))
    d.text((x0 + px + 38, top + py + 15), "AI Overview", font=font("arialbd.ttf", 27), fill=(95, 99, 104), anchor="lm")
    y = top + py + 46
    for txt in rows:
        if key in txt:
            wa, wk = d.textlength(txt.split(key, 1)[0], font=f), d.textlength(key, font=f)
            d.rectangle((x0 + px + wa - 3, y + 4, x0 + px + wa + wk + 3, y + lh - 5), fill=(232, 240, 254, 255))
        d.text((x0 + px, y + lh // 2), txt, font=f, fill=(32, 33, 36), anchor="lm"); y += lh
    return img

def card_phone_search(query, plain, hi, top=640):
    """D: phone screenshot with the search bar and query above the answer."""
    img = canvas(); d = ImageDraw.Draw(img); f = font("arial.ttf", 32)
    x0, cw, px, py, lh, bar = 140, 800, 34, 22, 44, 78
    rows = [(r, 0) for r in wrap(d, plain, f, cw - 2 * px)] + [(r, 1) for r in wrap(d, hi, f, cw - 2 * px)]
    d.rounded_rectangle((x0, top, x0 + cw, top + bar + py * 2 + lh * len(rows)), 16, fill=(255, 255, 255, 255))
    d.rounded_rectangle((x0 + 18, top + 14, x0 + cw - 18, top + bar - 8), 28, fill=(241, 243, 244, 255))
    d.ellipse((x0 + 40, top + 32, x0 + 66, top + 58), outline=(120, 124, 130), width=4)
    d.line((x0 + 63, top + 55, x0 + 76, top + 68), fill=(120, 124, 130), width=4)
    d.text((x0 + 92, top + 45), query, font=font("arial.ttf", 30), fill=(95, 99, 104), anchor="lm")
    y = top + bar + py
    for txt, h in rows:
        if h: d.rectangle((x0 + px - 2, y + 4, x0 + px + d.textlength(txt + " ", font=f), y + lh - 4), fill=(197, 220, 250, 255))
        d.text((x0 + px, y + lh // 2), txt, font=f, fill=(32, 33, 36), anchor="lm"); y += lh
    return img

def photo(path, box):
    """A photo pop-in (e.g. a condition close-up) placed at box=(x, y, w, h)."""
    img = canvas(); p = Image.open(path).convert("RGBA").resize(box[2:], Image.LANCZOS); img.alpha_composite(p, box[:2]); return img

def preview(video, seconds, out, pngs, ffmpeg="ffmpeg", labels=None):
    """Composite each overlay on the SAME real frame and tile them. Show this, get a pick, THEN render."""
    frame = Path(out).with_suffix(".frame.png")
    subprocess.run([ffmpeg, "-v", "error", "-y", "-ss", str(seconds), "-i", str(video), "-frames:v", "1",
                    "-vf", f"scale={W}:{H}:flags=lanczos", str(frame)], check=True)
    base = Image.open(frame).convert("RGBA"); tiles = []
    for i, p in enumerate(pngs):
        shot = Image.alpha_composite(base, Image.open(p).convert("RGBA")).resize((360, 640), Image.LANCZOS).convert("RGB")
        t = Image.new("RGB", (360, 684), (24, 24, 24)); t.paste(shot, (0, 44))
        ImageDraw.Draw(t).text((10, 22), (labels or [Path(x).stem for x in pngs])[i], font=font("seguisb.ttf", 22), fill="white", anchor="lm")
        tiles.append(t)
    cols = min(3, len(tiles)); sheet = Image.new("RGB", (360 * cols, 684 * ((len(tiles) + cols - 1) // cols)), (24, 24, 24))
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * 360, (i // cols) * 684))
    sheet.save(out); frame.unlink(); return out

if __name__ == "__main__" and sys.argv[1:2] == ["preview"]:
    sys.path.insert(0, str(Path(__file__).parent)); from take_combos import FF
    v, s, o, *pngs = sys.argv[2:]; print(preview(v, s, o, pngs, FF))
