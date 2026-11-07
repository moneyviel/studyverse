"""Offline 'viva' answer matcher — the Python twin of vivaScore() in js/ca-tools.js.
Both must give the same result; tools/ca_validate.py uses this one to prove that every model answer
covers 100% of its key points and that reading the question back does not.

Key point format (in a unit's "viva" block):
  {"id": "p1", "pt": "shown to the student", "w": 3, "kw": ["debit|dr", "credit|cr", "equal|same"], "min": 2}
  kw  = groups; a group is matched if ANY of its '|' alternatives (a word or a short phrase) is found
  min = how many groups must match for the point to count (default: all groups)
Matching: lower-case → abbreviations expanded (Dr→debit, A/c→account, ₹→rs, &→and, lakh/crore → digits)
→ stop-words dropped → light stemming. A phrase matches when its words appear in order, at most 2 other
words apart. Two words match when equal, when they share a long common stem (≥5 letters and ≥75% of the
shorter word) or, for words of 6+ letters, when they differ by one letter (typing / speech slips).
Numbers match within 0.5%.
"""
import re

STOP = set('a an the of is are was were be been being to in on at for with as that this it its by from or and which who whom will shall can may into than then so such also has have had do does did there their they he she his her them we our you your i me my am'.split())
ABBR = {'dr': 'debit', 'cr': 'credit', 'tb': 'trial balance', 'rs': 'rupees', 'inr': 'rupees', 'sec': 'section', 'pl': 'profit loss',
        'amt': 'amount', 'gst': 'gst', 'itc': 'input tax credit', 'cd': 'cash discount', 'td': 'trade discount', 'bal': 'balance', 'jf': 'jf', 'lf': 'lf'}
SMALL = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
         'fifteen': 15, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'hundred': 100}
MULT = {'thousand': 1000, 'lakh': 100000, 'lakhs': 100000, 'lac': 100000, 'lacs': 100000, 'crore': 10000000, 'crores': 10000000}
SUFFIX = [('ational', 'ate'), ('ations', 'ate'), ('ation', 'ate'), ('ings', ''), ('ities', 'ity'), ('ies', 'y'), ('ied', 'y'), ('ing', ''), ('edly', ''), ('ed', ''), ('ers', 'er'), ('es', ''), ('ly', ''), ('s', '')]


def stem(w):
    if len(w) <= 3 or w[0].isdigit(): return w
    for suf, rep in SUFFIX:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            if suf == 's' and w.endswith('ss'): break
            if suf == 'es' and not re.search(r'(ss|sh|ch|x|z)es$', w): continue
            w = w[:-len(suf)] + rep; break
    if len(w) > 3 and w[-1] == w[-2] and w[-1] not in 'lsz' and not w[-1].isdigit(): w = w[:-1]
    if w.endswith('e') and len(w) > 4: w = w[:-1]
    return w


def _fmtnum(v):
    v = round(v, 4)
    return str(int(v)) if v == int(v) else str(v)


def tokens(text):
    t = str(text).lower()
    t = t.replace('₹', ' rs ').replace('&', ' and ').replace('%', ' percent ')
    t = re.sub(r'\ba/c\b|\ba/cs\b', ' account ', t)
    t = re.sub(r'\bu/s\b|\bs\.\s*(?=\d)', ' section ', t)
    t = re.sub(r'(?<=\d),(?=\d)', '', t)
    t = re.sub(r'[^a-z0-9.\s]', ' ', t)
    t = re.sub(r'(?<!\d)\.|\.(?!\d)', ' ', t)
    raw = t.split()
    out = []
    i = 0
    while i < len(raw):
        w = raw[i]
        num = None
        if re.fullmatch(r'\d+(\.\d+)?', w): num = float(w)
        elif w in SMALL: num = float(SMALL[w])
        if num is not None and i + 1 < len(raw) and raw[i + 1] in MULT:
            num *= MULT[raw[i + 1]]; i += 1
        if num is not None:
            out.append(_fmtnum(num)); i += 1; continue
        if w in MULT: out.append(_fmtnum(MULT[w])); i += 1; continue
        if w in ABBR: out.extend(stem(x) for x in ABBR[w].split()); i += 1; continue
        if w not in STOP: out.append(stem(w))
        i += 1
    return [x for x in out if x not in STOP]


def _isnum(w): return bool(re.fullmatch(r'\d+(\.\d+)?', w))


def _lev1(a, b):
    if abs(len(a) - len(b)) > 1: return False
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) <= 1
    if len(a) > len(b): a, b = b, a
    i = 0
    while i < len(a) and a[i] == b[i]: i += 1
    return a[i:] == b[i + 1:]


def same(a, b):
    if a == b: return True
    if _isnum(a) or _isnum(b):
        if _isnum(a) and _isnum(b):
            x, y = float(a), float(b)
            return abs(x - y) <= max(abs(y) * 0.005, 0.01)
        return False
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]: n += 1
    if n >= 5 and n >= 0.75 * min(len(a), len(b)): return True
    return min(len(a), len(b)) >= 6 and _lev1(a, b)


def phrase_in(ph, toks):
    if not ph: return False
    for s in range(len(toks)):
        if not same(ph[0], toks[s]): continue
        j, ok = s, True
        for w in ph[1:]:
            k = next((k for k in range(j + 1, min(len(toks), j + 4)) if same(w, toks[k])), None)
            if k is None: ok = False; break
            j = k
        if ok: return True
    return False


def point_hit(p, toks):
    groups = p['kw']
    got = sum(1 for g in groups if any(phrase_in(tokens(alt), toks) for alt in g.split('|') if alt.strip()))
    return got >= p.get('min', len(groups))


def score(viva_q, answer):
    toks = tokens(answer)
    tot = sum(p['w'] for p in viva_q['points'])
    hit = [p['id'] for p in viva_q['points'] if point_hit(p, toks)]
    got = sum(p['w'] for p in viva_q['points'] if p['id'] in hit)
    return (round(got / tot * 100) if tot else 0), hit


if __name__ == '__main__':
    import sys
    print(tokens(' '.join(sys.argv[1:]) or 'Rs 1.5 lakh debited to Purchases A/c; posting balances'))
