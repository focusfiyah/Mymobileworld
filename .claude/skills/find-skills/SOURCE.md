Source: https://github.com/vercel-labs/skills (MIT, Vercel), folder skills/find-skills
Commit: 3694740352eeef5cdd689af694c485f1ff62eec3 (2026-09-28)
Copied: SKILL.md + LICENSE. Local changes: every CLI call pinned to `skills@1.7.0` (npm, MIT, same repo),
and Step 6 rewritten to Ralph's house rules (scan before install, install into both repos instead of `-g`,
claude.ai zip for every device, DO_NOT_TRACK=1). The CLI sends install telemetry unless DO_NOT_TRACK or
DISABLE_TELEMETRY is set.
Scanned 2026-10-01 with SkillSpector (--no-llm): upstream 12/100 LOW. All 12 findings were RP1 "unpinned npx skills"
(fixed in this copy by pinning; this copy 7/100, the one hit is the quote on the line above). Manual read: instructions only, no scripts, no hidden text, network use limited
to the documented skills.sh search + GitHub. Verdict: APPROVE.
