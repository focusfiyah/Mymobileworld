#!/bin/bash
# Run the remaining Seedance clips in batches of 20 so Kie's auto-refill keeps up; retry what a 402 refused (refused tasks are not billed).
cd "$(dirname "$0")/.."
for round in 1 2 3 4 5 6 7 8; do
  todo=$(python3 -c "import json,os;S=json.load(open('shots.json'));D=json.load(open('qc/dropped.json'));print(' '.join(k for k in S if k not in D and not os.path.exists(f'clips/{k}_sd.mp4')))")
  [ -z "$todo" ] && { echo "ALL_CLIPS_DONE"; exit 0; }
  set -- $todo; batch="${@:1:20}"
  echo "round $round: $(echo $batch | wc -w) of $(echo $todo | wc -w)"
  python3 run.py seedance $batch >> clips_main.log 2>&1
  grep -c "402" clips_main.log | sed 's/^/402s so far: /'
  sleep 45
done
echo "STOPPED with clips left"
