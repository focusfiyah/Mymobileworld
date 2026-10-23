# Scene prompt template (from the Pixar to Clawd prompt pack)

The structure of the prompt pack's 620-word prompt, for a Day One intro, sting or end card. Fill only the BRAND
block per piece; the rest refers to it by name. First used 2026-10-23 for the Day One sting: the filled prompt is
Dayone-ai `intro/SCENE.md`, the renderer `intro/intro.py` (Playwright frames + numpy sound from one timeline) and its
checks `intro/check.py`; copy those for the next one. Blender is not in the cloud container; HyperFrames installs
with Dayone-ai `setup.sh`. Any paid generation it leads to needs Ralph's OK with the cost first.

```text
BRAND
HERO: <the recurring character or object, by shape, size and exact colour, e.g. the D1 mark as a chunky 3D token,
      ink #141414 with an accent edge>
BAND: <a format everybody knows, described by its parts, never by its name; our own type and props, no logo files>
RESULT: <what the hero changes by the end, e.g. the format's title becomes the tool's name in its brand colour>
SET: <sizes and limits: what must stay in frame for every change, background, floor, horizon>

FORMAT: <tool (HyperFrames / Blender), resolution rendered and delivered, fps, length, BPM so one beat = N frames,
        loops or not>. One timeline file holds every event in seconds; picture and sound both read it.

BEATS (seconds):
0-2   the familiar format plays straight (recognition first)
2-3   the hero interrupts its famous beat
3-7   one change per beat; the end of each change launches the next
7-9   the payoff, whole in frame, on a downbeat
9-12  a loser or a button that leads back to frame 1

CAMERA: <lens, height, moves; go wide for every change so the whole word or result stays in frame>
LOOK: <key, fill, rim, materials; the brand colour must measure <hex> on the lit surface; bright, no muddy grade>
CHECKS: 24 half-res stills as two contact sheets first; measure exposure (p99, clipped %) and the brand colour;
        two full-res frames timed; only then the full render.
```

Sound, as one more prompt on the same timeline: synthesize everything (no samples, no borrowed melody), land each
hit on its frame, pan by position, stop the music dead before the payoff, give each change the next note of a
scale, master to about -14 LUFS with a true peak under -1.5 dBFS, then check loudness per quarter second.
