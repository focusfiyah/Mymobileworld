# House of Rameau (@houseoframeau): shared TikTok account (Ralph + Grace)

Status: 2026-10-20 access tested and 26 public videos pulled (`videos.json`); 8 are TikTok Shop videos, 5 of them our
AI videos. Only Tiger Eye has sold (1, in Grace's sales tracker; Ralph 2026-10-20). Next: first post here waits for
Ralph's OK on a video.

Ralph 2026-10-20: "we will be managing that together and posting videos there as well." Grace's rules
(`grace/PLAYBOOK.md`) and all the hard rules in CLAUDE.md apply to videos made for this account.

## Access (tested 2026-10-20)
- Composio TikTok connection `tiktok_buck-flunk` = House of Rameau (display name "House of Rameau🧑‍🧑‍🧒✨", bio "Az & Chana✨🧑‍🧑‍🧒").
- Since 2026-10-26 Composio has a second TikTok account, `tiktok_bac-stouth` = Ralph's @azariah2244 ("Azariah", 700 followers), and it is the DEFAULT. Every House of Rameau TikTok call must pass `account: tiktok_buck-flunk`, or it reads/posts on Azariah.
- Works: `TIKTOK_LIST_VIDEOS` (public videos, 20 a page, `cursor` for the next page: views, likes, comments, shares,
  caption, length) and `TIKTOK_GET_USER_STATS` (1,055 followers, 1,034 following, 4,686 likes, 26 videos on 2026-10-20).
- Not in that API: saves, sales/orders, GMV, watch time, traffic sources, private or draft videos. Saves, the shop
  product and transcripts come from `tiktok.py video <link>` (public page, free). Sales still come from Ralph/Grace.
- Posting: `TIKTOK_PUBLISH_VIDEO` (from a public URL, `is_aigc` flag for AI videos) exists but is NOT tested: posting is
  public, so it runs only on Ralph's OK for that video. An unaudited app may only allow private (SELF_ONLY) posts.

## Refresh the inventory
1. Composio `TIKTOK_LIST_VIDEOS` (max_count 20, then the returned cursor until has_more is false) +
   `TIKTOK_GET_USER_STATS`.
2. `tiktok.py video <each link> --no-media` for saves + shop product.
3. Rebuild `videos.json` (same fields), `python3 houseoframeau/check.py`.
A House of Rameau video that sold goes into the tracker like any other: `grace/winners/winners.py pull <link> --sales N`.

## Shop videos on 2026-10-20
AI = the videos we made (Ralph 2026-10-20: "It's the ones we created"). Sales from Ralph, 2026-10-20.

| Posted | Product | Views | Made by us (AI) | Sales |
|---|---|---|---|---|
| 09-20 | Fungix nail fungus (Approved Science) | 68 | yes | 0 |
| 09-15 | Arnica bruise cream (Approved Science) | 153 | yes | 0 |
| 09-14 | ARPURRAINA Tiger Eye necklace | 61 | yes (man on camera) | 1 |
| 09-14 | Restlex restless legs (Approved Science) | 53 | yes | 0 |
| 09-07 | Fungix nail fungus (Approved Science) | 70 | yes | 0 |
| 08-19 | Wooden HOME letters with eucalyptus wreath | 364 | no | 0 |
| 08-07 | ECAVUS zipper nursing shirts 3-pack | 371 | no | 0 |
| 08-02 | VeryVery Good Tea Energy Peach | 428 | no | 0 |
The account's own family videos get far more views (pregnancy reveal 49,759; godparents 3,650; most 500 to 1,900).
The September shop videos are at 53 to 153 views.

Flag: none of our 5 AI videos here (nor Grace's 6 AI sellers) carry TikTok's "AI-generated" label (meta `ai_generated_label` false); Ralph's rule is to use
TikTok's AI label where it applies.

## Test account for our AI videos (Ralph 2026-10-28)
Ralph: "we will be posting the AI videos that we do to House of Rameau to test them out on this account."
- Every AI video we make for Grace can also go here as a test. Post only on Ralph's OK for that video.
- Its own version, not Grace's file: a different shot order, framing or grade (`remix.py` style), so TikTok does not
  read it as a copy of her post, unless Ralph says the same cut is fine.
- Route (schema checked 2026-10-28): `TIKTOK_UPLOAD_VIDEO` with `publish: false`, `is_aigc: true`,
  `account: tiktok_buck-flunk` = a draft in the House of Rameau TikTok inbox. Ralph adds the TikTok Shop product link
  and caption in the app and posts it: the posting API has no product-link field, and an unaudited app may only post
  SELF_ONLY. Direct publish (`TIKTOK_PUBLISH_VIDEO`) only for a video with no product, on Ralph's word.
- Never use the default TikTok account (`tiktok_bac-stouth`, @azariah2244): another session posts a digital product
  there (Ralph 2026-10-28).
- After posting: add it to `videos.json` (mark AI + the job folder), refresh views weekly, and log any sale in Grace's
  tracker (`grace/winners/winners.py pull <link> --sales N`) so the two accounts can be compared on the same video.
