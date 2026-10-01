# Mymobileworld: Ralph's client ad work (UGC / TikTok Shop)

Owner: Ralph. Client jobs live under `ugc/<job>/` (Carpe for Grace), `fungix/` (Grace). Day One AI is a separate repo
(focusfiyah/Dayone-ai); sessions often have both attached.
**Grace: read `grace/PLAYBOOK.md` first** (rules, psychology, hooks, pacing, results). Add every new Grace lesson there,
not in a new file.

## How Ralph wants to work (2026-10-01, after the Carpe ad ran ~$1 over plan)
- Efficient, low token use, no wasted money. **Ask questions, don't assume.**
- **Ask before every paid generation, including redos and retries**, with the exact cost. A failed try is not
  permission for another one.
- An unclear instruction gets one short question, not a guess.
- Free fixes first (ffmpeg/PIL blur, crop, retime) before any reroll.
- Before the first paid image: confirm the real product (top, cap, label), the person's details (e.g. nail length)
  and which client it's for.
- Keep each job README's `Status:` line current (done / next / cost) so "continue the X ad" is one file read.

## Hard rules for every ad (Ralph, 2026-10-01, after Carpe Mountain Breeze: ~4h, ~20 review rounds, $6.60 vs a $2.50 quote)
1. **Lock the whole plan before the first paid call, in ONE message:** script, every shot, outfit, setting, which shots
   show the face, voiceover vs lip sync on those shots, and the total cost. One approval. Ask everything then, not
   mid-job. A later change gets a new total before anything is spent.
2. **One test clip before any batch** (all 8 clips once came back in the wrong outfit: $1.52 instead of $0.21).
3. **QC before sending anything; Ralph must never be the one to find it:** every clip ≥1.0x (never stretch footage),
   lips move whenever a face is on screen during the voiceover, product never cropped off or smeared, no forehead
   wrinkles, same outfit/product in every shot, frame-by-frame check where hands or the product cross the face.
4. **Prompt text overrides the image:** when the look changes, update every prompt block (grep for the old wording);
   leave the product description out of shots that must not show the product.
5. **Report the running total vs the quote at every paid step.** Details and fixes: `ugc-product-ad` skill
   ("On-camera demo over a voiceover") and `grace/PLAYBOOK.md` §6.

## Tools and keys
- Kie (api.kie.ai + kieai.redpandaai.co) and ElevenLabs keys are injected by the environment proxy: never ask for
  or paste keys. Kie balance (free): `curl -sS https://api.kie.ai/api/v1/chat/credit` (1 credit = $0.005).
- Skill `ugc-product-ad` (project copy in `.claude/skills/`, account copy on claude.ai) has every route. The
  hands-only route's template is `ugc/carpe-vanilla-peach/` (README, shots.json, kie.py, cut.py); the on-camera demo
  route's is `ugc/carpe-mountain-breeze/` (+ lipsync.py). Skill zip re-made 2026-10-01 with the Carpe v2 lessons.
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

## Skills (2026-10-01)
- Cloud sessions often start here, so `.claude/skills/` carries copies of every focusfiyah/Dayone-ai project skill
  (day-one-ai, find-skills, humanizer, hyperframes*, media-use, skill-inspector, tiktok-shop-coach, brag-slim).
  When you add or edit one of those, change it in BOTH repos. `ugc-product-ad` lives only here (client work).
- Scan every new skill first with the `skill-inspector` skill (SkillSpector). The claude.ai account upload (zip) is the
  only copy that reaches every device and chat; repo copies load only in sessions on that repo.
- The hyperframes/skillspector CLIs and the Chromium proxy-CA fix come from Dayone-ai's `bash setup.sh`.

## Learning reports (2026-10-01)
- `reports/`: daily (`YYYY-MM-DD-daily.md`) + weekly (`YYYY-Wnn-weekly.md`) notes Ralph pastes into new chats.
  Auto-written by triggers trig_01L7VTpGnzFjf2GnBeJgCdXb (daily 8:52pm ET) and trig_01WYmbt7urUsP5ALx1t6bSFE
  (Sunday 9:10pm ET), both bound to session_013SnHUp72Ux9iD1NpyvUKTe; steps in `reports/ROUTINE.md`.
  Archiving that session stops them. Reports are pushed straight to main (Ralph, 2026-10-01).
