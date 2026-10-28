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
LIVE = {"S7": (0.6, 1.3, 0.1, 1.9)}    # v8: S7 covers only the AI charm's own colours from the live frame (the still's
                                        # background patch stopped matching as the camera pushed in: pink blob, faint blocks)
TEMPORAL = set()                              # clean plate = per-pixel median of the clip's own frames where neither
                                              # the AI charm nor the hand covers it (S4 v6: the still's hand shadow stuck)
FIRST_PLATE = {"S4", "S8L"}                     # S8L: still camera, charm and hand move away: clean plate from its own frames
BOX = {"S4": (0.8, 1.9, 0.0, 3.5), "S9": (0.7, 1.4, 0.1, 2.4)}   # left, right, up, down, in charm widths/heights
# v11 (Ralph 2026-10-28 "Yes save rules": clips made with NO charm): S4N/S7N clips have no AI charm, so nothing is covered
NOCOVER = {"S4N", "S7N"}
STILL = {"S4N": "stills/S4.png", "S7N": "stills/S7.png"}     # the charm composite; the clip itself started from the charm-free plate
PLATE = {"S4N": "stills/S4N.png", "S7N": "stills/S7N.png", "S8L": "rooms/roomE_stocking2_crop.png", "S4": "stills/plate_S4.png", "S7": "stills/S7bg.png", "S8": "rooms/roomE_stocking2_crop.png", "S9": "stills/S9bg.png"}


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
# v8 (Grace 2026-10-28, 'she can tell it was pasted'): the real charm swings from where it hangs (S4: a pendulum driven
# by the hand's moves; S7/S9: a slow small sway), matches the footage's softness, light changes and grain, and takes
# a little of the room's colour on its edge. SOFT = blur in frame px (set with tools/hue_check.py --sharp).
PIVOT = {"S4N": (338, 749), "S7N": (537, 498), "S4": (338, 749), "S7": (537, 534), "S9": (529, 672)}
SWAY = {"S7": 0.8, "S9": 0.8, "S7N": 0.8}                 # idle sway, degrees; S4 is the pendulum
SOFT = {"S4N": 0.55, "S7N": 0.55, "S4": 0.55, "S7": 0.55, "S8": 0.35, "S8L": 0.35, "S9": 0.7}
HANG = {"S4": (338, 749), "S7": (537, 534), "S4N": (338, 749)}       # S7 v8: hang from the clip's own AI clasp (my drawn ring + patch smeared the handle)
GAP = {"S4": 13, "S7": 1, "S4N": 13}                            # S4 v8: hangs right under the AI's own ring and chain (none drawn)                         # px of chain between the ring's bottom and the charm's handles
STAY = set()                                      # tried on S4 2026-10-28: the charm then hung from nothing once the hand let go
FOLLOW_RING = {"S4", "S4N"}
AIBOX = {}                                        # S8L: the AI charm's box per frame (filled by the follow pre-pass)                     # still px where the charm's handles meet the chain (composite.swap hang)
_ring = {}


