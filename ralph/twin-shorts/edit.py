"""Reel-style edit of a talking-head clip (AI twin or real take): hook title on frame 0, split screen with a white top
panel showing real kit pages, punch-ins, and (version B only) pop-up key words + subtitles.
Usage (MuseTalk venv python, has cv2/PIL/numpy):
  python edit.py TALK.mp4 VO.wav OUT.mp4 --version A|B [--only T0,T1]   (--only renders a short stretch for a check)
Timeline lives in PLAN below (seconds on the VO clock, from work/words.json)."""
import json, subprocess, sys, argparse
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = __file__.rsplit("/", 1)[0]
ap = argparse.ArgumentParser(); ap.add_argument("talk"); ap.add_argument("vo"); ap.add_argument("out")
ap.add_argument("--version", default="A"); ap.add_argument("--only", default="")
ap.add_argument("--plan", default=""); ap.add_argument("--words", default="")
a = ap.parse_args()
W, H, FPS = 1080, 1920, 25
SERIF = f"{HERE}/fonts/InstrumentSerif-Regular.ttf"
YEL = (255, 210, 63)

# (start, end, mode, page, scroll) ; mode: full | punch | split
PLAN = [(0.00, 2.95, "title", None, 0), (2.95, 6.20, "split", "K-01", 0), (6.20, 9.95, "punch", None, 0),
        (9.95, 12.60, "split", "H-01", 0), (12.60, 15.15, "split", "H-04", 1), (15.15, 17.40, "split", "V-01", 0),
        (17.40, 19.50, "full", None, 0), (19.50, 99.0, "punch", None, 0)]
POPS = [(3.12, 4.60, "52", " pages"), (5.76, 7.20, "5", " photos"), (8.96, 9.95, "finished", " video"),
        (10.32, 11.70, "120", " hooks"), (17.04, 18.70, "your own", " voice"), (19.60, 99.0, "DM me", " KIT")]
words = json.load(open(a.words or f"{HERE}/work/words.json"))
for i, w in enumerate(words):
    if i and words[i - 1]["w"].lower() == "me" and w["w"].lower().startswith("kit"): w["w"] = "KIT" + w["w"][3:]


def font(sz): return ImageFont.truetype(SERIF, sz)


def shadow_text(img, xy, parts, sz, anchor_center=True):
    """Draw coloured text runs [(text, colour)] centred on xy with a soft dark shadow (premium, not flat)."""
    f = font(sz); d = ImageDraw.Draw(img)
    tw = sum(d.textlength(t, font=f) for t, _ in parts)
    if tw > 900: f = font(int(sz * 900 / tw)); tw = sum(d.textlength(t, font=f) for t, _ in parts)   # stay in the safe zone
    x = xy[0] - tw / 2 if anchor_center else xy[0]; y = xy[1]
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); xx = x
    for t, _ in parts: sd.text((xx, y + 4), t, font=f, fill=(0, 0, 0, 200)); xx += d.textlength(t, font=f)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    for t, c in parts: d.text((x, y), t, font=f, fill=c + (255,)); x += d.textlength(t, font=f)


def hook_layer():
    """Hook on the white top panel (title mode): dark serif, key words on a yellow marker. Inside the safe zone."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); NAVY = (27, 31, 59, 255)
    f1, f2 = font(112), font(100)
    t1 = "Everything inside"; w1 = d.textlength(t1, font=f1); d.text((540 - w1 / 2, 400), t1, font=f1, fill=NAVY)
    a_, b_ = "the ", "AI Product Video Kit"; wa, wb = d.textlength(a_, font=f2), d.textlength(b_, font=f2)
    x = 540 - (wa + wb) / 2; d.rounded_rectangle((x + wa - 10, 548, x + wa + wb + 10, 628), 12, fill=YEL + (255,))
    d.text((x, 520), a_, font=f2, fill=NAVY); d.text((x + wa, 520), b_, font=f2, fill=NAVY)
    return im


def page_card(name):
    p = Image.open(f"{HERE}/pages/{name}.png").convert("RGB")
    s = 640 / p.width; p = p.resize((640, int(p.height * s)), Image.LANCZOS)      # downscale only (sharp)
    m = Image.new("L", p.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *p.size), 18, fill=255)
    c = Image.new("RGBA", p.size); c.paste(p, (0, 0), m); return c


def room_panel():
    """Blurred studio photo behind the floating cards and the hook (rooms/px/bg36.jpg, Pexels), slightly darkened."""
    r = Image.open(f"{HERE}/rooms/px/bg36.jpg").convert("RGB"); s = max(W / r.width, 820 / r.height)
    r = r.resize((int(r.width * s) + 1, int(r.height * s) + 1), Image.LANCZOS); x0 = (r.width - W) // 2; y0 = int((r.height - 820) * 0.35)
    r = r.crop((x0, y0, x0 + W, y0 + 820)).filter(ImageFilter.GaussianBlur(16))
    return Image.eval(r, lambda v: int(v * 0.8)).convert("RGBA")


def hook_layer2():
    """Hook in the reference style: big yellow serif with a soft dark shadow, over the blurred room, in the safe zone."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_text(im, (540, 400), [("Everything inside", (255, 255, 255))], 112)
    shadow_text(im, (540, 520), [("the AI Product Video Kit", YEL)], 100)
    return im


ROOM = room_panel(); HOOK2 = hook_layer2()
CARDS = {n: page_card(n) for n in {s[3] for s in PLAN if s[3] and not s[3].startswith(("anim:", "card:"))}}
HOOK = hook_layer()
PANEL_H, WIN_TOP, WIN_H = 820, 140, 640


import motion, motion2


