---
name: kinetic-film
description: Makes fast, high-energy kinetic typography films in code (huge words on every beat, whip pans, colour flips, 3D letters the camera flies through, a hard drop) for a launch film, promo, teaser, trailer, channel intro, Shorts/Reels hook or brand sting: one web page assembled from scene blocks on the music's beat grid, rendered at 1080p or 4K with real motion blur, and checked frame by frame for stillness, holds, cuts and playback. Free only (code motion, a numpy sound kit, free music); Scenario's paid MCP is not used. Use when Ralph says motion graphics, kinetic type, kinetic film, Higgsfield Katana, "like this motion reel", beat-synced text video, hype intro or launch video. For general HTML video compositions, captions or edits use hyperframes; for a launch video from a repo or URL use brag-slim; for Grace's product footage use ugc-product-ad.
---

# Kinetic films in code

## Goal

A film that reads as professional motion design, not a slideshow: something moves every frame, a cut or
colour flip lands every 0.3 to 0.7 s on the music, and every word is exactly the word written. The film is
a spec (scene blocks on a beat grid, a palette, captions, a logo); the engine turns it into one web page
where each frame is a pure function of time, so the renderer can seek anywhere and average sub-frames into
real motion blur. Nothing in the motion is AI-generated, so changing one colour rebrands the film.

Done looks like: `finish.py` prints PASS on every gate (still share, longest hold, cuts per 10 s, size,
playback) for the delivered file, stills at the key beats were looked at, and the soundtrack was listened to.

Source: Scenario's "Kinetic Film" skill (@emmanuel_2m, Scenario co-founder, on X 2026-10-28: "R.I.P. Higgsfield Katana. I
reverse engineered it and made a Claude motion design skill that replaces it."); provenance, licence and scan in [SOURCE.md](SOURCE.md).

## Ralph's route (free first)

- **Motion: $0.** Renders on the machine. Cloud box (4 cores, no GPU, 2026-10-29): a review render takes ~0.9 s
  per frame with `--workers 2` (the default picks 1 worker on 4 cores), so ~13 min per 15 s at 60 fps; it measures
  the same as full quality, so run every check on review renders and render full quality once (SOURCE.md "Test render").
- **The starter alone does not pass `finish.py`** (42% still, median motion 2.03 after the retime): a real film needs
  more moving blocks than the template's five; plan them in the beat sheet before rendering.
- **Sound kit: $0.** `python3 $K/scripts/synth_kit.py <film> --keys /home/user/Dayone-ai/assets/sfx` writes
  the 12 core sounds mix.py needs (numpy-made whooshes, impacts, riser, logo hit) plus real CC0 key clicks.
  A better free sound dropped into `audio/sfx/` under the same name wins (free-assets skill: Pixabay, Mixkit).
- **Music: $0 first.** A free track from the free-assets skill (licence checked for monetized use), measured
  with `beat_grid.py` and the film's `bpm` set to what it measures. Or `mix.py --no-music` for effects only.
- **No Scenario MCP, no paid steps.** Why: Ralph 2026-10-29, "No paid anything on this just use the free
  resources we already have". The upstream's Scenario music, sound kit and key art are replaced by the free
  routes above; pictures come from free-assets or real product photos. The Scenario references stay only as the
  upstream's record ([references/scenario-mcp.md](references/scenario-mcp.md), [references/worked-example.md](references/worked-example.md)).
- **Ralph's video rules still apply** (Mymobileworld CLAUDE.md): a hook on screen is whole and readable in
  frame 0 and held 2 s+ (so for a hook video drop the starter's `charge` opener and put the first shot at beat
  0; check with `tools/hookcheck/hook_check.py`); Grace's TikToks carry on-screen text only on his yes, House of
  Rameau versions keep it; Day One AI keeps its own look rules (day-one-ai skill). Code-made films are not AI
  video, so the AI finish step does not apply.
- **9:16:** `finish.py` makes a vertical copy with the 16:9 film centred on black. A native 9:16 stage is not
  built yet; say so before promising a full-frame vertical.

## Quick reference

Needs Node 18+ with Playwright (the cloud box has a global install and Chromium at `/opt/pw-browsers`: set
`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`), ffmpeg, Python 3 with `numpy` and `opencv-python-headless`.

`$K` is this skill's folder.

