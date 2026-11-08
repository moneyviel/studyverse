"""Paper 3 Ch 12 — Blood Relations: extra MCQ templates.
A random family tree is built; statements are read off the tree; the asked relation is named from the tree.
Conventions (stated in every explanation): brothers/sisters share both parents; a parent's spouse is a parent
(no step-relations)."""
from common import *
import itertools

U = 'fnd-p3-ch12-u01'
C1, C2, C3, C4, C5, C6 = 'What is a blood relation?', 'Paternal and maternal side', 'Key relation words', 'Drawing the family tree', 'Pointing, photograph and introduction statements', 'Coded relations'
G = {'father': 'M', 'mother': 'F', 'son': 'M', 'daughter': 'F', 'brother': 'M', 'sister': 'F', 'husband': 'M', 'wife': 'F'}


class Person:
    def __init__(s, name, g): s.name, s.g, s.parents, s.spouse = name, g, [], None


def world(r, letters):
    it = iter(letters); ppl = []
    def new(g):
        p = Person(next(it), g); ppl.append(p); return p
    gf, gm = new('M'), new('F'); gf.spouse, gm.spouse = gm, gf
    for _ in range(r.randint(2, 3)):
        c = new(r.choice('MF')); c.parents = [gf, gm]
        sp = new('F' if c.g == 'M' else 'M'); c.spouse, sp.spouse = sp, c
        for _ in range(r.randint(1, 2)):
            k = new(r.choice('MF')); k.parents = [c, sp]
    return ppl


def par(p): return p.parents
def kids(p, ppl): return [q for q in ppl if p in q.parents]
def sibs(p, ppl): return [q for q in ppl if q is not p and q.parents and q.parents == p.parents]


def relname(x, y, ppl):
    """name of x's relation to y (x is y's ___) or None"""
    gx = x.g; pick = lambda m, f: m if gx == 'M' else f
    if y.spouse is x: return pick('husband', 'wife')
    if x in par(y): return pick('father', 'mother')
    if y in par(x): return pick('son', 'daughter')
    if x in sibs(y, ppl): return pick('brother', 'sister')
    if any(x in par(p) for p in par(y)): return pick('grandfather', 'grandmother')
    if any(y in par(p) for p in par(x)): return pick('grandson', 'granddaughter')
    if any(x in sibs(p, ppl) or (x.spouse and x.spouse in sibs(p, ppl)) for p in par(y)): return pick('uncle', 'aunt')
    if any(p in sibs(y, ppl) or (y.spouse and p in sibs(y.spouse, ppl)) for p in par(x)): return pick('nephew', 'niece')
    if any(p in sibs(q, ppl) for p in par(x) for q in par(y)): return 'cousin'
    if y.spouse and x in par(y.spouse): return pick('father-in-law', 'mother-in-law')
    if x.spouse and y in par(x.spouse): return pick('son-in-law', 'daughter-in-law')
    if (y.spouse and x in sibs(y.spouse, ppl)) or (x.spouse and x.spouse in sibs(y, ppl)): return pick('brother-in-law', 'sister-in-law')
    return None


def direct(u, v, ppl):
    n = relname(u, v, ppl)
    return n if n in G else None


DIST = {'father': ['uncle', 'grandfather', 'brother', 'father-in-law'], 'mother': ['aunt', 'grandmother', 'sister', 'mother-in-law'], 'son': ['nephew', 'grandson', 'brother', 'son-in-law'],
        'daughter': ['niece', 'granddaughter', 'sister', 'daughter-in-law'], 'brother': ['cousin', 'brother-in-law', 'son', 'uncle'], 'sister': ['cousin', 'sister-in-law', 'daughter', 'aunt'],
        'husband': ['brother-in-law', 'son-in-law', 'brother', 'father'], 'wife': ['sister-in-law', 'daughter-in-law', 'sister', 'mother'], 'grandfather': ['father', 'uncle', 'father-in-law', 'great-grandfather'],
        'grandmother': ['mother', 'aunt', 'mother-in-law', 'great-grandmother'], 'grandson': ['son', 'nephew', 'son-in-law', 'cousin'], 'granddaughter': ['daughter', 'niece', 'daughter-in-law', 'cousin'],
        'uncle': ['father', 'cousin', 'brother-in-law', 'grandfather'], 'aunt': ['mother', 'cousin', 'sister-in-law', 'grandmother'], 'nephew': ['son', 'cousin', 'grandson', 'brother'],
        'niece': ['daughter', 'cousin', 'granddaughter', 'sister'], 'cousin': ['brother', 'nephew', 'uncle', 'brother-in-law'], 'father-in-law': ['father', 'uncle', 'grandfather', 'brother-in-law'],
        'mother-in-law': ['mother', 'aunt', 'grandmother', 'sister-in-law'], 'son-in-law': ['son', 'nephew', 'brother-in-law', 'grandson'], 'daughter-in-law': ['daughter', 'niece', 'sister-in-law', 'granddaughter'],
        'brother-in-law': ['brother', 'cousin', 'son-in-law', 'uncle'], 'sister-in-law': ['sister', 'cousin', 'daughter-in-law', 'aunt']}
