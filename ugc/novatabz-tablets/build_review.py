"""Review page for Ralph (newest on top). python3 build_review.py -> review/index.html (+ review/img/*.jpg as published files)."""
import json, html, re
from pathlib import Path
from PIL import Image
E_ = html.escape
SH = json.loads(Path("shots.json").read_text())["shots"]
book = Path("BOOK.md").read_text()
script = [l.split(". ", 1)[1] for l in re.search(r"V1:\n(.*?)\nSource of each", book, re.S).group(1).strip().splitlines()]
qs = [l.split(". ", 1)[1] for l in re.search(r"## 7\. Questions\n(.*?)\n\n## 8", book, re.S).group(1).strip().splitlines()]
total = re.search(r"^TOTAL: \$([0-9.]+)", book, re.M).group(1)
cost_rows = re.search(r"\| Item \| Qty x unit \| \$ \|\n\|---\|---\|---\|\n(.*?)\nExpected", book, re.S).group(1).strip().splitlines()
expected = re.search(r"(Expected spend with Flow.*?)\n", book).group(1)
month = re.search(r"Month so far.*?: (.*?)\n", book).group(1)
ROOMS = {"A": "leaf-wallpaper bathroom", "B": "pink-tile bathroom", "C": "wood vanity + plant", "D": "cream room, suitcases"}
IMG = Path("review/img")
def save(name, src, w):
    im = Image.open(src).convert("RGB"); im.thumbnail((w, w * 2)); im.save(IMG / f"{name}.jpg", quality=86)
save("sheet", "refs/product_sheet.png", 1400)
save("hand", "../../grace/ref/hand-sheets/without_bracelet.jpg", 800)
save("hand_with", "../../grace/ref/hand-sheets/with_bracelet.jpg", 800)
save("winner", "research/coach/top/7680276084679626014/hook.png", 1200)
save("same", "research/videos_novatabz/7692511318053539103/hook.png", 1200)
for k in ROOMS: save(f"room_{k}", f"rooms/room_{k}.jpg", 600)
stills = all(Path(f"stills/{s['id']}.png").exists() for s in SH)
if stills:
    for s in SH: save(f"still_{s['id']}", f"stills/{s['id']}.png", 700)
def shot(s):
    pic = f"still_{s['id']}" if stills else f"room_{s['room']}"
    alt = "still" if stills else f"{ROOMS[s['room']]} room photo"
    chips = f"<span class='chip {'free' if not s['hand'] else ''}'>{'HAND' if s['hand'] else 'HAND-FREE'}</span><span class='chip'>{'Flow / Omni' if s['product'] else 'Seedance on Kie'}</span>{"<span class='chip'>Kling fallback</span>" if s['id'] in ('S1','S5') else ''}<span class='chip' hidden></span><span class='chip'>{ROOMS[s['room']]}</span>" + ("<span class='chip warn'>test clip first</span>" if s['id'] == 'S5' else "")
    return f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span>{chips}</div>
