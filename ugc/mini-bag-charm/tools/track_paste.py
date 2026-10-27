"""Real charm laid back onto a Seedance clip, frame by frame (Mini Bag Charm 2026-10-27). Seedance keeps the true size
but redraws the tiny real charm (a flap, a mark on the padlock, a wide scarf), so: the camera move is tracked on the
background (ORB + RANSAC, still -> frame), the AI charm is covered with the clean plate warped the same way, and the
real composite layer (charm, chain, ring, shadow) is warped on top. Free; a paste-back, so used only on Ralph's OK.
  python3 tools/track_paste.py S7 [--follow]  -> clips/S7_track.mp4  (--follow: the charm hangs from a moving hand, S4)"""
import json, os, subprocess, sys
from pathlib import Path
import cv2, numpy as np

CHAIN = set()
ANCHOR = {}  # tried on S9 2026-10-27: jumps late in the clip; was {"S9": (440, 560, 600, 700)}          # plate box: the right handle base + bag top edge
BOX = {"S4": (0.8, 1.9, 0.0, 2.7), "S9": (0.7, 1.4, 0.1, 2.4), "S7": (0.6, 1.3, 0.1, 1.9)}   # left, right, up, down, in charm widths/heights
PLATE = {"S4": "stills/plate_S4.png", "S7": "stills/S7bg.png", "S8": "rooms/roomE_stocking2_crop.png", "S9": "stills/S9bg.png"}


def frames(path):
    cap = cv2.VideoCapture(path)
    while True:
        ok, f = cap.read()
        if not ok: return
        yield f


def charm_colours(f, loose=False):
    """Pixels that belong to a burgundy charm, its pink / light blue / pale scarf, its tissue or its gold hardware."""
    b, g, r = [f[..., i].astype(int) for i in range(3)]
    burg = ((r > 35) & (r < 175) & (g < r * 0.5) & (b > g) & (b < r * 0.85)) if loose else ((r > 55) & (r < 175) & (g < r * 0.45) & (b > g) & (b < r * 0.8))
    pink = (r > 150) & (r - g > 30) & (b > g) & (g > r * 0.45)        # pink scarf, not a red stocking
    blue = (b > r + 15) & (b > 120)
    gold = ((r > 110) & (g > 75) & (b < g * 0.75) & (r > b + 40)) if loose else ((r > 150) & (g > 100) & (b < g * 0.7))
    return (burg | pink | blue | gold).astype(np.uint8) * 255


GAP_MAX = 12.0                                # px: the pasted charm must stay on what it hangs from (S4 v4 floated)                # QC limits (set on Mini Bag Charm v5 vs v6, 2026-10-27)
HANG = {"S4": (338, 749)}                     # still px where the charm's handles meet the chain (composite.swap hang)
_ring = {}


def hang_chain(f, g, M, hang):
    """Find the gold key ring the AI hand moves (gold blob above the charm), draw a short gold chain from its bottom
    to the real charm's handles, so the charm never floats."""
    FH, FW = f.shape[:2]; tx, ty = M @ np.array([hang[0], hang[1], 1.0])
    b, gg, r = [f[..., i].astype(int) for i in range(3)]
    gold = ((r > 140) & (gg > 95) & (b < gg * 0.72) & (r > b + 50)).astype(np.uint8)
    y0, y1, x0, x1 = int(ty - 140), int(ty - 3), int(tx - 70), int(tx + 70)
    ys, xs = np.nonzero(gold[y0:y1, x0:x1])
    if "p" not in _ring: return g
    rx, ry = _ring["p"]
    if ty - ry < 4: return g
    S = 4; lay = np.zeros((FH * S, FW * S, 4), np.uint8); n = max(2, int((ty - ry) / 7))
    for i in range(n):
        a0, a1 = i / n, (i + 1) / n
        cx = (rx + (tx - rx) * (a0 + a1) / 2) * S; cy = (ry + (ty - ry) * (a0 + a1) / 2) * S
        L = (ty - ry) / n * S; rw = (2.0 if i % 2 == 0 else 0.8) * S
        cv2.ellipse(lay, (int(cx), int(cy)), (int(rw), int(L * 0.62)), 0, 0, 360, (52, 132, 176, 255), max(2, int(1.1 * S)), cv2.LINE_AA)
        cv2.ellipse(lay, (int(cx), int(cy)), (max(1, int(rw - 1)), max(1, int(L * 0.62 - 1))), 0, 0, 360, (120, 200, 236, 255), max(1, int(0.4 * S)), cv2.LINE_AA)
    lay = cv2.resize(lay, (FW, FH), interpolation=cv2.INTER_AREA).astype(np.float32)
    a = lay[..., 3:] / 255; return g * (1 - a) + lay[..., :3] * a


