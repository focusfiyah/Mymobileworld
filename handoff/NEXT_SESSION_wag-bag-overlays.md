# Next session: Wag Bag hook overlays (photos instead of emoji)

Written 2026-10-06. Repo focusfiyah/Mymobileworld, branch `ccr-a0dae179-slh3lv` (Dayone-ai same branch, nothing pending there).
Job folder `ugc/wag-bag-v2/` (README.md = full job history, GATES.md = last round's unlazy ledger, `qc/verify_fix.py` = checks).
Model: Claude Sonnet 5.5 or Opus 5.5, either works for this job.

## Paste this as the first message of the new session
> Continue the Wag Bag overlays for Grace. Read handoff/NEXT_SESSION_wag-bag-overlays.md and ugc/wag-bag-v2/README.md. Keys are in the environment. Follow my standing rules (unlazy GATES.md first, speed rule: test one clip, re-render only what changed, give me an ETA, ask before any paid step with the exact cost).

## Where things stand
- **Drive** (Grace Tiktok assets / WagBag Final Edits, folder `1ZgU9Z8oQkT_Wca_EkXtfd6AbDFHZZgG8`): CURRENT - Wag Bag V1..V5 (2026-10-06) = **r3**: 5 videos from Grace's real takes, hook overlays are the 3D Fluent emoji (💧 water, 🔋 battery, ⚡ generator, 💩 + white ❔ poop), V3 jump + V4 clipped "make" FIXED. All 7 unlazy gates passed, $0 spent. File ids: V1 `130Y6zxfamvEaVUIAgB-hAGm2wnfQX8N-`, V2 `11m7D03oydQKOB7jPPfgWyjo3EVH-Fj28`, V3 `1N6yUptRaX6eOgx-y8X0UZciM03aQ4DTu`, V4 `181GYySGJgJxWbkIjI9o3t6WEpB55yNYL`, V5 `1sSuNb8dYjRbeVA7bVfTDLsR3LMfl8HQ-`. Captions doc `1JCxUpDcy55nlbcWnL4hw7bn9-2eBjtg3SvT5sNre_NA`. Older versions folder `1liz954HDVxBhewTbdgG4JqcGUTI2B-03` (Sept 30 set, r1 flat emoji, r2).
- **Ralph asked (2026-10-06): "use images instead" of emoji for the hook overlays; answered "Go with 1" = free real photos.** Not yet in any video.
- **Done for the photo route:** water (glass of water, CC0 StockSnap) and battery (single AA, CC0 StockSnap, no brand) are cut out as stickers: `photos/cut/water.png`, `photos/cut/battery.png`. Preview on Grace: `photos/preview_photos.png` (sent to Ralph, he did not object). Sources/licences: `photos/SOURCES.md`.
- **Open decisions for Ralph (asked, not answered):**
  1. **Generator photo.** No public-domain, brandless portable-generator photo found on Openverse (everything real is CC-BY/BY-SA and shows Honda/WEN). Options told to Ralph: (a) generate one, Gemini 3 Pro Image on Kie, $0.09 (ask first, show before use, no redo without OK), (b) Ralph drops a photo in the Drive folder, (c) a credited CC-BY photo (e.g. Honda EU7000iS flickr 40229947292) with credit in the caption. **New since then: `PEXELS_API_KEY` is set in the environment and works** (`python3 ugc/wag-bag-v2/photos/search_photos.py "portable generator" 12`); try Pexels first (free, no credit, brand may still show: check). `PIXABAY_API_KEY` is NOT set yet (Ralph is adding it; web pages of both sites 403, the APIs work).
  2. **Poop.** Keep 3D 💩 + ❔ (my recommendation: Grace asked for it by name, a poop photo is unpleasant) or make it a photo too.

## Do next (in this order, ETA ~25 min)
1. Load `unlazy`; write a new GATES file for this round (name it `GATES_overlay.md`; the old GATES.md is r3's). Gates: overlay PNGs exist at 512px and are shown <=1.2x size (rule), no overlay covers Grace's face, flash/sync/words/levels checks still pass (`python3 -I qc/verify_fix.py flash|sync|words|levels`), Drive replaced + sizes match, committed + pushed.
2. Search generator on Pexels (and Pixabay if the key is there); view a contact sheet; pick brandless, clean-background; `python3 photos/make_sticker.py full/generator.jpg cut/generator.png`. If nothing good: ask Ralph (options above).
3. Swap pops in `ugc/wag-bag-v2/videos.json` (segment 0 of every video, 5 pops: png, size, t, x, y; `png` is relative to `emoji/`, so put photos at `emoji/photo_*.png` or change the path logic in `cut.py` `pop_frames`). Timing per Grace's words is already set (water, battery, generator, "where", +0.3s question mark). Photo stickers at size ~220-260.
4. **Test ONE video first** (V3 hook): `python3 cut.py 3`, look at frames at full size (2x zoom on edges, per rule), then `python3 cut.py` for all. `cut.py` caches clips by content, so only the hook clip + final join re-render.
5. Run the 4 checks + gate-check (`node <unlazy skill>/scripts/gate-check.mjs --approve ugc/wag-bag-v2/GATES_overlay.md`).
6. Drive: rename current CURRENT files "Wag Bag Vn - v3 3D emoji (2026-10-06).mp4" into Older versions, upload new ones as "CURRENT - Wag Bag Vn (date).mp4" (host with `photos/../host.py`, upload with Composio `GOOGLEDRIVE_UPLOAD_FROM_URL`, account `googledrive_lin-ernst`), check byte sizes match.
7. PushNotification to Ralph (one line), update README Status + CLAUDE.md Wag Bag line, commit + push.

## Rebuilding the working files (not in git: big media, see .gitignore)
- Sources in Drive folder `1HpF7SZ9VDTC62pWK_HXpzx909YwVTBDR`: `WAG BAG 1 (NEW).mov` id `1kzfZXoD_2HcT2oa5jg5O9bx0tNcg0XX7` -> `src/p1_new.mov`; `WAG Bag 2 (NEW).mov` `1AtGY1CnLzj24ottvsELZdz7blgNyDCoj` -> `src/p2_new.mov`; `WAG BAG 2 (3-5).MOV` `1EztOdcaWPh3oO36irVXz8WoVbtSYRnx8` -> `src/old2_35.mov`; `WAGBAG3.MOV` `1v_p-KZfCDDtkR_8RpH9P1gnLRjlmObUY` -> `src/old3.mov`. Download: Composio `GOOGLEDRIVE_DOWNLOAD_FILE` (account `googledrive_lin-ernst`) gives an s3url, then curl it.
- `pip install faster-whisper soundfile rembg onnxruntime` (the words check uses faster-whisper `medium.en`; `small.en` misheard "orange cart"). rembg model: see `photos/make_sticker.py` header.
- `photos/full/*.jpg` (full-size source photos) are gitignored; re-fetch via `photos/SOURCES.md` links or `search_photos.py`.
- ffmpeg: `cut.py` writes `tmp/`, `out/` (gitignored). A full 5-video render is ~10 min on 4 cores; a hook-only re-render is much less.

## Lessons this job (all also in grace/PLAYBOOK.md, newest at the bottom)
- Grace's phone files are several takes joined: start clips just after a join (scene-cut scan). Never trim loudnorm output by time; cut sound by sample count; join with ONE concat filter. Check sync per clip against the source, not only by re-transcribing.
- Overlays: premium only (Fluent 3D or sharp photo stickers), never enlarged >1.2x, follow the spoken words (Grace said battery, not food), offer a free same-set stand-in before a paid image, free licences only (CC0/PDM, or Pexels/Pixabay licence) because overlay credit is impossible.
- Free photo sources from this server: Openverse API works (set a User-Agent, filter `license=cc0,pdm`); Wikimedia API 429s; Pexels/Pixabay APIs work with keys; their web pages 403.
- Time: Ralph said the r3 fix took far too long. Test one clip, re-render only changes, state the ETA first.

## Ralph's to-dos (outside the repo)
- Add `PIXABAY_API_KEY` in the cloud environment settings (Pexels is already in).
- Paste `handoff/REMEMBER_ME_paste.txt` into a new claude.ai chat; re-upload `handoff/ugc-product-ad-skill.zip` and `Dayone-ai/handoff/day-one-ai-skill.zip` to claude.ai (both contain the unlazy + overlay rules). Not confirmed done.
- Decide the two open questions above.

## Standing rules in force (full list: CLAUDE.md, handoff/REMEMBER_ME.txt)
Unlazy GATES.md on every job; speed rule; ask before every paid generation with the exact cost; free fixes first; QC before Ralph sees anything (2x zoom edges, first second); overlays premium; no text unless asked; every video different; Drive = one folder per product, CURRENT on top, old versions in "Older versions"; PushNotification when something needs his review; never say a tool/site is unavailable without testing it this session.