CAP = lambda s: s[0].upper() + s[1:]
CONV = 'Convention: brothers and sisters share both parents, and a parent\'s husband or wife is also a parent (no step-relations).'


def edges(p, ppl):
    out = list(par(p)) + kids(p, ppl) + sibs(p, ppl) + ([p.spouse] if p.spouse else [])
    return out


def chain_q(r):
    ppl = world(r, 'ABCDEFGHJKLMNPQRST')
    x = r.choice(ppl); L = r.choice([2, 3])
    path = [x]
    for _ in range(L):
        nx = [q for q in edges(path[-1], ppl) if q not in path]
        if not nx: return None
        path.append(r.choice(nx))
    y = path[-1]; ans = relname(x, y, ppl)
    if not ans or ans in G and L == 1: return None
    st = []
    for u, v in zip(path, path[1:]):
        d = direct(u, v, ppl)
        if not d: return None
        st.append(f'{u.name} is the {d} of {v.name}.')
    if len(set(direct(u, v, ppl) for u, v in zip(path, path[1:]))) == 1 and L == 2 and ans in G: return None
    steps = '; '.join(s[:-1] for s in st)
    return dict(q=' '.join(st) + f' How is {x.name} related to {y.name}?', a=CAP(ans), w=[CAP(w) for w in DIST[ans]],
                ex=f'Draw the tree one statement at a time ({steps}), marking males and females. Then trace from {y.name} back to {x.name}: {x.name} is {y.name}\'s {ans}. {CONV}',
                fast=f'Draw the tree with + for male and − for female; follow the chain from {y.name} to {x.name}.', secs=60, d='moderate', topic=C4, k='ch12.rel', data={'_t': 0})


PRON = {'M': ('a man', 'He'), 'F': ('a woman', 'She')}
SPK = {'M': ['Rahul', 'Amit', 'Karan', 'Vivek', 'Manoj'], 'F': ['Neha', 'Riya', 'Anita', 'Sunita', 'Priya']}
POSS = {'father': 'father', 'mother': 'mother', 'son': 'son', 'daughter': 'daughter', 'brother': 'brother', 'sister': 'sister', 'husband': 'husband', 'wife': 'wife'}


def matches(start, steps, ppl):
    """all persons reachable from start by the relation-word steps (set semantics)"""
    cur = {start}
    for w in steps:
        nxt = set()
        for p in cur:
            for q in ppl:
                if q is not p and direct(q, p, ppl) == w: nxt.add(q)
        cur = nxt
    return cur


def pointing(r):
    ppl = world(r, 'ABCDEFGHJKLMNPQRST')
    spk = r.choice(ppl); L = r.choice([2, 3]); steps = []; cur = spk; seen = [spk]
    for _ in range(L):
        nx = [q for q in edges(cur, ppl) if q not in seen]
        if not nx: return None
        q = r.choice(nx); steps.append(direct(q, cur, ppl)); seen.append(q); cur = q
    tgt = cur; ans = relname(tgt, spk, ppl)
    if not ans or None in steps: return None
    m = matches(spk, steps, ppl)
    if spk in m or len({relname(t, spk, ppl) for t in m}) != 1: return None     # description must not loop back to the speaker or be ambiguous
    who = r.choice(SPK[spk.g]); kind, pr = PRON[tgt.g]
    # sentence: "He is the <last> of my <first>'s <second>…"
    inner = 'my ' + "'s ".join(steps[:-1])
    sent = f'{pr} is the {steps[-1]} of {inner}.'
    return dict(q=f'Pointing to {kind} in a photograph, {who} said, "{sent}" How is that {"man" if tgt.g == "M" else "woman"} related to {who}?', a=CAP(ans), w=[CAP(w) for w in DIST[ans]],
                ex=f'Start from the speaker ("my") and move one word at a time: ' + ' → '.join(f'{w}' for w in steps) + f'. Following these links on a small family tree lands on {ans}, so the person in the photograph is {who}\'s {ans}. {CONV}',
                fast='Read the possessive chain from "my" outward and simplify two words at a time (father\'s wife = mother, mother\'s brother = uncle …).', secs=50, d='moderate', topic=C5, k='ch12.point', data={'_t': 0})


