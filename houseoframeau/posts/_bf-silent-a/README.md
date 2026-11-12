# HofR Black Friday: silent videos A (2026-11-12)

Status: DONE 2026-11-12, $0. Ralph OK'd all 5 (tapped "All 5 OK"); in Drive: butter 1VcHK7X9kd9_WqSovPKCafxTO8_lz1GoK, mirror 1drMRD4sgJx-I3hDqPMx9pA5OpbfuXR7C, ear 1sB3MbHDNn-aRY0uU8feLR1Z1X8P_3Mki, coloring 1w-VwRWBfE7cXiEp-sWlUznXmP9kVynk-, meat 1EAQI8iiLg2Vud5VaOoVWqijRLpS8Yr_3 (sizes = local). Hub told 2026-11-12. Round 3 b-roll (brown complexion, matched to each line).
Review https://claude.ai/code/artifact/62c62375-ddc3-41a2-b48c-3b93cbcd000f ; email to Ralph Gmail 1a1d1fb6b51cd5f6 (push tool not in this session: tested via ToolSearch, nothing found).
Next: Ralph's OK per cut -> Drive "HofR - <Product> BF.mp4" in its product folder (Kie host + Composio GOOGLEDRIVE_UPLOAD_FROM_URL, size check) -> one line per product to hub session_01Y1Pt3pfP7HcKsjq5xn9T1H.

Task (Ralph 2026-11-12, via the hub): Ralph's free Chatterbox voice over Grace's approved silent V1 (HD) cuts: Mirror, Body Butter, Ear Camera, Coloring Book, Meat Sticks. All 5 sources had no audio stream (G1).
Rebuild: download each CURRENT cut to /tmp/claude-0/src/<name>.mp4 (anyone-with-link: drive.usercontent.google.com/download?id=<id>&export=download&confirm=t;
ids mirror 13xqGy8n2bhTEKWPjCd7Gn_GSEibCGQ2E, butter 1BNdk_5KoLDVosS6KmmgPi0rD0B_vlsuy, ear 1O3Ef3KsarQhvQtYNRtyYo6T_hzYxlQcz, coloring 1wCY2DhFEX3tlPNzEZyudSIwKBYF2Gppk, meat 119UzBJrrVamyi6FPzzfUDyJgiyrNoNnV),
voice tools: Dayone-ai presenter_setup.sh + ralph_ref.wav (media set 1 of products/ai-on-autopilot). Then per post:
  ~/.presenter-tools/cbx/bin/python -I vo_gen.py ../bf-<p>        (SEED=2000 ... <line> to re-seed one line)
  ~/.presenter-tools/fw/bin/python -I readback.py ../bf-<p> 0.2 1.06 > ../bf-<p>/vo/readback.txt   (must end READBACK_OK)
  python3 cut.py ../bf-<p> && python3 check.py ../bf-<p>           (CHECK_OK) ; python3 page.py rebuilds the review page + script.md
pexels.py = free b-roll search (contact sheet). Lessons: Chatterbox runs ~3.2 words/s, so ~60 words + 1.06x tempo = 22 s; whisper writes "5"/"cents" for "five"/"scents" (readback.py maps them).
