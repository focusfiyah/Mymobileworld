"""Every-frame face check for overlays (Ralph 2026-11-23: "The overlays are showing on Grace face it need to not happens").
python3 facecheck.py detect BASE.mp4   -> out/faces.json (YuNet face box per frame, 30 fps, base cut without overlays)
python3 facecheck.py place             -> moves each overlay in pops.json to a spot clear of the face (+ hair margin) in EVERY frame it shows
python3 facecheck.py verify FINAL.mp4  -> re-detects faces on the final cut, prints FACE_CLEAR or each frame an overlay touches the face"""
import json, sys, cv2
from pathlib import Path
here = Path(__file__).resolve().parent; MODEL = "/tmp/claude-0/yunet.onnx"; FPS = 30
def detect(video):
    cap = cv2.VideoCapture(video); det = cv2.FaceDetectorYN.create(MODEL, "", (540, 960), 0.6); out = []
    while True:
        ok, fr = cap.read()
        if not ok: break
        fr = cv2.resize(fr, (540, 960)); _, f = det.detect(fr); boxes = []
        for r in (f if f is not None else []):
            x, y, w, h = [float(v) * 2 for v in r[:4]]
            boxes.append([x - w * 0.35, y - h * 0.55, x + w * 1.35, y + h * 1.25])  # face + hair/headband + chin margin
        out.append(boxes)
    return out
def boxes_of(P):
    res = []
    for p in P["pops"]:
        s = p.get("size", P["size"]) * 1.2 / 2; res.append((p, p["x"] - s, p["y"] - s, p["x"] + s, p["y"] + s))
    cx, cy, bw, bh = P["film_box"]
    for fm in P.get("films", []):
        fx, fy = fm.get("x", cx), fm.get("y", cy); w = fm.get("w", bw); h = w * bh / bw
        res.append((fm, fx - w / 2 - 8, fy - h / 2 - 8, fx + w / 2 + 8, fy + h / 2 + 8))
    for im in P.get("images", []):
        w = im["h"] * 0.81; res.append((im, im["x"] - w / 2, im["y"] - im["h"] / 2, im["x"] + w / 2, im["y"] + im["h"] / 2))
    return res
def hits(faces, P):
    bad = []
    for item, x0, y0, x1, y1 in boxes_of(P):
        for k in range(int(item["t"] * FPS), int((item["t"] + item["d"]) * FPS) + 1):
            for fx0, fy0, fx1, fy1 in (faces[k] if k < len(faces) else []):
                if x0 < fx1 and x1 > fx0 and y0 < fy1 and y1 > fy0: bad.append((item.get("png", item.get("src", "")).split("/")[-1], round(k / FPS, 2))); break
    return bad
cmd = sys.argv[1]
if cmd == "detect":
    f = detect(sys.argv[2]); (here / "out/faces.json").write_text(json.dumps(f)); print("frames", len(f), "with face", sum(1 for b in f if b))
elif cmd in ("place", "verify"):
    P = json.loads((here / "pops.json").read_text())
    faces = detect(sys.argv[2]) if cmd == "verify" else json.loads((here / "out/faces.json").read_text())
    if cmd == "place":
        for p in P["pops"] + P.get("images", []):
            half = (p.get("size", P["size"]) * 1.2 if "png" in p and "h" not in p else max(p["h"], p["h"] * 0.81)) / 2
            def clear(x, y):
                half = p.get("size", P["size"]) * 0.6
                q = dict(p, x=x, y=y); tmp = dict(P, pops=[q] if q in [q] and "h" not in p else [], images=[q] if "h" in p else [], films=[])
                return not hits(faces, tmp)
            if clear(p["x"], p["y"]): continue
            sizes = [p.get("size", P["size"])] + ([240, 200] if "h" not in p else [])
            cands = [(sz, x, y) for sz in sizes for y in range(int(360 + sz * 0.6), int(1560 - sz * 0.6) + 1, 40) for x in range(int(40 + sz * 0.6), int(1040 - sz * 0.6) + 1, 40)]
            cands.sort(key=lambda c: (-c[0], (c[1] - p["x"]) ** 2 + (c[2] - p["y"]) ** 2))
            for sz, x, y in cands:
                if "h" not in p: p["size"] = sz
                if (p["t"] < P.get("hook_until", 0) and y + half > 1140): continue
                if clear(x, y): print("moved", p.get("png"), (p["x"], p["y"]), "->", (x, y)); p["x"], p["y"] = x, y; break
            else: print("NO CLEAR SPOT", p.get("png"))
        (here / "pops.json").write_text(json.dumps(P, indent=1))
    if cmd == "place":
        cx, cy, bw, bh = P["film_box"]
        for fm in P.get("films", []):
            one = lambda x, y: not hits(faces, dict(P, pops=[], images=[], films=[dict(fm, x=x, y=y)]))
            if one(fm.get("x", cx), fm.get("y", cy)): continue
            cands = [(x, y) for y in range(360 + bh // 2 + 8, 1140 - bh // 2 - 8 + 1, 20) for x in range(40 + bw // 2 + 8, 1040 - bw // 2 - 8 + 1, 20)]
            cands.sort(key=lambda c: (c[0] - cx) ** 2 + (c[1] - cy) ** 2)
            done = False
            for w in (bw, 380, 320):
                fm["w"] = w; h = w * bh // bw
                cands = [(x, y) for y in range(360 + h // 2 + 8, 1140 - h // 2 - 8 + 1, 20) for x in range(40 + w // 2 + 8, 1040 - w // 2 - 8 + 1, 20)]
                cands.sort(key=lambda c: (c[0] - cx) ** 2 + (c[1] - cy) ** 2)
                for x, y in cands:
                    if one(x, y): print("moved film", fm["src"].split("/")[-1], "->", (x, y), "w", w); fm["x"], fm["y"] = x, y; done = True; break
                if done: break
            if not done: print("NO CLEAR SPOT film", fm["src"]); fm["w"] = bw
        (here / "pops.json").write_text(json.dumps(P, indent=1))
    bad = hits(faces, P)
    films_bad = [b for b in bad]
    print("FACE_CLEAR" if not bad else f"FACE_HITS {len(bad)}: " + ", ".join(f"{n}@{t}" for n, t in bad[:40]))
