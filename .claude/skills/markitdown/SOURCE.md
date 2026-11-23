# Source

- Tool: microsoft/markitdown (https://github.com/microsoft/markitdown), MIT, Copyright (c) Microsoft Corporation.
- Checked 2026-11-15 at commit ed17895 (2026-11-06); pip package `markitdown==0.1.9`, pinned in scripts/md.sh.
- The repo ships no Claude skill; this skill is ours, written to the skill-smith rules. The repo also has
  `markitdown-mcp` (MCP server), `markitdown-ocr` (LLM-vision OCR plugin, paid model) and a sample plugin: not used.
- Install: `pip install 'markitdown[pdf,docx,pptx,xlsx,xls,outlook]==0.1.9'` (md.sh does it). `[all]` also pulls audio
  transcription (Google web speech) and YouTube transcript libraries; not needed.

## Test 2026-11-15 (cloud session, $0)

| Input | Result |
|---|---|
| docx (heading, paragraph, 2x2 table) | heading, text, table OK; table header row came out blank |
| pptx (title + bullet) | slide number comment, `# Slide One`, bullet OK |
| xlsx (2 rows) | `## Sheet` + Markdown table OK |
| html | heading + link OK |
| pdf (LibreOffice from the docx) | text OK, table as plain lines |
| image-only pdf | 1 byte (empty) -> md.sh MD_EMPTY |
| csv, zip (xlsx+html inside) | table OK; zip lists each file's content |
| https://example.com | page text OK |
| YouTube watch URL | only the footer links (cloud bot block) |
