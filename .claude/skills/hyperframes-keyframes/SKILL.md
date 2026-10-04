---
name: hyperframes-keyframes
description: >
  Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe,
  Ken Burns treatment, camera move, visual match/whip handoff, or other seek-safe
  2D/3D keyframes; also for GSAP, CSS keyframes, Anime.js, WAAPI, FLIP, paths,
  masks, SVG morph/draw, text trails, 3D depth, or `hyperframes keyframes` diagnostics.
  Don't use for broad scene strategy, brand design, media sourcing, captions, or
  general video planning.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Keyframes

Keyframes are a pose contract: visible states, continuous subject identity, seek-safe runtime, verified pixels.

Use `hyperframes-animation` for broad scene recipes. Use `hyperframes-cli` for full command docs. Use `references/keyframe-patterns.md` only when choosing implementation mechanisms, not visual style.

## Creator editing boundary

Keyframes own visual motion, not clip assembly. Source-range hard cuts, trim,
splice, and reorder belong to `/hyperframes-core`: author one media element per
kept range, place it with `data-start` and `data-duration`, and select its source
offset with `data-media-start`. Adjacent ranges make a hard cut. A crossfade
uses overlapping clips on different tracks plus visual opacity keyframes; sound
fades use `/hyperframes-audio`.

| Creator request                         | Truthful mechanism                                                                                                                                                                                                          |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Punch-in / punch-out                    | Keyframe `scale` with `x`/`y` or percentage translation on a non-timed visual/crop wrapper inside the clip. Use a set/short tween for a hard punch and a tween for a smooth move.                                           |
| Smooth multi-state zoom or reframe      | Keep one subject wrapper alive and author multiple zoom/reframe states as a pose ladder with per-segment easing.                                                                                                            |
| Pan, reframe, or Ken Burns camera move  | Animate wrapper translation plus scale. Geometry is authored; this is not face tracking or automatic semantic reframing.                                                                                                    |
| Chained camera moves                    | Chain labeled transform beats on one registered seek-safe timeline.                                                                                                                                                         |
| Match cut or whip pan                   | `/hyperframes-animation` owns the visual handoff; `/hyperframes-registry` supplies primitives; keyframes preserve authored geometry, direction, and velocity. There is no automatic matching-frame discovery.               |
| Crop and mask reframe                   | Interpolate `clip-path` or a mask on an inner visual wrapper to crop/reframe without changing source time. Polygon keyframes can form a polygon/mask transition.                                                            |
| Directional wipe cut or iris/reveal cut | Animate a mask/clip boundary across overlapping visual clips; `/hyperframes-animation` owns the handoff choreography.                                                                                                       |
| Split-screen handoff                    | Keep both visual clips placed by core, then keyframe their inner crop/mask wrappers and divider geometry.                                                                                                                   |
| Constant source retime                  | `/hyperframes-core` owns normalized `data-playback-rate` (`0.1..10`) for render-safe picture and pitch-preserved sound. It is constant for the whole media element.                                                         |
| Source speed ramps                      | A `rate` lane in `data-automation` on the `<video>`/`<audio>` (`t` in clip seconds, `v` 0.1..10, log interpolation); it wins over the constant rate.                                                                        |
| Freeze / hold                           | A visual pose, final source frame, or finished sub-composition can hold. Arbitrary mid-source freeze is not supported; preprocess a still/derived segment, place it as its own clip, then resume with another source range. |

When editing picture and sound together, load `/hyperframes-core`, this skill for
visual motion, and `/hyperframes-audio` for fades, crossfades, volume automation,
ducking/carve, or effects on the placed tracks.

A visual transition or cropping treatment is not a temporal source trim or
splice. `/hyperframes-core` owns the timeline, clip timing, and source ranges;
keyframes only animate the visible handoff or crop on wrappers inside those clips.
For copyable combined picture/sound recipes, use `/hyperframes-core` → `references/creator-editing-recipes.md`.

## Procedure

1. Identify the animated subject, visible states, final state, and runtime.
2. Choose the smallest mechanism that proves the prompt. Read `references/keyframe-patterns.md` only if the mechanism is unclear.
3. Author seek-safe keyframes in the declared runtime. Build synchronously and register the runtime instance.
4. Verify with `hyperframes lint`, `hyperframes check`, `hyperframes keyframes`, one focused `--shot`, and snapshots at proof times.
5. If proof fails, fix the source keyframes and rerun the smallest failing diagnostic before rendering.

## Contract

- Name the moving subject.
- Name the poses needed to prove the intended motion, including the final state.
- Keyframe visible channels, not hidden helper state.
- Preserve object identity when continuity matters.
- Crossfade only when the intended motion is replacement or dissolve.
- Hold readable or semantic states long enough to see.
- Final frame is part of the animation, not cleanup.
- Do not reset to rest unless requested.
- Do not end on black unless requested.
- If editing a starter scene, preserve layout, copy, assets, colors, and final state unless asked to redesign.

## Runtime Rules

GSAP:

- build synchronously at page load
- use `gsap.timeline({ paused: true })`
- register as `window.__timelines[compositionId]`
- registry key must match `data-composition-id`
- do not call `tl.play()` for render-critical motion
- keep repeats finite

CSS keyframes:

- finite duration and iteration count
- deterministic delay
- `animation-fill-mode: both`
- use `data-start` when timing belongs to a clip

Anime.js:

- create synchronously
- `autoplay: false`
- finite duration and loops
- push every instance to `window.__hfAnime`

WAAPI:

- finite `duration`
- `fill: "both"`
- deterministic construction
- the text surface does not list WAAPI; verify with `--shot` (it seeks WAAPI) and snapshots

Never use for render-critical motion:

- `Date.now()`
- `performance.now()`
- unseeded `Math.random()`
- hover/scroll triggers
- timers
- async-created timelines
- unregistered `requestAnimationFrame`
- infinite loops

## Detailed guide
GSAP skeleton, keyframe forms, channels, mechanism choice, timing, text/SVG/3D/canvas, CLI proof and diagnostics are in the reference. Read `references/keyframe-details.md` (table of contents at the top) before doing this work.

## Error Handling

| Failure            | Fix                                                                                |
| ------------------ | ---------------------------------------------------------------------------------- |
| endpoint-only      | add middle poses, hold peak proof, rerun `--shot`                                  |
| identity break     | keep one element alive, use shared source/final boxes, remove substitute crossfade |
| fake 3D            | add z/camera travel, occlusion, angled proof                                       |
| wrong final        | add final hold, snapshot final-minus-hold and exact final                          |
| unseekable runtime | pause autoplay, register instance, remove timers, build synchronously              |
| unreadable text    | preserve line boxes, reduce displacement, add final hold, snapshot text frames     |

## Done

Run `hyperframes lint`, `hyperframes check`, `hyperframes keyframes`, one focused `--shot`, and snapshots. Confirm first frame, proof poses, final-minus-hold, exact final, subject-owned motion, and no debug overlays.
