"""Measured QC for a cut: python3 qc/cut_qc.py R1|R2 -> per-check OK/FAIL lines + qc/<V>_sheet.jpg (first/mid/last frame of every shot)
and qc/<V>_hands.jpg (2x zoom on the hand in the first and mid frame of every hand shot) for the eye checks."""
import json, subprocess, sys, numpy as np
from PIL import Image, ImageDraw
V = sys.argv[1]; J = json.load(open("shots.json")); shots = J["videos"][V]; out = f"out/shnuggle_{V}.mp4"; bad = 0
def run(c): return subprocess.run(c, capture_output=True, text=True).stdout
def frame(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", out, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (1080, 1920), raw)
def chk(ok, msg):
    global bad; bad += not ok; print(("OK   " if ok else "FAIL ") + msg)
d = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
chk(abs(d - shots[-1]["t"][1]) < 0.15, f"duration {d:.2f}s vs VO {shots[-1]['t'][1]:.2f}s")
vol = run(["ffmpeg", "-i", out, "-af", "volumedetect", "-f", "null", "-"]) + subprocess.run(["ffmpeg", "-i", out, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
mean = float(vol.split("mean_volume:")[1].split()[0]); chk(-30 < mean < -10, f"audio mean {mean} dB")
tiles, hands = [], []
for s in shots:
    a, b = s["t"]; ts = [a + 0.04, (a + b) / 2, b - 0.06]; fr = [frame(t) for t in ts]
    luma = [np.asarray(f.convert("L")).mean() for f in fr]
    chk(min(luma) > 95, f"{s['id']} bright (luma {min(luma):.0f})")
    rgb = np.asarray(fr[1]).reshape(-1, 3).mean(0); chk(rgb[2] > rgb[0] - 25, f"{s['id']} not yellow (R-B {rgb[0]-rgb[2]:.0f})")
    diff = np.abs(np.asarray(fr[0], float) - np.asarray(fr[2], float)).mean(); chk(diff > 1.0, f"{s['id']} moves (first-last diff {diff:.1f})")
    for f in fr: tiles.append((s["id"], f.resize((180, 320))))
    if s.get("hand"):
        for f in fr[:2]: hands.append((s["id"], f))
W = 180 * 6; S = Image.new("RGB", (W, 320 * ((len(tiles) + 5) // 6)), "white"); dr = ImageDraw.Draw(S)
for i, (sid, t) in enumerate(tiles): S.paste(t, ((i % 6) * 180, (i // 6) * 320)); dr.text(((i % 6) * 180 + 4, (i // 6) * 320 + 4), sid, fill="red")
S.save(f"qc/{V}_sheet.jpg", quality=85)
if hands:   # skin-pixel bounding box, padded, shown at 2x of a 540-wide downscale = full res
    H = []
    for sid, f in hands:
        a = np.asarray(f.convert("HSV")); m = (a[..., 0] < 22) & (a[..., 1] > 70) & (a[..., 2] > 50)
        ys, xs = np.nonzero(m)
        box = (0, 0, 1080, 1920) if len(xs) < 500 else (max(xs.min() - 60, 0), max(ys.min() - 60, 0), min(xs.max() + 60, 1080), min(ys.max() + 60, 1920))
        c = f.crop(box); c.thumbnail((540, 540)); H.append((sid, c))
    S = Image.new("RGB", (540 * 4, 540 * ((len(H) + 3) // 4)), "white"); dr = ImageDraw.Draw(S)
    for i, (sid, c) in enumerate(H): S.paste(c, ((i % 4) * 540, (i // 4) * 540)); dr.text(((i % 4) * 540 + 4, (i // 4) * 540 + 4), sid, fill="red")
    S.save(f"qc/{V}_hands.jpg", quality=88)
print(f"{V}: {bad} FAIL")
