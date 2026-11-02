"""Product reference sheet for Buttah Silky Soft Towels 24 ct, from the brand's real listing photos (2026-11-02, free).
refs/real/rNN = buttahskin.com listing images (SOURCES.md). Writes refs/product_sheet.png + refs/closeup_*.png."""
from PIL import Image, ImageDraw, ImageFont
R = 'refs/real/'
def o(n): return Image.open(R + n).convert('RGB')
front = o('r08.jpg').crop((600, 1650, 2400, 3050))
front.save('refs/front_clean.png')
logo = o('r08.jpg').crop((880, 1940, 2120, 2350)); logo.save('refs/closeup_logo.png')       # buttah. + Silky Soft Towels
badges = o('r08.jpg').crop((1150, 2380, 1950, 2900)); badges.save('refs/closeup_badges.png')  # window strip, 3 badges, white lines
W, H = 2400, 2100
s = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(s)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
def fit(im, w, h):
    r = min(w / im.width, h / im.height); return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
def put(im, xy, w, h, label):
    a = fit(im, w, h); s.paste(a, (xy[0], xy[1] + 40)); d.text(xy, label, fill='black', font=f); return a
put(front, (30, 20), 1100, 860, 'A  REAL POUCH FRONT (soft flat pack, 24 towels)')
put(logo, (1160, 20), 1200, 400, 'B  logo close-up')
put(badges, (1160, 470), 620, 420, 'C  window strip + badges + lines')
put(o('r01.png').crop((30, 330, 1122, 1300)), (1820, 470), 560, 500, 'D  pouch + folded towel stack')
put(o('r03.png').crop((0, 450, 1122, 1402)), (30, 960), 700, 620, 'E  ONE towel opened (XL)')
put(o('r05.jpg').crop((0, 0, 1200, 900)), (760, 960), 620, 460, 'F  waffle texture')
put(o('r06.jpg').crop((100, 200, 1000, 1000)), (1410, 1000), 560, 500, 'G  pouch in a hand (size)')
put(o('r04.jpg').crop((500, 450, 1200, 1500)), (2000, 1000), 380, 560, 'H  folded towels')
for i, t in enumerate(['Soft flat pouch: mint-teal glossy plastic edges, black front panel, crinkled seal ends left and right.',
                       'Each towel opens to 11.875 x 10.875 in (30 x 28 cm), white, small square waffle texture, no print.',
                       'Folded towels: small white squares with the same waffle texture, stacked neatly.']):
    d.text((30, 1900 + i * 50), t, fill='black', font=f)
s.save('refs/product_sheet.png'); print(s.size)
