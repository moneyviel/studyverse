"""Extra practice-MCQ banks (Papers 2 and 4): content/ca/foundation/<paper>/bank/<unit-id>.json
   = {"unit": "<unit-id>", "mcq": [MCQ objects]}  — merged into the unit's MCQs by the generic bank loader in js/ca.js.

MCQ object = the unit-file MCQ fields (id, q, options[4], answer, explain, concept, topic, difficulty, check?)
plus two optional fields: `fast` (quickest elimination / keyword trick) and `secs` (target time in seconds).
Every question is original (written for StudyVerse); numeric answers are computed here with exact
arithmetic (fractions) and stored as a `check` expression that tools/ca_validate.py-style checking re-evaluates.

Writing a question:  Q(concept_id, question, [correct, wrong1, wrong2, wrong3], explain, fast, secs=45, d='core', check=None)
The correct option is always written first; the writer rotates it to a fixed, varied position (the app shuffles anyway).
"""
import json, os
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def Q(c, q, opts, explain, fast, secs=45, d='core', check=None):
    return {'c': c, 'q': q, 'opts': opts, 'explain': explain, 'fast': fast, 'secs': secs, 'd': d, 'check': check}


def fx(v, nd=2):
    """Exact Fraction -> option text: integers plain, else rounded to nd decimals (trailing zeros dropped)."""
    v = F(v)
    if v.denominator == 1: return str(v.numerator)
    s = f'{float(v):.{nd}f}'.rstrip('0').rstrip('.')
    return s


def unit_file(uid):
    lv, pp, ch, un = uid.split('-')
    return os.path.join(ROOT, 'content', 'ca', 'foundation', pp, ch, un + '.json')


def bank_file(uid):
    lv, pp, ch, un = uid.split('-')
    return os.path.join(ROOT, 'content', 'ca', 'foundation', pp, 'bank', uid + '.json')


def make(uid, items, drop=()):
    """items -> list of MCQ dicts with ids bk01.., topic = the concept card's exact title."""
    u = json.load(open(unit_file(uid), encoding='utf-8'))
    titles = {c['id']: c['title'] for c in u['concepts']}
    out, n = [], 0
    for k, it in enumerate(items, 1):
        mid = f'bk{k:02d}'
        if mid in drop: continue                       # dropped after the independent re-answer pass (ids stay stable)
        if it['c'] not in titles: raise ValueError(f'{uid} {mid}: concept {it["c"]} not in unit')
        o = list(it['opts']); pos = (k * 3 + len(it['q'])) % 4
        correct = o[0]; rest = o[1:]; rest.insert(pos, correct) if pos < len(rest) else rest.append(correct)
        o = rest; ans = o.index(correct)
        m = {'id': mid, 'q': it['q'], 'options': o, 'answer': ans, 'explain': it['explain'], 'concept': it['c'],
             'topic': titles[it['c']], 'difficulty': it['d'], 'fast': it['fast'], 'secs': it['secs']}
        if it['check'] is not None: m['check'] = it['check']
        out.append(m)
    return out


def write(uid, items, drop=()):
    mcq = make(uid, items, drop)
    path = bank_file(uid)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'unit': uid, 'mcq': mcq}, f, ensure_ascii=False, indent=1)
    return path, len(mcq)
