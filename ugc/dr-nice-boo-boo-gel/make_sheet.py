"""Product reference sheet for Dr. Nice's Boo-Boo Gel (1 fl oz pump), from real photos (2026-11-03, free).
refs/real: grace_photo_*.jpg = photos Ralph sent (Telegram); bNN = drniceproducts.com listing images (SOURCES.md)."""
from PIL import Image, ImageDraw, ImageFont
R = 'refs/real/'
def o(n): return Image.open(R + n).convert('RGB')
bottle = o('b01.png').crop((300, 180, 640, 1500)); bottle.save('refs/bottle_front.png')        # whole bottle, cap on
label = o('b01.png').crop((345, 680, 675, 1185)); label.save('refs/closeup_label.png')          # front label, letter for letter
logo = o('b01.png').crop((350, 700, 670, 885)); logo = logo.resize((logo.width*2, logo.height*2), Image.LANCZOS); logo.save('refs/closeup_logo.png')
pump = o('b03.png').crop((230, 330, 700, 1100)); pump.save('refs/pump_open.png')                # cap off: silver pump head (current design)
hand = o('grace_photo_knee.jpg').crop((690, 100, 1100, 770)); hand.save('refs/bottle_in_hand.png') # size vs a child's hand
W, H = 2400, 1700
s = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(s)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
def fit(im, w, h):
    r = min(w / im.width, h / im.height); return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
def put(im, xy, w, h, label):
    a = fit(im, w, h); s.paste(a, (xy[0], xy[1] + 40)); d.text(xy, label, fill='black', font=f); return a
put(bottle, (30, 20), 460, 1440, 'A  REAL BOTTLE, cap on')
put(label, (520, 20), 720, 1100, 'B  REAL FRONT LABEL')
put(logo, (1270, 20), 1100, 300, 'C  logo close-up')
put(pump, (1270, 420), 560, 740, 'D  cap off: silver pump')
put(hand, (1860, 420), 500, 740, 'E  size in a child hand')
for i, t in enumerate(['1 fl oz (30 ml) airless pump: tall slim cylinder about 3.3x as tall as wide (about 11 cm tall, 3 cm wide).',
                       'Brushed silver cap over the top third, thin shiny chrome ring, sky-blue label band, silver base.',
                       'Clear gel, one pearl-sized dot per pump. Box: white front, blue edges (not used in shots).']):
    d.text((30, 1560 + i * 45), t, fill='black', font=f)
s.save('refs/product_sheet.png'); print(s.size)
