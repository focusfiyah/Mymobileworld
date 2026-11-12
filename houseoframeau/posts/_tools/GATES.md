# GATES: HofR BF silent batch B (Pinmoco, Calmi, COSRX, Eyeliner, Wig Milk), 2026-11-12
Run from houseoframeau/posts/_tools. Task: hub session_01Y1Pt3pfP7HcKsjq5xn9T1H, Ralph 2026-11-12 (VO on Grace's silent cuts, $0).

- [ ] G1: All 5 source cuts (CURRENT V1 from Drive) have no audio stream
  CHECK: python3 qc.py silent
  EXPECT: SILENT_OK 5/5
- [ ] G2: Every script opens on its HOOKS.md hook word for word, ends "It's in the orange cart.", no banned phrase, price or dash
  CHECK: python3 qc.py script
  EXPECT: SCRIPT_OK 5/5
- [ ] G3: Every VO line read back by faster-whisper matches its script line (<=10% words missing)
  CHECK: python3 qc.py vo
  EXPECT: VO_OK 5/5
- [ ] G4: Every cut is >=15 s, 1080x1920, 30 fps, -16.5..-13.5 LUFS and HOOK_OK in its declared hook box
  CHECK: python3 qc.py cut
  EXPECT: CUT_OK 5/5
- [ ] G5: Frame sheet of each final cut looked at: no freezes, every clip 1.0x (cut.py asserts), hook not over the product label, REMOVED.md items absent, bright neutral b-roll (manual)
- [ ] G6: One private review page with the 5 cuts stacked full width + script under each; link sent with push + email (manual)
- [ ] G7: Brain job note + session log pushed, Active work line removed
  CHECK: python3 ../../../tools/brain/check.py --terms "HofR BF silent B"
  EXPECT: BRAIN_OK
- [ ] G8: After Ralph's OK per cut: Drive "HofR - <Product> BF.mp4" size = local, hub messaged (handoff until he OKs)
