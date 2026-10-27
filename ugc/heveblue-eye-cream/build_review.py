"""Review page for Ralph (newest on top). python3 build_review.py -> review/index.html (images in review/img/)."""
import json, html, re
from pathlib import Path
from PIL import Image
D = json.loads(Path("shots.json").read_text()); SH = D["shots"]; E = html.escape
book = Path("BOOK.md").read_text()
script = re.search(r"V1, recommended:\n(.*?)\nWhy:", book, re.S).group(1).strip().splitlines()
qs = re.search(r"## 7\. Questions\n(.*?)\n\n## 8", book, re.S).group(1).strip().splitlines()
total = re.search(r"TOTAL: \$([0-9.]+)", book).group(1)
IMG = Path("review/img"); IMG.mkdir(parents=True, exist_ok=True)
ROOMS = {"rooms/roomA_sage_bathroom.jpg": "sage tile bathroom", "rooms/roomB_pink_bathroom.jpg": "pink tile bathroom", "rooms/roomC_bedroom_vanity.jpg": "bright bedroom vanity",
         "rooms/roomD_fireplace.jpg": "fireplace stockings", "rooms/roomE_marble_counter.jpg": "marble counter", "rooms/roomF_teal_vanity.jpg": "teal wall vanity"}
for name, src, w in [("sheet", "refs/product_sheet.png", 1400), ("inspo", "research/coach/inspo/7680831216869821710/hook.png", 1200),
                     ("maddy", "research/coach/top/7690713735131909407/hook.png", 1200), ("hand_with", "../../grace/ref/hand-sheets/with_bracelet.jpg", 800),
                     ("hand_without", "../../grace/ref/hand-sheets/without_bracelet.jpg", 800), ("face", "refs/grace_face.jpg", 500)] + \
                    [(Path(k).stem, k, 600) for k in ROOMS]:
    im = Image.open(src).convert("RGB"); im.thumbnail((w, w * 2)); im.save(IMG / f"{name}.jpg", quality=86)
