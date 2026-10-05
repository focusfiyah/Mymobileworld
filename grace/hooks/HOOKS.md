# Grace hook library

Fill-in-the-blank hook templates for Grace's videos. Source of truth: `hooks.json` (edit there, then run
`python3 grace/hooks/build.py`). Batches: B1 rows 2-28 (27 hooks, 2026-10-05), B2 rows 29-154 (126 hooks, 2026-10-05).

## How to use (every Grace job)
- Every Grace script picks its spoken hook options from here first (plus the coach-modeled hooks, PLAYBOOK §3); name the hook id in the plan's line sources. Ids match the sheet row: H016 = row 16.
- Say hooks WORD FOR WORD as written in the sheet, no contractions or rewording (Ralph, 2026-10-05). Only the blanks (__) get filled; the humanizer pass leaves the hook line itself alone.
- Fill every blank with a concrete moment from the product research, never a broad problem.
- The line after the hook answers or proves it on screen right away (demo, close-up, the back/side/pocket shot).
- Spread hook types across a product's videos (no two videos of one product on the same id; TikTok flags repeats).
- Comparison hooks (rows 71-75, 135-144) override the 'only our product' rule (Ralph, 2026-10-05): a second product may be on screen, and its brand may be named on screen and in the script unless Ralph says otherwise for that video. Price can be talked about ("the cheaper one"), but never a price number.
- These are spoken hooks. On-screen text stays curiosity-only, 5-7 words, and is burned in only on Ralph's yes.
- Log which id each finished video used (`used_in`) so results can show which hook types win.
- Types are as in the sheet; 'Comparison Hook', 'Time Pressure Hook' and 'Simple Fix Hook' are filed as Comparison, Time Pressure and Simple Fix.

## Pick by category

- **Accessories:** H002, H004, H009, H015, H022, H029, H030, H031, H038, H039, H041, H045, H055, H069, H074, H098, H109, H122, H125, H129
- **Affordable comparisons:** H138
- **Any category:** H024, H033, H034, H036, H037, H048, H051, H058, H060, H061, H062, H063, H065, H075, H081, H083, H084, H085, H096, H099, H100, H101, H102, H111, H113, H114, H118, H121, H123, H127
- **Any demonstrable product:** H095
- **Any product:** H028
- **Any visual product:** H072
- **Bags:** H021, H022
- **Bathroom:** H046
- **Beauty:** H002, H003, H004, H005, H006, H007, H009, H011, H012, H013, H014, H016, H017, H019, H020, H025, H026, H027, H029, H030, H031, H032, H035, H038, H039, H040, H043, H044, H045, H047, H049, H050, H052, H053, H054, H055, H057, H059, H064, H066, H067, H068, H069, H070, H071, H073, H074, H076, H077, H078, H079, H080, H082, H086, H087, H088, H089, H091, H092, H093, H094, H097, H098, H109, H112, H115, H119, H122, H124, H129, H131, H136, H154
- **Beauty tools:** H023
- **Bedding:** H093
- **Beverage:** H050
- **Busy routines:** H149
- **Buying guides:** H144
- **Car:** H046
- **Comfort:** H126
- **Convenience products:** H010
- **Desk:** H046
- **Electronics:** H015, H020, H026, H027, H031, H040, H042, H059, H067, H071, H073, H082, H090, H094, H112
- **Established TikTok Shop products:** H104
- **Established products:** H103, H105, H106, H107
- **Events:** H132
- **Everyday problem-solving products:** H008
- **Everyday products:** H108
- **Fashion:** H002, H003, H004, H005, H011, H012, H013, H014, H016, H017, H018, H019, H020, H021, H022, H023, H025, H026, H027, H029, H030, H032, H035, H038, H044, H047, H049, H052, H053, H054, H057, H059, H064, H066, H067, H068, H069, H070, H071, H073, H074, H076, H077, H078, H079, H080, H086, H087, H088, H089, H091, H092, H093, H097, H098, H112, H115, H119, H124, H125, H131, H136, H154
- **Food:** H012, H014, H016, H042, H047, H050, H052, H054, H068, H079, H087, H088, H089, H091, H092
- **Fragrance:** H052, H053, H056, H057, H070, H115, H119
- **Gifts:** H055, H056
- **Home:** H002, H003, H004, H005, H006, H007, H009, H010, H011, H012, H013, H014, H015, H016, H018, H019, H020, H023, H025, H026, H027, H029, H031, H032, H035, H038, H039, H040, H041, H042, H043, H044, H045, H047, H049, H050, H053, H054, H055, H056, H057, H059, H064, H066, H067, H068, H069, H070, H071, H073, H074, H076, H077, H078, H079, H080, H082, H086, H087, H088, H089, H090, H091, H092, H093, H094, H097, H098, H109, H112, H115, H119, H122, H124, H125, H126, H128, H129, H131, H136, H142, H153, H154
- **Household and preparedness products:** H133
- **Jewelry:** H030
- **Kids:** H040, H041, H056, H122
- **Kitchen:** H003, H005, H007, H009, H010, H013, H015, H017, H018, H019, H025, H032, H035, H039, H042, H043, H044, H045, H046, H049, H076, H080, H082, H086, H090, H094, H109, H124, H125, H126, H128, H129
- **Lifestyle:** H011, H064, H077
- **Niche products:** H066, H110
- **Organization:** H007, H126, H128, H142, H153
- **Organization and everyday essentials:** H148
- **Pets:** H005, H018, H040, H041, H122
- **Problem-solving products:** H006, H150
- **Product comparisons:** H135, H139, H140, H143
- **Product discoveries:** H097
- **Product education:** H141
- **Product reviews:** H116, H117, H120
- **Purse:** H046
- **Routines:** H153
- **Routines and everyday products:** H145
- **Routines and habits:** H147
- **Seasonal and lifestyle content:** H130
- **Shapewear:** H021
- **Shopping guides:** H134
- **Side-by-side reviews:** H137
- **Toys:** H090
- **Travel:** H132, H142
- **Tutorials and quick wins:** H146
- **Tutorials and routines:** H151
- **Weather:** H132
- **Wellness:** H003, H017, H043, H050, H078
- **Wellness and organization:** H152

