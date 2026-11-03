"""Product reference sheet + logo/label close-ups for the FOODOLOGY Red Jelliquid Bundle, from the brand's real
packshots (refs/brand, foodology-global.com) and Ralph's photo (refs/real/r01_ralph.jpg). Free. 2026-11-03."""
from PIL import Image, ImageDraw, ImageFont
B = 'refs/brand/'
def o(n): return Image.open(n if '/' in n else B + n).convert('RGB')
C = {  # close-ups passed as print references (real pixels)
 'cj_box':    ('coleology-cutting-jelly_00.jpg', (281, 144, 550, 862)),
 'cj_stick':  ('coleology-cutting-jelly_00.jpg', (575, 144, 719, 862)),
 'dm_box':    ('coleology-drink-mix_09.jpg', (712, 375, 1912, 2625)),
 'dm_stick':  ('coleology-drink-mix_09.jpg', (1931, 394, 2306, 2625)),
 'acv_box':   ('amazon-acv-jelly-ver1_08.jpg', (1040, 338, 1800, 1800)),
 'acv_box_front': ('refs/real/r01_ralph.jpg', (880, 275, 1125, 760)),
 'acv_stick': ('amazon-acv-jelly-ver1_00.jpg', (1150, 560, 1800, 1620)),
 'acv_jelly_hand': ('amazon-acv-jelly-ver1_06.jpg', (1150, 300, 1733, 1800)),
 'cj_jelly':  ('coleology-cutting-jelly_06.jpg', (225, 560, 1800, 1800)),
 'cj_open':   ('coleology-cutting-jelly_02.jpg', (1000, 0, 1800, 1800)),
 'dm_pour':   ('coleology-drink-mix_04.jpg', (950, 0, 1800, 1800)),
}
for k, (f, box) in C.items(): o(f).crop(box).save(f'refs/closeup_{k}.png')
W, H = 2400, 2000
s = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(s)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
def put(k, xy, w, h, label):
    im = Image.open(f'refs/closeup_{k}.png'); r = min(w / im.width, (h - 40) / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS); s.paste(im, (xy[0], xy[1] + 36)); d.text(xy, label, fill='black', font=f)
put('cj_box', (20, 10), 420, 800, 'A Cutting Jelly box')
put('cj_stick', (450, 10), 180, 800, 'B stick')
put('dm_box', (650, 10), 560, 800, 'C Drink Mix PRO box')
put('dm_stick', (1220, 10), 200, 800, 'D stick')
put('acv_box_front', (1440, 10), 420, 800, 'E ACV Apple Jelly box')
put('acv_stick', (1880, 10), 500, 800, 'F ACV stick print')
put('acv_box', (20, 850), 520, 900, 'G ACV box 3/4 (sharp)')
put('acv_jelly_hand', (560, 850), 560, 900, 'H ACV jelly, hand (size)')
put('cj_jelly', (1140, 850), 700, 560, 'I chia jelly (ruby red, black seeds)')
put('dm_pour', (1860, 850), 520, 560, 'J powder into water = pink drink')
import textwrap
y = 1430
for t in ['Boxes: cream-white with a red bottom third; sticks: white flat film, red bottom band, dashed OPEN tear line near the top.',
          'Jelly is a firm chewy block pushed out of the torn top: Cutting Jelly ruby red with black chia seeds, ACV pale lemon yellow.',
          'Sizes (estimated): stick ~15 x 3.5 cm (wrist crease to fingertips); jelly box ~10 x 16 x 4 cm; Drink Mix box a little wider.']:
    for line in textwrap.wrap(t, 70): d.text((1140, y), line, fill='black', font=f); y += 36
    y += 14
s.save('refs/product_sheet.png'); print(s.size)
