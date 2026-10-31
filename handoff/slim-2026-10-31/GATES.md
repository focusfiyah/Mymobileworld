# Gates: slimmer CLAUDE.md files (Ralph 2026-10-31: "Go" on the slim plan)

OWNS: CLAUDE.md, rules/**, tools/camofox/README.md, tools/broll/SOURCE.md, tools/media/README.md, handoff/history/SETUP_NOTES.md, handoff/slim-2026-10-31/** (+ Dayone-ai CLAUDE.md, rules/**, pointer files; claude-skills skills/day-one-ai)

Scope: move job-specific rules and setup/test history out of both CLAUDE.md files word for word, repoint every reference, keep every check that reads CLAUDE.md passing, measure the result.

- [x] G1: every sentence of both original CLAUDE.md files still exists word for word in the new layout
  CHECK: python3 handoff/slim-2026-10-31/verify.py lossless
  EXPECT: LOSSLESS_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=cd6685b7e571b7b3ba63d6b7542f4e68823762ee0e4c6b842bcd2acc11606e5f; exit=0; EXPECT=matched; output-sha256=6668540d5783ca4e54dbfb130380875816c9c0fdfb89c082c7591141c12d536c; output-bytes=61; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G2: each CLAUDE.md points to every rules file in its repo, no dead pointer, moved sections marked
  CHECK: python3 handoff/slim-2026-10-31/verify.py pointers
  EXPECT: POINTERS_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=78878c07452b13f5fa127a996d62c2a79c33e651248952dab2df7dcd98458f6d; exit=0; EXPECT=matched; output-sha256=e54198e61ad4b64cd378603b3b157726241a8db16cb77e7e8338844caf314011; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G3: phrases the repos' own checks and the job index need are still in CLAUDE.md
  CHECK: python3 handoff/slim-2026-10-31/verify.py phrases
  EXPECT: PHRASES_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=55ebef82953e17a0839032e050bf826f75503a15dc89fd99bca58d26a6b42a72; exit=0; EXPECT=matched; output-sha256=89376957b460980b0b98580ed8d998d9aba3957a2bf00936a77bd27d25b4aa42; output-bytes=23; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G4: no file still sends a reader to a CLAUDE.md section that moved (routines, skills, formats, scripts)
  CHECK: python3 handoff/slim-2026-10-31/verify.py refs
  EXPECT: REFS_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=ec6b32adff7bcbf0c0ea57cbca8a4181cc57daf76993ab6e2826db9b0d2cfeae; exit=0; EXPECT=matched; output-sha256=1b8700bf1175eaa367d070f738a073c21e1dd4c738e1550285fb937247b1c77d; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G5: the two CLAUDE.md files together are at least 25% smaller (measured)
  CHECK: python3 handoff/slim-2026-10-31/verify.py size
  EXPECT: SIZE_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=7466233c150cc0bdeb1162ad2920a5ac48d907977c1e30e2cea219178d171858; exit=0; EXPECT=matched; output-sha256=6aa42f1ad9a3a95ddb5c1af3494340ae2ad580ad11ba787cfb49e090dc84577b; output-bytes=196; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G6: the repos' existing CLAUDE.md checks give the same result as before (baseline 2026-10-31: broll docs OK, grace docs OK, clipcheck formats + saved OK, voice refs OK; camofox docs and voice r5 failed before on MEMORY_SHORT.txt, not CLAUDE.md)
  CHECK: sh -c 'python3 tools/broll/verify.py docs && python3 grace/tests/docs.py && python3 tools/clipcheck/check_rest.py formats && python3 tools/clipcheck/check_rest.py saved && python3 grace/voice/check.py refs'
  EXPECT: REFS OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=a17f6e3b670773c17cd0c8afb38edb3af10aa49dad4dc96f4b256761e568aecf; exit=0; EXPECT=matched; output-sha256=798134079a1cfeba93f508c486dd91129160a0e2f4cfd0e63480e11bf9a07f64; output-bytes=93; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G7: pushed to main in Mymobileworld, Dayone-ai and claude-skills; day-one-ai skill redeployed; brain updated; Ralph told with the measured numbers
  EVIDENCE: main = Mymobileworld 4672ef04, Dayone-ai 7bed9c2, claude-skills b225298 (rev-list 0/0); day-one-ai deployed + zip sent (dc4cd7dc); brain check BRAIN_OK; Gmail 1a191dfb8d0e6bf3; push requested; RGH session messaged (delivered)