SYM = ['+', '−', '×', '÷', '@', '#', '$', '%']


def coded(r):
    ppl = world(r, 'ABCDEFGHJKLMNPQRST')
    words = r.sample(list(G), 4); syms = r.sample(SYM, 4); code = dict(zip(words, syms))
    x = r.choice(ppl); path = [x]; used = []
    for _ in range(3):
        nx = [(q, direct(path[-1], q, ppl)) for q in edges(path[-1], ppl) if q not in path]
        nx = [(q, w) for q, w in nx if w in code]
        if not nx: return None
        q, w = r.choice(nx); path.append(q); used.append(w)
    names = r.sample('ABCDEFGHJK', 4)
    nm = {id(p): n for p, n in zip(path, names)}
    expr = names[0] + ''.join(f' {code[w]} {nm[id(q)]}' for w, q in zip(used, path[1:]))
    a_, b_ = (path[0], path[-1]) if r.random() < .5 else (path[-1], path[0])
    ans = relname(a_, b_, ppl)
    if not ans: return None
    if a_ is path[-1]: return None      # the last person's gender is not stated by the code
    defs = 'In a code, ' + '; '.join(f'X {code[w]} Y says "X is the {w} of Y"' for w in words)
    return dict(q=f'{defs}. If {expr}, how is {nm[id(a_)]} related to {nm[id(b_)]}?', a=CAP(ans), w=[CAP(w) for w in DIST[ans]],
                ex=f'Decode left to right: ' + '; '.join(f'{nm[id(p)]} is the {w} of {nm[id(q)]}' for p, w, q in zip(path, used, path[1:])) + f'. Drawing these links gives: {nm[id(a_)]} is {nm[id(b_)]}\'s {ans}. {CONV}',
                fast='Translate each symbol into words first, draw the three links, then read the asked relation.', secs=75, d='hard', topic=C6, k='ch12.code', data={'_t': 0})


def side_q(r):
    who = r.choice(['father', 'mother']); rel = r.choice(['brother', 'sister', 'father', 'mother'])
    name = {('father', 'brother'): 'paternal uncle', ('father', 'sister'): 'paternal aunt', ('father', 'father'): 'paternal grandfather', ('father', 'mother'): 'paternal grandmother',
            ('mother', 'brother'): 'maternal uncle', ('mother', 'sister'): 'maternal aunt', ('mother', 'father'): 'maternal grandfather', ('mother', 'mother'): 'maternal grandmother'}
    ans = name[(who, rel)]; other = 'mother' if who == 'father' else 'father'
    w = [name[(other, rel)], name[(who, {'brother': 'sister', 'sister': 'brother', 'father': 'mother', 'mother': 'father'}[rel])], name[(other, {'brother': 'sister', 'sister': 'brother', 'father': 'mother', 'mother': 'father'}[rel])]]
    return dict(q=f'Your {who}\'s {rel} is your:', a=CAP(ans), w=[CAP(x) for x in w],
                ex=f'Relatives on the father\'s side are "paternal" and on the mother\'s side "maternal". Your {who}\'s {rel} is on your {who}\'s side, so the relation is {ans}. The word after paternal/maternal follows the generation and gender: brother → uncle, sister → aunt, parents → grandparents.',
                fast='Father\'s side = paternal, mother\'s side = maternal; then name the relation by generation and gender.', secs=15, d='core', topic=C2, k='ch12.side', data={'_t': 0})


BANKS = {U: [(chain_q, 11), (pointing, 8), (coded, 6), (side_q, 3)]}
