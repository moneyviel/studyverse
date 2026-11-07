#!/usr/bin/env python3
"""StudyVerse CA content checker.

Checks:
  * structure files (content/ca/<level>/structure.json): ids unique, built units have files
  * every unit file: schema, unique ids, MCQ keys, marking-scheme totals,
    journal entries balance, ledgers balance (and agree with the journal they were posted from),
    trial balances agree, table totals add up, every `check` expression re-computed,
    numeric MCQ answers re-computed (and no wrong option equal to the answer)
  * optional originality guard (--src DIR): no run of 10+ consecutive words shared with the ICAI text

  * MCQ topic + explanation rules (unit and case MCQs): `topic` must match a structure.json topic of the unit
    or a concept-card title in the unit; `explain` must have 35+ words. These are warnings for now;
    with --strict they are errors.
  * automatic answer checking (tools/ca_vivamatch.py check_answer = js/ca-check.js): scheme-point fields kw/min, nums,
    rows, wrong/say, pad_ok are well-formed; a point with none of kw/nums/rows/pad_ok/ai_only is a warning (error with --strict);
    the model answer must earn every offline mark (warning; error with --strict); JS and Python checkers agree (needs node)

Usage:  python3 tools/ca_validate.py [--src /tmp/ca/txt] [--strict]      exit code 1 on any error
"""
import json, os, re, sys, glob, ast, operator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA = os.path.join(ROOT, 'content', 'ca')
errors, warns = [], []
def err(where, msg): errors.append(f'{where}: {msg}')
def warn(where, msg): warns.append(f'{where}: {msg}')
STRICT = '--strict' in sys.argv
def soft(where, msg): (err if STRICT else warn)(where, msg)   # MCQ topic / explain rules: warnings until every unit has them
UNIT_TOPICS = {}                                              # unit id -> structure.json topics (filled in main)
MIN_EXPLAIN = {'p1': 35, 'p2': 35, 'p3': 35, 'p4': 35}           # minimum words in an MCQ explanation, by Foundation paper
TOPIC_STATS = {'mcqs': 0, 'no_topic': 0, 'bad_topic': 0, 'short': 0}
def norm_topic(t): return re.sub(r'\s+', ' ', re.sub(r'[\u2010-\u2015\-]', ' ', str(t or '').replace('\u2019', "'").replace('\u2018', "'"))).strip().lower()

# ---------- safe arithmetic ----------
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos, ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv}
def calc(expr):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.operand))
        if isinstance(n, ast.Call) and getattr(n.func, 'id', '') in ('round', 'min', 'max', 'abs') and not n.keywords:
            return {'round': round, 'min': min, 'max': max, 'abs': abs}[n.func.id](*[ev(a) for a in n.args])
        raise ValueError(f'unsupported expression part: {ast.dump(n)[:60]}')
    return ev(ast.parse(str(expr), mode='eval'))

def num(s):
    """'₹ 1,20,000' -> 120000 ; '12.5%' -> 12.5 ; returns None if not a plain number"""
    if isinstance(s, (int, float)): return s
    t = str(s).strip().replace('₹', '').replace(',', '').replace('%', '').replace('Rs.', '').strip()
    t = re.sub(r'\s*(Dr|Cr)\.?$', '', t)
    try: return float(t)
    except ValueError: return None

def opt_num(s):
    """MCQ option -> (number, side) e.g. '₹23,300 Dr' -> (23300, 'dr'); '₹3,500 credit balance' -> (3500, 'cr')"""
    m = re.match(r'^\s*(?:₹|Rs\.?)?\s*(-?[\d,]*\.?\d+)\s*(%|[A-Za-z][A-Za-z .]*)?$', str(s))
    if not m: return None, None
    try: v = float(m.group(1).replace(',', ''))
    except ValueError: return None, None
    tail = (m.group(2) or '').lower()
    side = 'dr' if re.search(r'\bdr\b|debit', tail) else 'cr' if re.search(r'\bcr\b|credit', tail) else None
    return v, side

close = lambda a, b: abs(float(a) - float(b)) < 0.006

# ---------- blocks ----------
def acct_key(s):
    s = re.sub(r'^(To|By)\s+', '', str(s)).strip()
    s = re.sub(r'\s*(A/c|Account|a/c)\.?$', '', s).strip()
    return s.lower()

def check_journal(w, b):
    if not b.get('entries'): err(w, 'journal has no entries'); return
    for i, e in enumerate(b['entries']):
        d = sum(l.get('dr', 0) for l in e.get('lines', [])); c = sum(l.get('cr', 0) for l in e.get('lines', []))
        if not e.get('lines'): err(w, f'entry {i+1} has no lines')
        if not close(d, c): err(w, f'journal entry {i+1} ({e.get("date")}) does not balance: Dr {d} vs Cr {c}')
        if d <= 0: err(w, f'journal entry {i+1} has zero amount')
        if not e.get('narr'): warn(w, f'journal entry {i+1} has no narration')
        for l in e['lines']:
            if ('dr' in l) == ('cr' in l): err(w, f'journal entry {i+1}: line must have exactly one of dr/cr')

