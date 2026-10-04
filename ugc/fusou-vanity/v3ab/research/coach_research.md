# Coach research V3 (2026-10-04, tiktok-shop-coach, run in this job)
- `shop "vanity desk"` (shop-vanity-desk.json): HONGWAY $107 21k sold; HONGWAY transparent $150 9k; FUSOU 47" $338 8k. Our 71" FUSOU family ~2k sold.
- `tag vanitydesk --days 30` (tag-vanitydesk.json): @ivy.rogers3 2.4M (6s), @rizziannaa 1.8M (10s), @mariacox97 396k (7s). Short, one reveal, "My teenage self would be SCREAMING".
- `video` on the top 3 shop videos (videos/): @ivy.rogers3 7688436582893767967, @mariacox97 7689632879038532895, @theressa151 7683168124597701919 (6-8s; no TikTok captions, so no transcript; hook frames in hook.png).
- Daily `viral --category home` board: viral_home.txt (542 videos scanned, 71 shop videos in last 3 days; tiktok-out/viral-2026-10-04.json).
- Learnings: winners are 6-10 s with one reveal; ours is ~36 s (Grace's script, 121 words). Hook stays in the first 2 s; one feature per cut with a hand shot (@teddyandhudson, from the V1 research).

## Hand size / pointing research (2026-10-04, Ralph rejected the first pointing still)
4 furniture videos checked frame by frame (`research/pointing_examples.jpg`; `research/pointing/`): @aoxun.ultra 474k (small hand points at the TV stand base from the right edge), @lulumamiii 577k (hand reaches in from the edge, small), @kayla.ttsfinds 418k (hand only opens a drawer, product fills the frame), @cozygirlfindss 128k (no hand, slow pushes). The hand is always small, at a frame edge, the furniture stays the hero.

## Kling test (2026-10-04, Ralph's account via MCP, `kling-video-v3_0_turbo`, 4 s, 720p, from stills/P1_small.png)
32 credits (816 -> 784). `clips/P1_kling.mp4`: real 3D parallax dolly-in + small hand at the left edge pointing at the mirror, no forearm, vanity details stable. Prompt: POV handheld, slight dolly-in with parallax, hand small at the left edge, nothing else changes.

## Kling P1 final (2026-10-04): `clips/P1_kling3.mp4`, 32 credits (752 -> 720). Kling total this job: 96 credits (816 -> 720).
Prompt locks the hand ("only the CAMERA moves ... hand and wrist stay fixed at the left edge for the entire video"). QC: 2x zoom on the hand edge frames 0-95, fingertip frames 10-90: no halo, no forearm, no sweep, mirror stays lit, vanity details stable. Passes REMOVED.md.

## Kling P2 (2026-10-04): `clips/P2_kling.mp4`, 32 credits (720 -> 688). Kling total this job: 128 credits (816 -> 688).
QC (2x zoom, frames 0-95): hand small at the right edge, no halo, no forearm, real 3D dolly, vanity stable. PROBLEM: the camera drifted left and the hand slid OUT of frame after ~1.2 s (frames 40+ show no hand), the mirror cabinet also drifts off the right edge. Usable only as a ~1.2 s beat (trim 0-1.6 s). A redo should say "straight dolly-in, no sideways drift".
