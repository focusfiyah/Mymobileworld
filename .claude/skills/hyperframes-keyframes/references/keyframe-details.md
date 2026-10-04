# Keyframe details

## Contents

- GSAP Skeleton
- Keyframe Forms
- Channels
- Mechanism Choice
- Timing
- Text
- SVG
- 3D
- Canvas / WebGL
- CLI Proof
- Diagnostic Reading

## GSAP Skeleton

```js
const root = document.querySelector("[data-composition-id]");
const compositionId = root.dataset.compositionId;
const tl = gsap.timeline({ paused: true });

tl.addLabel("state-a", 0);
tl.to(".subject", {
  keyframes: [
    { x: 0, opacity: 1, duration: 0.2 },
    { x: 120, opacity: 1, duration: 0.4, ease: "power2.out" },
    { x: 100, opacity: 1, duration: 0.2, ease: "power2.inOut" },
  ],
  ease: "none",
});

window.__timelines = window.__timelines || {};
window.__timelines[compositionId] = tl;
```

Use labels for semantic states. Use position parameters instead of chained delays. Use `immediateRender: false` for later `from()`/`fromTo()` tweens touching the same property.

## Keyframe Forms

- Array keyframes: pose ladder with per-step duration/ease.
- Percentage keyframes: exact timing inside one tween.
- Property arrays: compact multi-stop changes.
- `ease: "none"` on the parent when each stop carries its own easing.
- `easeEach` when every segment should share the same feel.

Do not copy numeric distances or timing from examples. Derive them from the actual composition geometry and duration.

For one subject moving between two boxes, prefer one continuous transform tween or FLIP. Split `x/y/scale` into multiple eased keyframes only when the viewer should feel distinct beats; every segment changes velocity and can read as a hitch.

## Channels

Prefer compositor/visual channels: `x/y/z`, `xPercent/yPercent`, `scale`, `rotationX/Y/Z`, `skew`, `transformOrigin`, `svgOrigin`, `opacity`, `autoAlpha`, `clip-path`, masks, CSS vars, SVG path/dash values, camera transforms, shader uniforms.

Avoid layout/lifecycle channels: `top/left/right/bottom`, `width/height`, `margin/padding`, `display`, `visibility`, late DOM creation, helper overlays doing subject motion.

For visibility changes, use `autoAlpha` on the registered seekable GSAP timeline, or a zero-duration `tl.set()` at an explicit boundary. Target only a non-clip element or a wrapper inside the clip; never target `.clip` itself. Never duration-tween raw `visibility`, and never tween `display`.

## Mechanism Choice

Choose the smallest mechanism that proves the prompt:

| Need                                  | Mechanism                                          |
| ------------------------------------- | -------------------------------------------------- |
| Same subject changes box or hierarchy | shared element / FLIP                              |
| Subject travels a visible route       | path travel                                        |
| Stroke grows or traces                | stroke draw                                        |
| Shape becomes another shape           | shape interpolation                                |
| Reveal boundary is visible            | clip, mask, or shader uniform                      |
| Many items move with order            | stagger / indexed delay                            |
| Text itself moves                     | line, word, character, or band subdivision         |
| Surface bends, stretches, or crops    | parent/child counter-transform                     |
| UI has states                         | explicit state machine                             |
| Scene has depth                       | DOM 3D, Three.js, or WebGL camera/object keyframes |

Mechanisms can combine, but each one must clarify the idea. Decoration is not proof.

## Timing

- Anticipation only when it clarifies cause or direction.
- Acceleration leaves rest.
- Peak proof shows the mechanism unmistakably.
- Follow-through sells energy and direction.
- Overshoot only when the subject should feel elastic or tactile.
- Constant-speed path travel usually needs `ease: "none"`.
- Discrete UI states usually need a sharp ease-out.
- Repeated elements need ordered offsets, not identical timing.
- Final lockups need longer holds than transition poses.
- Smoothness means continuous velocity on the same subject.
- Do not overlap tweens that write the same transform property unless the overlap is intentional and verified.
- Avoid animating large `clip-path`/mask changes while the same hero surface is also scaling or traveling; use nested reveals after the main move settles.

## Text

Preserve line boxes, word spacing, readability, and final fit. If text moves internally, move the glyphs or masked bands, not only decorations around the text. Snapshot readable frames.

## SVG

For stroke growth prefer `DrawSVGPlugin`, then `stroke-dasharray`/`stroke-dashoffset`. For shape interpolation prefer `MorphSVGPlugin`; convert primitives to paths when needed and split complex silhouettes into simpler parts.

## 3D

Scale alone is fake depth. Use perspective on a stable parent, `transform-style: preserve-3d`, z travel, rotation, camera/world motion, occlusion, and layer order when objects cross.

Use one or two diagnostic angles that expose the depth relationship. If angled proof shows no depth crossing, improve z/camera/occlusion.

## Canvas / WebGL

Keyframe camera position, camera target, object transform, material opacity, shader uniforms, and postprocess intensity through deterministic state. Render from HyperFrames time. Use `--ghost` because marker boxes cannot see internal canvas motion.

## CLI Proof

```bash
npx hyperframes lint
npx hyperframes check
npx hyperframes keyframes .
npx hyperframes keyframes . --json
npx hyperframes keyframes . --runtime all
npx hyperframes keyframes . --selector "<selector>" --shot "<file>" --samples <n>
npx hyperframes keyframes . --selector "<selector>" --shot "<file>" --layout strip --from <t0> --to <t1>
npx hyperframes keyframes . --shot "<file>" --ghost --angle <angle>
npx hyperframes snapshot . --at <times>
```

Choose `<selector>` for the real animated subject. Choose `<times>` for first frame, proof poses, final-minus-hold, and exact final. Choose `<angle>` only when depth must be proven.

| Tool             | Proves                                                                                              |
| ---------------- | --------------------------------------------------------------------------------------------------- |
| `keyframes`      | targets, explicit stops, paths, traces, composed parent/child motion, CSS stops, Anime registration |
| `--shot`         | ghosts, route shape, time spacing, DOM 3D projection, focused selector proof                        |
| `--layout strip` | in-place motion, overlaps, contact, subtle scale/opacity, text waves                                |
| `--ghost`        | canvas, WebGL, shader motion, rendered 3D                                                           |
| `snapshot --at`  | masks, text readability, full state, final lockup, black/reset tails                                |

If selector proof looks wrong:

1. rerun `--json`
2. find the actual animated target
3. shoot that target
4. snapshot full frames
5. trust painted pixels over logs

## Diagnostic Reading

`flat` means no explicit middle poses. `keyframes` means explicit stops exist. `motionPath` means a route exists. `trace` means multi-stroke drawing. `composed with` means child motion inherits parent motion.

Even ghost spacing means constant speed. Clustered ghosts mean slow-in or settle. Large gaps mean fast travel.

A helper-selector shot is not proof. An onion shot over a broken full frame is not proof.
