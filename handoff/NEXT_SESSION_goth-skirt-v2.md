# Handoff: Goth High-Low Skirt v2 (Grace), try-on route (2026-10-25)

Ralph (2026-10-25): "Let's start a new session because there have been updates and I think you are not operating on the
most recent skills. Handoff and start a new session. Remember we are replicating the video from the link."

## THE GOAL: replicate the inspo video
@jaquelineee809, https://www.tiktok.com/t/ZPLADgmcu (local copy `ugc/goth-highlow-skirt/research/inspo/`, beat table
`ugc/goth-highlow-skirt/research/inspo_beats.md`). Mirror-style, 5 looks: top of knee -> turn to the back -> both hands pull
the front waist strings, hem rises to mid-thigh -> one leg JUST above the knee -> both sides up (shortest) -> walk, crossed legs.
Every plan, still and clip is judged against that beat table + the 3 product truths in the same file. Boots instead of heels.

## Read first (in this order)
1. Repo CLAUDE.md (new since the last session: Flow first for product clips, prompt-master MUST be loaded with the Skill tool,
   camofox, Obsidian brain: attach focusfiyah/obsidian-vault and read Brain/Index.md). Run `python3 handoff/branch_sync.py`.
2. grace/PLAYBOOK.md §6 (search "goth skirt"), `ugc/goth-highlow-skirt/README.md` (Status line), `BOOK.md`,
   `tryon/QC.md` (5 try-on tests), review page rounds 22-29: https://claude.ai/artifact/3JRHDgMib5grRRR9ybu1QA
3. Load the skills fresh: unlazy, ugc-product-ad, prompt-master (Skill tool), and grace-fashion-ads if listed.

## What the try-on tests proved (fal, $0.44 spent, logged in grace/spend.json other)
- Kling Kolors try-on (fal-ai/kling/v1-5/kolors-virtual-try-on, $0.07) keeps the REAL skirt's shape (round 26, best:
  `tryon/kolors_shorts.png`); colour reads a little khaki (free colour shift), front ruching softer, strings faint.
- FASHN v1.6 ($0.075) only swaps a SEPARATE bottom garment: on pants it gave the best waist + both drawstrings (round 23) but
  the hem copied the pants' column shape; on a one-piece bodysuit it did nothing. segmentation_free=false made it worse.
- Runner: `tryon/run_tryon.py` (fal queue, header `Authorization: Key $fal_key`, one-shot per name, log tryon_log.json).
  It is NOT wired into grace/gate.py start_task yet: wire it (usd passed explicitly) before the first paid still.

## Ralph's decisions so far
- 2026-10-25: use Grace's 4 real body photos (`grace/ref/body/`, sheet `grace_body_sheet.png`: front w/ face, front w/ feet,
  back, right side; pink tank, sheer black tights, pink satin head wrap) as the pose bases. Real back view -> L2 is the real back.
- 2026-10-25: top = black fitted long-sleeve (garment `tryon/garment_top_black_ls.jpg`, cropped from the approved FULL2 still).
- 2026-10-25 answers to BOOK §7: (1) "Neck down" -> crop every shot from the neck down (head wrap out of frame).
  (2) "No, wanted her legs to show with the boots" -> NO sheer black tights: bare legs with black knee-high boots (flat lug
  sole, as cut 1). The body photos have tights and no boots, so the plan needs a step for bare legs + boots
  (options to quote: a third try-on/edit pass, a Kie nano-banana-pro edit per still ($0.09), or Ralph's Gemini app $0 first).
  Re-quote BOOK.md with that step BEFORE any spend; BOOK.md is NOT approved yet (rev 2 at $2.14 is void once edited).
- Video clips: Flow first ($0 takes from Ralph's Google Flow app, kit = still + logo/fabric close-ups + sheet + one
  prompt-master prompt), Kie Omni $0.315 only when Flow can't. Music-only, no text, tug-cut edit, AI finish last.
- Redo cap $0.50 for the job; ask before every paid call with the exact cost. October has no cap; from November $100/month.

## State
- Drive: Grace Tiktok assets/Goth High-Low Skirt (Grace) (1dSRBdxMyA0_lZ4ZThrLCMpHfD0a59LED). Do not change CURRENT without Ralph.
- Kie Goth job spend $3.46; fal $0.44. Prompts `prompts/v2_L1..L5.txt` (write them again with prompt-master loaded).
- Phone push (PushNotification) was not offered by ToolSearch in the last session; email via Composio works
  (server name may be `Composio_for_Social_Media`, account gmail_correa-comus).
