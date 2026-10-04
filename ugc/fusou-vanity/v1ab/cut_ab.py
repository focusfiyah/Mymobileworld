"""V1 versions A and B cuts (free, 2026-10-03). Run from ugc/fusou-vanity:  python3 v1ab/cut_ab.py A B  -> v1ab/out/fusou_v1A.mp4, fusou_v1B.mp4
Reuses cut.py helpers (finish, darkroom, kb, 3-boxes pop). Every shot sits on the real Grace B word timings (v1ab/vo/vX_final_words.json), clips play at 1.0x."""
import json, os, subprocess, sys
import cv2, numpy as np
sys.path.insert(0, os.getcwd()); import cut
from cut import FPS, W, H, TMP, WIDE, run, dur_of, pop, B1CROP, B1BLUR, M1
V = "v1ab"


def words(v): return json.load(open(f"{V}/vo/v{v}_final_words.json"))
def clean(w): return w["text"].lower().strip(",.?!…\"")
def at(v, word, k=1): return [w["start"] for w in words(v) if clean(w) == word.lower()][k - 1]
def end_of(v, word, k=1): return [w["end"] for w in words(v) if clean(w) == word.lower()][k - 1]


def tint(im, a):   # a: 0 = warm bathroom light, 1 = cool daylight
    x = im.astype(np.float32)
    k = np.array([0.84, 0.96, 1.08]) * (1 - a) + np.array([1.08, 1.0, 0.94]) * a      # B, G, R gains
    return np.clip(x * k * (0.95 * (1 - a) + 1.06 * a), 0, 255).astype(np.uint8)


def bad(im):   # bad bathroom lighting: dim, flat, slightly green-yellow, top-lit vignette
    x = im.astype(np.float32); g = x.mean(2, keepdims=True); x = g + (x - g) * 0.78
    x *= np.array([0.80, 0.93, 0.90]) * 0.82
    yy = np.linspace(0, 1, x.shape[0])[:, None, None]; x *= (0.80 + 0.30 * (1 - yy) ** 1.5)
    return np.clip(x, 0, 255).astype(np.uint8)


def grade(src, out, t_sw, ramp=0.3, mode=None):
    cap = cv2.VideoCapture(src)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE); i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        a = 0 if t_sw is None else min(1, max(0, (i / FPS - t_sw) / ramp)); a = a * a * (3 - 2 * a)
        ff.stdin.write((bad(f) if mode == 'bad' else tint(f, a)).tobytes()); i += 1
    ff.stdin.close(); ff.wait()


def render(i, shot, d, tag):
    kind = shot[0]; out, raw = f"{TMP}/{tag}_{i:02d}.mp4", f"{TMP}/{tag}_{i:02d}_raw.mp4"; frames = round(d * FPS)
    if kind == "kb":
        _, src, box, o = shot
        args = ["python3", "kb.py", src, ",".join(map(str, box)), raw, f"{frames / FPS}"] + (["--out-pull"] if o.get("pull") else []) + (["--zoom", str(o["zoom"])] if o.get("zoom") else [])
        subprocess.run(args, check=True, capture_output=True); o = {}
    else:
        _, src, ss, o = shot
        assert ss + d <= dur_of(src) + 0.01, f"{tag} shot {i}: {src} too short ({ss}+{d:.2f} > {dur_of(src):.2f}); never stretch"
        vf = ([f"crop={o['crop']}", f"scale={W}:{H}:flags=lanczos"] if o.get("crop") else []) + [f"fps={FPS}", f"scale={W}:{H}"]
        run("ffmpeg", "-v", "error", "-y", "-ss", f"{ss}", "-i", src, "-frames:v", str(frames), "-vf", ",".join(vf), "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", raw)
    if "grade" in o:
        g = raw.replace("_raw.mp4", "_g.mp4"); grade(raw, g, o["grade"], mode=o.get("mode")); os.replace(g, raw)
    if o.get("dark"):
        dk = o["dark"]; d2 = raw.replace("_raw.mp4", "_dark.mp4")
        args = ["--mask", dk["mask"]] + sum([[f"--{k}", *map(str, v if isinstance(v, list) else [v])] for k, v in dk.items() if k != "mask"], [])
        subprocess.run(["python3", "darkroom.py", raw, d2] + args, check=True, capture_output=True); os.replace(d2, raw)
    if o.get("done"): os.replace(raw, out)
    else: subprocess.run(["python3", "finish.py", raw, out] + (["--topblur", *map(str, o["blur"])] if o.get("blur") else []), check=True, capture_output=True)
    got = int(cv2.VideoCapture(out).get(7)); assert abs(got - frames) <= 1, f"{tag} shot {i}: {got} frames, wanted {frames}"
    return out


