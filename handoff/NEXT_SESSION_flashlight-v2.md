# Next session: Power Bank Flashlight V2 (Grace), continue from stills

Session title: "Power Bank Flashlight V2 (TINEKO clip-on COB)". Job folder: `ugc/powerbank-flashlight-v2/` (README Status
line, GATES.md, research/, refs/real/, gemini_app/). Previous session: session_016BcMws1uo5YZ5j7HuqwFRK (2026-10-22).

## Locked with Ralph (do not re-ask)
- Ralph's script WORD FOR WORD (research/script.txt; "flashing" -> "flickering" was his fix). No on-screen text.
  McDonald's/Happy Meal spoken only, never shown. Flicker = the FRONT lens, side panel off.
- His storyboard image = shot guide only. 9 shots (review/storyboard.html, https://claude.ai/artifact/JxLUGnQXuDX8uwAivktZSf):
  S1 hand holds it up (clip visible) / S2 charging a phone (cap pulled out, USB-A) / S3 hanging in tent / S4 POV beam down
  a trail / S5 front lens flashing on a rock / S6 clipped on backpack at camp / S7 hand puts it in an emergency pouch /
  S8 hand stands it on the picnic table (clip on top) / S9 hand clips it to a backpack strap. One blue-hour campsite,
  bright and neutral. Storyboard approved ("Let's go with Gemini", GATES G4).
- THE REAL PRODUCT = Ralph's photos of Grace's unit (refs/real/*.jpg; sheet refs/product_sheet_real.png):
  light blue-grey matte plastic body; from the clip: light blue-grey plastic carabiner with silver wire gate, frosted
  pale light panel, square orange button with a POWER symbol, dark grey brushed-metal end cap (~1/4 length) printed
  with a white shark logo + SMILING SHARK, lens at its tip = rounded-square dark bezel, clear domed zoom lens, small
  square LED chip (no silver reflector). Ports under the end cap (pull it off: USB-C front, USB-A back). Box (Grace):
  29.5 x 29.5 x 157 mm with clip, 90 g, 18650, Type-C, modes flashlight / flashing ("explodes") / side light.
  Listing renders and Ralph's old AI sheet are WRONG (REMOVED.md). Last week's approved video used the wrong layout:
  told Ralph, not redoing it.
- Grace's hand: grace/ref/hand-sheets/with_bracelet.jpg (French tips, crown ring, gold solitaire, blue band, gold
  watch-link bracelet, pearl chain with leaf charm). Grip on the dark end cap so the button + panel stay visible.

## DONE 2026-10-23: cut r1 approved and in Drive (see the job README). Nothing left.

## Where it stood
- Gates (unlazy): 5 of 10 met (G1 script, G2 size, G3 storyboard, G4 approval, G5 script gate OK).
- Gemini kit (free route): https://claude.ai/artifact/BfZ9vrRMHETzaWSpsAp1rC = gemini_app/ (6 refs ref1..ref6,
  prompt_S1..S9.txt, make_prompts.py B, make_kit.py). Prompt Master "Ralph's stack" style, size block first.
- Ralph 2026-10-22: "I will provide images 1-4, however you will continue the rest thru kie." -> Ralph sends S1-S4
  stills from his Gemini app; S5-S9 stills go on Kie (nano-banana-pro, Gemini 3 Pro Image) with the SAME prompts and
  refs (gemini_app/prompt_S5..S9.txt + the refs each lists).
- Spent so far: $0.

## Next steps
1. Session start: `python3 handoff/branch_sync.py`; Playwright: `bash .claude/hooks/browser_setup.sh` if `import playwright` fails.
2. NEW RULE (main, 2026-10-22): write the plan as `BOOK.md` (`python3 grace/gate.py ugc/powerbank-flashlight-v2 --book-init`,
   template ugc-product-ad/templates/plan-message.md) with ONE `TOTAL:` line, send it, record Ralph's OK
   (`--approve-book "<his words>"`) before ANY paid call. Show `python3 grace/spend.py` beside it.
   Quote to put in the book: S5-S9 stills 5 x $0.09 = $0.45; 9 Omni product-lock clips on Kie 9 x $0.315 = $2.835
   (4 s each; S5 flicker added free in the edit if Omni won't flash); one likely redo each ($0.09 + $0.315);
   TOTAL $3.29 (up to $3.69 with one redo each); ElevenLabs ~450 chars (Grace cloned Rh3oAQMqRVf78UIVpBoQ, echo gate <= 150 ms).
3. Runner: copy ugc/youtheory-collagen/run.py + kie.py (has the start_task/task_submitted ledger wiring) into the job;
   stills = nano-banana-pro with the prompt_Sx.txt text + its refs; clips = omni_clip.py from the approved still +
   ref6 logo close-up + ref1 sheet (+ ref3 lens on S4/S5, ref5 port on S2, ref4 hand on hand shots).
4. QC every still at 2x (size vs hand/phone/strap, clip shows where the top is in frame, button = power symbol below the
   panel, logo letter for letter, grip, rings, edges, no text/brand other than SMILING SHARK) BEFORE any clip; storyboard
   of all 9 stills on the review page; one test clip (riskiest: S4 beam or S5 flashing) before the batch.
5. VO (grace/voice/README.md), cut (reuse ugc/powerbank-flashlight/cut.py), AI finish, gate --stage cut, review page +
   push + email; Drive "Grace Tiktok assets/Power Bank Flashlight (Grace)" (1r_tveoqKXNKBRcBei6G-wSHfIGOFoIW9) as
   "CURRENT - Flashlight V2.mp4" + script doc, older CURRENT files to "Older versions"; merge to main.
