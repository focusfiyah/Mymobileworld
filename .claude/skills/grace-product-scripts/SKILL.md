---
name: grace-product-scripts
description: Write short talking-head TikTok Shop scripts for Ralph's client Grace for any non-clothing product (first job, the Cleanwaste Wag Bag, 2026-09-30), modeled on a reference TikTok that is doing well. Analyses the reference (transcript, frames, beats), checks product facts, writes 5 different angles of about 30 seconds each, runs them through Humanizer, and delivers a phone-friendly Claude doc plus a PDF Ralph can send Grace on WhatsApp. Use when Ralph says Grace needs scripts, angles or hooks for a product, sends a TikTok for Grace to copy the feel of, or asks for "different angles" for her. For clothing (jeans, dresses, tops), use grace-fashion-ads.
---

# Grace product scripts

Grace is Ralph's client. She films herself; Ralph edits her takes (ugc-take-combos skill). This skill decides what she
says. The output is 5 short scripts, each built on a different angle, in the voice of a reference video that is
already working on TikTok. `examples/wag-bag.md` is the approved finished doc: match its shape and length.

**Read `grace/PLAYBOOK.md` in focusfiyah/Mymobileworld first.** It is the one source for Grace's rules, and where it
differs from this file, the playbook wins. Every script follows her structure (Ralph, 2026-10-02): curiosity-loop hook →
pain-point body → selling point and/or solution body → FOMO and/or urgency CTA (real urgency only).

## Ralph's format (settled 2026-09-30, don't re-ask)

- **5 angles, about 30 seconds each** = 80 to 100 spoken words. HOOK / BODY / CTA labeled, because Grace films them as
  separate takes; 2 alternate hooks per angle so Ralph can combine takes into more videos.
- **Talking head only.** Grace to camera, product in her hands the whole time, like the reference. At most one
  optional `[Insert: ...]` per angle: a 2 to 3 second close-up Ralph lays over her voice while she keeps talking.
- **No skits**, no second person, no storytime that only works if a specific event really happened.
- **No "questions for Grace" section.** Facts only she has stay as blanks in the script: `[price]`, a test result
  `[__]`, `[your con]`. Write downsides as plain tips backed by reviews ("seal it right away, a used one still smells
  if it sits"), never as her experience.
- Each angle gets its own on-screen headline + label (the reference style: a headline with an emoji plus a small
  label), different per angle so TikTok treats the posts as distinct.
- **Deliverables:** a Claude doc for Ralph, then a PDF of it. Grace has to sign in to open a doc link, so the PDF is
  what Ralph sends her on WhatsApp. No local markdown copy.

## Workflow

### 1. Analyse the reference (free)

```
python3 scripts/analyze_reference.py <video.mp4> <out_dir>
```

Writes `transcript.txt` (sentence timestamps, ElevenLabs scribe_v2 through the proxy, no key needed) and 1 fps
contact sheets `sheet1.jpg`, `sheet2.jpg` (6x4 tiles). Look at the sheets. Map the beats: time, beat, what she says,
what she does with the product, on-screen text layers. Write down why it works in plain terms, and what it skips
(the Wag Bag reference described the gel but never showed it, so angle 5 became the gel test).

The reference transcript is also the voice sample for the Humanizer pass: casual, spoken, "gonna", short sentences.

### 2. Check the product facts

WebFetch the official product page first, then reviews or forum threads for the common complaint, and one
competitor. Only verified facts go in the scripts. Correct the reference's mistakes instead of copying them (the Wag
Bag reference said "hand sanitizer"; the kit has a hand wipe). Brand claims are said as the box's claim ("the box
says it holds up to 32 ounces"). No scarcity unless it's true: "don't wait for a storm on the news" instead of "they
sell out". No invented numbers (uses per bag, gel time).

### 3. Write the 5 angles

The mix that worked for the Wag Bag:

1. **Reference remix:** the reference's exact beats (list hook with a twist, the gap nobody talks about, kit in hand,
   value vs the cheap alternative, joke CTA) in new words.
2. **Timely situation:** a season or event that makes the product urgent now (power outage, hurricane season).
3. **A specific moment:** one scene the buyer has lived ("next exit is 30 miles and somebody in the back has to go").
4. **Humor / deadpan:** the product's awkwardness as the joke ("everybody laughs at the poop bags until the water's off").
5. **Proof the reference skipped:** a test Grace does off camera first, then shows the result to camera and reports
   only what she saw.

Rules carried over from grace-fashion-ads: pain or moment first in the hook; value before price (how many, how long
it lasts, vs the alternative); one honest downside said calmly; no "so cute", "obsessed", "you need this". CTA points
to the orange cart. Use clean words ("poop", not the reference's swearing) so the videos can also run as Spark Ads,
since TikTok's ad policy doesn't allow profanity; mention this to Ralph once.

### 4. Humanizer pass

Load the humanizer skill and run it on the scripts with the reference transcript as the voice sample. The usual
survivors to check: not-X-but-Y lines ("ends on a joke, not a sales pitch"), one-line closers, forced triads, em
dashes. Spoken rhythm and fragments in the scripts are fine; that's the voice.

### 5. Deliver

Build the doc with the docs connector (load the docs skill; skeleton first, then fill one section per call). Keep it
readable on a phone: no wide tables, short bullets, a 3-line intro. Sections, in order:

- Intro: what it is, `[brackets]` = do or fill in, `[Insert]` = optional close-up, film hook/body/CTA separately
- Why the reference video works (5 or 6 bullets)
- Quick rules (4 bullets)
- Angle 1 to 5 (one-line intro, on-screen headline + label, HOOK, BODY, insert, value line, CTA, 2 alternate hooks)
- Shot list: one main talking-head setup (phone vertical on a stand at eye level, window light, waist up, product in
  hand), take counts, the optional inserts
- What's in the box: 4 or 5 verified facts + one link to the official product page

Then export the PDF (`export` tool, format pdf, paper letter). The result is too large to print, so it lands in a
tool-results file: decode `data.bytes_b64` into `Grace <Product> scripts.pdf` in the working directory, render a page
with pymupdf to check it, and send it with SendUserFile. Give Ralph the doc link and the PDF.

## Gotchas

- `ffmpeg` isn't installed in the cloud container; the script uses the imageio-ffmpeg binary (`pip install
  imageio-ffmpeg`). pymupdf (`pip install pymupdf`) renders PDF pages for checking; pdftoppm isn't there.
- TikTok downloads (ssstik) can end in a ~3 s logo card. It isn't part of the ad, so leave it out of the timing.
- If Ralph edits the doc after the PDF is sent, re-export; the PDF doesn't update itself.
