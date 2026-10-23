#!/usr/bin/env python3
"""Day One looks: a different thumbnail look for every video, measured against every thumbnail before it.

Run from the Dayone-ai repo root (it reads jobs/<slug>/job.json and writes data/looks.json).

  looks.py render jobs/<slug>              3 candidate looks + a labelled sheet (jobs/<slug>/_looks_sheet.png)
  looks.py render jobs/<slug> --band B     final jobs/<slug>/thumbnail.png in band B, recorded in data/looks.json
  looks.py render jobs/<slug> --auto       final thumbnail in the best candidate (least alike, text fits)
  looks.py check jobs/<a> [jobs/<b> ...]   sameness, band repeat and text fit; prints CHECK_PASS n/n
  looks.py control                         the old one-template thumbnails must all read as too alike
  looks.py selftest                        every band fits a long real title; an absurd one must fail
  looks.py bands                           list the bands

Job key (all optional except what a band needs): "look": {"band", "top", "big", "badge", "image", "url",
"image_mobile", "crop_y", "focus": "50% 20%", "prompt", "stat", "stat_label", "accent": "#RRGGBB"}. Missing text falls back to
thumb_top / thumb_big / thumb_badge, the image to thumb_url, then the first web shot's url.
"""
import argparse, base64, colorsys, datetime, html, io, itertools, json, re, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

TW, TH = 1280, 720
GRID, CLOSE, LIMIT = (32, 18), 30.0, 0.30   # cells, RGB distance that counts as "same colour", max shared share
REPEAT_WINDOW = 5                            # a band may not repeat within the last 5 thumbnails
LEDGER = Path("data/looks.json")
MARK = Path("brand/avatar.png")
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo+Black&family=Anton&family=Bebas+Neue"
         "&family=DM+Serif+Display&family=Space+Grotesk:wght@700&family=JetBrains+Mono:wght@700"
         "&family=Permanent+Marker&family=Rubik:wght@900&display=swap")
ACCENTS = ["#ff4d2e", "#2f6bff", "#14b37d", "#ffb800", "#c13cff", "#ff2e7e", "#00a6c8", "#7a5cff"]

# ---------------------------------------------------------------- bands
# Each band is a familiar format described by its parts (the prompt pack's BAND rule): it reads at once and copies
# nobody's design. Classes: .fit = text that must fit its box (auto-shrinks to data-min px); .avoid = image areas,
# which no .fit text may cover (nor the .badge or .mark).
BASE_CSS = """*{box-sizing:border-box}html,body{margin:0;width:1280px;height:720px;overflow:hidden;background:{BG}}
.fit{overflow:hidden}.mark{position:absolute;width:76px;height:76px;border-radius:50%}
.badge{position:absolute;font-family:'Archivo Black';font-size:34px;padding:8px 20px;border-radius:10px;
background:{ACCENT};color:{ON_ACCENT};white-space:nowrap}"""

