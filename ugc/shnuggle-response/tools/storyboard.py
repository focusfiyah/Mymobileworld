"""Free layout storyboard (no generation): real brand plates for plate shots; for still shots the setting plate, softened, with the
real tub cut-out placed where the shot frames it, plus the VO words and the action. Out: storyboard/<V>_storyboard.jpg"""
import json, textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont
J = json.load(open("shots.json")); F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLATE = {"R1": "refs/brand/ToddlerBathinShowerSquareImage.jpg", "R2": "refs/brand/ShnuggleToddlerBathinBathroomBath-HighRes-Square.jpg"}
cut = Image.open("refs/brand/Shnuggle_Toddler_Bath_Light_Grey_Backrest_Cut_out.png").convert("RGBA")
m = cut.convert("L").point(lambda v: 255 if v > 246 else 0)
for xy in [(0, 0), (m.width - 1, 0), (0, m.height - 1), (m.width - 1, m.height - 1)]: ImageDraw.floodfill(m, xy, 128)
cut.putalpha(m.point(lambda v: 0 if v == 128 else 255)); cut = cut.crop(cut.getbbox())
W, H, T = 300, 534, 250
def crop916(im, cx=0.5):
    w, h = im.size; cw = int(h * 9 / 16); x = int(max(0, min(w - cw, cx * w - cw / 2))); return im.crop((x, 0, x + cw, h)).resize((W, H))
for v, S in J["videos"].items():
    cols = 7; rows = (len(S) + cols - 1) // cols; sheet = Image.new("RGB", (W * cols, (H + T) * rows), "white"); d = ImageDraw.Draw(sheet)
    base = Image.new("RGB", (900, 1600), {"R1": (178, 201, 171), "R2": (236, 196, 196)}[v])
    for k, s in enumerate(S):
        x, y = (k % cols) * W, (k // cols) * (H + T)
        if s["src"].startswith("plate:"):
            p = crop916(Image.open(s["src"][6:]).convert("RGB")); tag = "REAL PHOTO PLATE (free)"
        else:
            p = crop916(base)
            if s["prod"]:
                sc = 0.75 if any(w in s["still"].lower() for w in ("close-up", "low angle")) else 0.45
                c = cut.resize((int(W * sc), int(W * sc * cut.height / cut.width))); p.paste(c, ((W - c.width) // 2, H - c.height - 60), c)
            tag = "AI still: " + ("Grace hand + rings, " if s["hand"] else "no hand, ") + ("real tub ref" if s["prod"] else "no tub")
        sheet.paste(p, (x, y)); d.rectangle([x, y, x + W - 1, y + H + T - 1], outline="#bbb")
        d.text((x + 8, y + 6), s["id"], font=ImageFont.truetype(FB, 22), fill="black")
        d.text((x + 8, y + H - 24), tag, font=ImageFont.truetype(F, 13), fill="#333")
        ty = y + H + 6
        for ln in textwrap.wrap('"' + s["vo"] + '"', 34)[:5]: d.text((x + 8, ty), ln, font=ImageFont.truetype(FB, 14), fill="#1a4"); ty += 18
        for ln in textwrap.wrap(s["video"], 38)[:7]: d.text((x + 8, ty + 4), ln, font=ImageFont.truetype(F, 13), fill="#222"); ty += 16
    sheet.save(f"storyboard/{v}_storyboard.jpg", quality=88); print("storyboard", v, sheet.size)
