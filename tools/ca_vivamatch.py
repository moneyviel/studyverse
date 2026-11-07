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
    if w in ('willing', 'willingly'): return 'willing'   # not 'will'
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
    t = re.sub(r'(?<=\d),(?=\d{2,3}(?!\d))', '', t)   # 4,20,000 / 420,000 are one number; (4,2) is two
    t = re.sub(r'(?<![a-z0-9.])[\u2212\-](?=\d)', ' minus ', t)   # −7 / -7 keep their sign (10-15 is a range)
    t = re.sub(r'[^a-z0-9.\s]', ' ', t)
    t = re.sub(r'(?<!\d)\.|\.(?!\d)', ' ', t)
    raw = t.split()
    out = []
    i = 0
    while i < len(raw):
        w = raw[i]
        num = None
        if w == 'minus' and i + 1 < len(raw) and (re.fullmatch(r'\d+(\.\d+)?', raw[i + 1]) or raw[i + 1] in SMALL): i += 1; num = -float(SMALL[raw[i]] if raw[i] in SMALL else raw[i])
        elif re.fullmatch(r'\d+(\.\d+)?', w): num = float(w)
        elif w in SMALL: num = float(SMALL[w])
        if num is not None and i + 1 < len(raw) and raw[i + 1] in MULT:
            num *= MULT[raw[i + 1]]; i += 1
        if num is not None:
            n = _fmtnum(num); out.append((n, n)); i += 1; continue
        if w in MULT: n = _fmtnum(MULT[w]); out.append((n, n)); i += 1; continue
        if w in ABBR: out.extend((x, stem(x)) for x in ABBR[w].split()); i += 1; continue
        if w == 'as' and i + 1 < len(raw) and re.fullmatch(r'\d+(\.\d+)?', raw[i + 1]): out.append(('as', 'astd')); i += 1; continue   # AS 10 (Accounting Standard)
        if w not in STOP: out.append((w, stem(w)))
        i += 1
    return [x for x in out if x[1] not in STOP]


def tokens(text): return [x[1] for x in pairs(text)]


def _isnum(w): return bool(re.fullmatch(r'-?\d+(\.\d+)?', w))


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
            return abs(x - y) <= max(abs(y) * (0.005 if '.' in a or '.' in b else 0.0005), 0.01)   # 0.05%; 0.5% when decimals are written
        return False
    if a in PROTECT or b in PROTECT: return False   # party words (drawee/drawer, lessee/lessor…) must match exactly
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]: n += 1
    if n >= 5 and n >= 0.75 * min(len(a), len(b)): return True
    return min(len(a), len(b)) >= 6 and a[0] == b[0] and _lev1(a, b)


def clauses(text):
    """stems, raw words, clause number (split at . , ; : ! ? new line) and sentence number (split at . ; ! ? new line);
    a dot after sec / no / viz / cf / rs / e.g. / i.e. and a colon between digits (ratios) are not breaks"""
    toks, raws, cl, sn, nc = [], [], [], [], []
    c = k = 0
    text = re.sub(r'(?<![a-z])no\.(?=\s*\d)', 'number ', str(text), flags=re.I)   # 'No. 5' is a number, not a negator
    text = re.sub(r'(?<![a-z])(sec|viz|cf|rs)\.', r'\1 ', text, flags=re.I)   # 'Sec. 37', 'No.', 'viz.' are not sentence ends
    text = re.sub(r'(?<![a-z])e\.g\.', 'eg ', text, flags=re.I); text = re.sub(r'(?<![a-z])i\.e\.', 'ie ', text, flags=re.I)
    for n, sent in enumerate(re.split(r'[;!?\n]|(?<!\d)\.|\.(?!\d)', text)):
        for part in re.split(r'(?<!\d):|:(?!\d)|(?<!\d),|,(?!\d)', sent):   # 5:4:3 is a ratio, not a clause break
            for piece in re.split(r'[\u2014\u2013()\[\]]|\s-\s', part):   # dashes and brackets end a negation window
                for r, w in pairs(piece): toks.append(w); raws.append(r); cl.append(c); sn.append(n); nc.append(k)
                k += 1
            c += 1
    return toks, raws, (cl, sn, nc)


def _negated(idx, raws, cs):
    cl = cs[2] if len(cs) > 2 else cs[0]
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



# ===================== Written-answer checker — the Python twin of the checker core in js/ca-check.js =====================
# check_answer(question, answer) marks every scheme point of a unit question offline:
#   kw/min  keyword groups (same matcher as the viva), nums  figures found in the text or in table cells
#   (Indian / international digit grouping, "1.5 lakh", ±0.5), rows  expected table lines [account keywords, side, amount]
#   matched against the student's tables (journal, ledger, trial balance, BRS, statements) or typed "… Dr 5,000 / To … 5,000" lines.
# Award rule per point: every component present (kw, nums, rows) scores 1, ½ or 0 —
#   kw    1 if ≥ min groups hit; ½ if min ≥ 2 and at least half of min hit
#   nums  1 if every figure found; ½ if 2+ figures and at least half found
#   rows  each expected line: 1 (account + side + amount), ½ (account + amount, wrong side — or account + side, wrong amount), 0;
#         component 1 if all lines 1, ½ if their average ≥ ½
#   point = 1 if all components 1, 0 if all 0, otherwise ½;  a triggered `wrong` statement caps the point at ½.
# Points with ai_only, or with none of kw/nums/rows, are "pending" (left for the AI examiners) and excluded from the offline total.
# Extras (table rows / sentences that match nothing in the model) are listed but never deducted.
import math

