# Clip check calibration (2026-10-26)

Why: Kie bills any task that returns a video, even one that ignored the input image (Sabrina Ramonov's /generate email,
2026-08-19: her first clip came back as a random landscape and was charged). `grace/clip_check.py` compares the
opening second of every paid clip with the still it was made from.

Data: 242 real pairs on disk (`ugc/*/stills/SID.png` + `ugc/*/clips/SID.mp4`, 28 jobs), the same 242 clips paired
with a random still from ANOTHER job (what "ignored my image" looks like), and a same-job other-shot set (info only).
Run: `python3 tools/clipcheck/calibrate.py` (6m45s on 4 cores), scores in `scores.json`.

| set | n | min | p5 | median | max |
|---|---|---|---|---|---|
| real pairs | 242 | 0.089 | 0.498 | 0.948 | 0.990 |
| other job's still | 242 | 0.003 | 0.057 | 0.195 | 0.564 |
| same job, other shot | 242 | 0.075 | 0.117 | 0.314 | 0.966 |

| threshold | real pairs flagged | mismatches caught |
|---|---|---|
| 0.45 | 11 | 238 / 242 |
| **0.50 (chosen)** | 13 | 241 / 242 |
| 0.55 | 16 | 241 / 242 |
| 0.60 | 19 | 242 / 242 |

The 13 lowest "real pairs" (`lowest_real_pairs.jpg`, still left, clip frame right): 9 are clips made from a different
or older still than the one now in `stills/` (FUSOU V1 day still vs night clips, JIYU S3 redone, Carpe MB, Turmeric
S4, Flashlight S7), so the flag was right; 4 are real pairs with a strong camera move (Shnuggle R2-02 0.47, Cleanwaste
V1S2 0.50, JIYU S2 0.43, Flashlight V2 S7 0.43). A FAIL means "look before it goes anywhere", not "pay again".
The one mismatch above 0.50 was two bathrooms (Shnuggle R1-02 still vs Carpe MB 15s S4, 0.56).
