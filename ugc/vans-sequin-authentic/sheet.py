"""Contact sheet of stills: python3 sheet.py out.jpg id ... (labels each tile)."""
import sys
from PIL import Image, ImageDraw
out, ids = sys.argv[1], sys.argv[2:]
W, H = 300, 537; cols = min(5, len(ids)); rows = (len(ids) + cols - 1) // cols
s = Image.new("RGB", (cols * W, rows * (H + 24)), "white"); d = ImageDraw.Draw(s)
for i, sid in enumerate(ids):
    p = f"stills/{sid}_clean.png"
    import os; p = p if os.path.exists(p) else f"stills/{sid}.png"
    im = Image.open(p).convert("RGB").resize((W, H)); x, y = (i % cols) * W, (i // cols) * (H + 24)
    s.paste(im, (x, y + 24)); d.text((x + 6, y + 6), sid, fill="black")
s.save(out, quality=88); print(out, s.size)