def panel(name, t, t0, t1, scroll):
    if name.startswith("anim:"): return motion.ANIMS[name[5:]](t - t0, t1 - t0)
    if name.startswith("card:"): return None
    pn = Image.new("RGBA", (W, PANEL_H), (250, 250, 248, 255)); c = CARDS[name]
    off = int((c.height - WIN_H) * min(1, (t - t0) / max(0.1, t1 - t0)) * 0.55) if scroll else 0
    crop = c.crop((0, off, c.width, off + WIN_H))
    sh = Image.new("RGBA", pn.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle(
        (220, WIN_TOP + 10, 860, WIN_TOP + WIN_H + 14), 18, fill=(0, 0, 0, 70))
    pn.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); pn.alpha_composite(crop, (220, WIN_TOP)); return pn


def subtitle(t):
    """3-word chunks from words.json; returns the chunk on screen at t."""
    for ch, nxt in CHUNKS:
        if ch[0]["s"] - 0.05 <= t < nxt: return " ".join(w["w"] for w in ch).replace(" -", "-")
    return ""


def chunks():
    """Up to 3 words per chunk, never across a sentence end."""
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["w"][-1] in ".,?!": out.append(cur); cur = []
    if cur: out.append(cur)
    return [(c, out[i + 1][0]["s"] if i + 1 < len(out) else 99) for i, c in enumerate(out)]


def frame(base, t):
    seg = next(s for s in PLAN if s[0] <= t < s[1]); mode = seg[2]
    if mode == "punch":
        z = 1.2; cw, chh = int(W / z), int(H / z); cx, cy = 526, 900
        x0, y0 = max(0, cx - cw // 2), max(0, min(H - chh, cy - chh // 2))
        img = cv2.resize(base[y0:y0 + chh, x0:x0 + cw], (W, H), interpolation=cv2.INTER_CUBIC)
    elif mode in ("split", "title"):
        cy0 = seg[5] if len(seg) > 5 else 180; img = np.full((H, W, 3), 248, np.uint8); img[PANEL_H:] = base[cy0:cy0 + H - PANEL_H]
    else: img = base.copy()
    im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert("RGBA")
    if mode == "split" and seg[3].startswith("card:"):
        im.alpha_composite(ROOM, (0, 0))
        nm = seg[3][5:]
        if nm.startswith("text:"):
            parts = nm[5:].split("|"); card = motion2.text_card(t - seg[0], seg[1] - seg[0], parts[0], parts[1] if len(parts) > 1 else "", dark=len(parts) > 2)
        else: card = motion2.ANIMS[nm](t - seg[0], seg[1] - seg[0])
        k = motion2.eob((t - seg[0]) / 0.35)
        cw, ch = int(motion2.CW * (0.9 + 0.1 * k)), int(motion2.CH * (0.9 + 0.1 * k)); card = card.resize((cw, ch), Image.LANCZOS)
        m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, ch - 1), 22, fill=255); card.putalpha(m)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((540 - cw // 2 + 6, 150 + 16, 540 + cw // 2 + 6, 150 + ch + 16), 22, fill=(0, 0, 0, 110))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18))); im.alpha_composite(card, (540 - cw // 2, 150 + (motion2.CH - ch) // 2))
    elif mode == "split": im.alpha_composite(panel(seg[3], t, seg[0], seg[1], seg[4]), (0, 0))
    if mode == "title": im.alpha_composite(ROOM, (0, 0)); im.alpha_composite(HOOK2)
    if a.version == "B":
        popping = False
        for p0, p1, w1, w2 in POPS:
            if p0 <= t < p1:
                k = min(1, (t - p0) / 0.12); sz = int(150 * (0.85 + 0.15 * k)); popping = True
                _d = ImageDraw.Draw(im); _w = _d.textlength(w1 + w2, font=font(sz))
                if _w > 900: sz = int(sz * 900 / _w)          # keep the pop inside the frame with margins
                y = 735 if mode == "split" else 1050          # boundary in split; chest (below the mouth) otherwise
                shadow_text(im, (540, y), [(w1, YEL), (w2, (255, 255, 255))], sz)
        s = subtitle(t)
        if s and mode != "title" and not (mode == "split" and popping):
            shadow_text(im, (540, 770 if mode == "split" else 1290), [(s, (255, 255, 255))], 68)
    return cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2BGR)


if a.plan:
    _p = json.load(open(a.plan)); PLAN[:] = [tuple(x) for x in _p["plan"]]; POPS[:] = [tuple(x) for x in _p["pops"]]
    if _p.get("hook"):
        HOOK2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shadow_text(HOOK2, (540, 400), [(_p["hook"][0], (255, 255, 255))], 112); shadow_text(HOOK2, (540, 520), [(_p["hook"][1], YEL)], 100)
    CARDS.update({n: page_card(n) for n in {s_[3] for s_ in PLAN if s_[3] and not s_[3].startswith(("anim:", "card:"))} if n not in CARDS})
CHUNKS = chunks()
cap = cv2.VideoCapture(a.talk); n = int(cap.get(7)); dur = n / FPS
t0, t1 = (map(float, a.only.split(",")) if a.only else (0, dur))
ff = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
      "-ss", str(t0), "-t", str(t1 - t0), "-i", a.vo, "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-threads", "4", a.out]
p = subprocess.Popen(ff, stdin=subprocess.PIPE); i = 0
while True:
    ok, fr = cap.read()
    if not ok: break
    t = i / FPS; i += 1
    if t < t0: continue
    if t >= t1: break
    if fr.shape[:2] != (H, W): fr = cv2.resize(fr, (W, H))
    try: p.stdin.write(frame(fr, t).tobytes())
    except BrokenPipeError: break
p.stdin.close(); p.wait(); print("EDIT_OK", a.out)
