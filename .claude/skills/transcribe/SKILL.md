---
name: transcribe
description: Transcribes speech from any video or audio file into text with word timings, free and offline-capable (faster-whisper, no API key, no credits). Use when Ralph sends a video or voice note to transcribe, says "transcribe this", "what do they say", "get the words from this video", "whisper", when a TikTok has no captions, or when a Telegram voice note or an X/Instagram video needs its words read. For TikTok links with captions use tiktok-shop-coach first (free, exact). ElevenLabs scribe_v2 is the paid fallback.
---

# Transcribe

Ralph keeps sending videos and voice notes whose words we need (references to copy, Telegram voice notes, rivals' ads).
Before this, a missing TikTok caption meant ElevenLabs credits or reading frames. Local Whisper costs $0.

## Route, cheapest first

1. TikTok link: `tiktok-shop-coach` `tiktok.py video <link>` gives TikTok's own captions (exact, free). Use them.
2. Anything else (file, X/Instagram video, voice note, TikTok with no captions): `python3 scripts/transcribe.py <file> --out <dir>`.
   First run installs faster-whisper in `~/.cache/transcribe-venv` and downloads the model (about a minute); after that a
   50 s clip takes seconds. Default model `small.en` (better with names and numbers); `--model base.en` is faster and rougher.
   Not English: `--model small --lang es`.
3. Only if the local result is clearly wrong (heavy music, accents) and Ralph OKs the cost: ElevenLabs `scribe_v2`
   (`tiktok.py compare <file> <file> --stt`; ask first, it uses credits).

It writes `transcript.txt`, `transcript_timed.txt`, `transcript_words.json` (flat word list for `talking-head-edit`) and `transcript.json` (word timings, the layout `reference-breakdown`'s
`measure.py` reads: run `python3 measure.py <ref dir> --force` afterwards to add pace to `measure.txt`).

Done when: the transcript exists and the numbers, names and product words in it were checked against the audio or frames.

## Rules

- Music-only or silent audio makes Whisper invent lines ("Thank you."). Check any line that sits over music against the frames.
  Why: tested 2026-11-06 on a 49 s demo; the model rendered "sloth" as "slaw" and filled a music stretch with one long segment.
- Video-model audio and ads: check names and numbers by ear or frame, never copy them in blind.

## Files

- `scripts/transcribe.py`: the tool (`--help`). Needs ffmpeg, python3 with venv and pip, network on first run only.