BANDS = {
    "stack": dict(
        needs=[], note="three browser windows fanned in depth under a full-width title",
        html="""<div class="fit" data-min="64" style="position:absolute;left:56px;top:34px;width:1168px;height:110px;
font-family:'Space Grotesk';font-size:96px;line-height:1;color:{INK};white-space:nowrap">{BIG}</div>
<div class="fit" data-min="28" style="position:absolute;left:60px;top:148px;width:760px;height:46px;font-family:'Space Grotesk';
font-size:40px;color:{ACCENT};white-space:nowrap">{TOP}</div>
<div style="position:absolute;left:0;top:0;width:1280px;height:720px;perspective:1600px">
 <div class="avoid win" style="left:110px;top:300px;transform:rotateY(24deg) rotateZ(-2deg)"><i></i><img src="{IMG}" style="object-position:0% 60%"></div>
 <div class="avoid win" style="left:600px;top:290px;transform:rotateY(-22deg) rotateZ(2deg)"><i></i><img src="{IMG}" style="object-position:100% 30%"></div>
 <div class="avoid win" style="left:330px;top:250px;width:620px;height:430px;z-index:2"><i></i><img src="{IMG}" style="object-position:{FOCUS}"></div>
</div>
<div class="badge" style="right:56px;top:160px;transform:rotate(3deg)">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:40px;bottom:30px">""",
        css=""".win{position:absolute;width:560px;height:390px;border-radius:14px;overflow:hidden;background:#fff;
border:3px solid {INK};box-shadow:0 30px 60px rgba(0,0,0,.35)}.win i{display:block;height:30px;background:{INK}}
.win img{width:100%;height:calc(100% - 30px);object-fit:cover}"""),
    "split": dict(
        needs=["prompt"], note="what you type on the left, what you get on the right, title on a bottom plate",
        html="""<div style="position:absolute;left:0;top:0;width:520px;height:560px;background:{INK}"></div>
<div class="fit" data-min="26" style="position:absolute;left:44px;top:40px;width:440px;height:300px;font-family:'JetBrains Mono';
font-size:44px;line-height:1.2;color:{PAPER}">&gt; {PROMPT}<span style="color:{ACCENT}">&#9608;</span></div>
<div class="fit" data-min="26" style="position:absolute;left:44px;top:420px;width:440px;height:100px;font-family:'Archivo Black';
font-size:40px;line-height:1.15;color:{ACCENT}">{TOP}</div>
<div class="avoid" style="position:absolute;left:520px;top:0;width:760px;height:560px;overflow:hidden">
 <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:468px;top:230px;width:104px;height:104px;border-radius:50%;background:{ACCENT};
color:{ON_ACCENT};font:900 70px/104px Rubik;text-align:center">&#8594;</div>
<div style="position:absolute;left:0;top:560px;width:1280px;height:160px;background:{ACCENT}"></div>
<div class="fit" data-min="64" style="position:absolute;left:44px;top:574px;width:1000px;height:132px;font-family:'Anton';
font-size:118px;line-height:1.1;color:{ON_ACCENT};white-space:nowrap">{BIG}</div>
<img class="mark" src="{MARK}" style="right:40px;top:602px">
<div class="badge" style="right:40px;top:24px;background:{INK};color:{PAPER}">{BADGE}</div>"""),
    "loupe": dict(
        needs=[], note="the full page, dimmed, with a magnifier on the one thing that matters",
        html="""<img src="{IMG}" style="position:absolute;left:0;top:0;width:1280px;height:720px;object-fit:cover;
object-position:0 0;filter:brightness(.42) saturate(.7)">
<div class="avoid" style="position:absolute;left:640px;top:110px;width:520px;height:520px;border-radius:50%;
border:14px solid {ACCENT};background:url('{IMG}') {FOCUS}/260% auto no-repeat #fff;box-shadow:0 0 0 10px rgba(0,0,0,.35)"></div>
<div style="position:absolute;left:1035px;top:560px;width:180px;height:44px;background:{ACCENT};border-radius:22px;transform:rotate(45deg)"></div>
<div style="position:absolute;left:40px;top:150px;width:580px;height:330px;background:{PAPER_PLATE};border-radius:6px"></div>
<div class="fit" data-min="22" style="position:absolute;left:72px;top:176px;width:520px;height:44px;font-family:'Archivo Black';
font-size:36px;color:{ACCENT};white-space:nowrap">{TOP}</div>
<div class="fit" data-min="64" style="position:absolute;left:72px;top:228px;width:520px;height:230px;font-family:'Archivo Black';
font-size:100px;line-height:1.02;color:{INK}">{BIG}</div>
<div class="badge" style="left:40px;top:60px">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:44px;bottom:40px">"""),
    "cover": dict(
        needs=[], note="a magazine cover: the tool's name as the masthead, the result as the cover photo, one cover line",
        html="""<div class="fit" data-min="60" style="position:absolute;left:40px;top:14px;width:1200px;height:150px;font-family:'DM Serif Display';
font-size:150px;line-height:1;color:{INK};text-align:center;white-space:nowrap;letter-spacing:-2px">{TOP}</div>
<div style="position:absolute;left:40px;top:168px;width:1200px;height:6px;background:{INK}"></div>
<div style="position:absolute;left:40px;top:190px;width:1200px;height:500px;overflow:hidden;border-radius:4px">
 <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:40px;top:470px;width:760px;height:220px;background:{ACCENT}"></div>
<div class="fit" data-min="60" style="position:absolute;left:70px;top:488px;width:700px;height:190px;font-family:'Anton';
font-size:96px;line-height:1;color:{ON_ACCENT}">{BIG}</div>
<div class="badge" style="right:60px;top:212px;background:{INK};color:{PAPER};border-radius:50%;width:150px;height:150px;
padding:0;display:flex;align-items:center;justify-content:center;text-align:center;white-space:normal;font-size:26px;line-height:1.05;transform:rotate(10deg)">{BADGE}</div>
<img class="mark" src="{MARK}" style="right:56px;bottom:40px">"""),
    "prompt": dict(
        needs=["prompt"], note="a dark chat box with the real prompt typed in, pointing at the result",
        html="""<div class="fit" data-min="60" style="position:absolute;left:56px;top:40px;width:1168px;height:120px;font-family:'Bebas Neue';
font-size:128px;line-height:1;color:{PAPER};white-space:nowrap">{BIG}</div>
<div style="position:absolute;left:56px;top:210px;width:520px;height:380px;border-radius:26px;background:#232323;border:2px solid #3a3a3a"></div>
<div class="fit" data-min="26" style="position:absolute;left:88px;top:240px;width:456px;height:320px;font-family:'JetBrains Mono';
font-size:40px;line-height:1.25;color:#f2f2f2">{PROMPT}<span style="color:{ACCENT}">&#9608;</span></div>
<div style="position:absolute;left:592px;top:350px;font:900 90px Rubik;color:{ACCENT}">&#8594;</div>
<div class="avoid" style="position:absolute;left:700px;top:190px;width:530px;height:420px;border-radius:20px;overflow:hidden;border:6px solid {ACCENT}">
 <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div class="fit" data-min="22" style="position:absolute;left:58px;top:622px;width:620px;height:50px;font-family:'Space Grotesk';
font-size:40px;color:{ACCENT};white-space:nowrap">{TOP}</div>
<div class="badge" style="right:50px;top:640px">{BADGE}</div>
<img class="mark" src="{MARK}" style="right:50px;top:44px">"""),
    "number": dict(
        needs=["stat"], note="one giant number with its label, the screen as a pinned print",
        html="""<div class="fit" data-min="160" style="position:absolute;left:40px;top:20px;width:620px;height:400px;font-family:'Anton';
font-size:400px;line-height:1;color:{ON_ACCENT};white-space:nowrap">{STAT}</div>
<div class="fit" data-min="30" style="position:absolute;left:52px;top:420px;width:600px;height:70px;font-family:'Archivo Black';
font-size:56px;color:{ON_ACCENT};white-space:nowrap">{STAT_LABEL}</div>
<div class="avoid" style="position:absolute;left:690px;top:60px;width:540px;height:420px;background:#fff;padding:16px 16px 60px;
transform:rotate(4deg);box-shadow:0 24px 50px rgba(0,0,0,.3)"><img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:0;top:540px;width:1280px;height:180px;background:{INK}"></div>
<div class="fit" data-min="56" style="position:absolute;left:52px;top:556px;width:1060px;height:150px;font-family:'Archivo Black';
font-size:84px;line-height:1.05;color:{PAPER}">{BIG}</div>
<div class="badge" style="right:40px;top:14px;background:{INK};color:{PAPER}">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:1150px;top:470px">"""),
    "phone": dict(
        needs=[], note="the result inside a phone on a two-tone field, title beside it",
        html="""<div style="position:absolute;left:0;top:0;width:760px;height:720px;background:{ACCENT}"></div>
<div class="fit" data-min="22" style="position:absolute;left:56px;top:60px;width:620px;height:44px;font-family:'Space Grotesk';
font-size:38px;color:{ON_ACCENT};white-space:nowrap">{TOP}</div>
<div class="fit" data-min="80" style="position:absolute;left:56px;top:120px;width:620px;height:420px;font-family:'Rubik';
font-size:118px;line-height:1;color:{ON_ACCENT}">{BIG}</div>
<div class="avoid" style="position:absolute;left:800px;top:40px;width:330px;height:660px;border-radius:52px;background:{INK};padding:16px;
box-shadow:-30px 30px 70px rgba(0,0,0,.35)"><img src="{IMG}" style="width:100%;height:100%;border-radius:38px;object-fit:cover;object-position:{FOCUS}"></div>
<div class="badge" style="left:56px;bottom:56px;background:{INK};color:{PAPER}">{BADGE}</div>
<img class="mark" src="{MARK}" style="right:30px;bottom:30px">"""),
    "poster": dict(
        needs=[], note="a gig poster: the title huge in the middle, the screen as a strip of film across the bottom",
        html="""<div class="fit" data-min="22" style="position:absolute;left:60px;top:40px;width:1160px;height:50px;font-family:'Space Grotesk';
font-size:42px;color:{ACCENT};text-align:center;white-space:nowrap;letter-spacing:6px">{TOP}</div>
<div class="fit" data-min="80" style="position:absolute;left:40px;top:100px;width:1200px;height:300px;font-family:'Bebas Neue';
font-size:260px;line-height:1;color:{PAPER};text-align:center;white-space:nowrap">{BIG}</div>
<div class="avoid" style="position:absolute;left:-60px;top:440px;width:1400px;height:250px;transform:rotate(-4deg);
background:{ACCENT};padding:18px 0;display:flex;gap:18px">
 <img src="{IMG}" style="flex:1;height:100%;object-fit:cover;object-position:0% 0%">
 <img src="{IMG}" style="flex:1;height:100%;object-fit:cover;object-position:{FOCUS}">
 <img src="{IMG}" style="flex:1;height:100%;object-fit:cover;object-position:100% 100%"></div>
<div class="badge" style="right:40px;bottom:30px;transform:rotate(-4deg);background:{PAPER};color:{INK}">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:40px;top:24px">"""),
    "note": dict(
        needs=[], note="the real page full-bleed with a taped sticky note written in marker",
        html="""<img src="{IMG}" style="position:absolute;left:0;top:0;width:1280px;height:720px;object-fit:cover;object-position:{FOCUS};filter:brightness(.8)">
<div style="position:absolute;left:70px;top:90px;width:600px;height:520px;background:{NOTE};transform:rotate(-4deg);
box-shadow:0 30px 60px rgba(0,0,0,.45)"></div>
<div style="position:absolute;left:290px;top:62px;width:180px;height:56px;background:rgba(255,255,255,.55);transform:rotate(3deg)"></div>
<div class="fit" data-min="22" style="position:absolute;left:120px;top:150px;width:510px;height:52px;font-family:'Permanent Marker';
font-size:40px;color:{ACCENT_DARK};white-space:nowrap;transform:rotate(-4deg)">{TOP}</div>
<div class="fit" data-min="60" style="position:absolute;left:116px;top:212px;width:520px;height:330px;font-family:'Permanent Marker';
font-size:100px;line-height:1.05;color:#1a1a1a;transform:rotate(-4deg)">{BIG}</div>
<div class="badge" style="right:50px;top:50px">{BADGE}</div>
<img class="mark" src="{MARK}" style="right:50px;bottom:40px">"""),
}