## Observation

**H002. "This is the part I actually care about"**
- Use when: You want to lead with a specific detail, feature, or payoff that matters more than the obvious selling point.
- Best for: Fashion, Beauty, Home, Accessories
- Note: Helps the creator center the video around one meaningful detail instead of trying to explain everything.

**H006. "I did not realize how much __ bothered me until I stopped dealing with it"**
- Use when: The benefit is easier to appreciate after experiencing the alternative.
- Best for: Problem-solving products, Home, Beauty
- Note: Works best when you can visibly show what changed.

**H009. "This is such a small thing, but it annoys me every single time"**
- Use when: You're talking about a small, recurring annoyance that isn't dramatic, but happens often enough to make the product feel useful.
- Best for: Home, Kitchen, Accessories, Beauty
- Note: Small frustrations can be more believable than dramatic ones.

**H024. "The first thing I checked was __"**
- Use when: There is one feature buyers are likely to inspect first.
- Best for: Any category
- Note: Name a real buying concern.

**H029. "The listing did not really show me this part"**
- Use when: A visual detail is clearer in real life than online
- Best for: Fashion, Accessories, Home, Beauty
- Note: Close-up footage makes this stronger.

**H030. "This looks completely different once you actually see it on"**
- Use when: The on-body or in-use appearance is the selling point
- Best for: Fashion, Jewelry, Beauty, Accessories
- Note: Show the product quickly.

**H031. "I did not realize how __ this was until I had it in my hand"**
- Use when: Scale, weight, texture, thickness, or construction surprises you
- Best for: Home, Beauty, Electronics, Accessories
- Note: Use your hand for visual scale when helpful.

**H032. "This is one of those details you do not notice until you use it"**
- Use when: A feature becomes meaningful only during actual use
- Best for: Home, Kitchen, Fashion, Beauty
- Note: Show the use moment.

**H033. "I thought __ would be the best part, but it is actually __"**
- Use when: A secondary feature becomes the real reason you like it
- Best for: Any category
- Note: The contrast creates natural curiosity.

**H034. "The thing that sold me was not even the obvious feature"**
- Use when: An overlooked detail is more compelling than the headline feature
- Best for: Any category
- Note: Reveal the unexpected detail quickly.

**H036. "This is probably my favorite part and I almost missed it"**
- Use when: A less-visible feature deserves attention
- Best for: Any category
- Note: Show the feature as you name it.

**H042. "This has somehow become the thing everyone in my house uses"**
- Use when: Shared household usefulness is a selling point
- Best for: Home, Kitchen, Electronics, Food
- Note: Show different use moments if possible.

**H049. "I did not realize I had a routine for this until I noticed I always grab this first"**
- Use when: The habit itself demonstrates usefulness
- Best for: Beauty, Kitchen, Home, Fashion
- Note: Good for mature products with no flashy feature.

**H069. "Maybe it is just me, but I always notice __"**
- Use when: A small visual or functional detail influences your opinion
- Best for: Fashion, Beauty, Home, Accessories
- Note: Follow with the exact detail.

