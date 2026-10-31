# Source

Ralph 2026-10-31: "Watch this and get that last 2 skills mentioned" about Taki Wong's Short "Top 5 Claude Skills to
100x Your Claude Outputs" (youtube.com/shorts/SIVI3elT22Q, 2026-06-13). Skill four of five: "Banana Claude. This
allows you to use Nano Banana Pro directly inside of your Claude". The Short names no repo; the match is
github.com/AgriciDaniel/banana-claude (the only "Banana Claude" Claude Code skill, MIT).

| Folder | Upstream | Commit | Licence |
| --- | --- | --- | --- |
| `GUIDE.md` | `skills/banana/SKILL.md` (v3.1.0) | 08e329b (2026-10-21) | MIT (`licenses/banana-claude-LICENSE`) |
| `references/`, `scripts/` | `skills/banana/references/`, `skills/banana/scripts/` unchanged | 08e329b | MIT |
| `agents/` | `agents/visual-architect.md`, `agents/visual-critic.md` unchanged | 08e329b | MIT |

Not taken: the plugin wrapper (`.claude-plugin/`, `.mcp.json` MCP server, plugin-managed key), `install.sh`, tests,
screenshots, docs. The scripts work standalone with `GEMINI_API_KEY`. Added: `SKILL.md` (Ralph's setup), this file,
`CHANGELOG.md`.

## Security review (2026-10-31)

- SkillSpector --no-llm: **65/100 HIGH, DO_NOT_INSTALL by score.** All 20 HIGH are rule MP3 "memory manipulation"
  in `scripts/presets.py`, matching words like "reset state" and "preset state directory" in its own error
  messages about `~/.banana/presets`: false positives. 2 MEDIUM, 4 LOW. Reports: session scratchpad
  `skillspector-2026-10-31/`.
- Source read: network only to `generativelanguage.googleapis.com` (redirects refused); reads only
  `GEMINI_API_KEY`, `BANANA_HOME`, `BANANA_OUTPUT_DIR`, `HOME`; writes `~/.banana/` (approvals, presets, cost
  ledger) and the output folder; no subprocess, eval, exec, cron or shell-profile writes; base64 only for image
  data. Every paid call needs a single-use approval id bound to the exact plan (30 min). `legacy_cleanup.py` only
  renames old Banana installs it can prove it made, and only when run.
- Upstream description triggers on any image request (logo, thumbnail, product shot); narrowed here so it does
  not take Grace's product stills from ugc-product-ad.
- Verdict: **CAUTION**. Paid Google calls and local state are documented, needed and gated; use under the cost rule.
