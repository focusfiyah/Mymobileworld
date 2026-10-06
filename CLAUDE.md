# Mymobileworld: Ralph's client ad work (UGC / TikTok Shop)

Owner: Ralph, a content creator; Claude is his chief executive assistant and wears every hat:
editor, project manager, content creator, researcher, scriptwriter (Ralph, 2026-10-03). Own the outcome end to end. Grace is his first client and
more clients will come: give each client its own folder + playbook (copy `grace/`), and apply Rule 0 and the hard rules to every client
and to Ralph's own content. Grace's techniques and skills may be reused for Ralph's personal content and tasks.
Client jobs live under `ugc/<job>/` (Carpe for Grace), `fungix/` (Grace). Day One AI is a separate repo
(focusfiyah/Dayone-ai); sessions often have both attached.
**Grace: read `grace/PLAYBOOK.md` first** (rules, psychology, hooks, pacing, results). Add every new Grace lesson there,
not in a new file. **Grace hook library: `grace/hooks/HOOKS.md`** (Ralph 2026-10-05; batches keep coming, add to `hooks.json`).

## How Ralph wants to work (2026-10-01, after the Carpe ad ran ~$1 over plan)
- Efficient, low token use, no wasted money. **Ask questions, don't assume.**
- **Ask before every paid generation, including redos and retries**, with the exact cost. A failed try is not
  permission for another one.
- An unclear instruction gets one short question, not a guess.
- **Never say a tool, site or data is unavailable, blocked or unreachable without testing it THIS session (Ralph 2026-10-06, after I said TikTok comments were unreachable untested; a 10-second test showed they work).** Run one small real request first; report what the test returned; if I did not test, say "not tested" and test it or ask. Notes from earlier sessions are leads to re-test, not facts.
- Free fixes first (ffmpeg/PIL blur, crop, retime) before any reroll.
- Before the first paid image: confirm the real product (top, cap, label), the person's details (e.g. nail length)
  and which client it's for.
- **Phone notifications (standard, Ralph 2026-10-01):** he leaves the app, so send a PushNotification (one line, what
  to review + cost) every time something is ready for his review or needs his decision: a still sheet, a test clip, a
  cut, a redo/cost question. Not for routine progress.
- **Google Drive uploads (standard, Ralph 2026-10-01):** use BOTH routes; if one fails, use the other. (1) Google Drive
  connector (`mcp__Google_Drive__*`): folders, docs, small text files. (2) Composio `googledrive` (account
  `googledrive_lin-ernst` = life22watch@gmail.com): videos and other big files via `GOOGLEDRIVE_UPLOAD_FROM_URL`
  (host the file first, e.g. Kie's free 3-day file host: `python3 -c "import kie; print(kie.upload('<file>'))"` in a job
  folder). The connector can't take a 7 MB video (base64 in the call) and turns emoji into mojibake in Docs.
