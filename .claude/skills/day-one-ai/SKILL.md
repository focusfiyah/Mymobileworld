---
name: day-one-ai
description: Run, fix or extend Ralph's automated faceless YouTube channel "Day One AI" (@dayoneaitools1), which posts the first "how to use [brand-new AI tool]" tutorial within ~48h of launch and earns through affiliate links. Covers where everything lives (GitHub repo focusfiyah/Dayone-ai, the cloud environment, the daily routine), Ralph's standing decisions (private drafts only, his cloned voice narrates, contrast voices for demos, cost rules), the radar → script → render → upload pipeline, YouTube auth recovery, affiliate links, channel branding and known gotchas. Use whenever Ralph mentions Day One AI, the YouTube tutorial channel, the daily video, a draft to publish or change, affiliate links for the channel, his voice for videos, or asks what was set up for the channel.
---

# Day One AI: Ralph's automated YouTube tutorial channel

Channel **Day One AI**, handle **@dayoneaitools1**, id `UCCV19HOfKIrAiNa5IZakr_w`. Faceless: screen-capture style
demo plus AI voiceover. The goal is to be first on YouTube with a tutorial for a newly launched AI tool or feature, and to earn
from **recurring affiliate links** in the description (not AdSense).

## Where everything lives
- **Code and records:** GitHub `focusfiyah/Dayone-ai`, branch **main** (source of truth; the daily runs push there).
  Read its `CLAUDE.md` first. It holds the live status and handoff notes and outranks this skill if they disagree.
  - `produce.py`: renderer (cards, stitched web-page captures, cursor/highlight animation, ElevenLabs TTS, ffmpeg).
  - `yt.py`: YouTube via Ralph's own Google OAuth client (`auth-url`, `exchange`, `whoami`, `upload`, `desc`, `thumb`, `publish`).
  - `config.json`: voices, contrast voice roster, affiliate links, FTC disclosure. `data/covered.json`: covered and rejected tools.
  - `jobs/<slug>/job.json`: one script per video (template: `jobs/elevenlabs-v4-audio-tags/job.json`).
  - `brand/`: channel art (`avatar.png`, `banner.png`, `render.py`). `.secrets/yt_refresh.enc`: encrypted YouTube token.
- **Runs in:** a Claude cloud environment (Full network; ElevenLabs key injected by the proxy as an API credential; env vars
  `YT_CLIENT_ID`/`YT_CLIENT_SECRET` from Google Cloud project "Day One AI Uploader"). The laptop does not need to be on.
- **Daily routine:** `trig_01Q8jo4ocwirrSZEuvzF9hUf`, created by Ralph in the claude.ai Routines page (repo Dayone-ai,
  environment My World, 6:45am ET: stored as 10:45 UTC, so it must become 11:45 UTC after Nov 1). Prompt:
  `handoff/DAILY_ROUTINE.md`. Only Ralph can edit or run it. Never recreate it via create_trigger: chat-created
  routines start with no repo and no MCP tools and fail. Manual run from a chat: create_session with source_url.
- A session may start in the `Mymobileworld` repo. If so, attach `focusfiyah/Dayone-ai` with add_repo, then run `bash setup.sh`.

## Ralph's standing decisions (don't re-ask)
1. **Every upload is PRIVATE.** Publish only when Ralph says so (`python3 yt.py publish <id>`).
2. **Voiceover paused (Ralph 2026-10-05, overrides the next sentence):** daily runs make SILENT drafts (`--dry`, no
   upload) and send Ralph a list of apps; he says per app "hold" or "audio + publish". Only then render with
   `VOICE_OK=<slug>` (produce.py refuses ElevenLabs otherwise while config.json `voiceover_paused` is true), upload and
   publish. Rank apps where Ralph already has an affiliate link first: he wants income before more ElevenLabs spend.
   **Cost:** the normal voiceover (~2.5–3.5k ElevenLabs characters per video) is pre-approved. Tell Ralph the exact cost
   before anything else paid (extra re-voicing, AI images or video). He chose free code-rendered channel art over
   AI images (Nano Banana Pro on Fal.ai is $0.15 per image, $0.30 at 4K; no FAL_KEY in the cloud env).