# Each band's background: dark bands on ink, light bands on paper, the number band on the accent.
BAND_BG = {"stack": "paper", "split": "paper", "loupe": "ink", "cover": "paper", "prompt": "ink",
           "number": "accent", "phone": "paper", "poster": "ink", "note": "ink"}

FIT_JS = """() => {
 const out = [];
 const avoid = [...document.querySelectorAll('.avoid,.badge,.mark')].map(e => e.getBoundingClientRect());
 for (const e of document.querySelectorAll('.fit')) {
  const min = +e.dataset.min || 20; let fs = parseFloat(getComputedStyle(e).fontSize);
  const over = () => e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1;
  while (over() && fs > min) { fs -= 2; e.style.fontSize = fs + 'px'; }
  // what shows = the text's box clipped to its own box (.fit hides overflow); tall glyph ascents don't count
  const r = document.createRange(); r.selectNodeContents(e); const tr = r.getBoundingClientRect(), b = e.getBoundingClientRect();
  const t = {left: Math.max(tr.left, b.left), top: Math.max(tr.top, b.top), right: Math.min(tr.right, b.right), bottom: Math.min(tr.bottom, b.bottom)};
  const off = b.left < -1 || b.top < -1 || b.right > 1281 || b.bottom > 721;
  const hit = avoid.some(a => !(t.right <= a.left || t.left >= a.right || t.bottom <= a.top || t.top >= a.bottom));
  out.push({text: e.innerText.slice(0, 40), size: fs, min, overflow: over(), offcanvas: off, covers_image: hit});
 }
 return out;
}"""


