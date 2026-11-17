"""Accent drift check for AI twin audio (Ralph 2026-11-16: on the posted T2 the voice turned "like a Russian accent" on "Follow for more").
Speech-to-text language check on every 3 s window; English below 0.90 = the voice drifted. Run on every raw Flow clip (Veo's own voice;
speech-to-speech copies its delivery) and on every final cut. Prints ACCENT_OK or ACCENT_FLAG with the windows.
Found 2026-11-16: posted T2 ends 0.86 / 0.82, its raw Veo clip T2_4 0.83; all other twin videos 0.96+.
Usage: ~/.presenter-tools/cbx/bin/python -I accent_check.py FILE [FILE ...]"""
import sys, subprocess, soundfile as sf
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
for f in sys.argv[1:]:
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    step=3.0; t=0; row=[]
    while t<d-0.5:
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-t',str(step),'-i',f,'-vn','-ac','1','-ar','16000','/tmp/claude-0/cut/seg.wav'],check=True)
        a,_=sf.read('/tmp/claude-0/cut/seg.wav',dtype='float32')
        lang,prob,allp=m.detect_language(a)
        en=dict(allp).get('en',0)
        row.append((t,lang,en)); t+=step
    bad=[f"{t:.0f}s {l} en={e:.2f}" for t,l,e in row if e<0.90]
    print(('ACCENT_FLAG ' if bad else 'ACCENT_OK ')+f, '; '.join(bad))