**H081. "I thought I needed __, but what I really cared about was __"**
- Use when: The true buyer motivation becomes clearer after use
- Best for: Any category
- Note: The second blank should be the emotional or practical payoff.

**H107. "If you have already seen this product 20 times, look at this part instead"**
- Use when: The product is familiar but there is still a fresh detail
- Best for: Established products
- Note: Good for crowded products without pretending they are new.

## Routine

**H003. "I keep reaching for this more than I expected"**
- Use when: You're showing a product that has quietly become part of your normal day, outfit, setup, or routine.
- Best for: Fashion, Beauty, Home, Kitchen, Wellness
- Note: Feels natural and experience-based without needing a dramatic transformation or problem.

**H044. "This is one of those things I keep reaching for without thinking about it"**
- Use when: The product has become naturally habitual
- Best for: Beauty, Fashion, Home, Kitchen
- Note: Show where you keep it or when you grab it.

**H045. "I keep this right by __ because that is where I actually use it"**
- Use when: Placement explains how the product fits real life
- Best for: Home, Beauty, Kitchen, Accessories
- Note: The location itself helps sell the use case.

**H046. "This stays in my __ for a reason"**
- Use when: The product earns a permanent place somewhere
- Best for: Purse, Car, Desk, Kitchen, Bathroom
- Note: Name the location and explain the real reason.

**H047. "This is the thing I grab when __"**
- Use when: A recurring situation triggers use
- Best for: Fashion, Beauty, Home, Food
- Note: Make the moment specific.

**H048. "Every time I __, I end up reaching for this"**
- Use when: The product fits a repeatable behavior
- Best for: Any category
- Note: Show the routine naturally.

**H050. "There is one time of day when I always want this"**
- Use when: The product has a strong time-based use case
- Best for: Food, Beverage, Beauty, Wellness, Home
- Note: Name the moment quickly.

**H051. "This makes more sense once you see when I actually use it"**
- Use when: The use case matters more than the feature list
- Best for: Any category
- Note: Lead into the situation instead of describing specs.

## Emotional Outcome

**H004. "This just makes everything feel a little more put together"**
- Use when: You're selling the feeling the product creates rather than a major functional result.
- Best for: Fashion, Beauty, Home, Accessories
- Note: Gives creators a softer way to talk about aesthetic or emotional payoff without overhyping the product.

**H053. "This is what I reach for when I want __"**
- Use when: The product supports a specific desired feeling or result
- Best for: Fashion, Beauty, Fragrance, Home
- Note: Fill the blank with a human payoff, not a marketing claim.

**H085. "This is the part that makes it worth it for me"**
- Use when: A single payoff matters more than the feature list
- Best for: Any category
- Note: Keep "for me" to make it personal.

## Problem Callout

**H005. "One thing I cannot stand is __"**
- Use when: The product solves a very specific annoyance people immediately recognize.
- Best for: Home, Kitchen, Beauty, Fashion, Pets
- Note: Be specific about the annoying moment. The blank should not be a broad problem.

**H007. "I have been putting up with this for way too long"**
- Use when: The buyer may have normalized an irritating problem.
- Best for: Home, Kitchen, Beauty, Organization
- Note: Name the actual thing you were putting up with quickly.

**H008. "If you also hate when __, look at this"**
- Use when: The product solves minor everyday friction.
- Best for: Everyday problem-solving products
- Note: Fill the blank with a concrete situation, not a vague pain point.

**H066. "This is such a specific problem, but if you have it, you know"**
- Use when: The pain point is narrow but meaningful
- Best for: Niche products, Fashion, Beauty, Home
- Note: Great for highly targeted content.

## Problem/Solution

**H010. "Why did nobody make this easier sooner?"**
- Use when: The solution feels obvious once viewers see it.
- Best for: Convenience products, Kitchen, Home
- Note: Let the demonstration answer the question.

## Confession

**H011. "I am done pretending this does not bother me"**
- Use when: The problem is relatable but people rarely say it out loud.
- Best for: Fashion, Beauty, Home, Lifestyle
- Note: Keep the tone playful rather than dramatic.

**H035. "I was not expecting to care this much about __"**
- Use when: A small feature turns out to matter more than expected
- Best for: Home, Fashion, Beauty, Kitchen
- Note: Works well with everyday conveniences.

**H043. "I did not think this would become part of my routine"**
- Use when: The product naturally earned a repeat-use spot
- Best for: Beauty, Wellness, Home, Kitchen
- Note: Explain when you now reach for it.

**H079. "I finally admitted that I just do not like __"**
- Use when: A personal preference changes the buying decision
- Best for: Fashion, Beauty, Food, Home
- Note: Specific dislikes can create strong recognition.

