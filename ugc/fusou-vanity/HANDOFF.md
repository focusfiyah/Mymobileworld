# FUSOU vanity (Grace): HANDOFF for a new session (2026-10-03)

Client Grace, Ralph's job. Product https://shop.tiktok.com/us/pdp/1732251413004981161 (FUSOU 71" white vanity, $639.99). 6 hands-only videos (Grace's hands
only), voiceover = ElevenLabs **Grace B** `bGrsdLmwBbYUgHRuMFOI` eleven_v4 (NOT Grace's own voice), no burned-in text. Branch `ccr-5c521a26-tc2gk0`
(Mymobileworld). Read first: `CLAUDE.md`, `grace/PLAYBOOK.md`, this file, `ugc/fusou-vanity/README.md` Status, `shot_plan_v2.md`.

## Where things are
- `scripts.md` 6 scripts (voice lines, hook text options, captions, sources). Also in Drive: Grace Tiktok assets / "FUSOU Vanity Desk – Grace hands-only (2026-10-02)" (doc
  id 1kKPDR1Cv8RFQPYBhTnEQ0dLt2V8EK_-lZ5up3IPuwCs). **That doc still says "Grace's own voice" and the old shot lists: overwrite it with Composio
  `GOOGLEDRIVE_UPLOAD_UPDATE_FILE` (HTML, same file id; the Drive connector garbles emoji).**
- `refs/` real listing photos `listing_01..20.jpg`, crops `vanity_*.jpg`, `base_A_916.jpg` (photo A padded to 9:16), Grace's hand refs `hand_dorsal/palm.png`.
- `kie.py` runner (import it; prompts come from the script you write), `v1_run.py` (Video 1 stills/clips), `edit_test*.py` (edit-the-real-photo recipe), `vo_v1.py`.
- `stills/`: `V1A_fix`, `V1B_fix` (clean wide stills), `EDIT_TEST2` (hand near the mirror button), `CLOSEUP_TEST` (drawer close-up, drifted). `clips/`: `V1S2-5`, `EDIT_TEST2_clip`.
- `vo/v1_voiceover.mp3` (21.9 s, 2.8 wps) and `vo/v1_voiceover_1p2x.mp3` (18.2 s, 3.4 wps, free atempo), `vo/v1_words.json`, `vo/v1_lines.json`.
- `out/video1_lights_roughcut_v3.mp4` silent rough cut (no hand), v1/v2 earlier. Spent so far: **$1.94 Kie** (balance 1651.8 -> 1263.6 credits) + V1 voiceover.

## Decisions (Ralph)
White, Grace's REAL hands (long almond, mauve + white tips: NOT the Vicks look), real listing photo as the master, bedroom/daylight look (no dark video), no hand in wide
shots (big), no hand glide, Grace B voice, examples' style (4 TikToks: @sdbby88 2.1M is the hands one; 4.4 wps, 2.7 cuts/10 s). Ask before EVERY paid step with the exact cost.

## What worked / what not (do not repeat)
- Prompt-only stills do NOT hold the vanity (cubbies, mirror shape, drawers drift; $0.63 lost). **Edit the real photo** (pad to 9:16 free, then Nano Banana Pro edit: repaint wall/floor,
  light LEDs, add small hand). Model often leaves the blurred padding: rebuild free (wall from a clean copy, floor stretched + soft blur; find band rows with per-row Laplacian).
- Close-up crops drift (drawer proportions): check a plate before making clips from it. Seedance adds a push-in and ends hands in odd poses: trim.
- Hand reaching from the camera looks huge in a wide: hands only in mid-close shots.

## Next steps, in order (nothing paid until Ralph says OK to `shot_plan_v2.md`)
1. Ralph approves the plan (total new Kie $2.60; steps 1-3 in the plan). 2. Step 1 test: still M1 + clip M1a, show, stop. 3. Step 2 plates, contact sheet, stop. 4. Step 3 clips.
5. Grace B voiceovers V2-V6 (ask), retime each cut to the real word timings, add SFX (click, soft whoosh, CC0), loudnorm -16 LUFS, 720x1280.
6. QC every cut (no clip <1.0x, product never cropped/smeared, same vanity in every shot, hand small, frame check where the hand crosses the product), coach
   `tiktok.py compare` against @sdbby88, fix, then send. 7. Drive: Grace Tiktok assets/FUSOU folder `1LDxaLUgsy_QR0Nq_9B7vokF_JqaYy1hx`: videos via Kie `upload()` + Composio
   `GOOGLEDRIVE_UPLOAD_FROM_URL`, update the scripts doc. 8. PushNotification at every review point; keep the README Status line current; add lessons to `grace/PLAYBOOK.md`.

## Prompt to paste into the new session
"Continue the FUSOU vanity job for Grace (Mymobileworld, branch ccr-5c521a26-tc2gk0). Read CLAUDE.md, grace/PLAYBOOK.md, ugc/fusou-vanity/HANDOFF.md and README Status, then
ugc/fusou-vanity/shot_plan_v2.md. Ask me for the OK on the plan and its exact cost before any paid step."