3. **Voices (eleven_v4):** narrator is **Ralph's cloned voice "Ralph Azariah"** `5YVjMzHn641xyj0jM38O`. Not his voice for
   everything: demo lines, before/after samples, dialogue and second speakers use contrast voices from
   `config.json` `contrast_voices` (default Matilda `XrExE9yKIg1WjnnlVkGX`; also Jessica, Alice, George, Liam, Chris).
   Use premade voices only. **Never** use the other cloned voices in the account (Grace skit clones are client voices).
4. Honest, practical tone; only UI steps verified on official pages or docs; FTC disclosure in every description.
   Motion style lives in `motion.py`: springs with a tiny overshoot, camera zooms to the highlighted element, cursor clicks
   with a ring and a soft click sound, card blocks stagger in, code/prompts type out, every shot dips through the cream
   background. Banned: bouncy easing, particles, glows, gradients on UI chrome, invented copy. Scripts get the most from it
   with real `highlight` targets on web shots and prompts or code in card `code` blocks. The `brag-slim` skill (MIT,
   latent-spaces/brag) is installed for standalone promo/launch videos. HyperFrames (HeyGen's HTML → MP4 framework,
   Apache-2.0) is installed too: CLI via `setup.sh` (background), skills in `.claude/skills/hyperframes*` (start with
   `hyperframes`). Use it only when asked; keep ElevenLabs narration, no unlicensed music, same motion bans, and ask
   before its paid cloud/TTS paths. Playwright MCP (`@playwright/mcp`, pinned in `.mcp.json`, auto-approved in
   `.claude/settings.json`; also in the Mymobileworld repo) gives interactive browser tools (`browser_navigate`,
   snapshots, clicks): use it to check UI steps on a launch page before scripting them. Needs `setup.sh` first (proxy CA).
5. Daily cadence: every day, one video. Records push straight to main.

