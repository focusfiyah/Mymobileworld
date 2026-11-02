# Production Book: Buttah Silky Soft Towels (24 ct) for Grace, V1 music-only

Sent to Ralph: https://claude.ai/artifact/5FBDUgNhzcj7ibWFnTSao9 (2026-11-02)

## 1. Job
- Client: Grace. Product: buttah. Silky Soft Towels, 24 count travel soft pack (XL disposable face cleansing towels). Route: product lock, `ugc-product-ad` references/product-lock.md (Omni on Kie for product shots, Seedance 2.0 Mini for the one no-product shot; Ralph picked Kie 2026-11-02).
- Job folder: `ugc/buttah-silky-towels/`  Target length: ~16 s  Shots: 7 (4 HAND, 3 HAND-FREE). Music only, no VO in our cut; Ralph adds music. Script below is for Grace to voice or caption later, every shot timed to its line.

## 2. Gate result (`python3 grace/gate.py ugc/buttah-silky-towels`)
| Proof | File | Result |
|---|---|---|
| Playbook rules read | research/playbook.md | done |
| Coach research (shop/discover + video x3) | research/coach.md, shop/, discover/, videos/ x3 | done (hashtag pages #disposablefacetowels and #facetowels returned 0 videos, tried twice) |
| Daily viral board | research/viral/viral-2026-11-02.json | ran twice, 0 shop videos returned (TikTok hashtag scans came back empty today) |
| Product facts (source) | research/product_facts.md (buttahskin.com) | done |
| Hooks modeled on named winners | research/hooks.md (H006 picked, H147, H010) | done |
| Humanizer | research/humanizer.md, captions.md | done |
| Readability (grade) | research/readability_v1.txt | grade 1.9 |
| Banned-phrase check | gate.py | GATE OK (2026-11-02) |

## 3. Script (final, Humanized)
1. Hook (H006): You won't know how much your washcloth bugs you until you stop using it.
2. Pain: It sits damp all week, then goes back on your face.
3. Solution: These are big, soft, and you use each one once.
4. Sell-side confession: Only downside? You'll want a pack in every bag.
5. Real urgency: Holiday travel's coming, so grab a few.
6. Close: It's in the orange cart.
56 words, about 16 s at Grace's pace. No price, no "order it now", only our product. On-screen text: none (hook text options in research/hooks.md, only on your yes).
Source of each line: research/line_sources.md (H006 + @mayahome02 637.9K switch angle; brand "Your washcloth is working against you"; listing XL 11.875 x 10.875 in, silky soft, single-use, travel soft pack; PLAYBOOK confession pattern; real holiday travel season).

## 4. Shot list
| # | Window (s) | Words | Shot | HAND? | Model | Room (real photo) |
|---|---|---|---|---|---|---|
| S1 | 0.0-2.6 | hook | Pouch flat on the vanity, stack of folded towels; Grace's hand pinches and lifts the top towel | HAND | Omni 4 s | bath_A (white vanity, gold faucet) |
| S2 | 2.6-5.0 | pain | Old damp grey washcloth on the hook by the sink, one drop falls, dolly in | HAND-FREE | Seedance Mini 4 s | towel_bar |
| S3 | 5.0-6.6 | "big, soft" | One towel hangs open full size from her pinch, small shake | HAND | Omni 4 s | bath_B_teal (wood vanity, teal tiles) |
| S4 | 6.6-8.2 | "use each one once" | Towel wet under the running tap, one squeeze | HAND | Omni 4 s | bath_A sink |
| S5 | 8.2-10.8 | confession | Hand slides the pouch into a beige tote on a teal bed | HAND | Omni 4 s | bedroom_teal |
| S6 | 10.8-13.4 | holiday travel | Pouch on top of a packed carry-on on a hotel bed, push-in | HAND-FREE | Omni 4 s | hotel |
| S7 | 13.4-16.0 | orange cart | ONE pouch standing on the vanity beside a towel stack, dolly in | HAND-FREE | Omni 4 s | bath_B_teal |
No face in any shot (no lip sync needed). Outfit: n/a, hands only. Nails / person: Grace's hand sheet (French tips, her rings; with or without bracelet = question 1).
Real product confirmed from the brand's photos (refs/product_sheet.png, product_truth.json): soft flat pouch, mint-teal glossy edges, black front, 'buttah.' white serif, 'Silky Soft Towels' teal with italic 'Towels', window strip, 3 badges, 'THE WASHCLOTH UPGRADE / LARGE | SINGLE-USE | DRY OR WET / 24 COUNT'; plain white waffle towels, 11.875 x 10.875 in open. No shot pulls a towel out of the pouch (no listing photo shows how it opens).

## 5. Order of work
Stills first, all 7 at once ($0.63), storyboard on the review page for your look (QC at 2x: print letter for letter, grip, size vs the hand, 3 badges, no lid). Then ONE test clip: S5 (riskiest: hand + moving pouch + print), then the other 6 at once. Cut to the line windows, QC (flash, levels, drift, every frame of the print), AI finish last, silent master for your music. Then a House of Rameau version ($0, own order and grade, on-screen hook text, no captions) only on your yes.
Free fixes planned: crop, retime, colour match; a small print wobble is fixed by framing, not a redo.
Time: about 35-40 min of machine time after your OK, plus your two review stops (storyboard, cut).

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills (Gemini 3 Pro Image = nano-banana-pro on Kie) | 7 x 0.09 | 0.63 |
| Omni 1.1 Flash 4 s clips on Kie | 6 x 0.315 | 1.89 |
| Seedance 2.0 Mini 4 s (S2, no product) | 1 x 0.164 | 0.164 |
| One likely redo (1 still + 1 Omni clip), asked before it runs | 1 | 0.405 |
Total Kie: $2.69 + $0.41 redo allowance  ElevenLabs: 0 chars (no VO)  Contingency redos beyond that (each asked separately): $0.315 per Omni clip
Month so far (`python3 grace/spend.py`): $1.32 of the $100 November cap

TOTAL: $3.09

**Approve?**

## 7. Questions (all of them, now)
1. Grace's hand sheet for this video: WITH the gold bracelet or WITHOUT?
2. Pouch size: the brand does not give it; I estimated about 17 x 15 cm (a little wider than her hand) from the brand's in-hand photo. OK, or can Grace measure hers?
3. House of Rameau version after V1 ($0 re-cut with on-screen hook text): yes or no?

## 8. Prompts (final, written with prompt-master; every reference named; all 14 pass grace/prompt_check.py lint)
| Item | Model | Prompt file |
|---|---|---|
| Stills S1-S7 | nano-banana-pro (Kie) | prompts/still_S1.txt ... still_S7.txt (full text on the review page) |
| Clips S1, S3-S7 | google/gemini-omni-flash-1-1 (Kie) | prompts/S1.txt, S3.txt ... S7.txt |
| Clip S2 | bytedance/seedance-2-mini (Kie), first frame = approved still | prompts/S2_seedance.txt |
References per shot: prompts/refs.json (product sheet, logo close-up, badge close-up, real pouch front, real room photo, Grace's hand sheet).
