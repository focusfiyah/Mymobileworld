"""Builds review/index.html (one review page for the job, newest on top) from shots.json + BOOK.md. python3 -I build_review.py"""
import html, json, os, re
from PIL import Image
e = html.escape
B = open("BOOK.md").read(); S = json.load(open("shots.json"))
os.makedirs("review/img", exist_ok=True)
def thumb(src, dst, w=520):
    im = Image.open(src).convert("RGB"); im.thumbnail((w, w * 2)); im.save("review/img/" + dst, quality=84); return "img/" + dst
room = thumb("rooms/cand/px_6580366.jpg", "room.jpg", 600)
sheet = thumb("refs/product_sheet.png", "sheet.jpg", 1200)
hand = thumb("../../grace/ref/hand-sheets/without_bracelet.jpg", "hand_nobracelet.jpg", 700)
hand2 = thumb("../../grace/ref/hand-sheets/with_bracelet.jpg", "hand_bracelet.jpg", 700)
total = re.search(r"^TOTAL: \$([\d.]+)", B, re.M).group(1)
script = re.search(r"^> (.+)$", B, re.M).group(1)
T = {m.group(1): m.group(2) for m in re.finditer(r"^\| (S\d) \| ([\d.\-]+) \|", B, re.M)}
qs = re.findall(r"^\d\. (.+)$", B.split("## 7.")[1].split("## 8.")[0], re.M)
rows = ""
NOTE = json.load(open('review/notes.json')) if os.path.exists('review/notes.json') else {}
for _s in S:
    if os.path.exists(f'stills/{_s["id"]}.png'): thumb(f'stills/{_s["id"]}.png', f'full_{_s["id"]}.jpg', 768)
