#!/usr/bin/env python3
"""Deploy one skill from focusfiyah/claude-skills (skill-smith).

Usage: deploy.py NAME [--repo ROOT] [--no-zip]

Copies skills/NAME to every target deploy.json lists for it (replacing the old copy),
then builds dist/NAME-skill.zip for the claude.ai upload. Refuses when the audit finds
errors or the description is over 1024 characters. Commit in each target repo afterwards.
"""
import argparse, json, os, shutil, subprocess, sys, zipfile

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("name")
ap.add_argument("--repo")
ap.add_argument("--no-zip", action="store_true")
a = ap.parse_args()
here = os.path.dirname(os.path.abspath(__file__))
root = a.repo or subprocess.run(["git", "-C", here, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
src = os.path.join(root, "skills", a.name)
if not os.path.isfile(os.path.join(src, "SKILL.md")):
    sys.exit(f"no skill at {src}")
if subprocess.run([sys.executable, os.path.join(here, "audit.py"), src]).returncode:
    sys.exit("audit found errors; fix them before deploying")
cfg = json.load(open(os.path.join(root, "deploy.json")))
ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "node_modules")
for target in cfg.get("skills", {}).get(a.name, cfg.get("default", [])):
    base = cfg["targets"][target]
    if not os.path.isdir(base):
        print(f"skip {target}: {base} not in this session")
        continue
    dst = os.path.join(base, a.name)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=ignore)
    print(f"deployed to {dst}")
if not a.no_zip:
    os.makedirs(os.path.join(root, "dist"), exist_ok=True)
    z = os.path.join(root, "dist", f"{a.name}-skill.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for r, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "node_modules")]
            for f in files:
                if f.endswith(".pyc") or f == ".DS_Store":
                    continue
                p = os.path.join(r, f)
                zf.write(p, os.path.join(a.name, os.path.relpath(p, src)))
    print(f"zip: {z} (Ralph uploads it at claude.ai > Settings > Capabilities > Skills)")
