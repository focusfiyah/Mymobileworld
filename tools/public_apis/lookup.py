"""Free, keyless lookups from the Public APIs list (github.com/public-apis/public-apis, MIT), added 2026-11-10
from the InsiderForce Short "Get 1000 Free APIs for Claude Code" Ralph sent. Every call is $0, no key.

  python3 tools/public_apis/lookup.py food "creatine gummies"        # Open Food Facts: ingredients, brand, barcode
  python3 tools/public_apis/lookup.py beauty "retinol serum"         # Open Beauty Facts: skincare/cosmetics
  python3 tools/public_apis/lookup.py barcode 0850012345678          # one product by barcode (food, then beauty)
  python3 tools/public_apis/lookup.py recalls "space heater"         # openFDA recalls (food, drug, device)
  python3 tools/public_apis/lookup.py words cheap                    # Datamuse: plainer words with the same meaning
  python3 tools/public_apis/lookup.py say collagen                   # Free Dictionary: phonetics for a VO word
  python3 tools/public_apis/lookup.py holidays [US]                  # Nager.Date: next public holidays (real urgency)
  python3 tools/public_apis/lookup.py vin 1HGCM82633A004352          # NHTSA: decode a VIN (Jean's auto school)

What it is for: product facts and recall checks before a Grace script (claims only from real photos still win:
product_truth.json); plainer words for readability; pronunciation checks before an ElevenLabs VO; dated holiday
hooks; VIN facts for Jean. Open data is user-submitted and unvalidated: a lead to check, never a claim on its own.
"""
import json, sys, urllib.parse, urllib.request

UA = {"User-Agent": "research-client/1.0"}


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}"}


def off(host, q, n=5):
    f = "code,product_name,brands,ingredients_text,quantity"
    d = get(f"https://{host}/cgi/search.pl?search_terms={urllib.parse.quote(q)}&search_simple=1&json=1&page_size={n}&fields={f}")
    return [{k: p.get(k) for k in f.split(",")} for p in d.get("products", [])]


def main(cmd, *a):
    q = " ".join(a)
    if cmd == "food":
        out = off("world.openfoodfacts.org", q)
    elif cmd == "beauty":
        out = off("world.openbeautyfacts.org", q)
    elif cmd == "barcode":
        out = None
        for host in ("world.openfoodfacts.org", "world.openbeautyfacts.org"):
            d = get(f"https://{host}/api/v2/product/{q}?fields=product_name,brands,ingredients_text,quantity")
            if d.get("status") == 1:
                out = {"source": host, **d["product"]}
                break
        out = out or {"error": "barcode not found in Open Food/Beauty Facts"}
    elif cmd == "recalls":
        s = urllib.parse.quote(f'product_description:"{q}"')
        out = {}
        for kind in ("food", "drug", "device"):
            d = get(f"https://api.fda.gov/{kind}/{'recall' if kind == 'device' else 'enforcement'}.json?search={s}&limit=5")
            out[kind] = [{k: r.get(k) for k in ("recalling_firm", "product_description", "reason_for_recall", "recall_initiation_date", "event_date_initiated")}
                         for r in d.get("results", [])]
    elif cmd == "words":
        out = [w["word"] for w in get(f"https://api.datamuse.com/words?ml={urllib.parse.quote(q)}&max=15")]
    elif cmd == "say":
        d = get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(q)}")
        out = d if isinstance(d, dict) else [{"word": e["word"], "phonetic": e.get("phonetic"),
                                              "audio": [p["audio"] for p in e.get("phonetics", []) if p.get("audio")]} for e in d]
    elif cmd == "holidays":
        out = [(h["date"], h["name"]) for h in get(f"https://date.nager.at/api/v3/NextPublicHolidays/{q or 'US'}")]
    elif cmd == "vin":
        r = get(f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{q}?format=json")["Results"][0]
        out = {k: r[k] for k in ("Make", "Model", "ModelYear", "BodyClass", "FuelTypePrimary", "ErrorText")}
    else:
        sys.exit(__doc__)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:]) if len(sys.argv) > 1 else sys.exit(__doc__)
