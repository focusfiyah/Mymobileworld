---
name: ugc-product-ad
description: Produce short creator-style UGC product ads (TikTok Shop / Meta). Covers (1) a talking-to-camera spokesperson spot from a person's photo plus a product packshot; (2) multi-character dialogue skit ads (couple or family "POV" skits with a product handoff) from Gemini 3 Pro stills and Seedance 2.0 Mini on Kie; (3) longer multi-shot ads from ONE recurring persona (an AI influencer), one Grok Imagine clip per shot on Kie, optionally lip-synced to a cloned ElevenLabs voice; (4) patching a mumbled off-camera line by cloning the clip's own voice; and (5) demo/tips ads over a voiceover, hands-only or with the person on camera (Kie stills + Seedance Mini per shot, lip sync on face shots). Use for any "make a UGC ad", "creator video", "TikTok Shop ad", "spokesperson spot", "skit", "tech UGC", "AI influencer", "use my voice", "remove the pauses", "hands-only" request, and for Fungix / Grace / Carpe / Restlex / Ralph / Seller AI OS ad work. Encodes models, prompts, timing, cost control, QC and compliance.
---

# UGC Product Ad

Repeatable recipes for creator-style product ads. Follow them and a job takes a
handful of tool calls. Working it out from scratch takes fifty calls and produces
worse output, which is why this file exists.

- **Single spokesperson, 10s, talking to camera:** "The recipe" below (Gemini Omni).
- **Recreate a trending spokesperson video (up to 15s, product close-ups):** "Recreate a trending
  spokesperson video" (Gemini 3 Pro stills + one Seedance Mini clip). Approved by Ralph on 2026-09-14.
- **Multi-character skit with dialogue and a product handoff:** "Multi-character
  skit ads" (Seedance Mini on Kie). Approved by Ralph on 2026-09-14.
- **One line mumbled or reworded after the render, speaker off camera:** "Patch a spoken line
  (audio only)" (ElevenLabs clone of the clip's voice + splice). Approved by Ralph on 2026-09-15.
- **Multi-shot ad from ONE persona, 25-35s, on-camera dialogue in every shot:** "Per-shot ads with
  a recurring persona" (Grok Imagine per shot, optional Kie lip sync to a cloned voice).
  Approved by Ralph on 2026-09-16. Cheapest route here by far: a 30s ad costs about **$3**.
- **Couple skit with one speaker OFF camera (a "caught you" POV, a partner reacting):** "Multi-character
  skit ads" below, but read **"Fix a line after the render"** first — an off-camera speaker means every one
  of her lines can be rewritten later for free. Proven on the Fungix "CAUGHT YOU" skit, 2026-09-19.
- **Editing a creator's REAL raw takes (hook / body / CTA files) into many combo ads:** not this
  skill, use the **`ugc-take-combos`** skill (no generation; audio-snapped cuts, reference-style
  overlays, previews before render). Approved on the Fungix / Grace job, 2026-09-18.
- **Faceless hands-only product demo / tips video over a voiceover (no face, no lip sync):**
  "Hands-only product ad" below (Kie Nano Banana Pro stills + one Seedance Mini clip per shot, free ffmpeg cut).
  Proven on Grace's Carpe Vanilla Peach ad, 2026-10-01 (36s, 9 shots, $3.52 actual vs $2.53 planned).
- **A real person (AI from their photo) demonstrating the product over a voiceover, face on some shots:**
  "On-camera demo over a voiceover" below (Kie stills + Seedance Mini per shot, lip sync on face shots, free
  edit-list cut). Carpe Mountain Breeze for Grace, 2026-10-01: 35s, $6.60 vs a $2.50 quote; read its lessons.

## Working with Ralph: money, questions, tokens (read first, every job)

Ralph's words (2026-10-01): "I don't like time wasted, I like you to be efficient, low usage/token, don't waste money
and ask questions, do not assume, because that's how we waste time and money."

- **Ask before EVERY paid call, including redos, retries and "one more try".** Quote the exact cost. A failed
  attempt is not permission for a second one: stop, show it, ask.
- **Ambiguous instruction → one short question, never a guess.** "To clarify, shorten the nails" was read as
  "even shorter" and two unrequested edits ($0.18) were run; he had liked the version already made.
