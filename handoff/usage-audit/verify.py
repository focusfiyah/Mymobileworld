"""Checks for the 2026-10-30 usage audit. Usage: verify.py size|lossless|keep|settings"""
import json, sys, os
H = os.path.dirname(os.path.abspath(__file__))
MMW, D1 = '/home/user/Mymobileworld', '/home/user/Dayone-ai'
pairs = [(f'{H}/orig_mmw_CLAUDE.md.txt', f'{MMW}/CLAUDE.md', [f'{MMW}/handoff/history/JOBS_LOG.md', f'{MMW}/handoff/history/SKILL_INSTALL_LOG.md']),
         (f'{H}/orig_d1_CLAUDE.md.txt', f'{D1}/CLAUDE.md', [f'{D1}/handoff/history/STATUS_LOG.md'])]
def rd(p): return open(p).read()
def size():
    for o, n, _ in pairs:
        a, b = len(rd(o).encode()), len(rd(n).encode())
        print(n, a, '->', b, f'{100 - 100 * b // a}% smaller'); assert b <= 0.7 * a, 'not 30% smaller'
    print('SIZE_OK')
def lossless():
    for o, n, logs in pairs:
        have = set(l.strip() for p in [n] + logs for l in rd(p).split('\n'))
        miss = [l for l in rd(o).split('\n') if l.strip() and l.strip() not in have]
        print(n, 'missing lines:', len(miss)); assert not miss, miss[:2]
    print('LOSSLESS_OK')
def keep():
    need = {f'{MMW}/CLAUDE.md': ['Rule 0: the SCRIPT GATE', 'Hard rules for every ad', 'House of Rameau (@houseoframeau)', 'Posting volume (2026-10-30', 'Jean Rameau (client #2', 'Skills (Ralph 2026-10-13): one home', 'handoff/history/JOBS_LOG.md', 'handoff/history/SKILL_INSTALL_LOG.md'],
            f'{D1}/CLAUDE.md': ["Ralph's decisions (do not re-ask)", 'Daily routine (fixed 2026-09-29)', 'Instagram (Ralph 2026-10-28', 'Higgsfield Ads Studio', 'Skill standard (Ralph, 2026-10-05)', 'handoff/history/STATUS_LOG.md']}
    for p, ks in need.items():
        t = rd(p)
        for k in ks: assert k in t, (p, k)
    for p in [f'{MMW}/handoff/history/JOBS_LOG.md', f'{MMW}/handoff/history/SKILL_INSTALL_LOG.md', f'{D1}/handoff/history/STATUS_LOG.md']: assert os.path.getsize(p) > 5000, p
    print('KEEP_OK')
def settings():
    for r in (MMW, D1):
        d = json.load(open(f'{r}/.claude/settings.json'))
        assert d['env']['BASH_MAX_OUTPUT_LENGTH'] == '20000' and 'Read(**/node_modules/**)' in d['permissions']['deny'], r
        assert d['hooks']['SessionStart'] and d['enabledMcpjsonServers'], r
    print('SETTINGS_OK')
globals()[sys.argv[1]]()