# ---------------------------------------------------------------- colour
def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luma(rgb):
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def brand_accent(img):
    """The page's own brand colour: the most common saturated hue, as its median pixel. None for a grey page."""
    a = np.asarray(img.convert("RGB").resize((240, 135)), float) / 255
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in a.reshape(-1, 3)])
    m = (hsv[:, 1] > 0.45) & (hsv[:, 2] > 0.35)
    if m.mean() < 0.01:
        return None
    bins = (hsv[m, 0] * 24).astype(int) % 24
    top = np.bincount(bins, minlength=24).argmax()
    px = a.reshape(-1, 3)[m][bins == top]
    return "#%02x%02x%02x" % tuple(int(v * 255) for v in np.median(px, axis=0))


def busy_focus(img):
    """Where the page has the most detail, as a CSS position ("62% 30%"): the default framing and loupe target."""
    from PIL import ImageFilter
    g = img.convert("L").resize((320, 200)).filter(ImageFilter.FIND_EDGES)
    e = np.asarray(g.resize((8, 5), Image.BOX), float)
    e[0, :] *= 0.5                                    # the top row is usually the site's menu bar
    y, x = np.unravel_index(e.argmax(), e.shape)
    return f"{round((x + .5) / 8 * 100)}% {round((y + .5) / 5 * 100)}%"


