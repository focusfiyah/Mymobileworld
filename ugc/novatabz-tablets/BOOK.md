# Production Book, NovaTabz Toothpaste Tablets V1 (Grace), 2026-10-30

Sent to Ralph: https://claude.ai/artifact/6A88QRQeyEJyNgZWrPwsRe (2026-10-30)

## 1. Job
- Client: Grace. Product: NovaTabz Toothpaste Tablets, Peppermint, 62 count (Nova Labs Innovation). Route: hands-only + hand-free AI over a voiceover (ugc-product-ad references/hands-only-and-demo.md + product-lock.md)
- Job folder: `ugc/novatabz-tablets/`  Target length: ~30 s  Shots: 12 (6 HAND, 6 HAND-FREE; 7 show the jar)

## 2. Gate result (`python3 grace/gate.py ugc/novatabz-tablets`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (tag/shop/discover + video x3) | research/coach_research.md | OK: DR.DENT 31.2M + 1.4M, Mouthology 960K, 3 NovaTabz videos |
| Daily viral board | research/coach/viral-2026-10-30.json | OK: hydroxyapatite gum #2 and Mouthology #6 today |
| Audience | research/audience.md (1,932 searches, 107 comments, Amazon buyers) | OK |
| Product facts (source) | research/product_facts.md (Amazon listing + your 3 photos) | OK |
| Hooks modeled on named winners | research/hooks.md | OK: H099 picked |
| Humanizer | proof/humanizer.md | OK |
| Readability (grade) | research/readability_v1.txt | 3.5 |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized), V1:
1. At first I thought these were breath mints.
2. Nope, it's toothpaste.
3. No more dried paste in the sink or a tube leaking in your bag.
4. Chew one, brush with a wet toothbrush, and it foams like regular paste.
5. Nano hydroxyapatite, no fluoride, and a glass jar instead of a tube.
6. People say it leaves a nice tingly, minty clean.
7. The only downside? Nobody has an excuse for a messy sink now.
8. With holiday trips coming, they're not a liquid, so they fly through security.
9. Sixty-two is about a month, so grab one for home and one for your carry-on.
10. It's in the orange cart.
Source of each line: research/line_sources.md (hook H099 + @king_okiki15 and the "I've been eating them!" comment; how-to from the listing + an Amazon buyer; facts from the listing only; no whitening or enamel claims).
On-screen hook text option (only on your yes): "I almost ate one of these".

## 4. Shot list
| # | VO words | On screen | Face? | VO or lip sync | Notes |
|---|---|---|---|---|---|
| S1 | "At first I thought these were breath mints." | Fingers pinch one white tablet up out of the open jar, pink-tile counter | no face | Grace cloned v5 VO | HAND; Flow/Omni; room B |
| S2 | "Nope, it's toothpaste." | Open jar full of tablets beside a toothbrush cup on the grey vanity, push-in | no face | Grace cloned v5 VO | HAND-FREE; Flow/Omni; room A |
| S3 | "No more dried paste in the sink" | Dried toothpaste globs in the vessel sink, plain crusty unbranded tube, push-in | no face | Grace cloned v5 VO | HAND-FREE; Seedance 2.0 Mini; room A |
| S4 | "or a tube leaking in your bag." | Hands open a toiletry pouch on a suitcase: a plain tube leaked paste inside | no face | Grace cloned v5 VO | HAND; Seedance 2.0 Mini; room D |
| S5 | "Chew one," | Hand holds one white tablet up, lifts it out of frame (toward the mouth, no face) | no face | Grace cloned v5 VO | HAND; Seedance 2.0 Mini; room C |
| S6 | "brush with a wet toothbrush," | Hand holds a bamboo toothbrush under the running tap | no face | Grace cloned v5 VO | HAND; Seedance 2.0 Mini; room C |
| S7 | "and it foams like regular paste." | Macro: white foam on the toothbrush resting on the sink rim, bubbles settle | no face | Grace cloned v5 VO | HAND-FREE; Seedance 2.0 Mini; room A |
| S8 | "Nano hydroxyapatite, no fluoride, and a glass jar instead of a tube." | Closed jar on the vanity, slow arc around it, tablets through the glass | no face | Grace cloned v5 VO | HAND-FREE; Flow/Omni; room A |
| S9 | "People say it leaves a nice tingly, minty clean." | Hand twists the silver lid off, mint sprig beside the jar | no face | Grace cloned v5 VO | HAND; Flow/Omni; room B |
| S10 | "The only downside? Nobody has an excuse for a messy sink now." | Spotless sink, jar beside the toothbrush cup, slow side slide | no face | Grace cloned v5 VO | HAND-FREE; Flow/Omni; room A |
| S11 | "With holiday trips coming, they're not a liquid, so they fly through security." | Hand sets the closed jar into a clear toiletry pouch in an open suitcase | no face | Grace cloned v5 VO | HAND; Flow/Omni; room D |
| S12 | "Sixty-two is about a month, so grab one for home and one for your carry-on. It's in the orange cart." | END: one closed jar on the pink-tile counter, push-in to the label | no face | Grace cloned v5 VO | HAND-FREE; Flow/Omni; room B |
Outfit: hands only. Setting: 4 real Pexels rooms (rooms/SOURCES.md): A leaf-wallpaper bathroom, B pink-tile bathroom, C wood vanity + plant, D cream living room with suitcases. Nails / person: Grace's hand sheet WITHOUT bracelet (short squared French tips, crown ring stack, gold heart ring, blue thumb band). Real product confirmed from your 3 photos: clear glass jar 2.17 x 2.17 x 1.65 in, brushed silver ridged screw lid, turquoise label (TOOTHPASTE TABLETS / NOVA TABZ / PEPPERMINT / 62 TABLETS / NET WT 23G (0.8 OZ)), plain white round flat tablets.