SIDEW = {'dr': 'debited', 'cr': 'credited', 'add': 'added', 'less': 'deducted', '': 'shown'}
_RE_NUM = re.compile(r'([0-9]+(?:,[0-9]{2,3}(?![0-9]))*)(\.[0-9]+)?(\s*(?:lakhs?|lacs?|crores?)(?![a-z]))?', re.I)
_RE_AMT = re.compile(r'[0-9]+(?:,[0-9]{2,3}(?![0-9]))*(?:\.[0-9]+)?')
_RE_NEG = re.compile(r'(?:^|[^a-z0-9.])[\u2212\-](?:₹|rs\.?\s*)?$|(?:^|[^a-z])minus\s*(?:₹|rs\.?)?\s*$', re.I)   # '−7', '−₹30', 'minus 7' (not 'n − 96')
_RE_BRO = re.compile(r'\(\s*(?:₹|rs\.?)?\s*$', re.I)
_MON = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?'
_RE_DATE = re.compile(r'^(?:[0-9]{1,2}[-/. ]' + _MON + r'(?:[-/.][0-9a-z]{2,4}| [0-9]{2,4})?|' + _MON + r' [0-9]{1,2}(?![0-9,])|[0-9]{1,2}[-/.][0-9]{1,2}[-/.][0-9]{2,4}|\([0-9a-z]{1,4}\)|[0-9]{1,2}[.)](?![0-9]))\s*', re.I)
_RE_SENT = re.compile(r'[;!?\n]|(?<![0-9])\.|\.(?![0-9])')
_RE_SEC = re.compile(r'^(add|less)(?![a-z])\s*:?\s*(.*)$', re.I)
_RE_PART = re.compile(r'particular|account|name|basis|ledger|supplier|customer|party|drawer|item|head', re.I)
STD_SIDES = ('dr', 'cr', 'add', 'less', '')
PENDING_AI = 'Will be checked by AI examiners (coming soon)'
PENDING_NOKEY = 'Not auto-checkable yet — will be checked by AI examiners (coming soon)'
WAITING_PHOTO = 'Photo answer — waiting for AI examiners'


def r2(x): return math.floor(x * 100 + 0.5) / 100


def near(x, n):
    """figures agree (sign included): within 0.5 but at most 0.5% of the figure for small ones (52.5 is not 53; 1.3801 is 1.38), and within 0.05% for large ones"""
    return abs(x - n) <= max(min(0.5, max(abs(n) * 0.005, 0.01)), abs(n) * 0.0005)


def fmt_n(v):
    """Indian digit grouping, up to 4 decimals: 150000 -> 1,50,000; 1.38010 -> 1.3801"""
    v = math.floor(abs(v) * 10000 + 0.5) / 10000
    ip = int(math.floor(v)); fr = v - ip
    s = str(ip)
    if len(s) > 3:
        head, parts = s[:-3], []
        while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ','.join(parts + [s[-3:]])
    if fr > 1e-9:
        d = ('%.4f' % fr)[1:].rstrip('0')
        if d != '.': s += d
    return s


def _str(x): return '' if x is None else (x if isinstance(x, str) else (str(int(x)) if isinstance(x, float) and x == int(x) else str(x)))


def nums_in(text, cells=False):
    """signed figures: −7 / -7 / minus 7 are negative; (30) counts as 30 and −30 (accounting brackets);
    '₹5,690 crore' gives 5690 and 56,90,00,00,000 (either may be listed in nums)"""
    out = []; t = str(text or '')
    for m in _RE_NUM.finditer(t):
        v = float(m.group(1).replace(',', '') + (m.group(2) or ''))
        pre = t[max(0, m.start() - 8):m.start()]
        neg = bool(_RE_NEG.search(pre)); br = not neg and bool(_RE_BRO.search(pre)) and t[m.end():m.end() + 1] == ')'
        u = (m.group(3) or '').strip().lower()
        vals = [v, v * (10000000 if u.startswith('cr') else 100000)] if u else [v]
        for x in vals:
            out.append(-x if neg else x)
            if br or (cells and neg): out.append(-x if br else x)   # in table cells a minus (or brackets) is presentation: both signs count
    return out


