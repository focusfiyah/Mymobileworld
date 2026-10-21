"""TrendyQueen V-neck 3-pack (Grace, 2026-10-21): Grace's own full take, pauses removed, nothing else changed.
Uses the ugc-take-combos engine, but only gaps >= 0.30s become cuts (Ralph: 'remove awkward pauses', keep her rhythm).
Usage: python3 -I cut.py [--draft]   then   python3 -I qc.py"""
import sys
sys.path.insert(0, "/home/user/Mymobileworld/.claude/skills/ugc-take-combos/scripts")
import take_combos as t
t.QUIET_MIN = 0.30    # natural breaths stay; only real pauses are cut
t.KEEP_QUIET = 0.06   # a touch more air than Fungix so it doesn't sound clipped
t.Job("job.json").build("V1", "--draft" in sys.argv)
