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
ORDER = []   # Flow kits retired 2026-10-27 (Ralph: "Use Kie")
LEN = {"S5": "8 s (the line is 4.7 s; if Flow only offers 4 s, make 4 s and tell me)", "S9": "8 s (the line is 5.2 s; if Flow only offers 4 s, make 4 s and tell me)"}
WORDS = {s["id"]: s["words"] for s in SH}
def card(i):
    imgs = [(f"kit/{i}-1_still.jpg", "still " + i), (f"kit/{i}-2_padlock.jpg", "padlock close-up"), (f"kit/{i}-3_scarf.jpg", "scarf close-up"), (f"kit/{i}-4_sheet.jpg", "product sheet")]
    fig = "".join(f'<figure><img src="{a}" alt="{i} image {n+1}"><figcaption>{n+1} · {b}</figcaption><button class="sv" data-src="{a}">Save</button></figure>' for n, (a, b) in enumerate(imgs))
    first = ' <span class="chip warn">make this one first</span>' if i == "S4" else ""
    return f"""<details class="box"{' open' if i == 'S4' else ''}><summary><b>{i}</b>{first} · &ldquo;{E(WORDS[i])}&rdquo;</summary>
<ol><li>Flow: new project › Video › <b>Gemini Omni Flash</b> › 9:16 › {LEN.get(i, '4 s')}</li><li>Add these 4 images in this order (tap Save under each one). Number 1 goes in the start frame if Flow asks.</li></ol>
<div class="kitimgs">{fig}</div>
<p style="margin:0">3. Paste this prompt: <button class="cp" data-p="p{i}">Copy prompt</button> <button class="svp" data-p="p{i}">Save prompt</button></p>
<pre id="p{i}" class="kitp">{E(Path('prompts/flow_'+i+'.txt').read_text().strip())}</pre>
<p class="note">4. Download at 1080 and send it back in the chat.</p></details>"""
KITS = "".join(card(i) for i in ORDER)
SCRIPT = """<p class="note dlnote" id="dlnote" hidden>Saving isn't available in this view: long-press an image to save it, and press and hold the prompt text to copy it.</p>
<script>
(async()=>{const note=document.getElementById('dlnote');
let dl=null;try{dl=await claude.use("downloads")}catch(e){}
if(!dl){document.querySelectorAll('.sv,.svp').forEach(b=>b.hidden=true);note.hidden=false;}
document.querySelectorAll('.sv').forEach(b=>b.addEventListener('click',async()=>{if(!dl)return;const src=b.dataset.src;b.textContent='...';
 try{const blob=await (await fetch(src)).blob();await dl.save({filename:src.split('/').pop(),data:blob});b.textContent='Saved';}
 catch(e){b.textContent=(e&&e.code==='declined')?'Save':'Try again';}}));
document.querySelectorAll('.svp').forEach(b=>b.addEventListener('click',async()=>{if(!dl)return;const id=b.dataset.p;
 try{await dl.save({filename:id.slice(1)+'-prompt.txt',data:document.getElementById(id).innerText});b.textContent='Saved';}
 catch(e){b.textContent='Save prompt';}}));
document.querySelectorAll('.cp').forEach(b=>b.addEventListener('click',async()=>{const el=document.getElementById(b.dataset.p);
 try{await navigator.clipboard.writeText(el.innerText);b.textContent='Copied';}
 catch(e){const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selected: tap Copy';}}));
})();
</script>"""
NOTES2 = [l.strip("| ").split(" | ") for l in Path("qc/stills_r2.md").read_text().splitlines() if l.startswith("| S")]
STORY2 = "".join(f'<figure><img src="st/{i}_r2.jpg" alt="{i} still"><figcaption><b class="{v.lower()}">{i} {v}</b> {E(n)}</figcaption></figure>' for i, v, n in NOTES2)
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
.tot td{{font-weight:700;border-bottom:none}} .sb{{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}} .pass{{color:var(--gold)}} .kitimgs{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}} .kitimgs button,.cp,.svp{{font:600 .8rem var(--body);padding:6px 10px;border-radius:6px;border:1px solid var(--wine);background:var(--card);color:var(--wine);cursor:pointer}} details.box summary{{cursor:pointer;font:600 1rem var(--body)}} .redo{{color:var(--wine)}} .note{{margin:0;color:var(--muted)}} .facts b{{color:var(--gold)}}
</style>
<div class="wrap">
<header><h1>Mini Bag Charm, burgundy</h1><p class="sub">Grace · cut v11 ready (S4 + S7 remade with no AI charm) · $9.24 spent of $9.55 OK'd</p></header>
<section class="ask"><h2>Cut v11 · S4 + S7 remade with no AI charm · 26.9 s</h2><video src="cut_v11.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li><b>Why it kept drifting:</b> the AI's own charm hardware (its clasp, its handles) kept showing through near the ring and the bag rim, and no patch could fully hide it.</li>
<li><b>Fix (the new standing rule):</b> S4 and S7 were made again with NO charm in the clip: S4 = Grace's hand holding just the plain gold ring, S7 = the empty bag with the slow push-in. The real charm is the only one in frame: in S4 it hangs from the clip's own ring, in S7 from the gold ring, tracked to the bag. Nothing is patched over the bag.</li>
<li>Every frame of both shots looked at in the final cut (strips below). Colour = Grace's burgundy (HUE_OK), sharpness matched (SHARP_OK), CUT_QC_OK.</li>
<li>Cost: 2 Seedance clips $0.32 (no redo needed). Job total $9.24.</li></ul>
<figure><img src="v11_S4.jpg" alt="S4 every frame"><figcaption>S4 (0:07-0:09), 15 frames a second</figcaption></figure>
<figure><img src="v11_S7.jpg" alt="S7 every 0.1 s"><figcaption>S7 (0:15-0:18), every 0.1 s</figcaption></figure></section>
<section class="box"><h2>Cut v10 (replaced by v11: drift still showed at 7-8 s and 16-18 s)</h2><video src="cut_v10.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li><b>S4 (0:07-0:09, your arrow):</b> the patch I used to hide the AI's charm changed the bag's shape and left blotches beside the charm (the AI redraws the bag's sag). Now only the AI charm, its scarf and its shadow are hidden; the bag's edge and the sofa stay as filmed. The charm now hangs from the bottom of the gold ring (it was covering half the ring).</li>
<li><b>S7 (0:17, circled):</b> checked every frame: the charm stays on the clip's own clasp, rim and curtain clean.</li>
<li><b>S8 (0:18-0:21):</b> the AI drew its charm bigger than the real one, so its dark handles and white tissue peeked out between the fingers and our charm, and part of the AI's scarf stayed as a pale ghost. Those are hidden now (the cuff and fingers stay as filmed), and the real charm's handle loop sits right in the pinch.</li>
<li>This time I looked at every frame of S4, S7 and S8 in the final cut (strips below), not samples. Colour still Grace's burgundy (HUE_OK), sharpness matched (SHARP_OK), CUT_QC_OK. $0 this round.</li></ul>
<figure><img src="v10_S4.jpg" alt="S4 every frame"><figcaption>S4, 15 frames a second</figcaption></figure>
<figure><img src="v10_S7.jpg" alt="S7 every 0.1 s"><figcaption>S7, every 0.1 s</figcaption></figure>
<figure><img src="v10_S8.jpg" alt="S8 every 0.1 s"><figcaption>S8, every 0.1 s</figcaption></figure></section>
<section class="box"><h2>Cut v9 (replaced by v10: Ralph saw misalignment in S4, S7, S8)</h2><video src="cut_v9.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li><b>0:07-0:09 (S4, "the bag does something weird"):</b> in this clip the AI hand lets go and the key ring drops onto a chain from the bag's rim. v8 kept the charm pinned under where the ring had been, so it jumped up and a stray chain was drawn toward the hand. Now the charm hangs from the AI's own ring and chain: held, let go, it drops and hangs. No drawn chain.</li>
<li><b>0:17 (S7, circled):</b> the brown lump at the handle and the faint blocks beside it came from my background patch and drawn ring. Now the charm hangs from the clip's own gold clasp, and only the AI charm's own colours are painted out from the live frame: clean handle, rim and curtain.</li>
<li><b>0:18-0:21 (S8, stocking):</b> new clip (Seedance, $0.16 of the $0.49 you OK'd): Grace's hand lowers the charm into the stocking, the cuff swallows its bottom, the hand lets go. Real charm laid on frame by frame, fingers in front of its handles, at its true size.</li>
<li>Checks: burgundy hue 352-354 vs 353 in her photo; sharpness vs the bag 0.86-1.02; CUT_QC_OK; drift strips looked at (S4, S7, S8 below).</li></ul>
<figure><img src="v9_strip_S8.jpg" alt="S8 every 0.2 s"><figcaption>S8 in the cut, every 0.2 s</figcaption></figure>
<figure><img src="v9_strip_S4.jpg" alt="S4 every 0.2 s"><figcaption>S4 in the cut, every 0.2 s</figcaption></figure></section>
<section class="box"><h2>Cut v8 (replaced by v9: drift at 0:07-0:09 and 0:17, stocking motion added)</h2><video src="cut_v8.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li><b>Grace's note: "she can tell it was pasted".</b> The colour was already her burgundy (same listing photo); what gave it away was a sharp studio photo on soft video, studio light, no shadow and no movement.</li>
<li><b>Colour:</b> locked to her listing photo's burgundy in all four shots (hue 352-354 vs 353 in the photo, checked on every 6th frame).</li>
<li><b>Sharpness:</b> softened to match the footage around it (edge steepness vs the handbag 0.95-1.07; v7 was 1.22).</li>
<li><b>Light:</b> the room's light across it (top lit, bottom in shade), the room's white balance, follows each frame's light changes; the tissue no longer glows.</li>
<li><b>Shadow + depth:</b> a contact shadow on the handbag, a slight turn instead of flat front-on, the footage's grain, a little of the room's colour on its edge.</li>
<li><b>Movement:</b> S4 swings like a pendulum when the hand moves and lets go; S7/S9 sway slightly.</li>
<li><b>Leftovers fixed:</b> S9 pale smear on the bag's right edge (in v7 too) and S8 pale ghost above the handle + dark sliver at its left edge (in v7 too). QC: CUT_QC_OK, gate OK, drift strips checked. $0.</li></ul>
<figure><img src="v8_compare.jpg" alt="v7 top, v8 bottom, 2x on S4, S7, S9"><figcaption>2x zoom: v7 (top) vs v8 (bottom), S4 · S7 · S9 · S9</figcaption></figure>
<figure><img src="cut_sheet_v8.jpg" alt="Cut v8 frames"><figcaption>12 frames across cut v8</figcaption></figure></section>
<section class="box"><h2>Cut v7 (approved 2026-10-28, replaced by v8: Grace could tell the charm was pasted)</h2><video src="cut_v7.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li><b>S4 (0:08, sofa + hand):</b> the dark patch under the charm is gone. It came from the background I used to cover the AI's own charm: it had the old still's look baked in, so it stayed after the hand left. That background is now taken from the clip itself, so the bag and sofa look the same as the rest of the shot once the hand moves away.</li>
<li>Drift strip checked over the S4 window in the final cut (every 0.2 s, 2x): charm on its ring, no shadow, no patch, no AI leftovers. QC: CUT_QC_OK, gate OK. $0.</li></ul>
<figure><img src="cut_sheet_v7.jpg" alt="Cut v7 frames"><figcaption>12 frames across cut v7</figcaption></figure></section>
<section class="box"><h2>Cut v6 (replaced by v7: Ralph saw the S4 shadow stay after the hand left)</h2><video src="cut_v6.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li><b>S7 (0:16, sofa by the window):</b> the patch behind the charm now stops at the handbag's edge, so the teal curtain beside it no longer smears as the camera moves. Checked on all 20 frames of the shot.</li>
<li>S4 and S9 re-made the same way and checked frame by frame: clean. Everything else as in v5. QC: CUT_QC_OK, gate OK. $0.</li></ul>
<figure><img src="cut_sheet_v6.jpg" alt="Cut v6 frames"><figcaption>12 frames across cut v6</figcaption></figure></section>
<section class="box"><h2>Cut v5 (replaced by v6: Ralph saw drift by the curtain on S7)</h2><video src="cut_v5.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li><b>S4 (0:08, sofa + hand):</b> the charm now hangs from the gold ring the whole time and moves with it as the hand lets go (in v4 it stayed put and floated). The soft patch beside it is gone.</li>
<li><b>S7 (sofa by the window):</b> the dark smudge under and beside the charm is gone; the handbag behind it is clean leather again.</li>
<li><b>S1 (opening, in the hand):</b> the key ring stays a whole circle to the end of the shot (v4 cut a notch into it where the extra key was removed).</li>
<li>Checked frame by frame on S4, S7, S8, S9: the charm stays on its ring, no slide or jump. QC again: CUT_QC_OK, flicker only at the shot cuts, gate OK. $0 (all free fixes).</li></ul>
<figure><img src="cut_sheet_v5.jpg" alt="Cut v5 frames"><figcaption>12 frames across cut v5</figcaption></figure></section>
<section class="box"><h2>Cut v4 (2026-10-27, replaced by v5: Ralph saw drift on S1, S4, S7)</h2><video src="cut_v4.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li><b>Size (Grace: "still way too big"):</b> S4, S7, S8 and S9 show the REAL charm cut from your listing photo at its true size next to the handbag and the stocking.</li>
<li><b>Design (Grace: "it should look like this throughout"):</b> the scarf is knotted on the right handle with its long tail, the padlock is plain with three lines, and nothing else hangs from the ring in every shot. Seedance kept redrawing the tiny charm, so on S4, S7, S8 and S9 the real charm is laid onto each frame (your OK). S1 is an Omni take with an extra key it drew painted out.</li>
<li><b>Stocking (Grace's eye-cream photo):</b> S8 is a real stocking photo with the real charm tucked inside the cuff, much smaller than the opening.</li>
<li>Unchanged from v3: S2, S3, S5b, S6 (close-ups with nothing to judge the size by, or no charm in frame).</li>
<li>QC: CUT_QC_OK (-16.5 LUFS, 1080x1920, every clip at 1.0x), flicker only at the shot cuts, hands clean at 2x, no text, AI finish on.</li>
<li>Spent this round: $3.00 of the $3.01 you OK'd (S9 Omni came back as a giant charm, $0.42 billed). On your OK, v4 replaces v3 in Drive (v3 moves to Older versions).</li></ul>
<figure><img src="cut_sheet_v4.jpg" alt="Cut v4 frames"><figcaption>12 frames across cut v4</figcaption></figure></section>
<section class="box"><h2>Round 4 working notes · the real charm, and why paste-back</h2>
<figure><img src="v4_stills.jpg" alt="The six round-4 stills"><figcaption>S1 · S4 · S5a · S7 · S8 · S9. S4, S7, S8 and S9 use the REAL charm cut from your listing photo, placed at 9.5 x 5.5 cm. S1 and S5a got the scarf fixed: knotted on the right handle, long tail.</figcaption></figure>
<p class="note"><b>What went wrong:</b> Seedance keeps the size but redraws the tiny charm a second or two into each clip. Top row is the first frame, bottom row is later in the same clip: S4 gets a flap and a wide scarf, S8 turns into a flap bag, S9 pushes in too close and puts a mark on the padlock, and S1's padlock gets a mark while a chain dangles.</p>
<figure><img src="v4_drift.jpg" alt="First frame vs later frame for S4, S8, S9, S1"><figcaption>First frame (top) vs later (bottom): S4 · S8 · S9 · S1</figcaption></figure>
<p class="note"><b>The free fix that works:</b> I track the camera move and lay the real charm back onto every frame. S7 and S8 below are done that way: the real charm stays the same through the whole clip. S5a needs no fix: its line runs 1.66 s and the clip's first 1.7 s are clean.</p>
<div class="grid"><figure><video src="S7_v4.mp4" controls playsinline preload="metadata" style="width:100%"></video><figcaption>S7 sofa · real charm laid on each frame</figcaption></figure>
<figure><video src="S8_v4.mp4" controls playsinline preload="metadata" style="width:100%"></video><figcaption>S8 stocking · real charm inside the cuff, like Grace's eye cream</figcaption></figure>
<figure><video src="S5a_v4.mp4" controls playsinline preload="metadata" style="width:100%"></video><figcaption>S5a earbuds · first 1.66 s, as it will be cut</figcaption></figure></div>
<details><summary>The raw takes that drifted (S1, S4, S9)</summary><div class="grid"><figure><video src="S1_v4raw.mp4" controls playsinline preload="metadata" style="width:100%"></video><figcaption>S1</figcaption></figure><figure><video src="S4_v4raw.mp4" controls playsinline preload="metadata" style="width:100%"></video><figcaption>S4</figcaption></figure><figure><video src="S9_v4raw.mp4" controls playsinline preload="metadata" style="width:100%"></video><figcaption>S9</figcaption></figure></div></details>
<ol><li><b>Paste-back OK?</b> Laying the real charm on the moving clip counts as a paste-back, so it needs your OK per shot: S7 and S8 now (made, $0), and S4 and S9 if you pick their redo.</li>
<li><b>S1, S4, S9</b> (recommended, $0.73): new S9 ($0.246) and S4 ($0.164) Seedance takes with a still camera and a still hand, so the same paste-back holds, plus S1 on Omni with the real close-ups ($0.315; a failed Omni try costs nothing). Cheaper option, $0.41: S4 and S9 only, and S1 stays as it is.</li></ol>
<p class="note">Spent this round: $1.61 (6 stills $0.54, 6 clips $1.07). Job $7.36 of $7.37 OK'd. Month $184.16 (no cap in October).</p></section>
<section class="box"><h2>Cut v3 (approved 2026-10-27; Grace: still too big)</h2><video src="cut_v3.mp4" controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:8px;border:1px solid var(--line)"></video>
<ul><li>Your note: S7 (sofa), S8 (stocking) and S9 (tree end shot) were still the v1 size. All three are redone at 9.5 x 5.5 cm. S7 and S9 used the approved S4 shot as a size reference; S7's padlock is plain now (v1 showed a mark).</li>
<li>S8: the charm is small next to the stocking and drops all the way inside.</li>
<li>S6 (close-up of the padlock and scarf) is the only v1 shot left: there is nothing in it to judge size by.</li>
<li>QC: -16.5 LUFS, no black or flash frames, 1080x1920, every clip at 1.0x, no text, AI finish on.</li>
<li>Spent $5.76 of the $5.76 you OK'd. On your OK, v3 replaces v2 in Drive (v2 moves to Older versions).</li></ul>
<figure><img src="cut_sheet_v3.jpg" alt="Cut v3 frames"><figcaption>12 frames across cut v3</figcaption></figure></section>
<section class="box"><h2>Cut v2 (approved 2026-10-27, replaced by v3)</h2><p class="note">S7, S8, S9 still at the v1 size.</p></section>
<section class="box"><h2>Cut v1 (approved 2026-10-27, replaced by v2)</h2><p class="note">Charm drawn too big; earbuds and lip balm together in one shot.</p></section>
<section class="box"><h2>S3 clip · Seedance · 4 s</h2><video src="S3.mp4" controls playsinline preload="metadata" style="width:100%;max-width:360px;border-radius:8px;border:1px solid var(--line)"></video><p class="note">Clip check OK (0.96), no flicker (max jump 1.46). Flaw: the bracelet turns into a watch with a face (question 2).</p></section>
<section class="box"><h2>Stills, round 2 (3 redos, $0.27)</h2><div class="grid sb">{STORY2}</div></section>
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
