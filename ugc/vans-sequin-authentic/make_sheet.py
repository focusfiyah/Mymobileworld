"""Product reference sheet (free, real Vans photos only): big 3/4 pair + side, top/sole, back, sequin close-up."""
from PIL import Image, ImageDraw, ImageFont
R = "refs/"
W, H = 1600, 2400
s = Image.new("RGB", (W, H), (236, 233, 228)); d = ImageDraw.Draw(s)
try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
except Exception: f = ImageFont.load_default()
def put(name, box, label):
    im = Image.open(R + name).convert("RGB"); x0, y0, x1, y1 = box
    im.thumbnail((x1 - x0, y1 - y0 - 40), Image.LANCZOS)
    s.paste(im, (x0 + (x1 - x0 - im.width) // 2, y0 + 40)); d.text((x0 + 10, y0 + 4), label, fill=(30, 30, 30), font=f)
put("vans_ALT1.jpg", (0, 0, 1600, 1250), "REAL PRODUCT - 3/4 PAIR (Vans Premium Authentic, sequin checkerboard)")
put("vans_HERO.jpg", (0, 1250, 800, 1830), "SIDE")
put("vans_ALT2.jpg", (800, 1250, 1600, 1830), "TOP (red insole) + WAFFLE SOLE")
put("vans_ALT3.jpg", (0, 1830, 800, 2400), "BACK (black heel, OFF THE WALL tab)")
put("vans_ALT4.jpg", (800, 1830, 1600, 2400), "SEQUIN CLOSE-UP")
s.save(R + "product_sheet.png"); print("ok", s.size)
