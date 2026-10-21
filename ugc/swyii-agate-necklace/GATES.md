# Gates: Swyii red agate + moonstone choker, voiceover scripts for Grace (2026-10-21)

OWNS: ugc/swyii-agate-necklace/**

Scope: 3 voiceover script options for Grace's existing footage (Drive "Moonstone Agate Necklace by Swyii .MOV"), full Grace script gate, delivered as a Claude doc + Drive Google Doc in one product folder, Ralph notified by push + email.

- [x] G1: Footage reviewed: shot list with timestamps in footage_notes.md, scripts timed to it
  EVIDENCE: footage_notes.md: 153.7 s clip, contact sheet review/contact.jpg, 0 speech segments; shot windows per line in scripts.md
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
- [x] G6: Drive: one product folder in Grace Tiktok assets with a CURRENT Google Doc, nothing loose (the footage stays where Grace put it)
  EVIDENCE: Drive folder 1rxeoSCW04tMk3JsTpm8tT0E6vqf8pXsj created in Grace Tiktok assets; Google Doc 1hK8ZT8TN8e5FqXgPZS85VGVRZff2d-G4-vbyCbZwnrM read back OK. Footage left where Grace put it (owner Grace); Ralph asked by email.
- [x] G7: Claude doc published, link in README
  EVIDENCE: https://claude.ai/artifact/Ackn9R5N4f1RVSkKt3Fh9Q published v1; link in README
- [ ] G8: README Status + CLAUDE.md Jobs line written with Drive + doc links
  CHECK: python3 ugc/swyii-agate-necklace/qc/verify.py readme
  EXPECT: README_OK
  EVIDENCE: pending
- [x] G9: Ralph notified: phone push + email sent (results recorded)
  EVIDENCE: PushNotification: "Mobile push requested." Gmail id 1a15d165ecc7e5f6 sent to life22watch@gmail.com
- [x] G10: Committed and pushed to ccr-1f9ae214-1gwzcu
  EVIDENCE: pushed to origin/ccr-1f9ae214-1gwzcu (tracking set up)
