# Production Book: PRITECH Heated Face Scrubber, black, 3 new videos V2-V4 (Grace), 2026-10-27

Sent to Ralph: https://claude.ai/artifact/Ud3ZURCMtYjMBMSK24vHdb (2026-10-27)

## 1. Job
- Client / own content: Grace  Product: PRITECH heatable vibrating face scrubber, BLACK (BCM-1485), same as V1  Route: hands + hand-free AI over Grace's voice, no full face, product lock with Flow first (`.claude/skills/ugc-product-ad/references/product-lock.md`, `grace/flow/README.md`)
- Job folder: `ugc/pritech-15s/`  Target length: 15-20 s each (V2 18.4 s, V3 19.5 s, V4 17.8 s at Grace's measured 3.53 words/sec)  Shots: 20 (V2 6, V3 7, V4 7; 8 HAND-FREE)
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
| Readability (grade) | research/readability_v2/v3/v4.txt | 2.2 / 2.4 / 3.3 |
| Banned-phrase check | gate.py | OK |

## 3. Scripts (final, Humanized; written by me from the research, not Grace's words)
Structure each: hook / pain / selling points / sell-side confession / real season + one-more-unit CTA / "It's in the orange cart." No price, no "order it now", only our product. Source of each line: research/line_sources.md.

**V2, hook H062 pain call-out (towel), ~18.4 s, grade 2.2**
> You know that moment you dry your face and the towel still comes up with makeup on it? Yeah, your hands are leaving it behind. This brush has soft silicone bristles and five speeds, so you get a real deep clean. Only problem? Washing with your hands feels sad after this. Grab one for you and one for your sister. It's in the orange cart.

**V3, hook H102 curiosity (warm silver end), ~19.5 s, grade 2.4**
> This looked like a normal face brush until I noticed the silver end. It warms up to a hundred and four degrees. Who has time or money for a facial every week? Wash with the soft bristles, then rub the warm end in little circles. I hate how much I look forward to it. Cold weather's coming, so get one for your mom too. It's in the orange cart.

**V4, hook H061 identity (falls asleep in makeup), ~17.8 s, grade 3.3**
> This is for everybody who always falls asleep with their makeup on. A quick splash with your hands leaves makeup behind. This brush does the work for you, with soft silicone bristles and five speeds. I'm mad it makes washing this easy. Now I have no excuse. The holidays are coming, so grab one for your bestie too. It's in the orange cart.

Flag: the confessions ("Only problem? Washing with your hands feels sad after this", "I hate how much I look forward to it", "Now I have no excuse") are Grace talking as an owner. She has the black one (your note 2026-10-23), so I kept them.
Facts: soft silicone (box), five speeds (listing: 5 levels), 104 degrees = the listing's constant 40°C on the SILVER END (not the bristles), deep clean (box "Deep cleaning"). No breakout or bacteria claims (the 2.7M winner said "breakouts"; we don't).
On-screen hook text (only on your yes; default none): V2 "the towel told on me", V3 "wait, it gets warm?", V4 "your pillowcase knows".
Captions: captions.md (#ad, no price).

## 4. Shot lists
Columns: shot | VO words | on screen | HAND? | face? | clip | room. Every shot moves; no text; product never glows; the heat shots show the silver end.

**V2** (bright neutral daylight; blush pink basin + walnut vanity; pink towel headband, white tee)

| # | VO words | On screen | HAND? | Face? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | "You know that moment you dry your face and the towel still comes up with makeup on it?" | Hand pulls a white face towel off her cheek: beige foundation + mascara smears on it | HAND | cheek/jaw only | Seedance $0.164 | D blush basin |
| S2 | "Yeah, your hands are leaving it behind." | Fingertips rub under a thin gold tap stream, makeup still on them | HAND | no | Seedance $0.164 | D blush basin |
| S3 | "This brush has soft silicone bristles" | Fingertip presses the black nubs, they bend and spring back | HAND | no | Flow (Omni) $0 | D blush basin |
| S4 | "and five speeds, so you get a real deep clean." | Brush circles on her foamy cheek, thumb on ((•)) | HAND | cheek/jaw only | Flow (Omni) $0 | D blush basin |
| S5 | "Only problem? Washing with your hands feels sad after this." | Brush lying wet on a folded towel by the vessel sink, slow sideways dolly | HAND-FREE | no | Flow (Omni) $0 | E walnut vanity |
| S6 | "Grab one for you and one for your sister. It's in the orange cart." | END: one brush in its stand (PRITECH readable), low angle, push-in | HAND-FREE | no | Flow (Omni) $0 | E walnut vanity |

**V3** (bright cool daylight; deep blue tile + blue bath with frosted window; light blue headband, white waffle robe)

| # | VO words | On screen | HAND? | Face? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | "This looked like a normal face brush until I noticed the silver end." | Brush tilted to the lens, silver end nearest, push-in | HAND | no | Flow (Omni) $0 | F blue tile |
| S2 | "It warms up to a hundred and four degrees." | Thumb presses the °C button | HAND | no | Flow (Omni) $0 | F blue tile |
| S3 | "Who has time or money for a facial every week?" | Spa corner: rolled towels, eucalyptus, unlit candle, slow dolly | HAND-FREE | no | Seedance $0.164 | G blue bath + window |
| S4 | "Wash with the soft bristles," | Bristles circle on her foamy cheek (side view) | HAND | cheek/jaw only | Flow (Omni) $0 | F blue tile |
| S5 | "then rub the warm end in little circles." | Silver end glides in small circles on her clean cheekbone | HAND | cheek/jaw only | Flow (Omni) $0 | F blue tile |
| S6 | "I hate how much I look forward to it." | Brush on a waffle towel on the tub edge, silver end to camera, half arc | HAND-FREE | no | Flow (Omni) $0 | F blue tile |
| S7 | "Cold weather's coming, so get one for your mom too. It's in the orange cart." | END: one brush in its stand under the frosted window, push-in | HAND-FREE | no | Flow (Omni) $0 | G blue bath + window |

**V4** (bright clean morning light; blue-grey bed + white marble vanity; grey tee)

| # | VO words | On screen | HAND? | Face? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | "This is for everybody who always falls asleep with their makeup on." | Pillowcase with a foundation smudge + mascara marks, slow push-in | HAND-FREE | no | Seedance $0.164 | H blue-grey bed |
| S2 | "A quick splash with your hands leaves makeup behind." | Cupped hands lift water up out of frame at the marble sink | HAND | no | Seedance $0.164 | I marble vanity |
| S3 | "This brush does the work for you," | Hand lifts the brush up out of its stand | HAND | no | Flow (Omni) $0 | I marble vanity |
| S4 | "with soft silicone bristles" | Bristles stroke along her foamy jawline (low angle) | HAND | cheek/jaw only | Flow (Omni) $0 | I marble vanity |
| S5 | "and five speeds." | Thumb presses ((•)), water drops shiver | HAND | no | Flow (Omni) $0 | I marble vanity |
| S6 | "I'm mad it makes washing this easy. Now I have no excuse." | Brush in its stand by the sink, wet, slow arc | HAND-FREE | no | Flow (Omni) $0 | I marble vanity |
| S7 | "The holidays are coming, so grab one for your bestie too. It's in the orange cart." | END: one brush in its stand beside a small white gift with a red ribbon, push-in | HAND-FREE | no | Flow (Omni) $0 | I marble vanity |

Nails / person details: Grace's hand sheet WITHOUT the bracelet, like V1: medium-brown skin, short squared French tips, silver crown ring stack, small gold heart ring, blue thumb band, bare wrist. Face shots = cheek or jaw only, eyes and mouth never in frame (REMOVED.md), so no lip sync.
Real product (from the real photos, product_truth.json): slim matte black curved wand ~15-16 cm, oval head of black silicone nubs, 3 moulded buttons ((•)) / O / °C, wide silver chrome end, black stand with grey PRITECH. Forbidden: glowing bristles, pink egg brush, screens, LED rings.
Rooms: 6 new real Pexels/Pixabay photos, none from V1 (rooms/SOURCES.md, contact sheet on the review page).

## 5. Order of work and time
1. Stills: all 20 at once (~6 min) -> still storyboard on the review page (your stop 1).
2. Riskiest clip first: V3 S5 (silver end on the cheek; Kie refused a foamy-cheek still on V1) as the ONE test: Flow kit for you (your stop 2) + the 5 Seedance no-product clips run while you make it (~5 min).
3. After the test passes: Flow kits for the other 14 product clips (on one review page, Save/Copy buttons), you make them (your stop 3).
4. Grace voice, 3 VOs (echo gate <= 150 ms), 3 cuts, QC (2x edges, first second, REMOVED.md, verify_fix), compare vs @joshjshowcase 2.7M, AI finish -> review page (your stop 4) -> Drive.
Machine time ~35-40 min for the first video + ~10 min for each of the other two (they run side by side) = about 1 hour, plus your Flow time and review stops.
Free fixes planned: crop/retime/trim any turn or flip (V1's flip after 2.5 s was trimmed free); Kie Omni only if a Flow take fails QC, asked with the cost.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro), like V1 | 20 x $0.09 | 1.80 |
| No-product clips, Seedance 2.0 Mini on Kie, 4 s | 5 x $0.164 | 0.82 |
| Product clips, Omni 1.1 Flash in your Google Flow app | 15 x 12 credits = 180 of your 1,050 | 0.00 |
| One likely redo (a still + a Seedance clip), asked before it runs | $0.09 + $0.164 | 0.254 |
Total Kie: $2.874 incl. the redo. ElevenLabs: ~1,040 chars (Grace cloned, 3 VOs). If you'd rather not make 15 Flow takes: Kie Omni for all 15 = +$4.725. $0 still option: you make the 20 stills in your Gemini app from my kit -> total $1.07.
Month so far (`python3 grace/spend.py`): $181.62 (no cap in October; from November $100/month).

TOTAL: $2.88

**Approve?**

## 7. Questions (all of them, now)
1. Scripts: OK to use my three (above), or does Grace have her own for these?
2. Product clips: Flow for all 15 (your standing rule, $0, ~15 takes for you), or Kie Omni for some/all (+$0.315 each)?
3. Stills on Kie ($1.80, like V1) or your Gemini app ($0)?
4. Same hand as V1 (no bracelet, French tips) and no on-screen text?

## 8. Prompts (final, written with prompt-master after loading it; every reference named; linted PROMPT_LINT_OK)
| Item | Model | Prompt file / text |
|---|---|---|
| 20 stills | Kie nano-banana-pro (Gemini 3 Pro Image), 9:16 1K | shots.json `still` (exact text sent) + `still_refs` (sheet, close-ups that frame shows, room, hand sheet) |
| 15 product clips | Omni 1.1 Flash (Flow kit; Kie only if asked) | shots.json `clip`, image 1 = approved still, then the real close-ups, last = sheet (`clip_refs`) |
| 5 no-product clips | Kie Seedance 2.0 Mini, reference mode, 4 s | shots.json `clip` + `clip_refs` (still, hand sheet when a hand shows); "no brush, no product appears" |
Generator: make_shots.py (shared product/hand blocks copied from V1's approved prompts).
