"""Derives content/ca/foundation/weightage.json from ICAI's Foundation Model Test Papers (text dump).
   python3 tools/ca_weightage.py /tmp/ca/txt
See "method" in the output. Parts were classified by keyword rules (P1/P2 below) and then every part was checked by hand:
P1MAP lists the hand-checked chapter for every part of each Paper 1 MTP in order (- = not mapped); P2FIX corrects the rules for Paper 2."""
import re, json, sys
import os
SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ca/txt"
F = os.path.join(SRC, "CA - Foundation__Model Test Papers__84774bos68243.txt")
L = open(F, encoding='utf-8').read().split('\n')
def papers(lo, hi):
    starts = [i for i in range(lo, hi) if re.match(r'\s*MODEL TEST PAPER \d+\s*$', L[i])]
    return [(int(re.search(r'\d+', L[s]).group()), s, (starts[k+1] if k+1 < len(starts) else hi)) for k, s in enumerate(starts)]
MK = re.compile(r'\((\d+)\s*Marks?\)\s*$', re.I)
TOT = re.compile(r'\(\s*\d+\s*(\+\s*\d+\s*)+=\s*\d+\s*Marks?\)|\(\s*100 Marks\)|Statements?\s*x', re.I)
def parts(s, e):
    out, buf = [], []
    for i in range(s, e):
        ln = L[i]
        if TOT.search(ln):
            m = re.search(r'(\d+)\s*Statements?\s*x\s*(\d+)\s*Marks', ln, re.I)
            if m:  # true/false block: split statements
                txt = '\n'.join(buf + [ln]); buf = []
                sts = re.split(r'\n\s*\((?:i|ii|iii|iv|v|vi|vii|viii)\)\s', txt)
                for st in sts[1:]: out.append({'m': int(m.group(2)), 't': ' '.join(st.split()), 'tf': 1})
            else: buf = []
            continue
        buf.append(ln)
        m = MK.search(ln)
        if m: out.append({'m': int(m.group(1)), 't': ' '.join(' '.join(buf).split())}); buf = []
    return out
STMT = re.compile(r'\n\s*(?:\((?:i|ii|iii|iv|v|vi|vii|viii)\)|(?:i|ii|iii|iv|v|vi|vii|viii)\.|[1-8]\.?(?=\s{2,}))\s')
MULT = re.compile(r'\((\d+)\s*(?:statements?\s*)?x\s*(\d+)\s*(?:marks?\s*)?=\s*(\d+)\s*Marks?\)', re.I)
def parts(s, e):
    out, buf = [], []
    for i in range(s, e):
        ln = L[i]
        m = MULT.search(ln)
        if m:
            txt = '\n'.join(buf + [ln]); buf = []
            if re.search(r'true or false|ture or false', txt, re.I):
                sts = STMT.split(txt)
                for st in [x for x in sts[1:] if not re.search(r'true or false|ture or false', x, re.I)][:int(m.group(1))]: out.append({'m': int(m.group(2)), 't': ' '.join(st.split()), 'tf': 1})
            else: out.append({'m': int(m.group(3)), 't': ' '.join(txt.split()), 'alt': False})
            continue
        if TOT.search(ln): buf = []; continue
        buf.append(ln)
        mm = MK.search(ln)
        if mm:
            t = ' '.join(' '.join(buf).split()); buf = []
            alt = bool(re.match(r'(\d+\s*)?(OR|Or)\b', t))
            out.append({'m': int(mm.group(1)), 't': t, 'alt': alt})
    return out
