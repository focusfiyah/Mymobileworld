---
name: ugc-take-combos
description: Edit a creator's REAL raw footage (separate hook, body and CTA files, several takes each) into many finished short ads by combining different takes, in the style of a finished reference video. Covers take inventory from transcripts, analysing the reference's cuts, overlays and pacing, dead-air removal that never clips words, alternating punch-ins, TikTok text bubbles, photo pop-ins, search-result "screenshot" cards, still previews for approval BEFORE any render, and verification (re-transcribe for dropped words, pause profile vs the reference, every overlay asserted visible). Use for "edit these takes", "hook / body / CTA", "make combos", "mix and match takes", "remove the pauses / dead air", "match this TikTok's style", "tighten the cuts", for Grace / Fungix / TikTok Shop creator edits and Ralph's own real-footage videos. Runs in Claude cloud sessions and on Ralph's PC. Not for generating footage with AI; that is the ugc-product-ad skill.
---

# UGC take combos

A creator films the script in three parts, each part several times: **hook** takes,
**body** takes, **CTA** takes. One finished ad = one hook take + one body take + one CTA
take, cut tight, styled like a reference ad the client already approved. N hooks × M
bodies × K CTAs gives many unique ads from one shoot.

The engine is `scripts/take_combos.py` (config-driven, proven on Fungix) and the art is
`scripts/overlay_art.py`. `examples/fungix_job.json` is a complete worked job. Run
`bash scripts/setup.sh` once per session (faster-whisper, numpy, Pillow; ffmpeg is on PATH in the
cloud), then `python3 scripts/take_combos.py ...`. On Ralph's PC the same commands work with any
Python that has those packages (set `PYTHONIOENCODING=utf-8` on Windows). Fonts resolve to the Windows
originals there and to Liberation Sans / bundled Open Sans in the cloud.

A job whose video sets are fixed by the client (one take set per video, emoji pops instead of cards)
can use a small job-specific `cut.py` instead; `ugc/wag-bag-v2/` in focusfiyah/Mymobileworld is the
cloud example (Grace, 2026-10-06). Either way the cutting and verification rules below apply.

## The client's rules (Ralph, learned the hard way)

1. **Still preview before ANY render.** Every visual choice (card design, text, overlay
   placement) is shown as a still composited on a real frame, picked, THEN rendered.
   `overlay_art.preview()` makes the sheet. Offer 4–5 real options, not one.
2. **Verify before sending, never after.** Every requested change must be measurably
   present before a file reaches Ralph. A missing card once cost him a full render cycle
   and real frustration ("these took so many hours"). `take_combos.py verify` is mandatory.
3. **Ask questions as you go**, batched with AskUserQuestion, recommended option first.
4. **Be token-mindful**: small contact sheets, measurements over watching, short updates.
5. **Never reuse the takes the published reference used** (usually take 1 of each part).
6. **No text on screen (bubbles, cards, captions) unless Ralph says yes for that video.** Why:
   Ralph 2026-10-05 after unasked hook text; `grace/gate.py --stage cut` blocks it without
   `text_overlay_ok` (source: Mymobileworld CLAUDE.md hard rule 6). Emoji or photo pops only when asked.

## Workflow

**1. Find and probe the sources.** In the cloud, put the raw files in the job's `src/` (Drive
download, or files Ralph shares into the session). Search by name, **never by "newer than"**: camera files
keep their original dates, and a date filter once hid the HD originals. Check the same
names in subfolders (Grace had 576p exports and 1080p `.MOV`s under the same names in two
folders). Probe each: resolution, bitrate, `color_transfer` (bt709 = fine; HLG/PQ needs
tone-mapping or it looks washed out). Prefer camera originals; a 576p/770kbps export can't
be rescued, so ask the client for originals rather than upscaling.

**2. Transcribe with word timestamps** (faster-whisper small.en, int8, CPU). The engine
caches `tx_<part>.json`. List the takes per part from the transcript and flag flubbed
takes ("These it's right there") and short variants. Takes are `[part, start, end]`
windows. If a newer file is the same recording (same duration), confirm by envelope
cross-correlation (≤1 frame offset) and reuse every take window unchanged.

