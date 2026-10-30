# Gates: Magnesium Trio plan (2026-10-30)
- [ ] G1: script gate passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/magnesium-night-trio
  EXPECT: GATE OK
- [ ] G2: every prompt linted
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/magnesium-night-trio/shots.json
  EXPECT: PROMPT_LINT_OK
- [ ] G3: script readability grade <= 6
  CHECK: cd /home/user/Mymobileworld/ugc/magnesium-night-trio && python3 ../../.claude/skills/tiktok-shop-coach/scripts/tiktok.py readability scripts.md
  EXPECT: Grade level \(Flesch-Kincaid\): [0-5]\.
- [ ] G4: book has one TOTAL line and a Sent to Ralph line with a link
  CHECK: cd /home/user/Mymobileworld/ugc/magnesium-night-trio && grep -c -E "^TOTAL: \$2.79$|^Sent to Ralph: https" BOOK.md
  EXPECT: ^2$
- [ ] G5: (manual) review page shows script, shots, product sheet, rooms, hand sheet; Ralph notified by push + email
