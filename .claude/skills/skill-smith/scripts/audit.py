#!/usr/bin/env python3
"""Mechanical audit of Claude skills (skill-smith).

Usage:
  audit.py PATH [--deploy] [--json OUT] [--repo ROOT]

PATH is one skill folder (contains SKILL.md) or a folder of skill folders.
--deploy compares each skill with its deployed copies listed in ROOT/deploy.json
(ROOT defaults to the git root above PATH). Exit code 1 when any ERROR is found.

Checks: frontmatter (name = folder, description present, third person, <= 1024 chars),
SKILL.md length (error > 200 lines), table of contents in files over 100 lines,
dead-weight phrases used as instructions, requests to write out reasoning,
dated notes piling up in SKILL.md, links that do not resolve inside the skill,
paragraphs duplicated across skills, and drift between source and deployments.
Judgment calls (out of date, contradictions, not needed) are for the reader.
"""
import argparse, glob, hashlib, json, os, re, subprocess, sys

DEAD = re.compile(r"\b(think (really |very )?carefully|think step[- ]by[- ]step|take a deep breath|"
                  r"double[- ]check (your|all|everything|the work)|make sure to double[- ]check)\b", re.I)
REASONING = re.compile(r"\b(show|write out|explain) (all |your |the )?(full )?(reasoning|chain of thought)\b", re.I)
DATE = re.compile(r"\b20\d\d-\d\d-\d\d\b")
LINK = re.compile(r"\]\(([^)#\s]+)\)|`((?:references|scripts|templates|assets|examples)/[^`\s]+)`")
PERSON = re.compile(r"^\s*(I |I'm |You |You can |We )", re.I)


def frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    raw, body = text[3:end], text[end + 4:]
    fm, key = {}, None
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            fm[key] = "" if val in ("|", ">", "|-", ">-") else val.strip('"\'')
        elif key and line.startswith((" ", "\t")):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    for k in fm:
        fm[k] = re.sub(r"\s+", " ", fm[k].replace("\\n", " ").replace('\\"', '"')).strip()
    return fm, body


def quoted(line, m):
    """True when the phrase is quoted or code, i.e. mentioned rather than instructed."""
    before, after = line[:m.start()], line[m.end():]
    return (before.count('"') % 2 == 1 and '"' in after) or (before.count("`") % 2 == 1) or \
        before.rstrip().endswith(("\u201c", "'", '"')) or "no \"" in before.lower()[-6:]


def md_files(skill):
    for root, dirs, files in os.walk(skill):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
        for f in files:
            if f.endswith(".md"):
                yield os.path.join(root, f)


def in_fence_lines(text):
    fence, out = False, []
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            out.append(True)
            continue
        out.append(fence)
    return out


def audit_skill(skill, upstream=()):
    name = os.path.basename(os.path.normpath(skill))
    out = []
    add = lambda lvl, where, msg: out.append({"skill": name, "level": lvl, "where": where, "msg": msg})
    p = os.path.join(skill, "SKILL.md")
    if not os.path.isfile(p):
        add("ERROR", "SKILL.md", "missing")
        return out, {}
    text = open(p, encoding="utf-8", errors="replace").read()
    fm, body = frontmatter(text)
    if fm is None:
        add("ERROR", "SKILL.md:1", "no YAML frontmatter")
        fm = {}
    if fm.get("name") and fm["name"] != name:
        add("ERROR", "SKILL.md:2", f"name '{fm['name']}' does not match folder '{name}'")
    desc = fm.get("description", "")
    if not desc:
        add("ERROR", "SKILL.md", "no description")
    elif len(desc) > 1024:
        add("ERROR", "SKILL.md", f"description {len(desc)} chars (claude.ai limit 1024)")
    if desc and PERSON.match(desc):
        add("WARN", "SKILL.md", "description not in third person")
    if desc and not re.search(r"\b(use (when|for|whenever|this|it|on|before|to)|when (the user|someone|ralph)|trigger|entry point)", desc, re.I):
        add("WARN", "SKILL.md", "description does not say when to use the skill")
    n = text.count("\n") + 1
    if n > 200:
        add("ERROR", "SKILL.md", f"{n} lines (limit 200)")
    dates = len(DATE.findall(body))
    if dates > 8:
        add("WARN", "SKILL.md", f"{dates} dated notes in the body; history belongs in CHANGELOG.md")
    vendored = os.path.isfile(os.path.join(skill, "SOURCE.md")) or name in upstream
    for f in md_files(skill):
        rel = os.path.relpath(f, skill)
        t = open(f, encoding="utf-8", errors="replace").read()
        lines = t.splitlines()
        if len(lines) > 100 and rel != "SKILL.md" and not re.search(r"(?im)^#+\s*(contents|table of contents)\b|^\s*-\s*\[.+\]\(#", t[:4000]):
            add("WARN", rel, f"{len(lines)} lines and no table of contents")
        fence = in_fence_lines(t)
        for i, line in enumerate(lines, 1):
            if fence[i - 1]:
                continue
            for rx, msg in ((DEAD, "dead-weight phrase"), (REASONING, "asks to write out reasoning (reasoning_extraction risk)")):
                m = rx.search(line)
                if m and not quoted(line, m) and not re.search(r"\b(no|never|avoid|don't|do not|delete|remove)\b", line[:m.start()], re.I):
                    add("WARN", f"{rel}:{i}", f"{msg}: '{m.group(0)}'")
            if rel == "SKILL.md" or rel.startswith("references"):
                for m in LINK.finditer(line):
                    target = (m.group(1) or m.group(2)).rstrip(".,;:")
                    if re.match(r"^[a-z]+://|^mailto:|^#", target) or "<" in target or "*" in target:
                        continue
                    base = os.path.dirname(f) if m.group(1) else skill
                    path = os.path.normpath(os.path.join(base, target))
                    if not path.startswith(os.path.normpath(skill)):
                        add("WARN", f"{rel}:{i}", f"link leaves the skill ({target}); dead in a claude.ai upload")
                    elif not os.path.exists(path) and not glob.glob(os.path.join(os.path.dirname(os.path.normpath(skill)), "*", target)):
                        add("ERROR" if not vendored else "WARN", f"{rel}:{i}", f"broken link {target}")
    return out, {"lines": n, "desc_len": len(desc), "vendored": vendored}


