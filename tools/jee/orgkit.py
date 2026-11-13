"""Tiny organic toolkit (no RDKit here): a SMILES-lite parser (C N O S F Cl Br I, branches, ring digits, = and #,
lowercase c for aromatic carbon), Weisfeiler–Lehman atom classes for 'different environments', chiral centres,
geometrical double bonds, stereoisomer counts (with the meso case of two equivalent centres), alkane isomer counts
by building carbon trees, and benzene substitution patterns under the hexagon's symmetry."""
import re, itertools
VAL = {'C': 4, 'c': 4, 'N': 3, 'O': 2, 'S': 2, 'F': 1, 'Cl': 1, 'Br': 1, 'I': 1}
def parse(smi):
    """returns (atoms, bonds) — atoms: list of element symbols; bonds: dict (i, j) → order (aromatic c–c = 1.5)"""
    atoms, bonds, stack, ring, prev, order = [], {}, [], {}, None, 1
    toks = re.findall(r'Cl|Br|[CNOSFIc]|\(|\)|=|#|\d', smi)
    for t in toks:
        if t == '(': stack.append(prev)
        elif t == ')': prev = stack.pop()
        elif t in '=#': order = 2 if t == '=' else 3
        elif t.isdigit():
            if t in ring:
                j, o = ring.pop(t); o = max(o, order); i = prev
                if atoms[i] == 'c' and atoms[j] == 'c' and o == 1: o = 1.5
                bonds[(min(i, j), max(i, j))] = o
            else: ring[t] = (prev, order)
            order = 1
        else:
            atoms.append(t); i = len(atoms) - 1
            if prev is not None:
                o = order
                if atoms[prev] == 'c' and t == 'c' and o == 1: o = 1.5
                bonds[(min(prev, i), max(prev, i))] = o
            prev = i; order = 1
    return atoms, bonds
class Mol:
    def __init__(self, smi):
        self.smi = smi; self.a, self.b = parse(smi); n = len(self.a)
        self.nb = [[] for _ in range(n)]
        for (i, j), o in self.b.items(): self.nb[i].append((j, o)); self.nb[j].append((i, o))
        self.h = [max(0, round(VAL[e] - sum(o for _, o in self.nb[i]))) for i, e in enumerate(self.a)]
    def wl(self, rounds=8):
        col = [f'{e}{h}' for e, h in zip(self.a, self.h)]
        for _ in range(rounds):
            new = [col[i] + '|' + ','.join(sorted(f'{o}{col[j]}' for j, o in self.nb[i])) for i in range(len(col))]
            m = {s: k for k, s in enumerate(sorted(set(new)))}; col = [str(m[s]) for s in new]
        return col
    def branch(self, root, frm, depth=10):
        """signature of the branch starting at root, coming from frm (rooted tree unfolding, depth-limited)"""
        def go(i, p, d):
            if d == 0: return self.a[i]
            kids = sorted(f'{o}{go(j, i, d - 1)}' for j, o in self.nb[i] if j != p)
            return f'{self.a[i]}{self.h[i]}(' + ','.join(kids) + ')'
        return go(root, frm, depth)
    def chiral(self):
        out = []
        for i, e in enumerate(self.a):
            if e != 'C' or any(o != 1 for _, o in self.nb[i]) or len(self.nb[i]) + self.h[i] != 4 or self.h[i] > 1: continue
            subs = [self.branch(j, i) for j, _ in self.nb[i]] + ['H'] * self.h[i]
            if len(set(subs)) == 4: out.append(i)
        return out
    def geo_db(self):
        out = []
        for (i, j), o in self.b.items():
            if o != 2 or self.a[i] != 'C' or self.a[j] != 'C': continue
            if any(p == j for p in ()) : pass
            ok = True
            for x, y in ((i, j), (j, i)):
                subs = [self.branch(k, x) for k, _ in self.nb[x] if k != y] + ['H'] * self.h[x]
                if len(subs) != 2 or subs[0] == subs[1]: ok = False
            if ok and not self._in_small_ring(i, j): out.append((i, j))
        return out
    def _in_small_ring(self, i, j, maxn=7):   # double bond inside a ring of < 8 atoms: no trans possible
        seen = {i: 0}; fr = [i]
        for d in range(1, maxn):
            nx = []
            for u in fr:
                for v, _ in self.nb[u]:
                    if (u, v) in ((i, j),): continue
                    if v == j and d > 1: return True
                    if v not in seen: seen[v] = d; nx.append(v)
            fr = nx
        return False
    def stereo_count(self):
        c = self.chiral(); g = self.geo_db(); n = len(c) + len(g); tot = 2 ** n
        if len(c) == 2 and not g:
            w = self.wl()
            if w[c[0]] == w[c[1]]: tot = 3   # RR, SS and meso
        return tot
    def optically_active(self):
        c = self.chiral()
        if not c: return 0
        if len(c) == 2 and not self.geo_db() and self.wl()[c[0]] == self.wl()[c[1]]: return 2
        return 2 ** len(c) * 2 ** len(self.geo_db())
    def h_classes(self, el='C'):   # distinct environments of H-bearing atoms of element el
        w = self.wl(); return len({w[i] for i, e in enumerate(self.a) if e == el and self.h[i] > 0})
    def substitute(self, X='Cl'):
        """all distinct products of replacing one H on a carbon by X (structural): list of SMILES-lite Mol objects"""
        w = self.wl(); seen, out = set(), []
        for i, e in enumerate(self.a):
            if e not in ('C', 'c') or self.h[i] == 0 or w[i] in seen: continue
            seen.add(w[i]); out.append(_add(self, i, X))
        return out