def cell_amt(x):
    if isinstance(x, bool): return None
    if isinstance(x, (int, float)): return abs(float(x))
    t = _str(x).strip().lower().replace('₹', '').replace(' ', '').replace('−', '-')
    t = re.sub(r'^\(|\)$', '', t)
    t = re.sub(r'^-', '', t)
    t = re.sub(r'^(rs\.?|inr)', '', t)
    t = re.sub(r'(dr|cr)\.?$', '', t)
    t = re.sub(r'^\(|\)$', '', t)
    if re.fullmatch(r'[0-9]+(,[0-9]{2,3})*(\.[0-9]+)?', t): return float(t.replace(',', ''))
    return None


def clean_ac(s):
    s = re.sub(r'\s+', ' ', _str(s)).strip()
    s = re.sub(r'^(?:to|by)\s+', '', s, flags=re.I)
    s = re.sub(r'(?:^|\s)(?:dr|cr)\.?\s*$', '', s, flags=re.I)
    s = re.sub(r'^[(\s]+|[)\s]+$', '', s) if s.startswith('(') and s.endswith(')') else s
    return s.strip()


def ac_toks(s): return [w for w in tokens(s) if w != 'account']


def _title(s):
    alt = _str(s).split('|')[0].strip()
    return ' '.join(w[:1].upper() + w[1:] for w in alt.split())


def ac_match(acc, rt, ct=None):
    """acc = account keywords ('lakshmi agencies|supplier|creditor'); rt = row stems; ct = stems of the sheet's account (ledger name)"""
    if not _str(acc).strip(): return True
    for alt in _str(acc).split('|'):
        ps = [p for p in pairs(alt) if p[1] != 'account']
        if not ps: continue
        if all(any(_kw(p, w) for w in rt) for p in ps): return True
        if ct and len(ps) >= 2 and any(any(_kw(p, w) for w in rt) for p in ps) and all(any(_kw(p, w) for w in rt + ct) for p in ps): return True
    return False


def sheets_of(table):
    if not table or not isinstance(table, dict): return []
    if table.get('sheets') is not None:
        out = []
        for s in table['sheets']:
            if isinstance(s, dict) and s.get('flat'):
                d = dict(s['flat']); d['name'] = s.get('name') or s.get('tpl') or 'Table'; d['title'] = _str(s.get('title')); d['ok'] = isinstance(s.get('check'), dict) and s['check'].get('ok') is True; out.append(d)
        return out
    if table.get('cols') is not None: return [{'cols': table.get('cols') or [], 'rows': table.get('rows') or [], 'name': 'Table'}]
    return []


def sheet_kind(s):
    if s.get('kind'): return s['kind']
    cols = [_str(c) for c in s.get('cols') or []]
    if len(cols) == 5 and cols[0] == 'Date' and cols[1] == 'Particulars' and 'Dr' in cols[3]: return 'journal'
    if 'account' in s: return 'tacc'
    return 'grid'


def _side_of(h):
    if re.search(r'(^|[^a-z])(dr|debit)(?![a-z])', h, re.I): return 'dr'
    if re.search(r'(^|[^a-z])(cr|credit)(?![a-z])', h, re.I): return 'cr'
    return ''


def _row(part, side, amt, ctx, src, col=''):
    ac = clean_ac(part)
    return {'ac': ac, 'side': side, 'amt': amt, 'ctx': _str(ctx), 'src': src, 'col': _str(col), 't': ac_toks(ac), 'ct': ac_toks(ctx) if ctx else []}


