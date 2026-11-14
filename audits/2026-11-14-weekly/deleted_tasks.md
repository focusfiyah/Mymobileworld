# Scheduled tasks deleted 2026-11-14 (weekly audit, Ralph: "do all the fixes that you recommended")

All were disabled. To bring a paused one back, recreate it with this prompt and schedule (ask Ralph first).

## Paused routines
- "Instagram AUTOPILOT comment DMs" (trig_01RDbsCxEBnCwanTzEErhuoj), CRON_TZ=America/New_York 23 8-23/2 * * *, into session_01Kz3N2SfB3ntoW4xgdMdJjJ. Prompt: Run the Instagram AUTOPILOT comment check: in the Composio workbench (session "fuel"), exec(open("/mnt/files/ig_comment_dm.py").read()) then run(dry=False). It DMs the cheat sheet to new AUTOPILOT commenters on @realgoodhustles reels from the last 7 days and replies "Sent! Check your DMs" under each. If /mnt/files/ig_comment_dm.py is missing, restore it from Dayone-ai products/ai-on-autopilot/automation/ig_comment_dm.py. No message to Ralph unless something failed or this is the first real DM sent.
- "RGH daily batch (builds tomorrow's, night-before OK)" (trig_01B2e7oxVNaP4m6H7pVEupL8), CRON_TZ=America/New_York 37 16 * * *, into session_01Kz3N2SfB3ntoW4xgdMdJjJ. Prompt: Run the AI on Autopilot daily reels: pull main in Dayone-ai, then follow products/ai-on-autopilot/reels/ROUTINE.md end to end (2 new reels in Ralph's TikTok drafts + the review page post kit by 7 AM Eastern, then one email and one push). Never post publicly and never spend money.
- "Diaspo Harvey weekday run" (trig_01Lo63d8GHBSwsQDpREb1B5m), CRON_TZ=America/New_York 8 10 * * 1-5, into session_01GcDUwxouKtV9sQwavBbXq3. Prompt: Diaspo Harvey weekday run. In the jean-rameau checkout: git pull origin main (was ccr-db3a2861-bpbghy, merged 2026-11-14), then follow diaspo-auto-school/harvey/phone/DAILY.md steps 1-7 exactly (partners only, no phone calls, nothing sent without Ralph's Approve on the review page). Email + push Ralph only if there are new drafts, a partner reply or an error. (19 approved emails were on hold when paused.)

## Finished one-shots (RGH batches of 2026-10-30/31, all fired or cancelled)
trig_01QESzmgZdmAj1bJKELy8R9n, trig_0192HPhv5zK2GYK7jQVhJrh4, trig_01F3qF2U7UwB3xSEdsGMNSFa, trig_015Z5PLkNsZcRmPK2TN3xfs2,
trig_01FohMTGzXSJw7VZgKfAPgSp, trig_01H3doXiy2juTMzAJTogMHFU, trig_013PwWShxNgGwSLPWcd7qAx2, trig_01Y6s3YPPKwroDHhTZdh31LT,
trig_016rJEmUQXogJg5dP6cZYAJu, trig_01UhSAiXP4PN5DC5PscKfcFn, trig_01Q1Y1wqmGbKhChndKFmnzex, trig_01KWmmaMR8FGrMX3VTJFP8JN.
