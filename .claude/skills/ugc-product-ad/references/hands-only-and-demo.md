# Hands-only, on-camera demo and GTT lessons

## Contents

- Hands-only product ad (approved route)
- On-camera demo over a voiceover (approved route)
- Lessons from the GTT KN95 mask ad (Grace, 2026-10-03: 10 shots, $4.38 vs $2.75 first quote)

## Hands-only product ad (approved route)

Proven on Grace's Carpe Vanilla Peach tips ad (2026-10-01, `focusfiyah/Mymobileworld` → `ugc/carpe-vanilla-peach/`,
the best template: README, shots.json, kie.py, cut.py). One hand (reference sheet) is the only character; the
voiceover is a separate ElevenLabs track, so no lip sync and no on-camera speech.

**The hand does not need to be in every shot (Ralph 2026-10-04):** "hands-only" means no face, not a hand in every frame.
Plan hand-free shots (product alone, setting, props) where they fit; they still move (camera move or product clip) and their
prompts carry no hand text.

1. **Research + script + voiceover first (free/cheap).** Pick the format from real data (tiktok-shop-coach skill),
   write to the client's rules, record the VO (eleven_v4), get word timings with scribe_v2, and cut a free timing
   animatic. Shot windows come from the word timings.
2. **Before the first paid still, ask:** product top/cap/label from a real photo, nail length/hand details, client.
3. **Still S1 first** (Nano Banana Pro on Kie, 1K 9:16, $0.09 = 18 credits): refs = hand crops + product crops.
   Show it, wait. S1 then doubles as the room reference for every later still (room continuity worked).
