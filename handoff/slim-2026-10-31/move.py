"""Slim the two CLAUDE.md files (Ralph 2026-10-31: "Go" on the slim plan). Moves text word for word; run once.

Rule text that only some jobs need goes to rules/<topic>.md (read when the job matches); setup and test history goes
to the tool's own folder. verify.py proves every original sentence still exists.
"""
import pathlib, sys

H = pathlib.Path(__file__).parent
M, D = pathlib.Path("/home/user/Mymobileworld"), pathlib.Path("/home/user/Dayone-ai")
STAMP = "Moved word for word from {src} on 2026-10-31 (slim plan, Ralph: \"Go\"); {why}\n\n"


def cut_lines(text, start, end):
    """Remove the block from the line starting with `start` up to (not incl.) the line starting with `end`."""
    lines = text.split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith(start))
    j = next(k for k, l in enumerate(lines) if k > i and l.startswith(end)) if end else len(lines)
    return "\n".join(lines[:i] + lines[j:]), "\n".join(lines[i:j]).rstrip("\n")


def split_sentence(text, bullet_start, at, keep_tail="", pointer=""):
    """In the one-line bullet starting with bullet_start, move everything from `at` on; keep `keep_tail` + pointer."""
    lines = text.split("\n")
    k = next(n for n, l in enumerate(lines) if l.startswith(bullet_start))
    line = lines[k]
    assert line.count(at) == 1, (bullet_start, at)
    pos = line.index(at)
    moved = line[pos:]
    kept = line[:pos].rstrip() + (" " + keep_tail if keep_tail else "") + (" " + pointer if pointer else "")
    lines[k] = kept
    return "\n".join(lines), moved


def remove_sentences(text, bullet_start, sentences, pointer):
    """Remove whole sentences from one bullet line (each must occur once); append pointer."""
    lines = text.split("\n")
    k = next(n for n, l in enumerate(lines) if l.startswith(bullet_start))
    line, moved = lines[k], []
    for s in sentences:
        assert line.count(s) == 1, (bullet_start, s[:60])
        line = line.replace(" " + s, "", 1) if (" " + s) in line else line.replace(s, "", 1)
        moved.append(s)
    lines[k] = line.rstrip() + " " + pointer
    return "\n".join(lines), " ".join(moved)


def shared(text):
    """Same edits in both repos' copies of the shared bullets; returns (text, {dest: [moved text]})."""
    out = {}
    text, mv = split_sentence(
        text, "- **Browser tools:", "The default browser tool in every session is camofox-browser",
        keep_tail="If the tools fail, run `bash /home/user/Mymobileworld/.claude/hooks/camofox_setup.sh` and wait for CAMOFOX_SETUP_OK.",
        pointer="Install, telemetry and test details: Mymobileworld `tools/camofox/README.md`.")
    out.setdefault("tools/camofox/README.md", []).append("- " + mv)
    text, mv = split_sentence(text, "- **broll-mcp", "SkillSpector 100/100 from test fixtures",
                              pointer="Security review and test: Mymobileworld `tools/broll/SOURCE.md`.")
    out.setdefault("tools/broll/SOURCE.md", []).append("- " + mv)
    text, mv = remove_sentences(text, "- **Playwright in every session", [
        "`.claude/hooks/browser_setup.sh` (SessionStart hook in `.claude/settings.json`, Mymobileworld + Dayone-ai) installs `playwright==1.56.0` (matches Chromium revision 1194) and the proxy CAs in the background, log `/tmp/browser-setup.log`.",
        "Hooks only load when the session starts inside the repo, so the environment's Setup script also carries `python3 -m pip install -q --break-system-packages playwright==1.56.0 || true`."],
        "Install details: Mymobileworld `handoff/history/SETUP_NOTES.md`.")
    out.setdefault("handoff/history/SETUP_NOTES.md", []).append("- Playwright: " + mv)
    text, mv = remove_sentences(text, "- **Obsidian vault (Ralph 2026-10-23", [
        "The free GitSync app syncs the vault with the private repo focusfiyah/obsidian-vault (GitHub sign-in, nested clone in Documents/obsidian-vault, syncs when Obsidian opens and closes; round trip phone -> GitHub -> phone tested 2026-10-23).",
        "Not used: vault-companion-for-claude (subscription mode needs a Mac relay, else API billing), the \"Git Sync\" plugin (failed to load on his phone), Obsidian Git (its author calls mobile very unstable)."],
        "Phone sync setup: Mymobileworld `handoff/history/SETUP_NOTES.md`.")
    out.setdefault("handoff/history/SETUP_NOTES.md", []).append("- Obsidian vault: " + mv)
    text, mv = remove_sentences(text, "- **Job media lives in Drive", [
        "`pack` tars a job's new media into parts of at most 95 MB (Kie's file host limit) on Kie's free host, a Composio workbench call pulls them into Drive and reads back Drive's own sha256, `record` + `untrack` finish it; `get UNIT` brings a job's files back, every file checked by sha256 (restore tested 2026-10-29).",
        "Why: tracked media was 10.2 GB, the repo cost ~20 GB of every session's disk and the avatar tools kept running out of room.",
        "**History cleaned 2026-10-29** (Ralph: \"Go ahead with the cleanup\"): every media file was removed from all of Mymobileworld's git history after the history-only versions went to Drive (each job's \"Older versions (from git history)\" subfolder); a fresh clone is 0.02 GB instead of ~10.6 GB."],
        "How the tool works, why and the history cleanup: `tools/media/README.md`.")
    out.setdefault("tools/media/README.md", []).append("- " + mv)
    return text, out


