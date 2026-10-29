# QC, Vans V13-V17 cut v2 (2026-10-29)
Machine checks (tools/cutqc.py, every cut): CUTQC_OK x5: 1080x1920, 27.43-27.47 s vs VO 27.52 s, audio = Grace's VO (sync r 1.000), no flash frames off the planned cuts, no dark frames, peak -3.3 dBFS. Cut gate (`grace/gate.py --stage cut`): GATE OK.
Look checks: every clip strip at 2 fps (qc/clips_V1x.jpg), the failing ones at 4-6 fps (qc/fine_*.jpg), every first second at 2x (qc/first_second_2x.jpg), every replaced window in the final cut (qc/redo_windows_final.jpg), every blue object in all five cuts at 4 fps (qc/blue_scan.jpg).

## REMOVED.md, row by row
| Item | Result |
|---|---|
| Blue band as a wrist strap | Found once: V16K (on the still too; my still QC missed it). Fixed free: V16K starts at 0.75 s, cropped 1.28x from the top, band out of frame (re-scan clean). All other blue = band on a finger or thumb, or painted stairs. |
| Logos on props | None (plain cups, plates, chairs). |
| Vans logo on a gift box / boxes | No boxes. |
| Feet opposite ways / empty shoes | V14G, V14H, V16J stills redone (r2); V14H clip redone; none left. |
| Grip switching mid-hold | None in the used windows. |
| Pale or floating side tab | Tab black with white VANS wherever readable (2x). |
| Extra hands | None. |
| Cream insole | Insoles red with the white VANS box. |
| On-screen text, cards | None (cut.py draws no text; cut gate OK). |
| Shoe flipping or turning in her hand | Trimmed to steady windows: V14I (shot shortened to 2.2 s), V16I from 1.5 s, V17I from 1.65 s, V16K from 0.75 s (a slow tilt of about 15 degrees left, no flip). V16B redone (r2: pair held still). |
| Walking in place | Walks travel (V13J, V14J, V15H/J, V16H/J, V17C/J). V14H redo: feet stay under the camera while the path moves. |
| A third shoe | Max two shoes in every frame. |
| Sparkle or glint effects | None; no effect words in any prompt. |
| Held shoe from the wrong side of the pair | Side-on holds show the outer side with the tab, as written. |
| Solid black sequin toe | Four stills redone (r2); none in the clips. |
| Empty worn shoe | Fixed in the r2 stills (V14H, V16J). |
