"""Review page for Ralph (plan stage, newest on top). python3 build_review.py -> review/index.html"""
import json, html
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); SH = D["videos"][0]["shots"]; E = html.escape
ROOM = {"rooms/pick/backyard.jpg": "backyard lawn", "rooms/pick/yard_house.jpg": "sunny garden", "rooms/pick/kitchen.jpg": "bright kitchen", "rooms/pick/counter.jpg": "white counter"}
MODEL = {"wan": "Flow take ($0) · else Wan 5 s $0.40", "seedance": "Seedance Mini 4 s $0.16"}
HANDS = {"kid": "HAND · child", "grace": "HAND · Grace", False: "HAND-FREE"}
def cf(s): return f"prompts/{s['id']}{'_seedance' if s['model']=='seedance' else ''}.txt"
shots = "".join(f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span><span class="win">{s['t'][0]:.1f}–{s['t'][1]:.1f} s</span>
<span class="chip {'free' if not s['hand'] else ''}">{HANDS[s['hand']]}</span><span class="chip">{ROOM[s['room']]}</span><span class="chip">{MODEL[s['model']]}</span></div>
<p class="say">{E(s['words'])}</p><p class="see">{E(s['still'])}</p><p class="mv"><b>Motion:</b> {E(s['motion'])}</p>
<details><summary>Full still prompt</summary><pre>{E(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>
<details><summary>Full clip prompt</summary><pre>{E(Path(cf(s)).read_text())}</pre></details></article>""" for s in SH)
v1 = "".join(f"<li>{E(l)}</li>" for l in json.loads(Path("vo/V1_lines.json").read_text())["lines"])
v2 = "".join(f"<li>{E(l)}</li>" for l in json.loads(Path("vo/V2_lines.json").read_text())["lines"])
page = f"""<title>Boo-Boo Gel Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito+Sans:wght@400;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: one column; decision box first, then scripts, shots with prompts, product truth, settings, research, cost */
:root{{--bg:#eef5fb;--card:#ffffff;--fg:#0f1d2a;--muted:#4f6274;--line:#d3e2ee;--accent:#1a7fc4;--warn:#c2571a;--chip:#dcecf8;--chipfree:#efe7d4;
--display:"Fredoka","Trebuchet MS",sans-serif;--body:"Nunito Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0c151d;--card:#14212c;--fg:#e6f0f8;--muted:#9ab0c2;--line:#253645;--accent:#5db6f2;--warn:#f39a62;--chip:#1b3446;--chipfree:#3a3322;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0c151d;--card:#14212c;--fg:#e6f0f8;--muted:#9ab0c2;--line:#253645;--accent:#5db6f2;--warn:#f39a62;--chip:#1b3446;--chipfree:#3a3322;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}}
.wrap{{max-width:860px;margin:0 auto;padding-block:24px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:22px}}
h1{{font:600 2.2rem/1.1 var(--display);margin:0;text-wrap:balance}} h1 em{{color:var(--accent);font-style:normal}} h2{{font:600 1.35rem/1.2 var(--display);margin:0;text-wrap:balance}}
.sub{{color:var(--muted);margin:4px 0 0}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:grid;gap:10px;min-width:0}}
.ask{{border-left:4px solid var(--warn);background:var(--card);padding:14px 18px;border-radius:0 10px 10px 0;display:grid;gap:8px}}
.ask strong{{color:var(--warn)}} ol,ul{{margin:0;padding-left:20px;display:grid;gap:4px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}}
figure{{margin:0;display:grid;gap:6px;min-width:0}} figure img{{width:100%;max-width:100%;border-radius:6px;border:1px solid var(--line)}}
figcaption{{font:500 .75rem var(--mono);color:var(--muted)}}
.script li{{font:700 1.05rem/1.45 var(--body)}}
.shot{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:6px;min-width:0}}
.sh{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline}} .num{{font:600 1.4rem/1 var(--display);color:var(--accent)}} .win{{font:500 .8rem var(--mono);color:var(--muted);font-variant-numeric:tabular-nums}}
.chip{{font:700 .7rem var(--body);letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--chip)}} .chip.free{{background:var(--chipfree)}}
.say{{font:700 1.05rem/1.35 var(--body);margin:0}} .say::before{{content:"\\201C"}} .say::after{{content:"\\201D"}}
.see,.mv{{margin:0;font-size:.95rem}} summary{{cursor:pointer;color:var(--accent);font-weight:700}} summary:focus-visible{{outline:2px solid var(--accent)}}
pre{{white-space:pre-wrap;font:500 .78rem/1.45 var(--mono);background:var(--bg);padding:10px;border-radius:6px;margin:6px 0 0;overflow-x:auto}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}} td,th{{border-bottom:1px solid var(--line);padding:6px 4px;text-align:left;vertical-align:top}} td.n,th.n{{text-align:right}}
figure.st img{{aspect-ratio:9/16;object-fit:cover}}.stgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}.ok{{color:var(--accent)}}.bad{{color:var(--warn)}}
.tot td{{font-weight:700;color:var(--accent)}} a{{color:var(--accent)}}
</style>
<div class="wrap">
<header><h1>Dr. Nice's <em>Boo-Boo Gel</em></h1><p class="sub">Grace, 1 fl oz pump. Music-only video, 12 s, 6 shots, plus a ~30 s script for her own voiceover. Plan for your OK; nothing has been paid for yet.</p></header>
<section class="ask"><strong>Storyboard round 1: one still needs a redo</strong><ol>
<li><b>S1, S2, S3, S4, S6 pass</b> at 2x: every letter of the label right on S1, S4, S6, the monster and horns right, silver pump on S1, child's hands with whole wrists, clear gel dot.</li>
<li>Free fix done: the real backyard photo had hookah pipes on a wall shelf (S1, S2, S3). I painted them out with plain wall.</li>
<li><b>S5 fails</b>: the bottle is about twice too big next to the backpack, and the small label came out garbled ("BOO BOX SEL"). New prompt: closer on the backpack pocket, bottle under a third of the backpack's height, label big, her hand on the silver base only. Redo $0.09 (inside the book's redo allowance).</li>
<li>Spent so far: Kie $0.54 of $2.96 (November $16.66 of $100).</li></ol></section>
<section class="box"><h2>Storyboard round 1</h2><div class="stgrid">STORY</div></section>
<details class="box"><summary><b>Plan you approved</b> (all on Kie, $2.96 ceiling; bites left out; HofR later)</summary>
<section class="ask"><strong>Your OK needed (nothing runs until you answer in the chat)</strong><ol>
<li><b>Approve the plan</b>: product clips S1, S4, S5, S6 as Flow takes in your app ($0, 48 credits), then Kie only for stills and the 2 no-product clips: <b>about $0.96</b>. Ceiling if every product clip falls back to Wan on Kie: <b>$2.96</b>. November so far $16.12 of $100.</li>
<li><b>Insect bites</b>: only the TikTok Shop title says it. The brand site and Amazon say scrapes, minor cuts, burns, blisters, chafing (they sell a separate bite gel). Scripts leave bites out unless you say add one line.</li>
<li><b>House of Rameau version</b> ($0 re-cut, own order and grade, on-screen hook text, no captions): now or later?</li></ol></section>
<section class="box"><h2>V1 · the 12 s music cut</h2><ol class="script">{v1}</ol>
<p class="sub">46 words, about 12–13 s at Grace's pace, grade 1.6. Each shot sits on its line, so she can caption it or voice it later. No text on the video. Hook H122.</p></section>
<section class="box"><h2>V2 · standard length for Grace's voiceover</h2><ol class="script">{v2}</ol>
<p class="sub">107 words, about 30–35 s, grade 2.0. Hook H040. A 30 s video for this voiceover would need about 6 more shots (quoted separately if you want it).</p>
<p class="sub">Captions: "the bandaid fight in our house is done. one pump and they put it on themselves #ad #momfinds #kidsfirstaid #momhacks #booboo" · On-screen hook options (only on your yes): "the bandaid fight is over", "they did it all by themselves".</p></section>
<section style="display:grid;gap:12px"><h2>Shots (3 HAND, 3 HAND-FREE)</h2>{shots}</section>
<section class="box"><h2>Real product (your photos = the brand's listing)</h2>
<div class="grid"><figure><img src="img/real_box.jpg" alt="Real bottle and box"><figcaption>Bottle + box (you sent)</figcaption></figure><figure><img src="img/real_knee.jpg" alt="Bottle in a child's hand on grass"><figcaption>Size in a child's hand (you sent)</figcaption></figure><figure><img src="img/howto.jpg" alt="Brand how-to-use panel"><figcaption>Brand HOW TO USE: silver pump, 1 dot, dries clear</figcaption></figure></div>
<ul><li>Slim silver cylinder about 11 cm tall, 3 cm across (box 1.37 x 1.37 x 4.75 in).</li><li>Brushed silver cap over the top third, thin chrome ring, silver base.</li>
<li>Sky-blue label: "DR. NICE'S" with a tiny green leaf, "NATURAL PRODUCTS", "BOO-BOO GEL", smiling blue furry monster with golden horns and an orange bandage, "1 fl oz (30ml)".</li>
<li>Cap off: silver pump head (one older brand photo shows a white pump; not used). Clear gel, one pearl-size dot. The box is never shown.</li></ul>
<figure><img src="img/sheet.jpg" alt="Product reference sheet"><figcaption>Reference sheet passed on every product still and clip, with the label and lettering close-ups</figcaption></figure></section>
<section class="box"><h2>Settings (real Pexels and Pixabay photos, no people)</h2><div class="grid">
<figure><img src="img/backyard.jpg" alt="Backyard lawn"><figcaption>Backyard: S1, S2, S3</figcaption></figure><figure><img src="img/counter.jpg" alt="White counter with oranges"><figcaption>Counter: S4</figcaption></figure>
<figure><img src="img/kitchen.jpg" alt="Bright kitchen"><figcaption>Kitchen: S5</figcaption></figure><figure><img src="img/yard_house.jpg" alt="Sunny garden"><figcaption>Garden: S6</figcaption></figure></div>
<p class="sub">No playground photo without people came up, so the scraped-knee moment is in the backyard.</p></section>
<section class="box"><h2>What the winners do</h2>
<figure><img src="img/winner_lanie.jpg" alt="Contact sheet of the @laniedoesdeals video"><figcaption>@laniedoesdeals, 10.8M views: "Your kid melts down every time you clean a scrape."</figcaption></figure>
<figure><img src="img/winner_natalee.jpg" alt="Contact sheet of the @nataleesnyder video"><figcaption>@nataleesnyder, 682.6K (shop): toddler does it herself, counting out loud</figcaption></figure>
<ul><li>All four top videos open on the kid's skin with the boo-boo in view; we open on the gel dot by the scrape.</li>
<li>Parents' words: "5+ year olds freak out about every single tiny little scrape", "They do peel off 5 minutes later", "What helped her was letting her do it on her own".</li>
<li>Bite relief is a summer niche (1 new shop video in 30 days), so the everyday-scrape angle fits November. The niche's top comments are about price, so no price talk.</li>
<li>Script gate: GATE OK (playbook, coach, viral board, facts, Grace's research workflow, hooks, humanizer, readability, audience, line sources). Most TikTok hashtag and shop searches came back empty today (each tried and logged).</li></ul></section>
</details>
<section class="box"><h2>Cost</h2><div class="tw"><table><tr><th>Item</th><th class="n">$</th></tr>
<tr><td>6 stills, Gemini 3 Pro Image on Kie, 6 x $0.09</td><td class="n">0.54</td></tr>
<tr><td>2 Seedance 2.0 Mini clips (S2, S3: no bottle), 2 x $0.164</td><td class="n">0.33</td></tr>
<tr><td>4 product clips as Flow takes in your app (48 credits)</td><td class="n">0.00</td></tr>
<tr><td>Fallback only: Wan 3.0 720P 5 s on Kie, up to 4 x $0.40, each asked first</td><td class="n">1.60</td></tr>
<tr><td>One likely redo (1 still + 1 Wan), asked first</td><td class="n">0.49</td></tr>
<tr class="tot"><td>Ceiling (expected with Flow: $0.96)</td><td class="n">2.96</td></tr></table></div>
<p class="sub">Order: 6 stills at once, storyboard here for your look, then the Flow kits (S1 first: open pump, two small hands, the gel dot), S2 and S3 on Seedance meanwhile. About 35–40 min of machine time after your OK, plus your stops.</p></section>
</div>"""
ST = [("S1","PASS","Open pump, gel dot, label exact; hookahs painted out"),("S2","PASS","Tipped scooter; hookahs painted out"),("S3","PASS","Child dabs the gel on the knee; hookahs painted out"),
 ("S4","PASS","Counter, label exact"),("S5","REDO","Bottle too big, label garbled"),("S6","PASS","End shot, one bottle, label exact")]
page = page.replace("STORY", "".join(f'<figure class="st"><img src="st/{i}_r1.jpg" alt="{i} still"><figcaption><b class="{'ok' if v=='PASS' else 'bad'}">{i} {v}</b> {n}</figcaption></figure>' for i,v,n in ST))
Path("review/index.html").write_text(page); print(len(page))
