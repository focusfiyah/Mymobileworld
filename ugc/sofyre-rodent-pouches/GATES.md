# Gates: SoFyre rodent repellent ad (Grace), plan stage

OWNS: ugc/sofyre-rodent-pouches/**

Scope: research, gated + humanized script, free storyboard and ONE plan message with one total cost, before any paid generation.

- [x] G1: script gate passes (audience, coach, viral, facts, hooks, humanizer, readability, sources, banned phrases)
  CHECK: python3 ../../grace/gate.py .
  EXPECT: GATE OK

- [x] G2: real product refs saved (bag front, real pouch, Grace's hand)
  CHECK: ls refs/bag_front.jpg refs/pouch_real.jpg refs/hand_grace.jpg
  EXPECT: hand_grace.jpg

- [x] G3: free storyboard built with all 11 shots
  CHECK: python3 -c "import json;print('shots', len(json.load(open('shots.json'))['shots']))" && ls preview/storyboard_v1.png
  EXPECT: shots 11

- [x] G4: Kie spend = the $3.12 quote (11 stills + 52s of clips, no redos)
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];print(round(0.09*len(s)+0.041*sum(x['dur'] for x in s),3))"
  EXPECT: 3.122

- [x] G5: cut gate passes (compare proof, no text overlay)
  CHECK: python3 ../../grace/gate.py . --stage cut
  EXPECT: GATE OK

- [x] G6: cut is 34-36 s with audio, never slowed below 1.0x
  CHECK: ffprobe -v error -show_entries format=duration -of csv=p=0 out/sofyre_r1_raw.mp4 && grep -c "speed >= 0.999" cut.py
  EXPECT: 34.87