def arm_mask(f):
    """S8L: the hand and arm only = skin-coloured blobs that reach in from a frame edge (+ the French tips next to
    them). A plain skin colour test also hit the charm and the wooden mantel (see-through charm, 2026-10-28)."""
    b, g, r = [f[..., j].astype(int) for j in range(3)]
    sk = ((r > 120) & (g > 75) & (b > 55) & (r > g) & (g > b * 0.9) & (r - b > 25) & (g > r * 0.5)).astype(np.uint8)
    sk = cv2.morphologyEx(sk, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(sk); keep = np.zeros_like(sk)
    for k in range(1, n):
        X_, Y_, W_, H_ = st[k, :4]                                 # touches the top, left or right edge (the arm comes in there)
        if st[k, 4] > 1500 and (Y_ <= 3 or X_ <= 3 or X_ + W_ >= f.shape[1] - 3): keep[lab == k] = 1
    nails = (np.minimum(np.minimum(r, g), b) > 175) & (cv2.dilate(keep, np.ones((11, 11), np.uint8)) > 0)
    return (keep | nails.astype(np.uint8)).astype(np.uint8)


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
    still = cv2.imread(STILL.get(sid, f"stills/{sid}.png")); plate = cv2.imread(PLATE[sid])
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
            elif sid == "S8L":                                    # v8 (Ralph 2026-10-28: 'see the motion of putting into the
                b, g, r = [f[..., i].astype(int) for i in range(3)]   # stocking'): the AI charm's burgundy body as the hand moves it
                m = ((r > 45) & (r < 160) & (g < r * 0.45) & (b > g * 1.05) & (b < r * 0.8)).astype(np.uint8) * 255
                m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
                # the stocking's own shaded folds and loop match these colours too: take the blob nearest the charm's last spot
                if prev is None: prev = Ms[0] @ np.array([x + w / 2, y + h * 0.5, 1.0])
                n8, lab8, st8, cen8 = cv2.connectedComponentsWithStats(m); best8 = None
                for k8 in range(1, n8):
                    if st8[k8, 4] < 400: continue
                    d8 = np.hypot(cen8[k8][0] - prev[0], cen8[k8][1] - prev[1])
                    if d8 < 110 and (best8 is None or d8 < best8[0]): best8 = (d8, k8)
                m = (lab8 == best8[1]).astype(np.uint8) * 255 if best8 else np.zeros_like(m)
            else:
                m[:int(FH * 0.45)] = 0
            ys, xs = np.nonzero(m)
            if len(xs) > 200:
                hx.append((np.median(xs), np.median(ys))); prev = hx[-1]
            else: hx.append((np.nan, np.nan))
        hx = np.array(hx, float); good = ~np.isnan(hx[:, 0])
        for j in range(2): hx[:, j] = np.interp(np.arange(len(hx)), np.nonzero(good)[0], hx[good, j])
        hx = np.array([hx[max(0, i - 4):i + 5].mean(0) for i in range(len(hx))])
        if sid == "S8L":                                           # the true-size charm's handles go to the fingertips while the
            P0 = Ms[0] @ np.array([x + w / 2, y, 1.0]); tg = []; top0 = None   # hand holds it (the AI drew a bigger charm, so
            for i, f in enumerate(src):                            # following its centre left a gap under the fingers)
                b, g, r = [f[..., j].astype(int) for j in range(3)]
                m = ((r > 45) & (r < 160) & (g < r * 0.45) & (b > g * 1.05) & (b < r * 0.8)).astype(np.uint8)
                cxy = hx[i]; n8, lab8, st8, cen8 = cv2.connectedComponentsWithStats(m); bt = None
                for k8 in range(1, n8):
                    if st8[k8, 4] > 400 and np.hypot(cen8[k8][0] - cxy[0], cen8[k8][1] - cxy[1]) < 40: bt = st8[k8, 1]; AIBOX[i] = tuple(st8[k8, :4])
                if bt is None: tg.append((np.nan, np.nan)); continue
                if top0 is None: top0 = bt - P0[1]
                arm = arm_mask(f); ys, xs = np.nonzero(arm[:, max(0, int(cxy[0]) - 90):int(cxy[0]) + 90])
                tip = ys.max() if len(ys) else -1
                held = tip >= bt - 35
                tx_ = cxy[0] - (hx[0][0] - P0[0])
                if held:                                          # v9: the handle loop centred on the pinch and tucked up under
                    tipx = max(0, int(cxy[0]) - 90) + float(np.median(xs[ys >= tip - 3]))   # the fingers (the hand is drawn
                    tx_ = tipx + 8                                # in front); the overlay's handle top is 8 px left of its centre
                ty_ = (tip - 12) if held else bt - top0
                tg.append((tx_, ty_))
            tg = np.array(tg, float); ok8 = ~np.isnan(tg[:, 0])
            for j in range(2): tg[:, j] = np.interp(np.arange(len(tg)), np.nonzero(ok8)[0], tg[ok8, j])
            hx = np.array([tg[max(0, i - 2):i + 3].mean(0) for i in range(len(tg))])
            hx[:, 0] += hx[0][0] - P0[0] if False else 0
    ring_xy = None
    if sid in HANG:                                                # where the AI ring hangs in each frame, smoothed
        pts = []
        for i, f in enumerate(src):
            tx, ty = Ms[i] @ np.array([HANG[sid][0], HANG[sid][1], 1.0])
            b_, g_, r_ = [f[..., j].astype(int) for j in range(3)]
            gold = ((r_ > 140) & (g_ > 95) & (b_ < g_ * 0.72) & (r_ > b_ + 50)).astype(np.uint8)
            prev = next((p for p in reversed(pts) if not np.isnan(p[0])), None) if sid in FOLLOW_RING else None
            if prev is None:
                y0, y1, x0, x1 = int(ty - 150), int(ty - 2), int(tx - 60), int(tx + 110)
                ys, xs = np.nonzero(gold[y0:y1, x0:x1])
                if len(ys) > 25:
                    yb = ys.max(); pts.append((x0 + float(np.median(xs[ys >= yb - 4])), y0 + float(yb)))
                else: pts.append((np.nan, np.nan))
                continue
            # v8 (Ralph 2026-10-28, S4 '6-9s the bag does something weird'): when the hand lets go, the AI ring drops below the
            # charm's old top and the lowest-gold rule grabbed the rim clasp (charm jumped up, a chain drawn toward the hand).
            # Follow the same ring frame to frame: the gold blob nearest its last bottom point.
            px_, py_ = prev; y0, y1, x0, x1 = max(0, int(py_ - 70)), int(py_ + 45), max(0, int(px_ - 60)), int(px_ + 60)
            n_, lab, st, cen = cv2.connectedComponentsWithStats(gold[y0:y1, x0:x1])
            best = None
            for k in range(1, n_):
                if st[k, 4] < 20: continue
                ys, xs = np.nonzero(lab == k); yb = ys.max(); cand = (x0 + float(np.median(xs[ys >= yb - 4])), y0 + float(yb))
                dist = np.hypot(cand[0] - px_, cand[1] - py_)
                if best is None or dist < best[0]: best = (dist, cand)
            pts.append(best[1] if best is not None and best[0] < 60 else (np.nan, np.nan))
        pts = np.array(pts); ok = ~np.isnan(pts[:, 0])
        for j in range(2): pts[:, j] = np.interp(np.arange(len(pts)), np.nonzero(ok)[0], pts[ok, j])
        rk = 1 if sid == "S4N" else 3                              # S4N v11: a fast drop lagged with +-3 frames of smoothing
        ring_xy = np.array([pts[max(0, i - rk):i + rk + 1].mean(0) for i in range(len(pts))])
    n = len(src); fps = 24.0; th = np.zeros(n)
    if sid in HANG and ring_xy is not None:                        # pendulum: L = 6 cm, 1 m = ~1170 frame px here
        Lp, g_, c_ = 70.0, 9.8 * 1170, 5.0
        ax_ = np.gradient(np.gradient(ring_xy[:, 0])) * fps * fps; ax_ = np.convolve(ax_, np.ones(3) / 3, "same")
        t_, w_ = 0.0, 0.0
        for i in range(n):
            for _ in range(8):
                dt = 1 / fps / 8; acc = -(g_ / Lp) * np.sin(t_) - c_ * w_ - 0.4 * ax_[i] / Lp * np.cos(t_)
                w_ += acc * dt; t_ += w_ * dt
            th[i] = np.clip(np.degrees(t_), -4, 4)
    elif sid in SWAY:
        th = SWAY[sid] * np.sin(2 * np.pi * np.arange(n) / fps / 2.4)
    lum = []
    for i, f in enumerate(src):                                    # the light around the charm, frame by frame
        X0, Y0, W0, H0 = cv2.boundingRect(cv2.warpAffine(diff, Ms[i], (FW, FH)))
        y0, y1, x0, x1 = max(0, Y0 - H0 // 2), min(FH, Y0 + H0 + H0 // 2), max(0, X0 - W0 // 2), min(FW, X0 + W0 + W0 // 2)
        a_ = cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY).astype(np.float32); inner = np.zeros_like(a_, bool)
        inner[Y0 - y0:Y0 - y0 + H0, X0 - x0:X0 - x0 + W0] = True; lum.append(np.median(a_[~inner]) if (~inner).any() else 1)
    lum = np.array(lum, float); lum = np.convolve(np.pad(lum, 4, mode="edge"), np.ones(9) / 9, "valid")
    lr = np.clip(lum / max(lum[0], 1), 0.9, 1.1)
    rng = np.random.default_rng(11); boxes = []
    out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{FW}x{FH}", "-r", "24",
                            "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", f"clips/{sid}_track.mp4"],
                           stdin=subprocess.PIPE)
    fplate = None
    if sid in FIRST_PLATE:                                         # static camera: the clip's own first frame IS the clean plate
        fplate = src[0].copy()                                     # (same light as every later frame); where the charm sat at
        m0 = cv2.dilate(cv2.warpAffine(diff, Ms[0], (FW, FH)), np.ones((31, 31), np.uint8)) > 0   # frame 0, the old plate,
        if sid == "S9":                                            # + the AI charm and its scarf in frame 0 (bigger than ours)
            X9, Y9, W9, H9 = cv2.boundingRect(cv2.warpAffine(diff, Ms[0], (FW, FH))); near9 = np.zeros((FH, FW), np.uint8)
            near9[max(0, Y9 - H9 // 2):Y9 + 2 * H9, max(0, X9 - W9 // 2):X9 + 2 * W9] = 255
            f0 = src[0]; b9, g9, r9 = [f0[..., j].astype(int) for j in range(3)]
            pale9 = ((r9 > 150) & (b9 > 130) & ((b9 - g9 > 8) | (r9 - g9 > 15)) & (np.abs(r9 - b9) < 90)).astype(np.uint8) * 255
            m0 |= cv2.dilate((charm_colours(f0, True) | pale9) & near9, np.ones((21, 21), np.uint8)) > 0
        old = cv2.warpAffine(plate, Ms[0], (FW, FH), borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        rg = cv2.dilate(m0.astype(np.uint8), np.ones((25, 25), np.uint8)).astype(bool) & ~m0          # colour-matched to it
        if sid == "S9":                                            # v8: a smooth local light match + soft edge (a mean shift
            q = 4; dd = np.clip(fplate.astype(np.float32) - old + 128, 0, 255).astype(np.uint8)   # left a lighter block)
            dq = cv2.resize(dd, (FW // q, FH // q), interpolation=cv2.INTER_AREA)
            mq = cv2.dilate(cv2.resize(m0.astype(np.uint8) * 255, (FW // q, FH // q), interpolation=cv2.INTER_NEAREST), np.ones((3, 3), np.uint8))
            dq = cv2.inpaint(dq, mq, 9, cv2.INPAINT_TELEA)
            old += cv2.GaussianBlur(cv2.resize(dq, (FW, FH), interpolation=cv2.INTER_LINEAR).astype(np.float32), (0, 0), 8) - 128
            sm = cv2.GaussianBlur(m0.astype(np.float32), (0, 0), 6)[..., None]; sm = np.maximum(sm, m0[..., None].astype(np.float32) * 0)
            fplate = np.clip(old * sm + fplate.astype(np.float32) * (1 - sm), 0, 255).astype(np.uint8)
        else:
            old += fplate[rg].astype(np.float32).mean(0) - old[rg].mean(0)
            fplate[m0] = np.clip(old[m0], 0, 255).astype(np.uint8)
        # frame 0 still copies the still's own paint-out (a straight bag bottom); by 0.5 s the model has redrawn it,
        # so take the 0.5 s frame wherever the AI charm, scarf, chain and hand are not
        got = np.zeros(fplate.shape[:2], bool); out_p = fplate.astype(np.float32).copy()
        early = [12, 6, 18, 24, 30, 36, 48, 60, 72, 84, len(src) - 1]
        f0_ = src[0].astype(int); sofa0 = cv2.dilate((f0_.min(2) > 140).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        passes = [([], sofa0), ([len(src) - 1, len(src) - 6, 84, 72, 60, 48, 36, 30, 24, 18, 12, 6], ~sofa0)] if sid == "S4" else [(early, np.ones_like(sofa0))]
        # S4 v9: the bag's leather from the end frames first (hand gone, one light: mixed early frames left blotches left of
        # the charm); the sofa stays frame 0 = the approved still (later frames have the AI charm, its scarf tip and shadow on it)
        for order5, zone in passes:
          for k5 in order5:                                        # each pixel from the first frame in this order where it is clean
              if k5 >= len(src): continue
              f5 = src[k5]; fb5, fg5, fr5 = [f5[..., j].astype(int) for j in range(3)]
              pale5 = (fr5 > 175) & (fg5 > 150) & (fb5 > 150) & ((fb5 - fg5 > 8) | (fr5 - fg5 > 15))
              skin5 = (fr5 > 170) & (fg5 > 115) & (fb5 > 85) & (fr5 - fb5 > 30) & (fr5 > fg5)
              dark5 = (fr5 < 50) & (fg5 < 32) & (fb5 < 40)
              bad5 = cv2.dilate(charm_colours(f5, True) | (pale5 | skin5 | dark5).astype(np.uint8) * 255, np.ones((31, 31), np.uint8)) > 0
              take = ~bad5 & ~got & zone; out_p[take] = f5[take]; got |= take
        soft = cv2.GaussianBlur(got.astype(np.float32), (0, 0), 3)[..., None]
        fplate = np.clip(out_p * soft + fplate * (1 - soft), 0, 255).astype(np.uint8)
        med = cv2.medianBlur(fplate, 21); spk = np.abs(fplate.astype(int) - med.astype(int)).max(2) > 26   # thin AI chain bits
        spk = cv2.dilate(spk.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        if sid == "S8L": spk[:] = False                            # keep the pine needles sharp
        fplate[spk] = med[spk]; print(sid, "plate: clean in some frame for", round(float(got.mean()) * 100, 1), "% of pixels")
        cv2.imwrite(f"qc/plate_{sid}_first.png", fplate)
    if sid in TEMPORAL:                                            # camera is static here: build the plate in frame space
        acc = []; okm = []
        for f in src[::3]:
            fb4, fg4, fr4 = [f[..., j].astype(int) for j in range(3)]
            pale = (fr4 > 175) & (fg4 > 150) & (fb4 > 150) & ((fb4 - fg4 > 8) | (fr4 - fg4 > 15))
            skin4 = (fr4 > 120) & (fg4 > 70) & (fr4 - fb4 > 25) & (fr4 > fg4) & (fr4 - fg4 < 90)
            vdark = (fr4 < 50) & (fg4 < 32) & (fb4 < 40)                                   # the AI charm's darkest inside
            bad = cv2.dilate(charm_colours(f, True) | (pale | skin4 | vdark).astype(np.uint8) * 255, np.ones((21, 21), np.uint8)) > 0
            acc.append(f); okm.append(~bad)
        A = np.array(acc, np.float32); O = np.array(okm)[..., None]
        A[~np.broadcast_to(O, A.shape)] = np.nan
        tp = np.nanmedian(A, 0); miss = np.isnan(tp[..., 0])
        base = cv2.resize(plate, (FW, FH)) if plate.shape[:2] != (FH, FW) else plate
        fallback = cv2.warpAffine(plate, Ms[0], (FW, FH), borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        tp[miss] = fallback[miss]; tplate = np.clip(tp, 0, 255).astype(np.uint8)
        mm = cv2.dilate(miss.astype(np.uint8) * 255, np.ones((7, 7), np.uint8))          # never seen clean: paint it from the
        tplate = cv2.inpaint(tplate, mm, 11, cv2.INPAINT_TELEA)                          # clip's own clean surroundings
        cv2.imwrite(f"qc/plate_{sid}_temporal.png", tplate); print(sid, "temporal plate:", round(float(miss.mean()) * 100, 1), "% from the old plate")
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
            if sid not in STAY:                                   # v8 (Ralph 2026-10-28, '6-9s the bag does something weird'):
                gp = GAP.get(sid, 10); M[0, 2] += rx - tx; M[1, 2] += (ry + gp) - ty   # S4's AI hand
                # LIFTS the ring; pinning the charm under it yanked the charm up. STAY: the charm hangs where it is, the chain stretches
            _ring["p"] = (rx, ry)
        if sid in PIVOT and th[i]:                                 # swing about where it hangs (in still px)
            px_, py_ = PIVOT[sid]; R = cv2.getRotationMatrix2D((float(px_), float(py_)), float(th[i]), 1.0)
            Mr = M @ np.vstack([R, [0, 0, 1]])
        else: Mr = M
        wp = fplate if fplate is not None else tplate if sid in TEMPORAL else cv2.warpAffine(plate, Ms[i], (FW, FH), borderMode=cv2.BORDER_REPLICATE)
        ws = cv2.warpAffine(still, Mr, (FW, FH), borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        wa = cv2.GaussianBlur(cv2.warpAffine(ov_a, Mr, (FW, FH)).astype(np.float32), (0, 0), 0.6)[..., None] / 255
        ws = cv2.GaussianBlur(ws, (0, 0), SOFT.get(sid, 1.0)) * lr[i]                  # the footage's softness and light
        ys_, xs_ = np.nonzero(wa[..., 0] > 0.5); boxes.append([int(xs_.min()), int(ys_.min()), int(xs_.max()), int(ys_.max())] if len(xs_) else None)
        # cover the AI charm: its colours near where the real one sits, grown a little, filled from the warped plate
        bx = cv2.boundingRect(cv2.warpAffine(diff, M, (FW, FH)))
        roi = np.zeros((FH, FW), np.uint8); X, Y, Wd, Hd = bx
        e = 0.35 if sid in ('S8', 'S8L') else 1.0               # S8: the AI charm sits where the real one does; spare the red stocking
        roi[max(0, Y - int(e * Hd)):Y + int((1 + e) * Hd), max(0, X - int(e * Wd)):X + int((1 + e) * Wd)] = 255
        L = sid == "S9"
        if L:                                                     # S9: loose colours, but only just around the charm body (not the bag's handle)
            near = np.zeros((FH, FW), np.uint8); near[int(Y + 0.25 * Hd):int(Y + 1.45 * Hd), max(0, int(X - 0.35 * Wd)):int(X + 1.35 * Wd)] = 255
            cov = cv2.dilate(charm_colours(f, True) & near, np.ones((9, 9), np.uint8))
        elif sid in LIVE:                                         # cover only the AI charm's own colours, painted from the live
            l, r_, t, b_ = LIVE[sid]                              # frame (default fill below), so real shadows come and go with
            box2 = np.zeros((FH, FW), np.uint8)                   # the hand (S4 v6: the plate kept the still's hand shadow)
            box2[max(0, int(Y - t * Hd)):int(Y + b_ * Hd), max(0, int(X - l * Wd)):int(X + r_ * Wd)] = 255
            hy2 = int((M @ np.array([HANG[sid][0], HANG[sid][1], 1.0]))[1]) if sid in HANG else 0; box2[:hy2 + 2] = 0
            fb3, fg3, fr3 = [f[..., j].astype(int) for j in range(3)]
            pale = (fr3 > 175) & (fg3 > 150) & (fb3 > 150) & ((fb3 - fg3 > 8) | (fr3 - fg3 > 15))     # the pale pink/blue scarf
            if sid == "S7": pale = (fr3 > 175) & (fg3 > 140) & (fb3 > 150) & ((fb3 - fg3 > 12) | (fr3 - fg3 > 25))   # not the cream sofa
            if sid == "S7":                                       # + the AI scarf's light grey tail on the bag front (below the rim)
                lt = (np.minimum(np.minimum(fr3, fg3), fb3) > 125); lt[:hy2 + 30] = False; pale = pale | lt
            cov = cv2.dilate((charm_colours(f, sid != "S7") | (pale.astype(np.uint8) * 255)) & box2, np.ones((15, 15), np.uint8))   # S7: strict
            # colours (loose ones match the handbag's own dark rim)
        else:
            cov = cv2.dilate(charm_colours(f, sid == "S8") & roi, np.ones((13, 13), np.uint8))   # S8 v8: loose, the AI charm's dark edge peeked out late
        if sid in BOX:                                            # near-still camera: cover the whole box with the clean plate
            l, r_, t, b_ = BOX[sid]; cov = np.zeros((FH, FW), np.uint8)
            cov[max(0, int(Y - t * Hd)):int(Y + b_ * Hd), max(0, int(X - l * Wd)):int(X + r_ * Wd)] = 255
            pb2, pg2, pr2 = [wp[..., j].astype(int) for j in range(3)]   # the plate only where it is the handbag's leather:
            # not leather = clearly curtain (blue-green), tree (green) or bright sofa/wall; everything else counts as the bag
            other = ((pg2 > pr2 + 5) | (pb2 > pr2 + 5) | ((pr2 > 190) & (pg2 > 175))).astype(np.uint8)
            other = cv2.morphologyEx(other, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            lea = (cv2.dilate(other, np.ones((3, 3), np.uint8)) == 0).astype(np.uint8)
            rest = cov.copy(); rest[lea > 0] = 0                       # curtain/tree/sofa in the box: only the AI's own colours,
            if not os.environ.get("TP_NOLEATHER") and fplate is None: cov[lea == 0] = 0  # live frame there (no parallax smear);
            if fplate is not None: rest[:] = 0                         # a static first-frame plate lines up everywhere
            if sid == "S9":                                       # v8: + the AI scarf's pale parts over the bag edge
                fb9, fg9, fr9 = [f[..., j].astype(int) for j in range(3)]
                pale9 = ((fr9 > 150) & (fb9 > 130) & ((fb9 - fg9 > 8) | (fr9 - fg9 > 15)) & (np.abs(fr9 - fb9) < 90)).astype(np.uint8) * 255
                rest = cv2.dilate((charm_colours(f, True) | pale9) & rest, np.ones((13, 13), np.uint8))
            else:
                rest = cv2.dilate(charm_colours(f, True) & rest, np.ones((9, 9), np.uint8))
            if sid == "S4":                                       # v9: cover only near the AI charm and its scarf (wide margin):
                fb4, fg4, fr4 = [f[..., j].astype(int) for j in range(3)]   # the whole box swapped in the plate's bag edge,
                sc4 = ((fr4 > 150) & (fb4 > 130) & ((fb4 - fg4 > 8) | (fr4 - fg4 > 18))).astype(np.uint8) * 255   # which the AI
                boxm = cov.copy()
                cov &= cv2.dilate(charm_colours(f, True) | sc4, np.ones((51, 51), np.uint8))   # redraws (the bag changed shape)
                lf = f.astype(np.float32).mean(2); lp = wp.astype(np.float32).mean(2)          # + the AI charm's shadow on the
                shd = ((lp - lf) > 14) & sofa0 & (boxm > 0)                                     # sofa: darker than the clean plate
                cov |= (cv2.dilate(shd.astype(np.uint8), np.ones((15, 15), np.uint8)) * 255)
            if sid in HANG:                                       # never over the ring or the fingers above the charm
                hy = int((M @ np.array([HANG[sid][0], HANG[sid][1], 1.0]))[1]); cov[:hy + 2] = 0
                pb_, pg_, pr_ = [wp[..., j].astype(int) for j in range(3)]   # the plate still holds the still's hand: skip it
                skin = (pr_ > 170) & (pg_ > 115) & (pb_ > 85) & (pr_ - pb_ > 30) & (pr_ > pg_)   # real skin, not lit brown leather
                cov[cv2.dilate(skin.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0] = 0
        if sid == "S8":                                           # never paint over the cuff's own white fur
            fi = f.astype(int); cov[(fi.min(2) > 160) & (fi.max(2) - fi.min(2) < 45)] = 0
        if sid in NOCOVER: cov = np.zeros((FH, FW), np.uint8)    # no AI charm in this clip: nothing to hide
        ring = cv2.dilate(cov, np.ones((15, 15), np.uint8)) & ~cov
        if sid in BOX:
            # local colour match: the frame-minus-plate difference around the box, spread smoothly inside it
            d = np.clip(f.astype(np.float32) - wp.astype(np.float32) + 128, 0, 255).astype(np.uint8)
            q = 4; ds = cv2.resize(d, (FW // q, FH // q), interpolation=cv2.INTER_AREA)
            fb, fg, fr = [f[..., j].astype(int) for j in range(3)]       # fingers next to the box must not tint it
            fskin = ((fr > 170) & (fg > 115) & (fb > 85) & (fr - fb > 30) & (fr > fg)).astype(np.uint8) * 255
            unk = cov | cv2.dilate(fskin, np.ones((9, 9), np.uint8)) | cv2.dilate(charm_colours(f), np.ones((9, 9), np.uint8))
            if sid in HANG: unk[:hy + 4] = 255                        # the AI ring and chain above the charm: not leather
            mq = cv2.dilate(cv2.resize(unk, (FW // q, FH // q), interpolation=cv2.INTER_NEAREST), np.ones((3, 3), np.uint8))
            ds = cv2.inpaint(ds, mq, 5, cv2.INPAINT_TELEA)
            off = cv2.GaussianBlur(cv2.resize(ds, (FW, FH), interpolation=cv2.INTER_LINEAR).astype(np.float32), (0, 0), 6) - 128
            if fplate is not None: off = 0.0                       # the first-frame plate already has this clip's light
            if fplate is not None and sid == "S4":                 # v9 (Ralph: arrow left of the charm): the hand's shadow changes
                band = (cv2.dilate(cov, np.ones((41, 41), np.uint8)) > 0) & (cov == 0)   # the light frame to frame; a smooth
                bad_ = cv2.dilate(fskin | charm_colours(f, True), np.ones((15, 15), np.uint8)) > 0   # plane fitted on the leather
                if sid in HANG: band[:hy + 4] = False                                    # around the patch matches it
                band &= ~bad_
                ys_, xs_ = np.nonzero(band)
                if len(ys_) > 300:
                    A_ = np.c_[np.ones(len(xs_)), xs_ / FW, ys_ / FH]; dlt = f[ys_, xs_].astype(np.float32) - wp[ys_, xs_].astype(np.float32)
                    keep_ = np.all(np.abs(dlt - np.median(dlt, 0)) < 25, 1)
                    co, *_ = np.linalg.lstsq(A_[keep_], dlt[keep_], rcond=None)
                    yy_, xx_ = np.mgrid[0:FH, 0:FW]; off = (co[0] + co[1] * (xx_ / FW)[..., None] + co[2] * (yy_ / FH)[..., None]).astype(np.float32)
            fill = np.clip(wp.astype(np.float32) + off, 0, 255)
            if sid in HANG:                                       # where the plate shows the still's hand, use the live frame
                pb_, pg_, pr_ = [wp[..., j].astype(int) for j in range(3)]
                pskin = cv2.dilate(((pr_ > 170) & (pg_ > 115) & (pb_ > 85) & (pr_ - pb_ > 30) & (pr_ > pg_)).astype(np.uint8), np.ones((31, 31), np.uint8)) > 0
                fill[pskin] = f[pskin]
            if rest.any():
                inp = fill.copy() if sid == "S9" else cv2.inpaint(f, rest, 7, cv2.INPAINT_TELEA).astype(np.float32)   # S9 v8: the real
                # photo behind the AI scarf (locked camera), light-matched; inpainting smeared the bag edge
                fill = np.where((rest > 0)[..., None], inp, fill); cov = np.maximum(cov, rest)
            restm = rest.copy() if rest.any() else None
            cov = cv2.GaussianBlur(cov, (61, 61) if sid == "S4" else (31, 31), 0)   # S4 v9: wider soft edge (a faint line showed)
            if sid == "S7" and fplate is None:                    # v8: the soft edge stays on the leather (it left a faint
                ls = cv2.GaussianBlur(lea.astype(np.float32), (0, 0), 2)          # block on the curtain)
                cov = cov.astype(np.float32) * ls
                if restm is not None: cov = np.maximum(cov, cv2.GaussianBlur(restm, (9, 9), 0).astype(np.float32))
                cov = np.clip(cov, 0, 255).astype(np.uint8)
        elif sid in ("S8", "S8L"):                                # v8: the AI charm is bigger than the real one; its handle
            top = np.zeros((FH, FW), np.uint8)                    # top and scarf left a pale ghost when inpainted. Cover a taller
            rt, dn = (2.4, 1.1) if sid == "S8L" else (1.4, 0.6)   # S8L: the AI scarf ribbons trail further right and down
            top[max(0, Y - int(0.7 * Hd)):Y + int(dn * Hd), max(0, X - int(0.4 * Wd)):X + int(rt * Wd)] = 255   # area and fill it
            fb3, fg3, fr3 = [f[..., j].astype(int) for j in range(3)]                                 # from the real photo,
            pale = (fr3 > 150) & (fb3 > 130) & ((fb3 - fg3 > 8) | (fr3 - fg3 > 15)) & (np.abs(fr3 - fb3) < 90)   # camera-tracked
            kd = 21 if sid == "S8L" else 15
            cov = np.maximum(cov, cv2.dilate((charm_colours(f, True) | pale.astype(np.uint8) * 255) & top, np.ones((kd, kd), np.uint8)))
            fi = f.astype(int); fur9 = (fi.min(2) > 160) & (fi.max(2) - fi.min(2) < 45)   # S8L: the AI's pale
            if sid == "S8L": fur9 &= ~(((fi[..., 2] - fi[..., 1]) > 14) | ((fi[..., 0] - fi[..., 1]) > 26))   # fur: r-g <= 7, b-g <= 23 (measured)
            cov[fur9] = 0
            if sid == "S8L":                                      # pink ribbon passed the looser fur test and stayed as a ghost
                ab = AIBOX.get(i)                                 # v9 (Ralph: 'still have drift or misalignment'): the AI drew a
                if ab is not None and fplate is not None:         # bigger charm; its dark handles and scarf showed between the
                    ax0, ay0 = min(ab[0], X) - 22, min(ab[1], Y) - 45   # fingertips and ours. Still camera + clean plate:
                    ax1, ay1 = max(ab[0] + ab[2], X + Wd) + 22, max(ab[1] + ab[3], Y + Hd) + 12   # cover the AI charm's whole
                    cov[max(0, ay0):ay1, max(0, ax0):ax1] = 255   # box and the gap above it
                    fp = fplate.astype(int); cuff = (fp.min(2) > 160) & (fp.max(2) - fp.min(2) < 45)   # the cuff from the clean plate:
                    cuff = cv2.erode(cuff.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0     # the AI's white tissue also passed
                    cov[fur9 & cuff] = 0                          # the fur test. Keep the live fur only where the cuff really is
                cov[cv2.dilate(arm_mask(f), np.ones((3, 3), np.uint8)) > 0] = 0
            wpl = fplate.astype(np.float32) if fplate is not None else cv2.warpAffine(plate, Ms[i], (FW, FH), borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
            ring2 = (cv2.dilate(cov, np.ones((21, 21), np.uint8)) > 0) & (cov == 0)
            fill = wpl + (f[ring2].astype(np.float32).mean(0) - wpl[ring2].mean(0) if ring2.any() else 0)
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
        if sid == "S8L":                                          # fingers (and their French tips) stay in front of the charm
            fb7, fg7, fr7 = [f[..., j].astype(int) for j in range(3)]
            hand = cv2.GaussianBlur((arm_mask(f) * 255).astype(np.uint8), (5, 5), 0).astype(np.float32)[..., None] / 255
            ais = (fr7 > 45) & (fr7 < 160) & (fg7 < fr7 * 0.45) & (fb7 > fg7 * 1.05) & (fb7 < fr7 * 0.8)
            ys_, xs_ = np.nonzero(ais & (cv2.warpAffine(diff, M, (FW, FH)) > 0) | ais & (roi > 0))
            ai_bot = ys_.max() if len(ys_) else 0
            ys2, _ = np.nonzero(wa[..., 0] > 0.5); our_bot = ys2.max() if len(ys2) else 0
            if our_bot > ai_bot + 6:                              # the AI charm's bottom is hidden: it is inside the cuff
                fi = f.astype(int); fur = ((fi.min(2) > 165) & (fi.max(2) - fi.min(2) < 40)).astype(np.uint8) * 255
                fur = cv2.GaussianBlur(cv2.morphologyEx(fur, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), (5, 5), 0)
                wa = wa * (1 - fur.astype(np.float32)[..., None] / 255)
            wa = wa * (1 - hand)
        if sid == "S8":                                           # the real charm stays BEHIND this frame's own white cuff
            fi = f.astype(int); fur = ((fi.min(2) > 165) & (fi.max(2) - fi.min(2) < 40)).astype(np.uint8) * 255
            fur = cv2.GaussianBlur(cv2.morphologyEx(fur, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), (5, 5), 0)
            wa = wa * (1 - fur.astype(np.float32)[..., None] / 255)
        edge = np.clip(4 * wa * (1 - wa), 0, 1) * 0.3                # a little of the room's colour on its edge
        ws = ws * (1 - edge) + cv2.GaussianBlur(g, (0, 0), 5) * edge
        fl_ = f.astype(np.float32); nz = float(np.std((fl_ - cv2.GaussianBlur(fl_, (0, 0), 1.5))[wa[..., 0] > 0.5])) if (wa > 0.5).any() else 2.0
        ws = ws + rng.normal(0, min(max(nz * 0.4, 0.8), 3.0), ws.shape[:2])[..., None]   # the footage's grain
        g = g * (1 - wa) + ws * wa
        if sid in HANG:                                           # S4: the real charm always hangs from the ring the hand moves
            g = hang_chain(f, g, M, HANG[sid])
        if os.environ.get("DEBUG_FRAME") == str(i):
            cv2.imwrite("/tmp/claude-0/dbg_cov.png", (cov if cov.dtype == np.uint8 else cov).astype(np.uint8)); cv2.imwrite("/tmp/claude-0/dbg_fill.png", fill.astype(np.uint8)); cv2.imwrite("/tmp/claude-0/dbg_f.png", f)
        out.stdin.write(np.clip(g, 0, 255).astype(np.uint8).tobytes())
    out.stdin.close(); out.wait(); print(sid, "tracked", len(src), "frames -> clips/" + sid + "_track.mp4")
    K = max(len(x) for x in seam) if seam else 0                  # slip per sector, added up over a 0.5 s window
    S = np.array([x + [0.0] * (8 - len(x)) for x in seam]) if seam else np.zeros((0, 8))
    win = 12; slip = [float(S[max(0, i - win):i + 1].sum(0).max()) for i in range(len(S))] if len(S) else [0.0]
    qc = {"slip_px_per_half_s": [round(x, 2) for x in slip], "charm_box": boxes, "sway_deg": [round(float(x), 2) for x in th]}
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