W = lambda *a: [(re.compile(p, re.I), w) for p, w in a]
P1 = {
 'fnd-p1-ch01': W((r'accounting standards?\b', 3), (r'accounting polic', 3), (r'accrual|prudence|going concern|materiality|consistency|full disclosure|conservatism|money measurement|matching concept|entity concept|historical cost', 3), (r'concepts?\b|conventions?\b|assumptions', 1), (r'(capital|revenue) (expenditure|receipt)|deferred revenue', 3), (r'contingent', 3), (r'book-?keeping and accounting|limitations .*financial statements|qualitative characteristics|measurement discipline|scope of accounting|functions of accounting|users of accounting', 3)),
 'fnd-p1-ch02': W((r'rectif', 3), (r'suspense', 3), (r'trial balance', 2), (r'compensating errors?', 3), (r'journal proper|petty cash|cash book|subsidiary books?|purchase (book|day book)|sales (book|day book)', 2), (r'rules of posting|ledger', 2), (r'journal entries', 1), (r'errors?\b', 1)),
 'fnd-p1-ch03': W((r'bank reconciliation', 4), (r'pass ?book', 3), (r'bank statement', 3)),
 'fnd-p1-ch04': W((r'inventor', 3), (r'stock[- ]taking|physical (stock|inventory|verification)|valuation of (stock|inventor)', 3), (r'closing stock', 1), (r'\bFIFO\b|weighted average|net realisable', 3)),
 'fnd-p1-ch05': W((r'depreciat', 2), (r'straight line|written down value|reducing balance|useful life|residual value|amortis|machinery account|change in (the )?method', 2)),
 'fnd-p1-ch06': W((r'bills? of exchange|promissory|drawee|accommodation bill|retire(ment|d)? (of )?(a )?bill|renewal of (a )?bill|noting charges|dishono', 4)),
 'fnd-p1-ch07': W((r'trading (and|&) profit|trading account|manufacturing (account|a/c|activit)|final accounts|vocation|sole (proprietor|trader)', 3), (r'profit and loss account|balance sheet', 1)),
 'fnd-p1-ch08': W((r'\bclub\b|receipts? (and|&) payments?|income (and|&) expenditure|not-?for-?profit|college|\bsociety|subscriptions?|hospital|charitable', 4)),
 'fnd-p1-ch09': W((r'not maintain(ed)? (proper|regular)|incomplete records|single entry|statement of affairs|no proper books|keeps? no (stock )?records', 4)),
 'fnd-p1-ch10': W((r'partner|partnership|goodwill|\bLLP\b|garner|realisation account|dissol', 3)),
 'fnd-p1-ch11': W((r'\bshares?\b|debenture|forfeit|allotment|bonus issue|right(s)? issue|redemption|redeem|share capital|securities premium|\bLtd\b|limited\b|company', 3)),
}
P2 = {
 'fnd-p2-ch01': W((r'legislat|executive|judiciary|parliament|constitution|regulatory (framework|bodies|body)|rules? of interpretation|lawmaking|\bstatut|SEBI|Reserve Bank|\bRBI\b|\bMCA\b|\bICAI\b', 3)),
 'fnd-p2-ch02': W((r'Indian Contract Act|contract act', 4), (r'\bcontract|offer|acceptance|consideration|\bminor\b|void|voidable|quasi|indemnity|guarant|surety|bail(ment|or|ee)|pledge|pawn|breach|damages|coercion|undue influence|fraud|misrepresent|novation|promis|agreement|wager|restitution|frustrat|quantum meruit|finder of goods|supply of necessaries', 1)),
 'fnd-p2-ch03': W((r'sale of goods', 5), (r'caveat emptor|unpaid seller|\blien\b|stoppage in transit|warrant(y|ies)|conditions? and warrant|property in (the )?goods|sale by (sample|description)|auction|agreement to sell|merchantable|right of resale|ascertained|specific goods|future goods|delivery|on approval|sale or return|nemo dat', 3), (r'\bgoods\b|seller|buyer', 1)),
 'fnd-p2-ch04': W((r'Indian Partnership Act|Partnership Act,? 1932', 5), (r'partner|partnership|\bfirm\b|holding out|implied authority|dissolution', 2)),
 'fnd-p2-ch05': W((r'\bLLP\b|limited liability partnership|designated partner', 5)),
 'fnd-p2-ch06': W((r'companies act|\bcompan(y|ies)\b|memorandum|articles of association|one person company|\bOPC\b|corporate veil|indoor management|ultra vires|constructive notice|private company|public company|holding company|subsidiary|dormant|small company|section 8|government company|foreign company', 3)),
 'fnd-p2-ch07': W((r'negotiable instruments?|cheque|promissory note|bills? of exchange|holder in due course|endorse|indorse|crossing|crossed|drawer|drawee|payee|dishono|maturity|days of grace|noting|protest', 3)),
}
def classify(t, rules):
    sc = {c: sum(w * len(p.findall(t)) for p, w in rs) for c, rs in rules.items()}
    best = sorted(sc.items(), key=lambda x: -x[1])
    return best
def run(lo, hi, rules, tag, show=False):
    res = []
    for n, s, e in papers(lo, hi):
        ps = parts(s, e)
        for k, p in enumerate(ps):
            b = classify(p['t'], rules)
            ch = b[0][0] if b[0][1] >= 3 and b[0][1] >= 2 * b[1][1] else None
            res.append({'paper': tag, 'mtp': n, 'k': k, 'm': p['m'], 'alt': p.get('alt', False), 'tf': p.get('tf', 0), 'auto': ch, 'sc': b[:3], 't': p['t'][:220]})
    return res

