"""Product reference sheet from the real NOVALL listing photos only, DARK BROWN (Ralph 2026-10-22), free. PLAYBOOK §6."""
from PIL import Image, ImageDraw, ImageFont
L = "research/listing/"
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
S = Image.new("RGB", (1600, 2400), "white"); d = ImageDraw.Draw(S)
def put(f, box, label):
    im = Image.open(L + f).convert("RGB"); x, y, w, h = box
    from PIL import ImageOps
    bb = ImageOps.invert(im).point(lambda v: 255 if v > 18 else 0).getbbox()
    if bb: im = im.crop((max(bb[0]-10,0), max(bb[1]-10,0), min(bb[2]+10,im.width), min(bb[3]+10,im.height)))
    im = im.resize((im.width*3, im.height*3)) if im.height*3 < h else im
    im.thumbnail((w, h - 44)); S.paste(im, (x + (w - im.width) // 2, y + 44)); d.text((x + 10, y + 6), label, fill="black", font=F)
put("28_x_13987564.webp", (0, 0, 1600, 1250), "FRONT (real photo, dark brown): 4 drawstring channels, ruffle hems, sheer under-layer")
put("29_x_4179ce65.webp", (0, 1250, 800, 575), "SIDE: flat fabric ties at the waist, long back")
put("30_x_c5008ece.webp", (800, 1250, 800, 575), "BACK: elastic waist, 4 ruffle tiers")
put("31_x_6602e02b.webp", (0, 1825, 800, 575), "CLOSE-UP: flat fabric tie + ruching")
put("34_x_c0560e04.webp", (800, 1825, 800, 575), "WORN SHAPE ONLY (ours is DARK BROWN)")
S.save("refs/product_sheet.png")
Image.open(L + "31_x_6602e02b.webp").convert("RGB").save("refs/closeup_tie.png")
Image.open(L + "28_x_13987564.webp").convert("RGB").crop((80, 0, 720, 620)).save("refs/closeup_ruching.png")
Image.open(L + "28_x_13987564.webp").convert("RGB").save("refs/front_real.png")
print("SHEET_OK", S.size)
