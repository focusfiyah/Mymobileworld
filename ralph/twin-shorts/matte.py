"""Free background removal for a talking-head clip: RobustVideoMatting (github.com/PeterL1n/RobustVideoMatting, GPL-3.0,
used as a tool; the output video is ours), resnet50 weights from its v1.0.0 release, recurrent so edges stay stable.
Writes an 8-bit alpha video (gray mp4, qp 0).
Usage: <musetalk venv python> matte.py IN.mp4 ALPHA.mp4 [--seconds N]"""
import sys, subprocess, time
import torch, cv2, numpy as np
sys.path.insert(0, "/root/.ram-tools/rvm/src")
from model import MattingNetwork

src, out = sys.argv[1], sys.argv[2]
lim = float(sys.argv[sys.argv.index("--seconds") + 1]) if "--seconds" in sys.argv else 1e9
torch.set_num_threads(4)
m = MattingNetwork("resnet50").eval()
m.load_state_dict(torch.load("/root/.ram-tools/rvm/rvm_resnet50.pth", map_location="cpu"))
cap = cv2.VideoCapture(src); fps = cap.get(5); W, H = int(cap.get(3)), int(cap.get(4))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", str(fps),
                      "-i", "-", "-c:v", "libx264", "-qp", "0", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
rec = [None] * 4; n = 0; t0 = time.time()
with torch.no_grad():
    while n / fps < lim:
        ok, f = cap.read()
        if not ok: break
        x = torch.from_numpy(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).permute(2, 0, 1)[None].float() / 255
        fgr, pha, *rec = m(x, *rec, downsample_ratio=0.25)
        p.stdin.write((pha[0, 0].numpy() * 255).round().astype(np.uint8).tobytes()); n += 1
p.stdin.close(); p.wait()
print(f"MATTE_OK {n} frames {time.time() - t0:.0f}s", flush=True)
