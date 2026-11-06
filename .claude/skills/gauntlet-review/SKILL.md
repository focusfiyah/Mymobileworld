---
name: gauntlet-review
description: Runs an independent-critic review loop on a rendered video (a fresh agent judges the actual render, another verifies each fix, a ledger keeps the proof) and gives measured quality checks for frozen time, loudness and audio mix. Use before a Day One AI video, Short, story reel or Ralph's own AI video goes to Ralph, or when Ralph says "review loop", "critic", "gauntlet", "is this good enough to ship", "check the audio levels". For Grace's ad QC use ugc-product-ad and its qc scripts; for per-second logic checks use reference-breakdown.
---

# Gauntlet review

The builder cannot judge its own cut: it remembers what it meant, not what is on screen. A fresh critic that sees only the
render finds the pops, collisions and dead seconds that a builder skims past. From the Gauntlet loop, via echris6's Motion Video Kit.

## The loop

1. State the outcome and the bar first ([references/quality-bar.md](references/quality-bar.md)).
2. Render. Start a FRESH agent (`Agent` tool) per review with only the video path, the brief and Ralph's own words; never your
   reasoning or what you think you fixed. Prompts: [references/critic-prompts.md](references/critic-prompts.md).
3. Fix the largest gap first. Then a NEW critic checks each earlier item as FIXED / PARTLY / STILL PRESENT and looks for regressions.
4. Stop at the bar, at diminishing returns, or when Ralph says. Keep a ledger (round, top findings, changes, measured result).
   Full rules: [references/gauntlet.md](references/gauntlet.md). Audio mix targets: [references/audio.md](references/audio.md).

Done when: the last critic says SHIP, the measured checks in the quality bar pass, and the ledger is in the job folder.

## Rules

- Critic agents cost tokens: use this for videos headed to Ralph or to the channel, not for every small fix. Why: Ralph's low-token rule.
- Critics judge pixels and measurements; the bar's numbers come from scripts, not opinion.
- `scripts/frozen-time.sh`, `loudness.sh`, `contact-sheet.sh` are short ffmpeg wrappers. Read them, then run them on a copy;
  they were read but NOT run when this skill was added (the auto-mode check blocked it, 2026-11-06). Run once and note the result in CHANGELOG.md.
- Ralph's rules still win: no on-screen text on Grace ads, bright neutral grade, AI finish.

## Files

- `references/`: gauntlet loop, critic prompts, quality bar, audio. `scripts/`: three measuring wrappers. `SOURCE.md`, `LICENSE`.
