# Still QC (2x)
- S3 r1 (Ralph's Gemini app, 2026-10-25): FAIL, shoes on backwards (Ralph): she faces left, both toes point right. Pants pass at 2x (solid matte black, front seam, wide waistband, pocket panel, full length to the floor); skin, almond nails, five fingers, room OK. Cause: prompt said "pointing the same way as her body", vague on a side view. Fix: $0 Gemini edit prompt (prompts/S3_gemini_edit_r2.txt); every still/clip prompt now names the toe direction in frame terms (FEET in tools/make_shots.py).
- Round 1 on Kie (2026-10-25, 8 x $0.09 = $0.72, Ralph: "Just use Kie to make the stills and continue"), checked at 2x (qc/storyboard_r1.jpg, qc/r1_2x*.jpg):
- S1 PASS: back view, white OQQ mark, hand on hip (5 fingers, whole wrist), heels to camera.
- S2 FAIL: feet point opposite ways (back shoe toe left, front shoe toe right): REMOVED.md item. Redo asked ($0.09).
- S3 PASS (framing changed: front three-quarter, hand on counter, phone in the pocket, toes to camera). Plays AFTER S4 (phone goes in, then shows in the pocket). The inspo's side shot is S8.
- S4 PASS: phone into the side pocket, 5 fingers, almond nails, solid matte black.
- S5 PASS: black walk-away, heels to camera, OQQ mark; elbows at the top edge only.
- S6 PASS: brown back three-quarter, hand on grey stool, phone top out of the pocket.
- S7 FAIL: back view walking away (planned front walk toward camera), repeats S5, hands in a hand-free shot. Redo asked ($0.09).
- S8 PASS: brown right side, phone up (inspo mirror moment, face out of frame), hand on hip, toes right.
- Round 2 (2026-10-25, Kie $0.18, Ralph: "Make sure to double check your prompts so that the still come out right"). Prompt fixes first: the body block's "frame cuts at her chest" and the top description fought "knees to floor" on S2/S7, and S7's back-mark ref + "when the back shows" pulled a back view; now legs-only shots carry no top/waist/back-mark text, and the shot, framing and foot direction come first (tools/make_shots.py LEGS, refs_for).
- S2 r2 PASS: knees-to-floor side view, both toes point left, back heel lifting; side tab sits a little forward of the real position (small).
- S7 r2 FAIL: front view is right, but her lifted foot shows its sole and heel to the camera, reads as a backwards shoe. Asked: redo $0.09 with "both soles flat on the floor, the soles never show", or drop S7.
- Round 3 (2026-10-25, Kie $0.27; Ralph: "Do not need to keep showing the backside so often. Front side and little of backside is good"; S5 + S6 rewritten as front views, S7 front walk). Every prompt linted (grace/prompt_check.py, new standard) and read in full before the run.
- S5 r3 PASS: front, knees down, toes at the lens, parallel, sequin Vans right.
- S7 r3 PASS: front walk toward the camera, soles flat, toes at the lens.
- S6 r3 FAIL: front view and hands right, but the shoes are a different pair at 2x (small brown/tan canvas checks, black heel panel, gold eyelets). Shoe colours now spelled out in every prompt (black and off-white only, black eyelets, checkerboard round the heel). Redo asked ($0.09).
- S6 r4 (Kie $0.09, Ralph: "Do the redos"): black and off-white sequin Vans, both toes the same way, front seam + waistband, five fingers on each hand. PASS.
## Final stills (2026-10-25)
S1 PASS (r1) · S2 PASS (r2; clip dropped: feet both ways) · S3 PASS (r1) · S4 PASS (r1) · S5 PASS (r3) · S6 PASS (r4) · S7 PASS (r3) · S8 PASS (r1)
