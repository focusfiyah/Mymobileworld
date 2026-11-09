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

- [x] G7: everything in Drive (one folder, per course docs + files), link sent to Ralph
  EVIDENCE: 2026-11-09 Composio upload 128/128, Drive size = local size each; folder 1ongDvMgSDRhk192t5IUQIlQ-VO7jWXQY; link in the final reply + Telegram

- [x] G8: Brain note written and tools/brain/check.py prints BRAIN_OK
  EVIDENCE: 2026-11-09 BRAIN_OK (346 notes), vault pushed

## Round 2: analysis (Ralph tapped "Full analysis", 2026-11-09)

- [ ] G9: all 7 part findings written (course x2, calls x3, community x2)
  CHECK: python3 -c "import os,sys;d='/tmp/claude-0/-home-user/c5113556-fd28-502d-a836-f2da8d77f539/scratchpad/findings';f=[x for x in os.listdir(d) if x.endswith('.md') and os.path.getsize(os.path.join(d,x))>3000];print('FINDINGS_OK' if len(f)>=7 else f'FINDINGS_FAIL {len(f)}');sys.exit(len(f)<7)"
  EXPECT: FINDINGS_OK
  EVIDENCE: pending

- [ ] G10: one combined analysis (what to copy for Grace and for Ralph, each item with its source) on a review page + Drive Google Doc
  EVIDENCE: pending

- [ ] G11: Brain note updated with the analysis status and link
  EVIDENCE: pending