**H117. "I was fully prepared not to like this"**
- Use when: You approached the product skeptically
- Best for: Product reviews
- Note: Explain what specifically changed your opinion.

**H118. "I did not expect this to be the thing I liked most"**
- Use when: Your favorite feature surprised you
- Best for: Any category
- Note: Follow with the unexpected feature.

**H119. "I had a completely different idea of what this would be like"**
- Use when: The real-life experience differs from your expectation
- Best for: Beauty, Fashion, Fragrance, Home
- Note: Describe the difference rather than using fake shock.

## Preference

**H012. "I know this is minor, but I really do care about __"**
- Use when: A specific preference drives the purchase.
- Best for: Fashion, Beauty, Home, Food
- Note: The specificity is the hook.

**H013. "Apparently I have very strong opinions about __"**
- Use when: The product connects to a personal standard.
- Best for: Fashion, Beauty, Kitchen, Home
- Note: Follow immediately with the preference.

**H014. "I am very particular about __"**
- Use when: The viewer may share a strong product preference.
- Best for: Beauty, Fashion, Food, Home
- Note: Explain what your standard actually is.

**H015. "I do not need __ to be fancy. I just need it to __"**
- Use when: The buyer values function over bells and whistles.
- Best for: Home, Kitchen, Electronics, Accessories
- Note: The second blank should be the real payoff.

**H068. "This might sound picky, but __"**
- Use when: A personal standard could sound overly specific without context
- Best for: Fashion, Beauty, Food, Home
- Note: Picky makes a detailed preference feel conversational.

**H070. "I never know how to explain why I like __ until I see something like this"**
- Use when: The product embodies a hard-to-describe preference
- Best for: Fashion, Beauty, Home, Fragrance
- Note: Use the product as the example.

**H082. "I do not need this to do everything"**
- Use when: The product wins because it does one job well
- Best for: Home, Kitchen, Beauty, Electronics
- Note: Follow with the one job that matters.

## Contrast

**H016. "I like __, but I do not like __"**
- Use when: The product gives the desired benefit without a common downside.
- Best for: Fashion, Beauty, Food, Home
- Note: One of the strongest structures for showing a tradeoff.

**H017. "I want __ without having to __"**
- Use when: The product removes an unwanted tradeoff.
- Best for: Fashion, Beauty, Kitchen, Wellness
- Note: Make both sides specific and believable.

**H019. "I would rather __ than spend another day __"**
- Use when: The product lets the buyer avoid something frustrating.
- Best for: Fashion, Beauty, Home, Kitchen
- Note: Keep the comparison natural, not exaggerated.

**H073. "Same idea. Completely different experience."**
- Use when: Two similar products perform or feel noticeably different
- Best for: Home, Beauty, Fashion, Electronics
- Note: Immediately explain what creates the difference.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H080. "I kept buying __ when what I actually wanted was __"**
- Use when: The buyer has been solving the wrong problem
- Best for: Fashion, Beauty, Home, Kitchen
- Note: Excellent for benefit translation.

## Humor

**H018. "I am willing to deal with a lot, but not __"**
- Use when: A small frustration has become the breaking point.
- Best for: Home, Kitchen, Fashion, Pets
- Note: Best when the annoyance is visually obvious.

**H041. "I bought one and apparently that was my first mistake"**
- Use when: Multiple family members or uses make one product insufficient
- Best for: Home, Kids, Pets, Accessories
- Note: Follow with who stole or claimed it.

**H064. "Please tell me I am not the only person who does this"**
- Use when: A common but rarely discussed behavior sets up the product
- Best for: Home, Beauty, Fashion, Lifestyle
- Note: Reveal the behavior quickly.

**H125. "This might be the most practical reason I have ever bought something"**
- Use when: The purchase was driven by a very ordinary convenience
- Best for: Home, Kitchen, Accessories, Fashion
- Note: Follow with the practical reason.

**H126. "I am apparently at the age where this excites me"**
- Use when: An ordinary home, kitchen, organization, or comfort product genuinely delights you
- Best for: Home, Kitchen, Organization, Comfort
- Note: Use naturally; do not force age-based stereotypes.

**H127. "I did not expect my favorite part to be this boring"**
- Use when: A mundane feature turns out to be genuinely useful
- Best for: Any category
- Note: Great for storage, cleanup, pockets, charging, etc.

**H128. "I know exactly how unexciting this sounds, but watch"**
- Use when: A practical feature is more satisfying than it sounds
- Best for: Home, Kitchen, Organization
- Note: Let the demo deliver the payoff.

