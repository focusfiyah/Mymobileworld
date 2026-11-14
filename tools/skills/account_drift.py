"""Which of Ralph's claude.ai skills are out of date, missing, or should be removed? (Ralph 2026-11-14 weekly audit:
"give me the skills that I need to upload, and also give me the names of the skills I need to remove").

Compares the claude.ai account copies, which every cloud session syncs to ~/.claude/skills/synced/<id>/ (manifest.json
says each skill's source), with the skill home focusfiyah/claude-skills/skills. Frontmatter formatting is ignored
(claude.ai re-writes the YAML); the description text, the SKILL.md body and every other file are compared.

  python3 tools/skills/account_drift.py [--home /home/user/claude-skills]
  -> UPLOAD <name> (stale or missing) / REMOVE <name> (ours on claude.ai, gone from the home) / ACCOUNT_OK
Anthropic's own skills (source anthropic*) are never listed. A skill listed in KEEP_OFF_ACCOUNT is not asked for.
"""
import filecmp, glob, json, os, re, sys

KEEP_OFF_ACCOUNT = {  # in the home but not meant for claude.ai: the social/marketing set comes from his plugin directory
    "audience-research", "brand-profile", "carousel-writer", "content-pillars", "creator-monetization", "hashtag-strategy",
    "hook-writer", "instagram-growth", "lead-magnets-and-funnels", "social-selling-and-dm", "social-seo",
    "social-strategy", "tiktok-growth", "tiktok-photo-mode", "tiktok-script"}

home = (sys.argv[sys.argv.index("--home") + 1] if "--home" in sys.argv else "/home/user/claude-skills") + "/skills"
synced = sorted(glob.glob(os.path.expanduser("~/.claude/skills/synced/*/manifest.json")))
if not synced:
    sys.exit("no synced account skills in ~/.claude/skills/synced (not a cloud session?)")
acct_dir = os.path.dirname(synced[0]); manifest = json.load(open(synced[0]))["skills"]
ours = {s["name"] for s in manifest if not str(s.get("source", "")).startswith("anthropic")}


def norm(v):
    """Words only: claude.ai re-quotes and re-folds the YAML (\\n escapes, '>-' block markers), so compare the words."""
    return " ".join(re.findall(r"[\w$%&+]+", str(v).replace("\\n", " ")))


def parse(p):
    t = open(p).read(); m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    if not m:
        return "", t.strip()
    desc, cur = {}, None
    for line in m.group(1).split("\n"):
        k = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if k:
            cur = k.group(1); desc[cur] = k.group(2)
        elif cur:
            desc[cur] += " " + line
    return norm(desc.get("description", "")), m.group(2).strip()


def stale(name):
    a, b = os.path.join(acct_dir, name), os.path.join(home, name)
    for root, _, files in os.walk(b):
        if "__pycache__" in root:
            continue
        for f in files:
            if f in ("CHANGELOG.md", "SOURCE.md", ".gitignore"):
                continue
            pb = os.path.join(root, f); pa = os.path.join(a, os.path.relpath(pb, b))
            if not os.path.exists(pa):
                return "missing " + os.path.relpath(pb, b)
            if f == "SKILL.md" and root == b:
                if parse(pa) != parse(pb):
                    return "SKILL.md"
            elif not filecmp.cmp(pa, pb, shallow=False):
                return os.path.relpath(pb, b)
    return None


found = 0
for name in sorted(os.listdir(home)):
    if name in KEEP_OFF_ACCOUNT or not os.path.isdir(os.path.join(home, name)):
        continue
    why = "not on claude.ai" if name not in ours else stale(name)
    if why:
        found += 1; print(f"UPLOAD {name}  ({why}; zip: claude-skills/dist/{name}-skill.zip via skill-smith deploy.py)")
for name in sorted(ours - set(os.listdir(home))):
    found += 1; print(f"REMOVE {name}  (on claude.ai, not in the skill home)")
print("ACCOUNT_OK" if not found else f"{found} account skill(s) to fix")