shots = "".join(f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span><span class="t">{s['t'][0]:.1f}&ndash;{s['t'][1]:.1f} s</span>
<span class="chip {'free' if not s['hand'] else ''}">{'HAND' if s['hand'] else 'HAND-FREE'}</span>{'<span class="chip">face crop, no mouth</span>' if s['face'] else ''}<span class="chip">{'Seedance on Kie' if s.get('no_product') else 'Flow first'}</span><span class="chip">{ROOMS[s['room']]}</span>{'<span class="chip warn">riskiest: made first</span>' if s['id']=='S1' else ''}</div>
<div class="shb"><img src="img/{Path(s['room']).stem}.jpg" alt="{ROOMS[s['room']]} room photo" loading="lazy"><div class="tx">
<p class="say">&ldquo;{E(s['words'])}&rdquo;</p><p class="see">{E(s['see'])}</p><p class="mv"><b>Motion:</b> {E(s['motion'])}</p>
<details><summary>Full still prompt</summary><pre>{E(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>
<details><summary>Full clip prompt</summary><pre>{E(Path('prompts/'+s['id']+'.txt').read_text())}</pre></details></div></div></article>""" for s in SH)
cost_rows = re.search(r"\| Item \| Qty x unit \| \$ \|\n\|---\|---\|---\|\n(.*?)\nExpected", book, re.S).group(1).strip().splitlines()
cost = "".join("<tr>" + "".join(f"<td>{E(c.strip())}</td>" for c in r.strip('|').split('|')) + "</tr>" for r in cost_rows)
note = re.search(r"(Expected spend with Flow:.*?)\nMonth so far.*?: (.*?)\n", book, re.S)
script_html = "".join(f"<li>{E(l.split('. ',1)[1])}</li>" for l in script)
q_html = "".join(f"<li>{E(q.split('. ',1)[1])}</li>" for q in qs)
STORY = Path("review/storyboard.html").read_text() if Path("review/storyboard.html").exists() else ""
page = f"""<title>HEVEBLUE Eye Cream Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gilda+Display&family=Work+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
/* Layout: one reading column; a chrome-and-ink plan sheet, the tube's black serif caps as the display voice, yuja yellow only for what needs Ralph */
:root {{ --bg:#f6f6f3; --card:#ffffff; --ink:#1d1f22; --mute:#5f6469; --line:#d9dbd7; --chrome:#e9ebec; --yuja:#e7b416; --yujaink:#5a4300; --ok:#2f6b4f;
  --display:"Gilda Display", Georgia, "Times New Roman", serif; --body:"Work Sans", system-ui, -apple-system, sans-serif; --mono:"IBM Plex Mono", ui-monospace, Menlo, monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#141517; --card:#1d1f22; --ink:#ecedee; --mute:#a3a8ad; --line:#33363a; --chrome:#26292d; --yuja:#f0c53a; --yujaink:#1d1600; --ok:#7fc4a2; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#141517; --card:#1d1f22; --ink:#ecedee; --mute:#a3a8ad; --line:#33363a; --chrome:#26292d; --yuja:#f0c53a; --yujaink:#1d1600; --ok:#7fc4a2; color-scheme:dark }}
body {{ background:var(--bg); color:var(--ink); font:16px/1.55 var(--body); }}
.wrap {{ max-width:860px; margin:0 auto; padding-block:28px 64px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:28px; }}
h1,h2 {{ font-family:var(--display); font-weight:400; text-wrap:balance; margin:0; letter-spacing:.02em; }}
h1 {{ font-size:clamp(28px,6vw,40px); text-transform:uppercase; line-height:1.15; }}
h2 {{ font-size:22px; text-transform:uppercase; }}
.eyebrow {{ font:500 12px/1 var(--body); letter-spacing:.12em; text-transform:uppercase; color:var(--mute); }}
section {{ display:grid; gap:12px; }}
p {{ margin:0; max-width:68ch; }}
.ask {{ background:var(--yuja); color:var(--yujaink); padding:14px 16px; border-radius:6px; display:grid; gap:6px; }}
.ask b {{ font-size:18px; }}
.chips {{ display:flex; flex-wrap:wrap; gap:6px; }}
.chip {{ font:500 12px/1 var(--body); padding:5px 8px; border:1px solid var(--line); border-radius:999px; color:var(--mute); background:var(--card); }}
.chip.free {{ border-color:var(--ok); color:var(--ok); }}
.chip.warn {{ background:var(--yuja); color:var(--yujaink); border-color:var(--yuja); }}
ol.script {{ margin:0; padding-left:22px; display:grid; gap:6px; font-size:17px; }}
ol.q {{ margin:0; padding-left:22px; display:grid; gap:10px; }}
.grid2 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr)); gap:12px; }}
.grid3 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr)); gap:10px; }}
figure {{ margin:0; display:grid; gap:4px; }} figure img {{ width:100%; border-radius:4px; border:1px solid var(--line); display:block; }}
figcaption {{ font-size:13px; color:var(--mute); }}
.shot {{ background:var(--card); border:1px solid var(--line); border-radius:6px; padding:14px; display:grid; gap:10px; }}
.sh {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }}
.num {{ font-family:var(--display); font-size:22px; margin-right:4px; }} .t {{ font:12px var(--mono); color:var(--mute); margin-right:6px; font-variant-numeric:tabular-nums; }}
.shb {{ display:grid; grid-template-columns:110px 1fr; gap:12px; }} .shb img {{ width:110px; border-radius:4px; }} .tx {{ min-width:0; display:grid; gap:6px; }}
.say {{ font-size:17px; font-weight:500; }} .see,.mv {{ color:var(--mute); font-size:15px; }}
details summary {{ cursor:pointer; font-size:14px; color:var(--ink); }} details summary:focus-visible {{ outline:2px solid var(--yuja); outline-offset:2px; }}
pre {{ white-space:pre-wrap; font:12.5px/1.5 var(--mono); background:var(--chrome); padding:10px; border-radius:4px; overflow-x:auto; margin:6px 0 0; }}
.tbl {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; font-variant-numeric:tabular-nums; font-size:15px; }}
td {{ border-bottom:1px solid var(--line); padding:8px 6px; vertical-align:top; }} td:last-child {{ text-align:right; white-space:nowrap; }}
.total {{ font-family:var(--display); font-size:30px; }}
.note {{ color:var(--mute); font-size:14px; }}
@media (max-width:480px) {{ .shb {{ grid-template-columns:1fr; }} .shb img {{ width:100%; max-width:220px; }} }}
</style>
<div class="wrap">
<header style="display:grid;gap:8px"><span class="eyebrow">Grace &middot; plan &middot; 2026-10-27 &middot; nothing spent yet</span>
<h1>Black Yuja Bean Lifting Auto Eye Cream</h1>
<p>Hands + hand-free AI video over Grace's cloned voice, about 34 s, 10 shots. Opens like the two biggest videos for this exact tube: the chrome tip touches a glass of water and the rings show the buzz.</p></header>
<div class="ask"><b>Approve the plan? Total ${total}</b><span>Expected with your Flow app: {re.search(r'\$[0-9.]+[0-9]', note.group(1)).group(0)}. Answer the 7 questions below (defaults are marked).</span></div>
{STORY}
<section><h2>Questions</h2><ol class="q">{q_html}</ol></section>
<section><h2>Script, Grace cloned voice</h2><ol class="script">{script_html}</ol>
<p class="note">Hook H094 from Grace's library (options B H077, C H099 in research/hooks.md). Reading grade 2.6. Gate: GATE OK. No price, no on-screen text, no "order it now". Caption: Hear that? It turns on by itself 👀 Yuja water, black bean and collagen, with a massage tip built in. #ad #heveblue #eyecream #kbeauty #koreanskincare #tiktokshopfinds</p></section>
<section><h2>The opener we copy</h2><div class="grid2">
<figure><img src="img/maddy.jpg" alt="First 3 seconds of the 1.8M video"><figcaption>@maddybeautyfinds, 1.8M views: tip in a glass of water at frame 0</figcaption></figure>
<figure><img src="img/inspo.jpg" alt="First 3 seconds of your inspo video"><figcaption>Your idea, @momfindsbyfaith, 730K: tip in a jar of water</figcaption></figure></div></section>
<section><h2>Real product</h2><figure><img src="img/sheet.jpg" alt="Product reference sheet from the real listing photos"><figcaption>Reference sheet, real listing pixels only. Size about 16 x 2 cm is my estimate: no maker dimensions online.</figcaption></figure></section>
<section><h2>Shots</h2>{shots}</section>
<section><h2>Hand and face</h2><div class="grid3">
<figure><img src="img/hand_with.jpg" alt="Hand sheet with bracelet"><figcaption>With bracelet (default)</figcaption></figure>
<figure><img src="img/hand_without.jpg" alt="Hand sheet without bracelet"><figcaption>Without bracelet</figcaption></figure>
<figure><img src="img/face.jpg" alt="Grace face reference crop"><figcaption>Face reference, for skin, brows and eye only</figcaption></figure></div></section>
<section><h2>Cost</h2><div class="tbl"><table>{cost}</table></div><p class="total">TOTAL ${total}</p>
<p class="note">{E(note.group(1))} Month so far {E(note.group(2))}.</p></section>
</div>"""
Path("review/index.html").write_text(page); print("ok", len(page))
