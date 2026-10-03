"""FUSOU vanity cuts V1-V6 (free, 2026-10-03). Every shot sits on the real Grace B word timings (vo/vN_final_words.json).

  python3 cut.py 1 2 ...   -> out/fusou_vN.mp4 (720x1280, 24 fps, VO + tap click + pop click + room tone, loudnorm -16 LUFS)
Shot kinds: ("clip", file, src_start, {opts})  plays at 1.0x (or reversed), never stretched
            ("kb", photo, box, {zoom, pull, to}) free slow push-in / pull-out on a REAL photo (kb.py)
Every shot gets finish.py (grain, no sway) unless it is already finished. The 3-boxes card (real listing photo 11) pops in on "three".
"""
import json, os, subprocess, sys
import cv2, numpy as np
FPS, W, H, TAIL = 24, 720, 1280, 0.4
TMP = "/tmp/claude-0/-home-user/eb264d06-2517-557b-a9f3-9de446d2ca4a/scratchpad/cut"; os.makedirs(TMP, exist_ok=True)
WIDE = ("stills/V1A_fix.png", (0, 0, 768, 1376))
CAB, CAB2 = ("refs/vanity_cabinet_open.jpg", (417, 6, 800, 687)), ("refs/vanity_cabinet_open.jpg", (500, 100, 800, 633))
DOOR = ("refs/listing_01.jpg", (500, 60, 800, 593))
PSTRIP = ("refs/vanity_power_strip.jpg", (255, 24, 500, 460))
M1 = "out/M1a_test_v5.mp4"                                   # approved v5: hand-only crop, lights fade on at 1.25 s, already finished
B1CROP, B1BLUR = "600:1067:110:0", (230, 400)


def run(*a): subprocess.run(a, check=True)
def dur_of(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)


def words(n): return json.load(open(f"vo/v{n}_final_words.json"))
def at(n, word, k=1):
    hits = [w["start"] for w in words(n) if w["text"].lower().strip(",.?!") == word.lower()]
    return hits[k - 1]


def three_boxes(n):   # the "three" right before "boxes"
    ws = words(n); i = next(k for k, x in enumerate(ws) if x["text"].lower().startswith("boxes")); return ws[i - 1]["start"]


def EDL(n):
    w = lambda word, k=1: at(n, word, k)
    if n == 1: return [(0, ("clip", M1, 0, {"done": 1})), (2.6, ("kb",) + WIDE + ({"pull": 1},)),
                       (w("this"), ("clip", "clips/V1S3.mp4", 0.4, {})), (w("heads"), ("clip", "clips/V1S5.mp4", 0, {})),
                       (w("ships") - 0.23, ("kb",) + WIDE + ({},))], [1.2], three_boxes(n)
    if n == 2: return [(0, ("kb",) + WIDE + ({},)), (w("if"), ("clip", "clips/M3a.mp4", 0, {})), (w("twelve"), ("clip", "clips/M6a.mp4", 0, {})),
                       (w("top") - 0.13, ("clip", "clips/M3b.mp4", 0, {})), (w("plan"), ("clip", "clips/M4a.mp4", 0.5, {})),
                       (w("holiday"), ("kb",) + WIDE + ({},))], [], three_boxes(n)
    if n == 3: return [(0, ("clip", "clips/V1S5.mp4", 0, {})), (w("no"), ("kb",) + WIDE + ({"pull": 1},)), (w("one", 2), ("clip", M1, 0.7, {"done": 1})),
                       (w("two"), ("kb",) + DOOR + ({},)), (w("three"), ("kb",) + CAB + ({},)), (w("four"), ("clip", "clips/M2a.mp4", 0.6, {})),
                       (w("five"), ("clip", "clips/M4a.mp4", 0.8, {})), (w("it"), ("kb",) + WIDE + ({"pull": 1},)),
                       (w("five", 2), ("clip", "clips/V1S3.mp4", 0, {}))], [w("one", 2) + 0.5], three_boxes(n)
    if n == 4: return [(0, ("clip", "clips/M5a.mp4", 0, {})), (0.45, ("kb",) + CAB + ({},)), (w("bags"), ("clip", "clips/B1a.mp4", 0, {"crop": B1CROP, "blur": B1BLUR})),
                       (w("behind"), ("kb",) + CAB2 + ({},)), (w("close"), ("kb",) + DOOR + ({},)), (w("just"), ("clip", "clips/V1S5.mp4", 0, {})),
                       (w("it", 3), ("kb",) + WIDE + ({},))], [], three_boxes(n)
    if n == 5: return [(0, ("clip", "clips/M2a.mp4", 0, {})), (w("no"), ("clip", "clips/M2b.mp4", 0.5, {})), (w("two"), ("clip", "clips/M2c.mp4", 0, {})),
                       (w("your", 2), ("clip", M1, 0.5, {"done": 1})), (w("only"), ("kb",) + PSTRIP + ({"to": "300,330"},)),
                       (w("holiday"), ("kb",) + WIDE + ({},))], [w("your", 2) + 0.7], three_boxes(n)
    if n == 6: return [(0, ("clip", "clips/B1a.mp4", 0, {"crop": B1CROP, "blur": B1BLUR})), (w("makeup"), ("clip", "clips/B1b.mp4", 0, {"blur": (190, 335)})),
                       (w("lipsticks"), ("clip", "clips/M3a.mp4", 1.0, {"reverse": 1})), (w("perfume", 2), ("kb",) + CAB2 + ({},)),
                       (w("hair"), ("clip", "clips/M2b.mp4", 0.6, {})), (w("give"), ("clip", "clips/V1S5.mp4", 0, {})),
                       (w("if"), ("clip", "clips/M6a.mp4", 0, {})), (w("this", 2), ("kb",) + WIDE + ({},))], [], three_boxes(n)


