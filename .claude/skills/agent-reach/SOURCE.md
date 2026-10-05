Source: https://github.com/Panniantong/Agent-Reach (MIT, "Agent Eyes" / Neo Reid), commit a19a171 (2026-09-16), v1.5.0
Copied: agent_reach/skill/references/*.md (unchanged, Chinese) and LICENSE. SKILL.md rewritten in English to Ralph's skill
standard and rules; scripts/setup.sh is ours (pinned CLI + mcporter 0.14.2, venv, Exa config, yt-dlp JS runtime).
Removed from the upstream skill: "MUST USE for any research" trigger (it would override WebSearch, tiktok-shop-coach,
scrapling), the auto update check + "paste this update link" nag, and fetching install/update guides from GitHub main at
run time (remote, unpinned instructions). Added: ask Ralph before any login/cookie, paid step or optional install.
Not run: `agent-reach install --system` (it would also copy the unreviewed upstream skill into ~/.claude/skills).

Review 2026-10-05, SkillSpector 2.12.0 --no-llm on the full upstream repo: 100/100 CRITICAL. Manual review of every
HIGH finding in shipped code: SSRF1 (utils/url.py, transcribe.py) = blocklists that STOP requests to localhost/cloud
metadata; PE3/E2 (reddit.py, cookie_extract.py, cli.py) = writing the user's own cookies to private local files when
they run `configure`; YR1 remote bootstrap (cli.py:2248) = the printed update instructions; P6 (cli.py) = "safe mode"
docstrings; AST9 = getattr on argparse args; SC2 = curl of the podcast page being transcribed; the rest are tests and
README examples. Outbound hosts: the platforms themselves, r.jina.ai, mcp.exa.ai, api.github.com (update check only,
which our rules don't run), Groq/OpenAI only if a key is configured. No telemetry (it even disables gh telemetry).
Browser-cookie reading (browser-cookie3) is optional, not installed by setup.sh, and only runs on an explicit
`configure --from-browser`. Verdict: CAUTION → installed with the rules above.
This copy: Score 36/100  MEDIUM CAUTION. Remaining: AE1 (reference list past the parser limit), RP1 career.md LinkedIn MCP via unpinned uvx (only on Ralph's ask; pin it then), E1 video.md:109 (podcast audio sent to Groq for transcription, documented).
