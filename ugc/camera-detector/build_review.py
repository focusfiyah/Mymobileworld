"""Review page for Ralph (newest on top). python3 build_review.py -> review/index.html (images in review/img/)."""
import json, html, re
from pathlib import Path
from PIL import Image
D = json.loads(Path("shots.json").read_text()); SH = D["shots"]; E = html.escape
book = Path("BOOK.md").read_text()
script = re.search(r"## 3\. Script.*?\n(1\. .*?)\nWhy:", book, re.S).group(1).strip().splitlines()
qs = re.search(r"## 7\. Questions\n(.*?)\n\n## ", book, re.S).group(1).strip().splitlines()
total = re.search(r"TOTAL: \$([0-9.]+)", book).group(1)
IMG = Path("review/img"); IMG.mkdir(parents=True, exist_ok=True)
ROOMS = {"rooms/roomA_hotel_colour_art.jpg": "colourful hotel room", "rooms/roomB_navy_tile_bathroom.jpg": "navy tile bathroom",
         "rooms/roomC_gold_lever_door.jpg": "gold lever door", "rooms/roomD_red_wallpaper_teal_nightstand.jpg": "teal nightstand",
         "rooms/roomE_bedroom_colour_pillows.jpg": "colourful pillows bedroom", "rooms/roomF_vessel_sink_bathroom.jpg": "vessel sink bathroom"}
REAL = sorted(Path("ref/real").glob("*.jpg"))
for name, src, w in [("sheet", "refs/product_sheet.png", 1400), ("ex1", "research/coach/inspo/7680943338752609549/sheet.png", 1200),
                     ("ex2", "research/coach/inspo/7693104034340818207/sheet.png", 1200), ("hand_with", "../../grace/ref/hand-sheets/with_bracelet.jpg", 800),
                     ("hand_without", "../../grace/ref/hand-sheets/without_bracelet.jpg", 800)] + \
                    [(Path(k).stem, k, 600) for k in ROOMS] + [("real_" + p.stem, str(p), 700) for p in REAL]:
    im = Image.open(src).convert("RGB"); im.thumbnail((w, w * 2)); im.save(IMG / f"{name}.jpg", quality=86)
def chip(s):
    c = f"<span class=\"chip {'free' if not s['hand'] else ''}\">{'HAND' if s['hand'] else 'HAND-FREE'}</span>"
    c += f"<span class=\"chip\">{'free edit of S2' if s.get('free') else ('Seedance on Kie' if s.get('no_product') else 'Flow first')}</span>"
    c += f"<span class=\"chip\">{ROOMS[s['room']]}</span>"
    if s['id'] == 'S4': c += '<span class="chip warn">riskiest: made first</span>'
    return c
def body(s):
    if s.get("free"): return f"<p class=\"see\">{E(s['note'])}</p>"
    return (f"<p class=\"see\">{E(s['still'])}</p><p class=\"mv\"><b>Motion:</b> {E(s['motion'])}</p>"
            f"<details><summary>Full still prompt</summary><pre>{E(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>"
            f"<details><summary>Full clip prompt</summary><pre>{E(Path('prompts/'+s['id']+'.txt').read_text())}</pre></details>")
