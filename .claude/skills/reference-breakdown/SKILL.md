---
name: reference-breakdown
description: Measures a winning short video second by second (cuts, camera moves, pace, palette, caption boxes, sound effects, contact sheets) with free local ffmpeg tools, then checks our own cut against the same per-second logic gate before it goes to Ralph. Use when Ralph sends a viral TikTok, reel or Short to copy the feel of, says "break down this video", "measure the reference", "match its pacing", "per-second check", or before sending any cut for review. For why a post went viral use viral-reverse-engineering; for TikTok Shop data and `compare` use tiktok-shop-coach.
---

# Reference breakdown

A reference gets copied by impression and the copy plays flat: wrong pace, wrong camera rhythm, a dead second. This skill
turns the reference into numbers and gives every cut of ours a per-second check. Free, local, no credits.

## Measure a reference

1. Get the file (TikTok/Instagram: `tiktok-shop-coach` `tiktok.py video <link> --out <dir>`; other links: yt-dlp).
2. `bash scripts/breakdown.sh <file> <out dir>` (about 20 s for 50 s of video; needs ffmpeg, python3, numpy). It writes
   `info.txt`, `cuts.txt`, `sheets/` (one frame per second), `full/` (frames at each cut), `measure.txt` (camera move every
   0.5 s as HOLD/DRIFT/PAN/TILT/WHIP, palette, caption boxes, pace, loud non-voice moments = likely sound effects).
   `transcript.txt` needs a local Whisper; without one, take words from the tiktok.py transcript or read the frames.
3. Read every sheet in order, then the full-res frames. Fill the table in
   [references/read-the-reference.md](references/read-the-reference.md): per-second row, why each second holds attention,
   the numbers to match (cuts per minute, hold length, words per second, a new fact every n seconds).
4. Copy the format, change the content: same rhythm and camera grammar, our own shots, words and look. Never upload the
   reference's frames to a generation model (hard rule 6: every video different).

Done when: every second of the reference has a row, and the plan for our cut names the pace numbers it matches.

## Gate our own cut

Before a cut goes to Ralph, extract it at 2 fps (`ffmpeg -i cut.mp4 -vf fps=2 audit/%04d.png`), look at every frame at full
size and apply [references/logic-gate.md](references/logic-gate.md). Write the log from the frames, not the plan. This
sits beside the QC in `ugc-product-ad` and the word-to-picture match; it replaces neither.

Done when: each second is pass or has a fix, and nothing is absurd or dead.

## Files

- `scripts/breakdown.sh`, `scripts/measure.py`: the measuring tools (from Scenario, see SOURCE.md). Local only.
- `references/read-the-reference.md`: what to write down from a breakdown.
- `references/logic-gate.md`: the per-second logic and entertainment checks.
