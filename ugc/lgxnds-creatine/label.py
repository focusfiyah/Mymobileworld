"""Paste the REAL LGXNDS label (refs/crop_tub.png) over the AI tub's label (free). SIFT + RANSAC homography, label band only
(lid and anything above/below stay AI), shading carried over from the AI frame so it sits in the scene's light.

  python3 label.py still IN OUT        writes OUT + OUT_check.jpg (mask outline)
  python3 label.py video IN OUT [--ref N]   every frame, one homography fitted on frame N (locked camera)
  python3 label.py video IN OUT --track     tub or camera moves: per-frame fit, corners smoothed over 9 frames
  python3 label.py video IN OUT --flow      better: fit frame 0, then follow the tub frame to frame
                                            [--deshade] remove the pale box behind the print; [--wordmark] also the vertical LGXNDS; [--rigid] fast tub, [--from N] anchor + start at frame N (drops earlier frames)
"""
import subprocess, sys
import cv2, numpy as np

REAL = cv2.imread("refs/crop_tub.png")
BAND = np.zeros(REAL.shape[:2], np.uint8); cv2.rectangle(BAND, (22, 158), (678, 598), 255, -1)
_g = cv2.cvtColor(REAL, cv2.COLOR_BGR2HSV)
INK = cv2.dilate((((_g[..., 2] < 200) | (_g[..., 1] > 50)) & (BAND > 0)).astype(np.uint8) * 255, np.ones((11, 11), np.uint8))
CORE = np.zeros(REAL.shape[:2], np.uint8); cv2.rectangle(CORE, (188, 196), (560, 588), 255, -1)
_g = cv2.cvtColor(REAL, cv2.COLOR_BGR2HSV)  # right of x=560 only the print itself (the AI tub ends sooner than the real one)
_ink = cv2.dilate((((_g[..., 2] < 150) | (_g[..., 1] > 60))).astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
_ink[:, :560] = 0; _ink[:196] = 0; _ink[588:] = 0; _ink[:, 672:] = 0
CORE = np.maximum(CORE, _ink)  # printed block right of the
if "--wordmark" in sys.argv:   # 2026-10-19 (S3 camera arc): the AI's vertical LGXNDS turned into "LGXNDD"; paste the real one too
    cv2.rectangle(CORE, (136, 190), (190, 590), 255, -1)
# stripes/wordmark: the homography fits it well; the AI's stripes + vertical LGXNDS stay (they render right, the cylinder edges don't fit)
# 2026-10-05 (Ralph: "how come the product quality did not come out the same"): print from the 1223 px listing packshot
# (refs/crop_tub_hi.png, exactly crop_tub.png x1.588) instead of the 700 px phone-screenshot crop: masks are drawn in the old
# coordinates above and scaled up here.
REAL = cv2.imread("refs/crop_tub_hi.png"); _sz = (REAL.shape[1], REAL.shape[0])
BAND = cv2.resize(BAND, _sz, interpolation=cv2.INTER_NEAREST); CORE = cv2.resize(CORE, _sz, interpolation=cv2.INTER_NEAREST)
REAL_AA = cv2.GaussianBlur(REAL, (0, 0), 0.8)   # anti-alias before the ~2x downscale into a 720p frame
sift = cv2.SIFT_create(6000)
kR, dR = sift.detectAndCompute(cv2.cvtColor(REAL, cv2.COLOR_BGR2GRAY), BAND)


def fit(img):
    k, d = sift.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
    m = [a for a, b in cv2.BFMatcher().knnMatch(dR, d, k=2) if a.distance < 0.75 * b.distance]
    if len(m) < 25: return None, len(m)
    H, inl = cv2.findHomography(np.float32([kR[x.queryIdx].pt for x in m]), np.float32([k[x.trainIdx].pt for x in m]), cv2.RANSAC, 4.0)
    return (H if H is not None and inl.sum() >= 20 else None), int(inl.sum()) if inl is not None else 0


_EDGE = {}


def deshade(img, H):
    # 2026-10-19: Kling/Seedance re-render the pasted still's label area as a paler rectangle. Bring the paper level inside
    # the print box back to the tub's own shading (per column, interpolated between just above and just below the box)
    # BEFORE pasting. Only darkens (gain <= 1.05).
    h, w = img.shape[:2]
    m = cv2.warpPerspective(CORE, H, (w, h)) > 0
    ys, xs = np.where(m); y0, y1 = ys.min(), ys.max()
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    P = cv2.GaussianBlur(cv2.medianBlur(cv2.morphologyEx(g, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8)), 21).astype(np.float32), (0, 0), 4)
    a = P[max(0, y0 - 14)]; b = P[min(h - 1, y1 + 14)]   # paper level just above and below the box, per column
    t = np.linspace(0, 1, y1 - y0 + 1)[:, None]; tgt = P.copy(); tgt[y0:y1 + 1] = a * (1 - t) + b * t
    gain = np.clip(tgt / (P + 1), 0.7, 1.05)
    mm = cv2.GaussianBlur(cv2.dilate(m.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(np.float32), (0, 0), 3)
    gain = 1 + (gain - 1) * mm
    return np.clip(img.astype(np.float32) * gain[..., None], 0, 255).astype(np.uint8)


DESHADE = "--deshade" in sys.argv


def geom(img, H):
    """label-band mask for this frame: CORE warped, eroded, cut at the tub's right edge (no occluders yet)"""
    h, w = img.shape[:2]
    m = cv2.warpPerspective(CORE, H, (w, h))
    m = cv2.erode(m, np.ones((7, 7), np.uint8)).astype(np.float32) / 255
    # 2026-10-19 (v2 still): the real print ran past the AI tub's right edge. Find that edge (strongest vertical line near the
    # mask's right end, inside the mask's rows) once per homography and keep the paste 4 px left of it.
    key = H.tobytes()
    if key not in _EDGE:
        ys, xs = np.where(m > 0.5); y0, y1, xr = ys.min(), ys.max(), xs.max()
        g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.5)
        med = np.median(np.abs(np.diff(g[y0:y1, :], axis=1)), 0)   # the tub edge is a line on EVERY row; letter edges are not
        lo, hi = max(0, xr - 80), min(len(med), xr + 30)
        hits = [x for x in range(lo, hi) if med[x] > 2.5]
        _EDGE[key] = hits[-1] if hits else w
    m[:, max(0, _EDGE[key] - 4):] = 0
    # 2026-10-19: the tub's bottom curves in, so per row also stop at that row's own edge (strongest vertical step within
    # 40 px left of the global edge, gradient smoothed down the rows) or the print hangs past the rounded bottom corner
    if key + b"rows" not in _EDGE:
        g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.5)
        gx = cv2.GaussianBlur(np.abs(np.diff(g, axis=1)), (1, 0), sigmaX=0.1, sigmaY=6)
        e = _EDGE[key]; lo = max(0, e - 40); rows = {}
        ys = np.where(m.max(1) > 0.5)[0]; y0 = ys.max() - int(0.12 * (ys.max() - ys.min()))   # bottom 12% only: letters above
        for y in ys[ys >= y0]:
            seg = gx[y, lo:e + 2]; rows[y] = lo + int(seg.argmax()) if seg.max() > 2.0 else e
        _EDGE[key + b"rows"] = rows
    for y, x in _EDGE[key + b"rows"].items():
        m[y, max(0, x - 4):] = 0
    return m