**H129. "This is peak "why did this make me so happy?""**
- Use when: A small convenience produces disproportionate satisfaction
- Best for: Home, Kitchen, Beauty, Accessories
- Note: Show the satisfying moment.

## Buyer Question

**H020. "This is the part I wanted to see before I bought it"**
- Use when: The listing or other videos do not clearly answer an important purchase question.
- Best for: Fashion, Beauty, Home, Electronics
- Note: Show the answer immediately after the hook.

**H023. "I needed to know how this looked from the side"**
- Use when: The side profile may reveal fit, shape, bulk, or coverage.
- Best for: Fashion, Beauty tools, Home
- Note: Show rather than over-explain.

**H025. "Here is what I would want someone to show me before I ordered this"**
- Use when: The product has several details that matter more than the listing.
- Best for: Fashion, Beauty, Home, Kitchen
- Note: Pick one or two details for this video, not every feature.

**H026. "I kept looking for a video that showed __"**
- Use when: Existing content leaves an important question unanswered.
- Best for: Fashion, Beauty, Home, Electronics
- Note: Great opportunity for search-friendly content.

**H105. "I have seen this everywhere, but nobody showed me this part"**
- Use when: A popular product still has an unanswered buyer question
- Best for: Established products
- Note: Freshens crowded products by focusing on missing information.

## Question

**H021. "Okay, but what does the back actually look like?"**
- Use when: The back view matters to the buying decision.
- Best for: Fashion, Bags, Shapewear
- Note: Excellent for products where creators usually only show the front.

**H022. "Does it actually have usable pockets?"**
- Use when: Pocket size or placement matters.
- Best for: Fashion, Bags, Accessories
- Note: Put your hands or real items inside them.

**H028. "If you are wondering whether __, here you go"**
- Use when: You can directly answer a likely buyer question.
- Best for: Any product
- Note: Demonstrate the answer instead of talking around it.

**H065. "Does anybody else __?"**
- Use when: A common habit or annoyance invites recognition
- Best for: Any category
- Note: Avoid generic engagement bait. The question should lead naturally to the product.

## Reassurance

**H027. "Before you buy this, look at __"**
- Use when: The buyer needs to inspect one important detail.
- Best for: Fashion, Home, Beauty, Electronics
- Note: Avoid fear-based wording. Make it useful.

**H108. "I am not going to tell you this is life-changing"**
- Use when: You want to lower the hype and focus on a practical benefit
- Best for: Everyday products
- Note: Follow with the modest reason you still like it.

**H109. "This is not dramatic. It is just really convenient"**
- Use when: The value is small but recurring
- Best for: Home, Kitchen, Beauty, Accessories
- Note: Understatement can make the recommendation more credible.

**H110. "I do not think everyone needs this, but I know exactly who will appreciate it"**
- Use when: The product has a specific audience rather than mass appeal
- Best for: Niche products
- Note: Describe that person next.

**H111. "There is nothing complicated about why I like this"**
- Use when: The product solves a simple need well
- Best for: Any category
- Note: Then state the reason plainly.

## Story

**H037. "I bought it because of __, but I keep using it because of __"**
- Use when: The initial reason to buy differs from the long-term payoff
- Best for: Any category
- Note: Strong for products you have used more than once.

**H038. "I thought I would use this for __, but somehow it became my __"**
- Use when: The product found an unexpected role in your life
- Best for: Home, Fashion, Beauty, Accessories
- Note: Keep the second use believable and specific.

**H040. "This was supposed to be for __"**
- Use when: Someone else in the household claimed or adopted the product
- Best for: Pets, Kids, Home, Beauty, Electronics
- Note: Let the little story carry the hook.

**H056. "This immediately made me think of my __"**
- Use when: The product connects to a relationship or person
- Best for: Gifts, Kids, Home, Fragrance
- Note: Use the relationship to make the product emotionally relevant.

**H116. "I almost skipped this because of __"**
- Use when: A concern or assumption nearly stopped the purchase
- Best for: Product reviews
- Note: The turning point should be meaningful.

**H120. "I changed my mind about this after __"**
- Use when: A specific use moment shifted your opinion
- Best for: Product reviews
- Note: The "after" should be the turning point.

**H121. "The first time I used this, I immediately noticed __"**
- Use when: A first-use observation is strong enough to lead
- Best for: Any category
- Note: Specific observations feel more credible than "I loved it."

**H122. "I did not think much of this until __ happened"**
- Use when: A small event revealed the product's usefulness
- Best for: Home, Pets, Kids, Beauty, Accessories
- Note: Tell the moment, then show why it mattered.

**H123. "This earned its spot after one very specific moment"**
- Use when: A real-life situation proved the product useful
- Best for: Any category
- Note: The moment is the angle.

