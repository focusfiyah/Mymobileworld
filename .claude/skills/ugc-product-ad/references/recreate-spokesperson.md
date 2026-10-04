# Recreate a trending spokesperson video

## Contents

- Recreate a trending spokesperson video (approved route)

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
