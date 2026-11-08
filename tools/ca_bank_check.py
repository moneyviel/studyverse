#!/usr/bin/env python3
"""Checks the extra MCQ banks: content/ca/<level>/<paper>/bank/<unit-id>.json = {"unit": id, "mcq": [...]}

Uses the same MCQ rules as tools/ca_validate.py (check_mcq: 4 distinct options, answer index, numeric `check`
re-computed and equal to the keyed option and to no other option) plus:
  * the unit exists; bank ids unique and not clashing with the unit's own MCQ / case-MCQ ids
  * `topic` = a structure.json topic of the unit or a concept-card title; `concept` exists; explain 35+ words
  * `fast` (non-empty text) and `secs` (10-180) present; difficulty core/moderate/hard
  * duplicates: question stems compared with the unit's MCQs, its case MCQs and every other bank item
    (word-set overlap >= 0.75 is an error)
  * originality: --ref FILE (repeatable) — no run of 8 consecutive words shared with a reference text
    (e.g. pdftotext output of a coaching question book); --src DIR — 10-word ICAI check as in ca_validate.py

Usage: python3 tools/ca_bank_check.py [--paper p2 --paper p4] [--ref /tmp/ref/law.txt ...] [--src /tmp/ca/txt]
"""
import json, os, re, sys, glob
sys.dont_write_bytecode = True          # do not leave .pyc files next to the shared tools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ca_validate as V

ROOT = V.ROOT
def args(flag): return [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == flag and i + 1 < len(sys.argv)]
PAPERS = args('--paper'); REFS = args('--ref'); SRC = (args('--src') or [None])[0]

def stem_words(s): return set(w for w in re.findall(r'[a-z0-9₹]+', s.lower()) if len(w) > 2)
def jacc(a, b): return len(a & b) / max(1, len(a | b))
def stem_nums(s):
    # the data of a question: numbers and capitalised tokens not starting a sentence (names, letters, codes, directions);
    # templated Paper 3 questions with different data are different questions, not duplicates
    return sorted(re.findall(r'\d+(?:\.\d+)?', s) + re.findall(r'(?:(?<=[^.?!:] )|(?<= "))[A-Z][\w-]*', s))

def main():
    struct = {}
    for lv in ('foundation', 'inter', 'final'):
        p = os.path.join(V.CA, lv, 'structure.json')
        if os.path.exists(p):
            for pp in json.load(open(p, encoding='utf-8'))['papers']:
                for c in pp['chapters']:
                    for u in c['units']: struct[u['id']] = u
    files = sorted(glob.glob(os.path.join(V.CA, '*', 'p*', 'bank', '*.json')))
    if PAPERS: files = [f for f in files if os.path.basename(os.path.dirname(os.path.dirname(f))) in PAPERS]
    allq, per = [], {}
    for f in files:
        w0 = os.path.relpath(f, ROOT)
        try: b = json.load(open(f, encoding='utf-8'))
        except Exception as e: V.err(w0, f'bad JSON: {e}'); continue
        uid = b.get('unit')
        if os.path.basename(f) != f'{uid}.json': V.err(w0, 'file name must be <unit>.json')
        if uid not in struct: V.err(w0, f'unknown unit {uid}'); continue
        uf = os.path.join(ROOT, struct[uid].get('file', ''))
        if not os.path.exists(uf): V.err(w0, f'unit file {uf} missing'); continue
        u = json.load(open(uf, encoding='utf-8'))
        cids = {c['id'] for c in u.get('concepts', [])}
        allowed = {V.norm_topic(t) for t in struct[uid].get('topics') or []} | {V.norm_topic(c.get('title')) for c in u.get('concepts', [])}
        own = u.get('mcqs', []) + [m for cs in u.get('cases', []) for m in cs.get('mcqs', [])]
        used = {m['id'] for m in own}
        mcq = b.get('mcq')
        if not isinstance(mcq, list) or not mcq: V.err(w0, 'needs a non-empty "mcq" list'); continue
        for q in mcq:
            w = f'{w0}#{q.get("id")}'
            if q.get('id') in used: V.err(w, 'id clashes with the unit or another bank question')
            used.add(q.get('id'))
            V.check_mcq(w, q, cids)
            if len({str(o).strip().lower() for o in q['options']}) != 4: V.err(w, 'options not distinct (case-insensitive)')
            if V.norm_topic(q.get('topic')) not in allowed: V.err(w, f'topic "{q.get("topic")}" not a unit topic / concept title')
            if not q.get('concept'): V.err(w, 'needs concept')
            n = len(re.findall(r'\S+', q.get('explain', '')))
            if n < 35: V.err(w, f'explain has {n} words (35+ needed)')
            if not str(q.get('fast', '')).strip(): V.err(w, 'needs fast')
            if not isinstance(q.get('secs'), int) or not 10 <= q['secs'] <= 180: V.err(w, 'secs must be an integer 10-180')
            if q.get('difficulty') not in ('core', 'moderate', 'hard'): V.err(w, 'difficulty must be core/moderate/hard')
            sw = stem_words(q['q'])
            for m in own:
                if jacc(sw, stem_words(m['q'])) >= 0.75 and stem_nums(q['q']) == stem_nums(m['q']): V.err(w, f'near-duplicate of unit question {m["id"]}: "{m["q"][:60]}"')
            allq.append((w, uid, q, sw))
        per[uid] = len(mcq)
    for i in range(len(allq)):
        for j in range(i + 1, len(allq)):
            if jacc(allq[i][3], allq[j][3]) >= 0.75 and stem_nums(allq[i][2]['q']) == stem_nums(allq[j][2]['q']): V.err(allq[i][0], f'near-duplicate of {allq[j][0]}')
    # originality against reference texts
    def grams(ws, n): return {' '.join(ws[i:i + n]) for i in range(len(ws) - n + 1)}
    texts = lambda q: [q['q'], q['explain'], q['fast']] + [str(o) for o in q['options']]
    if REFS:
        rg = set()
        for r in REFS: rg |= grams(V.words(open(r, encoding='utf-8', errors='ignore').read()), 8)
        for w, uid, q, _ in allq:
            for t in texts(q):
                hit = grams(V.words(t), 8) & rg
                if hit: V.err(w, f'ORIGINALITY (reference text): 8 words match: "{sorted(hit)[0]}"'); break
    if SRC:
        sg = set()
        for f in glob.glob(os.path.join(SRC, 'CA - Foundation__*.txt')): sg |= grams(V.words(open(f, encoding='utf-8', errors='ignore').read()), 10)
        for w, uid, q, _ in allq:
            for t in texts(q):
                hit = grams(V.words(t), 10) & sg
                if hit: V.err(w, f'ORIGINALITY (ICAI text): 10 words match: "{sorted(hit)[0]}"'); break
    byp = {}
    for uid, n in per.items():
        ch = uid.rsplit('-', 1)[0]; byp[ch] = byp.get(ch, 0) + n
    for ch, n in sorted(byp.items()): print(f'{ch}: {n} bank MCQs')
    print(f'bank files {len(per)} · bank MCQs {sum(per.values())} · numeric (check) {sum(1 for _, _, q, _ in allq if "check" in q)}'
          + (f' · reference texts {len(REFS)}' if REFS else '') + (' · ICAI text checked' if SRC else ''))
    for x in V.warns: print('WARN ', x)
    for x in V.errors: print('ERROR', x)
    print('OK' if not V.errors else f'{len(V.errors)} error(s)')
    sys.exit(1 if V.errors else 0)

if __name__ == '__main__':
    main()
