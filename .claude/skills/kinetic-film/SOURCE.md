# Source

- **Upstream:** Scenario's "Kinetic Film" Claude skill (`scenario-kinetic-film`), from the Explorations page
  https://www.scenario.com/explorations/kinetic-film/ (linked from @emmanuel_2m, Scenario co-founder, on X
  2026-10-28: "I reverse engineered [Higgsfield Katana] and made a Claude motion design skill that replaces it").
- **Download:** `scenario-kinetic-film-skill.zip` (Vercel blob), 568,073 bytes,
  sha256 `2217ab5dbd452185a5c3c1509994da46b1ac20d2ebeaa888536244372ce73ebf`, files dated 2026-09-26, fetched 2026-10-29.
- **Licence:** the zip carries NO licence file and no `license:` line. Scenario's public skills repo
  github.com/scenario-labs/skills (@ d44410f, 2026-10-27) is MIT (Copyright 2026 Scenario Inc.) and holds 82
  skills, but not this one (its sibling `scenario-kinetic-music-video` is there, `license: MIT`). The page offers
  the zip as a free download for "your own brief". Treated like the Kapso skills (no LICENSE file, installed with
  CAUTION): fine for Ralph's own videos; do not redistribute the engine as a product. Fonts (Archivo, Instrument
  Sans, JetBrains Mono) are SIL OFL 1.1, licences beside them in `engine/fonts/`.

## Changes from upstream

- Folder renamed `kinetic-film`; SKILL.md rewritten to Ralph's skill standard (free-first route, his video rules,
  neighbour skills in the description); the Kaiju Postal walkthrough moved to `references/worked-example.md`;
  the Scenario-only "common mistakes" (image prompts, watermarks, brand marks, model ids, teams) live in
  `references/sound.md`, `references/scenario-mcp.md` and the worked example, where they already were.
- Added `scripts/synth_kit.py`: the 12 core sounds made with numpy, plus real CC0 key clicks if given a folder.
- `scripts/post.py`: `MAXS` env var passes a motion-blur sample cap to `render.mjs` (its existing 4th argument).
- `references/blocks.md`: a contents line added at the top. `examples/starter/spec.js`: retimed (see CHANGELOG), it failed its own check as shipped. Everything else (engine, other scripts, references, examples) is byte-for-byte upstream.

## Security review (SkillSpector --no-llm, 2026-10-29, on the upstream zip)

**100/100 CRITICAL, DO_NOT_INSTALL by count; max single finding HIGH.** 36 findings:
- AE1 HIGH: `snap.mjs` "partially analysed" (parser limit). Read in full: launches the browser, seeks, screenshots.
- E2 HIGH x3 (`finish.py`, `mix.py`, `render.py`): `{**os.environ, 'FILM_URL': url}`. They pass the normal
  environment plus the local server URL to their own `node` child processes; nothing is read, logged or sent.
- AST4 MEDIUM x26: fixed-argument `subprocess` calls to `ffmpeg`, `ffprobe`, `node` and the skill's own scripts.
- RP1 MEDIUM x3: documented `npx playwright install`, `npx skills add` (optional, in scenario-mcp.md).
- TT2 MEDIUM: `post.py` pipes raw frames to ffmpeg. LP3, P7 MEDIUM: no `allowed-tools`; the word "rules".

**Manual review:** every script read. Network: only `127.0.0.1` (the film's own local server) and
`get_fonts.sh` (Google Fonts' GitHub, runs only if the bundled fonts are missing). No eval, no downloaded code,
no credentials, no persistence, no telemetry. `render.py` calls `sysctl` (macOS memory) and falls back on Linux;
`finish.py`'s hardware-decoder check uses macOS VideoToolbox. The paid part is Scenario MCP (cloud, Scenario
credits), which the upstream already gates behind a dry-run price and the user's go.
**Verdict: CAUTION** (findings explained, purpose matches, no licence file), installed.

## Test render (cloud box, 4 cores, 16 GB, no GPU, 2026-10-29)

Starter spec rebranded "DAY ONE AI", 15 s, 889 frames at 60 fps, 1080p, no music, free kit.
- Full quality (default 99 blur samples, slower preset), 1 worker: ~2.9 s per frame (stopped at frame 240;
  the whole film would take ~43 min).
- Review mode (`MAXS=6`, `ENC="-c:v libx264 -crf 20 -preset veryfast -threads 2"`, `--workers 2`): 889 frames in
  12 min 52 s (~0.87 s per frame; ~1.6 s per frame per worker). The screenshot, not the blur samples, is the bottleneck.
- Same 106 frames (beats 5-10) at full quality vs review mode: still share 45.2% vs 45.2%, median motion 2.6 vs 2.7.
  Review renders give the same `finish.py` dynamism numbers, so check on them and render full quality once at the end.
- `finish.py` on the retimed starter: frames, size, H.264 level, loudness and holds PASS; still frames 42% (target
  <= 40%) and median motion 2.03 (target 2.5) FAIL. The starter is a short template with few blocks; a real film
  needs more moving blocks (Fly, Chain, Counters, camera moves) to clear those two. The hardware-decoder check is
  macOS-only and is skipped on Linux.

Final installed copy (2026-10-29): 100/100 by count, same findings plus TT1 HIGH on `post.py` (the `MAXS` env value,
cast to int, passed as `render.mjs`'s sample cap). No `__pycache__` shipped.
