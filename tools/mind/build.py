#!/usr/bin/env python3
"""Turns the hand-written Mind Gym files (eq.txt, sq.txt, aq.txt, cq.txt) into content/mind/<test>.json and checks them.
Line: band | situation | best | weaker 1 | weaker 2 | weaker 3 | why.   band: j (Gr 1-3), m (4-8), s (9-12), p (CA)."""
import json, os, sys, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', '..', 'content', 'mind')
TARGET = {'j': 60, 'm': 70, 's': 70, 'p': 50}
ok = True
allq = {}
for t in ('eq', 'sq', 'aq', 'cq'):
    f = os.path.join(HERE, t + '.txt')
    if not os.path.exists(f):
        continue
    qs, seen = [], set()
    for n, line in enumerate(open(f, encoding='utf-8'), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        p = [x.strip() for x in line.split('|')]
        if len(p) != 7 or p[0] not in TARGET or any(not x for x in p):
            print('%s.txt line %d: bad line' % (t, n)); ok = False; continue
        b, q, best, w1, w2, w3, why = p
        opts = [best, w1, w2, w3]
        if len(set(o.lower() for o in opts)) != 4:
            print('%s.txt line %d: repeated option' % (t, n)); ok = False
        key = re.sub(r'\W+', ' ', q.lower()).strip()
        if key in seen:
            print('%s.txt line %d: repeated situation' % (t, n)); ok = False
        seen.add(key)
        for o2, prev in allq.items():
            if key in prev:
                print('%s.txt line %d: same situation as in %s' % (t, n, o2)); ok = False
        qs.append({'b': b, 'q': q, 'o': opts, 'a': 0, 'why': why})
    allq[t] = seen
    c = collections.Counter(q['b'] for q in qs)
    longest = sum(1 for q in qs if len(q['o'][0]) == max(len(o) for o in q['o']))
    print('%s: %d questions %s · best answer is the longest option in %d%%' % (t, len(qs), dict(c), round(100 * longest / max(1, len(qs)))))
    for b, n in TARGET.items():
        if c[b] < n:
            print('  %s band %s: %d of %d' % (t, b, c[b], n))
    for i, q in enumerate(qs):
        q['id'] = '%s-%s-%03d' % (t, q['b'], i + 1)
    json.dump({'test': t, 'v': 1, 'questions': qs}, open(os.path.join(OUT, t + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
sys.exit(0 if ok else 1)
