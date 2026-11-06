"""Product reference sheet for Migrastil Extra Strength Neuropathy Cream (4 oz jar), from Grace's 2 real photos (Telegram 2026-11-06, free)."""
from PIL import Image, ImageDraw, ImageFont
R = 'refs/real/'
front = Image.open(R + '2026-11-06 photo-786406539.jpg').convert('RGB')
back = Image.open(R + '2026-11-06 photo-786406538.jpg').convert('RGB')
crops = {
 'jar_front': front.crop((95, 50, 725, 760)),
 'closeup_label': front.crop((180, 290, 680, 640)),
 'closeup_band': front.crop((270, 135, 690, 235)),
 'closeup_logo': front.crop((185, 300, 650, 525)),
 'closeup_usa': front.crop((560, 505, 680, 620)),
 'jar_back': back.crop((60, 30, 1010, 1060)),
}
for k, im in crops.items():
    if im.width < 300: im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im.save(f'refs/{k}.png'); crops[k] = im
W, H = 2400, 1700
s = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(s)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
def put(im, xy, w, h, t):
    r = min(w / im.width, h / im.height); a = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    s.paste(a, (xy[0], xy[1] + 40)); d.text(xy, t, fill='black', font=f)
put(crops['jar_front'], (30, 20), 760, 820, 'A  REAL JAR, front, lid on')
put(crops['jar_back'], (30, 880, ), 600, 620, 'B  REAL JAR, back (ingredients)')
put(crops['closeup_label'], (830, 20), 900, 640, 'C  REAL FRONT LABEL')
put(crops['closeup_band'], (1760, 20), 620, 200, 'D  green top band')
put(crops['closeup_logo'], (1760, 300), 620, 360, 'E  logo close-up')
put(crops['closeup_usa'], (830, 720), 300, 300, 'F  USA shield')
for i, t in enumerate([
 '4 oz (113 g) round jar, straight sides, about as tall as wide (lid included).',
 'Glossy dark cobalt-blue jar, wide glossy black screw lid.',
 'Navy wrap label. Green band at the top: navy NON-BURNING RELIEF',
 'and a white hand icon on a blue square.',
 'MIGRASTIL white serif caps, Extra Strength white,',
 'Neuropathy Cream big lime green, Gentle, Non-Burning Relief white,',
 'white arcs lower left, red-white-blue USA shield, Made in the USA.',
 'Back: white ingredient text on navy, white barcode panel.']):
    d.text((1180, 760 + i * 44), t, fill='black', font=f)
s.save('refs/product_sheet.png'); print(s.size)
