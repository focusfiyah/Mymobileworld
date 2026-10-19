"""Cut for one video (default V1), adapted from ugc/lgxnds-creatine/cut_v2.py. No text overlay.
  python3 cut.py [V1] [--final]   review render (veryfast) -> out/heater_V1_raw.mp4; --final adds ai_finish.sh -> out/heater_V1.mp4
Each shot = its clip from frame `from` (shots.json "from", default 0) for its VO window t (shots.json, written by vo.py), real
footage at 1.0x. Every clip gets a per-clip neutral white balance (half of a gray-world correction), so warm stock rooms read
bright and neutral (Ralph: no yellow/golden grades). Clip choice per shot: shots.json "clip" (default clips/<id>.mp4)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]; FIN = ROOT / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"
V = next((a for a in sys.argv[1:] if a.startswith("V")), "V1")
S = [s for s in json.load(open("shots.json"))["shots"] if s["video"] == V]
VO = f"vo/{V}_tight.wav"; raw, fin = f"out/heater_{V}_raw.mp4", f"out/heater_{V}.mp4"


def wb(src, at):
    """Half-strength gray-world gains from one frame (keeps some warmth, removes the yellow cast)."""
    f = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(at), "-i", src, "-frames:v", "1", "-vf", "scale=64:-2", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    m = np.frombuffer(f, np.uint8).reshape(-1, 3).astype(float).mean(0); g = m.mean() / m
    r, gg, b = (1 + (g - 1) * 0.5).clip(0.85, 1.15)
    return f"colorchannelmixer=rr={r:.3f}:gg={gg:.3f}:bb={b:.3f},eq=brightness=0.015:contrast=1.03,"


carry = 0.0   # a shot with max_len (bad tail in its clip) hands its remaining time to the next shot
for s in S:
    d = round(s["t"][1] - s["t"][0] + carry, 3); carry = 0.0
    if s.get("max_len") and d > s["max_len"]: carry = d - s["max_len"]; d = s["max_len"]
    s["_d"] = d
inp, ch = [], []
for i, s in enumerate(S):
    src = s.get("clip", f"clips/{s['id']}.mp4"); a = s.get("from", 0.0); d = s["_d"]
    inp += ["-i", src]
    tt = f"crop=iw:ih-{s['trim_top']}:0:{s['trim_top']}," if s.get("trim_top") else ""
    ch.append(f"[{i}:v]trim=start={a}:duration={d},setpts=PTS-STARTPTS,{tt}{wb(src, a + d / 2)}scale=720:1280:force_original_aspect_ratio=increase,"
              f"crop=720:1280,setsar=1,fps=24[v{i}]")
k = len(S)
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[v]"
Path("out").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-i", VO, "-filter_complex", fc, "-map", "[v]", "-map", f"{k}:a", "-shortest",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", raw], check=True)
print("raw", raw)
if "--final" in sys.argv:   # AI finish = the LAST step (Ralph 2026-10-07)
    subprocess.run(["bash", str(FIN), raw, fin], check=True)
    json.dump({"in": raw, "out": fin, "tool": "ai_finish.sh grain 6 sharpen 0.6 sat 0.92"}, open(f"out/heater_{V}.finish.json", "w"))
    print("final", fin)
