# Label-drift bake-off, 2026-10-18 (Ralph's yes; $0.705 spent = quote)
Same start still (stills/S8.png) as first AND last frame, same prompt, 720p 9:16, no audio. Measured by modeltest/drift.py
(SIFT fit of the real printed label on every frame).

| Model (Kie id) | Cost | Label found | Jitter frame to frame (px, median / p95) | Drift vs frame 0 (px, median / max) | Print match (NCC) | Eye check (2x zoom) |
|---|---|---|---|---|---|---|
| Seedance 2.0 Mini (`bytedance/seedance-2-mini`) | $0.205 / 5 s | 121/121 | 1.11 / 3.23 | 2.7 / 6.8 | 0.896 | small print garbled |
| **Kling 3.0 Omni (`kling-3.0-omni/image-to-video`)** | $0.35 / 5 s | 121/121 | **0.49 / 1.24** | **0.9** / 4.8 | 0.906 | small print closest to readable |
| Veo 3.1 Lite (`veo-3-1`, veo3_lite) | $0.15 / 6 s | 144/144 | 0.70 / 3.43 | 1.7 / 4.8 | 0.911 | small print smudged |

Winner: Kling 3.0 Omni, about half the jitter of the others and the steadiest label. It outputs 716x1284: scale/crop to 720x1280 in the cut.
Seen in all three (from the old still, not the model): a soft grey glow around the pasted print. New stills: check the paste at 2x zoom.