def paragraphs(skill):
    for f in md_files(skill):
        t = open(f, encoding="utf-8", errors="replace").read()
        for para in re.split(r"\n\s*\n", t):
            norm = re.sub(r"\W+", " ", para).strip().lower()
            if len(norm) >= 160 and not para.lstrip().startswith(("```", "|")):
                yield os.path.relpath(f, skill), norm


def normalized_tree(skill):
    """Hash files, comparing SKILL.md by parsed frontmatter + body so YAML reformatting is not drift."""
    res = {}
    for root, dirs, files in os.walk(skill):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
        for f in files:
            if f in (".DS_Store",) or f.endswith(".pyc"):
                continue
            p = os.path.join(root, f)
            data = open(p, "rb").read()
            rel = os.path.relpath(p, skill)
            if rel == "SKILL.md":
                fm, body = frontmatter(data.decode("utf-8", "replace"))
                data = json.dumps([fm, body.strip()], sort_keys=True).encode()
            res[rel] = hashlib.sha256(data).hexdigest()
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--json")
    ap.add_argument("--repo")
    a = ap.parse_args()
    path = os.path.abspath(a.path)
    skills = [path] if os.path.isfile(os.path.join(path, "SKILL.md")) else \
        sorted(os.path.join(path, d) for d in os.listdir(path) if os.path.isfile(os.path.join(path, d, "SKILL.md")))
    root = a.repo or subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"],
                                    capture_output=True, text=True).stdout.strip()
    cfgp = os.path.join(root, "deploy.json")
    cfg = json.load(open(cfgp)) if root and os.path.isfile(cfgp) else {}
    findings, stats = [], {}
    for s in skills:
        f, st = audit_skill(s, cfg.get("upstream", {}))
        findings += f
        stats[os.path.basename(s)] = st
    if len(skills) > 1:
        seen = {}
        for s in skills:
            for rel, norm in set(paragraphs(s)):
                seen.setdefault(hashlib.sha1(norm.encode()).hexdigest(), []).append((os.path.basename(s), rel))
        for locs in seen.values():
            owners = sorted({k for k, _ in locs})
            if len(owners) > 1:
                findings.append({"skill": owners[0], "level": "WARN", "where": ", ".join(f"{k}/{r}" for k, r in locs),
                                 "msg": f"same paragraph in {len(owners)} skills; give it one home"})
    if a.deploy:
        if not cfg:
            sys.exit("--deploy needs deploy.json at the repo root")
        for s in skills:
            name = os.path.basename(s)
            src = normalized_tree(s)
            for target in cfg.get("skills", {}).get(name, cfg.get("default", [])):
                dst = os.path.join(cfg["targets"][target], name)
                if not os.path.isdir(dst):
                    if os.path.isdir(cfg["targets"][target]):
                        findings.append({"skill": name, "level": "WARN", "where": target, "msg": "not deployed"})
                    continue
                d = normalized_tree(dst)
                diff = sorted(k for k in set(src) | set(d) if src.get(k) != d.get(k))
                if diff:
                    findings.append({"skill": name, "level": "WARN", "where": target,
                                     "msg": f"deployment differs from source: {', '.join(diff[:5])}"})
            acct = cfg.get("account_copy")
            bases = glob.glob(os.path.expanduser(acct)) if acct else []
            if bases:
                adir = os.path.join(bases[0], name)
                if os.path.isdir(adir):
                    d = normalized_tree(adir)
                    diff = sorted(k for k in set(src) | set(d) if src.get(k) != d.get(k))
                    if diff:
                        findings.append({"skill": name, "level": "WARN", "where": "claude.ai account",
                                         "msg": f"account copy differs from source (re-upload zip): {', '.join(diff[:5])}"})
    errs = sum(f["level"] == "ERROR" for f in findings)
    warns = len(findings) - errs
    for f in sorted(findings, key=lambda x: (x["skill"], x["level"] != "ERROR")):
        print(f"{f['level']:5} {f['skill']}: {f['where']}: {f['msg']}")
    print(f"\n{len(skills)} skills, {errs} errors, {warns} warnings")
    if a.json:
        json.dump({"skills": stats, "findings": findings}, open(a.json, "w"), indent=1)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
