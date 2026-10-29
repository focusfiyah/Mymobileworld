# synth_kit.py <film folder> [--keys DIR]: a free sound kit for mix.py, made with numpy (no Scenario credits).
# Writes the 12 core names (whoosh_1/2, whoosh_big, impact, impact_big, hit, slash, key_1/2, pop, tick, riser,
# glitch, logo_hit) to <film>/audio/sfx/. --keys copies real CC0 key clicks (e.g. Dayone-ai assets/sfx/key-*.wav)
# as key_1..key_N instead of the synthesized ones. Existing files are kept, so a better sound dropped in wins.
import os, sys, glob, shutil, wave, argparse, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('film'); ap.add_argument('--keys')
a = ap.parse_args()
SR = 48000; D = os.path.join(a.film, 'audio', 'sfx'); os.makedirs(D, exist_ok=True)
rng = np.random.default_rng(7)
t = lambda s: np.arange(int(s * SR)) / SR
def env(n, att, dec):  # attack then exponential decay, in seconds
    x = np.arange(n) / SR; return np.minimum(1, x / max(att, 1e-4)) * np.exp(-np.maximum(0, x - att) / dec)
def lp(x, k):  # one-pole low-pass, k in 0..1 (per sample, may be an array)
    y = np.empty_like(x); s = 0.0; k = np.broadcast_to(k, x.shape)
    for i in range(len(x)): s += k[i] * (x[i] - s); y[i] = s
    return y
def noise(s): return rng.standard_normal(int(s * SR))
def sweep(s, lo, hi):  # band of noise whose brightness rises and falls: a pass-by
    n = int(s * SR); p = np.sin(np.linspace(0, np.pi, n)) ** 2
    k = lo + (hi - lo) * p; x = lp(noise(s), k) - lp(noise(s), k * .25)
    return x * p
def thump(s, f0, f1, dec):
    x = t(s); f = f1 + (f0 - f1) * np.exp(-x / .04); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), .002, dec)
def save(name, x):
    p = os.path.join(D, name + '.wav')
    if os.path.exists(p): return
    x = x / (np.abs(x).max() or 1) * .89; st = np.stack([x, x], 1)
    if len(x) > 400: st[:, 1] = np.roll(x, 12)  # a little width
    with wave.open(p, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
save('whoosh_1', sweep(.7, .02, .35)); save('whoosh_2', sweep(.6, .03, .45))
save('whoosh_big', sweep(1.3, .01, .2) + .6 * thump(1.3, 90, 40, .5) * np.sin(np.linspace(0, np.pi, int(1.3 * SR))))
save('impact', thump(1.2, 160, 45, .25) + .35 * lp(noise(1.2), .25) * env(int(1.2 * SR), .001, .06))
save('impact_big', thump(2.2, 120, 32, .7) + .5 * lp(noise(2.2), .15) * env(int(2.2 * SR), .001, .25))
save('hit', .8 * lp(noise(.5), .6) * env(int(.5 * SR), .0005, .04) + thump(.5, 220, 120, .06))
save('slash', sweep(.6, .15, .9) * env(int(.6 * SR), .01, .15))
save('pop', np.sin(2 * np.pi * np.cumsum(np.linspace(900, 400, int(.3 * SR))) / SR) * env(int(.3 * SR), .002, .05))
save('tick', lp(noise(.25), .8) * env(int(.25 * SR), .0003, .008) + .4 * np.sin(2 * np.pi * 3200 * t(.25)) * env(int(.25 * SR), .0005, .01))
x = t(2.2); save('riser', lp(noise(2.2), np.linspace(.01, .7, len(x))) * (x / 2.2) ** 2.5 + .3 * np.sin(2 * np.pi * np.cumsum(np.linspace(200, 1600, len(x))) / SR) * (x / 2.2) ** 3)
g = noise(.6) * np.repeat(rng.random(int(.6 * SR) // 900 + 1) > .45, 900)[:int(.6 * SR)]
save('glitch', np.round(g * 3) / 3 * env(int(.6 * SR), .001, .25))
x = t(3); save('logo_hit', thump(3, 110, 30, 1.0) + .25 * sum(np.sin(2 * np.pi * f * x) for f in (880, 1320, 1760)) * env(len(x), .005, .9))
keys = sorted(glob.glob(os.path.join(a.keys, 'key*'))) if a.keys else []
for i, f in enumerate(keys, 1):
    dst = os.path.join(D, f'key_{i}' + os.path.splitext(f)[1])
    if not os.path.exists(dst): shutil.copy(f, dst)
if not keys:
    for i in (1, 2): save(f'key_{i}', lp(noise(.3), .7 - .1 * i) * env(int(.3 * SR), .0005, .015) + .5 * thump(.3, 400 + 80 * i, 250, .02))
print('kit:', D, len(os.listdir(D)), 'files')
