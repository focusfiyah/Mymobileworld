# Source
github.com/Leonxlnx/unlazy @ 1667149 (v2.1.0, MIT). Installed 2026-10-06 (Ralph).
Changes: SKILL.md description broadened so it fires on every multi-step job; tests/, README, CI, research/, agents/ left out.
SkillSpector --no-llm: 100/100 CRITICAL, all pattern hits for what it documents (opt-in Stop-hook installer writes .claude settings = AS1/RA2/MP3; approvals stored in ~/.unlazy; npx/tsc mentions in docs). Manual review: no network calls, CHECK lines run only after explicit per-command approval, hook never installed without consent. Verdict CAUTION, installed. The Stop hook is NOT installed.