def check_ledger(w, b):
    d = sum(x['amt'] for x in b.get('dr', [])); c = sum(x['amt'] for x in b.get('cr', []))
    if not b.get('open') and not close(d, c): err(w, f'ledger {b.get("ac")} does not balance: Dr {d} vs Cr {c}')
    if 'next' in b:
        bal = [x for x in b['dr'] + b['cr'] if x.get('bal')]
        if bal and not close(bal[0]['amt'], b['next']['amt']): err(w, f'ledger {b.get("ac")}: balance b/d differs from balance c/d')

def check_tb(w, b):
    d = sum(r.get('dr', 0) for r in b['rows']); c = sum(r.get('cr', 0) for r in b['rows'])
    want = b.get('diff')
    ok = close(d, c) if want is None else close(abs(d - c), want)
    if not ok: err(w, f'trial balance totals Dr {d} / Cr {c} (expected difference {want or 0})')

def check_table(w, b):
    rows = b.get('rows', []); ncol = len(b.get('head', []))
    for i, r in enumerate(rows):
        if ncol and len(r) != ncol: err(w, f'table row {i+1} has {len(r)} cells, header has {ncol}')
    if b.get('total'):
        for c in b.get('num', []):
            vals = [num(r[c]) for r in rows[:-1] if num(r[c]) is not None]
            tot = num(rows[-1][c])
            if tot is None or not close(sum(vals), tot): err(w, f'table column {c} total {rows[-1][c]} != sum {sum(vals)}')

def check_cashbook(w, b):
    cols = b.get('cols', [])
    for side in ('dr', 'cr'):
        for r in b.get(side, []):
            if len(r.get('v', [])) != len(cols): err(w, f'cash book row "{r.get("part")}" needs {len(cols)} values')
    for i in b.get('balanced', []):
        d = sum(r['v'][i] or 0 for r in b.get('dr', [])); c = sum(r['v'][i] or 0 for r in b.get('cr', []))
        if not close(d, c): err(w, f'cash book column {cols[i]} does not balance: Dr {d} vs Cr {c}')

def check_legal(w, b):
    for k in ('provision', 'facts', 'analysis', 'conclusion'):
        if not str(b.get(k, '')).strip(): err(w, f'legal answer missing "{k}"')

def check_blocks(w, blocks):
    if not isinstance(blocks, list): err(w, 'blocks must be a list'); return
    js = {}
    for i, b in enumerate(blocks):
        ww = f'{w}[{i}:{b.get("t")}]'
        t = b.get('t')
        if t == 'journal': check_journal(ww, b); js[b.get('id')] = b
        elif t == 'ledger': check_ledger(ww, b)
        elif t == 'tb': check_tb(ww, b)
        elif t == 'table': check_table(ww, b)
        elif t == 'legal': check_legal(ww, b)
        elif t == 'cashbook': check_cashbook(ww, b)
        elif t in ('p', 'note', 'wn'):
            if not str(b.get('text', '')).strip(): err(ww, 'empty text')
        elif t == 'list':
            if not b.get('items'): err(ww, 'empty list')
        else: err(ww, f'unknown block type {t}')
    # ledgers posted from a journal in the same block list must agree with it
    for i, b in enumerate(blocks):
        if b.get('t') == 'ledger' and b.get('from'):
            j = js.get(b['from'])
            if not j: err(f'{w}[{i}]', f'ledger says from "{b["from"]}" but no such journal block'); continue
            k = acct_key(b['ac'])
            jd = sum(l.get('dr', 0) for e in j['entries'] for l in e['lines'] if acct_key(l['ac']) == k)
            jc = sum(l.get('cr', 0) for e in j['entries'] for l in e['lines'] if acct_key(l['ac']) == k)
            ld = sum(x['amt'] for x in b['dr'] if not x.get('bal') and not x.get('ob') and 'b/d' not in x['part'])
            lc = sum(x['amt'] for x in b['cr'] if not x.get('bal') and not x.get('ob') and 'b/d' not in x['part'])
            if not (close(jd, ld) and close(jc, lc)): err(f'{w}[{i}]', f'ledger {b["ac"]} postings Dr {ld}/Cr {lc} differ from journal Dr {jd}/Cr {jc}')

def check_checks(w, checks):
    for c in checks or []:
        try: v = calc(c['expr'])
        except Exception as e: err(w, f'check "{c.get("expr")}" cannot be evaluated: {e}'); continue
        if not close(v, c['value']): err(w, f'CHECK FAILED "{c.get("label")}": {c["expr"]} = {v}, stored {c["value"]}')

