"""Writes BOOK.md (the one plan message) for Vans V13-V17 from shots.json + labels.json. python3 tools/book.py [--sent "<link, date>"]"""
import json, sys
from pathlib import Path

J = Path(__file__).resolve().parent.parent
S = json.loads((J / "shots.json").read_text())
L = json.loads((J / "tools/labels.json").read_text())
sent = sys.argv[sys.argv.index("--sent") + 1] if "--sent" in sys.argv else "____ (review page link + date)"
V = {"V13": ("Cafe", "green cafe (wood floor, green velvet armchairs) + stone cafe sidewalk", "light-wash straight jeans, cream knit cuff", "black satin slip midi skirt", "gold chain anklet (right)"),
     "V14": ("Bedroom", "sage-green bedroom (wood floor, white rug) + sunny park path", "grey joggers, oatmeal sweatshirt cuff", "cream pleated satin midi skirt", "gold beaded anklet (left)"),
     "V15": ("Living room", "teal velvet sofa living room (cream rug, coffee table) + cobblestone alley", "brown corduroy straight pants, camel sweater cuff", "red and black plaid mini skirt", "gold chain anklet (right)"),
     "V16": ("Loft", "colourful loft (red brick wall, patchwork rug, white sofa) + rainbow painted steps", "olive cargo pants, black ribbed cuff", "white wide-leg linen trousers", "gold chain anklet (left)"),
     "V17": ("Kitchen", "bright kitchen (mint table, geometric rug, pink flowers) + wooden boardwalk", "cream wide-leg sweatpants, light-blue denim cuff", "pastel floral midi dress", "gold beaded anklet (right)")}

n = len(S); st, cl = 0.09, 0.315
redo = 5 * (st + cl)
total = round(n * st + n * cl + redo, 2)
rows = []
for v, (name, place, main, dress, ank) in V.items():
    hand = sum(1 for k, s in S.items() if s["video"] == v and s["kind"] == "HAND")
    rows.append(f"\n### {v} {name}: {place}\nEveryday: {main}. Dressy shot: {dress}. {ank}. {hand} HAND / {11 - hand} HAND-FREE.\n")
    rows.append("| # | Window (s) | Grace says | On screen | HAND? | Logos in frame |\n|---|---|---|---|---|---|")
    for k, s in S.items():
        if s["video"] != v: continue
        logos = ", ".join({"real_vans_tab.jpg": "side tab", "real_heel_label.jpg": "heel label", "real_insole_logo.jpg": "insole"}[x.split("/")[-1]] for x in s["clip_refs"][1:-1])
        rows.append(f"| {k} | {s['window'][0]:.1f}-{s['window'][1]:.1f} | {s['line']} | {L[k]} | {s['kind']} | {logos} |")

