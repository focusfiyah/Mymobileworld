# GPT Image 2 test (2026-10-26)

Status: test still run, see RESULTS below. Cost quoted $0.05 (Kie 2K still).

Why: Sabrina Ramonov's /generate email (2026-08-19) routes any frame with readable text or an app screen to Kie's
`gpt-image-2-text-to-image`. Test: can it render a Day One AI phone screen with small text spelled exactly, for the
"POV: you wake up and..." Short format (Dayone-ai `formats/shorts.md`)?

Ralph's OK (2026-10-26): "Build 1 and 2 and run the test and add the two day one short formats", after the quote
"A one-still test would cost about $0.05, and I'd ask first."

Not a Grace script job, so grace/gate.py's script gate and BOOK do not apply; run.py still runs the Kie field check,
the prompt check (prompt.txt linted + marked), the monthly cap and the paid-task ledger (grace/paid.py) before Kie is
asked, and logs to kie_log.json so grace/spend.py counts it.

## Results (2026-10-26)

- Task a2b0e2bf703f8ef0147044d5b1bf393d, billed 10 credits = **$0.05** (Kie balance 712.2 -> 702.2), ~1 min.
- `still.png` 1440x2560 (9:16 at 2K). Previews: `preview_half.jpg`, `zoom_screen.png` (2x), `zoom_hand.png`.
- Screen text, all 5 items spelled exactly as asked and sharp at 2x, including the smallest line: icon with no letters,
  "Day One AI", "Tutorial ready: 2:31", "Thumbnail done", "Saved as a private draft". No stray text elsewhere.
- POV holds: right hand from the right frame edge, wrist runs off-frame, five fingers, phone off to one side (not
  overhead), window on the left as asked, bright neutral light. 2x edge check on the hand: no halo or smear.
- Verdict: use `gpt-image-2-text-to-image` (2K, $0.05) for Day One stills where a phone/app screen or card text must be
  readable (POV Short format, listicle cards). Grace's real-app screens stay tracked on from real captures
  (`screen_track.py`); product stills stay on the product-lock routes.