def check_mcq(w, q, concept_ids=None):
    o = q.get('options', [])
    if len(o) != 4: err(w, 'ICAI-style MCQs have exactly 4 options')
    if len(set(map(str, o))) != len(o): err(w, 'duplicate options')
    a = q.get('answer')
    if not isinstance(a, int) or not 0 <= a < len(o): err(w, 'answer index out of range'); return
    if not q.get('explain'): err(w, 'MCQ needs explain')
    if q.get('concept') and concept_ids is not None and q['concept'] not in concept_ids: err(w, f'concept {q["concept"]} not found')
    if 'check' in q:
        try: v = calc(q['check'])
        except Exception as e: err(w, f'check cannot be evaluated: {e}'); return
        av, aside = opt_num(o[a])
        if av is None or not close(v, av): err(w, f'ANSWER KEY WRONG: check {q["check"]} = {v}, marked "{o[a]}"')
        for i, oo in enumerate(o):
            ov, oside = opt_num(oo)
            if i != a and ov is not None and close(ov, v) and oside == aside: err(w, f'wrong option "{oo}" equals the answer')
    elif opt_num(o[a])[0] is not None and len(re.sub(r'[^0-9]', '', str(o[a]))) >= 2:
        err(w, f'numeric answer "{o[a]}" has no check expression')

def check_question(w, q):
    for k in ('marks', 'minutes', 'q', 'model', 'scheme', 'remarks', 'mistakes', 'tips', 'pad'):
        if k not in q or q[k] in ('', [], None): err(w, f'question missing {k}')
    if q.get('pad') not in ('text', 'journal', 'ledger', 'tb', 'table', 'legal'): err(w, 'pad must be text|journal|ledger|tb|table|legal')
    tot = sum(s.get('m', 0) for s in q.get('scheme', []))
    if not close(tot, q.get('marks', 0)): err(w, f'marking scheme adds to {tot}, question carries {q.get("marks")} marks')
    sids = set()
    for s in q.get('scheme', []):
        if not s.get('id') or s['id'] in sids: err(w, f'scheme point id missing/duplicate: {s.get("id")}')
        sids.add(s.get('id'))
        if not s.get('pt') or not s.get('skill'): err(w, f'scheme point {s.get("id")} needs pt and skill')
        if s.get('m', 0) <= 0: err(w, f'scheme point {s.get("id")} must carry marks')
    check_blocks(w + '.given', q.get('given', []))
    check_blocks(w + '.model', q.get('model', []))
    check_checks(w, q.get('checks'))
    check_autocheck(w, q)

# ---------- automatic answer checking (js/ca-check.js = check_answer in tools/ca_vivamatch.py) ----------
AUTO = {'points': 0, 'checkable': 0, 'ai_only': 0, 'questions': 0, 'model_full': 0, 'cases': []}
STD_SIDES = ('dr', 'cr', 'add', 'less', '')

def _isnumber(x): return isinstance(x, (int, float)) and not isinstance(x, bool)

def _check_groups(pw, kw, mn, what):
    if not isinstance(kw, list) or not kw or not all(isinstance(g, str) and g.strip() for g in kw): err(pw, f'{what}: kw must be a non-empty list of keyword-group strings'); return
    for g in kw:
        for alt in g.split('|'):
            if alt.strip() and not VM.tokens(alt): err(pw, f'{what}: keyword "{alt}" is only stop-words — it can never match')
    if mn is not None and (not isinstance(mn, int) or not 1 <= mn <= len(kw)): err(pw, f'{what}: min must be 1..{len(kw)}')

