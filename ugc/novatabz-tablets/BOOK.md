# Production Book, NovaTabz Toothpaste Tablets V1 (Grace), 15 s, 2026-10-30

Sent to Ralph: https://claude.ai/artifact/6A88QRQeyEJyNgZWrPwsRe (2026-10-30, v2: 15 s)

## 1. Job
- Client: Grace. Product: NovaTabz Toothpaste Tablets, Peppermint, 62 count (Nova Labs Innovation). Route: hands-only + hand-free AI over a voiceover (ugc-product-ad references/hands-only-and-demo.md + product-lock.md)
- Job folder: `ugc/novatabz-tablets/`  Target length: 15 s (Ralph 2026-10-30: "Make it 15s")  Shots: 6 (3 HAND, 3 HAND-FREE; 4 show the jar)

## 2. Gate result (`python3 grace/gate.py ugc/novatabz-tablets`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (tag/shop/discover + video x3) | research/coach_research.md | OK: DR.DENT 31.2M + 1.4M, Mouthology 960K, 3 NovaTabz videos |
| Daily viral board | research/coach/viral-2026-10-30.json | OK: hydroxyapatite gum #2 and Mouthology #6 today |
| Audience | research/audience.md | OK |
| Product facts (source) | research/product_facts.md (Amazon listing + your 3 photos) | OK |
| Hooks modeled on named winners | research/hooks.md | OK: H099 |
| Humanizer | proof/humanizer.md | OK |
| Readability (grade) | research/readability_v1.txt | 1.8 |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized), V1:
1. At first I thought these were breath mints.
2. Nope, toothpaste. No more crusty tubes.
3. Chew one, brush, and it foams like paste.
4. Only downside? No excuse for a messy sink.
5. No fluoride, no liquid, so they fly through holiday security.
6. Grab one for home and one for your carry-on. It's in the orange cart.
Source of each line: research/line_sources.md (cut for 15 s: the nano-hydroxyapatite line, now in the caption; "people say tingly minty clean"; "sixty-two is about a month").
On-screen hook text option (only on your yes): "I almost ate one of these".

## 4. Shot list
| # | VO words | On screen | Face? | VO or lip sync | Notes |
|---|---|---|---|---|---|
| S1 | "At first I thought these were breath mints." | Fingers pinch one white tablet up out of the open jar, pink-tile counter | no face | Grace cloned v5 VO | HAND; Flow/Omni; Kling fallback; room B |
| S2 | "Nope, toothpaste. No more crusty tubes." | Dried toothpaste globs in the vessel sink, plain crusty unbranded tube, push-in | no face | Grace cloned v5 VO | HAND-FREE; Seedance 2.0 Mini; room A |
| S3 | "Chew one, brush, and it foams like paste." | Hand holds a foamy bamboo toothbrush over the wood vanity basin, bubbles settle | no face | Grace cloned v5 VO | HAND; Seedance 2.0 Mini; room C |
| S4 | "Only downside? No excuse for a messy sink." | Spotless sink, jar beside the toothbrush cup, slow side slide | no face | Grace cloned v5 VO | HAND-FREE; Flow/Omni; room A |
| S5 | "No fluoride, no liquid, so they fly through holiday security." | Hand sets the closed jar into a clear toiletry pouch in an open suitcase | no face | Grace cloned v5 VO | HAND; Flow/Omni; Kling fallback; room D |
| S6 | "Grab one for home and one for your carry-on. It's in the orange cart." | END: one closed jar on the pink-tile counter, push-in to the label | no face | Grace cloned v5 VO | HAND-FREE; Flow/Omni; room B |
Outfit: hands only. Rooms: A leaf-wallpaper bathroom, B pink-tile bathroom, C wood vanity + plant, D cream room with suitcases (Pexels, rooms/SOURCES.md). Hand: Grace's sheet WITHOUT bracelet unless you say with. Real product: clear glass jar 2.17 x 2.17 x 1.65 in, brushed silver ridged screw lid, turquoise label (TOOTHPASTE TABLETS / NOVA TABZ / PEPPERMINT / 62 TABLETS / NET WT 23G (0.8 OZ)), plain white round flat tablets.

## 5. Order of work
6 stills at once -> still storyboard (your stop 1) -> test clip S5 (hand sets the jar in the pouch: grip + jar drift risk) -> the other 5 at once -> cut on the Grace cloned v5 VO (echo <= 150 ms, ~15 s), QC (2x edges, first second, label letters on several frames, REMOVED.md), compare vs @nextgenthreads, AI finish -> review page (your stop 2) -> Drive. House of Rameau version: re-ordered/re-graded with the hook text, no captions (posting only on your OK).
Kling (Ralph 2026-10-30, shared 668-credit account): booked 80 credits max in Brain/Kling credits.md as a FALLBACK for S1 and S5 only, used only if their first take fails QC and only after your OK; 300 stay reserved for your other projects.
Time: ~25 min machine time plus your two review stops.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 6 x $0.09 | 0.54 |
| No-product clips, Seedance 2.0 Mini on Kie, 4 s | 2 x $0.164 | 0.328 |
| Product clips, Omni 1.1 Flash on Kie, 4 s (only if you skip Flow) | 4 x $0.315 | 1.26 |
| One likely redo (a still + an Omni clip), asked before it runs | $0.09 + $0.315 | 0.405 |
Expected spend with Flow for the 4 product clips (48 of your Flow credits): $0.96 (stills $0.54 + Seedance $0.33 + a still redo $0.09). With your Gemini app for the stills too: $0.33.
Kling: 0 planned; up to 80 credits (~2 clips) only as a fallback, asked first.
ElevenLabs: ~260 chars (Grace cloned v5).
Month so far (`python3 grace/spend.py`): KIE $232.27  OTHER $0.65  MONTH 2026-10 TOTAL $232.92 (no cap this month; from Nov 1 the $100 cap starts, and anything that runs then counts there).

TOTAL: $2.53

**Approve?**

## 7. Questions
1. Product clips: Flow in your app ($0, 48 credits) or Kie Omni ($1.26)?
2. Stills: Kie ($0.54) or your Gemini app ($0, I send a kit)?
3. Hand sheet without the bracelet (my pick for a bathroom) or with it?
4. On-screen hook text on Grace's version: no (default) or yes?
5. Product details above right (jar, lid, label, white tablets), and the facts we say (no whitening/enamel claims)?

## 8. Prompts (final, written with prompt-master after loading it; every reference named; linted MARKED_OK)
| Item | Model | Prompt file / text |
|---|---|---|
| 6 stills | Kie nano-banana-pro, 9:16 | prompts/still_S1..S6.txt (refs in shots.json still_refs) |
| 4 product clips | Omni 1.1 Flash (Flow kit or Kie), 4 s | prompts/clip_S1,S4,S5,S6.txt; image 1 = approved still, 2 = label, 3 = lid, 4 = sheet |
| 2 no-product clips | Seedance 2.0 Mini, reference mode, 4 s | prompts/clip_S2,S3.txt |
| Kling fallback (S1, S5 only, asked first) | Kling 3.0 turbo, image-to-video from the approved still, 5 s | prompts/kling_S1.txt, prompts/kling_S5.txt |
