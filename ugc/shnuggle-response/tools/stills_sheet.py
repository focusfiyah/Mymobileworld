"""Still sheet with VO lines: python3 tools/stills_sheet.py R2 'R2-01=REDO? wider than the bath' ..."""
import json, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
V = sys.argv[1]; marks = dict(a.split('=', 1) for a in sys.argv[2:])
J = json.load(open('shots.json')); shots = J['videos'][V]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
FL = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
W, H, T = 300, 533, 70
S = Image.new('RGB', (W * 7, (H + T) * 2), 'white'); d = ImageDraw.Draw(S)
for k, s in enumerate(shots):
    x, y = (k % 7) * W, (k // 7) * (H + T)
    S.paste(Image.open(f"stills/{s['id']}.png").convert('RGB').resize((W, H)), (x, y))
    d.text((x + 6, y + 4), s['id'], font=FL, fill='white', stroke_width=3, stroke_fill='black')
    for j, ln in enumerate(textwrap.wrap(s['vo'], 34)[:3]):
        d.text((x + 6, y + H + 4 + j * 19), ln, font=F, fill=(20, 100, 60))
    if s['id'] in marks:
        d.rectangle((x + 1, y + 1, x + W - 2, y + H - 2), outline='red', width=5)
        d.text((x + 8, y + H - 30), marks[s['id']], font=F, fill='white', stroke_width=3, stroke_fill='red')
S.save(f'storyboard/{V}_stills.jpg', quality=88)