<div class="shb"><img src="img/{pic}.jpg" alt="{alt}" loading="lazy"><div class="tx"><p class="say">&ldquo;{E_(s['words'])}&rdquo;</p><p class="see">{E_(s['see'])}</p>
<details><summary>Still prompt</summary><pre>{E_(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>
<details><summary>Clip prompt</summary><pre>{E_(Path('prompts/clip_'+s['id']+'.txt').read_text())}</pre></details></div></div></article>"""
cost = "".join("<tr>" + "".join(f"<td>{E_(c.strip())}</td>" for c in r.strip('|').split('|')) + "</tr>" for r in cost_rows)
page = f"""<title>NovaTabz Video Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Bodoni:wght@500&family=Figtree:wght@400;500;600&display=swap">
<style>
/* Layout: one reading column, a turquoise-label plan sheet: the jar's serif caps as display, glass-clear neutrals, turquoise only where Ralph acts */
:root {{ --bg:#f3f7f7; --card:#ffffff; --ink:#16282b; --mute:#56696c; --line:#d3e0e1; --teal:#1fb3b8; --tealink:#04383b; --tint:#e2f4f4;
  --display:"Libre Bodoni", Georgia, serif; --body:"Figtree", system-ui, -apple-system, sans-serif; --mono:ui-monospace, Menlo, monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#0f1a1b; --card:#162426; --ink:#e6f0f0; --mute:#9db1b3; --line:#2a3c3e; --teal:#3fc9cd; --tealink:#022426; --tint:#1a3234; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#0f1a1b; --card:#162426; --ink:#e6f0f0; --mute:#9db1b3; --line:#2a3c3e; --teal:#3fc9cd; --tealink:#022426; --tint:#1a3234; color-scheme:dark }}
body {{ background:var(--bg); color:var(--ink); font:16px/1.55 var(--body); }}
.wrap {{ max-width:860px; margin:0 auto; padding-block:28px 64px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:28px; }}
h1,h2 {{ font-family:var(--display); font-weight:500; text-wrap:balance; margin:0; text-transform:uppercase; letter-spacing:.03em; }}
h1 {{ font-size:clamp(28px,6vw,40px); line-height:1.1; }} h2 {{ font-size:21px; }}
.eyebrow {{ font:600 12px/1 var(--body); letter-spacing:.12em; text-transform:uppercase; color:var(--mute); }}
section {{ display:grid; gap:12px; min-width:0; }} p {{ margin:0; max-width:68ch; }}
.ask {{ background:var(--teal); color:var(--tealink); padding:16px; border-radius:6px; display:grid; gap:8px; }}
.ask ol {{ margin:0; padding-left:20px; display:grid; gap:4px; }}
.total {{ font:500 32px/1 var(--display); }}
ol.script {{ margin:0; padding-left:24px; display:grid; gap:6px; font-size:18px; }}
.shot {{ background:var(--card); border:1px solid var(--line); border-radius:6px; padding:12px; display:grid; gap:10px; }}
.sh {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }}
.num {{ font:500 20px/1 var(--display); margin-right:6px; }}
.chip {{ font-size:12px; padding:3px 8px; border-radius:99px; background:var(--tint); color:var(--ink); }}
.chip.free {{ outline:1px solid var(--teal); }} .chip.warn {{ background:var(--teal); color:var(--tealink); }}
.shb {{ display:grid; grid-template-columns:150px 1fr; gap:12px; }} .shb img {{ width:150px; border-radius:4px; object-fit:cover; max-width:100%; }}
.tx {{ min-width:0; display:grid; gap:6px; align-content:start; }} .say {{ font-weight:600; }} .see {{ color:var(--mute); }}
pre {{ white-space:pre-wrap; font:12px/1.5 var(--mono); background:var(--tint); padding:10px; border-radius:4px; overflow-x:auto; }}
summary {{ cursor:pointer; color:var(--mute); font-size:14px; }} summary:focus-visible {{ outline:2px solid var(--teal); }}
.tbl {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; font-size:14px; font-variant-numeric:tabular-nums; }}
td {{ border-bottom:1px solid var(--line); padding:6px 8px 6px 0; vertical-align:top; }}
.pics {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:10px; }} .pics figure {{ margin:0; display:grid; gap:4px; font-size:13px; color:var(--mute); }}
.wide img {{ width:100%; border-radius:4px; }}
@media (max-width:520px) {{ .shb {{ grid-template-columns:1fr; }} .shb img {{ width:100%; }} }}
</style>
<div class="wrap">
<header style="display:grid;gap:8px"><span class="eyebrow">Grace · TikTok Shop · plan v2 (15 s) · 2026-10-30</span><h1>NovaTabz toothpaste tablets</h1>
<p>Hands and hand-free AI video over Grace's cloned voice (v5), 15 s, 6 shots, no on-screen text. Script gate passed: research, hook H099, Humanizer, reading grade 1.8. Kling: up to 80 credits as a fallback for S1 and S5 only, booked in the shared ledger.</p></header>
<section class="ask"><span class="eyebrow" style="color:var(--tealink)">Cut v1 · 15.2 s · 2026-10-30</span><video src="novatabz_v1.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:6px;background:#000"></video><p>Grace cloned v5 voice (echo 150 ms, -17.3 LUFS), no text, AI finish. QC: CUT_QC_OK, edges clean at 2x, REMOVED.md list clear, compare vs the 31.3M winner done. S4 runs on through "No fluoride, no liquid" because S5's clip is clean only for 1.8 s (free fix). Small flaw left: the tiny weight print reads 25G/35G on some frames (real: 23G), only visible on a freeze. Spent $2.67 of $2.71 approved.</p></section>
<section class="ask"><span class="eyebrow" style="color:var(--tealink)">Still storyboard round 2 · 2026-10-30</span><p>Your OK: redo S1, S4, S5, S6 ($0.36). Picks below: S1 round 2 (two-line NOVA TABZ, plain font, small print under the name), S4 round 2 (jar small next to the cup), S5 round 2 (squat jar, label right), S6 round 1 (label exact, jar a little tall; round 2 moved the small print). Spent $0.90 of $2.53. Next: the S5 test clip on Kie Omni ($0.315), then the other 5 clips.</p></section>
<section class="ask"><span class="eyebrow" style="color:var(--tealink)">Your OK + 5 answers</span><div class="total">TOTAL ${total}</div><p>{E_(expected)}</p><ol>{''.join(f'<li>{E_(q)}</li>' for q in qs)}</ol></section>
<section><h2>Script</h2><ol class="script">{''.join(f'<li>{E_(l)}</li>' for l in script)}</ol><p class="see">Where each line comes from: hook H099 + a NovaTabz creator's "yeah, this is toothpaste" + a viewer comment "I've been eating them!"; the how-to from the listing and an Amazon buyer ("Chew a bit and they start to foam"); the facts only from the listing (no whitening or enamel claims). Cut for 15 s: the hydroxyapatite line (now in the caption), the minty-clean line and the month line.</p></section>
<section><h2>Real product</h2><div class="wide"><img src="img/sheet.jpg" alt="NovaTabz product sheet from your 3 photos"></div><p>Clear glass jar 2.17 × 2.17 × 1.65 in, brushed silver ridged screw lid, turquoise label, plain white round tablets. Built only from your photos.</p></section>
<section><h2>Shots</h2>{''.join(shot(s) for s in SH)}</section>
<section><h2>Rooms and hand</h2><div class="pics">{''.join(f'<figure><img src="img/room_{k}.jpg" alt="{v}"><figcaption>{k}: {v} (Pexels)</figcaption></figure>' for k,v in ROOMS.items())}
<figure><img src="img/hand.jpg" alt="Grace hand sheet without bracelet"><figcaption>Hand: without bracelet (my pick)</figcaption></figure><figure><img src="img/hand_with.jpg" alt="Grace hand sheet with bracelet"><figcaption>With bracelet</figcaption></figure></div></section>
<section><h2>What's working on TikTok</h2><div class="wide"><img src="img/winner.jpg" alt="DR.DENT tablets first 3 seconds"></div><p class="see">@nextgenthreads, 31.2M views: result at frame 0, then "chew one and brush like normal".</p>
<div class="wide"><img src="img/same.jpg" alt="NovaTabz creator first 3 seconds"></div><p class="see">@king_okiki15, same product: tube vs tablet, "yeah, this is toothpaste". NovaTabz videos are all under 2K views, so there's room for Grace here.</p></section>
<section><h2>Cost</h2><div class="tbl"><table>{cost}</table></div><p class="see">ElevenLabs about 560 characters. Month so far: {E_(month)}.</p></section>
</div>"""
Path("review/index.html").write_text(page.replace("<span class='chip' hidden></span>", "")); print("ok", len(page))
