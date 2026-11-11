"""Clip QC sheets: per video, one row per clip (8 frames across 4 s) -> qc/clips_<V>.jpg. python3 tools/clipqc.py V13 ..."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
J = Path(__file__).resolve().parent.parent
S = json.loads((J / "shots.json").read_text())
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
for v in sys.argv[1:]:
    ks = sorted((k for k in S if S[k]["video"] == v), key=lambda k: S[k]["window"][0])
    W, H, N = 180, 320, 8
    sheet = Image.new("RGB", (W * N, H * len(ks)), "white"); d = ImageDraw.Draw(sheet)
    for r, k in enumerate(ks):
        f = J / f"clips/{k}_sd.mp4"
        if not f.exists(): continue
        tmp = J / f"qc/_t_{k}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", f"fps={N/4:.3f},scale={W}:{H},tile={N}x1", "-frames:v", "1", str(tmp)])
        sheet.paste(Image.open(tmp), (0, r * H)); tmp.unlink()
        d.rectangle([0, r * H, 70, r * H + 30], fill="black"); d.text((5, r * H + 3), k[-1], font=F, fill="white")
    sheet.save(J / f"qc/clips_{v}.jpg", quality=82)
    print(v, "sheet ok")