def three_boxes(v):
    ws = words(v); k = next(i for i, x in enumerate(ws) if clean(x) == "boxes"); return ws[k - 1]["start"]


def m1_shot(v, t_start, t_ring, ss_max=1.3):    # tap clip: LED ring comes on at t_ring (clip's own ring-on = 1.22-1.47 s)
    x = t_ring - t_start; ss = min(max(0, 1.22 - x), ss_max); on = [x + ss - (t_ring - t_start) + (1.22 - ss), 1.47 - ss]
    return ("clip", M1, ss, {"done": 1, "dark": {"mask": "refs/m1a_led_mask.png", "ramp": [0, 0.01], "on": on, "dark": 0.34}}), t_start + (1.22 - ss) - 0.02


def lights_shot(v, t0, t_warm, t_dip0, t_yellow):   # V1S3 in the dark room: cold white -> warm white -> dip -> warm yellow
    return ("clip", "clips/V1S3.mp4", 0, {"dark": {"mask": "refs/v1s3_led_mask.png", "ramp": [-0.2, -0.1], "colors": [t_warm - t0, t_yellow - t0], "dip": [t_dip0 - t0, t_yellow - t0 - 0.03]}, "zoomout": 1})


def lights_day(t0, t_warm, t_dip0, t_yellow):   # Grace: no dark room. Same LED colour changes, room stays bright
    return ("clip", "clips/V1S3.mp4", 0, {"dark": {"mask": "refs/v1s3_led_mask.png", "ramp": [-0.2, -0.1], "dark": 1.0, "colors": [t_warm - t0, t_yellow - t0], "dip": [t_dip0 - t0, t_yellow - t0 - 0.03]}})


def EDL2(v, face=False):
    """Grace's notes 2026-10-04 (both videos): ~3 s of Grace making up in bad lighting, vanity on screen by 3 s; room never dark; the tap/light-on shot
    is replaced by hands walking toward the vanity in full view (V1S4)."""
    w = lambda x, k=1: at(v, x, k); end = cut.dur_of(f"{V}/vo/v{v}_final.wav") + cut.TAIL
    L = [x["start"] for x in json.load(open(f"{V}/vo/v{v}_final_lines.json"))]; s4 = L[3]
    w4 = lambda x, k=1: [y["start"] for y in words(v) if clean(y) == x and y["start"] >= s4][k - 1]
    BAD = ("clip", "clips/B1a.mp4", 0, {"crop": B1CROP, "blur": B1BLUR, "grade": 0, "mode": "bad"})
    if face: BAD = ("clip", "clips/OPEN_FACE.mp4", 0.2, {"crop": "531:945:70:40"})   # Grace's face, bad light, cropped above the lips (no lip sync needed)
    if v == "A":
        t_hand = 5.2; t_lights = L[3] - 5.0
        edl = [(0, BAD), (2.73, ("clip", "clips/V1S5.mp4", 0, {})), (t_hand, ("clip", "clips/V1S4.mp4", 0, {})),
               (t_lights, lights_day(t_lights, w("adjustable"), w("brightness") - 0.1, w("so"))),
               (s4, ("clip", "clips/V1S5.mp4", 0.5, {})), (w4("with") - 0.05, ("clip", "clips/M6a.mp4", 0, {})),
               (w4("makeup") + 0.2, ("clip", "clips/M5a.mp4", 1.4, {})), (w4("and", 3) - 0.1, ("clip", "clips/M4a.mp4", 0.7, {})),
               (w("ships") - 0.23, ("kb",) + WIDE + ({},))]
        taps = [w("adjustable") - 0.05, w("so") - 0.05]
    else:
        t_lights = L[2]
        edl = [(0, BAD), (3.0, ("clip", "clips/V1S5.mp4", 0, {})), (L[1], ("clip", "clips/V1S4.mp4", 0, {})),
               (t_lights, lights_day(t_lights, w("adjustable"), w("brightness") - 0.1, w("so"))),
               (min(s4, t_lights + 5.0), ("clip", "clips/V1S5.mp4", 0.8, {})),
               (w4("lot") - 0.1, ("clip", "clips/M3a.mp4", 0.3, {})), (w4("makeup") - 0.05, ("clip", "clips/M5a.mp4", 1.4, {})),
               (w4("jewelry") - 0.15, ("clip", "clips/M4a.mp4", 0.7, {})), (L[4], ("kb",) + WIDE + ({"zoom": 1.08},))]
        taps = [w("adjustable") - 0.05, w("so") - 0.05]
    return edl, taps, end


