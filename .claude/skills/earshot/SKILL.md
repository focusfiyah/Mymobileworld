---
name: earshot
description: Lets Claude hear sound with earshot (free, local, MIT): a sound critique of a finished video (loudness, sync of sound to the cuts, too many or missing hits), picking or trimming a sound effect or music by description, real-vs-synthesized checks, and 252 free sound effects (whoosh, tick, pop, hit, ding) rendered by name and aimed at a moment in the picture. Use before saying how any audio sounds, when a reel, Short, Day One video or Grace cut needs sound effects or a sound check, or when Ralph says earshot, "give Claude ears", sound effects, whoosh, SFX, "check the sound", "is the audio off". For cutting, loudness fixes and exports use ffmpeg-skill; for free recorded sounds and music use free-assets.
---

# earshot

Claude cannot hear. Until 2026-11-07 every sound choice in our reels was a guess and the only audio check was a
loudness number. earshot (by Leon Lin, maker of unlazy) turns sound into readings Claude can act on, runs on CPU,
and keeps audio on the machine. Quote its numbers when reporting how something sounds.

## Setup (once per session)

`bash <skill-dir>/scripts/setup.sh` prints EARSHOT_SETUP_OK (~4 min cold: CPU torch + 1.1 GB of free models
from Hugging Face; seconds when already installed). Then run every command through `<skill-dir>/scripts/es`.
`--no-models` installs only what the sound bank needs. The bank (`sfx`, `kit`, `measure`) loads no models;
every other command loads them, ~20 s per call, so for many calls write one Python script with
`from earshot import api` using `~/.cache/earshot-venv/bin/python`.

## Check a finished video's sound

`es critique VIDEO.mp4 --video VIDEO.mp4 --out critique.json` scores the mix against 7 professional launch films
and lists timestamped fixes, most important first. `es timeline VIDEO.mp4 --video VIDEO.mp4` gives the
second-by-second listening transcript; `es sheet VIDEO.mp4 -o sheet.png` the same as a picture to read.

Read the fixes against the format: the reference films are music-led, so on a voice-led reel or Grace ad a
"no music" or "voice in 100% of windows" note is a style difference, not a fault. The useful ones there are
cuts with no sound on them, loudness, too many hits and a thin low end.

Done when: the critique ran on the final cut, each fix is applied or skipped with a reason, and the numbers
are in the review note.

## Add sound effects

`es sfx list --kind whoosh` (or `--category ui_pop`, `--kind hit`, `pop`, `click`, `note`) lists the bank;
`es sfx render ID -o x.wav [--dur 0.8 --apex 0.32 --pitch E5]` renders one in ~3 s and prints its measured
onset and peak, so the peak can be placed on the cut. For a whole video, `es kit init --preset launch`,
`kit render`, `kit check` (steps in `references/upstream-skill.md`, Loop 5). Re-run `critique` after adding them.

## Choose or trim a sound

`es rank "a soft wooden tap" folder/ --top 5`, `es find long.wav "one clean key press" --top 3` (trims in
seconds), `es describe x.wav`, `es match x.wav "description" --alts ...`, `es realness x.wav`.

## Rules

- Never run `es llm`: it uploads audio to Gemini. Why: Ralph's Gemini key is paid with no free tier
  (2026-10-20, 2026-11-01).
- Do not install the upstream `real-sound` skill without Ralph's OK. Why: it overlaps free-assets and our own
  mixing, and was not part of what he approved on 2026-11-07.

## Files

- `references/upstream-skill.md`: earshot's own skill, every command and loop in full (forge, fit, MCP server).
- `scripts/setup.sh`: install at the pinned commit. `scripts/es`: runs earshot from that install.
- `SOURCE.md`: where it came from, the review and the first test.