def check_autocheck(w, q):
    """scheme point fields kw/min, nums, rows, wrong/say, pad_ok, ai_only; the model answer must earn every offline mark"""
    pts = q.get('scheme', []) or []; missing = []
    AUTO['questions'] += 1
    for p in pts:
        pw = f'{w}.{p.get("id")}'; AUTO['points'] += 1
        if p.get('ai_only'): AUTO['ai_only'] += 1; continue
        if not any(p.get(k) for k in ('kw', 'nums', 'rows', 'pad_ok')): missing.append(p.get('id')); continue
        AUTO['checkable'] += 1
        if p.get('kw') is not None: _check_groups(pw, p['kw'], p.get('min'), 'kw')
        elif p.get('min') is not None: err(pw, 'min given without kw')
        if p.get('nums') is not None and (not isinstance(p['nums'], list) or not all(_isnumber(x) for x in p['nums'])): err(pw, 'nums must be a list of numbers')
        if p.get('rows') is not None:
            if not isinstance(p['rows'], list): err(pw, 'rows must be a list of [account keywords, side, amount]')
            else:
                for r in p['rows']:
                    if not (isinstance(r, list) and len(r) == 3 and isinstance(r[0], str) and isinstance(r[1], str) and (r[2] is None or _isnumber(r[2]))):
                        err(pw, f'row {r!r} must be [account keywords (str), side (str), amount (number or null)]'); continue
                    for alt in r[0].split('|'):
                        if alt.strip() and not VM.tokens(alt): err(pw, f'row account keyword "{alt}" is only stop-words')
                    if r[1].lower() not in STD_SIDES and not VM.tokens(r[1]): err(pw, f'row side "{r[1]}" must be dr|cr|add|less|"" or a column-header keyword')
        for wr in (p.get('wrong') or []) if isinstance(p.get('wrong'), list) else [p.get('wrong')] if p.get('wrong') else []:
            if isinstance(wr, str): continue
            if not isinstance(wr, dict): err(pw, 'wrong must be a list of {kw, min?, say}'); continue
            _check_groups(pw, wr.get('kw'), wr.get('min'), 'wrong')
            if not str(wr.get('say') or '').strip(): err(pw, 'wrong rule needs say (the remark shown)')
    if missing: soft(w, f'{len(missing)}/{len(pts)} scheme points have none of kw/nums/rows/ai_only — shown as "pending AI check": {", ".join(map(str, missing))}')
    if not any(p.get(k) for p in pts for k in ('kw', 'nums', 'rows', 'pad_ok')): return
    try:
        ma = VM.model_attempt(q); ans = {'text': ma['text'], 'sheets': ma['sheets']}
        r = VM.check_answer(q, ans)
        AUTO['cases'] += [[q, ans], [q, {'text': q.get('q', '')}]]
        if r['total'] < r['max']:
            bad = [f'{x["id"]} {x["status"]}' + (f' ({x["remark"][:80]})' if x['remark'] else (f' (missing {", ".join(x["expected"][:3])})' if x['expected'] else '')) for x in r['points'] if x['status'] not in ('correct', 'pending')]
            soft(w, f'AUTO-CHECK: the model answer scores only {r["total"]}/{r["max"]} offline — ' + '; '.join(bad))
        else: AUTO['model_full'] += 1
        rq = VM.check_answer(q, {'text': q.get('q', '')})
        if rq['max'] and rq['total'] >= 0.6 * rq['max']: warn(w, f'auto-check: reading the question back already scores {rq["total"]}/{rq["max"]} — keywords/figures too generic')
    except Exception as e: err(w, f'answer checker failed: {type(e).__name__}: {e}')

# ---------- viva key points ----------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ca_vivamatch as VM

def check_viva(w, v, concept_ids=None):
    for k in ('q', 'model', 'points'):
        if not v.get(k): err(w, f'viva missing {k}'); return
    if v.get('concept') and concept_ids is not None and v['concept'] not in concept_ids: err(w, f'concept {v["concept"]} not found')
    if len(v['points']) < 2: err(w, 'viva needs 2+ key points')
    pids = set()
    for p in v['points']:
        pw = f'{w}.{p.get("id")}'
        if not p.get('id') or p['id'] in pids: err(pw, 'key point id missing/duplicate')
        pids.add(p.get('id'))
        if not p.get('pt'): err(pw, 'key point needs pt (text shown to the student)')
        if not isinstance(p.get('w'), int) or p['w'] <= 0: err(pw, 'weight w must be a positive integer')
        kw = p.get('kw')
        if not kw or not all(isinstance(g, str) and g.strip() for g in kw): err(pw, 'kw must be a non-empty list of keyword groups'); continue
        for g in kw:
            for alt in g.split('|'):
                if alt.strip() and not VM.tokens(alt): err(pw, f'keyword "{alt}" is only stop-words — it can never match')
        mn = p.get('min', len(kw))
        if not isinstance(mn, int) or not 1 <= mn <= len(kw): err(pw, f'min must be 1..{len(kw)}')
    try:
        sc, hit = VM.score(v, v['model'])
        if sc != 100: err(w, f'VIVA: model answer covers only {sc}% — missed {[p["id"] for p in v["points"] if p["id"] not in hit]}')
        sq, _ = VM.score(v, v['q'])
        if sq >= 80: err(w, f'VIVA: reading the question back already scores {sq}% — key points too generic')
        elif sq >= 50: warn(w, f'viva: the question text alone scores {sq}%')
    except Exception as e: err(w, f'viva matcher failed: {e}')

