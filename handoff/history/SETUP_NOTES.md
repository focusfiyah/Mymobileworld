# Setup notes

## Moved from CLAUDE.md (2026-10-31)

Moved word for word from Mymobileworld and Dayone-ai CLAUDE.md (same text in both) on 2026-10-31 (slim plan, Ralph: "Go"); the rule itself stays in CLAUDE.md.

- Playwright: `.claude/hooks/browser_setup.sh` (SessionStart hook in `.claude/settings.json`, Mymobileworld + Dayone-ai) installs `playwright==1.56.0` (matches Chromium revision 1194) and the proxy CAs in the background, log `/tmp/browser-setup.log`. Hooks only load when the session starts inside the repo, so the environment's Setup script also carries `python3 -m pip install -q --break-system-packages playwright==1.56.0 || true`.
- Obsidian vault: The free GitSync app syncs the vault with the private repo focusfiyah/obsidian-vault (GitHub sign-in, nested clone in Documents/obsidian-vault, syncs when Obsidian opens and closes; round trip phone -> GitHub -> phone tested 2026-10-23). Not used: vault-companion-for-claude (subscription mode needs a Mac relay, else API billing), the "Git Sync" plugin (failed to load on his phone), Obsidian Git (its author calls mobile very unstable).