def rows_of_sheet(s):
    kind = sheet_kind(s); cols = [_str(c) for c in s.get('cols') or []]; rows = s.get('rows') or []
    ctx = _str(s.get('account')); out = []; n = len(cols)
    if kind == 'journal':
        for r in rows:
            r = list(r) + [''] * 5
            d, c = cell_amt(r[3]), cell_amt(r[4])
            if d is None and c is None: continue
            side, amt = ('dr', d) if d is not None else ('cr', c)
            if amt and clean_ac(r[1]): out.append(_row(r[1], side, amt, ctx, 'table', cols[3] if side == 'dr' and len(cols) > 3 else (cols[4] if len(cols) > 4 else '')))
        return out
    if kind == 'tacc':
        h = n // 2
        for k in (0, 1):
            cs = cols[k * h:(k + 1) * h]
            pi = next((i for i, c in enumerate(cs) if re.search(r'particular', c, re.I)), -1)
            if pi < 0: pi = next((i for i, c in enumerate(cs) if not re.search(r'date|₹|j\.?f|l\.?f', c, re.I)), 0)
            am = [i for i, c in enumerate(cs) if '₹' in c and i != pi]
            for r in rows:
                seg = (list(r) + [''] * n)[k * h:(k + 1) * h]
                for i in am:
                    v = cell_amt(seg[i])
                    if v and clean_ac(seg[pi]): out.append(_row(seg[pi], 'dr' if k == 0 else 'cr', v, ctx, 'table', cs[i]))
        return out
    pi = s.get('part')
    if pi is None: pi = next((i for i, c in enumerate(cols) if _RE_PART.search(c)), 0)
    am = s.get('amt')
    if am is None:
        am = [i for i, c in enumerate(cols) if '₹' in c and i != pi]
        if not am:
            for i in range(n):
                if i == pi: continue
                cells = [_str(r[i]).strip() if i < len(r) else '' for r in rows]
                filled = [x for x in cells if x]
                if filled and all(cell_amt(x) is not None for x in filled): am.append(i)
    # column segments: a text column after an amount column starts a new segment (two-sided statements:
    # Expenditure | ₹ | Income | ₹ or columnar capital accounts); each segment's amounts belong to its particulars column
    segs, cur, seen = [], [], False
    for i in range(n):
        if i not in am and seen: segs.append(cur); cur, seen = [], False
        cur.append(i)
        if i in am: seen = True
    if cur: segs.append(cur)
    pj = {}
    for sg in segs:
        tc = [j for j in sg if j not in am]
        pc = pi if pi in sg else next((j for j in tc if _RE_PART.search(cols[j])), tc[0] if tc else pi)
        for i in sg:
            if i in am: pj[i] = pc
    two = len(segs) == 2 and len(set(pj.values())) == 2; first = min(pj.values()) if pj else pi
    sec = ''
    for r in rows:
        r = list(r) + [''] * n
        p = _str(r[pi]).strip()
        m = _RE_SEC.match(p)
        if m: sec = m.group(1).lower(); p = m.group(2).strip()
        if not p and not m: sec = ''
        for i in am:
            v = cell_amt(r[i])
            if not v: continue
            part = p if pj[i] == pi else _str(r[pj[i]]).strip()
            if not part: continue
            sd = _side_of(cols[i] if i < n else '') or (('dr' if pj[i] == first else 'cr') if two else sec)
            out.append(_row(part, sd, v, ctx, 'table', cols[i] if i < n else ''))
    return out


def text_rows(text):
    out, sec, dr_seen = [], '', False
    for line in _str(text).split('\n'):
        L = re.sub(r'\s+', ' ', line).strip()
        if not L: continue
        m = _RE_SEC.match(L)
        if m: sec = m.group(1).lower(); L = m.group(2).strip()
        if not L: continue
        L = _RE_DATE.sub('', L, count=1)
        ns = list(_RE_AMT.finditer(L))
        if not ns: continue
        md = re.search(r'(?:^|[^a-z])(dr|cr)\.?(?![a-z])', L, re.I)
        if md:
            side = md.group(1).lower(); ac = L[:md.start(1)]
            after = [x for x in ns if x.start() >= md.end()]
            am = after[0] if after else ns[-1]
            if side == 'dr': dr_seen = True
        elif re.match(r'^by\s', L, re.I): side = 'cr'; ac = L[:ns[-1].start()]; am = ns[-1]
        elif re.match(r'^to\s', L, re.I): side = 'cr' if dr_seen else 'dr'; ac = L[:ns[-1].start()]; am = ns[-1]
        elif sec: side = sec; ac = L[:ns[-1].start()]; am = ns[-1]
        else: continue
        ac = re.sub(r'[\s₹:=\-–—]+$', '', ac)
        ac = re.sub(r'(?:^|\s)(?:rs\.?|inr)$', '', ac, flags=re.I)
        amt = float(am.group(0).replace(',', ''))
        if amt and clean_ac(ac): out.append(_row(ac, side, amt, '', 'text'))
    return out


def table_text(sheets):
    lines = []
    for s in sheets:
        cols = [_str(c) for c in s.get('cols') or []]; kind = sheet_kind(s)
        if _str(s.get('title')).strip(): lines.append(_str(s.get('title')).strip())
        if kind == 'grid' and any(c.strip() for c in cols): lines.append(', '.join(c for c in cols if c.strip()))
        for r in s.get('rows') or []:
            cells = [re.sub(r'^[\u2212\-](?=[0-9])', '', _str(x).strip()) for x in r]   # a minus in a statement cell is presentation
            if not any(cells): continue
            lines.append(', '.join(c for c in cells if c))
            if kind == 'grid' and len(cells) >= 3 and cells[0] and cell_amt(cells[0]) is None:
                for i in range(1, len(cells)):
                    if cells[i] and cell_amt(cells[i]) is None and i < len(cols) and cols[i]:
                        lines.append(cols[i] + ' — ' + cells[i])
    return '\n'.join(lines)


