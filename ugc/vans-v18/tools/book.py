"""Writes BOOK.md (the one plan, grace/gate.py) for Vans V18-V37 from shots.json + scripts.md. python3 tools/book.py"""
import json, re
from pathlib import Path

J = Path(__file__).resolve().parent.parent
S = json.loads((J / "shots.json").read_text())
CAP = dict(re.findall(r"## (V\d\d)\n(.+)", (J / "scripts.md").read_text()))
SHORT = {"1a": "hand lifts the held shoe over her legs, side tab", "1b": "held shoe top view, laces", "1c": "held shoe tilted, red insole",
         "1d": "feet crossed on the ground, foot bounce", "1e": "one shoe on the ground, push-in",
         "2a": "finger taps the side tab on her worn shoe", "2b": "heel lift shows the gum sole", "2c": "seated wide, toes tap together",
         "2d": "hand pulls the worn shoe's bow tight", "2e": "the pair side by side, dolly in",
         "3a": "held shoe in front of the dash, side tab", "3b": "held shoe toe at the lens", "3c": "held shoe back view, heel label",
         "3d": "feet up on the dash, crossed, sway", "3e": "one shoe on the cream seat, push-in",
         "4a": "held shoe over the coffee table, side tab", "4b": "sequin macro slide", "4c": "held shoe tilted, red insole",
         "4d": "one shoe on the table by the mug, push-in", "4e": "feet by the table, ankle cross",
         "5a": "held shoe beside her worn foot on the door sill", "5b": "held shoe insole over the sill", "5c": "held shoe top view over her foot",
         "5d": "both feet on the sill, toe tap", "5e": "she steps out onto the sidewalk",
         "6a": "legs swing out of the car, feet land", "6b": "held shoe against the door panel", "6c": "walks toward the camera",
         "6d": "held shoe sole to the lens, gum waffle", "6e": "standing by the car, heel lift"}
PLACE = {"street": "cafe sidewalk", "bedroom": "Grace's saved cream bedroom", "car": "car interior (cream seats)",
         "living": "bright living room, coffee table", "curb": "car door open onto the cafe sidewalk"}
LINK = {"1": "Link 1", "2": "Link 2", "3": "Link 3", "4": "Link 4", "5": "Link 5", "6": "Link 6"}

N = len(S); STILL, CLIP = 0.09, 0.164
redo_s, redo_c = round(N * 0.2), round(N * 0.2)
tot = round(N * STILL + N * CLIP + redo_s * STILL + redo_c * CLIP, 2)

rows = []
for k, s in S.items():
    rows.append(f"| {k} | {s['window'][0]:.1f}-{s['window'][1]:.1f} | {SHORT[s['beat']]} (beat {s['beat']}) | {s['kind']} | {PLACE[s['place']]} | none | no face | music only |")
vids = []
for v in sorted({s["video"] for s in S.values()}):
    ss = [s for s in S.values() if s["video"] == v]
    links = sorted({LINK[s["beat"][0]] for s in ss})
    vids.append(f"- {v}: {', '.join(links)} | {PLACE[ss[0]['place']]} | caption: {CAP[v]}")

