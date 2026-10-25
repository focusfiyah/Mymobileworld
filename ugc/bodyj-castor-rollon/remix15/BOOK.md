# Production Book: BodyJ castor V3, grandma's hair longer (Grace), 2026-10-23

(The round-5 book, on hold since 2026-10-23, is `BOOK_r5_onhold.md`; rename it back to BOOK.md when Ralph restarts round 5.)

## 1. Job
- Client: Grace  Product: BodyJ4You castor oil roll-on (50 ml)  Video: V3 ("grandmama knew", 19 s), round 4 cut
- Ralph (2026-10-23, his words): "I want to adjust one for the videos with the grandma. Only thing is to make her hair much longer and keep the grayish hair and texture."
- Scope: ONLY shot R3 (3.86 s to 7.90 s, "But grandmama knew what she was doing..."). Every other V3 shot, the voice and the grade stay as in round 4.

## 2. Gate result
Script unchanged since round 2 (Grace's script word for word, `scripts.json`), voice `vo/v3.mp3` unchanged. `python3 ../../../grace/gate.py .` result in the plan message.

## 3. Script
Unchanged. V3: "Let's be real, castor oil doesn't smell like your favorite perfume. But grandmama knew what she was doing with this liquid gold for her hair, skin and nails. When I saw they made it into a roll-on, I had to get it. No pouring, no oily fingers, just roll it where you need it. I linked this one in the orange cart. You're welcome!"

## 4. Shot list (only what changes)
| Shot | Words | New picture | HAND / FREE | Product |
|---|---|---|---|---|
| R3 | But grandmama knew what she was doing with this liquid gold for her hair | Same shot as round 4 (from behind, roll-on on the part, lavender sweater, same room), hair now long: loose grey and salt-and-pepper coils past her shoulders down her back, same tight coily texture | HAND (grandma's own hands, not Grace's) | yes: Omni on Kie |

## 5. Order of work
Still edit (one item: the hair) -> QC at 2x (hair edges, hands, label) -> still to Ralph -> one Omni clip -> QC (2x edges, first second, label on several frames, no flicker) -> V3 re-cut free with the round-4 clips for every other shot (`cut.py 3 --final`, AI finish inside) -> qc.py, check.py, gate --stage cut, REMOVED.md -> review page, Drive (current V3 -> Older versions), email + push. About 35 minutes of machine time plus the still review stop.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| R3 still edit, Kie nano-banana-pro 1K (refs: round-4 R3 still, real front label, product sheet) | 1 x $0.09 | 0.09 |
| R3 clip, Kie google/gemini-omni-flash-1-1, 4 s, 720p | 1 x $0.315 | 0.315 |
| One likely redo (one still + one clip) | $0.09 + $0.315 | 0.405 |
| Flow trial take of R3 (standing rule, Ralph's Flow credits) | 1 x $0 | 0.00 |
| V3 re-cut, QC, Drive | free | 0.00 |
Kie balance now 771 credits = $3.86 (enough). Month so far (`python3 grace/spend.py`): $154.23 (no cap in October). This job so far: Kie ~$16.28.
$0 still option: you make the still in your Gemini app from my kit (R3 still + label + sheet + the prompt below); the total drops by $0.09 per still.

TOTAL: $0.81

## 7. Questions (all of them, now)
1. Length: past her shoulders down her back (my pick), or just to the shoulders?
2. Still: Kie ($0.09) or your Gemini app ($0)?
3. Flow trial on this clip (your standing rule): I also send you the kit to make R3 in Flow for free, side by side with the Kie take? (yes / skip)

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file |
|---|---|---|
| R3 still | Kie nano-banana-pro (Gemini 3 Pro Image), 9:16 1K | `r6hair/prompts/R3_still.txt` (refs on its last line: 1 round-4 R3 still, 2 real front label, 3 product sheet) |
| R3 clip | Kie google/gemini-omni-flash-1-1, 4 s (`omni_clip.py`) | `r6hair/prompts/R3_clip.txt`: image 1 the new still, 2 real front label `../refs/bottle_front.png`, 3 product sheet `../refs/ralph_sheet_bottle.jpg` |
