#!/usr/bin/env python3
"""Job media (images, sound, video) lives in Google Drive, not in git (Ralph 2026-10-29: "I don't need you to be
saving the images, the sounds, the videos on the Git. Just put them on the drive").

Each job folder (unit = the first two path parts, e.g. ugc/fusou-vanity, grace/voice, products/ai-on-autopilot) has
its media packed into tar parts of at most 95 MB (Kie's free file host refuses ~300 MB, takes 100 MB; tested
2026-10-29), each part hosted on Kie for 3 days, pulled into Drive by Composio GOOGLEDRIVE_UPLOAD_FROM_URL
(account googledrive_lin-ernst) and checked against Drive's own sha256Checksum. Drive layout:
"Repo media (Claude, do not delete)" (1a_SwrVzG0Jmpi1cYzFTnqj1JySCxd7p2) / <repo> / <unit with / as " - ">.
Every unit's record is media-in-drive/<unit with / as __>.json in the repo (parts + every file's sha256).

Run from the repo root (any repo; the keep list is media-in-drive/config.json):
  python3 tools/media/media.py plan                    # units with media not yet in Drive
  python3 tools/media/media.py pack UNIT... | --all    # tar + host on Kie; writes pending parts
  python3 tools/media/media.py pending > pending.json  # list for the workbench upload (see README)
  python3 tools/media/media.py record results.json     # Drive ids + sha256 from the workbench, checked
  python3 tools/media/media.py untrack                 # git rm every media file now safe in Drive
  python3 tools/media/media.py need UNIT               # Drive file ids to get download links for
  python3 tools/media/media.py get UNIT links.json     # download, check, unpack into the repo
  python3 tools/media/media.py check                   # MEDIA_OK when nothing is left to move
Steps with the Composio calls: tools/media/README.md (Mymobileworld).
"""
import hashlib, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests

EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic", ".bmp",
       ".tif", ".tiff", ".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus"}
PART = 95_000_000
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                           check=True).stdout.strip())
REC = ROOT / "media-in-drive"
CFG = json.loads((REC / "config.json").read_text()) if (REC / "config.json").exists() else {}
KEEP = tuple(CFG.get("keep_in_git", [".claude/", "tools/"]))   # code/skill assets that scripts need stay in git


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, check=True).stdout


def is_media(p):
    return Path(p).suffix.lower() in EXT and not p.startswith(KEEP)


def unit_of(p):
    parts = p.split("/")
    return "/".join(parts[:2]) if len(parts) > 2 else (parts[0] if len(parts) > 1 else "_root")


def rec_path(unit):
    return REC / (unit.replace("/", "__") + ".json")


def load(unit):
    f = rec_path(unit)
    return json.loads(f.read_text()) if f.exists() else {"unit": unit, "repo": ROOT.name, "sets": []}


def save(r):
    REC.mkdir(exist_ok=True)
    rec_path(r["unit"]).write_text(json.dumps(r, indent=1) + "\n")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def stored(r):
    """path -> sha256 of every file in a set that is safely in Drive."""
    out = {}
    for s in r["sets"]:
        if all(p.get("drive_id") for p in s["parts"]):
            out.update({k: v[1] for k, v in s["files"].items()})
    return out


def candidates():
    """Media on disk: tracked files + untracked files the old ignore rules let through (media-in-drive/skip.gitignore)."""
    files = git("ls-files", "-z").split("\0")
    excl = REC / "skip.gitignore"
    extra = ["--exclude-from", str(excl)] if excl.exists() else ["--exclude-standard"]
    files += git("ls-files", "-z", "-o", *extra).split("\0")
    out = {}
    for p in files:
        if p and is_media(p) and (ROOT / p).is_file():
            out.setdefault(unit_of(p), []).append(p)
    return out


def todo(unit, paths):
    r = load(unit)
    have = stored(r)
    pend = {k for s in r["sets"] if not all(p.get("drive_id") for p in s["parts"]) for k in s["files"]}
    new = []
    for p in sorted(paths):
        if p in pend:
            continue
        if p not in have or have[p] != sha(ROOT / p):
            new.append(p)
    return r, new


def upload_bytes(name, data):
    for attempt in range(5):
        try:
            r = requests.post(UPLOAD, files={"file": (name, data)}, data={"uploadPath": "repo-media"}, timeout=600)
            d = (r.json().get("data") or {}) if r.ok else {}
            if d.get("downloadUrl") and int(d.get("fileSize", -1)) == len(data):
                return d["downloadUrl"]
        except (requests.RequestException, ValueError):
            pass
        time.sleep(2 ** attempt)
    sys.exit(f"Kie upload failed for {name}")


