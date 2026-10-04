# FUSOU vanity (Grace): HANDOFF for a new session (2026-10-03, end of V2 redo)

Client Grace, Ralph's job. Product https://shop.tiktok.com/us/pdp/1732251413004981161 (FUSOU 71" white vanity, $639.99). Hands-only (Grace's real
hands, refs `refs/hand_dorsal.png`/`hand_palm.png`), voiceover = ElevenLabs **Grace B** `bGrsdLmwBbYUgHRuMFOI` eleven_v4 (NOT Grace's own voice), no burned-in text.
Branch `ccr-5c521a26-tc2gk0` (Mymobileworld; Dayone-ai has the same branch name for handoff/memory files only).
Read first: `CLAUDE.md`, `grace/PLAYBOOK.md` (lessons 2026-10-03 at the bottom), this file, README `Status:`.

## State (all pushed)
- **V2 = DONE and APPROVED by Ralph** ("Good, that's the one"): Grace's own script verbatim, motion-first cut `out/fusou_v2_grace_r2.mp4` (42.7 s, 14 moving clips,
  no package card, no hand sweeping the vanity). In Drive FUSOU folder (id 1LDxaLUgsy_QR0Nq_9B7vokF_JqaYy1hx) as `FUSOU Video 2 - Grace script (motion cut r2).mp4`
  (id 1fU3brTc-7XLrXAL8YhFmH898CPb3glTy). Old V2 and my r1 upload are in the Drive trash. Scripts doc (id 1kKPDR1Cv8RFQPYBhTnEQ0dLt2V8EK_-lZ5up3IPuwCs) has the new V2.
  V2 Kie cost $0.918 = quote. Gate readability override for V2 ONLY is in `checklist.json` (`overrides`, Ralph's quote); other five keep max grade 3.0.
- **V1, V3-V6: "leave as is for now" (Ralph).** Local finals V1-V4 `out/fusou_vN_r4.mp4`, V5-V6 `out/fusou_vN_r5.mp4`; Drive still holds the older r1 versions of these, and the
  Drive scripts doc rows for them are the r1 text. Ralph has not yet said "good" on r4/r5, so do NOT replace them in Drive until he does.
- Kie balance 1289 credits (~$6.45) at handoff (it was ~$0.82 after V2, so it was topped up or another session added). Shared account; check with `curl -sS https://api.kie.ai/api/v1/chat/credit`.

## Likely next ask: apply the V2 motion look to V1, V3-V6 (needs Ralph's OK + exact cost first)
- Rule 7 in CLAUDE.md: every shot a real moving clip; no Ken Burns on photos, no freezes (`WK1_back` freeze, `kb` shots are the "pictures" problem).
- Reusable moving assets already paid for: `clips/WK1.mp4` (walk-in, use only 0-2.6 s), `WK2` (walk-in + mirror light on), `WK3` (dolly-out, use <= 4.6 s), `JD1a` (top-down drawer pull, first ~3 s),
  `B2a` (bag out from under the sink), `M1a/M2a-c/M3a-c/M4a/M5a/M6a`, `V1S2-S5`, `B1a/B1b`, `FL1a`. New clips: plate with `kie.py`/`v2_clips.py` templates (still nano-banana-pro $0.09,
  Seedance 2 Mini clip $0.041/s, 4-5 s = $0.164-0.205); a dolly-out = start frame grabbed from a walk-in clip. Ask before each paid step (Ralph's rule), one test first.
- Cut builder pattern: `cut_v2g.py` (explicit EDL with times from the Grace B word timings `vo/vNg_words.json`, `render_shot` from `cut_r5.py`); output a NEW filename, never overwrite.
- Before any new cut goes out: `python3 grace/gate.py ugc/fusou-vanity --stage cut` (needs tiktok.py compare proofs newer than scripts.md), frame-sheet QC, PushNotification.
- Grace B TTS can stutter: always STT-check (scribe_v2) every voice take; cut fragments for free (`vo_destutter.py` pattern).

## Where things are
- `scripts.md` 6 scripts + hook options + captions; `research/` gate proofs (hooks, humanizer_report, line_sources, product_facts, vN_readability, compare_*); `checklist.json`.
- `refs/` real listing photos and hand refs; `stills/WB.png` bedroom plate (photo F extended); `clips/`, `vo/`, `out/`.
- Drive uploads: Composio `GOOGLEDRIVE_UPLOAD_FROM_URL` after `kie.upload()` (videos); doc edits = rebuild HTML and `GOOGLEDRIVE_UPLOAD_UPDATE_FILE` via the Composio workbench
  (same file id; fetch the hosted HTML inside the workbench, then `upload_local_file`). Generator used for the scripts doc: see the transcript; data = `scripts.md` + the timing tables.
- Memory files updated 2026-10-03 (`handoff/CLAUDE_PREFERENCES.txt`, `MEMORY_SHORT.txt`, `GLOBAL_MEMORY.md`, both repos). Ralph still has to paste MEMORY_SHORT and PREFERENCES into claude.ai.
