# Gates: Creator Pathway (Skool) full pull

OWNS: research/creator-pathway/**

Scope: every lesson of TikTok Shop, UGC, Weekly Call Replays (= Live Coaching), Community Resources, Loom Lessons and Mindset saved word for word (text, files, video transcripts), plus Community posts on coaching / 1:1, put in Drive and the Brain.

- [ ] G1: all 70 lessons crawled, every Skool video has a stream link
  CHECK: python3 verify.py crawl
  EXPECT: CRAWL_OK
  EVIDENCE: pending

- [ ] G2: every video lesson (Skool + Loom) has its audio saved
  CHECK: python3 verify.py audio
  EXPECT: AUDIO_OK
  EVIDENCE: pending

- [ ] G3: every video lesson has a word-for-word transcript
  CHECK: python3 verify.py transcripts
  EXPECT: TRANSCRIPTS_OK
  EVIDENCE: pending

- [ ] G4: every attached file (59) downloaded
  CHECK: python3 verify.py files
  EXPECT: FILES_OK
  EVIDENCE: pending

- [ ] G5: Community posts mentioning coaching or 1:1 saved
  CHECK: python3 verify.py community
  EXPECT: COMMUNITY_OK
  EVIDENCE: pending

- [ ] G6: one word-for-word document per course built
  CHECK: python3 verify.py docs
  EXPECT: DOCS_OK
  EVIDENCE: pending

- [ ] G7: everything in Drive (one folder, per course docs + files), link sent to Ralph
  EVIDENCE: pending

- [ ] G8: Brain note written and tools/brain/check.py prints BRAIN_OK
  EVIDENCE: pending
