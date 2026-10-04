# Tools, single-spokesperson recipe, QC and compliance

## Contents

- Where the tools live
- The recipe (start here)
- Prompt template
- Say-ability pre-check (before ANY paid render)
- Script length is arithmetic, not taste
- Reference image hygiene (do this before generating)
- Verify by measurement, never by the success flag
- Cut timing comes from the delivered audio
- Compose the insert as an overlay cut
- Do NOT build a label workaround
- Compliance guardrails (health / supplement ads)
- Cost table (10s, 9:16)
- Run it in one pass

## Where the tools live

Everything below runs through **OpenMontage at `C:\dev\OpenMontage`**. Assets
usually sit somewhere else (a Desktop folder), so the toolchain will not be
visible from the working directory — go to it explicitly.

```bash
cd "C:/dev/OpenMontage"
export PYTHONIOENCODING=utf-8     # required; tool output contains → and crashes cp1252
.venv/Scripts/python.exe -c "..."
```

```python
from tools.tool_registry import registry
registry.discover()
registry._tools["gemini_omni_video"].execute({...})
```

Scripts saved under `projects/` also need `PYTHONPATH=C:/dev/OpenMontage`.
Availability is `get_info()["status"] == "available"`. `projects/` is gitignored,
so put scratch scripts and working assets there. Full detail and more gotchas:
the `openmontage-toolchain` memory.

For a single short ad, call the generation tool directly and assemble with
`video_compose` — the full pipeline ceremony in `AGENT_GUIDE.md` is for real
multi-stage productions.

## The recipe (start here)

**Model: `gemini_omni_fal`, `operation="reference_to_video"`.** It is the only
configured route that binds a person reference AND a product reference in ONE
call, and it renders real printed brand text legibly in-camera.

```python
inputs = {
    "prompt": prompt,                       # template below
    "operation": "reference_to_video",      # NOT text_to_video, NOT image_to_video
    "reference_image_paths": [person_photo, packshot],   # order = IMAGE_REF_0, IMAGE_REF_1
    "aspect_ratio": "9:16",
    "duration": 10,                         # 3-10 only
    "output_path": out,
}
```

Hard limits: **3-10s, 720p (720x1280 at 9:16), 24fps.** ~$1.30 at 10s.

Operation traps, each of which fails or silently degrades:
- `text_to_video` **rejects** reference images on fal (errors before submit).
- `image_to_video` sends **only the first** image — silently drops the packshot,
  so you get a blank or invented label.
- `reference_to_video` sends all of them. This is the one you want.

## Prompt template

Bind each image by tag and say what it *is*. Describe scene + camera + lighting +
motion + audio. Negatives go in prose — there is no negative_prompt.

```
<FIRST_FRAME> Vertical 9:16 selfie video, handheld phone footage she is filming
of herself at home.
<IMAGE_REF_0> is the woman: keep her face, <hair>, <wardrobe>, <jewellery> and
the background exactly as they appear, with no morphing and no drift for the
whole clip.
<IMAGE_REF_1> is the product: <shape, colour, cap, label wording>. Reproduce
that <item> and its printed label faithfully and keep the label sharp, upright
and squarely facing the camera lens so the wording stays readable.
Motion: she starts with empty hands, looking straight down the lens, talking
with high energy and an expressive face, gesturing with one open hand. About a
third of the way in she raises the <IMAGE_REF_1> <item> into frame at chest
height beside her face and holds it steady with the label toward the camera.
Camera: fixed selfie distance with constant subtle natural handheld shake. No
zoom, no camera moves.
Lighting: warm natural indoor light, realistic unretouched skin texture,
authentic phone-camera look, no cinematic grading.
Audio: she speaks this line clearly and at an energetic pace: "<dialogue>"
No background music. No extra sound effects. No on-screen text or captions.
There is no <prop to exclude> anywhere in the shot.
```

## Say-ability pre-check (before ANY paid render)

Ralph will not pay for a redo that a script check would have caught. Before the storyboard, read every
dialogue line for seams where the words will blur together, and fix them in the script:

- **Vowel-linking seams:** a word ending in a vowel, L, R, N, W or X followed by a word starting with a vowel.
  "real. Onyx and" rendered as "Rioona" (tiger eye v1). "look how it" rendered as "look out" (v2). Reword so hard
  consonants sit at the seam: "the real deal. Black and gold".
- **Rare words** (onyx, ingredient names): use a common word or a phonetic spelling.
- **Density:** no shot window above ~4.5 words/s.
- Add to the prompt: "fast, energetic but crisp articulation, every word pronounced fully and separately, never
  slurred, short breath between sentences".
- When presenting the script, list the lines you changed for say-ability.

Post-render whisper checks (small + medium on a slice) remain the backstop, not the check.

## Script length is arithmetic, not taste

Sustainable fast UGC speech is **3.0-3.6 words/second**. Multiply before promising
anything:

| Runtime | Words |
|---|---|
| 10s | ~32-36 |
| 15s | ~45-50 |
| 20s | ~60-64 |

A 65-word script does not fit 10 seconds — that is 6.5 w/s, roughly double
speech. Say so immediately and offer the trim, rather than discovering it later.
Keep the client's own wording; cut whole beats, never rewrite lines.

## Reference image hygiene (do this before generating)

Reference-driven video **reproduces props and background from the photo**, even
when the prompt says otherwise. Prompt wording competes with pixels and loses.

- Inspect the reference. Crop out anything that must not appear — an ffmpeg crop
  is free and instant; a retake is not. A wine glass in a wellness ad cost a full
  take once.
