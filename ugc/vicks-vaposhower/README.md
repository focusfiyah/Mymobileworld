# Vicks VapoShower Plus: hands-only UGC video

**Client: Grace** (Ralph, 2026-10-01). Hands-only route (`ugc-product-ad` skill), template `../plant-therapy-top6/`.
Rules: `grace/PLAYBOOK.md`. One video, 9:16, ~22s, 7 shots, voiceover ElevenLabs **Grace B** (`bGrsdLmwBbYUgHRuMFOI`,
eleven_v4). Shots, prompts and windows: `shots.json` (windows are estimates until the voiceover's word timings).

Status: **Script v2 APPROVED 2026-10-01 (coach data + psychology + Grace structure; CTA = count + gift; one box, no price). Voiceover v2 25.75s done. Stills S2/S3/S6/S7 rendering, then S4/S5 (need S3). Next: still sheet to Ralph, then test clip S5 ($0.16). S2 and S7 windows (5.5s) run past their clips: free still-hold push-in in the cut. Spent $0.09 / $1.86 (+$0.54 for stills in flight).**

## Product facts (Vicks box + vicks.com, 2026-10-01)

| Fact | Source |
|---|---|
| 12 shower tablets per box | box front, vicks.com |
| "10% MORE SOOTHING VAPORS*", footnote "*vs. VapoShower" = "10% more of our proprietary blend of eucalyptus and essential oils + scents of menthol & camphor" | box front, vicks.com |
| "Infuses with Shower Steam", "Dissolves Cleanly", "Non-Medicated" | box front |
| Directions: "Place on shower floor in direct stream of water and continue running shower until completely dissolved." | vicks.com / retailers |
| Not intended to treat cold or flu symptoms | vicks.com |
| "CAUTION: HARMFUL IF SWALLOWED OR PUT IN MOUTH. Keep out of reach of children. Keep away from eyes." | box front + back panel |
| TikTok Shop (Grace's screenshot): $29.49, free shipping, 5.0★ (5), 10 sold | refs/tiktok_listing.jpg |

Not said on purpose: any cold/flu/sinus/breathing/congestion relief (it's non-medicated), "sauna"/"spa" health
claims, any personal-use line, the review count (5 reviews is too thin for social proof), price (pack size unconfirmed).
Caption disclosure: `#ad`.

## Script (75 words, ~22s at 3.3 words/s)
Structure: hook → what's in it → claim (box wording) → how to use → honest caveat → detached CTA.

| Shot | VO | Picture |
|---|---|---|
| S1 hook | Love the smell of Vicks? Put one of these in your shower. | hand holds the box up at the bathroom counter, shower steaming behind |
| S2 | Eucalyptus and essential oils, plus menthol and camphor scents. | hand lifts a white tablet out of the open box |
| S3 | The Plus has ten percent more of that blend than the original. | tablet in the palm; free pop-up of the box's red "10% MORE…*vs. VapoShower" banner |
| S4 | Set it on the shower floor, right in the stream. | hand sets the tablet on the wet shower floor under the water |
| S5 | It dissolves and infuses the steam. | tablet fizzing, steam rising, no hand (test clip) |
| S6 caveat | Just know it's non-medicated. It's for the scent, not a cold remedy. | fingertips wipe a streak in the fogged glass door |
| S7 CTA | Not a Vicks person? Skip this. If you are, it's in the orange cart. | box on the counter, open palm "up to you", points down |

Setting: bright white-tile bathroom, glass walk-in shower, chrome rain head, grey stone floor, white counter, window
light. Hands only (same hand as Carpe/Plant Therapy, short squared lilac-white nails). No face anywhere → no lip sync.

## Cost plan
| Step | Cost |
|---|---|
| Voiceover (~400 chars, Grace B) + word timings | ElevenLabs plan characters |
| Still S1 (check hand + box + bathroom) → stop for review | $0.09 |
| Stills S2–S7 (S3 before S4/S5: it's their tablet ref) → one sheet, stop for review | $0.54 |
| Test clip S5 (fizz + steam, hardest) → stop for review | $0.16 |
| Other 6 clips (24s × $0.041; S7 cut to 4s once the VO came in at 21.6s) | $0.98 |
| Cut: banner pop-up from the real packshot, CC0 SFX (water, fizz), loudnorm | free |
| **Total** | **$1.78** (+ ~$0.25 per redone shot; each redo asked first) |

Running total: $0.09 / $1.78 (S1 still).

## Files
- `kie.py`: runner (box text + box refs left out of S4/S5; S3 still is their tablet ref).
- `cut.py`: copied from Plant Therapy, rewrite the PIECES/inserts for this job after the clips are in.
- `refs/`: Vicks packshots (front/left/right, vicks.com), hand refs, Grace's listing screenshot.
