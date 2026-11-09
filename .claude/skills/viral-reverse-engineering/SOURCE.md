Source: https://github.com/social-media-skills/skills (MIT)
Commit: f28cef2, copied 2026-10-29 for Ralph's AI on Autopilot reels (Ralph 2026-10-29: "Yes", bring in the picked skills).
Copied: SKILL.md, references/ and LICENSE (evals/ left out).
Scanned 2026-10-29 with SkillSpector 2.12.0 (--no-llm): 0/100 LOW SAFE  scripts=0.
Local use: see the social-growth-stack skill (which step uses this skill, our accounts, Composio instead of WoopSocial).
Added 2026-11-07 from https://github.com/Jakeschincariol/instagram-agent-skill (MIT, Jake Schincariol), commit d03c56b, Ralph tapped "Add ranker, Shorts+TikTok (Recommended)". scripts/swipe.py is ig-viral/swipe.py with one local change: it reads hooks.json and hookscore.py from the sibling reels-script skill. scripts/to_swipe.py is ours (TikTok/Shorts to TSV). SkillSpector 2.12.0 (--no-llm) on the whole skill after the change: 16/100, two MEDIUM notes, both read: SKILL.md has no tool allow-list (generic), and to_swipe.py runs yt-dlp with subprocess (argument list, no shell; yt-dlp pinned to 2026.10.26 when run through uvx). Licence: LICENSE-instagram-agent.
