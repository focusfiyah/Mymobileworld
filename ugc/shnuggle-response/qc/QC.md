# QC (2026-10-16, review 1)
Measured (qc/cut_qc.py): R1 0 FAIL, R2 0 FAIL (duration = VO, audio level, every shot bright, not yellow, moving).
Eye checks (qc/R1_sheet.jpg, R2_sheet.jpg, *_hands.jpg, per-clip strips at 2-4 fps):
- Hands: birthstone ring + thin gold ring, no bracelet/watch after fixes; hand enters from a frame edge; grips the item.
- Found and fixed free: R1-01 fake 'shnuggle' logo on the coffee sleeve (fix_sleeve.py, shot starts at 1.5s after the hand leaves); R1-05 teal bangle (cropped, teal blob check = ring only); R2-10 bangle from 0.75s (only 0-0.7s used); R2-12 jump to another scene at 1.21s (only 0-1.2s used).
- OPEN: R2-02 infant tub slides into the big bath and a second tub appears on the floor -> paid redo asked ($0.164).
- Scale: Shnuggle smaller than the claw-foot bath in every wide R2 shot (R2-01, 04, 06, 07, 13, 14).
- No text, no child, no price, product logo/shape unchanged; REMOVED.md checked.
- Accepted: R1-13 white sleeve cuff at the bottom-left edge (phone POV, no bracelet).
- R2-02 fixed free: r2 clip cropped (432x768 @ 0,180) to the hand lowering the infant tub; wall crossing outside the frame.
Status: R1 ALL CLEAR. R2 ALL CLEAR.

# QC (2026-10-16, review 2: plug removed)
Ralph: "Remove the plug because the product does not have it that size and positioned where it is. You can mention it however do need to show it."
- Plug-pull shots R1-11 and R2-12 cut; the voice still says "easy-drain plug" over the feet shot.
- Plug painted out free (tools/unplug_kf.py, hand-read keyframes, frame-accurate checks): R1-12 (row blend), R1-14 (duck protected), R2-01; earlier fixes R1-02, R1-08, R1-13, R2-08.
- Cropped above the plug: R1-07 [90,0,540,960], R2-04 [85,0,540,960] (+ the inner plug painted out).
- Dense check every 0.45 s over all these shots in the finished cuts: no plug left. Shower-tray and big-bath drains stay (real fixtures, not the product).
- cut_qc: R1 0 FAIL, R2 0 FAIL. Durations 45.67 s / 39.53 s.
Status: R1 ALL CLEAR. R2 ALL CLEAR.
