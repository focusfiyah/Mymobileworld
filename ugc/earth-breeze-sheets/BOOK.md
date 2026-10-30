# Production Book: Earth Breeze Laundry Detergent Sheets, Fresh Scent (Grace), 2026-10-30

Sent to Ralph: https://claude.ai/artifact/Atwr5b9T6LruEECtf5T7Zr (2026-10-30, plan v1)

## 1. Job
- Client: Grace  Product: Earth Breeze Laundry Detergent Sheets, Fresh Scent, 30 sheets (TikTok Shop 1731996819249271400, 41,232 sold, 4.5 stars)  Route: hands + hand-free AI over the Grace cloned v5 voice (`ugc-product-ad` references/hands-only-and-demo.md + product-lock.md)
- Ralph's choices (2026-10-30): my script + Grace's clone, 1 video 15-20 s, Kie only (no Flow), facts and product sheet from the 8 listing images
- Job folder: `ugc/earth-breeze-sheets/`  Length: ~18.5 s  Shots: 9 (4 HAND-FREE)

## 2. Gate result (`python3 grace/gate.py ugc/earth-breeze-sheets`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | research/playbook.md | OK |
| Coach research (shop + tag + video x5) | research/coach.md | OK: 3 biggest sheet videos (1.7M, 339K, 290K) all open on the sheet melting in water |
| Daily viral board | research/viral/viral-2026-10-30.json | OK (61 shop videos, no sheets in the top 20) |
| Product facts (source) | research/product_facts.md | OK, every line backed by the listing/box |
| Audience | research/audience.md (+ 1,068 searches, 298 comments, reviews) | top question "do laundry detergent sheets work" |
| Hooks modeled on named winners | research/hooks.md | H094 chosen, H117 + H008 as alternates |
| Humanizer | research/humanizer.md, captions.md | triads and stacked closers removed |
| Readability (grade) | research/readability_v1.txt | 3.7 |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized, 58 words)
> Okay, watch what happens when I drop this in water. That's a whole load, melting away. No more hauling a heavy jug, and it leaves no harsh chemical residue. Just pull one out and toss it in. I'm kinda mad nobody told me sooner. Grab a couple boxes before Thanksgiving guests show up. It's in the orange cart.

