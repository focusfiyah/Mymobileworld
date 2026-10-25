# Production Book: Vans sequin V12, recreation of @sophmademebuyit (Grace), 2026-10-24

## 1. Job
- Client: Grace  Product: Vans Premium Authentic low top, sequin checkerboard (same shoe as V1-V11)  Route: hands-only AI + product lock, Flow first (`.claude/skills/ugc-product-ad/references/product-lock.md`, `grace/flow/README.md`)
- Job folder: `ugc/vans-sequin-v12/` (refs and research reused from `ugc/vans-sequin-authentic/`)  Target length: 16 s (ref 18 s)  Shots: 6 (3 HAND / 3 HAND-FREE)
- Ref: https://www.tiktok.com/t/ZPLAqjmEX (@sophmademebuyit, 75.7K views, 18 s, music only)

## 2. Gate result (`python3 grace/gate.py ugc/vans-sequin-v12`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read (+ live rules doc) | proof/playbook.md | OK |
| Audience research | research/audience.md (from the V1-V11 job, 2026-10-21, same shoe) | OK |
| Coach research (tag + video x3 + the ref) | proof/coach_research.md, research/coach/ | OK: #sequinvans top 115.7K / 104.6K / 55.9K; 2 of 3 + the ref are music only |
| Daily viral board | research/coach/viral-2026-10-24.json | OK (run today) |
| Product facts (source) | research/product_facts.md | OK (vans.com + TikTok listing) |
| Hooks modeled on named winners | research/hooks.md | H020 / H092 / H097 |
| Humanizer | proof/humanizer.md | OK, caption + 1 text option reworded |
| Readability (grade) | proof/readability_v12.txt | 2.0 |
| Banned-phrase check | gate.py | OK |

## 3. Script
Music only, silent track (Grace adds the TikTok sound when posting), like the ref and V1-V11. No text.
Optional voice line (only if you want one; H020 word for word): "This is the part I wanted to see before I bought it. The black squares are all sequins, and the insole is soft. It's in the orange cart."
Caption: "Every black square on these is sequins 🖤 #ad #vans #sequinvans #vansauthentic"
Source of each line: proof/line_sources.md.

## 4. Shot list
| # | Window (s) | On screen | HAND? | Clip | Logos in frame |
|---|---|---|---|---|---|
| S1 | 0-3.0 | POV: her hand holds one shoe by the heel above her other (worn) foot, red insole + white VANS box up, small tilt | HAND | Omni 4 s | insole, side tab |
| S2 | 3.0-7.0 | POV walking forward on red herringbone brick, both shoes on, bricks travel under her | HAND-FREE | Omni 4 s | side tab, heel label |
| S3 | 7.0-9.0 | Hand holds the shoe side-on: black VANS side tab, small lift, no turn | HAND | Omni 4 s | side tab |
| S4 | 9.0-11.0 | Same shoe, heel to the lens: OFF THE WALL label, camera pushes in, no turn | HAND | Omni 4 s | heel label |
| S5 | 11.0-12.5 | Ankle close-up, gold Cuban anklet over the black collar, heel-to-toe rock | HAND-FREE | Omni 4 s | side tab |
| S6 | 12.5-16.0 | Low front view, feet side by side, one foot pivots on its heel and back, green bushes behind | HAND-FREE | Omni 4 s | side tab |

**The fix for last time's problem:** the ref turns the held shoe insole > side > heel in one take. On V1-V11 every turn came back flipped, switched sides or morphed (REMOVED.md). Here that turn is three separate holds (S1, S3, S4) cut together, each with one grip and a small move, so no clip ever turns the shoe. Every clip also gets a close-up of each real logo it shows (the 13-redo side-tab lesson).
Different from V5 (same beats, asphalt + black leggings): new place, outfit, order and framing.
Outfit: sage-green ribbed ankle leggings, cream chunky-knit sleeve, thin gold chain anklet (left) + gold Cuban anklet (right).
Setting: real Pexels photo of a red herringbone brick sidewalk (rooms/SOURCES.md), bright overcast daylight, neutral grade.
Hand: Grace's hand ref as on V11 (long soft pink French tips, silver ring stack, gold trillion ring, blue thumb band, flat gold link bracelet + pearl leaf chain).
Real product (refs/product_sheet.png, Vans' own photos): black squares sequined, off-white squares plain canvas, black leather collar binding with white stitching, black laces, 4 black eyelets, black woven VANS side tab, off-white sidewall, white OFF THE WALL heel label, red insole with white VANS box, gum waffle sole. New close-up made today: refs/real_insole_logo.jpg (cut from Vans' photo).

## 5. Order of work (machine time ~35 min + your stops; your Flow takes ~2-3 min each on your phone)
All 6 stills at once -> still storyboard on the review page (stop 1) -> S1 Flow kit first, the riskiest (held shoe + insole logo) (stop 2: you make it, I QC it) -> Flow kits for S2-S6 together on the review page -> cut + QC (2x edges, first second, shoe count, no turn, every logo vs its close-up, REMOVED.md, verify_fix) + compare vs the ref -> AI finish -> review page (stop 3) -> Drive "Vans sequin (Grace)" as CURRENT - Vans V12.
Free fixes first: trim to the clean window before any redo.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 6 x $0.09 | 0.54 |
| Product clips, Omni 1.1 Flash in your Flow app (12 credits each, 72 credits) | 6 x $0 | 0.00 |
| ...same 6 on Kie only if Flow fails or you can't (asked first) | 6 x $0.315 | 1.89 |
| One likely redo (one still + one clip), asked before it runs | 1 x $0.405 | 0.405 |
Expected spend with Flow: $0.54 ($0 if you make the stills in your Gemini app). The cap includes the Kie fallback so nothing surprises you. ElevenLabs: 0 chars (music only).
Month so far (`python3 grace/spend.py`): $161.71 (no cap in October). Kie balance 275 credits.

TOTAL: $2.835

**Approve?**

## 7. Questions
1. Place + outfit: red herringbone brick sidewalk, sage-green leggings, cream knit sleeve: OK, or another look?
2. Hand: Grace's hand as on V11 (long pink French tips, bracelets, rings): OK?
3. Stills on Kie ($0.54) or your Gemini app ($0, I send the kit)?
4. Sound: silent for Grace's TikTok sound (default), or the optional voice line in Grace's voice (~130 chars)?
5. On-screen text: none (default), or the ref's "sequin low top vans 🔥"?

## 7b. Ralph's answers (2026-10-24: "Ok, yes, Kie, silent, no text and go ahead")
1. Brick sidewalk + sage leggings + cream sleeve OK. 2. Grace's V11 hand: yes. 3. Stills on Kie ($0.54). 4. Silent (no voice). 5. No text.

## 8. Prompts
Every still and clip prompt is in shots.json (`still`, `clip`), written with prompt-master (loaded this session, Ralph's stack). Still refs, numbered and named in each prompt: 1 product sheet, 2 sequin close-up, 3 side tab, 4 heel label, 5 insole logo, 6 skin, 7 Grace's hand, 8 the brick sidewalk photo. Clip refs: 1 the approved still ("Recreate image 1 exactly as the first frame"), then one real close-up per logo in that frame, then the sheet. Every prompt: print letter for letter and colour for colour, one grip, never turns or flips, at most two shoes, feet side by side and parallel, true colours of each small mark in words, no sparkle words, no text, no music, no voice.