book = f"""# Production Book: Vans sequin V18-V37, 20 music-only videos (Grace), 2026-11-11

Sent to Ralph: https://claude.ai/artifact/Hvvw2NxP4JCwL7bVLFidvT, 2026-11-11

## 1. Job
- Client: Grace  Product: Vans Premium Authentic low top, sequin checkerboard (same shoe as V1-V17)  Route: hands + feet AI from stills (Gemini 3 Pro Image on Kie) + Seedance 2.0 Mini first-frame clips on Kie (Ralph tapped "Seedance Mini, ~$30.50 (Recommended)" 2026-11-11, as V13-V17), `.claude/skills/ugc-product-ad`
- Job folder: `ugc/vans-v18/`  Length: 16 s each  Shots: 5 per video (3.2 s), {N} in all ({sum(s['kind']=='HAND-FREE' for s in S.values())} hand-free)
- Ask (Ralph 2026-11-11): about 20 videos of the Vans, 3 from each of the 6 links Grace sent, matching the scenes; made on Kie; 16 s. Answers he tapped: sequin shoe, 20 videos (18 + 2 that mix the best beats), music only, same beats new look, Kie for all and OK over the cap, free music he can swap in TikTok. Hypit: breakdown only (Ralph tapped "Breakdown only, Kie makes it").
- Links: 1 https://www.tiktok.com/t/ZPLnjUU3p/ (V18-V20) · 2 https://www.tiktok.com/t/ZPLnjhxGh/ (V21-V23) · 3 https://www.tiktok.com/t/ZPLnj2pMc/ (V24-V26) · 4 https://www.tiktok.com/t/ZPLnjFctx/ (V27-V29) · 5 https://www.tiktok.com/t/ZPLnjkDyF/ (V30-V32) · 6 https://www.tiktok.com/t/ZPLn2wKg5/ (V33-V35) · mixes V36 (Links 6+5+3), V37 (Links 2+4+1)

## 2. Gate result (`python3 grace/gate.py ugc/vans-v18`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (ref video x6 + tag) | proof/coach_research.md | OK: top ref 367.8K views (Link 6); today's tag/viral pages returned 0 (TikTok captcha), Oct 29 tag data stands |
| Daily viral board | research/coach/viral-2026-11-11.json | ran today, 0 videos returned (captcha) |
| Product facts (source) | research/product_facts.md + product_truth.json | OK (Vans' real photos) |
| Hooks modeled on named winners | research/hooks.md | 20 different Grace library hooks, word for word |
| Humanizer | proof/humanizer.md | OK, 3 captions reworded |
| Readability (grade) | proof/readability.txt | 1.8 |
| Banned-phrase check | gate.py | OK |

## 3. Script
Music only: no voice, no on-screen text (Ralph 2026-11-11; Creator Pathway decision 4). The words are the TikTok post captions:
{chr(10).join(vids)}
Source of each line: research/line_sources.md (library hook id + product_truth fact). Music: a free licensed track per video (free-assets: Mixkit/Pixabay), each video its own track; Grace can swap in a trending sound in TikTok.

## 4. Shot list
| # | Window (s) | Shot | Kind | Setting | On screen | Face? | VO or lip sync |
|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}
Outfit: its own per video (tools/make_shots.py OUT, 10 looks rotating, never the same look twice in a link's 3 videos)  Setting: one per video (Grace's one-room rule; saved bedroom reused; car, sidewalk and living room picked today from free real photos, rooms/SOURCES.md)  Nails / person details: Grace's hand reference (pink French tips, silver ring stack, gold trillion ring, gold link bracelet), her skin reference  Real product confirmed: same shoe as V1-V17, product_truth.json (black side tab with white VANS, red insole with white box, checkerboard toe, gum sole)

## 5. Order of work
1. All {N} stills at once (parallel), storyboard on the review page for your look (no clips paid before your OK on the stills).
2. ONE test clip, the riskiest: V30S1 (held shoe beside the worn one in the car door: grip, side tab, which shoe is which).
3. Then all clips at once, cuts, QC (2x edges, drift, flash/levels, REMOVED.md), AI finish, review page.
Free fixes planned: trim each clip to the cleanest 3.2 s window, crop, grade per video (bright neutral), mirror where a frame needs the other side.
Time: stills ~15 min, test clip ~5 min, clips ~20 min, cuts + QC ~40 min (machine time, plus your review stops).

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image (nano-banana-pro 1K) | {N} x $0.09 | {N*STILL:.2f} |
| Clips, Seedance 2.0 Mini 4 s 720p first-frame | {N} x $0.164 | {N*CLIP:.2f} |
| Likely redos (about 20%, from V13-V17's rate), each asked first | {redo_s} stills x $0.09 + {redo_c} clips x $0.164 | {redo_s*STILL + redo_c*CLIP:.2f} |
| Music (free licensed tracks) | 20 x $0 | 0.00 |
Total Kie: ${tot:.2f}  ElevenLabs: 0 chars  Contingency redos: inside the total, each one still asked with its cost
Month so far (`python3 grace/spend.py`): $39.90 of the $100 cap; this job takes it to about ${39.90 + tot:.2f} (you OK'd going over; it stays under)

TOTAL: ${tot:.2f}

**Approve?**

## 7. Questions (all of them, now)
1. Approve the plan and the ${tot:.2f} total? (stills first, then one test clip, then the rest)

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| {N} stills | nano-banana-pro | shots.json "still" + "still_refs" (tools/make_shots.py) |
| {N} clips | bytedance/seedance-2-mini first-frame | prompts/<ID>_sd.txt |
Lint: `python3 grace/prompt_check.py lint ugc/vans-v18/shots.json` = PROMPT_LINT_OK; every prompt read end to end (2 clashes fixed: clip look lines now name only the logos in frame; no "same grip" on the finger-tap shot).
"""
(J / "BOOK.md").write_text(book)
print("BOOK.md TOTAL", tot)