def render_shot(i, shot, d, n):
    out, raw = f"{TMP}/v{n}_{i:02d}.mp4", f"{TMP}/v{n}_{i:02d}_raw.mp4"; frames = round(d * FPS)
    if shot[0] == "kb":
        _, src, box, o = shot
        args = ["python3", "kb.py", src, ",".join(map(str, box)), raw, f"{frames / FPS}"] + (["--out-pull"] if o.get("pull") else []) + (["--to", o["to"]] if o.get("to") else [])
        subprocess.run(args, check=True, capture_output=True); o = {}
    else:
        _, src, ss, o = shot
        assert ss + d <= dur_of(src) + 0.01, f"V{n} shot {i}: {src} too short ({ss}+{d:.2f} > {dur_of(src):.2f}); never stretch"
        vf = ["reverse"] if o.get("reverse") else []
        if o.get("crop"): vf += [f"crop={o['crop']}", f"scale={W}:{H}:flags=lanczos"]
        vf += [f"fps={FPS}", f"scale={W}:{H}"]
        if o.get("reverse"):
            run("ffmpeg", "-v", "error", "-y", "-i", src, "-vf", ",".join(vf), "-an", "-c:v", "libx264", "-crf", "16", f"{TMP}/rev.mp4")
            src, vf = f"{TMP}/rev.mp4", [f"fps={FPS}"]
        run("ffmpeg", "-v", "error", "-y", "-ss", f"{ss}", "-i", src, "-frames:v", str(frames), "-vf", ",".join(vf), "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", raw)
    if o.get("done"): os.replace(raw, out)
    else: subprocess.run(["python3", "finish.py", raw, out] + (["--topblur", *map(str, o["blur"])] if o.get("blur") else []), check=True, capture_output=True)
    got = int(cv2.VideoCapture(out).get(7)); assert abs(got - frames) <= 1, f"V{n} shot {i}: {got} frames, wanted {frames}"
    return out


