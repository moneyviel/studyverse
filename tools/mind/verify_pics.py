"""Second, independent check of content/mind/pics.json (does not reuse the generator's answer code)."""
import json, itertools, os
d = json.load(open(os.path.join(os.path.dirname(__file__), '../../content/mind/pics.json')))
bad = 0
def fail(q, m):
    global bad; bad += 1; print('FAIL', q['id'], m)
# dice: brute-force every labelled cube against both views
F = 'U D F B L R'.split(); opp = dict(U='D', D='U', F='B', B='F', L='R', R='L')
def rots():
    tx = lambda c: dict(U=c['F'], F=c['D'], D=c['B'], B=c['U'], L=c['L'], R=c['R'])
    ty = lambda c: dict(U=c['U'], D=c['D'], F=c['R'], R=c['B'], B=c['L'], L=c['F'])
    seen, st = {}, [{f: f for f in F}]
    while st:
        c = st.pop(); k = tuple(c[f] for f in F)
        if k not in seen: seen[k] = c; st += [tx(c), ty(c)]
    return list(seen.values())
RT = rots(); assert len(RT) == 24
for q in d['questions']:
    a = q['o'][q['a']]; k = q['k']
    if len(set(json.dumps(o) for o in q['o'])) != len(q['o']): fail(q, 'repeated option')
    if k == 'dice':
        x = int(q['q'].split('opposite ')[1].rstrip('?'))
        views = [tuple(v) for v in q['views']]; ans = set()
        for p in itertools.permutations(range(1, 7)):
            die = dict(zip(F, p)); vs = {(die[r['U']], die[r['F']], die[r['R']]) for r in RT}
            if all(v in vs for v in views):
                f = [g for g in F if die[g] == x][0]; ans.add(die[opp[f]])
        if ans != {int(a)}: fail(q, 'dice %s vs %s' % (ans, a))
    if k == 'paper':
        hs = {tuple(h) for h in q['holes']}
        for f in reversed(q['folds']):
            hs |= {(r, 3 - c) if f == 'v' else (3 - r, c) if f == 'h' else (c, r) for r, c in hs}
        if sorted(hs) != sorted(map(tuple, a)): fail(q, 'paper')
    if k == 'count':
        if q['find'] == 'sq':
            w, h = q['grid']; n = sum((w - s + 1) * (h - s + 1) for s in range(1, min(w, h) + 1))
        elif q['find'] == 'rect':
            w, h = q['grid']; n = (w + 1) * w // 2 * (h + 1) * h // 2
        else:
            m, hl = q['fan']; n = m * (m + 1) // 2 * (hl + 1)
        if str(n) != a or len(q['items']) != n: fail(q, 'count %d vs %s' % (n, a))
    if k == 'matrix':
        g = q['grid']; mr, mc = [(r, c) for r in range(3) for c in range(3) if g[r][c] is None][0]
        row = [g[mr][c] for c in range(3) if c != mc]; col = [g[r][mc] for r in range(3) if r != mr]
        fits = [o for o in q['o'] if o['s'] not in [y['s'] for y in row + col] and o['c'] not in [y['c'] for y in row + col] and all(y['n'] == o['n'] for y in col)]
        if fits != [a]: fail(q, 'matrix')
    if k == 'symmetry':
        t = q['tile']; r0, c0 = q['hole']
        def sym(o):
            full = [row[:] for row in t]
            for r in range(3):
                for c in range(3): full[r0 + r][c0 + c] = o[r][c]
            return all(full[r][c] == full[r][5 - c] and full[r][c] == full[5 - r][c] for r in range(6) for c in range(6))
        if [o for o in q['o'] if sym(o)] != [a]: fail(q, 'symmetry')
print('checked', len(d['questions']), 'failures', bad)
