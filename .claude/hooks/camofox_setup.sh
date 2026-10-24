#!/bin/bash
# camofox-browser for every cloud session (Ralph 2026-10-24: "This should replace playwright").
# github.com/jo-inc/camofox-browser (MIT): Camoufox (anti-detection Firefox) behind a local REST server on
# 127.0.0.1:9377; the camofox-browser MCP in .mcp.json is a thin client over it. Pinned: npm package 1.18.1
# (2026-10-05) and the browser release that package pins, 152.0.4-beta.30.
# Why the browser is not fetched by npm: its downloader asks api.github.com for the release list, which the
# session proxy refuses (403, tested 2026-10-24); the direct release URL works. Firefox ignores the system CA
# store, so the proxy's Anthropic CAs go into Camoufox's enterprise policy (else SEC_ERROR_UNKNOWN_ISSUER).
# Telemetry off (it files crash reports to the maker by default). Runs in the background, log /tmp/camofox-setup.log.
# Idempotent: a session that already has it only starts the server. Python Playwright (browser_setup.sh) stays for
# the scripts that import it (produce.py, tiktok.py, looks.py).
PKG_VER=1.18.1
FOX_VER=152.0.4
FOX_REL=beta.30
(
  set -e
  export CAMOFOX_CRASH_REPORT_ENABLED=false CAMOFOX_BIND_HOST=127.0.0.1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt
  DIR="$HOME/.camofox-browser"
  FOX="${XDG_CACHE_HOME:-$HOME/.cache}/camoufox"
  SRV="$DIR/node_modules/@askjo/camofox-browser/server.js"
  if curl -sf -m 3 http://127.0.0.1:9377/health >/dev/null; then echo "CAMOFOX_SETUP_OK (already running)"; exit 0; fi
  if [ "$(node -p "require('$DIR/node_modules/@askjo/camofox-browser/package.json').version" 2>/dev/null)" != "$PKG_VER" ]; then
    mkdir -p "$DIR"; cd "$DIR"
    [ -f package.json ] || echo '{"name":"camofox-local","private":true}' > package.json
    CAMOFOX_SKIP_DOWNLOAD=1 npm install -s --no-fund --no-audit "@askjo/camofox-browser@$PKG_VER"
  fi
  if ! grep -q "\"$FOX_REL\"" "$FOX/version.json" 2>/dev/null; then
    TMP=$(mktemp -d)
    curl -sSfL -o "$TMP/fox.zip" \
      "https://github.com/daijro/camoufox/releases/download/v$FOX_VER-$FOX_REL/camoufox-$FOX_VER-$FOX_REL-lin.x86_64.zip"
    rm -rf "$FOX"; mkdir -p "$FOX"; unzip -q "$TMP/fox.zip" -d "$FOX"; rm -rf "$TMP"
    echo "{\"version\":\"$FOX_VER\",\"release\":\"$FOX_REL\"}" > "$FOX/version.json"
  fi
  if [ -f /root/.ccr/ca-bundle.crt ]; then
    python3 - "$FOX/distribution/policies.json" <<'PY'
import json, os, re, subprocess, sys
out = os.path.expanduser("~/.camofox/ca"); os.makedirs(out, exist_ok=True); files = []
pems = re.findall(r"-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----", open("/root/.ccr/ca-bundle.crt").read(), re.S)
for i, pem in enumerate(pems):
    subj = subprocess.run(["openssl", "x509", "-noout", "-subject"], input=pem, capture_output=True, text=True).stdout
    if "Anthropic" in subj:
        path = f"{out}/proxy-ca-{i}.pem"; open(path, "w").write(pem + "\n"); files.append(path)
pol = json.load(open(sys.argv[1])); pol["policies"]["Certificates"] = {"Install": files}
json.dump(pol, open(sys.argv[1], "w"), indent=2)
PY
  fi
  cd "$DIR"; nohup node "$SRV" > /tmp/camofox.log 2>&1 &
  for _ in $(seq 1 30); do curl -sf -m 2 http://127.0.0.1:9377/health >/dev/null && { echo CAMOFOX_SETUP_OK; exit 0; }; sleep 1; done
  echo "CAMOFOX_SETUP_FAILED: server did not answer, see /tmp/camofox.log"; exit 1
) > /tmp/camofox-setup.log 2>&1 &
exit 0
