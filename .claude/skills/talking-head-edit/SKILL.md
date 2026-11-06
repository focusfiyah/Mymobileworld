---
name: talking-head-edit
description: Edits a raw talking-head recording (Ralph's own videos, voice-over takes, reels, Shorts, Day One AI explainers) by cutting dead air and retakes from a word-level transcript, with Nate Herk's measured short-form editing playbook (pacing, B-roll, captions, sound). Use when Ralph says "cut the silences", "remove my mistakes", "edit this recording", "tighten this up", "make this a reel", or sends raw footage of himself talking. For Grace's AI product ads use ugc-product-ad (no captions or on-screen text there); for HyperFrames motion graphics use hyperframes; for transcripts use transcribe.
---

# Talking-head edit

Raw takes are full of dead air, stutters and re-recorded lines. This skill cuts them from the transcript so every cut lands
between phrases, never inside one, and gives the pacing numbers that Herk measured on his top reels.

## Steps

1. Transcribe with word timings: `python3 <transcribe skill>/scripts/transcribe.py FILE --out DIR`. It writes
   `transcript_words.json` (`{words:[{text,start,end}]}`), the shape the scripts below read. Check names and numbers.
2. Silences: `node scripts/cut-silences.mjs DIR/transcript_words.json --video FILE` (plan only; add `--apply` to render).
   Rules and flags: [references/cut-silences.md](references/cut-silences.md).
3. Mistakes and retakes: `node scripts/find-cut-candidates.mjs ...` lists candidates, you review each, then
   `scripts/apply-cuts.mjs`. Steps: [references/cut-mistakes.md](references/cut-mistakes.md).
4. Story, B-roll, captions, sound: [references/editing-playbook.md](references/editing-playbook.md), hook and payoff:
   [references/curiosity-and-entertainment.md](references/curiosity-and-entertainment.md), final checks:
   [references/quality-gates.md](references/quality-gates.md).
5. Before it goes to Ralph: delivery check with the `ffmpeg-skill` (`check.py --platform tiktok|reels|shorts`).

Done when: the cut has no clipped words (listen at every cut), the sync check passes, and the delivery check passes.

## Rules

- Never speed the voice up; cut between phrases at real silence. Why: Herk's rounds clipped "First" when a filler was cut
  next to it (playbook, "Lessons that cost us time").
- Ralph's rules override the playbook: no on-screen text or captions unless he says yes for that video; House of Rameau keeps
  the hook text but no captions; the AI finish and the hook-from-frame-0 check apply to AI video. Why: Mymobileworld CLAUDE.md.
- Transcription is local (`transcribe`), not ElevenLabs Scribe, which Herk's kit defaults to and which costs credits.
- The playbook mentions HyperFrames skills and Herk's own accounts; use our `hyperframes` skills for motion graphics.

## Files

- `scripts/`: `cut-silences.mjs`, `find-cut-candidates.mjs`, `apply-cuts.mjs` (node 22, ffmpeg; no network, read before use).
- `references/`: the five files above. Source and licence: `SOURCE.md`, `LICENSE`.
