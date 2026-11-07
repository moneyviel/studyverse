#!/usr/bin/env python3
"""StudyVerse CA content checker.

Checks:
  * structure files (content/ca/<level>/structure.json): ids unique, built units have files
  * every unit file: schema, unique ids, MCQ keys, marking-scheme totals,
    journal entries balance, ledgers balance (and agree with the journal they were posted from),
    trial balances agree, table totals add up, every `check` expression re-computed,
    numeric MCQ answers re-computed (and no wrong option equal to the answer)
  * optional originality guard (--src DIR): no run of 10+ consecutive words shared with the ICAI text

Usage:  python3 tools/ca_validate.py [--src /tmp/ca/txt]      exit code 1 on any error
"""
import json, os, re, sys, glob, ast, operator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA = os.path.join(ROOT, 'content', 'ca')
errors, warns = [], []
def err(where, msg): errors.append(f'{where}: {msg}')
def warn(where, msg): warns.append(f'{where}: {msg}')

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

# ---------- unit ----------
TOP = ['schema', 'id', 'level', 'paper', 'chapter', 'title', 'outcomes', 'meta', 'concepts', 'illustrations', 'jobs', 'mcqs', 'questions', 'revision', 'quickref']

def text_of(o):
    if isinstance(o, str): return [o]
    if isinstance(o, list): return [t for x in o for t in text_of(x)]
    if isinstance(o, dict): return [t for k, v in o.items() if k not in ('id', 'expr', 't', 'schema', 'skill', 'concept', 'date') for t in text_of(v)]
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
        uid(q, 'mcq'); w = f'{w0}#{q.get("id")}'
        o = q.get('options', [])
        if len(o) != 4: err(w, 'ICAI-style MCQs have exactly 4 options')
        if len(set(map(str, o))) != len(o): err(w, 'duplicate options')
        a = q.get('answer')
        if not isinstance(a, int) or not 0 <= a < len(o): err(w, 'answer index out of range'); continue
        if not q.get('explain'): err(w, 'MCQ needs explain')
        if q.get('concept') and q['concept'] not in concept_ids: err(w, f'concept {q["concept"]} not found')
        if 'check' in q:
            try: v = calc(q['check'])
            except Exception as e: err(w, f'check cannot be evaluated: {e}'); continue
            av, aside = opt_num(o[a])
            if av is None or not close(v, av): err(w, f'ANSWER KEY WRONG: check {q["check"]} = {v}, marked "{o[a]}"')
            for i, oo in enumerate(o):
                ov, oside = opt_num(oo)
                if i != a and ov is not None and close(ov, v) and oside == aside: err(w, f'wrong option "{oo}" equals the answer')
        elif opt_num(o[a])[0] is not None and len(re.sub(r'[^0-9]', '', str(o[a]))) >= 2:
            err(w, f'numeric answer "{o[a]}" has no check expression')
    if len(u.get('questions', [])) < 2: err(w0, 'needs 2+ descriptive questions')
    for q in u.get('questions', []):
        uid(q, 'question'); w = f'{w0}#{q.get("id")}'
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
    r = u.get('revision', {})
    for k in ('summary', 'remember', 'traps'):
        if not r.get(k): err(w0, f'revision.{k} missing')
    if len(u.get('quickref', [])) < 3: err(w0, 'quickref needs 3+ items')
    for qr in u.get('quickref', []):
        if not qr.get('k') or not qr.get('v'): err(w0, 'quickref item needs k and v')
    # no leftover placeholders
    for t in text_of(u):
        if re.search(r'TODO|XXX|lorem|\{\w+\}', t): err(w0, f'placeholder text: {t[:60]}')
    return u

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
        for t in text_of(u):
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
        if os.path.abspath(f) not in {os.path.abspath(x) for x in built.values()}: err(os.path.relpath(f, ROOT), 'unit file not marked built in structure.json')
    # MCQ / question ids unique across units (used as keys for progress and future AI checking)
    seen = {}
    for f, u in units:
        for q in u.get('mcqs', []) + u.get('questions', []):
            k = f'{u["id"]}#{q["id"]}'
            if k in seen: err(f, f'duplicate global id {k}')
            seen[k] = 1
    if src: originality(units, src)
    for lv, (p, c, n) in counts.items(): print(f'{lv:10s} papers {p:2d}  chapters {c:3d}  units {n:3d}')
    nm = sum(len(u['mcqs']) for _, u in units); nq = sum(len(u['questions']) for _, u in units); ni = sum(len(u['illustrations']) for _, u in units)
    nc = sum(len(x.get('checks') or []) for _, u in units for x in u['illustrations'] + u['questions'] + u['jobs']) + sum(1 for _, u in units for q in u['mcqs'] if 'check' in q)
    print(f'built units {len(units)} · illustrations {ni} · MCQs {nm} · descriptive questions {nq} · numeric checks {nc}')
    for x in warns: print('WARN ', x)
    for x in errors: print('ERROR', x)
    print('OK' if not errors else f'{len(errors)} error(s)')
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
