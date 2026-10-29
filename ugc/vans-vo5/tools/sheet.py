"""Storyboard sheets: one row image per video (11 stills, labelled) -> review/img/sb_<V>.jpg; and 2x crops for QC.
python3 tools/sheet.py"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
J = Path(__file__).resolve().parent.parent
S = json.loads((J / "shots.json").read_text())
try: F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except Exception: F = ImageFont.load_default()
for v in sorted({s["video"] for s in S.values()}):
    ks = sorted((k for k in S if S[k]["video"] == v), key=lambda k: S[k]["window"][0])
    W, H = 300, 533; sheet = Image.new("RGB", (W * 6, H * 2), "white"); d = ImageDraw.Draw(sheet)
    for i, k in enumerate(ks):
        p = J / f"stills/{k}.png"
        if not p.exists(): continue
        im = Image.open(p).convert("RGB").resize((W, H)); x, y = (i % 6) * W, (i // 6) * H
        sheet.paste(im, (x, y)); d.rectangle([x, y, x + 80, y + 34], fill="black"); d.text((x + 6, y + 3), k[-1], font=F, fill="white")
    sheet.save(J / f"review/img/sb_{v}.jpg", quality=85)
print("sheets ok")
