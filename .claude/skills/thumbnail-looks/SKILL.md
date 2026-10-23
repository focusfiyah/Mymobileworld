---
name: thumbnail-looks
description: Gives every video its own thumbnail or cover look instead of one repeated template, on any channel (Day One AI on YouTube, Grace, House of Rameau, Ralph's own videos, future clients), in 16:9 or 9:16, and proves it with a measured sameness check against the channel's earlier thumbnails, a text-fit and safe-zone check and a no-repeat rule for the layout. Built from the "Pixar to Clawd" prompt pack (a swappable BRAND block, a famous format described by its parts, measure don't guess). Use when making or fixing any thumbnail, YouTube thumbnail, Shorts or TikTok cover, when videos or thumbnails "look the same", when YouTube or TikTok flags AI, template-based, repetitive or inauthentic content, "make it look different each time", "new look", "Pixar to Clawd", "prompt pack", "BRAND block", or for a scene prompt for a channel intro or sting. For the Day One pipeline use day-one-ai; for Grace's ad footage use ugc-product-ad; for animated compositions use hyperframes.
---

# Thumbnail looks

A channel whose uploads all look alike reads as template-made: YouTube's monetization policy treats generic,
repetitive, template-based uploads as inauthentic content, and TikTok flags reused-looking posts. All 25 Day One
thumbnails up to 2026-10-23 came from one template, and three had titles running off the frame. This skill gives each
video its own look that still carries the channel: the subject's own name and colour, its real page, product or
result, and the channel's mark if it has one.

The method comes from a prompt pack Ralph shared, a 12-second "Pixar to Clawd" film written by Claude: only a small
BRAND block changes per film, the famous thing is described by its parts (so it reads at once and copies nothing),
and every look is measured before it ships. How each idea maps over: `references/formula.md`.

When to use it (Ralph 2026-10-23): on Day One, for every video, automatically; outside Day One (Grace, House of
Rameau, Ralph's own videos, new clients), only when Ralph calls for it ("Will use this skill when called for on
anything outside Day One").

## Make a look

A target is a Day One job folder (`jobs/<slug>`, run from the Dayone-ai root, `look` block in job.json) or a spec
file for anything else (format at the top of `scripts/looks.py`: name, out, size `16:9` or `9:16`, top, big, badge,
image or url, focus, prompt, stat, pool of earlier thumbnails, ledger, mark). Keep one ledger and one pool per
channel, so each channel is compared with its own history.

1. Fill the words and the picture. The strongest picture is the real result or the real product (a saved image or
   a still from the video); a web page works too. For a photo, set `focus` on the product ("45% 78%"); for a page it
   defaults to the busiest part. Add `prompt` (for the split and prompt bands) or `stat` + `stat_label` (number band)
   when the video has a real one. Every word must be true and shown in the video.
2. `python3 <skill-dir>/scripts/looks.py render TARGET` renders three candidates in bands not used in the channel's
   last five, plus a `_looks_sheet.png` with each one's shared-frame score. Look at it at full size.
3. `looks.py render TARGET --band <band>` (or `--auto`) writes the final image and records it in the ledger. On Day
   One, `produce.py --final` does this when the job has a `look` block; `produce.py JOB.json --thumb` redoes only it.
4. `looks.py check TARGET` must print `CHECK_PASS`.

Done when: `looks.py check` passes, you have looked at the image at full size (no cookie box, no bot-check page, the
result or product visible, the title readable) and it sits on the job's review page.

## Where it applies

| Channel | Size | Notes |
|---|---|---|
| Day One AI (YouTube) | 16:9 (+ 9:16 for Shorts) | Every video; wired into produce.py; ledger `data/looks.json`, D1 mark |
| Grace, House of Rameau (TikTok) | 9:16 cover | When Ralph asks. Text on a cover is on-screen text: only when Ralph says yes for that video (source: Mymobileworld CLAUDE.md hard rule 6). Without text, the layouts still vary the framing of the product still. |
| Ralph's own or a new client's YouTube | 16:9 | When Ralph asks; own pool, ledger and mark per channel |

## What the checks measure

- **Sameness:** the share of the frame (32x18 cells; 18x32 for 9:16) whose average colour matches an earlier
  thumbnail's within 30 RGB units. Limit 0.30. Calibrated 2026-10-23: every pair of the 22 old Day One template
  thumbnails shares 0.37 or more (`looks.py control`, the positive control); the first new looks shared 0.08 to 0.16.
- **Band repeat:** the same band may not come back within five looks on that ledger.
- **Text fit and safe zones:** each title shrinks to fit its box down to a floor that still reads at phone size;
  text that overflows, sits on the picture, badge or mark, or leaves the safe area fails. Safe areas: on 16:9, clear
  of the bottom-right corner where YouTube prints the video length (the first three Day One looks had the D1 mark
  there); on 9:16, inside the middle 3:4 that TikTok's profile grid shows and clear of the like/share rail.
  `looks.py selftest` proves every band fits a real title at both sizes and that an absurd one fails.
- **Capture:** a page that answers with a bot check stops the render with a message (canva.com did, 2026-10-23);
  cookie and consent boxes are hidden. The loupe never magnifies past 1.2x the source pixels, so a small photo makes
  it a spotlight rather than a zoom.

## Rules

- No AI-generated imagery in a look without Ralph's OK and its cost first; the default is $0 (real pages, real
  stills, our type). Why: Ralph's standing paid-step rule, and the real thing is what the policies reward.
- Never put a claim, number or prompt on a thumbnail that the video does not show. Why: Day One's honest-tone rule;
  a misleading thumbnail also breaks YouTube's thumbnail policy.
- Changing the thumbnail or cover of a published video changes a live page: ask Ralph first.

## Adding a band

A band is one familiar format described by its parts (magazine cover, gig poster, sticky note). Add it to `BANDS` in
`scripts/looks.py`: `html` for 16:9 and `v` for 9:16, every text box with the `fit` class and a `data-min`, picture
areas marked `avoid`, its background in `BAND_BG`. Then `looks.py selftest --out <dir>` must print `SELFTEST_OK`;
look at both sheets it writes.

## Files

`<skill-dir>` is the folder holding this SKILL.md.

- `scripts/looks.py`: render, check, control, selftest, bands (`--help`; spec format in its docstring).
- `references/formula.md`: the prompt pack's six rules, follow-up habit and timeline idea, mapped to thumbnails.
- `templates/scene-prompt.md`: the prompt pack's structure as a fill-in prompt for a channel intro or sting.
