# FUSOU V1 (two Grace-script versions): HANDOFF for a new session (2026-10-04)

Client Grace, Ralph's job. Read first: `CLAUDE.md`, `grace/PLAYBOOK.md` (§6 "Removed items stay removed"), `ugc/fusou-vanity/v1ab/README.md`, `ugc/fusou-vanity/v1ab/REMOVED.md`.
Repos: focusfiyah/Mymobileworld and focusfiyah/Dayone-ai, both on branch `ccr-ddbbbcb3-tykpxz` (pushed, no PR opened: Ralph hasn't asked for one).

## State: DONE and APPROVED (Ralph, 2026-10-04)
- Two versions of FUSOU V1 from Grace's two scripts (`scripts.md`; Grace's words as written, only periods added for readability grade 5.3, "dissaperar" read as "disappears"; flash sale confirmed live; close "It's linked in the orange cart.").
- Finals: `ugc/fusou-vanity/v1ab/out/fusou_v5A.mp4` (24.9 s) and `fusou_v5B.mp4` (27.3 s). Rebuild: `cd ugc/fusou-vanity && python3 v1ab/cut_ab.py A5 B5` (free). VO files in `v1ab/vo/` (Grace B, 1,080 ElevenLabs chars, already paid; do not regenerate).
- Drive (Grace Tiktok assets / FUSOU `1LDxaLUgsy_QR0Nq_9B7vokF_JqaYy1hx`, organized 2026-10-04, nothing deleted, sizes verified):
  - Final videos `1wKbdhCfQZgopOdRGXfcnPw-NQi5iHb_w`: Videos 1-6, `Video 1A ... (Script 1) FINAL` `1cz_477QXARcQ1hDi1szs-DcfPwATwApp`, `Video 1B ... (Script 2) FINAL` `1CWsMqHmF_L2RMuKmkh2cTJBlSjODdJqj`, original `Video 1 - Lights On` `1E-Tffp3nBT-ofMLtamdnXcm0G_zpIszA`.
  - Scripts `1UiltfBgEi7IWMwt96RQ6RRFxdDBHQ_kQ`: 6-scripts doc `1kKPDR1Cv8RFQPYBhTnEQ0dLt2V8EK_-lZ5up3IPuwCs`.
  - Older versions `1WgpKqHP8x52NEPzK2udbdHJwqRLh4x_z`: first V1 A/B cuts.
- Spend: Kie $0.508 on the new face opening (2 stills + 2 clips; first tight tense-brow pair wasted). Balance 1,187 credits (~$5.94). Script gate OK (plan + cut) in `v1ab/`.

## What the final cut is (Grace's notes, all applied)
~2.7-2.8 s of Grace's FACE in bad bathroom light (medium shot, relaxed, mouth closed, brush on cheek, no lip sync: Ralph OK, VO plays over it; `clips/OPEN_FACE2.mp4`, still `stills/OPEN_FACE2.png`), vanity on screen by 2.8 s, slow push-in toward the full vanity (no hand), LED colours cold white > warm white > dim > warm yellow IN DAYLIGHT (room never dark), then storage: all drawers open, mirror-door cabinet (bags), stool drawer opening, wide close. No 3-boxes card.
Face references: Ralph's 3 photos only, `ugc/fusou-vanity/refs/grace/` (sheet + crops). NEVER the blue-shirt photo.

## Open items (none blocking)
1. Grace's two V1 scripts (A, B) + captions are not in the Drive scripts doc yet. Doc is Google Doc id above; overwrite via Composio GOOGLEDRIVE_UPLOAD_UPDATE_FILE (HTML) to keep emoji; ask Ralph first.
2. Original `Video 1 - Lights On` still sits in Final videos next to 1A/1B: ask Ralph if it should move to Older versions.
3. Video 2 was renamed "Drawer by Drawer" (was "Grace script (motion cut r2)"): mention if Ralph objects.
4. Bad lighting is "dull and flat", not harsh. Can be darkened free (`badlite` -> `bad` in `v1ab/cut_ab.py`) if Grace wants worse.
5. Repo folder `ugc/fusou-vanity` left as is on purpose (tools use relative paths). `v1ab/` is the clean job folder.

## Rules that bit us this job (all written into CLAUDE.md / PLAYBOOK / memory files)
- Removed items stay removed: keep/check `REMOVED.md` before sending ANY cut (dark room, tap/light-on shot, hand sweep V1S4, 3-boxes card, tight face crop, blue-shirt ref were each removed and some came back).
- Ask before every paid generation with the exact cost; show the still before the clip (done: still $0.09, clip $0.164).
- Own gate per job: `v1ab/kie_ab.py` / `vo_ab.py` call `grace/gate.py` on `v1ab/`. The old `ugc/fusou-vanity/checklist.json` has stale file times after a fresh clone and blocks `kie.py`: do not use `kie.py run_task` there; do not weaken the gate.
- Frame the face at medium distance and ask for relaxed brows in the FIRST prompt (the tight close-up came back tense).
- Push to the branch after each step (the stop hook asks); notify Ralph with PushNotification at every review point.

## Prompt to paste into the new session
"Continue the FUSOU V1 job for Grace (Mymobileworld + Dayone-ai, branch ccr-ddbbbcb3-tykpxz). Read CLAUDE.md, grace/PLAYBOOK.md, ugc/fusou-vanity/v1ab/HANDOFF.md, README.md and REMOVED.md. The job is approved and in Drive; ask me which open item in HANDOFF.md to do. Ask before any paid step, with the exact cost."