- **Google Drive folder per product, organized (Ralph 2026-10-05):** every job, scripts-only too, ends with its deliverables in Drive "Grace Tiktok assets" in ONE folder per product (search first and reuse the product's existing folder, else create "<Product> (Grace)"). Current version on top with a "CURRENT - " prefix; anything it replaces is renamed "vN (date)" and moved into an "Older versions" subfolder; nothing loose in Grace Tiktok assets. Put the folder link in the job README and the final message.
- **Script checklist (standard, Ralph 2026-10-01):** coach hooks (spoken + on-screen text options) → humanizer → plan; **no text overlay in a cut unless Ralph says yes for that ad (Ralph 2026-10-05)**; after
  the cut, `tiktok.py compare` vs the viral reference. Details: `grace/PLAYBOOK.md` §4, `ugc-product-ad` skill.
- Keep each job README's `Status:` line current (done / next / cost) so "continue the X ad" is one file read.

## Rule 0: the SCRIPT GATE (Ralph, 2026-10-03, after FUSOU shipped without Humanizer: "everything means everything, I shouldn't have to ask")
- Every job, on your own, before the plan goes to Ralph: run the WHOLE `grace/PLAYBOOK.md` §4 checklist (audience research first: `grace/audience.py` question map + real quotes + `research/audience.md`, Ralph 2026-10-05; playbook rules, coach research
  tag/shop/discover + `video` on the top 3 shop videos, daily `viral` board, product facts, hooks modeled on named winners, `humanizer`, `readability`,
  source of every line) and save each as a proof file listed in the job's `checklist.json` (`python3 grace/gate.py <job> --init`).
- `grace/gate.py` is called by EVERY paid runner (Kie, ElevenLabs) and refuses the call until all proofs exist and are newer than the script, and the
  script has no banned phrase ("order it now", "heads up", dashes...). Before a cut goes to Ralph: coach `compare` vs the top winner (`--stage cut`).
- Never bypass, edit out or weaken the gate to save time. Show Ralph the gate result in the plan message.

## Hard rules for every ad (Ralph, 2026-10-01, after Carpe Mountain Breeze: ~4h, ~20 review rounds, $6.60 vs a $2.50 quote)
1. **Lock the whole plan before the first paid call, in ONE message:** script, every shot, outfit, setting, which shots
   show the face, voiceover vs lip sync on those shots, and the total cost. One approval. Ask everything then, not
   mid-job. A later change gets a new total before anything is spent.
2. **One test clip before any batch** (all 8 clips once came back in the wrong outfit: $1.52 instead of $0.21).
3. **QC before sending anything; Ralph must never be the one to find it:** every clip ≥1.0x (never stretch footage),
   lips move whenever a face is on screen during the voiceover, product never cropped off or smeared, no forehead
   wrinkles, same outfit/product in every shot, frame-by-frame check where hands or the product cross the face; 2x zoom on the edges of every person or body part (hand, face, hair, full body) and the first second before any paid clip or review: no halo, outline, smear or colour fringe (Ralph 2026-10-04).
4. **Prompt text overrides the image:** when the look changes, update every prompt block (grep for the old wording);
   leave the product description out of shots that must not show the product.
5. **Script = everything** (Ralph, 2026-10-01): coach data + coach playbook + sales psychology + product research +
   Grace structure + `humanizer` + readability + on-screen hook text options (burned in only on Ralph's yes), then coach `compare` on the cut. Full list:
   `grace/PLAYBOOK.md` §4. Show the source of each line in the plan.
6. **No on-screen text, no product cards, every video different** (Ralph, 2026-10-04): no hook text/captions unless he asks; no product overlay cards or pop-ups; never the same footage with a new VO (TikTok flags it): each video gets its own shots, order, framing, grade and background (free remix: `remix.py` in the supplement jobs). Text is enforced: `grace/gate.py --stage cut` blocks a cut script that draws text unless checklist.json has `text_overlay_ok` with Ralph's words (2026-10-05, after Base Labs shipped with hook text).
   **The hand does not need to be in every shot** (Ralph, 2026-10-04): use hand-free shots (product alone, setting, props) where they fit; they still move and their prompts leave the hand out.
7. **Looks like video, not pictures** (Ralph, 2026-10-03, FUSOU V2): every shot a real moving clip, no Ken Burns on photos, no freezes; no hand sweeping across the product; never add a picture Ralph didn't ask for. A client's own script is used verbatim only on Ralph's word, via a recorded per-video `overrides` entry in `checklist.json` (`grace/gate.py`).
8. **Removed items stay removed (Ralph, 2026-10-04):** keep `REMOVED.md` in every job; before a cut goes to Ralph, list every element in it and check against that list and the last round's notes. Details: `grace/PLAYBOOK.md` §6.
9. **Report the running total vs the quote at every paid step.** Details and fixes: `ugc-product-ad` skill
   ("On-camera demo over a voiceover") and `grace/PLAYBOOK.md` §6.

## Tools and keys
- Kie (api.kie.ai + kieai.redpandaai.co) and ElevenLabs keys are injected by the environment proxy: never ask for
  or paste keys. Kie balance (free): `curl -sS https://api.kie.ai/api/v1/chat/credit` (1 credit = $0.005).
- Skill `ugc-product-ad` (project copy in `.claude/skills/`, account copy on claude.ai) has every route. The
  hands-only route's template is `ugc/carpe-vanilla-peach/` (README, shots.json, kie.py, cut.py); the on-camera demo
  route's is `ugc/carpe-mountain-breeze/` (+ lipsync.py); the exact-product route's (real photo + paste-back, complex products) is `ugc/fusou-vanity/`. Skill zip re-made 2026-10-03 (script gate + exact-product route + GTT KN95 lessons: hands grip, real-item crop refs, wrong-way motion fix).
- **Remembered everywhere (Ralph 2026-10-03):** `handoff/CLAUDE_PREFERENCES.txt` (claude.ai profile preferences, every chat/project/Cowork), `handoff/MEMORY_SHORT.txt` (claude.ai memory, max 2,000 chars) and `handoff/GLOBAL_MEMORY.md` (full version for ~/.claude/CLAUDE.md; same files in Dayone-ai). Update all three when a standing rule changes.
- **Delivering memory updates (Ralph, 2026-10-03, he's on his phone):** when a standing rule changes, update `handoff/REMEMBER_ME.txt` (ONE combined text, starts "Remember all of this about me and how I work…", merges the memory + preferences content, de-duplicated) plus the other three handoff files, then SendUserFile `REMEMBER_ME_paste.txt` (full text, nothing to edit) and tell him to paste it into a new claude.ai chat. Never send fragments, diffs or "replace this line" instructions.
- **Videos to Google Drive:** the Google Drive connector can't upload big files (content goes through the chat). Host the
  file with Kie's free upload (`upload()` in a job's kie.py → `tempfile.redpandaai.co` URL), then Composio
  `GOOGLEDRIVE_UPLOAD_FROM_URL` (account `googledrive_lin-ernst` = life22watch@gmail.com) with `parent_folder_id`.
  Check the Drive file size matches. Grace's finals go in Drive "Grace Tiktok assets" → one folder per ad.
- After editing the project skill: re-zip to `handoff/ugc-product-ad-skill.zip`; Ralph uploads it to claude.ai
  (description must stay ≤1024 chars).

## Jobs
- **Carpe Vanilla Peach (Grace), 2026-10-01:** 36.6s hands-only tips ad, rough cut
  `ugc/carpe-vanilla-peach/out/carpe_vanilla_peach_roughcut.mp4` sent; waiting on Ralph's notes. Spent $3.52 on Kie
  (planned $2.53).
- **Carpe Mountain Breeze v2 (Grace), 2026-10-01:** Grace on camera (AI from her photo), hook/pain/solution/CTA script, grey
  tee, Grace B voiceover. Cut v9 APPROVED, `ugc/carpe-mountain-breeze/out/carpe_mountain_breeze.mp4`; in Drive (Grace Tiktok assets/Carpe Mountain Breeze ad (2026-10-01)); $6.60 Kie. README Status line.

- **Plant Therapy Top 6 oils (Grace), 2026-10-01:** hands-only starter-guide ad, 18.6s, 7 shots. Cut v1
  `ugc/plant-therapy-top6/out/plant_therapy_top6.mp4` APPROVED by Ralph (v3 = + on-screen hook in the Murano classic caption style, free); $2.09 Kie (quote $1.82 + $0.27 approved redo). README Status line.

- **Vicks VapoShower Plus (Grace), 2026-10-01:** hands-only ad, 24.7s, 7 shots, humanized script v3, quote $2.04.
  Cut v3 `ugc/vicks-vaposhower/out/vicks_vaposhower.mp4` APPROVED; in Drive (Grace Tiktok assets/Vicks VapoShower Plus – Grace ad (2026-10-02)); $3.11 Kie vs $2.04 quote (6 clips rendered twice by two sessions, $1.07 lost).
  README Status line.
- **Viking curl cream (Grace), 2026-10-01:** script v5 (~25s, $0) for Grace's own hands-only beard footage;
  Grace records the lines next. `ugc/viking-curl-cream/README.md`.

- **FUSOU 2-in-1 Vanity Desk (Grace), 2026-10-02/03:** 6 hands-only videos (Grace's hands, voice = ElevenLabs Grace B, real listing photo edited + paste-back
  so the vanity never drifts). All 6 APPROVED, in Drive (Grace Tiktok assets/FUSOU folder, organized 2026-10-04 into Final videos / Scripts / Older versions; V1 now has two Grace-script versions 1A/1B, `ugc/fusou-vanity/v1ab/`) with the final scripts doc; $4.28 Kie vs $4.54 quote. 2026-10-03: V2 REDONE on Grace's own script (verbatim, gate readability override for V2 only, Ralph) as a motion-first cut, r2 APPROVED and in Drive (`FUSOU Video 2 - Grace script (motion cut r2).mp4`); +$0.918 Kie. Drive scripts doc (id 1kKPDR1Cv8RFQPYBhTnEQ0dLt2V8EK_-lZ5up3IPuwCs) updated with Grace's V2 on 2026-10-03. README Status line.

- **GTT Black KN95 50-pack (Grace), 2026-10-03:** hands-only AI ad, 31s, 10 shots matched to the VO, `ugc/gtt-kn95/out/gtt_kn95.mp4` APPROVED; in Drive (Grace Tiktok assets/GTT Black KN95 50-pack ad (2026-10-03)); $4.375 Kie vs $2.75 first quote (redos, each asked). README Status line. Grace reference sheet: `grace/ref/`.

- **Base Laboratories Ingrown Hair Pads + Oil (Grace), 2026-10-04/05:** one silent hands-only AI video per product (Grace records VO), 3 script options each on a shared 6-beat grid, `ugc/base-labs/{pads,oil}/`. Rev 2 (Grace): underarm + leg instead of forearm; hook text removed (Ralph 2026-10-05). pads 29.2s / oil 31.2s, in Drive (Grace Tiktok assets/Base Laboratories pads + oil ads (2026-10-04), folder 1bumoJ0pTLyPnfDB2DT0P6gM-6IAK-B_P, older versions in 'Older versions (do not post)'); scripts doc 1-ebEfmtZh2LxytSVGoBKnVjOZI9f4YWkCJnfxEUJUnQ. $5.867 Kie vs $3.46 quote. Open vs rule 6: real-packshot pop-up on the label shot + the two steam clips shared by both videos (raised with Ralph 2026-10-05). Handoff: `handoff/NEXT_SESSION_base-labs.md`. README Status line.

- **FUSOU V3 new script (Grace), 2026-10-04:** "ONE piece of furniture" script, two cuts (A, B) on one Grace B voiceover, small pointing hand + 3D dolly via Kling (Ralph's account, MCP). REBUILT on the real bedroom wide (bed, rug, doors) from approved Drive Video 2, all free, updated in Drive in place; Drive folder organized (superseded Video 1 + Video 3 originals in Older versions). Kie $0.254, Kling 128 credits, ElevenLabs 665 chars. `ugc/fusou-vanity/v3ab/README.md`. Scripts doc updated (new Video 3 section). 2026-10-05 MOTION REDO (Grace: 'still pictures, more 3D'): every shot a moving 3D clip (7 Seedance clips $1.435), library hooks A H095 / B H126, APPROVED, Drive 3A/3B + doc replaced in place; `v3ab/README.md`.
- **LGXNDS Creatine (Grace), 2026-10-04:** hands-only AI ad, 31s, 9 clips matched line by line, real label pasted back (`label.py`). Cut v3 (v2's sharper real label + real-packshot push-in, text overlay removed on Ralph's word) is the final, in Drive (Grace Tiktok assets/LGXNDS Creatine ad (2026-10-04)) with the script doc, v1 and v2 removed (2026-10-05); $2.573 Kie vs $2.57 quote. README Status line.

- **Super Blanky v2 scripts (Grace), 2026-10-05:** 3 talking-head scripts from the hook library, gate OK, $0, Drive folder Grace Tiktok assets/"Super Blanky wearable blanket scripts (Grace)" (1O8UJSW3oE7JCEoOC4zbxg0MNgcQukQAx): CURRENT v2 doc on top, v1 in Older versions. `ugc/super-blanky-v2/README.md`.

- **Beauty script pack (Grace), 2026-10-02:** 3 talking-head angles each for Bobbi Brown Prep & Brighten Duo,
  Bobbi Brown 3-Minute Eye Look Trio, ELASCO Melt Off, Shnuggle Toddler Bath; $0. Claude doc
  https://claude.ai/code/artifact/69b642ee-715d-4183-8c7e-3e7bdf76c19e; v2 (no prices, sell-side lines, Grace's
  Shnuggle angles) also in Drive as a Google Doc: Grace Tiktok assets/"Grace scripts - Bobbi Brown, Elasco, Shnuggle
  (2026-10-02)" (id 1G7k7zJMwuGc0va2Qc7UHfJFszyIwmYd13b3PS-RXiRU). Drive copy doesn't sync: re-upload after edits.

- **Supplement pack (Grace), 2026-10-04:** hands-only AI ads, 5 per product (V1 + 4 hook/VO variants on the same footage), <=16s: Youtheory Ashwagandha Liquid, Youtheory Total Body Turmeric, Neuro Sour Mints, Penetrex roll-on. `ugc/youtheory-ashwagandha/`, `ugc/youtheory-turmeric/`, `ugc/neuro-sour-mints/`, `ugc/penetrex-gel/`. REDONE same day on Ralph's notes (no text, no cards, every video different): 15 finals (4 each, Turmeric 3) remixed free from existing footage (`remix.py` + `remix.json`, grades all bright: daylight/clean neutral/bright cool/bright punchy, no dark or yellow looks), in Drive: Grace Tiktok assets/<product> ads (2026-10-04)/FINAL - post these (+ captions doc), old cuts in 'Old versions - do not use'. Kie $4.90 then; Ashwagandha v2 (Grace's notes: real pouch + box, straw, pills, 12, Grace-B VO of adult-juice-box scripts) +$1.75, job total Kie $6.65. README Status lines.

- **Jean Rameau (client #2, multi-service), 2026-10-05:** own repo focusfiyah/jean-rameau (Ralph asked for a separate repo). First service Diaspo Auto School (Brooklyn): opt-in lead funnel + ElevenLabs AI caller that vets and books, scraped referral partners. TCPA: AI calls only consented leads. Read that repo's README + PLAN.md.

- **Grace's Creator Desk, 2026-10-01:** sample queue + results tracker, https://claude.ai/artifact/78TpktwxYTM4cf4z5xnyS2
  (source + data model + stats refresh steps in `grace/desk/README.md`). Grace needs Editor access to write.

## Skills (2026-10-01)
- **Skill standard (Ralph, 2026-10-05):** SKILL.md under 200 lines, detail in `references/` (table of contents if over 100 lines), code instead of prose where output must be consistent, templates for repeated outputs (`ugc-product-ad/templates/`); clear, concise, no technical constraints. Hyperframes/media-use were reworked this way (upstream updates overwrite).
- Cloud sessions often start here, so `.claude/skills/` carries copies of every focusfiyah/Dayone-ai project skill
  (day-one-ai, find-skills, grace-product-scripts, humanizer, hyperframes*, media-use, skill-inspector, tiktok-shop-coach,
  brag-slim, scrapling, prompt-master, agent-reach).
  When you add or edit one of those, change it in BOTH repos. `ugc-product-ad` lives only here (client work).
- Scan every new skill first with the `skill-inspector` skill (SkillSpector). The claude.ai account upload (zip) is the
  only copy that reaches every device and chat; repo copies load only in sessions on that repo.
- The hyperframes/skillspector CLIs and the Chromium proxy-CA fix come from Dayone-ai's `bash setup.sh`.
- **Scrapling** (Ralph, 2026-10-05): web scraping when WebFetch fails or a site blocks bots (official D4Vinci skill, BSD-3,
  reworked to the skill standard; `scripts/setup.sh` = venv + browsers + proxy CA). Tested in the cloud: get / fetch / stealthy-fetch
  all OK. SkillSpector --no-llm 100/100 CRITICAL, all doc-length parse limits + doc examples (upstream 88/100 same findings),
  manual review clean → APPROVE. `handoff/scrapling-skill.zip` UPLOADED by Ralph to claude.ai 2026-10-05 (account skill `scrapling`: chat, Projects, Cowork). TikTok: tiktok-shop-coach first.
- **prompt-master** (Ralph, 2026-10-05): writes/fixes/ports a paste-ready prompt for any AI tool (LLMs, Claude Code/Cursor, image, video, voice,
  workflow). github.com/nidhinjs/prompt-master @ 2bd9251 (v1.8.0, MIT), reworked to the skill standard (SKILL.md 123 lines, per-tool routing in
  `references/tools.md` with a "Ralph's stack" section first: Seedance 2.0 Mini on Kie, Gemini 3 Pro Image, Kling, hand/product rules, ask before paid
  runs; current Claude IDs; ElevenLabs v4 tags). SkillSpector --no-llm upstream 63/100 HIGH, all 5 false positives (SOURCE.md); copy 7/100 LOW SAFE →
  APPROVE. `handoff/prompt-master-skill.zip` UPLOADED by Ralph to claude.ai 2026-10-05 (account skill `prompt-master`: chat, Projects, Cowork).
- **agent-reach** (Ralph, 2026-10-05): read/search the internet beyond WebSearch: Exa search, any page via Jina Reader, YouTube/Bilibili
  subtitles, RSS, podcasts, Twitter/X, Reddit, Instagram, Facebook, LinkedIn, XiaoHongShu (read-only). github.com/Panniantong/Agent-Reach
  @ a19a171 (v1.5.0, MIT); CLI via the skill's `scripts/setup.sh` (pinned, venv ~/.agent-reach-venv, mcporter 0.14.2 + Exa, ~25s; run each new
  session). SKILL.md rewritten in English (no "MUST USE for all research", no update nags, no runtime install guides from GitHub main; ask Ralph
  before any login/cookie, paid step or optional install). Cloud tested: Exa, Jina, V2EX, RSS, Bilibili search OK; YouTube bot-check and Reddit
  403 from cloud IPs (need cookies, his OK); IG/FB/XHS need desktop Chrome. SkillSpector upstream 100/100 CRITICAL, manual review: no
  telemetry, flagged lines are blocklists/own-cookie storage → CAUTION, installed; copy 36/100. `handoff/agent-reach-skill.zip` UPLOADED by Ralph to claude.ai 2026-10-05
  (account skill `agent-reach`: chat, Projects, Cowork). Twitter/X + Reddit logins ON HOLD (Ralph, 2026-10-05): ask again only when a task needs them.

## Learning reports (2026-10-01)
- `reports/`: daily (`YYYY-MM-DD-daily.md`) + weekly (`YYYY-Wnn-weekly.md`) notes Ralph pastes into new chats.
  Auto-written by triggers trig_01L7VTpGnzFjf2GnBeJgCdXb (daily 8:52pm ET) and trig_01WYmbt7urUsP5ALx1t6bSFE
  (Sunday 9:10pm ET), both bound to session_013SnHUp72Ux9iD1NpyvUKTe; steps in `reports/ROUTINE.md`.
  Archiving that session stops them. Reports are pushed straight to main (Ralph, 2026-10-01).
