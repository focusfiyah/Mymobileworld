# Grace's Creator Desk

Status (2026-10-01): v1 published, empty. Waiting on Ralph to share it with Grace (Editor) and on her first samples.

Link: https://claude.ai/artifact/78TpktwxYTM4cf4z5xnyS2 (page source: `index.html`; republish from here to keep the URL).
Capabilities: `db`, `user`, `sample`. Grace needs **Editor** access (invited by email, no public link) to write.

## What it does
- **Samples** (`samples/<id>`): name, brand, category, setting, price, commission, unitsSold, effort (1-3), received,
  deadline, stage (inbox → picked → scripted → filmed → posted / skipped), link, facts (exact label wording),
  notes (Grace's true experience only), script.
- **Score /100** (computed in the page): pay per sale 30, lifetime units sold 25, deadline 20,
  category track record 15 (save rate vs her overall, needs ≥2 videos), effort 10.
- **This week**: top N open samples by score (N = `settings/main.weeklyGoal`, default 3) + anything due in 7 days.
- **Shoot list**: picked/scripted samples grouped by setting.
- **Script pack**: "Draft with Claude" uses the viewer's own Claude usage (no Kie/ElevenLabs cost) with the
  PLAYBOOK house rules baked into the prompt; output is 4 hooks, 1 body, 1 CTA, shots, "Ask Grace".
- **Results** (`videos/<id>`): sampleId, url, posted, hook, format, stats {views, likes, comments, shares, saves,
  updated, source}, avgWatchSec, finishedPct, orders, gmv, earned. Save rate, share rate, $/1k views, grouped by
  hook type, format and category.

## Refreshing public stats (free)
For each `videos` doc with a url: `python3 .claude/skills/tiktok-shop-coach/scripts/tiktok.py video <url>` →
write views/likes/comments/shares/saves into `stats` with `source: "claude"` and `updated` = ISO time, via
ArtifactData `update` (pin `if_version`). Never overwrite Grace's Studio fields (watch time, orders, GMV, earned).
