"""Build content/jee/phy/u01.json (Units & Measurements) with five independent checks.
  1  official NTA key                         (real questions)
  2  our own code re-computation               (real + practice)
  3  same computation on the DEFINITION-built dimension table (real) / independent re-solver check2.py (practice)
  4  option integrity: distinct options, exactly one marked correct, displayed correct text re-parsed
  5  runtime check in the app (tools/jee/app_check.py, Playwright)"""
import json, random, re, os, sys, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import dims, u01_pyq as R, u01_gen as G, check2, u01_learn as L
from fractions import Fraction as F
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
dims.check(); check2.homo_check()
n_real = R.verify()                                                   # checks 1 + 2
DQ = dict(dims.TABLE); DQ.update(dims.DEFS)
R.Q = DQ; R.verify(); R.Q = dims.TABLE                                 # check 3 (real): definition-built table
PERR_HINT = [('resistivity', 'dens'), ('density', 'dens'), ('Ohm', 'ohm'), ('resistance R', 'ohm'), ('spring', 'shm'), ('oscillat', 'shm'), ("Young", 'young'), ('sphere', 'sphere'), ('e^{−', 'exp'), ('parallel', None)]
pyq, prac, seen = [], [], set()
for i, p in enumerate(R.P):
    pid = f'p{p["src"]["d"].replace("-", "")[2:]}{p["src"]["sh"]}-{i:02d}'
    q = dict(id=pid, src=p['src'], t=p['t'], q=p['q'], sol=p['sol'], fam=p['fam'], diff=p['diff'])
    if p['o']: q.update(o=p['o'], a=p['key'] - 1)
    else: q.update(n=p['key'])
    pyq.append(q)
    gen = G.GEN[p['fam']]; want = next((w for k, w in PERR_HINT if k in p['q']), 'powint' if not p['o'] else None) if p['fam'] == 'perr' else None
    made, seed = 0, 0
    while made < 12 and seed < 400:
        rng = random.Random(f'{pid}:{seed}'); seed += 1
        it = gen(rng, want if seed % 3 else None) if p['fam'] == 'perr' else gen(rng)
        key = re.sub(r'\s+', ' ', it['q']) + '|' + '|'.join(sorted(it.get('o') or []))
        if key in seen: continue
        # check 3 (practice): independent re-solve;  check 4: option integrity
        assert check2.solve(it), ('independent solver disagrees', it['q'], it.get('o'), it['a'], it['p'])
        if it.get('o'):
            assert len(set(it['o'])) == len(it['o']) == 4 and 0 <= it['a'] < 4, it
        else:
            assert isinstance(it['a'], int), it
        seen.add(key); made += 1
        tt = ('units' if 'SI unit' in it['q'] else 'dim') if p['fam'] in ('dimq', 'units') else p['t']
        item = dict(id=f'{pid}-v{made:02d}', like=pid, t=tt, q=it['q'], sol=it['sol'], diff=p['diff'])
        if it.get('o'): item.update(o=it['o'], a=it['a'])
        else: item.update(n=it['a'])
        prac.append(item)
    assert made == 12, (pid, made)
# quick checks inside the concept cards
for c in L.CARDS:
    ch = c['check']; assert len(set(ch['o'])) == 4 and 0 <= ch['a'] < 4
out = dict(v=1, unit='phy-u01', subject='phy', title='Units and Measurements', cls=11,
           syllabus='Units of measurements, system of units, SI units, fundamental and derived units, least count, significant figures, errors in measurements, dimensions of physical quantities, dimensional analysis and its applications.',
           cards=L.CARDS, formulas=L.FORMULAS, traps=L.TRAPS, steps=L.STEPS, pyq=pyq)
os.makedirs(os.path.join(ROOT, 'content/jee/phy'), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, 'content/jee/phy/u01.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(dict(v=1, unit='phy-u01', items=prac), open(os.path.join(ROOT, 'content/jee/phy/u01-practice.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print(f'real questions: {n_real} (NTA key ✓, code ✓, definition table ✓) · practice: {len(prac)} (independent re-solve ✓, options ✓)')
from collections import Counter
print('by year:', dict(Counter(p['src']['y'] + ' ' + p['src']['s'] for p in pyq)), '| by topic:', dict(Counter(p['t'] for p in pyq)))
