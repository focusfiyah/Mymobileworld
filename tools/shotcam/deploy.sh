#!/bin/bash
# Publish Shot Cam to https://shotcam-azariah.netlify.app (Netlify site 3ef9e069-06a1-4ff2-ad8b-507f57399e81, Ralph's account).
# The Netlify key is injected by the session proxy for api.netlify.com (never stored here).
# Every change (page or a new shot list in site/lists/): run this, then python3 check_live.py.
set -e
cd "$(dirname "$0")/site"
Z=$(mktemp -d)/site.zip; zip -qr "$Z" .
curl -sS -X POST https://api.netlify.com/api/v1/sites/3ef9e069-06a1-4ff2-ad8b-507f57399e81/deploys \
  -H "Content-Type: application/zip" --data-binary @"$Z" --max-time 300 | python3 -c "import json,sys;d=json.load(sys.stdin);print('deploy',d.get('id'),d.get('state'))"
