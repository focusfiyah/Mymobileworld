"""Fallback for `tiktok.py video` when its headless browser gets no data (2026-10-16: 4/4 failed, plain HTTPS worked).
python3 tools/tt_fetch.py OUTDIR URL... -> OUTDIR/<id>/meta.json, video.mp4, hook.png (0,0.5,1,1.5,2,3s), sheet.png, transcript.txt (TikTok captions if any)."""
import json, re, subprocess, sys
from pathlib import Path
import requests
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Referer": "https://www.tiktok.com/"}
out = Path(sys.argv[1])
for url in sys.argv[2:]:
    s = requests.Session(); s.headers.update(UA)
    t = s.get(url, timeout=30).text
    m = re.search(r'__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', t)
    i = json.loads(m.group(1))["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
    d = out / i["id"]; d.mkdir(parents=True, exist_ok=True)
    v = i.get("video", {})
    meta = {"url": url, "author": i["author"]["uniqueId"], "caption": i.get("desc"), "stats": i.get("stats"), "duration": v.get("duration"),
            "posted": i.get("createTime"), "product": (i.get("anchors") or [{}])[0].get("keyword") if i.get("anchors") else None}
    (d / "meta.json").write_text(json.dumps(meta, indent=1))
    subs = [x for x in v.get("subtitleInfos", []) if x.get("LanguageCodeName", "").startswith("eng")]
    if subs:
        vtt = s.get(subs[0]["Url"], timeout=30).text; (d / "captions.vtt").write_text(vtt)
        (d / "transcript.txt").write_text(" ".join(l for l in vtt.splitlines() if l and "-->" not in l and l != "WEBVTT" and not l.isdigit()))
    play = v.get("playAddr") or v.get("downloadAddr")
    r = s.get(play, timeout=120); (d / "video.mp4").write_bytes(r.content)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d / "video.mp4"), "-vf", "select='eq(n\\,0)+eq(n\\,15)+eq(n\\,30)+eq(n\\,45)+eq(n\\,60)+eq(n\\,90)',scale=240:-2,tile=6x1", "-vsync", "0", "-frames:v", "1", str(d / "hook.png")])
    dur = max(1, int(v.get("duration") or 30))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d / "video.mp4"), "-vf", f"fps=12/{dur},scale=200:-2,tile=6x2", "-frames:v", "1", str(d / "sheet.png")])
    print(i["id"], meta["author"], meta["stats"].get("playCount"), "video", len(r.content), "bytes", "captions" if subs else "no captions")
