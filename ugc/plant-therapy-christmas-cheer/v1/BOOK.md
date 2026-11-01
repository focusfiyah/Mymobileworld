# Production Book: Plant Therapy Christmas Cheer Essential Oil Blend 3 Set (Grace, 15 s), 2026-10-30

Sent to Ralph: https://claude.ai/artifact/HHa8EJ3Xp8diKpLcUrYB6V (2026-10-30, plan v1)

## 1. Job
- Client: Grace  Product: Plant Therapy Christmas Cheer Essential Oil Blend 3 Set (Christmas Tree, Sugar Plum Fairy, Vanilla Spice, 3 x 10 mL)  Route: hands + hand-free AI over Grace's cloned voice (ugc-product-ad hands-only + product lock)
- Job folder: `ugc/plant-therapy-christmas-cheer/`  Length: ~15 s  Shots: 7 (3 HAND-FREE), no text, no music bed under the voice
- Real product: planttherapy.com listing photos (10, `refs/`) + a real creator video for the cap-off neck. Your attached picture did not come through (empty upload folder).

## 2. Gate result (`python3 grace/gate.py ugc/plant-therapy-christmas-cheer`): GATE OK (9 of 9)
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (shop + tag + video x5 on THIS product) | research/coach_research.md | OK. TikTok Shop listing: 74 sold, 4.4 stars (10). Top same-product videos 10.2K / 9.1K / 4.2K / 4.0K views |
| Daily viral board | research/coach/viral-2026-10-30.json (holiday, 32 shop videos) | OK |
| Product facts | research/product_facts.md + product_truth.json | every line backed (table below) |
| Audience | research/audience.md + audience/voc.md (20 TikTok comments, 1,544 search phrases) | OK: fake-tree owners who miss the real-tree smell |
| Hooks (3, each on a named winner) | research/hooks.md | OK: H062 picked, H055 / H061 as alternates |
| Humanizer | proof/humanizer.md | OK |
| Readability | research/readability_v1.txt | grade 2.5 |
| Banned phrases | gate.py | OK |

## 3. Script (final, humanized)
> You know that moment when the fake tree's up, but the house doesn't smell like Christmas? Ours smelled like the storage box. A few drops of Christmas Tree in my diffuser, and now people ask where the real tree is. Get one to gift too before Christmas. It's in the orange cart.