```bash
sh $K/scripts/new_film.sh my-film starter        # engine + an editable spec.js + fonts + audio/ folder
cd my-film && npm install playwright             # once per folder
python3 -m http.server 5671                       # preview: http://127.0.0.1:5671  (space plays, arrows step one beat)
node $K/scripts/snap.mjs stills 0.5 b4 b12 b20    # stills at beats (or seconds) to look at
python3 $K/scripts/beat_grid.py audio/music.mp3 --bpm 172 --window 40   # tempo, downbeat offset, drops
python3 $K/scripts/mix.py .                       # the soundtrack, from the film's own cue list -> out/mix.wav
python3 $K/scripts/render.py . --res 1080         # check render; workers sized to the machine's memory
python3 $K/scripts/finish.py . --video out/video_1080.mp4 --audio out/mix.wav   # deliverables + every check
python3 $K/scripts/render.py . --res 4k && python3 $K/scripts/finish.py . --video out/video_4k.mp4 --audio out/mix.wav
```

| Rule | Why |
| --- | --- |
| Everything is in beats: blocks, shots, captions, cues. `B(k)` = k beats in seconds | cuts land on the music; one tempo change retimes the film |
| One idea per beat or half beat; one or two words, filling the frame width | the references change something every 0.3 to 0.7 s |
| No still stretch over 0.6 s before the end card | `finish.py` fails it; a parked frame reads as a slideshow |
| Transitions are moves: `whipIn`/`whipOut`, a zoom through a letter, a collapse to a point | fades are the tell of template motion |
| Flip the ground (`bg`, `accent`, `paper`) on phrase changes | colour rhythm carries as much energy as cuts |
| A pure function of `t`: no `Math.random`, `Date` or state between frames | motion blur renders sub-frames out of order |
| 4K masters: H.264 Level 5.2 at most, under 1 GB, checked on the hardware decoder | above 5.2 QuickTime and phones refuse the file |
| On-screen numbers come from the film (`{lines}`, `{frames}`, `{seconds}`) or the user, never invented | a launch film's claims get checked |

## How a film is built

1. **Brief to beat sheet.** Length, tempo, the phrases, one block per phrase, where the drop lands, how it
   ends: [references/method.md](references/method.md). For a film made "like this reference", measure the
   reference first (`rectify2.py` flattens a filmed screen, `dyn.py` and `holds.py` measure it).
2. **Sound.** Free kit and music as above; cue names, levels and the beat grid: [references/sound.md](references/sound.md) (its Scenario prompts are not used).
3. **spec.js.** Start from `examples/starter/spec.js` (15 s) or `examples/just-code/spec.js` (the 52 s film).
   Every block and option: [references/blocks.md](references/blocks.md); motion rules: [references/craft.md](references/craft.md).
4. **Preview and stills.** Scrub in the browser (space plays, arrows step a beat); `snap.mjs` at the beats
   that matter; fix and repeat. Stills are free and take seconds: settle the look here, not in renders.
5. **Render and check.** 1080p check render, `mix.py`, `finish.py` (every gate PASS), then 4K if needed and
   `finish.py` again: [references/render.md](references/render.md). Review renders: `MAXS=6
   ENC="-c:v libx264 -crf 20 -preset veryfast -threads 2" ... --workers 2`; the final goes out at full quality.

## Common mistakes

- **Matching the cut timing but parking between hits.** A film can land every cut on the reference's
  rhythm and still feel slow: the first version of "Just code" had 81 % still frames and a 6 s hold. Keep
  something moving every frame (camera drift, sliding type, ghost rows, particles); `finish.py` measures it.
- **Trusting a generated track's tempo.** Fit the grid on the stretch the film uses (`--window`), give the
  intended tempo (`--bpm`), and prefer a music model with a tempo input. A 0.15 % tempo error puts the last
  hits of a 50 s film 70 ms late.
- **Text that does not fit.** Blocks measure and scale words to the frame; custom code must too, and must
  measure once, while visible (a hidden element measures 0).
- **Reading `offsetLeft` inside a transformed parent.** It is relative to that parent, and a typing caret
  jumps back. Use `relPos` from blocks.js.
- **A nested film sharing state.** The Rewind block builds a second film from the same spec: never store
  per-film state on shared objects.
- **Headless capture traps.** A 1920x1080 viewport paints only about 990 px (use the 1300 px viewport in
  `browser.mjs`); a capture without `clip.scale` comes back at 1080p; big 3D layers come out half drawn
  without `--run-all-compositor-stages-before-draw`. The scripts handle all three.
- **Too many 4K workers.** Six filled 36 GB of memory and stalled the machine. `render.py` sizes workers to
  memory; do not override upward at 4K (at 1080p a worker needs about 4 GB, so 2 fit a 16 GB, 4-core box).
- **Clipping the shutter at a cut.** The fastest frame of every whip renders sharp. `render.mjs` slides the
  window back instead.
- **A slower preset without a level.** The file came out H.264 Level 6.0: it plays in ffmpeg and nowhere on
  a Mac. Keep `-level 5.2` at 4K; `finish.py` checks it on the hardware decoder.
- **`-shortest` when muxing.** It drops the last frames when the audio is a few milliseconds shorter.
