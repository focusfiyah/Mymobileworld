"""Review page for Ralph (newest on top). python3 build_review.py -> review/index.html"""
import json, html
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); SH = D["videos"][0]["shots"]; E = html.escape
ROOM = {"rooms/pick/bath_A.jpg": "white vanity bathroom", "rooms/pick/bath_B_teal.jpg": "teal tile bathroom", "rooms/pick/towel_bar.jpg": "sink corner",
        "rooms/pick/bedroom_teal.jpg": "teal bedroom", "rooms/pick/hotel.jpg": "hotel room"}
MODEL = {"omni": "Omni 4 s $0.315", "seedance": "Seedance Mini 4 s $0.164"}
def cf(s): return f"prompts/{s['id']}{'_seedance' if s['model']=='seedance' else ''}.txt"
shots = "".join(f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span><span class="win">{s['t'][0]:.1f}-{s['t'][1]:.1f} s</span>
<span class="chip {'free' if not s['hand'] else ''}">{'HAND' if s['hand'] else 'HAND-FREE'}</span><span class="chip">{ROOM[s['room']]}</span><span class="chip">{MODEL[s['model']]}</span></div>
<p class="say">{E(s['words'])}</p><p class="see">{E(s['still'])}</p><p class="mv"><b>Motion:</b> {E(s['motion'])}</p>
<details><summary>Full still prompt</summary><pre>{E(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>
<details><summary>Full clip prompt</summary><pre>{E(Path(cf(s)).read_text())}</pre></details></article>""" for s in SH)
lines = json.loads(Path("vo/V1_lines.json").read_text())["lines"]
script = "".join(f"<li>{E(l)}</li>" for l in lines)
page = f"""<title>Buttah Towels Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,600&family=Karla:wght@400;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: one column; the decision box first, then script, shots with prompts, product truth, rooms, research, cost */
:root{{--bg:#f1f6f5;--card:#ffffff;--fg:#121a19;--muted:#55635f;--line:#d6e3e0;--accent:#1f8a7d;--ink:#111;--warn:#b4531b;--chip:#e2f1ee;--chipfree:#ece9f5;
--display:"Playfair Display",Georgia,serif;--body:"Karla",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0f1514;--card:#17201e;--fg:#e8f1ef;--muted:#9fb2ad;--line:#2a3633;--accent:#5fd0c0;--ink:#000;--warn:#f0985e;--chip:#1e3430;--chipfree:#272438;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0f1514;--card:#17201e;--fg:#e8f1ef;--muted:#9fb2ad;--line:#2a3633;--accent:#5fd0c0;--ink:#000;--warn:#f0985e;--chip:#1e3430;--chipfree:#272438;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 var(--body)}}
.wrap{{max-width:860px;margin:0 auto;padding-block:24px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:22px}}
h1{{font:600 2.1rem/1.1 var(--display);margin:0;text-wrap:balance}} h1 em{{color:var(--accent)}} h2{{font:600 1.3rem/1.2 var(--display);margin:0;text-wrap:balance}}
.sub{{color:var(--muted);margin:4px 0 0}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:grid;gap:10px;min-width:0}}
.ask{{border-left:4px solid var(--warn);background:var(--card);padding:14px 18px;border-radius:0 10px 10px 0;display:grid;gap:8px}}
.ask strong{{color:var(--warn)}} ol,ul{{margin:0;padding-left:20px;display:grid;gap:4px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}}
figure{{margin:0;display:grid;gap:6px;min-width:0}} figure img{{width:100%;max-width:100%;border-radius:6px;border:1px solid var(--line)}}
figcaption{{font:500 .75rem var(--mono);color:var(--muted)}}
.script li{{font:600 1.08rem/1.45 var(--body)}}
.shot{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:6px;min-width:0}}
.sh{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline}} .num{{font:600 1.4rem/1 var(--display);color:var(--accent)}} .win{{font:500 .8rem var(--mono);color:var(--muted)}}
.chip{{font:600 .7rem var(--body);letter-spacing:.08em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--chip)}} .chip.free{{background:var(--chipfree)}}
.say{{font:600 1.05rem/1.35 var(--body);margin:0}} .say::before{{content:"\\201C"}} .say::after{{content:"\\201D"}}
.see,.mv{{margin:0;font-size:.95rem}} summary{{cursor:pointer;color:var(--accent);font-weight:600}}
pre{{white-space:pre-wrap;font:500 .78rem/1.45 var(--mono);background:var(--bg);padding:10px;border-radius:6px;margin:6px 0 0;overflow-x:auto}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}} td,th{{border-bottom:1px solid var(--line);padding:6px 4px;text-align:left;vertical-align:top}} td.n,th.n{{text-align:right}}
.tot td{{font-weight:600;color:var(--accent)}} a{{color:var(--accent)}}
</style>
<div class="wrap">
<header><h1>buttah. Silky Soft <em>Towels</em></h1><p class="sub">Grace, 24 count travel pack. Music-only video, ~16 s, 7 shots, with a script Grace can voice later. Plan for your OK; nothing has been paid for yet.</p></header>
<section class="ask"><strong>Your OK needed (nothing runs until you answer)</strong><ol>
<li><b>Approve the plan</b> below: total <b>$3.09</b> on Kie (7 stills $0.63, 6 Omni clips $1.89, 1 Seedance $0.16, one likely redo $0.41). November so far $1.32 of $100.</li>
<li>Grace's hand sheet: <b>with</b> the gold bracelet or <b>without</b>?</li>
<li>Pouch size: the brand gives none. I used about 17 x 15 cm (a little wider than her hand), from the brand's in-hand photo. OK, or can Grace measure hers?</li>
<li>House of Rameau version after V1 ($0 re-cut, its own order and grade, on-screen hook text, no captions): yes or no?</li></ol></section>
<section class="box"><h2>Script for Grace (~16 s at her pace, grade 1.9)</h2><ol class="script">{script}</ol>
<p class="sub">Our cut has no voice: you add the music. Each shot sits on its line, so Grace's voiceover drops straight on. No on-screen text. Hook H006 from her library; other hook options: "Why did nobody tell me about these sooner?" (H010), "One small switch made washing my face so much easier." (H147, only if true for her).</p>
<p class="sub">Caption: me and my old washcloth are done. these are big, soft and you toss each one after. #ad #facetowel #disposablefacetowel #skincareroutine #travelessentials</p></section>
<section style="display:grid;gap:12px"><h2>Shots (4 HAND, 3 HAND-FREE)</h2>{shots}</section>
<section class="box"><h2>Real product (from the brand's own photos)</h2>
<div class="grid"><figure><img src="img/front.jpg" alt="Real Buttah pouch front"><figcaption>Real pouch front (buttahskin.com)</figcaption></figure></div>
<ul><li>Soft flat pouch, wider than tall, glossy mint-teal edges, crinkled sealed ends, matte black front.</li>
<li>Print: "buttah." white serif with a full stop; "Silky Soft Towels" teal, only "Towels" in italic; a window strip showing the towel; 3 round badges (biodegradable, eco friendly, natural fibers); THE WASHCLOTH UPGRADE / LARGE | SINGLE-USE | DRY OR WET / 24 COUNT.</li>
<li>Towels: plain white, small square waffle texture, 11.875 x 10.875 in open.</li>
<li>No listing photo shows how the pouch opens, so no shot pulls a towel out of it; the towels come off a stack beside it.</li></ul>
<figure><img src="img/sheet.jpg" alt="Product reference sheet"><figcaption>Product reference sheet passed on every product still and clip</figcaption></figure></section>
<section class="box"><h2>Rooms (real Pexels and Pixabay photos, no people)</h2><div class="grid">
<figure><img src="img/bath_A.jpg" alt="White vanity bathroom"><figcaption>White vanity: S1, S4</figcaption></figure><figure><img src="img/towel_bar.jpg" alt="Sink corner"><figcaption>Sink corner: S2</figcaption></figure>
<figure><img src="img/bath_B_teal.jpg" alt="Teal tile bathroom"><figcaption>Teal tiles: S3, S7</figcaption></figure><figure><img src="img/bedroom_teal.jpg" alt="Teal bedroom"><figcaption>Teal bedroom: S5</figcaption></figure>
<figure><img src="img/hotel.jpg" alt="Hotel room"><figcaption>Hotel room: S6</figcaption></figure></div></section>
<section class="box"><h2>What the winners do</h2><figure><img src="img/winner_maya.jpg" alt="Contact sheet of the @mayahome02 video"><figcaption>@mayahome02, 637.9K views (shop): packs on the counter, towel pulled, wet under the tap, end on the stock-up</figcaption></figure>
<ul><li>@enhancedbeautybykori, 1.9M views (shop): stock-up pile, "Everyone should have these in their car".</li>
<li>@dermarkologist, 203.6K views: a dermatologist says they are not needed, so the script makes no bacteria or breakout claim.</li>
<li>Buyers: "I can never go back", "I never thought about how dirty towels are, even when washed", "We always take them to Europe because they don't always have facecloths in the hotels". One Ulta buyer found Buttah rougher than Clean Skin Club, so "soft" is shown, not oversold.</li>
<li>Script gate: GATE OK (playbook, coach, viral board, facts, hooks, humanizer, readability, audience, line sources). TikTok's hashtag and viral scans came back empty today (tried twice); the keyword page gave the 3 winners above.</li></ul></section>
<section class="box"><h2>Cost</h2><div class="tw"><table><tr><th>Item</th><th class="n">$</th></tr>
<tr><td>7 stills, Gemini 3 Pro Image on Kie, 7 x $0.09</td><td class="n">0.63</td></tr>
<tr><td>6 Omni 1.1 Flash product clips on Kie, 6 x $0.315</td><td class="n">1.89</td></tr>
<tr><td>1 Seedance 2.0 Mini clip (S2, no product)</td><td class="n">0.164</td></tr>
<tr><td>One likely redo (1 still + 1 Omni), asked before it runs</td><td class="n">0.405</td></tr>
<tr class="tot"><td>Total</td><td class="n">3.09</td></tr></table></div>
<p class="sub">Order: all 7 stills at once, storyboard here for your look, then ONE test clip (S5, the riskiest), then the other 6 at once. About 35-40 min of machine time after your OK, plus your two review stops.</p></section>
</div>"""
Path("review/index.html").write_text(page); print(len(page))
