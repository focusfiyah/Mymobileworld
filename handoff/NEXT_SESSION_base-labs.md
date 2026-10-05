# Handoff: Grace's Base Laboratories ads (paste this into a new Claude Code session on focusfiyah/Mymobileworld)

Continue Grace's Base Laboratories job. Read `CLAUDE.md`, `grace/PLAYBOOK.md`, then `ugc/base-labs/pads/README.md` and
`ugc/base-labs/oil/README.md` (Status lines). Work on branch `ccr-358dbefe-cadn5u` (not merged to main yet).

## Where it stands (2026-10-05)
- Request: ONE video per product (Ingrown Hair Pads + Ingrown Hair Oil), silent hands-only AI video, Grace records her own
  voiceover; 3 script options per product. Done and approved.
- Finals: `ugc/base-labs/pads/out/pads.mp4` (29.2s) and `ugc/base-labs/oil/out/oil.mp4` (31.2s). NO text on screen.
  How-to beat = shaved underarm + leg (Grace's request; forearm removed). Real-packshot pop-up on the label shot.
- Drive: Grace Tiktok assets / "Base Laboratories pads + oil ads (2026-10-04)" (folder 1bumoJ0pTLyPnfDB2DT0P6gM-6IAK-B_P):
  "Ingrown Hair Pads video (no text).mp4" (1I3Y484bo5BCCLkmO_5Nv9xbeYGvGKQqR), "Ingrown Hair Oil video (no text).mp4"
  (1LJa27_T4K_czY6807_0IptnKw1Oe8tPO), scripts doc (1-ebEfmtZh2LxytSVGoBKnVjOZI9f4YWkCJnfxEUJUnQ). Every older version is in
  subfolder "Older versions (do not post)" (1RtPzX2DzLEH4yra-CYXFy6l_lmM_L34c).
- Spend: Kie $5.867 total vs $3.46 first quote (Seedance rerolls + Grace's underarm/leg change, each approved). ElevenLabs $0.
- Rebuild (free): `cd ugc/base-labs && python3 cut.py pads` / `python3 cut.py oil`. Clip windows are in cut.py
  (pads leg clip S4b uses only its clean first 2.0s; the pain beat uses the clean first 0.9s/2.3s of the two steam clips).

## Open items
1. When Grace sends her recorded voiceover: retime each cut to her words (free; never stretch clips, no freezes, no text).
   If her read runs longer than the picture, ask Ralph before any new clip (~$0.164 per 4s clip).
2. The scripts doc still labels each option's line as "On-screen hook text": those are OPTIONAL lines for Grace to type
   in TikTok herself, never burned into the video. Relabel if Ralph wants (free).
3. Ralph still to do: paste `handoff/REMEMBER_ME_paste.txt` into a new claude.ai chat; upload
   `handoff/ugc-product-ad-skill.zip` to claude.ai (both sent to him 2026-10-05).

## Rules that bit this job (now in PLAYBOOK/skill/CLAUDE.md)
- NO text in videos unless Ralph asks in that job; `grace/gate.py --stage cut` blocks cut scripts that draw text.
- Ask before every paid call with the exact cost; still storyboard before clips; one test clip first; report running total.
- Removed items: see each job's REMOVED.md (forearm shot, burned-in hook text, A/B/C text versions).
