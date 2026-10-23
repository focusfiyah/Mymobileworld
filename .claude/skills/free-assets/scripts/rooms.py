"""Free room backgrounds from Pexels + Pixabay: real rooms, portrait, no people or pets, no AI images, not mostly
white, not dark.

usage: python3 rooms.py OUT_DIR "teal tiled bathroom" "green kitchen plants" ... [--per 6] [--max-white 0.45]
needs PEXELS_API_KEY and PIXABAY_API_KEY (env). Writes OUT_DIR/cand/*.jpg, OUT_DIR/cand.json (query, source page,
licence, white share, brightness) and OUT_DIR/contact.jpg (numbered) to pick from.
"""
import argparse, io, json, os, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageStat

SKIP = ("woman", "man", "person", "girl", "boy", "people", "child", "baby", "kid", "dog", "cat", "puppy")
ROOM = ("interior", "room", "bathroom", "kitchen", "bedroom", "living", "home", "house", "apartment", "furniture",
        "sofa", "bed", "shelf", "desk", "sink", "counter", "nook", "hallway", "dining", "office", "nursery", "laundry")
PEXELS = "Pexels License (free commercial use, no attribution)"
PIXABAY = "Pixabay Content License (free commercial use, no attribution)"


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", **(headers or {})})
    return urllib.request.urlopen(req, timeout=60).read()


def words(text):
    return set((text or "").lower().replace(",", " ").replace("-", " ").split())


def why_skip(alt, allow_ai=False):
    """'people', 'not a room' or 'ai' from the photo's alt text / tags, else None."""
    w, low = words(alt), (alt or "").lower()
    if any(x in w for x in SKIP):
        return "people"
    if not allow_ai and ("ai generated" in low or "generated" in w or " ai " in f" {low} "):
        return "ai"
    if not any(x in w for x in ROOM):
        return "not a room"
    return None


def tone(img):
    """Share of pale, colourless pixels (white/off-white/light grey), and mean brightness (0-255).
    Measured 2026-10-22: all-white bathroom 0.76, white kitchen 0.79, white-tile kitchen 0.62, coloured rooms 0.1-0.47."""
    small = img.convert("RGB").resize((96, 160))
    b = small.convert("HSV").tobytes()
    white = sum(1 for i in range(0, len(b), 3) if b[i + 1] < 40 and b[i + 2] > 140) / (len(b) // 3)
    return round(white, 2), round(ImageStat.Stat(small.convert("L")).mean[0])


def search(q, per, allow_ai=False):
    r = json.loads(get("https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": q, "orientation": "portrait", "per_page": per}), {"Authorization": os.environ["PEXELS_API_KEY"]}))
    for p in r["photos"]:
        yield f"px_{p['id']}", p["src"]["original"] + "?auto=compress&w=1440", p["url"], p.get("alt"), PEXELS
    r = json.loads(get("https://pixabay.com/api/?" + urllib.parse.urlencode(
        {"key": os.environ["PIXABAY_API_KEY"], "q": q + " interior", "image_type": "photo", "orientation": "vertical",
         "per_page": max(per, 3), "safesearch": "true"})))  # "interior": plain "sage bathroom" returns sage plants
    for p in r["hits"]:
        if p.get("isLowQuality") or (p.get("isAiGenerated") and not allow_ai):
            yield f"pb_{p['id']}", None, p["pageURL"], None, "low quality" if p.get("isLowQuality") else "ai"
            continue
        yield f"pb_{p['id']}", p["largeImageURL"], p["pageURL"], p["tags"], PIXABAY


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--per", type=int, default=6, help="results per query per site")
    ap.add_argument("--max-white", type=float, default=0.6, help="skip rooms whiter than this share")
    ap.add_argument("--allow-ai", action="store_true", help="also keep AI rooms (fallback when the real ones are not good)")
    ap.add_argument("--min-bright", type=int, default=95, help="skip rooms darker than this mean")
    a = ap.parse_args()
    cand = os.path.join(a.out, "cand")
    os.makedirs(cand, exist_ok=True)
    meta, skipped = {}, {"people": 0, "not a room": 0, "ai": 0, "low quality": 0, "white": 0, "dark": 0}
    for q in a.queries:
        for key, url, page, alt, lic in search(q, a.per, a.allow_ai):
            f = key + ".jpg"
            if f in meta:
                continue
            reason = lic if url is None else why_skip(alt, a.allow_ai)  # url None = Pixabay flagged it
            if reason:
                skipped[reason] += 1
                continue
            img = Image.open(io.BytesIO(get(url))).convert("RGB")
            white, bright = tone(img)
            if white > a.max_white:
                skipped["white"] += 1
                continue
            if bright < a.min_bright:
                skipped["dark"] += 1
                continue
            img.save(os.path.join(cand, f), quality=92)
            meta[f] = {"q": q, "src": page, "alt": alt, "licence": lic, "white": white, "bright": bright,
                       "size": list(img.size)}
        print(q, "->", len(meta), "kept", flush=True)
    json.dump(meta, open(os.path.join(a.out, "cand.json"), "w"), indent=1)
    # numbered contact sheet, 6 across
    tw, th, cols = 240, 400, 6
    files = list(meta)
    sheet = Image.new("RGB", (cols * tw, max(1, -(-len(files) // cols)) * th), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(os.path.join(cand, f))
        im.thumbnail((tw, th))
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 120, y + 22], fill="black")
        d.text((x + 4, y + 5), f"{i + 1} {f[:-4]}", fill="white")
    sheet.save(os.path.join(a.out, "contact.jpg"), quality=88)
    print(f"kept {len(meta)}, skipped {skipped}; sheet {os.path.join(a.out, 'contact.jpg')}")


if __name__ == "__main__":
    main()