ex = S["V14B"]
book = f"""# Production Book: Vans sequin V13-V17, five AI videos on Grace's own VO (Grace), 2026-10-29

Sent to Ralph: {sent}

## 1. Job
- Client: Grace  Product: Vans Premium Authentic low top, sequin checkerboard (same shoe as V1-V12)  Route: hands + feet AI, product lock (`.claude/skills/ugc-product-ad/references/product-lock.md`), Omni on Kie or your Flow app
- Job folder: `ugc/vans-vo5/`  Length: 27.5 s each (= Grace's audio)  Shots: 11 per video, 55 in all
- Ask (Ralph 2026-10-29): "Grace wants 5 more ai videos of this. Use the audio from the link as the VO and match the visuals. Different visuals for each video." Link: https://www.tiktok.com/t/ZPLDRH7Rk = Grace's own post (@shewiththeglow, 2026-10-21, 535 views, 21 cuts in 27.6 s).

## 2. Gate result (`python3 grace/gate.py ugc/vans-vo5`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (ref + #sequinvans tag + video x3) | proof/coach_research.md | OK: top #sequinvans 115.7K / 104.6K / 55.9K open on the shoe in frame 0 |
| Daily viral board | research/coach/viral-2026-10-29.json | OK, today: sequin Vans rising (@jillgemma sequin slip-on 3,384 views/day) |
| Product facts (source) | research/product_facts.md + product_truth.json | OK (Vans' own photos) |
| Hooks modeled on named winners | research/hooks.md | Spoken hook = Grace's own line; 3 text options per video for the HofR versions |
| Humanizer | proof/humanizer.md | OK (VO is her recording; 1 caption reworded) |
| Readability (grade) | proof/readability_vo.txt | 5.7 |
| Banned-phrase check | gate.py | OK |

## 3. Script (Grace's own recording, word for word, on your say)
Who told Vans to come out with these sparkly low tops? Because whoever made that decision deserves a raise. These are the Premium Authentic, and they really took the classic Vans look and gave it a major upgrade. The sequins add just the right amount of shine without being over the top, so you can dress it up or keep it casual. And they're actually so comfortable, so you're getting the style and the comfort. These are new, but I wouldn't wait too long to grab them, because when the shiny girlies find these, they're going to sell them out fast. Tap that orange cart and get your size before they're gone.
Audio: her track as posted, untouched. I separated it to check: there is no music under her voice (the music stem measured -68.6 dB, silence), so nothing to remove. Same voice on all five; it is also logged as a free clone sample (round 5).
Captions: scripts.md (one each). No on-screen text in Grace's versions.

## 4. Shot list (every shot shows the shoe; one shoe or one pair only; the shoe never turns in a hand)
Same 11 word windows in every video so each line gets its picture: hook / raise / Premium Authentic + classic look / upgrade / shine / dress up / casual / comfortable / grab them / sell out fast / orange cart. What changes per video: place, outfit, every shot idea, framing, direction and grade. Nothing reused from V1-V12.
Hand (all five): Grace's hand ref as on V11/V12 (long soft pink French tips, silver ring stack, gold trillion ring, blue thumb band, flat gold link bracelet + pearl leaf chain). Skin: Grace's skin ref. Feet: always the correct shoe on each foot, toes pointing the same way.
Places: real Pexels/Pixabay photos, 2 per video (rooms/SOURCES.md). HAND-FREE is more than half here because feet are where shoes live; each video still has 3-4 hand shots.
Real product (Vans' own photos, product_truth.json): only the black squares are sequined, off-white squares plain canvas, black collar binding with white stitching, black tongue, tan lining, black laces, 4 black eyelets, black woven VANS side tab, vertical black heel stripe, off-white sidewall, white OFF THE WALL heel label, red insole with a white VANS box, gum waffle sole. New vs V12 prompts: the black tongue and black heel stripe are now named.
{chr(10).join(rows)}

## 5. Order of work and time (machine ~85 min + your 3 stops)
1. All 55 stills at once (~6 min) -> storyboard page, 5 rows of 11 (stop 1: you check looks and outfits).
2. The riskiest clip first, V14B (her hand tightening the lace bow on a worn shoe) (stop 2: one clip, ~3 min).
3. The other 54 clips at once (~15 min), each checked against its still (clip_check.py) and at 2x.
4. Five cuts on Grace's audio at once (~10 min), QC on every cut (2x edges, first second, shoe count, no turn, logos vs close-ups, REMOVED.md, verify_fix), coach compare vs her post, AI finish (stop 3: review page with all five).
Edit in Grace's own style (grace/winners/STYLE_pritech.md, in force since 2026-10-28; free): every video opens on the shoe moving in her hand at frame 0; cuts land on the first word of each phrase; the last line closes on a fast run (0.3-0.6 s each) of that video's own hand shots instead of one held ending; no still-life ending.
5. Drive "Vans sequin (Grace)" as CURRENT - Vans V13..V17 + captions.
Free fixes first: trim to the clean window, crop; a redo only on your OK with its cost.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | {n} x $0.09 | {n*st:.2f} |
| Clips, Omni 1.1 Flash 4 s on Kie | {n} x $0.315 | {n*cl:.2f} |
| ...or the same clips as free takes in your Flow app (12 credits each, {n*12} credits) | {n} x $0 | 0.00 |
| One likely redo per video (one still + one clip), each asked first | 5 x $0.405 | {redo:.2f} |
Expected: ${n*st+n*cl:.2f} all on Kie, ${n*st:.2f} with Flow clips. ElevenLabs: 0 chars (Grace's own voice). HofR versions: $0 (re-cut).
Month so far (`python3 grace/spend.py`): $201.62 in October (no cap this month). If this runs past Oct 31 it counts toward November's $100 cap. Kie balance $1.45 (auto-refills).

TOTAL: ${total:.2f}

**Approve?**

## 7. Questions
1. Clips: all 55 on Kie ($17.33, ~15 min) or free takes in your Flow app (660 of your 1,050 monthly credits, about 55 takes on your phone)? Flow first is the standing rule; at 55 clips I'd suggest Kie for speed, or Flow for some videos and Kie for the rest.
2. Stills on Kie ($4.95) or your Gemini app ($0, 55 images by hand)?
3. The five looks (places + outfits above): OK, or swap any?
4. Grace's hand and anklets as on V12: OK?
5. House of Rameau: one version of each at $0 (reframed + regraded, a hook text from research/hooks.md, no captions), posted only on your OK per video. Make them?
6. Grace's style also likes ~1.5 s middle shots; this plan's are ~2.5 s (11 per video). Keep 11 (this TOTAL), or 16 per video (+25 stills and clips, +$10.13, cap $34.43)?

## 8. Prompts (final, prompt-master loaded this session; all 55 still + 55 clip prompts in shots.json, linted PROMPT_LINT_OK)
Still refs, numbered in each prompt: 1 product sheet (real photos), 2 sequin close-up, then a real close-up of each logo that shot shows (side tab / heel label / insole), her skin ref (feet shots), her hand ref (hand shots), last the place photo; 8 at most. Clip refs: 1 the approved still ("Recreate image 1 exactly as the first frame"), then each logo close-up, then the sheet. Every prompt: framing and toe direction first, which shoe of the pair faces the lens, who wears/holds what, one grip and never turns, print letter for letter and colour for colour, no sparkle words, no text.
Example, V14B still ({len(ex['still_refs'])} refs): {ex['still']}
Example, V14B clip: {ex['clip']}
"""
(J / "BOOK.md").write_text(book)
print("BOOK written, TOTAL", total)
