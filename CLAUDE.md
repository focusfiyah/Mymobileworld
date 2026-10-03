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
- **Phone notifications (standard, Ralph 2026-10-01):** he leaves the app, so send a PushNotification (one line, what
  to review + cost) every time something is ready for his review or needs his decision: a still sheet, a test clip, a
  cut, a redo/cost question. Not for routine progress.
- **Google Drive uploads (standard, Ralph 2026-10-01):** use BOTH routes; if one fails, use the other. (1) Google Drive
  connector (`mcp__Google_Drive__*`): folders, docs, small text files. (2) Composio `googledrive` (account
  `googledrive_lin-ernst` = life22watch@gmail.com): videos and other big files via `GOOGLEDRIVE_UPLOAD_FROM_URL`
  (host the file first, e.g. Kie's free 3-day file host: `python3 -c "import kie; print(kie.upload('<file>'))"` in a job
  folder). The connector can't take a 7 MB video (base64 in the call) and turns emoji into mojibake in Docs.
- **Script checklist (standard, Ralph 2026-10-01):** coach hooks (spoken + on-screen text) → humanizer → plan; after
  the cut, `tiktok.py compare` vs the viral reference. Details: `grace/PLAYBOOK.md` §4, `ugc-product-ad` skill.
- Keep each job README's `Status:` line current (done / next / cost) so "continue the X ad" is one file read.

## Rule 0: the SCRIPT GATE (Ralph, 2026-10-03, after FUSOU shipped without Humanizer: "everything means everything, I shouldn't have to ask")
- Every job, on your own, before the plan goes to Ralph: run the WHOLE `grace/PLAYBOOK.md` §4 checklist (playbook rules, coach research
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
   wrinkles, same outfit/product in every shot, frame-by-frame check where hands or the product cross the face.
4. **Prompt text overrides the image:** when the look changes, update every prompt block (grep for the old wording);
   leave the product description out of shots that must not show the product.
5. **Script = everything** (Ralph, 2026-10-01): coach data + coach playbook + sales psychology + product research +
   Grace structure + `humanizer` + readability + on-screen hook text, then coach `compare` on the cut. Full list:
   `grace/PLAYBOOK.md` §4. Show the source of each line in the plan.
6. **Report the running total vs the quote at every paid step.** Details and fixes: `ugc-product-ad` skill
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

- **Plant Therapy Top 6 oils (Grace), 2026-10-01:** hands-only starter-guide ad, 18.6s, 7 shots. Cut v1
  `ugc/plant-therapy-top6/out/plant_therapy_top6.mp4` APPROVED by Ralph (v3 = + on-screen hook in the Murano classic caption style, free); $2.09 Kie (quote $1.82 + $0.27 approved redo). README Status line.

- **Vicks VapoShower Plus (Grace), 2026-10-01:** hands-only ad, 24.7s, 7 shots, humanized script v3, quote $2.04.
  Cut v3 `ugc/vicks-vaposhower/out/vicks_vaposhower.mp4` APPROVED; in Drive (Grace Tiktok assets/Vicks VapoShower Plus – Grace ad (2026-10-02)); $3.11 Kie vs $2.04 quote (6 clips rendered twice by two sessions, $1.07 lost).
  README Status line.
- **Viking curl cream (Grace), 2026-10-01:** script v5 (~25s, $0) for Grace's own hands-only beard footage;
  Grace records the lines next. `ugc/viking-curl-cream/README.md`.

- **FUSOU 2-in-1 Vanity Desk (Grace), 2026-10-02/03:** 6 hands-only videos (Grace's hands, voice = ElevenLabs Grace B, real listing photo edited + paste-back
  so the vanity never drifts). All 6 APPROVED, in Drive (Grace Tiktok assets/FUSOU folder) with the final scripts doc; $4.28 Kie vs $4.54 quote. README Status line.

- **Grace's Creator Desk, 2026-10-01:** sample queue + results tracker, https://claude.ai/artifact/78TpktwxYTM4cf4z5xnyS2
  (source + data model + stats refresh steps in `grace/desk/README.md`). Grace needs Editor access to write.

## Skills (2026-10-01)
- Cloud sessions often start here, so `.claude/skills/` carries copies of every focusfiyah/Dayone-ai project skill
  (day-one-ai, find-skills, grace-product-scripts, humanizer, hyperframes*, media-use, skill-inspector, tiktok-shop-coach,
  brag-slim).
  When you add or edit one of those, change it in BOTH repos. `ugc-product-ad` lives only here (client work).
- Scan every new skill first with the `skill-inspector` skill (SkillSpector). The claude.ai account upload (zip) is the
  only copy that reaches every device and chat; repo copies load only in sessions on that repo.
- The hyperframes/skillspector CLIs and the Chromium proxy-CA fix come from Dayone-ai's `bash setup.sh`.

## Learning reports (2026-10-01)
- `reports/`: daily (`YYYY-MM-DD-daily.md`) + weekly (`YYYY-Wnn-weekly.md`) notes Ralph pastes into new chats.
  Auto-written by triggers trig_01L7VTpGnzFjf2GnBeJgCdXb (daily 8:52pm ET) and trig_01WYmbt7urUsP5ALx1t6bSFE
  (Sunday 9:10pm ET), both bound to session_013SnHUp72Ux9iD1NpyvUKTe; steps in `reports/ROUTINE.md`.
  Archiving that session stops them. Reports are pushed straight to main (Ralph, 2026-10-01).
