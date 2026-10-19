# Source and review

Written by Claude for Ralph on 2026-10-13 (no third-party code). Rules draw on Anthropic's skill authoring best
practices and "Prompting Claude Opus 5.5" (links in references/rules.md).

## SkillSpector (v2.12.0, --no-llm), 2026-10-13: 56/100 HIGH
- HIGH AE1 "obfuscated instruction text" in scripts/audit.py: the regexes that detect "think step by step" and
  "show your reasoning" contain those phrases. Expected; the detector has to name what it detects.
- MEDIUM AST4/TT2 subprocess: `git rev-parse --show-toplevel` (audit.py, deploy.py) and `python3 audit.py <skill>`
  (deploy.py), fixed argument lists, no shell, no network.
- MEDIUM LP3: no allowed-tools declared (same as Ralph's other skills).
Manual review: no network calls, no credentials, writes only to deploy.json targets and dist/. Verdict: APPROVE.
