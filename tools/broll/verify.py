"""Checks for the broll-mcp install (tools/broll/GATES.md). One check per call:

    python3 tools/broll/verify.py <review|search|cut|config|docs|merged>

Each prints a success token only after every assertion passes; anything else exits 1.
search/cut talk to archive.org through the same command .mcp.json runs (free, no key).
"""
import json, os, subprocess, sys

ROOT = "/home/user"
REPOS = ["Mymobileworld", "Dayone-ai"]
SHA = "d8fda0a4972235fb7591187242a4e583aca84f12"
HERE = os.path.dirname(os.path.abspath(__file__))


def session(calls, timeout=600):
    """Run the .mcp.json broll command, initialize, list tools, then make each tools/call; return the results."""
    cfg = json.load(open(f"{ROOT}/Mymobileworld/.mcp.json"))["mcpServers"]["broll"]
    env = dict(os.environ, **cfg.get("env", {}))
    p = subprocess.Popen([cfg["command"], *cfg["args"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, text=True, env=env)
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18",
             "capabilities": {}, "clientInfo": {"name": "gate", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}]
    msgs += [{"jsonrpc": "2.0", "id": 10 + i, "method": "tools/call", "params": {"name": n, "arguments": a}}
             for i, (n, a) in enumerate(calls)]
    out = {}
    try:
        for m in msgs:
            p.stdin.write(json.dumps(m) + "\n"); p.stdin.flush()
            if "id" in m:
                while True:
                    line = p.stdout.readline()
                    assert line, "server closed stdout"
                    d = json.loads(line)
                    if d.get("id") == m["id"]:
                        out[m["id"]] = d; break
    finally:
        p.kill()
    names = {t["name"] for t in out[2]["result"]["tools"]}
    assert names == {"search_footage", "inspect_item", "extract_clip", "get_provenance"}, names
    return [out[10 + i]["result"] for i in range(len(calls))]


def review():
    s = open(f"{HERE}/SOURCE.md").read()
    for need in (SHA, "SkillSpector 2.12.0", "Verdict: CAUTION", "Manual review"):
        assert need in s, need
    print("BROLL_REVIEW_OK")


def search():
    (r,) = session([("search_footage", {"brief": "aerial highway traffic 1950s"})])
    assert not r.get("isError"), json.dumps(r)[:400]
    items = r["structuredContent"]["results"]
    assert len(items) >= 1 and all(i.get("identifier") and "license" in i for i in items), items[:1]
    print(f"BROLL_SEARCH_OK items={len(items)} first={items[0]['identifier']}")


def cut():
    # a known public-domain Prelinger film (the README's own example); 4 s cut, then its provenance
    r, = session([("inspect_item", {"identifier": "AboutBan1935"})])
    assert not r.get("isError"), json.dumps(r)[:400]
    f = r["structuredContent"].get("file") or r["structuredContent"]["files"][0]["name"]
    c, = session([("extract_clip", {"identifier": "AboutBan1935", "file": f if isinstance(f, str) else f["name"],
                                    "start_s": 300, "duration_s": 4, "label": "gate"})])
    assert not c.get("isError"), json.dumps(c)[:400]
    sc = c["structuredContent"]
    mp4 = sc["path"]; prov = sc.get("provenance_path") or mp4.rsplit(".", 1)[0] + ".provenance.json"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                               capture_output=True, text=True).stdout)
    assert abs(dur - 4.0) <= 0.1, dur
    p = json.load(open(prov))
    assert p["source"]["identifier"] == "AboutBan1935" and p["license"]["commercial_use"], p["license"]
    print(f"BROLL_CUT_OK dur={dur:.3f} commercial_use={p['license']['commercial_use']} path={mp4}")


def config():
    first = None
    for r in REPOS:
        b = json.load(open(f"{ROOT}/{r}/.mcp.json"))["mcpServers"]["broll"]
        assert f"git+https://github.com/edigeh/broll-mcp@{SHA}" in b["args"], (r, b["args"])
        assert "claude-" not in json.dumps(b).replace("claude-code", ""), "model id in config"
        first = first or b
        assert b == first, f"{r} broll entry differs"
        s = json.load(open(f"{ROOT}/{r}/.claude/settings.json"))
        assert "broll" in s["enabledMcpjsonServers"], r
        assert "broll_setup.sh" in json.dumps(s["hooks"]), r
        assert open(f"{ROOT}/{r}/.claude/hooks/broll_setup.sh").read() == \
            open(f"{ROOT}/Mymobileworld/.claude/hooks/broll_setup.sh").read(), f"{r} hook differs"
    print("BROLL_CONFIG_OK")


def docs():
    files = ["CLAUDE.md", "handoff/REMEMBER_ME.txt", "handoff/REMEMBER_ME_paste.txt", "handoff/GLOBAL_MEMORY.md",
             "handoff/CLAUDE_PREFERENCES.txt", "handoff/MEMORY_SHORT.txt"]
    for r in REPOS:
        for f in files:
            assert "broll" in open(f"{ROOT}/{r}/{f}").read().lower(), f"{r}/{f} lacks broll"
        short = open(f"{ROOT}/{r}/handoff/MEMORY_SHORT.txt").read()
        assert len(short) <= 2000, f"{r} MEMORY_SHORT {len(short)} chars"
    print("BROLL_DOCS_OK")


def merged():
    for r in REPOS:
        g = lambda *a: subprocess.run(["git", "-C", f"{ROOT}/{r}", *a], capture_output=True, text=True)
        g("fetch", "-q", "origin", "main")
        assert SHA in g("show", "origin/main:.mcp.json").stdout, f"{r} main .mcp.json lacks broll"
        assert g("cat-file", "-e", "origin/main:.claude/hooks/broll_setup.sh").returncode == 0, f"{r} main lacks hook"
    print("BROLL_MERGED_OK")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
