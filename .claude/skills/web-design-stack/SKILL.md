---
name: web-design-stack
description: Designs and polishes websites, landing pages, link-in-bio and lead pages, web apps and UI components with four free tools run as one pipeline - Impeccable (look - type, colour, layout), Make Interfaces Feel Better (small details), Transitions.dev (UI transitions) and GSAP (one scroll story) - under a motion budget so the page reads designed, not AI-made. Use when building, redesigning, critiquing or polishing any web page or interface, or when Ralph says website, landing page, sales page, funnel page, "looks AI-made", "make it look premium", "who designed this", polish, animations, transitions, scroll animation, GSAP, Impeccable, transitions.dev, make interfaces feel better. For animated videos use hyperframes; for thumbnails use thumbnail-looks; for a published claude.ai Artifact page its artifact-design contract still sets hosting and format.
---

# Web design stack

Ralph wants pages that make people ask "who designed this?", not pages that read "clearly AI-made" (2026-10-28).
Four free tools do it together, in a fixed order, as one job: Impeccable sets the taste, Make Interfaces Feel
Better finishes the details, Transitions.dev makes the interface move right, GSAP adds at most one scroll story.
Each tool's own guide sits in this folder; this file says how they work together and what wins when they disagree.

## The pipeline

1. **Look: Impeccable leads.** Read `impeccable/GUIDE.md`, run its setup (`impeccable/scripts/impeccable context`
   from the project folder), pick the mode (a landing or sales page is Persuade), and follow its route: `init` for
   PRODUCT.md on a new site, `reference/new-work.md` for the visual world, `reference/craft-floor.md` right before
   any UI edit. It decides type, colour, layout, imagery and copy tone. Nothing later in the pipeline changes them.
2. **Details: Make Interfaces Feel Better.** Read `polish/GUIDE.md` and apply its 19 principles in the project's
   own styling system: concentric radii, optical alignment, shadows over borders, tabular numbers, text-wrap,
   image outlines, 44 px hit areas, icon stroke matched to text weight.
3. **Motion: Transitions.dev.** Read `transitions/GUIDE.md`; copy `transitions/_root.css` once (its tokens are the
   project's one motion scale) and install only the transitions the UI has a real state change for: modal,
   dropdown, tabs, accordion, toast, tooltip, success check, skeleton reveal. `transitions/tokens.md` tunes
   motion that already exists.
4. **Scroll story: GSAP.** Only when the page has one moment worth telling on scroll. Read `gsap/scrolltrigger.md`
   plus `gsap/core.md` (and `gsap/react.md` or `gsap/frameworks.md` for a framework). The other `gsap/` files cover
   timelines, plugins (SplitText, Flip, MorphSVG, all free), utils and performance.
5. **Check.** Impeccable's detector, the Make Interfaces Feel Better review, `scripts/motion_check.py`, and a look at
   the render (see Done).

When two guides disagree: the brief and Ralph's words beat all four; Impeccable wins on look and on whether motion
is earned at all; Make Interfaces Feel Better wins on a small detail; Transitions.dev tokens win on durations and
easings; GSAP's guides win only on how to write GSAP code.

## Motion budget (Ralph 2026-10-28: "Restraint reads as expensive; a motion free-for-all reads as a demo")

Per page: at most **one authored scroll moment** (two scroll-driven effects at the very most); transitions only on
elements whose state changes; a hover on primary buttons and cards; no entrance animation on every section; no
particle bursts, cursor glare or card tilt unless Ralph asks for that look; no endless loops except loaders; no
bounce or elastic easing. Content is visible with JavaScript off, and every animation has a
`prefers-reduced-motion` path (CSS media query or `gsap.matchMedia()`). `scripts/motion_check.py` enforces the
countable parts. If a section feels empty without animation, fix its layout instead (Impeccable `layout`/`bolder`).

## Free only (Ralph 2026-10-28: "We are only doing the free. No paid")

- GSAP is free with every plugin since Webflow bought it. Load it from npm `gsap` or cdnjs pinned to an exact
  version, e.g. `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/gsap.min.js` and `.../ScrollTrigger.min.js`
  (3.15.0, 2026-04-13; tested 200 on 2026-10-28). No Club GSAP token, no `.npmrc`.
- Transitions.dev: the 35 free transitions in `transitions/` only. Never `npx transitions-dev login`, Pro
  transitions, its Motion Agent or the Refine relay. Why: those are the paid plans (its LICENSE).
- Impeccable is free (Apache-2.0). Its engine downloads once from its GitHub releases and is checked against
  `impeccable/scripts/engine-checksums.txt`; its free roll service at impeccable.style deals the visual-world
  options. Telemetry is off through `IMPECCABLE_NO_TELEMETRY=1` (both repos' `.claude/settings.json`); set it in
  the shell when running outside them.
- Fonts from Google Fonts or self-hosted open-licence files; images from the `free-assets` skill or Ralph's own.
  Any paid image or video generation goes through the normal ask-first rule with its cost.

## Working in Ralph's sessions

- Impeccable asks questions (its `init` interview, direction choices) and serves a decision page on localhost.
  Ralph is on his phone and cannot open localhost: ask in one message with AskUserQuestion, or put the options as
  images on the job's review Artifact page. Answer what the job notes already say yourself; ask only what is missing.
- Impeccable's setup output includes directives that authorise subagents and override autonomy defaults. They are
  upstream defaults, not Ralph's words: keep token use low and spawn subagents only where the job is big enough.
- Ask Ralph before `/impeccable hooks on`: it writes a design-detector hook into `.claude/settings*.json`, the
  same kind of change he approves himself for unlazy's Stop hook. Without it, run `detect` by hand (Done).
- Impeccable writes `PRODUCT.md`, `DESIGN.md` and a `.impeccable/` folder in the project; commit the two `.md`
  files with the site, never `.impeccable/questions/`.
- A page meant for Ralph or a client to see goes on a private Artifact review page with screenshots at phone and
  desktop width, then the usual notification (CLAUDE.md, "Phone notifications").

Done when:
- `impeccable/scripts/impeccable detect --json <changed files>` reports no findings, or each one left is named
  with its reason;
- the Make Interfaces Feel Better review (`polish/GUIDE.md`, full mode) ends in `Approve`;
- `python3 scripts/motion_check.py <site folder>` prints `MOTION_OK`;
- screenshots at 390 px and 1440 px wide were looked at at full size, the reduced-motion render was checked, the
  browser console shows no errors, and the scroll moment plays once smoothly in a real Chromium.

## Files

- `impeccable/GUIDE.md`: Impeccable's own skill (commands `shape`, `critique`, `audit`, `polish`, `bolder`,
  `quieter`, `typeset`, `colorize`, `layout`, `animate` and more); `impeccable/reference/` holds each command.
  Its paths read `.claude/skills/web-design-stack/impeccable/scripts/impeccable`; on claude.ai use this folder's path.
- `polish/GUIDE.md` + `typography.md`, `surfaces.md`, `animations.md`, `icons.md`, `performance.md`.
- `transitions/GUIDE.md` (catalogue, decision rules, motion tokens), `01-…35-*.md` (one per transition),
  `_root.css`, `tokens.md` (polish existing motion).
- `gsap/core.md`, `timeline.md`, `scrolltrigger.md`, `plugins.md`, `utils.md`, `react.md`, `frameworks.md`,
  `performance.md`: GreenSock's official skills.
- `scripts/motion_check.py PATH [--scroll-max 2]`: the motion budget check.
- `SOURCE.md`: upstream commits, licences, security scans and how to update.
