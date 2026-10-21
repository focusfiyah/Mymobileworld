# Gates: Swyii red agate + moonstone choker, voiceover scripts for Grace (2026-10-21)

OWNS: ugc/swyii-agate-necklace/**

Scope: 3 voiceover script options for Grace's existing footage (Drive "Moonstone Agate Necklace by Swyii .MOV"), full Grace script gate, delivered as a Claude doc + Drive Google Doc in one product folder, Ralph notified by push + email.

- [ ] G1: Footage reviewed: shot list with timestamps in footage_notes.md, scripts timed to it
  EVIDENCE: pending
- [ ] G2: 3 spoken scripts, each a different library hook said word for word, 60-100 words (about 30 s or less), closing "It's in the orange cart."
  CHECK: python3 ugc/swyii-agate-necklace/qc/verify.py scripts
  EXPECT: SCRIPTS_OK
  EVIDENCE: pending
- [ ] G3: No banned words (reviewer, label says, prices, sale, order now, dashes, healing/energy claims, sterling, pendant)
  CHECK: python3 ugc/swyii-agate-necklace/qc/verify.py banned
  EXPECT: BANNED_OK
  EVIDENCE: pending
- [ ] G4: Readability grade <= 6 on every spoken script
  CHECK: python3 ugc/swyii-agate-necklace/qc/verify.py readability
  EXPECT: READABILITY_OK
  EVIDENCE: pending
- [ ] G5: Script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources)
  CHECK: python3 ugc/swyii-agate-necklace/qc/verify.py gate
  EXPECT: GATE_OK
  EVIDENCE: pending
- [ ] G6: Drive: one product folder in Grace Tiktok assets with a CURRENT Google Doc, nothing loose (the footage stays where Grace put it)
  EVIDENCE: pending
- [ ] G7: Claude doc published, link in README
  EVIDENCE: pending
- [ ] G8: README Status + CLAUDE.md Jobs line written with Drive + doc links
  CHECK: python3 ugc/swyii-agate-necklace/qc/verify.py readme
  EXPECT: README_OK
  EVIDENCE: pending
- [ ] G9: Ralph notified: phone push + email sent (results recorded)
  EVIDENCE: pending
- [ ] G10: Committed and pushed to ccr-1f9ae214-1gwzcu
  EVIDENCE: pending