def palette(accent, bg):
    ink, paper = "#141414", "#f4f1ea"
    on_accent = ink if luma(hexrgb(accent)) > 150 else "#ffffff"
    r, g, b = hexrgb(accent)
    note = "#%02x%02x%02x" % tuple(int(c + (255 - c) * 0.72) for c in (r, g, b))      # accent, light, for paper
    dark = "#%02x%02x%02x" % tuple(int(c * 0.55) for c in (r, g, b))
    return {"ACCENT": accent, "ON_ACCENT": on_accent, "INK": ink, "PAPER": paper, "PAPER_PLATE": paper,
            "BG": {"paper": paper, "ink": ink, "accent": accent}[bg], "NOTE": note, "ACCENT_DARK": dark}


# ---------------------------------------------------------------- browser
def browser():
    from playwright.sync_api import sync_playwright
    p = sync_playwright().start()
    exe = "/opt/pw-browsers/chromium" if Path("/opt/pw-browsers/chromium").exists() else None
    b = p.chromium.launch(executable_path=exe, args=["--disable-dev-shm-usage", "--disable-gpu"])
    return p, b


# Bot walls and cookie boxes: a thumbnail of "Verifying you are human" happened on the first test (canva.com, 2026-10-23).
WALL = re.compile(r"verifying you are human|verify you are human|just a moment|checking your browser|access denied|"
                  r"attention required|are you a robot|enable javascript and cookies|get past this page|ray ?id:", re.I)
HIDE_OVERLAYS = """() => { for (const e of document.querySelectorAll('body *')) { const cs = getComputedStyle(e);
  if ((cs.position === 'fixed' || cs.position === 'sticky') && /cookie|consent|privacy|we use/i.test(e.innerText || ''))
    e.style.setProperty('display', 'none', 'important'); } }"""


def capture(url, out, crop_y=0, mobile=False):
    p, b = browser()
    try:
        vp = {"viewport": {"width": 390, "height": 844}, "device_scale_factor": 2, "is_mobile": True} if mobile \
            else {"viewport": {"width": 1440, "height": 900}}
        pg = b.new_page(**vp)
        try:
            pg.goto(url, wait_until="networkidle", timeout=45000)
        except Exception:
            pg.goto(url, wait_until="load", timeout=45000)
        pg.wait_for_timeout(2500)
        text = pg.evaluate("document.body ? document.body.innerText.slice(0, 3000) : ''")
        if pg.query_selector("iframe[src*='challenges.cloudflare.com']"):   # the checkbox lives in this iframe
            text += " verify you are human"
        if WALL.search(text) and len(text) < 1500:
            sys.exit(f"{url} answered with a bot wall ({WALL.search(text).group(0)!r}); set look.url to another page "
                     f"or look.image to a saved picture of the result")
        pg.evaluate(HIDE_OVERLAYS)
        pg.evaluate(f"window.scrollTo(0,{0 if mobile else int(crop_y)})")
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(out))
    finally:
        b.close(); p.stop()