def pack(unit, paths):
    r, new = todo(unit, paths)
    if not new:
        return f"{unit}: nothing new"
    n = len(r["sets"]) + 1
    files = {p: [(ROOT / p).stat().st_size, sha(ROOT / p)] for p in new}
    tar = subprocess.Popen(["tar", "-C", str(ROOT), "--null", "-T", "-", "-cf", "-"], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
    tar.stdin.write("\0".join(new).encode() + b"\0"); tar.stdin.close()
    parts, i = [], 1
    while True:
        data = tar.stdout.read(PART)
        if not data:
            break
        name = f"{unit.replace('/', '__')}.set{n}.part{i:02d}.tar"
        parts.append({"name": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                      "kie_url": upload_bytes(name, data), "hosted": time.strftime("%Y-%m-%d")})
        i += 1
    if tar.wait() != 0:
        sys.exit(f"tar failed for {unit}")
    r["sets"].append({"set": n, "date": time.strftime("%Y-%m-%d"), "files": files, "parts": parts})
    save(r)
    return f"{unit}: set {n}, {len(new)} files, {len(parts)} parts, {sum(p['size'] for p in parts)/1e6:.0f} MB"


def all_records():
    return [json.loads(f.read_text()) for f in sorted(REC.glob("*.json")) if f.name != "config.json"]


def cmd_plan():
    tot = 0
    for unit, paths in sorted(candidates().items()):
        _, new = todo(unit, paths)
        if new:
            b = sum((ROOT / p).stat().st_size for p in new); tot += b
            print(f"{b/1e6:9.1f} MB {len(new):5d} files  {unit}")
    print(f"total {tot/1e9:.2f} GB")


def cmd_pack(units):
    c = candidates()
    units = sorted(c) if units == ["--all"] else units
    with ThreadPoolExecutor(6) as ex:   # 6 x 95 MB in memory at most; uploads are the bottleneck
        for line in ex.map(lambda u: pack(u, c.get(u, [])), units):
            print(line, flush=True)


def cmd_pending():
    out = [{"repo": r["repo"], "unit": r["unit"], "folder": r["unit"].replace("/", " - "), "sub": s.get("sub"), **p}
           for r in all_records() for s in r["sets"] for p in s["parts"] if not p.get("drive_id")]
    print(json.dumps(out, indent=1))


def cmd_record(path):
    res = {x["name"]: x for x in json.loads(Path(path).read_text())}
    ok = bad = 0
    for r in all_records():
        for s in r["sets"]:
            for p in s["parts"]:
                x = res.get(p["name"])
                if not x or p.get("drive_id"):
                    continue
                if x.get("sha256") == p["sha256"] and int(x.get("size", -1)) == p["size"]:
                    p["drive_id"], p["drive_folder"] = x["id"], x.get("folder_id")
                    p.pop("kie_url", None); ok += 1
                else:
                    bad += 1; print("MISMATCH", p["name"], x)
        save(r)
    print(f"recorded {ok}, mismatched {bad}")


def cmd_untrack():
    tracked = set(git("ls-files", "-z").split("\0"))
    gone = []
    for r in all_records():
        for p, h in stored(r).items():
            f = ROOT / p
            if p in tracked and f.is_file() and sha(f) == h:
                gone.append(p)
    for i in range(0, len(gone), 500):
        git("rm", "-q", "--", *gone[i:i + 500])
    print(f"untracked + removed {len(gone)} files now safe in Drive")


def cmd_need(unit):
    r = load(unit)
    ids = [p["drive_id"] for s in r["sets"] for p in s["parts"] if p.get("drive_id")]
    print(json.dumps(ids))


def cmd_get(unit, links_path):
    """links.json: {drive_id: download url} (GOOGLEDRIVE_DOWNLOAD_FILE s3url). Sets unpack oldest first."""
    links = json.loads(Path(links_path).read_text())
    r = load(unit)
    for s in r["sets"]:
        tar = subprocess.Popen(["tar", "-C", str(ROOT), "-xf", "-"], stdin=subprocess.PIPE)
        for p in s["parts"]:
            h = hashlib.sha256()
            with requests.get(links[p["drive_id"]], stream=True, timeout=600) as resp:
                resp.raise_for_status()
                for b in resp.iter_content(1 << 20):
                    h.update(b); tar.stdin.write(b)
            if h.hexdigest() != p["sha256"]:
                tar.kill(); sys.exit(f"part {p['name']} is corrupt; nothing trusted")
        tar.stdin.close()
        if tar.wait() != 0:
            sys.exit(f"tar failed on set {s['set']}")
    have = stored(r)
    bad = [p for p, h in have.items() if not (ROOT / p).is_file() or sha(ROOT / p) != h]
    print(f"{unit}: {len(have) - len(bad)} files restored and checked" + (f", {len(bad)} WRONG" if bad else ""))


def cmd_check():
    probs = []
    tracked = [p for p in git("ls-files", "-z").split("\0") if p and is_media(p)]
    if tracked:
        probs.append(f"{len(tracked)} media files still tracked by git, e.g. {tracked[0]}")
    for r in all_records():
        for s in r["sets"]:
            miss = [p["name"] for p in s["parts"] if not p.get("drive_id")]
            if miss:
                probs.append(f"{r['unit']} set {s['set']}: {len(miss)} parts not in Drive yet")
    for unit, paths in candidates().items():
        _, new = todo(unit, paths)
        if new:
            probs.append(f"{unit}: {len(new)} media files not stored, e.g. {new[0]}")
    print("\n".join(probs) if probs else "MEDIA_OK")
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    {"plan": lambda: cmd_plan(), "pack": lambda: cmd_pack(a[1:]), "pending": lambda: cmd_pending(),
     "record": lambda: cmd_record(a[1]), "untrack": lambda: cmd_untrack(), "need": lambda: cmd_need(a[1]),
     "get": lambda: cmd_get(a[1], a[2]), "check": lambda: cmd_check()}[a[0]]()
