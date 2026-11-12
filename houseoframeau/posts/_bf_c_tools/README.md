# HofR Black Friday, batch C: Ralph's voice on 5 Grace silent edits (2026-11-12)

Status: REVIEW SENT 2026-11-12, $0. Review page https://claude.ai/code/artifact/90f11b0d-ed64-4c5a-9368-43dede2d34e8 (email sent;
phone push tool not in this session). Waiting for Ralph to finish reading, then questions. Nothing in Drive yet (only after his OK per cut).
Next after OK: Drive "HofR - <Product> BF.mp4" in each product folder (Kie file host + Composio upload, size check), then one line per
product to the hub session session_01Y1Pt3pfP7HcKsjq5xn9T1H. No TikTok upload, no queue edit here.

Posts: ../bf-purcell (H046, 22.4 s), ../bf-jiyu-nad (H089, 22.5 s), ../bf-luvum (H055, 23.8 s), ../bf-momo-nashi (H134, 25.7 s),
../bf-manners (H130, 25.1 s). Each has script.md, cut.py, vo/lines.txt, broll/SOURCES.md.

Tools here:
- vo.py: Ralph's free Chatterbox clone (Dayone-ai presenter_setup.sh + avatar/voice/ralph_ref.wav), one seed per line (vo/seeds.json),
  faster-whisper small.en read-back, joins lines (0.18 s gap) into vo/ralph.wav + vo/words.json. vo/heard_ok.json = lines whose
  Whisper spelling differs but the sound is right (numbers, brand names).
- build.py: shared cut builder (shots anchored to VO lines, crop per shot, hook card in x 60-940 / y 360+, exact trim after a coarse
  seek: an input seek on Grace's HEVC .mov leaked a pre-roll frame at t=0).
- post_check.py, hooks_all.py: QC oracles used by GATES.md.
- pexels/: free Pexels holiday clips (media, not in git), index.json = sources.
Setup gotcha: faster-whisper 1.1.1 needs av<15 (`pip install av==13.1.0` in ~/.presenter-tools/fw), av 19 breaks it.
Media (orig/, out/, vo wavs, pexels mp4s, review mp4s) stays out of git (job-media rule).
