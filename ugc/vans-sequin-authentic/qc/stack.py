import sys
from PIL import Image, ImageDraw
out, ids = sys.argv[1], sys.argv[2:]
ims = [Image.open(f"qc/sheets/{i}.jpg").resize((1600, 356)) for i in ids]
s = Image.new("RGB", (1600, 376 * len(ims)), "white"); d = ImageDraw.Draw(s)
for k, (i, im) in enumerate(zip(ids, ims)): d.text((4, k * 376 + 4), i, fill="black"); s.paste(im, (0, k * 376 + 20))
s.save(out, quality=82)
