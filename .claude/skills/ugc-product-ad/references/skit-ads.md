# Multi-character skit ads

## Contents

- Multi-character skit ads (approved route)
  - Steps
  - Patch a spoken line (audio only)
  - Cheap verification (every clip)
  - Traps hit on this route
  - Fix a line after the render (no video spend)
  - Before any paid render: pre-flight the first frame
  - Cost reference (720p, 9:16)
  - In Cowork or on another machine

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
