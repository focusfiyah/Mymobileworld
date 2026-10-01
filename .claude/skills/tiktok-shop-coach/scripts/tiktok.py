#!/usr/bin/env python3
"""Pull public TikTok data through a headless Chromium (no login, no API key).

  tiktok.py viral [--days 3] [--top 20] [--category beauty|home|fashion|holiday|gifts] [--tags a,b]
                  [--add-tags a,b] [--discover URL ...] [--all] [--state FILE] [--out DIR]
      "What's going viral on TikTok Shop right now": scans shop-heavy hashtag pages (~100 recent shop videos in
      ~2 min), keeps shop videos (TikTok's own shop-video flag) posted in the last --days, and ranks them by
      views per day. Shows the product each video sells when TikTok includes it (title, category, shop link).
      Run it again later with the same --state file and it ranks by views GAINED since the last run instead.
      Writes DIR/viral-<date>.json.
  tiktok.py video <url> [<url> ...] [--out DIR] [--no-media]
      Short links (tiktok.com/t/...) are fine. Per video, in DIR/<id>/:
        meta.json            author, caption, hashtags, stats, duration, sound, posted, product
        transcript.txt       TikTok's own captions (absent if the video has none)
        transcript_timed.txt same, one line per caption with start-end seconds
        video.mp4            the video
        hook.png             frames at 0, 0.5, 1, 1.5, 2, 3 s (what the first 3 seconds look like)
        sheet.png            contact sheet, one frame every ~duration/12 s
  tiktok.py compare <A> <B> [--stt] [--out DIR]
      A/B compare, e.g. a viral video vs yours. A and B are TikTok links or local video files. Writes
      DIR/compare/compare.png (hook frames, A on top, B below) and compare.md (length, words/sec, cuts, first
      3 s spoken, timed transcripts side by side). Local files have no captions: --stt transcribes them with
      ElevenLabs speech-to-text (uses ElevenLabs credits; ask first).
  tiktok.py readability <text or file>
      Reading grade (Flesch-Kincaid), sentence length, hard words, speaking time. Aim for grade 6 or lower.
  tiktok.py tag <hashtag> [--top 15] [--days N] [--out DIR]
      Videos TikTok shows on the hashtag page (30-200), ranked by views. --days 30 = recent winners only.
  tiktok.py discover <discover-url-or-slug> [...] [--top 15] [--days N] [--out DIR]
      Keyword pages (tiktok.com/discover/<slug>): ~16 videos each, stats pulled per video, ranked by views.
      Only slugs TikTok already created exist (others redirect home), so find them with a web search first:
      site:tiktok.com/discover <product or keyword>.
  tiktok.py shop <keyword> [--top 20] [--out DIR]
      TikTok Shop search (shop.tiktok.com/us/k/<keyword>, any keyword): ~30 products with price, LIFETIME units
      sold, rating, reviews, shop. Ranked by units sold.

Not supported (tested 2026-10-01): tiktok.com keyword search (needs a login), a profile's video list (empty body to
headless browsers), product detail pages (captcha), GMV / recent sales, LIVE rankings.
Chromium: /opt/pw-browsers/chromium (Claude cloud env) or Playwright's default.
"""
import argparse, asyncio, datetime, json, os, re, subprocess, sys, time

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0 Safari/537.36")
REF = {"Referer": "https://www.tiktok.com/"}

# Hashtags where most videos are TikTok Shop videos (measured 2026-10-01: 55-90% shop, 8-40 shop videos <=3 days
# old per tag; #amazonfinds and #fallfinds are mostly non-shop). Seasonal tags (holidayhaul, christmas) may need
# swapping as the year moves on.
VIRAL_TAGS = ["tiktokshop", "tiktokshopfinds", "tiktokshopcreatorpicks", "tiktokshopholidayhaul", "tiktokshophome",
              "tiktokshopbeauty", "tiktokshopfashion", "tiktokmademebuyit"]
