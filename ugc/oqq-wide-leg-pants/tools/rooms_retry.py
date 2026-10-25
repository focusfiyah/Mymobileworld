"""Runs the free-assets rooms.py with a retry on HTTP 429 (Pexels/Pixabay rate limit hit 2026-10-25). Same arguments as rooms.py."""
import sys, time, urllib.error, importlib.util
spec = importlib.util.spec_from_file_location("rooms", "/home/user/Mymobileworld/.claude/skills/free-assets/scripts/rooms.py")
rooms = importlib.util.module_from_spec(spec); spec.loader.exec_module(rooms)
_get = rooms.get
def get(url, headers=None):
    for i in range(5):
        try:
            return _get(url, headers)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(4 * (i + 1))
    return _get(url, headers)
rooms.get = get
sys.argv = ["rooms.py"] + sys.argv[1:]
rooms.main()