def model_attempt(q):
    """the question's model answer as an answer {text, sheets} — used to prove the model scores full marks, and for extras"""
    text, sheets = [], []
    for b in q.get('model') or []:
        t = b.get('t')
        if t in ('p', 'note'): text.append(_str(b.get('text')))
        elif t == 'wn': text.append((b.get('title') or 'Working note') + ': ' + _str(b.get('text')))
        elif t == 'list': text.extend(_str(x) for x in b.get('items') or [])
        elif t == 'legal': text.extend(n + ': ' + _str(b.get(k)) for k, n in (('provision', 'Provision'), ('facts', 'Facts'), ('analysis', 'Analysis'), ('conclusion', 'Conclusion')))
        elif t == 'journal':
            rows = []
            for e in b.get('entries') or []:
                for i, l in enumerate(e.get('lines') or []):
                    if l.get('dr') is not None: rows.append([_str(e.get('date')) if i == 0 else '', _str(l.get('ac')) + ' Dr.', '', l['dr'], ''])
                    else: rows.append(['', 'To ' + _str(l.get('ac')), '', '', l.get('cr')])
                if e.get('narr'): rows.append(['', '(' + _str(e['narr']) + ')', '', '', ''])
            sheets.append({'ok': True, 'kind': 'journal', 'name': b.get('title') or 'Journal', 'title': _str(b.get('title')), 'cols': ['Date', 'Particulars', 'L.F.', 'Dr. Amount (₹)', 'Cr. Amount (₹)'], 'rows': rows})
        elif t == 'ledger':
            dr, cr = b.get('dr') or [], b.get('cr') or []
            rows = []
            for i in range(max(len(dr), len(cr))):
                a = dr[i] if i < len(dr) else None; c = cr[i] if i < len(cr) else None
                rows.append(([_str(a.get('date')), _str(a.get('part')), '', a.get('amt')] if a else ['', '', '', '']) + ([_str(c.get('date')), _str(c.get('part')), '', c.get('amt')] if c else ['', '', '', '']))
            if not b.get('open'):
                rows.append(['', 'Total', '', sum(x.get('amt') or 0 for x in dr), '', 'Total', '', sum(x.get('amt') or 0 for x in cr)])
            nx = b.get('next')
            if isinstance(nx, dict) and nx.get('amt'):
                bd = [_str(nx.get('date')), ('To' if nx.get('side') == 'dr' else 'By') + ' Balance b/d', '', nx['amt']]
                rows.append(bd + ['', '', '', ''] if nx.get('side') == 'dr' else ['', '', '', ''] + bd)
            sheets.append({'ok': True, 'kind': 'tacc', 'name': b.get('ac') or 'Ledger', 'title': _str(b.get('title') or b.get('ac')), 'account': _str(b.get('ac')), 'cols': ['Dr. Date', 'Dr. Particulars', 'Dr. J.F.', 'Dr. Amount (₹)', 'Cr. Date', 'Cr. Particulars', 'Cr. J.F.', 'Cr. Amount (₹)'], 'rows': rows})
        elif t == 'tb':
            tr = b.get('rows') or []
            sheets.append({'ok': not b.get('diff'), 'kind': 'grid', 'name': 'Trial Balance', 'title': _str(b.get('title')) or ('Trial Balance as at ' + _str(b.get('date'))).strip(), 'cols': ['Particulars', 'Dr. Amount (₹)', 'Cr. Amount (₹)'],
                           'rows': [[_str(r.get('ac')), '' if r.get('dr') is None else r['dr'], '' if r.get('cr') is None else r['cr']] for r in tr] + [['Total', sum(r.get('dr') or 0 for r in tr), sum(r.get('cr') or 0 for r in tr)]]})
        elif t == 'cashbook':
            cols = b.get('cols') or []; dr, cr = b.get('dr') or [], b.get('cr') or []
            hd = lambda p: [p + ' Date', p + ' Particulars', p + ' L.F.'] + [p + ' ' + _str(c) + ' (₹)' for c in cols]
            side = lambda a: ([_str(a.get('date')), _str(a.get('part')), _str(a.get('lf'))] + [(x if x else '') for x in (list(a.get('v') or []) + [''] * len(cols))[:len(cols)]]) if a else [''] * (3 + len(cols))
            rows = [side(dr[i] if i < len(dr) else None) + side(cr[i] if i < len(cr) else None) for i in range(max(len(dr), len(cr)))]
            tot = lambda L: ['', 'Total', ''] + [sum(((a.get('v') or []) + [0] * len(cols))[k] or 0 for a in L) for k in range(len(cols))]
            rows.append(tot(dr) + tot(cr))
            sheets.append({'ok': True, 'kind': 'tacc', 'name': 'Cash Book', 'title': _str(b.get('title')) or 'Cash Book', 'account': 'Cash Book', 'cols': hd('Dr.') + hd('Cr.'), 'rows': rows})
        elif t == 'table':
            sh = {'ok': True, 'kind': 'grid', 'name': b.get('title') or 'Table', 'title': _str(b.get('title')), 'cols': b.get('head') or [], 'rows': b.get('rows') or []}
            if b.get('num'): sh['amt'] = list(b['num'])
            sheets.append(sh)
    return {'text': '\n'.join(text), 'sheets': sheets}


def _hits(groups, toks, raws, cl):
    hit, neg, found = [], [], []
    for g in groups:
        alts = [a for a in _str(g).split('|') if a.strip()]
        h = next((a for a in alts if phrase_in(pairs(a), toks, raws, cl)), None)
        if h is not None: hit.append(True); neg.append(''); found.append(h.strip()); continue
        n = next((a for a in alts if phrase_in(pairs(a), toks, None, cl)), None)
        hit.append(False); neg.append(n.strip() if n is not None else '')
    return hit, neg, found


