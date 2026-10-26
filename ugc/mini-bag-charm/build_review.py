"""Review page for Ralph (newest on top). python3 build_review.py -> review/index.html (images in review/img/)."""
import json, html, re
from pathlib import Path
from PIL import Image
D = json.loads(Path("shots.json").read_text()); SH = D["shots"]; E = html.escape
book = Path("BOOK.md").read_text()
script = re.search(r"V1, recommended.*?\n(.*?)\nWhy:", book, re.S).group(1).strip().splitlines()
qs = re.search(r"## 7\. Questions\n(.*?)\n\n## 8", book, re.S).group(1).strip().splitlines()
IMG = Path("review/img"); IMG.mkdir(parents=True, exist_ok=True)
for name, src, w in [("sheet", "refs/product_sheet.png", 1400), ("listing", "refs/real/front_crop.png", 900), ("storyboard", "refs/storyboard.jpg", 1024),
                     ("roomA", "rooms/roomA_wood_table.jpg", 600), ("roomB", "rooms/roomB_sofa_window.jpg", 600), ("roomC", "rooms/roomC_fireplace.jpg", 600),
                     ("roomD", "rooms/roomD_tree_bows.jpg", 600), ("hand_with", "../../grace/ref/hand-sheets/with_bracelet.jpg", 800),
                     ("hand_without", "../../grace/ref/hand-sheets/without_bracelet.jpg", 800),
                     ("model", "research/coach/top/7689843077464214814/sheet.png", 1200)]:
    im = Image.open(src).convert("RGB"); im.thumbnail((w, w * 2)); im.save(IMG / f"{name}.jpg", quality=86)
