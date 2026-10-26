# Gates: done-for-you service research (Ralph 2026-10-26)

OWNS: ralph/dfy-service/**

Scope: watch both TikToks, give Ralph my take, research and rank the top 3 pain points businesses will pay a done-for-you service to fix (with proof, offer, price, how we deliver, first client), say whether a better model exists, publish it for him to read on his phone.

- [x] G1: both TikToks pulled with full transcripts saved in research/
  CHECK: python3 ralph/dfy-service/verify.py videos
  EXPECT: VIDEOS_OK
  EVIDENCE: VIDEOS_OK (run by hand 2026-10-26; gate-check approval not used per Ralph rule)

- [x] G2: REPORT.md has my take on the video (120+ words)
  CHECK: python3 ralph/dfy-service/verify.py thoughts
  EXPECT: THOUGHTS_OK
  EVIDENCE: THOUGHTS_OK (by hand 2026-10-26)

- [x] G3: REPORT.md ranks exactly 3 pain points, each with who, proof, offer, price, delivery, first client and 3+ source links
  CHECK: python3 ralph/dfy-service/verify.py top3
  EXPECT: TOP3_OK
  EVIDENCE: TOP3_OK (by hand 2026-10-26)

- [x] G4: REPORT.md compares done-for-you with the other models and names a pick
  CHECK: python3 ralph/dfy-service/verify.py better
  EXPECT: BETTER_OK
  EVIDENCE: BETTER_OK (by hand 2026-10-26)

- [x] G5: report reads at grade 9 or below
  CHECK: python3 ralph/dfy-service/verify.py readability
  EXPECT: READ_OK
  EVIDENCE: grade 7.2, READ_OK (by hand 2026-10-26)

- [x] G6: every number in the report traced to a source in research/sources.md or marked as my estimate; Humanizer pass done
  EVIDENCE: research/sources.md lists a source for every figure; prices and money math marked "my estimate"; unsourced affiliate claim removed; humanizer skill loaded and applied (no dashes, no staged contrasts)

- [x] G7: published as a private Artifact page, link in the reply, email + phone push sent
  EVIDENCE: Claude doc https://claude.ai/artifact/MKsDAs1BTwncytZpydrTAk filled (rev 6); Gmail sent id 1a176b5562c4dfc3; PushNotification requested

- [x] G8: brain notes written (job note + session log), tools/brain/check.py prints BRAIN_OK, branch merged to main in Mymobileworld and vault pushed
  EVIDENCE: Brain notes + session log, check.py BRAIN_OK; Mymobileworld main at 3b1e298+; vault 5fa9cbf pushed
