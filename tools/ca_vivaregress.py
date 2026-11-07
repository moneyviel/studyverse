"""Viva regression: natural correct paraphrases and wrong answers for every viva question of the original 7 CA units.
   python3 tools/ca_vivaregress.py            (checks both matchers: Python tools/ca_vivamatch.py and the JS one in js/ca-tools.js)
Cases live in tools/ca_viva_regression.json — see its "_about". Questions are read from tools/ca_src/ca_viva.py (the source of
the shipped viva blocks), so run this before python3 tools/ca_src/build.py."""
import json, os, sys, subprocess, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'ca_src'))
import ca_vivamatch as VM
from ca_viva import VIVA

cases = json.load(open(os.path.join(ROOT, 'tools', 'ca_viva_regression.json'), encoding='utf-8'))['cases']
bad, per = [], {}
pairs = []
for c in cases:
    v = next((x for x in VIVA.get(c['u'], []) if x['id'] == c['v']), None)
    if not v: bad.append(f"{c['u']}#{c['v']}: question not found"); continue
    per.setdefault((c['u'], c['v']), [0, 0])[0 if c['ok'] else 1] += 1
    pairs.append((c, v))

def judge(c, pct, hit, v=None):
    if c['ok']:
        need = c.get('hit')
        if need: miss = [p for p in need if p not in hit]; return f'should cover {miss}' if miss else None
        return None if pct == 100 else f'scored {pct}% (missed {[p["id"] for p in v["points"] if p["id"] not in hit]})'
    if pct >= 80: return f'wrong answer scored {pct}% (viva-ready)'
    leak = [p for p in c.get('miss', []) if p in hit]
    return f'wrong answer covered {leak}' if leak else None

for c, v in pairs:
    pct, hit = VM.score(v, c['a'])
    m = judge(c, pct, hit, v)
    if m: bad.append(f"PY {c['u']}#{c['v']} {'OK ' if c['ok'] else 'BAD'}: {m}\n     “{c['a'][:110]}”")
js = 'not run'
if shutil.which('node'):
    r = subprocess.run(['node', os.path.join(ROOT, 'tools', 'ca_vivaparity.js'), os.path.join(ROOT, 'js', 'ca-tools.js')],
                       input=json.dumps([[v, c['a']] for c, v in pairs]), capture_output=True, text=True, timeout=60)
    if r.returncode: bad.append('JS matcher failed: ' + r.stderr[:300]); js = 'failed'
    else:
        diff = 0
        for (c, v), (pj, hj, tj) in zip(pairs, json.loads(r.stdout)):
            pp, hp = VM.score(v, c['a'])
            if pp != pj or hp != hj: diff += 1; bad.append(f"PARITY {c['u']}#{c['v']}: JS {pj}% {hj} vs PY {pp}% {hp}")
            m = judge(c, pj, hj, v)
            if m and not (pp == pj and hp == hj): bad.append(f"JS {c['u']}#{c['v']}: {m}")
        js = 'same as Python' if not diff else f'{diff} differences'
thin = [f'{u}#{v}: {n[0]} correct / {n[1]} wrong' for (u, v), n in per.items() if n[0] < 3 or n[1] < 2]
nq = sum(len(x) for k, x in VIVA.items() if k in {c['u'] for c in cases})
missing = [f'{u}#{x["id"]}' for u in {c['u'] for c in cases} for x in VIVA[u] if (u, x['id']) not in per]
print(f'{len(pairs)} answers · {len(per)} of {nq} questions covered · JS matcher {js}')
for t in thin + [m + ': no regression answers' for m in missing]: print('  THIN', t)
for b in bad: print('  FAIL', b)
print('PASS' if not bad and not thin and not missing else f'{len(bad)} failure(s)')
sys.exit(1 if bad or thin or missing else 0)
