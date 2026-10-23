# Compare: cut r1 vs the top winner (2026-10-23)

`tiktok.py compare` A = @zin5bamu 7674078707387993375 (13.7M views, 2-in-1 flashlight power bank), B = out/flashlight_v2_r1.mp4.
Output: research/compare_r1/compare/compare.md + compare.png. B's words come from our own STT (vo/stt.json, scribe_v2), not re-billed.

| | Winner | Ours r1 |
|---|---|---|
| Length | 30.4 s | 22.6 s |
| Words/s | 2.66 | 3.8 (84 words in 22.1 s) |
| Cuts per 10 s | 4.9 | 3.5 (8 cuts) |
| First word | 1.2 s | 0.05 s |
| Light on at frame 0 | yes | yes (S1 panel lit) |

What we kept from the winner: product working in the first frame (lit panel), POV beam on a dark trail (S4), one spec per line.
What differs on purpose: Ralph's script word for word (faster, shorter); one shot per line, so fewer cuts than the winner.
Fixed in this round: segments rounded up to whole 24 fps frames and drifted 0.25 s late by S9; each segment is now trimmed
to its exact window after the 30 fps conversion (cuts land within 2 frames of the voice windows).
REMOVED.md checked: no button-by-clip layout, no gunmetal, no McDonald's on screen, flicker from the front lens with the
side panel off, no text, real layout (ports under the cap, power-symbol button, SMILING SHARK) in every shot.
