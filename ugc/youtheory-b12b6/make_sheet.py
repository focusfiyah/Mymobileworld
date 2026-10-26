"""Product reference sheet from Grace's real photos + the listing render (2026-10-26).
Grace's real pouch has NO 'essential daily vitamins' line next to B12B6 (the listing render does), so that line is
filled with the pouch's own white in the sharp listing crop; Grace's photos stay the truth for shape and print."""
from PIL import Image, ImageDraw, ImageFont
R = 'refs/real/'
lst = Image.open(R + 'listing_pouch_front.jpg').convert('RGB').crop((24, 683, 896, 1553))   # 872x870 white panel
d0 = ImageDraw.Draw(lst)
# remove 'essential daily vitamins' (not on Grace's pouch): each row blends the clean foil left of it into the clean foil right of it
px = lst.load()
for y in range(500, 566):
    a, b = px[472, y], px[596, y]
    for x in range(474, 594):
        k = (x - 472) / 124; px[x, y] = tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))
lst.save('refs/listing_front_clean.png')
W, H = 2400, 2000
s = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(s)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
def fit(im, w, h):
    r = min(w / im.width, h / im.height); return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
def put(im, xy, w, h, label):
    a = fit(im, w, h); s.paste(a, (xy[0], xy[1] + 40)); d.text(xy, label, fill='black', font=f); return a
put(lst.crop((240, 40, 640, 870)), (30, 20), 560, 1160, 'A  FRONT (1 fl oz pouch)')
put(Image.open(R + 'grace_pouch_in_hand.jpg').convert('RGB').crop((40, 200, 520, 1024)), (620, 20), 480, 820, 'B  REAL size in hand')
put(Image.open(R + 'grace_pouch_back_flat.jpg').convert('RGB').crop((150, 260, 400, 680)), (620, 900, ), 480, 1040, 'C  back (facts)')
put(Image.open(R + 'grace_box_front_open.jpg').convert('RGB').crop((40, 330, 450, 780)), (1130, 20), 560, 620, 'D  box front (torn open)')
put(Image.open(R + 'grace_box_end_pouches.jpg').convert('RGB').crop((150, 230, 420, 620)), (1130, 700), 560, 600, 'E  box end + pouches')
crops = {'F logo + dot circle': (330, 270, 560, 500), 'G B12B6 liquid + claims': (290, 490, 600, 760), 'H flavor bar': (330, 715, 560, 760), 'I flat tear-off tab': (350, 55, 540, 160)}
y = 20
for k, bx in crops.items():
    c = lst.crop(bx); c.save('refs/closeup_' + k.split()[0] + '.png')
    a = put(c, (1730, y), 640, 420 if 'flavor' not in k and 'tab' not in k else 200, k); y += a.height + 70
d.text((30, 1830), 'Single-serve 1 fl oz (30 mL) foil pouch, about 6.5 cm wide x 15 cm tall incl. tab.', fill='black', font=f)
d.text((30, 1880), 'White glossy foil, flat magenta tear-off tab (no cap, no spout), magenta dot circle, magenta B12B6.', fill='black', font=f)
d.text((30, 1930), '12 pouches per box. Raspberry flavor.', fill='black', font=f)
s.save('refs/product_sheet.png'); print(s.size)
