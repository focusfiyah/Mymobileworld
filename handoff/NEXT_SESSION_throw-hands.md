# Next session: Throw Hands card game ad (Grace), r2 with Google Veo

Branch `claude/project-thread-gh53m6` (focusfiyah/Mymobileworld). Job folder `ugc/throw-hands-rps/` (README Status line, GATES.md, PLAN.md, REMOVED.md).

## Where it stands (2026-10-14 03:10 UTC)
- Cut r1 (29.4s, Grace B VO, no text) sent: https://claude.ai/artifact/2LZPz3movpRwm8CQWTovQF. Kie $2.90 of the $2.95 approved cap.
- Ralph's notes on r1: (1) the box warps "when Grace opens it" (shot S3), (2) cards stick to hands, not held (S5 palm-up card, S7 card sliding under fingers).
- Ralph wants the redo on **Google Veo through his own Google API key** (he has Google Flow), not Kie.
- Key setup: Ralph added a network secret `GEMINI_API_KEY` in the "My World" environment for `generativelanguage.googleapis.com`, header `x-goog-api-key`, no prefix.
  Old session tests: first try reached Google but "API key not valid" (prefix was Bearer); after his fix, "unregistered caller" (no key sent).
  **Step 1 of the new session:** `curl -sS "https://generativelanguage.googleapis.com/v1beta/models?pageSize=200"` and list the veo models. If it errors, tell Ralph the exact error (one line) and what to check.
- Price: look up the current Gemini API Veo price (per second) and tell Ralph the exact cost before any clip. Flow plan credits may not cover API use.
  Fallback if the key can't work: Veo 3.1 on Kie (`python3 kie.py veo S5`, Fast $0.30 / `veo_lite` $0.15 per clip; route already in kie.py, untested). A decision card about the Kie route is still open in the thread.

## Plan for r2 (ask before every paid clip, exact cost; riskiest first)
1. Test S5 on Veo first (image-to-video from `stills/S5.png`, 9:16, ~6s, prompt = shots.json `video_veo` + identity/cards blocks + `video_suffix`). QC every frame at 10fps: cards pinched by their edges, released onto the table, never stuck to a palm.
2. If good, S3 (box tilt, prompt says rigid box) and S7. Then run `python3 boxfix.py <clip> <out> --clear-label` on S3 (real box front pasted frame by frame).
3. Re-cut with `cut.py` (PARTS table: point S3/S5/S7 at the new clips; S8 currently borrows S5 3.6s-end and S7 3.9-4.5s, re-check those), drop Veo's own audio, `ai_finish.sh`, gate `--stage cut` (rerun `tiktok.py compare` vs research/videos/7659861170408426783), REMOVED.md check, playable Artifact (republish th_r1 page as a new version or new page), email (Composio GMAIL_SEND_EMAIL, account gmail_correa-comus) + PushNotification.
4. On approval: Drive "Grace Tiktok assets/Throw Hands Card Game (Grace)", CURRENT- prefix, Older versions subfolder (G7).

## Notes
- Grace's skin in S5/S6/S9 matches her real hand photo (refs/grace_hand.jpg); S3 only looks darker (palm in shade). No fix needed.
- GATES.md: 5 of 7 met. G3 is unmet as recorded; G7 waits on approval.