4. **Remaining stills on one sheet**, ask first ($0.09 each). Pin product shape in close-ups ("the same tall
   oval stick as in every other shot, not a short round jar"): macro prompts drift the shape.
5. **Hardest clip first** (Seedance 2.0 Mini, `first_frame_url` = the still, `generate_audio: false`, 720p 9:16,
   $0.041/s = 8.2 credits/s), then the rest in parallel. Clip length ≥ its VO window.
6. **Free cut** (`scripts/hands_cut.py`): trim each clip to its window (start offset when the action comes late,
   e.g. a cap tap), badge close-up insert cropped from a still over the claim words, CC0 SFX (knob ticks, cap tap)
   placed from timestamped frames (`drawtext=text='%{pts\:flt}'`), loudnorm -16 LUFS, 720x1280.

Kie runner (`scripts/kie_hands_runner.py`): balance check is free (`GET https://api.kie.ai/api/v1/chat/credit`,
1 credit = $0.005); it logs every taskId at submit (a killed run's result can be fetched with recordInfo), renders
clips in parallel threads with a locked log, and builds one preview sheet. Kie latency was 3-8 min per still:
run in the background with a ≥1h timeout, never a 10-min foreground call (one run was killed mid-task).
Traps: a nano-banana-pro *edit* barely changes small details (nails: first edit ~no change); a blur on the still
carries into the Seedance clip (good for a wrong label line); small label text comes out garbled or wrong
("1.7 FL OZ (350 mL)") → blur it on the still, free.
Seedance turns a hand-held box to show its side panel mid-clip even with "the box stays upright with its front
facing the camera" in the prompt (Vicks S1, at ~2s): use the clip's front-facing start + a push-in hold on its last
good frame, or another take of the shot if one exists. It also redraws scenes late in a clip (stray hands walked in
at 2.2s in a no-hand shot): plan each window from the clip's first ~2s.

## On-camera demo over a voiceover (approved route)

Proven on Grace's Carpe Mountain Breeze ad (2026-10-01, `focusfiyah/Mymobileworld` → `ugc/carpe-mountain-breeze/`:
README, shots.json, kie.py, lipsync.py, cut.py; copies in `scripts/persona_*.py`, rename to kie.py / lipsync.py /
cut.py in the job folder). The person is an AI version of a real client from ONE photo; the voice is a separate
ElevenLabs track. Structure Ralph asked for: curiosity-loop hook → pain → selling point / solution → urgency CTA
(real reason, no false scarcity). Final: 35s, 9 shots, $6.60, of which ~$3.20 was footage that made the cut.

1. **Lock everything first** (see "Working with Ralph"): script, VO, shots, outfit, setting, which shots show the
   face, which face shots get lip sync, cost. Then record the VO (eleven_v4), STT word timings (scribe_v2), trim
   pauses to 0.25s (free; 38.6s → 35.0s) and set shot windows from the words.
2. **Stills** (Nano Banana Pro on Kie, $0.09): refs = person photo + product crops; the first approved still is the
   room/person reference for the rest. Relaxed brows in every prompt (raised brows = forehead wrinkles the clip
   copies). Outfit change later = an edit of the approved still, "change ONLY her top to the one in image 2"
   ($0.09, keeps the pose; `kie.py tee`).
3. **One test clip** (Seedance 2.0 Mini, $0.041/s), check it, then the rest one by one or in a small batch. Clip
   length ≥ its VO window: never stretch footage in the edit (Ralph: "why is the whole video in slow motion"), and
   Seedance already moves slowly. A pull-back from a close-up = `first_frame_url` (close-up) + `last_frame_url`.
4. **Lip sync the face shots** (`lipsync.py`, Kie `volcengine/video-to-video-lip-sync`, lite, $0.04/s of audio,
   one at a time: parallel calls get "server busy", $0). Mix the ORIGINAL voiceover, not the lip-sync audio.
5. **Cut** (`cut.py`, an edit list of clip pieces, free): whip-pan = xfade slideleft 0.24s + dblur + a noise
   whoosh; CC0 SFX; loudnorm -16 LUFS. QC (see above) before sending.

Traps, each paid for once:
- **The prompt TEXT beats the first frame.** Stills were edited to a grey tee but the identity text still said
  "sky-blue tank top": all 8 clips came back in the tank ($1.52). Grep every prompt block for the old look.
- **A product description in the prompt puts the product in the shot.** "No deodorant in this shot" lost to the
  identity block's stick description ($0.41). For product-free shots, drop the product text (`no_product` in shots.json).
- **A clean first frame does not survive a busy prompt either:** Seedance added a giant stick in the foreground of a
  "dry shirt" shot. Fix in text, not with a reroll.
- **Voiceover + face on camera reads as "her lips aren't moving".** Ralph rejected chin-down crops (they cut the
  product off) and chose lip sync.
- **Lip sync smears whatever passes the mouth** (the stick as she lowers it: flattened top, skin-coloured blob) and
  runs ~2 frames late. Fix free: keep the lip-synced mouth in a soft oval over the original frames (shifted 2
  frames), or jump-cut past the crossing and lip-sync only the clean part ($0.04). Swapping whole frames to the
  original makes the mouth stop mid-word, which Ralph spotted.
- **Free fixes that worked:** shallow-focus background blur on a still with normalized convolution (no orange halo
  around the product); blue→grey recolor with the label protected by a mask; chin-down crops for demo shots; skin-only
  bilateral smoothing for forehead lines; mirrored punch-in jump cut to fill a short clip.
- **Label text garbles at small sizes**; the logo and colour panel read. Use the real packshot or a sharp close-up still
  for label moments.

## Lessons from the GTT KN95 mask ad (Grace, 2026-10-03: 10 shots, $4.38 vs $2.75 first quote)
Match every shot to the exact words it sits on (one clip per phrase, windows from the word timings). Quote redos before paying.
- **Hands grip.** Any item a hand touches is pinched by its edge, fingers curled, never a flat palm (a rug stuck to the palm, masks
  under a palm and a box under a flat hand all got rejected). Write "pinches X between thumb and finger by its top edge, NOT lying
  flat" in the still AND the clip prompt; the clip must show the hand holding the item through the whole move.
- **Product drift on simple products too.** With the listing's box-and-product picture as the ref, Nano Banana Pro drew a generic
  flat-fold mask and the wrong box colour (the white-mask box is blue). Fix: a tight crop of the real item alone as the ref
  (`refs/ref_mask_only.png`) + exact shape/colour text with "NOT ..." clauses; drop the box from shots that do not need it.
- **Wrong-way motion is a free fix:** use the half of the clip that moves the right way, or reverse the wrong half. Min clip is 4s:
  for 1-1.5s windows use the first ~1.5s or an offset where the action happens; fill long windows with a push-in hold on a clean frame.
- **A face shot of AI Grace** (from her photos) changed her hair colour and drew the wrong mask: dropped. Build a proper reference
  sheet first (`grace/ref/grace_reference_sheet.png`). A mask over the mouth means no lip sync is needed.
- **Script:** plain words, no "the box says", CTA that sells more units ("Grab a couple boxes, so there's always one close"), never
  "plenty to share". Health-adjacent products: the listing's own pitch only (dust/outdoor), no illness/N95/FDA/layer-count lines.
- **Pace of a job:** ~25 review messages on this ad. Ask Ralph's four questions (angle, product facts conflicts, image model, hands)
  and show the matched shot list in the FIRST plan message so edits happen before spend.
