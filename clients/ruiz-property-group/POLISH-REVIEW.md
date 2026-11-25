# Polish review (G6), Make Interfaces Feel Better, full mode, 2026-11-25
Checked against the 19 principles in the stack's polish guide, on index, we-buy-houses, property-management at 390 and 1440.
- Surfaces: borders on cards replaced by layered shadows (--shadow, --shadow-lift); image outlines 1px at 10% black on every photo class.
- Press feedback: .btn, menu button scale .96 on :active; hover lift 2px on buttons and 4px on the four-ways cards.
- Hit areas: every link, button and input at least 44px (nav links, footer links, menu items, FAQ heads 60px, inputs 48px).
- Type: text-wrap balance on headings, pretty on paragraphs, tabular numerals on phone numbers and step numbers, antialiased.
- Browser details themed: ::selection brick, caret brick, scrollbar brick, focus ring 3px (white on dark sections), theme-color meta.
- Motion: exact Transitions.dev tokens (dropdown menu, accordion, success check, stagger rise on hero); one GSAP moment (steps line draws on scroll); all of it behind prefers-reduced-motion (verified: h1 opacity 1 with reduced motion).
- States verified in the browser: menu opens/closes (button, Escape, outside click, link tap), FAQ opens one at a time, form shows validation then the success check, no console errors.
- Mobile: sticky call bar, safe-area padding, one column, no sideways scroll (pages_check).
Known, accepted: Impeccable "cramped-padding" x15 are full-bleed sections whose inner .wrap supplies the gutter (false positives).
Verdict: Approve.