def data_uri(img_or_path, fmt="JPEG"):
    im = Image.open(img_or_path) if not isinstance(img_or_path, Image.Image) else img_or_path
    buf = io.BytesIO(); im.convert("RGB").save(buf, fmt, quality=90)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def page_html(band, fields, pal):
    spec = BANDS[band]
    css = BASE_CSS + spec.get("css", "")
    body = spec["html"]
    for k, v in {**pal, **fields}.items():
        css, body = css.replace("{%s}" % k, v), body.replace("{%s}" % k, v)
    return (f"<!doctype html><html><head><meta charset=utf-8><link href='{FONTS}' rel=stylesheet>"
            f"<style>{css}</style></head><body>{body}</body></html>")


def render_png(pages):
    """pages: list of (html, out_path). Returns the fit report for each."""
    p, b = browser()
    reports = []
    try:
        pg = b.new_page(viewport={"width": TW, "height": TH})
        for doc, out in pages:
            pg.set_content(doc, wait_until="networkidle")
            pg.evaluate("document.fonts.ready.then(()=>1)")
            pg.wait_for_timeout(300)
            rep = pg.evaluate(FIT_JS)
            pg.screenshot(path=str(out))
            reports.append(rep)
    finally:
        b.close(); p.stop()
    return reports


def fit_ok(rep):
    return all(not (r["overflow"] or r["offcanvas"] or r["covers_image"]) for r in rep)


# ---------------------------------------------------------------- sameness
def cells(path_or_img):
    im = path_or_img if isinstance(path_or_img, Image.Image) else Image.open(path_or_img)
    return np.asarray(im.convert("RGB").resize(GRID, Image.BOX), float)


def shared(a, b):
    """Share of the frame (32x18 cells) whose average colour matches within 30 RGB units. 0 = nothing alike."""
    return float((np.linalg.norm(a - b, axis=2) < CLOSE).mean())


def closest(img, exclude_slug):
    c = cells(img)
    best = (0.0, None)
    for f in sorted(Path("jobs").glob("*/thumbnail.png")):
        if f.parent.name == exclude_slug:
            continue
        s = shared(c, cells(f))
        best = max(best, (s, f.parent.name))
    return best


# ---------------------------------------------------------------- ledger
def ledger():
    return json.loads(LEDGER.read_text()) if LEDGER.exists() else {}


def recent_bands(led, before_slug=None, n=REPEAT_WINDOW):
    items = sorted(led.items(), key=lambda kv: kv[1]["date"])
    if before_slug in led:
        items = [kv for kv in items if kv[1]["date"] < led[before_slug]["date"]]
    return [v["band"] for _, v in items[-n:]]


# ---------------------------------------------------------------- job fields
def job_fields(jobdir):
    job = json.loads((jobdir / "job.json").read_text())
    look = job.get("look", {})
    first_web = next((s["shot"].get("url") for s in job["segments"] if s["shot"]["type"] == "web"), None)
    return job, look, {
        "TOP": look.get("top", job.get("thumb_top", job.get("tool", ""))).upper(),
        "BIG": look.get("big", job.get("thumb_big", "")),
        "BADGE": look.get("badge", job.get("thumb_badge", "JUST LAUNCHED")),
        "PROMPT": look.get("prompt", ""), "STAT": look.get("stat", ""), "STAT_LABEL": look.get("stat_label", ""),
        "FOCUS": look.get("focus", ""),
    }, look.get("image") or None, look.get("url") or job.get("thumb_url") or first_web, look.get("crop_y", job.get("thumb_crop_y", 0))


def source_image(jobdir, image, url, crop_y, mobile=False):
    """The picture a look is built from: look.image (look.image_mobile for the phone band) or a capture of the url."""
    if image:
        return Image.open(jobdir / image if not Path(image).is_absolute() else image).convert("RGB")
    cap = jobdir / ("_look_cap_mobile.png" if mobile else "_look_cap.png")
    if not cap.exists():
        if not url:
            sys.exit(f"{jobdir}: no look.image, look.url, thumb_url or web shot to build the thumbnail from")
        capture(url, cap, crop_y, mobile)
    return Image.open(cap).convert("RGB")


def eligible(fields):
    return [b for b, s in BANDS.items() if all(fields.get(k.upper()) for k in s["needs"])]


def build(jobdir, band, fields, img, accent, out):
    pal = palette(accent, BAND_BG[band])
    f = {k: html.escape(v) for k, v in fields.items()}
    f.update(IMG=data_uri(img), MARK=data_uri(MARK, "PNG") if MARK.exists() else "")
    return page_html(band, f, pal), out