P1MAP = {1: '01 01 05 06 10 08 01 05 02 03 09 10 10 08 02 - - 11 11 05 06', 2: '01 01 05 06 10 - 01 03 - 05 09 10 10 08 02 - 11 11 -', 3: '01 11 01 10 02 11 01 05 - 03 07 10 10 10 09 02 08 11 -', 4: '01 02 01 10 09 11 01 02 05 - - 10 10 07 06 - - 11 11 11 03', 5: '02 04 08 11 06 02 - - 02 - 07 10 10 08 03 09 11 11 -', 6: '01 01 02 06 10 11 01 - 05 03 08 - 10 - 09 11 11 11 -', 7: '01 02 - 11 08 11 01 04 02 05 10 07 08 10 06 09 11 11 03', 8: '05 02 01 10 02 11 01 - - 03 08 10 10 10 09 02 - 11 11 06', 9: '- 02 01 06 02 10 01 02 02 05 08 10 10 09 04 - - 11 11 02', 10: '02 01 - 06 08 10 01 02 03 06 07 10 10 08 04 - 11 11 04'}
P2FIX = {(1, 4): '05', (1, 12): '01', (1, 17): '02', (1, 19): '02', (2, 5): '02', (2, 11): '02', (2, 13): '01', (3, 0): '02', (3, 15): '03', (3, 20): '02', (4, 9): '05', (4, 22): '02', (5, 17): '01', (6, 0): None, (6, 1): '02', (6, 8): '05', (6, 10): '04', (6, 11): '04', (6, 17): '01', (7, 15): '02', (7, 17): '01', (7, 24): '02', (8, 5): '03', (8, 18): '03', (8, 22): '07', (8, 24): '02', (9, 3): '03', (10, 21): '02', (10, 30): '07', (10, 32): '02'}
P2ALT = {(10, 34)}
def derive():
    rows, out = [], {}
    for paper, lo, hi, rules in (('p1', 138, 3286, P1), ('p2', 3286, 5288, P2)):
        r = run(lo, hi, rules, paper)
        for x in r:
            if paper == 'p1':
                codes = P1MAP[x['mtp']].split(); assert len(codes) == len([y for y in r if y['mtp'] == x['mtp']]), (paper, x['mtp'])
                c = codes[x['k']]; ch = None if c == '-' else f'fnd-p1-ch{c}'
            else:
                key = (x['mtp'], x['k'])
                ch = (None if P2FIX[key] is None else f'fnd-p2-ch{P2FIX[key]}') if key in P2FIX else x['auto']
                if key in P2ALT: x['alt'] = True
            rows.append({**x, 'ch': ch})
    for paper in ('p1', 'p2'):
        R = [x for x in rows if x['paper'] == paper and not x['alt']]
        mt = sorted({x['mtp'] for x in R}); offered = sum(x['m'] for x in R); mapped = sum(x['m'] for x in R if x['ch'])
        chs = {}
        for x in R:
            if not x['ch']: continue
            c = chs.setdefault(x['ch'], {'marks': 0, 'papers': set(), 'parts': 0}); c['marks'] += x['m']; c['papers'].add(x['mtp']); c['parts'] += 1
        out[f'fnd-{paper}'] = {'mtps': len(mt), 'offered_marks': offered, 'mapped_marks': mapped, 'unmapped_marks': offered - mapped,
            'chapters': {k: {'total_marks': v['marks'], 'avg_per_paper': round(v['marks'] / len(mt), 1), 'in_papers': len(v['papers']), 'parts': v['parts']} for k, v in sorted(chs.items())}}
    return out, rows
if __name__ == '__main__':
    import json
    out, rows = derive()
    doc = {'schema': 'ca-weightage/1', 'level': 'foundation',
      'source': 'ICAI Board of Studies, Model Test Papers, Foundation Course (relevant for May 2025 examination and onwards), edition February 2025 — 10 papers each for Paper 1 and Paper 2.',
      'label': 'Derived from ICAI Model Test Papers — not an official ICAI weightage.',
      'method': ['Every sub-question carrying its own marks (and each 2-mark true/false statement) was cut out of the question papers with its marks.',
                 'Each part was mapped to one chapter of the current Foundation study material only when its subject was unambiguous (keyword rules, then every part checked by hand). Parts that mix chapters or could belong to two chapters were left unmapped.',
                 'Marks counted are marks OFFERED in the paper: Question 1 is compulsory and four of the remaining five are answered, so each paper offers 120 marks for a 100-mark exam. Where a part says "OR", only the first alternative is counted.',
                 'avg_per_paper = total marks for the chapter across the 10 papers / 10. in_papers = in how many of the 10 papers the chapter appeared.',
                 'Papers 3 and 4 (objective MCQ papers) are not included yet: their questions carry no chapter labels and were not mapped.'],
      'script': 'tools/ca_weightage.py', 'papers': out}
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'ca', 'foundation', 'weightage.json')
    json.dump(doc, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    for k, v in out.items():
        print(k, f"offered {v['offered_marks']} mapped {v['mapped_marks']} ({round(v['mapped_marks']/v['offered_marks']*100)}%)")
        for c, d in v['chapters'].items(): print('  ', c, d)
