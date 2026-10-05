# Per-shot ads with a recurring persona

## Contents

- Per-shot ads with a recurring persona (approved route)
  - Prompt rules that each cost a retry here
  - Trim the dead air
  - Animated CTA
  - Lip sync to a cloned voice (optional)
  - Stills: use Kie
  - Video model prices on Kie (read 2026-09-15)

## Per-shot ads with a recurring persona (approved route)

Proven on the Seller AI OS 30s tech UGC ad (Ralph in a home office, 7 shots, 9:16). His verdict:
"this version is good". A clean run costs about **$3**. Use this whenever ONE person talks to camera
across many shots.

**Generate ONE clip per shot, never one multi-shot clip.** Same total cost, no multi-shot risk, and a
bad shot is a ~$0.10 retry instead of the whole thing. Each shot animates from its own approved still.

1. **Stills on Kie** (see "Stills: use Kie" below). One outfit/identity still, then one per distinct
   setting. Show every still before the next spend.
2. **Blur logos on the STILL, not the video** (`gblur` over the region). The video model reproduces
   whatever is in its first frame, so an Apple laptop lid blurred later costs a re-render.
3. **One Grok clip per shot:** `grok-imagine-video-1-5-preview` via Kie REST, `image_urls: [still]`,
   `duration` 1-15s, `resolution: "720p"`, `aspect_ratio: "9:16"`. **$0.0225/s** (a 5s shot is $0.11),
   ~35s each, and it DOES generate lip-synced speech although Kie's schema lists no audio field.
   Output is 704x1280 plus a harmless mjpeg cover stream; scale to 720. `scripts/grok_per_shot.py`.
4. **Voice: two routes.** Keep each clip's own audio (free, mouths match, but **the voice changes at
   every cut**), or run `scripts/kie_lipsync.py` to re-drive the mouth from a cloned ElevenLabs voice
   ($0.04/s). Ralph picked the AI voice here, but only after seeing both.
5. **Trim the pauses — he will ask.** `scripts/trim_pauses.py`, see below.
6. **Overlays in ffmpeg** (free): corner windows showing the real product UI, and an animated CTA.

### Prompt rules that each cost a retry here

- **Never name a gesture the model can over-interpret.** "Present the screen with an open palm" made it
  pick the laptop up and tilt it at the camera. State it as a hard negative instead: "THE LAPTOP STAYS
  FLAT ON THE DESK AT ALL TIMES: never lifts, picks up, tilts or shows its screen to camera; hands stay
  at desk level."
- **Never ask for counting gestures.** Video models get exact finger counts wrong, so "step two / step
  three" never matches the fingers. Use open-palm presents and nods, plus "he never counts on his
  fingers and never holds up individual fingers".
- **Words with two pronunciations are invisible to ASR.** "Twelve listings live" was read as *to live*,
  not *live on the internet*. Whisper spells both the same, so no transcript check catches it — only a
  human listen. Reword instead ("listings up"). Same family as the say-ability seams.

### Trim the dead air

Grok leaves ~0.5-1.0s of silence at the head and tail of every clip; on a 7-shot ad that is ~4.8s of
slack (34.6s became 29.8s). Measure each shot's **first and last word with the transcriber**, not
silencedetect alone, then trim with ~0.15s lead and ~0.25s tail handles. **Keep a longer tail wherever
the tail is a visual beat** — a coffee sip finishing, a held finger-point under the CTA — because
cutting on the last word clips the action. Recompute every overlay window and the CTA start from the
new shot boundaries afterwards.

### Animated CTA

`drawtext` cannot scale over time, so a static text layer with a fade reads as "not animated" and Ralph
will say so. Render a transparent PNG sequence (pop-in overshoot, steady pulse, bouncing arrow) with
`scripts/cta_animate.py` and overlay it with `setpts=PTS-STARTPTS+<start>/TB` and `eof_action=pass`.

### Lip sync to a cloned voice (optional)

`volcengine/video-to-video-lip-sync` on Kie, **$0.04/s**, `mode: "lite"`, `video_url` + `audio_url`,
`align_audio: true`. Output follows the AUDIO duration. **The lip-sync step re-encodes the audio and
degrades it** — "Seller" came back as "Cellar" on BOTH whisper models even though the source mp3 passed
both. Fix by muxing the original mp3 back onto the result (`-map 0:v -map 1:a -c:v copy -shortest`):
free, and the mouth still matches because that same audio drove it.

### Stills: use Kie

**Kie is Ralph's primary provider now, with fal as backup** (prices read 2026-09-15): Nano Banana Pro
(Gemini 3 Pro Image) **$0.09** at 1K/2K vs $0.134 direct and $0.15 on fal; Nano Banana 2 $0.04 (1K) /
$0.06 (2K); Seedream 4.5 $0.0325; Seedream 5.0 Lite $0.0275; GPT Image 2.5 $0.03 (1K). A side-by-side
identity test on Ralph put **Nano Banana Pro first** (closest face), Nano Banana 2 a close second
(build closest, face wider), Seedream 4.5 last (narrower face, groomed beard). Stills feeding a 720p
video only need 1K.

**Kie REST specifics:** upload files to `POST https://kieai.redpandaai.co/api/file-stream-upload`
(NOT api.kie.ai, which 404s), form fields `file` + `uploadPath`, public URL in `data.downloadUrl`, kept
3 days. Model ids: `nano-banana-pro` / `nano-banana-2` (`image_input`, `aspect_ratio`, `resolution`),
`seedream/4.5-edit` (`image_urls`, `quality`). Kie returns **500 "The server is busy"** under parallel
load; failed tasks cost $0 and an immediate retry works.

### Video model prices on Kie (read 2026-09-15)

Artificial Analysis image-to-video Elo in brackets, where ranked.

| Model | Price | Notes |
|---|---|---|
| **Grok Imagine Video 1.5** | **$0.0225/s** | [1116] Speaks, lip-synced. Cheapest usable talking route |
| Seedance 2.0 Mini | $0.041/s | Not ranked. Proven for skits and multi-character dialogue |
| MiniMax H3 | $0.04/s (768p) | [1190] **No audio field on Kie** — silent B-roll only |
| Veo 3.1 Lite | $0.15/video (720p) | [1072] Cheap, fixed length |
| Kling 3.0 | $0.10/s (720p, audio) | [1072] |
| Seedance 2.0 full | $0.205/s (720p), $0.51/s (1080p) | [1197] 5x Mini at 720p. Sharper faces, legible label in-camera; Ralph ruled it too costly on 2026-09-19 and set **Mini as the default for redos** |
| Seedance 2.5 | $0.315/s (720p) | Ralph rejected as costly |
| Lip sync (volcengine) | $0.04/s | Re-drives a mouth from any audio |
