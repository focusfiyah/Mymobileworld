"""Product reference sheet for the Monbix Remy comforter set, Autumn Leaf (2026-10-26). Real pixels only:
the TikTok Shop listing photos (refs/listing/) and frames from two creators' videos of the same listing
(refs/real/, cropped below their on-screen text so no text reaches a prompt)."""
from PIL import Image, ImageDraw, ImageFont
Image.open('research/frames/tori/t17.png').convert('RGB').crop((0, 640, 720, 1280)).save('refs/real/flatsheet_back_tori.png')
import cv2, numpy as np
lst = {k: Image.open(f'refs/listing/{k}.png').convert('RGB') for k in ['main_01', 'main_03', 'main_07', 'main_08']}
lst['main_03'].crop((172, 460, 262, 590)).save('refs/closeup_pocket_listing.png')
lst['main_07'].crop((330, 380, 800, 800)).save('refs/closeup_stripe_listing.png')
# paint out the listing's numbered circles on B (they are not on the product)
m8 = np.array(lst['main_08']); mask = np.zeros(m8.shape[:2], np.uint8)
for x, y in [(608, 77), (548, 108), (694, 86), (736, 133), (643, 166), (520, 192), (647, 242)]:
    cv2.circle(mask, (int((x - 410) * 2 / 0.95), int((y - 29) * 2 / 0.95 + 150)), 26, 255, -1)
lst['main_08'] = Image.fromarray(cv2.inpaint(m8, mask, 9, cv2.INPAINT_TELEA))
W, H = 2400, 2100
s = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(s)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
def put(im, xy, w, h, label):
    r = min(w / im.width, h / im.height); a = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    s.paste(a, (xy[0], xy[1] + 38)); d.text(xy, label, fill='black', font=f)
put(lst['main_01'], (30, 20), 760, 760, 'A  whole set (throw + small cushion NOT in set)')
put(lst['main_08'].crop((0, 150, 800, 640)), (820, 20), 760, 600, 'B  the 7 pieces')
put(Image.open('refs/real/pocket_real_tori2.png'), (1610, 20), 760, 680, 'C  REAL side pocket (fitted sheet)')
put(Image.open('refs/closeup_pocket_listing.png'), (30, 840), 560, 560, 'D  pocket each side')
put(Image.open('refs/real/stripe_real_grace.jpg'), (620, 840), 560, 420, "E  REAL stripe, Grace's own sheet")
put(Image.open('refs/real/comforter_texture_tori.png'), (1210, 840), 560, 460, 'F  REAL comforter (solid)')
put(Image.open('refs/real/flatsheet_back_tori.png'), (1800, 840), 570, 560, 'G  REAL flat sheet, pale back')
lines = ['Monbix Remy Stripe comforter set, colour "Autumn Leaf" (terracotta / burnt orange). Queen = 7 pieces:',
         '1 comforter: SOLID terracotta both sides, prewashed crinkled microfiber, soft quilting lines, no pattern, no logo.',
         '2 shams: solid terracotta. 2 pillowcases + flat sheet + fitted sheet: thin terracotta and white stripes,',
         'terracotta bands a little wider than the off-white ones, distressed print texture. Print on one side: backs pale.',
         'Fitted sheet: ONE sewn-on striped patch pocket on EACH long side of the bed (phone / book size), on the side drop.',
         'Queen stripes run head to foot on top of the bed. No labels, logos or text anywhere on the bedding.']
for i, t in enumerate(lines): d.text((30, 1480 + i * 46), t, fill='black', font=f)
s.save('refs/product_sheet.png'); print(s.size)
