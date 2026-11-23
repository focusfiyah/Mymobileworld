# Report routine (fired by one scheduled trigger (weekly only; daily reports stopped, Ralph 2026-10-10, usage) into this session)

Goal: short notes on what we learned, so Ralph can paste them into a new chat. Free: no Kie or ElevenLabs calls.

## Weekly (Sunday, 9:10pm ET)
1. `git fetch --all -q` in /home/user/Mymobileworld and /home/user/Dayone-ai (add_repo if missing). Read the git logs for the week (Mon–Sun) in both repos, plus any older daily files in `reports/`, and job README `Status:` lines changed this week.
2. Write `reports/YYYY-Wnn-weekly.md` (≤400 words), using the same sections as `2026-W40-weekly.md`:
   per project/client · Skills acquired (table, new ones marked) · Gotchas · Next.
3. Workflow health (Ralph 2026-11-14 weekly audit, "so that tomorrow ... everything is working well"), each with its
   result in a "Health" section: `handoff/branch_sync.py` in every repo (SYNC_OK, no SKILL DRIFT); `tools/skills/account_drift.py` (ACCOUNT_OK, else list the UPLOAD and REMOVE names for Ralph); `tools/media/media.py
   check` (MEDIA_OK); the grace/tests suites (`python3 <file>` each, not pytest); list_triggers (finished one-shots and
   tasks past their end date: list them for deletion, ask Ralph); every skill, tool or source added that week: name the
   session that used it, or flag it unused; the Creator Pathway decisions (BOOK.md Product open/screen lines, one-change
   remakes, the no-music VO test, RALPH.md read on own-content jobs); `grace/spend.py` vs the cap.
4. Commit and push straight to main, then send with SendUserFile (status proactive).

## Pushing to main 
In /home/user/Mymobileworld: `git stash -u -q` if dirty, `git fetch -q origin main && git checkout -q -B main origin/main`,
write the report, `git add reports && git commit` (message `Report: <file>`), `git push origin main`
(on a rejected push: `git pull --rebase origin main`, push again), then check out the previous branch and `git stash pop`.
Only report files go to main this way; any other change still goes through a branch + PR.
