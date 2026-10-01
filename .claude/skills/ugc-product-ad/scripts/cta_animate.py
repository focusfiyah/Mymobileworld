"""Render an animated CTA as a transparent PNG sequence, then overlay it with ffmpeg.

Why a sequence: ffmpeg's `drawtext` cannot scale over time, so a static text layer with a fade reads
as "not animated" and Ralph will say so. This gives a real pop-in overshoot, a steady pulse and a
bouncing arrow.

    python cta_animate.py "LINK IN BIO" out_dir [seconds]

Then composite it (start time in the setpts expression, NOT only in enable=):

    ffmpeg -i cut.mp4 -framerate 30 -i out_dir/cta_%04d.png -filter_complex \
      "[1:v]setpts=PTS-STARTPTS+26.0/TB[cta];[0:v][cta]overlay=x=0:y=790:eof_action=pass:\
       enable='between(t,26.0,30.0)'[v]" -map "[v]" -map 0:a -c:a copy out.mp4

Canvas is 720 wide to match a 9:16 720x1280 film; `y` places the whole canvas, so the pill lands at
y + 250 and the arrow floats above it.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/segoeuib.ttf"
FPS = 30
W, H = 720, 420
BASE_SIZE = 66


def render(text: str, out_dir: Path, duration: float = 4.0) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("cta_*.png"):
        old.unlink()
    frames = int(FPS * duration)
    for i in range(frames):
        t = i / FPS
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # pop-in with overshoot over the first 0.45s, then a steady breathing pulse
        if t < 0.45:
            p = t / 0.45
            scale = 0.4 + 0.75 * p + 0.18 * math.sin(p * math.pi)
            alpha = min(1.0, p * 2)
        else:
            scale = 1.0 + 0.035 * math.sin(2 * math.pi * (t - 0.45) * 1.9)
            alpha = 1.0
        bounce = -26 * abs(math.sin(2 * math.pi * t)) if t > 0.3 else 0

        font = ImageFont.truetype(FONT, max(10, int(BASE_SIZE * scale)))
        box = d.textbbox((0, 0), text, font=font)
        tw, th = box[2] - box[0], box[3] - box[1]
        padx, pady = int(34 * scale), int(20 * scale)
        pill_w, pill_h = tw + padx * 2, th + pady * 2
        px, py = (W - pill_w) // 2, 250
        d.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=pill_h // 2,
                            fill=(0, 0, 0, int(190 * alpha)))
        d.text((px + padx - box[0], py + pady - box[1]), text, font=font,
               fill=(255, 255, 255, int(255 * alpha)))

        aw, ah = int(74 * scale), int(62 * scale)
        ax, ay = (W - aw) // 2, int(150 + bounce)
        d.polygon([(ax + aw // 2, ay), (ax, ay + ah), (ax + aw, ay + ah)],
                  fill=(255, 255, 255, int(255 * alpha)))
        img.save(out_dir / f"cta_{i:04d}.png")
    return frames


if __name__ == "__main__":
    label = sys.argv[1] if len(sys.argv) > 1 else "LINK IN BIO"
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("cta")
    secs = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
    print("frames:", render(label, target, secs), "->", target)
