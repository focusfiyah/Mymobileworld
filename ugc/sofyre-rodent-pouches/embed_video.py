# Fallback for `tiktok.py video` when video pages return "Site Maintenance" (2026-10-13): the embed player
# (tiktok.com/embed/v2/<id>) still carries stats + a playable mp4. Writes <out>/<id>/{meta.json,video.mp4,hook.png,sheet.png}.
# Usage: python3 embed_video.py <out_dir> <video_id> [...]
import json, os, re, subprocess, sys, requests
out = sys.argv[1]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
      "Referer": "https://www.tiktok.com/"}
for vid in sys.argv[2:]:
    h = requests.get(f"https://www.tiktok.com/embed/v2/{vid}", headers=UA, timeout=30).text
    t = re.search(r'<script id="__FRONTITY_CONNECT_STATE__"[^>]*>(.*?)</script>', h, re.S).group(1)
    st = json.loads(t)
    item = None
    def walk(o):
        global item
        if isinstance(o, dict):
            if str(o.get("id")) == vid and "stats" in o: item = o
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(st)
    d = os.path.join(out, vid); os.makedirs(d, exist_ok=True)
    s = (item or {}).get("stats", {})
    if not s:  # embed state keeps stats in a flat object: pull them by regex
        for k in ["playCount", "diggCount", "shareCount", "commentCount", "collectCount"]:
            m = re.search(r'"%s":(\d+)' % k, t); s[k] = int(m.group(1)) if m else None
        m = re.search(r'"duration":(\d+)', t); item = {"video": {"duration": int(m.group(1)) if m else None}, "isECVideo": 1 if '"isECVideo":1' in t else 0}
    vids = [u for u in re.findall(r'https?:[^"]+', t.replace("\\u002F", "/")) if "/video/tos/" in u]
    ok = False
    for u in vids:
        r = requests.get(u.replace("\\u0026", "&"), headers=UA, timeout=120)
        if r.ok and len(r.content) > 50000:
            open(os.path.join(d, "video.mp4"), "wb").write(r.content); ok = True; break
    dur = (item or {}).get("video", {}).get("duration")
    meta = {"id": vid, "author": (item or {}).get("author", {}).get("uniqueId") if isinstance((item or {}).get("author"), dict) else (item or {}).get("author"),
            "desc": (item or {}).get("desc"), "views": s.get("playCount"), "likes": s.get("diggCount"),
            "shares": s.get("shareCount"), "comments": s.get("commentCount"), "saves": s.get("collectCount"),
            "duration": dur, "isECVideo": (item or {}).get("isECVideo"), "source": "embed/v2"}
    json.dump(meta, open(os.path.join(d, "meta.json"), "w"), indent=2)
    if ok:
        v = os.path.join(d, "video.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vf",
                        "select='eq(n\\,0)+eq(n\\,15)+eq(n\\,30)+eq(n\\,45)+eq(n\\,60)+eq(n\\,90)',scale=270:-2,tile=6x1",
                        "-vsync", "vfr", "-frames:v", "1", os.path.join(d, "hook.png")])
        n = max(1, int((dur or 30)))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vf", f"fps=12/{n},scale=240:-2,tile=6x2",
                        "-frames:v", "1", os.path.join(d, "sheet.png")])
    print(vid, "video" if ok else "NO VIDEO", meta["views"], meta["duration"], meta["desc"])