def EDL(v):
    w = lambda x, k=1: at(v, x, k); end = cut.dur_of(f"{V}/vo/v{v}_final.wav") + cut.TAIL; taps = []
    if v == "A":
        L = [x["start"] for x in json.load(open(f"{V}/vo/v{v}_final_lines.json"))]; s2, s3, s4 = L[1], L[2], L[3]
        w4 = lambda x, k=1: [y["start"] for y in words(v) if clean(y) == x and y["start"] >= s4][k - 1]
        m1, tap = m1_shot(v, s3, w("three")); t_in = tap + 0.92; assert s4 - t_in <= 5.0   # V1S3 starts as the hand leaves; zoom-out bridge
        taps = [tap, w("adjustable") - 0.05, w("so") - 0.05]
        edl = [(0, ("clip", "clips/B1a.mp4", 0, {"crop": B1CROP, "blur": B1BLUR, "grade": None})),
               (3.4, ("clip", "clips/B1b.mp4", 0, {"blur": (190, 335), "grade": w("step") - 3.4 - 0.1})),
               (s3, m1), (t_in, lights_shot(v, t_in, w("adjustable"), w("brightness") - 0.1, w("so"))),
               (s4, ("clip", "clips/V1S5.mp4", 0, {})), (w4("with") - 0.05, ("clip", "clips/M6a.mp4", 0, {})),
               (w4("makeup") + 0.2, ("clip", "clips/M5a.mp4", 1.4, {})), (w4("and", 3) - 0.1, ("clip", "clips/M4a.mp4", 0.7, {})),
               (w("ships") - 0.23, ("kb",) + WIDE + ({},))]
    else:
        L = [x["start"] for x in json.load(open(f"{V}/vo/v{v}_final_lines.json"))]; s2, s3, s4 = L[1], L[2], L[3]
        m1, tap = m1_shot(v, s2, w("mirror") - 0.1, ss_max=1.0); t_l = w("it")
        taps = [tap, w("adjustable") - 0.05, w("so") - 0.05]
        w4 = lambda x, k=1: [y["start"] for y in words(v) if clean(y) == x and y["start"] >= s4][k - 1]
        edl = [(0, ("clip", "clips/B1a.mp4", 0, {"crop": B1CROP, "blur": B1BLUR, "grade": None})),
               (w("then") - 0.1, ("clip", "clips/B1b.mp4", 0, {"blur": (190, 335), "grade": w("step") - (w("then") - 0.1) - 0.1})),
               (s2, m1), (tap + 0.92, lights_shot(v, tap + 0.92, w("adjustable"), w("brightness") - 0.1, w("so"))),
               (min(s4, tap + 0.92 + 5.0), ("clip", "clips/V1S5.mp4", 0, {})),
               (w4("lot") - 0.1, ("clip", "clips/M3a.mp4", 0.3, {})), (w4("makeup") - 0.05, ("clip", "clips/M5a.mp4", 1.4, {})),
               (w4("jewelry") - 0.15, ("clip", "clips/M4a.mp4", 0.7, {})), (L[4], ("kb",) + WIDE + ({"zoom": 1.08},))]
    return edl, taps, end


def ring_box(frame, landscape=False):
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); m = (g > 225).astype(np.uint8); m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m); i = max([k for k in range(1, n) if (not landscape or st[k, 2] > st[k, 3])], key=lambda k: st[k, 2] * st[k, 3]); return st[i, :4]   # x, y, w, h of the biggest bright ring


