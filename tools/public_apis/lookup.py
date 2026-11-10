"""Free, keyless lookups from the Public APIs list (github.com/public-apis/public-apis, MIT), added 2026-11-10
from the InsiderForce Short "Get 1000 Free APIs for Claude Code" Ralph sent. Every call is $0, no key.

  python3 tools/public_apis/lookup.py food "creatine gummies"        # Open Food Facts: ingredients, brand, barcode
  python3 tools/public_apis/lookup.py beauty "retinol serum"         # Open Beauty Facts: skincare/cosmetics
  python3 tools/public_apis/lookup.py barcode 0850012345678          # one product by barcode (food, then beauty)
  python3 tools/public_apis/lookup.py recalls "space heater"         # openFDA recalls (food, drug, device)
  python3 tools/public_apis/lookup.py words cheap                    # Datamuse: plainer words with the same meaning
  python3 tools/public_apis/lookup.py say collagen                   # Free Dictionary: phonetics for a VO word
  python3 tools/public_apis/lookup.py vo script.txt [out.md]          # VO word check: words the dictionary does not know
                                                                    # (brands, coined words) to set a pronunciation for
                                                                    # before the ElevenLabs call, + phonetics of long words
  python3 tools/public_apis/lookup.py holidays [US]                  # Nager.Date: next public holidays (real urgency)
  python3 tools/public_apis/lookup.py job ugc/<job> "creatine gummies"  # Grace gate step public_data: writes
                                                                    # JOB/research/public_data.md (food+beauty+recalls)
  python3 tools/public_apis/lookup.py vin 1HGCM82633A004352          # NHTSA: decode a VIN (Jean's auto school)

What it is for: product facts and recall checks before a Grace script (claims only from real photos still win:
product_truth.json); plainer words for readability; pronunciation checks before an ElevenLabs VO; dated holiday
hooks; VIN facts for Jean. Open data is user-submitted and unvalidated: a lead to check, never a claim on its own.
"""
import json, sys, urllib.parse, urllib.request

UA = {"User-Agent": "research-client/1.0"}


def get(url, tries=3):
    """JSON from url. openFDA's 404 = no matches (returned as {}); anything else is retried, then {"error": ...}."""
    import time
    err = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: return {}
            err = f"HTTP {e.code}"
        except Exception as e:   # timeout, reset, bad JSON
            err = type(e).__name__
        time.sleep(2 * (i + 1))
    return {"error": err}


def fda_q(q):
    """openFDA search: every word must appear in the product description (an exact phrase misses most products)."""
    return urllib.parse.quote("+AND+".join(f"product_description:{w}" for w in q.split()), safe="+:")


