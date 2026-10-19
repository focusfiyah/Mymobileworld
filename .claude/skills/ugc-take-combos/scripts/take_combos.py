"""Cut a creator's raw hook / body / CTA takes into finished combo videos.

    python take_combos.py build  job.json [V1 V2 ...] [--draft]
    python take_combos.py verify job.json [V1 V2 ...]

Everything job-specific lives in job.json (see SKILL.md): source files, take windows,
which takes make each video, and overlays timed by spoken-word anchors. Run with python3
after scripts/setup.sh (faster-whisper, numpy, Pillow), in a cloud session or on Ralph's PC.
Proven on the Fungix / Grace job.

Hard-won rules this encodes (each cost a client-visible mistake once):
  * whisper decides WHERE the words are; the AUDIO decides where a cut lands. Whisper
    stretched "who" 3s back across a pause and timed "baby" 0.5s early.
  * the room-tone floor is local (rolling), not one number per file.
  * word-based trims may only remove quiet audio, never speech.
  * every overlay is asserted visible on screen, not just present in the config.
"""
import difflib, json, os, re, shutil, subprocess, sys
from pathlib import Path
import numpy as np

W, H, FPS = 1080, 1920, 30
QUIET_MIN = 0.18    # quiet longer than this inside speech becomes a jump cut
KEEP_QUIET = 0.04   # breath kept on each side of a voiced run
HARD_PAUSE = 0.30   # nothing quieter than speech survives longer than this, even inside a "word"
LEAD, TAIL = 0.12, 0.23   # max lead-in / tail around the words (0.15 tail clipped the "s" of "worse")

def ffmpeg():
    """FFMPEG env var, then PATH (cloud: /usr/bin/ffmpeg), then the imageio-ffmpeg binary."""
    cands = [os.environ.get("FFMPEG"), shutil.which("ffmpeg")]
    try:
        import imageio_ffmpeg; cands.append(imageio_ffmpeg.get_ffmpeg_exe())
    except ImportError:
        pass
    for c in cands:
        if c and Path(c).exists(): return c
    sys.exit("ffmpeg not found: run scripts/setup.sh or set FFMPEG")
FF = ffmpeg(); FP = str(Path(FF).with_name("ffprobe" + Path(FF).suffix))

def run(cmd): subprocess.run(cmd, check=True, capture_output=True)

