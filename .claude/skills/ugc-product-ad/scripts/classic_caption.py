"""Ralph's on-screen caption style for Grace's ads (the "Murano earrings" style, Ralph 2026-09-18):
TikTok 'Classic' look: white semibold text, NO background, a soft drop shadow, lowercase, two balanced lines once a
caption is over five words, no "orange cart" text line. Original: Segoe UI Semibold 48px at y=300 on 1080x1920;
here Open Sans SemiBold (OFL, next to this file) because Segoe UI is Windows-only.

  python3 classic_caption.py "don't buy 20 essential oils" out.png [--w 720 --h 1280]

Returns a full-frame transparent PNG to overlay at 0:0 (ffmpeg overlay, enable='between(t,a,b)').
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = Path(__file__).with_name("OpenSans-SemiBold.ttf")


def classic_png(text, w=1080, h=1920, size=48, y=300):
    k = w / 1080                                   # sizes are specified for 1080x1920
    size, y = round(size * k), round(y * k)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = ImageFont.truetype(str(FONT), size)
    words = text.replace("|", " ").split()
    if len(words) <= 5: rows = [" ".join(words)]
    elif "|" in text: rows = [r.strip() for r in text.split("|")]
    else: rows = min(([" ".join(words[:i]), " ".join(words[i:])] for i in range(1, len(words))),
                     key=lambda r: max(d.textlength(x, font=f) for x in r))
    lh = int(size * 1.25)
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for i, r in enumerate(rows):
        sd.text((w // 2 + round(2 * k), y + i * lh + round(3 * k)), r, font=f, fill=(0, 0, 0, 190), anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4 * k)))
    for i, r in enumerate(rows):
        d.text((w // 2, y + i * lh), r, font=f, fill="white", anchor="mm")
    return img


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("text"); a.add_argument("out")
    a.add_argument("--w", type=int, default=1080); a.add_argument("--h", type=int, default=1920)
    o = a.parse_args(); classic_png(o.text, o.w, o.h).save(o.out); print(o.out)
