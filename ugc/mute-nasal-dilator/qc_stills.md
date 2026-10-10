# Still QC (2026-10-08)
S1 ok (back of a head far in the background, no face; hand on pillow). S2 ok (earplugs, plain tape, open drawer). S3 ok (box exact: mu:te, flag, window, STARTER PACK, RHINOMED). S4 ok (tray card + 3 dilators match refs). S5 ok for test (U-loop dilator with ribbed stent, hand from the left edge, wrist not shown). S6 ok. S7 FAIL: box front shows a white clip in the window instead of the nose picture, no "fully adjustable" ring, boxes squat; redo only on Ralph's yes ($0.09).
Spent: 7 stills $0.63 + nose preview $0.09 = $0.72.
S7 redone (single box, Ralph 2026-10-08): box exact (mu:te, flag, nose-picture window, ring text, STARTER PACK, RHINOMED), hand from the left edge. OK. Old two-box still in old/.
S5 test clip (6.04s, 720x1280, $0.246): lots of motion, hand/rings/nails consistent, tray consistent. FLAG: the dilator bends into an S/squiggle from ~1s and one stent is hidden behind the fingertip, so it no longer reads as the real symmetric U with two stents. Frames 1-4 (first ~1.5s) are closest to the real shape.
Spent: stills $0.72 + S7 redo $0.09 + S5 clip $0.246 = $1.056 of the $2.40 cap.

## Cut r1 QC (2026-10-10)
qc/verify.py: flash OK (only the 7 joins + the S6 lamp switch), sync OK (34.83s vs VO 34.85s), every clip >= window at 1.0x, levels -16.3 LUFS peak -2.8, no text overlay. Gate --stage cut: GATE OK. Coach compare vs @joybreath.sleep: research/compare_report.md.
Free fix applied: real box print pasted over the AI box in S3, S4, S7 (boxfix.py, per-frame homography, skin kept in front): the AI's garbled "SMORR LESS" etc is gone from the box front.
KNOWN FLAWS left (need paid redo or Ralph's call): (1) S4 second half: the purple tray card carries invented text "BREATHE MORE / SMAR LESS / SLEEP BETTER" and the box window below shows an AI clip graphic; (2) S5 dilator bends into an S-curve after ~1s, one stent hidden (Ralph's option A trim was not possible: only 29.6s of clean footage for a 34.8s VO); (3) S3 first 0.6s box rotates with garbled flap text; (4) S6 empty tray prop is lilac, not the real dark purple tray.
Kie total $2.286 of the $2.40 cap (9 stills, 36s of clips); ElevenLabs 627 chars.
