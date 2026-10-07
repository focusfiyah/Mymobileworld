"""Photo -> sticker PNG for the hook overlays (Ralph 2026-10-06: real photos instead of emoji).
Free, local. Needs: pip install rembg onnxruntime; model u2netp.onnx in ~/.u2net/
(curl -L -o ~/.u2net/u2netp.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2netp.onnx).
Usage: python3 make_sticker.py full/battery.jpg cut/battery.png      (512px canvas, 9px black outline, soft shadow)"""
import sys
from PIL import Image, ImageFilter
from rembg import remove, new_session

def sticker(src, dst, pad=14, px=512):
    cut = remove(Image.open(src).convert("RGB"), session=new_session("u2netp"))
    cut = cut.crop(cut.getbbox())
    sc = (px - 2 * pad) / max(cut.size)
    cut = cut.resize((max(1, round(cut.width * sc)), max(1, round(cut.height * sc))), Image.LANCZOS)
    canvas = Image.new("RGBA", (px, px), (0, 0, 0, 0)); canvas.alpha_composite(cut, ((px - cut.width) // 2, (px - cut.height) // 2))
    ring = canvas.split()[3].filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1))
    white = Image.new("RGBA", canvas.size, (0, 0, 0, 255)); white.putalpha(ring)   # black outline (Ralph 2026-10-06, was white)
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 110)); shadow.putalpha(ring.point(lambda v: v * 110 // 255).filter(ImageFilter.GaussianBlur(6)))
    out = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); out.alpha_composite(shadow, (0, 5)); out.alpha_composite(white); out.alpha_composite(canvas)
    out.save(dst)

if __name__ == "__main__":
    sticker(sys.argv[1], sys.argv[2])