CATEGORY_TAGS = {
    "beauty": ["tiktokshopbeauty", "tiktokshopskincare", "tiktokshopmakeup", "tiktokshopfinds"],
    "home": ["tiktokshophome", "tiktokshopkitchen", "tiktokshopcleaning", "tiktokshopfinds"],
    "fashion": ["tiktokshopfashion", "tiktokshopoutfit", "tiktokshopclothes", "tiktokshopfinds"],
    "holiday": ["tiktokshopholidayhaul", "giftideas", "tiktokshopchristmas", "tiktokshopfinds"],
    "gifts": ["giftideas", "tiktokshopchristmas", "tiktokshopholidayhaul", "giftsforher"],
}


def ensure_proxy_trust():
    """Claude cloud envs re-sign HTTPS with several Anthropic CAs. Chromium trusts only its NSS db, so import them
    all (idempotent); otherwise pages fail intermittently with ERR_CERT_AUTHORITY_INVALID."""
    bundle = "/root/.ccr/ca-bundle.crt"
    if not os.path.exists(bundle) or subprocess.run(["which", "certutil"], capture_output=True).returncode:
        return
    import tempfile
    nss = os.path.expanduser("~/.pki/nssdb")
    os.makedirs(nss, exist_ok=True)
    db = "sql:" + nss
    if not os.path.exists(os.path.join(nss, "cert9.db")):
        subprocess.run(["certutil", "-d", db, "-N", "--empty-password"], capture_output=True)
    pems = re.findall(r"-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----", open(bundle).read(), re.S)
    for pem in pems:
        subj = subprocess.run(["openssl", "x509", "-noout", "-subject"], input=pem,
                              capture_output=True, text=True).stdout
        if "Anthropic" not in subj:
            continue
        cn = re.search(r"CN\s*=\s*([^,/\n]+)", subj).group(1).strip()
        if subprocess.run(["certutil", "-d", db, "-L", "-n", cn], capture_output=True).returncode == 0:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".pem") as f:
            f.write(pem); f.flush()
            subprocess.run(["certutil", "-d", db, "-A", "-t", "C,,", "-n", cn, "-i", f.name], capture_output=True)


def chromium_path():
    p = "/opt/pw-browsers/chromium"
    return p if os.path.exists(p) else None


def product_of(it):
    """The TikTok Shop product linked in a video, from its product anchor (present for some shop videos)."""
    for a in it.get("anchors") or []:
        try:
            for x in json.loads(a.get("extra") or "[]"):
                inner = json.loads(x.get("extra") or "{}")
                if inner.get("product_id") and inner.get("title"):
                    cats = inner.get("categories") or []
                    sponsored = "sponsored" in str(inner.get("extra") or "")
                    return {"product_id": str(inner["product_id"]), "title": inner["title"],
                            "category": cats[0].get("category_name") if cats else None,
                            "url": inner.get("seo_url") or f"https://shop.tiktok.com/us/pdp/{inner['product_id']}",
                            "sponsored_label": sponsored}
        except Exception:
            continue
    return None


def summarize(it, now=None):
    now = now or time.time()
    s = it.get("statsV2") or it.get("stats") or {}
    n = lambda k: int(s.get(k) or 0)
    views, likes, comments, shares, saves = (n("playCount"), n("diggCount"), n("commentCount"),
                                             n("shareCount"), n("collectCount"))
    a = it.get("author") or {}
    v = it.get("video") or {}
    ts = int(it.get("createTime") or 0)
    age_h = (now - ts) / 3600 if ts else None
    return {
        "id": it.get("id"),
        "url": f"https://www.tiktok.com/@{a.get('uniqueId', '')}/video/{it.get('id')}",
        "author": a.get("uniqueId"),
        "author_followers": (it.get("authorStatsV2") or it.get("authorStats") or {}).get("followerCount"),
        "caption": it.get("desc"),
        "hashtags": [t.get("hashtagName") for t in it.get("textExtra") or [] if t.get("hashtagName")],
        "posted": datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") if ts else None,
        "age_hours": round(age_h, 1) if age_h is not None else None,
        "duration_s": v.get("duration"),
        "sound": (it.get("music") or {}).get("title"),
        "views": views, "likes": likes, "comments": comments, "shares": shares, "saves": saves,
        "views_per_day": round(views / max(age_h, 6) * 24) if age_h else None,  # 6 h floor: brand-new videos extrapolate wildly
        "engagement_pct": round(100 * (likes + comments + shares + saves) / views, 1) if views else None,
        "save_pct": round(100 * saves / views, 2) if views else None,
        "shop_video": bool(it.get("isECVideo")),
        "product": product_of(it),
        "is_ad": it.get("isAd", False),
        "ai_generated_label": it.get("IsAigc", False),
    }


