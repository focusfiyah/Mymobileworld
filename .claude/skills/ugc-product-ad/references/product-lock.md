# Product lock (Ralph 2026-10-21, every job, every product)

Ralph: "We need to have product lock on all products moving forward ... using Google Omni to ensure product stay true
to the original. Pasting labels should be a last resort." Why: in October the Kie bill reached about $144 (grace/spend.py),
most of it redos after the product drifted (Vans: the pink-bag gift shot's shoe design changed and was let go only to
stop spending; 13 of 27 Vans clips came back with a pale side tab; Cleanwaste: 3 of 4 small boxes drew an old design).

## Contents
- The route
- Prompt template (write it with prompt-master)
- Fixing a drifted take
- Cost and budget
- What stays the same

## The route
1. **References first, free:** the product reference sheet (real photos, PLAYBOOK §6), plus a tight close-up crop of
   EACH logo/label/print the camera will see, cut from the brand's real photo. Ralph confirms every product detail in
   the plan before spend.
2. **Stills:** Gemini 3 Pro Image (Kie `nano-banana-pro`) with the sheet + close-ups, used clean. QC at 2x against the
   real photo (shape, colours, every letter, size) before any clip is paid for.
3. **Flow first (Ralph 2026-10-24, after the PRITECH trial: "we can do it until credits run out"):** every clip where the
   product is in frame is first a free take Ralph makes in his Google Flow phone app (Omni 1.1 Flash, 12 credits per 4 s
   clip, 1,050 a month, no rollover; he downloads it at 1080) from your kit: the still, a close-up of each logo, the sheet
   and one prompt (format and steps: Mymobileworld `grace/flow/README.md`). QC it exactly like a paid take. Kie (below)
   only when his Flow credits run out, he can't make it, or the Flow take fails QC, asked with the cost.
   **Otherwise: Google Gemini Omni 1.1 Flash ON KIE** (Ralph 2026-10-22: "Use Omni on
   kie not thru the API key"; Kie model `google/gemini-omni-flash-1-1`, cheaper than Google direct and 1080p at the
   same price): `python3 .claude/skills/ugc-product-ad/scripts/omni_clip.py <job> S3 --prompt-file prompts/S3.txt
   --still stills/S3.png --ref refs/logo_side.png --ref refs/product_sheet.png --seconds 4` (`--dry` first: prints the
   cost, spends nothing). Never call Omni through the Gemini API key or OpenMontage's Google tool. Omni binds the product as a named reference for the whole clip; Seedance only copies the
   first frame and then redraws the print.
4. **Clips with no product in frame** (room, hand-free scenery, a hand without the product): Seedance 2.0 Mini on Kie
   as before ($0.041/s). No Kling unless Ralph asks.
5. **QC every Omni take at 2x on several frames** against the close-ups (letters, colours, shape) and the hand rules
   (grip, whole wrist, no flip). Omni renders audio; the runner strips it. Before that, the runner checks the still is
   9:16 before paying and the clip against its still after the download (Mymobileworld `grace/clip_check.py`,
   2026-10-26): a CLIP_CHECK_FAIL means look first and fetch the task again; Kie bills a clip that ignored the image.
6. **Paste-back is the last resort:** only when free fixes (crop, trim to the clean window, static patch) and one
   Omni edit turn have failed, and only with Ralph's OK for that shot. A pasted label reads as a sticker (LGXNDS 2026-10-19).

Unverified until the first job uses it: how well Omni holds small print through a big hand move. The first job runs ONE
product clip (the riskiest), QCs it, and only then the rest (CLAUDE.md hard rule 2).

## Prompt template (write it with prompt-master)
Kie's Omni takes either a first frame or reference images, not both, so it runs in reference mode: image 1 is the still,
then one real close-up per logo/label, then the sheet (7 images at most). The runner refuses a prompt that leaves an
image unnamed or never says "first frame".

```
Recreate image 1 exactly as the first frame: keep its room, light, framing and hand exactly.
Image 2 is the real <logo/label> of the product: it stays on the product the whole clip and matches image 2
letter for letter and colour for colour. Image 3 is the product sheet: keep this exact shape, size and colours,
no added marks, no ® or ™, no extra text.
Motion: <one small motion, the hand keeps one grip, the product never turns its back or flips>.
Camera: <slow push-in / locked-off>. Vertical 9:16 phone footage, bright neutral daylight, realistic skin.
No music, no voice, no captions, no on-screen text.
```

## Fixing a drifted take
Use an Omni edit before any new take: `omni_clip.py <job> S3 --edit --prompt-file fix.txt` sends the last take back as
video input with a prompt naming only the change: "Make the side tab match <the close-up's look> exactly. Keep
everything else the same." $0.84 per edit on Kie (more than a new 4 s take, $0.315), so use it only when the rest of
the take is already right. Ask Ralph with the cost first, like any redo.

## Cost and budget
- Omni on Kie (list price, kie.ai/gemini-omni-1-1-flash, 2026-10-22; 360p/720p/1080p the same): 4 s $0.315, 6 s $0.42,
  8 s $0.525, 10 s $0.63; edit with video input $0.84. Seedance Mini is $0.041/s (4 s $0.164). Keep product shots 4 s;
  the plan quotes each shot's model and price and includes one likely fix. Kie logs it in the job's kie_log.json, so
  `grace/spend.py` counts it.
- Every plan and every redo question shows `python3 grace/spend.py`'s line: month so far vs Ralph's cap (none in October 2026, $100/month from November). At the cap,
  `grace/gate.py` refuses every paid runner until Ralph's OK is recorded in `grace/spend.json` over_cap_ok.

## What stays the same
Script gate, one plan + one approval, storyboard before video spend, one test clip, free fixes first, AI finish, QC
templates. Grace's voice: `grace/voice/README.md`.

## When the AI keeps redrawing a tiny product (Mini Bag Charm, 2026-10-27)
**Rule (Ralph 2026-10-28, "Yes save rules"): for a small or detailed product that will be pasted back, generate every
clip with NO product in it** (the bag, stocking or hand empty; a hand pinching a plain gold ring or nothing), then add
the real product as the only one in frame. Plan it that way in the storyboard, before any still. When a clip already
has the AI's copy, cover only that copy, its scarf and its shadow, never a whole box over the object it sits on.
Why: on Mini Bag Charm most of 10 cuts went to hiding the AI's own charm (bigger than the real one, it peeked out
between the fingers and under the real one), and box patches swapped in a different bag edge because the AI redraws
the host's shape frame to frame.

Seedance kept the true size but redrew a 9.5 cm charm within 1-2 s (a flap, a wide scarf, a mark on the padlock), and
Omni drew a whole handbag as the charm in a wide shot. What held, with Ralph's per-shot paste-back OK: the real charm
cut from the listing photo, placed at its true size on a charm-free still (`ugc/mini-bag-charm/tools/composite.py`),
a clip with a LOCKED or very slow camera, then the real charm laid onto every frame with the AI's own charm covered
by the clean plate, the patch stopping at the object's edge, and the charm hung from whatever the hand moves
(`ugc/mini-bag-charm/tools/track_paste.py`). Then the drift strip (SKILL.md QC) on every such shot.
