"""Product reference sheet from the real NOVALL listing photos only (black), free. PLAYBOOK §6."""
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
put("08_x_b9a1ca23.webp", (0, 0, 1600, 1250), "FRONT (real photo, black): 4 drawstring ruched channels, ruffle hems, high-low")
put("27_x_c2006017.webp", (0, 1250, 800, 575), "SIDE: cord tie at the waist, long back")
put("25_x_e6301527.webp", (800, 1250, 800, 575), "BACK: elastic waist, 4 ruffle tiers")
put("26_x_4fe3e4b5.webp", (0, 1825, 800, 575), "CLOSE-UP: drawstring channel, ruching")
put("34_x_c0560e04.webp", (800, 1825, 800, 575), "WORN SHAPE ONLY (ours is BLACK)")
S.save("refs/product_sheet.png")
for f, n in [("26_x_4fe3e4b5.webp", "closeup_ruching.png"), ("08_x_b9a1ca23.webp", "front_real.png")]:
    Image.open(L + f).convert("RGB").save("refs/" + n)
print("SHEET_OK", S.size)
