#!/bin/bash
# render NAME (review preset), close gaps until none are left (max 4 passes)
n=$1
for i in 1 2 3 4; do
  python3 cut.py $n --fast >/dev/null
  r=$(python3 close_gaps.py $n)
  case "$r" in *": 0 drops"*) echo "$n pass $i: $(python3 gapmeter.py out/wagbag_$n.mp4 2>/dev/null | head -1 | cut -c1-140)"; exit 0;; esac
done
echo "$n: still adding drops after 4 passes"
