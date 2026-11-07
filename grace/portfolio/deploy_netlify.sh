#!/bin/bash
# Publish Grace's portfolio to https://graceglows.netlify.app (Netlify site 82feefbb-2c53-4038-8fb1-a42a9117cb5a, Ralph's account).
# The Netlify key is injected by the session proxy for api.netlify.com (never stored here).
# Every change: edit site/index.html, publish the Artifact as usual, then run this.
set -e
cd "$(dirname "$0")"
python3 build_standalone.py
Z=$(mktemp -d)/site.zip; (cd dist && zip -qr "$Z" .)
curl -sS -X POST https://api.netlify.com/api/v1/sites/82feefbb-2c53-4038-8fb1-a42a9117cb5a/deploys \
  -H "Content-Type: application/zip" --data-binary @"$Z" --max-time 300 | python3 -c "import json,sys;d=json.load(sys.stdin);print('deploy',d.get('id'),d.get('state'))"
sleep 15
curl -sS -o /dev/null -w "live %{http_code}\n" https://graceglows.netlify.app/
