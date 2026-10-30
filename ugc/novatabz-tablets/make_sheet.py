"""Product reference sheet from the 3 listing photos Ralph sent (free), NovaTabz 2026-10-30.
  python3 make_sheet.py -> refs/product_sheet.png, refs/real/closeup_label.png, refs/real/closeup_lid.png, refs/real/closeup_tablets.png"""
from PIL import Image, ImageDraw, ImageFont
a = Image.open("refs/jar_front_render.jpg").convert("RGB")
b = Image.open("refs/jar_open_mint.jpg").convert("RGB")
c = Image.open("refs/jar_box.jpg").convert("RGB")
front = a.crop((15, 95, 1015, 930))                      # closed jar, straight front, silver lid
label = a.crop((300, 425, 720, 760)).resize((840, 670), Image.LANCZOS)     # front print close-up (2x)
lid = a.crop((15, 95, 1015, 340))                         # knurled silver lid
opened = b.crop((10, 160, 1000, 1137))                    # lid off, white tablets inside (mint leaves cropped out)
tabs = c.crop((30, 760, 210, 900)).resize((540, 420), Image.LANCZOS)      # loose tablets, 3x
box = c.crop((690, 90, 1072, 720))                       # white box
label.save("refs/real/closeup_label.png"); lid.save("refs/real/closeup_lid.png"); tabs.save("refs/real/closeup_tablets.png")
W, H = 2200, 2000
s = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(s)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
def put(im, x, y, w, title):
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS); s.paste(im, (x, y + 45)); d.text((x, y), title, fill="black", font=f); return im.height + 45
h = put(front, 40, 30, 1100, "FRONT, CLOSED: clear glass jar, silver screw lid, turquoise label")
put(label, 1180, 30, 980, "LABEL PRINT (white + turquoise, serif NOVA TABZ)")
h2 = put(opened, 40, 30 + h + 30, 820, "OPEN: lid off, white round tablets inside")
put(tabs, 900, 30 + h + 30, 600, "TABLETS: white, round, flat")
put(box, 1600, 30 + h + 30, 480, "BOX: white cube")
d.text((40, H - 60), "Jar about 2.6 in wide x 2 in tall (palm-sized, estimate). 62 tablets, 23 g. Glass jar, metal lid, no plastic.", fill="black", font=f)
s.save("refs/product_sheet.png"); print("ok", s.size)
