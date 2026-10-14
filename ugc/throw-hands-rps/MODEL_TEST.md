# Video model test on Throw Hands (Ralph 2026-10-14)

Ralph asked to look at Seedance 2.0 / 2.0 Fast, Vidu Q3 Turbo and Hailuo 02 Pro / 2.3 Standard, and to use this ad as the test.
Status: research done, runner `modelfight.py` ready, **no money spent; waiting on Ralph's OK for the test cost.**

## What each one costs and can do (Kie's own price table, read 2026-10-14 from api.kie.ai/client/v1/model-pricing/page)
| Model | On Kie? | Price, silent, 720p-ish | One 5-6s clip | Notes |
|---|---|---|---|---|
| Seedance 2.0 Mini (our default) | yes `bytedance/seedance-2-mini` | $0.041/s 720p | $0.205 (5s) | 4-15s, first + last frame, 9:16 |
| Seedance 2.0 Fast | yes `bytedance/seedance-2-fast` | $0.124/s 720p (480p $0.059/s) | $0.62 (5s) | same inputs as Mini, 3x the price |
| Seedance 2.0 | yes `bytedance/seedance-2` | $0.205/s 720p, $0.51/s 1080p | $1.025 (5s) | 5x Mini; Ralph called it too costly 2026-09-19 |
| Hailuo 2.3 Standard | yes `hailuo/2-3-image-to-video-standard` | $0.15 per 6s 768p, $0.25 per 10s | $0.15 (6s) | only 6 or 10s, no aspect setting (follows the still), no last frame |
| Hailuo 02 Pro | yes `hailuo/02-image-to-video-pro` | $0.285 per 6s, 1080p only | $0.285 (6s) | fixed 6s 1080p, end frame allowed, prompt max 1,500 chars |
| Vidu Q3 Turbo | **no** (Kie only has Vidu Q4) | Vidu's own API $0.06/s 720p, Replicate $0.06/s | ~$0.30 (5s) | needs a new Vidu or Replicate account + key; tested 2026-10-14: api.vidu.com and api.replicate.com reachable, both refuse without a key (400/401) |
| (stand-in) Vidu Q4 | yes | $0.076/s 720p | $0.38 (5s) | the Vidu model we can run today |

Cheapest per clip: Hailuo 2.3 Standard ($0.15 for 6s, cheaper than Mini's $0.246 for 6s). Most expensive: Seedance 2.0 full.

## The test (one shot, every model, same input)
- Shot **S4**, the riskiest one in the plan: straight overhead, four players' hands slam real Throw Hands cards at the same time.
  It stresses what breaks most: many hands, fast motion, card symbols that must stay fist / flat hand / peace sign.
- One still first (Nano Banana Pro on Kie, $0.09), QC'd at full size before any clip. That still is also the ad's S4 still, so nothing is wasted.
- Same motion prompt to every model, audio off: `python3 modelfight.py S4` → `fight/S4_<model>.mp4` + `preview/fight_S4.png` (frames per model, one row each).
- Scored per model on: card symbols stay right, hand count/fingers/wrists, flicker/shimmer, real speed (not slow-mo), 2x edge zoom (halo/smear), prompt followed, render time, cost.
- The winning clip becomes the ad's S4, and the winner becomes the model for the other 8 clips (new total before any spend).

## Cost of the test
| Item | Cost |
|---|---|
| S4 still | $0.09 |
| Seedance 2.0 Mini 5s | $0.205 |
| Seedance 2.0 Fast 5s | $0.62 |
| Seedance 2.0 5s | $1.025 |
| Hailuo 2.3 Standard 6s | $0.15 |
| Hailuo 02 Pro 6s | $0.285 |
| **Total (Kie)** | **$2.375** (balance $7.75) |
| optional: Vidu Q4 5s as the Vidu stand-in | +$0.38 |
| optional: Vidu Q3 Turbo itself | ~$0.30 + a Vidu/Replicate account Ralph would have to open |

Kie charges $0 for failed tasks. A redo of any clip gets its own price and Ralph's OK first.