def card():
    im = cv2.imread("refs/listing_11.jpg")[230:700, 560:800]; im = cv2.resize(im, (170, 333), interpolation=cv2.INTER_AREA)
    b = 8; c = cv2.copyMakeBorder(im, b, b, b, b, cv2.BORDER_CONSTANT, value=(255, 255, 255)).astype(np.float32)
    a = np.zeros(c.shape[:2], np.float32); r = 18; cv2.rectangle(a, (r, 0), (c.shape[1] - r, c.shape[0]), 1, -1); cv2.rectangle(a, (0, r), (c.shape[1], c.shape[0] - r), 1, -1)
    for x, y in [(r, r), (c.shape[1] - r, r), (r, c.shape[0] - r), (c.shape[1] - r, c.shape[0] - r)]: cv2.circle(a, (x, y), r, 1, -1)
    return c, cv2.GaussianBlur(a, (3, 3), 0)


def pop(src, out, t0):
    c, a = card(); ch, cw = a.shape; X, Y = 48, 600              # left side: clear of TikTok's right-hand buttons and bottom caption
    sh = cv2.GaussianBlur(np.pad(a, 20), (0, 0), 9) * 0.35                     # soft drop shadow
    cap = cv2.VideoCapture(src)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        t = i / FPS; f = f.astype(np.float32)
        if t >= t0:
            e = min(1, (t - t0) / 0.22); e = 1 - (1 - e) ** 3                    # ease-out, no bounce
            s = 0.92 + 0.08 * e; cs = cv2.resize(c, None, fx=s, fy=s); as_ = cv2.resize(a, None, fx=s, fy=s)[..., None] * e
            hh, ww = as_.shape[:2]; x, y = X + (cw - ww) // 2, Y + (ch - hh) // 2
            shs = cv2.resize(sh, (ww + 40, hh + 40))[..., None] * e; f[y - 14:y + hh + 26, x - 20:x + ww + 20] *= 1 - shs
            f[y:y + hh, x:x + ww] = cs * as_ + f[y:y + hh, x:x + ww] * (1 - as_)
        ff.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); i += 1
    ff.stdin.close(); ff.wait()


def build(n):
    edl, taps, t_three = EDL(n)
    vo = f"vo/v{n}_final.wav"; end = dur_of(vo) + TAIL
    starts = [s for s, _ in edl] + [end]
    assert all(b > a for a, b in zip(starts, starts[1:])), f"V{n}: shot starts not increasing {starts}"
    last = edl[-1][1]
    if last[0] == "clip": end = min(end, starts[-2] + dur_of(last[1]) - last[2]); starts[-1] = end
    files = [render_shot(i, shot, starts[i + 1] - starts[i], n) for i, (_, shot) in enumerate(edl)]
    open(f"{TMP}/list{n}.txt", "w").write("".join(f"file '{f}'\n" for f in files))
    run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/list{n}.txt", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f"{TMP}/v{n}_cat.mp4")
    pop(f"{TMP}/v{n}_cat.mp4", f"{TMP}/v{n}_pop.mp4", t_three - 0.05)
    vd = dur_of(f"{TMP}/v{n}_pop.mp4")
    inputs = ["-i", f"{TMP}/v{n}_pop.mp4", "-i", vo, "-f", "lavfi", "-t", f"{vd}", "-i", "anoisesrc=color=brown:amplitude=0.004:sample_rate=44100"]
    fx = [f"[1:a]aresample=44100,apad=whole_dur={vd}[vo]", "[2:a]lowpass=f=900,volume=0.5[room]"]; mix = ["[vo]", "[room]"]
    for k, t in enumerate(taps + [t_three - 0.05]):
        snd = "sfx/click.ogg" if k < len(taps) else "sfx/tick.ogg"
        inputs += ["-i", snd]; idx = 3 + k
        fx.append(f"[{idx}:a]aresample=44100,volume={0.35 if k < len(taps) else 0.25},adelay={int(t * 1000)}|{int(t * 1000)}[s{k}]"); mix.append(f"[s{k}]")
    fx.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fx), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-ar", "44100", "-t", f"{vd}", f"out/fusou_v{n}.mp4")
    print(f"V{n}: {vd:.2f}s, {len(edl)} shots -> out/fusou_v{n}.mp4", flush=True)


if __name__ == "__main__":
    for n in sys.argv[1:]: build(int(n))
