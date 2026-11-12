"""Builds extra situation questions for eq/sq/aq/cq from scen_data.py (used by build.py). Deterministic.
Every question: one clearly right option + three clearly wrong ones, drawn from pools written to fit EVERY situation of the skill."""
import random, re, hashlib
from scen_data import ALL, FEEL_CLUSTERS, AVOID
MIX = {'j': ['j'], 'm': ['m', 'j'], 's': ['s', 'm'], 'p': ['p', 's']}
NOT_WHY = {'not': '“{o}” would not help. '}
def clus(f):
    for c in FEEL_CLUSTERS:
        if f in c: return c
    raise ValueError(f)
def sits(sk, b):
    return sk.get('sit', {}).get(b, []) + sk.get('pools', {}).get(b, [])
def gen(t):
    spec, out, seen = ALL[t], [], set()
    for b in 'jmsp':
        grp = 'j' if b == 'j' else 'x'
        for skn, sk in spec.items():
            for src in MIX[b]:
                for s in sits(sk, src):
                    rnd = random.Random(hashlib.md5(f'{t}{b}{skn}{s}'.encode()).hexdigest())
                    nv = 3 if b in 'jp' else 2
                    frames = []
                    if sk['kind'] == 'match':
                        text, ans, clue = s.split('|')
                        c = clus(ans); others = [f for cc in FEEL_CLUSTERS if cc is not c for f in cc if f not in AVOID.get(ans, [])]
                        q = f"{text} {sk['q'][grp]}"
                        frames.append((q, [ans] + rnd.sample(others, 3), sk['why'].format(clue=clue)))
                    else:
                        G, B = sk['good'][grp], sk['bad'][grp]
                        for fr, ftxt in sk['frames'].items():
                            q = f"{s} {ftxt}"
                            if fr == 'best': pg, pb = G, B
                            elif fr == 'not': pg, pb = B, G
                            else: pg, pb = sk['gsay'][grp], sk['bsay'][grp]
                            rights = rnd.sample(pg, min(nv, len(pg)))
                            for r in rights:
                                opts = [r] + rnd.sample(pb, 3)
                                why = sk['why']['best'] if fr == 'best' else (f'“{r}” would not help. ' + sk['why']['not']) if fr == 'not' else sk['why']['say']
                                frames.append((q, opts, why))
                    for q, opts, why in frames:
                        key = (b, re.sub(r'\W+', ' ', q.lower()).strip(), opts[0])
                        if key in seen: continue
                        assert len(set(opts)) == 4, (t, q, opts)
                        seen.add(key); out.append({'b': b, 'q': q, 'o': opts, 'a': 0, 'why': why, 'sk': skn})
    return out
if __name__ == '__main__':
    import collections
    for t in ALL:
        g = gen(t); print(t, len(g), dict(collections.Counter(q['b'] for q in g)))
