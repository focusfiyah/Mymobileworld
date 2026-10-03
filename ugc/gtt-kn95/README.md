# GTT Black KN95 50-pack (ELEHOME GTT shop): hands-only UGC video

**Client: Grace** (Ralph, 2026-10-03). Hands-only + ElevenLabs Grace B voiceover (`bGrsdLmwBbYUgHRuMFOI`, eleven_v4). Route: `ugc-product-ad` hands-only (template `../vicks-vaposhower/`). Rules: `grace/PLAYBOOK.md`.

Status: **2026-10-03 script v2 + matched shot list (10 shots, one AI-Grace face shot S4 with the mask on, no lip sync) waiting on Ralph. $0 spent. Gate OK (plan). Quote $2.75 Kie full / $2.24 lean. Next: Ralph answers questions, approves, then VO, still S1, test clip S2b. Kie balance $10.82.**

Quote (full match): 10 stills x $0.09 = $0.90; clips 45s x $0.041 = $1.85; VO ~534 chars ElevenLabs; cut/pop-up/SFX free; total Kie **$2.75**. Lean option: drop S2a + S5c, $2.24. Face shot S4 needs no lip sync (mask covers mouth). +~$0.25 per redone shot, each asked first.
Compliance: dust/outdoor angle only (the listing's own pitch); no illness, no N95/NIOSH/FDA, no layer count (listing says 4-layer in title, 5-layer in image: ask Grace), no price.
Refs: `refs/tiktok_listing.jpg` (screenshot), `refs/crop_black_set.png` (real box + mask packshot crop for the pop-up). Research + gate proofs: `research/`, `checklist.json`.

## Lessons baked into this job (PLAYBOOK + ugc-product-ad skill, checked 2026-10-03)
Plan/cost: whole plan in one message (done), ask before every paid call incl. redos, one test clip (S2 first), still storyboard before any clip, running total vs $1.82 at every step, phone push at each review point.
Product never drifts: pin in EVERY still prompt "grey GTT KN95 box, black GTT logo top-left, KN95 black text, DISPOSABLE PARTICULATE; black fish-shape mask with KN95 printed on the side, black ear loops, dotted seam" (small objects drift to a new design in close-ups); label text garbles, so the real-packshot pop-up (crop_black_set.png) covers every label moment; no box text/refs in no-box shots (S2), no hand text in no-hand shots; prompt text beats the image, so grep every prompt for the old look before rendering.
Seedance: "locked-off camera on a tripod"; plan each window from the clip's first ~1.5-2s (it redraws late: extra hands, box turning to its side panel); box front-facing start + free push-in hold if it turns; clip length >= its window, never stretch (>=1.0x); `generate_audio: false`, 720p 9:16.
Hands: one hand enters from the frame edge, whole wrist, no forearm, short squared lilac-white nails (same hand as Carpe/Plant Therapy); keep out of wide shots; `qc_hands.py` on EVERY frame of every hand clip (no background through the hand, no missing wrist, no stray second hand); nothing resting on thin air (crop to the object's base).
Free fixes first: crop, push-in (INTER_AREA 1.05x), blur, retime; measure shimmer/flicker on the FINAL file; no sway.
Edit: cuts on word timings (scribe_v2), pauses trimmed to 0.25s, 3.0-3.6 words/s, voice at ~0.05s, Classic caption "why fifty?" from frame 0 (`classic_caption.py`), pop-up anchored to the exact phrase and left of TikTok's right-hand buttons, CC0 SFX (shake, loop snap, box tap), loudnorm -16 LUFS.
Before Ralph sees the cut: `tiktok.py compare` vs @toashouse (closest) + the 1.6M benchmark (gate `--stage cut`), then frame-by-frame QC.
Delivery: Drive "Grace Tiktok assets" folder via BOTH routes (Kie host + Composio for the mp4; connector for folder/doc), sizes checked; scripts doc with no prices and no client name, emoji as HTML codes; update README Status, PLAYBOOK §7 line, handoff files if a standing rule changes.