def pcm16k(path):
    """Decode with ffmpeg to the 16 kHz mono float array faster-whisper takes. Skips PyAV, whose
    newer releases broke faster-whisper's own decoder (cloud, 2026-10-13: av 19 vs faster-whisper 1.2.1)."""
    raw = subprocess.run([FF, "-nostdin", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32)
def norm(w): return re.sub(r"[^a-z0-9%]", "", w.lower())

class Job:
    def __init__(self, path):
        self.path = Path(path); self.cfg = json.loads(self.path.read_text(encoding="utf-8"))
        c = self.cfg
        self.src = Path(c["src_dir"]); self.work = Path(c["work_dir"]); self.out = Path(c.get("out_dir", c["work_dir"]))
        self.work.mkdir(parents=True, exist_ok=True); self.out.mkdir(parents=True, exist_ok=True)
        self.zoom = c.get("zoom", 1.14); self._lv = {}; self._tx = {}

    def video(self, part): return self.src / self.cfg["parts"][part]["video"]
    def audio(self, part): return self.src / self.cfg["parts"][part].get("audio", self.cfg["parts"][part]["video"])

    def words(self, part):
        """Word timestamps for a part's audio, cached in work_dir/tx_<part>.json."""
        if part not in self._tx:
            f = self.work / f"tx_{part}.json"
            if not f.exists():
                from faster_whisper import WhisperModel
                m = WhisperModel("small.en", device="cpu", compute_type="int8")
                segs, _ = m.transcribe(pcm16k(self.audio(part)), word_timestamps=True)
                f.write_text(json.dumps([[round(w.start, 2), round(w.end, 2), w.word] for s in segs for w in s.words]))
            self._tx[part] = json.loads(f.read_text())
        return self._tx[part]

    def level(self, part):
        """10ms RMS dB of a part's audio plus a rolling room-tone floor (5th pct over +-3s)."""
        if part not in self._lv:
            r = subprocess.run([FF, "-v", "error", "-i", str(self.audio(part)), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True)
            x = np.frombuffer(r.stdout, np.int16).astype(np.float32); x = x[: len(x) // 160 * 160].reshape(-1, 160)
            db = 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1)
            pts = np.arange(0, len(db), 100)
            fl = np.interp(np.arange(len(db)), pts, [np.percentile(db[max(0, i - 300): i + 300], 5) for i in pts])
            self._lv[part] = (db, fl)
        return self._lv[part]

    def src_width(self, part):
        r = subprocess.run([FP, "-v", "error", "-select_streams", "v", "-show_entries", "stream=width", "-of", "csv=p=0", str(self.video(part))], capture_output=True, text=True)
        return int(r.stdout.split()[0])

    # ---------------- cutting ----------------
    def chunks(self, take):
        part, a, b = self.cfg["takes"][take]
        db, fl = self.level(part); words = self.words(part)
        voiced = db > fl + 16                                   # clearly speech
        for w0, w1, _ in words:                                 # protect soft onsets whisper heard,
            lo, hi = int(w0 * 100), int(w1 * 100) + 1           # only in words that peak like speech,
            if hi > lo and db[lo:hi].max() > fl[lo:hi].mean() + 12:   # only where there is energy
                voiced[lo:hi] |= db[lo:hi] > fl[lo:hi] + 6
        runs, st = [], None
        for i in range(int(a * 100), min(int(b * 100), len(voiced))):
            if voiced[i] and st is None: st = i
            elif not voiced[i] and st is not None: runs.append([st, i]); st = None
        if st is not None: runs.append([st, min(int(b * 100), len(voiced))])
        merged = [runs[0]]
        for r in runs[1:]:
            if (r[0] - merged[-1][1]) / 100 < QUIET_MIN: merged[-1][1] = r[1]
            else: merged.append(r)
        loud = db > fl + 12; split = []
        for st, en in merged:                                   # a protected "word" can hide a long hush
            cut, q = st, None
            for i in range(st, en):
                if not loud[i] and q is None: q = i
                elif loud[i] and q is not None:
                    if i - q >= int(HARD_PAUSE * 100): split.append([cut, q]); cut = i
                    q = None
            split.append([cut, en])
        out = []
        for st, en in [r for r in split if r[1] > r[0]]:
            s_t, e_t = st / 100 - KEEP_QUIET, en / 100 + KEEP_QUIET
            if e_t - s_t < 0.25: continue
            ws = [w for w in words if s_t <= (w[0] + w[1]) / 2 < e_t]
            if not ws: continue
            i, j = int(s_t * 100), int(e_t * 100)
            lo = [k for k in range(i, j) if loud[k]]
            if lo:
                vo = [k for k in range(i, j) if voiced[k]]
                i = max(i, min(vo[0], lo[0] - 6)); j = min(j, max(vo[-1], lo[-1] + 6) + 1)
            out.append(dict(part=part, s=round(max(a, i / 100), 3), e=round(j / 100, 3), words=ws))
        L = lambda t: db[min(int(t * 100), len(db) - 1)] > fl[min(int(t * 100), len(db) - 1)] + 12
        for c in out:   # land on the words, but a trim may only remove QUIET audio
            s0 = max(c["s"], c["words"][0][0] - LEAD); e0 = min(c["e"], c["words"][-1][1] + TAIL)
            while s0 > c["s"] and L(s0 - 0.01): s0 -= 0.01
            while e0 < c["e"] and L(e0): e0 += 0.01
            c["s"], c["e"] = round(s0, 3), round(e0, 3)
        return out

    # ---------------- overlays ----------------
    def anchor(self, spec, timeline, start=None):
        if "t" in spec: return spec["t"]
        if "dur" in spec:
            t = start + spec["dur"]
            if "cap_section" in spec: t = min(t, max(x[3] for x in timeline if x[0] == spec["cap_section"]))
            return t
        after = self.anchor(spec["after"], timeline) if "after" in spec else 0.0
        names = [norm(n) for n in (spec["word"] if isinstance(spec["word"], list) else [spec["word"]])]
        hit = next((x for x in timeline if x[0] == spec["in"] and x[1] in names and x[2] >= after), None)
        if hit is None: raise SystemExit(f"overlay anchor not found: {spec}")
        return (hit[3] if spec.get("edge") == "end" else hit[2]) + spec.get("plus", 0.0)

    def overlay_png(self, ov, vid):
        if "png" in ov: return Path(ov["png"]) if Path(ov["png"]).is_absolute() else self.path.parent / ov["png"]
        sys.path.insert(0, str(Path(__file__).parent)); from overlay_art import text_bubble
        p = self.work / vid / "bubble.png"; text_bubble(ov["bubble"]).save(p); return p

    # ---------------- build ----------------
    def build(self, vid, draft=False):
        v = self.cfg["videos"][vid]; wd = self.work / vid; wd.mkdir(exist_ok=True)
        chunks = [c | {"section": self.cfg["takes"][t][0]} for t in v["takes"] for c in self.chunks(t)]
        t_out, timeline, lst = 0.0, [], []
        for i, c in enumerate(chunks):
            dur = c["e"] - c["s"]; z = self.zoom if i % 2 else 1.0
            sw = self.src_width(c["part"]); native = sw >= W
            if native:   # punch-in = crop of the native frame; light sharpen on crops only
                cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
                vf = f"crop={cw}:{ch}:{(W - cw) // 2}:{int((H - ch) * 0.35)},scale={W}:{H}:flags=lanczos"
                vf += ",unsharp=5:5:0.4:3:3:0.0" if z > 1 else ""
            else:        # low-res source: crop at source res, ONE upscale, sharpen everything
                shh = sw * H // W; cw, ch = int(sw / z) // 2 * 2, int(shh / z) // 2 * 2
                vf = f"crop={cw}:{ch}:{(sw - cw) // 2}:{int((shh - ch) * 0.35)},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.8:3:3:0.0"
            vf += f",setsar=1,fps={FPS}"
            af = f"afade=t=in:d=0.015,afade=t=out:st={dur - 0.025:.3f}:d=0.025"
            seg = wd / f"seg{i:02d}.mp4"
            run([FF, "-y", "-ss", str(c["s"]), "-i", str(self.video(c["part"])), "-ss", str(c["s"]), "-i", str(self.audio(c["part"])),
                 "-t", f"{dur:.3f}", "-map", "0:v", "-map", "1:a", "-vf", vf, "-af", af, "-c:v", "libx264",
                 "-preset", "veryfast" if draft else "medium", "-crf", "22" if draft else "17", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(seg)])
            lst.append(f"file '{seg.name}'")
            timeline += [(c["section"], norm(w[2]), t_out + w[0] - c["s"], t_out + w[1] - c["s"]) for w in c["words"]]
            t_out += dur
        (wd / "list.txt").write_text("\n".join(lst))
        run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(wd / "list.txt"), "-c", "copy", str(wd / "base.mp4")])
        windows = []
        for ov in v.get("overlays", []) + self.cfg.get("overlays", []):   # per-video first = underneath
            a = self.anchor(ov["from"], timeline); b = self.anchor(ov["to"], timeline, start=a)
            windows.append((self.overlay_png(ov, vid), a, b))
        inputs, fc, last = [], [], "0:v"
        for k, (png, a, b) in enumerate(windows, 1):
            inputs += ["-i", str(png)]
            fc.append(f"[{last}][{k}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{k}]"); last = f"v{k}"
        fc.append("[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
        final = self.out / f"{self.cfg['name']} {vid}{' (draft)' if draft else ''}.mp4"
        run([FF, "-y", "-i", str(wd / "base.mp4"), *inputs, "-filter_complex", ";".join(fc), "-map", f"[{last}]" if last != "0:v" else "0:v", "-map", "[a]",
             "-c:v", "libx264", "-preset", "veryfast" if draft else "medium", "-crf", "22" if draft else "17",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)])
        (wd / "edl.json").write_text(json.dumps(dict(final=str(final), duration=t_out,
            chunks=[{k: c[k] for k in ("section", "part", "s", "e")} for c in chunks],
            windows=[(str(p), a, b) for p, a, b in windows],
            words=[w for t in v["takes"] for w in self.words(self.cfg["takes"][t][0])
                   if self.cfg["takes"][t][1] <= max(w[0], w[1] - 0.8) < self.cfg["takes"][t][2]]), indent=1))
        print(f"{vid}: {len(chunks)} cuts, {t_out:.2f}s -> {final.name}")

    # ---------------- verify ----------------
    def pauses(self, path):
        r = subprocess.run([FF, "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True)
        x = np.frombuffer(r.stdout, np.int16).astype(np.float32); x = x[: len(x) // 160 * 160].reshape(-1, 160)
        db = 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1); pts = np.arange(0, len(db), 100)
        fl = np.interp(np.arange(len(db)), pts, [np.percentile(db[max(0, i - 300): i + 300], 5) for i in pts])
        runs, st = [], None
        for i, q in enumerate(db < fl + 12):
            if q and st is None: st = i
            elif not q and st is not None:
                if i - st >= 20: runs.append((round(st / 100, 2), round((i - st) / 100, 2)))
                st = None
        return sorted(runs, key=lambda r: -r[1])

    def verify(self, vid, model):
        e = json.loads((self.work / vid / "edl.json").read_text()); f = Path(e["final"])
        expected = [norm(w[2]) for w in e["words"]]
        got = [norm(w.word) for s in model.transcribe(pcm16k(f), word_timestamps=True)[0] for w in s.words]
        diffs = [(op, expected[a:b], got[c:d]) for op, a, b, c, d in difflib.SequenceMatcher(None, expected, got).get_opcodes() if op != "equal"]
        drops = [d for d in diffs if d[0] == "delete"]
        missing = []
        for png, a, b in e["windows"]:   # overlay must be VISIBLE: frame differs from the un-overlaid base
            fr = []
            for src in (self.work / vid / "base.mp4", f):
                r = subprocess.run([FF, "-v", "error", "-ss", f"{(a + b) / 2:.2f}", "-i", str(src), "-frames:v", "1",
                                    "-f", "rawvideo", "-pix_fmt", "gray", "-s", "270x480", "-"], capture_output=True)
                fr.append(np.frombuffer(r.stdout, np.uint8).astype(np.int16))
            if float(np.abs(fr[0] - fr[1]).mean()) < 2: missing.append(Path(png).name)
        p = self.pauses(f)[:3]
        print(f"{vid}: {e['duration']:.1f}s | longest pauses {[d for _, d in p]} (at {[t for t, _ in p]}) | "
              f"overlays {len(e['windows']) - len(missing)}/{len(e['windows'])} visible{' MISSING ' + str(missing) if missing else ''}")
        print(f"   DROPPED WORDS: {drops}" if drops else "   no dropped words", "| other diffs (usually ASR noise):", [d for d in diffs if d[0] != "delete"])

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("build", "verify"):
        sys.exit(__doc__)
    cmd, cfg, rest = sys.argv[1], sys.argv[2], sys.argv[3:]
    job = Job(cfg); draft = "--draft" in rest; vids = [v for v in rest if v != "--draft"] or list(job.cfg["videos"])
    if cmd == "build":
        for v in vids: job.build(v, draft)
    elif cmd == "verify":
        from faster_whisper import WhisperModel
        m = WhisperModel("small.en", device="cpu", compute_type="int8")
        if job.cfg.get("reference"):
            print("REFERENCE longest pauses:", [d for _, d in job.pauses(job.path.parent / job.cfg["reference"])[:3]])
        for v in vids: job.verify(v, m)
