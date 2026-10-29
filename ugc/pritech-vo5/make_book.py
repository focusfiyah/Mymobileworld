"""Writes BOOK.md (the one plan message) from shots.json + the short shot notes below. python3 make_book.py"""
import json, subprocess

S = json.load(open("shots.json"))
VO = " ".join(json.load(open("vo/vo_lines.json"))["lines"])
WHAT = {
 "V5S1": "Hand brings the wet brush toward the lens, bristle face to camera", "V5S2": "Just-washed palms up, beige makeup + oily shine still on the fingertips",
 "V5S3": "Crumpled used towel with makeup marks over the tub rim, push-in", "V5S4": "Thumb presses into the nubs, they bend and spring back",
 "V5S5": "Bristle head touches the water in the stone bowl: fast rings spread", "V5S6": "Silver end on the inside of her wrist (testing the warmth)",
 "V5S7": "Steamy tub under the mint niche of rolled towels + plant, push-in", "V5S8": "Brush circles on her foamy cheek (cheek only), sage headband",
 "V5S9": "END: one brush on the wooden vanity by the stone basin, low push-in",
 "V6S1": "Brush across the sink edge, tap running, low dolly in", "V6S2": "Fingertips rub an oily post-gym cheek, come away shiny",
 "V6S3": "Grey gym towel rubbed on her cheek", "V6S4": "Bristles sweep across the back of her other hand, nubs bend",
 "V6S5": "Bristles pressed into her open palm: the palm skin jiggles", "V6S6": "Silver end glides down the side of her neck",
 "V6S7": "Eucalyptus bundle on the shower head over the tub, push-in", "V6S8": "Hand lowers the wet brush into its stand (PRITECH on the stand)",
 "V6S9": "END: brush in the side pocket of a plain grey gym bag, push-in",
 "V7S1": "Hand picks the brush up off the bulb-mirror makeup table", "V7S2": "Fingertip swipes her cheek after a hand wash: beige foundation on it",
 "V7S3": "Hand pulls a makeup-marked towel off its hook to reuse it", "V7S4": "Brush on a fluffy white towel, camera arcs to the bristle face",
 "V7S5": "Brush switched on, on a mirrored tray: water drops jump around it", "V7S6": "Thumb presses the °C button, silver end below the hand",
 "V7S7": "Hands tie the belt of a white satin robe (no face)", "V7S8": "Bristles patted dry on a folded white cloth",
 "V7S9": "END: brush in its stand on the bulb-mirror vanity, push-in",
 "V8S1": "Hand pulls the brush out of a grey toiletry pouch in a hotel bathroom", "V8S2": "Hands lather hotel soap, beige makeup streaks stay on the fingers",
 "V8S3": "Damp used hand towel limp on a chrome hotel bar, tilt down", "V8S4": "Bristle head lifted out of a basin of water, nubs dripping",
 "V8S5": "Thumb presses ((•)) over the basin: droplets spray off the nubs", "V8S6": "Brush on the freestanding tub rim, slow slide to the silver end",
 "V8S7": "Robe + slippers on a stool by the freestanding tub, push-in", "V8S8": "Hand slides the brush into the toiletry pouch (packed every trip)",
 "V8S9": "END: brush in its stand on the hotel counter by a plain key card",
 "V9S1": "Top-down: brush on the square basin rim, camera descends", "V9S2": "Window light macro: thumb rubs oily, makeup-tinted fingertips",
 "V9S3": "Hands wring out a makeup-marked face cloth over the basin", "V9S4": "Macro slide across the nubs, brush on a wooden tub caddy",
 "V9S5": "Bristle head in a dish of cleanser foam: the foam jiggles", "V9S6": "Silver end glides along her jaw toward the ear",
 "V9S7": "Knit blanket + book on a bench by the big window, dolly", "V9S8": "Thumb presses the O button, hand lifts the brush out of frame",
 "V9S9": "END: one brush on the wooden windowsill, push-in",
}
THEME = {"V5": "Fresh mint morning. Rooms V5A mint tile + wood stool vanity + stone bowl basin, V5B mint mosaic niche + tub. Sage towel headband, white tee. Bright neutral daylight.",
         "V6": "After the gym, oily skin. Rooms V6A oxblood red tile + white tub, V6B teal-blue tile bath. Grey sports tank, ponytail. Bright cool daylight.",
         "V7": "Makeup off at the vanity. Rooms V7A pink terracotta tile + leaf print, V7B bulb-mirror makeup vanity. White satin robe. Bright even vanity light.",
         "V8": "Travel / hotel. Rooms V8A navy tile hotel bath, V8B wood-plank wall + freestanding tub. White waffle robe. Bright neutral hotel light.",
         "V9": "Self-care Sunday. Rooms V9A green tile + square basin + pink floor, V9B wood cabin bath + big window. Cream knit sweater, claw clip. Bright soft window light."}
