# Google Flow route (standing rule since 2026-10-24)

**Flow first for every product clip, Kie second (Ralph 2026-10-24, after the PRITECH trial: "we can do it until credits run out").**
Measured on the trial: Omni 1.1 Flash = 12 credits per 4 s clip (Flow shows the cost before generating; Veo 3.1 Lite 10, Veo 3.1 Fast 20),
download 720p or 1080p (ask for the 1080 download). Send the kit as files in the chat (SendUserFile: prompt txt + the images in upload order)
and on the review page. Kie Omni only when his credits run out, he can't make it, or the Flow take fails QC (asked with cost).
The trial steps below stay as the how-to.

Ralph has the Google Flow phone app on his Google AI Pro plan: 1,050 credits a month (1,000 + 50 daily), no rollover,
visible watermark already off (screenshot 2026-10-23). Flow runs Gemini Omni Flash (the model we pay Kie $0.315 per 4 s
for) and Veo 3.1 Fast, with Ingredients to Video (reference images). Ralph: "Yes, set it up for the next job."

Why: October Kie spend was about $144, mostly product clips and redos. A clip made in Flow costs $0 extra; the cost
is Ralph's time on his phone. Same idea as the Gemini app stills route (CLAUDE.md, 2026-10-20).

Not tested yet (third-party figures, 2026-10-23): Omni Flash 4 s about 7 to 15 credits, Veo 3.1 Fast about 20;
whether Flow's Omni takes a start frame and ingredients together; download resolution. The trial measures these.


**Kit delivery (2026-10-24, JIYU: Ralph "It's not clear how you provided the 6 flow kits" after 29 loose files in the chat):** put each shot's kit on the job's review page as its own card (the line, the steps, the images in upload order with a Save button each, the prompt with Copy and Save buttons; the page declares the `downloads` capability). Template: `ugc/jiyu-polish-pads/review/index.html` (Flow kits section). Send files in the chat only for a single shot.

## The trial (next job with a product clip, then ask Ralph)
1. Pick the riskiest product clip (the one most likely to drift: small print, a hand move, a turn).
2. Make it BOTH ways: the Kie Omni take from the BOOK.md quote as usual, and a Flow take from the same still and refs.
   The Flow take is $0 and goes in BOOK.md as its own line ("S3 Flow trial: $0, Ralph's credits").
3. Send Ralph the kit (below) on the job's review page, with each reference image downloadable on his phone.
4. Ralph notes his Flow credits before and after (Account screen), makes the clip, saves it and sends it back
   (chat upload or the job's Drive folder).
5. QC the Flow take exactly like a paid one: `ffprobe` size, fps and length; 2x zoom on hand/product edges and the
   first second; every letter of the label against the close-up; grip, whole wrist, no flip; REMOVED.md.
6. Put both takes side by side on the review page with: credits used, resolution, QC result, which one holds the print.
7. Log the result in `grace/flow/RESULTS.md` (date, job, shot, credits, resolution, QC verdict, Ralph's pick).
8. Ask Ralph once: make "Flow first for product clips, Kie second" a standing rule? Save it everywhere only on his yes.

## Kit format (one block per clip, written with prompt-master "Ralph's stack")
```
## S3 (HAND or HAND-FREE): "<the spoken line>"
Flow: new project > Video > model Gemini Omni Flash (if missing: Veo 3.1 Fast and say so) > 9:16 > 4 s
Upload as Ingredients, in this order: 1 still_S3.png (if Flow offers a start frame, put it there instead),
2 logo_closeup.png (one per logo/label in frame), 3 product_sheet.png
Prompt:
<product-lock.md template: image 1 = the first frame; image 2 = the real label, letter for letter and colour for
colour; image 3 = the sheet, exact shape/size/colours, no added marks; ONE small motion, one grip, never flips;
camera move; bright neutral light; no music, no voice, no captions, no on-screen text>
```
Keep each prompt under the length Flow's box takes; if it cuts off, shorten the PLACE block first, never the product
block.
