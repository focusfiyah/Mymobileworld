"""Review page for Vans V13-V17 (one page per job, republished each round). python3 review/build.py -> review/index.html"""
import html, json, re
from pathlib import Path

J = Path(__file__).resolve().parent.parent
S = json.loads((J / "shots.json").read_text())
L = json.loads((J / "tools/labels.json").read_text())
book = (J / "BOOK.md").read_text()
total = re.search(r"\nTOTAL: \$([\d.]+)", book).group(1)
e = html.escape
LOOK = {"V13": ("Cafe", "Green cafe + stone cafe sidewalk", "Light-wash straight jeans, cream knit cuff", "Black satin slip midi skirt"),
        "V14": ("Bedroom", "Sage-green bedroom + sunny park path", "Grey joggers, oatmeal sweatshirt cuff", "Cream pleated satin midi skirt"),
        "V15": ("Living room", "Teal sofa living room + cobblestone alley", "Brown corduroy pants, camel sweater cuff", "Red and black plaid mini skirt"),
        "V16": ("Loft", "Colourful brick loft + rainbow painted steps", "Olive cargo pants, black ribbed cuff", "White wide-leg linen trousers"),
        "V17": ("Kitchen", "Bright kitchen with a mint table + wooden boardwalk", "Cream wide-leg sweatpants, denim cuff", "Pastel floral midi dress")}
LOGO = {"real_vans_tab.jpg": "side tab", "real_heel_label.jpg": "heel label", "real_insole_logo.jpg": "insole"}
CAP = {m.group(1): m.group(2) for m in re.finditer(r"- (V1\d) [^:]+: (.+)", (J / "scripts.md").read_text())}

vids = []
for v, (name, place, main, dress) in LOOK.items():
    rows = []
    for k, s in S.items():
        if s["video"] != v: continue
        logos = ", ".join(LOGO[x.split("/")[-1]] for x in s["clip_refs"] if x.split("/")[-1] in LOGO)
        kind = "hand" if s["kind"] == "HAND" else "free"
        test = " test" if k == "V14B" else ""
        rows.append(f'<tr class="{kind}{test}"><td class="t">{s["window"][0]:.1f}–{s["window"][1]:.1f}</td>'
                    f'<td class="say">{e(s["line"])}</td><td>{e(L[k].replace(" (TEST CLIP)", ""))}'
                    f'{"<span class=chip>test clip</span>" if test else ""}</td>'
                    f'<td><span class="chip {kind}">{s["kind"].lower()}</span></td><td class="lg">{logos}</td></tr>')
    vids.append(f"""<section class="vid" id="{v.lower()}">
  <div class="vhead"><span class="vnum">{v}</span><h2>{name}</h2></div>
  <div class="looks"><figure><img src="img/{v}_in.jpg" alt="{name} indoor place photo" loading="lazy"><figcaption>Inside</figcaption></figure>
  <figure><img src="img/{v}_out.jpg" alt="{name} outdoor place photo" loading="lazy"><figcaption>Outside</figcaption></figure>
  <dl><dt>Places</dt><dd>{place}</dd><dt>Everyday</dt><dd>{main}</dd><dt>Dress it up</dt><dd>{dress}</dd><dt>Caption</dt><dd>{e(CAP.get(v, ''))}</dd></dl></div>
  <div class="tw"><table><thead><tr><th>Time (s)</th><th>Grace says</th><th>On screen</th><th>Shot</th><th>Logos</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</section>""")

prompts = "".join(f'<details><summary>{k} · {e(L[k].replace(" (TEST CLIP)", ""))}</summary><p class="pl">Still ({len(s["still_refs"])} refs: {", ".join(r.split("/")[-1] for r in s["still_refs"])})</p>'
                  f'<pre>{e(s["still"])}</pre><p class="pl">Clip (Omni 4 s; image 1 = the approved still)</p><pre>{e(s["clip"])}</pre></details>' for k, s in S.items())

