"""stills/<ID>.png (1536x2752) -> slides/<ID>.jpg 1080x1920 (resize, centre crop 15 px). python3 make_slides.py [IDs]"""
import sys
from pathlib import Path
from PIL import Image
for sid in sys.argv[1:] or [p.stem for p in sorted(Path("stills").glob("S*.png"))]:
    im = Image.open(f"stills/{sid}.png").convert("RGB").resize((1080, 1935), Image.LANCZOS)
    im.crop((0, 7, 1080, 1927)).save(f"slides/{sid}.jpg", quality=95); print(sid)
