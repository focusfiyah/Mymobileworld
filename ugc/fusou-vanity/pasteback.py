"""Paste-back (free): keep the REAL photo everywhere the AI didn't intend to change (Ralph, 2026-10-03).

  python3 pasteback.py still BASE AI OUT [--keep x0,y0,x1,y1 ...]   still: real pixels outside the hand/LED areas
  python3 pasteback.py video BASE CLIP OUT [--hand-below ROW]       clip: same, frame by frame (locked camera only); ROW = top of the hand's area
AI image is aligned to BASE (ORB + RANSAC affine), colour-matched, then a diff mask picks what the AI changed.
Writes OUT and OUT_mask.png (white = AI pixels kept) so the mask can be checked.
"""
import os, subprocess, sys
from pathlib import Path
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
    opt = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
    boxes = [tuple(map(int, sys.argv[i + 1].split(","))) for i, a in enumerate(sys.argv) if a == "--ai-box"]
    video(base, src, out, int(opt("--hand-below") or 0), light="--no-light" not in sys.argv, ai_boxes=boxes, seed=opt("--seed"))


def skin(img):  # Grace's skin + mauve nails vs the white/grey vanity (YCrCb)
    y, cr, cb = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb))
    return ((cr > 133) & (cr < 185) & (cb > 77) & (cb < 135) & (y > 30) & (y < 170)).astype(np.uint8)   # y<170: lit white surfaces are not skin


