# Round 5 free check (2026-10-23): round-4 cuts vs Grace's real hand sheet

Source: the 4 round-4 cuts pulled from the review page; 3 frames per shot (start/mid/end) next to
grace/ref/hand-sheets/without_bracelet.jpg: `qc/r5/r4_v{1..4}_shots.jpg` (`shots_sheet.py`); hand-entry strips for the
box shots `qc/r5/strips_boxshots.jpg` (`strip.py`).

Grace's sheet: medium-brown skin, long nude nails with white French tips, crown-stack + heart ring, blue band on the thumb.
Round 4 prompt said "short natural nude nails, no rings" with an old AI hand crop as the ref: NO hand shot has her nails or rings.

## Headless (Ralph: "v1 it shows a head missing")
- V1g elbow: arm raised, torso and shoulder in frame, no head.
- V1h hair ends: hair over the shoulder, torso in frame, head cut off at the top.
- Same look, not flagged by Ralph: V3f (neck/collarbone, cut at the jaw), V4d4 (hair ends held in front of the torso).

## Skin tone off Grace's sheet
- Clearly wrong (pale white hands): V1i (enters at 1.0 s), V2b (whole shot), V2h (enters at 0.5 s), V3g (enters at 1.9 s), V4b (whole shot), V4f (enters at 2.25 s).
  These were all HAND-FREE shots: Seedance added a hand the prompt never asked for.
- Lighter / golden vs the sheet: V1b, V1c, V2a, V2e (face lighter).
- Close-ish tone but wrong nails, no rings, varies shot to shot: V1d, V1f, V1g, V1h, V2c, V2d, V2f, V3c, V3d, V3e, V3f, V4c, V4d2, V4d3, V4d4, V4e.
- Brow shots show three different women's faces: V1e (darker), V2e (lighter), V4d1.
- OK as is: V1a, V3a, V4a, V4a2 (no hands), R3 (grandma's hands, meant to differ).

## Redo list (proposed)
- Full redo (new still + clip, Grace's hand sheet as a ref): V1b V1c V1d V1e V1f V1g V1h · V2a V2c V2d V2e V2f · V3c V3d V3e V3f · V4c V4d1 V4d2 V4d3 V4d4 V4e = 22 shots.
- Clip only (the still is hand-free and fine; re-run with "no hands anywhere"): V2b V2h V4b = 3.
- Free fix (cut before the hand enters, forward-then-back push so it still moves, no freeze): V1i V3g V4f = 3.
