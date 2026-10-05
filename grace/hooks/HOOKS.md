# Grace hook library

Fill-in-the-blank hook templates for Grace's videos. Source of truth: `hooks.json` (edit there, then run
`python3 grace/hooks/build.py`). Batches: B1 (2026-10-05, Ralph's sheet screenshot, rows 2-28 (27 hooks)).

## How to use (every Grace job)
- Every Grace script picks its spoken hook options from here first (plus the coach-modeled hooks, PLAYBOOK §3); name the hook id in the plan's line sources (e.g. `B1-15`).
- Fill every blank with a concrete moment from the product research, never a broad problem.
- Spoken lines are stored verbatim from the sheet; Grace says them with contractions ("I can't stand", "I'm very particular") after the humanizer pass.
- The line after the hook answers or proves it on screen right away (demo, close-up, the back/side/pocket shot).
- Spread hook types across a product's videos (no two videos of one product on the same id; TikTok flags repeats).
- These are spoken hooks. On-screen text stays curiosity-only, 5-7 words, and is burned in only on Ralph's yes.
- Log which id each finished video used (`used_in`) so results can show which hook types win.

## Pick by category

- **Accessories:** B1-01, B1-03, B1-08, B1-14, B1-21
- **Any category:** B1-23
- **Any product:** B1-27
- **Bags:** B1-20, B1-21
- **Beauty:** B1-01, B1-02, B1-03, B1-04, B1-05, B1-06, B1-08, B1-10, B1-11, B1-12, B1-13, B1-15, B1-16, B1-18, B1-19, B1-24, B1-25, B1-26
- **Beauty tools:** B1-22
- **Convenience products:** B1-09
- **Electronics:** B1-14, B1-19, B1-25, B1-26
- **Everyday problem-solving products:** B1-07
- **Fashion:** B1-01, B1-02, B1-03, B1-04, B1-10, B1-11, B1-12, B1-13, B1-15, B1-16, B1-17, B1-18, B1-19, B1-20, B1-21, B1-22, B1-24, B1-25, B1-26
- **Food:** B1-11, B1-13, B1-15
- **Home:** B1-01, B1-02, B1-03, B1-04, B1-05, B1-06, B1-08, B1-09, B1-10, B1-11, B1-12, B1-13, B1-14, B1-15, B1-17, B1-18, B1-19, B1-22, B1-24, B1-25, B1-26
- **Kitchen:** B1-02, B1-04, B1-06, B1-08, B1-09, B1-12, B1-14, B1-16, B1-17, B1-18, B1-24
- **Lifestyle:** B1-10
- **Organization:** B1-06
- **Pets:** B1-04, B1-17
- **Problem-solving products:** B1-05
- **Shapewear:** B1-20
- **Wellness:** B1-02, B1-16

## Observation

**B1-01. "This is the part I actually care about"**
- Use when: You want to lead with a specific detail, feature, or payoff that matters more than the obvious selling point.
- Best for: Fashion, Beauty, Home, Accessories
- Note: Helps the creator center the video around one meaningful detail instead of trying to explain everything.

**B1-05. "I did not realize how much __ bothered me until I stopped dealing with it"**
- Use when: The benefit is easier to appreciate after experiencing the alternative.
- Best for: Problem-solving products, Home, Beauty
- Note: Works best when you can visibly show what changed.

**B1-08. "This is such a small thing, but it annoys me every single time"**
- Use when: You're talking about a small, recurring annoyance that isn't dramatic, but happens often enough to make the product feel useful.
- Best for: Home, Kitchen, Accessories, Beauty
- Note: Small frustrations can be more believable than dramatic ones.

**B1-23. "The first thing I checked was __"**
- Use when: There is one feature buyers are likely to inspect first.
- Best for: Any category
- Note: Name a real buying concern.

## Routine

**B1-02. "I keep reaching for this more than I expected"**
- Use when: You're showing a product that has quietly become part of your normal day, outfit, setup, or routine.
- Best for: Fashion, Beauty, Home, Kitchen, Wellness
- Note: Feels natural and experience-based without needing a dramatic transformation or problem.

## Emotional Outcome

**B1-03. "This just makes everything feel a little more put together"**
- Use when: You're selling the feeling the product creates rather than a major functional result.
- Best for: Fashion, Beauty, Home, Accessories
- Note: Gives creators a softer way to talk about aesthetic or emotional payoff without overhyping the product.

## Problem Callout

**B1-04. "One thing I cannot stand is __"**
- Use when: The product solves a very specific annoyance people immediately recognize.
- Best for: Home, Kitchen, Beauty, Fashion, Pets
- Note: Be specific about the annoying moment. The blank should not be a broad problem.

**B1-06. "I have been putting up with this for way too long"**
- Use when: The buyer may have normalized an irritating problem.
- Best for: Home, Kitchen, Beauty, Organization
- Note: Name the actual thing you were putting up with quickly.

**B1-07. "If you also hate when __, look at this"**
- Use when: The product solves minor everyday friction.
- Best for: Everyday problem-solving products
- Note: Fill the blank with a concrete situation, not a vague pain point.

## Problem/Solution

**B1-09. "Why did nobody make this easier sooner?"**
- Use when: The solution feels obvious once viewers see it.
- Best for: Convenience products, Kitchen, Home
- Note: Let the demonstration answer the question.

## Confession

**B1-10. "I am done pretending this does not bother me"**
- Use when: The problem is relatable but people rarely say it out loud.
- Best for: Fashion, Beauty, Home, Lifestyle
- Note: Keep the tone playful rather than dramatic.

## Preference

**B1-11. "I know this is minor, but I really do care about __"**
- Use when: A specific preference drives the purchase.
- Best for: Fashion, Beauty, Home, Food
- Note: The specificity is the hook.

**B1-12. "Apparently I have very strong opinions about __"**
- Use when: The product connects to a personal standard.
- Best for: Fashion, Beauty, Kitchen, Home
- Note: Follow immediately with the preference.

**B1-13. "I am very particular about __"**
- Use when: The viewer may share a strong product preference.
- Best for: Beauty, Fashion, Food, Home
- Note: Explain what your standard actually is.

**B1-14. "I do not need __ to be fancy. I just need it to __"**
- Use when: The buyer values function over bells and whistles.
- Best for: Home, Kitchen, Electronics, Accessories
- Note: The second blank should be the real payoff.

## Contrast

**B1-15. "I like __, but I do not like __"**
- Use when: The product gives the desired benefit without a common downside.
- Best for: Fashion, Beauty, Food, Home
- Note: One of the strongest structures for showing a tradeoff.

**B1-16. "I want __ without having to __"**
- Use when: The product removes an unwanted tradeoff.
- Best for: Fashion, Beauty, Kitchen, Wellness
- Note: Make both sides specific and believable.

**B1-18. "I would rather __ than spend another day __"**
- Use when: The product lets the buyer avoid something frustrating.
- Best for: Fashion, Beauty, Home, Kitchen
- Note: Keep the comparison natural, not exaggerated.

## Humor

**B1-17. "I am willing to deal with a lot, but not __"**
- Use when: A small frustration has become the breaking point.
- Best for: Home, Kitchen, Fashion, Pets
- Note: Best when the annoyance is visually obvious.

## Buyer Question

**B1-19. "This is the part I wanted to see before I bought it"**
- Use when: The listing or other videos do not clearly answer an important purchase question.
- Best for: Fashion, Beauty, Home, Electronics
- Note: Show the answer immediately after the hook.

**B1-22. "I needed to know how this looked from the side"**
- Use when: The side profile may reveal fit, shape, bulk, or coverage.
- Best for: Fashion, Beauty tools, Home
- Note: Show rather than over-explain.

**B1-24. "Here is what I would want someone to show me before I ordered this"**
- Use when: The product has several details that matter more than the listing.
- Best for: Fashion, Beauty, Home, Kitchen
- Note: Pick one or two details for this video, not every feature.

**B1-25. "I kept looking for a video that showed __"**
- Use when: Existing content leaves an important question unanswered.
- Best for: Fashion, Beauty, Home, Electronics
- Note: Great opportunity for search-friendly content.

## Question

**B1-20. "Okay, but what does the back actually look like?"**
- Use when: The back view matters to the buying decision.
- Best for: Fashion, Bags, Shapewear
- Note: Excellent for products where creators usually only show the front.

**B1-21. "Does it actually have usable pockets?"**
- Use when: Pocket size or placement matters.
- Best for: Fashion, Bags, Accessories
- Note: Put your hands or real items inside them.

**B1-27. "If you are wondering whether __, here you go"**
- Use when: You can directly answer a likely buyer question.
- Best for: Any product
- Note: Demonstrate the answer instead of talking around it.

## Reassurance

**B1-26. "Before you buy this, look at __"**
- Use when: The buyer needs to inspect one important detail.
- Best for: Fashion, Home, Beauty, Electronics
- Note: Avoid fear-based wording. Make it useful.