shots = "".join(f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span><span class="t">{s['t'][0]:.1f}&ndash;{s['t'][1]:.1f} s</span>{chip(s)}</div>
<div class="shb"><img src="img/{Path(s['room']).stem}.jpg" alt="{ROOMS[s['room']]} room photo" loading="lazy"><div class="tx">
<p class="say">&ldquo;{E(s['words'])}&rdquo;</p>{body(s)}</div></div></article>""" for s in SH)
cost_rows = re.search(r"\| Item \| Qty x unit \| \$ \|\n\|---\|---\|---\|\n(.*?)\nExpected", book, re.S).group(1).strip().splitlines()
cost = "".join("<tr>" + "".join(f"<td>{E(c.strip())}</td>" for c in r.strip('|').split('|')) + "</tr>" for r in cost_rows)
note = re.search(r"(Expected spend with Flow:.*?)\nMonth so far.*?: (.*?)\n", book, re.S)
script_html = "".join(f"<li>{E(l.split('. ',1)[1])}</li>" for l in script)
q_html = "".join(f"<li>{E(q.split('. ',1)[1])}</li>" for q in qs)
real_html = "".join(f'<figure><img src="img/real_{p.stem}.jpg" alt="{p.stem.replace("_"," ")}" loading="lazy"><figcaption>{p.stem.replace("_"," ")}</figcaption></figure>' for p in REAL)
STORY = (Path("review/cut.html").read_text() if Path("review/cut.html").exists() else "") + (Path("review/storyboard.html").read_text() if Path("review/storyboard.html").exists() else "")
page = f"""<title>Camera Detector Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700;800&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
/* One reading column. The detector's own palette: matte black ink, the teal-green filter glass as the accent, LED red only for what needs Ralph. */
:root {{ --bg:#f4f5f4; --card:#ffffff; --ink:#151617; --mute:#5c6166; --line:#d8dbda; --glass:#e3f2ef; --teal:#127a6d; --led:#d6362c; --ledink:#ffffff; --ok:#127a6d;
  --body:"Archivo", system-ui, -apple-system, sans-serif; --mono:"IBM Plex Mono", ui-monospace, Menlo, monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#111213; --card:#1b1d1e; --ink:#eceeed; --mute:#a2a8ac; --line:#303436; --glass:#17302c; --teal:#5fd0bf; --led:#ff5a4f; --ledink:#1a0303; --ok:#5fd0bf; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#111213; --card:#1b1d1e; --ink:#eceeed; --mute:#a2a8ac; --line:#303436; --glass:#17302c; --teal:#5fd0bf; --led:#ff5a4f; --ledink:#1a0303; --ok:#5fd0bf; color-scheme:dark }}
body {{ background:var(--bg); color:var(--ink); font:16px/1.55 var(--body); margin:0; }}
.wrap {{ max-width:860px; margin:0 auto; padding-block:28px 64px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:28px; }}
h1,h2 {{ font-weight:800; text-wrap:balance; margin:0; letter-spacing:-.01em; }}
h1 {{ font-size:clamp(28px,6vw,42px); line-height:1.08; }}
h2 {{ font-size:20px; text-transform:uppercase; letter-spacing:.04em; }}
.eyebrow {{ font:500 12px/1 var(--body); letter-spacing:.12em; text-transform:uppercase; color:var(--mute); }}
section {{ display:grid; gap:12px; }}
p {{ margin:0; max-width:68ch; }}
.ask {{ background:var(--led); color:var(--ledink); padding:14px 16px; border-radius:8px; display:grid; gap:6px; }}
.ask b {{ font-size:18px; }}
.flag {{ background:var(--glass); border-left:4px solid var(--teal); padding:12px 14px; border-radius:6px; }}
.chip {{ font:500 12px/1 var(--body); padding:5px 8px; border:1px solid var(--line); border-radius:999px; color:var(--mute); background:var(--card); }}
.chip.free {{ border-color:var(--ok); color:var(--ok); }}
.chip.warn {{ background:var(--led); color:var(--ledink); border-color:var(--led); }}
ol.script {{ margin:0; padding-left:22px; display:grid; gap:6px; font-size:17px; }}
ol.q {{ margin:0; padding-left:22px; display:grid; gap:10px; }}
.grid2 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr)); gap:12px; }}
.grid3 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr)); gap:10px; }}
figure {{ margin:0; display:grid; gap:4px; }} figure img {{ width:100%; border-radius:4px; border:1px solid var(--line); display:block; }}
figcaption {{ font-size:13px; color:var(--mute); }}
.shot {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:14px; display:grid; gap:10px; }}
.sh {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }}
.num {{ font-weight:800; font-size:22px; margin-right:4px; }} .t {{ font:12px var(--mono); color:var(--mute); margin-right:6px; font-variant-numeric:tabular-nums; }}
.shb {{ display:grid; grid-template-columns:110px 1fr; gap:12px; }} .shb img {{ width:110px; border-radius:4px; }} .tx {{ min-width:0; display:grid; gap:6px; }}
.say {{ font-size:17px; font-weight:500; }} .see,.mv {{ color:var(--mute); font-size:15px; }}
details summary {{ cursor:pointer; font-size:14px; color:var(--ink); }} details summary:focus-visible {{ outline:2px solid var(--teal); outline-offset:2px; }}
pre {{ white-space:pre-wrap; font:12.5px/1.5 var(--mono); background:var(--glass); padding:10px; border-radius:4px; overflow-x:auto; margin:6px 0 0; }}
.tbl {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; font-variant-numeric:tabular-nums; font-size:15px; }}
td {{ border-bottom:1px solid var(--line); padding:8px 6px; vertical-align:top; }} td:last-child {{ text-align:right; white-space:nowrap; }}
.total {{ font-weight:800; font-size:30px; font-variant-numeric:tabular-nums; }}
.note {{ color:var(--mute); font-size:14px; }}
@media (max-width:480px) {{ .shb {{ grid-template-columns:1fr; }} .shb img {{ width:100%; max-width:220px; }} }}
</style>
<div class="wrap">
<header style="display:grid;gap:8px"><span class="eyebrow">Grace &middot; plan &middot; 2026-10-28 &middot; nothing spent yet</span>
<h1>Hidden Camera Detector, black</h1>
<p>Hands + hand-free AI video over Grace's cloned voice, about 34 s, 11 shots, no face. The hook shows the one thing none of the winners show: how to use it. Look through the window and a hidden lens shines back as a red dot.</p></header>
<div class="ask"><b>Your OK on the plan + 7 quick answers</b><span>TOTAL ${total} (expected about $1.41 with Flow). No paid call runs before your OK.</span></div>
{STORY}
<section><h2>Questions</h2><ol class="q">{q_html}</ol></section>
<section><h2>Script, Grace cloned v5</h2><ol class="script">{script_html}</ol>
<p class="note">Hook H105 from Grace's library (options B H028, C H132 in research/hooks.md). Reading grade 4.9. Gate: GATE OK. No price, no on-screen text, no "order it now". Caption: Nobody shows you this part 👀 Look through the little window and a hidden lens shines back red. Then hang it on the door at night. #ad #cameradetector #travelsafety #hotelsafety #airbnb #tiktokshopfinds</p>
<div class="flag"><b>Flag:</b> both your examples say it beeps the second it finds a camera. Nothing on the box or listing backs that, and buyers ask "why does mine not beep?" (the listing sits at 3.7 stars, mostly from people who never looked through the window). Our script never claims it.</div></section>
<section><h2>Your examples</h2><div class="grid2">
<figure><img src="img/ex1.jpg" alt="Contact sheet of example 1"><figcaption>Example 1, 191.5K: bathroom, the red view through the window, hung on the door</figcaption></figure>
<figure><img src="img/ex2.jpg" alt="Contact sheet of example 2"><figcaption>Example 2, 15.9K: hotel room, red pinpoint, door handle</figcaption></figure></div></section>
<section><h2>Real product</h2><figure><img src="img/sheet.jpg" alt="Product reference sheet from Grace's own unit"><figcaption>Reference sheet from your photos of Grace's black unit. The listing renders show a purple window; the real one is teal-green, so the real photos win. Size from the listing: 4.29 x 1.61 x 0.71 in with the loop, 50 g.</figcaption></figure>
<details><summary>Your 7 photos, saved in ugc/camera-detector/ref/real/</summary><div class="grid3" style="margin-top:10px">{real_html}</div></details></section>
<section><h2>Shots</h2>{shots}</section>
<section><h2>Hand</h2><div class="grid3">
<figure><img src="img/hand_without.jpg" alt="Hand sheet without bracelet"><figcaption>Without bracelet (default, as HEVEBLUE)</figcaption></figure>
<figure><img src="img/hand_with.jpg" alt="Hand sheet with bracelet"><figcaption>With bracelet</figcaption></figure></div></section>
<section><h2>Cost</h2><div class="tbl"><table>{cost}</table></div><p class="total">TOTAL ${total}</p>
<p class="note">{E(note.group(1))} Month so far {E(note.group(2))}.</p></section>
</div>"""
Path("review/index.html").write_text(page); print("ok", len(page))
