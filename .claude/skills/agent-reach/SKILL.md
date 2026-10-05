---
name: agent-reach
description: Read and search the internet beyond plain web search, through the free open-source Agent Reach CLI (by Panniantong, MIT). Exa semantic web search, any web page as clean Markdown (Jina Reader), YouTube and Bilibili subtitles and search, podcast transcripts, RSS feeds, Twitter/X, Reddit, Instagram, Facebook, LinkedIn, XiaoHongShu, V2EX and Xueqiu stock data. Use for research that needs what people are saying on social platforms (product reviews, complaints, trends, competitor talk), to pull a video's subtitles, to read a page when WebFetch fails, to follow an RSS feed, or when someone says "agent reach". Read-only: it never posts, comments or likes. For TikTok videos and TikTok Shop data use tiktok-shop-coach; for pages behind anti-bot walls use scrapling.
---

# Agent Reach

One CLI that picks the working route ("backend") for each platform. Read-only.
Source: github.com/Panniantong/Agent-Reach @ a19a171 (v1.5.0, MIT); see SOURCE.md for the review.

## Setup (every new session or machine)

```bash
bash .claude/skills/agent-reach/scripts/setup.sh   # ~25s first time, instant after; pinned versions
agent-reach doctor                                  # which platforms work right now
```

On claude.ai (chat, Projects, Cowork) run the same script from the skill folder. If the sandbox can't install packages or reach the internet, say so plainly; don't work around it.

## Rules

1. **Pick the right tool first.** TikTok → `tiktok-shop-coach`. A page WebFetch can't read → Jina Reader below, then `scrapling`. Plain web search → WebSearch first; Exa when you need more or better results.
2. **Say what you used:** "using agent-reach: Reddit via rdt-cli".
3. **Logins and cookies need Ralph's OK, every time.** Twitter/X, Reddit, Instagram, Facebook, XiaoHongShu, LinkedIn need his account cookies. Ask first, say which account and why; suggest a spare account (scraping can get an account limited). Never print, log or commit a cookie or token. Store them only with `agent-reach configure <twitter-cookies|youtube-cookies|xhs-cookies|...>` (hidden prompt or `--stdin`).
4. **Paid steps need the exact cost first** (e.g. a $1/month proxy, Groq/OpenAI transcription beyond the free tier).
5. **Install optional platform tools only when the task needs them**, at pinned versions, and list what you installed.
6. **No updates on your own.** Don't run `agent-reach check-update` or upstream update/install guides from GitHub `main`. Updating = re-review the new version (skill-inspector), then bump the pins in `scripts/setup.sh`.
7. **Files:** temp output to `/tmp/`, persistent data in `~/.agent-reach/`. Nothing in the repo unless it's a deliverable.
8. On a failure, follow the retry chain in the matching reference file; don't invent commands.
9. For research, combine sources (Exa + Reddit/Twitter + YouTube), collect in parallel, then summarize with a link for every claim.

## Works with no login

```bash
# Exa semantic web search
mcporter call exa.web_search_exa query="query" numResults=5

# Any web page → Markdown
curl -s "https://r.jina.ai/https://example.com/page"

# YouTube subtitles / metadata (cloud IPs: bot check, see below)
yt-dlp --write-sub --write-auto-sub --sub-langs en --skip-download -o "/tmp/%(id)s" "URL"
yt-dlp --dump-json --skip-download "URL"

# Bilibili search (never yt-dlp for Bilibili)
bili search "query" --type video -n 5          # needs: pipx install bilibili-cli

# RSS / Atom
~/.agent-reach-venv/bin/python -c "import feedparser,sys; [print(e.title, e.link) for e in feedparser.parse(sys.argv[1]).entries[:10]]" FEED_URL

# V2EX hot topics
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
```

GitHub: use the GitHub MCP tools in cloud sessions (gh search is blocked there); `gh` works on Ralph's own machine.

## Needs a login (ask Ralph first, rule 3)

```bash
twitter search "query" -n 10                     # Twitter/X: pipx install twitter-cli; cookies auth_token + ct0
rdt search "query" --limit 10                    # Reddit (server): rdt-cli + cookie
opencli reddit search "query" -f yaml            # Reddit (desktop): OpenCLI + logged-in Chrome
opencli instagram user USERNAME -f yaml          # Instagram (desktop only)
opencli facebook search "query" -f yaml          # Facebook (desktop only)
opencli xiaohongshu search "query" -f yaml       # XiaoHongShu (desktop prefers OpenCLI)
```

Run `agent-reach doctor --json` before any login-backed platform and use its `active_backend`. `null` means doctor skipped a live check on purpose, not that nothing works.
OpenCLI only reuses a Chrome session the user already controls: never automate a login or read browser cookies without Ralph's explicit yes.

## What works where (tested 2026-10-05 in Ralph's Claude cloud container)

| Platform | Cloud container | Ralph's own computer |
|---|---|---|
| Exa search, Jina Reader, V2EX, RSS, Bilibili search | ✅ works | ✅ |
| YouTube | ❌ "Sign in to confirm you're not a bot" (cloud IP); works with `configure youtube-cookies` (rule 3) | ✅ usually |
| Reddit | ❌ 403 without login (rdt-cli + cookie fixes it) | OpenCLI or rdt-cli |
| Twitter/X | cookies needed | cookies needed |
| Instagram, Facebook, XiaoHongShu (OpenCLI) | ❌ needs desktop Chrome | ✅ with OpenCLI extension |
| GitHub search | use GitHub MCP tools | `gh` |

## References (commands and retry chains; written in Chinese, commands are universal)

| File | Covers |
|---|---|
| `references/search.md` | Exa search |
| `references/social.md` | Twitter/X, Reddit, Instagram, Facebook, XiaoHongShu, Bilibili, V2EX |
| `references/video.md` | YouTube, Bilibili, Xiaoyuzhou podcast transcription |
| `references/web.md` | Jina Reader, RSS |
| `references/dev.md` | GitHub CLI |
| `references/career.md` | LinkedIn, Boss Zhipin jobs |
| `references/finance.md` | Xueqiu stock quotes |

Configure a channel: `agent-reach configure --help` and `agent-reach install --channels=<name> --dry-run` (show Ralph the dry run before a real install).