def parse_captions(raw):
    """TikTok serves captions as WebVTT or as JSON {"utterances": [...]} (ms). Returns [(start_s, end_s, text)]."""
    raw = raw.strip()
    segs = []
    if raw.startswith("{"):
        try:
            for u in json.loads(raw).get("utterances") or []:
                segs.append((u.get("start_time", 0) / 1000, u.get("end_time", 0) / 1000, (u.get("text") or "").strip()))
        except Exception:
            pass
        return [s for s in segs if s[2]]
    t = lambda x: sum(float(p) * 60 ** i for i, p in enumerate(reversed(x.replace(",", ".").split(":"))))
    cur = None
    for ln in raw.splitlines():
        ln = ln.strip()
        if "-->" in ln:
            a, b = [p.strip().split(" ")[0] for p in ln.split("-->")]
            cur = [t(a), t(b), []]
            segs.append(cur)
        elif ln and cur is not None and not ln.isdigit():
            cur[2].append(ln)
        elif not ln:
            cur = None
    out = []
    for a, b, lines in segs:
        text = " ".join(lines)
        if text and (not out or out[-1][2] != text):
            out.append((a, b, text))
    return out


def write_transcript(d, segs):
    open(os.path.join(d, "transcript.txt"), "w").write(" ".join(s[2] for s in segs))
    open(os.path.join(d, "transcript_timed.txt"), "w").write(
        "\n".join(f"[{a:5.1f}-{b:5.1f}] {x}" for a, b, x in segs))


def frames(mp4, outdir, duration):
    hook = os.path.join(outdir, "hook.png")
    times = [0, 0.5, 1, 1.5, 2, 3]
    inputs = []
    for t in times:
        inputs += ["-ss", str(t), "-i", mp4]
    fc = "".join(f"[{i}:v]scale=270:480:force_original_aspect_ratio=decrease,"
                 f"pad=270:480:(ow-iw)/2:(oh-ih)/2,trim=end_frame=1[f{i}];" for i in range(len(times)))
    fc += "".join(f"[f{i}]" for i in range(len(times))) + f"hstack=inputs={len(times)}"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", fc,
                    "-frames:v", "1", hook], check=False)
    step = max(1.0, (duration or 30) / 12)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-vf",
                    f"fps=1/{step:.2f},scale=270:-2,tile=6x2", "-frames:v", "1",
                    os.path.join(outdir, "sheet.png")], check=False)
    return hook


def probe_duration(mp4):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def count_cuts(mp4):
    """Hard cuts (scene changes) via ffmpeg scene detection, threshold 0.3."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp4, "-vf", "select='gt(scene,0.3)',showinfo",
                        "-f", "null", "-"], capture_output=True, text=True)
    return len(re.findall(r"pts_time:", r.stderr))


def elevenlabs_stt(mp4):
    """ElevenLabs speech-to-text (scribe_v2). In Ralph's cloud env the proxy adds the API key. Costs credits."""
    import requests
    with open(mp4, "rb") as f:
        r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2"},
                          files={"file": (os.path.basename(mp4), f)}, timeout=300)
    r.raise_for_status()
    words = [w for w in r.json().get("words") or [] if w.get("type", "word") == "word"]
    segs, cur = [], []
    for w in words:  # group into caption-sized lines, breaking at sentence ends
        cur.append(w)
        if re.search(r"[.!?]$", w["text"]) or len(cur) >= 10:
            segs.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"] for x in cur))); cur = []
    if cur:
        segs.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"] for x in cur)))
    return segs


async def new_ctx(p):
    b = await p.chromium.launch(executable_path=chromium_path(), args=["--no-sandbox"])
    ctx = await b.new_context(user_agent=UA, viewport={"width": 1280, "height": 900})
    return b, ctx


