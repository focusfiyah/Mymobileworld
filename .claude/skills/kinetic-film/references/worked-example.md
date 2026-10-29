# Worked example: Kaiju Postal, a game teaser scored with Scenario MCP

The paid Scenario route end to end, from the upstream skill. Ralph's free route is in SKILL.md.

Goal: a 24-second teaser for an indie game about a courier delivering mail in a city of giant monsters:
kinetic type on a 172 BPM drum and bass track, two pieces of key art cut in on the drop, a door-knock gag
on the beat cuts, the title card on the last hit.

1. **Connect.** `teams_list`. If several teams or projects come back, ask which one to use and pass its
   `team_id` and `project_id` to every later call.

2. **Write the beat sheet (local, free).** 68 beats at 172 BPM (23.7 s): beats 0-8 type (a charge, then
   THE CITY / HAS NEW / VERY BIG NEIGHBOURS. / THEY STOMP.), 8-16 key art 1 on the drop, 16-24 type
   ending in a zoom through the D of DELIVER., 24-32 key art 2, 32-43 a fly-through (DODGE THE BIG FEET.),
   43-51 the 3D title YOU ARE THE POST., 51-57 the knock gag, 57-68 the title card.

3. **Music at an exact tempo.** `recommend`:

   ```json
   { "capability": "txt2audio", "prompt": "Instrumental drum and bass for a playful video game trailer at a fixed 172 BPM, a tense intro, then a huge drop, punchy kick on every downbeat, no vocals", "limit": 4 }
   ```

   Prefer a model whose schema has a tempo (`bpm`) input and an instrumental switch: a tempo you set beats a
   tempo you hope for. `model_schema_get`, then a dry run with the full parameters, for example:

   ```json
   { "model_id": "<id from recommend>", "dry_run": true, "parameters": { "prompt": "High-energy drum and bass for a playful video game trailer, 172 BPM. Eight bars of tense intro with filtered drums and a rising synth, then a huge drop: punchy kick on every downbeat, rolling breakbeats, growling reese bass, bright brass stabs. No vocals.", "instrumental": true, "duration": 40, "bpm": 172, "numOutputs": 2 } }
   ```

   Tell the user the price and wait for a go. Run, `jobs_wait`, `asset_download`, `curl -L -o audio/music_a.mp3 "<url>"`.
   Then measure each take:

   ```bash
   python3 $K/scripts/beat_grid.py audio/music_a.mp3 --bpm 172
   ```

   Pick the take with the clearest grid and the strongest drop (`drops[].rise`). In the build, take B held
   172.0 BPM with a drop at 10.74 s; the film starts on the downbeat 8 beats earlier
   (`music: { offset: 7.95, stopBeat: 58 }`), so the drop lands on the first key art and the music stops dead
   on the title.

4. **The sound kit.** `recommend` with `"capability": "txt2audio"` and "short isolated sound effects for
   motion graphics". One run per sound, short durations (each second costs), a negative prompt that keeps
   music and voices out, `"wait": false` for all of them, then one `jobs_wait` with every job id. The 12 core
   names and the prompts that worked are in [references/sound.md](references/sound.md); add custom sounds
   for the film's own jokes (here `stomp`, `roar`, `bell`, `knock`). Save them as `audio/sfx/<name>.wav`
   (variants `key_1.wav`, `key_2.wav` rotate).

5. **Key art.** `recommend` with `"capability": "txt2img"` and the art direction. Describe the composition,
   never ask for empty space: "a calm darker band for the title" was drawn as a literal grey band. Darken
   for type in the film instead (`tint`). For the second picture, pass the first as a reference image so the
   character and city match:

   ```json
   { "model_id": "<id from recommend>", "dry_run": true, "parameters": { "prompt": "Same game, same art style, same courier and same rainy neon city as the reference image. Close-up three-quarter shot of the courier on the yellow scooter, looking up with a determined grin; a puddle on the right reflects one enormous glowing monster eye. Stylized 3D, soft global illumination, crisp rim light.", "referenceImages": ["<asset id of picture 1>"], "aspectRatio": "16:9", "resolution": "2K", "numOutputs": 1 } }
   ```

   Download with `"format": "png"` into `art/`. Look at every picture at 100 %: generated vehicles and
   clothes carry real brand marks (the scooter came back with a maker's script logo). Remove them before the
   film uses the picture.

6. **spec.js.** Start from `examples/kaiju-postal/spec.js` or `examples/starter/spec.js`. An excerpt:

   ```js
   bpm: 172, beats: 68,
   palette: { bg: '#0B1020', paper: '#F3EEE3', accent: '#FFC21A', hot: '#FF8A1F', ink: '#14120E' },
   music: { file: 'audio/music.mp3', offset: 7.95, stopBeat: 58, gain: -7 },
   sounds: { stomp: -1, roar: -5, bell: -7, knock: -1, hit: 1 },
   cues: [[5.5, 'stomp'], [8.25, 'roar', .9], [24.6, 'bell']],
   scenes: [
     [Words, 0, 8, { charge: true, shots: [
       { at: 1, style: 'punch3d', text: 'THE CITY', fx: 'punch' },
       { at: 2, style: 'slam', text: 'HAS NEW', ground: 'accent' },
       { at: 3, style: 'stack', text: ['VERY BIG', 'NEIGHBOURS.'], ground: 'paper', in: 'whipX', fx: 'none' },
       { at: 5, style: 'split', text: ['THEY', 'STOMP.'], in: 'whipY', fx: 'punch', big: true } ] }],
     [Picture, 8, 16, { src: 'art/key1.png', weather: 'rain', words: [[1, 'MONSTERS'], [3, 'NEXT DOOR.', 'accent']], cutIns: [[5, 1.65, [.62, .2], 'stomp']] }],
     ...
   ```

7. **Preview, mix, check render.** Scrub the page, snap stills, then:

   ```bash
   python3 $K/scripts/mix.py .            # lists any hit quieter than the music: raise it in spec.sounds
   python3 $K/scripts/render.py . --res 1080
   python3 $K/scripts/finish.py . --video out/video_1080.mp4 --audio out/mix.wav
   ```

   In the build, the first check failed on two pictures that held for 1.5 s and 1.2 s; the Picture block
   now pushes, pans, punches in on every word, cuts in to a detail and draws weather over the image, and
   the teaser passed with 24 % still frames, no hold over 0.6 s and 12.5 cuts per 10 s.

8. **Master.** `render.py . --res 4k`, then `finish.py` on it: a 4K master under 1 GB, a 1080p version and a
   9:16 version (the film centred on black), each checked.
