# Ralph AI consultant site (2026-10-28)

Status: v2 preview sent 2026-10-28 (Ralph: clips only from videos that sold incl. flashlight + castor oil; YouTube = the new-look thumbnails). All automatic checks pass; waiting on his OK to go live. Cost $0.

- Site source: repo focusfiyah/focusfiyah.github.io (`index.html`, `media/`, `PRODUCT.md`), live address https://focusfiyah.github.io once pushed to main (GitHub Pages, free). Custom domain later (Ralph).
- Review page: https://claude.ai/artifact/RA6YtvCKGPqkztYQuNWtmg (v1 = 3 mockups, v2 = full page preview).
- Ralph's answers: show all 4 kinds of work, clients anonymous, free GitHub address, contact form only (to life22watch@gmail.com), name "Ralph, AI Consultant", no prices (free consult), bright and clean, no numbers yet, photo later, plain HTML/CSS; after two re-rolls asked for personal + premium, picked C (studio reel) from mockups.
- Clips: `clips.py` cuts single-shot muted loops from approved Grace ads (no client names, no voices). Day One thumbnails from Dayone-ai jobs (videos public, checked by API 2026-10-28).
- Form: FormSubmit (free, no account). First message triggers an activation email to life22watch@gmail.com that Ralph must click once. After activation, swap the address in index.html for the random alias FormSubmit gives (keeps the email out of the page source).
- Checks: `python3 verify.py all` (render, hero, privacy, media, copy, motion, detect, form), `verify.py shots`, `verify.py live`. Ledger: GATES.md. Humanizer proof: proof/humanizer.md.