def cmd_render(a):
    jobdir = Path(a.job); slug = jobdir.name
    job, look, fields, image, url, crop_y = job_fields(jobdir)
    img = source_image(jobdir, image, url, crop_y)
    fields["FOCUS"] = fields["FOCUS"] or busy_focus(img)
    led = ledger()
    recent = recent_bands(led, slug if slug in led else None)
    prev_accents = [v["accent"] for _, v in sorted(led.items(), key=lambda kv: kv[1]["date"])[-3:]]
    accent = look.get("accent") or brand_accent(img)
    near = lambda x, y: np.linalg.norm(np.subtract(hexrgb(x), hexrgb(y))) < 60
    if not look.get("accent") and (not accent or any(near(accent, p) for p in prev_accents)):
        accent = next(c for c in ACCENTS if not any(near(c, p) for p in prev_accents))   # the last 3 looks' colours stay unused
    ok_bands = [b for b in eligible(fields) if b not in recent]
    if a.band:
        if a.band not in BANDS:
            sys.exit(f"unknown band {a.band}; see `looks.py bands`")
        if a.band not in eligible(fields):
            sys.exit(f"band {a.band} needs look.{', look.'.join(BANDS[a.band]['needs'])}")
        if a.band in recent and not a.force:
            sys.exit(f"band {a.band} was used in the last {REPEAT_WINDOW} thumbnails ({recent}); pick another")
        cands = [a.band]
    else:
        never = [b for b in ok_bands if b not in [v["band"] for v in led.values()]]
        cands = (never + [b for b in ok_bands if b not in never])[:a.candidates if not a.auto else len(ok_bands)]
    phone_img = lambda: source_image(jobdir, look.get("image_mobile") or image, url, crop_y, mobile=True)
    pages = [build(jobdir, b, fields, phone_img() if b == "phone" else img, accent, jobdir / f"_look_{b}.png") for b in cands]
    reps = render_png(pages)
    rows = []
    for b, rep in zip(cands, reps):
        s, who = closest(jobdir / f"_look_{b}.png", slug)
        rows.append(dict(band=b, fit=fit_ok(rep), shared=round(s, 3), closest=who, report=rep))
        print(f"{b:8s} fit={'ok' if fit_ok(rep) else 'FAIL'}  shared={s:.2f} with {who}  "
              f"title={next((r['size'] for r in rep if r['min'] >= 56), '-')}px")
    if a.band or a.auto:
        good = [r for r in rows if r["fit"] and r["shared"] < LIMIT]
        if not good:
            sys.exit("no candidate passes fit + sameness; shorten the title or set look.focus / look.image")
        pick = min(good, key=lambda r: r["shared"])
        Image.open(jobdir / f"_look_{pick['band']}.png").save(jobdir / "thumbnail.png")
        led[slug] = dict(band=pick["band"], accent=accent, date=datetime.datetime.now().isoformat(timespec="seconds"),
                         fit=pick["fit"], shared=pick["shared"], closest=pick["closest"])
        LEDGER.parent.mkdir(exist_ok=True)
        LEDGER.write_text(json.dumps(led, indent=1) + "\n")
        print(f"THUMB {jobdir/'thumbnail.png'} band={pick['band']} shared={pick['shared']:.2f}")
    else:
        sheet(jobdir, rows)


