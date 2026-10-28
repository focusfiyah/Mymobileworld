"""Real-photo composite (Ralph 2026-10-27, "All 6 shots"): the real charm cut from the listing photo, hung at its TRUE size
(9.5 x 5.5 cm vs a ~38 cm handbag) on a charm-free still, with a drawn gold key ring + short chain. Free.
  python3 tools/composite.py S7   -> stills/S7.png (from stills/S7bg.png)"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
CUT, ORIG = "refs/cutout/charm_real_cutout.png", "refs/real/listing_burgundy_10of10.jpg"
# hang = point on the handbag handle base where the ring goes; body = charm bag-body width in px; bright = light match
SPEC = {"S7": dict(bg="stills/S7bg.png", hang=(537, 498), body=92, bright=0.86, tilt=-4),   # v11: drawn ring again (the S7N clip has no AI clasp to hang from)
        "S9": dict(bg="stills/S9bg.png", hang=(529, 672), body=92, bright=0.95, tilt=-4)}


def charm():
    """Cutout with the white tissue in the opening restored from the real photo (rembg dropped it)."""
    c = Image.open(CUT).convert("RGBA"); o = Image.open(ORIG).convert("RGB").crop((150, 520, 870, 1220)).convert("RGBA")
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).polygon([(96, 325), (102, 250), (300, 243), (478, 252), (490, 325)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(3))
    a = c.split()[3]; fill = Image.composite(o, c, m)
    fill.putalpha(Image.composite(Image.new("L", c.size, 255), a, m))
    lit = ImageEnhance.Color(ImageEnhance.Brightness(fill).enhance(0.97)).enhance(0.85); lit.putalpha(fill.split()[3])   # v8: no glowing tissue
    tm = Image.new("L", c.size, 0); ImageDraw.Draw(tm).polygon([(96, 325), (102, 250), (300, 243), (478, 252), (490, 325)], fill=255)
    tm = Image.composite(tm, Image.new("L", c.size, 0), a.point(lambda v: 255 if v < 128 else 0)).filter(ImageFilter.GaussianBlur(2))
    return Image.composite(lit, fill, tm)


def look(c, bg, ox, oy, turn=0.05):
    """v8 (Grace 2026-10-28: 'she can tell it was pasted'): make the studio photo sit in the room. A slight turn (the far
    side a little smaller), the room's own light across it (the plate's brightness around it, top lit, bottom in shade)
    and the room's white balance. The hue stays the listing's burgundy (tools/hue_check.py)."""
    import numpy as np, cv2
    a = np.asarray(c).astype(np.float32); h, w = a.shape[:2]
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]]); d = turn * h / 2
    dst = np.float32([[0, 0], [w * (1 - turn / 2), d], [w * (1 - turn / 2), h - d], [0, h]])
    al = a[..., 3:] / 255; a[..., :3] *= al                       # premultiplied, so the edge does not pull in black
    a = cv2.warpPerspective(a, cv2.getPerspectiveTransform(src, dst), (w, h), flags=cv2.INTER_LINEAR)
    al = np.maximum(a[..., 3:] / 255, 1e-3); a[..., :3] = np.where(al > 0.004, a[..., :3] / al, 0)
    P = np.asarray(bg.convert("RGB")).astype(np.float32); H, W = P.shape[:2]
    L = P.mean(2); Lb = cv2.GaussianBlur(L, (0, 0), max(8, w * 0.35))
    x0, y0 = max(0, ox), max(0, oy); x1, y1 = min(W, ox + w), min(H, oy + h)
    g = np.ones((h, w), np.float32); reg = Lb[y0:y1, x0:x1]
    g[y0 - oy:y1 - oy, x0 - ox:x1 - ox] = reg / max(reg.mean(), 1)
    g = np.clip(1 + 0.8 * (g - 1), 0.8, 1.2) * np.linspace(1.06, 0.9, h)[:, None]
    hi = P[L > np.percentile(L, 80)].mean(0); wb = (hi / hi.mean()) ** 0.4
    a[..., :3] = np.clip(a[..., :3] * g[..., None] * wb, 0, 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def shadow(size, c, ox, oy, k=1.0):
    """Two shadows: a tight contact one where the charm touches the bag and a soft wider one."""
    sh = Image.new("RGBA", size, (0, 0, 0, 0))
    for (dx, dy, op, bl) in [(3, 4, 0.5, 3), (7, 9, 0.2, 8)]:
        blk = Image.new("RGBA", c.size, (22, 10, 8, 255)); blk.putalpha(c.split()[3].point(lambda v: int(v * op * k)))
        lay = Image.new("RGBA", size, (0, 0, 0, 0)); lay.alpha_composite(blk, (ox + dx, oy + dy)); sh.alpha_composite(lay.filter(ImageFilter.GaussianBlur(bl)))
    return sh


def gold_chain(d, p0, p1, links, w):
    """Small alternating gold links from p0 to p1 (drawn at 4x)."""
    for i in range(links):
        t0, t1 = i / links, (i + 1) / links
        x0, y0 = p0[0] + (p1[0] - p0[0]) * t0, p0[1] + (p1[1] - p0[1]) * t0
        x1, y1 = p0[0] + (p1[0] - p0[0]) * t1, p0[1] + (p1[1] - p0[1]) * t1
        cx, cy, L = (x0 + x1) / 2, (y0 + y1) / 2, ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
        rx, ry = (w * 0.9, L * 0.62) if i % 2 == 0 else (w * 0.35, L * 0.62)
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(150, 110, 52, 255), width=max(2, int(w * 0.5)))
        d.ellipse([cx - rx + 1, cy - ry + 1, cx + rx - 1, cy + ry - 1], outline=(214, 178, 112, 255), width=max(1, int(w * 0.18)))


def build(sid):
    s = SPEC[sid]; bg = Image.open(s["bg"]).convert("RGBA"); W, H = bg.size
    c = charm(); k = s["body"] / 440.0   # the real bag body is ~440 px wide in the cutout
    c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
    c = ImageEnhance.Brightness(c).enhance(s["bright"]); c = c.rotate(s["tilt"], resample=Image.BICUBIC, expand=True)
    hx, hy = s["hang"]; chain_len = int(26 * k / 0.209)
    # hang it by the top of its handles: the highest opaque pixel row of the charm
    al = c.split()[3].point(lambda v: 255 if v > 128 else 0); top = al.getbbox()[1] + 1
    xs = [x for x in range(c.width) if al.getpixel((x, top))]; ax, ay = sum(xs) // len(xs), top
    ox, oy = hx - ax, hy + 10 + chain_len - ay
    c = look(c, bg, ox, oy); out = bg.copy(); out.alpha_composite(shadow(bg.size, c, ox, oy))
    if not s.get("ring", True):                          # no drawn ring/chain: the charm's handles at the hang point
        print(sid, "charm top (HANG point for track_paste):", (hx, oy + ay)); out.alpha_composite(c, (ox, oy))
        out.convert("RGB").save(f"stills/{sid}.png"); return
    S = 4; lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    r = 9 * S; d.ellipse([hx * S - r, hy * S - r * 1.15, hx * S + r, hy * S + r * 1.15], outline=(150, 110, 52, 255), width=int(2.4 * S))
    d.ellipse([hx * S - r + 3, hy * S - r * 1.15 + 3, hx * S + r - 3, hy * S + r * 1.15 - 3], outline=(214, 178, 112, 255), width=S)
    gold_chain(d, ((hx) * S, (hy + 10) * S), ((ox + ax) * S, (oy + ay + 4) * S), 6, 2.2 * S)
    lay = lay.resize((W, H), Image.LANCZOS); out.alpha_composite(lay)
    # the handle passes THROUGH the ring: put the handle's own pixels back over the ring's upper half
    for y in range(hy - 12, hy + 1):
        for x in range(hx - 12, hx + 13):
            r_, g_, b_, _ = bg.getpixel((x, y))
            if r_ > b_ + 12 and r_ + g_ + b_ < 420: out.putpixel((x, y), bg.getpixel((x, y)))
    out.alpha_composite(c, (ox, oy))
    out.convert("RGB").save(f"stills/{sid}.png"); print(sid, "composite", c.size, "at", (ox, oy))




def stocking(out="stills/S8.png", body=100, cx=285, sink=0.45, tilt=-10):
    """S8 (Grace 2026-10-27: 'see how the eye cream fits in like it can fall in'): the real charm sits INSIDE a real
    Pexels stocking (rooms/roomE_stocking2_crop.png, px 5727880), its lower part hidden behind the white fur cuff."""
    bg = Image.open("rooms/roomE_stocking2_crop.png").convert("RGBA"); W, H = bg.size
    c = charm(); k = body / 440.0
    c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
    c = ImageEnhance.Brightness(c).enhance(0.97).rotate(tilt, resample=Image.BICUBIC, expand=True)
    pts = [(150, 575), (190, 533), (250, 490), (290, 459), (330, 423), (370, 381), (410, 372)]   # the cuff's top edge, measured
    def edge(x):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x <= x1: return y0 + (y1 - y0) * (max(x, x0) - x0) / (x1 - x0)
        return pts[-1][1]
    al = c.split()[3].point(lambda v: 255 if v > 128 else 0); bb = al.getbbox()
    vis_h = bb[3] - bb[1]; ox = cx - c.width // 2; oy = int(edge(cx) - bb[1] - vis_h * (1 - sink))
    c = look(c, bg, ox, oy, turn=0.03)
    lay = Image.new("RGBA", bg.size, (0, 0, 0, 0)); lay.alpha_composite(c, (ox, oy))
    lay.save("stills/overlay_S8.png")                     # uncut: in the clip each frame's own cuff hides its lower part
    # inside the stocking it is darker: shade the part just above the rim
    sh = Image.new("L", bg.size, 0); d = ImageDraw.Draw(sh)
    for x in range(W): d.line([(x, edge(x) - 30), (x, edge(x))], fill=0)
    px = lay.load(); bgp = bg.load()
    for y in range(max(0, oy), min(H, oy + c.height)):
        for x in range(max(0, ox), min(W, ox + c.width)):
            r, g, b, a = px[x, y]
            if not a: continue
            e = edge(x); R, G, B, _ = bgp[x, y]
            fur = R > 175 and G > 175 and B > 175 and max(R, G, B) - min(R, G, B) < 40
            if y > e - 1 or (y > e - 12 and fur): px[x, y] = (r, g, b, 0); continue
            if y > e - 28:                                    # ambient occlusion near the opening
                f = 0.62 + 0.38 * (e - y + 4) / 32
                px[x, y] = (int(r * f), int(g * f), int(b * f), a)
    o = bg.copy(); o.alpha_composite(lay); o.convert("RGB").save(out); print("S8 stocking composite at", (ox, oy), c.size)


def swap(src="stills/S4e.png", out="stills/S4.png", body=118, hang=(338, 749)):
    """S4: the AI charm (draped scarf, too big, a letter on the lock) is painted out (OpenCV inpaint, the handbag and the
    sofa filled separately so the bag's bottom edge stays crisp) and the real charm hangs from the same gold ring and clasp
    the hand holds, at its true size next to the hand. Free."""
    import cv2, numpy as np
    im = cv2.imread(src); H, W = im.shape[:2]; m = np.zeros((H, W), np.uint8)
    poly = np.array([(195, 830), (240, 760), (300, 745), (380, 745), (445, 770), (505, 860), (512, 1045), (548, 1045),
                     (552, 1250), (436, 1250), (428, 1095), (238, 1095), (192, 1010)], np.int32)
    cv2.fillPoly(m, [poly], 255)
    b_, g_, r_ = [im[..., i].astype(int) for i in range(3)]          # + any scarf pink/blue left near it
    near = np.zeros_like(m); near[730:1270, 170:580] = 255
    m[(near > 0) & (((r_ > 150) & (r_ - g_ > 35) & (b_ > g_)) | ((b_ > r_ + 25) & (b_ > 110)))] = 255
    m = cv2.dilate(m, np.ones((15, 15), np.uint8))
    yy = np.arange(H)[:, None].repeat(W, 1); xx = np.arange(W)[None, :].repeat(H, 0)
    base = 1050 + (xx - 120) * 0.1                       # the handbag's soft bottom edge, measured at x 120/200/560
    # fill each row by blending the nearest clean pixels left and right of the hole (leather shades across, the sofa too);
    # the band at the bag's bottom edge is blurred vertically so the edge stays soft like the real one
    fill = im.astype(np.float32).copy()
    for y in range(H):
        row = np.where(m[y] > 0)[0]
        if not len(row): continue
        for run in np.split(row, np.where(np.diff(row) > 1)[0] + 1):
            x0, x1 = max(run[0] - 3, 0), min(run[-1] + 3, W - 1)
            L, R = im[y, max(x0 - 6, 0):x0 + 1].mean(0), im[y, x1:x1 + 7].mean(0)
            w = ((run - x0) / max(x1 - x0, 1))[:, None]; fill[y, run] = L * (1 - w) + R * w
    band = (m > 0) & (np.abs(yy - base) < 14); blur = cv2.GaussianBlur(fill, (1, 0), 0, sigmaY=6) if False else cv2.GaussianBlur(fill, (0, 0), sigmaX=1, sigmaY=6)
    fill = np.where(band[..., None], blur, cv2.GaussianBlur(fill, (0, 0), sigmaX=0.8, sigmaY=3))   # no row streaks
    # leather grain: the fine detail of the clean left side of the same handbag, tiled across the painted part
    src = im.astype(np.float32); hp = src - cv2.GaussianBlur(src, (0, 0), 1.5)
    tile = hp[900:1000, 95:180]; grain = np.tile(tile, (H // 100 + 1, W // 85 + 1, 1))[:H, :W]   # a clean interior patch
    fill += np.where((yy <= base - 10)[..., None], grain * 0.9, 0) + np.random.default_rng(7).normal(0, 1.5, fill.shape)
    clean = np.where((m > 0)[..., None], np.clip(fill, 0, 255), im).astype(np.uint8)
    bg = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)).convert("RGBA"); bg.convert("RGB").save("stills/plate_S4.png")
    c = charm(); k = body / 440.0; c = c.resize((int(c.width * k), int(c.height * k)), Image.LANCZOS)
    c = ImageEnhance.Brightness(c).enhance(0.92)
    al = c.split()[3].point(lambda v: 255 if v > 128 else 0); top = al.getbbox()[1] + 1
    xs = [x for x in range(c.width) if al.getpixel((x, top))]; ax = sum(xs) // len(xs)
    ox, oy = hang[0] - ax, hang[1] - top
    c = look(c, bg, ox, oy); bg.alpha_composite(shadow(bg.size, c, ox, oy)); bg.alpha_composite(c, (ox, oy))
    bg.convert("RGB").save(out); print("S4 swap at", (ox, oy), c.size)


if __name__ == "__main__":
    for sid in sys.argv[1:]: stocking() if sid == "S8" else swap() if sid == "S4" else build(sid)
