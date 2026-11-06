# Grace UGC portfolio (2026-10-28)

Status: 2026-11-06 PARKED until Grace sends her new intro video (her words: "We're all good for now. Let's come back to this when I have the new intro video complete."). Live: https://claude.ai/artifact/JeSC2FCYMuNH3RsREQDR2C (version 1793978493-ccbc), her Canva layout in powder pink A, her photos, her 8 videos (they play on her iPhone through the blob fallback), her copy. Open: (1) new intro video from Grace: re-encode, re-caption, swap under a new name; (2) Ralph deploys the Apps Script ideas form (form/README.md) and sends the /exec URL for both "Get 3 free UGC ideas" buttons; (3) the Drive CURRENT doc. Media in Drive (media-in-drive/grace__portfolio.json, set 3). Cost $0.

A one-page portfolio so higher-priced brands reach out to Grace ("Grace With The Glow", TikTok @shewiththeglow) for UGC.
- Page: `site/index.html` + `site/media/` (16 web-encoded videos + posters + hero captions). Published as a private claude.ai Artifact (link in the Brain note and the final message).
- Ralph's calls (2026-10-28): only videos Grace filmed herself (no AI videos); contact Gracewiththeglow@gmail.com; no packages or prices, she negotiates per brand; name "Grace With The Glow"; look = one-pink signature.
- Videos: her intro clip (sent by Ralph, VID-20261019-WA0017.mp4) opens the page; 3 featured with TikTok numbers; 12 more by category. `picks.txt` = what is on the page, `videos.json` = numbers pulled 2026-10-28 with tiktok.py.
- Of the 38 Grace TikToks logged in this repo, 29 are self-filmed and 9 are our AI videos (excluded; ids in check.py).
- Checks: `python3 grace/portfolio/check.py files|stats|copy`, web-design-stack `motion_check.py`, Impeccable `detect` (0 findings), gates in `GATES.md`.
- Updating numbers: re-run `tiktok.py video <links> --no-media`, rebuild videos.json, fix the data-stat values until `check.py stats` passes, republish to the same Artifact.
