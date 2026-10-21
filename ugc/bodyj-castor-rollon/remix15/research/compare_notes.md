# Coach compare: the winner (7697844264050511135) vs the 4 finals (2026-10-21)
`tiktok.py compare` (no --stt; word timing measured from our own Whisper word files and the winner's TikTok captions).

| | Winner | V1 (script 2) | V2 (script 1) | V3 (script 4) | V4 (script 3) |
|---|---|---|---|---|---|
| Length | 31.8 s | 14.8 s | 15.8 s | 19.0 s | 15.5 s |
| Words/s | 3.3 | 3.3 | 3.3 | 3.4 | 3.2 |
| Cuts per 10 s | 2.5 | 4.1 | 3.8 | 3.7 | 4.5 |
| First frame | generic oil pour | the roll-on in hand | generic pour (same as winner) | roll-on alone on the counter | roll-on alone, push-in |
| First word | 0.1 s | 0.0 s | 0.0 s | 0.0 s | 0.0 s |

Same footage family and order logic as the winner (mess -> roll-on -> proof -> uses -> nightstand box). Faster cut rate because the same beats fit in half the time; no shot under 0.6 s.
Fixed after compare: nothing (the drift fix, cuts on exact frames, was made before this, found by qc.py sync).
- 2026-10-21 round 3 (all-new footage): compare re-run on the 4 new finals; cuts per 10 s above, same beats as the winner, every shot shows its line.