def _add(m, i, X):
    n = Mol.__new__(Mol); n.smi = m.smi + f'+{X}@{i}'; n.a = m.a + [X]; k = len(m.a); n.b = dict(m.b); n.b[(i, k)] = 1
    n.nb = [list(x) for x in m.nb] + [[(i, 1)]]; n.nb[i].append((k, 1)); n.h = list(m.h) + [0]; n.h[i] -= 1; return n
def canon(m):   # canonical string of a whole molecule (WL multiset) — good enough to tell small isomers apart
    return ','.join(sorted(f'{e}{c}' for e, c in zip(m.a, m.wl())))
# ---- alkane isomers by growing carbon trees
def alkanes(n):
    def code(adj, r, p):
        return '(' + ''.join(sorted(code(adj, c, r) for c in adj[r] if c != p)) + ')'
    def canon_tree(adj):
        return min(code(adj, r, -1) for r in range(len(adj)))
    level = {canon_tree([[]]): [[]]}
    for k in range(1, n):
        nxt = {}
        for adj in level.values():
            for i in range(len(adj)):
                if len(adj[i]) >= 4: continue
                new = [list(x) for x in adj] + [[i]]; new[i].append(len(adj)); nxt.setdefault(canon_tree(new), new)
        level = nxt
    return len(level)
# ---- substituted benzenes: ring positions 0..5, symmetry D6
D6 = [[(k + s) % 6 for k in range(6)] for s in range(6)] + [[(s - k) % 6 for k in range(6)] for s in range(6)]
def ring_patterns(subs):
    """subs: list of substituent labels (multiset) → distinct arrangements on benzene"""
    seen = set()
    for pos in itertools.permutations(range(6), len(subs)):
        lab = ['H'] * 6
        for p, s in zip(pos, subs): lab[p] = s
        seen.add(min(tuple(lab[g.index(i)] for i in range(6)) for g in D6))
    return sorted(seen)
def ring_h_sites(pattern):
    """number of distinct ring C–H environments of one arrangement (orbits of the pattern's own symmetry)"""
    stab = [g for g in D6 if all(pattern[g[i]] == pattern[i] for i in range(6))]
    orb = set()
    for i in range(6):
        if pattern[i] == 'H': orb.add(min(g[i] for g in stab))
    return len(orb)
