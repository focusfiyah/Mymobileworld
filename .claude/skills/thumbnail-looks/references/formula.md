# The prompt pack method, mapped to thumbnails

Source: "Prompt Pack: Pixar to Clawd" (Clawd Motion Lab; the film, lamp rig and sound written by Claude from one
620-word prompt), a 6-page PDF Ralph shared on 2026-10-23. The film: a famous studio-logo intro plays straight for
two seconds, then Clawd lands on the lamp's switch, puts it to sleep and hops along the letters until PIXAR reads
CLAWD. Nothing in it is copied; it is all built from a description of the parts.

Policy background (checked 2026-10-23): YouTube renamed "repetitious content" to "inauthentic content" in July
2025, and a July 2026 update lists generic, repetitive or template-based content as not monetizable (TechCrunch,
2026-07-20, "YouTube clarifies policies around AI slop"). Nothing found names thumbnails specifically; the policy
judges the channel as a whole, and identical thumbnails are the most visible sign of a template.

## The six rules of the formula

| Prompt pack rule | What it meant in the film | What it means for a thumbnail look |
|---|---|---|
| Recognition first | Two seconds of the intro played straight, so nobody doubts what they are watching | The tool's own name and brand colour (sampled from its page) and its real page or result lead the frame; viewers search the brand |
| Flip the famous beat | The lamp gets switched off and Clawd takes its beat | A familiar format (the band) carries our twist: the tool's result inside it |
| Same letter count | PIXAR and CLAWD are both five letters, one hop per letter | Fit the words to the frame: each text box has a size floor that still reads on a phone, and the title is cut until it fits, never squeezed past it |
| Keep the word in frame | The camera goes wide for the swaps; a payoff seen by half is no payoff | The result is whole on screen: `focus` (or the busiest part of the page) frames it, the loupe band magnifies it |
| A loser for the loop | The lamp storms off and hops back in on frame 1 | For a Short or a sting: the last beat leads back into the first |
| Measure, don't guess | Exposure percentiles, the orange in RGB, loudness per quarter second | The sameness score, the text-fit report and the sampled accent, printed for every candidate |

## Habits worth keeping

- **One block changes.** The film's prompt names HERO, BAND, RESULT and SET once and the rest only refers to
  them; swapping the block makes a new film. Our `look` block is that block: change it and the thumbnail changes,
  the rules around it stay.
- **Describe the famous thing by its parts, not its name.** "A magazine cover: masthead, cover photo, one cover
  line" reads at once and copies no one's design or trademark. Never name or imitate a real brand's layout.
- **Stills before the expensive render.** The film checked 24 half-res stills as contact sheets before any GPU
  time. Here: the candidate sheet before the final, the one-clip test before a batch.
- **Follow-ups carry numbers.** Each of the film's four notes said what was measured and what to change ("key
  210 to 55 W, now p99 231, 0.00% clipped"). Write review notes the same way: "shared 0.46 with motion-test,
  cream background; switch band".
- **One timeline drives picture and sound.** Every hop, swap and sound hit sat on a 120 BPM grid read from one
  `timeline.py`, and each letter pop played the next note of a scale. For an animated intro or sting, keep one
  timeline file that both the motion and the sound read, so hits land on their frame.
- **Silence is a hit.** After the click the music stopped for 1.4 s; the quiet made the next beat land. Useful in
  a cold open: cut the bed under the result reveal.
- **Different means a different layout, not new words and a new colour.** The first Day One intro sting (2026-10-23)
  kept one split-flap board and swapped only the tool name and colour; Ralph: "No they all look the same". The
  thumbnails passed because each one uses a different band. Anything meant to vary per video changes its format,
  not just its fill.
