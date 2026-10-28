# Gates: Grace's PRITECH remix style + voice round 5, 2026-10-28

OWNS: grace/winners/**, grace/voice/**, grace/PLAYBOOK.md, CLAUDE.md, handoff/**

Scope: learn the edit style of Grace's selling PRITECH re-edit (saved as a lesson with the shot map and a Black Friday brief for later), and start improving her voice clone from the voiceovers she records herself (rule saved everywhere, clean samples built, nothing paid without Ralph's OK).

- [ ] S1: STYLE note has the shot-by-shot map of the selling edit (14 shots, source of each: Grace real / our V1 S#), the Oct 23 comparison and the rules drawn from it
  CHECK: python3 grace/winners/check.py style
  EXPECT: PASS style 14
  EVIDENCE: pending

- [ ] S2: the PLAYBOOK points to the STYLE note and the Black Friday brief is recorded as not made yet
  CHECK: python3 grace/winners/check.py playbook
  EXPECT: PASS playbook
  EVIDENCE: pending

- [ ] V1: clean vocal samples (music removed) exist for all 7 of Grace's own posted voiceovers, listed in grace/voice/r5/samples.json with duration and echo reading
  CHECK: python3 grace/voice/r5/check.py samples
  EXPECT: PASS samples 7
  EVIDENCE: pending

- [ ] V2: the "her own VOs feed the clone" rule is in CLAUDE.md, grace/voice/README.md and all handoff memory files (MEMORY_SHORT <= 2,000 chars)
  CHECK: python3 grace/voice/r5/check.py rule
  EXPECT: PASS rule
  EVIDENCE: pending

- [ ] V3: new clone + A/B test: only after Ralph OKs the ElevenLabs characters (ask with the exact count)
  EVIDENCE: pending
