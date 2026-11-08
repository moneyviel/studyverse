#!/usr/bin/env python3
"""Builds the extra Paper 3 (Quantitative Aptitude) MCQ banks.

  python3 tools/ca_bank/build_p3.py [--ref /tmp/qa.txt]

Writes content/ca/foundation/p3/bank/<unit-id>.json  ({"unit", "mcq": [...]}, merged into the unit by js/ca.js)
and tools/ca_bank/p3_data.json (inputs for the independent re-solver tools/ca_bank/p3_verify.py).
Every question comes from a template in tools/ca_bank/p3_*.py that computes its answer. The builder asserts:
four distinct options (also after number parsing), exactly one equal to the computed answer, the check expression
equals the keyed option, explanation 35+ words, a fast method and a target time, no duplicate of an existing unit
MCQ, and (with --ref, a text dump of a reference question book) no stem whose set of numbers equals a reference stem.
Seeds are fixed, so the output is reproducible.
"""
import json, os, re, sys, random, importlib, difflib
sys.dont_write_bytecode = True          # keep the shared tools folders free of .pyc files
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'tools'))
from common import words
import ca_validate as V          # calc(), opt_num(), close(): the validator's own parsers

MODULES = ['p3_ch01', 'p3_ch02', 'p3_ch03', 'p3_ch04', 'p3_ch05', 'p3_ch06', 'p3_ch07', 'p3_ch08', 'p3_ch09',
           'p3_ch10', 'p3_ch11', 'p3_ch12', 'p3_ch13', 'p3_ch14', 'p3_ch15', 'p3_ch16', 'p3_ch17', 'p3_ch18']
ONLY = [a for a in sys.argv[1:] if a.startswith('p3_')]


def nums_in(s):
    return frozenset(x for x in (re.sub(r',', '', m) for m in re.findall(r'\d[\d,]*\.?\d*', s)) if x not in ('0', '1', '2', '3', '4', '5', '10', '100'))


def ref_sets():
    if '--ref' not in sys.argv: return set()
    t = open(sys.argv[sys.argv.index('--ref') + 1], encoding='utf-8', errors='ignore').read()
    out = set()
    for blk in re.split(r'\n\s*\d{1,3}\.\s', t):
        stem = re.split(r'\n\s*\(?a\)', blk)[0]
        s = nums_in(stem)
        if len(s) >= 2: out.add(s)
    return out