def _colname(c): return re.sub(r'\s*\(₹\)\s*', ' ', _str(c)).strip() or 'another column'


def _frac(got, need):
    if got >= need: return 1
    if need >= 2 and 2 * got >= need: return 0.5
    return 0


def _desc(acc, side, amt):
    parts = [acc or 'Entry']
    if side: parts.append(SIDEW.get(side, side))
    if amt is not None: parts.append('₹' + fmt_n(amt))
    return ' '.join(parts)


def _tier(e, r):
    acc, side, amt = e
    a = ac_match(acc, r['t'], r['ct'])
    sd = (side == '' or r['side'] == '' or r['side'] == side) if side in STD_SIDES else ac_match(side, ac_toks(r['col']))
    am = amt is None or near(r['amt'], amt)
    if a and sd and am: return 4
    if a and am: return 3
    if a and sd and amt is not None: return 2
    if sd and am and side != '' and acc.strip() and amt is not None: return 1
    return -1


def _exp_rows(p):
    E = []
    for e in p.get('rows') or []:
        e = list(e) + ['', '', None]
        amt = e[2]
        E.append((_str(e[0]), _str(e[1]).lower(), None if amt is None or amt == '' else abs(float(amt))))
    return E


def _match_rows(E, rows):
    n = len(E); best = [(-1, -1)] * n; used = set()
    for i, e in enumerate(E):
        for j, r in enumerate(rows):
            if j not in used and _tier(e, r) == 4: best[i] = (4, j); used.add(j); break
    for want in ((3, 2), (1, 0)):
        for i, e in enumerate(E):
            if best[i][0] >= 2: continue
            bt, bj = -1, -1
            for j, r in enumerate(rows):
                if j in used: continue
                t = _tier(e, r)
                if t in want and t > bt: bt, bj = t, j
            if bj >= 0:
                best[i] = (bt, bj)
                if bt >= 2: used.add(bj)
    return best


def _wrong_rules(w, say=''):
    if not w: return []
    if isinstance(w, dict): w = [w]
    if all(isinstance(x, str) for x in w): return [{'kw': w, 'say': say}]
    return [x for x in w if isinstance(x, dict) and x.get('kw')]


def _rule_hit(rule, toks, raws, cl):
    kw = rule['kw'] if isinstance(rule['kw'], list) else [rule['kw']]
    got = sum(1 for g in kw if any(phrase_in(pairs(a), toks, raws, cl) for a in _str(g).split('|') if a.strip()))
    return got >= (rule.get('min') or len(kw))




def _mask_copied(toks, qt, lim, n=6):
    """words copied from the question into the written text (6+ words in the same order — figures and 'rupees' are skipped,
    since restating the given data is normal) cannot earn keyword credit; table headings and cells (tokens from lim on) are never masked"""
    W = lambda w: not _isnum(w) and w != 'rupe'
    qw = [w for w in qt if W(w)]
    idx = [i for i in range(min(lim, len(toks))) if W(toks[i])]
    if len(qw) < n or len(idx) < n: return toks
    grams = set(tuple(qw[i:i + n]) for i in range(len(qw) - n + 1))
    mask = [False] * len(toks)
    for i in range(len(idx) - n + 1):
        if tuple(toks[j] for j in idx[i:i + n]) in grams:
            for j in idx[i:i + n]: mask[j] = True
    return ['~' if mask[i] else t for i, t in enumerate(toks)]


_IGN = None


