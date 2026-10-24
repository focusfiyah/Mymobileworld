"""Checks for the camofox-browser install (tools/camofox/GATES.md). One check per call:

    python3 tools/camofox/verify.py <health|browse|mcp|config|docs|merged>

Each prints a success token only after every assertion passes; anything else exits 1.
"""
import json, os, re, subprocess, sys, urllib.request

ROOT = "/home/user"
REPOS = ["Mymobileworld", "Dayone-ai"]
BASE = "http://127.0.0.1:9377"


def call(method, path, body=None, timeout=90):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def health():
    d = call("GET", "/health")
    assert d["engine"] == "camoufox" and d["ok"], d
    print("CAMOFOX_HEALTH_OK")


def browse():
    # a real HTTPS page through the session proxy: fails with SEC_ERROR_UNKNOWN_ISSUER if the CA policy is missing
    t = call("POST", "/tabs", {"userId": "gate", "sessionKey": "default", "url": "https://example.com"})
    assert t.get("httpStatus") == 200, t
    s = call("GET", f"/tabs/{t['tabId']}/snapshot?userId=gate")
    assert "documentation examples" in s["snapshot"], s["snapshot"][:200]
    call("DELETE", f"/tabs/{t['tabId']}?userId=gate")
    print("CAMOFOX_BROWSE_OK")


def mcp():
    # stdio handshake with the same command .mcp.json runs; counts the tools it offers
    cfg = json.load(open(f"{ROOT}/Mymobileworld/.mcp.json"))["mcpServers"]["camofox-browser"]
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18",
             "capabilities": {}, "clientInfo": {"name": "gate", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "camofox_create_tab",
             "arguments": {"url": "https://example.com"}}}]
    env = dict(os.environ, **cfg.get("env", {}))
    p = subprocess.Popen([cfg["command"], *cfg["args"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, text=True, env=env)
    out = {}
    for m in msgs:
        p.stdin.write(json.dumps(m) + "\n"); p.stdin.flush()
        if "id" in m:
            while True:
                line = json.loads(p.stdout.readline())
                if line.get("id") == m["id"]:
                    out[m["id"]] = line; break
    p.kill()
    names = {t["name"] for t in out[2]["result"]["tools"]}
    assert {"camofox_create_tab", "camofox_snapshot", "camofox_click", "camofox_evaluate"} <= names, names
    text = json.dumps(out[3]["result"])
    assert "tabId" in text and not out[3]["result"].get("isError"), text[:300]
    print(f"CAMOFOX_MCP_OK tools={len(names)}")


def config():
    for r in REPOS:
        m = json.load(open(f"{ROOT}/{r}/.mcp.json"))["mcpServers"]
        assert "camofox-browser" in m and "playwright" in m, (r, list(m))  # camofox first, Playwright backup (Ralph 2026-10-24)
        s = json.load(open(f"{ROOT}/{r}/.claude/settings.json"))
        assert {"camofox-browser", "playwright"} <= set(s["enabledMcpjsonServers"]), (r, s["enabledMcpjsonServers"])
        assert s["env"].get("CAMOFOX_CRASH_REPORT_ENABLED") == "false", r
        hooks = json.dumps(s["hooks"])
        assert "camofox_setup.sh" in hooks and "browser_setup.sh" in hooks, r  # Python Playwright stays for scripts
        a = open(f"{ROOT}/Mymobileworld/.claude/hooks/camofox_setup.sh").read()
        assert open(f"{ROOT}/{r}/.claude/hooks/camofox_setup.sh").read() == a, f"{r} hook differs"
        assert "CAMOFOX_CRASH_REPORT_ENABLED=false" in a
    print("CAMOFOX_CONFIG_OK")


def docs():
    files = ["CLAUDE.md", "handoff/REMEMBER_ME.txt", "handoff/REMEMBER_ME_paste.txt", "handoff/GLOBAL_MEMORY.md",
             "handoff/CLAUDE_PREFERENCES.txt", "handoff/MEMORY_SHORT.txt"]
    for r in REPOS:
        for f in files:
            t = open(f"{ROOT}/{r}/{f}").read().lower()
            assert "camofox" in t and "playwright" in t and "backup" in t, f"{r}/{f} lacks the camofox-first rule"
        short = open(f"{ROOT}/{r}/handoff/MEMORY_SHORT.txt").read()
        assert len(short) <= 2000, f"{r} MEMORY_SHORT {len(short)} chars"
    print("CAMOFOX_DOCS_OK")


def merged():
    for r in REPOS:
        g = lambda *a: subprocess.run(["git", "-C", f"{ROOT}/{r}", *a], capture_output=True, text=True)
        g("fetch", "-q", "origin", "main")
        assert g("cat-file", "-e", "origin/main:.claude/hooks/camofox_setup.sh").returncode == 0, f"{r} main lacks hook"
        assert "camofox-browser" in g("show", "origin/main:.mcp.json").stdout, f"{r} main .mcp.json"
    print("CAMOFOX_MERGED_OK")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
