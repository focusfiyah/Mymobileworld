---
name: grace-sales-tracker
description: Logs Grace's AI videos that made sales into her sales tracker (product, hook, faceless, pain point, problem the product solves, why it converted, script as posted, link, sales), finds the patterns across them, and writes new versions built to sell more. Use when Ralph or Grace sends TikTok links with a sales count ("this one got 2 sales", "AI videos that made sales", "add to the tracker", "winners sheet", "why did this convert"), or asks for better versions of a video that sold. For writing scripts for a new product use grace-product-scripts; for breaking down someone else's TikTok use tiktok-shop-coach.
---

# Grace sales tracker

Grace wants one list of her AI videos that turned into sales, so each new video copies what sold. She sends a link
and a sales count; everything else comes from TikTok's public page, the frames and our job folders. The tracker's
source of truth is `grace/winners/winners.json` in focusfiyah/Mymobileworld; the Google Sheet in Drive is the copy
Grace reads.

## Add a video

1. `export WINNERS_OUT=<scratchpad>/winners; python3 grace/winners/winners.py pull <link> --sales N` (Mymobileworld
   repo root; needs Playwright, so run Dayone-ai `bash setup.sh` first in a fresh container). It fills product,
   caption, views, saves, posted date, the script as posted (TikTok captions, or a free local transcript when TikTok
   has none) and the closest library hook. Sales is Grace's number: TikTok does not show it.
2. Look at the frames it prints (`sheet.png`, `hook.png`) and fill the judgment fields with
   `winners.py set <id> faceless=... format=... onscreen_text=... pain_point=... problem_solved=... why_converted=... job=...`.
   `job` = our `ugc/<job>` folder and how the posted words differ from our draft (compare with `vo/vo.json`).
   `winners.py todo` lists what is still empty.
   House of Rameau (@houseoframeau, shared by Ralph and Grace): Composio TikTok `tiktok_buck-flunk` lists every
   public video with views; `houseoframeau/README.md` has the refresh steps and the shop-video inventory.
3. Same video again with a new count: `pull` again; it updates the numbers and keeps sales notes and judgment.
4. `winners.py export`, then replace the Google Sheet's contents (folder link in `grace/winners/README.md`).
5. Update `PATTERNS.md` when a new video confirms or breaks a pattern; the number to beat is views per sale, not views.

Done when: `python3 grace/winners/check.py fields` passes for every row (update its SEED list when rows are added),
the sheet in Drive matches `winners.csv`, and Ralph has the sheet link.

## Write better versions

Each new version changes ONE thing from `PATTERNS.md` (sharper scene, deadline as hook, objection as hook, gift
angle that asks for two, proof in the first second, shorter cut) and says which, so the next sales show what
worked. Write them in Grace's looser wording on top of a named library hook: her posted scripts in `winners.json` are
the voice sample. Add them to `VERSIONS.md` and run `check.py versions` (hook base named and not read word for word,
orange cart close, banned phrases, grade 6 or lower). The script rules are Grace's (`grace/PLAYBOOK.md`); making the video is ugc-product-ad, with the
cost asked first.

## Rules

- Never guess a sales count or a reason Grace gave. Why: only she can see orders. TikTok's ad label on her videos
  means the brand paid to promote it (Ralph 2026-10-20); `winners.py` fills the Promoted column from it, and views
  per sale are compared within promoted or not.
- The script column is what was said in the posted video, not our draft. Why: on 2026-10-20, 4 of the first 5 Grace
  videos had been re-worded by her when posted, and her version is the one that sold; Ralph then chose her looser
  wording for new versions.
- Flag claims in a selling video that the listing cannot back, and leave them out of new versions. Why: "these keep
  selling out" (Tiger Eye) and "hair growing longer" (BodyJ) were in winners on 2026-10-20.

## Files

- `grace/winners/winners.py` (Mymobileworld): pull, set, refresh, export, todo.
- `grace/winners/check.py`: the gate checks (fields, intake, export, patterns, versions, proofs).
- `grace/winners/PATTERNS.md`, `VERSIONS.md`, `README.md`: the read, the new versions, links and status.