async def fetch_item(ctx, url):
    """itemStruct of one video page, or None."""
    pg = await ctx.new_page()
    try:
        await pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(3000)
        raw = await pg.evaluate("()=>{const s=document.querySelector('#__UNIVERSAL_DATA_FOR_REHYDRATION__');"
                                "return s?s.textContent:null}")
        return json.loads(raw)["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
    except Exception:
        return None
    finally:
        await pg.close()


async def download_video(ctx, it, d):
    """Captions + mp4 + frames for one itemStruct into dir d. Returns (segments, mp4 path or None)."""
    os.makedirs(d, exist_ok=True)
    v = it.get("video") or {}
    subs = v.get("subtitleInfos") or []
    sub = next((s for s in subs if str(s.get("LanguageCodeName", "")).startswith("eng")), subs[0] if subs else None)
    segs = []
    if sub:
        r = await ctx.request.get(sub["Url"], headers=REF)
        if r.ok:
            segs = parse_captions((await r.body()).decode("utf-8", "replace"))
            if segs:
                write_transcript(d, segs)
    mp4 = None
    if v.get("playAddr"):
        r = await ctx.request.get(v["playAddr"], headers=REF, timeout=120000)
        if r.ok:
            mp4 = os.path.join(d, "video.mp4")
            open(mp4, "wb").write(await r.body())
            frames(mp4, d, v.get("duration"))
    return segs, mp4


async def collect_tag(ctx, name, scrolls=4):
    """Raw itemStructs TikTok serves on a hashtag page."""
    items = {}
    pg = await ctx.new_page()

    async def on(r):
        if "/api/challenge/item_list" in r.url:
            try:
                for it in (await r.json()).get("itemList") or []:
                    items[it["id"]] = it
            except Exception:
                pass
    pg.on("response", lambda r: asyncio.ensure_future(on(r)))
    try:
        await pg.goto(f"https://www.tiktok.com/tag/{name}", wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(5000)
        for _ in range(scrolls):
            await pg.mouse.wheel(0, 4000)
            await pg.wait_for_timeout(2200)
    except Exception as e:
        print(f"  #{name}: {e.__class__.__name__}")
    finally:
        await pg.close()
    return items


async def collect_discover(ctx, page):
    """Video URLs on a tiktok.com/discover/<slug> page ([] if TikTok has no such page)."""
    slug = page.rstrip("/").split("/discover/")[-1].split("?")[0]
    pg = await ctx.new_page()
    try:
        await pg.goto(f"https://www.tiktok.com/discover/{slug}", wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(5000)
        if "/discover/" not in pg.url:
            return slug, []
        return slug, await pg.evaluate(
            "()=>[...new Set([...document.querySelectorAll('a[href*=\"/video/\"]')].map(a=>a.href.split('?')[0]))]")
    finally:
        await pg.close()


def recent(rows, days):
    if not days:
        return rows
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    kept = [r for r in rows if (r["posted"] or "") >= cutoff]
    print(f"--days {days}: kept {len(kept)} of {len(rows)} videos posted since {cutoff}")
    return kept


def print_videos(rows, top):
    print(f"{'views':>11} {'eng%':>5} {'save%':>6} {'dur':>4} {'posted':>10}  author / caption / url")
    for r in rows[:top]:
        cap = re.sub(r"\s+", " ", r["caption"] or "")[:70]
        print(f"{r['views']:>11,} {r['engagement_pct'] or 0:>5} {r['save_pct'] or 0:>6} "
              f"{r['duration_s'] or 0:>4} {r['posted'] or '':>10}  @{r['author']}: {cap}\n{'':>42}{r['url']}")


def short(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.0f}K" if n >= 1e4 else f"{n / 1e3:.1f}K" if n >= 1e3 else str(n)


async def cmd_viral(a):
    from playwright.async_api import async_playwright
    tags = (a.tags.split(",") if a.tags else CATEGORY_TAGS.get(a.category, VIRAL_TAGS))
    tags = list(dict.fromkeys(t.strip().lstrip("#") for t in tags + (a.add_tags.split(",") if a.add_tags else [])))
    now = time.time()
    items = {}
    async with async_playwright() as p:
        b, ctx = await new_ctx(p)
        for t in tags:
            got = await collect_tag(ctx, t, scrolls=3)
            items.update(got)
            print(f"  #{t}: {len(got)} videos")
        for page in a.discover or []:
            slug, links = await collect_discover(ctx, page)
            for url in links:
                vid = url.rstrip("/").split("/")[-1]
                if vid not in items:
                    it = await fetch_item(ctx, url)
                    if it:
                        items[it["id"]] = it
            print(f"  /discover/{slug}: {len(links)} videos")
        await b.close()
    rows = [summarize(it, now) for it in items.values()]
    total = len(rows)
    if not a.all:
        rows = [r for r in rows if r["shop_video"]]
    rows = [r for r in rows if r["age_hours"] is not None and r["age_hours"] <= a.days * 24]
    # Growth since the last run, from the state file (views per video per run).
    state_path = a.state or os.path.join(a.out, "viral-state.json")
    try:
        state = json.load(open(state_path))
    except Exception:
        state = {}
    for r in rows:
        prev = [h for h in state.get(r["id"], []) if now - h["t"] >= 3600]
        if prev:
            h = prev[-1]
            hours = (now - h["t"]) / 3600
            r["gained"] = r["views"] - h["views"]
            r["gained_hours"] = round(hours, 1)
            r["gained_per_day"] = round(r["gained"] / hours * 24)
    for r in rows:
        r["rank_score"] = r.get("gained_per_day", r["views_per_day"] or 0)
    rows.sort(key=lambda r: r["rank_score"], reverse=True)
    for it in items.values():  # remember this run's numbers for next time; keep 10 days, 6 points per video
        st = state.setdefault(it["id"], [])
        st.append({"t": now, "views": summarize(it, now)["views"]})
        state[it["id"]] = st[-6:]
    state = {k: v for k, v in state.items() if now - v[-1]["t"] < 10 * 86400}
    os.makedirs(os.path.dirname(state_path) or ".", exist_ok=True)
    json.dump(state, open(state_path, "w"))
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"viral-{datetime.datetime.utcnow():%Y-%m-%d}.json")
    json.dump(rows, open(path, "w"), indent=2)
    growth = sum(1 for r in rows if "gained" in r)
    print(f"\n{total} videos scanned, {len(rows)} {'shop ' if not a.all else ''}videos posted in the last {a.days} "
          f"day(s) -> {path}")
    print("Ranked by views gained since the last run (+) where known, else average views/day since posting.\n"
          if growth else "Ranked by average views/day since posting (run again later with the same --state for "
          "views gained between runs).\n")
    print(f"{'#':>3} {'per day':>9} {'views':>7} {'age':>5} {'save%':>5}  product / creator / url")
    for i, r in enumerate(rows[:a.top], 1):
        per = f"+{short(r['gained_per_day'])}" if "gained_per_day" in r else short(r["views_per_day"] or 0)
        prod = r["product"]["title"][:55] if r["product"] else "(product not in TikTok's data)"
        cat = f" [{r['product']['category']}]" if r["product"] and r["product"]["category"] else ""
        cap = re.sub(r"\s+", " ", r["caption"] or "")[:60]
        print(f"{i:>3} {per:>9} {short(r['views']):>7} {r['age_hours'] / 24:>4.1f}d {r['save_pct'] or 0:>5}  "
              f"{prod}{cat}\n{'':>34}@{r['author']}: {cap}\n{'':>34}{r['url']}")


async def cmd_video(urls, out, media):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b, ctx = await new_ctx(p)
        for url in urls:
            it = await fetch_item(ctx, url)
            if not it:
                print(f"FAILED {url}: no video data (private, deleted, region-blocked or a captcha)")
                continue
            meta = summarize(it)
            d = os.path.join(out, meta["id"])
            os.makedirs(d, exist_ok=True)
            if media:
                segs, _ = await download_video(ctx, it, d)
            else:
                segs = []
                v = it.get("video") or {}
                subs = v.get("subtitleInfos") or []
                sub = next((s for s in subs if str(s.get("LanguageCodeName", "")).startswith("eng")),
                           subs[0] if subs else None)
                if sub:
                    r = await ctx.request.get(sub["Url"], headers=REF)
                    if r.ok:
                        segs = parse_captions((await r.body()).decode("utf-8", "replace"))
                        if segs:
                            write_transcript(d, segs)
            meta["has_transcript"] = bool(segs)
            json.dump(meta, open(os.path.join(d, "meta.json"), "w"), indent=2)
            print(f"OK {meta['url']}\n   -> {d}  ({meta['duration_s']}s, {meta['views']:,} views, "
                  f"transcript={'yes' if segs else 'NO'})")
        await b.close()


async def cmd_compare(a):
    from playwright.async_api import async_playwright
    out = os.path.join(a.out, "compare")
    os.makedirs(out, exist_ok=True)
    sides = []
    async with async_playwright() as p:
        b, ctx = await new_ctx(p)
        for label, src in (("A", a.a), ("B", a.b)):
            d = os.path.join(out, label)
            os.makedirs(d, exist_ok=True)
            info = {"label": label, "source": src, "meta": None}
            if os.path.exists(src):
                mp4, segs = src, []
                info["duration"] = probe_duration(src)
                frames(src, d, info["duration"])
                if a.stt:
                    segs = elevenlabs_stt(src)
                    write_transcript(d, segs)
            else:
                it = await fetch_item(ctx, src)
                if not it:
                    print(f"FAILED {label}: {src}")
                    await b.close()
                    return
                info["meta"] = summarize(it)
                segs, mp4 = await download_video(ctx, it, d)
                info["duration"] = (probe_duration(mp4) if mp4 else None) or info["meta"]["duration_s"]
            info["segs"] = segs
            info["mp4"] = mp4
            info["cuts"] = count_cuts(mp4) if mp4 else None
            sides.append(info)
        await b.close()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(out, "A", "hook.png"),
                    "-i", os.path.join(out, "B", "hook.png"), "-filter_complex", "vstack=inputs=2",
                    os.path.join(out, "compare.png")], check=False)

    def stats(s):
        words = sum(len(x[2].split()) for x in s["segs"])
        dur = s["duration"] or 0
        first = " ".join(x[2] for x in s["segs"] if x[0] < 3.0)
        start = s["segs"][0][0] if s["segs"] else None
        return {"duration_s": round(dur, 1), "words": words,
                "words_per_sec": round(words / dur, 2) if dur and words else None,
                "cuts": s["cuts"], "cuts_per_10s": round(s["cuts"] / dur * 10, 1) if dur and s["cuts"] is not None else None,
                "first_word_at_s": round(start, 1) if start is not None else None, "spoken_first_3s": first}
    rows = [(s["label"], stats(s), s) for s in sides]
    md = ["# A/B compare", ""]
    for lab, st, s in rows:
        m = s["meta"]
        src = f"{m['url']} ({m['views']:,} views, saves {m['save_pct']}%)" if m else s["source"]
        md.append(f"**{lab}**: {src}")
    md += ["", "| | A | B |", "|---|---|---|"]
    for k in ("duration_s", "words", "words_per_sec", "cuts", "cuts_per_10s", "first_word_at_s", "spoken_first_3s"):
        md.append(f"| {k} | {rows[0][1][k]} | {rows[1][1][k]} |")
    md += ["", "Hook frames: compare.png (A top, B bottom; 0, 0.5, 1, 1.5, 2, 3 s). Whole videos: A/sheet.png, "
           "B/sheet.png.", ""]
    for lab, st, s in rows:
        md += [f"## {lab} transcript (timed)", ""]
        md += [f"- [{x[0]:.1f}s] {x[2]}" for x in s["segs"]] or ["(no captions" + (
            "; rerun with --stt to transcribe)" if not s["meta"] else ")")]
        md.append("")
    open(os.path.join(out, "compare.md"), "w").write("\n".join(md))
    print("\n".join(md[:14 + 7]))
    print(f"\n-> {out}/compare.md, {out}/compare.png")


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def cmd_readability(src):
    text = open(src).read() if os.path.exists(src) else src
    sents = [s for s in re.split(r"(?<=[.!?])\s+|\n+", text) if re.search(r"[A-Za-z]", s)]
    words = re.findall(r"[A-Za-z']+", text)
    if not words:
        print("No words found.")
        return
    syl = [syllables(w) for w in words]
    wps = len(words) / max(len(sents), 1)
    grade = 0.39 * wps + 11.8 * sum(syl) / len(words) - 15.59
    hard = sorted({w for w, s in zip(words, syl) if s >= 3}, key=str.lower)
    longs = sorted(sents, key=lambda s: -len(s.split()))[:3]
    print(f"Grade level (Flesch-Kincaid): {grade:.1f}   (aim for 6 or lower)")
    print(f"Words: {len(words)}  Sentences: {len(sents)}  Avg words/sentence: {wps:.1f}")
    print(f"Speaking time at ~150 words/min: {len(words) / 2.5:.0f} s")
    print(f"Words with 3+ syllables ({len(hard)}): {', '.join(hard[:30])}")
    print("Longest sentences:")
    for s in longs:
        if len(s.split()) > 14:
            print(f"  ({len(s.split())} words) {s.strip()}")


