"""Free fix: restore the real pale-yellow lens tint on an over-glasses still (model rendered clear lenses).
python3 tint_fo.py ID "x,y x,y ..." "x,y ..."   (lens polygons in still pixels; raw kept in old_stills/ID_raw.png)"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sid = sys.argv[1]
src = Image.open(f"old_stills/{sid}_raw.png").convert("RGB")
m = Image.new("L", src.size, 0); d = ImageDraw.Draw(m)
for poly in sys.argv[2:]:
    d.polygon([tuple(map(float, p.split(","))) for p in poly.split()], fill=255)
m = m.filter(ImageFilter.GaussianBlur(4))
yellow = ImageChops.multiply(src, Image.new("RGB", src.size, (255, 226, 120)))
lift = Image.blend(yellow, Image.new("RGB", src.size, (235, 205, 90)), 0.18)
Image.composite(lift, src, m.point(lambda v: int(v * 0.85))).save(f"stills/{sid}.png")
