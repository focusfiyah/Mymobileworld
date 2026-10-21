# Footage inventory for the 15 s remixes (2026-10-20, free prep)

All clips: 720x1280, 24 fps, 5.04 s each, in `../clips/` (AI label) and `../clips_label/` (real label tracked
back on: S1 S5 S7 S8 S9 N4). Sheet of each clip at 0.3 / 2.5 / 4.7 s: `inventory_sheet.png`.
Rule: every clip at 1.0x, never stretched; a clip can be reused from a different start (unused tails).

| Clip | What moves | Setting | Real label | Used in winner (posted) at |
|---|---|---|---|---|
| S3 | glass bottle pours thick oil into a cupped hand, it runs off; hands rub | sage bathroom, marble | n/a (no BodyJ) | 0.0-4.4 (hook "thick and messy") |
| N1 | oil drips through both hands onto the counter, tipped bottle, puddle | sage bathroom | n/a | 4.4-9.1 (pain, "dripping") |
| N2 | hand lifts the dropper from a glass oil bottle | marble counter | n/a | 9.1-13.4 ("the smell") |
| S1 | hand picks the roll-on up off the counter, turns it to camera | sage bathroom | yes | 13.4-17.1 ("liquid gold") |
| S4 | rolls the roller across the back of the hand on a towel | sage bathroom | AI only (small/turned) | 17.1-20.9 ("no pouring, no oily fingers") |
| S8 | bottle alone on the counter, camera pushes in to the label | sage bathroom | yes | 20.9-24.8 ("USDA organic") |
| S5 | rolls the roller along a scalp part, coily hair | bedroom | yes | 24.8-28.1 ("rose quartz roller") |
| S9 | hand lifts the roll-on beside the Gemstone Roller box, nightstand | bedroom, lamp | yes | 28.1-30.7 ("orange cart") |
| S7 | rolls down the length of a braid | bedroom | yes | ~30.7-31.8 (hair line; matched from the sheet) |
| S6 | rolls the inner elbow | bedroom | AI only | not in posted cut (v2g "moisturized skin") |
| N3 | rolls along the brow, eyes closed (face: lips cropped out in v2g) | bedroom | AI only | not in posted cut (v2g "brows") |
| N4 | rolls the cuticles, hand on a towel | bathroom counter | yes | not in posted cut (v2g "cuticles") |

## The winner's shot map (measured)
`ref/7697844264050511135/video.mp4` (pulled 2026-10-20 with `tiktok.py video`, 31.8 s, 720x1280, 1,645 views,
promoted). Scene cuts (ffmpeg scdet): 4.43, 9.10, 13.43, 17.13, 20.87, 24.83, 28.07, 30.67 s. Frame matching
against our clips (`match.py` style, mse on 36x64 grey) shows Grace posted our v2g footage in the same order,
re-timed to HER own voice, with the comment sticker "I think we all need castor oil" on top and the brows,
cuticles and elbow shots dropped. Her timed captions: `ref/7697844264050511135/transcript_timed.txt`.

## What 15 s means here
The winner's first 15 s ends at "Freaking ingenious" (14.6 s): hook + pain + smell + liquid gold + the roll-on.
The proof ("no pouring, no oily fingers") lands at 14.6-16.6 s, so a 15 s version has to move it earlier or
merge it with the reveal. At her measured pace (106 words / 31.8 s = 3.3 words/s, pauses included) a 15 s script is ~45-50 words.
