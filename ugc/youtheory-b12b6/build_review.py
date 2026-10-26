"""Review page for Ralph (newest on top). python3 build_review.py -> review/index.html"""
import json, html
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); SH = D["videos"][0]["shots"]
E = html.escape
room = {"rooms/room_A.jpg": "A bedroom", "rooms/room_B.jpg": "B kitchen", "rooms/room_C.jpg": "C entryway", "rooms/room_D.jpg": "D plant office"}
shots = "".join(f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span>
<span class="chip {'free' if not s['hand'] else ''}">{'HAND' if s['hand'] else 'HAND-FREE'}</span><span class="chip">{room[s['room']]}</span></div>
<p class="say">{E(s['words'])}</p><p class="see">{E(s['still'])}</p><p class="mv"><b>Motion:</b> {E(s['motion'])}</p>
<details><summary>Full still prompt</summary><pre>{E(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>
<details><summary>Full clip prompt</summary><pre>{E(Path('prompts/'+s['id']+'.txt').read_text())}</pre></details></article>""" for s in SH)
STORY = [("S1","PASS","Pouch small on the nightstand; the lamp is lit (warm glow), the room stays bright."),
 ("S2","PASS","Torn top, straw, thin serif print."),
 ("S3","REDO","B12B6 drawn in a bold sans font; the real one is a thin serif."),
 ("S4","REDO","Same bold sans B12B6, and an invented disclaimer line."),
 ("S5","PASS","Thin serif print, good grip. The torn tab still hangs off one side, like it was just torn: OK, or redo?"),
 ("S6","PASS","Box print right. Her thumb covers part of B6 at the start; in the clip she sets it down and lets go, so it shows."),
 ("S7","REDO","Pouch tiny and its print unreadable; reframed close."),
 ("S8","PASS","Fake book-spine and screen text blurred free."),
 ("S9","REDO","Bold sans B12B6 again.")]
story = "".join(f"""<figure class="st"><img src="st/{i}_r2.jpg" alt="{i} still"><figcaption><b class="{'ok' if v=='PASS' else 'bad'}">{i} {v}</b> {E(n)}</figcaption></figure>""" for i,v,n in STORY)
page = f"""<title>B12B6 Pouch Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Work+Sans:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: one column, decision box first, then product truth (photos), script, shots with full prompts, cost */
:root{{--bg:#f7f3f5;--card:#ffffff;--fg:#2a1820;--muted:#6f5a64;--line:#e6d9df;--accent:#b0185e;--warn:#b4471b;--chip:#f3e4ec;--chipfree:#e7efe9;--good:#2f7d4f;
--display:"Fraunces",Georgia,serif;--body:"Work Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1a1216;--card:#24191f;--fg:#f2e8ed;--muted:#b9a4ae;--line:#3a2a32;--accent:#f06aa6;--warn:#f0905e;--chip:#3a2430;--chipfree:#22332a;--good:#7fd19f;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#1a1216;--card:#24191f;--fg:#f2e8ed;--muted:#b9a4ae;--line:#3a2a32;--accent:#f06aa6;--warn:#f0905e;--chip:#3a2430;--chipfree:#22332a;--good:#7fd19f;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 var(--body)}}
.wrap{{max-width:860px;margin:0 auto;padding-block:24px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:22px}}
h1{{font:600 2.1rem/1.1 var(--display);margin:0;text-wrap:balance;color:var(--accent)}} h2{{font:600 1.35rem/1.2 var(--display);margin:0}}
.sub{{color:var(--muted);margin:4px 0 0}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:grid;gap:10px;min-width:0}}
.ask{{border-left:4px solid var(--warn);background:var(--card);padding:14px 18px;border-radius:0 10px 10px 0;display:grid;gap:8px}}
.ask strong{{color:var(--warn)}} ol,ul{{margin:0;padding-left:20px;display:grid;gap:4px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}
figure{{margin:0;display:grid;gap:6px;min-width:0}} figure img{{width:100%;max-width:100%;border-radius:6px;border:1px solid var(--line)}}
figcaption{{font:500 .75rem var(--mono);color:var(--muted)}}
.script{{font:600 1.1rem/1.5 var(--body);margin:0}}
.shot{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:6px;min-width:0}}
.sh{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline}} .num{{font:600 1.4rem/1 var(--display);color:var(--accent)}}
.chip{{font:600 .7rem var(--body);letter-spacing:.08em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--chip)}} .chip.free{{background:var(--chipfree)}}
.say{{font:600 1.05rem/1.35 var(--body);margin:0}} .say::before{{content:"\\201C"}} .say::after{{content:"\\201D"}}
.see,.mv{{margin:0;font-size:.95rem}} summary{{cursor:pointer;color:var(--accent);font-weight:600}}
pre{{white-space:pre-wrap;font:500 .78rem/1.45 var(--mono);background:var(--bg);padding:10px;border-radius:6px;margin:6px 0 0;overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}} td,th{{border-bottom:1px solid var(--line);padding:6px 4px;text-align:left}} td:last-child,th:last-child{{text-align:right}}
figure.st img{{aspect-ratio:9/16;object-fit:cover}}.stgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}.ok{{color:var(--good)}}.bad{{color:var(--warn)}}
.tot td{{font-weight:600;color:var(--accent)}}
</style>
<div class="wrap">
<header><h1>Youtheory B12B6 Liquid</h1><p class="sub">Grace, hands-only AI video, ~20 s, 9 shots. Plan for your OK before anything else is paid for. Round 1 stills were wrong (below).</p></header>
<section class="ask"><strong>Storyboard round 2: your call</strong><ol>
<li>Redo S3, S4, S7, S9 on Kie: 4 x $0.09 = <b>$0.36</b> (job so far $1.62 of $4.455; October $168.83). Font now forced to the thin serif, S7 framed close.</li>
<li>S5: keep the half-torn tab hanging off, or redo it with the tab fully gone?</li>
<li>Then the clips on Kie (Omni), S6 first as the test clip.</li></ol></section>
<section class="box"><h2>Storyboard, round 2 (no spouts this time)</h2><div class="stgrid">{story}</div></section>
<details class="box"><summary><b>Plan you approved</b> (answers: 1 none, 2 yes, 3 say box, 4 yes, 5 yes, 6 Kie, 7 yes)</summary>
<section class="ask"><strong>Your OK needed (nothing runs until you answer)</strong><ol>
<li>Check the <b>real product details</b> below (top, shape, print, box). Anything wrong?</li>
<li>Your script <b>word for word</b> ("12" written as "twelve")?</li>
<li>"B12 supports normal nervous system function" is not on the box or pouch (they say "promotes brain health"). Keep it, or swap free to "and B12 promotes brain health"?</li>
<li>Hand: Grace's sheet with bracelet (French tips, crown ring, gold solitaire, blue band, flat gold link bracelet, pearl chain), as on Collagen?</li>
<li>Straw: plain white paper straw in the torn-open top, OK?</li>
<li>Stills redo: on Kie (9 x $0.09 = $0.81) or free in your Gemini app (I send a kit)?</li>
<li>On-screen text: none unless you say so.</li></ol></section>
<section class="box"><h2>Real product details (from Grace's photos)</h2>
<div class="grid"><figure><img src="img/grace_pouch_front_flat.jpg" alt="Grace's real pouch"><figcaption>Grace's real pouch</figcaption></figure>
<figure><img src="img/torn_top.jpg" alt="Torn top with straw"><figcaption>Reference for every shot: tab torn off, straw in (real pixels)</figcaption></figure>
<figure><img src="img/grace_box_front_open.jpg" alt="Grace's real box"><figcaption>Grace's real display box (S6)</figcaption></figure></div>
<ul><li>Flat white glossy foil pouch, ~6.5 x 15 cm, 1 fl oz. Straight sides, flat bottom, square shoulders, narrow neck. Not a stand-up pouch.</li>
<li>Top: flat magenta <b>tear-off tab</b>. No screw cap, no spout. In every shot the tab is torn off and one white paper straw stands in the opening.</li>
<li>Print: youtheory logo, magenta dot circle, magenta "B12B6", grey "liquid", "promotes brain health*", "helps support energy production*", magenta "raspberry flavor" bar, "1 fl oz (30 ml)", "dietary supplement". No "essential daily vitamins" (that is only on the listing render).</li>
<li>Box: Grace's torn-open display carton, front "B6 liquid", three + lines incl. "1,000 mcg of B12 per serving", raspberry splash, 12 pouches.</li></ul>
<figure><img src="img/sheet.jpg" alt="Product reference sheet"><figcaption>Product reference sheet passed on every still and clip</figcaption></figure></section>
<section class="box"><h2>Script (your words)</h2><p class="script">A pouch a day keeps laziness away. Because sometimes, you don't need more motivation. Your body may need B vitamins! This delicious raspberry-flavored B6 and B12 pouch makes it easy. There are twelve in a box, so I'd stock up on a few! B6 and B12 support normal energy metabolism, and B12 promotes brain health. Tap the orange cart and grab yours while they're in stock!</p>
<p class="sub">Gate OK. Readability grade 5.7. Voiceover made (Grace voice, 19.7 s, echo 150 ms = pass).</p></section>
<section class="box"><h2>Rooms (real Pexels photos)</h2><div class="grid">
<figure><img src="img/room_A.jpg" alt="Bedroom"><figcaption>A bedroom: S1, S2</figcaption></figure><figure><img src="img/room_B.jpg" alt="Kitchen"><figcaption>B kitchen: S3-S6</figcaption></figure>
<figure><img src="img/room_C.jpg" alt="Entryway"><figcaption>C entryway: S7</figcaption></figure><figure><img src="img/room_D.jpg" alt="Office"><figcaption>D plant office: S8, S9</figcaption></figure></div></section>
<section style="display:grid;gap:12px"><h2>Shots (straw in every one)</h2>{shots}</section>
<section class="box"><h2>Cost</h2><table><tr><th>Item</th><th>$</th></tr>
<tr><td>Round 1 stills (wrong top, my prompt)</td><td>0.81</td></tr>
<tr><td>Stills redo, Kie 9 x $0.09 (or $0 in your Gemini app)</td><td>0.81</td></tr>
<tr><td>9 product clips, Omni in your Flow app first (108 credits)</td><td>0.00</td></tr>
<tr><td>Same 9 on Kie only if Flow fails, asked first, 9 x $0.315</td><td>2.835</td></tr>
<tr class="tot"><td>Most it can cost</td><td>4.455</td></tr></table>
<p class="sub">Expected with Flow: $1.62 ($0.81 if the redo is in Gemini). October so far: $168.02, no cap this month.</p></section>
</details>
<section class="box"><h2>Round 1 stills: rejected</h2><figure><img src="img/r1_wrong.jpg" alt="Round 1 stills with a screw spout"><figcaption>All drew a screw spout (my prompt said "cap twisted off"). Not used.</figcaption></figure></section>
</div>"""
Path("review/index.html").write_text(page); print(len(page))
