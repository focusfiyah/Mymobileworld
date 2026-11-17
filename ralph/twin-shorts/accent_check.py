"""Accent drift check for AI twin audio (Ralph 2026-11-16: on the posted T2 the voice turned "like a Russian accent" on "Follow for more";
he asked for a skill that can listen). Two free local ears on every 3 s window:
  1. faster-whisper language ID: English below 0.90 = drift.
  2. SpeechBrain CommonAccent accent ID (Jzuluaga/accent-id-commonaccent_ecapa, Apache-2.0, cached in /root/.cache/sb/accent;
     hyperparams.yaml pretrained_path points at that folder): top accent not "us" or "canada" (same to the ear), or us below 0.40 = drift.
Tested 2026-11-16: posted T2 tail flagged by both (whisper en 0.82-0.86; accent "african" 0.33 / "england" 0.44, us 0.28-0.33);
every other week 1 and week 2 line: en 0.96+, accent "us". A voice-match check (speechbrain spkrec-ecapa vs ralph_ref.wav)
was tried and dropped: scores 0.38-0.54 on every line, it could not tell the drifted one apart.
Run on every raw Flow clip (Veo's own voice; speech-to-speech copies its delivery) and on every speech-to-speech output / final cut.
Setup if missing: ~/.presenter-tools/cbx/bin/pip install speechbrain==1.0.3, then snapshot_download the model to /root/.cache/sb/accent
and set its hyperparams.yaml pretrained_path to that folder (speechbrain 1.0.3 + new huggingface_hub break the direct download).
Usage: ~/.presenter-tools/cbx/bin/python -I accent_check.py FILE [FILE ...]   -> ACCENT_OK / ACCENT_FLAG per file"""
import sys, subprocess, soundfile as sf, torch
from faster_whisper import WhisperModel
from speechbrain.inference.classifiers import EncoderClassifier
wm = WhisperModel('small', device='cpu', compute_type='int8')
acc = EncoderClassifier.from_hparams(source="/root/.cache/sb/accent", savedir="/root/.cache/sb/accent"); L = acc.hparams.label_encoder
US = L.encode_label('us'); W = '/tmp/accent_check.wav'
for f in sys.argv[1:]:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vn', '-ac', '1', '-ar', '16000', W], check=True)
    a, _ = sf.read(W, dtype='float32'); bad = []; t = 0.0
    while t < len(a) / 16000 - 0.5:
        seg = a[int(t * 16000):int((t + 3) * 16000)]
        if abs(seg).max() > 0.02:
            lang, p, allp = wm.detect_language(seg); en = dict(allp).get('en', 0)
            o = acc.classify_batch(torch.tensor(seg)[None])[0][0]; top = L.decode_ndim(int(o.argmax())); us = float(o[US])
            if en < 0.90 or top not in ('us', 'canada') or us < 0.40: bad.append(f"{t:.1f}s en={en:.2f} accent={top} us={us:.2f}")
        t += 2.5
    print(('ACCENT_FLAG ' if bad else 'ACCENT_OK ') + f, '; '.join(bad), flush=True)
