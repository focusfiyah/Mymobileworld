# Gates: Dr. Nice's Kids' Boo-Boo Gel (plan stage, 2026-11-03)

- [ ] G1: Script gate passes (all Rule 0 proofs newer than the script, no banned phrase)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/dr-nice-boo-boo-gel
  EXPECT: GATE OK
- [ ] G2: Every still and clip prompt passes the prompt lint
  CHECK: cd /home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel && n=$(ls prompts/*.txt | wc -l) && ok=$(for f in prompts/*.txt; do python3 ../../grace/prompt_check.py lint $f | tail -n 1; done | grep -c PROMPT_LINT_OK) && test "$n" -gt 5 && test "$n" = "$ok" && echo "LINT_ALL $ok"
  EXPECT: LINT_ALL
- [ ] G3: Product reference sheet, label and logo close-ups exist
  CHECK: cd /home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel && ls refs/product_sheet.png refs/closeup_label.png refs/closeup_logo.png refs/pump_open.png | wc -l
  EXPECT: /^ *4$/m
- [ ] G4: BOOK.md has the review link and one TOTAL line, no blanks
  CHECK: cd /home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel && grep -c "^Sent to Ralph: https://claude.ai/\|^TOTAL: \$[0-9]" BOOK.md && ! grep -q "___\|\$__" BOOK.md && echo NOBLANK
  EXPECT: /^2\nNOBLANK/m
- [ ] G5: Both scripts have no banned phrase, no price, no medical claim words, close on the orange cart
  CHECK: cd /home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel && ! grep -Eiq "order (it )?now|heads up|\$[0-9]|reviewer|the label says|—|–|cure|heal|infection|antibiotic|antibacterial|kills|germs" scripts.md && test "$(grep -c "orange cart" scripts.md)" -ge 2 && echo CLEAN
  EXPECT: CLEAN
- [ ] G6: RESEARCH.md has the 7 sections and the 4 role lines
  CHECK: cd /home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel && grep -c "is the hook\.\|is the desire\.\|is the objection killer\.\|is the purchase justification\." research/RESEARCH.md
  EXPECT: /^4$/m
- [ ] G7: Ralph notified (phone push + email) with the review link (manual)
Later stages (after his OK): stills QC at 2x, test clip, clips, cut + QC + AI finish, REMOVED.md check, Drive folder, merge to main, brain note.
