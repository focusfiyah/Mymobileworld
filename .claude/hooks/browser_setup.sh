#!/bin/bash
# Playwright for every cloud session (Ralph 2026-10-22: "Playwright should be accessible for every session").
# The container ships Chromium at /opt/pw-browsers (revision 1194) but not the Python package; 1.56.0 matches that
# revision (tested 2026-10-22). Also trusts the proxy's Anthropic CAs in Chromium's NSS db (else random
# ERR_CERT_AUTHORITY_INVALID). Runs in the background so the session never waits; log /tmp/browser-setup.log.
# Idempotent: a session that already has both does nothing.
(
  python3 -c "import playwright" 2>/dev/null || \
    python3 -m pip install -q --break-system-packages playwright==1.56.0 2>&1 | grep -vi "warning\|notice"
  if [ -f /root/.ccr/ca-bundle.crt ]; then
    command -v certutil >/dev/null || apt-get install -y -qq libnss3-tools >/dev/null 2>&1 || \
      { apt-get update -qq && apt-get install -y -qq libnss3-tools >/dev/null; }
    mkdir -p "$HOME/.pki/nssdb"
    [ -f "$HOME/.pki/nssdb/cert9.db" ] || certutil -d "sql:$HOME/.pki/nssdb" -N --empty-password
    python3 - <<'PY'
import re, subprocess, os, tempfile
db = "sql:" + os.path.expanduser("~/.pki/nssdb")
for pem in re.findall(r"-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----", open("/root/.ccr/ca-bundle.crt").read(), re.S):
    subj = subprocess.run(["openssl", "x509", "-noout", "-subject"], input=pem, capture_output=True, text=True).stdout
    if "Anthropic" not in subj:
        continue
    cn = re.search(r"CN\s*=\s*([^,/\n]+)", subj).group(1).strip()
    if subprocess.run(["certutil", "-d", db, "-L", "-n", cn], capture_output=True).returncode == 0:
        continue
    with tempfile.NamedTemporaryFile("w", suffix=".pem") as f:
        f.write(pem); f.flush()
        subprocess.run(["certutil", "-d", db, "-A", "-t", "C,,", "-n", cn, "-i", f.name], check=True)
PY
  fi
  python3 -c "import playwright; print('BROWSER_SETUP_OK')"
) > /tmp/browser-setup.log 2>&1 &
exit 0
