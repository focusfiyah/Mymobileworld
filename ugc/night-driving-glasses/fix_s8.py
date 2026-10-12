"""Free fix: remove the fake 'REC 00:02:14' camera text the model drew on still S8 (no text in videos)."""
from PIL import Image, ImageFilter, ImageDraw
im = Image.open("old/S8_raw.png").convert("RGB")
box = (10, 1060, 100, 1300)
patch = im.crop((100, 1060, 190, 1300)).filter(ImageFilter.GaussianBlur(6))   # dark dashboard just right of the text
m = Image.new("L", (box[2] - box[0], box[3] - box[1]), 0); ImageDraw.Draw(m).rectangle((6, 6, 84, 234), fill=255)
im.paste(patch, box[:2], m.filter(ImageFilter.GaussianBlur(5)))
im.save("stills/S8.png"); im.crop((0, 1000, 300, 1376)).save("/tmp/claude-0/s8fix.png")