- **Unlazy on every job (Ralph 2026-10-06):** load the `unlazy` skill at the start of every job (client ads, scripts, Day One AI videos, personal tasks) and write a GATES.md before the work: one checkable outcome per gate, CHECK/EXPECT wherever a command can decide it, lint it, run it before reporting. Report the measured met/unmet counts; never say done while a gate is unmet. Trivial edits and plain factual answers are exempt (the skill's own rule). Job ledgers live in the job folder; `.unlazy/` stays untracked.

## Pipeline (per video)
1. **Radar:** tools or features launched in the last ~72h. Prefer tools with a recurring affiliate program, especially
   ones in `config.json` `affiliate_links`. Skip anything with ≥3 real YouTube tutorials or already in `data/covered.json`.
   Before "no video today": check every source in CLAUDE.md "Minimum radar" (PH last 3 days, TechCrunch AI, HN Show,
   all affiliate-tool changelogs), score ≥10 candidates, record `sources_checked`. Model: Opus unless Ralph says otherwise.
2. **Script:** `jobs/<slug>/job.json`, 8–12 segments, ~3 min. Shots: `web` (url + highlight/scroll; `start` = text to begin the capture at on long pages) or `card`.
   `sample` is a string (default demo voice), or `[["Matilda","..."],["George","..."]]` for several voices;
   `sample_voice` overrides the voice for one segment. `thumb_crop_y` picks the thumbnail region; badge "JUST LAUNCHED".
3. **Render:** `python3 produce.py jobs/<slug>/job.json --seg N` for each N, then `--final` (`--dry` = free silent test).
   Verify: 6-frame contact sheet, duration, audio level; run speech-to-text (scribe_v2) on demo lines if tags matter.
   Then `--short` renders the daily Short from the job's `short` block (see below) and gets verified the same way.
4. **Upload:** `python3 yt.py upload jobs/<slug>` (private + thumbnail), then `python3 yt.py upload-short jobs/<slug>`
   (private Short that links the long video) → both in `jobs/<slug>/youtube.json`.
5. Update `data/covered.json`, commit, push to main, notify Ralph (title, video + Short links, why this tool, affiliate status,
   plus 2–3 lines from `python3 yt.py analytics` on how earlier uploads are doing).

## Shorts (in the daily run since 2026-09-29) and Instagram (pending)
- `python3 produce.py jobs/<slug>/job.json --short` builds a vertical Short from `job["short"]` =
  `{"hook": "...", "clips": [{"seg": 0, "from": "first words", "to": "last words"}, {"seg": 4, "sample": true}]}`.
  It reuses the long video's narration (trimmed with speech-to-text word timings), so there's no new voiceover cost; an end card is added.
  Links in Shorts aren't clickable; a Short's job is to send viewers to the full tutorial.
- Every daily video gets a Short (2–3 clips, 25–40s). **Tease, don't tell:** open on the strongest sentence, show ONE
  result, keep the rest for the long video, and end with `short.tease` (a spoken open-loop line, ≤20 words, narrator
  voice) plus `short.tease_card` (2–5 word end-card title). Only promise what the long video shows.
- The only tappable link on a Short is its **Related video** (YouTube Studio → Short → Details). The upload API can't set
  it as far as we know, so remind Ralph to set it when he publishes. First Short: https://youtube.com/shorts/tlut-IXq07s.
- Check `CLAUDE.md` for whether the Instagram account is connected yet.
  Instagram plan: separate Day One AI account (Creator/Business), Composio connection, link-in-bio page, Reels.

## Analytics
- `python3 yt.py analytics [jobs/<slug> ...]`: views, watch time, avg % viewed, retention checkpoints, traffic sources,
  impressions/CTR when the API offers them; writes `jobs/<slug>/analytics.json`. Needs the `yt-analytics.readonly` scope
  (added 2026-09-29). ANALYTICS_SCOPE_MISSING means Ralph must re-authorize once (same flow as below). A 403 "YouTube Analytics API has not been used in project" means the API must be enabled in Cloud project 1483488540 (console.cloud.google.com/apis/library/youtubeanalytics.googleapis.com?project=1483488540), no re-auth needed. Analytics lags
  1–3 days; the public counters in the output are live.

## Affiliate links Ralph has joined
- ElevenLabs: `https://try.elevenlabs.io/6rw6sfid5efk` (22% recurring for 12 months). After he joins a new program, add
  it to `config.json` `affiliate_links`, and update any live video with `python3 yt.py desc jobs/<slug>`.

## History (2026-09-29)
- Pilot "ElevenLabs v4 Audio Tags: How to Use Them (Real Before & After Examples)": https://youtu.be/8sdp88VhbWo
  (**public**, Ralph's voice, new motion style, affiliate link + custom thumbnail; built from `jobs/motion-test/`).
  It replaced the first upload (Chris narration, old motion), which was deleted. Short: https://youtube.com/shorts/tlut-IXq07s
- Channel phone-verified (custom thumbnails work); banner set via API; Ralph uploaded the D1 profile picture.

## Gotchas already solved (keep the fixes)
- Chromium in the cloud image: `produce.py` uses the preinstalled `/opt/pw-browsers` build; `setup.sh` adds every
  Anthropic proxy CA from /root/.ccr/ca-bundle.crt to the NSS db (with only one of them, pages fail at random with
  ERR_CERT_AUTHORITY_INVALID; fixed 2026-10-01).
- The `cryptography` library can be broken in fresh containers; `setup.sh` reinstalls it. `yt.py exchange` self-tests
  encryption before spending Google's single-use code.
- YouTube re-auth if `TOKEN_REFRESH_FAILED`: `yt.py auth-url` → Ralph approves (screen says "Day One AI Uploader";
  "unverified app" → Advanced → continue) → he pastes the localhost URL → `yt.py exchange '<url>'` within ~10 min.
- Don't use Composio's YouTube connector for uploads (shared quota). Profile pictures can't be set via the API.
- The ElevenLabs key can't read subscription or balance (no `user_read`), so quote costs in characters.
