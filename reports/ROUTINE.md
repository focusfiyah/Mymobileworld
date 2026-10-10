# Report routine (fired by one scheduled trigger (weekly only; daily reports stopped, Ralph 2026-10-10, usage) into this session)

Goal: short notes on what we learned, so Ralph can paste them into a new chat. Free: no Kie or ElevenLabs calls.

## Weekly (Sunday, 9:10pm ET)
1. `git fetch --all -q` in /home/user/Mymobileworld and /home/user/Dayone-ai (add_repo if missing). Read the git logs for the week (Mon–Sun) in both repos, plus any older daily files in `reports/`, and job README `Status:` lines changed this week.
2. Write `reports/YYYY-Wnn-weekly.md` (≤400 words), using the same sections as `2026-W40-weekly.md`:
   per project/client · Skills acquired (table, new ones marked) · Gotchas · Next.
3. Commit and push straight to main, then send with SendUserFile (status proactive).

## Pushing to main 
In /home/user/Mymobileworld: `git stash -u -q` if dirty, `git fetch -q origin main && git checkout -q -B main origin/main`,
write the report, `git add reports && git commit` (message `Report: <file>`), `git push origin main`
(on a rejected push: `git pull --rebase origin main`, push again), then check out the previous branch and `git stash pop`.
Only report files go to main this way; any other change still goes through a branch + PR.
