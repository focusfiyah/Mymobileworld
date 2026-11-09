# Creator Pathway (Skool) course pull

Status (2026-11-09): pull DONE (gates 1-8) + analysis DONE (gates 9-11), $0. Analysis: ANALYSIS.md, review page https://claude.ai/artifact/7DnHxBB3wML5tNW67Zyi6B , Drive "Creator Pathway (Skool course)" https://drive.google.com/drive/folders/1ongDvMgSDRhk192t5IUQIlQ-VO7jWXQY. Next: Ralph's A-F decisions, then add the free items to Grace's gate/PLAYBOOK.

What: Ralph asked (Telegram 2026-11-09) for everything word for word from skool.com/creator-pathway-9391 (Grace's login) to study for Grace + Ralph's TikTok Shop / UGC work: Classroom sections TikTok Shop, UGC, Weekly Call Replays (= Live Coaching), Community Resources, Loom Lessons, Mindset (not Start Here) + Community posts that mention coaching or 1:1.

How: Playwright with a logged-in session (login never stored in git). Lesson text = __NEXT_DATA__ course tree; Skool videos = Mux HLS (needs Referer https://www.skool.com/) with Skool's own English captions; Loom = yt-dlp audio + local Whisper; files = POST api2.skool.com/files/<id>/download-url; comments = api2 /posts/<id>/comments paged with created-gt. Content stays in Drive, not git.

Files: GATES.md (gates), verify.py (gate checks), build.py (docs).