LMASK = None   # --flow: frame 0's trimmed mask in label space, carried with the tub (per-frame edge trims fail as it turns)


def paste(img, H):
    if DESHADE: img = deshade(img, H)
    h, w = img.shape[:2]
    real = cv2.warpPerspective(REAL_AA, H, (w, h), flags=cv2.INTER_LANCZOS4)
    m = geom(img, H) if LMASK is None else cv2.warpPerspective(LMASK, H, (w, h))
    dark = cv2.morphologyEx((cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[..., 2] < 70).astype(np.uint8), cv2.MORPH_OPEN, np.ones((31, 31), np.uint8))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   # the hand always stays in front of the label
    skin = ((hsv[..., 0] < 25) & (hsv[..., 1] > 60) & (hsv[..., 2] > 40) & (hsv[..., 2] < 200)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = m * (1 - cv2.dilate(skin, np.ones((7, 7), np.uint8)).astype(np.float32))
    m = m * (1 - cv2.dilate(dark, np.ones((9, 9), np.uint8)).astype(np.float32))   # big dark occluders (the bag) stay in front
    m = cv2.GaussianBlur(m, (0, 0), 3.0)[..., None]
    # light: paper brightness of the AI tub vs the real print, text removed by a median filter, so the curved tub's shading
    # (darker toward its edges) carries onto the pasted print and no pale box shows at the tub's sides
    # 2026-10-19: close (remove dark ink) BEFORE the median, or the AI's big letters leave a grey ghost glow around the real print
    pap = lambda x: cv2.GaussianBlur(cv2.medianBlur(cv2.morphologyEx(cv2.cvtColor(x, cv2.COLOR_BGR2GRAY), cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8)), 21).astype(np.float32), (0, 0), 6)
    lum = np.clip(pap(img) / (pap(real) + 1), 0.6, 1.25)[..., None]
    out = real.astype(np.float32) * lum
    out = np.clip(out, 0, 255)
    return (out * m + img.astype(np.float32) * (1 - m)).astype(np.uint8), m


