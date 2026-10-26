"""Product reference sheet from the real listing photo only (real pixels, no AI views). Run: python3 make_sheet.py"""
from PIL import Image
src = Image.open("refs/real/listing_burgundy_10of10.jpg").convert("RGB")
crops = {  # boxes in the 944x2048 phone screenshot
    "front": (150, 520, 860, 1200),
    "lock": (370, 730, 500, 1130),
    "scarf": (460, 640, 840, 1200),
    "handles": (270, 530, 680, 800),
    "base": (220, 1060, 680, 1170),
}
for k, b in crops.items():
    src.crop(b).save(f"refs/real/closeup_{k}.png")
W, H = 2000, 1400
sheet = Image.new("RGB", (W, H), "white")
f = src.crop(crops["front"]); s = 1300 / f.height; f = f.resize((int(f.width * s), 1300), Image.LANCZOS)
sheet.paste(f, (50, 50))
x0 = 100 + f.width; cw = W - x0 - 50
y = 50
for k in ("lock", "scarf", "handles"):
    c = src.crop(crops[k]); h = 410 if k != "handles" else 380
    s = min(cw / c.width, h / c.height, 2.0); c = c.resize((int(c.width * s), int(c.height * s)), Image.LANCZOS)
    sheet.paste(c, (x0 + (cw - c.width) // 2, y)); y += c.height + 30
sheet.save("refs/product_sheet.png"); print(sheet.size, f.size)
