# Gates: Grace's PRITECH remix style + voice round 5, 2026-10-28

OWNS: grace/winners/**, grace/voice/**, grace/PLAYBOOK.md, CLAUDE.md, handoff/**

Scope: learn the edit style of Grace's selling PRITECH re-edit (saved as a lesson with the shot map and a Black Friday brief for later), and start improving her voice clone from the voiceovers she records herself (rule saved everywhere, clean samples built, nothing paid without Ralph's OK).

- [x] S1: STYLE note has the shot-by-shot map of the selling edit (14 shots, source of each: Grace real / our V1 S#), the Oct 23 comparison and the rules drawn from it
  CHECK: python3 grace/winners/check.py style
  EXPECT: PASS style 14
  EVIDENCE: 2026-10-28 PASS style 14 (run on main's files)

- [x] S2: the PLAYBOOK points to the STYLE note and the Black Friday brief is recorded as not made yet
  CHECK: python3 grace/winners/check.py playbook
  EXPECT: PASS playbook
  EVIDENCE: 2026-10-28 PASS playbook

- [x] V1: clean vocal samples (music removed) exist for all 7 of Grace's own posted voiceovers, listed in grace/voice/r5/samples.json with duration and echo reading
  CHECK: python3 grace/voice/r5/check.py samples
  EXPECT: PASS samples 7
  EVIDENCE: 2026-10-28 PASS samples 7 (200.6 s, music at -36..-71 dB before demucs; castor echo 200 ms)

- [x] V2: the "her own VOs feed the clone" rule is in CLAUDE.md, grace/voice/README.md and all handoff memory files (MEMORY_SHORT <= 2,000 chars)
  CHECK: python3 grace/voice/r5/check.py rule
  EXPECT: PASS rule
  EVIDENCE: 2026-10-28 PASS rule (main). Also: restored the 2026-10-27 drift-strip rule that my first push dropped from the handoff files; live doc 1pCwM9Pb... has both

- [ ] V3: new clone + A/B test: only after Ralph OKs the ElevenLabs characters (ask with the exact count)
  EVIDENCE: pending
