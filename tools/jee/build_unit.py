"""Generic unit build (all units after Unit 1):  python3 build_unit.py ce
Needs <code>_pyq.py (P registry with chk), <code>_learn.py (CARDS, FORMULAS, TRAPS, STEPS, TOPICS, META), <code>_gen.py (GEN, check, finish).
Checks: 1 official key · 2 our code re-solve (chk) · 3 independent re-solve of every practice item (check) · 4 option integrity · 5 app_check.py"""
import json, random, re, os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import verify
code = sys.argv[1]; R = importlib.import_module(code + '_pyq'); L = importlib.import_module(code + '_learn'); G = importlib.import_module(code + '_gen')
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'); M = L.META
n_real = verify(R.P)
PER = int(os.environ.get('PER', 12))
pyq, prac, seen = [], [], set()
for i, p in enumerate(R.P):
    pid = f'{M["unit"].split("-")[1]}-{p["src"]["d"].replace("-", "")[2:]}{p["src"]["sh"]}-{i:02d}'
    q = dict(id=pid, src=p['src'], t=p['t'], q=p['q'], sol=p['sol'], fam=p['fam'], diff=p['diff'])
    if p.get('fig'): q['fig'] = p['fig']
    if p['o']: q.update(o=p['o'], a=p['key'] - 1)
    else: q.update(n=p['key'])
    pyq.append(q)
    made, seed = 0, 0
    while made < PER and seed < 600:
        rng = random.Random(f'{pid}:{seed}'); seed += 1
        it = G.finish(G.GEN[p['fam']](rng))
        key = re.sub(r'\s+', ' ', it['q']) + '|' + '|'.join(sorted(it.get('o') or []))
        if key in seen: continue
        assert G.check(it), ('independent check failed', it)
        if it.get('o'): assert len(set(it['o'])) == len(it['o']) == 4 and 0 <= it['a'] < 4, it
        else: assert isinstance(it['a'], int), it
        seen.add(key); made += 1
        item = dict(id=f'{pid}-v{made:02d}', like=pid, t=p['t'], q=it['q'], sol=it['sol'], diff=p['diff'])
        if it.get('fig'): item['fig'] = it['fig']
        if it.get('o'): item.update(o=it['o'], a=it['a'])
        else: item.update(n=it['a'])
        prac.append(item)
    if made < PER: print(f'  note: {pid} family {p["fam"]} gave {made} unique variants')
for c in L.CARDS: ch = c['check']; assert len(set(ch['o'])) == 4 and 0 <= ch['a'] < 4
for st in L.STEPS: assert all(any(c['id'] == x for c in L.CARDS) for x in st['cards'])
for p in pyq: assert p['t'] in L.TOPICS, p['t']
out = dict(v=1, **M, topics=L.TOPICS, cards=L.CARDS, formulas=L.FORMULAS, traps=L.TRAPS, steps=L.STEPS, pyq=pyq)
s, n = M['unit'].split('-'); os.makedirs(os.path.join(ROOT, f'content/jee/{s}'), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, f'content/jee/{s}/{n}.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(dict(v=1, unit=M['unit'], items=prac), open(os.path.join(ROOT, f'content/jee/{s}/{n}-practice.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
from collections import Counter
print(f'{M["title"]}: real {n_real} (key ✓ code ✓) · practice {len(prac)} (independent re-solve ✓ options ✓) · by year {dict(Counter(p["src"]["y"] for p in pyq))}')