assert set(WHAT) == {x["id"] for x in S}
n_still, n_omni, n_seed = len(S), sum(x["product"] for x in S), sum(not x["product"] for x in S)
c_still, c_omni, c_seed, redo = n_still * 0.09, n_omni * 0.315, n_seed * 0.164, 0.09 + 0.315
total = round(c_still + c_omni + c_seed + redo, 2); flow_total = round(c_still + c_seed + redo, 2)
spend = subprocess.run(["python3", "grace/spend.py"], cwd="../..", capture_output=True, text=True).stdout.strip().splitlines()[-2]

L = [f"# Production Book: PRITECH Heated Face Scrubber, black, 5 videos V5-V9 on Grace's VO (Grace), 2026-10-29", "",
     "Sent to Ralph: https://claude.ai/artifact/V7f83RDGV3AqyAMYNQXDbt (2026-10-29, plan v1: 45 shots, Kie Omni or Flow)", "",
     "## 1. Job",
     "- Client: Grace  Product: PRITECH heatable vibrating face scrubber, BLACK (BCM-1485), same as V1-V4  Route: hands + hand-free AI over Grace's OWN voiceover from her post https://www.tiktok.com/t/ZPLDRXhd4, no full face, product lock = Omni 1.1 Flash (Flow first or Kie Omni, your pick)",
     f"- Job folder: `ugc/pritech-vo5/`  Length: 20.9 s each (the VO)  Shots: {n_still} (9 per video, 17 HAND-FREE)",
     "- Reused for $0: product sheet (real photos only), real close-ups (bristle head, buttons, silver end, PRITECH on the stand), Grace's hand sheet without bracelet, all research. NOT reused: any V1-V4 footage, room or shot idea (Grace's own post already re-uses our V1-V4 clips).", "",
     "## 2. Gate result (`python3 grace/gate.py ugc/pritech-vo5`): GATE OK",
     "| Proof | File | Result |", "|---|---|---|",
     "| Playbook rules read | research/playbook.md | OK |",
     "| Coach research | research/coach.md (+ the linked post: 51 views at 10 h, save rate 3.9%) | OK |",
     "| Daily viral board | research/viral/viral-2026-10-29.json (today, 55 shop videos) | OK |",
     "| Product facts | research/product_facts.md (2026-10-29 table) | 5 of 6 VO claims backed; 1 flagged (below) |",
     "| Audience | research/audience.md | OK (from V1) |",
     "| Hooks | research/hooks.md (spoken hook fixed; 3 on-screen options per video for the House of Rameau versions) | OK |",
     "| Humanizer | research/humanizer.md, captions.md | VO verbatim; captions humanized |",
     "| Readability | research/readability_v5..v9.txt | 7.1, OVERRIDE recorded: your words \"Use the VO from the link\" |",
     "| Banned phrases | gate.py | OK |", "",
     "## 3. Script (Grace's own VO, word for word, same audio in all 5)",
     f"> {VO}", "",
     "Flag (not edited, it is her audio): \"towels just transfer bacteria right back into your skin\" is not on the listing or box; it is her opinion line. I show it as a used towel only, never germs.",
     "VO: her audio as posted, -16.7 LUFS, echo 150 ms (passes <= 150), no music under it. 0 ElevenLabs characters.", "",
     "## 4. Shot list (9 beats, same timing in every video; every shot idea used once across V5-V9)",
     "Columns: shot | VO words | on screen | HAND? | clip | room. Every shot moves; no text; the brush never glows; heat shots show the silver end; cheek/jaw/neck crops only, never eyes or mouth.", ""]
