"""Ralph's FREE local Chatterbox voice for the HofR Black Friday posts (Ralph 2026-11-12: "Do not use 11 Labs for voiceovers.
Use the other voice that we use."). Settings = Sorry I Lied ep7 vo_gen.py (exaggeration 0.75, cfg_weight 0.35, one seed per line),
reference = Dayone-ai products/ai-on-autopilot/avatar/voice/ralph_ref.wav. $0, no ElevenLabs.

  ~/.presenter-tools/cbx/bin/python -I vo.py gen POST [n ...]   -> POST/vo/L<n>.wav (all lines, or just the listed ones)
     seeds: POST/vo/seeds.json {"<n>": seed}, default 1000+n; change a line's seed there to re-voice it
  ~/.presenter-tools/fw/bin/python -I vo.py check POST           -> Whisper small.en reads each line back, trims silence,
     joins them with a 0.18 s gap into POST/vo/ralph.wav and writes POST/vo/words.json (line start/end on the VO timeline).
     Prints VO_LINES_OK when every line is heard word for word (punctuation and case ignored), else VO_MISHEARD <n> ...
"""
import json, os, re, subprocess, sys, time
from pathlib import Path
REF = "/home/user/dayone-ai/products/ai-on-autopilot/avatar/voice/ralph_ref.wav"
GAP = float(os.environ.get("VO_GAP", "0.18"))
cmd, post = sys.argv[1], Path(sys.argv[2]).resolve()
V = post / "vo"; lines = [l.strip() for l in (V / "lines.txt").read_text().splitlines() if l.strip()]
seeds = json.loads((V / "seeds.json").read_text()) if (V / "seeds.json").exists() else {}

if cmd == "gen":
    import torch, torchaudio as ta
    torch.set_num_threads(4)
    from chatterbox.tts import ChatterboxTTS
    model = ChatterboxTTS.from_pretrained(device="cpu")
    todo = [int(x) for x in sys.argv[3:]] or range(len(lines))
    for n in todo:
        t0 = time.time(); seed = int(seeds.get(str(n), 1000 + n)); torch.manual_seed(seed)
        wav = model.generate(lines[n], audio_prompt_path=REF, exaggeration=0.75, cfg_weight=0.35)
        ta.save(str(V / f"L{n}.wav"), wav, model.sr)
        print(f"VO_OK L{n} seed {seed} {wav.shape[-1] / model.sr:.1f}s in {time.time() - t0:.0f}s", flush=True)

elif cmd == "check":
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=4)
    norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("’", "'")).split()
    bad, parts, words, t = [], [], [], 0.0
    for n, text in enumerate(lines):
        src = V / f"L{n}.wav"; trim = V / f"L{n}.trim.wav"
        # trim leading/trailing silence (-45 dB), mono 44.1 kHz
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                        "afade=t=in:d=0.01,areverse,afade=t=in:d=0.03,areverse", "-ac", "1", "-ar", "44100", str(trim)], check=True)
        segs, _ = m.transcribe(str(trim), language="en", beam_size=5)
        heard = " ".join(s.text for s in segs).strip()
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(trim)], capture_output=True, text=True).stdout)
        ok = norm(heard) == norm(text)
        print(("OK " if ok else "MISHEARD ") + f"L{n} {d:.2f}s | said: {text} | heard: {heard}", flush=True)
        if not ok: bad.append(n)
        words.append({"n": n, "text": text, "heard": heard, "start": round(t, 3), "end": round(t + d, 3)})
        parts.append(str(trim)); t += d + GAP
    (V / "words.json").write_text(json.dumps(words, indent=1))
    ins = sum([["-i", p] for p in parts], [])
    pads = ";".join(f"[{i}:a]apad=pad_dur={GAP}[a{i}]" for i in range(len(parts) - 1))
    fc = (pads + ";" if pads else "") + "".join(f"[a{i}]" for i in range(len(parts) - 1)) + f"[{len(parts) - 1}:a]concat=n={len(parts)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[o]", "-ar", "44100", str(V / "ralph.wav")], check=True)
    print(f"VO_TOTAL {words[-1]['end']:.2f}s")
    print("VO_LINES_OK" if not bad else "VO_MISHEARD " + " ".join(map(str, bad)))
