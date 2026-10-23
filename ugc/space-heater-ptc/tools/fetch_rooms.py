"""Free room plates (Pexels + Pixabay APIs, portrait, no people) -> rooms/cand/ + rooms/cand.json (source + licence)."""
import json, os, sys, urllib.request, urllib.parse
OUT = os.path.join(os.path.dirname(__file__), "..", "rooms", "cand")
Q = ["cozy bedroom interior", "bright bedroom nightstand", "home office desk interior", "living room sofa interior",
     "reading nook window", "dorm room interior", "nursery room interior", "cozy living room blanket",
     "kitchen breakfast nook", "bedside table lamp", "minimal workspace desk", "bright scandinavian living room"]
meta = {}
def get(url, headers=None):
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"}), timeout=60).read()
for q in Q:
    slug = q.replace(" ", "_")
    r = json.loads(get("https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": q, "orientation": "portrait", "per_page": 6}),
                       {"Authorization": os.environ["PEXELS_API_KEY"], "User-Agent": "Mozilla/5.0"}))
    for p in r["photos"]:
        if any(w in (p.get("alt") or "").lower() for w in ("woman", "man ", "person", "girl", "boy", "people", "child", "baby", "dog", "cat")): continue
        f = f"px_{p['id']}.jpg"
        if f in meta: continue
        open(os.path.join(OUT, f), "wb").write(get(p["src"]["original"] + "?auto=compress&w=1440"))
        meta[f] = {"q": q, "src": p["url"], "alt": p.get("alt"), "licence": "Pexels License (free commercial use, no attribution)"}
    r = json.loads(get("https://pixabay.com/api/?" + urllib.parse.urlencode({"key": os.environ["PIXABAY_API_KEY"], "q": q, "image_type": "photo", "orientation": "vertical", "per_page": 5, "safesearch": "true"})))
    for p in r["hits"]:
        if any(w in p["tags"] for w in ("woman", "man", "person", "girl", "people", "child", "baby", "dog", "cat")): continue
        f = f"pb_{p['id']}.jpg"
        if f in meta: continue
        open(os.path.join(OUT, f), "wb").write(get(p["largeImageURL"]))
        meta[f] = {"q": q, "src": p["pageURL"], "alt": p["tags"], "licence": "Pixabay Content License (free commercial use, no attribution)"}
    print(q, len(meta), flush=True)
json.dump(meta, open(os.path.join(OUT, "..", "cand.json"), "w"), indent=1)