def zoomout(prev_file, file, dur=0.7):
    """Pull-back bridge: the lit-mirror close-up (last frame of prev_file) widens into the room (file). Free, one smooth ease, no bounce."""
    cp = cv2.VideoCapture(prev_file); n = int(cp.get(7)); cp.set(1, n - 1); _, last = cp.read()
    cap = cv2.VideoCapture(file); frames = []
    while True:
        ok, f = cap.read()
        if not ok: break
        frames.append(f)
    bx, by, bw, bh = ring_box(last, True); wx, wy, ww, wh = ring_box(frames[0], True); print("boxes", (bx, by, bw, bh), (wx, wy, ww, wh), flush=True); z0 = bw / ww
    # mirror ring in the wide frame (wx,wy,ww,wh) must land on its close-up place (bx,by,bw,bh) at t=0 and on itself at the end
    cx, cy = wx + ww / 2, wy + wh / 2; dx, dy = bx + bw / 2, by + bh / 2; k = round(dur * FPS)
    out = file + ".z.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i, f in enumerate(frames):
        if i < k:
            e = i / k; e = 1 - (1 - e) ** 3; z = z0 + (1 - z0) * e; px = dx + (cx - dx) * e; py = dy + (cy - dy) * e
            f = cv2.warpAffine(f, np.float32([[z, 0, px - z * cx], [0, z, py - z * cy]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait(); os.replace(out, file); print("zoomout z0 %.2f" % z0, flush=True)


def build(v, ver=1):
    edl, taps, end = EDL2(v, face=(ver == 3)) if ver >= 2 else EDL(v); tag = f"ab{v}{ver}"
    starts = [s for s, _ in edl] + [end]
    assert all(b > a for a, b in zip(starts, starts[1:])), f"{v}: starts not increasing {starts}"
    files = [render(i, sh, starts[i + 1] - starts[i], tag) for i, (_, sh) in enumerate(edl)]
    for i, (_, sh) in enumerate(edl):
        if sh[0] == "clip" and sh[3].get("zoomout"): zoomout(files[i - 1], files[i])
    open(f"{TMP}/{tag}_list.txt", "w").write("".join(f"file '{f}'\n" for f in files))
    run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/{tag}_list.txt", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f"{TMP}/{tag}_cat.mp4")
    t3 = three_boxes(v) if v == "A" else None; vo = f"{V}/vo/v{v}_final.wav"
    if t3: pop(f"{TMP}/{tag}_cat.mp4", f"{TMP}/{tag}_pop.mp4", t3 - 0.05)
    else: os.replace(f"{TMP}/{tag}_cat.mp4", f"{TMP}/{tag}_pop.mp4")
    vd = dur_of(f"{TMP}/{tag}_pop.mp4"); assert vd >= dur_of(vo) + 0.2, f"{v}: video {vd:.2f}s would cut the voiceover"
    inputs = ["-i", f"{TMP}/{tag}_pop.mp4", "-i", vo, "-f", "lavfi", "-t", f"{vd}", "-i", "anoisesrc=color=brown:amplitude=0.004:sample_rate=44100"]
    fx = [f"[1:a]aresample=44100,apad=whole_dur={vd}[vo]", "[2:a]lowpass=f=900,volume=0.5[room]"]; mix = ["[vo]", "[room]"]
    ev = [(t, "sfx/click.ogg", 0.35) for t in taps] + ([(t3 - 0.05, "sfx/tick.ogg", 0.25)] if t3 else [])
    for k, (t, snd, vol) in enumerate(ev):
        inputs += ["-i", snd]; fx.append(f"[{3 + k}:a]aresample=44100,volume={vol},adelay={int(t * 1000)}|{int(t * 1000)}[s{k}]"); mix.append(f"[s{k}]")
    fx.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fx), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{vd}", f"{V}/out/fusou_v{ver}{v}.mp4")
    print(f"{v}: {vd:.2f}s, {len(edl)} shots, starts {[round(s, 2) for s in starts]}", flush=True)


if __name__ == "__main__":
    for a in sys.argv[1:]: build(a[0], int(a[1]) if len(a) > 1 else 1)
