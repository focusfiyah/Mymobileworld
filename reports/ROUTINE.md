# Report routine (fired by two scheduled triggers into this session)

Goal: short notes on what we learned, so Ralph can paste them into a new chat. Free: no Kie or ElevenLabs calls.

## Daily (every night, 8:52pm ET)
1. `git fetch --all -q` in /home/user/Mymobileworld and /home/user/Dayone-ai (attach a repo with add_repo if it is missing).
2. `git log --all --since="<today> 00:00" --format='%ad %s' --date=short` in both repos, plus `git diff` of CLAUDE.md
   and job README `Status:` lines changed today.
3. Nothing new today → write nothing, send nothing, stop.
4. Otherwise write `reports/YYYY-MM-DD-daily.md` (≤250 words), using the same sections as `2026-10-01-daily.md`:
   Clients (status, $ spent vs plan, lessons) · Personal (Day One AI + tools) · New rules · Gotchas.
   Only facts from the commits/notes; no filler. Skip empty sections.
5. Commit and push it **straight to main** (Ralph, 2026-10-01), then send the file with SendUserFile (status proactive).

## Weekly (Sunday, 9:10pm ET, after the daily)
1. Read this week's daily files (Mon–Sun) plus the git logs for the week.
2. Write `reports/YYYY-Wnn-weekly.md` (≤400 words), using the same sections as `2026-W40-weekly.md`:
   per project/client · Skills acquired (table, new ones marked) · Gotchas · Next.
3. Commit and push straight to main, then send with SendUserFile (status proactive).

## Pushing to main (both reports)
In /home/user/Mymobileworld: `git stash -u -q` if dirty, `git fetch -q origin main && git checkout -q -B main origin/main`,
write the report, `git add reports && git commit` (message `Report: <file>`), `git push origin main`
(on a rejected push: `git pull --rebase origin main`, push again), then check out the previous branch and `git stash pop`.
Only report files go to main this way; any other change still goes through a branch + PR.
