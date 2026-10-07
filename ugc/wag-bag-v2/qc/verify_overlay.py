"""Overlay checks for r4 (photo stickers). python3 -I qc/verify_overlay.py stickers|zones"""
import json, sys
from pathlib import Path
from PIL import Image
J = Path(__file__).resolve().parent.parent
V = json.loads((J / "videos.json").read_text())["videos"]
def fail(m): print("FAIL", m); sys.exit(1)
pops = [(v["n"], p) for v in V for s in v["segments"] for p in s.get("pops", [])]
g = sys.argv[1]
if g == "stickers":
    for n in ("water", "battery", "generator"):
        im = Image.open(J / "emoji" / f"photo_{n}.png")
        if im.size != (512, 512) or im.mode != "RGBA" or im.getchannel("A").getextrema()[0] != 0: fail(f"photo_{n}.png not 512px RGBA with transparency")
    for n, p in pops:
        src = Image.open(J / "emoji" / p["png"]).size[0]
        if p["size"] / src > 1.2: fail(f"V{n} {p['png']} shown at {p['size'] / src:.2f}x")
    kinds = {p["png"] for _, p in pops}
    if not {"photo_water.png", "photo_battery.png", "photo_generator.png"} <= kinds: fail("a photo sticker is missing from the pops")
    if kinds & {"fluent/droplet_3d.png", "fluent/battery_3d.png", "fluent/high_voltage_3d.png"}: fail("old emoji still used")
    print("stickers OK")
elif g == "zones":   # Grace's face sits in x 300-780 on the hook; top overlays must clear it and stay in frame, 5 pops per video
    for v in V:
        ps = [p for s in v["segments"] for p in s.get("pops", [])]
        if len(ps) != 5: fail(f"V{v['n']} has {len(ps)} pops")
    for n, p in pops:
        h = p["size"] / 2
        if not (h <= p["x"] <= 1080 - h and h <= p["y"] <= 1920 - h): fail(f"V{n} {p['png']} leaves the frame")
        if p["png"].startswith("photo_") and not (p["x"] + h <= 300 or p["x"] - h >= 780): fail(f"V{n} {p['png']} overlaps the face zone")
    print("zones OK")