def ref_grams(n=8):
    if '--ref' not in sys.argv: return set()
    ws = V.words(open(sys.argv[sys.argv.index('--ref') + 1], encoding='utf-8', errors='ignore').read())
    return {' '.join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def shares_run(m, grams, n=8):
    for t in [m['q'], m['explain'], m['fast']] + list(m['options']):
        ws = V.words(t)
        if any(' '.join(ws[i:i + n]) in grams for i in range(len(ws) - n + 1)): return True
    return False


def stem_words(s): return set(w for w in re.findall(r'[a-z0-9₹]+', s.lower()) if len(w) > 2)      # same rule as tools/ca_bank_check.py
def stem_data(s): return sorted(re.findall(r'\d+(?:\.\d+)?', s) + re.findall(r'(?:(?<=[^.?!:] )|(?<= "))[A-Z][\w-]*', s))
def near_dup(a, b): return len(a[0] & b[0]) / max(1, len(a[0] | b[0])) >= 0.75 and a[1] == b[1]


def norm(s): return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()


def opt_val(o):
    v, side = V.opt_num(o)
    return None if v is None else (round(v, 6), side)


def finish(t, r, mid):
    """t: template output -> MCQ dict (answer position random), or raises AssertionError"""
    a = t['a']; av = opt_val(a); seen = {a}; vals = {av} if av else set(); wrong = []
    for w in t['w']:
        if w in seen: continue
        wv = opt_val(w)
        if av and wv and wv[1] == av[1] and V.close(wv[0], av[0]): continue
        if wv and any(V.close(wv[0], x[0]) and wv[1] == x[1] for x in vals): continue
        seen.add(w); wrong.append(w)
        if wv: vals.add(wv)
        if len(wrong) == 3: break
    assert len(wrong) == 3, f'only {len(wrong)} usable distractors'
    pos = r.randrange(4); opts = wrong[:pos] + [a] + wrong[pos:]
    assert len(set(opts)) == 4
    m = {'id': mid, 'q': t['q'], 'options': opts, 'answer': pos, 'explain': t['ex'], 'concept': None,
         'topic': t['topic'], 'difficulty': t.get('d', 'moderate'), 'fast': t['fast'], 'secs': int(t['secs'])}
    if t.get('check') is not None and av: m['check'] = str(t['check'])   # fractions like 3/8 are not parsed by the validator; p3_verify.py checks them
    elif av and len(re.sub(r'[^0-9]', '', a)) >= 2: raise AssertionError(f'numeric answer {a} needs a check')
    if 'check' in m:
        v = V.calc(m['check'])
        assert av and V.close(v, av[0]), f'check {m["check"]} = {v} but answer {a}'
    assert words(m['explain']) >= 35, f'explain only {words(m["explain"])} words: {m["explain"][:60]}'
    assert words(m['fast']) >= 6 and 15 <= m['secs'] <= 180, f'fast too short: {m["fast"]}'
    return m


def main():
    refs = ref_sets(); grams = ref_grams(); banks = {}; data = {}; seen_all = []
    existing = {}
    st = json.load(open(os.path.join(ROOT, 'content/ca/foundation/structure.json'), encoding='utf-8'))
    units = {u['id']: u for p in st['papers'] if p['key'] == 'p3' for c in p['chapters'] for u in c['units']}
    datap = os.path.join(HERE, 'p3_data.json')
    if ONLY and os.path.exists(datap): data = json.load(open(datap, encoding='utf-8'))
    for modname in MODULES:
        if ONLY and modname not in ONLY: continue
        mod = importlib.import_module(modname)
        for uid, temps in mod.BANKS.items():
            data = {k: v for k, v in data.items() if not k.startswith(uid + '#')}
            u = units[uid]; ud = json.load(open(os.path.join(ROOT, u['file']), encoding='utf-8'))
            concepts = {c['title']: c['id'] for c in ud['concepts']}
            old = [q['q'] for q in ud['mcqs']] + [q['q'] for cs in ud.get('cases', []) for q in cs['mcqs']]
            oldsig = [(stem_words(x), stem_data(x)) for x in old]
            oldn = {norm(x) for x in old}; oldsets = [(nums_in(x), norm(x)) for x in old]
            used = set(q['id'] for q in ud['mcqs']) | {q['id'] for cs in ud.get('cases', []) for q in cs['mcqs']}
            out = []; texts = set(); n = 0; skipped = {'ref': 0, 'dup': 0, 'bad': 0}
            for ti, (fn, want) in enumerate(temps):
                got = 0; seed = 0; errs = __import__('collections').Counter()
                while got < want:
                    seed += 1
                    if seed > 4000: raise SystemExit(f'{uid}: template {fn.__name__} could not make {want} questions')
                    r = random.Random(f'{uid}:{fn.__name__}:{seed}')
                    t = fn(r)
                    if not t: continue
                    nq = norm(t['q'])
                    if nq in texts or nq in oldn: skipped['dup'] += 1; continue
                    ns = nums_in(t['q'])
                    if len(ns) >= 2 and ns in refs: skipped['ref'] += 1; continue
                    sig = (stem_words(t['q']), stem_data(t['q']))
                    if any(near_dup(sig, o) for o in oldsig) or any(near_dup(sig, o) for o in seen_all): skipped['dup'] += 1; continue
                    if len(ns) >= 2 and any(ns == s and difflib.SequenceMatcher(None, nq, o).ratio() > .6 for s, o in oldsets): skipped['dup'] += 1; continue
                    n += 1; mid = f'b{n:02d}'
                    assert mid not in used
                    try: m = finish(t, r, mid)
                    except AssertionError as e:
                        n -= 1; skipped['bad'] += 1; errs[re.sub(r'\d+', '#', str(e))[:70]] += 1
                        if seed > 3000: raise SystemExit(f'{uid} {fn.__name__}: {errs.most_common(3)}')
                        continue
                    if grams and shares_run(m, grams):             # no run of 8 words in common with the reference book
                        n -= 1; skipped['ref'] += 1; errs['8-word run shared with the reference'] += 1
                        if seed > 3000: raise SystemExit(f'{uid} {fn.__name__}: {errs.most_common(3)}')
                        continue
                    assert t['topic'] in concepts, f'{uid}: topic {t["topic"]!r} is not a concept title'
                    m['concept'] = concepts[t['topic']]
                    out.append(m); texts.add(nq); got += 1; seen_all.append(sig)
                    data[f'{uid}#{mid}'] = {'k': t['k'], 'd': t['data']}
            banks[uid] = out
            print(f'{uid}: {len(out)} MCQs  (skipped: {skipped})')
    for uid, qs in banks.items():
        f = os.path.join(ROOT, 'content/ca/foundation/p3/bank', uid + '.json')
        os.makedirs(os.path.dirname(f), exist_ok=True)
        json.dump({'unit': uid, 'mcq': qs}, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(data, open(datap, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    print('total', sum(len(v) for v in banks.values()))


if __name__ == '__main__':
    main()
