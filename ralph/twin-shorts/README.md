# AI twin shorts (free automated talking heads)

Status: 2026-11-15: test 1 in progress (kit promo 7 "What's inside", glasses take Talking 03, MuseTalk running on CPU). $0.

Route (Ralph 2026-11-15, tapped "AI twin"; start with the 4 existing kitchen takes, remind him to record more base takes when variety is needed):
1. script.txt -> vo_script.txt (spelled for the voice) -> `~/.presenter-tools/cbx/bin/python -I vo_gen.py` (free Chatterbox clone) -> `python3 join_vo.py` -> `python3 check_vo.py` (VO_WORDS_OK)
2. base take (Drive "Ralph AI Assets", Talking 0x) cut to the VO length at 25 fps -> MuseTalk 1.5 (`ralph/avatar-test/tools/musetalk_setup.sh`, --saved_coord) -> `ralph/avatar-test/tools/lips_only.py` (real face, only the lips from MuseTalk)
3. `edit.py TALK VO OUT --version A|B` (A = hook text only, B = reel style: pop words + subtitles) -> ai_finish.sh
4. Gates: GATES.md (check_cut.py, check_hook.py).
5. Accent check: a flagged clip is fixed BEFORE Ralph sees the cut (Flow redo, else text-to-speech in his clone for that line; Ralph 2026-11-24). Ralph 2026-11-16, posted T2 ended in a foreign-sounding voice; he asked for a skill that can listen): `accent_check.py` (speech-to-text language ID + SpeechBrain accent ID, both free and local) on every raw Flow clip before speech-to-speech AND on every final cut; any ACCENT_FLAG window = remake that Flow clip (10 credits, ask) before the cut goes to Ralph.
Style reference (style only, nothing from its workflow): Brain note "Free talking head automation".
Media (base takes, vo, renders) stay out of git: Drive via tools/media.