def check_answer(q, ans=None):
    """q = unit question (scheme with kw/nums/rows/wrong/ai_only); ans = {text, table (ca-pad/1 or {cols, rows}) | sheets, photos}.
    Returns {schema, provider, status, total, max, full, pendingMarks, points[], extras[], remarks[], pending[], tips[]}"""
    global _IGN
    if _IGN is None: _IGN = set(tokens('total totals balance c/d b/d grand subtotal carried brought forward down'))
    ans = ans or {}
    text = _str(ans.get('text'))
    sheets = ans['sheets'] if ans.get('sheets') is not None else sheets_of(ans.get('table'))
    ph = ans.get('photos') or 0
    nph = ph if isinstance(ph, int) else len(ph)
    typed = bool(text.strip()) or any(len(s.get('rows') or []) for s in sheets)
    scheme = q.get('scheme') or []
    full = r2(sum(p.get('m', 0) for p in scheme))
    base = lambda p: {'id': p.get('id'), 'pt': _str(p.get('pt')), 'm': p.get('m', 0), 'skill': _str(p.get('skill'))}
    if nph and not typed:
        pts = [dict(base(p), status='pending', marks=0, found=[], expected=[], remark=WAITING_PHOTO) for p in scheme]
        return {'schema': 'ca-check/1', 'provider': 'offline', 'status': 'waiting', 'total': 0, 'max': 0, 'full': full, 'pendingMarks': full,
                'points': pts, 'extras': [], 'remarks': [], 'pending': [p['id'] for p in pts], 'tips': []}
    rows = []
    for s in sheets: rows.extend(rows_of_sheet(s))
    rows.extend(text_rows(text))
    cells = '\n'.join(_str(x) for s in sheets for r in (s.get('rows') or []) for x in r)
    toks, raws, cl = clauses(text + '\n' + table_text(sheets))
    toks = _mask_copied(toks, tokens(_str(q.get('q'))), len(clauses(text)[0]))
    pool = nums_in(text) + nums_in(cells, True)
    points, remarks = [], []
    for p in scheme:
        o = base(p)
        kw, nums, er, pok = p.get('kw') or [], p.get('nums') or [], p.get('rows') or [], bool(p.get('pad_ok'))
        if p.get('ai_only') or not (kw or nums or er or pok):
            o.update(status='pending', marks=0, found=[], expected=[], remark=PENDING_AI if p.get('ai_only') else PENDING_NOKEY); points.append(o); continue
        comps, found, expected, notes, evid = [], [], [], [], False
        if kw:
            hit, neg, fk = _hits(kw, toks, raws, cl)
            g = sum(1 for x in hit if x)
            f = _frac(g, p.get('min') or len(kw))
            if f == 0.5 and any(o is not p and (o.get('kw') or []) == kw for o in scheme): f = 0   # "any N points": points sharing the same groups are all-or-nothing
            comps.append(f); found.extend(fk)
            if f < 1:
                expected.extend(_str(kw[i]).split('|')[0].strip() for i in range(len(kw)) if not hit[i])
                for x in neg:
                    if x: notes.append('Stated in the negative: "' + x + '"'); evid = True
        if nums:
            fn, mn = [], []
            for n in nums:
                n = float(n)
                if any(near(x, n) for x in pool): fn.append(n); continue
                mn.append(n); cand = None
                for x in pool:
                    d = abs(x - n)
                    if not near(x, n) and d <= 0.25 * abs(n) and (cand is None or d < abs(cand - n)): cand = x
                if cand is not None: notes.append(fmt_n(cand) + ' found — expected ' + fmt_n(n)); evid = True
            comps.append(1 if len(fn) == len(nums) else (0.5 if len(nums) >= 2 and 2 * len(fn) >= len(nums) else 0))
            found.extend(fmt_n(x) for x in fn); expected.extend(fmt_n(x) for x in mn)
        if er:
            E = _exp_rows(p); best = _match_rows(E, rows); sc = []
            for (acc, side, amt), (t, j) in zip(E, best):
                r = rows[j] if j >= 0 else None
                if t == 4: sc.append(1); found.append(_desc(r['ac'], r['side'], r['amt'])); continue
                sc.append(0.5 if t in (3, 2) else 0)
                if t == 3: found.append(_desc(r['ac'], r['side'], r['amt'])); notes.append(r['ac'] + ': ' + (SIDEW.get(r['side'], r['side']) + ' instead of ' + SIDEW.get(side, side) if side in STD_SIDES else 'under "' + _colname(r['col']) + '" instead of "' + side + '"')); evid = True
                elif t == 2: found.append(_desc(r['ac'], r['side'], r['amt'])); notes.append(r['ac'] + ': ₹' + fmt_n(r['amt']) + ' found — expected ₹' + fmt_n(amt)); evid = True
                elif t == 1: expected.append(_desc(_title(acc), side, amt)); notes.append('₹' + fmt_n(amt) + ' ' + SIDEW.get(side, side) + ' to ' + r['ac'] + ' — expected ' + _title(acc)); evid = True
                elif t == 0: expected.append(_desc(_title(acc), side, amt)); notes.append(r['ac'] + ': ' + SIDEW.get(r['side'], r['side']) + ' ₹' + fmt_n(r['amt']) + ' — expected ' + _desc(_title(acc), side, amt)); evid = True
                else: expected.append(_desc(_title(acc), side, amt))
            avg = sum(sc) / len(sc)
            comps.append(1 if all(x == 1 for x in sc) else (0.5 if avg >= 0.5 else 0))
        if pok:
            good = any(s.get('ok') is True and (s.get('rows') or []) for s in sheets)
            comps.append(1 if good else 0)
            if good: found.append('Your table checks out (totals agree)')
            else: expected.append('Totals that agree in the exam-format table')
        f = 1 if all(c == 1 for c in comps) else (0 if all(c == 0 for c in comps) else 0.5)
        for w in _wrong_rules(p.get('wrong'), _str(p.get('say'))):
            if _rule_hit(w, toks, raws, cl):
                say = _str(w.get('say')) or 'This statement is not correct here.'
                notes.append(say); evid = True; f = min(f, 0.5)
                if say not in remarks: remarks.append(say)
        st = 'correct' if f == 1 else ('partial' if f == 0.5 else ('wrong' if evid else 'missing'))
        o.update(status=st, marks=r2(f * o['m']), found=found, expected=expected, remark='; '.join(notes))
        points.append(o)
    for w in _wrong_rules(q.get('wrong'), _str(q.get('say'))):
        if _rule_hit(w, toks, raws, cl):
            say = _str(w.get('say')) or 'This statement is not correct here.'
            if say not in remarks: remarks.append(say)
    # extras: table rows / sentences that match nothing in the model (listed, never deducted)
    extras = []
    ma = model_attempt(q)
    mrows = [r for s in ma['sheets'] for r in rows_of_sheet(s)]
    allE = [e for p in scheme for e in _exp_rows(p)]
    if (mrows or allE) and any(r['src'] == 'table' for r in rows):
        for r in rows:
            if r['src'] != 'table' or not r['t'] or all(w in _IGN for w in r['t']): continue
            ok = any(ac_match(acc, r['t'], r['ct']) and (amt is None or near(r['amt'], amt)) for acc, side, amt in allE) or \
                any(near(r['amt'], m['amt']) and any(same(a, b) for a in r['t'] for b in m['t']) for m in mrows)
            if not ok: extras.append({'kind': 'row', 'text': _desc(r['ac'], r['side'], r['amt'])})
    vtext = '\n'.join([ma['text'], table_text(ma['sheets']), _str(q.get('q'))] + [_str(p.get('pt')) for p in scheme] +
                      [_str(a) for p in scheme for g in (p.get('kw') or []) for a in _str(g).split('|')])
    vocab = set(tokens(vtext))
    for sent in _RE_SENT.split(text):
        st_ = [w for w in tokens(sent) if not _isnum(w)]
        if len(st_) < 4: continue
        h = sum(1 for w in st_ if w in vocab or any(same(w, v) for v in vocab))
        if h * 4 < len(st_): extras.append({'kind': 'sentence', 'text': sent.strip()[:160]})
    extras = extras[:8]
    # how to avoid this next time: the common mistakes / examiner remarks / tips that share words with the points lost
    lost = [p for p in points if p['status'] in ('partial', 'wrong', 'missing')]
    poolt = [('mistake', _str(x)) for x in q.get('mistakes') or []] + [('remark', _str(x)) for x in q.get('remarks') or []] + [('tip', _str(x)) for x in q.get('tips') or []]
    ptok = [list(dict.fromkeys(w for w in tokens(x) if len(w) >= 4 and not _isnum(w))) for _, x in poolt]
    chosen = []
    for p in lost:
        pt = [w for w in tokens(p['pt']) if len(w) >= 4 and not _isnum(w)]
        bi, bs = -1, 1
        for i, xt in enumerate(ptok):
            s = sum(1 for w in xt if any(same(w, y) for y in pt))
            if s > bs: bi, bs = i, s
        if bi >= 0 and bi not in chosen: chosen.append(bi)
        if len(chosen) >= 4: break
    if lost and not chosen:
        for kind in ('mistake', 'tip'):
            i = next((k for k, x in enumerate(poolt) if x[0] == kind), -1)
            if i >= 0: chosen.append(i)
    tips = [{'kind': poolt[i][0], 'text': poolt[i][1]} for i in chosen]
    chk = [p for p in points if p['status'] != 'pending']; pend = [p for p in points if p['status'] == 'pending']
    return {'schema': 'ca-check/1', 'provider': 'offline', 'status': 'checked' if not pend else ('pending' if not chk else 'partial'),
            'total': r2(sum(p['marks'] for p in chk)), 'max': r2(sum(p['m'] for p in chk)), 'full': full, 'pendingMarks': r2(sum(p['m'] for p in pend)),
            'points': points, 'extras': extras, 'remarks': remarks, 'pending': [p['id'] for p in pend], 'tips': tips}