def off(host, q, n=5):
    f = "code,product_name,brands,ingredients_text,quantity"
    d = get(f"https://{host}/cgi/search.pl?search_terms={urllib.parse.quote(q)}&search_simple=1&json=1&page_size={n}&fields={f}")
    if "error" in d: return d
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
        s = fda_q(q)
        out = {}
        for kind in ("food", "drug", "device"):
            d = get(f"https://api.fda.gov/{kind}/{'recall' if kind == 'device' else 'enforcement'}.json?search={s}&limit=5")
            out[kind] = d if "error" in d else [{k: r.get(k) for k in ("recalling_firm", "product_description", "reason_for_recall", "recall_initiation_date", "event_date_initiated")}
                         for r in d.get("results", [])]
    elif cmd == "words":
        out = [w["word"] for w in get(f"https://api.datamuse.com/words?ml={urllib.parse.quote(q)}&max=15")]
    elif cmd == "say":
        d = get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(q)}")
        out = d if isinstance(d, dict) else [{"word": e["word"], "phonetic": e.get("phonetic"),
                                              "audio": [p["audio"] for p in e.get("phonetics", []) if p.get("audio")]} for e in d]
    elif cmd == "vo":
        import re
        from concurrent.futures import ThreadPoolExecutor
        from pathlib import Path
        text = Path(a[0]).read_text()
        words = sorted({w for w in re.findall(r"[A-Za-z][A-Za-z']+", text) if len(w) >= 4 and not w.lower().endswith("'s")},
                       key=str.lower)
        seen, uniq = set(), []
        for w in words:
            if w.lower() not in seen: seen.add(w.lower()); uniq.append(w)
        def one(w):
            d = get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(w.lower())}")
            if isinstance(d, dict): return w, ("ERROR" if "error" in d else None)
            return w, next((e.get("phonetic") for e in d if e.get("phonetic")), "")
        with ThreadPoolExecutor(8) as ex: res = list(ex.map(one, uniq))
        if any(p == "ERROR" for _, p in res): sys.exit("LOOKUP_ERROR: dictionary lookups failed, rerun")
        unknown = [w for w, p in res if p is None]
        long_ = [(w, p) for w, p in res if p and len(w) >= 9]
        md = [f"# VO word check: {a[0]}", "", f"{len(uniq)} words checked (Free Dictionary, $0).", "",
              "## Not in the dictionary: brand or coined words; set how each is said (ElevenLabs pronunciation / respell) before the VO"]
        md += [f"- {w}" for w in unknown] or ["- none"]
        md += ["", "## Long words with dictionary phonetics (listen for these in the first take)"]
        md += [f"- {w} {p}" for w, p in long_] or ["- none"]
        if len(a) > 1: Path(a[1]).write_text("\n".join(md) + "\n")
        out = {"checked": len(uniq), "not_in_dictionary": unknown, "long_words": len(long_)}
    elif cmd == "holidays":
        out = [(h["date"], h["name"]) for h in get(f"https://date.nager.at/api/v3/NextPublicHolidays/{q or 'US'}")]
    elif cmd == "job":
        from pathlib import Path
        job, q = Path(a[0]), " ".join(a[1:])
        res = {"food": off("world.openfoodfacts.org", q), "beauty": off("world.openbeautyfacts.org", q)}
        main_rec = {}
        s = fda_q(q)
        for kind in ("food", "drug", "device"):
            d = get(f"https://api.fda.gov/{kind}/{'recall' if kind == 'device' else 'enforcement'}.json?search={s}&limit=5")
            main_rec[kind] = d if "error" in d else [{k: r.get(k) for k in ("recalling_firm", "product_description", "reason_for_recall", "recall_initiation_date", "event_date_initiated")}
                              for r in d.get("results", [])]
        md = [f"# Public data: {q}", "", "Source: tools/public_apis/lookup.py (Open Food Facts, Open Beauty Facts, openFDA), $0.",
              "Open data is user-submitted and unvalidated: a lead to check against the real photos/listing, never a claim on its own.", "",
              "## Product lookup"]
        def bad(rows): return isinstance(rows, dict)
        if any(bad(v) for v in [*res.values(), *main_rec.values()]):
            sys.exit(f"LOOKUP_ERROR, nothing written (rerun): { {k: v for k, v in {**res, **main_rec}.items() if bad(v)} }")
        for src, rows in res.items():
            md.append(f"### {src}: {len(rows)} match(es)")
            md += [f"- {r.get('brands')} | {r.get('product_name')} | {r.get('quantity')} | {(r.get('ingredients_text') or '')[:300]}" for r in rows] or ["- none found"]
        md.append("\n## Recall check (openFDA)")
        for kind, rows in main_rec.items():
            md.append(f"### {kind}: {len(rows)} recall(s)")
            md += [f"- {r.get('recall_initiation_date') or r.get('event_date_initiated')} | {r.get('recalling_firm')} | {(r.get('product_description') or '')[:160]} | why: {r.get('reason_for_recall')}" for r in rows] or ["- none found"]
        md += ["", "## What it means for the script", "Matches this exact product? (yes/no, which fields) / Any recall on this brand or type to avoid in claims? / Anything to verify on the real photos:", ""]
        (job / "research").mkdir(parents=True, exist_ok=True)
        f = job / "research" / "public_data.md"
        f.write_text("\n".join(md))
        out = {"wrote": str(f), "food": len(res["food"]), "beauty": len(res["beauty"]), "recalls": {k: len(v) for k, v in main_rec.items()}}
    elif cmd == "vin":
        r = get(f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{q}?format=json")["Results"][0]
        out = {k: r[k] for k in ("Make", "Model", "ModelYear", "BodyClass", "FuelTypePrimary", "ErrorText")}
    else:
        sys.exit(__doc__)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:]) if len(sys.argv) > 1 else sys.exit(__doc__)
