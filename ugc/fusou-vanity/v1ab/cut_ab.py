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
    k = np.array([0.74, 0.93, 1.12]) * (1 - a) + np.array([1.08, 1.0, 0.94]) * a      # B, G, R gains
    return np.clip(x * k * (0.92 * (1 - a) + 1.06 * a), 0, 255).astype(np.uint8)


def grade(src, out, t_sw, ramp=0.3):
    cap = cv2.VideoCapture(src)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE); i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        a = 0 if t_sw is None else min(1, max(0, (i / FPS - t_sw) / ramp)); a = a * a * (3 - 2 * a)
        ff.stdin.write(tint(f, a).tobytes()); i += 1
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
        g = raw.replace("_raw.mp4", "_g.mp4"); grade(raw, g, o["grade"]); os.replace(g, raw)
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
    return ("clip", "clips/V1S3.mp4", 0, {"dark": {"mask": "refs/v1s3_led_mask.png", "ramp": [0, 0.01], "colors": [t_warm - t0, t_yellow - t0], "dip": [t_dip0 - t0, t_yellow - t0 - 0.03]}})


def EDL(v):
    w = lambda x, k=1: at(v, x, k); end = cut.dur_of(f"{V}/vo/v{v}_final.wav") + cut.TAIL; taps = []
    if v == "A":
        s2, s3, s4 = at(v, "because"), w("this"), w("and", 2) if False else w("and", 3)
        s4 = [x["start"] for x in words(v) if clean(x) == "and"][-3]
        t_in = s4 - 4.6                                            # V1S3 plays its full ~4.6 s up to the storage line
        m1, tap = m1_shot(v, s3, w("three")); taps = [tap, w("adjustable") - 0.05, w("so") - 0.05]
        edl = [(0, ("clip", "clips/B1a.mp4", 0, {"crop": B1CROP, "blur": B1BLUR, "grade": None})),
               (3.4, ("clip", "clips/B1b.mp4", 0, {"blur": (190, 335), "grade": w("step") - 3.4 - 0.1})),
               (s3, m1), (t_in, lights_shot(v, t_in, w("adjustable"), w("brightness") - 0.1, w("so"))),
               (s4, ("clip", "clips/V1S5.mp4", 0, {})), (w("tons") + 0.1, ("clip", "clips/M6a.mp4", 0, {})),
               (w("bag") - 0.15, ("clip", "clips/M5a.mp4", 1.6, {})), (w("jewelry") - 0.1, ("clip", "clips/M4a.mp4", 0.6, {})),
               (w("ships") - 0.23, ("kb",) + WIDE + ({},))]
    else:
        s3 = w("it"); s2 = w("that's")
        m1, tap = m1_shot(v, s2, w("mirror") - 0.1, ss_max=1.0); t_l = w("it")
        taps = [tap, w("adjustable") - 0.05, w("so") - 0.05]
        edl = [(0, ("clip", "clips/B1a.mp4", 0, {"crop": B1CROP, "blur": B1BLUR, "grade": None})),
               (w("think") - 0.1, ("clip", "clips/B1b.mp4", 0, {"blur": (190, 335), "grade": w("step") - (w("think") - 0.1) - 0.1})),
               (s2, m1), (s3, lights_shot(v, s3, w("adjustable"), w("brightness") - 0.1, w("so"))),
               (w("and", 2) if False else [x["start"] for x in words(v) if clean(x) == "and"][-1], ("clip", "clips/V1S5.mp4", 0, {})),
               (w("lot") - 0.1, ("clip", "clips/M3a.mp4", 0.3, {})), (w("bags") - 0.15, ("clip", "clips/M5a.mp4", 1.6, {})),
               (w("jewelry") - 0.1, ("clip", "clips/M4a.mp4", 0.6, {})), (w("flash") - 0.1, ("kb",) + WIDE + ({"zoom": 1.08},))]
    return edl, taps, end


def build(v):
    edl, taps, end = EDL(v); tag = f"ab{v}"
    starts = [s for s, _ in edl] + [end]
    assert all(b > a for a, b in zip(starts, starts[1:])), f"{v}: starts not increasing {starts}"
    files = [render(i, sh, starts[i + 1] - starts[i], tag) for i, (_, sh) in enumerate(edl)]
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
    run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fx), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{vd}", f"{V}/out/fusou_v1{v}.mp4")
    print(f"{v}: {vd:.2f}s, {len(edl)} shots, starts {[round(s, 2) for s in starts]}", flush=True)


if __name__ == "__main__":
    for v in sys.argv[1:]: build(v)
