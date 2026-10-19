# Free still storyboard (no generation): one panel per shot with the real product refs it uses, the picture and the VO line.
import json, textwrap
from PIL import Image, ImageDraw, ImageFont
J = json.load(open("shots.json")); F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = F.replace("Sans.", "Sans-Bold.")
f, fb, fs = ImageFont.truetype(F, 17), ImageFont.truetype(FB, 24), ImageFont.truetype(F, 15)
refs = {"bag": Image.open("refs/bag_front.jpg"), "pouch": Image.open("refs/pouch_real.jpg"), "hand": Image.open("refs/hand_grace.jpg")}
W, H, cols = 420, 760, 6; shots = J["shots"]; rows = -(-len(shots) // cols)
sheet = Image.new("RGB", (W * cols, H * rows), "white")
for i, s in enumerate(shots):
    p = Image.new("RGB", (W - 10, H - 10), (246, 246, 243)); d = ImageDraw.Draw(p)
    d.text((14, 10), f"{s['id']}  {s['dur']}s  {s['scene']}", font=fb, fill=(20, 20, 20))
    x = 14
    for k in ("bag", "pouch", "hand"):
        if s.get(k):
            t = refs[k].copy(); t.thumbnail((120, 120)); p.paste(t, (x, 48)); d.text((x, 172), k, font=fs, fill=(90, 90, 90)); x += 130
    if x == 14: d.text((14, 90), "no product, no hand", font=f, fill=(120, 120, 120))
    y = 200
    d.text((14, y), "PICTURE", font=fs, fill=(30, 110, 60)); y += 22
    for line in textwrap.wrap(s["still"] + " MOTION: " + s["video"], 44)[:16]:
        d.text((14, y), line, font=fs, fill=(40, 40, 40)); y += 19
    y += 10; d.text((14, y), "VO (Grace B)", font=fs, fill=(30, 60, 150)); y += 22
    for line in textwrap.wrap('"' + s["vo"] + '"', 36):
        d.text((14, y), line, font=f, fill=(10, 10, 60)); y += 22
    sheet.paste(p, ((i % cols) * W + 5, (i // cols) * H + 5))
sheet.save("preview/storyboard_v1.png"); print(sheet.size)
