# Gates: Grace scripts, 5 products x 3 (2026-10-07)

OWNS: ugc/skin1004-centella-kit/**, ugc/ilso-blackhead-bundle/**, ugc/emerald-tennis-necklace/**, ugc/seamless-bras-4pack/**, ugc/shapewear-pants-4pack/**, ugc/_packs/grace-2026-10-07/**

Scope: 15 humanized scripts (3 per product) with the gate proofs, a Claude Doc, a WhatsApp PDF and one Drive folder per product, $0 spent.

- [x] G1: 15 spoken scripts exist and each closes with "It's in the orange cart."
  CHECK: node verify.mjs scripts
  EXPECT: SCRIPTS_OK 15
  EVIDENCE: automatic-evidence=v1; definition-sha256=55b4a5db085be6d8dd4d58d43c8aa3b3db06859530f3782db92f0aebdb37f73a; exit=0; EXPECT=matched; output-sha256=34bd198737d4adad597eb2e8d01451a9c4c22572fa78a01e8f5c14997e3f18a3; output-bytes=14; shell=/bin/sh; cwd=/home/claude/Mymobileworld/ugc/_packs/grace-2026-10-07; path=7f4fb4b02918/15 entries

- [x] G2: no banned phrase, dash or price in any script file
  CHECK: node verify.mjs banned
  EXPECT: BANNED_CLEAN 20
  EVIDENCE: automatic-evidence=v1; definition-sha256=a4cb5731f797d19cac8527eeff868967d49768c59befdd637987f7e2cb8e473d; exit=0; EXPECT=matched; output-sha256=b7632b4eec3ae5f54bf5b81cc13d3971332662c88dd5d2cbf87220a1628e4931; output-bytes=16; shell=/bin/sh; cwd=/home/claude/Mymobileworld/ugc/_packs/grace-2026-10-07; path=7f4fb4b02918/15 entries

- [x] G3: every script reads at grade 6 or lower and stays under 115 words
  CHECK: node verify.mjs readability
  EXPECT: READABILITY_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=494d083b1ef7c553c04cd4d3b2ac6f5eb51eb60466b6bde6a9efef037423fc63; exit=0; EXPECT=matched; output-sha256=49a19fa1bb2618f7e9eacefa83c6016c39058f040bb3d16194e7d5800c41b9fb; output-bytes=15; shell=/bin/sh; cwd=/home/claude/Mymobileworld/ugc/_packs/grace-2026-10-07; path=7f4fb4b02918/15 entries

- [x] G4: grace/gate.py passes every step except viral_board for all 5 jobs
  CHECK: node verify.mjs gate
  EXPECT: GATE_8_OF_9_ALL
  EVIDENCE: automatic-evidence=v1; definition-sha256=e8034bfc550ec9f317fea9dd5690f5c8b395863d48912f450dc1ad305e1f5cd1; exit=0; EXPECT=matched; output-sha256=fe4798e3261f124a86317b48ffdb5a8f1da53c89f81c8c8823dbfc7a8cacbc63; output-bytes=40; shell=/bin/sh; cwd=/home/claude/Mymobileworld/ugc/_packs/grace-2026-10-07; path=7f4fb4b02918/15 entries

- [x] G5: each job README has a DONE ($0) Status line with its Drive folder link
  CHECK: node verify.mjs readme
  EXPECT: README_OK 5
  EVIDENCE: automatic-evidence=v1; definition-sha256=29f6cc0c9665de9e3ba504385e10fe6aadbdbad65d8941457047b30d03677e57; exit=0; EXPECT=matched; output-sha256=06844679fe3dd212aa41fd7783d8c5a914b97b2d8da8dd31bba66c20d474d172; output-bytes=12; shell=/bin/sh; cwd=/home/claude/Mymobileworld/ugc/_packs/grace-2026-10-07; path=7f4fb4b02918/15 entries

- [x] G6: Claude Doc filled (all 5 products + shot list) and the PDF exported and page 1 checked
  EVIDENCE: doc c2f4631f-6201-4054-a6a3-17c9ab67c77e rev 8; PDF 12 pages, 324 KB, /mnt/project-files/grace/scripts-2026-10-07/

- [x] G7: one Drive folder per product in Grace Tiktok assets, each with a CURRENT scripts doc, nothing loose
  EVIDENCE: folders 1HdrFxw7..., 1Y3C2TK7..., 131GPBBi..., 13ZFseOC..., 1BFTn7NU... each holds one CURRENT doc (created 2026-10-07 21:18-21:19Z); test and emoji-garbled docs trashed

- [ ] G8: tiktok.py viral board run for each product category
  EVIDENCE: not run

ABANDON: G8 container proxy returns 403 for tiktok.com and this project has no cloud environment with network access; the Composio sandbox browser returned 0 items. Needs Ralph to add an environment in Project settings, then re-run.
