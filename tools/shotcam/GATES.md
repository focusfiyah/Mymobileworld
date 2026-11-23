# Gates: Shot Cam Part A (phone shot-list camera)

OWNS: tools/shotcam/**, research/shot-cam/**

Scope: a web page that opens from a link on iPhone and Android, shows a job's shot list, records each shot with a 3-2-1 countdown (page camera or the phone's own camera), allows retakes and any order, and sends the takes to Google Drive through the share menu; deployed free on Netlify.

- [x] G1: the page records a take end to end in a real browser (fake camera): shot list loads, countdown, record, keep, shot ticked, take named by shot, no sideways scroll at phone width
  CHECK: python3 test_shotcam.py
  EXPECT: SHOTCAM_TEST_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=325944f204ee2d0fdd416719673054589158aface88bd1827e6ce30091a61f59; exit=0; EXPECT=matched; output-sha256=d05a68c7abc3a0b7888583c0e2fa3aa224a2da61134d62232a3d50180095ff25; output-bytes=150; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/shotcam; path=7f4fb4b02918/15 entries

- [x] G2: the live Netlify link serves the page and the sample shot list
  CHECK: python3 check_live.py
  EXPECT: SHOTCAM_LIVE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=d57066d3837d38d5b500ee4418d9eb59143004fb9c2d717b2230901df8a4611d; exit=0; EXPECT=matched; output-sha256=d7a08bb61db5620d7e1d64f238bdd3139597771dcbf4b3e2e2b0948ab0c85689; output-bytes=87; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/shotcam; path=7f4fb4b02918/15 entries

- [ ] G3: iPhone test by Grace (Safari): one shot with the page camera and one with "Use phone camera", both reach Drive; I check size and quality
  EVIDENCE: pending

- [x] G4: Android test on Ralph's OnePlus (Chrome): same as G3
  EVIDENCE: 2026-11-11 Ralph's OnePlus, Chrome. Page camera: 3 takes in Drive "Shot Cam test" at the phone's sizes (18.4/17.0/13.1 MB); S01 probed 1080x1920 H.264 28.8 fps 11.6 Mbit/s + AAC. Phone camera: 1 take, 20.8 MB, 1080x1920 (rotated), 29.6 fps, 17.5 Mbit/s. Frames looked at, sharp. Bug found and fixed: a single shared take was named after the list title with no .mp4 (share title removed, deployed 6af4bc50); fix not yet re-sent from the phone.
