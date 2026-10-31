Source: https://github.com/bradautomates/claude-video (MIT, Bradley Bonanno), commit 03ceb42 (2026-09-25), skill v0.3.2.
Found via Ralph's TikTok from @bengusberg ("Teach Claude any skill using YouTube", 2026-10-31).

Copied: skills/watch/scripts/*.py (minus build-skill.sh) and LICENSE. The upstream SKILL.md is kept as
references/upstream.md; SKILL.md is ours. Not copied: the plugin SessionStart hook (advisory only), tests, CI.

Changes from upstream:
- Every `GEMINI_API_KEY` in scripts/*.py renamed to `GEMINI_FREE_API_KEY` (config.py, setup.py, watch.py, gemini.py).
  Why: in Ralph's environments GEMINI_API_KEY is his paid key and upstream's default engine `auto` would have used it
  on every run. Tested 2026-10-31: with only GEMINI_API_KEY set, `setup.py --json` reports engine local and
  gemini_key_present false; with GEMINI_FREE_API_KEY set, engine gemini.
- SKILL.md rewritten to Ralph's skill standard: free key only, no paid fallback, no installers without his OK.

Review 2026-10-31, SkillSpector 2.12.0 --no-llm: full upstream repo 100/100 CRITICAL (74 findings, mostly tests and
CI); this copy 100/100 CRITICAL with 19 findings, all expected behaviour on manual review: PE3 (config.py reads the
key from env / ~/.config/watch/.env / cwd .env), E4 (gemini.py uploads a downloaded video to Google's Files API,
documented, gemini engine only), E2 (local_whisperx.py passes the environment to its own local child process;
WhisperX is not installed), AST4/EA (subprocess runs of yt-dlp, ffmpeg, ffprobe, and setup.py's optional installers,
which our rules do not run), E1/E5 (Groq/OpenAI transcription endpoints, used only if their keys are set; none are).
Outbound hosts: the video site via yt-dlp, generativelanguage.googleapis.com (key in the x-goog-api-key header only),
api.groq.com / api.openai.com only with their keys. No telemetry, standard library only.
Proxy check 2026-10-31: a bogus key sent to generativelanguage.googleapis.com got HTTP 400, so the environment proxy
does not swap in the paid key; the free key is what Google sees.
Verdict: CAUTION, installed with the changes above.
