"""Faceless motion-graphics video (Ralph 2026-11-15): live Pexels background video per line (darkened), a cinematic
card per line (motion2.py from twin-shorts: kinetic type, format list, 3D reveal, bundle), the hook in yellow serif
from frame 0, and subtitles. Voice: Ralph's free Chatterbox clone.
  ~/.presenter-tools/cbx/bin/python -I faceless.py vo WEEK F1        -> WEEK/faceless/F1/vo.wav + lines.json + words.json
  /root/.ram-tools/musetalk/venv/bin/python faceless.py render WEEK F1 -> WEEK/faceless/F1/F1.mp4"""
import sys, json, pathlib, subprocess, re
HERE = pathlib.Path(__file__).parent
TS = "/home/user/Mymobileworld/ralph/twin-shorts"
W, H, FPS = 1080, 1920, 25
cmd, week, fid = sys.argv[1:4]
D = HERE / week; spec = next(f for f in json.load(open(D / "scripts.json"))["faceless"] if f["id"] == fid)
O = D / "faceless" / fid; O.mkdir(parents=True, exist_ok=True)


def say_text(s):   # how the voice should read it (Veo/TTS spell capitals; DM said as letters)
    return re.sub(r"\bDM\b", "D M", s).replace("KIT", "kit")


if cmd == "vo":
    import torch, torchaudio as ta, torchaudio.functional as F, numpy as np, os
    from chatterbox.tts import ChatterboxTTS
    from faster_whisper import WhisperModel
    torch.set_num_threads(4); m = ChatterboxTTS.from_pretrained(device="cpu")
    REF = "/home/user/Dayone-ai/products/ai-on-autopilot/avatar/voice/ralph_ref.wav"
    parts, lines, t = [], [], 0.0
    for n, l in enumerate(spec["lines"]):
        torch.manual_seed(int(os.environ.get("SEED", 1000)) + n)
        w = m.generate(say_text(l["say"]), audio_prompt_path=REF, exaggeration=0.75, cfg_weight=0.35)[0].numpy()
        a = np.abs(w) > 0.01; i0, i1 = (np.argmax(a), len(a) - np.argmax(a[::-1])) if a.any() else (0, len(w))
        w = np.concatenate([w[max(0, i0 - 600):i1 + 600], np.zeros(int(m.sr * 0.25))])
        lines.append({"start": round(t, 3), "end": round(t + len(w) / m.sr, 3)}); t += len(w) / m.sr; parts.append(w)
        print("VO_LINE", n, round(len(w) / m.sr, 2), flush=True)
    full = torch.tensor(np.concatenate(parts))[None]
    ta.save(str(O / "vo_raw.wav"), full, m.sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(O / "vo_raw.wav"), "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "48000", "-ac", "1", str(O / "vo.wav")], check=True)
    wm = WhisperModel("small.en", device="cpu", compute_type="int8")
    s, _ = wm.transcribe(F.resample(full[0], m.sr, 16000).numpy(), word_timestamps=True)
    words = [{"w": x.word.strip(), "s": round(float(x.start), 2), "e": round(float(x.end), 2)} for seg in s for x in seg.words]
    for i, x in enumerate(words):
        if x["w"].lower().strip(".,") in ("kit", "kit.") and i and words[i - 1]["w"].lower() == "me": x["w"] = "KIT" + x["w"][3:]
    json.dump(lines, open(O / "lines.json", "w")); json.dump(words, open(O / "words.json", "w"))
    print("HEARD:", " ".join(x["w"] for x in words)); print("VO_OK", round(t, 2))
    sys.exit()

# ---------- render ----------
sys.path.insert(0, TS)
import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import motion2 as M
lines, words = json.load(open(O / "lines.json")), json.load(open(O / "words.json"))
for i, x in enumerate(words):                       # "DM. Me KIT." -> "DM me KIT."
    if x["w"].rstrip(".,") == "DM": x["w"] = "DM"
    if i and words[i - 1]["w"] == "DM" and x["w"].lower().startswith("me"): x["w"] = "me"
YEL, CY = (255, 210, 63), 660                      # card top y (below the hook zone)
serif = lambda sz: ImageFont.truetype(f"{TS}/fonts/InstrumentSerif-Regular.ttf", sz)


def shadow_text(im, cx, y, runs, sz):
    f = serif(sz); d = ImageDraw.Draw(im); tw = sum(d.textlength(t, font=f) for t, _ in runs)
    if tw > 940: f = serif(int(sz * 940 / tw)); tw = sum(d.textlength(t, font=f) for t, _ in runs)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); x = cx - tw / 2
    for t, _ in runs: sd.text((x, y + 4), t, font=f, fill=(0, 0, 0, 210)); x += d.textlength(t, font=f)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7))); x = cx - tw / 2
    for t, c in runs: d.text((x, y), t, font=f, fill=c + (255,)); x += d.textlength(t, font=f)


