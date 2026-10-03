"""V2 (Grace's own script, verbatim) motion cut: every shot is a real moving clip, no Ken Burns on photos, no freezes. Times from vo/v2g_words.json (Grace B take, STT-checked).
   python3 cut_v2g.py  -> out/fusou_v2_grace_r1.mp4 (720x1280, 24 fps, VO + tap click + room tone, loudnorm -16 LUFS). Free."""
import json, os, subprocess
import cv2, numpy as np
import cut_r5 as c
from cut_r5 import W, H, FPS, TAIL, TMP, run, dur_of, render_shot, card
WORDS = json.load(open("vo/v2g_words.json")); VO = "vo/v2g_voiceover.mp3"; NAME = "out/fusou_v2_grace_r1.mp4"
def at(word, k=1): return [w["start"] for w in WORDS if w["text"].lower().strip(",.?!:") == word.lower()][k - 1]
M1 = ("clip", c.M1, 0, {"done": 1, "dark": {"mask": "refs/m1a_led_mask.png", "ramp": [0, 0.01], "on": [1.22, 1.47], "dark": 0.34}})
EDL = [(0,                  ("clip", "clips/WK1.mp4", 0, {})),            # "Just look at the drawers on this vanity." walk-in
       (at("if"),           ("clip", "clips/B2a.mp4", 0, {})),            # bag under the sink: hand drags the stuffed makeup bag out, products spill
       (6.40,     ("clip", "clips/WK2.mp4", 0, {})),            # "just isn't cutting it anymore, look at this": walk-in, mirror light fades on
       (at("you've"),       ("clip", "clips/M6a.mp4", 0, {})),            # 12 drawers: drawers open overview
       (at("plus"),         ("clip", "clips/M4a.mp4", 0, {})),            # two more in the stool
       (16.24, ("clip", "clips/JD1a.mp4", 0, {})),   # makeup, jewelry, perfume, all of it: top-down drawer pull on the trays
       (at("top") - 0.4,    ("clip", "clips/M3b.mp4", 0, {})),            # the top is glass: tap on the glass
       (at("see"),          ("clip", "clips/M3a.mp4", 0, {})),            # see what you have: lipstick lift through the glass
       (at("i'd"),          ("clip", "clips/WK3.mp4", 0, {})),            # grab this sooner: dolly-out across the bedroom
       (29.04, ("clip", "clips/V1S4.mp4", 0, {})),           # three boxes, give yourself time (+ package card)
       (at("together") - 1.5, ("clip", "clips/M5a.mp4", 0, {})),          # put it together: hand opens the mirror door
       (34.56, M1),                            # crazy sale: tap, LED fades on
       (37.16,              ("clip", "clips/WK2.mp4", 3.44, {})),         # unused tail of the walk-in: lit vanity close
       (38.76,              ("clip", "clips/V1S2.mp4", 0, {}))]           # deal or the vanity is gone: push-in on the lit vanity
CARD_ON, CARD_OFF = at("three"), at("together") - 0.3
TAPS = [34.56 + 1.2]


def pop2(src, out):
    cd, a = card(); ch, cw = a.shape; X, Y = 48, 600
    sh = cv2.GaussianBlur(np.pad(a, 20), (0, 0), 9) * 0.35
    cap = cv2.VideoCapture(src)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        t = i / FPS; f = f.astype(np.float32)
        if CARD_ON <= t < CARD_OFF:
            e = min(1, (t - CARD_ON) / 0.22, (CARD_OFF - t) / 0.18); e = 1 - (1 - e) ** 3
            s = 0.92 + 0.08 * e; cs = cv2.resize(cd, None, fx=s, fy=s); as_ = cv2.resize(a, None, fx=s, fy=s)[..., None] * e
            hh, ww = as_.shape[:2]; x, y = X + (cw - ww) // 2, Y + (ch - hh) // 2
            shs = cv2.resize(sh, (ww + 40, hh + 40))[..., None] * e; f[y - 14:y + hh + 26, x - 20:x + ww + 20] *= 1 - shs
            f[y:y + hh, x:x + ww] = cs * as_ + f[y:y + hh, x:x + ww] * (1 - as_)
        ff.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); i += 1
    ff.stdin.close(); ff.wait()


n = 92
vo_dur = dur_of(VO); end = vo_dur + TAIL
starts = [s for s, _ in EDL] + [end]
assert all(b > a for a, b in zip(starts, starts[1:])), starts
last = EDL[-1][1]; end = min(end, starts[-2] + dur_of(last[1]) - last[2]); starts[-1] = end
files = [render_shot(i, shot, starts[i + 1] - starts[i], n) for i, (_, shot) in enumerate(EDL)]
for i, (s, (_, f, ss, _)) in enumerate(EDL): print(f"{s:6.2f} {starts[i+1]-s:5.2f}s {f}")
open(f"{TMP}/list{n}.txt", "w").write("".join(f"file '{f}'\n" for f in files))
run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/list{n}.txt", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f"{TMP}/v{n}_cat.mp4")
pop2(f"{TMP}/v{n}_cat.mp4", f"{TMP}/v{n}_pop.mp4")
vd = dur_of(f"{TMP}/v{n}_pop.mp4"); assert vd >= vo_dur + 0.2, (vd, vo_dur)
inputs = ["-i", f"{TMP}/v{n}_pop.mp4", "-i", VO, "-f", "lavfi", "-t", f"{vd}", "-i", "anoisesrc=color=brown:amplitude=0.004:sample_rate=44100"]
fx = [f"[1:a]aresample=44100,apad=whole_dur={vd}[vo]", "[2:a]lowpass=f=900,volume=0.5[room]"]; mix = ["[vo]", "[room]"]
for k, t in enumerate(TAPS):
    inputs += ["-i", "sfx/click.ogg"]; fx.append(f"[{3 + k}:a]aresample=44100,volume=0.35,adelay={int(t * 1000)}|{int(t * 1000)}[s{k}]"); mix.append(f"[s{k}]")
fx.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fx), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{vd}", NAME)
print(NAME, f"{vd:.2f}s", len(EDL), "shots")
