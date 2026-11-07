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
Negation: a keyword hit does not count when a negator (not, no, never, cannot, neither, nor, without, n't, नहीं …) stands
within the 3 words before any of its matched words in the same clause (clauses end at . , ; : ! ? or a new line) —
unless the keyword phrase itself contains a negator ("not recorded", "not every"), which then simply has to be present.
Negators are checked on the raw word ("noting" is not "not"); "not less / more / only / just …" is not a negation.
A phrase must match inside one sentence (. ; ! ? new line) and may cross at most two commas or colons (asides like ", which …,"). 'then' is kept as a word (for phrases like "then loan") but does not count in gaps.
CA party words (drawee, payee, bailee, guarantee …) are not stemmed; one-letter typo tolerance needs the same first letter
(so paternal ≠ maternal); a keyword written as a stem ("balanc") matches the stemmed answer word too.
"""
import re

STOP = set('a an the of is are was were be been being to in on at for with as that this it its by from or and which who whom will shall can may into than so such also has have had do does did there their they he she his her them we our you your i me my am'.split())
ABBR = {'dr': 'debit', 'cr': 'credit', 'tb': 'trial balance', 'rs': 'rupees', 'inr': 'rupees', 'sec': 'section', 'pl': 'profit loss',
        'amt': 'amount', 'gst': 'gst', 'itc': 'input tax credit', 'cd': 'cash discount', 'td': 'trade discount', 'bal': 'balance', 'jf': 'jf', 'lf': 'lf'}
SMALL = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
         'fifteen': 15, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'hundred': 100}
MULT = {'thousand': 1000, 'lakh': 100000, 'lakhs': 100000, 'lac': 100000, 'lacs': 100000, 'crore': 10000000, 'crores': 10000000}
PROTECT = set('drawee drawer payee bailee bailor lessee lessor mortgagee mortgagor guarantee guarantor'.split())   # CA terms never stemmed
ORDER = {'then'}   # order word kept as a token; inside a phrase gap it does not count as a word
SUFFIX = [('ational', 'ate'), ('ations', 'ate'), ('ation', 'ate'), ('ings', ''), ('ities', 'ity'), ('ies', 'y'), ('ied', 'y'), ('ing', ''), ('edly', ''), ('ed', ''), ('ers', 'er'), ('es', ''), ('ly', ''), ('s', '')]


def stem(w):
    if len(w) <= 3 or w[0].isdigit(): return w
    if w in PROTECT: return w
    if w.endswith('s') and w[:-1] in PROTECT: return w[:-1]
    for suf, rep in SUFFIX:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            if suf == 'ed' and w.endswith('eed'): break        # exceed, proceed: not a past tense
            if suf == 's' and w.endswith('ss'): break
            if suf == 'es' and not re.search(r'(ss|sh|ch|x|z)es$', w): continue
            w = w[:-len(suf)] + rep; break
    if len(w) > 3 and w[-1] == w[-2] and w[-1] not in 'lsz' and not w[-1].isdigit(): w = w[:-1]
    if w.endswith('e') and len(w) > 4: w = w[:-1]
    return w


def _fmtnum(v):
    v = round(v, 4)
    return str(int(v)) if v == int(v) else str(v)


NEG = set('not no never cannot neither nor without cant dont doesnt isnt wont didnt arent wasnt shouldnt couldnt'.split())
NEGX = set('less more exceed exceeds exceeding later earlier only just merely fewer greater'.split())   # raw words   # "not less than 15 days", "not only … but also" are not negations


def pairs(text):
    """(raw word, stem) pairs after normalisation, stop-words removed"""
    t = str(text).lower()
    t = t.replace('नहीं', ' not ')
    t = re.sub(r"n['’]t\b", ' not', t)
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
            n = _fmtnum(num); out.append((n, n)); i += 1; continue
        if w in MULT: n = _fmtnum(MULT[w]); out.append((n, n)); i += 1; continue
        if w in ABBR: out.extend((x, stem(x)) for x in ABBR[w].split()); i += 1; continue
        if w not in STOP: out.append((w, stem(w)))
        i += 1
    return [x for x in out if x[1] not in STOP]


def tokens(text): return [x[1] for x in pairs(text)]


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
    if a in PROTECT or b in PROTECT: return False   # party words (drawee/drawer, lessee/lessor…) must match exactly
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]: n += 1
    if n >= 5 and n >= 0.75 * min(len(a), len(b)): return True
    return min(len(a), len(b)) >= 6 and a[0] == b[0] and _lev1(a, b)


def clauses(text):
    """stems, raw words, clause number (split at . , ; : ! ? new line) and sentence number (split at . ; ! ? new line)"""
    toks, raws, cl, sn = [], [], [], []
    c = 0
    for n, sent in enumerate(re.split(r'[;!?\n]|(?<!\d)\.|\.(?!\d)', str(text))):
        for part in re.split(r':|(?<!\d),|,(?!\d)', sent):
            for r, w in pairs(part): toks.append(w); raws.append(r); cl.append(c); sn.append(n)
            c += 1
    return toks, raws, (cl, sn)


def _negated(idx, raws, cs):
    cl = cs[0]
    for x in idx:
        for y in range(max(0, x - 3), x):
            if y not in idx and cl[y] == cl[x] and raws[y] in NEG and not (y + 1 < len(raws) and raws[y + 1] in NEGX): return True
    return False


def _kw(p, w):
    """keyword (raw, stem) against an answer stem; a keyword written as a stem ('balanc') also matches"""
    return same(p[1], w) or (p[0] != p[1] and same(p[0], w))


def phrase_in(ph, toks, raws=None, cl=None):
    """ph = keyword pairs. Words in order within one clause, at most 2 other words between them ('then' is free)."""
    if not ph: return False
    if ph and isinstance(ph[0], str): ph = [(w, w) for w in ph]
    check = raws is not None and not any(r in NEG for r, _ in ph)
    for s in range(len(toks)):
        if not _kw(ph[0], toks[s]): continue
        j, ok, idx = s, True, [s]
        for w in ph[1:]:
            k, cnt, x = None, 0, j + 1
            while x < len(toks) and cnt < 3:
                if cl is not None and (cl[1][x] != cl[1][s] or cl[0][x] - cl[0][s] > 2): break   # same sentence, at most two , or : crossed
                if _kw(w, toks[x]): k = x; break
                if toks[x] not in ORDER: cnt += 1
                x += 1
            if k is None: ok = False; break
            j = k; idx.append(k)
        if ok and not (check and _negated(idx, raws, cl)): return True
    return False


def point_hit(p, toks, raws=None, cl=None):
    groups = p['kw']
    got = sum(1 for g in groups if any(phrase_in(pairs(alt), toks, raws, cl) for alt in g.split('|') if alt.strip()))
    return got >= p.get('min', len(groups))


def score(viva_q, answer):
    toks, raws, cl = clauses(answer)
    tot = sum(p['w'] for p in viva_q['points'])
    hit = [p['id'] for p in viva_q['points'] if point_hit(p, toks, raws, cl)]
    got = sum(p['w'] for p in viva_q['points'] if p['id'] in hit)
    return (round(got / tot * 100) if tot else 0), hit


if __name__ == '__main__':
    import sys
    print(tokens(' '.join(sys.argv[1:]) or 'Rs 1.5 lakh debited to Purchases A/c; posting balances'))
