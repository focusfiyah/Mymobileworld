"""Product reference sheet from REAL listing pixels only (free), HEVEBLUE eye cream 2026-10-27.
  python3 make_sheet.py -> refs/product_sheet.png, refs/real/closeup_print.png, refs/real/closeup_tip.png"""
from PIL import Image, ImageDraw, ImageFont
R = "refs/real/"
im1, im2, im3, im4 = (Image.open(R + f"listing_img0{i}.jpg") for i in (1, 2, 3, 4))
front = im1.crop((405, 50, 575, 965))                     # whole tube, straight front
printc = im1.crop((415, 60, 565, 470)).resize((450, 1230), Image.LANCZOS)   # print close-up (3x)
tip = im1.crop((440, 680, 545, 965)).resize((315, 855), Image.LANCZOS)      # chrome neck, black ring, tip
held = im3.crop((300, 400, 580, 760))                    # hand on the chrome, tip with cream (dashed circle cropped out)
capped = im2.crop((420, 380, 980, 940))                   # with the black cap, on beans
angled = im4.crop((700, 0, 1000, 1000))                   # tube only, no marketing text
printc.save(R + "closeup_print.png"); tip.save(R + "closeup_tip.png")
W, H = 2000, 2000
s = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(s)
try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
except OSError: f = ImageFont.load_default()
fr = front.resize((int(front.width * 1780 / front.height), 1780), Image.LANCZOS); s.paste(fr, (40, 120))
d.text((40, 40), "FRONT (real photo): white tube, black print, chrome applicator", fill="black", font=f)
x0 = 40 + fr.width + 40
s.paste(printc.resize((330, 900)), (x0, 120)); d.text((x0, 70), "PRINT", fill="black", font=f)
s.paste(tip.resize((260, 705)), (x0 + 360, 120)); d.text((x0 + 360, 70), "TIP", fill="black", font=f)
x1 = x0 + 660
s.paste(capped.resize((W - x1 - 40, W - x1 - 40)), (x1, 120)); d.text((x1, 70), "CAP ON (matte black)", fill="black", font=f)
s.paste(angled.resize((266, 886)), (x0 + 180, 1080)); d.text((x0, 1040), "ANGLED", fill="black", font=f)
d.text((40, 1930), "15 ml tube, about 16 cm long x 2 cm wide (estimate). No button, no light.", fill="black", font=f)
s.save("refs/product_sheet.png"); print("ok", s.size)
