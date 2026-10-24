---
name: free-assets
description: Ralph's list of free sources for stock video clips, photos, music, sound effects, emoji and overlay art, with what each is good for and the licence check before use. Use when any job, client ad (Grace), Day One AI video or personal project needs b-roll, a stock photo or sticker, background music, a sound effect, an emoji, a room background for a still or clip, or when Ralph says "b rolls", "archive.org", "resources", "free stock", "Mixkit", "Pixabay", "Pexels", "different rooms", "room backgrounds", "where do we get a sound/clip/photo". For generating media with AI use ugc-product-ad or media-use; for HyperFrames catalog assets use media-use.
---

# Free assets

Ralph wants one list of free asset sources that every job uses, his own and his clients', not just Grace's.
Add a source here when he gives one; check this list before paying for generation or going searching.

## Sources

| Source | Gives | Notes |
|---|---|---|
| https://mixkit.co/ (added 2026-10-14) | stock video, music, sound effects, video templates, art; no account | Each item type has its own licence (https://mixkit.co/license/). Terms NOT read yet (pop-up behind a cookie banner): read the item's licence before first use, then record the result under Licence checks below. Never use a "Restricted" video. |
| broll MCP: archive.org public-domain film (added 2026-10-24) | b-roll clips cut to length while editing: old, mostly black-and-white SD film (Prelinger, NASA, newsreels) | Tools `search_footage` → `inspect_item` (keyframe per scene, pick by looking) → `extract_clip` (1-60 s, verified) with a provenance JSON per clip; copy both into the job. Use only clips with `commercial_use: "allowed"` in a monetized video. Fits Day One AI and Ralph's retro/space/history cutaways; Grace's bright modern ads take the stock sources above first. Setup and review: Mymobileworld CLAUDE.md (broll-mcp) and `tools/broll/SOURCE.md`. |
| Microsoft Fluent 3D emoji (MIT) | premium 3D emoji for overlays | `cdn.jsdelivr.net/gh/microsoft/fluentui-emoji@main/assets/<Name>/3D/<name>_3d.png`, 256px: never enlarge past about 1.2x. No emoji for a word: offer a free stand-in from the same set first (source: grace/PLAYBOOK.md §4 overlays). |
| Pexels | room backgrounds | Needs `PEXELS_API_KEY` (env var). Pexels License: free commercial use, no attribution. |
| Pixabay | room backgrounds, isolated photos (stickers) | Needs `PIXABAY_API_KEY` (env var); an invalid key returns HTTP 400. Photos may carry a brand logo: remove it by masking and inpainting, never a flat fill (Wag Bag r4). |
| StockSnap | isolated photos | Page can 403; the files load from `cdn.stocksnap.io/img-thumbs/960w/<ID>.jpg`. |
| Day One AI sound folder (focusfiyah/Dayone-ai, assets, sfx) | CC0 click and transition sounds | Licence is the LICENSE.md file in that folder. |

Pexels was tried for a portable generator sticker on 2026-10-06 and had nothing usable.

## Room backgrounds

When a job needs rooms (ad stills, hand-free plates, Day One AI or personal video), look for real Pexels and Pixabay
photos first, never the all-white rooms Claude kept defaulting to. When no real room fits the shot, AI rooms are fine:
re-run with `--allow-ai` (Pixabay's AI rooms), then a generated room (Ralph's Gemini app first, $0; a paid still only
with the cost asked). Why: Ralph, 2026-10-22: "use instead of the white theme backgrounds you always choose", and
"AI generated rooms are ok. Just go with real rooms 1st if they are not good then go with ai generated rooms". Rooms
with colour also make each video look different (TikTok flags reused footage).

`python3 scripts/rooms.py <job>/rooms "sage green bathroom" "terracotta kitchen" ...` keeps portrait photos of real
rooms with no people or pets, skips Pixabay's AI-flagged images (unless `--allow-ai`), rooms whiter than `--max-white` (pale share 0.6)
and dark ones, and writes `cand/`, `cand.json` (source page, licence) and a numbered `contact.jpg`. Name a colour or
material in every query; "bright" alone brings back white rooms.

Done when: each video has its own rooms (none shared between videos), every room is bright but has colour, you have
looked at the contact sheet and dropped crowded or branded shots (AI rooms that slipped past the flag are
fine only when no real room fits), and the job's `rooms/SOURCES.md` lists file, video, source page and licence for each
(template: Mymobileworld `ugc/space-heater-ptc/rooms/SOURCES.md`). The room goes into the still as a reference image;
the product still comes only from its real photo and reference sheet (source: Mymobileworld CLAUDE.md, product lock).

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