**H124. "I bought this for a very boring reason"**
- Use when: An ordinary need can create relatable content
- Best for: Home, Kitchen, Fashion, Beauty
- Note: The boring reason is often more believable than hype.

## Unexpected Use

**H039. "I did not buy this for __, but that is exactly what I keep using it for"**
- Use when: A secondary use case is surprisingly useful
- Best for: Home, Kitchen, Accessories, Beauty
- Note: A good way to create another video from an established product.

## Occasion

**H052. "I save this specifically for __"**
- Use when: The product has a distinct moment or event when it shines
- Best for: Fashion, Beauty, Fragrance, Food
- Note: Occasion should be natural, not forced.

## Identity

**H054. "This is my __ kind of product"**
- Use when: The product fits a recognizable personal preference or lifestyle
- Best for: Fashion, Beauty, Home, Food
- Note: Use a specific identity like "I hate complicated routines."

**H057. "This feels very __"**
- Use when: The product has a clear aesthetic or personality
- Best for: Fashion, Beauty, Fragrance, Home
- Note: Fill with something viewers can picture, like "Sunday morning coffee."

**H058. "If you are a __ person, you will understand why I noticed this"**
- Use when: A niche preference makes the feature especially relevant
- Best for: Any category
- Note: The identity should be specific enough to create recognition.

**H059. "I know exactly the kind of person who is going to care about this detail"**
- Use when: A specific feature matters strongly to a particular buyer
- Best for: Fashion, Beauty, Home, Electronics
- Note: Name the detail right after the hook.

**H060. "I am absolutely the person who __"**
- Use when: Your own habit or preference makes the recommendation believable
- Best for: Any category
- Note: Use self-recognition rather than broad demographic labels.

**H061. "This is for the people who always __"**
- Use when: A recurring behavior defines the audience
- Best for: Any category
- Note: Behavior is usually stronger than vague labels like "busy women."
- Used in: super-blanky-v2 (2026-10-05)

**H067. "You either care about this detail or you really do not"**
- Use when: The product has a feature that matters intensely to some buyers
- Best for: Fashion, Beauty, Home, Electronics
- Note: Then explain why you personally care.

## Gift

**H055. "I already know exactly who would love this"**
- Use when: The product clearly fits a type of person
- Best for: Gifts, Home, Beauty, Accessories
- Note: Describe the person rather than saying "perfect gift."
- Used in: super-blanky-v2 (2026-10-05)

## Recognition

**H062. "You know that moment when __?"**
- Use when: The product fits a very recognizable little situation
- Best for: Any category
- Note: Finish with a concrete moment viewers can picture.

**H063. "I know I cannot be the only one who __"**
- Use when: A slightly quirky habit or frustration creates relatability
- Best for: Any category
- Note: The more specific the behavior, the better.

## Comparison

**H071. "I did not think there was a difference until I put them next to each other"**
- Use when: The contrast is visually meaningful
- Best for: Beauty, Fashion, Home, Electronics
- Note: Show both versions together.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H072. "This is one of those things you have to see side by side"**
- Use when: The difference is hard to appreciate in isolation
- Best for: Any visual product
- Note: Keep explanation short and let the camera work.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H074. "I thought these would feel basically the same"**
- Use when: Two options look similar but differ in use
- Best for: Fashion, Beauty, Home, Accessories
- Note: Good for texture, fit, weight, sound, or construction.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H075. "This is why I picked this version instead"**
- Use when: The buyer has multiple comparable options
- Best for: Any category
- Note: Give one clear reason for your choice.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H135. "I tried both so you can see the real difference"**
- Use when: Contrast effect + authority
- Best for: Product comparisons
- Note: Compare the features that matter during actual use.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H136. "One looks better, but the other works better"**
- Use when: Appearance-performance contrast
- Best for: Beauty, Fashion, Home
- Note: Clarify which priority matters for the intended buyer.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H137. "These seem identical until you use them"**
- Use when: Similarity disruption + curiosity
- Best for: Side-by-side reviews
- Note: Demonstrate the experience that separates them.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H138. "The cheaper one surprised me"**
- Use when: Price expectation reversal
- Best for: Affordable comparisons
- Note: Explain where the lower-cost option performs well.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook. Saying 'cheaper' or comparing price is fine; never say a price number.