# ---------- mock papers (content/ca/<level>/mocks/*.json, schema ca-mock/1) ----------
def check_mock(path, units_by_id):
    w0 = os.path.relpath(path, ROOT)
    try: m = json.load(open(path, encoding='utf-8'))
    except Exception as e: err(w0, f'cannot read JSON: {e}'); return None
    if m.get('schema') != 'ca-mock/1': err(w0, 'schema must be "ca-mock/1"')
    for k in ('id', 'level', 'paper', 'title', 'label', 'hours', 'marks', 'questions', 'rules', 'choose'):
        if k not in m: err(w0, f'missing "{k}"')
    if 'not an ICAI paper' not in m.get('label', ''): err(w0, 'label must say "not an ICAI paper"')
    qs = m.get('questions', []); comp = set(m.get('compulsory', []))
    opt = [q for q in qs if q['id'] not in comp]
    if len({q['marks'] for q in opt}) > 1: err(w0, 'optional questions must carry equal marks')
    if opt and m.get('choose', 0) > len(opt): err(w0, 'choose is more than the optional questions')
    tot = sum(q['marks'] for q in qs if q['id'] in comp) + (opt[0]['marks'] * m.get('choose', 0) if opt else 0)
    if not close(tot, m.get('marks', 0)): err(w0, f'compulsory + {m.get("choose")} optional questions = {tot}, paper says {m.get("marks")}')
    for q in qs:
        w = f'{w0}#{q["id"]}'
        ps = sum(p.get('marks', 0) for p in q.get('parts', []))
        if not close(ps, q['marks']): err(w, f'parts add to {ps}, question carries {q["marks"]}')
        for p in q.get('parts', []):
            pw = f'{w}({p.get("id")})'; k = p.get('kind')
            if k == 'tf':
                its = p.get('items', [])
                if not its: err(pw, 'true/false part needs items')
                if not close(len(its) * 2, p['marks']): err(pw, f'{len(its)} statements x 2 marks != {p["marks"]}')
                for it in its:
                    if not isinstance(it.get('answer'), bool) or not it.get('s') or not it.get('reason'): err(pw, f'statement {it.get("id")} needs s, answer (true/false) and reason')
                    elif not it['reason'].startswith('True' if it['answer'] else 'False'): err(pw, f'statement {it.get("id")}: reason must begin with the verdict')
            elif k == 'ref':
                uidq, _, qid = str(p.get('ref', '')).partition('#')
                u = units_by_id.get(uidq)
                bq = u and next((x for x in u['questions'] if x['id'] == qid), None)
                if not bq: err(pw, f'ref {p.get("ref")} not found in a built unit')
                elif not close(bq['marks'], p['marks']): err(pw, f'ref {p["ref"]} carries {bq["marks"]} marks, part says {p["marks"]}')
            elif k == 'q':
                bq = p.get('question') or {}
                check_question(pw, bq)
                if not close(bq.get('marks', 0), p['marks']): err(pw, 'question marks differ from part marks')
            else: err(pw, f'unknown part kind {k}')
    return m

# ---------- unit ----------
TOP = ['schema', 'id', 'level', 'paper', 'chapter', 'title', 'outcomes', 'meta', 'concepts', 'illustrations', 'jobs', 'mcqs', 'questions', 'revision', 'quickref']

def text_of(o):
    if isinstance(o, str): return [o]
    if isinstance(o, list): return [t for x in o for t in text_of(x)]
    if isinstance(o, dict): return [t for k, v in o.items() if k not in ('id', 'expr', 't', 'schema', 'skill', 'concept', 'date', 'topic') for t in text_of(v)]
    return []