**3. Analyse the reference** (ask before downloading it; yt-dlp works for TikTok). Build
a 4 fps contact sheet over its first 10s and 2 fps later. Note every overlay's type,
position and the WORD it enters and leaves on, plus the pause profile (`verify` prints the
reference's longest pauses; that is the tightness target). Crop reusable photo overlays
from the client's OWN reference and rebuild them from clean rectangles, since the edges
carry the background.

**4. Ask** (one batch): how many videos; export size (1080×1920); overlays to copy or
rebuild; hook text per video (different per video helps TikTok treat them as distinct);
whether body sub-sections can mix across takes (Grace: keep takes paired); punch-ins.

**5. Write job.json** (schema below), preview overlays as stills, get picks.

**6. Build with `--draft` first** (veryfast/crf22). Verify. Then the final (medium/crf17).

**7. Verify, then deliver.** Copy finals to the client's folder, byte-compare against the
render, and send. Files over 30 MB don't reach the phone; say so, and offer light copies.

## job.json

```json
{"name": "Fungix combo", "src_dir": "...", "work_dir": "...", "out_dir": "...",
 "reference": "reference.mp4", "zoom": 1.14,
 "parts": {"hook": {"video": "Fungix (hook).MOV", "audio": "Fungix part 1 clear.mp4"},
           "body": {"video": "FUNGIX (body).MOV"}, "cta": {"video": "FUNGIX (cta).MOV"}},
 "takes": {"H2": ["hook", 15.2, 29.5], "B5": ["body", 91.1, 112.1], "C2": ["cta", 10.5, 19.6]},
 "overlays": [ {"png": "card.png",
     "from": {"word": "has", "in": "body", "plus": 0.15, "after": {"word": "oil", "in": "body", "edge": "end"}},
     "to": {"dur": 4.6, "cap_section": "body"}} ],
 "videos": {"V1": {"takes": ["H2", "B5", "C2"], "overlays": [
     {"bubble": ["somebody had to say it", "about the toenails…"], "from": {"t": 0},
      "to": {"word": "sorry", "in": "hook", "plus": 1.2}}]}}}
```

- `audio` overrides a part's audio track (Grace's cleaned "clear" hook audio on HD picture).
- Anchors: `{"t": s}` absolute · `{"word": w | [w1, w2], "in": part, "edge": "start"|"end",
  "plus": s, "after": anchor}` = first match at or after `after` · `to` may be
  `{"dur": s, "cap_section": part}`. Anchoring on words keeps overlays in sync on every
  take, whatever its pace.
- Per-video overlays draw underneath shared ones. `bubble` renders a TikTok text bubble.

## How the cutting works (don't "simplify" this, every rule fixed a real miss)

- **Whisper says WHERE the words are; the audio says where a cut lands.** Whisper stretched
  "who" 3s back across a pause, timed "baby" 0.5s early, and mistimes soft onsets
  ("S-orry") and trailing sibilants. Cutting on whisper word gaps left 0.8s of dead air
  after "fungus" that the client caught.
- **Rolling room-tone floor** (5th percentile over ±3s). One global floor misfired where
  the room noise drifted, leaving a 0.4s tail.
- Speech = level > floor + 16 dB, **or** inside a whisper word that peaks > floor + 12 and
  only on frames > floor + 6 (protects a soft "Who" without protecting silence).
- Quiet longer than 0.18s becomes a cut; any near-silence ≥ 0.30s is cut even inside a
  "word"; 0.04s of breath is kept either side.
- Trims to the words (lead 0.12s, **tail 0.23s**: 0.15s clipped the "s" off "worse", tested
  by transcribing candidate cut points) may **only remove quiet audio, never speech**.
- Alternate 1.0 / 1.14 punch-ins on every cut. On a 1080p source, a punch-in is a crop of
  the native frame (light unsharp on crops only). On a low-res source, crop at source
  resolution and upscale ONCE with lanczos + unsharp 0.8, which beats uploading native.
- 15/25 ms audio fades at every cut (no clicks); loudnorm −14 LUFS at the end.

## Verification (`take_combos.py verify job.json`)

- **Dropped words** = `delete` ops when the output transcript is diffed against the source
  takes. Must be none. Replacements are almost always ASR noise (cart→car, baby→maybe);
  if one looks like a clip, transcribe the source at candidate cut points to prove it.
- **Pauses**: longest gaps (local-floor measure) vs the reference. Target ≤ reference (≈0.45s
  on Fungix); the client's hard ceiling is 1s.
- **Overlays visible**: each window's mid-frame is diffed against the un-overlaid
  `base.mp4`. Mean pixel change < 2 = missing. This exists because a card silently fell
  out of the overlay list during a redesign.

## Overlays and compliance

- Card designs in `overlay_art.py`: `card_dark` (A, the reference's dark result panel,
  **approved on Fungix**), `card_light` (B), `card_ai_overview` (C), `card_phone_search`
  (D). Arial stands in for Roboto. Keep claim text to approved wording (health/supplement:
  "to target fungal growth and support healthier-looking nails", never cures/kills). A
  reference's card may make a stronger claim than approved; rebuild it, don't copy it.
- A condition-only photo collage is not a before/after, so check what a "before/after" in
  the reference actually shows before raising it.
- Drawing functions shared by preview and build mean the render cannot drift from what
  the client approved.

## Timing and cost

No generation spend: everything is local ffmpeg. A final 1080p render of 6 × ~38s takes
≈15 min, a draft much less. Segment cutting dominates, so rerun only what changed.