**H139. "Here is who should choose each one"**
- Use when: Decision clarity + personalization
- Best for: Product comparisons
- Note: Match each option to a different buyer or need.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H140. "I would buy this one for __ and the other for __"**
- Use when: Context-based decision making
- Best for: Product comparisons
- Note: Show that the better choice depends on the use case.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H141. "The real difference is not what you think"**
- Use when: Information gap + contrast
- Best for: Product education
- Note: Reveal the less obvious distinction that affects the experience.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H142. "This one saves space, but this one saves time"**
- Use when: Trade-off framing + decision support
- Best for: Home, Travel, Organization
- Note: Compare two meaningful benefits without forcing one winner.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H143. "Same purpose, completely different experience"**
- Use when: Contrast effect + sensory anticipation
- Best for: Product comparisons
- Note: Describe how design or usability changes the result.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

**H144. "Before you choose between these, decide what matters more"**
- Use when: Value clarification + decision support
- Best for: Buying guides
- Note: Help the viewer identify the priority that should guide the choice.
- Grace note: Ralph OK 2026-10-05: a second product may be shown and its brand named on screen and in the script, overriding 'only our product' for this hook.

## Contrarian

**H076. "I did not need more __, I needed a better __"**
- Use when: The real problem is quality, fit, format, or suitability rather than quantity
- Best for: Fashion, Beauty, Home, Kitchen
- Note: Useful for reframing without sounding combative.

**H077. "Maybe the problem is not __"**
- Use when: The obvious explanation is not the whole story
- Best for: Beauty, Home, Fashion, Lifestyle
- Note: Only use when you have a credible alternative explanation.

**H078. "I stopped trying to make __ work for me"**
- Use when: A common approach does not fit your personal needs
- Best for: Fashion, Beauty, Home, Wellness
- Note: Keep it personal rather than declaring everyone else wrong.

**H106. "This product does not need another "you need this" video"**
- Use when: The product is saturated and needs fresher creative
- Best for: Established products
- Note: Follow with the angle you think is actually interesting.

## Outcome-Based

**H083. "This does one thing I really wanted it to do"**
- Use when: A single clear benefit is enough to justify interest
- Best for: Any category
- Note: Show that one thing.

**H084. "The entire reason I wanted this was __"**
- Use when: There is one dominant buying motivation
- Best for: Any category
- Note: Strong for focused videos. Do not add five more features.

**H086. "This is what I was hoping it would do"**
- Use when: The product delivers a clear expected result
- Best for: Home, Kitchen, Fashion, Beauty
- Note: Show the payoff right after the hook.

**H087. "This is exactly the kind of difference I wanted to see"**
- Use when: The visual result validates the purchase
- Best for: Beauty, Fashion, Home, Food
- Note: Works especially well with visible proof.

**H088. "This is what I mean when I say I wanted __"**
- Use when: The product gives a visual example of a desired quality
- Best for: Fashion, Beauty, Home, Food
- Note: Fill with something concrete like "soft structure," not vague "quality."

## Sensory

**H089. "I do not think the picture really shows how __ this is"**
- Use when: A tactile, visual, dimensional, or size detail does not translate in listing photos
- Best for: Fashion, Beauty, Home, Food
- Note: Close-up footage is essential.

**H090. "You can actually hear the difference"**
- Use when: Sound is part of the selling point
- Best for: Electronics, Home, Kitchen, Toys
- Note: Let viewers hear it rather than narrating over it.

**H091. "Look at the texture on this"**
- Use when: Texture itself is compelling
- Best for: Food, Beauty, Fashion, Home
- Note: Do not bury the visual under a long hook.

**H092. "This is one of those products where the close-up matters"**
- Use when: Small visual details influence the purchase
- Best for: Beauty, Fashion, Food, Home
- Note: Get close enough for the viewer to inspect it.

**H093. "I wish you could feel this through the screen"**
- Use when: Texture or softness is unusually noticeable
- Best for: Fashion, Bedding, Beauty, Home
- Note: Describe your own tactile impression after showing it.

## Product Demo

**H094. "Watch what happens when I __"**
- Use when: The product has a simple satisfying demonstration
- Best for: Kitchen, Home, Beauty, Electronics
- Note: Let the action create curiosity.

**H095. "I am just going to show you because explaining it is harder"**
- Use when: The product difference is easier to demonstrate than describe
- Best for: Any demonstrable product
- Note: Excellent 3.0 hook because visual proof leads.
- Used in: super-blanky-v2 (2026-10-05)

**H096. "This makes more sense if I show you"**
- Use when: The benefit sounds abstract until demonstrated
- Best for: Any category
- Note: Get into the demo quickly.

## Curiosity

**H097. "Here is the part that made me stop scrolling"**
- Use when: A visible or unusual feature caught your attention
- Best for: Product discoveries, Fashion, Beauty, Home
- Note: Reveal the detail quickly. Do not manufacture suspense.

