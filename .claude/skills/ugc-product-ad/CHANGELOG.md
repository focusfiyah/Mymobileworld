# Changelog

- 2026-10-22 (Ralph, ideas from Video Factory): plan template is now the Production Book (BOOK.md, TOTAL line, prompts section) that grace/gate.py requires Ralph's recorded OK on; budget lock; omni_clip.py saves each paid task before createTask (paid-task ledger); scripts/gate.py is now a pointer to grace/gate.py (the drifted copy let older runners skip the monthly cap).
- 2026-10-21 (Ralph): no Kling on any job unless he says so; every clip Seedance 2.0 Mini on Kie, hand-free prompts say no hand appears.
- 2026-10-13 (skill-smith audit): script-gate paragraph and unlazy paragraph shortened to one-line summaries tagged with their homes (PLAYBOOK §4, CLAUDE.md).
- 2026-10-19 (Ralph): product reference sheet first; no pasted labels, product clips from reference images (Seedance reference mode, Kling hand-free) after LGXNDS v5. Ported from the Mymobileworld deployment copy.
- 2026-10-13 (Ralph: "slim"): "Working with Ralph" now points to Mymobileworld CLAUDE.md for the general rules (cost asks, plan, test clip, notifications, Drive, text, overlays, unlazy) and keeps only the ad-specific lessons, each with its reason.
- 2026-10-18 (Ralph): shot-mix rule (mark each shot HAND / HAND-FREE, a third to half hand-free) and Kling-first for hand-free dollies, in references/hands-only-and-demo.md.
- 2026-10-18 (Ralph): review-point rule now says email AND phone push (PushNotification is deferred; ToolSearch first).
- 2026-10-18 (Ralph): push is skipped while he has the app open; email is the backup.
- 2026-10-14: grip check on every still before its clip (Throw Hands S5/S7 no-grip stills cost clips + a rejected cut).
- 2026-10-14: end shot shows one product, VO still sells more than one (Ralph).
- 2026-10-19: product-truth lesson from the Shnuggle slideshow test (real dimensions + size anchor, details confirmed by Ralph, free route first, quotes include one redo); details in grace/PLAYBOOK.md §6.
- 2026-10-20 (Ralph: one Grace voice): skit-ads.md points to Mymobileworld grace/voice/README.md for Grace's clone (the old Seedance clone 3dmag... no longer exists on the account, tested 400); script notes say 'Grace voiceover', not Grace B (deleted).
- 2026-10-21 (Ralph): product lock on every product: Gemini Omni clips via scripts/omni_clip.py (references/product-lock.md), paste-back last resort, prompt-master on every prompt, monthly budget line (grace/spend.py) and cap guard in grace/gate.py; OpenMontage paths point at the cloud copy (no PC). Why: October Kie spend ~$144, mostly redos after product drift (Vans, Cleanwaste).
- 2026-10-21 (Ralph): caps per month: none in October 2026, $100/month from November.
- 2026-10-22 (Ralph: "Use Omni on kie not thru the API key"): omni_clip.py now calls Kie google/gemini-omni-flash-1-1 (reference mode, 4 s $0.315, edit $0.84), logs to kie_log.json; product-lock.md updated.
