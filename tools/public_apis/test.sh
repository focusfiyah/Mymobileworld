#!/bin/bash
# Runs each lookup once; prints PUBLIC_APIS_OK when all return data.
cd "$(dirname "$0")/../.." || exit 1
fail=0
printf "CeraVe cleanser works." > /tmp/_vo.txt
for c in "vo /tmp/_vo.txt" "food creatine" "beauty moisturizer" "barcode 3017620422003" "recalls peanut" "words cheap" "say collagen" "holidays US" "vin 1HGCM82633A004352"; do
  out=$(python3 tools/public_apis/lookup.py $c 2>&1)
  if [ ${#out} -lt 40 ] || echo "$out" | grep -q '"error"\|Traceback'; then echo "FAIL: $c -> ${out:0:150}"; fail=1; else echo "ok: $c"; fi
done
[ $fail = 0 ] && echo PUBLIC_APIS_OK
