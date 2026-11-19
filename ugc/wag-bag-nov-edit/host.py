"""Host finished cuts on Kie's free 3-day file host (no generation, $0) so Composio can pull them into Drive."""
import hashlib, json, sys, time, requests
from pathlib import Path
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
out = {}
for f in sys.argv[1:]:
    p = Path(f)
    for attempt in range(4):
        r = requests.post(UPLOAD, files={"file": (p.name, p.read_bytes())}, data={"uploadPath": "wagbag"}, timeout=300)
        if r.ok and (r.json().get("data") or {}).get("downloadUrl"): break
        time.sleep(2 ** attempt)
    url = r.json()["data"]["downloadUrl"]
    assert hashlib.sha256(requests.get(url, timeout=300).content).digest() == hashlib.sha256(p.read_bytes()).digest(), f"hosted copy differs: {p}"
    out[p.name] = {"url": url, "size": p.stat().st_size}
print(json.dumps(out, indent=1))
