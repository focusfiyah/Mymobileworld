---
name: day-one-looks
description: Gives every Day One AI video its own thumbnail look instead of one repeated template, and proves it with a measured sameness check against every earlier thumbnail, a text-fit check and a no-repeat rule for the layout. Built from the "Pixar to Clawd" prompt pack method (a swappable BRAND block, a famous format described by its parts, measure don't guess). Use when making or fixing a Day One thumbnail, when Ralph says the thumbnails or videos look the same, YouTube is flagging AI, template-based, repetitive or inauthentic content, "make it look different each time", "new look", "Pixar to Clawd", "prompt pack" or "BRAND block", or when writing a scene prompt for a channel intro or sting. For the rest of the video pipeline use day-one-ai; for animated compositions use hyperframes.
---

# Day One looks

All 25 thumbnails up to 2026-10-23 came from one template (cream panel, tilted screenshot, orange "JUST LAUNCHED"),
and three of them had titles running off the frame. YouTube's monetization policy treats generic, repetitive,
template-based uploads as inauthentic content, and a channel whose every upload looks alike reads that way. The
fix is one look per video that still carries the brand: the tool's own name and colour, the real page or result,
the D1 mark in a corner.

The method comes from a prompt pack Ralph shared, a 12-second "Pixar to Clawd" film written by Claude: only a
small BRAND block changes per film, the famous thing is described by its parts (so it reads at once and copies
nothing), and every look decision is measured before it ships. How each idea maps to Day One:
`references/formula.md`.

## Make a video's thumbnail

1. In `jobs/<slug>/job.json`, add a `look` block. Text falls back to `thumb_top` / `thumb_big` / `thumb_badge`
   and the picture to `thumb_url`, so `"look": {}` already works. Add what makes the better bands possible:
   `prompt` (the real prompt the video types, for `split` and `prompt`), `stat` + `stat_label` (one true number,
   for `number`), `image` (a saved picture of the tool's real output: the strongest thumbnail, since Day One opens
   on the result), `focus` ("60% 30%", where the result sits on the page). Every word on it must be true and
   shown in the video.
2. From the Dayone-ai root: `python3 .claude/skills/day-one-looks/scripts/looks.py render jobs/<slug>` renders
   three candidates in bands not used in the last five videos and writes `jobs/<slug>/_looks_sheet.png` with each
   one's shared-frame score. Look at the sheet at full size.
3. Pick: `looks.py render jobs/<slug> --band <band>` (or `--auto` for the least-alike candidate that fits). This
   writes `thumbnail.png` and records the band, accent and score in `data/looks.json`. `produce.py --final` does
   this step itself when the job has a `look` block (`look.band` if set, else `--auto`); `produce.py JOB.json
   --thumb` re-renders only the thumbnail.
4. `looks.py check jobs/<slug>` must print `CHECK_PASS`.

Done when: `looks.py check` passes for the job, you have looked at `thumbnail.png` at full size (no cookie box, no
bot-check page, the result visible, the title readable), and the daily list shows the thumbnail next to the draft.

## What the checks measure

- **Sameness:** the share of the frame (32x18 cells) whose average colour matches another thumbnail's within 30 RGB
  units. Limit 0.30. Calibrated on 2026-10-23: every pair of the 22 old template thumbnails shares 0.37 or more
  (`looks.py control`, the positive control); the first new looks shared 0.10 to 0.17 with their closest
  neighbour.
- **Band repeat:** the same band may not come back within five videos.
- **Text fit:** every title shrinks to fit its box down to a set minimum (80 to 160 px on the 1280 canvas, so
  it still reads at phone size); text that overflows, leaves the canvas or sits on the picture, badge or mark
  fails. `looks.py selftest` proves each band fits a real long title and that an absurd one fails.
- **Capture:** a page that answers with a bot check ("Verify you are human", Cloudflare) stops the render with a
  message instead of becoming the thumbnail (canva.com did, 2026-10-23); fixed cookie and consent boxes are hidden.

## Rules

- No AI-generated imagery in a thumbnail without Ralph's OK and its cost first; the default is $0 (the real page,
  real output, our type). Why: Ralph's standing paid-step rule, and a real result is what the policy rewards.
- Never put a claim, number or prompt on a thumbnail that the video does not show. Why: Day One's honest-tone
  rule (Dayone-ai CLAUDE.md); a misleading thumbnail also breaks YouTube's thumbnail policy.
- Swapping the thumbnail on a published video (`python3 yt.py thumb jobs/<slug>`) changes a live page: ask Ralph
  first.

## Adding a band

A band is one familiar format described by its parts (magazine cover, gig poster, sticky note on the screen). Add
it to `BANDS` in `scripts/looks.py` with its `needs`, give every text box the `fit` class and a `data-min`, mark
picture areas `avoid`, set its background in `BAND_BG`, then run `looks.py selftest` (must print `SELFTEST_OK`) and
look at the sheet from `selftest --out <dir>`.

## Files

- `scripts/looks.py`: render, check, control, selftest, bands (`--help`).
- `references/formula.md`: the prompt pack's six rules, follow-up habit and timeline idea, mapped to Day One.
- `templates/scene-prompt.md`: the prompt pack's structure as a fill-in prompt for a channel intro or sting
  (HERO, BAND, RESULT, SET, FORMAT, BEATS, CAMERA, LOOK, CHECKS).
