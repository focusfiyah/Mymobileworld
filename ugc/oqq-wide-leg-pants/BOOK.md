# Production Book: OQQ wide-leg pants (black + brown), recreation of @krunch.7 (Grace), 2026-10-25

## 1. Job
- Client: Grace  Product: OQQ Women's High-Waisted Casual Pants (wide straight leg, side hidden pocket), black + dark brown  Route: AI recreation, Grace's body (grace/ref/body), product lock, Flow first (`.claude/skills/ugc-product-ad/references/product-lock.md`, `grace/flow/README.md`)
- Inspo: https://www.tiktok.com/t/ZPLAg5udN/ (@krunch.7, same pants in brown, 555.8K views, 26.8 s, her own voice)
- Job folder: `ugc/oqq-wide-leg-pants/`  Target length: ~28 s  Shots: 8 (5 HAND / 3 HAND-FREE)

## 2. Gate result (`python3 grace/gate.py ugc/oqq-wide-leg-pants`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK (incl. the goth skirt lessons: beat table, money move first, solid fabric, skin match) |
| Inspo beat table (every move, setting, camera) | research/inspo_beats.md | OK: one continuous mirror shot, side and back three-quarter, chest to floor, kitchen with bar stools, no face |
| Coach research (tag + video x3 + the inspo) | proof/coach_research.md | OK: top 3 #widelegpants shop videos 510K / 267K / 165K, all music only, pants moving at frame 0 |
| Daily viral board | research/coach/viral-2026-10-25.json | OK (fashion) |
| Audience (questions + 225 TikTok comments) | research/audience.md | OK: top asks = "what does the back look like" (52 likes) and "regular or longer?" |
| Product facts (source) | research/product_facts.md | OK: listing + its 12 real photos |
| Hooks modeled on named winners | research/hooks.md | OK: H021 (pick), H023, inspo opener |
| Humanizer | proof/humanizer.md | OK |
| Readability | proof/readability_v1.txt | grade 3.6 |
| Banned-phrase check | gate.py | OK |

## 3. Script (Grace's voice, Humanized; blanks = Grace's real facts from you)
S1 Okay, y'all keep asking what the back of these looks like.
S2 If wide-leg pants always stop at your ankles, look at this length.
S3 I'm [height], wearing a [size] in the [Regular or Longer], and they go all the way down over my sneakers.
S4 The waist sits up high, and there's a hidden pocket right here for my phone.
S5 I've got them in black,
S6 and in brown too, because when I find something I like, I get more than one.
S7 Black and brown go with everything for fall, so grab both.
S8 I linked them in the orange cart for you.
Caption: The back view y'all asked for 🖤🤎 black and brown, wide leg, hidden phone pocket #ad #oqq #widelegpants #ootd #fallfashion
Source of each line: proof/line_sources.md (hook H021 + the 52-like comment; ankle pain from the 73-like "tall girl" comments; length question; listing pocket; your "black and brown"; CTA = both colours + fall).
Music-only option: same 8 shots, no voice, silent track for Grace's TikTok sound (the top 3 sellers are music only).

