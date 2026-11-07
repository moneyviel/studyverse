#!/usr/bin/env python3
"""Validate the General Knowledge content in content/gk/.

Usage:  python3 tools/gk_validate.py            (from the repo root)
Checks: unique ids, valid grade ranges, every quiz answer is one of its options,
4 distinct options per question, no duplicate facts / thoughts / wow facts,
one "On this day" entry for every calendar day (incl. 29 Feb), minimum counts.
Exit code 1 if any error is found."""
import json, os, re, sys, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content', 'gk')
errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)
def norm(s): return re.sub(r'[^a-z0-9ऀ-ॿ]+', ' ', str(s).lower()).strip()

def grade_ok(g, where):
    if not (isinstance(g, list) and len(g) == 2 and all(isinstance(x, int) for x in g) and 1 <= g[0] <= g[1] <= 12):
        err(f'{where}: bad grade range {g!r}')

def text_ok(s, where):
    if not isinstance(s, str) or not s.strip(): err(f'{where}: empty text')

ids = {}
def uid(i, where):
    if i in ids: err(f'duplicate id {i} ({where} and {ids[i]})')
    ids[i] = where

idx = json.load(open(os.path.join(ROOT, 'index.json'), encoding='utf-8'))
fact_seen = {}
counts = {}
for c in idx['categories']:
    cid = c['id']
    d = json.load(open(os.path.join(ROOT, f'{cid}.json'), encoding='utf-8'))
    if d['id'] != cid: err(f'{cid}.json: id mismatch')
    if len(d['facts']) != c['nf'] or len(d['quiz']) != c['nq']: err(f'{cid}: index.json counts out of date')
    for f in d['facts']:
        w = f'{cid}/{f.get("id")}'; uid(f['id'], w); text_ok(f.get('f'), w); text_ok(f.get('e'), w); grade_ok(f.get('g'), w)
        k = norm(f['f'])
        if k in fact_seen: err(f'duplicate fact: {w} and {fact_seen[k]}')
        fact_seen[k] = w
    qseen = set()
    for q in d['quiz']:
        w = f'{cid}/{q.get("id")}'; uid(q['id'], w); text_ok(q.get('q'), w); text_ok(q.get('x'), w); grade_ok(q.get('g'), w)
        o = q.get('o', [])
        if len(o) != 4: err(f'{w}: needs exactly 4 options, has {len(o)}')
        if len({str(x).strip().lower() for x in o}) != len(o): err(f'{w}: options are not distinct')
        if not (isinstance(q.get('a'), int) and 0 <= q['a'] < len(o)): err(f'{w}: answer index {q.get("a")} is not one of the options')
        k = norm(q['q'])
        if k in qseen: err(f'{w}: duplicate question in category')
        qseen.add(k)
    counts[cid] = (len(d['facts']), len(d['quiz']))
    if len(d['facts']) < 40: err(f'{cid}: only {len(d["facts"])} facts (need 40)')
    if len(d['quiz']) < 20: err(f'{cid}: only {len(d["quiz"])} questions (need 20)')

dl = json.load(open(os.path.join(ROOT, 'daily.json'), encoding='utf-8'))
def uniq_list(lst, key, label):
    seen = {}
    for it in lst:
        w = f'{label}/{it.get("id")}'; uid(it['id'], w); text_ok(it.get(key), w); grade_ok(it.get('g'), w)
        k = norm(it[key])
        if k in seen: err(f'duplicate {label}: {w} and {seen[k]}')
        seen[k] = w
uniq_list(dl['thoughts'], 't', 'thought')
uniq_list(dl['wow'], 't', 'wow')
uniq_list(dl['words'], 'w', 'word')
for w in dl['wow']:
    if norm(w['t']) in fact_seen: warn(f'wow {w["id"]} repeats category fact {fact_seen[norm(w["t"])]}')
for b in dl['bites']:
    text_ok(b.get('q'), 'bite'); text_ok(b.get('a'), 'bite'); grade_ok(b.get('g'), f'bite/{b.get("id")}')
    if b['id'] not in ids: err(f'bite {b["id"]} does not match any quiz question')
# On this day: every calendar day of a leap year
day, need = datetime.date(2024, 1, 1), set()
while day.year == 2024: need.add(day.strftime('%m-%d')); day += datetime.timedelta(days=1)
have = set(dl['otd'])
for m in sorted(need - have): err(f'On this day: missing {m}')
for m in sorted(have - need): err(f'On this day: invalid date {m}')
for k, v in dl['otd'].items():
    text_ok(v.get('t'), f'otd/{k}')
    if not (isinstance(v.get('y'), int) and -3000 < v['y'] <= datetime.date.today().year): err(f'otd/{k}: bad year {v.get("y")}')
if len(dl['thoughts']) < 366: err(f'only {len(dl["thoughts"])} thoughts (need 366)')
if len(dl['wow']) < 200: err(f'only {len(dl["wow"])} wow facts (need ~200)')
# every grade must have something to show each day
for g in range(1, 13):
    for name in ('thoughts', 'wow', 'words', 'bites'):
        if not any(x['g'][0] <= g <= x['g'][1] for x in dl[name]): err(f'grade {g}: no {name}')

print('GK content')
for cid, (nf, nq) in counts.items(): print(f'  {cid:12s} {nf:4d} facts {nq:4d} questions')
print(f'  total        {sum(v[0] for v in counts.values()):4d} facts {sum(v[1] for v in counts.values()):4d} questions')
print(f'  daily: {len(dl["thoughts"])} thoughts, {len(dl["wow"])} wow facts, {len(dl["otd"])} on-this-day, {len(dl["words"])} words, {len(dl["bites"])} GK bites')
for w in warnings: print('WARN', w)
for e in errors: print('ERROR', e)
print('OK' if not errors else f'{len(errors)} error(s)')
sys.exit(1 if errors else 0)