def video(base, src, out, zone=0, light=True, ai_boxes=(), seed=None):
    """v2 (2026-10-03, after Ralph saw shimmer): ONE smoothed alignment path, ONE colour match, and only two AI areas:
    the hand (skin pixels that differ from the real photo) + a FIXED ring where the LEDs light up. Everything else = real photo."""
    cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); h, w = base.shape[:2]; frames = []
    while True:
        ok, fr = cap.read()
        if not ok: break
        frames.append(cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA))
    As = []
    for fr in frames:
        _, A = align(fr, base); As.append(A if A is not None else (As[-1] if As else np.float32([[1, 0, 0], [0, 1, 0]])))
    As = np.array(As, np.float64); k = 9                                   # moving average over 9 frames = no jitter
    pad = np.concatenate([As[:1].repeat(k // 2, 0), As, As[-1:].repeat(k // 2, 0)])
    As = np.array([pad[i:i + k].mean(0) for i in range(len(frames))])
    al = [cv2.warpAffine(fr, A, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT) for fr, A in zip(frames, As)]
    calm = cv2.absdiff(al[0], base).max(axis=2) < T
    gains = [(base[..., c][calm].mean(), base[..., c][calm].std(), al[0][..., c][calm].mean(), max(al[0][..., c][calm].std(), 1)) for c in range(3)]
    def cm(img):
        o = img.astype(np.float32)
        for c, (bm, bs, am, as_) in enumerate(gains): o[..., c] = (o[..., c] - am) * (bs / as_) + bm
        return np.clip(o, 0, 255)
    al = [cm(a) for a in al]; bf = base.astype(np.float32)
    static = np.zeros((h, w), bool); static[:zone or h // 2] = True                  # area with no hand
    ref = al[0][static].mean(0)
    al = [np.clip(a * (ref / np.maximum(a[static].mean(0), 1)), 0, 255) for a in al]  # hold exposure + white balance steady
    lit = (al[-1].mean(2) - bf.mean(2)) > 45                               # LED ring only: much brighter in the last (lit) frame
    lit = cv2.morphologyEx(lit.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    lit = cv2.morphologyEx(lit, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(lit)
    if n > 1: lit = (lab == 1 + int(np.argmax(st[1:, 4]))).astype(np.uint8)   # only the LED ring (largest shape), not stray edges
    hand_any = np.zeros((h, w), np.uint8)
    hand_masks, prev = [], None
    if seed:   # start from the still's own hand area (a wrist hidden behind an object never touches the frame edge)
        sm = cv2.resize(cv2.imread(seed, cv2.IMREAD_GRAYSCALE), (w, h)) > 127
        prev = cv2.dilate(sm.astype(np.uint8), np.ones((31, 31), np.uint8))
    base_skin = cv2.dilate(skin(base), np.ones((5, 5), np.uint8))          # nude lipsticks, wood: skin-coloured in the REAL photo = never the hand
    for a in al:
        d = (np.abs(a - bf).max(2) > T).astype(np.uint8) & skin(a.astype(np.uint8)) & (1 - base_skin)
        d[:zone] = 0                                                        # hand can only be below this row (per shot)
        d = cv2.morphologyEx(d, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(d)                 # pick the hand BEFORE closing, so items never merge into it
        edge = lambda i: st[i, 1] + st[i, 3] >= h - 2 or st[i, 0] + st[i, 2] >= w - 2 or st[i, 0] <= 1   # hand enters from bottom/right/left
        keep = [i for i in range(1, n) if st[i, 4] > MIN_AREA * d.size and (edge(i) or (prev is not None and (prev[lab == i] > 0).any()))]
        if prev is not None:   # track: keep only blobs that overlap last frame's hand
            keep = [i for i in keep if (prev[lab == i] > 0).any()]
        d = np.isin(lab, keep).astype(np.uint8)
        d = cv2.morphologyEx(d, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
        cs, _ = cv2.findContours(d, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(d, cs, -1, 1, cv2.FILLED)
        hand_masks.append(cv2.dilate(d, np.ones((9, 9), np.uint8)).astype(np.float32))
        prev = cv2.dilate(d, np.ones((31, 31), np.uint8)) if d.any() else prev
    ring = cv2.GaussianBlur(cv2.dilate(lit, np.ones((11, 11), np.uint8)).astype(np.float32), (31, 31), 0) if lit.any() else np.zeros((h, w), np.float32)
    if not light: lit = np.zeros_like(lit)
    lum = np.array([a[lit > 0].mean() if lit.any() else 0 for a in al]); on = int(np.argmax(np.diff(lum))) + 1 if lit.any() else len(al)
    lit_f = al[min(on + 5, len(al) - 1)]                                     # ONE lit frame, held steady (no AI drift)
    L, Lb = lit_f.mean(2), bf.mean(2)
    wl = np.clip((L - 190) / 40, 0, 1)[..., None]                            # only where the AI shows near-white LED light
    plate = np.clip(bf + np.maximum(L - Lb, 0)[..., None] * wl, 0, 255)      # ADD light to the real photo: items keep their real look
    FADE = round(0.25 * fps)                                                 # LED soft-start, like a dimmable mirror
    obj = np.zeros((h, w), np.float32)                                       # areas where the hand MOVES something (plug, drawer, door, lipstick)
    for x0, y0, x1, y1 in ai_boxes: obj[y0:y1, x0:x1] = 1
    obj = cv2.GaussianBlur(obj, (41, 41), 0)
    print(f"lights on at frame {on} ({on / fps:.2f}s), fade {FADE} frames")
    if os.environ.get("PB_ON_FILE"): Path(os.environ["PB_ON_FILE"]).write_text(f"{on / fps:.3f} {FADE / fps:.3f}")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps),
                           "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    shares = []
    for i, a in enumerate(al):
        hm = np.max(hand_masks[max(0, i - 1):i + 2], axis=0)                 # +-1 frame: a fast finger never gets clipped
        k = float(np.clip((i - on + 1) / FADE, 0, 1)); k = k * k * (3 - 2 * k)      # smooth 0->1 fade of the ring
        bg = bf * (1 - ring[..., None] * k) + plate * ring[..., None] * k       # real photo + steady lit ring
        mh = np.maximum(cv2.GaussianBlur(hm, (21, 21), 0), obj)[..., None]
        if os.environ.get("PB_DEBUG") and i == 72: cv2.imwrite(os.environ["PB_DEBUG"], np.hstack([hm * 255, ring * 255]).astype(np.uint8))
        ff.stdin.write((a * mh + bg * (1 - mh)).astype(np.uint8).tobytes()); shares.append(float(np.maximum(mh[..., 0], ring).mean()))
    ff.stdin.close(); ff.wait()
    sc = np.hypot(As[:, 0, 0], As[:, 1, 0])
    print(f"frames {len(al)}  AI share min/max {min(shares):.3f}/{max(shares):.3f}  ring {ring.mean():.3f}  scale {sc.min():.3f}/{sc.max():.3f}")

if __name__ == "__main__":
    main()
