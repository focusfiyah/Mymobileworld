# Coach compare, cut r1 vs top winner (2026-10-12)
A = @thelyfeofky 7585057664544034079 (6.3M views), B = out/night_driving_glasses_r1.mp4. Tool output: research/coach/compare/compare.md + compare.png.
Words/sec computed free (A from TikTok's own captions, B from vo/words_trimmed.json; --stt not used, it costs credits).

| | A (winner) | B (ours) |
|---|---|---|
| length | 45.2s | 33.0s |
| words/sec | 3.58 | 3.74 |
| first spoken word | 2.3s | 0.05s |
| cuts | 1 (glare POV, then talking head) | 8 (one per line) |
| frame 0 | headlight-glare POV, no product | headlight glare behind the product on the dashboard (Ralph: product first) |

What it shows / fixed: same opener idea (glare POV) but ours shows the product from frame 0 and speaks at once, as Ralph asked. Pace is close
to the winner (3.74 vs 3.58 w/s), inside Grace's 3.0-3.6 range +0.14; no change made since every word is whole and pauses are already trimmed.
The S1 darken jump at 3.1s is covered by a white bloom on "goes white" (cut.py).
