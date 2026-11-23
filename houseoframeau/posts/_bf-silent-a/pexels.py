"""Free Pexels video search for holiday b-roll ($0, Pexels License). Portrait files >= 1080 wide only.
  python3 pexels.py OUTDIR "query one" "query two" ...   -> OUTDIR/cand.json + OUTDIR/cand.jpg (numbered thumbnails)"""
import json, os, sys, urllib.request, urllib.parse, io
from PIL import Image, ImageDraw
H = {"Authorization": os.environ["PEXELS_API_KEY"], "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read()
out = sys.argv[1]; os.makedirs(out, exist_ok=True); cand = []
for q in sys.argv[2:]:
    d = json.loads(get("https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": q, "orientation": "portrait", "per_page": 8})))
    for v in d["videos"]:
        f = [x for x in v["video_files"] if x.get("width") and x["width"] >= 1080 and x["height"] > x["width"] and x["width"] <= 1440]
        if not f: continue
        f = min(f, key=lambda x: x["width"])
        cand.append({"q": q, "id": v["id"], "dur": v["duration"], "url": v["url"], "file": f["link"], "w": f["width"], "img": v["image"]})
json.dump(cand, open(f"{out}/cand.json", "w"), indent=1)
W, Hh = 180, 320; cols = 8; rows = (len(cand) + cols - 1) // cols
sheet = Image.new("RGB", (W * cols, Hh * rows), "white"); dr = ImageDraw.Draw(sheet)
for i, c in enumerate(cand):
    try: im = Image.open(io.BytesIO(get(c["img"]))).convert("RGB")
    except Exception: continue
    im = im.resize((W, int(im.height * W / im.width)))
    sheet.paste(im.crop((0, 0, W, Hh)), ((i % cols) * W, (i // cols) * Hh))
    dr.rectangle(((i % cols) * W, (i // cols) * Hh, (i % cols) * W + 60, (i // cols) * Hh + 24), fill="black")
    dr.text(((i % cols) * W + 4, (i // cols) * Hh + 4), f"{i} {c['dur']}s", fill="yellow")
sheet.save(f"{out}/cand.jpg"); print(len(cand), "candidates")
