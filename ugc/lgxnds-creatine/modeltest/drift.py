"""Measure label drift per clip: SIFT-fit the real label (refs/crop_tub_hi.png, printed core only) on every frame.
Reports: frames where the label could not be found, corner movement vs frame 0 (px, median/max), frame-to-frame jitter
(px, median/p95) and print fidelity = NCC of the rectified printed block vs the real label (1.0 = identical)."""
import sys, json, cv2, numpy as np
sys.path.insert(0, ".")
import label as L

real = cv2.cvtColor(L.REAL, cv2.COLOR_BGR2GRAY)
h, w = real.shape
sift = cv2.SIFT_create(4000)
kr, dr = sift.detectAndCompute(real, L.CORE)
bf = cv2.BFMatcher()
corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
ys, xs = np.where(L.CORE > 0); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
ref_core = real[y0:y1, x0:x1].astype(np.float32)

def ncc(a, b):
    a = a - a.mean(); b = b - b.mean(); return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-6))

out = {}
for name in sys.argv[1:]:
    cap = cv2.VideoCapture(f"modeltest/{name}.mp4"); pts, fid, lost, n = [], [], 0, 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        n += 1
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        kf, df = sift.detectAndCompute(g, None)
        m = [a for a, b in bf.knnMatch(dr, df, k=2) if a.distance < 0.75 * b.distance] if df is not None else []
        H = None
        if len(m) >= 12:
            H, inl = cv2.findHomography(np.float32([kr[a.queryIdx].pt for a in m]), np.float32([kf[a.trainIdx].pt for a in m]), cv2.RANSAC, 4.0)
            if H is not None and inl.sum() < 12: H = None
        if H is None:
            lost += 1; pts.append(None); fid.append(0.0); continue
        pts.append(cv2.perspectiveTransform(corners, H).reshape(-1, 2))
        warped = cv2.warpPerspective(g, np.linalg.inv(H), (w, h))[y0:y1, x0:x1].astype(np.float32)
        fid.append(ncc(cv2.GaussianBlur(warped, (0, 0), 1.5), cv2.GaussianBlur(ref_core, (0, 0), 1.5)))
    good = [p for p in pts if p is not None]
    p0 = good[0]
    move = [float(np.abs(p - p0).max()) for p in good]
    jit = [float(np.abs(b - a).max()) for a, b in zip(pts, pts[1:]) if a is not None and b is not None]
    out[name] = {"frames": n, "label_lost_frames": lost, "move_vs_first_px_median": round(float(np.median(move)), 1),
                 "move_vs_first_px_max": round(max(move), 1), "jitter_px_median": round(float(np.median(jit)), 2),
                 "jitter_px_p95": round(float(np.percentile(jit, 95)), 2), "print_fidelity_median": round(float(np.median(fid)), 3),
                 "print_fidelity_min": round(min(fid), 3)}
    print(name, json.dumps(out[name]))
json.dump(out, open("modeltest/drift.json", "w"), indent=1)
