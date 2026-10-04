# Handoff: TIRTIR Mask Fit Red Cushion scripts for Grace (best-quality pass)
Paste this whole file into a Claude Code session on focusfiyah/Mymobileworld (desktop, where TikTok video pages load). Written 2026-10-04.

## Task
Upgrade the 3 talking-head scripts for Grace (client) for the TIRTIR [Official] Mask Fit Red Cushion Foundation (0.63oz). Use EVERY tool and rule we have. Ralph is the owner; you are his chief executive assistant. Ask before any paid call (scripts need none, $0).

## Where things are
- Job folder: `ugc/tirtir-red-cushion/` (scripts.md = current final, checklist.json + proof files, research/ = viral board, shop, tag data, coach_notes.md).
- Drive: Grace Tiktok assets / "TIRTIR Mask Fit Red Cushion scripts (2026-10-04)", Google Doc "TIRTIR Mask Fit Red Cushion scripts for Grace (2026-10-04)" (id 1b3Qoq6QJP6hKokobdBCpFHsp4mYM6zf3qQgT5ZVF_NQ, folder id 10l9sE-0gw5eotnQkBYhh6rE2ijP4wjGh). The Drive copy does not sync: re-upload after edits.
- Rules: `grace/PLAYBOOK.md` (read first), `CLAUDE.md` Rule 0, skills `grace-product-scripts`, `tiktok-shop-coach`, `humanizer`, `ugc-product-ad` (reference only).

## Current scripts (all ~30 s, 83-98 spoken words, readability 3.8-5.3)
1. Full coverage that feels light (category-gap hook)  2. Read the label (five listing claims)  3. Sensitive skin, full coverage (identity call-out). Each: HOOK / BODY / CTA, 2 alternate hooks, on-screen text, caption with #ad, one optional [Insert].

## What is missing (why this pass exists)
The cloud session could NOT run `tiktok.py video` (TikTok returned "no video data" for every link, even stats-only), so hooks were modeled from captions, stats and the playbook, not from transcripts and hook frames. Do this properly now.

## Steps (do all, unasked)
1. `git pull`; read `grace/PLAYBOOK.md` and the job's `research/coach_notes.md`, `hooks.md`, `line_sources.md`.
2. Coach (`.claude/skills/tiktok-shop-coach/scripts/tiktok.py`; run `bash setup.sh` from Dayone-ai if Playwright is missing). Save outputs under `ugc/tirtir-red-cushion/research/`:
   - `video` on these winners (transcript, hook.png, sheet.png; LOOK at every hook.png): jawarshere 7690680310077345025 (62.6k, "Now, THIS is how you do COVERAGE!!"), machyismuch 7692555066393267487 (1.94% saves), magicwithmercedes 7690615922326867213, tammyyyrr 7691794132557204749, luvphoebeee 7686647173416570142 (146.5k HERA cushion shop video), missdarcei 7683571029494615317 (7.9M TIRTIR glow cushion), tirtir.official 7681104429344476446 (742k, 4.09% saves).
   - Rerun `viral --days 30 --category beauty --add-tags cushionfoundation,tirtir,kbeautymakeup,koreanmakeup` if a day has passed, plus `discover` pages (WebSearch `site:tiktok.com/discover tirtir red cushion`, `cushion foundation`) and `tag cushionfoundation`, `tag koreanmakeup`.
   - Note per winner: first-second visual, spoken hook, on-screen text, length, words/s, cuts/10 s, proof moment, CTA, save rate.
3. Product facts: listing text (below) is the source of truth; recheck https://tirtir.global/products/mask-fit-red-cushion and the TikTok Shop page (68k lifetime units, 4.6, 9.9k reviews). Keep: no SPF, refill, mask-proof or transfer-proof claims; 72-hour claim only as "the listing says"; no price.
4. Rework hooks and bodies from the real winners. Keep Grace's structure: curiosity-loop hook, pain beat at top of body, selling point/solution, FOMO/urgency CTA (real: holidays, photo season), close "It's in the orange cart." Never "order it now", never a price, no downsides or "heads up", no "one is enough". Grace's point of view (friend voice, reading the label), no expert voice. Three scripts must be different angles; give each its own on-screen text (5-7 words, curiosity only, never names the product).
5. `humanizer` on every spoken line, on-screen text and caption (casual spoken voice); no dashes; report tells found.
6. `tiktok.py readability` on each script (grade <= 6; 80-100 words each).
7. After rewriting scripts.md, refresh EVERY proof file so it is newer than scripts.md (`hooks.md`, `humanizer.md`, `readability.txt`, `line_sources.md`), update `checklist.json` proofs (add the new `research/videos/*` files under coach_research), then `python3 grace/gate.py ugc/tirtir-red-cushion` must print GATE OK. Never weaken the gate; keep banned phrases out of the rules text too (the gate scans scripts.md).
8. Compare drafts to the top winner: for any of Grace's later cuts use `tiktok.py compare <winner> <cut> --stage cut`; for scripts, add a short "beats vs winner" table to `hooks.md`.
9. Deliver: update the Google Doc in the Drive folder (Google Drive connector; Docs mangle 4-byte emoji, so none). NO PDF (Ralph said not needed). Update the job `README.md` Status line and add one line to `grace/PLAYBOOK.md` §7. Commit and push to main. Send Ralph a phone push (PushNotification) with one line.
10. Ask Ralph one short question only if something is unclear; do not guess.

## Listing facts (Ralph pasted, TIRTIR Official)
Mask Fit Red Cushion Foundation, Korean makeup, 0.63oz, satin finish, lightweight radiant coverage, 40 shades, effortless application. Flawless coverage (evens skin tone, blurs pores); hydrating (hyaluronic acid, botanical extracts); long-lasting "up to 72 hours of flawless, fade-resistant coverage"; lightweight, breathable, non-cakey, suitable for sensitive and acne-prone skin; 40 shades; dermatologist-tested, sensitive skin friendly.

## Done when
GATE OK, the doc in Drive updated, README Status current, pushed, Ralph notified. Report: what changed from v1 and which winner each hook is modeled on (link + views + saves).
