#!/usr/bin/env bash
# One-time Scrapling setup. Prints the scrapling binary path to use afterwards.
# Usage: bash scripts/setup.sh [venv_dir]   (default ~/.scrapling-venv)
set -e
VENV="${1:-$HOME/.scrapling-venv}"
[ -x "$VENV/bin/scrapling" ] || {
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q "scrapling[all]>=0.4.15"
}
# Browsers for fetch / stealthy-fetch (skip with SCRAPLING_NO_BROWSERS=1 for plain `get` only).
[ -n "$SCRAPLING_NO_BROWSERS" ] || "$VENV/bin/scrapling" install --force >/dev/null 2>&1 || echo "WARN: browser install failed; 'get' still works" >&2

# Behind a TLS-inspecting proxy (Claude cloud sessions), Chromium needs the proxy CAs in its NSS db,
# otherwise `fetch` fails with ERR_CERT_AUTHORITY_INVALID. Same fix as Dayone-ai/setup.sh.
CA=/root/.ccr/ca-bundle.crt
if [ -f "$CA" ]; then
  command -v certutil >/dev/null || apt-get install -y -qq libnss3-tools >/dev/null 2>&1 || true
  if command -v certutil >/dev/null; then
    mkdir -p "$HOME/.pki/nssdb"
    [ -f "$HOME/.pki/nssdb/cert9.db" ] || certutil -d "sql:$HOME/.pki/nssdb" -N --empty-password
    python3 - "$CA" <<'PY'
import os, re, subprocess, sys, tempfile
db = "sql:" + os.path.expanduser("~/.pki/nssdb")
for pem in re.findall(r"-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----", open(sys.argv[1]).read(), re.S):
    subj = subprocess.run(["openssl", "x509", "-noout", "-subject"], input=pem, capture_output=True, text=True).stdout
    if "Anthropic" not in subj:  # only the proxy's CAs
        continue
    cn = re.search(r"CN\s*=\s*([^,/\n]+)", subj).group(1).strip()
    if subprocess.run(["certutil", "-d", db, "-L", "-n", cn], capture_output=True).returncode == 0:
        continue
    with tempfile.NamedTemporaryFile("w", suffix=".pem") as f:
        f.write(pem); f.flush()
        subprocess.run(["certutil", "-d", db, "-A", "-t", "C,,", "-n", cn, "-i", f.name], check=True)
PY
  fi
fi
echo "$VENV/bin/scrapling"
