# Pinterest (Ralph's own marketing; Azariah manages it)

Status: 2026-11-26: decided, waiting on setup by Ralph (Pinterest Business account + second Zernio account + key). Nothing posted, $0.

Decisions (Ralph 2026-11-26: "we need to incorporate Pinterest with our marketing and automate it. Meaning you are managing it"; tapped):
- Promotes the free flag check (https://dayoneai.gumroad.com/l/flagcheck) and the AI Product Video Kit; same AI side hustle / AI product video audience as @realgoodhustles.
- Content: our AI twin reels and carousels recut as video/idea pins ($0) + new 1000x1500 text pins built from our scripts and the kit with our own tools (no AI images unless asked with cost).
- Pace: 3 pins a day. Ralph OKs one batch a week on a review page; a scheduled task posts 3 a day and turns itself off when the batch runs out (the task itself is OK'd with him first).
- Posting route: Zernio, on a SECOND Zernio account (the free plan allows 2 connected accounts; the primary holds TikTok azariah2244 + houseoframeau). Its key is the environment variable `Zernio_API_key_2` (never a network secret: one secret per host would override the primary key, as with the two Netlify accounts). Primary key stays `Zernio_API_key`. Every Pinterest call sends `Authorization: Bearer $Zernio_API_key_2`.
- Pinterest endpoints (Zernio llms.txt): GET/PUT /v1/accounts/{accountId}/pinterest-boards (list, default board); POST /v1/posts with platforms [{platform: pinterest, accountId}] (see "Pinterest Pins").

Ralph's setup steps:
1. Make a free Pinterest Business account (or switch one to Business).
2. In the second Zernio account, connect that Pinterest account.
3. In this cloud environment: session title bar > environment > Edit > Environment variables: add `Zernio_API_key_2` = the second account's API key. Never paste it in chat. A new session (or resume) picks it up.
