"""Helpers for writing CA unit content in Python so that every number is computed, not typed.

A unit is written as a Python dict (see content/ca/README.md for the JSON schema).
These helpers build the JSON blocks and record a `check` for every figure they compute,
so tools/ca_validate.py can re-verify the arithmetic independently.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def inr(n):
    """Indian digit grouping: 1234567 -> 12,34,567 (used only inside prose)."""
    neg = n < 0; n = abs(n)
    s = f'{n:.2f}'.rstrip('0').rstrip('.') if isinstance(n, float) and n != int(n) else str(int(n))
    if '.' in s: whole, dec = s.split('.'); dec = '.' + dec
    else: whole, dec = s, ''
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        parts = []
        while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        whole = ','.join(parts + [tail])
    return ('-' if neg else '') + whole + dec


R = lambda n: '₹' + inr(n)


class Checks(list):
    def add(self, expr, label):
        """expr: a Python arithmetic string. Its value is stored, and the validator re-evaluates it."""
        v = eval(expr, {'__builtins__': {}}, {'round': round, 'min': min, 'max': max, 'abs': abs})
        v = round(v, 2)
        if v == int(v): v = int(v)
        self.append({'expr': expr, 'value': v, 'label': label})
        return v


def je(date, debits, credits, narr):
    """One journal entry. debits/credits: list of (account, amount)."""
    return {'date': date, 'lines': [{'ac': a, 'dr': x} for a, x in debits] + [{'ac': a, 'cr': x} for a, x in credits], 'narr': narr}


def journal(entries, title=None, bid=None):
    b = {'t': 'journal', 'entries': entries}
    if title: b['title'] = title
    if bid: b['id'] = bid
    return b


def ledgers_from(entries, accounts, opening=None, closing_label='Balance c/d', from_id=None, year_end='Mar 31', next_day='Apr 1'):
    """Builds balanced ledger accounts for `accounts` from journal entries.
    Posting rule: debit line of entry -> Dr side of that account, particulars = 'To <the credit account(s)>';
    credit line -> Cr side, particulars = 'By <the debit account(s)>'. Accounts closed with balance c/d."""
    opening = opening or {}
    out = []
    for acc in accounts:
        dr, cr = [], []
        if acc in opening:
            side, amt, date = opening[acc]
            (dr if side == 'dr' else cr).append({'date': date, 'part': 'To Balance b/d' if side == 'dr' else 'By Balance b/d', 'amt': amt, 'ob': True})
        for e in entries:
            drs = [l for l in e['lines'] if 'dr' in l]; crs = [l for l in e['lines'] if 'cr' in l]
            for l in drs:
                if l['ac'] != acc: continue
                if len(crs) == 1: dr.append({'date': e['date'], 'part': 'To ' + crs[0]['ac'], 'amt': l['dr']})
                elif len(drs) == 1: dr.extend({'date': e['date'], 'part': 'To ' + c['ac'], 'amt': c['cr']} for c in crs)
                else: dr.append({'date': e['date'], 'part': 'To Sundries', 'amt': l['dr']})
            for l in crs:
                if l['ac'] != acc: continue
                if len(drs) == 1: cr.append({'date': e['date'], 'part': 'By ' + drs[0]['ac'], 'amt': l['cr']})
                elif len(crs) == 1: cr.extend({'date': e['date'], 'part': 'By ' + d['ac'], 'amt': d['dr']} for d in drs)
                else: cr.append({'date': e['date'], 'part': 'By Sundries', 'amt': l['cr']})
        sd, sc = sum(x['amt'] for x in dr), sum(x['amt'] for x in cr)
        bal = abs(sd - sc)
        nm = acc[:-4] if acc.endswith(' A/c') else acc
        blk = {'t': 'ledger', 'ac': nm if nm.endswith('Account') else nm + ' Account', 'dr': dr, 'cr': cr}
        if bal:
            if sd > sc: cr.append({'date': year_end, 'part': 'By ' + closing_label, 'amt': bal, 'bal': True})
            else: dr.append({'date': year_end, 'part': 'To ' + closing_label, 'amt': bal, 'bal': True})
            blk['next'] = {'date': next_day, 'side': 'dr' if sd > sc else 'cr', 'amt': bal}
        if from_id: blk['from'] = from_id
        out.append(blk)
    return out


def ledger_balance(entries, acc, opening=0):
    """Signed balance (+ debit, - credit) of an account from journal entries."""
    b = opening
    for e in entries:
        for l in e['lines']:
            if l['ac'] == acc:
                b += l.get('dr', 0) - l.get('cr', 0)
    return b


def tb(rows, date, title=None, diff=None):
    """rows: list of (account, signed balance) -> trial balance block."""
    b = {'t': 'tb', 'date': date, 'rows': [{'ac': a, 'dr': v} if v > 0 else {'ac': a, 'cr': -v} for a, v in rows if v]}
    if title: b['title'] = title
    if diff is not None: b['diff'] = diff
    return b


def table(head, rows, num=None, total=False, title=None, note=None):
    b = {'t': 'table', 'head': head, 'rows': rows}
    if num: b['num'] = num
    if total: b['total'] = True
    if title: b['title'] = title
    if note: b['note'] = note
    return b


def p(text): return {'t': 'p', 'text': text}
def ul(items): return {'t': 'list', 'items': items}
def wn(title, text): return {'t': 'wn', 'title': title, 'text': text}
def note(text): return {'t': 'note', 'text': text}
def legal(provision, facts, analysis, conclusion, title=None):
    b = {'t': 'legal', 'provision': provision, 'facts': facts, 'analysis': analysis, 'conclusion': conclusion}
    if title: b['title'] = title
    return b


def minutes(marks):
    """ICAI papers: 100 marks in 180 minutes -> about 1.8 minutes per mark."""
    return max(2, round(marks * 1.8))


def write_unit(u):
    parts = u['id'].split('-')                      # int-p3-a-ch01-u01: papers split into sections keep the section in the folder (p3-a)
    lv, un, ch = parts[0], parts[-1], parts[-2]; pp = '-'.join(parts[1:-2])
    folder = {'fnd': 'foundation', 'int': 'inter', 'fin': 'final'}[lv]
    path = os.path.join(ROOT, 'content', 'ca', folder, pp, ch, un + '.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    return path
