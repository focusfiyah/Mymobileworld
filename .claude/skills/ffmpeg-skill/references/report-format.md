## Report format

Reply in the request's language; keep the labels in English. Numbers come from `--json` or a probe:

```
Done: final.mp4 — 59.98 s, 1080x1920, 30 fps, H.264, AAC stereo, -14.1 LUFS
Steps: cut 0:12-1:12 (lossless) -> fit 9:16 crop -> captions (pop, karaoke) -> loudness -14 -> export reels
Check: reels — all 12 checks pass (verified: true)
Look: final_sheet.png (captions inside the safe area, logo top-right)
Notes: source was VFR, conformed to 30 fps; audio was mono, made stereo
```

A failure starts `Failed:` and quotes `error.message`; with nothing to check or see, `Check: nothing to verify`,
`Look: not needed`. A partial result is `Done:` with the shortfall in `Notes:`, never `Done (partially):`.
These fillers are sentences, not labels: a Japanese report says `Check: 検証するものなし` / `Look: 不要`.
Never describe a fix you did not run. Full Japanese example and more rules: `references/report.md`.
