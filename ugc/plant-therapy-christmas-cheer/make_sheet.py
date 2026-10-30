"""Free product reference sheet + label close-ups from the REAL listing photos (no AI views)."""
from PIL import Image, ImageDraw, ImageFont
R = "refs/"
trio = Image.open(R + "listing_1.jpg").convert("RGB")           # 1080x1080 fronts
boxp = Image.open(R + "listing_5.jpg").convert("RGB")           # 3000: box + trio on orange
back = Image.open(R + "listing_10.jpg").convert("RGB")          # 3000: back labels
neck = Image.open(R + "real_neck_capoff.jpg").convert("RGB")
# label close-ups (whole bottle, cap to base) from the 1080 front photo
crops = {"tree": (95, 50, 365, 840), "plum": (405, 50, 675, 840), "vanilla": (715, 50, 985, 840)}
for k, b in crops.items():
    c = trio.crop(b); c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS); c.save(R + f"closeup_{k}.png")
box = boxp.crop((150, 600, 1950, 2200)); box.save(R + "closeup_box.png")
W, H = 2160, 2880
S = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(S)
try:
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
except OSError:
    f = ImageFont.load_default()
S.paste(trio.resize((1440, 1440)), (0, 0)); d.text((30, 1450), "FRONT (real photo): Christmas Tree / Sugar Plum Fairy / Vanilla Spice", fill="black", font=f)
b2 = box.resize((720, 640)); S.paste(b2, (1440, 0)); d.text((1460, 650), "BOX (real)", fill="black", font=f)
n2 = neck.resize((720, int(neck.height * 720 / neck.width))); n2 = n2.crop((0, 0, 720, 760)); S.paste(n2, (1440, 720))
d.text((1460, 1490), "CAP OFF (real)", fill="black", font=f)
bk = back.crop((200, 800, 2800, 2600)).resize((2160, 1300)); S.paste(bk, (0, 1540))
d.text((30, 2850 - 44), "BACK (real). Each bottle 10 mL, ~2.5 cm wide, ~6 cm tall with cap, black ribbed cap", fill="black", font=f)
S.save(R + "product_sheet.png"); print("sheet ok")
