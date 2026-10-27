# Production Book: PRITECH Heated Face Scrubber, black, 3 new videos V2-V4 (Grace), 2026-10-27

Sent to Ralph: https://claude.ai/artifact/Ud3ZURCMtYjMBMSK24vHdb (2026-10-27, 15 s version)

## 1. Job
- Client / own content: Grace  Product: PRITECH heatable vibrating face scrubber, BLACK (BCM-1485), same as V1  Route: hands + hand-free AI over Grace's voice, no full face, product lock = Omni 1.1 Flash on Kie (Ralph's pick 2026-10-27, `.claude/skills/ugc-product-ad/references/product-lock.md`)
- Job folder: `ugc/pritech-15s/`  Target length: ~15 s each (V2 14.2 s, V3 15.3 s, V4 14.4 s at 3.53 words/sec)  Shots: 18 (V2 6, V3 5, V4 7; 7 HAND-FREE)
- Reused from V1 for $0: the approved product sheet (real photos only), the real close-ups (bristle head, buttons, PRITECH on the stand), Grace's hand sheet, all research. NOT reused: any V1 footage, room, framing or order (every video looks different, hard rule 6).

## 2. Gate result (`python3 grace/gate.py ugc/pritech-15s`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | research/playbook.md | OK |
| Coach research (tag/shop/discover + video x3) | research/coach.md (V1 research + today's 2 new PRITECH winners: @giovanni.welch 2.8M, @joshjshowcase 2.7M) | OK |
| Daily viral board | research/viral/viral-2026-10-27.json (today) | OK |
| Product facts (source) | research/product_facts.md (+ 2026-10-27 section) | every claim backed |
| Audience | research/audience.md, voc.md ("heated?", "facial cleansing brush vs hands") | OK |
| Hooks modeled on named winners | research/hooks.md (3 options per video + on-screen text options) | OK |
| Humanizer | research/humanizer.md, captions.md | OK, 4 lines tightened (no claim we can't back) |
| Readability (grade) | research/readability_v2/v3/v4.txt | 1.6 / 2.4 / 2.8 |
| Banned-phrase check | gate.py | OK |

## 3. Scripts (final, Humanized; mine, Ralph: "1. Yours"; cut to ~15 s, Ralph 2026-10-27: "Lets drop the timefrane to 15s")
Structure each: hook / pain / selling points / sell-side confession / real season + one-more-unit CTA / "It's in the orange cart." No price, no "order it now", only our product. Source of each line: research/line_sources.md. The 15-20 s versions: research/scripts_round2_20s.md.

**V2, hook H062 pain call-out (towel), 50 words ~14.2 s, grade 1.6**
> You know when you dry your face and the towel still has makeup on it? Your hands are leaving it behind. This brush has soft silicone bristles and five speeds. Only problem? Washing with your hands feels sad now. Grab one for your sister too. It's in the orange cart.

**V3, hook H102 curiosity (warm silver end), 54 words ~15.3 s, grade 2.4**
> This looked like a normal face brush until I saw the silver end. It warms up to a hundred and four degrees, so you get a facial at home, no spa bill. I hate how much I look forward to it. Cold weather's coming, get one for your mom. It's in the orange cart.

**V4, hook H061 identity (falls asleep in makeup), 51 words ~14.4 s, grade 2.8**
> This is for everybody who falls asleep in their makeup. A quick splash with your hands leaves it behind. This brush does the work: soft bristles, five speeds. I'm mad it's this easy, now I have no excuse. Holidays are coming, grab one for your bestie. It's in the orange cart.

Facts: soft silicone (box), five speeds (listing: 5 levels), 104 degrees = the listing's constant 40°C on the SILVER END, no breakout or bacteria claims. No on-screen text (Ralph: "4.same"). Captions: captions.md.

## 4. Shot lists (15 s; each video its own theme, no shot idea repeated, every shot shows its words)
Columns: shot | VO words | on screen | HAND? | face? | clip | room. Every shot moves; no text; no word on the brush itself (PRITECH only on the stand).
Dropped for 15 s (stills already made, no clips): V2 S3 bristle macro, V3 S3 spa corner, V3 S4 cleanser pump.

**V2** (proof on the towel and the hands, then the fix; bright neutral daylight; blush pink basin + walnut vanity)

| # | VO words | On screen | HAND? | Face? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | "You know when you dry your face and the towel still has makeup on it?" | Towel on its ring with beige foundation + mascara smears, push-in | HAND-FREE | no | Seedance $0.164 | D blush basin |
| S2 | "Your hands are leaving it behind." | Fingertips under a thin gold tap, makeup still on them | HAND | no | Seedance $0.164 | D blush basin |
| S5 | "This brush has soft silicone bristles" | Bristles circle on her foamy cheek | HAND | cheek/jaw only | Kie Omni $0.315 | D blush basin |
| S4 | "and five speeds." | Thumb taps ((•)), the drops on the nubs shiver harder each tap | HAND | no | Kie Omni $0.315 | D blush basin |
| S6 | "Only problem? Washing with your hands feels sad now." | Bare palms rub cleanser together, slow and half-hearted | HAND | no | Seedance $0.164 | E walnut vanity |
| S7 | "Grab one for your sister too. It's in the orange cart." | END (new, Ralph: old S7 "not good"): one brush standing upright on its silver end on the tile ledge by the blush basin, wet, push-in | HAND-FREE | no | Kie Omni $0.315 | D blush basin |

**V3** (warmth: the silver end, a bath tray with tea, a frosty window; bright cool daylight; blue tile + blue bath)

| # | VO words | On screen | HAND? | Face? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | "This looked like a normal face brush until I saw the silver end." | Brush pointed away, silver end nearest the lens, push-in (still redo) | HAND | no | Kie Omni $0.315 | F blue tile + tub |
| S2 | "It warms up to a hundred and four degrees," | Thumb presses the °C button | HAND | no | Kie Omni $0.315 | F blue tile + tub |
| S5 | "so you get a facial at home, no spa bill." | Silver end glides in small circles on her clean cheekbone (still redo) | HAND | cheek/jaw only | Kie Omni $0.315 | F blue tile + tub |
| S6 | "I hate how much I look forward to it." | Brush on a wooden bath tray with a mug of tea over the bath, push-in | HAND-FREE | no | Kie Omni $0.315 | F blue tile + tub |
| S7 | "Cold weather's coming, get one for your mom. It's in the orange cart." | END: brush on a cream knit blanket by a frosty window, push-in | HAND-FREE | no | Kie Omni $0.315 | G blue bath + window |

**V4** (bedtime: the pillowcase, quick and easy; bright clean morning light; blue-grey bedroom + marble vanity)

| # | VO words | On screen | HAND? | Face? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | "This is for everybody who falls asleep in their makeup." | Pillowcase with a foundation smudge + mascara marks, push-in | HAND-FREE | no | Seedance $0.164 | H blue-grey bed |
| S2 | "A quick splash with your hands leaves it behind." | Cupped hands splash water up out of frame at the marble sink | HAND | no | Seedance $0.164 | I marble vanity |
| S3 | "This brush does the work:" | Hand lifts the brush up out of its stand | HAND | no | Kie Omni $0.315 | I marble vanity |
| S4 | "soft bristles," | Bristles stroke along her foamy jawline, seen from below | HAND | cheek/jaw only | Kie Omni $0.315 | I marble vanity |
| S5 | "five speeds." | Brush switched on lying on wet marble: the water around it ripples and jumps | HAND-FREE | no | Kie Omni $0.315 | I marble vanity |
| S6 | "I'm mad it's this easy, now I have no excuse." | Brush rinsed under the tap, foam gone in two seconds | HAND | no | Kie Omni $0.315 | I marble vanity |
| S7 | "Holidays are coming, grab one for your bestie. It's in the orange cart." | END: brush in its stand on the bedside table next to a small wrapped gift, push-in | HAND-FREE | no | Kie Omni $0.315 | H blue-grey bed |

Nails / person details: Grace's hand sheet WITHOUT the bracelet, like V1: medium-brown skin, short squared French tips, silver crown ring stack, small gold heart ring, blue thumb band, bare wrist. Face shots = cheek or jaw only, eyes and mouth never in frame (REMOVED.md), so no lip sync.
Real product (from the real photos, product_truth.json): slim matte black curved wand ~15-16 cm, oval head of black silicone nubs, 3 moulded buttons ((•)) / O / °C, wide silver chrome end, black stand with grey PRITECH. Forbidden: glowing bristles, pink egg brush, screens, LED rings.
Rooms: 6 new real Pexels/Pixabay photos, none from V1 (rooms/SOURCES.md, contact sheet on the review page).

## 5. Order of work and time
1. Stills: done (21); 3 more (2 redos + new V2 S7) (~6 min) -> still storyboard on the review page (your stop 1).
2. Riskiest clip first: V3 S5 (silver end on the cheek; Kie refused a foamy-cheek still on V1) as the ONE Kie Omni test clip, with the 6 Seedance no-product clips alongside (~5 min).
3. After the test passes QC: the other 12 Omni clips at once (~6 min).
4. Grace voice, 3 VOs (echo gate <= 150 ms), 3 cuts, QC (2x edges, first second, REMOVED.md, verify_fix), compare vs @joshjshowcase 2.7M, AI finish -> review page (your stop 4) -> Drive.
Machine time from here ~45 min (3 stills ~5 min, VOs ~3 min, test clip ~5 min, 12 Omni + 5 Seedance ~10 min, cuts + QC ~20 min), plus your review stops (storyboard, cuts).
Free fixes planned: crop/retime/trim any turn or flip (V1's flip after 2.5 s was trimmed free); an Omni edit turn ($0.84) or redo only when asked, with the cost.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills already made (21, Kie nano-banana-pro) | 21 x $0.09 | 1.89 (spent) |
| Still redos V3 S1 (handle print) + V3 S5 (backwards) | 2 x $0.09 | 0.18 |
| New V2 S7 end still (old one "not good") | 1 x $0.09 | 0.09 |
| Product clips, Omni 1.1 Flash on Kie, 4 s | 13 x $0.315 | 4.095 |
| No-product clips, Seedance 2.0 Mini on Kie, 4 s | 5 x $0.164 | 0.82 |
| One likely redo (an Omni clip), asked before it runs | 1 x $0.315 | 0.315 |
Total Kie: $7.39 incl. the $1.89 spent. ElevenLabs: ~810 chars for the 3 new 15 s voiceovers (the 15-20 s ones used ~1,040).
Month so far (`python3 grace/spend.py`): $183.51 (no cap in October).

TOTAL: $7.39

**Approve?**

## 7. Ralph's answers (2026-10-27: "1. Yours 2.kie omni 3.kie 4.same")
1. Scripts: mine (V2 H062, V3 H102, V4 H061), as in §3.
2. Product clips: Kie Omni for all of them (13 in the 15 s version, in the TOTAL), not Flow.
3. Stills on Kie ($1.89).
4. Same hand as V1 (sheet without the bracelet, short squared French tips); no on-screen text.

## 8. Prompts (final, written with prompt-master after loading it; every reference named; linted PROMPT_LINT_OK)
| Item | Model | Prompt file / text |
|---|---|---|
| 21 stills | Kie nano-banana-pro (Gemini 3 Pro Image), 9:16 1K | shots.json `still` (exact text sent) + `still_refs` (sheet, close-ups that frame shows, room, hand sheet) |
| 15 product clips | Omni 1.1 Flash on Kie (omni_clip.py), 4 s | shots.json `clip`, image 1 = approved still, then the real close-ups, last = sheet (`clip_refs`) |
| 6 no-product clips | Kie Seedance 2.0 Mini, reference mode, 4 s | shots.json `clip` + `clip_refs` (still, hand sheet when a hand shows); "no brush, no product appears" |
Generator: make_shots.py (shared product/hand blocks copied from V1's approved prompts).
