"""Builds review/index.html (plan v1) from shots.json, scripts.md and BOOK.md numbers."""
import json, html
from pathlib import Path
J = Path(__file__).parent
S = json.load(open(J / "shots.json"))["shots"]
script = (J / "scripts.md").read_text().split("## Spoken\n")[1].split("\n\n")[0]
e = html.escape
rows = "".join(f"<tr><td>{x['id']}</td><td class=n>{x['t'][0]:.1f}–{x['t'][1]:.1f}</td><td>“{e(x['line'])}”</td>"
               f"<td><span class='pill {'h' if x['hand'] else 'f'}'>{'HAND' if x['hand'] else 'HAND-FREE'}</span></td>"
               f"<td>{'Omni $0.315' if x['model']=='omni' else 'Seedance $0.164'}</td><td>{x['room']}</td></tr>" for x in S)
prompts = "".join(f"<details><summary>{x['id']} · {e(x['line'])}</summary><h4>Still ({len(x['still_refs'])} refs)</h4><pre>{e(x['still'])}</pre>"
                  f"<h4>Clip · {x['model']} ({len(x['clip_refs'])} refs)</h4><pre>{e(x['clip'])}</pre></details>" for x in S)
page = f"""<title>Earth Breeze Sheets Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Atkinson+Hyperlegible:wght@400;700&display=swap">
<style>
/* layout: one reading column, laundry-room blues, plan sections in order of Ralph's decision */
:root{{--bg:#f3f7fa;--fg:#13283b;--muted:#4f6577;--line:#cfdbe5;--card:#ffffff;--accent:#1d4f91;--fresh:#1f8a4c;--warn:#a3561b;
--display:'Fraunces',Georgia,serif;--body:'Atkinson Hyperlegible',system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0e1822;--fg:#e4edf4;--muted:#9fb3c3;--line:#26394a;--card:#152331;--accent:#8fb8ef;--fresh:#5fc98c;--warn:#e7a46c;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0e1822;--fg:#e4edf4;--muted:#9fb3c3;--line:#26394a;--card:#152331;--accent:#8fb8ef;--fresh:#5fc98c;--warn:#e7a46c;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}}
main{{max-width:880px;margin:0 auto;padding-block:28px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:30px}}
h1,h2{{font-family:var(--display);font-weight:600;text-wrap:balance;margin:0}} h1{{font-size:2rem}} h2{{font-size:1.35rem;color:var(--accent)}}
.eyebrow{{text-transform:uppercase;letter-spacing:.08em;font-size:.75rem;color:var(--muted)}}
section{{display:grid;gap:12px}} p{{margin:0;max-width:65ch}}
blockquote{{margin:0;padding:16px 18px;background:var(--card);border:1px solid var(--line);border-radius:10px;font-size:1.1rem}}
.total{{display:flex;flex-wrap:wrap;gap:8px 24px;align-items:baseline;padding:16px 18px;background:var(--card);border:2px solid var(--accent);border-radius:10px}}
.total b{{font-family:var(--display);font-size:2rem;color:var(--accent)}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:.92rem;min-width:640px}}
td,th{{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left;vertical-align:top}} .n{{font-variant-numeric:tabular-nums;white-space:nowrap}}
.pill{{font-size:.72rem;font-weight:700;padding:2px 8px;border-radius:99px;white-space:nowrap}} .h{{background:var(--accent);color:var(--bg)}} .f{{background:var(--fresh);color:var(--bg)}}
img{{max-width:100%;border-radius:8px;border:1px solid var(--line);display:block}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}} .two>*{{min-width:0}}
ol{{margin:0;padding-left:1.2em;display:grid;gap:8px}} .q li{{padding:10px 12px;background:var(--card);border:1px solid var(--line);border-radius:8px}}
details{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px}} summary{{cursor:pointer;font-weight:700}}
pre{{white-space:pre-wrap;font-size:.82rem;background:var(--bg);padding:10px;border-radius:6px;margin:4px 0 10px}} h4{{margin:8px 0 0}}
.small{{color:var(--muted);font-size:.88rem}}
</style>
<main>
<header style="display:grid;gap:6px"><span class=eyebrow>Grace · cut v1 · 30 Oct 2026</span><h1>Earth Breeze Laundry Detergent Sheets</h1>
<p class=small>One 15-20 s hands + hand-free video over the Grace cloned v5 voice. Kie only. Script gate: GATE OK.</p></header>
<div class=total><span>Total, one approval</span><b>$3.75</b><span class=small>Kie, includes one likely redo. ElevenLabs ~300 chars. October so far $232.92 (no cap this month).</span></div>
<section><h2>Cut v1 · 17.2 s · for your OK</h2><div class=two><figure style=margin:0><video src="earth_breeze_v1.mp4" controls playsinline preload="metadata" style="width:100%;border-radius:8px"></video><figcaption class=small>Grace's version: no text, AI finish on.</figcaption></figure><figure style=margin:0><video src="earth_breeze_hor_v1.mp4" controls playsinline preload="metadata" style="width:100%;border-radius:8px"></video><figcaption class=small>House of Rameau version: own framing, in-points and cooler grade, hook text from frame 0 (HOOK_OK), no captions. Posts only on your OK.</figcaption></figure></div>
<p class=small>QC: every cut within 0.1 s of its line, no freeze or black frames, -17 LUFS, voice echo 150 ms (passes), hands and edges clean at 2x, REMOVED.md checked. Washer brand logos cropped (S1, S4, S7) or softly blurred (S3), free. One flag: in S8 the two boxes' small print slips at 2x ("LOAOS", "NO NARSH" on one box); hard to see at phone size, so I let it go rather than spend. Kie $3.52 of $3.75.</p>
<img src="storyboard_final.jpg" alt="Final stills S1 to S9"></section>
<section><h2>Storyboard round 1 · 9 stills</h2><img src="storyboard_r1.jpg" alt="Nine stills S1 to S9"><p class=small>Good: S1-S7 (S5 and S7 print match the real box letter for letter at 2x; hands grip, whole wrists). Redo asked: S9 drew a made-up box design; S8 boxes too far, print garbled at 2x. The washer brand logos (Electrolux, Indesit) get blurred or cropped for free in the cut.</p></section>
<section><h2>Script · 58 words · grade 3.7</h2><blockquote>{e(script)}</blockquote>
<p class=small>Hook H094, modeled on the three biggest sheet videos (1.7M, 339K, 290K): all open on the sheet melting in water. Top search: “do laundry detergent sheets work”. “No harsh chemical residue” is the box's own wording. Thanksgiving is 26 Nov. Sources per line in research/line_sources.md.</p></section>
<section><h2>Questions</h2><ol class=q>
<li><b>Hand sheet:</b> without the bracelet (my default) or with it? Both shown below.</li>
<li><b>S1, S2, S6</b> show only the plain white sheet, no print. Keep them on Omni like the product-lock rule (in the total), or Seedance to save $0.45?</li>
<li><b>House of Rameau version</b> (free re-cut, different order and grade) with hook text “this is a whole load of laundry” from frame 0, no captions: yes?</li></ol></section>
<section><h2>Shots · 9 · 4 hand-free</h2><div class=tw><table><tr><th>#</th><th>s</th><th>Words</th><th>Hand</th><th>Clip</th><th>Room</th></tr>{rows}</table></div>
<p class=small>S1 drop sheet on water · S2 melts (top-down) · S3 heavy plain jug, blue drip · S4 clean navy tee · S5 pull a sheet from the top slot · S6 toss in the drum · S7 box on the washer · S8 two boxes on guest towels · S9 one box toward the lens. Riskiest first: S5.</p></section>
<section><h2>Product truth</h2><p>Built from the 8 listing images only (no real photos from Grace). Flat slim box ~25 × 16 × 1 cm, sheets slide out a slot on the top edge, each sheet plain white 14 × 11 cm with no perforation. Not the older “eco sheets” box from the brand site.</p>
<img src="sheet.jpg" alt="Product reference sheet: real box front, how it opens, the plain white sheets">
<details><summary>The 8 listing images</summary><img src="listing.jpg" alt="Eight TikTok Shop listing images"></details></section>
<section><h2>Rooms A · B · C · D</h2><img src="rooms.jpg" alt="Four real room photos: laundry corner, green tile bathroom, blue patterned tile, guest bedroom"><p class=small>Real Pexels/Pixabay photos, no people (rooms/SOURCES.md).</p></section>
<section><h2>Hand sheet (Q1)</h2><div class=two><figure style=margin:0><img src="hand_nob.jpg" alt="Grace's hands without bracelet"><figcaption class=small>Without bracelet (default)</figcaption></figure><figure style=margin:0><img src="hand_b.jpg" alt="Grace's hands with bracelet"><figcaption class=small>With bracelet</figcaption></figure></div></section>
<section><h2>Winners we modeled</h2><img src="winners.jpg" alt="First 3 seconds of four winning videos"><p class=small>Rows: @austinfamilytok 339K, @joy_joyful_creations 290K (both this listing), @thegirltut 104K, @get_whitehack 1.7M.</p></section>
<section><h2>Order and time</h2><ol><li>9 stills at once, storyboard here (your stop 1).</li><li>Test clip S5 + the 2 Seedance clips.</li><li>Other 6 Omni clips, VO, cut, QC, AI finish (your stop 2), then Drive.</li></ol><p class=small>Machine time about 35-40 min plus your two stops.</p></section>
<section><h2>Prompts (18, all linted)</h2>{prompts}</section>
</main>"""
(J / "review/index.html").write_text(page)