CUTS2 = "".join(f'<figure class="cut"><video src="media/{v}_v2.mp4" controls playsinline preload="metadata"></video><figcaption>{v} {LOOK[v][0]} v2</figcaption></figure>' for v in LOOK)
CUTS = "".join(f'<figure class="cut"><video src="media/{v}_v1.mp4" controls playsinline preload="metadata"></video><figcaption>{v} {LOOK[v][0]}</figcaption></figure>' for v in LOOK)
SB = "".join(f'<figure class="sb"><img src="img/sb_{v}.jpg" alt="{v} storyboard, 11 stills" loading="lazy"><figcaption>{v} {LOOK[v][0]}: A to K left to right, top row then bottom</figcaption></figure>' for v in LOOK)
page = f"""<title>Vans V13–V17 Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: one column; ask first, then Grace's post + voice, the five videos as place strips + shot tables, cost, prompts */
:root{{
  --bg:#f2f4f3; --card:#ffffff; --fg:#1b2420; --muted:#5a6762; --line:#d9e0dc;
  --accent:#2c55a8; --warn:#c2552d; --chip:#e6eeea; --free:#efe9f6; --test:#fff4e0;
  --display:"Barlow Condensed","Arial Narrow",sans-serif; --body:"Source Sans 3",system-ui,sans-serif; --mono:"JetBrains Mono",ui-monospace,monospace;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121815;--card:#1a221e;--fg:#e6ece9;--muted:#9aa8a2;--line:#2b3631;--accent:#8fb0f0;--warn:#f08a62;--chip:#24302b;--free:#2a2433;--test:#3a3020;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121815;--card:#1a221e;--fg:#e6ece9;--muted:#9aa8a2;--line:#2b3631;--accent:#8fb0f0;--warn:#f08a62;--chip:#24302b;--free:#2a2433;--test:#3a3020;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 var(--body)}}
.wrap{{max-width:900px;margin:0 auto;padding-block:24px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:22px}}
h1{{font:700 2.3rem/1.05 var(--display);margin:0;text-wrap:balance}}
h2{{font:700 1.45rem/1.1 var(--display);margin:0;letter-spacing:.02em}}
.sub{{color:var(--muted);margin:6px 0 0}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:grid;gap:10px;min-width:0}}
.ask{{border-left:4px solid var(--warn);background:var(--card);padding:14px 18px;border-radius:0 10px 10px 0;display:grid;gap:8px}}
.ask strong{{color:var(--warn)}} .ask ol{{margin:0;padding-left:20px;display:grid;gap:6px}}
.total{{font:700 2rem/1 var(--display);color:var(--accent)}}
.media{{display:grid;grid-template-columns:minmax(0,220px) 1fr;gap:16px;align-items:start}}
.media video{{width:100%;border-radius:8px;background:#000}}
.media audio{{width:100%}}
.script p{{margin:0 0 6px}} .script .t{{font:500 .78rem var(--mono);color:var(--muted);margin-right:6px}}
.vid{{display:grid;gap:12px}}
.vhead{{display:flex;align-items:baseline;gap:10px}}
.vnum{{font:700 1.6rem/1 var(--display);color:var(--accent)}}
.looks{{display:grid;grid-template-columns:repeat(2,minmax(0,140px)) 1fr;gap:12px;align-items:start}}
.looks figure{{margin:0}} .looks img{{border-radius:8px;aspect-ratio:9/16;object-fit:cover;width:100%;display:block}}
.looks figcaption{{font-size:.78rem;color:var(--muted)}}
dl{{margin:0;display:grid;grid-template-columns:max-content 1fr;gap:4px 12px;min-width:0}}
dt{{font:600 .72rem var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding-top:3px}} dd{{margin:0}}
.tw{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}}
table{{border-collapse:collapse;width:100%;font-size:.92rem;min-width:640px}}
th{{text-align:left;font:600 .72rem var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:10px 10px;border-bottom:1px solid var(--line)}}
td{{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
tr:last-child td{{border-bottom:0}}
td.t{{font:500 .78rem var(--mono);white-space:nowrap;font-variant-numeric:tabular-nums;color:var(--muted)}}
td.say{{font-style:italic;color:var(--muted);max-width:240px}} td.lg{{font-size:.82rem;color:var(--muted)}}
tr.test td{{background:var(--test)}}
.chip{{font:600 .68rem var(--body);letter-spacing:.08em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background:var(--chip);white-space:nowrap;margin-left:6px}}
.chip.free{{background:var(--free)}} td .chip.hand,td .chip.free{{margin-left:0}}
.cost table{{min-width:0}} .cost td:last-child,.cost th:last-child{{text-align:right;font-variant-numeric:tabular-nums}}
details{{border-top:1px solid var(--line);padding:8px 0}} summary{{cursor:pointer;font-weight:600}}
pre{{white-space:pre-wrap;font:500 .78rem/1.5 var(--mono);background:var(--bg);padding:10px;border-radius:8px;margin:6px 0;overflow-x:auto}}
.pl{{margin:8px 0 0;font-size:.82rem;color:var(--muted)}}
.sb{{margin:0}} .sb img{{width:100%;border-radius:8px;display:block}} .sb figcaption{{font-size:.8rem;color:var(--muted);margin-top:4px}}
.cuts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}} .cut{{margin:0}} .cut video{{width:100%;border-radius:8px;background:#000}} .cut figcaption{{font-size:.8rem;color:var(--muted)}}
.truth img{{border-radius:8px;max-width:360px;width:100%}}
ul.facts{{margin:0;padding-left:20px;display:grid;gap:3px}}
@media (max-width:620px){{.media{{grid-template-columns:1fr}} .media video{{max-width:240px}} .looks{{grid-template-columns:repeat(2,minmax(0,1fr))}} .looks dl{{grid-column:1/-1}}}}
</style>
<main class="wrap">
<header><h1>Vans sequin V13–V17</h1><p class="sub">Five AI videos on Grace's own voice, one look each. Plan approved 29 Oct 2026. Cut v3 below.</p></header>

<div class="ask"><strong>Cut v3: V14 and V17 fixed, ready for your OK</strong>
<div>Your notes, fixed ($0.76): V14's pair-on-the-floor shot redone with checkerboard all over (the only black left is the real heel stripe), V14's walk now steps toward the camera and then cuts to her side-on step on the path, and V17's walk is a side-on walk on the boardwalk with real steps. Nothing slides. V13, V15, V16 unchanged.</div>
<ol><li>Approve, and I'll put all five in Drive "Vans sequin (Grace)" as CURRENT - Vans V13 to V17 with the captions.</li></ol>
<div class="cuts"><figure class="cut"><video src="media/V14_v3.mp4" controls playsinline preload="metadata"></video><figcaption>V14 Bedroom v3</figcaption></figure><figure class="cut"><video src="media/V17_v3.mp4" controls playsinline preload="metadata"></video><figcaption>V17 Kitchen v3</figcaption></figure></div></div>
<div class="ask"><strong>Cut v2 (V13, V15, V16 approved as is)</strong>
<div>The 4 redos are in ($0.66): the V14 walk keeps her feet under the camera, the V16 pair holds still, and V16/V17 use only the steady part of their holds. I also caught Grace's blue band on her wrist in V16's last shot (a removed item) and cropped it out free. QC on all five: audio = Grace's VO, no flashes or dark frames, every REMOVED.md item checked. Spent $16.07 of $24.30.</div>
<ol><li>Approve the five, and I'll put them in Drive "Vans sequin (Grace)" as CURRENT - Vans V13 to V17 with the captions.</li><li>Or tell me what to change.</li></ol>
<div class="cuts">{CUTS2}</div></div>
<div class="ask"><strong>Cut v1 (replaced by v2)</strong>
<div>Each cut is 27.5 s on Grace's own voice, in Grace's edit style (hand shot first, cuts on each phrase, a quick hand-shot close). My QC: audio matches her VO exactly, no flashes or dark frames, levels OK, clean edges at 2x on every first second, cut gate OK. Spent $15.41 of $24.30.</div>
<ol><li><strong>4 shots still in these cuts fail my check</strong> and need a redo, $0.66 (4 × $0.164): V14 at 16.1–19.8 s (feet drift away on the walk), V16 at 2.8–5.2 s (the held pair turns), V16 at 19.8–22.1 s and V17 at 19.8–22.1 s (the held shoe rotates). OK to redo them?</li>
<li>Anything else you want changed in the five cuts?</li></ol>
<div class="cuts">{CUTS}</div>
<figure class="sb"><img src="img/first_second_2x.jpg" alt="First second of each video at 2x"><figcaption>First second of V13–V17 at 2x (0.0 s top, 0.8 s bottom)</figcaption></figure></div>
<div class="ask"><strong>Re-test V14B: Seedance won ("Ok on seed")</strong>
<div>Seedance 2.0 Mini from our exact still ($0.164): the side tab reads VANS, the black squares look like sequins, Grace's long pink French tips, no band on the wrist, five fingers. Omni with the fixed prompt ($0.315): the tab still garbled ("LGCDI"), the squares still drawn as outlines. Spent $6.55 of $24.30.</div>
<ol><li>Run the other 54 clips on Seedance 2.0 Mini: 54 × $0.164 = <strong>$8.86</strong> (instead of $17.01 on Omni). It's Seedance, not the Omni product lock, so every clip gets the 2x logo check before you see it.</li></ol>
<div class="media"><video src="media/V14B_seedance.mp4" controls playsinline muted preload="metadata"></video><video src="media/V14B_omni2.mp4" controls playsinline muted preload="metadata"></video></div>
<p class="sub">Left: Seedance (winner). Right: Omni, fixed prompt.</p>
<figure class="sb"><img src="img/V14B_test2_2x.jpg" alt="2x: top row Omni with a garbled tab, bottom row Seedance with VANS readable"><figcaption>2x at 0.5, 1.8, 3.2 s. Top: Omni (tab "LGCDI"). Bottom: Seedance (tab VANS).</figcaption></figure></div>
<div class="ask"><strong>First test clip V14B (Omni): failed my check</strong>
<div>The 9 redone stills all pass. The V14B test clip on Omni ($0.315) fails: the side tab reads "VANDO", the black squares came out as scribbled outlines instead of sequins, the hands lost Grace's long French tips and bracelets, and the blue band sits on her wrist (a removed item). Omni on Kie also re-framed the shot instead of starting from our still. Spent $6.07 of $24.30.</div>
<ol>
<li>Test V14B again two ways, side by side, then run the other 54 on the winner: Seedance 2.0 Mini starting from our exact still ($0.164) and Omni with a fixed prompt (Grace's hand reference added, band stays on her finger) ($0.315). Both: <strong>$0.48</strong>.</li>
<li>If Seedance wins, the 54 clips cost $8.86 instead of $17.01.</li>
</ol>
<div class="media"><video src="media/V14B_omni.mp4" controls playsinline muted preload="metadata"></video><figure class="sb"><img src="img/V14B_2x.jpg" alt="V14B test clip at 2x: garbled side tab, outline squares, short nails, blue band"><figcaption>2x at 0.0, 1.5, 2.4, 3.5 s</figcaption></figure></div></div>
<div class="ask"><strong>Storyboard, round 1</strong>
<div>Done: the 9 failed stills were redone ($0.81) and all pass (sheet below).</div>
<ol>
<li>OK to redo the 9 stills ($0.81) and run the V14B test clip ($0.315)?</li>
<li>Anything in the 46 passing stills you want changed before the clips? (A free swap now saves a paid clip later.)</li>
</ol>
<p class="sub">Your plan answers (29 Oct): everything on Kie, looks OK, Grace's hand as on V12, 11 shots per video, 5 videos, no House of Rameau versions.</p></div>
<section class="box"><h2>Storyboard round 1 (stills)</h2>
<p class="sub">Fails, already fixed in the prompts: V13A, V13I, V15D, V15G solid black toe (the real toe is checkerboard) · V14H, V16J empty shoe on a walking foot · V14G feet pointing opposite ways · V15A no grip · V14B holds a loose shoe instead of tightening the bow.</p>
<figure class="sb"><img src="img/r1_fails.jpg" alt="The 9 failed stills, each labelled with its fault" loading="lazy"><figcaption>The 9 failed stills, each with its fault</figcaption></figure>
{SB}
</section>

<section class="box"><h2>Grace's post and voice</h2>
<div class="media"><video src="media/grace_post.mp4" controls playsinline preload="metadata"></video>
<div class="script"><audio src="media/grace_vo.mp3" controls preload="none"></audio>
<p class="sub">Her audio, used as posted. I split it to check for music: the music part measured −68.6 dB (silent), so there is nothing under her voice to remove.</p>
{''.join(f'<p><span class="t">{S["V13" + b]["window"][0]:.1f}</span>{e(S["V13" + b]["line"])}</p>' for b in "ABCDEFGHIJK")}
</div></div></section>

<section class="box"><h2>How they're cut: Grace's own style</h2><p>From her PRITECH re-edit (in force since 28 Oct), all free: every video opens on the shoe moving in her hand at frame 0, cuts land on the first word of each phrase, and the last line closes on a quick run of that video's own hand shots (0.3–0.6 s each) instead of one held ending.</p></section>
{''.join(vids)}

<section class="box truth"><h2>The real shoe (Vans' own photos)</h2>
<img src="img/product_sheet.jpg" alt="Real Vans Premium Authentic sequin checkerboard from every side" loading="lazy">
<ul class="facts">{''.join(f'<li>{e(f)}</li>' for f in json.loads((J / "product_truth.json").read_text())["facts"][:9])}</ul>
<p class="sub">New in these prompts vs V12: the black tongue and the vertical black heel stripe are named. Every side-on shot says which shoe of the pair faces the lens, so the side tab is always on the visible side.</p></section>

<section class="box cost"><h2>Cost</h2><div class="tw"><table><thead><tr><th>Item</th><th>Qty × unit</th><th>$</th></tr></thead><tbody>
<tr><td>Stills, Gemini 3 Pro Image on Kie</td><td>55 × $0.09</td><td>4.95</td></tr>
<tr><td>Clips, Omni 1.1 Flash 4 s on Kie</td><td>55 × $0.315</td><td>17.33</td></tr>
<tr><td>…or the clips in your Flow app (660 credits)</td><td>55 × $0</td><td>0.00</td></tr>
<tr><td>One likely redo per video, each asked first</td><td>5 × $0.405</td><td>2.03</td></tr>
<tr><td><strong>Total cap</strong></td><td></td><td><strong>{total}</strong></td></tr></tbody></table></div>
<p class="sub">ElevenLabs 0 characters (Grace's own voice). October so far $201.62, no cap this month; anything that runs after Oct 31 counts toward November's $100.</p>
<p class="sub">Time: about 85 min of machine time plus your three stops (storyboard, the V14B test clip, the five cuts).</p></section>

<section class="box"><h2>Every prompt (55 stills + 55 clips)</h2><p class="sub">Written with prompt-master, all lint clean. Tap a shot to read both prompts.</p>{prompts}</section>
</main>
"""
(J / "review/index.html").write_text(page)
print("review/index.html", len(page), "chars")
