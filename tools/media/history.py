#!/usr/bin/env python3
"""Git history cleanup for job media (Ralph 2026-10-29: "Go ahead with the cleanup").

Before the history is rewritten, every media version that lived only in git history (older versions of stills and
clips, media on unmerged branches) is stored in Drive like the rest (media.py), as a "git-history" set in the job's
media-in-drive record, in a subfolder "Older versions (from git history)" of the job's Drive folder. Restored with
`media.py get UNIT`, they land in UNIT/_git_history/<blob>_<name>.

  python3 tools/media/history.py snapshot OUT.json   # non-media files of every origin branch (before the rewrite)
  python3 tools/media/history.py pack                # store history-only media: tar parts on Kie, records pending
  python3 tools/media/history.py check               # HISTORY_STORED when nothing is left and all are in Drive
  python3 tools/media/history.py same-files          # main's non-media files match the snapshot
  python3 tools/media/history.py branches-kept       # every snapshot branch is on GitHub with the same files
  python3 tools/media/history.py fresh-clone-check   # clone from GitHub, no job media anywhere, under 1 GB
Run from the Mymobileworld root; the rewrite itself is in tools/media/README.md ("History cleanup").
"""
import hashlib, io, json, os, shutil, subprocess, sys, tarfile, tempfile, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import media  # noqa: E402  (EXT, is_media, unit_of, load/save records, upload_bytes, PART)

SNAP = Path(os.environ.get("HISTORY_SNAPSHOT", "/tmp/mmw_history_snapshot.json"))
SUB = "Older versions (from git history)"


def git(*a, text=True):
    return subprocess.run(["git", "-C", str(media.ROOT), *a], capture_output=True, text=text, check=True).stdout


def branches():
    return [r for r in git("for-each-ref", "refs/remotes/origin", "--format=%(refname:short)").split()
            if r not in ("origin", "origin/HEAD")]


def tree(ref):
    out = {}
    for line in git("ls-tree", "-r", "-z", ref).split("\0"):
        if line:
            meta, path = line.split("\t", 1)
            out[path] = meta.split()[2]
    return out


def non_media(ref):
    return {p: b for p, b in tree(ref).items() if not media.is_media(p)}


def history_media():
    """{blob id: (path, size)} for every media blob reachable from any branch."""
    objs = git("rev-list", "--objects", "--all")
    want = {}
    for line in objs.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2 and media.is_media(parts[1]):
            want.setdefault(parts[0], parts[1])
    return want


def stored_sha256():
    return {v[1] for r in media.all_records() for s in r["sets"] for v in s["files"].values()
            if all(p.get("drive_id") for p in s["parts"])}


def pending_sha256():
    return {v[1] for r in media.all_records() for s in r["sets"] for v in s["files"].values()}