def tf_reason(item, text):
    """mock paper true/false: is the student's reason right? item.kw/min (key points) when present, else an approximate
    overlap with the model reason's own key words (those not already in the statement): ≥2 and ≥35% of them."""
    text = _str(text)
    if not text.strip(): return {'ok': False, 'how': 'none', 'hits': [], 'key': []}
    if item.get('kw'):
        toks, raws, cl = clauses(text)
        return {'ok': point_hit({'kw': item['kw'], 'min': item.get('min') or len(item['kw'])}, toks, raws, cl), 'how': 'kw', 'hits': [], 'key': []}
    reason = re.sub(r'^\s*(true|false)(?![a-z])\.?\s*', '', _str(item.get('reason')), flags=re.I)
    st = set(tokens(_str(item.get('s'))))
    key = list(dict.fromkeys(w for w in tokens(reason) if len(w) >= 4 and not _isnum(w) and w not in st))
    at = tokens(text)
    hits = [w for w in key if any(same(w, y) for y in at)]
    return {'ok': len(hits) >= min(2, len(key)) and len(hits) * 100 >= 35 * len(key), 'how': 'overlap', 'hits': hits, 'key': key}

if __name__ == '__main__':
    import sys
    print(tokens(' '.join(sys.argv[1:]) or 'Rs 1.5 lakh debited to Purchases A/c; posting balances'))
