"""Review page for Ralph (newest on top). python3 build_review.py -> review/index.html (images in review/img/)."""
import json, html, re
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); SH = D["videos"][0]["shots"]; E = html.escape
book = Path("BOOK.md").read_text()
script = re.search(r"^> (.+)$", book, re.M).group(1)
qs = re.search(r"## 7\. Questions.*?\n(.*?)\n\n## 8", book, re.S).group(1).strip().splitlines()
shots = "".join(f"""<article class="shot"><div class="sh"><span class="num">{s['id']}</span>
<span class="chip {'free' if not s['hand'] else ''}">{'HAND' if s['hand'] else 'HAND-FREE'}</span>{'<span class="chip pk">POCKET</span>' if s['pocket'] else ''}</div>
<p class="say">&ldquo;{E(s['words'])}&rdquo;</p><p class="see">{E(s['still'])}</p><p class="mv"><b>Motion:</b> {E(s['motion'])}</p>
<details><summary>Full still prompt</summary><pre>{E(Path('prompts/still_'+s['id']+'.txt').read_text())}</pre></details>
<details><summary>Full clip prompt</summary><pre>{E(Path('prompts/'+s['id']+'.txt').read_text())}</pre></details></article>""" for s in SH)
cost = """<table><tr><td>Stills, Gemini 3 Pro Image on Kie</td><td>11 x $0.09</td><td>$0.99</td></tr>
<tr><td>One likely redo (about 3 stills)</td><td>3 x $0.09</td><td>$0.27</td></tr>
<tr><td>Clips, Omni 1.1 Flash in your Flow app first</td><td>11 x 12 credits</td><td>$0.00</td></tr>
<tr><td>Same 11 on Kie only if Flow fails (asked first)</td><td>11 x $0.315</td><td>$3.465</td></tr>
<tr class="tot"><td>TOTAL (incl. the Kie fallback)</td><td></td><td>$4.725</td></tr></table>
<p class="note">Expected with Flow: <b>$1.26</b>. ElevenLabs about 560 characters (Grace cloned). Month so far $169.56, no cap in October.</p>"""
NOTES = [("S1","PASS","Walk-in view, pumpkin pillow, stripes right."),("S2","PASS","Hand grips the comforter edge, pocket shows."),
 ("S3","REDO","Hand rests flat on the phone (no grip); blue band on the wrist instead of a ring."),("S4","PASS","Phone in the pocket, hand grips the top. Riskiest clip, goes first."),
 ("S5","PASS","Whole set, flat sheet fold."),("S6","PASS","Shams, pillowcases, pumpkin."),("S7","REDO","Blue band on the wrist (it is a ring in Grace's sheet)."),
 ("S8","REDO","Hand lies flat instead of gripping the edge to fold it; blue band on the wrist."),("S9","PASS","Lying-in-bed POV, covers over the legs."),
 ("S10","REDO","Shows a whole bed with WHITE pillows that aren't in the set; should be a close-up of the edge."),("S11","REDO","A wristwatch with a face (Grace wears a link bracelet, no watch).")]