## 4. Shot list (no face in any shot: frame cuts at the chest like the inspo)
| # | Window (s) | Line | On screen | HAND? | Clip |
|---|---|---|---|---|---|
| S1 | 0-3.2 | back question | BLACK, back three-quarter by the island, hand slides down the back of her hip, white OQQ circle mark at centre back | HAND | Omni 4 s |
| S2 | 3.2-6.2 | ankles / length | BLACK, knee-height side view, two steps, hems swing over the sequin Vans | HAND-FREE | Omni 4 s |
| S3 | 6.2-11.0 | height, size, length | BLACK, the inspo shot: right side, chest to floor, hand on a bar stool, hip sway, hem on the floor | HAND | Omni 4 s x2 (window is 4.8 s; second take from the same still, cut on the sway) |
| S4 | 11.0-14.6 | high waist + pocket | BLACK, hip close-up, phone slides into the hidden side pocket, top edge stays out | HAND | Omni 4 s |
| S5 | 14.6-16.6 | "I've got them in black" | BLACK, low back view, walks away, hems over the Vans heels | HAND-FREE | Omni 4 s |
| S6 | 16.6-21.8 | "and in brown too..." | BROWN, back three-quarter, hand on a grey stool, hip rock | HAND | Omni 4 s x2 |
| S7 | 21.8-25.0 | fall, grab both | BROWN, floor-level front, walks toward the camera, Vans toes under the hems | HAND-FREE | Omni 4 s |
| S8 | 25.0-28.0 | orange cart | BROWN, right side, hand smooths the waistband, quarter turn away | HAND | Omni 4 s |
Look A (black): white ribbed cropped square-neck tank, sage-green kitchen island + black stools + oak floor (real Pexels photo, rooms/SOURCES.md).
Look B (brown): cream boxy cropped top with puffed sleeves (the inspo's top), grey-stool kitchen + grey wood floor (real Pexels photo).
Shoes: the sequin checkerboard Vans Authentic from the Vans jobs, both looks. Person: Grace's body photos (slim, her skin tone on every still), long almond nails white/nude.
Real product (refs/product_sheet.png, the listing's own photos): smooth matte solid jersey, wide plain high waistband (no drawstring, buttons or fly), one seam down the front of each leg, fitted hip, wide straight leg to the floor, tonal hidden pocket on the outer hip, small white round OQQ mark at centre back.
The money move (what the inspo sells): the side/back sway with the wide leg falling to the floor. S3 is built on it and goes first.

## 5. Order of work (machine time ~40 min + your stops; each Flow take ~2-3 min on your phone)
1. Stills S3 + S4 only (the money move + the riskiest hand/phone shot) -> QC at 2x (fabric solid, seam, pocket, skin, nails, 5 fingers) -> review page (stop 1).
2. Flow kits for S3 + S4 -> you make the 2 takes -> I QC them (stop 2). If either fails twice I tell you plainly and stop before spending more.
3. Then the other 6 stills at once + VO (if voice) -> storyboard (stop 3) -> 6 Flow kits.
4. Cut + QC (2x edges, first second, fabric, colour, shoe count, REMOVED.md, verify_fix) + compare vs the inspo -> AI finish -> review page (stop 4) -> Drive "OQQ Wide Leg Pants (Grace)".
Free fixes first: trim to the clean window, colour match free, before any redo.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 8 x $0.09 | 0.72 |
| Product clips, Omni 1.1 Flash in your Flow app (12 credits each, 120 credits incl. S3 + S6 x2) | 10 x $0 | 0.00 |
| ...same on Kie only if Flow fails or you can't (asked first) | 10 x $0.315 | 3.15 |
| One likely redo (one still + one clip), asked before it runs | 1 x $0.405 | 0.405 |
Expected spend with Flow: $0.72 ($0 if you make the stills in your Gemini app). ElevenLabs: ~500 chars (voice option only, subscription credits).
Month so far (`python3 grace/spend.py`): $163.00 (no cap in October). Kie balance 2,059 credits.

TOTAL: $4.275

**Approve?**

## 7. Questions
1. Grace's height, size and which length she got (Regular or Longer)? S3 says them out loud (the #1 buyer question).
2. Sound: Grace's voice (script above, ~500 chars) or music only?
3. Shoes: by "Vans crocs shiny ones" you mean the sequin checkerboard Vans Authentic from the Vans videos?
4. Outfits + rooms: black with a white crop tank in the sage kitchen, brown with the cream puff-sleeve crop top in the grey-stool kitchen: OK?
5. Stills on Kie ($0.72) or your Gemini app ($0, I send the kits)?
6. On-screen text: none (default), or the inspo's height/size/length line?

## 8. Prompts (final, written with prompt-master "Ralph's stack", loaded this session)
Every still and clip prompt is in shots.json (`still`, `clip`), built by tools/make_shots.py from shared blocks. Still refs, numbered and named in each prompt: 1 pants product sheet (real photos), 2 real hidden pocket close-up, 3 real centre-back OQQ mark, 4 Vans sheet, 5 real Vans side tab, 6 Grace's body sheet (skin + build), 7 the room photo (+ 8 the Vans heel label on S5). Clip refs: 1 the approved still ("Recreate image 1 exactly as the first frame"), then a real close-up of each mark in that frame, then the sheet. Every prompt: solid matte fabric (never sheer), colour for colour, seam + waistband + full-length wide leg, face never in frame, five fingers and whole wrists, exactly two shoes, no sparkle words, no text, no music, no voice.
