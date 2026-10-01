# Handoff: Vicks VapoShower Plus ad (Grace), paused 2026-10-01

Paste into a new session:

> Continue the Vicks VapoShower ad for Grace. Read `ugc/vicks-vaposhower/HANDOFF.md` on branch `ccr-618f1cff-f9ivwb`
> of focusfiyah/Mymobileworld first.

## Where it lives
- Repo focusfiyah/Mymobileworld, **branch `ccr-618f1cff-f9ivwb`** (not merged to main). New session:
  `git fetch origin ccr-618f1cff-f9ivwb && git checkout ccr-618f1cff-f9ivwb`.
- Job folder `ugc/vicks-vaposhower/`: README (facts, cost plan, Status line), shots.json (script, prompts, windows),
  kie.py (stills/clips runner), par_stills.py (parallel stills), vo.py (voiceover + timings), cut.py (still the Plant
  Therapy copy: rewrite it for this job).
- Rules: `CLAUDE.md` + `grace/PLAYBOOK.md` (Ralph's working rules, the "Script = everything" rule, lessons).
- Setup in a fresh container: `pip install pillow requests` (Kie/ElevenLabs keys come from the proxy, never ask).
  The TikTok coach also needs `bash setup.sh` in focusfiyah/Dayone-ai (Playwright + proxy CA).

## Money
- Quote **$2.04**, spent **$0.97** (7 stills $0.63 + S4/S6 redo $0.18 + test clip S5 $0.16). Kie auto-refills below
  200 credits (Ralph). Ask before EVERY paid call, with the cost; report running total vs quote.
- **Next paid step, NOT yet approved:** the other 6 clips: S1 5s, S2 4s, S3 4s, S4 4s, S6 4s, S7 5s = 26s ×
  $0.041 = **$1.07** → total $2.04. Ask Ralph first. Command (background, Kie takes 3-8 min):
  `cd ugc/vicks-vaposhower && nohup python3 kie.py clips S1 S2 S3 S4 S6 S7 > preview/clips.log 2>&1 &`
  (wait on the python PID with `kill -0`, not `pgrep -f`: pgrep matches the wait loop itself).

## Decided (do not re-ask)
- Hands only, same hand as Carpe/Plant Therapy (short squared lilac-white nails), unwrapped white disc tablet, one
  12-count box, no price in the ad ($29.49 for one box ≈ $2.46/shower: not a selling point).
- Script v3 (humanized), approved. Built from: coach data (top shower-steamer TikToks: JojoWell 879k "each pack comes
  with six", bundle video 173k "you get 18 tablets", stocking-stuffer gifting), sales psychology (pain/moment hook,
  specificity, how-to, honest caveat, count + gift close), box wording, Grace structure, humanizer, readability 3.3.
- CTA sells more units (count + gift), not the old detached CTA. Caveat = non-medicated.
- Hook text on S1 (free, in the cut): **"the only 10 min you get to yourself 🚿"**.
- Voiceover done: Grace B, `vo/voiceover_tight.mp3`, 24.7s, word times `vo/words_trimmed.json`.

| Shot | Window (s) | VO | Picture |
|---|---|---|---|
| S1 | 0.00–4.94 | Your shower's probably the only ten minutes you get to yourself, so make it smell like Vicks. | hand holds box up, steamy shower behind + hook text |
| S2 | 4.94–8.98 | Eucalyptus and essential oils, plus that menthol and camphor scent. | hand lifts tablet from open box (window 4.04s > 4s clip: hold last frame 1 frame) |
| S3 | 8.98–12.44 | The Plus has ten percent more of that blend than the regular ones. | tablet in palm + `inserts/banner.png` pop-up at "ten percent more" (9.87s) |
| S4 | 12.44–15.00 | Drop one on the shower floor, right where the water hits, | hand sets tablet on grey shower floor (v2 still) |
| S5 | 15.00–16.64 | and the steam fills up with it. | **clips/S5.mp4 done: use 0.1–1.75s only** (pale hands enter at 2.2s) |
| S6 | 16.64–20.42 | It's non-medicated, so it's just for the smell. It won't treat a cold. | hand at the steamy glass door (v2 still, no box) |
| S7 | 20.42–24.71 | Twelve in a box, so grab one for you and one to gift. It's in the orange cart. | box on counter, hand taps it, two fingers, points down |

## After the clips (all free)
1. QC every clip frame by frame (contact sheet with timestamps): same hand/nails, box never morphs or crops, no stray
   hands/people, clips ≥1.0x (never stretch; use still-hold push-ins from a clip's frame if a window runs long).
   Seedance redraws scenes late in a clip: prefer each clip's first ~2s. Ask before any redo (~$0.16–0.21 each).
2. Rewrite `cut.py` for this job (Plant Therapy's has the clip/hold PIECES pattern): 720x1280 24fps, windows above,
   hook text bubble on S1, banner pop-up on S3, CC0 SFX (copy `../plant-therapy-top6/sfx/`, add water/fizz only if
   CC0), loudnorm -16 LUFS → `out/vicks_vaposhower.mp4`.
3. Coach compare: `python3 .claude/skills/tiktok-shop-coach/scripts/tiktok.py compare
   https://www.tiktok.com/@momwifelifestyletts/video/7594493710100958495 ugc/vicks-vaposhower/out/vicks_vaposhower.mp4
   --out <scratchpad>/tt` and fix what it flags, before Ralph sees it.
4. SendUserFile the cut + PushNotification (one line: what to review + spent vs quote). Update README Status line,
   CLAUDE.md Jobs line, and add a results line to `grace/PLAYBOOK.md` §7. Commit + push this branch.