for s in S:
    tag = "HAND" if s["hand"] else "HAND-FREE"
    st = f'stills/{s["id"]}.png'
    img = f'<a href="img/full_{s["id"]}.jpg"><img src="{thumb(st, "sb_"+s["id"]+".jpg", 520)}" alt="Still {s["id"]}"></a>' if os.path.exists(st) else f'<div class="ph">still {s["id"]}<br>after your OK</div>'
    rows += f"""<article class="shot">{img}<div class="sb"><div class="meta"><b>{s['id']}</b><span class="pill {'' if s['hand'] else 'hf'}">{tag}</span><span class="pill hf">{"ALL FOUR" if s["group"] else "GREEN ONLY"}</span><span class="t">{T.get(s['id'],'')} s</span></div>
<p class="line">{e(s['label'])}</p><p class="qc">{e(NOTE.get(s['id'], ''))}</p><p class="model">Omni 1.1 Flash on Kie, 4 s &middot; still: Gemini 3 Pro Image</p>
<details><summary>Still prompt</summary><p class="pr">{e(s['still'])}</p></details><details><summary>Clip prompt</summary><p class="pr">{e(s['clip'])}</p></details></div></article>"""
cost = re.findall(r"^\| ([^|]+) \| ([^|]+) \| ([\d.]+) \|$", B, re.M)
crow = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>${c}</td></tr>" for a, b, c in cost)
page = f"""<title>CeraVe Winter Bundle Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600&display=swap">
<style>
/* layout: one phone-width column; plan and total first, then the storyboard cards, then the references */
:root{{--bg:#f4f7fb;--fg:#1a2433;--muted:#5d6b80;--line:#d9e2ee;--card:#ffffff;--blue:#1f63c6;--green:#6aab2e;
--display:"Barlow Condensed","Arial Narrow",sans-serif;--body:"Source Sans 3",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#111722;--fg:#e8eef7;--muted:#9fb0c6;--line:#2a3547;--card:#18202e;--blue:#79a8ff;--green:#9bd165;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#111722;--fg:#e8eef7;--muted:#9fb0c6;--line:#2a3547;--card:#18202e;--blue:#79a8ff;--green:#9bd165;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 48px}}
main{{max-width:760px;margin:0 auto;display:grid;gap:28px}}
h1,h2{{font-family:var(--display);text-wrap:balance;margin:0;letter-spacing:.01em}} h1{{font-size:2.2rem;line-height:1.05;color:var(--blue)}} h2{{font-size:1.4rem}}
.eyebrow{{text-transform:uppercase;letter-spacing:.09em;font-size:.78rem;color:var(--green);font-weight:600}}
section{{display:grid;gap:12px}} p{{margin:0}} .muted{{color:var(--muted)}}
.total{{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:baseline;border-top:3px solid var(--blue);padding-top:12px}}
.total b{{font-family:var(--display);font-size:2.4rem;color:var(--blue);font-variant-numeric:tabular-nums}}
ol.q{{margin:0;padding-left:1.3em;display:grid;gap:8px}}
blockquote{{margin:0;font-size:1.15rem;line-height:1.45;border-left:4px solid var(--green);padding-left:14px}}
table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}} td{{border-bottom:1px solid var(--line);padding:6px 4px;vertical-align:top}} td:last-child{{text-align:right;white-space:nowrap}}
.shot{{display:grid;grid-template-columns:130px 1fr;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}}
.shot img,.ph{{width:130px;border-radius:6px;object-fit:cover;aspect-ratio:9/16}} .ph{{display:grid;place-items:center;text-align:center;font-size:.8rem;color:var(--muted);border:1px dashed var(--line)}}
.sb{{min-width:0;display:grid;gap:6px;align-content:start}}
.meta{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}} .t{{color:var(--muted);font-variant-numeric:tabular-nums;font-size:.9rem}}
.pill{{font-size:.72rem;letter-spacing:.06em;font-weight:600;padding:2px 8px;border-radius:99px;border:1px solid var(--blue);color:var(--blue)}} .pill.hf{{border-color:var(--green);color:var(--green)}}
.line{{font-weight:600}} .qc{{font-size:.92rem;border-left:3px solid var(--blue);padding-left:8px}} .model{{color:var(--muted);font-size:.9rem}}
details summary{{cursor:pointer;color:var(--blue);font-size:.9rem}} .pr{{font-size:.85rem;color:var(--muted);overflow-wrap:anywhere}}
.refs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}} figure{{margin:0;display:grid;gap:4px}} figure img{{border-radius:8px;border:1px solid var(--line)}} figcaption{{font-size:.85rem;color:var(--muted)}}
@media (max-width:420px){{.shot{{grid-template-columns:96px 1fr}} .shot img,.ph{{width:96px}}}}
</style>
<main>
<header><p class="eyebrow">Grace &middot; TikTok Shop &middot; 10 s music-only</p><h1>CeraVe Winter Skin Bundle</h1><p class="muted">Cut v3 ready to compare with v2. Kie $2.47; Kling 100 credits. Tap a still to see it full size.</p></header>
<section><h2>Total</h2><div class="total"><b>${total}</b><span class="muted">Kie, 5 stills + 5 Omni clips + one likely redo. November so far: $1.32 of $100.</span></div>
<table>{crow}</table></section>
<section><h2>Your answers</h2><ol class="q">{''.join(f'<li>{e(q)}</li>' for q in qs)}</ol></section>
<section><h2>Spoken script for later</h2><blockquote>{e(script)}</blockquote><p class="muted">Hook H005 word for word, blank filled with real buyer words ("it hurts to even open my mouth", "every winter"). Grade 3.3. The video itself has no voice; music added later.</p></section>
<section><h2>Cut v3 vs v2: S1 only changed</h2><div class="refs"><figure><video controls playsinline muted preload="metadata" src="media/cut_v3.mp4" style="width:100%;border-radius:10px;background:#000"></video><figcaption><b>v3</b>: S1 on Kling. Her cupped palm sits by the nozzle side of the pump while she presses. Honest note: the palm is beside and below the nozzle tip, not right under it, and later in the clip a drop lands on the bottle shoulder (that part is cut out; a tiny white dot stays on the shoulder).</figcaption></figure><figure><video controls playsinline muted preload="metadata" src="media/cut_v2.mp4" style="width:100%;border-radius:10px;background:#000"></video><figcaption><b>v2</b> (in Drive now): S1 from Omni, nozzle to the side, dollop lands in the palm in front of the bottle.</figcaption></figure></div><p class="muted">Both 10.0 s, silent for music, no black or frozen frames, AI finish on. Kie $2.47 of $2.48 allowed; Kling 100 credits on this job (568 left).</p></section>
<section><h2>Storyboard v2: green cleanser first, the group of four at the end</h2><p class="muted">Your change: S1-S3 show only the green cleanser, S4 brings in the other three, S5 ends on all four. A 1.2 s fast run between S4 and S5 reuses spare windows of S1 and S3 ($0). S1 is the test clip.</p>{rows}</section>
<section><h2>References</h2><div class="refs">
<figure><img src="{sheet}" alt="Product sheet"><figcaption>Product sheet: real CeraVe fronts; cream tube from the listing (navy text)</figcaption></figure>
<figure><img src="{room}" alt="Room"><figcaption>Room: real Pexels bathroom (free licence)</figcaption></figure>
<figure><img src="{hand}" alt="Hand sheet without bracelet"><figcaption>Grace hand sheet, no bracelet (default)</figcaption></figure>
<figure><img src="{hand2}" alt="Hand sheet with bracelet"><figcaption>Grace hand sheet, with bracelet</figcaption></figure>
</div></section>
<section><h2>Research behind it</h2><p>Music-only CeraVe videos had the best save rates in the research: @lordkierra 199.6K views, 0.18% saves (cleanser pumped into the palm at frame 0); @shakyra._ 0.39% saves (cream texture, 11 s, a cut every 1.4 s). Deal voiceovers got views but 0.03-0.08% saves.</p></section>
</main>"""
open("review/index.html", "w").write(page); print("ok", len(page))
