# Mymobileworld: Ralph's client ad work (UGC / TikTok Shop)

Owner: Ralph. Client jobs live under `ugc/<job>/` (Carpe for Grace), `fungix/` (Grace). Day One AI is a separate repo
(focusfiyah/Dayone-ai); sessions often have both attached.

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