async def cmd_tag(name, top, out, days=None):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b, ctx = await new_ctx(p)
        items = await collect_tag(ctx, name)
        await b.close()
    rows = recent(sorted((summarize(i) for i in items.values()), key=lambda r: r["views"], reverse=True), days)
    if not rows:
        print(f"No videos returned for #{name} (no such tag, nothing recent, or TikTok served a captcha).")
        return
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"tag-{name}.json")
    json.dump(rows, open(path, "w"), indent=2)
    print(f"{len(rows)} videos -> {path}\n")
    print_videos(rows, top)


async def cmd_discover(pages, top, out, days=None):
    from playwright.async_api import async_playwright
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b, ctx = await new_ctx(p)
        for page in pages:
            slug, links = await collect_discover(ctx, page)
            if not links:
                print(f"No discover page for '{slug}' (TikTok only has pages for keywords it created; "
                      f"web-search site:tiktok.com/discover <keyword> for real ones).")
                continue
            print(f"/discover/{slug}: {len(links)} videos, fetching stats...")
            rows = []
            for url in links:
                it = await fetch_item(ctx, url)
                if it:
                    rows.append(summarize(it))
            rows = recent(sorted(rows, key=lambda r: r["views"], reverse=True), days)
            path = os.path.join(out, f"discover-{slug}.json")
            json.dump(rows, open(path, "w"), indent=2)
            print(f"{len(rows)} videos -> {path}\n")
            print_videos(rows, top)
            print()
        await b.close()


