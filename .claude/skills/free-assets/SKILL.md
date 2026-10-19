---
name: free-assets
description: Ralph's list of free sources for stock video clips, photos, music, sound effects, emoji and overlay art, with what each is good for and the licence check before use. Use when any job, client ad (Grace), Day One AI video or personal project needs b-roll, a stock photo or sticker, background music, a sound effect, an emoji, or when Ralph says "resources", "free stock", "Mixkit", "Pixabay", "where do we get a sound/clip/photo". For generating media with AI use ugc-product-ad or media-use; for HyperFrames catalog assets use media-use.
---

# Free assets

Ralph wants one list of free asset sources that every job uses, his own and his clients', not just Grace's.
Add a source here when he gives one; check this list before paying for generation or going searching.

## Sources

| Source | Gives | Notes |
|---|---|---|
| https://mixkit.co/ (added 2026-10-14) | stock video, music, sound effects, video templates, art; no account | Each item type has its own licence (https://mixkit.co/license/). Terms NOT read yet (pop-up behind a cookie banner): read the item's licence before first use, then record the result under Licence checks below. Never use a "Restricted" video. |
| Microsoft Fluent 3D emoji (MIT) | premium 3D emoji for overlays | `cdn.jsdelivr.net/gh/microsoft/fluentui-emoji@main/assets/<Name>/3D/<name>_3d.png`, 256px: never enlarge past about 1.2x. No emoji for a word: offer a free stand-in from the same set first (source: grace/PLAYBOOK.md §4 overlays). |
| Pixabay | isolated photos (stickers) | Needs `PIXABAY_API_KEY` (env var); an invalid key returns HTTP 400. Photos may carry a brand logo: remove it by masking and inpainting, never a flat fill (Wag Bag r4). |
| StockSnap | isolated photos | Page can 403; the files load from `cdn.stocksnap.io/img-thumbs/960w/<ID>.jpg`. |
| Day One AI sound folder (focusfiyah/Dayone-ai, assets, sfx) | CC0 click and transition sounds | Licence is the LICENSE.md file in that folder. |

Pexels was tried for a portable generator on 2026-10-06 and had nothing usable.

## Using a source

Done when the asset is in the job folder, its source URL and licence type are written in the job README, and any
brand logo, face or readable text in it is cleared or approved by Ralph.

- Read the licence of the exact item type before first use. Why: Mixkit and others license video, music and
  sound effects separately, and music is the type most likely to carry claim or attribution rules on TikTok and YouTube.
- A stock clip must look different in every video and never replaces a shot the spoken words need. Why: Ralph's
  rule that no two videos share footage (TikTok flags it).
- Day One AI: no music until its licence is checked for monetized use (focusfiyah/Dayone-ai CLAUDE.md). Mixkit music
  is the first thing to check for that.

## Licence checks

(none recorded yet: add `date, item type, what the licence says, attribution needed yes/no` here)