if __name__ == "__main__":
    mode, src, dst = sys.argv[1:4]
    if mode == "still":
        img = cv2.imread(src); H, n = fit(img); print("inliers", n)
        if H is None: sys.exit("no fit")
        out, m = paste(img, H); cv2.imwrite(dst, out)
        chk = out.copy(); cs, _ = cv2.findContours((m[..., 0] > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(chk, cs, -1, (0, 0, 255), 2); cv2.imwrite(dst.rsplit(".", 1)[0] + "_check.jpg", chk)
    else:
        cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
        while True:
            ok, f = cap.read()
            if not ok: break
            frames.append(f)
        h, w = frames[0].shape[:2]; lastH = None; bad = 0; a0 = None
        C = np.float32([[22, 158], [678, 158], [678, 598], [22, 598]]).reshape(-1, 1, 2)
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                              "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
        # ONE homography per clip (locked camera, tub never moves): per-frame SIFT fits jitter by up to 25 px and the print
        # shimmers. Fit on the frame given by --ref (default 0 = the approved still).
        ref = int(sys.argv[sys.argv.index("--ref") + 1]) if "--ref" in sys.argv else 0
        if "--flow" in sys.argv:
            # 2026-10-19: fitting each frame to the real print fails once the AI print drifts (wrong scale, doubled letters).
            # Instead fit frame 0 (the pasted still, exact) and follow the TUB frame to frame: SIFT matches between
            # consecutive frames inside the label band (hand and dark bag masked out), RANSAC homography, chained.
            st = int(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else 0   # start frame (anchor)
            frames = frames[st:]; H, n = fit(frames[0]); print(f"frame {st} inliers", n); Hs = [H]
            if "--edgecut" not in sys.argv:
                LMASK = cv2.warpPerspective(geom(frames[0], H), np.linalg.inv(H), _sz)
            sf = cv2.SIFT_create(3000)
            def feats(f, H):
                mk = cv2.dilate(cv2.warpPerspective(BAND, H, (w, h)), np.ones((15, 15), np.uint8))
                hv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
                mk[(hv[..., 2] < 70) | ((hv[..., 0] < 25) & (hv[..., 1] > 60))] = 0
                return sf.detectAndCompute(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), mk)
            kp, dp = feats(frames[0], H)
            for f in frames[1:]:
                k, d = feats(f, Hs[-1]); M = None
                if d is not None and dp is not None and len(k) > 10:
                    mm = [a for a, b in cv2.BFMatcher().knnMatch(dp, d, k=2) if a.distance < 0.7 * b.distance]
                    if len(mm) >= 12 and "--rigid" in sys.argv:   # fast-moving tub (S6): shift + scale + small turn only
                        A2, inl = cv2.estimateAffinePartial2D(np.float32([kp[x.queryIdx].pt for x in mm]), np.float32([k[x.trainIdx].pt for x in mm]), method=cv2.RANSAC, ransacReprojThreshold=2.0)
                        if A2 is not None and abs(np.hypot(*A2[:, 0]) - 1) < 0.08: M = np.vstack([A2, [0, 0, 1]])
                    elif len(mm) >= 12:
                        M, inl = cv2.findHomography(np.float32([kp[x.queryIdx].pt for x in mm]), np.float32([k[x.trainIdx].pt for x in mm]), cv2.RANSAC, 2.0)
                if M is None: bad += 1; M = np.eye(3)
                Hs.append(M @ Hs[-1]); kp, dp = k, d
            Q = np.float32([[0, 0], [_sz[0], 0], [_sz[0], _sz[1]], [0, _sz[1]]]).reshape(4, 1, 2)
            A = np.stack([cv2.perspectiveTransform(Q, x) for x in Hs])
            for i, f in enumerate(frames):
                c = A[max(0, i - 2):i + 3].mean(0)
                p.stdin.write(paste(f, cv2.getPerspectiveTransform(Q.reshape(4, 2), c.reshape(4, 2)))[0].tobytes())
            p.stdin.close(); p.wait(); print(f"{len(frames)} frames followed, {bad} lost"); sys.exit()
        if "--track" in sys.argv:
            # 2026-10-19 (S3 camera arc, S6 tub lifted into a bag): the tub moves, so fit EVERY frame, then smooth the four
            # label-band corners over 9 frames (raw per-frame fits jitter) and rebuild each frame's homography from them
            Q = np.float32([[0, 0], [_sz[0], 0], [_sz[0], _sz[1]], [0, _sz[1]]]).reshape(-1, 1, 2); cs = []
            for f in frames:
                Hf, n = fit(f)
                if Hf is None: bad += 1; cs.append(cs[-1] if cs else None)
                else: cs.append(cv2.perspectiveTransform(Q, Hf))
            first = next(c for c in cs if c is not None); cs = [first if c is None else c for c in cs]; A = np.stack(cs)
            for i, f in enumerate(frames):
                c = A[max(0, i - 4):i + 5].mean(0)
                p.stdin.write(paste(f, cv2.getPerspectiveTransform(Q.reshape(4, 2), c.reshape(4, 2)))[0].tobytes())
            p.stdin.close(); p.wait(); print(f"{len(frames)} frames tracked, {bad} without a fit"); sys.exit()
        H, n = fit(frames[ref]); print("ref frame", ref, "inliers", n)
        for f in frames:
            p.stdin.write(paste(f, H)[0].tobytes())
        p.stdin.close(); p.wait(); print(f"{len(frames)} frames, {bad} without a fresh fit")
