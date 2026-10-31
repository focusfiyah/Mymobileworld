# broll-mcp: source and safety review (2026-10-24)

- Source: https://github.com/edigeh/broll-mcp @ d8fda0a4972235fb7591187242a4e583aca84f12 (2026-10-23, v0.1.0, MIT, single commit).
- What it is: a local stdio MCP server that searches archive.org (Prelinger, NASA, newsreels, stock_footage, feature_films),
  shows keyframes per scene, and cuts 1-60 s H.264 clips with a provenance JSON (source, licence copied verbatim,
  commercial_use, attribution text). No API key. Tools: search_footage, inspect_item, extract_clip, get_provenance.
- Install here: `uvx --from git+https://github.com/edigeh/broll-mcp@<sha> broll-mcp` (pinned to the commit; the README's
  form is unpinned). Cold install ~70 s (opencv 70 MB), pre-warmed by `.claude/hooks/broll_setup.sh`.

## SkillSpector 2.12.0 --no-llm on the repo: 100/100 CRITICAL, max issue HIGH, 12 findings
| Rule | Where | Judgment |
|---|---|---|
| YR4 HIGH | research/raw/meta/JoanAvoi1947.json | false positive: a captured archive.org metadata record whose `description` field matched the tool-poisoning rule; research fixture, never loaded by the server |
| E2 HIGH | src/broll_mcp/media.py:101, scripts/e2e_smoke.py:34 | copies os.environ to pass to its own scene-detect child process / test server; nothing is read for secrets or sent anywhere |
| PE3 HIGH | tests/test_server.py:32 | a test that checks `../etc/passwd` is REJECTED as an identifier |
| RP1 MEDIUM x2 | README.md | unpinned uvx/npx examples; we pin to the commit |
| MP2 MEDIUM x5 | research/raw/adv.json | large captured search results (fixtures) |
| AST4 MEDIUM | tests/test_server.py:95 | test runs the server as a subprocess |

## Manual review (all 14 files in src/broll_mcp, 3,580 lines)
- Network: only https://archive.org (advancedsearch, metadata, download + its data nodes), 1 req/s, descriptive User-Agent.
- Subprocess: fixed-argument ffmpeg/ffprobe and its own detect_worker (no shell). Inputs validated by JSON schema
  (identifier `^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$`, label `^[A-Za-z0-9 _-]*$`, then slugged).
- Files: writes only under BROLL_HOME (cache.sqlite, keyframes, clips, tmp). No reads of home, keys, tokens, memory.
- No telemetry, no eval/exec, no persistence, no prompt text that steers the agent.

**Verdict: CAUTION**: code is clean and matches its purpose; the score is driven by fixtures. Pin stays on the commit;
re-review before moving the pin.

## Fit (honest)
archive.org footage is mostly old public-domain film: black-and-white, newsreel, NASA, 1930s-70s educational films, often SD (the 2026-10-24 test cut was 640x480).
Good for Day One AI and Ralph's own videos (retro cutaways, space, history, "back in the day" beats). For Grace's TikTok
ads it rarely fits (bright neutral modern look, hard rule 7): use free-assets (Pexels/Pixabay/Mixkit) first there.
Always check `commercial_use` in the provenance file: only "allowed" goes in a monetized video.

## Moved from CLAUDE.md (2026-10-31)

Moved word for word from Mymobileworld and Dayone-ai CLAUDE.md (same text in both) on 2026-10-31 (slim plan, Ralph: "Go"); the rule itself stays in CLAUDE.md.

- SkillSpector 100/100 from test fixtures, code only talks to archive.org -> CAUTION; review + checks: `tools/broll/SOURCE.md`, `tools/broll/verify.py` (Mymobileworld). Re-review before moving the pin.