- **Free fixes first.** Blur a wrong label line, crop, retime, re-cut in ffmpeg/PIL before any reroll.
- **Confirm the real product before the first paid still:** applicator/top, cap, label, size. Ask for a real
  photo if the reference is a generated sheet. The Carpe sheet showed a ribbed white dome; the real stick has an
  orange slotted top → 5 stills redone (~$0.54).
- **Confirm the person's details too** (nail length, jewellery, skin): the reference pixels win over the prompt.
  Long nails in the hand sheet came out long; say "short nails" up front if that's wanted, and ask.
- **A pasted prompt that clashes with the video** (product-sheet style, grey background, "no hands") → say so and
  ask how to use it before spending. Run verbatim it gave a 3-panel sheet, usable only as a reference crop.
- **Client:** ask who the ad is for at the start; apply that client's rules (Grace: no personal-use claims unless
  true, no false scarcity, detached CTA, one honest caveat).
- **Lock the whole plan before the first paid call** (Ralph, 2026-10-01: "You are having me spend all my credits
  today"; "I don't think you remembered me wanting the process to be time efficient and cost effective"): ONE
  message with script, every shot, outfit, setting, face or no face, voiceover vs lip sync, and the total cost; one
  approval. A mid-job change gets a new total before anything is spent.
- **One test clip before any batch.** Carpe v2 rendered 8 clips at once and all came back wrong ($1.52); one clip
  would have cost $0.21.
- **QC before sending, so Ralph never finds it first** (each miss cost him a review round, ~20 rounds / 4h on
  Carpe v2): every clip at ≥1.0x speed; no face on screen while the voice talks unless lip-synced; product never
  cropped off or smeared; no forehead wrinkles; same outfit and product in every shot; frame-by-frame check wherever
  hands or the product cross the face.
- **Script checklist, every ad (standard):** Every script, before the plan goes to Ralph (Ralph 2026-10-01, after the Plant Therapy hook shipped with no on-screen text):
  (1) tiktok-shop-coach: research + 3 hook options (spoken line AND on-screen hook text) modeled on proven videos;
  (2) humanizer pass on the script and caption; (3) after the cut, `tiktok.py compare <viral video> <our cut>` and fix
  what it shows (hook text in frame 0, pace, cuts) before sending.
- **On-screen text style (standard, Ralph 2026-09-18 Murano earrings; reapplied 2026-10-01):** TikTok "Classic": white
  semibold, NO background bubble, soft drop shadow, lowercase, two balanced lines past five words, no "orange cart"
  text line. Use `ugc-product-ad/scripts/classic_caption.py` (Open Sans SemiBold stands in for Segoe UI Semibold).
- **Report the running total against the quote at every paid step.**
- **Phone notification at every review point** (Ralph, 2026-10-01: "Make that a standard"): he leaves the app, so
  send a PushNotification (one line: what to review + any cost to approve) whenever a still sheet, test clip or cut is
  ready, or a redo needs his OK. Send the file with SendUserFile first. Not for routine progress.
- **Delivering to Google Drive** (Ralph, 2026-10-01): use both the Google Drive connector and Composio `googledrive`;
  if one fails, use the other. Videos go through Composio `GOOGLEDRIVE_UPLOAD_FROM_URL` after hosting the file on
  Kie's file host (`kie.upload`); the connector handles folders and docs but can't carry a video.
- **Tokens:** keep the job README's `Status:` line current (what's done, what's next, what it costs) so "continue
  the X ad" needs one file read. Short updates, chained shell steps, one contact sheet per batch.

## Multi-character skit ads (approved route)

Proven on the Restlex "2am" couple skit: Ralph as the husband, Grace as the wife,
20s, 9:16, two 10s clips. Ralph's verdict: "This version is good". A clean run
costs about **$1.50**.

**Working with Ralph (non-negotiable):**
- Show a **still-image storyboard before any video spend**. He will not pay
  twice for fixes.
- State the exact cost and ask before each paid step. Run the riskiest clip first.
- Keep identity exact: no morphing, no facial drift. Swap wardrobe to fit the
  scene. No burned captions unless he asks.
- **He reviews the script before approving it.** Present it as a table and wait. Run the
  Say-ability pre-check first and list the lines you changed for it.
- **He wants to see every still preview before the next paid run,** even after saying "go ahead".
- Be token-mindful: small previews, one combined contact sheet, chained shell
  steps, short updates.

### Steps

1. **Script to clips.** Keep each clip at or under 10s with about 2-3 words/s,
   because action beats eat time. Split at a natural beat. Keep his wording verbatim.
2. **Clean the reference photos.** Crop out props that must not appear (Grace's
   green-shirt photo has a wine glass: crop `860:1907:0:0`). Crop face panels
   out of turnaround sheets.
3. **Identity and wardrobe with Gemini 3 Pro Image** (`gemini-3-pro-image`,
   google-genai `generate_content`, `ImageConfig(aspect_ratio, image_size="2K")`,
   about $0.134/image; see `scripts/gemini_image_frames.py`). Prompt: "Change ONLY
   the clothing … exact identity, no morphing, no facial drift, no beautification."
   Check one small side-by-side of the face crops against the originals.
4. **Storyboard stills (Gemini 3 Pro).** Every call gets the real face photo, the
   outfit portrait and the packshot. Describe the room in text, never with a photo
   of other people. Render the wide shot first and pass it as the room reference for
   the later stills. **Don't use nano-banana (Gemini 2.5 Flash Image) for product
   shots.** Its bottle looks pasted in and the label comes out garbled.
5. **Video with Seedance 2.0 Mini on Kie via REST** (`scripts/kie_seedance_mini.py`,
   plus `scripts/example_skit_prompts.py` for prompt structure). Model
   `bytedance/seedance-2-mini`; input `{prompt, reference_image_urls (≤9),
   generate_audio: true, resolution: "720p", aspect_ratio: "9:16", duration: 4-15}`.
   It costs **$0.041/s, so $0.41 per 10s clip**, and takes about 4 min. Refer to refs
   in prose as "Reference image N" and lay out shots as `Shot 1 (0-2s): …`. Quote the
   dialogue exactly and add "just once" to stop repeated words. End with "No background
   music. No other dialogue. No on-screen text." Host refs as public URLs
   (OpenMontage `upload_image_fal`), never base64 through context. Kie's MCP tool
   only runs Seedance 2.5 at $0.315/s, which Ralph rejected as costly.
6. **Fix shots without regenerating the clip:**
   - Weak action shot: a 4s Mini insert with `first_frame_url` set to that shot's
     frame and **`generate_audio: false`** ($0.16), spliced over it with
     `scripts/splice_insert.py`.
   - Unreadable label: about 0.8s of product close-up cropped from the approved
     Gemini 3 Pro still, overlaid in a dialogue pause:
     `[1:v]scale=1440:2560,zoompan=z='1+0.0035*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=24,trim=duration=0.8,setpts=PTS-STARTPTS+T/TB[ins];[0:v][ins]overlay=enable='between(t,T,T+0.8)':eof_action=pass`
   - Mumbled or reworded line while the speaker is off camera: patch the audio only,
     see "Patch a spoken line" below ($0 video).
7. **Assemble.** Loudnorm each clip (`I=-16:TP=-1.5`), concat with hard cuts, 720x1280.

### Patch a spoken line (audio only)

Proven on the Bruise Cream "clumsy partner" skit (2026-09-15). Seedance said "arnica" as
"Ernieja" (whisper small and medium both agreed, at 0.43-0.51), and Ralph also changed the
line to "arnica-based". He approved the patch: "this was good". It costs only ElevenLabs
subscription characters, with no video spend and no re-roll of the other lines.

**Only when the mouth isn't visible** during that line (off camera, B-roll, product insert).
If lips are on screen, use a retake or an insert instead.

1. **Map the gap from the transcript.** The new take has to fit between the end of the
   previous line and the start of the next. Adding two syllables takes about 0.4s.
2. **Clone and render takes** with `scripts/eleven_clone_takes.py <clip> <out_dir> "<line>" --keep
   a:b c:d ...`. `--keep` = the same speaker's *other* lines, ~10s+ total, with no SFX. Pass
   `--voice-id` to reuse a clone. **Grace's Seedance voice is kept as `3dmagVYZFvrGkBbWWmGC`**
   ("Grace Bruise Skit Seedance"), so reuse it rather than re-cloning.
3. **Splice each take into the full clip and test it there, never on its own.** Use
   `scripts/splice_voice_line.py <clip> <take> <out> --line s:e --gap s:e --pause s:e`.
   Take t1 scored 0.91 in isolation but read "Ornica" once spliced in, even with the room
   tone off, so the take itself was the problem, not the mix. Pass = whisper `small` on the
   **full file** and `medium` on a slice both hear the word.
4. **Pick the passing take closest in f0** to the speaker's other lines that fits the gap.
   On Bruise Cream t2 won (multilingual_v2, stability 0.6, style 0.15). t3 (eleven_v3)
   passed too but ran 2.35s and collided with the next line.
5. **Rebuild** (label insert + loudnorm) on the patched clip, re-run the full transcript,
   and still ask for one human listen, since it's a different voice engine.

ElevenLabs MCP traps: its file tools only take paths under `C:\Users\ralph\Desktop`, and
`voice_clone` fails 400 `invalid_labels`. The scripts call the REST API directly with the
`.env` key.

### Cheap verification (every clip)

- Measure duration, audio presence and volume with ffprobe and volumedetect.
- Build one downscaled contact sheet per clip. Combine clips into one image.
- Run the transcriber (faster-whisper `small`) and use `medium` on a sliced wav
  for a doubtful word.
- Check speakers per line with autocorrelation f0: female ~215-245 Hz, male ~105-150 Hz.
- Detect cuts where the gray frame mean-abs-diff exceeds 25. Measure motion by
  region, e.g. whole leg vs foot.

### Traps hit on this route

- **Direct Google Gemini Omni (`gemini_omni_video`) blocks couple-in-bed scenes**
  with photoreal refs (400 prohibited use), even with sanitized wording. The same
  refs pass Gemini 3 Pro Image.
- **Kie's content audit rejects inserts that have audio on** ("output audio may
  be related to copyright"). Turn audio off for inserts. **Failed Kie tasks cost 0**
  (check kie.ai/logs).
- **Seedance Mini garbles small label text**, so use the still close-up insert.
  It frames a "restless leg" as the foot unless told "the WHOLE LEG, from the knee,
  lying ON the mattress, never hanging off the bed".
- **Kie's prepare step returns no price.** Read kie.ai/pricing in the logged-in
  browser (the search box needs a real click first). 1 credit = $0.005.

### Fix a line after the render (no video spend)

Anything said while the speaker's mouth is off screen can be replaced with a clone of that clip's own
voice ("Patch a spoken line" above). On the Fungix skit that covered the entire opening hook, the brand
name, the ingredient name and the closing CTA — four rewrites, zero re-renders. Techniques:

- **Hide the mouth on purpose.** A product close-up held over a phrase (0.8-2.1s) turns an on-camera line
  into a patchable one, and a product insert under the CTA is good advertising anyway.
- **Buy time for a LONGER line** rather than re-rendering: insert B-roll (a condition close-up, the
  packshot) plus a ~0.8s freeze of the listener's face. That bought 2.2s for a rewritten hook.
- **Tune pace with `atempo`** (pitch preserved), after trimming inter-phrase silence with
  `silenceremove=stop_periods=-1:stop_duration=0.16`. Ralph rejected one take as too fast and another as
  too slow; `atempo=1.18` on the slow one was the approved middle.
- **Cut the dead air in picture and sound together** when the new line is shorter than the old one.
- **eleven_v3 gives the best emphasis** (shouted / disgusted) but pads pauses and sometimes appends a
  **hallucinated gibberish tail**; multilingual_v2 with style 0.7-0.9 is tighter. Whisper every take, and
  splice it into the clip before judging it.
- Pronunciation: spell brand names phonetically for TTS ("Funjicks" for Fungix) and hard words too
  ("un-deh-suh-LEN-ik"). ASR can't confirm a brand name it has never seen — ask for a human listen.

### Before any paid render: pre-flight the first frame

Kie's upload helper cached by file path, so a regenerated still at the same path reused the OLD hosted
URL and Seedance rendered a $2.87 clip from a rejected frame. Key the cache on path+size+mtime, and
**download the hosted first frame and byte-compare it to the local still before submitting**.

### Cost reference (720p, 9:16)

| Item | Cost |
|---|---|
| Gemini 3 Pro Image still (2K) | $0.134 |
| Seedance 2.0 Mini (Kie), 10s clip | **$0.41** |
| Seedance Mini 4s insert | $0.16 |
| Seedance 2 Fast (Kie), 10s | $1.24 |
| Seedance 2.5 (Kie), 10s | $3.15 |
| Gemini Omni fal / Google, 10s | $1.30 / $1.00 |

### In Cowork or on another machine

The local toolchain (`C:\dev\OpenMontage`, keys in its `.env` and in
`~/.claude.json`) may not be reachable. Check before assuming. The bundled
`scripts/` are the working reference: adapt their paths, and ask Ralph for the Kie
and Google keys or a connector rather than guessing.

## Recreate a trending spokesperson video (approved route)

Proven on the tiger eye necklace ad (2026-09-14). Ralph was restyled with a trimmed beard, glasses, a black tee
and a walnut home study, in a 15s 9:16 clip. His verdict: "looks good". A clean run costs about **$1.15**
(4 Gemini 3 Pro stills at $0.54 plus one 15s Seedance Mini clip at $0.615).

1. **Analyse the source for free:** ffprobe, a 1fps contact sheet, a whisper transcript with timestamps, and
   silencedetect. Map each beat (hook / reframe / close-up proof / personal proof / urgency / CTA) to a time, a
   shot and a word count. A downloaded TikTok ends with a ~3s logo end card, which is not ad content, so "keep
   the same timeframe" means the spoken ad length (19.1s file = 15s ad).
2. **Rewrite on the same beats:** same time window per beat, about the same word count, new wording, same energy.
   Keep any line the client insists on verbatim. Scarcity only if the client confirms it's true. Run the
   **Say-ability pre-check**. Present a table (time | shot | beat | line | words) and wait for approval.
3. **Stills (Gemini 3 Pro, `scripts/gemini_restyle_portrait.py`, `scripts/gemini_product_closeups.py`):**
   restyle the portrait, then the medium hero still, then 1-2 product close-ups that reuse the hero still as the
   identity ref. Show each before the next spend. Traps:
   - Crop the source creator's face out of any video frame used as a product reference, or his features bleed in.
   - To copy the product *as it looks in the video*, drop a packshot that differs (a square pendant packshot
     kept pulling the teardrop pendant square).
   - Ask for "phone propped on the desk, NO arm extended toward the camera" when the hands must be free.
   - Black beads on a black tee still read if you ask for "bright specular highlights".
   - The medium shot's small product detail drifts more than the close-ups; the close-up refs fix it in video.
4. **Video: ONE Seedance 2.0 Mini call, up to 15s** (`scripts/kie_tiger_eye_15s.py`, $0.041/s). Refs are the
   hero still plus the close-up stills; use a multi-shot prompt `Shot N (a-bs)` with quoted lines. No need to
   split under 15s. Add the crisp-articulation sentence to the audio block.
5. **Verify before showing:** whisper `small` on the full clip; any word under ~0.8 goes to `small` + `medium`
   on a sliced wav. A 2fps contact sheet (`fps=2,scale=144:-2,tile=10x3`) and scene cuts
   (`select='gt(scene,0.3)',showinfo`). Then save a loudnorm copy (`I=-16:TP=-1.5`, video stream copied) into
   the client's assets folder.

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

## Hands-only product ad (approved route)

Proven on Grace's Carpe Vanilla Peach tips ad (2026-10-01, `focusfiyah/Mymobileworld` → `ugc/carpe-vanilla-peach/`,
the best template: README, shots.json, kie.py, cut.py). One hand (reference sheet) is the only character; the
voiceover is a separate ElevenLabs track, so no lip sync and no on-camera speech.