def formats_card(t, dur, items):
    c = M.blue_bg(); n = len(items); step = max(0.25, (dur - 0.4) / n); f = M.font(54)
    for i, it in enumerate(items):
        k = M.eob((t - i * step) / 0.35)
        if k <= 0: continue
        col, row = i % 2, i // 2; x = 70 + col * 420 + (1 - k) * 120; y = 70 + row * 150
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((x, y, x + 390, y + 120), 18, fill=(255, 255, 255, int(235 * min(1, k))))
        d.text((x + 24, y + 30), f"{i + 1}", font=f, fill=(46, 58, 240, 255)); d.text((x + 76, y + 34), it, font=M.font(44), fill=(20, 24, 60, 255))
        c.alpha_composite(lay)
    return c


def kinetic_card(t, dur, text):
    c = M.blue_bg() if text.isupper() or text[0].isdigit() else M.black_bg()
    M.blur_text(c, text, 450, 270, 150 if len(text) < 10 else 110, 0.05, t, col=YEL if not text.isupper() else (255, 255, 255), shake=9)
    return c


def card_for(l, t, dur):
    k = l["card"]
    if k == "kinetic": return kinetic_card(t, dur, l["text"])
    if k == "list": return formats_card(t, dur, l["items"])
    return M.ANIMS[k](t, dur)


class BG:
    def __init__(self, p):
        self.cap = cv2.VideoCapture(str(p)); self.n = int(self.cap.get(7)); self.fps = self.cap.get(5) or 25; self.i = 0
    def frame(self):
        ok, f = self.cap.read()
        if not ok: self.cap.set(1, 0); ok, f = self.cap.read()
        h, w = f.shape[:2]; s = max(W / w, H / h); f = cv2.resize(f, (int(w * s) + 1, int(h * s) + 1), interpolation=cv2.INTER_CUBIC)
        y0, x0 = (f.shape[0] - H) // 2, (f.shape[1] - W) // 2; f = f[y0:y0 + H, x0:x0 + W]
        return (f * 0.62).astype(np.uint8)          # darkened so the card and text read


bgs = [BG(D / "bg" / f"{fid}_{n + 1}.mp4") for n in range(len(spec["lines"]))]
chunks, cur = [], []
for w_ in words:
    cur.append(w_)
    if len(cur) == 3 or w_["w"][-1] in ".,?!": chunks.append(cur); cur = []
if cur: chunks.append(cur)
dur = lines[-1]["end"]; hook = spec.get("hook", spec["title"])
out = O / f"{fid}_edit.mp4"
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-i", str(O / "vo.wav"), "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "192k", "-threads", "4", str(out)], stdin=subprocess.PIPE)
for i in range(int(dur * FPS) + 1):
    t = i / FPS; li = next((k for k, L in enumerate(lines) if L["start"] <= t < L["end"]), len(lines) - 1); L = lines[li]
    im = Image.fromarray(cv2.cvtColor(bgs[li].frame(), cv2.COLOR_BGR2RGB)).convert("RGBA")
    card = card_for(spec["lines"][li], t - L["start"], L["end"] - L["start"])
    k = M.eob((t - L["start"]) / 0.3); cw, ch = int(M.CW * (0.9 + 0.1 * k)), int(M.CH * (0.9 + 0.1 * k)); card = card.resize((cw, ch), Image.LANCZOS)
    mk = Image.new("L", card.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, cw - 1, ch - 1), 22, fill=255); card.putalpha(mk)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((540 - cw // 2 + 6, CY + 16, 540 + cw // 2 + 6, CY + ch + 16), 22, fill=(0, 0, 0, 130))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18))); im.alpha_composite(card, (540 - cw // 2, CY + (M.CH - ch) // 2))
    if t < max(2.5, lines[0]["end"]):              # hook: whole, readable from frame 0, in the safe zone
        a, b = hook if isinstance(hook, list) else (hook, "")
        band = np.zeros((H, W, 4), np.uint8); yy = np.arange(H)
        al = np.clip(1 - np.abs(yy - 500) / 260, 0, 1) ** 0.7 * 170; band[..., 3] = al[:, None].astype(np.uint8)
        im.alpha_composite(Image.fromarray(band, "RGBA"))          # soft dark band so the hook reads on any background
        shadow_text(im, 540, 400, [(a, (255, 255, 255))], 100)
        if b: shadow_text(im, 540, 515, [(b, YEL)], 96)
    else:
        for c_ in chunks:
            nxt = chunks[chunks.index(c_) + 1][0]["s"] if c_ is not chunks[-1] else 99
            if c_[0]["s"] - 0.05 <= t < nxt:
                shadow_text(im, 540, 1270, [(" ".join(x["w"] for x in c_).replace(" -", "-"), (255, 255, 255))], 70); break
    try: p.stdin.write(cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2BGR).tobytes())
    except BrokenPipeError: break
p.stdin.close(); p.wait(); print("FACELESS_OK", out)
