# Sources (pulled 2026-10-26)

Numbers in REPORT.md come from these. "My estimate" in the report means no source; it is my math.

## The two TikToks
- Part 1: https://www.tiktok.com/@behind.the.car/video/7692796913363504414 (posted 2026-10-04, 316 s, 7,626 views on 2026-10-26). Transcript: tiktok_part1.txt
- Part 2: https://www.tiktok.com/@behind.the.car/video/7692810561863650590 (posted 2026-10-04, 289 s, 1,114 views). Transcript: tiktok_part2.txt
- Speaker: Shane Hummus (his name shows on screen, "@Shane Hummus"); @behind.the.car is a repost account (caption hashtags #hiringnow #jobs). Part 2 ends mid-sentence.

## Pain 1: missed calls, slow replies
- Invoca 2026 benchmark: 70 million calls, 44% missed (via JustCall summary) https://justcall.io/blog/missed-call-statistics.html ; Invoca LinkedIn: average business answers 56% https://linkedin.com/company/invoca-com
- CallRail 2025 survey of 1,000 US consumers: 78% have given up on a business after an unanswered call, 42% leave a voicemail, 21% call another business (via Beside, which checked it) https://beside.com/blog/missed-calls-cost-small-business
- The "85% never call back" and "62% unanswered" numbers have no solid source (Beside, JustCall). Not used.
- NP Digital Feb 2026 survey of 500 marketers: 3% reply to a lead within 5 minutes https://neilpatel.com/marketing-stats/response-time-new-leads/
- Lead response study (MIT/InsideSales, older): reaching a lead at 5 min vs 30 min, much higher odds; exact multiplier shaky https://callingly.com/blog/state-of-speed-to-lead
- Reddit r/smallbusiness, Jan 2026 HVAC thread (478 points, 110 comments), commenter: "We're always open M-F at 9 am, we answer the phone, and return calls and emails within 24 business hours. That's quickly becoming the 'outside the box'..." https://www.reddit.com/r/smallbusiness/comments/1q71vdk/most_hvac_companies_compete_on_price_i_competed/ (the original post itself was flagged by commenters as likely fake; the comment is what we use)
- AI receptionist self-serve prices: $25-$300/month, most $50-$150 https://www.myaifrontdesk.com/blogs/how-much-does-an-ai-receptionist-cost-a-straight-answer-for-2026 ; live answering from ~$130/month, virtual receptionists up to $1,600/month https://www.getjobber.com/academy/plumbing/plumbing-answering-service/
- ElevenLabs agents: $0.08 per call minute platform rate, LLM and phone line extra https://www.getmacha.com/blog/elevenlabs-agents-pricing-explained ; all-in $0.12-$0.42/min (competitor estimate) https://trtc.io/blog/details/conversational-ai-pricing-2026
- Generic AI agency offers (chatbots, lead capture) pitched cold are crowded; offline service businesses less so; churn is the big risk https://ciela.ai/blogs/is-ai-agency-market-saturated-reddit
- Our proof: Diaspo Phone Assistant, live on 718-576-2667 since Oct 2026 (Brain/Jobs/Diaspo Phone Assistant.md)

## Pain 2: product sellers need a steady flow of new video ads
- eMarketer: US TikTok Shop sales about $23.4B in 2026, ~48% up https://www.metaintro.com/blog/ai-avatars-tiktok-shop-23-billion-creator-jobs-2026
- WSJ (via AI Weekly): TikTok Shop flooded with AI product videos; sellers switch because AI clips are fast and cheap https://aiweekly.co/alerts/tiktok-shop-sellers-turn-to-ai-avatars-sidelining-creators
- Enthusiasm for AI creator content fell from ~60% (2023) to ~26% (early 2026) (same metaintro piece)
- Meta Andromeda: Meta test, 1 ad set with 25 creatives got 17% more conversions at 16% lower cost than 5 ad sets of 5 (via Segwise) https://segwise.ai/blog/meta-andromeda-update-creative-strategy-2026 ; ad fatigue window 6+ weeks down to 2-3 weeks (Pixel Panda via Segwise); agencies advise 10-20 new ads a week https://billo.app/blog/meta-andromeda-update/
- Human UGC video: average $150-$212, median ~$175 https://influee.co/blog/ugc-price ; AI UGC under $20 per video (Billo) https://billo.app/blog/ugc-ads/
- Reddit r/TikTokShop, 2026-09-08: hair care seller, "$50k a month" GMV, "ACOS>150%", asking how to raise video count, has 5,000 customers https://www.reddit.com/r/TikTokshop/comments/1wamw9d/hello_sellers_need_help_increasing_video_count/
- Our proof: Grace jobs Oct 2026, Kie cost per finished video $2.09 to $6.60 (Mymobileworld CLAUDE.md Jobs list); Grace sales tracker: 6 AI videos with 1 sale each (2026-10-20, grace/winners/README.md)

## Pain 3: reviews go stale
- BrightLocal Local Consumer Review Survey 2026 (Feb 2026, 1,002 US adults): 74% look for reviews from the last 3 months; 31% only use businesses rated 4.5+ (up from 17%); 80% more likely to use a business that replies to all reviews; 50% put off by templated replies; 97% use reviews https://www.brightlocal.com/research/local-consumer-review-survey/ ; summary https://www.pinmeto.com/news/brightlocal-local-consumer-review-survey-2026/
- Google: selectively asking only happy customers for reviews is not allowed https://searchengineland.com/google-review-guidelines-say-discouraging-negative-or-selectively-soliciting-positive-reviews-is-not-allowed-388541
- FTC final rule (Aug 2024) bans fake reviews and review suppression https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials

## Owner surveys (background)
- Main Street America Fall 2026 (1,568 owners): getting new customers and cash flow are top problems https://mainstreet.org/resources/knowledge-hub/publication/fall-2026-small-business-survey-results
- Small Business Expo (n=372): nearly half say the one thing they'd change is having more time https://www.thesmallbusinessexpo.com/blog/small-business-more-time/
- Businesses on social: 54% struggle to make enough content, 56% struggle to fit social media in https://www.netinfluencer.com/over-60-percent-of-small-businesses-boost-content-creation-investment-while-half-struggle-to-keep-pace-report-shows/

## Tested this session
- Reddit: camofox loaded r/smallbusiness and r/TikTokShop searches and threads (2026-10-26). Reddit .json API from curl: blocked (non-JSON reply). WebSearch with reddit.com domain filter: refused (400).
- camofox first start failed on the Camoufox zip download (connection reset); second run CAMOFOX_SETUP_OK.
