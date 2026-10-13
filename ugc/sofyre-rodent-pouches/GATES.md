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

- [x] G4: no paid call made yet (no kie_log.json)
  CHECK: test ! -e kie_log.json && echo NOPAID
  EXPECT: NOPAID