def main():
    if (H / "DONE").exists():
        sys.exit("already ran")
    mm, dd = (M / "CLAUDE.md").read_text(), (D / "CLAUDE.md").read_text()
    mm, out_m = shared(mm)
    dd, out_d = shared(dd)
    assert out_m == out_d, "shared bullets differ between repos"

    # Dayone-ai: Day One video rules and RGH post rules to rules/
    day, rgh = [], []
    dd, b = cut_lines(dd, "- Tell Ralph the exact cost before any paid generation", "- **Never say a tool"); day.append(b)
    dd, b = cut_lines(dd, "- **Daily list + silent drafts", "- **Lip sync (Ralph, 2026-10-18)"); day.append(b)
    dd, b = cut_lines(dd, "- **Original value rules", "- **AI on Autopilot reels"); day.append(b)
    dd, b = cut_lines(dd, "- **AI on Autopilot reels", "- **Ralph's own look in AI"); rgh.append(b)
    dd, b = cut_lines(dd, "- **Social growth (Ralph OK", "- **Model: Opus**"); rgh.append(b)
    dd, b = cut_lines(dd, "- **Motion style**", "## Environment"); day.append(b)
    dd, b = cut_lines(dd, "## Pipeline", "- **Skill standard (Ralph, 2026-10-05)"); day.append(b)
    index = ("## Read first for these jobs (moved out 2026-10-31 to keep this file small; nothing in them changed)\n"
             "- **Day One AI YouTube videos** (daily routine, radar, script, render, upload, publish, Shorts incl. "
             "`formats/shorts.md`, Instagram cross-post, YouTube auth, channel numbers): read `rules/day-one-videos.md` "
             "in full before the first step.\n"
             "- **@realgoodhustles / @azariah2244 / AI on Autopilot** (reels, carousels, posts, daily batches, cartoon "
             "presenter, 2027 trends, posting volume, social growth): read `rules/rgh-posts.md` in full before the first step.\n")
    dd = dd.replace("## Ralph's decisions (do not re-ask)\n", index + "\n## Ralph's decisions (do not re-ask)\n", 1)
    (D / "rules").mkdir(exist_ok=True)
    (D / "rules/day-one-videos.md").write_text(
        "# Day One AI videos: rules and pipeline\n\n" + STAMP.format(src="Dayone-ai CLAUDE.md", why=(
            "read it in full before any Day One video step. The rules that apply to every job stay in CLAUDE.md.")) +
        "## Channel decisions (do not re-ask)\n" + "\n".join(day[:2]) + "\n\n## Channel rules\n" + day[2] + "\n" +
        day[3] + "\n\n" + day[4] + "\n")
    (D / "rules/rgh-posts.md").write_text(
        "# @realgoodhustles, @azariah2244 and AI on Autopilot posts: rules\n\n" + STAMP.format(src="Dayone-ai CLAUDE.md", why=(
            "read it in full before any post, reel, carousel or daily batch. Steps: "
            "`products/ai-on-autopilot/reels/ROUTINE.md`.")) + "\n".join(rgh) + "\n")

    # Mymobileworld: other jobs (not ads) to rules/other-jobs.md
    other = []
    mm, b = cut_lines(mm, "- **Jean Rameau (client #2", "- **House of Rameau (@houseoframeau)"); other.append(b)
    mm, b = cut_lines(mm, "- **Posting volume (2026-10-30", "- **Per-job history"); other.append(b)
    mm, b = cut_lines(mm, "## Learning reports (2026-10-01)", None); other.append(b)
    mm = mm.replace("- **Per-job history", "- **Other jobs** (Jean Rameau, Grace AI-video sales tracker, @realgoodhustles "
                    "posting volume, Grace's Creator Desk, weekly learning reports): read their section in "
                    "`rules/other-jobs.md` before working on one (moved out 2026-10-31, nothing changed).\n\n"
                    "- **Per-job history", 1)
    (M / "rules").mkdir(exist_ok=True)
    (M / "rules/other-jobs.md").write_text(
        "# Other jobs: rules and pointers\n\n" + STAMP.format(src="Mymobileworld CLAUDE.md", why=(
            "read the section for the job before working on it.")) + "\n\n".join(x.strip("\n") for x in other) + "\n")

    for dest, parts in out_m.items():
        p = M / dest
        head = "" if p.exists() else f"# {dest.split('/')[-2] if dest.endswith('README.md') else 'Setup notes'}\n\n"
        sec = ("\n\n## Moved from CLAUDE.md (2026-10-31)\n\n" + STAMP.format(
            src="Mymobileworld and Dayone-ai CLAUDE.md (same text in both)", why="the rule itself stays in CLAUDE.md.") +
            "\n".join(parts) + "\n")
        p.write_text((p.read_text().rstrip("\n") if p.exists() else head.rstrip("\n")) + sec)

    (M / "CLAUDE.md").write_text(mm)
    (D / "CLAUDE.md").write_text(dd)
    (H / "DONE").write_text("ran\n")
    print("MOVED")


main()
