"""Weekly content batch for Ralph (2026-11-15): one scripts.json per week -> AI twin Flow kits, faceless motion videos,
carousels. Rules: Mymobileworld/Dayone-ai CLAUDE.md "AI twin videos of Ralph", "Grace's methods and hooks stay private".

  python3 batch.py rooms WEEK        Pexels room candidates per twin shot -> WEEK/rooms/<T>_<n>/cand_*.jpg + contact.jpg (pick by looking)
  python3 batch.py kit WEEK          Flow kit per twin video from the picked rooms (WEEK/rooms/picks.json) -> WEEK/kits/<T>/
  python3 batch.py bg WEEK           Pexels background VIDEOS per faceless line -> WEEK/bg/<F>_<n>.mp4 (+ contact sheet)
  (faceless.py renders the faceless videos, carousel.py the carousels)
"""
import json, os, sys, urllib.request, urllib.parse, pathlib
from io import BytesIO
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
TWIN = pathlib.Path("/home/user/Mymobileworld/ralph/twin-shorts")
UA = {"User-Agent": "Mozilla/5.0"}
PX = {"Authorization": os.environ.get("PEXELS_API_KEY", ""), **UA}

ANGLES = {   # camera angle per shot, written for Veo (Flow); one per shot, never the same twice in a video
    "low": "Low angle: the camera sits below his chest line looking slightly up at him, medium shot from the waist up, slow push-in. He stands and talks straight to the lens with one open hand gesture at chest height.",
    "side": "Three-quarter side angle: the camera is 45 degrees to his left at chest height, medium shot from the waist up. He turns his head to the lens and talks to camera, one relaxed hand gesture toward the room.",
    "high": "High angle: the camera is a little above his eye line and to his right, medium close-up. He sits with both forearms resting on the table, turns to the lens and talks to camera; hands stay relaxed, at most one small open-palm gesture.",
    "close": "Close-up from the chest up at eye level, shallow depth of field, slow push-in. He leans slightly toward the lens and talks straight to camera, a small smile on the last words, hands out of frame.",
    "walk": "Medium-wide shot from the knees up at eye level. He takes one step toward the camera and stops, then talks straight to camera with one relaxed hand gesture.",
}
HEAD = ("Vertical 9:16 talking-head video, 8 seconds. Image 1 is the real man: keep his exact face, rimless glasses, smooth bald head and beard shape from image 1. "
        "Image 2 is his reference sheet: same build, black crew-neck t-shirt, beard clean cut with the grey at the chin exactly as shown. Image 3 is the room he is in.")
TAIL = ("Bright, even daylight, natural colours, sharp face, real skin texture. He moves naturally, blinks and breathes. No counting on fingers, no pointing. "
        "No music, no sound effects, no captions, no on-screen text, no brand names or logos anywhere, no other people.")


def get(url, hdr=UA): return urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=60).read()


def sheet(paths, out, tw=220, th=300):
    S = Image.new("RGB", (tw * len(paths), th), "white"); d = ImageDraw.Draw(S)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB"); im.thumbnail((tw, th - 18)); S.paste(im, (i * tw, 18)); d.text((i * tw + 3, 3), str(i), fill="black")
    S.save(out)


def rooms(week):
    d = json.load(open(HERE / week / "scripts.json"))
    for t in d["twin"]:
        for n, s in enumerate(t["shots"], 1):
            o = HERE / week / "rooms" / f"{t['id']}_{n}"; o.mkdir(parents=True, exist_ok=True); got = []
            r = json.loads(get("https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": s["room"], "per_page": 6, "orientation": "landscape"}), PX))
            for k, p in enumerate(r["photos"][:6]):
                f = o / f"cand_{k}.jpg"; Image.open(BytesIO(get(p["src"]["original"] + "?auto=compress&w=1800"))).convert("RGB").save(f, quality=92)
                got.append({"file": f.name, "url": p["url"], "alt": p.get("alt", "")})
            json.dump(got, open(o / "cand.json", "w"), indent=1); sheet([o / g["file"] for g in got], o / "contact.jpg")
            print("ROOMS", t["id"], n, len(got))


def kit(week):
    d = json.load(open(HERE / week / "scripts.json")); picks = json.load(open(HERE / week / "rooms" / "picks.json"))
    for t in d["twin"]:
        o = HERE / week / "kits" / t["id"]; o.mkdir(parents=True, exist_ok=True); out = []
        for n, s in enumerate(t["shots"], 1):
            key = f"{t['id']}_{n}"; pk = picks[key]
            src = HERE / week / "rooms" / key / pk["file"]; im = Image.open(src).convert("RGB"); im.thumbnail((1600, 1600))
            room = f"{key}_room.jpg"; im.save(o / room, quality=90)
            line = s["line"].replace("KIT", "kit")             # Veo spells capitalised keywords letter by letter
            p = f"{HEAD}\nRoom: he is in {pk['desc']}.\nShot: {ANGLES[s['angle']]}\nHe says, in a warm, clear American male voice at a natural pace, exactly: \"{line}\"\n{TAIL}"
            out.append({"shot": key, "angle": s["angle"], "line": s["line"], "room": room, "room_source": pk["url"], "prompt": p})
            (o / f"prompt_{key}.txt").write_text(p)
        json.dump(out, open(o / "kit.json", "w"), indent=1); print("KIT", t["id"], len(out))


def bg(week):
    d = json.load(open(HERE / week / "scripts.json")); o = HERE / week / "bg"; o.mkdir(parents=True, exist_ok=True); log = {}
    for f in d["faceless"]:
        for n, l in enumerate(f["lines"], 1):
            r = json.loads(get("https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": l["bg"], "per_page": 5, "orientation": "portrait"}), PX))
            cands = []
            for v in r["videos"][:4]:
                fs = sorted([x for x in v["video_files"] if x.get("height") and x["height"] >= 1280 and x["file_type"] == "video/mp4"], key=lambda x: x["height"])
                if not fs: continue
                cands.append({"id": v["id"], "url": v["url"], "file": fs[0]["link"], "pic": v["image"], "dur": v["duration"]})
            key = f"{f['id']}_{n}"; log[key] = cands
            paths = []
            for k, c in enumerate(cands):
                p = o / f"{key}_c{k}.jpg"; Image.open(BytesIO(get(c["pic"]))).convert("RGB").save(p); paths.append(p)
            if paths: sheet(paths, o / f"{key}_contact.jpg", 160, 300)
            print("BG", key, len(cands))
    json.dump(log, open(o / "cand.json", "w"), indent=1)


if __name__ == "__main__":
    {"rooms": rooms, "kit": kit, "bg": bg}[sys.argv[1]](sys.argv[2])
