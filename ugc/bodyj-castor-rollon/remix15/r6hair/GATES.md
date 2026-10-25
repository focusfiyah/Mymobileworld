# Gates: V3 grandma long hair (2026-10-23)

Goal: V3 with R3 remade so grandma's hair is much longer, same grey colour and coily texture; nothing else in V3 changes.

1. Book approved by Ralph before any paid call.
   CHECK: python3 -c "import json;print(bool(json.load(open('checklist.json')).get('book_ok')))"  EXPECT: True
2. New R3 still: hair long (past the shoulders), grey/salt-and-pepper, tight coils; hands, ring, sweater, room, roll-on size and label as round 4. Looked at full size + 2x on hair edges, hands and label.
3. New R3 clip: 4 s, label holds on frames 0/1/2/3 s at 2x, hair stays long and coily (no straightening, no colour shift), two hands only, no flicker, first second clean.
4. V3 re-cut: only R3 changed; every other shot is the round-4 clip.
   CHECK: python3 -c "import json;p=json.load(open('out/remix15_v3_plan.json'));print(p['shots'])"  EXPECT: ['V3a', 'R3', 'V3c', 'V3d', 'V3e', 'V3f', 'V3g']
5. Cut QC passes: qc.py 3, check.py cuts, gate --stage cut, REMOVED.md, AI finish applied.
   CHECK: python3 ../../../grace/gate.py . --stage cut  EXPECT: GATE OK
6. Review page republished (same URL) with the new V3; Drive: new CURRENT - V3, the old one in Older versions as v (date).
7. Ralph told by push + email; README/BRIEF Status lines and the brain note updated; branch merged to main.
