"""Free still fixes (2026-10-29): crops that cut out lips/eyes, a wrist bracelet or a toilet, back to 768x1376 (9:16).
Originals in stills/orig/. python3 free_fix.py"""
from PIL import Image
CROPS = {  # x, y, width (height = width * 16/9 - ish, kept at the still's exact 768:1376 ratio)
    "V6S2": (0, 60, 640),     # lips, nose and the eye at the right/top edge out
    "V8S3": (256, 300, 512),  # toilet out, towel on the hotel bar stays
    "V8S4": (100, 0, 600),    # blue band on the wrist (bottom right) out
    "V9S5": (0, 0, 600),      # lips at the right edge and the wrist band at the bottom out
    "V5S7": (0, 0, 700),      # r2: her eye at the top right edge out
    "V7S2": (160, 514, 481),  # r2: her eye out (keeps cheek, foundation and fingertips)
}
for sid, (x, y, w) in CROPS.items():
    im = Image.open(f"stills/orig_r2/{sid}.png" if sid in ("V5S7", "V7S2") else f"stills/orig/{sid}.png"); h = round(w * 1376 / 768)
    assert x + w <= im.width and y + h <= im.height, (sid, x, y, w, h)
    im.crop((x, y, x + w, y + h)).resize((768, 1376), Image.LANCZOS).save(f"stills/{sid}.png")
    print(sid, "crop", (x, y, w, h), f"{768 / w:.2f}x")
