# Gates: Plant Therapy Christmas Cheer V3, plan stage (2026-11-07)

- [x] G1: Telegram updates 786406572-573 are claimed by this session
  CHECK: cd /home/user/Mymobileworld && python3 tools/telegram/claim.py status 786406572 786406573
  EXPECT: /786406572 CLAIMED_BY session_01Y1Pt3sCL1HyiRynDkY6twm[\s\S]*786406573 CLAIMED_BY session_01Y1Pt3sCL1HyiRynDkY6twm/
  EVIDENCE: automatic-evidence=v1; definition-sha256=23562596faf60903144eac712ed50fb6bfc2d6fc9aee937df02d6b78c73e19d7; exit=0; EXPECT=matched; output-sha256=20d6508426f148a8ec874e062277c6ccdbddb7db98ee5dea640cd50e76752bc8; output-bytes=266; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/plant-therapy-christmas-cheer/v3; path=7f4fb4b02918/15 entries
- [x] G2: V3 Production Book has shots S1-S6, one TOTAL $3.19 line and a Sent to Ralph line
  CHECK: cd /home/user/Mymobileworld/ugc/plant-therapy-christmas-cheer/v3 && python3 -c 'import json;t=open("../BOOK.md").read();print("BOOK_OK" if all(s in t for s in ["| S1 |","| S6 |","TOTAL: $3.19","Sent to Ralph: https://claude.ai/artifact/"]) else "MISSING")'
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=28c909407ffb8c29a45ca99838b6b152beb4f777aa3e360a916cdc8604f693da; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/plant-therapy-christmas-cheer/v3; path=7f4fb4b02918/15 entries
- [x] G3: No paid spend on this job this session (job total still $0.81 for November)
  CHECK: cd /home/user/Mymobileworld && python3 grace/spend.py | python3 -c 'import sys,re;t=sys.stdin.read();m=re.search(r"plant-therapy-christmas-cheer +\$ +([\d.]+)",t);print("SPEND_UNCHANGED" if m and m.group(1)=="0.81" else "CHANGED")'
  EXPECT: SPEND_UNCHANGED
  EVIDENCE: automatic-evidence=v1; definition-sha256=f12bba5902f36919bebf2b3f7b625de07aa243bfd1649bb76c45c6452710ddc4; exit=0; EXPECT=matched; output-sha256=48203cdc9cde6402d494fa3b62e919ea276b0e8c9be7ae451f528c811d7969b5; output-bytes=16; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/plant-therapy-christmas-cheer/v3; path=7f4fb4b02918/15 entries
- [x] G4: Grace's photo is in Drive Telegram Assets at the same size as the local file, and indexed
  EVIDENCE: 2026-11-07 GOOGLEDRIVE_UPLOAD_FROM_URL returned id 1eQW3BK9ktt2OhgiM_sguniFOA6tYnqvr size 93569 = local wc; GOOGLEDRIVE_EDIT_FILE on README - asset index.txt succeeded with the 2026-11-07 entry
- [x] G5: Grace got one "Received, working on" reply, no tick mark or the word done
  EVIDENCE: 2026-11-07 Telegram sendMessage to -5234107715 (reply to msg 212) returned ok true; text starts "Received, working on:"
- [x] G6: Ralph got the plan questions as tap cards and an email for each decision
  EVIDENCE: AskUserQuestion answered 2026-11-07 (4 taps); Gmail ids 1a1b70a9f4ed139f and 1a1b714a99cc4eb5 sent
- [ ] G7: Ralph got a phone push for each decision
ABANDON: G7 PushNotification is not loadable this session (ToolSearch select:PushNotification returned no match, tested 2026-11-07); email went instead
