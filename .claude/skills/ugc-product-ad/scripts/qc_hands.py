"""Free QC (2026-10-03, after Ralph found background items ON the hand and missing wrists): for every frame, count hand pixels the paste-back
replaced. A pixel counts when the raw Seedance frame shows skin there, the raw differs from the real photo there (the hand is really in front),
and the final differs from the raw (so the background was pasted over the hand).

  python3 qc_hands.py CLIP ...   (CLIP = M2a ...; reads clips/<CLIP>_raw.mp4, clips/<CLIP>.mp4, refs/base_<still>.png)
Prints the worst frame and saves qc/<CLIP>_worst.jpg (raw | final | holes in red).
"""
import os, sys
import cv2, numpy as np
import pasteback as pb   # same folder as this script
os.makedirs("qc", exist_ok=True)


def frames(f, w, h):
    c = cv2.VideoCapture(f); out = []
    while True:
        ok, x = c.read()
        if not ok: return out
        out.append(cv2.resize(x, (w, h), interpolation=cv2.INTER_AREA))


for clip in sys.argv[1:]:
    base = cv2.imread(f"refs/base_{clip[:2]}.png"); h, w = base.shape[:2]; bf = base.astype(np.float32)
    raw, fin = frames(f"clips/{clip}_raw.mp4", w, h), frames(f"clips/{clip}.mp4", w, h)
    worst = (0, 0, None)
    for i, (r, f) in enumerate(zip(raw, fin)):
        ra, _ = pb.align(r, base); ra = ra.astype(np.float32); ff = f.astype(np.float32)
        hand = pb.skin(ra.astype(np.uint8)).astype(bool) & (np.abs(ra - bf).max(2) > 30)
        hand = cv2.morphologyEx(hand.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)).astype(bool)
        holes = hand & (np.abs(ff - ra).max(2) > 45)
        holes = cv2.morphologyEx(holes.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)).astype(bool)
        n = int(holes.sum())
        if n > worst[0]: worst = (n, i, (ra, ff, holes))
    n, i, data = worst
    print(f"{clip}: worst frame {i} ({i / 24:.2f}s): {n} hand pixels replaced ({n / (w * h) * 100:.2f}% of frame)")
    if data:
        ra, ff, holes = data; red = ff.copy(); red[holes] = (0, 0, 255)
        cv2.imwrite(f"qc/{clip}_worst.jpg", cv2.resize(np.hstack([ra, ff, red]).astype(np.uint8), (810, 480)))
