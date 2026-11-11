# Shot Cam

Phone camera page that tells you what to film (Ralph 2026-11-11, inspired by Brooke Hall's IRIS; our own name and look).
Live: https://shotcam-azariah.netlify.app/?list=<list id>  (Netlify site 3ef9e069-06a1-4ff2-ad8b-507f57399e81, team login turned off so Grace opens it without signing in).

Status (2026-11-11): Part A built and live, $0. Browser test passes (fake camera, 1920x1080 MP4). Waiting on the real-phone tests: Grace's iPhone (Safari) and Ralph's OnePlus (Chrome), gates G3/G4 in GATES.md. Parts B-D (auto first cut, camera roll mode, style memory) not started. Plan: https://claude.ai/artifact/GEAzcFQRkMgtMn1fcC7ppz

## Use
- One shot list per video: `site/lists/<id>.json` (title, slug for file names, note, folder = Drive folder name to pick, shots: n, direction, line, frame, hand, seconds). Then `./deploy.sh` and `python3 check_live.py <id>`. Send the link `...?list=<id>`.
- On the phone: tap a shot, red button = 3-2-1 then record, tap to stop, Keep or retake; any order; Flip = front camera; Phone camera = the phone's own camera app at full quality. Takes stay on the phone (IndexedDB) until sent.
- Send to Drive: share menu, Drive, pick the folder. Files are named `<slug> S03 take2.mp4` (`... phone.mov` for phone-camera takes).

## Check
- `python3 test_shotcam.py` (headless Chromium, fake camera) prints SHOTCAM_TEST_OK.
- `python3 check_live.py` prints SHOTCAM_LIVE_OK.
