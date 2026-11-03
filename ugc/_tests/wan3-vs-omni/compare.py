"""Side-by-side: S3 still | Omni take | Wan 3.0 take at the same times, plus 2x label crops and a 15 fps strip of Wan.
  python3 compare.py   -> compare.png, label_2x.png, strip/  (all gitignored media)
"""
import subprocess as sp
from pathlib import Path
J = Path(__file__).resolve().parent; Z = J.parents[1] / "zytrell-acne-cream"
OMNI, WAN, STILL = Z / "clips/S3_omni_1.mp4", J / "S3_wan3.mp4", Z / "stills/S3.png"
def f(src, t, out, vf):
    sp.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(src), "-frames:v", "1", "-vf", vf, str(out)], check=True)
tmp = J / "_tmp"; tmp.mkdir(exist_ok=True)
times = [0.3, 1.0, 2.0, 3.0, 3.8]
rows = []
for name, src in (("omni", OMNI), ("wan", WAN)):
    tiles = []
    for i, t in enumerate(times):
        p = tmp / f"{name}{i}.png"; f(src, t, p, "scale=-2:720,drawtext=text='%s %.1fs':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6" % (name.upper(), t)); tiles.append(p)
    r = tmp / f"row_{name}.png"
    sp.run(["ffmpeg", "-loglevel", "error", "-y", *sum([["-i", str(x)] for x in tiles], []), "-filter_complex", f"hstack={len(tiles)}", str(r)], check=True); rows.append(r)
sp.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(rows[0]), "-i", str(rows[1]), "-filter_complex", "scale2ref=iw:ih[a][b];[a][b]vstack", str(J / "compare.png")], check=True)
# 2x label crop: centre band of the frame where the tube sits, upscaled 2x
crops = []
for name, src in (("omni", OMNI), ("wan", WAN)):
    for t in (1.0, 3.0):
        p = tmp / f"lab_{name}_{t}.png"; f(src, t, p, "crop=iw*0.5:ih*0.5:iw*0.25:ih*0.12,scale=iw*2:-2,scale=-2:900"); crops.append(p)
sp.run(["ffmpeg", "-loglevel", "error", "-y", *sum([["-i", str(x)] for x in crops], []), "-filter_complex", f"hstack={len(crops)}", str(J / "label_2x.png")], check=True)
(J / "strip").mkdir(exist_ok=True)
sp.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(WAN), "-vf", "fps=15,scale=-2:480,tile=10x1", str(J / "strip/wan_%02d.png")], check=True)
print("COMPARE_OK")