def cat_blobs(ids):
    """Yield (id, bytes) for each blob, through one git cat-file --batch process."""
    p = subprocess.Popen(["git", "-C", str(media.ROOT), "cat-file", "--batch"], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    for i in ids:
        p.stdin.write(i.encode() + b"\n"); p.stdin.flush()
        head = p.stdout.readline().split()
        size = int(head[2])
        data = p.stdout.read(size); p.stdout.read(1)
        yield i, data
    p.stdin.close(); p.wait()


def missing():
    """[(blob id, path, sha256, size)] media in history whose content is in no record yet (data re-read when packed)."""
    have = pending_sha256()
    want = history_media()
    out, seen = [], set()
    for i, data in cat_blobs(list(want)):
        h = hashlib.sha256(data).hexdigest()
        if h in have or h in seen:
            continue
        seen.add(h)
        out.append((i, want[i], h, len(data)))
    return out


class Parts(io.RawIOBase):
    """File-like sink that cuts the tar stream into <=95 MB parts and hosts each one on Kie."""
    def __init__(self, stem):
        self.stem, self.buf, self.parts = stem, bytearray(), []

    def writable(self):
        return True

    def write(self, b):
        self.buf += b
        while len(self.buf) >= media.PART:
            self._flush(bytes(self.buf[:media.PART])); del self.buf[:media.PART]
        return len(b)

    def _flush(self, data):
        name = f"{self.stem}.part{len(self.parts) + 1:02d}.tar"
        self.parts.append({"name": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                           "kie_url": media.upload_bytes(name, data), "hosted": time.strftime("%Y-%m-%d")})

    def finish(self):
        if self.buf:
            self._flush(bytes(self.buf)); self.buf = bytearray()
        return self.parts


def cmd_snapshot(out):
    snap = {r: non_media(r) for r in branches()}
    Path(out).write_text(json.dumps(snap))
    print(f"snapshot: {len(snap)} branches -> {out}")


def cmd_pack():
    todo = missing()
    by_unit = {}
    for i, path, h, size in todo:
        by_unit.setdefault(media.unit_of(path), []).append((i, path, h))
    print(f"{len(todo)} history-only media files, {sum(x[3] for x in todo)/1e9:.2f} GB, {len(by_unit)} units", flush=True)
    for unit, items in sorted(by_unit.items()):
        r = media.load(unit)
        n = len(r["sets"]) + 1
        sink = Parts(f"{unit.replace('/', '__')}.history{n}")
        tf = tarfile.open(fileobj=sink, mode="w|")
        files, origins = {}, {}
        paths = {i: (path, h) for i, path, h in items}
        for i, data in cat_blobs(list(paths)):
            path, h = paths[i]
            member = f"{unit}/_git_history/{i[:12]}_{Path(path).name}"
            ti = tarfile.TarInfo(member); ti.size = len(data); ti.mtime = int(time.time())
            tf.addfile(ti, io.BytesIO(data))
            files[member] = [len(data), h]; origins[member] = path
        tf.close()
        r["sets"].append({"set": n, "kind": "git-history", "sub": SUB, "date": time.strftime("%Y-%m-%d"),
                          "files": files, "origins": origins, "parts": sink.finish()})
        media.save(r)
        print(f"{unit}: history set {n}, {len(items)} files, {len(r['sets'][-1]['parts'])} parts", flush=True)


def cmd_check():
    left = missing()
    undrive = [p["name"] for r in media.all_records() for s in r["sets"] if s.get("kind") == "git-history"
               for p in s["parts"] if not p.get("drive_id")]
    if left or undrive:
        print(f"{len(left)} history media not packed, {len(undrive)} parts not in Drive"); sys.exit(1)
    print("HISTORY_STORED")


def cmd_same_files():
    snap = json.loads(SNAP.read_text())
    a, b = snap["origin/main"], non_media("origin/main")
    diff = sorted(set(a.items()) ^ set(b.items()))
    print("SAME_FILES_OK" if not diff else f"{len(diff)} differences, e.g. {diff[:3]}")
    sys.exit(1 if diff else 0)


def cmd_branches_kept():
    snap = json.loads(SNAP.read_text())
    git("fetch", "-q", "--prune", "origin")
    now = set(branches())
    bad = [r for r in snap if r not in now or non_media(r) != snap[r]]
    print("BRANCHES_KEPT" if not bad else f"{len(bad)} branches differ or are gone, e.g. {bad[:5]}")
    sys.exit(1 if bad else 0)


def cmd_fresh_clone_check():
    url = git("remote", "get-url", "origin").strip()
    d = tempfile.mkdtemp(prefix="mmw_fresh_")
    try:
        subprocess.run(["git", "clone", "-q", "--no-checkout", url, d + "/r"], check=True)
        r = subprocess.run(["git", "-C", d + "/r", "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*"],
                           check=True)
        objs = subprocess.run(["git", "-C", d + "/r", "rev-list", "--objects", "--all"], capture_output=True,
                              text=True, check=True).stdout
        bad = [l.split(" ", 1)[1] for l in objs.splitlines() if " " in l and media.is_media(l.split(" ", 1)[1])]
        size = sum(f.stat().st_size for f in Path(d, "r", ".git").rglob("*") if f.is_file())
        print(f"fresh clone .git {size/1e9:.2f} GB, media objects {len(bad)}")
        ok = not bad and size < 1e9
        print("FRESH_CLONE_OK" if ok else f"not clean, e.g. {bad[:3]}")
        sys.exit(0 if ok else 1)
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    {"snapshot": lambda: cmd_snapshot(a[1] if len(a) > 1 else SNAP), "pack": cmd_pack, "check": cmd_check,
     "same-files": cmd_same_files, "branches-kept": cmd_branches_kept,
     "fresh-clone-check": cmd_fresh_clone_check}[a[0]]()
