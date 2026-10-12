"""Free fix (no paid call): restore the real pale-yellow lens tint on still S4 v2 (model rendered it grey-olive)."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
src = Image.open("old/S4_v2_raw.png").convert("RGB")
m = Image.new("L", src.size, 0); d = ImageDraw.Draw(m)
f = lambda pts: [(x / 2 + 80, y / 2 + 470) for x, y in pts]   # points measured on the 2x lens crop
d.polygon(f([(70, 70), (440, 82), (448, 290), (385, 335), (85, 325)]), fill=255)
d.polygon(f([(575, 92), (945, 115), (960, 325), (900, 345), (565, 340)]), fill=255)
m = m.filter(ImageFilter.GaussianBlur(4))
yellow = ImageChops.multiply(src, Image.new("RGB", src.size, (255, 226, 120)))
lift = Image.blend(yellow, Image.new("RGB", src.size, (235, 205, 90)), 0.18)
out = Image.composite(lift, src, m.point(lambda v: int(v * 0.85)))
out.save("stills/S4.png")
out.crop((80, 470, 600, 720)).resize((1040, 500)).save("/tmp/claude-0/lens2.png")
