"""Product reference sheet from REAL pixels (free), Hidden Camera Detector LY-10, 2026-10-28.
  python3 make_sheet.py -> refs/product_sheet.png
Views: Grace's own black unit (Ralph's photos, ref/real/) for print, buttons, LEDs and window; the listing's
side view only for thickness (listing renders show a purple/pink window: wrong, the real window is teal-green)."""
from PIL import Image, ImageDraw, ImageFont
R = "refs/real/"
back = Image.open(R + "closeup_back_buttons.jpg"); front = Image.open(R + "closeup_front_leds.jpg")
side = Image.open(R + "listing_size.jpg").crop((255, 140, 395, 530))      # listing side view, shape/thickness only
W, H = 2320, 1700
s = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(s)
try:
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    g = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
except OSError:
    f = g = ImageFont.load_default()
for i, (im, label) in enumerate([(back, "BACK (real): 3 speaker dots, window, power + light buttons"),
                                 (front, "FRONT (real): sensor, flashlight LED, 4 clear LEDs, window")]):
    t = im.resize((int(im.width * 1380 / im.height), 1380), Image.LANCZOS)
    x = 40 + i * (t.width + 60)
    s.paste(t, (x, 120)); d.text((x, 40), label.split(":")[0], fill="black", font=f)
    d.text((x, 80), label.split(": ")[1], fill="black", font=g)
x2 = 40 + 2 * (int(back.width * 1380 / back.height) + 60)
sv = side.resize((int(side.width * 1100 / side.height), 1100), Image.LANCZOS)
s.paste(sv, (x2 + 20, 200)); d.text((x2, 40), "SIDE", fill="black", font=f)
d.text((x2, 80), "thickness only", fill="black", font=g)
for k, line in enumerate(["Matte BLACK body, soft rounded oval, about 6 x 4 x 1.8 cm (body), 50 g: about the size of an AirPods case.",
                          "Black silicone teardrop loop at the bottom; about 11 cm long with the loop (listing: 4.29 x 1.61 x 0.71 in).",
                          "Window = glossy teal-green filter with a thin red edge (NOT purple). LEDs are clear when off, glow red when on."]):
    d.text((40, 1540 + k * 40), line, fill="black", font=g)
s.save("refs/product_sheet.png"); print("ok", s.size)
