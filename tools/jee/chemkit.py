"""Shared helpers for the chemistry PYQ files: pick the option that matches a truth pattern for two-statement and
assertion–reason items, and pick a letter set (e.g. 'ACD') from options like 'A, C and D only'."""
import re
from common import pick
def _norm(o):
    o = o.lower().replace('correct', 'true').replace('incorrect', 'false').replace('intrue', 'false').replace('in true', 'false')
    return o
def stmt(a, b, opts):
    """two statements I, II with truth a, b"""
    hits = []
    for i, o in enumerate(opts):
        lo = _norm(o)
        if lo.startswith('both'):
            v = 'false' not in lo; ok = (a and b) if v else (not a and not b)
        else:
            m = re.search(r'(i|a)\b[^,]*?\b(true|false)\b.*\b(ii|r)\b[^,]*?\b(true|false)\b', lo)
            if not m: continue
            ok = ((m.group(2) == 'true') == a) and ((m.group(4) == 'true') == b)
        if ok: hits.append(i + 1)
    assert len(hits) == 1, (a, b, opts, hits); return hits[0]
def ar(a, r, explains, opts):
    """assertion (A) / reason (R)"""
    hits = []
    for i, o in enumerate(opts):
        lo = _norm(o)
        if lo.startswith('both'):
            if not (a and r): continue
            neg = ' not ' in lo or 'not the' in lo
            if neg != explains: hits.append(i + 1)
        else:
            m = re.search(r'\(?a\)?\s*is\s*(true|false).*\(?r\)?\s*is\s*(true|false)', lo)
            if m and ((m.group(1) == 'true') == a) and ((m.group(2) == 'true') == r): hits.append(i + 1)
    assert len(hits) == 1, (a, r, explains, opts, hits); return hits[0]
def letters(opts):
    return [''.join(re.findall(r'\b([A-E])\b', o.split('only')[0].split('Only')[0])) for o in opts]
def pickset(opts, truth):
    """truth: dict letter -> bool; returns the option listing exactly the true letters"""
    want = ''.join(k for k in sorted(truth) if truth[k]); return pick(letters(opts), want)