- Do not ask for a different background. Match the photo's own background in the
  prompt; it is more authentic and strengthens identity retention.

## Verify by measurement, never by the success flag

A tool that reports success can still emit silence, black frames, or the wrong
length. Every time:

```bash
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height \
  -of default=noprint_wrappers=1 out.mp4          # duration, dims, audio stream present
ffmpeg -hide_banner -i out.mp4 -af volumedetect -f null - 2>&1 | grep volume
                                                  # real speech, not a silent track
ffmpeg -hide_banner -v error -y -i out.mp4 -vf "fps=1,scale=150:-1,tile=5x2" -frames:v 1 sheet.png
                                                  # identity + product across all 10s, one image
```

Check the contact sheet for: face consistent with the reference, no excluded
props, product legible, label correct.

**Then verify the words, not just the waveform.** `transcriber` (faster-whisper,
installed locally, free, no key) returns segments plus per-word confidence:

```python
registry._tools["transcriber"].execute(
    {"input_path": out, "model_size": "small", "language": "en"})
```

Diff the transcript against the script. Confidence is the tell — ordinary words
land at 0.83-0.99; anything materially below that was mumbled or is rare
vocabulary. To tell those two apart, re-run at `model_size="medium"`: if two
models disagree AND confidence is low, the delivery is genuinely unclear.
Compliance-critical wording must match verbatim — verify it, never assume it.

**Hard words:** spell them phonetically in the dialogue itself
("un-deh-sil-EN-ic") rather than trusting the model with rare vocabulary. Check
the word's duration in the word timings; a 5-syllable term compressed into ~0.5s
is being rushed.

ASR closes most of the gap but not all of it — it confirms *what* was said, not
whether the tone lands. That still needs one human listen.

**Audio headroom:** if `max_volume` is at 0.0 dBFS there is none. Platforms
normalise on upload so it usually survives, but flag it.

## Cut timing comes from the delivered audio

Never reuse timings between takes — models pace the same script differently.

```bash
ffmpeg -hide_banner -i take.mp4 -af "silencedetect=noise=-38dB:d=0.10" -f null - 2>&1 | grep silence
```

The first pause is the end of the hook. Cut the B-roll insert ~0.2s before it so
it lands on the final word, and hold it ~0.8-1.0s: long enough to register, short
enough not to lose the viewer. Hard cuts both ways — a dissolve reads as an ad.

## Compose the insert as an overlay cut

Use `video_compose` `operation="render"` with `render_runtime="ffmpeg"` and mark
the still `layer: "overlay"` — it composites over the primary instead of being
concatenated into it. (`layer` support was added in
`fix/compose-video-primary-with-still-inserts`; without it the FFmpeg path
refuses stills in cuts and Remotion's TalkingHead cannot take a video primary.)

```python
"cuts": [
  {"id":"c1","source":"<take>","in_seconds":0,"out_seconds":10.0,"layer":"primary"},
  {"id":"c2","source":"<insert.png>","in_seconds":2.30,"out_seconds":3.15,"layer":"overlay",
   "transform":{"scale":1.0,"position":"center"}},
],
"metadata": {"compose_target": {"width":720,"height":1280,"fit":"cover"}}
```

Set `compose_target` or the output silently becomes 1920x1080.

## Do NOT build a label workaround

Do not composite or track a label onto the product. If the label is wrong, the
generation was set up wrong — almost always `image_to_video` instead of
`reference_to_video`, or the packshot missing from `reference_image_paths`.
Per-frame label tracking has been built once, unnecessarily, and it cost hours.

## Compliance guardrails (health / supplement ads)

- **No fabricated before/after.** A synthetic result image is a fabricated claim:
  FTC substantiation exposure plus platform health-ad policy, and the downside
  lands on the Shop account, not just the ad. Use real substantiated photos, an
  on-screen "Dramatization" label, or a condition-only insert (which depicts the
  problem and carries no outcome claim).
- **Scarcity is a factual claim.** "Selling out / low in stock" must be true.
  Confirm before it goes in. Neutral swap: "don't put it off."
- **Keep hedged claim wording exact.** "Target ... and support healthier-looking
  nails" is structure/appearance language. Never let a caption or regeneration
  upgrade it to cures / eliminates / kills, and never attach a timeframe.
- Write percentages as words ("twenty five percent") in the dialogue or the model
  mangles the numeral. Supply a phonetic hint for hard words.

## Cost table (10s, 9:16)

| Route | Cost | Res | Label from packshot |
|---|---|---|---|
| **`gemini_omni_fal`** | **$1.30** | 720p | **yes** |
| `gemini_omni_video` (Google key) | $1.00 | 720p | yes — but check quota first |
| `minimax_fal_video` | $1.90 | 2K | no — separate endpoints |
| `kling_video` v3/standard | $0.20 | 720p | no |
| `seedance_ark` mini | $0.69 | 720p | needs non-empty ARK_API_KEY |

`gemini_omni_video` is cheaper and supports conversational editing
(`previous_interaction_id` + a short surgical prompt + "Keep everything else the
same", needs `store=true`) — so a near-miss can be patched instead of
regenerated. It returned HTTP 429 `limit: 0` on the free tier, which is a plan
issue, not a rate limit. Check before routing there.

Choose MiniMax only when a 2K master matters more than an in-camera label.

## Run it in one pass

Ask, don't assume (see "Working with Ralph"). Settle these in a single question before generating, not one at a time:
runtime, budget cap, one variant or several, captions or none, and whether the
scarcity claim is true. Then offer full-run pre-authorization up front so the
job does not stop at six gates.