def check_unit(path, built_ids):
    w0 = os.path.relpath(path, ROOT)
    try: u = json.load(open(path, encoding='utf-8'))
    except Exception as e: err(w0, f'cannot read JSON: {e}'); return None
    for k in TOP:
        if k not in u: err(w0, f'missing "{k}"')
    if u.get('schema') != 'ca-unit/1': err(w0, 'schema must be "ca-unit/1"')
    if u.get('id') not in built_ids: err(w0, f'unit id {u.get("id")} is not marked built in structure.json')
    ids = set()
    def uid(x, kind):
        i = x.get('id')
        if not i: err(w0, f'{kind} without id'); return
        if i in ids: err(w0, f'duplicate id {i}')
        ids.add(i)
    if len(u.get('outcomes', [])) < 2: err(w0, 'needs 2+ learning outcomes')
    m = u.get('meta', {})
    if m.get('difficulty') not in ('core', 'moderate', 'hard'): err(w0, 'meta.difficulty must be core|moderate|hard')
    if not isinstance(m.get('minutes', {}).get('learn'), int) or not isinstance(m.get('minutes', {}).get('practice'), int): err(w0, 'meta.minutes.learn/practice must be integers')
    if len(u.get('concepts', [])) < 3: err(w0, 'needs 3+ concept cards')
    for c in u.get('concepts', []):
        uid(c, 'concept'); w = f'{w0}#{c.get("id")}'
        for k in ('title', 'body', 'analogy', 'work'):
            if not c.get(k): err(w, f'concept missing {k}')
        if c.get('blocks'): check_blocks(w, c['blocks'])
    for x in u.get('illustrations', []):
        uid(x, 'illustration'); w = f'{w0}#{x.get("id")}'
        if not x.get('q') or not x.get('solution'): err(w, 'illustration needs q and solution')
        check_blocks(w + '.given', x.get('given', []))
        check_blocks(w + '.solution', x.get('solution', []))
        check_checks(w, x.get('checks'))
        if not x.get('checks') and any(b.get('t') in ('journal', 'ledger', 'tb', 'cashbook') or (b.get('t') == 'table' and b.get('num')) for b in x.get('solution', [])): warn(w, 'numeric illustration without explicit checks (structural checks still ran)')
    if len(u.get('jobs', [])) < 1: err(w0, 'needs 1+ "On the job" scenario')
    for j in u.get('jobs', []):
        uid(j, 'job'); w = f'{w0}#{j.get("id")}'
        for k in ('title', 'role', 'situation', 'steps', 'takeaway'):
            if not j.get(k): err(w, f'job missing {k}')
        check_checks(w, j.get('checks'))
    if len(u.get('mcqs', [])) < 5: err(w0, 'needs 5+ MCQs')
    concept_ids = {c.get('id') for c in u.get('concepts', [])}
    for q in u.get('mcqs', []):
        uid(q, 'mcq'); check_mcq(f'{w0}#{q.get("id")}', q, concept_ids)
    if len(u.get('questions', [])) < 2: err(w0, 'needs 2+ descriptive questions')
    for q in u.get('questions', []):
        uid(q, 'question'); check_question(f'{w0}#{q.get("id")}', q)
    r = u.get('revision', {})
    for k in ('summary', 'remember', 'traps'):
        if not r.get(k): err(w0, f'revision.{k} missing')
    if len(u.get('quickref', [])) < 3: err(w0, 'quickref needs 3+ items')
    for qr in u.get('quickref', []):
        if not qr.get('k') or not qr.get('v'): err(w0, 'quickref item needs k and v')
    # viva (speak & revise): 5+ per unit; the model answer must cover 100% of the key points; reading the question back must not pass
    if len(u.get('viva', [])) < 5: err(w0, 'needs 5+ viva questions')
    for v in u.get('viva', []):
        uid(v, 'viva'); w = f'{w0}#{v.get("id")}'
        check_viva(w, v, concept_ids)
    # case-study MCQ sets: 1+ per unit, each 3-5 linked MCQs
    if len(u.get('cases', [])) < 1: err(w0, 'needs 1+ case-study MCQ set')
    for cs in u.get('cases', []):
        uid(cs, 'case'); w = f'{w0}#{cs.get("id")}'
        if not str(cs.get('case', '')).strip() or not cs.get('title'): err(w, 'case needs title and case text')
        if cs.get('difficulty') not in ('core', 'moderate', 'hard'): err(w, 'case difficulty must be core|moderate|hard')
        if not 3 <= len(cs.get('mcqs', [])) <= 5: err(w, 'a case set needs 3 to 5 linked MCQs')
        check_blocks(w + '.given', cs.get('given', []))
        for q in cs.get('mcqs', []):
            uid(q, 'case mcq'); check_mcq(f'{w}.{q.get("id")}', q, concept_ids)
            if q.get('difficulty') not in ('core', 'moderate', 'hard'): err(f'{w}.{q.get("id")}', 'difficulty must be core|moderate|hard')
    for q in u.get('mcqs', []):
        if q.get('difficulty') not in ('core', 'moderate', 'hard'): err(f'{w0}#{q.get("id")}', 'difficulty must be core|moderate|hard')
    check_topics(w0, u)
    # no leftover placeholders
    for t in text_of(u):
        if re.search(r'TODO|XXX|\blorem\b|\{\w+\}', t): err(w0, f'placeholder text: {t[:60]}')
    return u

