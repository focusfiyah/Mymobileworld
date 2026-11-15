# Gates: AI twin short, test 1 (Kit promo 7 "What's inside")

Ralph 2026-11-15: AI twin route, start with the existing kitchen takes (remind him to record more when needed), topic = kit promo, no price.

- [ ] G1: Script ends on the CTA "DM me KIT" and says no price
  CHECK: python3 -c "t=open('script.txt').read(); import re; assert t.strip().endswith('DM me KIT to grab it.'); assert not re.search(r'\$|dollar|\b29\b|\b45\b|\b59\b', t); print('SCRIPT_OK')"
  EXPECT: SCRIPT_OK
- [ ] G2: Voiceover exists and every script word is heard
  CHECK: python3 check_vo.py
  EXPECT: VO_WORDS_OK
- [ ] G3: Final cuts are 1080x1920, 15-40 s, with audio
  CHECK: python3 check_cut.py
  EXPECT: CUTS_OK
- [ ] G4: Hook whole and readable from frame 0, held 2 s, in the safe zone (both cuts)
  CHECK: python3 check_hook.py
  EXPECT: HOOK_BOTH_OK
- [ ] G5: Lips follow the words, no double mouth, beard/glasses edges clean at 2x (looked at the frame strip)
- [ ] G6: Review page published with both cuts stacked
- [ ] G7: Brain updated
  CHECK: python3 /home/user/Mymobileworld/tools/brain/check.py --terms "AI twin,twin shorts"
  EXPECT: BRAIN_OK