Hook (H094) / proof / pain / selling point (box's exact words) / how to use / sell-side confession / real urgency (Thanksgiving 2026-11-26) + more units / close. Sources per line: research/line_sources.md. No price, no "order it now", only our product.
On-screen hook text (Grace's cut: none; House of Rameau version keeps one): 1 "this is a whole load of laundry" 2 "watch it disappear" 3 "i'm never buying a jug again".

## 4. Shot list
| # | Window (s) | VO words | On screen | HAND? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | 0-2.6 | "Okay, watch what happens when I drop this in water." | Her fingers drop one white sheet onto a clear glass bowl of water on the washer | HAND | Omni $0.315 | A laundry corner |
| S2 | 2.6-4.6 | "That's a whole load, melting away." | Top-down: the sheet goes see-through and melts into cloudy water, push-in | HAND-FREE | Omni $0.315 | A |
| S3 | 4.6-6.4 | "No more hauling a heavy jug," | Her hand heaves a big plain unlabeled jug, blue drip down its side | HAND | Seedance $0.164 | A |
| S4 | 6.4-8.3 | "and it leaves no harsh chemical residue." | Clean dark navy tee folded on the washer, camera glides along it | HAND-FREE | Seedance $0.164 | B green-tile bathroom |
| S5 | 8.3-10.0 | "Just pull one out" | One hand holds the box, the other pulls a sheet out of the top slot (like the listing how-to photo) | HAND | Omni $0.315 | C blue patterned tile |
| S6 | 10.0-11.6 | "and toss it in." | Her hand tosses the sheet into the open washer onto colourful clothes | HAND | Omni $0.315 | B |
| S7 | 11.6-13.6 | "I'm kinda mad nobody told me sooner." | One box standing on the washer by the plant and folded towels, push-in | HAND-FREE | Omni $0.315 | A |
| S8 | 13.6-16.4 | "Grab a couple boxes before Thanksgiving guests show up." | TWO boxes on fresh folded towels at the foot of a made guest bed, dolly in | HAND-FREE | Omni $0.315 | D guest bedroom |
| S9 | 16.4-18.5 | "It's in the orange cart." | END: her hand holds ONE box toward the lens | HAND | Omni $0.315 | B |

Hand: Grace's hand sheet WITHOUT the bracelet (medium-brown skin, short squared French tips, silver crown ring stack, gold heart ring, blue thumb band, bare wrist): your pick in Q1.
Setting: 4 real Pexels/Pixabay rooms (rooms/SOURCES.md): A laundry corner with plant, B green-tile bathroom with washer, C blue patterned tile + woven hamper, D bright guest bedroom. Bright, colour, no white-on-white.
Real product (product_truth.json, from the listing photos): flat slim box ~25 x 16 x 1 cm (tablet size, phone thin), sky-blue front exactly as the listing (FRESH SCENT tab, 60 LOADS, earth breeze logo, "laundry detergent sheets" banner, turtle, NO HARSH CHEMICAL RESIDUE, t-shirt, 30 SHEETS); sheets pull out of a slot on the top edge; each sheet plain white, paper-thin, 14 x 11 cm, NOT perforated. NOT the older "eco sheets" box on earthbreeze.com.

## 5. Order of work and time
1. All 9 stills at once (~6 min) -> still storyboard on the review page (your stop 1). Riskiest first: S5 (two hands + box print + sheet coming out of the slot).
2. One test clip: S5 Omni, with the 2 Seedance no-product clips alongside (~5 min).
3. After S5 passes QC: the other 6 Omni clips at once (~6 min). VO made while the stills render.
4. Cut on the Grace v5 voice (echo gate <= 150 ms), QC (2x edges, first second, REMOVED.md, verify_fix), coach compare vs @get_whitehack 1.7M, AI finish -> review page (your stop 2) -> Drive.
5. House of Rameau version: free re-cut of the same clips (other order, framing and grade) + hook text from frame 0, no captions; posted only on your OK.
Machine time ~35-40 min plus your two review stops.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 9 x $0.09 | 0.81 |
| Product clips, Omni 1.1 Flash on Kie, 4 s | 7 x $0.315 | 2.205 |
| No-product clips, Seedance 2.0 Mini on Kie, 4 s | 2 x $0.164 | 0.328 |
| One likely redo (a still + an Omni clip), asked before it runs | $0.09 + $0.315 | 0.405 |
ElevenLabs: ~300 characters (Grace cloned v5). House of Rameau version: $0 (re-cut).
Month so far (`python3 grace/spend.py`): KIE $232.27  OTHER $0.65  MONTH 2026-10 TOTAL $232.92 (no cap this month)

TOTAL: $3.75

**Approve?**

## 7. Questions (all of them, now)
1. Hand sheet: WITHOUT the bracelet (my default) or WITH it?
2. S1, S2, S6 show only the plain white sheet (no print). Keep them on Omni as the product-lock rule says (in the total), or Seedance to save $0.45?
3. House of Rameau version with hook text 1 "this is a whole load of laundry": yes?

## 8. Prompts (final, written with prompt-master after loading it; every reference named; all 18 linted PROMPT_LINT_OK)
| Item | Model | Prompt file / text |
|---|---|---|
| 9 stills | Kie nano-banana-pro (Gemini 3 Pro Image), 9:16 | prompts/still_S1..S9.txt (= shots.json `still`) + `still_refs` (sheet, front close-up, sheet close-up, hand sheet, room) |
| 7 product clips | Omni 1.1 Flash on Kie (omni_clip.py), 4 s | prompts/clip_S1,S2,S5..S9.txt, image 1 = approved still, then the real front close-up / sheet close-up, last = product sheet |
| 2 no-product clips | Kie Seedance 2.0 Mini, reference mode, 4 s | prompts/clip_S3.txt, clip_S4.txt ("no detergent box, no laundry sheet appears") |
Generator: make_shots.py.
