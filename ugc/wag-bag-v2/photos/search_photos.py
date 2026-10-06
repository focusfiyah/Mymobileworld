"""Find free, commercial-safe photos. Usage: python3 search_photos.py "portable generator" [n]
Order: Pexels, Pixabay (keys from env PEXELS_API_KEY / PIXABAY_API_KEY, set by Ralph in the cloud environment), then Openverse
(no key, CC0/PDM only = no credit needed). Prints id, size, license, page URL and writes thumbs to raw_search/ for a contact sheet.
Never print or log the keys. Wikimedia API 429s from this server; Pexels/Pixabay web pages 403 (use the APIs)."""
import json, os, subprocess, sys, urllib.parse, urllib.request
UA = "RalphUGCBot/1.0 (life22watch@gmail.com)"
q, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 12
os.makedirs("raw_search", exist_ok=True); rows = []
def get(u, h=None): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, **(h or {})}), timeout=30))
if os.environ.get("PEXELS_API_KEY"):
    for p in get(f"https://api.pexels.com/v1/search?query={urllib.parse.quote(q)}&per_page={n}", {"Authorization": os.environ["PEXELS_API_KEY"]}).get("photos", []):
        rows.append(("pexels", p["id"], p["src"]["large"], p["src"]["medium"], "Pexels license (free commercial, no credit)", p["url"]))
if os.environ.get("PIXABAY_API_KEY"):
    for p in get(f"https://pixabay.com/api/?key={os.environ['PIXABAY_API_KEY']}&q={urllib.parse.quote(q)}&per_page={max(n, 3)}&image_type=photo").get("hits", []):
        rows.append(("pixabay", p["id"], p["largeImageURL"], p["webformatURL"], "Pixabay license (free commercial, no credit)", p["pageURL"]))
for p in get(f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(q)}&license=cc0,pdm&page_size={n}").get("results", []):
    rows.append(("openverse", p["id"], p["url"], p["thumbnail"], p["license"], p["foreign_landing_url"]))
for i, (src, pid, full, thumb, lic, page) in enumerate(rows):
    print(i, src, pid, lic, page); subprocess.run(["curl", "-sS", "-L", "-A", UA, "--max-time", "30", "-o", f"raw_search/{i:02d}_{src}.jpg", thumb])
json.dump(rows, open("raw_search/results.json", "w"))