def check_topics(w0, u):
    """every MCQ (unit and case) needs a `topic` naming a structure.json topic of its unit or one of the unit's concept-card titles,
    and an `explain` of MIN_EXPLAIN words or more. Soft (warning) rules unless --strict."""
    allowed = {norm_topic(t) for t in UNIT_TOPICS.get(u.get('id'), [])} | {norm_topic(c.get('title')) for c in u.get('concepts', [])}
    allowed.discard('')
    m = re.match(r'fnd-(p\d)', str(u.get('id', ''))); need = MIN_EXPLAIN.get(m.group(1), 35) if m else 35
    items = [(f'{w0}#{q.get("id")}', q) for q in u.get('mcqs', [])] + [(f'{w0}#{cs.get("id")}.{q.get("id")}', q) for cs in u.get('cases', []) for q in cs.get('mcqs', [])]
    missing, short = [], []
    for w, q in items:
        TOPIC_STATS['mcqs'] += 1
        t = q.get('topic')
        if not str(t or '').strip(): missing.append(q.get('id')); TOPIC_STATS['no_topic'] += 1
        elif norm_topic(t) not in allowed: TOPIC_STATS['bad_topic'] += 1; soft(w, f'topic "{t}" is neither a structure.json topic of this unit nor a concept-card title')
        n = len(re.findall(r'\S+', str(q.get('explain', ''))))
        if n < need: short.append(f'{q.get("id")}({n})'); TOPIC_STATS['short'] += 1
    if STRICT:
        for i in missing: err(f'{w0}#{i}', 'MCQ needs a topic')
        for x in short: err(f'{w0}#{x.split("(")[0]}', f'explain has {x.split("(")[1][:-1]} words — needs {need}+')
    else:
        if missing: warn(w0, f'{len(missing)}/{len(items)} MCQs have no topic (' + ', '.join(missing[:8]) + (' …' if len(missing) > 8 else '') + ')')
        if short: warn(w0, f'{len(short)}/{len(items)} MCQ explanations are under {need} words: ' + ', '.join(short[:8]) + (' …' if len(short) > 8 else ''))

# ---------- originality guard ----------
def words(s): return re.findall(r"[a-z0-9]+", s.lower())
def originality(units, src, n=10):
    texts = {}
    for f in glob.glob(os.path.join(src, 'CA - Foundation__*.txt')):
        texts[f] = words(open(f, encoding='utf-8', errors='ignore').read())
    grams = set()
    for ws in texts.values():
        for i in range(len(ws) - n + 1): grams.add(' '.join(ws[i:i + n]))
    for path, u in units:
        # the unit's official ICAI title/topic list is meant to match ICAI exactly (navigation labels), so skip those
        body = {k: v for k, v in u.items() if k not in ('title', 'topics', 'chapter_title', 'paper_title')} if isinstance(u, dict) else u
        for t in text_of(body):
            ws = words(t)
            for i in range(len(ws) - n + 1):
                g = ' '.join(ws[i:i + n])
                if g in grams:
                    err(os.path.relpath(path, ROOT), f'ORIGINALITY: {n}+ words match the ICAI text: "...{g}..."'); break

