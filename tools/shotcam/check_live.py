"""Check the live Shot Cam site: page, sample list, manifest and camera permission header.
Prints SHOTCAM_LIVE_OK only when all pass. Run: python3 tools/shotcam/check_live.py [list-id ...]"""
import json, sys, urllib.request

BASE = "https://shotcam-azariah.netlify.app/"
fails = []
def get(path):
    with urllib.request.urlopen(urllib.request.Request(BASE + path, headers={"Cache-Control": "no-cache"}), timeout=30) as r:
        return r.status, dict(r.headers), r.read()
st, h, body = get("?list=sample")
if st != 200 or b"<title>Shot Cam</title>" not in body or b"MediaRecorder" not in body:
    fails.append(f"page: status {st}")
if "camera=(self)" not in h.get("Permissions-Policy", ""):
    fails.append("Permissions-Policy header missing camera=(self)")
for lid in ["sample"] + sys.argv[1:]:
    st, _, b = get(f"lists/{lid}.json")
    d = json.loads(b)
    if st != 200 or not d.get("shots"):
        fails.append(f"list {lid}: status {st}")
    else:
        print(f"list {lid}: {len(d['shots'])} shots, {BASE}?list={lid}")
st, _, b = get("manifest.json")
if st != 200 or json.loads(b).get("name") != "Shot Cam":
    fails.append("manifest")
if fails:
    print("FAILED: " + "; ".join(fails)); sys.exit(1)
print("SHOTCAM_LIVE_OK")
