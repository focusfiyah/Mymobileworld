# Handoff: Vans sequin Authentic, 10 AI videos for Grace (2026-10-21)

Read first: this file, README.md (Status), REMOVED.md (everything Ralph rejected), GATES.md (7/9 met), cut.py (EDIT = which clip windows each video uses),
grace/PLAYBOOK.md §6 "Vans sequin" lesson, and the prompt-master skill's "Ralph's stack" (Ralph 2026-10-21: write every image/video prompt with Prompt Master).

## Where it stands
- Review page (one page, newest round on top): https://claude.ai/artifact/L6jv2tbQ5AySPMuUiSr9GH . Round 9 = V2, V3, V4 rebuilt with feet-only moving shots; waiting on Ralph.
- All 10 finals exist (out/V1..V10_final.mp4, 7.1-13.6 s, music-only with a silent track, no text, AI finish applied in cut.py). FINALS_OK, cut gate GATE OK.
- Kie spent $15.86 vs $7.73 plan (50 images, 195 s Seedance, 48 s Kling 3.0). Kie auto-refills. Ralph's own Kling account: one 30-credit job stuck in QUEUING since ~02:00 UTC (generation AUt2nW9YQTZf...; feedback sent); 218 credits left.
- Media is NOT in git (*.mp4 ignored). handoff_media.json maps every clip in use + all 10 finals to a Kie file-host URL (expires ~3 days after 2026-10-21). Restore:
  `python3 -c "import json,requests; [open(p,'wb').write(requests.get(u).content) for p,u in json.load(open('handoff_media.json')).items()]"` (mkdir clips out first).

## Next steps
1. Wait for Ralph's notes on round 9 (V2, V3, V4). Fix only what he flags; ask before every paid redo with the exact cost.
2. On approval: Drive "Grace Tiktok assets" -> search for an existing Vans folder, else create "Vans Premium Authentic sequin (Grace)"; upload the 10 finals as "CURRENT - Vans sequin V<n> (2026-10-21).mp4"
   via Kie host URL + Composio GOOGLEDRIVE_UPLOAD_FROM_URL (account googledrive_lin-ernst), check sizes; add a Google Doc with the 10 captions from scripts.md (no emoji in Drive docs, no PDF).
   Put the folder link in README + CLAUDE.md Jobs line, mark GATES G8/G9, email + push Ralph the link.
3. Re-upload reminder: prompt-master-skill.zip (claude-skills/dist) was rebuilt twice today; Ralph to re-upload the latest. REMEMBER_ME_paste.txt was sent (Prompt Master rule).

## What Ralph rejected this job (do not repeat)
- Any held shoe that turns, flips or "switches side" (Seedance does this whatever the prompt says). Freezing it (Kling first=last frame) read as still images: also rejected.
- Sparkle/glint/light effects (my prompt wording caused them). Feet pointing opposite ways. More than 2 shoes in a video. Walking in place. Brand logos on props.
- Pale "floating" side tab: always pass a close-up of every real logo as a numbered reference (refs/real_vans_tab.jpg).
