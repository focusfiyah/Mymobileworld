---
name: tiktok-shop-coach
description: Free TikTok Shop affiliate coach (no paid subscription). Breaks down any TikTok from a link (video, exact transcript, hook frames; why it worked or flopped), shows a daily board of the fastest-rising TikTok Shop videos with the product each sells, A/B compares a viral video with yours, checks a script's reading level, finds top videos for a keyword or hashtag without a login, lists TikTok Shop products with price, lifetime units sold and rating, and writes hooks and scripts modeled on proven videos. Use when someone pastes a TikTok link, asks why a video flopped, wants hooks or a script for a TikTok Shop product, asks what to film or which product to push, asks what's viral or trending on TikTok Shop today, wants viral videos in a niche, wants to compare their video to a viral one, mentions BMC Coach, Brands Meet Creators, The Daily Virals, Kalodata or FastMoss, or says "TikTok Shop coach".
---

# TikTok Shop coach

Built 2026-10-01 for Ralph as a free alternative to the "BMC Coach" (Brands Meet Creators) Claude connector, after
watching two TikToks that sell it. That connector does four things: product research on live sales data, reading the
creator's own showcase, pulling the top-earning videos in a niche, and diagnosing flops. This skill covers everything
that doesn't need a private sales database. Be upfront about the rest (see **Limits**). Never present a guess as data.

Extended the same day as a free alternative to **The Daily Virals** (thedailyvirals.com, paid): its daily "most viral"
TikTok Shop video board, transcripts, A/B compare and readability checker are covered here (workflow 0, `compare`,
`readability`). Its "Highest GMV" and "Top LIVEs" tabs need sales and LIVE data this skill can't get.

## Tools

`scripts/tiktok.py` (Python + Playwright + ffmpeg; no login, no API key, free):

```bash
S=.claude/skills/tiktok-shop-coach/scripts/tiktok.py     # path relative to the repo root
python3 $S viral --days 3 --top 20 --out <scratch>/tt    # today's fastest-rising TikTok Shop videos + their products
python3 $S video <link> [<link> ...] --out <scratch>/tt  # meta.json, transcript(_timed).txt, video.mp4, hook.png, sheet.png
python3 $S compare <viral-link> <your-link-or-file> --out <scratch>/tt   # A/B: hook frames, pace, cuts, transcripts
python3 $S readability "<script text>"                   # reading grade + long sentences + hard words
python3 $S tag <hashtag> --days 30 --top 15 --out <scratch>/tt   # top recent videos on a hashtag page, by views
python3 $S discover <discover-url> [...] --top 15 --out <scratch>/tt   # videos on TikTok keyword pages, by views
python3 $S shop <keyword> --top 20 --out <scratch>/tt    # TikTok Shop products: price, lifetime units sold, rating
```

- Short share links (`tiktok.com/t/...`) work. Write output to the scratchpad, not the repo.
- Read `transcript.txt` for the words and `transcript_timed.txt` for timing. **Look at** `hook.png` (frames at 0–3 s) and
  `sheet.png` (whole video) with the Read tool. The hook is usually on-screen text plus the first spoken line plus the
  first visual, so read all three.