for v in ["V5", "V6", "V7", "V8", "V9"]:
    L += [f"**{v}** ({THEME[v]})", "", "| # | VO words | On screen | HAND? | Clip | Room |", "|---|---|---|---|---|---|"]
    for x in [s for s in S if s["video"] == v]:
        clip = "Omni $0.315 / Flow $0" if x["product"] else "Seedance $0.164"
        L.append(f"| {x['id'][2:]} | \"{x['line']}\" | {WHAT[x['id']]} | {'HAND' if x['hand'] else 'HAND-FREE'} | {clip} | {x['room']} |")
    L.append("")
L += ["Hand: Grace's sheet WITHOUT the bracelet (as V1-V4): medium-brown skin, short squared French tips, silver crown ring stack, small gold heart ring, blue thumb band, bare wrist.",
      "Real product (product_truth.json): slim matte black curved wand ~15-16 cm, oval head of black nubs, 3 moulded buttons ((•)) / O / °C, short silver chrome end flush with the handle, black stand with grey PRITECH. No print on the handle, no glow.",
      "Rooms: 10 new real Pexels/Pixabay photos, none used in V1-V4 (rooms/SOURCES.md, contact sheet on the review page).", "",
      "## 5. Order of work and time",
      "1. All 45 stills at once (~8 min) -> still storyboard on the review page (your stop 1). Riskiest first: V5 S8 (brush on a foamy cheek, Kie once refused a foamy-cheek still).",
      "2. One test clip: V5 S8, with the 15 Seedance no-product clips alongside (~6 min).",
      "3. After the test passes QC: the other 29 product clips at once (Kie ~8 min, or your Flow takes).",
      "4. 5 cuts on Grace's VO, QC (2x edges, first second, REMOVED.md, verify_fix), compare vs @joshjshowcase 2.7M, AI finish -> review page (your stop 2) -> Drive.",
      "Machine time ~40 min for the first video + ~10 min for each of the other four (they run side by side) = about 1.5 hours, plus your two review stops.",
      "House of Rameau: 5 HofR versions (own order/framing, on-screen hook text from research/hooks.md, no captions) cut free after you approve Grace's; posting each only on your OK.", "",
      "## 6. Cost (one total)", "| Item | Qty x unit | $ |", "|---|---|---|",
      f"| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | {n_still} x $0.09 | {c_still:.2f} |",
      f"| No-product clips, Seedance 2.0 Mini on Kie, 4 s | {n_seed} x $0.164 | {c_seed:.2f} |",
      f"| Product clips, Omni 1.1 Flash on Kie, 4 s | {n_omni} x $0.315 | {c_omni:.2f} |",
      f"| One likely redo (a still + an Omni clip), asked before it runs | $0.09 + $0.315 | {redo:.3f} |",
      f"Flow instead of Kie Omni for the {n_omni} product clips: {n_omni * 12} of your Flow credits (12 each; October's credits end in 2 days, they do not roll over), Kie total then ${flow_total:.2f}.",
      "VO: $0 (Grace's audio). ElevenLabs: 0 chars.",
      f"Month so far (`python3 grace/spend.py`): {spend}", "",
      f"TOTAL: ${total:.2f}", "",
      "## 7. Questions",
      f"1. Product clips: Kie Omni (${c_omni:.2f}, in the TOTAL) or your Flow app ({n_omni} takes, ${flow_total:.2f} total)?",
      "2. Is this VO Grace's own voice (not our clone)? If yes I add it to her clone samples ($0).",
      "3. Grace's post has on-screen hook text; hers stay text-free unless you say yes (HofR versions get the text either way).", "",
      "## 8. Prompts (final, written with prompt-master after loading it; every reference named; linted PROMPT_LINT_OK)",
      "| Item | Model | Prompt file / text |", "|---|---|---|",
      f"| {n_still} stills | Kie nano-banana-pro (Gemini 3 Pro Image), 9:16 1K | shots.json `still` (exact text sent) + `still_refs` (sheet, close-ups that frame shows, room, hand sheet) |",
      f"| {n_omni} product clips | Omni 1.1 Flash (Kie omni_clip.py or Flow kit), 4 s | shots.json `clip`, image 1 = approved still, then the real close-ups, last = sheet |",
      f"| {n_seed} no-product clips | Kie Seedance 2.0 Mini, reference mode, 4 s | shots.json `clip` + `clip_refs` (still, hand sheet when a hand shows); \"no brush, no product appears\" |",
      "Generator: make_shots.py (shared product/hand blocks copied from V2-V4's approved prompts)."]
open("BOOK.md", "w").write("\n".join(L) + "\n")
print("TOTAL", total, "flow", flow_total)
