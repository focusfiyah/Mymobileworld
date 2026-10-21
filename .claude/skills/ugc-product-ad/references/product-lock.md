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
3. **Every clip where the product is in frame: Google Gemini Omni** reference-to-video (`gemini-omni-1.1-flash`,
   direct Gemini API, key injected in the cloud) through OpenMontage's `gemini_omni_video` tool:
   `python3 .claude/skills/ugc-product-ad/scripts/omni_clip.py <job> S3 --prompt-file prompts/S3.txt
   --first stills/S3.png --ref refs/logo_side.png --ref refs/product_sheet.png --seconds 4` (`--dry` first: prints the
   cost, spends nothing). Omni binds the product as a named reference for the whole clip; Seedance only copies the
   first frame and then redraws the print.
4. **Clips with no product in frame** (room, hand-free scenery, a hand without the product): Seedance 2.0 Mini on Kie
   as before ($0.041/s). No Kling unless Ralph asks.
5. **QC every Omni take at 2x on several frames** against the close-ups (letters, colours, shape) and the hand rules
   (grip, whole wrist, no flip). Omni renders audio; the runner strips it.
6. **Paste-back is the last resort:** only when free fixes (crop, trim to the clean window, static patch) and one
   Omni edit turn have failed, and only with Ralph's OK for that shot. A pasted label reads as a sticker (LGXNDS 2026-10-19).

Unverified until the first job uses it: how well Omni holds small print through a big hand move. The first job runs ONE
product clip (the riskiest), QCs it, and only then the rest (CLAUDE.md hard rule 2).

## Prompt template (write it with prompt-master)
Images go in order: the still is `<IMAGE_REF_0>`, close-ups `<IMAGE_REF_1>`.., the sheet last. The runner refuses a
prompt that leaves a tag out.

```
<FIRST_FRAME> <IMAGE_REF_0> is the opening frame: keep its room, light, framing and hand exactly.
<IMAGE_REF_1> is the real <logo/label> of the product: it stays on the product the whole clip and matches
<IMAGE_REF_1> letter for letter and colour for colour. <IMAGE_REF_2> is the product sheet: keep this exact shape,
size and colours, no added marks, no ® or ™, no extra text.
Motion: <one small motion, the hand keeps one grip, the product never turns its back or flips>.
Camera: <slow push-in / locked-off>. Vertical 9:16 phone footage, bright neutral daylight, realistic skin.
No music, no voice, no captions, no on-screen text.
```

## Fixing a drifted take
Use Omni's conversational edit before any new take: `omni_clip.py <job> S3 --edit --prompt-file fix.txt`, where
fix.txt names only the change: "Make the side tab match <the close-up's look> exactly. Keep everything else the same."
Same price per second as a new take, but everything Ralph already liked stays. Ask Ralph with the cost first, like any redo.

## Cost and budget
- Omni 720p is about $0.10/s ($0.51 for 5 s) vs Seedance Mini $0.041/s. Keep product shots 3-4 s; the plan quotes each
  shot's model and price and includes one likely fix.
- Every plan and every redo question shows `python3 grace/spend.py`'s line: month so far vs Ralph's cap. At the cap,
  `grace/gate.py` refuses every paid runner until Ralph's OK is recorded in `grace/spend.json` over_cap_ok.

## What stays the same
Script gate, one plan + one approval, storyboard before video spend, one test clip, free fixes first, AI finish, QC
templates. Grace's voice: `grace/voice/README.md`.
