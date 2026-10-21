"""Product reference sheet (Ralph 2026-10-19 standard), free, from the real listing images only.
Big = cleanest front (listing 3/9). Small = standing 3/4 view and lying lens-end view (1/9), hanging lit view (2/9),
ports end (charging image; its render is darker gunmetal than the others). No text on the sheet itself (models copy text).
python3 refs/make_sheet.py -> refs/product_sheet.png + refs/product_sheet_labeled.jpg (review copy)."""
from PIL import Image, ImageDraw, ImageFont
R = "refs/"
def crop(f, box): return Image.open(R + f).convert("RGB").crop(box)
views = {
    "front": crop("listing_3_carry.jpg", (186, 872, 346, 1460)),
    "standing": crop("listing_1_multifunction.jpg", (640, 690, 840, 1460)),
    "lens": crop("listing_1_multifunction.jpg", (120, 1010, 620, 1230)),
    "hanging_lit": crop("listing_2_camping.jpg", (318, 820, 522, 1162)),
    "ports": crop("listing_charging.jpg", (200, 320, 880, 990)),
}
W, H, BG = 1800, 1400, (232, 232, 232)
sheet = Image.new("RGB", (W, H), BG)
def put(im, x, y, w, h):
    s = min(w / im.width, h / im.height); im2 = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    sheet.paste(im2, (x + (w - im2.width) // 2, y + (h - im2.height) // 2)); return (x, y, w, h)
boxes = {"front": put(views["front"], 30, 30, 520, 1340), "standing": put(views["standing"], 590, 30, 380, 1340),
         "lens": put(views["lens"], 1000, 30, 770, 330), "hanging_lit": put(views["hanging_lit"], 1000, 390, 330, 440),
         "ports": put(views["ports"], 1350, 390, 420, 440)}
sheet.save(R + "product_sheet.png")
lab = sheet.copy(); d = ImageDraw.Draw(lab)
try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception: f = ImageFont.load_default()
names = {"front": "FRONT (main ref)", "standing": "3/4 standing", "lens": "torch head / lens end",
         "hanging_lit": "hung, side light on", "ports": "ports (colour differs)"}
for k, (x, y, w, h) in boxes.items():
    d.rectangle((x, y, x + w, y + h), outline=(255, 120, 0), width=3); d.rectangle((x + 4, y + 4, x + 12 + d.textlength(names[k], font=f), y + 30), fill=(255, 255, 255)); d.text((x + 8, y + 6), names[k], fill=(200, 60, 0), font=f)
d.text((1000, 870), "Real listing pixels only (images 1/9, 2/9, 3/9 + charging).", fill=(40, 40, 40), font=f)
d.text((1000, 910), "Need: a photo of Grace's sample.", fill=(40, 40, 40), font=f)
lab.save(R + "product_sheet_labeled.jpg", quality=90)
print("sheet", sheet.size)
