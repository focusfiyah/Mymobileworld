"""Review page for Ralph (newest on top). python3 build_review.py -> review/index.html"""
import json, html, re
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); SH = D["videos"][0]["shots"]; E = html.escape
ROOM = {"rooms/pick/kitchen_window.jpg": "kitchen window", "rooms/pick/kitchen_wood.jpg": "wood counter", "rooms/pick/office_plants.jpg": "desk with plants",
        "rooms/pick/dining.jpg": "dining table", "rooms/pick/counter_grey.jpg": "grey counter", "rooms/pick/kitchen_sage.jpg": "sage kitchen"}
MODEL = {"wan": "Flow ($0) or Wan $0.40", "seedance": "Seedance Mini $0.16"}
def cf(s): return f"prompts/{s['id']}_seedance.txt" if s["model"] == "seedance" else f"prompts/flow_{s['id']}.txt"
shots = "".join(f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span><span class="win">{s['t'][0]:.1f} to {s['t'][1]:.1f} s</span>
<span class="chip {'free' if not s['hand'] else ''}">{'HAND' if s['hand'] else 'HAND-FREE'}</span><span class="chip">{ROOM[s['room']]}</span><span class="chip">{MODEL[s['model']]}</span></div>
<p class="beat">{E(s['beat'])}</p><p class="see">{E(s['still'])}</p><p class="mv"><b>Motion:</b> {E(s['motion'])}</p>
<details><summary>Still prompt</summary><pre>{E(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>
<details><summary>{'Clip prompt (Seedance)' if s['model']=='seedance' else 'Clip prompt (Flow kit; Wan version in prompts/)'}</summary><pre>{E(Path(cf(s)).read_text())}</pre></details></article>""" for s in SH)
sc = Path("scripts.md").read_text()
rows = re.findall(r"^\| (\d) \| ([^|]+) \| ([^|]+) \|", sc, re.M)
script = "".join(f"<li><span class='bt'>{E(b.strip())}</span>{E(l.strip())}</li>" for _, b, l in rows)
rooms = "".join(f'<figure><img src="img/{Path(k).stem}.jpg" alt="{v}"><figcaption>{v}: {", ".join(s["id"] for s in SH if s["room"]==k)}</figcaption></figure>' for k, v in ROOM.items())
page = f"""<title>Red Jelliquid Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Figtree:wght@400;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: one reading column; decision box first, then script, shots, product truth, rooms, research, cost. Palette from the boxes: cream card, pomegranate red, ACV yellow. */
:root{{--bg:#faf6f4;--card:#ffffff;--fg:#2a1416;--muted:#6f5a5c;--line:#ead9d8;--accent:#c4122f;--acv:#e9d26a;--chip:#f8e3e5;--chipfree:#f6efcf;
--display:"Fraunces",Georgia,serif;--body:"Figtree",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#170e0f;--card:#221617;--fg:#f5e9e9;--muted:#bba3a5;--line:#3a2a2c;--accent:#ff5a6e;--acv:#d8c35e;--chip:#3a1d21;--chipfree:#38321a;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#170e0f;--card:#221617;--fg:#f5e9e9;--muted:#bba3a5;--line:#3a2a2c;--accent:#ff5a6e;--acv:#d8c35e;--chip:#3a1d21;--chipfree:#38321a;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}}
.wrap{{max-width:820px;margin:0 auto;padding-block:24px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:22px}}
h1{{font:600 2.2rem/1.1 var(--display);margin:0;text-wrap:balance}} h1 em{{color:var(--accent);font-style:normal}} h2{{font:600 1.3rem/1.2 var(--display);margin:0;text-wrap:balance}}
.sub{{color:var(--muted);margin:0}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:grid;gap:10px;min-width:0}}
.ask{{border-left:4px solid var(--accent);background:var(--card);padding:14px 18px;border-radius:0 10px 10px 0;display:grid;gap:8px}}
.ask strong{{color:var(--accent)}} ol,ul{{margin:0;padding-left:20px;display:grid;gap:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
figure{{margin:0;display:grid;gap:6px;min-width:0}} figure img{{width:100%;max-width:100%;border-radius:6px;border:1px solid var(--line)}}
figcaption{{font:500 .75rem var(--mono);color:var(--muted)}}
.script{{list-style:none;padding:0;gap:8px}} .script li{{font:600 1.06rem/1.4 var(--body);display:grid;gap:2px}}
.bt{{font:600 .68rem var(--body);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}}
.shot{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:6px;min-width:0}}
.sh{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline}} .num{{font:600 1.4rem/1 var(--display);color:var(--accent)}} .win{{font:500 .8rem var(--mono);color:var(--muted);font-variant-numeric:tabular-nums}}
.chip{{font:600 .68rem var(--body);letter-spacing:.08em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--chip)}} .chip.free{{background:var(--chipfree)}}
.beat{{font:600 1.02rem/1.35 var(--body);margin:0}} .see,.mv{{margin:0;font-size:.95rem}} summary{{cursor:pointer;color:var(--accent);font-weight:600}}
summary:focus-visible,a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
pre{{white-space:pre-wrap;font:500 .78rem/1.45 var(--mono);background:var(--bg);padding:10px;border-radius:6px;margin:6px 0 0;overflow-x:auto}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}} td,th{{border-bottom:1px solid var(--line);padding:6px 4px;text-align:left;vertical-align:top}} td.n,th.n{{text-align:right}}
.tot td{{font-weight:700;color:var(--accent)}} a{{color:var(--accent)}}
.sticks{{display:flex;gap:6px;align-items:center}} .sticks i{{display:block;width:10px;height:34px;border-radius:2px;background:linear-gradient(var(--accent) 0 30%,#fff 30% 75%,var(--accent) 75%);border:1px solid var(--line)}}
.sticks i:nth-child(2){{background:linear-gradient(#b0102b 0 25%,#fff 25% 70%,var(--accent) 70%)}} .sticks i:nth-child(3){{background:linear-gradient(var(--acv) 0 25%,#fff 25% 70%,var(--accent) 70%)}}
</style>
<div class="wrap">
<header style="display:grid;gap:6px"><div class="sticks" aria-hidden="true"><i></i><i></i><i></i></div><h1>FOODOLOGY Red <em>Jelliquid</em> Bundle</h1>
<p class="sub">Grace. Cutting Jelly + ACV Apple Jelly + Drink Mix PRO. A 12 s music-only video (6 shots) plus a standard ~30 s script Grace can record later. Plan for your OK: nothing has been paid for yet.</p></header>
<section class="ask"><strong>Approved and in Drive (2026-11-03)</strong><ol>
<li>Drive: <a href="https://drive.google.com/drive/folders/1u1rlGuihgxPJbaQT2yMu-i3934-eImVy">FOODOLOGY Red Jelliquid (Grace)</a>: CURRENT - FOODOLOGY Jelliquid V1 (Grace, no text, no sound), CURRENT - Jelliquid HofR V1, the script doc and the research verdict doc.</li>
<li>House of Rameau version below: hook card "wait, this is apple cider vinegar?" from frame 0 for 2.4 s (hook check OK), its own shot order, in-points, a 1.12x punch-in and a cooler grade, no captions, no sound. It posts to @houseoframeau only on your OK.</li>
<li>Kie spend: $3.83 ($3.19 book + $0.64 you OK'd for the S3/S6 redo).</li></ol></section>
<section class="box"><h2>House of Rameau V1</h2><video src="hofr_v1.mp4" controls playsinline muted loop style="width:100%;max-width:520px;border-radius:8px"></video></section>
<section class="box"><h2>Grace V1 (approved)</h2><video src="cut_v1.mp4" controls playsinline muted loop style="width:100%;max-width:520px;border-radius:8px"></video></section>
<details class="box"><summary><b>Clips</b> (S3, S6 = Wan r2)</summary>CLIPS</details>
<details class="box"><summary><b>Storyboard r1</b> (approved; small print let go)</summary><div class="grid">STORY</div></details>
<details class="box"><summary><b>Plan you approved</b> (all on Kie $3.19; no-jewellery hand; House of Rameau version yes)</summary>

<section class="box"><h2>Script for Grace (~30 s at her pace, 102 words, grade 2.5)</h2><ol class="script">{script}</ol>
<p class="sub">Leads with the hook (looks like candy, it's apple cider vinegar), then answers the question buyers ask most in the comments: "which one, and when?". Hook H099 from her library; other options H017 "I want apple cider vinegar without having to drink the vinegar", H051 "These make more sense once you see when each one goes". No weight, fat, debloat or GLP-1 lines: the listing makes them, Grace can't. No price.</p>
<p class="sub">Caption: apple cider vinegar you chew, plus which stick goes when. red drink mix in the morning, red chia jelly after lunch, yellow ACV whenever. #foodology #cuttingjelly #acvjelly #koreanjelly #tiktokshop #ad</p></section>
<section style="display:grid;gap:12px"><h2>Shots, 12 s, music only (3 HAND, 3 HAND-FREE)</h2>{shots}</section>
<section class="box"><h2>Real product (FOODOLOGY's own photos match yours)</h2>
<div class="grid"><figure><img src="img/ralph.jpg" alt="Ralph's photo of the three boxes and sticks"><figcaption>Your photo (Telegram)</figcaption></figure></div>
<ul><li>Three upright cream-white boxes with a red bottom third. Cutting Jelly: coleus rosette, "Garcinia Cambogia Extract 1,200mg". Drink Mix PRO: a little wider, "For Women", "Coleus Forskohlii Extract 500 mg". ACV Apple Jelly: red apple with a yellow "Jelly!" burst, "Apple Cider Vinegar 6,250 mg".</li>
<li>Jelly sticks: flat white film, red bottom band, a dashed OPEN tear line; the jelly is a firm block pushed out of the torn top (Cutting Jelly ruby red with black chia seeds; ACV pale lemon yellow).</li>
<li>Drink Mix PRO stick: red top, white middle, red bottom; pink-red powder, 1 stick in 17 oz cool water.</li>
<li>Uses from the listings: drink mix in the morning, Cutting Jelly after a meal, ACV jelly anytime.</li></ul>
<figure><img src="img/sheet.jpg" alt="Product reference sheet"><figcaption>Product reference sheet (real pixels) passed on every product still and clip, plus a close-up of each stick and box print</figcaption></figure></section>
<section class="box"><h2>Rooms (real Pexels and Pixabay photos, no people)</h2><div class="grid">{rooms}</div></section>
<section class="box"><h2>What the winners do</h2><figure><img src="img/winner_bundle.jpg" alt="Contact sheet of the @yagirlcedes bundle video"><figcaption>@yagirlcedes, 1.7M views (shop, 3-in-1 Jelly Bundle): sticks fanned in one hand, jelly pushed out, each colour gets a job, "It's in the cart."</figcaption></figure>
<ul><li>@ilovebubbies 5.5M, @yagirlcedes 1.9M ("I can't tell if it's jello or a snack"), @yannnique 1.8M: all Cutting Jelly shop videos; every one leans on body claims we leave out.</li>
<li>Top buyer question in 319 comments: "It says to take 1 a day after meal but WHICH MEAL?!", "Do you eat both together, and when do you eat it?". The set answers it, so the script does too.</li>
<li>Script gate: GATE OK (playbook, audience + VOC, Grace's research workflow, coach, viral board, facts, hooks, humanizer, readability, line sources). TikTok hashtag pages came back empty today; the keyword pages gave the winners above.</li></ul></section>
</details>
<section class="box"><h2>Cost</h2><div class="tw"><table><tr><th>Item</th><th class="n">$</th></tr>
<tr><td>6 stills, Gemini 3 Pro Image on Kie, 6 x $0.09</td><td class="n">0.54</td></tr>
<tr><td>5 product clips as Flow kits in your app (60 credits)</td><td class="n">0.00</td></tr>
<tr><td>1 Seedance 2.0 Mini clip (S5, jelly only, no packaging)</td><td class="n">0.164</td></tr>
<tr><td>One likely still redo, asked before it runs</td><td class="n">0.09</td></tr>
<tr class="tot"><td>Total (Flow route)</td><td class="n">0.79</td></tr>
<tr><td>All on Kie instead: 5 Wan 3.0 720P clips (5 x $0.40) + one Wan redo</td><td class="n">3.19</td></tr></table></div>
<p class="sub">Order: all 6 stills at once, storyboard here for your look, then the Flow kits (S1 first, the riskiest) and S5 on Seedance. About 35 to 40 min of machine time after your OK, plus your stops.</p></section>
</div>"""
ST=[("S1","PASS","ACV print right; Korean small text invented"),("S2","PASS","pour + pink water; stick drops PRO"),("S3","PASS","box print right"),("S4","PASS","chia jelly, grip"),("S5","PASS","jelly only"),("S6","CHECK","small print: 6,290 mg, Dely Care, BMP seals")]
page=page.replace("STORY","".join(f'<figure><img src="st/{i}_r1.jpg" alt="{i} still"><figcaption><b>{i} {v}</b> {n}</figcaption></figure>' for i,v,n in ST))
page=page.replace("CLIPS","".join(f'<figure><figcaption><b>{c}</b> {n}</figcaption><video src="clips/{c}.mp4" controls playsinline muted loop style="width:100%;max-width:520px;border-radius:8px"></video></figure>' for c,n in [("S1","ACV stick, clean"),("S2","drink mix pour, clean"),("S3","Wan r2, clean"),("S4","cut uses 0-1.8 s"),("S5","chia jelly, clean"),("S6","Wan r2, clean")]))
Path("review/index.html").write_text(page); print(len(page))