**H098. "I had to look twice when I saw __"**
- Use when: A genuinely unusual detail deserves a closer look
- Best for: Fashion, Beauty, Home, Accessories
- Note: Name what caught your eye.

**H099. "At first I thought this was just __"**
- Use when: The product initially appears ordinary but has a meaningful difference
- Best for: Any category
- Note: The reveal needs to be worthwhile.

**H100. "I almost missed what was different about this"**
- Use when: The differentiator is subtle
- Best for: Any category
- Note: Zoom in or demonstrate the exact difference.

**H101. "There is one detail here that changes the whole thing"**
- Use when: One feature meaningfully changes the use or appeal
- Best for: Any category
- Note: Do not delay the reveal too long.

**H102. "This looked pretty normal until I noticed __"**
- Use when: A hidden or less-obvious feature is the selling point
- Best for: Any category
- Note: Specificity keeps this from becoming clickbait.

## Social Proof

**H103. "I did not understand why people liked this until I saw __"**
- Use when: A popular product has one concrete feature that explains its appeal
- Best for: Established products
- Note: Use popularity as context, not proof that the product is good.

**H104. "Now I understand why this keeps showing up on my feed"**
- Use when: You personally discovered what makes a trending product interesting
- Best for: Established TikTok Shop products
- Note: Immediately explain the actual reason.

## Objection

**H112. "I was worried this would __"**
- Use when: You had a real concern before trying or seeing the product
- Best for: Fashion, Beauty, Home, Electronics
- Note: Only use objections you genuinely had.

**H113. "My biggest question before ordering was __"**
- Use when: A buyer concern almost prevented purchase
- Best for: Any category
- Note: Answer it with visual proof whenever possible.

**H114. "The one thing I was unsure about was __"**
- Use when: You want to address a realistic hesitation
- Best for: Any category
- Note: Keep the concern specific.

**H115. "I thought this might be too __ for me"**
- Use when: A style, fit, scent, size, or intensity concern existed
- Best for: Fashion, Beauty, Fragrance, Home
- Note: Explain what changed your mind without overselling.

## Time Pressure

**H130. "This is going to matter once __"**
- Use when: Future relevance + curiosity
- Best for: Seasonal and lifestyle content
- Note: Connect the product to an approaching situation.

**H131. "Before the season changes, look at this"**
- Use when: Seasonal anticipation + preparedness
- Best for: Fashion, Beauty, Home
- Note: Explain how the product supports the transition.

**H132. "You will want this ready before __"**
- Use when: Future pacing + convenience
- Best for: Events, Travel, Weather
- Note: Fill the blank with a real moment of need.

**H133. "This is the kind of thing you buy before you are desperate"**
- Use when: Problem prevention + urgency
- Best for: Household and preparedness products
- Note: Frame early action as practical rather than fear-based.

**H134. "Put this on your list before __"**
- Use when: Planning cue + anticipation
- Best for: Shopping guides
- Note: Connect the recommendation to a clear timeline.

## Simple Fix

**H145. "This takes one extra step out of my routine"**
- Use when: Friction reduction + habit support
- Best for: Routines and everyday products
- Note: Show the exact step the product removes.

**H146. "Here is a faster way to deal with __"**
- Use when: Cognitive ease + problem solving
- Best for: Tutorials and quick wins
- Note: Demonstrate the shortcut clearly.

**H147. "One small switch made __ much easier"**
- Use when: Low-friction change + relief
- Best for: Routines and habits
- Note: Keep the solution realistic and easy to repeat.

**H148. "Keep this where you always __"**
- Use when: Environmental cue + habit formation
- Best for: Organization and everyday essentials
- Note: Connect product placement to consistent use.

**H149. "Use this when you do not have time to __"**
- Use when: Time pressure relief + convenience
- Best for: Busy routines
- Note: Position the product as a practical backup or shortcut.

**H150. "This is the simplest solution I have found for __"**
- Use when: Simplicity bias + authority
- Best for: Problem-solving products
- Note: Explain why the solution requires less effort.

**H151. "Add this one step before you __"**
- Use when: Action cue + process improvement
- Best for: Tutorials and routines
- Note: Show how the added step prevents a larger problem.

**H152. "This makes it easier to remember to __"**
- Use when: Habit cue + cognitive ease
- Best for: Wellness and organization
- Note: Connect the product to a visible or automatic reminder.

**H153. "The quickest way to make __ feel more manageable"**
- Use when: Overwhelm reduction + low friction
- Best for: Home, Routines, Organization
- Note: Break the problem into one approachable action.

**H154. "This is such an easy upgrade for __"**
- Use when: Low commitment + improvement
- Best for: Beauty, Fashion, Home
- Note: Show how a small change improves the overall experience.