## 5. Order of work
Still storyboard first (your stop 1) -> riskiest clip first as the ONE test clip (S9: hand unscrews the lid; lids and grips drift most) -> the rest at once -> cut on the Grace cloned v5 VO (echo <= 150 ms), QC (2x edges, first second, label letters on several frames, REMOVED.md), coach compare vs @nextgenthreads, AI finish -> review page (your stop 2) -> Drive. House of Rameau version: the same footage re-ordered/re-graded with the on-screen hook, no captions (posting only on your OK).
Free fixes planned: crop or retime before any redo; tablet-only S5 needs no jar.
Time: ~40 min machine time, plus your two review stops (Flow clips add your app time).

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 12 x $0.09 | 1.08 |
| No-product clips, Seedance 2.0 Mini on Kie, 4 s | 5 x $0.164 | 0.82 |
| Product clips, Omni 1.1 Flash on Kie, 4 s (only if you skip Flow) | 7 x $0.315 | 2.205 |
| One likely redo (a still + an Omni clip), asked before it runs | $0.09 + $0.315 | 0.405 |
Expected spend with Flow for the 7 product clips (84 of your Flow credits): $1.99 (stills $1.08 + Seedance $0.82 + a still redo $0.09). With your Gemini app for the stills too: $0.82.
ElevenLabs: ~560 chars (Grace cloned v5).
Month so far (`python3 grace/spend.py`): KIE $232.27  OTHER $0.65  MONTH 2026-10 TOTAL $232.92 (no cap this month; from Nov 1 the $100 cap starts, and anything that runs then counts there).

TOTAL: $4.51

**Approve?**

## 7. Questions
1. Product clips: Flow in your app ($0, 84 credits) or Kie Omni ($2.21)?
2. Stills: Kie ($1.08) or your Gemini app ($0, I send a kit)?
3. Hand sheet without the bracelet (my pick for a bathroom) or with it?
4. On-screen hook text on Grace's version: no (default) or yes?
5. Product details above right (jar, lid, label, white tablets), and the facts we say (no whitening/enamel claims)?

## 8. Prompts (final, written with prompt-master after loading it; every reference named; linted MARKED_OK)
| Item | Model | Prompt file / text |
|---|---|---|
| 12 stills | Kie nano-banana-pro, 9:16 | prompts/still_S1..S12.txt (refs in shots.json still_refs: sheet, label close-up, lid close-up, room, hand sheet) |
| 7 product clips | Omni 1.1 Flash (Flow kit or Kie), 4 s | prompts/clip_S1,S2,S8-S12.txt; image 1 = approved still, 2 = label, 3 = lid, 4 = sheet |
| 5 no-product clips | Seedance 2.0 Mini, reference mode, 4 s | prompts/clip_S3-S7.txt; image 1 = still, 2 = hand sheet when a hand shows |
