"""Drift strip: the frame-by-frame 2x look every pasted, patched or tracked product shot gets before a cut goes out
(Ralph 2026-10-27, Mini Bag Charm: "I see some video drifts", "Slight drift here as well", then "Make sure you have
in your QC process to check for that"). An automatic number could not tell his v5 curtain smear from the fixed v6, so
this is a look, made easy: crops of the product AND a wide margin around it (patch edges, background, what it hangs
from) every ~0.2 s, at 2x, in one sheet. Look for: (1) the product stays attached to what holds it, (2) the background
around it moves with the camera (no smear, blur, blocks or seam), (3) nothing left of the AI's own product, (4) no slide.
  python3 grace/qc/strip.py VIDEO --box X,Y,W,H [--from S --to S] [--every 0.2] [--out sheet.jpg]
  (box in the video's own pixels; give it ~2.5x the product size so the patch edges are in it)"""
import argparse, subprocess
import cv2, numpy as np


def sheet(video, box, t0=0.0, t1=None, every=0.2, out="strip.jpg", cols=8):
    x, y, w, h = box; cap = cv2.VideoCapture(video); fps = cap.get(5) or 24; n = int(cap.get(7))
    t1 = n / fps if t1 is None else t1; tiles = []
    t = t0
    while t <= t1 + 1e-6:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps))); ok, f = cap.read()
        if not ok: break
        c = f[max(0, y):y + h, max(0, x):x + w]; c = cv2.resize(c, (c.shape[1] * 2, c.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
        cv2.putText(c, f"{t:.2f}s", (8, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA); tiles.append(c); t += every
    if not tiles: raise SystemExit("STRIP: no frames")
    th, tw = tiles[0].shape[:2]; tiles = [cv2.resize(c, (tw, th)) for c in tiles]
    rows = [np.hstack(tiles[i:i + cols] + [np.zeros_like(tiles[0])] * (cols - len(tiles[i:i + cols]))) for i in range(0, len(tiles), cols)]
    cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85]); print("STRIP", out, len(tiles), "frames")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--box", required=True)
    ap.add_argument("--from", dest="t0", type=float, default=0.0); ap.add_argument("--to", dest="t1", type=float)
    ap.add_argument("--every", type=float, default=0.2); ap.add_argument("--out", default="strip.jpg")
    a = ap.parse_args(); sheet(a.video, [int(v) for v in a.box.split(",")], a.t0, a.t1, a.every, a.out)