async def cmd_shop(keyword, top, out):
    from playwright.async_api import async_playwright
    slug = re.sub(r"[^a-z0-9]+", "-", keyword.lower()).strip("-")
    found = {}

    def add(prods):
        for x in prods or []:
            if x.get("product_id") and (x.get("sold_info") or x.get("rate_info")):
                found.setdefault(x["product_id"], x)
    async with async_playwright() as p:
        b, ctx = await new_ctx(p)
        pg = await ctx.new_page()
        await pg.goto(f"https://shop.tiktok.com/us/k/{slug}", wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(6000)
        raw = await pg.evaluate("()=>{const s=document.querySelector('#__MODERN_ROUTER_DATA__');"
                                "return s?s.textContent:null}")
        # Search results are server-rendered (~30). Ignore the product_list XHRs: they page through the
        # "recommended shop" block, i.e. one brand's other products, not more search results.
        try:
            for page in json.loads(raw)["loaderData"].values():
                for c in ((page or {}).get("page_config") or {}).get("components_map") or []:
                    if c.get("component_name") == "feed_list_search_word":
                        add((c.get("component_data") or {}).get("products"))
        except Exception:
            pass
        await b.close()
    rows = []
    for x in found.values():
        price = x.get("product_price_info") or {}
        rate = x.get("rate_info") or {}
        url = (x.get("seo_url") or {}).get("canonical_url") or f"https://shop.tiktok.com/us/pdp/{x['product_id']}"
        rows.append({"product_id": x["product_id"], "title": x.get("title"),
                     "price": price.get("sale_price_decimal") or price.get("sale_price_format"),
                     "sold_lifetime": int((x.get("sold_info") or {}).get("sold_count") or 0),
                     "rating": rate.get("score"), "reviews": int(rate.get("review_count") or 0),
                     "shop": (x.get("seller_info") or {}).get("shop_name"), "url": url})
    rows.sort(key=lambda r: r["sold_lifetime"], reverse=True)
    if not rows:
        print(f"No products returned for '{keyword}' (no results, or TikTok served a captcha).")
        return
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"shop-{slug}.json")
    json.dump(rows, open(path, "w"), indent=2)
    print(f"{len(rows)} products for '{keyword}' -> {path}  (sold = lifetime units, not recent sales)\n")
    print(f"{'sold':>9} {'price':>8} {'rating':>6} {'reviews':>8}  shop / product / url")
    for r in rows[:top]:
        print(f"{r['sold_lifetime']:>9,} {('$' + str(r['price'])) if r['price'] else '':>8} {r['rating'] or '':>6} "
              f"{r['reviews']:>8,}  {r['shop']}: {(r['title'] or '')[:60]}\n{'':>36}{r['url']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    vi = sp.add_parser("viral")
    vi.add_argument("--days", type=float, default=3, help="only videos posted in the last N days (default 3)")
    vi.add_argument("--top", type=int, default=20)
    vi.add_argument("--category", choices=sorted(CATEGORY_TAGS), help="scan that category's hashtags instead")
    vi.add_argument("--tags", help="comma-separated hashtags to scan instead of the defaults")
    vi.add_argument("--add-tags", help="comma-separated hashtags to scan in addition")
    vi.add_argument("--discover", nargs="*", help="tiktok.com/discover pages to include")
    vi.add_argument("--all", action="store_true", help="include videos without a shop link")
    vi.add_argument("--state", help="state file for views-gained-since-last-run (default OUT/viral-state.json)")
    vi.add_argument("--out", default="tiktok-out")
    v = sp.add_parser("video"); v.add_argument("urls", nargs="+")
    v.add_argument("--out", default="tiktok-out"); v.add_argument("--no-media", action="store_true")
    c = sp.add_parser("compare"); c.add_argument("a"); c.add_argument("b")
    c.add_argument("--stt", action="store_true", help="transcribe local files with ElevenLabs (costs credits)")
    c.add_argument("--out", default="tiktok-out")
    rd = sp.add_parser("readability"); rd.add_argument("text", nargs="+")
    t = sp.add_parser("tag"); t.add_argument("name")
    t.add_argument("--top", type=int, default=15)
    t.add_argument("--days", type=int, help="only videos posted in the last N days")
    t.add_argument("--out", default="tiktok-out")
    d = sp.add_parser("discover"); d.add_argument("pages", nargs="+")
    d.add_argument("--top", type=int, default=15)
    d.add_argument("--days", type=int, help="only videos posted in the last N days")
    d.add_argument("--out", default="tiktok-out")
    sh = sp.add_parser("shop"); sh.add_argument("keyword", nargs="+")
    sh.add_argument("--top", type=int, default=20); sh.add_argument("--out", default="tiktok-out")
    a = ap.parse_args()
    if a.cmd == "readability":
        return cmd_readability(" ".join(a.text))
    ensure_proxy_trust()
    if a.cmd == "viral":
        asyncio.run(cmd_viral(a))
    elif a.cmd == "video":
        asyncio.run(cmd_video(a.urls, a.out, not a.no_media))
    elif a.cmd == "compare":
        asyncio.run(cmd_compare(a))
    elif a.cmd == "tag":
        asyncio.run(cmd_tag(a.name.lstrip("#"), a.top, a.out, a.days))
    elif a.cmd == "discover":
        asyncio.run(cmd_discover(a.pages, a.top, a.out, a.days))
    else:
        asyncio.run(cmd_shop(" ".join(a.keyword), a.top, a.out))


if __name__ == "__main__":
    sys.exit(main())
