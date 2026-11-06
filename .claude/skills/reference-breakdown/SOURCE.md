Source: Scenario "scenario-remake" skill, https://www.scenario.com/explorations/content-engine/ (post https://x.com/Scenario_gg/status/2118387681197457494, 2026-11-05). No licence file in the zip; offered as a public download.
Copied unmodified: scripts/breakdown.sh, scripts/measure.py. SKILL.md and references are our own condensed rewrite.
Left out: build.py, the generation steps (need the paid Scenario MCP, not connected here), story-engines, episode.json.
Reviewed 2026-11-06: grep for network/eval/exec found one curl (URL download in breakdown.sh) and ffmpeg/ffprobe subprocess calls only. SkillSpector not installed here, not run.
Tested 2026-11-06: breakdown.sh on the post's 49 s demo, 22 s, wrote measure.txt with 15 cuts. No Whisper, so no transcript.