def sheet(jobdir, rows, prefix="_look_"):
    w, h, cols = 640, 360, 3
    s = Image.new("RGB", (w * min(cols, len(rows)), (h + 40) * -(-len(rows) // cols)), "white")
    d = ImageDraw.Draw(s)
    for i, r in enumerate(rows):
        x, y = (i % cols) * w, (i // cols) * (h + 40)
        s.paste(Image.open(Path(jobdir) / f"{prefix}{r['band']}.png").resize((w, h)), (x, y))
        d.text((x + 10, y + h + 12), f"{r['band']}  fit {'ok' if r['fit'] else 'FAIL'}  shared {r['shared']:.2f}", fill="black")
    s.save(jobdir / "_looks_sheet.png")
    print("SHEET", jobdir / "_looks_sheet.png")


def cmd_check(a):
    led, passed = ledger(), 0
    for j in a.jobs:
        jobdir = Path(j); slug = jobdir.name; errs = []
        if not (jobdir / "thumbnail.png").exists():
            errs.append("no thumbnail.png")
        elif slug not in led:
            errs.append("not made with looks.py (no data/looks.json entry)")
        else:
            s, who = closest(jobdir / "thumbnail.png", slug)
            if s >= LIMIT:
                errs.append(f"shares {s:.2f} of its frame with {who} (limit {LIMIT})")
            if led[slug]["band"] in recent_bands(led, slug):
                errs.append(f"band {led[slug]['band']} repeats within the last {REPEAT_WINDOW}")
            if not led[slug]["fit"]:
                errs.append("text did not fit")
        print(f"{slug}: {'ok' if not errs else '; '.join(errs)}")
        passed += not errs
    print(f"CHECK_{'PASS' if passed == len(a.jobs) else 'FAIL'} {passed}/{len(a.jobs)}")
    sys.exit(0 if passed == len(a.jobs) else 1)


def cmd_control(a):
    led = ledger()
    old = [f for f in sorted(Path("jobs").glob("*/thumbnail.png")) if f.parent.name not in led]
    C = [cells(f) for f in old]
    pairs = [shared(C[i], C[j]) for i, j in itertools.combinations(range(len(C)), 2)]
    flagged = sum(p >= LIMIT for p in pairs)
    print(f"{len(old)} template thumbnails, {flagged}/{len(pairs)} pairs at or over {LIMIT} shared "
          f"(lowest {min(pairs):.2f})")
    ok = len(pairs) >= 10 and flagged / len(pairs) >= 0.95
    print("CONTROL_OK" if ok else "CONTROL_FAIL")
    sys.exit(0 if ok else 1)


def cmd_selftest(a):
    from tempfile import TemporaryDirectory
    g = np.zeros((900, 1440, 3), np.uint8)
    g[..., 0] = np.linspace(30, 220, 1440)[None, :]; g[..., 2] = np.linspace(200, 40, 900)[:, None]
    g[200:500, 300:900] = (250, 250, 250); g[560:640, 300:1200] = (40, 40, 40)
    img = Image.fromarray(g)
    real = dict(TOP="HIGGSFIELD CONTENT FACTORY", BIG="1 LINE → FULL VIDEO", BADGE="JUST LAUNCHED",
                PROMPT="What if cats ran the morning news? Make it a 60 second faceless video", STAT="55",
                STAT_LABEL="LANGUAGES", FOCUS="50% 20%")
    absurd = dict(real, BIG="THIS TITLE IS FAR TOO LONG TO EVER FIT ON ANY THUMBNAIL AT A SIZE A PHONE CAN READ OK")
    ok = True
    with TemporaryDirectory() as t:
        t = a.out or t
        for name, fields, want in (("real", real, True), ("absurd", absurd, False)):
            pages = [build(Path(t), b, fields, img, "#2f6bff", Path(t) / f"{name}_{b}.png") for b in BANDS]
            for b, rep in zip(BANDS, render_png(pages)):
                good = fit_ok(rep)
                bad = [r for r in rep if r["overflow"] or r["offcanvas"] or r["covers_image"]]
                print(f"{name:6s} {b:8s} fit={'ok' if good else 'FAIL'} {bad[:1] if bad and want else ''}")
                ok &= good if want else (not good)
    if a.out:   # a sheet of every band with the real title, to look at
        sheet(Path(a.out), [dict(band=b, fit=True, shared=0.0) for b in BANDS], prefix="real_")
    print("SELFTEST_OK" if ok else "SELFTEST_FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render"); r.add_argument("job"); r.add_argument("--band"); r.add_argument("--auto", action="store_true")
    r.add_argument("--candidates", type=int, default=3); r.add_argument("--force", action="store_true")
    c = sub.add_parser("check"); c.add_argument("jobs", nargs="+")
    sub.add_parser("control"); sub.add_parser("bands")
    t = sub.add_parser("selftest"); t.add_argument("--out", help="keep the renders here and write a sheet")
    a = ap.parse_args()
    if a.cmd == "bands":
        for b, s in BANDS.items():
            print(f"{b:8s} {BAND_BG[b]:6s} needs={','.join(s['needs']) or '-':12s} {s['note']}")
        return
    if not Path("jobs").is_dir():
        sys.exit("run from the Dayone-ai repo root")
    {"render": cmd_render, "check": cmd_check, "control": cmd_control, "selftest": cmd_selftest}[a.cmd](a)


if __name__ == "__main__":
    main()
