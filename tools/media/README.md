# Job media in Google Drive (Ralph 2026-10-29)

Images, sound and video never go into git. They live in Drive "Repo media (Claude, do not delete)"
(https://drive.google.com/drive/folders/1a_SwrVzG0Jmpi1cYzFTnqj1JySCxd7p2) / <repo> / <job>, as tar parts of at most
95 MB. Each job's record (parts, Drive ids, every file's sha256) is `media-in-drive/<unit>.json` in its repo.
The rule: Mymobileworld CLAUDE.md "Job media lives in Drive". Run every command from the repo root
(Dayone-ai: `python3 /home/user/Mymobileworld/tools/media/media.py ...`).

## Store a job's media (end of every job, or when Ralph sends footage)
1. `python3 tools/media/media.py plan` lists what is not stored yet.
2. `python3 tools/media/media.py pack ugc/<job>` (or `--all`): tars the new files, hosts each part on Kie's free
   3-day file host. Only new or changed files go in; a later round becomes set 2, 3, ...
3. `python3 tools/media/media.py pending > pending.json`, host it the same way
   (`curl -sS -X POST https://kieai.redpandaai.co/api/file-stream-upload -F file=@pending.json -F uploadPath=repo-media`).
4. In COMPOSIO_REMOTE_WORKBENCH paste `workbench_upload.py`, then `print(run("<pending url>"))` until `left` is 0,
   then `print(results_link())`.
5. `curl -sSL <link> -o results.json`, `media.py record results.json` (refuses any part whose Drive sha256 or size
   differs), `media.py untrack` (git rm of every file now safe in Drive), commit.
6. `media.py check` must print MEDIA_OK.

## Bring a job's media back
1. `python3 tools/media/media.py need ugc/<job>` prints the Drive ids.
2. Paste `workbench_restore.py` with those ids into the workbench; it prints a link to links.json.
3. `curl -sSL <link> -o links.json`, `media.py get ugc/<job> links.json`: downloads, checks every part and file
   by sha256, unpacks in place. The files stay untracked (`.gitignore` media block).

## Facts (tested 2026-10-29)
- Kie's file host: 100 MB upload OK, ~300 MB refused ("Memory limit would be exceeded").
- Composio GOOGLEDRIVE_UPLOAD_FROM_URL pulled 100 MB in 7 s; Drive's `sha256Checksum` matched the local file.
- Restore test: ralph/dfy-service, 18 files back, all checked.
