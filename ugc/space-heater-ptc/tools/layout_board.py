"""Free layout boards (room plate per shot + line + HAND/HAND-FREE), one per video: storyboard/<V>_layout.jpg. Layout only: the paid stills replace it."""
import json, textwrap
from PIL import Image, ImageDraw, ImageFont
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; fb = ImageFont.truetype(F.replace(".ttf", "-Bold.ttf"), 22); fs = ImageFont.truetype(F, 18)
S = json.load(open("shots.json"))["shots"]
for v in ("V1", "V2", "V3"):
    vs = [s for s in S if s["video"] == v]; W, H, cols = 300, 533, 5; rows = (len(vs) + cols - 1) // cols
    b = Image.new("RGB", (W * cols, (H + 190) * rows), "white"); d = ImageDraw.Draw(b)
    for i, s in enumerate(vs):
        im = Image.open(s["room"]).convert("RGB"); r = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * r), round(im.height * r))); x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        x, y = (i % cols) * W, (i // cols) * (H + 190); b.paste(im.crop((x0, y0, x0 + W, y0 + H)), (x, y))
        tag = s["kind"]; d.rectangle((x + 6, y + 6, x + 20 + d.textlength(f"{s['id']} {tag}", font=fb), y + 36), fill=(255, 140, 0) if s["hand"] else (40, 120, 220))
        d.text((x + 12, y + 8), f"{s['id']} {tag}", font=fb, fill="white")
        d.multiline_text((x + 6, y + H + 6), "\n".join(textwrap.wrap(s["line"], 30)[:7]), font=fs, fill="black")
    b.save(f"storyboard/{v}_layout.jpg", quality=85)
print("ok")