def main():
    src = None
    if '--src' in sys.argv: src = sys.argv[sys.argv.index('--src') + 1]
    built, all_ids = {}, set()
    counts = {}
    for lv in ('foundation', 'inter', 'final'):
        p = os.path.join(CA, lv, 'structure.json')
        if not os.path.exists(p): err(lv, 'structure.json missing'); continue
        s = json.load(open(p, encoding='utf-8'))
        nch = nun = 0
        for pp in s['papers']:
            if not pp.get('chapters'): err(lv, f'{pp["id"]} has no chapters')
            for c in pp['chapters']:
                nch += 1
                if c['id'] in all_ids: err(lv, f'duplicate id {c["id"]}')
                all_ids.add(c['id'])
                if not c.get('title'): err(lv, f'{c["id"]} has no title')
                for u in c['units']:
                    nun += 1
                    if u['id'] in all_ids: err(lv, f'duplicate id {u["id"]}')
                    all_ids.add(u['id'])
                    if u.get('status') not in ('built', 'soon'): err(lv, f'{u["id"]} bad status')
                    UNIT_TOPICS[u['id']] = u.get('topics') or []
                    if u.get('status') == 'built':
                        f = os.path.join(ROOT, u.get('file', ''))
                        if not os.path.exists(f): err(lv, f'{u["id"]} marked built but {u.get("file")} missing')
                        built[u['id']] = f
        counts[lv] = (len(s['papers']), nch, nun)
    units = []
    for uid_, f in built.items():
        u = check_unit(f, set(built))
        if u: units.append((f, u))
    # every unit file on disk must be listed
    for f in glob.glob(os.path.join(CA, '*', 'p*', 'ch*', 'u*.json')):
        if os.path.abspath(f) not in {os.path.abspath(x) for x in built.values()}:
            # new unit not yet in structure.json (writers run in parallel; structure is regenerated before publishing): validate it too
            u = check_unit(f, set(built)); warn(os.path.relpath(f, ROOT), 'not yet marked built in structure.json (run tools/ca_build_structure.py)')
            if u: units.append((f, u))
    # MCQ / question ids unique across units (used as keys for progress and future AI checking)
    seen = {}
    for f, u in units:
        for q in u.get('mcqs', []) + u.get('questions', []) + [m for cs in u.get('cases', []) for m in cs.get('mcqs', [])] + u.get('viva', []):
            k = f'{u["id"]}#{q["id"]}'
            if k in seen: err(f, f'duplicate global id {k}')
            seen[k] = 1
    mocks = []
    ubid = {u['id']: u for _, u in units}
    for f in sorted(glob.glob(os.path.join(CA, '*', 'mocks', '*.json'))):
        mm = check_mock(f, ubid)
        if mm: mocks.append((f, mm))
    # the JS matcher (js/ca-tools.js) must give exactly the same result as tools/ca_vivamatch.py
    try:
        import subprocess, shutil
        if shutil.which('node'):
            pairs = [[v, a] for _, u in units for v in u.get('viva', []) for a in (v['model'], v['q'], ' '.join(v['model'].split()[::2]))]
            r = subprocess.run(['node', os.path.join(ROOT, 'tools', 'ca_vivaparity.js'), os.path.join(ROOT, 'js', 'ca-tools.js')], input=json.dumps(pairs), capture_output=True, text=True, timeout=60)
            if r.returncode: err('viva parity', r.stderr.strip()[:200])
            else:
                for (v, a), (pj, hj, tj) in zip(pairs, json.loads(r.stdout)):
                    pp, hp = VM.score(v, a)
                    if pp != pj or hp != hj or VM.tokens(a) != tj: err('viva parity', f'JS and Python matchers differ on "{a[:50]}"'); break
                print(f'viva matcher parity JS = Python on {len(pairs)} answers')
        else: warn('viva parity', 'node not found — JS/Python matcher parity not checked')
    except Exception as e: err('viva parity', str(e))
    # the JS answer checker (js/ca-check.js) must give exactly the same result as check_answer() in tools/ca_vivamatch.py
    try:
        import subprocess, shutil
        if shutil.which('node') and AUTO['cases']:
            r = subprocess.run(['node', os.path.join(ROOT, 'tools', 'ca_vivaparity.js'), os.path.join(ROOT, 'js', 'ca-tools.js'), os.path.join(ROOT, 'js', 'ca-check.js')], input=json.dumps(AUTO['cases']), capture_output=True, text=True, timeout=120)
            if r.returncode: err('checker parity', r.stderr.strip()[:300])
            else:
                def canon(o):
                    if isinstance(o, bool) or o is None or isinstance(o, str): return o
                    if isinstance(o, (int, float)): return round(float(o), 6)
                    if isinstance(o, list): return [canon(x) for x in o]
                    return {k: canon(v) for k, v in sorted(o.items())}
                for (q, a), j in zip(AUTO['cases'], json.loads(r.stdout)):
                    if canon(VM.check_answer(q, a)) != canon(j): err('checker parity', f'JS and Python answer checkers differ on question {q.get("id")} ("{str(a.get("text", ""))[:40]}")'); break
                print(f'answer checker parity JS = Python on {len(AUTO["cases"])} answers')
        elif AUTO['cases']: warn('checker parity', 'node not found — JS/Python answer-checker parity not checked')
    except Exception as e: err('checker parity', str(e))
    if src: originality(units + mocks, src)
    for lv, (p, c, n) in counts.items(): print(f'{lv:10s} papers {p:2d}  chapters {c:3d}  units {n:3d}')
    nm = sum(len(u['mcqs']) for _, u in units); nq = sum(len(u['questions']) for _, u in units); ni = sum(len(u['illustrations']) for _, u in units)
    nc = sum(len(x.get('checks') or []) for _, u in units for x in u['illustrations'] + u['questions'] + u['jobs']) + sum(1 for _, u in units for q in u['mcqs'] if 'check' in q)
    print(f'built units {len(units)} · illustrations {ni} · MCQs {nm} · descriptive questions {nq} · numeric checks {nc}')
    nv = sum(len(u.get('viva', [])) for _, u in units); ncs = sum(len(u.get('cases', [])) for _, u in units); ncm = sum(len(c['mcqs']) for _, u in units for c in u.get('cases', []))
    print(f'viva questions {nv} · key points {sum(len(v["points"]) for _, u in units for v in u.get("viva", []))} · case sets {ncs} ({ncm} linked MCQs) · mock papers {len(mocks)}')
    print(f'auto-check: {AUTO["checkable"]}/{AUTO["points"]} scheme points checkable offline · {AUTO["ai_only"]} ai_only · model answer earns every offline mark in {AUTO["model_full"]} questions' + ('' if STRICT else '  (points without fields: warnings; errors with --strict)'))
    ts = TOPIC_STATS; print(f'MCQ topics: {ts["mcqs"] - ts["no_topic"]}/{ts["mcqs"]} have one, {ts["bad_topic"]} do not match · explanations under the minimum: {ts["short"]}' + ('' if STRICT else '  (warnings; errors with --strict)'))
    for x in warns: print('WARN ', x)
    for x in errors: print('ERROR', x)
    print('OK' if not errors else f'{len(errors)} error(s)')
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
