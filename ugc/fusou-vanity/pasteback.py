"""Paste-back (free): keep the REAL photo everywhere the AI didn't intend to change (Ralph, 2026-10-03).

  python3 pasteback.py still BASE AI OUT [--keep x0,y0,x1,y1 ...]   still: real pixels outside the hand/LED areas
  python3 pasteback.py video BASE CLIP OUT                          clip: same, frame by frame (locked camera only)
AI image is aligned to BASE (ORB + RANSAC affine), colour-matched, then a diff mask picks what the AI changed.
Writes OUT and OUT_mask.png (white = AI pixels kept) so the mask can be checked.
"""
import subprocess, sys
import cv2, numpy as np

T = 30          # per-pixel diff (0-255) above which the AI pixel is kept
MIN_AREA = 0.002  # drop changed blobs smaller than this share of the frame (re-render noise)


def align(ai, base):
    g1, g2 = cv2.cvtColor(ai, cv2.COLOR_BGR2GRAY), cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(4000); k1, d1 = orb.detectAndCompute(g1, None); k2, d2 = orb.detectAndCompute(g2, None)
    m = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d1, d2), key=lambda x: x.distance)[:800]
    A, inl = cv2.estimateAffinePartial2D(np.float32([k1[x.queryIdx].pt for x in m]), np.float32([k2[x.trainIdx].pt for x in m]),
                                         method=cv2.RANSAC, ransacReprojThreshold=2.0)
    if A is None: return ai, None
    return cv2.warpAffine(ai, A, (base.shape[1], base.shape[0]), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT), A


def colour_match(ai, base, calm):
    out = ai.astype(np.float32)
    for c in range(3):
        a, b = out[..., c][calm], base[..., c][calm].astype(np.float32)
        out[..., c] = (out[..., c] - a.mean()) * (b.std() / max(a.std(), 1)) + b.mean()
    return np.clip(out, 0, 255).astype(np.uint8)


def diff_mask(ai, base, keep=()):
    d = cv2.absdiff(cv2.GaussianBlur(ai, (7, 7), 0), cv2.GaussianBlur(base, (7, 7), 0)).max(axis=2)
    m = (d > T).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    m = np.isin(lab, [i for i in range(1, n) if st[i, 4] > MIN_AREA * m.size]).astype(np.uint8)
    for x0, y0, x1, y1 in keep: m[y0:y1, x0:x1] = 1
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(m, cs, -1, 1, cv2.FILLED)   # fill holes (skin that happens to match the background colour)
    m = cv2.dilate(m, np.ones((15, 15), np.uint8))
    return cv2.GaussianBlur(m.astype(np.float32), (31, 31), 0)[..., None]


def composite(ai, base, keep=()):
    ai, A = align(ai, base)
    rough = cv2.absdiff(ai, base).max(axis=2) < T
    ai = colour_match(ai, base, rough)
    m = diff_mask(ai, base, keep)
    return (ai * m + base * (1 - m)).astype(np.uint8), m, A, ai


def main():
    mode, base_p, src, out = sys.argv[1:5]
    keep = [tuple(map(int, k.split(","))) for k in sys.argv[sys.argv.index("--keep") + 1:]] if "--keep" in sys.argv else []
    base = cv2.imread(base_p)
    if mode == "still":
        ai = cv2.resize(cv2.imread(src), (base.shape[1], base.shape[0]), interpolation=cv2.INTER_AREA)
        img, m, A, _ = composite(ai, base, keep)
        cv2.imwrite(out, img); cv2.imwrite(out.rsplit(".", 1)[0] + "_mask.png", (m[..., 0] * 255).astype(np.uint8))
        print("affine", None if A is None else np.round(A, 3).tolist(), "AI share", round(float(m.mean()), 3))
        return
    cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); h, w = base.shape[:2]
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps),
                           "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    shares, scales, prev = [], [], None
    while True:
        ok, fr = cap.read()
        if not ok: break
        fr = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA)
        _, m, A, al = composite(fr, base)
        m = prev = m if prev is None else np.maximum(m, 0.6 * prev)   # current AI area always fully kept; old area fades (no flicker, no see-through hand)
        img = (al * m + base * (1 - m)).astype(np.uint8)
        ff.stdin.write(img.tobytes()); shares.append(float(m.mean()))
        scales.append(None if A is None else float(np.hypot(*A[:, 0])))
    ff.stdin.close(); ff.wait()
    s = [x for x in scales if x]
    print(f"frames {len(shares)}  AI share min/max {min(shares):.3f}/{max(shares):.3f}  scale min/max {min(s):.3f}/{max(s):.3f}")


if __name__ == "__main__":
    main()
