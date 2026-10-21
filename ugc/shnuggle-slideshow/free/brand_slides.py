"""Option 2 (free): Shnuggle's own photos framed 9:16 (1080x1920), no AI. python3 brand_slides.py"""
from PIL import Image, ImageFilter
B = "../../shnuggle-response/refs/brand/"
# B2: in-shower photo, plain 9:16 crop centred on the tub (true size, real room)
a = Image.open(B + "ToddlerBathinShowerSquareImage.jpg").convert("RGB")
a.crop((440, 0, 1940, 2666)).resize((1080, 1920), Image.LANCZOS).save("../slides_free/B2.jpg", quality=95)
# B1: in-bath photo is wider than 9:16 around the tub: whole photo across the width, over a soft blurred copy of itself
a = Image.open(B + "ShnuggleToddlerBathinBathroomBath-HighRes-Square.jpg").convert("RGB")
bg = a.resize((1920, 1920), Image.LANCZOS).crop((420, 0, 1500, 1920)).filter(ImageFilter.GaussianBlur(45))
from PIL import ImageEnhance
bg = ImageEnhance.Brightness(bg).enhance(1.04); fg = a.resize((1080, 1080), Image.LANCZOS); bg.paste(fg, (0, 420)); bg.save("../slides_free/B1.jpg", quality=95)
# B3: the real front cut-out on a soft light-grey studio background with a floor shadow
t = Image.open("tub_cut.png"); t = t.crop(t.getbbox()); s = 860 / t.width; t = t.resize((860, round(t.height * s)), Image.LANCZOS)
c = Image.new("RGB", (1080, 1920), (236, 238, 240)); g = Image.new("L", (1080, 1920), 0)
from PIL import ImageDraw
by = 1280; ImageDraw.Draw(g).ellipse((540 - 380, by - 90, 540 + 400, by + 20), fill=120); g = g.filter(ImageFilter.GaussianBlur(25))
c = Image.composite(Image.new("RGB", c.size, (150, 152, 158)), c, g); c.paste(t, (540 - t.width // 2, by - t.height), t)
c.save("../slides_free/B3.jpg", quality=95); print("ok")
