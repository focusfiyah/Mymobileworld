# Handoff: fashion AI videos for Grace — virtual try-on test (2026-10-22)

Ralph (2026-10-22): "This has been a fail. Grace is going to be getting into more fashion like this and we need to have a
better outcome. Especially with the spending on redos." He does NOT want a third-party subscription. Then: "Create a
handoff and start a new session ... run the test."

## Why the goth skirt job failed (ugc/goth-highlow-skirt/, read README.md + research/inspo_beats.md)
1. Planned before studying the inspo: missed its looks, the waist strings, the one-leg height, the solid fabric until Ralph named each.
2. Image/video models REDREW the garment every time, so it drifted: fitted midi, short back, see-through chiffon, side ties.
3. Paid one weak test after another instead of locking stills of every look first, then animating once.
4. Judged takes loosely instead of ticking a written beat table + product truths; Ralph had to find every miss.
Spend: Kie $3.46 (quote was $1.62), Kling 310 of Ralph's credits (8 left). PLAYBOOK §6 has the lessons (search "goth skirt").

## Product truths for this skirt (check every still and take against these first, at 2x)
- Drawstrings come out of the waistband at the FRONT; every pull is up and out from the waist. No side tie, no hand lifting the hem.
- One-leg lift reaches only JUST ABOVE THE KNEE (inspo 11.4 s).
- NOT see-through: solid dark chocolate brown fabric (only a lining is faintly sheer; legs never visible through it).
- Inspo (@jaquelineee809, research/inspo/): knee -> turn to the back -> both hands pull strings from the waist, hem rises to mid-thigh -> one leg just above the knee -> both sides up (front mid-thigh) -> walk, crossed legs. Beat table: research/inspo_beats.md.

## The test to run now (Ralph said "run the test")
Goal: see if VIRTUAL TRY-ON puts the REAL skirt (from the listing photo) on Grace without redrawing it, so fabric, opacity,
ruching and front waist strings stay true. These run on accounts already connected (fal is proxy-injected here; Kling is
Ralph's MCP account), no new subscription.
1. Check the current price of each model on its own page first (not tested last session): FASHN try-on on fal
   (https://blog.fal.ai/new-sota-virtual-try-on-model-by-fashn-live-on-fal, fal "fashn/tryon" v1.6) and Kling Kolors
   virtual try-on on fal (`fal-ai/kling/v1-5/kolors-virtual-try-on`). Test one free/tiny request to confirm fal access works.
2. Inputs: person = `ugc/goth-highlow-skirt/stills/FULL2.png` (Grace, full body, both hands at the waist, no phone, Ralph's
   bedroom); garment = the real brown listing photo `ugc/goth-highlow-skirt/research/listing/28_x_13987564.webp` (front) —
   convert to PNG/JPG; try the back photo 30_x_c5008ece.webp only if a model takes a second view.
3. ONE image per model (2 total). Budget for the test: up to $0.50 total across both, pre-approved by "run the test";
   anything above that, or any second try, ask Ralph first with the exact cost (CLAUDE.md). Log spend in
   `grace/spend.json` "other" (fal is not Kie).
4. QC at 2x against the product truths + the real listing photo: solid fabric (no legs through it), ruching, the two front
   waist strings, long ruffled back, Grace's face/skin/braids unchanged, boots unchanged. Write the verdict per model.
5. Put both results side by side with the real photo and FULL2 on the job's review page
   (https://claude.ai/artifact/3JRHDgMib5grRRR9ybu1QA, file ugc/goth-highlow-skirt/review/index.html, newest on top),
   push + email Ralph (one line: what to review + exact cost).

## If try-on works: the new fashion route to propose (quote it, one approval)
1. Inspo beat table + product truths BEFORE any plan; Ralph approves the list.
2. Try-on stills, one per look, same framing; storyboard to Ralph before any video spend.
3. One Kling 4.0 keyframe take (first_image + keyframe_1..n = the approved stills) with the skirt saved as a Kling Element
   (element_create from the real photos) so every clip is bound to it.
4. Every take ticked against the beat table + product truths before Ralph sees it; a miss is a fail.
5. Redo cap per job, stated in the plan.
Then write the route into the skills via skill-smith (focusfiyah/claude-skills: grace-fashion-ads + ugc-product-ad
references) and deploy.

## State
- Drive: Grace Tiktok assets/Goth High-Low Skirt (Grace) (1dSRBdxMyA0_lZ4ZThrLCMpHfD0a59LED): CURRENT V2 + V3..V10 + caption doc;
  cut 1 in Older versions. Ralph has not picked a final; do not change CURRENT without his word.
- Kling account: 8 credits left. October Kie: `python3 grace/spend.py` (no cap in October; $100/month from November).
- Session start: `python3 handoff/branch_sync.py`; rename the session to the job; load unlazy and write a GATES.md for the test.
