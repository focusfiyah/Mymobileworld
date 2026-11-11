# Shot Cam

Phone camera page that tells you what to film (Ralph 2026-11-11, inspired by Brooke Hall's IRIS; our own name and look).
Live: https://shotcam-azariah.netlify.app/?list=<list id>  (Netlify site 3ef9e069-06a1-4ff2-ad8b-507f57399e81, team login turned off so Grace opens it without signing in).

Status (2026-11-11): Part A built and live, $0. Browser test passes (fake camera, 1920x1080 MP4). Android test passed on Ralph's OnePlus (G4). Waiting on Grace's iPhone test (G3), sent to her on Telegram 2026-11-11 with the Drive folder "Shot Cam test" (1J4cLHJTbiW4OYZDLyyMdjqZ8rITEi2nU, anyone with link can edit). Parts B-D (auto first cut, camera roll mode, style memory) not started. Plan: https://claude.ai/artifact/GEAzcFQRkMgtMn1fcC7ppz

## Decisions
- Main camera = the page camera (red button), so the shot card stays on screen while filming; the Phone camera button for hero/close-up product shots that need the most detail (Ralph 2026-11-11, tapped). Measured on his OnePlus: page 1080x1920 28.8 fps 11.6 Mbit/s, phone camera 1080x1920 29.6 fps 17.5 Mbit/s.
- Takes go to Google Drive at full quality, never Telegram (Telegram shrinks to 464x848) (Ralph 2026-11-11).
- Netlify free plan shows a "Powered by Netlify" badge bottom right that cannot be turned off on this plan; every screen keeps a 68 px strip clear for it (test checks it).

## Use
- One shot list per video: `site/lists/<id>.json` (title, slug for file names, note, folder = Drive folder name to pick, shots: n, direction, line, frame, hand, seconds). Then `./deploy.sh` and `python3 check_live.py <id>`. Send the link `...?list=<id>`.
- On the phone: tap a shot, red button = 3-2-1 then record, tap to stop, Keep or retake; any order; Flip = front camera; Phone camera = the phone's own camera app at full quality. Takes stay on the phone (IndexedDB) until sent.
- Send to Drive: share menu, Drive, pick the folder. Files are named `<slug> S03 take2.mp4` (`... phone.mov` for phone-camera takes).

## After sending (status screen)
- When every take is sent, the page shows "Sent to Drive" with a 4-step tracker: Filmed, Sent to Drive, First cut being made, Ready to watch (plus "you can close this page", or which shots are still missing). "Free up phone space" deletes sent takes from the phone only.
- Steps 3-4 read `site/lists/<id>-status.json`, which Azariah writes and deploys: `{"stage": "cutting", "note": "..."}` while editing, then `{"stage": "ready", "note": "...", "review_url": "<review page>"}`. The page re-reads it every minute. Also send the Telegram message the page promises.

## Check
- `python3 test_shotcam.py` (headless Chromium, fake camera) prints SHOTCAM_TEST_OK.
- `python3 check_live.py` prints SHOTCAM_LIVE_OK.
