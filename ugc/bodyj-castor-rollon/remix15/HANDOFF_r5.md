# Handoff: castor 15s videos, round 5 (2026-10-23)

Read first: `BRIEF.md` (job, winner, scripts), `REDO_PLAN.md`, `grace/PLAYBOOK.md` §6 (size lesson), this file.
Review page (republish to the same URL): https://claude.ai/code/artifact/6841627a-baca-40c2-bdfd-55d8dc8f53eb
(source `preview/index.html`; publish the embedded copy `preview/review_embedded.html`, built from index.html + `preview/s1-4.mp4`).
Drive: Grace Tiktok assets / BodyJ folder / "CURRENT - 15s castor videos" (1zDf5VAgV5Hoy5V3v61xl8snCiUN3GG9-),
Older versions subfolder 148CA_goEsAdnYYRyR5l54o8MvB5WbiPW. Short names: "CURRENT - V1 Liquid gold" ... "CURRENT - V4 Keep castor oil around".

## Ralph's notes on round 4 (2026-10-23, his words)
"there are issues with some of the videos. For example v1 it shows a head missing. The other videos her hands do not
stay true to Graces skin tone, it looks like a different hand with a different skin tone."

## What went wrong (root causes)
1. **Hand reference was wrong.** I used `redo/hand_ref.png`, a crop of an old AI still (`../stills/S4.png`), NOT Grace's real
   hand sheets. Standing rule (grace/ref/hand-sheets/README.md, Ralph 2026-10-15): use `grace/ref/hand-sheets/with_bracelet.jpg`
   or `without_bracelet.jpg` for every Grace hand shot, and ASK RALPH which sheet before any hand still. Not done. Also the
   Seedance clips got only the still + label refs, no hand ref, so skin tone drifted clip to clip.
2. **"Head missing" in V1:** find it. Likely V1h (hair ends over the shoulder, head cropped off at the top: reads as a
   headless body) or V1g (elbow, arm up, no head). Check every V1 shot (`out/remix15_v1_plan.json` has the shot times).
   Also check V2-V4 for the same (V4d4 hair ends, V3f neck).

## Plan for round 5 (ask Ralph before any paid call, exact cost, one approval)
1. Ask Ralph: bracelet or no bracelet sheet? (rule). Keep the mauve tee? Confirm the head-missing shot with him if unclear.
2. Free check first: list every shot whose hand skin tone differs from Grace's sheet (side-by-side sheet vs one frame per shot)
   and every shot where a body shows without a head. Only those get redone.
3. Stills: `redo.py` `pm()` prompts (size + shape rules first, prompt-master), hand ref = Grace's sheet (not hand_ref.png),
   add "skin tone exactly as the hand reference sheet, same in every frame". Body-part shots: frame so no headless body
   (show the face from the eyebrow up, or crop to the part only, e.g. just the hair ends in the hand, no shoulder/neck).
4. Clips: Seedance 2.0 Mini reference mode; add the hand sheet as a reference image too (refs: still, front label, product
   sheet, Grace hand sheet); camera locked where the bottle could grow. No Kling (Ralph: low credits). One test clip first.
5. Cut: `cut.py N --final` (edits.json; PRE crops for brow shots keep the mouth out), `qc.py N out/remix15_vN_final.mp4`,
   `check.py cuts`, `grace/gate.py . --stage cut`, compare, 2x edge zooms, REMOVED.md, AI finish (in cut.py --final).
6. Deliver: review page republished, Drive (current -> Older versions as v3, new CURRENT with short names), email Ralph
   (Composio gmail_correa-comus); PushNotification was not available in this session (try ToolSearch select:PushNotification).

## Tools/state
- `redo.py`: stills (`python3 redo.py stills ID`) + clips (`redo.clip`); upload refs ONE AT A TIME before parallel runs
  (the parent kie upload cache is not thread-safe). Run from `remix15/` (it chdirs to the parent for kie.py).
- Voice: `vo/v1..v4.mp3` (E voices, approved), word times `vo/vN_words.json`. Don't re-render voice.
- Kie balance at handoff: check `curl -sS https://api.kie.ai/api/v1/chat/credit` (was ~1534 credits = $7.67 on 2026-10-21).
- Spend so far: ElevenLabs 1,143 chars; Kie round 3 ~$11.14, round 4 ~$5.14; Kling 0.
- Winner now at 5 sales / 2,126 views (2026-10-22).
- Kie logs can contain signed Volcengine URLs: GitHub push protection blocks them; strip `?X-Tos-...` from kie_log.json before committing.
