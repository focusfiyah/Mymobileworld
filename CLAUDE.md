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

## Tools and keys
- Kie (api.kie.ai + kieai.redpandaai.co) and ElevenLabs keys are injected by the environment proxy: never ask for
  or paste keys. Kie balance (free): `curl -sS https://api.kie.ai/api/v1/chat/credit` (1 credit = $0.005).
- Skill `ugc-product-ad` (project copy in `.claude/skills/`, account copy on claude.ai) has every route. The
  hands-only route's template is `ugc/carpe-vanilla-peach/` (README, shots.json, kie.py, cut.py).
- After editing the project skill: re-zip to `handoff/ugc-product-ad-skill.zip`; Ralph uploads it to claude.ai
  (description must stay ≤1024 chars).

## Jobs
- **Carpe Vanilla Peach (Grace), 2026-10-01:** 36.6s hands-only tips ad, rough cut
  `ugc/carpe-vanilla-peach/out/carpe_vanilla_peach_roughcut.mp4` sent; waiting on Ralph's notes. Spent $3.52 on Kie
  (planned $2.53).
- **Carpe Mountain Breeze v2 (Grace), 2026-10-01:** Grace on camera (AI from her photo), hook/pain/solution/CTA script, grey
  tee, Grace B voiceover. Rough cut `ugc/carpe-mountain-breeze/out/carpe_mountain_breeze.mp4` sent; $5.42 Kie. README Status line.

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
