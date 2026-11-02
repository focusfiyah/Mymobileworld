# Production Book: Bare Anatomy Rosemary & Rice Water Hair Spray, 3-pack (Grace), 2026-11-02

Sent to Ralph: https://claude.ai/artifact/W6yuV9J7ewgwm9ytzV4WBs (2026-11-02, plan v1)

## 1. Job
- Client: Grace  Product: Bare Anatomy Rosemary & Rice Water Hair Spray, 200 ml, pack of 3 (TikTok Shop 1729505063356962201, 190,793 sold, 4.7 stars)
- Route: hands + hand-free AI clips, music only (Grace adds the music), no voiceover, no on-screen text, no caption (Ralph 2026-11-02)
- Ralph's choices (2026-11-02): "10s, 10-12s"; text "No"; "One video, spray first"; "No captions needed"; "All on kie"
- Job folder: `ugc/bare-anatomy-rosemary-spray/`  Length: 11.4 s  Shots: 7 (3 HAND-FREE); shot 7 is three 0.6 s cuts

## 2. Gate result (`python3 grace/gate.py ugc/bare-anatomy-rosemary-spray`): GATE OK
Playbook, coach research (shop + discover + 5 videos), product facts, audience (1,756 searches, 268 comments), hooks, humanizer, readability (3.2), banned-phrase check: all OK. Viral board: TikTok hashtag pages returned 0 videos this run.

## 3. Script
Music only. Script versions for later are in Drive ("CURRENT - Rosemary Spray 3 script versions"); none is burned in.

## 4. Shot list
| # | Window (s) | Beat | On screen | HAND? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | 0-2.0 | Hook | Her hand sprays the bottle onto the scalp along a braid part of Grace's braids, mist | HAND | Omni $0.315 | A green tiles |
| S2 | 2.0-3.4 | Pain | Small pot of rosemary simmering on a gas stove, steam, dolly in | HAND-FREE | Seedance $0.164 | C kitchen |
| S3 | 3.4-5.0 | Solution | Exactly three bottles on the counter with a rosemary sprig and a bowl of rice, small slide | HAND-FREE | Omni $0.315 | B green mosaic + plants |
| S4 | 5.0-6.6 | How to use | Her fingertips rub the scalp along a braid part (no bottle) | HAND | Seedance $0.164 | A |
| S5 | 6.6-8.0 | Selling point | Her fingers slide down her braids to the curly ends, soft and light (no bottle; a comb cannot go through braids) | HAND | Seedance $0.164 | A |
| S6 | 8.0-9.4 | Urgency | One bottle on a white windowsill, frost on the glass, snowy garden, push-in | HAND-FREE | Omni $0.315 | described (no real frosty window found) |
| S7a | 9.4-10.0 | Close | Her hand sets a bottle on the shower ledge | HAND | Omni $0.315 | D tropical-leaf shower |
| S7b | 10.0-10.6 | Close | Her hand drops a bottle into an open gym bag | HAND | Omni $0.315 | E wood table + plants |
| S7c | 10.6-11.4 | Close | Her hand holds a bottle out toward the lens | HAND | Omni $0.315 | F bright plant kitchen |

Hand: Grace's hand sheet WITHOUT the bracelet (medium-brown skin, short French tips, silver crown ring stack, gold heart ring, blue thumb band, bare wrist).
Hair (S1, S4, S5): Grace's real hair (Ralph 2026-11-02: "it should look like Grace's hair"): long black knotless boho braids with curly ends, from her own photo (refs/grace_hair.jpg, cropped with no face); no face anywhere.
Rooms: 6 real Pexels photos (rooms/SOURCES.md), bright with colour.
Real product (product_truth.json, from the listing photos + Grace's screenshots): clear round bottle with rounded shoulders, clear colourless liquid, tall black collar, black trigger sprayer; front label BARE ANATOMY / NATURE x SCIENCE / splash with rosemary / "Rosemary & Rice Water" purple / HAIR SPRAY / ALCOHOL FREE + SULPHATE FREE icons / 200 ml | 6.76 fl oz. No box. Size ~17 cm tall, ~5 cm wide (estimated: the maker gives no dimensions).
References on every product still and clip: product sheet (refs/product_sheet.png), real front label close-up (refs/closeup_front.png), sprayer close-up (S1).

## 5. Order of work and time
1. All 9 stills at once (~6 min) -> storyboard on the review page (your stop 1). Riskiest: S1 (hand + trigger + label + hair).
2. One test clip: S1 Omni, with the 3 Seedance no-product clips alongside (~5 min).
3. After S1 passes QC: the other 5 Omni clips at once (~6 min).
4. Cut (music-free, Grace adds music), QC (2x edges, first second, label on several frames, REMOVED.md, verify_fix), AI finish -> review page (your stop 2) -> Drive.
Machine time ~35-40 min plus your two review stops.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 9 x $0.09 | 0.81 |
| Product clips, Omni 1.1 Flash on Kie, 4 s | 6 x $0.315 | 1.89 |
| No-product clips, Seedance 2.0 Mini on Kie, 4 s | 3 x $0.164 | 0.492 |
| One likely redo (a still + an Omni clip), asked before it runs | $0.09 + $0.315 | 0.405 |
Month so far (`python3 grace/spend.py`): KIE $1.32 of the $100 November cap.

TOTAL: $3.60

**Approve?**

## 7. Questions
Ralph's answers 2026-11-02: "The plan is approved and it should look like Grace's hair." Grace's hair = braids, so S5 changed from a comb to fingers sliding down the braids (same model, same cost).

## 8. Prompts (written with prompt-master after loading it; all 18 linted PROMPT_LINT_OK and marked checked)
| Item | Model | Prompt file |
|---|---|---|
| 9 stills | Kie nano-banana-pro, 9:16 | prompts/still_*.txt (= shots.json `still`) + `still_refs` |
| 6 product clips | Omni 1.1 Flash on Kie (omni_clip.py), 4 s | prompts/clip_S1,S3,S6,S7a,S7b,S7c.txt: image 1 = approved still, then the front label close-up (+ sprayer for S1), last = product sheet |
| 3 no-product clips | Kie Seedance 2.0 Mini, reference mode, 4 s | prompts/clip_S2,S4,S5.txt ("no spray bottle and no hair product appears") |
Generator: make_shots.py.