- No `transcript.txt` means TikTok has no captions for it. Then say so and work from the frames, or (only after
  telling the user it uses ElevenLabs credits) transcribe the file: `compare <file> <file> --stt` does it for local
  files (ElevenLabs `scribe_v2`; the proxy adds the key in Ralph's cloud env).
- `viral` scans 8 shop-heavy hashtags (`--category beauty|home|fashion|holiday|gifts` swaps in that category's tags,
  `--add-tags` adds niche ones, `--discover` adds keyword pages), keeps videos TikTok flags as shop videos, posted in
  the last `--days`, and ranks by average views/day since posting. TikTok includes the linked product (title,
  category, shop link) for almost all of them. **Views gained today** needs two runs: the script saves each run's
  view counts to `--state`, and a later run (1 h+) ranks by views gained since then (marked `+`). The container is
  wiped between sessions, so for day-over-day growth keep the state file somewhere that lasts, or run it twice in a
  session (morning and afternoon). Hashtag pages vary from load to load: it's a big sample, not all of TikTok.
- `compare` takes links or local video files (e.g. a draft before posting). Cuts = hard scene changes (ffmpeg scene
  detection), so a smooth handheld video counts few. Local files have no captions without `--stt`.
- **Keyword search without a login = web search + `discover`.** tiktok.com search needs a login, but TikTok publishes
  keyword pages (`tiktok.com/discover/<slug>`, ~16 videos each) that load without one. They exist only for keywords
  TikTok already created (a made-up slug redirects home), so find them first with the WebSearch tool:
  `site:tiktok.com/discover <product or keyword>`, plus variants (`<product> tiktok shop`, `<product> review`). Pass
  the 2–3 most relevant URLs to `discover` (~1 min per page, it fetches each video's stats). WebSearch sometimes
  returns direct `/video/` links too: run those through `video --no-media` for stats. Search engines don't index every
  TikTok, so this finds the established winners, not every video. Combine with `tag` for the newest ones.
- `shop` works for any keyword. `sold` is **lifetime** units sold, shown by TikTok on the product card. It is not
  recent sales, GMV, commission or affiliate count. A product with a low lifetime count and a burst of recent viral
  videos is newer or rising; a huge count can be years of sales.
- Not possible headless (tested 2026-10-01): tiktok.com search (login), a profile's video list (empty body), product
  detail pages (captcha). For a specific creator, ask for the video links.
  Re-tested 2026-10-06 with plain HTTPS: comments (`https://www.tiktok.com/api/comment/list/?aweme_id=<id>&count=20&cursor=0&aid=1988`, only the first few, no login) and search suggestions (`/api/search/general/preview/?keyword=<q>&aid=1988`) DO work; search results, post lists and related videos return empty bodies; product pages show a captcha.
- The script imports every proxy CA into Chromium's trust store itself. Before that fix, pages failed at random with
  `ERR_CERT_AUTHORITY_INVALID`. If that error still shows up, run `bash setup.sh` in the Dayone-ai repo.
- No browser available (e.g. the claude.ai chat app)? Ask the user to paste the caption/transcript and screenshots of
  the first second and the analytics, and continue from those. Or suggest running it in a Claude Code session.

## Workflows

Read `references/playbook.md` before the first breakdown or script in a session. It holds the hook types, script
frameworks, buyer-psychology levers, the breakdown checklist and the product scorecard used below.

### 0. "What's going viral on TikTok Shop today?" (the Daily Virals board)
1. Run `viral` (add `--category` if they named a niche). ~2 min.
2. Show the top 10–15 as a short list: product, views/day (or `+` gained), age, creator, link. Group repeats: the
   same product in several top videos is the strongest signal that the product, not one creator, is selling.
3. Pick the 2–3 most useful for the user and run `video` on them: what the hook does, why it travels.
4. Offer the next step: model one (same framework, their product, never word for word), check the product with
   `shop <product name>`, or `compare` their draft against the winner.
5. Their saved list ("sandbox") lives wherever they want it: a doc, a note, or the JSON the script writes.

### A/B compare ("why does mine do worse than this one?")
Run `compare <viral> <theirs>`, look at `compare.png` and read `compare.md`. Report the differences that matter
most, in this order: what's in frame and said in the first second, time to the first word, pace (words/sec,
cuts/10 s), length, the proof moment, the CTA. Then 3 concrete changes for their video.

### Script check
Run `readability` on any script before handing it over (yours or theirs). Grade 6 or lower, sentences under ~15
words. Rewrite the flagged long sentences and swap the hard words for everyday ones.

### 1. "Why did this work?" / "Why did my video flop?"
1. Run `video` on the link(s). Read the meta, transcript and both images.
2. Give the breakdown in the playbook's order: hook (0–3 s: words, text, visual), structure beat by beat with
   timestamps, proof/demo moment, CTA, numbers in context (views vs the creator's followers, engagement %, save %).
3. For the user's **own** flop, ask for a screenshot of that video's retention graph and traffic sources from TikTok
   Studio / analytics. Only the poster can see those. Read where the curve drops and match the second to the
   transcript. Without the screenshot, say the drop-off points are your read of the video, not their data.
4. End with 3 concrete fixes, each tied to a moment in the video, plus a rewritten hook.

### 2. "What's working in my niche?" / "Find viral hooks for <product>"
1. Find videos two ways and merge them:
   - Keyword: WebSearch `site:tiktok.com/discover <product/keyword>` → `discover` on the 2–3 best pages.
   - Hashtag: 1–3 tags (product name squashed, niche tag, e.g. `adventcalendar`, `tiktokshopfinds`) → `tag --days 30`.
2. Shortlist by views and by save % (saves suggest buying intent better than likes). Prefer creators whose views far
   exceed their follower count. That points to the content, not the audience.
3. Run `video` on the top 3–5 and break them down. Pull out the shared hook pattern, format and length.
4. Hand back: the links (so the user can watch them), the patterns, and hooks adapted to their product.

### 3. "Which product should I push?" / "What sells in <niche>?"
1. Run `shop <keyword>` for the niche or product type: price, lifetime units sold, rating, reviews per product.
2. For the top candidates, run workflow 2 (discover + tag) to see content demand: how many recent videos, how big,
   from small or big creators. Many units sold but few recent videos = room for a new affiliate.
3. Commission % and sample availability aren't public. Ask for a screenshot of the affiliate/creator marketplace
   listing, and of their showcase for "what should I film from my showcase".
4. Score with the playbook's scorecard, rank, and give the reason for each rank. Label every number with where it
   came from: TikTok Shop page (lifetime sold, price, rating), TikTok video pages (views, saves), their screenshot,
   or your estimate.

### 4. "Write me a script"
Confirm product, price, commission if known, the audience, and whether they show their face (or it's faceless/voiceover).
Deliver 5 hooks across different hook types, then 1–2 full scripts in a playbook framework: timestamped lines,
on-screen text, shot list, CTA, 15–45 s unless asked. Model on a real winning video and link it. For
client scripts, find the models with workflow 0 narrowed to the niche (`viral --days 30 --category <cat> --add-tags
<niche tags>`, keep shop videos selling the same kind of product, `video` on the top 5-8, look at each hook.png):
keyword `discover` pages alone gave generic angles that Grace rejected (2026-10-02). Client rules beat this playbook
(Grace: never say a price, no downsides; `grace/PLAYBOOK.md` in Mymobileworld). Write like a person talking: short sentences, no hype words. Run `readability` on each script before
handing it over, and use the humanizer skill if the draft reads like an AI wrote it.

### Hand-offs
- AI-generated ad video (no filming): `ugc-product-ad` skill.
- Editing real raw takes (hooks/bodies/CTAs) into many ads: `ugc-take-combos` skill.
- Ralph's fashion client Grace: `grace-fashion-ads` skill.

## Rules
- Honest numbers only. Views, likes, saves, follower counts come from TikTok's public pages; lifetime units
  sold, price and rating from TikTok Shop pages; GMV, commission and affiliate counts only from what the user shows you. Never invent a GMV figure or a "% of creators".
- Claims in scripts must be true for the product: no medical/health cure claims, no fake scarcity or fake prices, no
  "I've used this for months" unless the user has. Suggest a commission/affiliate disclosure in the caption.
- Respect creators: analyze and learn from videos; never script a copy of someone's video word for word, and don't
  re-upload their footage.
- Keep answers phone-readable: short sections, the links up top.

## Limits (say these when they matter)
- No recent sales data: lifetime units sold yes (from TikTok Shop), but no 7-day GMV, no sales trend, no commission or
  affiliate count. That's what BMC Coach, Kalodata and FastMoss charge for. If the user needs trend numbers daily, a
  subscription to one of them is worth it.
- Can't see anyone's retention graph except from a screenshot the poster provides.
- Can't log in to the user's TikTok, so the showcase and analytics come from screenshots.
- No GMV ranking and no LIVE rankings (The Daily Virals' "Highest GMV" and "Top LIVEs"): those need sales and
  LIVE data. Views/day and saves are the public proxy.
- Hashtag and discover pages show what TikTok chooses to show (30–200 and ~16 videos), and web search finds only the
  pages search engines indexed. None of it is a complete ranking.
