"""Product reference sheet from Ralph's real photos (2026-10-22): big front label + in-box view + logo close-ups."""
from PIL import Image, ImageDraw, ImageFont
R = 'refs/real/'
up = Image.open(R + 'ralph_pouch_upright.jpg').convert('RGB')
box = Image.open(R + 'ralph_pouches_in_box.jpg').convert('RGB')
W, H = 2000, 2000
s = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(s)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
except Exception: f = ImageFont.load_default()
def fit(im, w, h):
    r = min(w / im.width, h / im.height); return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
a = fit(up, 820, 1880); s.paste(a, (30, 80)); d.text((30, 20), 'A  REAL FRONT (1 fl oz pouch)', fill='black', font=f)
b = fit(box, 560, 1240); s.paste(b, (900, 80)); d.text((900, 20), 'B  pouches in the open box', fill='black', font=f)
# close-ups cut from the upright pouch (pixel boxes measured on ralph_pouch_upright.jpg, 1670x3980)
crops = {'C logo + dot circle': (330, 900, 1330, 2000), 'D wordmark + claims': (100, 2000, 1590, 3480), 'E tear tab': (550, 0, 1280, 420)}
y = 80
for k, bx in crops.items():
    c = fit(up.crop(bx), 480, 560 if 'tab' not in k else 300)
    s.paste(c, (1490, y + 40)); d.text((1490, y), k, fill='black', font=f); y += c.height + 80
s.save('refs/product_sheet.png'); print(s.size)
for k, bx in crops.items(): up.crop(bx).save('refs/closeup_' + k.split()[0] + '.png')
