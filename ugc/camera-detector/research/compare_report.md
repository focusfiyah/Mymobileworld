# Compare, cut v1 vs the top same-product winner (2026-10-29)
A = @lism792 173.4K (same detector, white), B = out/camera_detector_v1.mp4. `tiktok.py compare` (no --stt: our words come from vo/words_trimmed.json, free).

| | A | B |
|---|---|---|
| length | 36.5 s | 33.3 s |
| words / speed | 151, 4.14 w/s | 129, 3.94 w/s (vo/words_trimmed.json) |
| cuts | 3 (0.8 per 10 s) | 9 (2.7 per 10 s, Grace's edit style: one clip per line) |
| first word | 0.0 s | 0.05 s |
| frame 0 | bathroom ceiling, no product yet | the detector in her hand in a hotel bathroom |

What it shows: our pace matches the winner (a touch slower, Grace's voice), our product is on screen from frame 0 where A shows it at 2 s, and we cut 3x as often, which suits a 33 s ad. A claims "give an alarm when it recognizes an infrared light source"; we don't (REMOVED.md). Fixed: nothing needed.
