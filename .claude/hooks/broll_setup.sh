#!/bin/bash
# broll-mcp for every cloud session (Ralph 2026-10-24: "Use this when we are editing and need b rolls").
# github.com/edigeh/broll-mcp (MIT): archive.org public-domain b-roll search, keyframe preview and verified cuts with a
# provenance file per clip. Pinned to commit d8fda0a (review: tools/broll/SOURCE.md in Mymobileworld).
# Why a warm-up: the first `uvx` run downloads ~37 packages incl. opencv (70 MB, ~70 s), longer than an MCP start
# should wait; this fills uv's cache in the background so the broll server in .mcp.json starts in seconds.
# Log /tmp/broll-setup.log.
SHA=d8fda0a4972235fb7591187242a4e583aca84f12
(
  uvx --from "git+https://github.com/edigeh/broll-mcp@$SHA" python -c "import broll_mcp, cv2; print('BROLL_SETUP_OK', broll_mcp.__version__)"
) > /tmp/broll-setup.log 2>&1 &
exit 0
