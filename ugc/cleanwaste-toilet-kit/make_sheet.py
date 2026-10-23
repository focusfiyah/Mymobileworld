"""Product reference sheet (Ralph 2026-10-19, PLAYBOOK §6), free, real pixels only.
Big: the real 12-pack box front. Small: box back, kit pouch front/back, kit contents, waste + zip bags, bag on a seat.
Also writes tight crops used as separate refs: refs/crop_box_front.png, refs/crop_pouch_front.png."""
from PIL import Image, ImageDraw, ImageFont, ImageChops
R = "refs/real/"

def trim(im, bg=None, tol=18):
    im = im.convert("RGB"); bg = bg or im.getpixel((5, 5))
    diff = ImageChops.difference(im, Image.new("RGB", im.size, bg)).convert("L").point(lambda v: 255 if v > tol else 0)
    return im.crop(diff.getbbox() or (0, 0, *im.size))

box = trim(Image.open(R + "box_front_12pk.jpg")); box.save("refs/crop_box_front.png")
pouch = trim(Image.open(R + "kit_pouch_front.jpg")); pouch.save("refs/crop_pouch_front.png")
small = [("box back (real)", trim(Image.open(R + "box_back_12pk.jpg"))), ("kit pouch front (real)", pouch),
         ("kit pouch back (real)", trim(Image.open(R + "kit_pouch_back.jpg"))), ("kit contents (real)", trim(Image.open(R + "kit_contents_layout.jpg"))),
         ("blue-grey bags (real)", trim(Image.open(R + "waste_bag_and_zip_disposal_bag.jpg"))),
         ("bag on a seat (real)", Image.open(R + "bag_on_toilet_seat_and_contents.jpg").convert("RGB").crop((0, 0, 600, 743)))]
W = 2000; sheet = Image.new("RGB", (W, 2050), "white"); d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
except OSError: f = ImageFont.load_default()
b = box.copy(); b.thumbnail((1900, 1000), Image.LANCZOS); sheet.paste(b, ((W - b.width) // 2, 70))
d.text((50, 15), "CLEANWASTE 12-PACK BOX FRONT (REAL, the exact print): wide low box, about twice as wide as tall", fill="black", font=f)
y0 = 90 + b.height + 40; cw = (W - 40) // 3
for i, (lab, im) in enumerate(small):
    t = im.copy(); t.thumbnail((cw - 30, 420), Image.LANCZOS)
    x = 20 + (i % 3) * cw; y = y0 + (i // 3) * 500
    sheet.paste(t, (x + (cw - t.width) // 2, y + 45)); d.text((x + 10, y), lab, fill="black", font=f)
sheet = sheet.crop((0, 0, W, y0 + 1000)); sheet.save("refs/product_sheet.png"); print(sheet.size, box.size, pouch.size)