ROOM = {"rooms/roomA_wood_table.jpg": "wood table", "rooms/roomB_sofa_window.jpg": "sofa by the window", "rooms/roomC_fireplace.jpg": "fireplace", "rooms/roomD_tree_bows.jpg": "tree with white bows"}
shots = "".join(f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span>
<span class="chip {'free' if not s['hand'] else ''}">{'HAND' if s['hand'] else 'HAND-FREE'}</span><span class="chip">{'Seedance on Kie' if s.get('no_product') else 'Flow first'}</span><span class="chip">{ROOM[s['room']]}</span>{'<span class="chip warn">waits for the clip photo</span>' if s.get('needs_clasp') else ''}</div>
<p class="say">&ldquo;{E(s['words'])}&rdquo;</p><p class="see">{E(s['still'])}</p><p class="mv"><b>Motion:</b> {E(s['motion'])}</p>
<details><summary>Full still prompt</summary><pre>{E(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>
<details><summary>Full clip prompt</summary><pre>{E(Path('prompts/'+s['id']+'.txt').read_text())}</pre></details></article>""" for s in SH)
cost = """<table><tr><td>Stills, Gemini 3 Pro Image on Kie</td><td>9 x $0.09</td><td>$0.81</td></tr>
<tr><td>One likely still redo</td><td>1 x $0.09</td><td>$0.09</td></tr>
<tr><td>S3 clip (no product), Seedance 2.0 Mini on Kie</td><td>1 x $0.164</td><td>$0.164</td></tr>
<tr><td>8 product clips, Omni in your Flow app first</td><td>8 x 12 credits</td><td>$0.00</td></tr>
<tr><td>Same 8 on Kie only if Flow fails (asked first)</td><td>8 x $0.315</td><td>$2.52</td></tr>
<tr><td>One likely clip redo (asked first)</td><td>1 x $0.315</td><td>$0.315</td></tr>
<tr class="tot"><td>TOTAL (incl. the Kie fallback)</td><td></td><td>$3.899</td></tr></table>
<p class="note">Expected with Flow: <b>$1.06</b>. ElevenLabs about 450 characters (Grace cloned). Month so far $176.80, no cap in October. Nothing has been spent on this job yet.</p>"""
script_html = "".join(f"<li>{E(l.split('. ',1)[1]).replace('[+]','<mark>added</mark>')}</li>" for l in script)
NOTES = [l.strip("| ").split(" | ") for l in Path("qc/stills_r1.md").read_text().splitlines() if l.startswith("| S")]
STORY = "".join(f'<figure><img src="st/{i}_r1.jpg" alt="{i} still"><figcaption><b class="{v.lower()}">{i} {v}</b> {E(n)}</figcaption></figure>' for i, v, n in NOTES)
page = f"""<title>Mini Bag Charm Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Mulish:wght@400;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: one column; your decisions first, then the real product, script, shots with full prompts, cost, research */
:root{{--bg:#f6f1f1;--card:#fffbfb;--fg:#2a1a1d;--muted:#6f5a5e;--line:#e6d6d8;--wine:#7d1f2e;--gold:#9a7417;--chip:#f1e4e6;
--display:"Fraunces",Georgia,serif;--body:"Mulish",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1a1214;--card:#231a1c;--fg:#f3e8ea;--muted:#bba6aa;--line:#3a2b2e;--wine:#e2808f;--gold:#d8b45a;--chip:#33252a;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#1a1214;--card:#231a1c;--fg:#f3e8ea;--muted:#bba6aa;--line:#3a2b2e;--wine:#e2808f;--gold:#d8b45a;--chip:#33252a;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}}
.wrap{{max-width:880px;margin:0 auto;padding-block:24px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:22px}}
h1{{font:600 2.1rem/1.1 var(--display);margin:0;text-wrap:balance;color:var(--wine)}} h2{{font:600 1.3rem/1.2 var(--display);margin:0;text-wrap:balance}}
.sub{{color:var(--muted);margin:4px 0 0}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px 18px;display:grid;gap:10px;min-width:0}}
.ask{{border:2px solid var(--wine);background:var(--card);padding:14px 18px;border-radius:8px;display:grid;gap:8px}}
.ask h2{{color:var(--wine)}} ol,ul{{margin:0;padding-left:20px;display:grid;gap:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
figure{{margin:0;display:grid;gap:6px;min-width:0;align-content:start}} figure img{{width:100%;max-width:100%;border-radius:6px;border:1px solid var(--line)}}
figcaption{{font:500 .75rem var(--mono);color:var(--muted)}}
.script li{{font:600 1.05rem/1.5 var(--display)}} mark{{background:var(--chip);color:var(--wine);font:500 .7rem var(--mono);padding:1px 6px;border-radius:99px;vertical-align:middle}}
.shot{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;display:grid;gap:6px;min-width:0}}
.sh{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}} .num{{font:500 .9rem var(--mono);color:var(--wine)}}
.chip{{font:500 .7rem var(--mono);letter-spacing:.05em;background:var(--chip);padding:2px 8px;border-radius:99px}}
.chip.free{{outline:1px solid var(--gold)}} .chip.warn{{color:var(--wine);outline:1px solid var(--wine)}}
.say{{font-weight:700;margin:0}} .see,.mv{{margin:0;color:var(--muted);font-size:.93rem}}
details summary{{cursor:pointer;font:500 .8rem var(--mono);color:var(--wine)}} details summary:focus-visible{{outline:2px solid var(--wine)}}
pre{{white-space:pre-wrap;font:400 .78rem/1.5 var(--mono);background:var(--bg);padding:10px;border-radius:6px;overflow-x:auto;margin:6px 0 0}}
table{{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}} td{{padding:6px 4px;border-bottom:1px solid var(--line)}} td:last-child{{text-align:right}}
.tot td{{font-weight:700;border-bottom:none}} .sb{{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}} .pass{{color:var(--gold)}} .redo{{color:var(--wine)}} .note{{margin:0;color:var(--muted)}} .facts b{{color:var(--gold)}}
</style>
<div class="wrap">
<header><h1>Mini Bag Charm, burgundy</h1><p class="sub">Grace · hands + hand-free AI over Grace's voice · still storyboard round 1 · $0.81 spent of $3.90</p></header>
<section class="ask"><h2>Storyboard round 1: 6 pass, 3 need a redo</h2>
<p class="note">Redo S1, S7 and S9 with the fixed prompts: 3 x $0.09 = <b>$0.27</b> (the book has one redo; the job stays inside its $3.90). Small flaw you can let go for free: the blue band sits on the thumb or index finger in S1, S4 and S5 instead of the ring finger.</p></section>
<section class="box"><h2>Stills, round 1 (9 on Kie, $0.81)</h2><div class="grid sb">{STORY}</div></section>
<section class="box"><h2>Voiceover (Grace cloned, 26.3 s)</h2><audio src="vo.mp3" controls preload="metadata" style="width:100%"></audio><p class="note">Echo 150 ms (passes, the approved flashlight level). Paced to 3.5 words/s, -16 LUFS. S5 and S9 lines run 4.7 s and 5.2 s, so those two get 8 s Flow takes.</p></section>
<section class="box"><h2>The real product (what every prompt copies)</h2>
<ul class="facts"><li><b>Shape</b>: mini bucket bag, open top (no zip, no flap), deep burgundy pebbled faux leather</li><li><b>Handles</b>: two rolled handles with darker painted edges</li><li><b>Gold</b>: rectangular buckle on the front strap, padlock with three engraved lines (no letters), ring + grommet, four little feet</li><li><b>Scarf</b>: pink, light blue and white twilly knotted on the right handle, long frayed tail</li><li><b>Missing</b>: the clip that attaches it to a bag is not in this photo (question 1)</li></ul>
<div class="grid"><figure><img src="img/sheet.jpg" alt="Product reference sheet"><figcaption>Reference sheet, real pixels from your listing photo only</figcaption></figure>
<figure><img src="img/storyboard.jpg" alt="Grace's storyboard"><figcaption>Grace's storyboard (shots kept; colours lineup, golden tone and text not used)</figcaption></figure></div></section>
<section class="box"><h2>Script, V1 (Grace cloned voice, ~26 s)</h2><ol class="script">{script_html}</ol>
<p class="note">Your script plus 2 small edits: a pain line (Grace's structure) and "and one for a friend" so the CTA sells two. Grade 4.9. Humanizer done. Hook = H061 in Grace's wording; the top comment on the 331K model video is "Why am I so obsessed with the mini version of anything?"</p></section>
<section style="display:grid;gap:12px"><h2>Shots (5 hand, 4 hand-free)</h2>{shots}</section>
<section class="box"><h2>Rooms (real photos, free)</h2><div class="grid"><figure><img src="img/roomA.jpg" alt="Wood table"><figcaption>S1 S2 S5 S6 · wood table, pink candle (Pixabay)</figcaption></figure><figure><img src="img/roomB.jpg" alt="Sofa"><figcaption>S3 S4 S7 · cream sofa by a window (Pixabay)</figcaption></figure><figure><img src="img/roomC.jpg" alt="Fireplace"><figcaption>S8 · fireplace, stocking (Pexels)</figcaption></figure><figure><img src="img/roomD.jpg" alt="Tree"><figcaption>S9 end · green tree, white bows (Pexels)</figcaption></figure></div></section>
<section class="box"><h2>Hand (question 5)</h2><div class="grid"><figure><img src="img/hand_with.jpg" alt="With bracelet"><figcaption>WITH bracelet (default in the prompts)</figcaption></figure><figure><img src="img/hand_without.jpg" alt="Without bracelet"><figcaption>WITHOUT bracelet</figcaption></figure></div></section>
<section class="box"><h2>Cost</h2>{cost}</section>
<section class="box"><h2>What the winners do</h2><figure><img src="img/model.jpg" alt="Model video frames"><figcaption>@the_little_beannn 331K: burgundy mini charm in hand at frame 0, packed with tiny things, clipped onto a bigger bag at the end. Our order follows it.</figcaption></figure>
<ul><li>@meenyminimo 333K "pack my mini bag": comment "Can you actually like use it?" → S5 shows the earbuds going in.</li><li>@lujushop 603K "I genuinely cannot choose just one" + multi-packs sell most on TikTok Shop (12,006 units) → CTA for two.</li><li>Buyers on Reddit: "Did it fit??" (AirPods), "It's too much money for a charm." → the "more expensive" line.</li></ul></section>
</div>"""
Path("review/index.html").write_text(page); print("ok", len(page))
