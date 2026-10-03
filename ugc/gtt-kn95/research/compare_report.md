# Compare report (cut v1 vs @toashouse 2.6k, the closest dust-job winner), 2026-10-03
Command: tiktok.py compare <toashouse> out/gtt_kn95.mp4 (research/compare_v1.txt, research/compare_v1/compare/compare.png).
| | Winner | Ours | Fix |
|---|---|---|---|
| Hook frame 0 | action (saw + dust) + burned-in caption | product in hand + on-screen hook text "why fifty?" at 0.0s | none (Ralph: no burned-in captions beyond the hook text) |
| First voice | 0.0s | 0.05s | none |
| Words per second | 4.8 (12s video) | 3.3 | none: playbook target 3.0-3.6 |
| Cuts per 10s | 1.6 | 3.0 | none: more cuts, one per sentence |
| Length | 12.8s | 30.5s | none (Grace default 30-45s) |
Found by looking at the hook frames: after 0.8s the S1 box tilts and its small print warps ("INDIVIALLY"). Fixed free: S1 uses 0-0.5s then a push-in hold on the front-on 0.5s frame (cut.py). Rebuilt as cut v2.
