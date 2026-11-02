# Gates: Buttah Silky Soft Towels (plan stage, 2026-11-02)

- [x] G1: Script gate passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/buttah-silky-towels
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b69c62700bd2dd31bd9528c07b50769ed96c15711f0d86232c5fa99d3267f8ad; exit=0; EXPECT=matched; output-sha256=d6be10eab47db4808ad98b557c0da077fefee1360779ac765ac9ec5d77d1c57e; output-bytes=165; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/buttah-silky-towels; path=7f4fb4b02918/15 entries
- [x] G2: Every still and clip prompt passes the prompt lint (14 files)
  CHECK: cd /home/user/Mymobileworld/ugc/buttah-silky-towels && for f in prompts/*.txt; do python3 ../../grace/prompt_check.py lint $f | tail -n 1; done | grep -c PROMPT_LINT_OK
  EXPECT: /^14$/m
  EVIDENCE: automatic-evidence=v1; definition-sha256=6fb4424b50402cb7e08ebdcef6988f15c746cf1df1a549669dd25b453fafc798; exit=0; EXPECT=matched; output-sha256=9a92adbc0cee38ef658c71ce1b1bf8c65668f166bfb213644c895ccb1ad07a25; output-bytes=3; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/buttah-silky-towels; path=7f4fb4b02918/15 entries
- [x] G3: Product reference sheet and both logo close-ups exist
  CHECK: cd /home/user/Mymobileworld/ugc/buttah-silky-towels && ls refs/product_sheet.png refs/closeup_logo.png refs/closeup_badges.png refs/towel_ref.png | wc -l
  EXPECT: /^ *4$/m
  EVIDENCE: automatic-evidence=v1; definition-sha256=41dcf163d016d8c83d5f634345c363b614ee9017eb7650434b0c3a1860efba1d; exit=0; EXPECT=matched; output-sha256=7de1555df0c2700329e815b93b32c571c3ea54dc967b89e81ab73b9972b72d1d; output-bytes=2; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/buttah-silky-towels; path=7f4fb4b02918/15 entries
- [x] G4: BOOK.md has the review link and one TOTAL line, no blanks
  CHECK: cd /home/user/Mymobileworld/ugc/buttah-silky-towels && grep -c "Sent to Ralph: https://claude.ai/artifact/\|^TOTAL: \$3.09" BOOK.md && ! grep -q "___\|\$__" BOOK.md && echo NOBLANK
  EXPECT: /^2\nNOBLANK/m
  EVIDENCE: automatic-evidence=v1; definition-sha256=1eb9e14c07d473dfc8faeb7b32e84e6f0a2ee7261ea8c1ae1e795bdbadf565bc; exit=0; EXPECT=matched; output-sha256=0fcf27406be4dda750349b8152b1a9ac9daacfd37ce1e8ab846164f53a05f3ec; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/buttah-silky-towels; path=7f4fb4b02918/15 entries
- [x] G5: Script has no banned phrase, no price, closes on the orange cart
  CHECK: cd /home/user/Mymobileworld/ugc/buttah-silky-towels && ! grep -Eiq "order (it )?now|heads up|\\$[0-9]|reviewer|the label says|—|–" scripts.md && grep -q "It's in the orange cart." scripts.md && echo CLEAN
  EXPECT: CLEAN
  EVIDENCE: automatic-evidence=v1; definition-sha256=24a0f5db3b9bdbbd864e23aff0d163c136b5c44382dd81d3ef26e7c416fd362b; exit=0; EXPECT=matched; output-sha256=0b98843240a0b1a2384483206c02be8968dd809eb73838820be24cb7d6d6aeb9; output-bytes=6; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/buttah-silky-towels; path=7f4fb4b02918/15 entries
- [ ] G6: Ralph notified (phone push + email) with the review link (manual)
Later stages (after his OK): stills QC at 2x, test clip S5, clips, cut + QC + AI finish, REMOVED.md check, Drive folder, merge to main, brain note.