52 words, ~14.5-15 s (Grace's clone runs ~3.6 words a second). Sources: hook H062 + the same-product winner "Does it smell like Christmas in here?" (@summer_moon_11.11) + search "christmas tree smell for fake trees"; pain = search "artificial christmas tree smells musty"; drops = listing How to use ("3-4 drops per 100 mL"); "real tree" = listing "freshly cut evergreens" + winners "smells like a fresh cut pine"; gift + before Christmas = more units + real season (comment "What a great gift"). Never said: non-toxic, calming/sleep, pure, the price.
On-screen hook text options (only on your yes; default none): "when the tree's up but the house doesn't smell like christmas".

## 4. Shot list
| # | Window (s) | VO words | On screen | HAND? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | 0.0-2.5 | "You know that moment when the fake tree's up," | Push-in past the 3 bottles on a little wood side table toward the tinsel tree + red armchair | HAND-FREE | Omni 1.1 Flash (Flow $0 / Kie $0.315) | A |
| S2 | 2.5-4.4 | "but the house doesn't smell like Christmas?" | Close-up: her fingers bend a plastic branch tip of the fake tree, it springs back | HAND | Seedance 2.0 Mini on Kie ($0.164) | A |
| S3 | 4.4-6.1 | "Ours smelled like the storage box." | Coat closet: both hands lift the lid off a storage tote of folded fake-tree branches | HAND | Seedance 2.0 Mini on Kie ($0.164) | C |
| S4 | 6.1-8.6 | "A few drops of Christmas Tree in my diffuser," | Her hand tips the open Christmas Tree bottle over a white diffuser: two drops fall, ripples | HAND | Omni 1.1 Flash (Flow $0 / Kie $0.315) | A |
| S5 | 8.6-11.0 | "and now people ask where the real tree is." | White mist curls up from the diffuser, tree + armchair behind, slow arc | HAND-FREE | Seedance 2.0 Mini on Kie ($0.164) | A |
| S6 | 11.0-13.1 | "Get one to gift too before Christmas." | Gift table: her hand lowers the closed Christmas Cheer box into a kraft gift bag with red tissue | HAND | Omni 1.1 Flash (Flow $0 / Kie $0.315) | B |
| S7 | 13.1-14.8 | "It's in the orange cart." | END: the box + the 3 bottles in a row on the side table, push-in (one set) | HAND-FREE | Omni 1.1 Flash (Flow $0 / Kie $0.315) | A |

Rooms (real, free): A = red velvet armchair + tinsel fake tree (Pexels 40431132), B = pink gift-wrapping table (Pixabay 3823530), C = coat closet with colourful coats (Pexels 9957166). Bright, colourful, no all-white rooms.
Hand: Grace's sheet WITHOUT the bracelet (medium-brown skin, short squared French tips, crown ring stack, gold heart ring, blue thumb band) unless you pick the bracelet one.
Real product (product_truth.json): 3 small amber 10 mL bottles (~6 cm tall with cap, thumb height), black ribbed caps with a round scent sticker on top, labels: Christmas Tree hot pink + chartreuse tree + KidSafe; Sugar Plum Fairy lavender + cream blob + KidSafe; Vanilla Spice cream + taupe circle + vanilla pod, NO KidSafe. Cap off: black ring stays, clear-white dropper insert. Box: white with small coloured stars, "Christmas Cheer / Essential Oil Blend Set". No dropper bulb, pump or roller ball. References in every product prompt: a real close-up of each label in frame + the product sheet (refs/product_sheet.png).

## 5. Order of work and time
1. Voiceover (Grace cloned v5) + echo check while all 7 stills render at once (~8 min) -> still storyboard on the review page (your stop 1). Riskiest first: S4 (hand tipping the open bottle, drops).
2. One test clip: S4, with the 3 Seedance no-product clips alongside (~6 min).
3. After S4 passes QC: S1, S6, S7 (~6 min).
4. Cut on the VO, QC (2x edges, first second, labels at 2x, REMOVED.md, verify_fix), compare vs @gretchen_sahm 10.2K, AI finish -> review page (your stop 2) -> Drive.
Machine time ~35-40 min plus your two review stops. House of Rameau version (own order/grade, on-screen hook text, no captions) made free after your OK on the cut; posting only on your OK.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 7 x $0.09 | 0.63 |
| No-product clips, Seedance 2.0 Mini on Kie, 4 s | 3 x $0.164 | 0.49 |
| Product clips, Omni 1.1 Flash on Kie, 4 s | 4 x $0.315 | 1.26 |
| One likely redo (a still + an Omni clip), asked before it runs | $0.09 + $0.315 | 0.41 |
Flow option: you make the 4 product clips free in your Flow app (48 credits) -> Kie total $1.53.
Kling: 0 booked. Ralph 2026-10-30 (via the Niagara session): keep 300 credits for other projects, max 80 per Grace session, only where a shot needs it. Seedance stays first for S2 S3 S5; Kling (40 credits a clip, asked first) only if one of them fails QC.
VO: ElevenLabs Grace cloned v5, ~280 characters.
Month so far (`python3 grace/spend.py`): KIE $232.27  OTHER $0.65  MONTH 2026-10 TOTAL $232.92 (no cap in October; $100 cap from November 1)

TOTAL: $2.79

**Approve?**

## 7. Questions (all of them, now)
Answered by Ralph 2026-10-30 (question cards): 1. hand sheet WITHOUT the bracelet; 2. product clips on Kie Omni ($1.26); 3. voice Grace cloned v5; 4. "Approve, I'll resend pic" (start the stills, check his picture when it arrives).

## 8. Prompts (final, written with prompt-master; every reference named)
Every still and clip prompt is in `shots.json` (built by `make_shots.py`), linted PROMPT_LINT_OK and read end to end; the full text is on the review page.
