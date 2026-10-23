---
name: day-one-ai
description: Run, fix or extend Ralph's automated faceless YouTube channel "Day One AI" (@dayoneaitools1), which posts the first "how to use [brand-new AI tool]" tutorial within ~48h of launch and earns through affiliate links. Covers where everything lives (GitHub repo focusfiyah/Dayone-ai, the cloud environment, the daily routine), Ralph's standing decisions (private drafts only, his cloned voice narrates, contrast voices for demos, cost rules), the radar → script → render → upload pipeline, YouTube auth recovery, affiliate links, channel branding and known gotchas. Use whenever Ralph mentions Day One AI, the YouTube tutorial channel, the daily video, a draft to publish or change, affiliate links for the channel, his voice for videos, or asks what was set up for the channel.
---
# Day One AI: Ralph's automated YouTube tutorial channel

Channel **Day One AI** (@dayoneaitools1, id `UCCV19HOfKIrAiNa5IZakr_w`): faceless screen-capture tutorials, narrated
by AI, aiming to be the first "how to use [new AI tool]" video within ~48h of launch. It earns from **recurring
affiliate links** in the description, not AdSense, so apps where Ralph already has a link come first.

**The repo's `CLAUDE.md` (GitHub `focusfiyah/Dayone-ai`, branch main) is the one home** for the pipeline, the
script schema, motion style, Shorts, engagement rules, published videos and status. Read it before any run; it wins
over this skill. This skill carries only what a chat without the repo needs to act safely.

## Starting a run
- In a session on the repo: `bash setup.sh`, then follow CLAUDE.md "Pipeline". A session that started in
  Mymobileworld attaches the repo first (`add_repo focusfiyah/Dayone-ai`).
- From a chat: `create_session` with `source_url=https://github.com/focusfiyah/Dayone-ai` and the task as prompt.
- The daily routine `trig_01Q8jo4ocwirrSZEuvzF9hUf` belongs to Ralph (claude.ai Routines page; prompt in
  `handoff/DAILY_ROUTINE.md`). Never recreate it with create_trigger. Why: a chat-created routine started with no
  repo and no tools and quit after 27s (2026-09-29). Its cron is 10:45 UTC = 6:45am EDT; remind Ralph to move it to
  11:45 UTC after Nov 1.

## Ralph's decisions (don't re-ask)
1. **Every upload is PRIVATE** until Ralph says publish. Why: draft, then his approval (2026-09-29).
2. **Daily = silent drafts and one list** (Ralph 2026-10-05): radar, up to 3 apps as silent drafts, ONE list to
   Ralph; per app he answers "hold" or "audio + publish". ElevenLabs runs only with `VOICE_OK=<slug>`. Why: earn
   affiliate money before spending more on voiceovers.
3. **Voices:** narrator = Ralph's clone "Ralph Azariah" `5YVjMzHn641xyj0jM38O`; demo lines and second speakers =
   premade contrast voices from `config.json`. Never another cloned voice in the account. Why: the others are
   clients' voices.
4. **Cost:** the normal voiceover (~2.5-3.5k characters) is pre-approved once he says "audio + publish"; anything
   else paid gets the exact cost first. Quote ElevenLabs in characters (the key can't read the balance).
5. **Honest, verified:** only UI steps seen on official pages; FTC disclosure in every description.
6. **Own thumbnail look per video** (Ralph 2026-10-23): every job gets a `look` block, made and checked with the
   `day-one-looks` skill. Why: YouTube demonetizes template-based, repetitive channels, and all 25 thumbnails up to
   then came from one template.

Done when (per video): the job's `job.json`, video, Short and contact sheets are checked, both uploads are PRIVATE
with ids in `jobs/<slug>/youtube.json`, `data/covered.json` is updated and pushed to main, and Ralph has a phone push
(ToolSearch `select:PushNotification` first; skipped while he has the app open, so the email is the backup) plus the email (Composio GMAIL_SEND_EMAIL, account `gmail_correa-comus`): title, both links, why this tool, affiliate status.

## Affiliate links
`config.json` `affiliate_links` is the one list (ElevenLabs, Synthesia, Higgsfield as of 2026-10-13; Shopify declined
him; Manus pending). After he joins a program, add it there and run `python3 yt.py desc jobs/<slug>`; the Short's
description needs the same snippet by hand.

## Gotchas already solved (keep the fixes)
- YouTube `TOKEN_REFRESH_FAILED`: `yt.py auth-url`, Ralph approves ("unverified app" > Advanced > continue), pastes
  the localhost URL, `yt.py exchange '<url>'` within ~10 min (the code is single-use).
- `ANALYTICS_SCOPE_MISSING` = re-authorize as above. Analytics lags 1-3 days.
- Chromium pages failing with ERR_CERT_AUTHORITY_INVALID: run `setup.sh` (it trusts every proxy CA).
- Never upload with Composio's YouTube connector (shared quota); use `yt.py`. Profile pictures can't be set by API.
- A Short's only tappable link is its Related video, set by Ralph in YouTube Studio; remind him after publishing.
