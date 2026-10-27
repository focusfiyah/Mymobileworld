"""Hook check: a video that puts a hook on screen must show the WHOLE hook in its very first frame.

Ralph 2026-10-27 (AI on Autopilot reel 1, its first frame was blank and the hook built in word by word under
TikTok's top tabs): "Make sure that does not happen with any of the videos we use."

  python3 hook_check.py VIDEO [--hook x,y,w,h] [--hold 2.0]

--hook is the hook's box in 1080x1920 pixels (default: the 9:16 safe zone x 60-940, y 360-1340, clear of
TikTok/Reels top tabs, caption and right rail). PASS needs: frame 0 is not blank in that box (texture), and the
box at --hold seconds still matches frame 0 (the hook was complete at frame 0 and stayed up). It cannot read text:
it checks the box, so put the hook in a declared box. Prints HOOK_OK or HOOK_FAIL with the numbers.
"""
import argparse, subprocess, sys
import numpy as np
from PIL import Image

def frame(path, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
                          "-vf", "scale=1080:1920", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1920, 1080).astype(np.float32)

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("--hook", default="60,360,880,980"); ap.add_argument("--hold", type=float, default=2.0)
a = ap.parse_args()
x, y, w, h = map(int, a.hook.split(","))
f0, f1 = frame(a.video, 0), frame(a.video, a.hold)
z0, z1 = f0[y:y+h, x:x+w], f1[y:y+h, x:x+w]
texture = float(z0.std())                      # a blank background is near 0-10; set type is well above 25
ink0 = float((np.abs(z0 - np.median(z0)) > 60).mean())
ink1 = float((np.abs(z1 - np.median(z1)) > 60).mean())
same = float(np.abs(z0 - z1).mean())           # small when the hook did not change between 0 s and --hold
ok = texture > 25 and ink0 > 0.02 and ink0 >= 0.85 * ink1 and same < 12
print(f"frame0 texture={texture:.1f} ink0={ink0:.3f} ink@{a.hold}s={ink1:.3f} diff={same:.1f}")
print("HOOK_OK" if ok else "HOOK_FAIL")
sys.exit(0 if ok else 1)
