Source: https://github.com/kajisho5/ffmpeg-skill (MIT, npm ffmpeg-skill), commit 9bdb444, copied 2026-11-06 after Ralph's OK (post https://x.com/heyrimsha/status/2118662273044807904).
Copied unmodified apart from line-length trimming of SKILL.md (see CHANGELOG): SKILL.md, scripts/ (46 files), references/, templates/, LICENSE.
Left out: site, demos, brand, evals, tests, docs, mcp, bin/install.js, npm package files.
Reviewed 2026-11-06: grep of scripts for network, eval/exec, base64, pickle found only report.py's contact-sheet base64 and install.js (not copied). Python standard library only.
Tested 2026-11-06 on a 49 s 1280x720 clip: probe.py, loudness.py --dry-run, fit.py --aspect 9:16 --fit crop (10 s, 406x720), check.py --platform tiktok (13 checks: true peak -0.4 dBTP failed, resolution below 1080 warned). SkillSpector not installed here.
