# Exact-product route

## Contents

- Exact-product route: complex products that must not drift (FUSOU vanity, 2026-10-03, approved)

## Exact-product route: complex products that must not drift (FUSOU vanity, 2026-10-03, approved)
Use for furniture, appliances and anything with many parts (drawers, knobs, mirrors). Prompt-only stills and crops redrawn
by the model drift; this route kept the product pixel-exact across 6 videos. Template job: Mymobileworld `ugc/fusou-vanity/`
(README, step2.py stills, step3.py clips, cut.py on word timings, build_doc.py scripts doc).
1. Base = the brand's REAL listing photo cropped to 9:16 (clean label lines/patches free with cv2.inpaint first).
2. Nano Banana Pro edit adds ONLY the hand (prompt: "only the hand enters from the frame edge, wrist at the edge, no forearm").
3. `scripts/pasteback.py still BASE AI OUT`: real pixels everywhere except what the AI changed. Clips: Seedance Mini with a
   "locked-off camera on a tripod" prompt, then `pasteback.py video BASE CLIP OUT --hull --seed <still>_mask.png`
   [+ `--ai-box x0,y0,x1,y1` where the hand MOVES an object (drawer, plug, door) and out to the frame edge where the wrist exits;
   `--no-light` unless lights switch on; `--hand-below ROW`]. Never trust a few sample frames:
4. `scripts/qc_hands.py CLIP`: every frame vs raw (background showing through the hand, missing wrist). Then check by eye where
   the wrist crosses wood/beige (the metric is blind there). Seedance can swap objects in frame 1 (lipstick tray) or open a
   door by itself: compare frame 1 with the still and drop the clip.
5. Free shots: `scripts/kb.py` slow push-in on real photos (INTER_AREA, 1.05x: less crawl than Seedance's own push-in).
   `scripts/finish.py` grain only (sway OFF: sub-pixel moves on soft photos read as shimmer). Measure shimmer on the FINAL file.
6. Lights: `scripts/darkroom.py` (mask = lit frame minus the real unlit photo; `--on`, `--colors` for the listing's exact
   colour modes on the words, `--dip` on "dims"). Ralph liked it: use it for every product with lights.
7. Never stretch clips; overlays (pop-up cards) left of TikTok's right-hand buttons; anchor them to the exact phrase.
