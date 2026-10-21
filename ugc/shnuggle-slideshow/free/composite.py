"""Option 3 (free): the REAL Shnuggle cut-out placed at true size into a free real bathroom photo (Unsplash licence).
Scale: floor tiles read as 22.3 cm squares set on the diagonal -> ~18 px/cm at the placement depth (y~3950);
true rim width 49 cm (maker's drawing) -> ~880 px. python3 composite.py -> slides/C1.jpg"""
from PIL import Image, ImageDraw, ImageFilter
room = Image.open("stock/chevron.jpg").convert("RGB"); tub = Image.open("tub_cut.png")
tub = tub.crop(tub.getbbox()); PX_CM, RIM_CM = 18.0, 49.0
from PIL import ImageEnhance
rgb = ImageEnhance.Brightness(tub.convert("RGB")).enhance(1.05); rgb.putalpha(tub.getchannel("A")); tub = rgb  # studio grey -> room whites
s = PX_CM * RIM_CM / tub.width; tub = tub.resize((round(tub.width * s), round(tub.height * s)), Image.LANCZOS)
cx, base_y = 1300, 3950; x0, y0 = cx - tub.width // 2, base_y - tub.height
# contact shadow on the floor (multiply)
sh = Image.new("L", room.size, 0); d = ImageDraw.Draw(sh)
bw = int(39.0 * PX_CM * 1.05); d.ellipse((cx - bw // 2 - 20, base_y - 120, cx + bw // 2 + 50, base_y + 22), fill=150)
d.ellipse((cx - bw // 2 + 30, base_y - 45, cx + bw // 2 - 20, base_y + 6), fill=235)
sh = sh.filter(ImageFilter.GaussianBlur(22))
dark = Image.new("RGB", room.size, (70, 72, 80)); room = Image.composite(dark, room, sh.point(lambda v: int(v * 0.8)))
room.paste(tub, (x0, y0), tub)
W = 1700; H = W * 16 // 9; L = max(0, min(room.width - W, cx - W // 2)); T = room.height - H
out = room.crop((L, T, L + W, T + H)).resize((1080, 1920), Image.LANCZOS)
out.save("../slides_free/C1.jpg", quality=95); print("tub px", tub.size, "crop", (L, T, W, H))
