# Production Book: PRITECH Heated Face Scrubber, black (Grace), 2026-10-23

## 1. Job
- Client / own content: Grace  Product: PRITECH heatable vibrating face scrubber, BLACK (BCM-1485)  Route: hands-only AI + product lock, no full face (`.claude/skills/ugc-product-ad/references/product-lock.md`)
- Job folder: `ugc/pritech-cleansing-brush/`  Target length: ~27 s (89 words; the storyboard's "15 seconds" can't hold this script)  Shots: 9 (6 HAND / 3 HAND-FREE)

## 2. Gate result (`python3 grace/gate.py ugc/pritech-cleansing-brush`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | research/playbook.md | OK, 3 flags below (not edited) |
| Coach research (tag/shop/discover + video x3) | research/coach.md, shop/, tag/, videos/ (4 winners: 3 are this PRITECH brush) | OK |
| Daily viral board | research/viral/viral-2026-10-23.json | OK |
| Product facts (source) | research/product_facts.md | OK, every script claim backed |
| Hooks modeled on named winners | research/hooks.md | Grace's own hook; same call-out as @ttspaulking 110K PRITECH video |
| Humanizer | research/humanizer.md, captions.md | OK, no changes |
| Readability (grade) | research/readability_v1.txt | 7.3, override recorded: Ralph 2026-10-23 "Use the script in the storyboard. Word for word" |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized)
Grace's storyboard script, word for word:
> If you're not washing your face with a cleansing brush, what are you doing? Your hands leave makeup and oil behind, and using a dirty face towel can transfer bacteria right back onto your skin. This one has soft silicone bristles, five vibration settings, and a warming feature that heats up to 104°F for that extra little spa feel. And for something you do every single day, you might as well do it right. Go grab yours from the orange cart before you forget!

Voiced "104°F" = "one hundred and four degrees Fahrenheit". Flags (kept as written): no sell-side confession line; the CTA doesn't push more units; close is "Go grab yours from the orange cart" not "It's in the orange cart." Every claim checks out: soft silicone (box), 5 vibration levels (listing), 40°C = 104°F heat (listing). The heat is on the SILVER METAL END, not the bristles, so S6/S7 show the metal end (the storyboard's glowing bristles would be a false visual). Source of each line: research/line_sources.md.

## 4. Shot list
| # | VO words | On screen | HAND? | Face? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | "If you're not washing your face with a cleansing brush, what are you doing?" | Close side view of Grace's foamy cheek and jaw, her hand moves the black brush in small circles. Product from frame 0 (like the 490K winner) | HAND | cheek + jaw only, eyes and mouth out of frame | Omni 4 s | A sage tile |
| S2 | "Your hands leave makeup and oil behind," | Two hands under the running tap; beige foundation and black mascara smudges stay on the fingertips | HAND | no | Seedance 4 s | B pink tile |
| S3 | "and using a dirty face towel can transfer bacteria right back onto your skin." | Hand grips a crumpled grey face towel with beige makeup smears and lifts it off the sink edge | HAND | no | Seedance 4 s | B |
| S4 | "This one has soft silicone bristles," | Macro slow push-in on the black bristle head, the brush standing in its stand, water drops | HAND-FREE | no | Omni 4 s | A |
| S5 | "five vibration settings," | Thumb presses the top ((•)) button; drops on the bristles shiver | HAND | no | Omni 4 s | A |
| S6 | "and a warming feature that heats up to 104°F" | Thumb presses the °C button, camera tilts down to the silver metal end | HAND | no | Omni 4 s + FLOW TRIAL | A |
| S7 | "for that extra little spa feel." | Metal end glides in slow circles on the cheek, rolled towel + candle soft behind | HAND | cheek only, eyes and mouth out | Omni 4 s | A |
| S8 | "And for something you do every single day, you might as well do it right." | Slow dolly along a bright counter by the window: brush in its stand beside a cleanser bottle (no brand) and a plant | HAND-FREE | no | Omni 4 s | C window bath |
| S9 | "Go grab yours from the orange cart before you forget!" | End shot: one brush in its stand, slow push-in, grey PRITECH on the stand readable | HAND-FREE | no | Omni 4 s | C |

Outfit: white waffle robe at the shoulder edge, beige towel headband just at the top of frame (S1/S7).
Setting: real Pexels rooms (rooms/SOURCES.md): A sage tile + wood vanity, B pink tile, C bright window bath. Bright neutral grade, no candles lit dark, no text.
Nails / person details: Grace's hand sheet WITHOUT the bracelet: medium-brown skin, short squared French tips, silver crown ring stack (ring finger), small gold heart-stone ring (middle finger), blue silicone band (thumb), bare wrist. Skin tone from grace/ref. Cheek shots never show eyes or mouth (Ralph: "Don't show full face"), so no lip sync.
Real product confirmed: matte black body + black silicone nubs, 3 front buttons ((•)) / O / °C, silver chrome end, black stand with grey PRITECH (refs/product_sheet.png, Ralph's photo). Size estimate ~15-16 cm, about one hand long (no maker size found: Amazon refuses cloud requests, tested today, 503).

## 5. Order of work
Still storyboard first (review stop) → S6 = riskiest clip (small button icons + thumb + metal end) as the ONE test clip, made both ways: Kie Omni + a $0 Flow take on Ralph's phone (kit on the review page) → batch after OK → Grace voice (echo gate ≤150 ms) → cut, QC (2x edges, first second, REMOVED.md, verify_fix), compare vs the 490K winner → AI finish → review page.
Free fixes planned: crop/retime before any reroll; Omni edit turn ($0.84) only if asked.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 9 x $0.09 | 0.81 |
| Product clips, Omni 1.1 Flash on Kie, 4 s | 7 x $0.315 | 2.205 |
| No-product clips, Seedance 2.0 Mini, 4 s | 2 x $0.164 | 0.328 |
| One likely redo (an Omni clip), asked before it runs | 1 x $0.315 | 0.315 |
| S6 Flow trial take | Ralph's Flow credits | 0.00 |
Total Kie: $3.343 + one redo $0.315. ElevenLabs: ~330 chars (Grace cloned). $0 option: Ralph makes the 9 stills in his Gemini app from my prompts → total $2.85.
Month so far (`python3 grace/spend.py`): $154.23 (no cap in October).

TOTAL: $3.66

## 7. Ralph's answers (2026-10-23: "1. Without 2.yes like hand sheet 3. Kie 4. No")
1. Hand sheet WITHOUT the bracelet (grace/ref/hand-sheets/without_bracelet.jpg).
2. Nails as on the hand sheet: short squared French tips (pale pink, white tips).
3. Stills on Kie ($0.81, in the TOTAL).
4. No on-screen text.
Size: the ~15-16 cm estimate stands (not answered; it is the only figure found).

## 8. Prompts
Still prompts: shots.json `still` (Gemini 3 Pro Image; refs = refs/product_sheet.png, refs/closeup_head.png, refs/closeup_buttons.png, refs/closeup_stand_logo.png, the room photo, Grace's hand sheet). Clip prompts: shots.json `clip` (Omni reference mode: image 1 = approved still, 2..n = real close-ups, last = sheet; Seedance for S2/S3 with "no brush, no product appears"). All written with prompt-master (Ralph's stack).
