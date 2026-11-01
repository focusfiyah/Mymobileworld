# Plant Therapy Christmas Cheer Essential Oil Blend 3 Set (Grace), 15 s

Status: **DONE 2026-11-01: cut v2 APPROVED (18.8 s, all three scents). Drive: Grace Tiktok assets/Plant Therapy Christmas Cheer (Grace) https://drive.google.com/drive/folders/1JaroYpWM1uz616yJWI2ZNdiDF7-xpExA (CURRENT - Christmas Cheer V2 + V2 script + HofR V2, not posted; v1 in Older versions). Kie: v1 $2.47 + v2 $0.81 = $3.28. Kling 0. Media in Drive (sets 1-2).**

- Route: hands + hand-free AI over Grace cloned v5 (ugc-product-ad), product lock (Omni), Seedance for no-product clips. 7 shots, 3 hand-free.
- Plan: `BOOK.md`; prompts: `make_shots.py` -> `shots.json` (PROMPT_LINT_OK); product truth `product_truth.json`; research `research/`; rooms `rooms/SOURCES.md`.
- Media (refs, rooms, review images) are gitignored: refs = planttherapy.com listing photos (`research/listing.json` image list) + 2 frames from @annmarieeckhart video 7696276798249749773 (13 s, 15 s); rebuild sheet with `make_sheet.py`. Pack to Drive with tools/media/media.py before the job ends.
- Next: on Ralph's OK record `python3 grace/gate.py ugc/plant-therapy-christmas-cheer --approve-book "<his words>"`, restore `grace/ref` hand sheets (media.py get), copy kie.py from ugc/oqq-wide-leg-pants, VO + 7 stills at once, S4 test clip first.

## v2 (2026-11-01, Ralph: "the only scent talked about is the Christmas Tree we need to mention and visualize the other 3 as well")
HANDOFF (session compacting): v1 files kept in `v1/` (vo_lines, scripts, BOOK). New `vo_lines.txt` = v2 draft, 64 words, grade 2.1, ~17 s at Grace's 3.8 words/s:
hook / storage box / "Christmas Tree smells like a fresh cut tree." / "Sugar Plum Fairy is sweet and citrusy," / "and Vanilla Spice is warm and cozy." / "Now people ask where the real tree is." / gift + orange cart.
Plan: reuse 7 v1 clips (S1 S2 S3 S4 S5 S6 S7, all approved), ADD 2 shots: S4b hand holds the Sugar Plum Fairy bottle beside halved clementines (Omni), S4c hand-free push-in on Vanilla Spice beside cinnamon sticks + vanilla pods by the tinsel tree (Omni). Cost: 2 stills $0.18 + 2 Omni $0.63 + one likely redo $0.41 = $1.22 Kie (Flow route $0.18 + redo), VO ~350 ElevenLabs chars. November cap $100, spent $0.
Waiting on: Ralph's OK on length (~17 s vs cut the storage-box line for ~15.5 s) and Kie vs Flow. Then: gate proofs (humanizer, line_sources, hooks touch, readability) newer than script, BOOK v2 with Sent line, --approve-book, prompts via prompt-master, mark, run.