def run(sid, follow=False):
    still = cv2.imread(f"stills/{sid}.png"); plate = cv2.imread(PLATE[sid])
    diff = (np.abs(still.astype(int) - plate.astype(int)).max(2) > 3).astype(np.uint8) * 255
    diff = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    ov_a = cv2.GaussianBlur(diff, (3, 3), 0)                       # the real layer: charm, chain, ring, shadow
    import os
    if os.path.exists(f"stills/overlay_{sid}.png"):               # an uncut layer saved by composite.py (S8)
        o = cv2.imread(f"stills/overlay_{sid}.png", cv2.IMREAD_UNCHANGED); still = o[..., :3].copy(); ov_a = o[..., 3].copy()
    x, y, w, h = cv2.boundingRect(diff)
    keep = np.zeros(plate.shape[:2], np.uint8)                     # track the handbag NEAR the charm (no parallax from the far room)
    keep[max(0, y - h):y + 3 * h, max(0, x - 2 * w):x + 3 * w] = 255
    keep[max(0, y - h // 3):y + int(1.6 * h), max(0, x - w // 3):x + int(1.4 * w)] = 0
    if sid in BOX:                                                 # only the handbag's own leather (the tree/room move differently)
        pb, pg, pr = [plate[..., i].astype(int) for i in range(3)]
        leather = ((pr > 50) & (pr < 210) & (pr > pg + 8) & (pg > pb) & (pr - pb > 20) & (pg > pr * 0.5)).astype(np.uint8) * 255
        leather = cv2.dilate(leather, np.ones((21, 21), np.uint8))   # + its outline against the room: strong edges to track
        keep[leather == 0] = 0
    orb = cv2.ORB_create(4000, fastThreshold=7); kp0, d0 = orb.detectAndCompute(cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY), keep)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    src = list(frames(f"clips/{sid}_seedance.mp4")); FH, FW = src[0].shape[:2]
    Ms = []
    for f in src:
        kp1, d1 = orb.detectAndCompute(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), None)
        mt = sorted(bf.match(d0, d1), key=lambda m: m.distance)[:600]
        a = np.float32([kp0[m.queryIdx].pt for m in mt]); b = np.float32([kp1[m.trainIdx].pt for m in mt])
        M, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=2.5)
        Ms.append(M)
    if sid in ANCHOR:                                              # lock onto the handle base the charm hangs from (no drift)
        (ax0, ay0, ax1, ay1) = ANCHOR[sid]; tpl = cv2.cvtColor(plate[ay0:ay1, ax0:ax1], cv2.COLOR_BGR2GRAY)
        cx, cy = (ax0 + ax1) / 2, (ay0 + ay1) / 2; k0 = float(np.hypot(*Ms[0][:, 0])); out_M = []
        for f in src:
            g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY); best = (-2, 0, 0, 0)
            for sc in np.linspace(0.92, 1.35, 22):
                t = cv2.resize(tpl, None, fx=k0 * sc, fy=k0 * sc, interpolation=cv2.INTER_AREA)
                r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
                if mv > best[0]: best = (mv, k0 * sc, ml[0] + t.shape[1] / 2, ml[1] + t.shape[0] / 2)
            _, k, mx, my = best; out_M.append(np.array([[k, 0, mx - k * cx], [0, k, my - k * cy]]))
        Ms = out_M
    elif sid in CHAIN:                                             # low-texture leather: chain frame to frame with optical flow
        A = lambda M: np.vstack([M, [0, 0, 1]])
        cur = A(Ms[0]); chained = [Ms[0]]
        for i in range(1, len(src)):
            g0 = cv2.cvtColor(src[i - 1], cv2.COLOR_BGR2GRAY); g1 = cv2.cvtColor(src[i], cv2.COLOR_BGR2GRAY)
            km = cv2.warpAffine(keep, cur[:2], (FW, FH))
            p0 = cv2.goodFeaturesToTrack(g0, 600, 0.005, 6, mask=km)
            p1, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p0, None, winSize=(31, 31), maxLevel=4)
            ok = st.ravel() == 1
            Mi, _ = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
            cur = A(Mi) @ cur; chained.append(cur[:2].copy())
        Ms = chained
    Ms = np.array(Ms); k = 7                                       # smooth the track (no jitter)
    Ms = np.array([Ms[max(0, i - k):i + k + 1].mean(0) for i in range(len(Ms))])
    hang0 = None; hx = []
    if follow:                                                     # where the AI charm hangs in each frame
        prev = None
        for f in src:
            m = charm_colours(f)
            if sid == "S9":                                       # only the burgundy body, in a window that follows it
                b, g, r = [f[..., i].astype(int) for i in range(3)]
                m = ((r > 35) & (r < 175) & (g < r * 0.5) & (b > g) & (b < r * 0.85)).astype(np.uint8) * 255
                if prev is None: prev = (M0x := Ms[0] @ np.array([x + w / 2, y + h * 0.6, 1.0]))
                win = np.zeros_like(m); px, py = int(prev[0]), int(prev[1]); win[max(0, py - 110):py + 110, max(0, px - 90):px + 90] = 255; m &= win
                m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            else:
                m[:int(FH * 0.45)] = 0
            ys, xs = np.nonzero(m)
            if len(xs) > 200:
                hx.append((np.median(xs), np.median(ys))); prev = hx[-1]
            else: hx.append((np.nan, np.nan))
        hx = np.array(hx, float); good = ~np.isnan(hx[:, 0])
        for j in range(2): hx[:, j] = np.interp(np.arange(len(hx)), np.nonzero(good)[0], hx[good, j])
        hx = np.array([hx[max(0, i - 4):i + 5].mean(0) for i in range(len(hx))])
    ring_xy = None
    if sid in HANG:                                                # where the AI ring hangs in each frame, smoothed
        pts = []
        for i, f in enumerate(src):
            tx, ty = Ms[i] @ np.array([HANG[sid][0], HANG[sid][1], 1.0])
            b_, g_, r_ = [f[..., j].astype(int) for j in range(3)]
            gold = ((r_ > 140) & (g_ > 95) & (b_ < g_ * 0.72) & (r_ > b_ + 50)).astype(np.uint8)
            y0, y1, x0, x1 = int(ty - 150), int(ty - 2), int(tx - 60), int(tx + 110)
            ys, xs = np.nonzero(gold[y0:y1, x0:x1])
            if len(ys) > 25:
                yb = ys.max(); pts.append((x0 + float(np.median(xs[ys >= yb - 4])), y0 + float(yb)))
            else: pts.append((np.nan, np.nan))
        pts = np.array(pts); ok = ~np.isnan(pts[:, 0])
        for j in range(2): pts[:, j] = np.interp(np.arange(len(pts)), np.nonzero(ok)[0], pts[ok, j])
        ring_xy = np.array([pts[max(0, i - 3):i + 4].mean(0) for i in range(len(pts))])
    out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{FW}x{FH}", "-r", "24",
                            "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", f"clips/{sid}_track.mp4"],
                           stdin=subprocess.PIPE)
    seam, gap = [], []; prev_go = None
    for i, f in enumerate(src):
        M = Ms[i].copy()
        if follow and sid == "S9": M[:, :2] = Ms[0][:, :2]                  # S9: the camera barely zooms; keep the frame-0 scale
        if follow:
            p0 = M @ np.array([x + w / 2, y + (h * 0.6 if sid == "S9" else 0), 1.0])
            if hang0 is None: hang0 = hx[0] - p0
            M[:, 2] += (hx[i] - p0) - hang0
        if ring_xy is not None:                                    # hang the charm 10 px of chain below the ring
            tx, ty = M @ np.array([HANG[sid][0], HANG[sid][1], 1.0]); rx, ry = ring_xy[i]
            M[0, 2] += rx - tx; M[1, 2] += max(0.0, (ry + 10) - ty) if ry + 10 > ty else (ry + 10) - ty
            _ring["p"] = (rx, ry)
        wp = cv2.warpAffine(plate, Ms[i], (FW, FH), borderMode=cv2.BORDER_REPLICATE)
        ws = cv2.warpAffine(still, M, (FW, FH), borderMode=cv2.BORDER_REPLICATE)
        wa = cv2.warpAffine(ov_a, M, (FW, FH)).astype(np.float32)[..., None] / 255
        # cover the AI charm: its colours near where the real one sits, grown a little, filled from the warped plate
        bx = cv2.boundingRect(cv2.warpAffine(diff, M, (FW, FH)))
        roi = np.zeros((FH, FW), np.uint8); X, Y, Wd, Hd = bx
        e = 0.35 if sid == 'S8' else 1.0               # S8: the AI charm sits where the real one does; spare the red stocking
        roi[max(0, Y - int(e * Hd)):Y + int((1 + e) * Hd), max(0, X - int(e * Wd)):X + int((1 + e) * Wd)] = 255
        L = sid == "S9"
        if L:                                                     # S9: loose colours, but only just around the charm body (not the bag's handle)
            near = np.zeros((FH, FW), np.uint8); near[int(Y + 0.25 * Hd):int(Y + 1.45 * Hd), max(0, int(X - 0.35 * Wd)):int(X + 1.35 * Wd)] = 255
            cov = cv2.dilate(charm_colours(f, True) & near, np.ones((9, 9), np.uint8))
        else:
            cov = cv2.dilate(charm_colours(f) & roi, np.ones((13, 13), np.uint8))
        if sid in BOX:                                            # near-still camera: cover the whole box with the clean plate
            l, r_, t, b_ = BOX[sid]; cov = np.zeros((FH, FW), np.uint8)
            cov[max(0, int(Y - t * Hd)):int(Y + b_ * Hd), max(0, int(X - l * Wd)):int(X + r_ * Wd)] = 255
            pb2, pg2, pr2 = [wp[..., j].astype(int) for j in range(3)]   # the plate only where it is the handbag's leather:
            # not leather = clearly curtain (blue-green), tree (green) or bright sofa/wall; everything else counts as the bag
            other = ((pg2 > pr2 + 5) | (pb2 > pr2 + 5) | ((pr2 > 190) & (pg2 > 175))).astype(np.uint8)
            other = cv2.morphologyEx(other, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            lea = (cv2.dilate(other, np.ones((3, 3), np.uint8)) == 0).astype(np.uint8)
            rest = cov.copy(); rest[lea > 0] = 0                       # curtain/tree/sofa in the box: only the AI's own colours,
            if not os.environ.get("TP_NOLEATHER"): cov[lea == 0] = 0  # painted from the live frame (no parallax smear)
            rest = cv2.dilate(charm_colours(f, True) & rest, np.ones((9, 9), np.uint8))
            if sid in HANG:                                       # never over the ring or the fingers above the charm
                hy = int((M @ np.array([HANG[sid][0], HANG[sid][1], 1.0]))[1]); cov[:hy + 2] = 0
                pb_, pg_, pr_ = [wp[..., j].astype(int) for j in range(3)]   # the plate still holds the still's hand: skip it
                skin = (pr_ > 140) & (pg_ > 95) & (pr_ - pb_ > 30) & (pr_ > pg_)
                cov[cv2.dilate(skin.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0] = 0
        if sid == "S8":                                           # never paint over the cuff's own white fur
            fi = f.astype(int); cov[(fi.min(2) > 160) & (fi.max(2) - fi.min(2) < 45)] = 0
        ring = cv2.dilate(cov, np.ones((15, 15), np.uint8)) & ~cov
        if sid in BOX:
            # local colour match: the frame-minus-plate difference around the box, spread smoothly inside it
            d = np.clip(f.astype(np.float32) - wp.astype(np.float32) + 128, 0, 255).astype(np.uint8)
            q = 4; ds = cv2.resize(d, (FW // q, FH // q), interpolation=cv2.INTER_AREA)
            fb, fg, fr = [f[..., j].astype(int) for j in range(3)]       # fingers next to the box must not tint it
            fskin = ((fr > 140) & (fg > 95) & (fr - fb > 30) & (fr > fg)).astype(np.uint8) * 255
            unk = cov | cv2.dilate(fskin, np.ones((9, 9), np.uint8)) | cv2.dilate(charm_colours(f), np.ones((9, 9), np.uint8))
            if sid in HANG: unk[:hy + 4] = 255                        # the AI ring and chain above the charm: not leather
            mq = cv2.dilate(cv2.resize(unk, (FW // q, FH // q), interpolation=cv2.INTER_NEAREST), np.ones((3, 3), np.uint8))
            ds = cv2.inpaint(ds, mq, 5, cv2.INPAINT_TELEA)
            off = cv2.GaussianBlur(cv2.resize(ds, (FW, FH), interpolation=cv2.INTER_LINEAR).astype(np.float32), (0, 0), 6) - 128
            fill = np.clip(wp.astype(np.float32) + off, 0, 255)
            if sid in HANG:                                       # where the plate shows the still's hand, use the live frame
                pb_, pg_, pr_ = [wp[..., j].astype(int) for j in range(3)]
                pskin = cv2.dilate(((pr_ > 140) & (pg_ > 95) & (pr_ - pb_ > 30) & (pr_ > pg_)).astype(np.uint8), np.ones((31, 31), np.uint8)) > 0
                fill[pskin] = f[pskin]
            if rest.any():
                inp = cv2.inpaint(f, rest, 7, cv2.INPAINT_TELEA).astype(np.float32)
                fill = np.where((rest > 0)[..., None], inp, fill); cov = np.maximum(cov, rest)
            cov = cv2.GaussianBlur(cov, (31, 31), 0)
        else:
            fill = cv2.inpaint(f, cov, 7, cv2.INPAINT_TELEA).astype(np.float32)   # from the frame itself: no misaligned plate
        ca = cv2.GaussianBlur(cov, (9, 9), 0).astype(np.float32)[..., None] / 255
        g = f.astype(np.float32) * (1 - ca) + fill * ca
        # QC (drift): the patch must move WITH the picture around it. Optical flow just inside its edge vs just outside,
        # per sector around it; a patch that slides against its surroundings (S7 curtain, v5) adds up px of slip.
        go = cv2.cvtColor(np.clip(g, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
        if prev_go is not None and cov.max() > 0:
            fl = cv2.calcOpticalFlowFarneback(prev_go, go, None, 0.5, 3, 21, 3, 5, 1.1, 0)
            cm = (cov > 127).astype(np.uint8); inner = cm & ~cv2.erode(cm, np.ones((15, 15), np.uint8))
            outer = cv2.dilate(cm, np.ones((15, 15), np.uint8)) & ~cm
            ys, xs = np.nonzero(cm); cy, cx = ys.mean(), xs.mean(); yy, xx = np.mgrid[0:FH, 0:FW]
            sect = ((np.arctan2(yy - cy, xx - cx) + np.pi) / (2 * np.pi) * 8).astype(int) % 8
            sl = []
            for k_ in range(8):
                ii, oo = (inner > 0) & (sect == k_), (outer > 0) & (sect == k_)
                if ii.sum() > 30 and oo.sum() > 30:
                    sl.append(np.linalg.norm(np.median(fl[ii], 0) - np.median(fl[oo], 0)))
            seam.append(sl)
        prev_go = go
        if sid == "S8":                                           # the real charm stays BEHIND this frame's own white cuff
            fi = f.astype(int); fur = ((fi.min(2) > 165) & (fi.max(2) - fi.min(2) < 40)).astype(np.uint8) * 255
            fur = cv2.GaussianBlur(cv2.morphologyEx(fur, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), (5, 5), 0)
            wa = wa * (1 - fur.astype(np.float32)[..., None] / 255)
        g = g * (1 - wa) + ws.astype(np.float32) * wa
        if sid in HANG:                                           # S4: the real charm always hangs from the ring the hand moves
            g = hang_chain(f, g, M, HANG[sid])
        if os.environ.get("DEBUG_FRAME") == str(i):
            cv2.imwrite("/tmp/claude-0/dbg_cov.png", (cov if cov.dtype == np.uint8 else cov).astype(np.uint8)); cv2.imwrite("/tmp/claude-0/dbg_fill.png", fill.astype(np.uint8)); cv2.imwrite("/tmp/claude-0/dbg_f.png", f)
        out.stdin.write(np.clip(g, 0, 255).astype(np.uint8).tobytes())
    out.stdin.close(); out.wait(); print(sid, "tracked", len(src), "frames -> clips/" + sid + "_track.mp4")
    K = max(len(x) for x in seam) if seam else 0                  # slip per sector, added up over a 0.5 s window
    S = np.array([x + [0.0] * (8 - len(x)) for x in seam]) if seam else np.zeros((0, 8))
    win = 12; slip = [float(S[max(0, i - win):i + 1].sum(0).max()) for i in range(len(S))] if len(S) else [0.0]
    qc = {"slip_px_per_half_s": [round(x, 2) for x in slip]}
    os.makedirs("qc", exist_ok=True); json.dump(qc, open(f"qc/track_{sid}.json", "w"))
    # the drift strip: product + a wide margin, every 0.2 s, 2x (grace/qc/strip.py); LOOK at it before any cut goes out
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "grace" / "qc")); import strip
    X0, Y0, W0, H0 = cv2.boundingRect(cv2.warpAffine(diff, Ms[0], (FW, FH)))
    box = [max(0, X0 - W0), max(0, Y0 - H0 // 2), min(FW, 3 * W0), min(FH, int(2.5 * H0))]
    strip.sheet(f"clips/{sid}_track.mp4", box, out=f"qc/strip_{sid}.jpg")
    print(f"TRACK_QC {sid}: patch slip max {max(slip):.1f} px per 0.5 s (info only, a number alone missed the v5 curtain smear)"
          f" -> LOOK at qc/strip_{sid}.jpg: attached to its holder, background moves with the camera, no smear/blocks/AI leftovers, no slide")


if __name__ == "__main__":
    run(sys.argv[1], "--follow" in sys.argv)
