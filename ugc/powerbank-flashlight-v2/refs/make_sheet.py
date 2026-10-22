"""Flashlight V2 product sheet, real listing pixels only (Ralph 2026-10-22: the listing 3/9 front view with the power-symbol
button 'is not correct, all other looks to be ok'). Views: standing 3/4 (1/9, main), lying lens end lit (1/9), hung with the
side light on (2/9), ports end (charging image; darker render). python3 refs/make_sheet.py -> refs/product_sheet_v2.png"""
from PIL import Image
R = "refs/"
def crop(f, box): return Image.open(R + f).convert("RGB").crop(box)
views = {
    "standing": crop("listing_1_multifunction.jpg", (640, 690, 840, 1460)),
    "lens": crop("listing_1_multifunction.jpg", (120, 1010, 620, 1230)),
    "hanging_lit": crop("listing_2_camping.jpg", (318, 820, 522, 1162)),
    "ports": crop("listing_charging.jpg", (200, 320, 880, 990)),
}
W, H, BG = 1800, 1400, (232, 232, 232)
sheet = Image.new("RGB", (W, H), BG)
def put(im, x, y, w, h):
    s = min(w / im.width, h / im.height); im2 = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    sheet.paste(im2, (x + (w - im2.width) // 2, y + (h - im2.height) // 2))
put(views["standing"], 30, 30, 560, 1340)
put(views["lens"], 640, 30, 1130, 520)
put(views["hanging_lit"], 640, 590, 540, 780)
put(views["ports"], 1210, 590, 560, 780)
sheet.save(R + "product_sheet_v2.png"); print("sheet", sheet.size)
