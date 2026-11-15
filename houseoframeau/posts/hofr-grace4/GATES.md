# GATES: HofR versions of 4 approved Grace cuts (2026-11-15)

- [x] G1: SoFyre HofR passes QC (1080x1920, >=15 s, -16..-14 LUFS, HOOK_OK, differs from Grace's cut at 8 times)
  CHECK: python3 qc.py sofyre final
  EXPECT: QC_OK sofyre
  EVIDENCE: automatic-evidence=v1; definition-sha256=f0c5468cad7a7cb0d5c8633ec0a235268b325b0b283441edbe0ab79e71727c52; exit=0; EXPECT=matched; output-sha256=5b1697899de969632f71e1b977cd9e8880ddf37ec5d170f2a440c3d1c8a3bef1; output-bytes=63; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/hofr-grace4; path=7f4fb4b02918/15 entries
- [x] G2: Throw Hands HofR passes QC
  CHECK: python3 qc.py throw final
  EXPECT: QC_OK throw
  EVIDENCE: automatic-evidence=v1; definition-sha256=4efa3a7810761137d4f1904877d0831d700059cc9cdb9efe0d608a0d88141ca2; exit=0; EXPECT=matched; output-sha256=501f31e0fe937e3b6767d5e8b3cc828c0b56fb2b014875c6276a6a31e332fbd7; output-bytes=62; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/hofr-grace4; path=7f4fb4b02918/15 entries
- [x] G3: Mute HofR passes QC
  CHECK: python3 qc.py mute final
  EXPECT: QC_OK mute
  EVIDENCE: automatic-evidence=v1; definition-sha256=0246ad2c43278dcbb723e7a2fe6bc1645004e15d48f4eb193daefdb889987a31; exit=0; EXPECT=matched; output-sha256=c692d05718722ea47d61072a460c5934d7cf36b95fbf0a169632dbf19e54770f; output-bytes=61; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/hofr-grace4; path=7f4fb4b02918/15 entries
- [x] G4: Night Driving Glasses HofR passes QC
  CHECK: python3 qc.py night final
  EXPECT: QC_OK night
  EVIDENCE: automatic-evidence=v1; definition-sha256=87f9f6084b3364f1898e11c46ae24e561d56550dfacd94bb8f6c182871b9a16f; exit=0; EXPECT=matched; output-sha256=3f38a4a71793a8e9820c28db1b9acaba670f580e479b4e6d896d713e291dc7e4; output-bytes=62; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/hofr-grace4; path=7f4fb4b02918/15 entries
- [x] G5: No freezes (>=0.6 s) in any final
  CHECK: for n in hofr_sofyre_v1 hofr_throw_hands_v1 hofr_mute_v1 hofr_night_glasses_v1; do ffmpeg -i out/$n.mp4 -vf freezedetect=n=0.003:d=0.6 -an -f null - 2>&1 | grep -q freeze_start && exit 1; done; echo FREEZE_CHECK_DONE
  EXPECT: FREEZE_CHECK_DONE
  EVIDENCE: automatic-evidence=v1; definition-sha256=c591b04927e231e26ae075ea817c73af5f1fe8055ffcad915cae1dbe747c12df; exit=0; EXPECT=matched; output-sha256=b6c78323061fa981096551b593bf31b7fb77e89369635b894f4ef14c9923ab3e; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/hofr-grace4; path=7f4fb4b02918/15 entries
- [ ] G6: Frame sheets looked at (frame 0 + one per shot): same hands, product never covered by the hook card, every shot matches its line (manual)
- [ ] G7: Review page published, Ralph notified (push + email) (manual)
- [ ] G8: Ralph OK per cut, then Drive upload "HofR - <Product> BF.mp4" with Drive size = local size, hub messaged (manual, waits on Ralph)