1. **Research + script + voiceover first (free/cheap).** Pick the format from real data (tiktok-shop-coach skill),
   write to the client's rules, record the VO (eleven_v4), get word timings with scribe_v2, and cut a free timing
   animatic. Shot windows come from the word timings.
2. **Before the first paid still, ask:** product top/cap/label from a real photo, nail length/hand details, client.
3. **Still S1 first** (Nano Banana Pro on Kie, 1K 9:16, $0.09 = 18 credits): refs = hand crops + product crops.
   Show it, wait. S1 then doubles as the room reference for every later still (room continuity worked).
4. **Remaining stills on one sheet**, ask first ($0.09 each). Pin product shape in close-ups ("the same tall
   oval stick as in every other shot, not a short round jar"): macro prompts drift the shape.
5. **Hardest clip first** (Seedance 2.0 Mini, `first_frame_url` = the still, `generate_audio: false`, 720p 9:16,
   $0.041/s = 8.2 credits/s), then the rest in parallel. Clip length ≥ its VO window.
6. **Free cut** (`scripts/hands_cut.py`): trim each clip to its window (start offset when the action comes late,
   e.g. a cap tap), badge close-up insert cropped from a still over the claim words, CC0 SFX (knob ticks, cap tap)
   placed from timestamped frames (`drawtext=text='%{pts\:flt}'`), loudnorm -16 LUFS, 720x1280.

Kie runner (`scripts/kie_hands_runner.py`): balance check is free (`GET https://api.kie.ai/api/v1/chat/credit`,
1 credit = $0.005); it logs every taskId at submit (a killed run's result can be fetched with recordInfo), renders
clips in parallel threads with a locked log, and builds one preview sheet. Kie latency was 3-8 min per still:
run in the background with a ≥1h timeout, never a 10-min foreground call (one run was killed mid-task).
Traps: a nano-banana-pro *edit* barely changes small details (nails: first edit ~no change); a blur on the still
carries into the Seedance clip (good for a wrong label line); small label text comes out garbled or wrong
("1.7 FL OZ (350 mL)") → blur it on the still, free.

## On-camera demo over a voiceover (approved route)

Proven on Grace's Carpe Mountain Breeze ad (2026-10-01, `focusfiyah/Mymobileworld` → `ugc/carpe-mountain-breeze/`:
README, shots.json, kie.py, lipsync.py, cut.py; copies in `scripts/persona_*.py`, rename to kie.py / lipsync.py /
cut.py in the job folder). The person is an AI version of a real client from ONE photo; the voice is a separate
ElevenLabs track. Structure Ralph asked for: curiosity-loop hook → pain → selling point / solution → urgency CTA
(real reason, no false scarcity). Final: 35s, 9 shots, $6.60, of which ~$3.20 was footage that made the cut.

1. **Lock everything first** (see "Working with Ralph"): script, VO, shots, outfit, setting, which shots show the
   face, which face shots get lip sync, cost. Then record the VO (eleven_v4), STT word timings (scribe_v2), trim
   pauses to 0.25s (free; 38.6s → 35.0s) and set shot windows from the words.
2. **Stills** (Nano Banana Pro on Kie, $0.09): refs = person photo + product crops; the first approved still is the
   room/person reference for the rest. Relaxed brows in every prompt (raised brows = forehead wrinkles the clip
   copies). Outfit change later = an edit of the approved still, "change ONLY her top to the one in image 2"
   ($0.09, keeps the pose; `kie.py tee`).
3. **One test clip** (Seedance 2.0 Mini, $0.041/s), check it, then the rest one by one or in a small batch. Clip
   length ≥ its VO window: never stretch footage in the edit (Ralph: "why is the whole video in slow motion"), and
   Seedance already moves slowly. A pull-back from a close-up = `first_frame_url` (close-up) + `last_frame_url`.
4. **Lip sync the face shots** (`lipsync.py`, Kie `volcengine/video-to-video-lip-sync`, lite, $0.04/s of audio,
   one at a time: parallel calls get "server busy", $0). Mix the ORIGINAL voiceover, not the lip-sync audio.
5. **Cut** (`cut.py`, an edit list of clip pieces, free): whip-pan = xfade slideleft 0.24s + dblur + a noise
   whoosh; CC0 SFX; loudnorm -16 LUFS. QC (see above) before sending.

Traps, each paid for once:
- **The prompt TEXT beats the first frame.** Stills were edited to a grey tee but the identity text still said
  "sky-blue tank top": all 8 clips came back in the tank ($1.52). Grep every prompt block for the old look.
- **A product description in the prompt puts the product in the shot.** "No deodorant in this shot" lost to the
  identity block's stick description ($0.41). For product-free shots, drop the product text (`no_product` in shots.json).
- **A clean first frame does not survive a busy prompt either:** Seedance added a giant stick in the foreground of a
  "dry shirt" shot. Fix in text, not with a reroll.
- **Voiceover + face on camera reads as "her lips aren't moving".** Ralph rejected chin-down crops (they cut the
  product off) and chose lip sync.
- **Lip sync smears whatever passes the mouth** (the stick as she lowers it: flattened top, skin-coloured blob) and
  runs ~2 frames late. Fix free: keep the lip-synced mouth in a soft oval over the original frames (shifted 2
  frames), or jump-cut past the crossing and lip-sync only the clean part ($0.04). Swapping whole frames to the
  original makes the mouth stop mid-word, which Ralph spotted.
- **Free fixes that worked:** shallow-focus background blur on a still with normalized convolution (no orange halo
  around the product); blue→grey recolor with the label protected by a mask; chin-down crops for demo shots; skin-only
  bilateral smoothing for forehead lines; mirrored punch-in jump cut to fill a short clip.
- **Label text garbles at small sizes**; the logo and colour panel read. Use the real packshot or a sharp close-up still
  for label moments.

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