STORY = "".join(f'<figure><img src="st/{i}_r1.jpg" alt="{i} still"><figcaption><b class="{v.lower()}">{i} {v}</b> {E(n)}</figcaption></figure>' for i,v,n in NOTES)
page = f"""<title>Monbix Comforter Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,600&family=Karla:wght@400;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: one column; decision box first, then product truth, script, shot cards with full prompts, cost */
:root{{--bg:#eef0ea;--card:#fbfcf8;--fg:#1f2620;--muted:#5d6a5f;--line:#d5dbd0;--accent:#4f6b3a;--rust:#b4542b;--chip:#e3e9dc;
--display:"Newsreader",Georgia,serif;--body:"Karla",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151a16;--card:#1d241e;--fg:#e9eee6;--muted:#a3b0a4;--line:#2f3a31;--accent:#a9c98f;--rust:#e88a5c;--chip:#2a352b;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#151a16;--card:#1d241e;--fg:#e9eee6;--muted:#a3b0a4;--line:#2f3a31;--accent:#a9c98f;--rust:#e88a5c;--chip:#2a352b;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}}
.wrap{{max-width:880px;margin:0 auto;padding-block:24px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:22px}}
h1{{font:600 2.2rem/1.1 var(--display);margin:0;text-wrap:balance}} h2{{font:600 1.35rem/1.2 var(--display);margin:0;text-wrap:balance}}
.sub{{color:var(--muted);margin:4px 0 0}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px 18px;display:grid;gap:10px;min-width:0}}
.ask{{border:2px solid var(--rust);background:var(--card);padding:14px 18px;border-radius:8px;display:grid;gap:8px}}
.ask h2{{color:var(--rust)}} ol,ul{{margin:0;padding-left:20px;display:grid;gap:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
figure{{margin:0;display:grid;gap:6px;min-width:0}} figure img{{width:100%;max-width:100%;border-radius:6px;border:1px solid var(--line)}}
figcaption{{font:500 .75rem var(--mono);color:var(--muted)}}
blockquote{{margin:0;font:600 1.15rem/1.5 var(--display);border-left:3px solid var(--accent);padding-left:14px}}
.shot{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;display:grid;gap:6px;min-width:0}}
.sh{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}} .num{{font:500 .9rem var(--mono);color:var(--accent)}}
.chip{{font:500 .7rem var(--mono);letter-spacing:.06em;background:var(--chip);padding:2px 8px;border-radius:99px}}
.chip.free{{outline:1px solid var(--accent)}} .chip.pk{{color:var(--rust)}}
.say{{font-weight:600;margin:0}} .see,.mv{{margin:0;color:var(--muted);font-size:.93rem}}
details summary{{cursor:pointer;font:500 .8rem var(--mono);color:var(--accent)}} details summary:focus-visible{{outline:2px solid var(--accent)}}
pre{{white-space:pre-wrap;font:400 .78rem/1.5 var(--mono);background:var(--bg);padding:10px;border-radius:6px;overflow-x:auto;margin:6px 0 0}}
table{{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}} td{{padding:6px 4px;border-bottom:1px solid var(--line)}} td:last-child{{text-align:right}}
.tot td{{font-weight:600;border-bottom:none}} .note{{margin:0;color:var(--muted)}}
.facts li b{{color:var(--rust)}} .pass{{color:var(--accent)}} .redo{{color:var(--rust)}} .sb{{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}}
</style>
<div class="wrap">
<header><h1>Monbix Remy comforter set, POV</h1><p class="sub">Grace · Autumn Leaf, queen · cut v1 ready for review · $4.86 spent</p></header>
<section class="box"><h2>Cut v1 (28.6 s, AI finish on)</h2><video src="monbix_v1.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li>QC: levels -16.6 LUFS, echo 150 ms (passes), no black or flash frames, every clip at 1.0x, no text, no pumpkin, hands checked at 2x.</li>
<li>Free fixes: S5 dropped (it drew the pocket on the flat sheet; S6 covers both lines), S2 starts after the white pillows leave the frame, S9 cropped 1.25x so no toes show.</li>
<li><b>Your call:</b> in S8 (18-19 s) a second hand comes in to fold the comforter, and both wrists wear the same bracelets. Keep it, or redo that one clip for $0.315.</li>
<li>Spent $4.86 of the $5.17 you OK'd. Month $174.42 (no cap in October).</li></ul></section>
<section class="box"><h2>Storyboard, round 1 (11 stills, $0.99)</h2><div class="grid sb">{STORY}</div></section>
<section class="ask" hidden><h2>Your OK on this plan + 6 answers</h2><ol>{''.join('<li>'+E(q.split('. ',1)[1] if '. ' in q else q)+'</li>' for q in qs)}</ol>
<p class="note">Reply with the numbers, e.g. "1 yes 2 yes 3 with 4 yes 5 none 6 Flow". Total if everything ran on Kie: <b>$4.725</b>; with Flow: <b>$1.26</b>.</p></section>
<section class="box"><h2>The real product (what every prompt copies)</h2>
<ul class="facts"><li><b>Comforter</b>: solid terracotta on both sides, soft quilting, no stripes</li><li><b>2 shams</b>: solid terracotta. <b>2 pillowcases, flat + fitted sheet</b>: thin terracotta-and-white stripes</li><li><b>Pockets</b>: one sewn striped pocket on EACH long side of the fitted sheet (Monbix's own video: "pockets on BOTH sides of the fitted sheet")</li><li>No logo anywhere. The throw and small cushion in the listing photo are staging, never shown.</li></ul>
<figure><img src="img/sheet.jpg" alt="Product reference sheet"><figcaption>Reference sheet, real pixels only. Stripe = Grace's own sheet from the nose ad photo (terracotta bands a little wider than the white)</figcaption></figure>
<div class="grid"><figure><img src="img/grace_sheet.jpg" alt="Grace's sheet"><figcaption>Grace's own sheet (Mute box photo): the stripe every prompt copies</figcaption></figure>
<figure><img src="img/pocket_frames.jpg" alt="Real pocket frames"><figcaption>The real pocket (@tori_didit, 13.4M)</figcaption></figure>
<figure><img src="img/room.jpg" alt="Room"><figcaption>The bedroom: real Pexels photo, olive wall</figcaption></figure></div></section>
<section class="box"><h2>Script (Grace cloned voice)</h2><blockquote>{E(script)}</blockquote>
<p class="note">Hook H102 in her wording. Grade 4.1. Humanizer done. Line sources and the gate result are in BOOK.md. The colour name is in because the top comment on both examples is "What color is this?". "Breathable/cooling" left out: the creator said it, the listing doesn't.</p></section>
<section class="box"><h2>Hand (question 3)</h2><div class="grid"><figure><img src="img/hand_with.jpg" alt="With bracelet"><figcaption>WITH bracelet (default in the prompts)</figcaption></figure><figure><img src="img/hand_without.jpg" alt="Without bracelet"><figcaption>WITHOUT bracelet</figcaption></figure></div></section>
<section style="display:grid;gap:12px"><h2>Shots (6 hand, 5 hand-free)</h2>{shots}</section>
<section class="box"><h2>Cost</h2>{cost}</section>
<section class="box"><h2>What the examples do</h2><div class="grid"><figure><img src="img/ref_niki.jpg" alt="nikifulmer"><figcaption>@nikifulmer 5.3M: pure POV, text + song</figcaption></figure><figure><img src="img/ref_tori.jpg" alt="tori_didit"><figcaption>@tori_didit 13.4M: talking bed tour</figcaption></figure></div></section>
</div>"""
Path("review/index.html").write_text(page); print("ok", len(page))
