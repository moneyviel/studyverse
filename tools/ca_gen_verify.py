#!/usr/bin/env python3
"""Independent verifier for js/ca-gen.js (CA Foundation question engine).

Runs the Node harness (tools/ca_gen_dump.js) to produce N seeded items per generator, then for every item:
  * re-computes the answer from the item's raw inputs (item.data) here in Python with Fractions — written
    separately from the JavaScript, not translated line by line — and checks options[answer] equals it;
  * checks exactly one correct option (4 distinct options, none numerically equal to the key);
  * checks every arithmetic equality written in the working ("a × b = c", "≈" for rounded results);
  * checks the last step is "Answer: <exact option text>";
  * checks Indian number formatting (1,23,456), real minus signs, marks (P1/P2 = 2, P3/P4 = 1) and unit ids;
  * for show-working (descriptive) items: the marking scheme adds up to the marks and the final figure.
Usage: python3 tools/ca_gen_verify.py [N=2000] [--gen ID] [--keep FILE]
Prints a per-generator table and exits non-zero on any failure.
"""
import ast, json, math, os, re, subprocess, sys, tempfile, collections, datetime
from fractions import Fraction as Fr
from decimal import Decimal, getcontext, ROUND_HALF_UP
from itertools import permutations
from math import comb, perm, factorial

getcontext().prec = 60
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- formatting (Indian style)
def ind(n):
    n = int(n); s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:]); head = head[:-2]
        if head: groups.insert(0, head)
        s = ','.join(groups) + ',' + tail
    return ('−' if n < 0 else '') + s

def rhalf(x, dp):                      # round half away from zero, exact
    x = Fr(x); m = 10 ** dp
    q = math.floor(abs(x) * m + Fr(1, 2))
    return Fr(q if x >= 0 else -q, m)

def fixed(x, dp):
    r = rhalf(x, dp); m = 10 ** dp; a = abs(r) * m
    assert a.denominator == 1
    a = a.numerator; i, f = divmod(a, m)
    return ('−' if r < 0 else '') + ind(i) + ('.' + str(f).zfill(dp) if dp else '')

def dp_of(x):
    x = Fr(x); d = x.denominator
    for k in range(0, 9):
        if (10 ** k) % d == 0: return k
    return None

def num(x, maxdp=4):
    x = Fr(x)
    if x.denominator == 1: return ind(x.numerator)
    k = dp_of(x)
    if k is not None and k <= maxdp: return fixed(x, k)
    return ('−' if x < 0 else '') + ind(abs(x.numerator)) + '/' + ind(x.denominator)

def fr(x):
    x = Fr(x)
    return ind(x.numerator) if x.denominator == 1 else ('−' if x < 0 else '') + ind(abs(x.numerator)) + '/' + ind(x.denominator)

def rs(x):
    x = Fr(x); assert x >= 0, 'negative money'
    if x.denominator == 1: return '₹' + ind(x.numerator)
    assert dp_of(x) is not None and dp_of(x) <= 2, 'money > 2dp'
    return '₹' + fixed(x, 2)

rs2 = lambda x: '₹' + fixed(x, 2)
rsr = lambda x: '₹' + fixed(x, 0)
rsS = lambda x: ('−' if Fr(x) < 0 else '') + rs(abs(Fr(x)))
d2 = lambda x: fixed(x, 2)
d4 = lambda x: fixed(x, 4)
r2s = lambda x: ('−' if Fr(x) < 0 else '') + fixed(abs(Fr(x)), 2)
cr = lambda x: '₹' + ind(abs(Fr(x))) + ' crore'
crS = lambda x: ('−' if Fr(x) < 0 else '') + cr(x)
PorL = lambda x: ('Profit ' if Fr(x) > 0 else 'Loss ') + rs(abs(Fr(x)))

def ratio(parts):
    parts = [Fr(p) for p in parts]; L = 1
    for p in parts: L = L * p.denominator // math.gcd(L, p.denominator)
    ints = [int(p * L) for p in parts]; g = 0
    for i in ints: g = math.gcd(g, i)
    ints = [i // g for i in ints]
    assert all(i > 0 for i in ints)
    return ' : '.join(str(i) for i in ints)

def sqrt_round(x, dp):                 # Decimal square root, then half-up rounding (independent of the JS integer method)
    x = Fr(x); v = (Decimal(x.numerator) / Decimal(x.denominator)).sqrt()
    return Fr(v.quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP))

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def dstr(d): return f'{d.day} {MONTHS[d.month - 1]} {d.year}'
def F(s): return Fr(str(s).replace('−', '-'))

# ---------------------------------------------------------------- independent answer functions (keyed by generator id)
A = {}
def gen(name):
    def deco(f): A[name] = f; return f
    return deco

# ===== Paper 1
@gen('p1_trade_cash')
def _(d, x):
    inv = Fr(d['L']) * (100 - d['t']) / 100; cd = inv * d['c'] / 100
    return rs({'paid': inv - cd, 'purch': inv, 'disc': cd}[d['ask']])

GOLD = {'start': ('Cash A/c', 'Capital A/c'), 'cashpur': ('Purchases A/c', 'Cash A/c'), 'credpur': ('Purchases A/c', '@ A/c'), 'credsale': ('@ A/c', 'Sales A/c'), 'rent': ('Rent A/c', 'Cash A/c'),
        'comm': ('Cash A/c', 'Commission Received A/c'), 'furn': ('Furniture A/c', 'Bank A/c'), 'draw': ('Drawings A/c', 'Cash A/c'), 'goodsdraw': ('Drawings A/c', 'Purchases A/c'), 'paycred': ('@ A/c', 'Cash A/c'),
        'recdebt': ('Cash A/c', '@ A/c'), 'deposit': ('Bank A/c', 'Cash A/c'), 'samples': ('Advertisement A/c', 'Purchases A/c'), 'outsal': ('Salary A/c', 'Outstanding Salary A/c'), 'dep': ('Depreciation A/c', 'Machinery A/c'),
        'retin': ('Sales Returns A/c', '@ A/c'), 'retout': ('@ A/c', 'Purchases Returns A/c'), 'baddebt': ('Bad Debts A/c', '@ A/c'), 'withdraw': ('Cash A/c', 'Bank A/c'), 'salpaid': ('Salaries A/c', 'Bank A/c')}
@gen('p1_golden')
def _(d, x):
    dr, c = GOLD[d['key']]; return f"{dr.replace('@', d['n'])} Dr. To {c.replace('@', d['n'])}"

@gen('p1_acc_class')
def _(d, x):
    ac = d['ac']
    if re.search(r'customer|supplier\)$', ac) and not re.search(r'Ltd', ac): c = 'Natural personal'
    elif re.search(r'Bank of|Ltd\.|Club', ac): c = 'Artificial personal'
    elif re.search(r'Outstanding|Prepaid|Accrued|in Advance', ac): c = 'Representative personal'
    elif re.search(r'Machinery|^Cash$|Goodwill|Land|Patents|Furniture', ac): c = 'Real'
    else: c = 'Nominal'
    return c + ' account'

@gen('p1_gst_sale')
def _(d, x):
    tv = Fr(d['V']) * (100 - d['t']) / 100; tax = tv * d['g'] / 100
    return rs({'total': tv + tax, 'cgst': tax / 2, 'igst': tax}[d['ask']])

@gen('p1_gst_setoff')
def _(d, x):
    g = d['g']; CC = SC = Fr(d['Pi']) * g / 200; IC = Fr(d['Pe']) * g / 100; OC = OS = Fr(d['Si']) * g / 200; OI = Fr(d['Se']) * g / 100
    best = None
    left_i = max(IC - OI, 0); liab_i = max(OI - IC, 0)
    cands = {Fr(0), left_i, min(left_i, max(OC - CC, 0)), max(left_i - max(OS - SC, 0), 0)}
    for xg in cands:                                      # split of balance IGST credit between CGST and SGST
        if xg < 0 or xg > left_i: continue
        c_l = max(OC - xg, 0); s_l = max(OS - (left_i - xg), 0)
        c_used = min(CC, c_l); s_used = min(SC, s_l)
        c_l -= c_used; s_l -= s_used
        i_l = max(liab_i - (CC - c_used) - (SC - s_used), 0)
        cash = c_l + s_l + i_l
        best = cash if best is None else min(best, cash)
    return rs(best)

@gen('p1_ledger_bal')
def _(d, x):
    b = d['O'] + d['s1'] + d['s2'] - d['r'] - d['dsc'] - d['rt']; return f"{rs(b)} {'Dr' if d['debtor'] else 'Cr'} balance"

TB_DR = {'Cash in hand', 'Bank balance', 'Trade receivables', 'Opening inventory', 'Purchases', 'Wages', 'Rent', 'Salaries', 'Drawings', 'Furniture', 'Machinery', 'Sales returns', 'Discount allowed', 'Carriage inwards'}
TB_CR = {'Sales', 'Trade payables', 'Bank loan', 'Commission received', 'Purchases returns', 'Discount received', 'Bills payable'}
@gen('p1_tb_capital')
def _(d, x):
    dr = sum(v for n, v, s in d['items'] if n in TB_DR); c = sum(v for n, v, s in d['items'] if n in TB_CR)
    assert all(n in TB_DR or n in TB_CR for n, v, s in d['items'])
    return rs(dr - c)

SUSP = {'sales_under': ('cr', -1), 'sales_over': ('cr', 1), 'purch_over': ('dr', 1), 'purch_under': ('dr', -1), 'disc_wrong_side': ('both', 0), 'receipt_not_posted': ('cr', -1),
        'payment_not_posted': ('dr', -1), 'two_sided': (None, 0), 'wrong_ac_same_side': (None, 0), 'omitted': (None, 0)}
@gen('p1_suspense')
def _(d, x):
    dr = cr_ = 0
    for t, v in d['errs']:
        side, s = SUSP[t]
        if side == 'dr': dr += s * v
        elif side == 'cr': cr_ += s * v
        elif side == 'both': dr -= v; cr_ += v           # posted to the wrong side
    diff = dr - cr_
    return f"{rs(abs(diff))} {'Cr' if diff > 0 else 'Dr'}"

PERR = {'cap_to_rev': 1, 'rev_to_cap': -1, 'sales_under': 1, 'purch_under': -1, 'out_omitted': -1, 'comm_personal': 1, 'draw_as_exp': 1, 'asset_to_sales': -1, 'stock_under': 1, 'wages_building': 1}
@gen('p1_rectify_profit')
def _(d, x): return rs(d['P'] + sum(PERR[t] * v for t, v in d['errs']))

@gen('p1_cashbook')
def _(d, x):
    t = d['t']; cash = d['C0'] + t['cs'] - t['dep'] + t['wd'] - t['cp'] - t['sal']; bank = d['B0'] + t['dep'] + t['chq'] - t['pay'] - t['wd']
    return rs(cash if d['ask'] == 'cash' else bank)

@gen('p1_daybook')
def _(d, x): return rs(Fr(d['L1'] * (100 - d['t1']), 100) + d['L2'] + Fr(d['L3'] * (100 - d['t3']), 100))

def brs_pb_adjust(it, fav):
    eff = {'cni': 1, 'cnc': -1, 'bc': -1, 'int': 1 if fav else -1, 'dd': -1, 'dc': 1}
    return sum(eff[k] * v for k, v in it.items())
@gen('p1_brs')
def _(d, x):
    if x['kind'] == 'desc':
        pb = (d['B'] if d['fav'] else -d['B']) + brs_pb_adjust(d['it'], d['fav'])
        return ('Balance as per Pass Book (favourable) ' if pb > 0 else 'Overdraft as per Pass Book ') + rs(abs(pb))
    start = d['B'] if d['fav'] else -d['B']; adj = brs_pb_adjust(d['it'], d['fav'])
    res = start + adj if d['dir'] == 'cb2pb' else start - adj
    return f"{rs(abs(res))} {'favourable' if res > 0 else 'overdraft'}"

@gen('p1_fifo')
def _(d, x):
    lots = [list(l) for l in d['L']]; S = d['S']
    for l in lots:                                        # issue from the earliest lots
        u = min(S, l[0]); l[0] -= u; S -= u
    return rs(sum(u * r for u, r in lots))

@gen('p1_wavg')
def _(d, x):
    L = d['L']; tu = sum(u for u, r in L); avg = Fr(sum(u * r for u, r in L), tu); return rs(avg * (tu - d['S']))

@gen('p1_nrv')
def _(d, x): return rs(sum(q * min(c, sp - sc) for n, q, c, sp, sc in d['rows']))

@gen('p1_inv_cost')
def _(d, x): return rs(Fr(d['P']) * (100 - d['t']) / 100 + d['duty'] + d['fr'])

@gen('p1_dep_slm')
def _(d, x): return rs(Fr(d['C'] + d['I'] - d['S'], d['n']) * (12 - d['off']) / 12)

@gen('p1_dep_wdv')
def _(d, x):
    b = Fr(d['C']); dep = None
    for _ in range(d['k']): dep = b * d['r'] / 100; b -= dep
    return rs(b if d['ask'] == 'wdv' else dep)

def months_between(a, b): return max(0, b - a)
@gen('p1_dep_sale')
def _(d, x):
    C, r = Fr(d['C']), d['r']; buy = d['fy'] * 12 + 3 + d['off']; sell = (d['fy'] + d['yrs'] - 1) * 12 + 3 + d['so']
    if d['method'] == 'slm':
        bv = C - C * r / 100 * months_between(buy, sell) / 12
    else:
        bv = C; y0 = d['fy']
        while True:
            fs, fe = y0 * 12 + 3, y0 * 12 + 15
            m = months_between(max(buy, fs), min(sell, fe))
            bv -= bv * r / 100 * m / 12
            if fe >= sell: break
            y0 += 1
    return PorL(d['P'] - bv)

@gen('p1_dep_change')
def _(d, x):
    carrying = Fr(d['C']) - Fr(d['C']) * d['r'] * d['k'] / 100; return rs(carrying * d['w'] / 100)

@gen('p1_dep_schedule')
def _(d, x):
    C, r = Fr(d['C']), d['r']; b = C
    for y in range(3):
        m = 12 - d['off'] if y == 0 else 12
        b -= (C if d['method'] == 'slm' else b) * r / 100 * m / 12
    return 'Closing value after 3 years ' + rs(b)

def add_months(dt, n):
    y, m = divmod(dt.month - 1 + n, 12); y += dt.year; m += 1
    last = (datetime.date(y + (m // 12), m % 12 + 1, 1) - datetime.timedelta(days=1)).day
    return datetime.date(y, m, min(dt.day, last))
@gen('p1_bill_due')
def _(d, x):
    dt = datetime.date(d['y'], d['m'] + 1, d['dd'])
    if d['kind'] == 'days': base = dt + datetime.timedelta(days=d['n'])
    elif d['kind'] == 'sight': a = d['acc']; base = add_months(datetime.date(a[0], a[1] + 1, a[2]), d['n'])
    else: base = add_months(dt, d['n'])
    due = base + datetime.timedelta(days=3)
    if d['hol']: due -= datetime.timedelta(days=1)
    return dstr(due)

@gen('p1_bill_disc')
def _(d, x):
    disc = Fr(d['Fv']) * d['r'] / 100 * (d['T'] - d['k']) / 12; return rs(d['Fv'] - disc if d['ask'] == 'net' else disc)

@gen('p1_gross_profit')
def _(d, x):
    cogs = d['OS'] + d['P'] - d['PR'] + d['CI'] + d['W'] - d['CS']; gp = d['S'] - d['SR'] - cogs
    if x['kind'] == 'desc':
        tot = [r for r in x['model'][0]['rows'] if r[0] == 'Total'][0]
        assert tot[1] == tot[3] == ind(d['S'] - d['SR'] + d['CS']), 'trading account totals'
        return 'Gross profit ' + rs(gp)
    return rs(gp)

NPADJ = {'out': -1, 'pre': 1, 'acc': 1, 'adv': -1, 'dep': -1, 'cs_omit': 1}
@gen('p1_np_adjust')
def _(d, x): return rs(d['P'] + sum(NPADJ[k] * v for k, v in d['adj']))

@gen('p1_bad_debts')
def _(d, x): return rs(d['b0'] + d['b1'] + Fr(d['D'] - d['b1']) * d['r'] / 100 - d['p0'])

@gen('p1_mfg')
def _(d, x): return rs(d['RO'] + d['RP'] + d['CP'] - d['RC'] + d['DW'] + d['FP'] + d['FR'] + d['FD'] + d['WO'] - d['WC'])

@gen('p1_npo_subs')
def _(d, x): return rs(d['Rc'] - d['a1'] - d['a2'] + d['o'] + d['a0'])

@gen('p1_npo_sports')
def _(d, x): return rs(d['so'] + (d['paid'] - d['co'] + d['cc']) - d['sc'])

@gen('p1_capital_compare')
def _(d, x): return PorL((d['A1'] - d['L1']) - (d['A0'] - d['L0']) + d['dw'] - d['add'])

@gen('p1_credit_purchases')
def _(d, x): return rs(d['C'] + d['cash'] + d['disc'] + d['ret'] + d['bd'] - d['O'])

@gen('p1_int_capital')
def _(d, x):
    r = Fr(d['r'], 100); i = d['ca'] * r + d['x'] * r * Fr(12 - d['addOff'], 12)
    if d['wd']: i -= d['y'] * r * Fr(12 - d['wOff'], 12)
    return rs(i)

IOD_M = {'begm': Fr(13, 2), 'midm': Fr(6), 'endm': Fr(11, 2), 'begq': Fr(15, 2), 'endq': Fr(9, 2)}
@gen('p1_int_drawings')
def _(d, x):
    n = 4 if d['k'].endswith('q') else 12; return rs(Fr(d['per'] * n) * d['r'] / 100 * IOD_M[d['k']] / 12)

@gen('p1_iod_product')
def _(d, x): return rs(Fr(sum(a * (12 - o) for o, a in zip(d['offs'], d['amts'])) * d['r'], 1200))

@gen('p1_appropriation')
def _(d, x):
    ia = Fr(d['ca'] * d['r'], 100); ib = Fr(d['cb'] * d['r'], 100); rem = d['NP'] - d['sal'] - ia - ib; sa = rem * d['ra'] / (d['ra'] + d['rb'])
    if x['kind'] == 'desc':
        A_, B_ = re.match(r'(\S+) and (\S+) share', x['q']).groups(); sb = rem - sa
        assert sa + sb + d['sal'] + ia + ib == d['NP']
        return f'{A_} {rs(sa)}; {B_} {rs(sb)}'
    return rs(sa if d['ask'] == 'share' else sa + d['sal'] + ia)

@gen('p1_goodwill')
def _(d, x):
    pr = list(d['pr'])
    if d['abn']: pr[d['abn'][0]] += d['abn'][1]
    avg = Fr(pr[0] + 2 * pr[1] + 3 * pr[2], 6) if d['meth'] == 'wavg' else Fr(sum(pr), len(pr))
    yp = F(d['yp']); normal = Fr(d['CE'] * d['nrr'], 100)
    g = {'avg': avg * yp, 'wavg': avg * yp, 'super': (avg - normal) * yp, 'cap_avg': avg * 100 / d['nrr'] - d['CE'], 'cap_super': (avg - normal) * 100 / d['nrr']}[d['meth']]
    return rs(g)

@gen('p1_admission_ratio')
def _(d, x):
    old = d['old']; t = sum(old); s = F(d['s'])
    if d['ask'] == 'sac': return ratio([F(g) for g in d['give']])
    if d['mode'] == 'old': new = [Fr(o, t) * (1 - s) for o in old]
    elif d['mode'] == 'equal': new = [Fr(o, t) - s / len(old) for o in old]
    else: new = [Fr(o, t) - F(g) for o, g in zip(old, d['give'])]
    return ratio(new + [s])

@gen('p1_gaining_ratio')
def _(d, x):
    o = d['old']; t = sum(o)
    nA, nB = (F(d['nA']), F(d['nB'])) if d['given'] else (Fr(o[0], o[0] + o[1]), Fr(o[1], o[0] + o[1]))
    return ratio([nA - Fr(o[0], t), nB - Fr(o[1], t)])

@gen('p1_revaluation')
def _(d, x):
    net = Fr(d['bl'] * d['bu'], 100) - Fr(d['mc'] * d['md'], 100) - Fr(d['deb'] * d['pp'], 100) - d['ol'] - d['stk']
    if d['ask'] == 'A': net = net * d['old'][0] / sum(d['old'])
    return PorL(net)

@gen('p1_retire_goodwill')
def _(d, x):
    o = d['old']; t = sum(o)
    nA, nB = (F(d['nA']), F(d['nB'])) if d['given'] else (Fr(o[0], o[0] + o[1]), Fr(o[1], o[0] + o[1]))
    gA, gB = nA - Fr(o[0], t), nB - Fr(o[1], t)
    return rs(Fr(d['G'] * o[2], t) * gA / (gA + gB))

@gen('p1_death_profit')
def _(d, x):
    base = Fr(d['pr'][2]) if d['basis'] == 'last' else Fr(sum(d['pr']), 3); return rs(base * d['off'] / 12 * d['old'][2] / sum(d['old']))

@gen('p1_realisation')
def _(d, x): return PorL(d['Rv'] - d['Bv'] + (d['Lb'] - d['Lp']) - d['e'])

@gen('p1_share_calls')
def _(d, x):
    N, p, c, H = d['N'], d['p'], d['c'], d['H']
    return rs({'callrec': (N - H) * c, 'arrears': H * c, 'total': N * (10 + p) - H * c, 'premium': N * p}[d['ask']])

@gen('p1_forfeit')
def _(d, x): return rs(d['K'] * d['x'] - d['K'] * (10 - d['z']))

@gen('p1_debentures')
def _(d, x):
    if d['ask'] == 'interest': return rs(Fr(d['N'] * 100 * d['r'], 100) * (12 - d['off']) / 12)
    return rs(d['N'] * (d['dsc'] + d['red']))

@gen('p1_bonus_right')
def _(d, x):
    if d['ask'] == 'bonus': return rs(d['S'] // d['k'] * 10)
    ex = Fr(d['MV'] * d['k'] + d['IP'], d['k'] + 1); return rs(d['MV'] - ex)

# ===== Paper 3
@gen('q_ratio')
def _(d, x):
    v = d['v']
    if v == 'divide': return rs(Fr(d['T']) * d['r'][d['who']] / sum(d['r']))
    if v == 'chain': p, q, r2, s2 = d['p'], d['q'], d['r2'], d['s2']; return ratio([p * r2, q * r2, q * s2])
    if v == 'dup':
        a, b = d['a'], d['b']; return {'duplicate': f'{a*a} : {b*b}', 'triplicate': f'{a**3} : {b**3}'}.get(d['t'], f'{a} : {b}')
    r = d['r']; return rs(Fr(d['T']) * Fr(1, r[0]) / (Fr(1, r[0]) + Fr(1, r[1])))

@gen('q_proportion')
def _(d, x):
    if d['v'] == 'fourth': return num(Fr(d['b'] * d['c'], d['a']))
    if d['v'] == 'third': return num(Fr(d['b'] ** 2, d['a']))
    r = math.isqrt(d['X'] * d['Y']); assert r * r == d['X'] * d['Y']; return num(r)

@gen('q_indices')
def _(d, x):
    if d['v'] == 'eval':
        base1, base2 = d['k'] ** d['qd'], d['j'] ** d['sd']
        v1 = round(base1 ** (1 / d['qd'])) ** d['pnum']; v2 = Fr(1, round(base2 ** (1 / d['sd'])))
        return fr(v1 * v2)
    return num(Fr(d['n'] - d['c'], d['a']))

@gen('q_logs')
def _(d, x):
    if d['v'] == 'base': return num(Fr(d['j'], d['i']))
    if d['v'] == 'given':
        l2, l3 = F('0.3010'), F('0.4771'); return fixed(d['a'] * l2 + d['b'] * l3 + d['c'] * (1 - l2), 4)
    k = d['k']; val = k ** d['e1'] * d['x1'] * k ** d['e2'] // d['x1']; e = round(math.log(val, k)); assert k ** e == val; return num(e)

@gen('q_linear')
def _(d, x):
    if d['v'] == 'solve': return num(Fr(d['dd'] - d['b'], d['a'] - d['c']))
    if d['v'] == 'ages':
        B, k, t = d['B'], d['k'], d['t']; m = Fr(k * B + t, B + t); assert m.denominator == 1; return num(Fr(t) * (m - 1) / (k - m))
    return num(Fr(d['S'] + d['D'], 2))

@gen('q_simultaneous')
def _(d, x):
    a1, b1, a2, b2 = d['a1'], d['b1'], d['a2'], d['b2']; c1 = a1 * d['x'] + b1 * d['y']; c2 = a2 * d['x'] + b2 * d['y']
    det = a1 * b2 - a2 * b1; X = Fr(c1 * b2 - c2 * b1, det); Y = Fr(a1 * c2 - a2 * c1, det)
    return num({'x': X, 'y': Y, 'sum': X + Y}[d['ask']])

@gen('q_quadratic')
def _(d, x):
    v = d['v']
    if v == 'form':
        p, q = d['r1'] + d['r2'], d['r1'] * d['r2']
        s = f"x² {'+' if p < 0 else '−'} {abs(p)}x {'−' if q < 0 else '+'} {abs(q)} = 0"
        s = re.sub(r' [+−] 0x', '', s, count=1); s = re.sub(r' [+−] 0 = 0', ' = 0', s, count=1); return s
    if v == 'roots':
        a, r1, r2 = d['a'], d['r1'], d['r2']; b, c = -a * (r1 + r2), a * r1 * r2; D = b * b - 4 * a * c; sq = math.isqrt(D); assert sq * sq == D
        roots = sorted([Fr(-b - sq, 2 * a), Fr(-b + sq, 2 * a)]); return f'{int(roots[0])}, {int(roots[1])}'.replace('-', '−')
    a, b, c = d['a'], d['b'], d['c']
    if v == 'sum': return num(Fr(-b, a))
    if v == 'prod': return num(Fr(c, a))
    s, p = Fr(-b, a), Fr(c, a); return num(s * s - 2 * p)

def feasible(d, X, Y): return X >= 0 and Y >= 0 and d['a1'] * X + d['b1'] * Y <= d['c1'] and d['a2'] * X + d['b2'] * Y <= d['c2']
@gen('q_inequality')
def _(d, x):
    if d['v'] == 'point':
        good = [o for o in x['options'] if feasible(d, *map(int, re.findall(r'\d+', o)))]
        assert len(good) == 1, f'feasible options {good}'
        return f"({d['g'][0]}, {d['g'][1]})"
    lines = [(1, 0, 0), (0, 1, 0), (d['a1'], d['b1'], d['c1']), (d['a2'], d['b2'], d['c2'])]
    best = None
    for i in range(4):
        for j in range(i + 1, 4):
            a1, b1, c1 = lines[i]; a2, b2, c2 = lines[j]; det = a1 * b2 - a2 * b1
            if det == 0: continue
            X, Y = Fr(c1 * b2 - c2 * b1, det), Fr(a1 * c2 - a2 * c1, det)
            if feasible(d, X, Y):
                z = d['p'] * X + d['q'] * Y; best = z if best is None else max(best, z)
    return num(best)

@gen('q_simple_interest')
def _(d, x):
    P, r, t = Fr(d['P']), F(d['r']), F(d['t']); si = P * r * t / 100
    return {'si': rs(si), 'amt': rs(P + si), 'rate': num(r) + '%', 'time': num(t) + ' years'}[d['v']]

@gen('q_compound_interest')
def _(d, x):
    P, r = Fr(d['P']), d['r']
    if d['v'] == 'diff': return rs2(P * Fr(r, 100) ** 2)
    m, t = d['m'], d['t']; amt = P * (1 + Fr(r, 100 * m)) ** (m * t)
    return rs2(amt - P if d['v'] == 'ci' else amt)

@gen('q_effective_rate')
def _(d, x): return fixed(((1 + Fr(d['r'], 100 * d['m'])) ** d['m'] - 1) * 100, 2) + '%'

@gen('q_annuity')
def _(d, x):
    i = Fr(d['r'], 100); n = d['n']; g = (1 + i) ** n
    if d['v'] == 'sink': return rsr(d['T'] * i / (g - 1))
    A_ = d['A']; fv = A_ * (g - 1) / i; pv = A_ * (1 - 1 / g) / i
    return rsr({'fv': fv, 'pv': pv, 'due': fv * (1 + i)}[d['v']])

@gen('q_perm')
def _(d, x):
    v = d['v']
    if v == 'npr': return num(perm(d['n'], d['r']))
    if v == 'word':
        c = collections.Counter(d['w']); val = factorial(len(d['w']))
        for k in c.values(): val //= factorial(k)
        return num(val)
    if v == 'together': return num(factorial(d['n'] - d['k'] + 1) * factorial(d['k']))
    return num(factorial(d['n'] - 1))

@gen('q_comb')
def _(d, x):
    if d['v'] == 'ncr': return num(comb(d['n'], d['r']))
    if d['v'] == 'mixed': return num(comb(d['m'], d['a']) * comb(d['w'], d['b']))
    return num(comb(d['m'] + d['w'], d['r']) - comb(d['m'], d['r']))

@gen('q_ap')
def _(d, x):
    if d['v'] == 'term': return num(d['a'] + (d['n'] - 1) * d['dd'])
    if d['v'] == 'sum': return num(sum(d['a'] + k * d['dd'] for k in range(d['n'])))
    return num(sum(v for v in range(d['lo'], d['hi'] + 1) if v % d['k'] == 0))

@gen('q_gp')
def _(d, x):
    if d['v'] == 'inf': return num(Fr(d['a']) / (1 - F(d['rq'])))
    r = F(d['r']); terms = [d['a'] * r ** k for k in range(d['n'])]
    return num(terms[-1] if d['v'] == 'term' else sum(terms))

@gen('q_sets')
def _(d, x):
    if d['v'] == 'inter': return num(d['nA'] + d['nB'] - (d['U2'] - d['N']))
    u = d['nA'] + d['nB'] - d['AB']
    return num({'union': u, 'onlyA': d['nA'] - d['AB'], 'neither': d['U2'] - u}[d['v']])

@gen('q_functions')
def _(d, x):
    f = lambda t: d['a'] * t + d['b']
    if d['v'] == 'inv': return num(Fr(d['y'] - d['b'], d['a']))
    g = lambda t: d['c'] * t * t + d['e']
    return num(f(g(d['k'])) if d['v'] == 'fog' else g(f(d['k'])))

@gen('q_limits')
def _(d, x):
    if d['v'] == 'factor':
        a, b = d['a'], d['b']; h = Fr(1, 10 ** 9)          # (x-a)(x-b)/(x-a) evaluated just beside a, then exact limit
        assert abs(((a + h - a) * (a + h - b)) / (a + h - a) - (a - b)) < Fr(1, 10 ** 6)
        return num(a - b)
    if d['v'] == 'power': return num(d['n'] * d['a'] ** (d['n'] - 1))
    return fr(Fr(d['p'], d['s']))

@gen('q_calculus')
def _(d, x):
    if d['v'] == 'deriv':
        c, k = d['c'], d['k']; return num(sum(c[i] * (3 - i) * Fr(k) ** (2 - i) for i in range(3)))
    if d['v'] == 'mc': return num(2 * d['a'] * d['qq'] + d['b'])
    cc = d['cc']; Fn = lambda t: Fr(cc[0]) * Fr(t) ** 3 / 3 + Fr(cc[1]) * Fr(t) ** 2 / 2 + cc[2] * Fr(t)
    return num(Fn(d['b']) - Fn(d['a']))

@gen('q_series')
def _(d, x):
    t, v = d['t'], d['v']; s5 = t[:5]
    if v == 'ap': dd = s5[1] - s5[0]; assert all(s5[i + 1] - s5[i] == dd for i in range(4)); nxt = s5[4] + dd
    elif v == 'gp': r = Fr(s5[1], s5[0]); assert all(Fr(s5[i + 1], s5[i]) == r for i in range(4)); nxt = s5[4] * r
    elif v == 'diff2':
        df = [s5[i + 1] - s5[i] for i in range(4)]; e = df[1] - df[0]; assert all(df[i + 1] - df[i] == e for i in range(3)); nxt = s5[4] + df[3] + e
    elif v in ('sq', 'cube'):
        p = 2 if v == 'sq' else 3; sol = [(s, c) for s in range(1, 30) for c in range(-5, 6) if all((s + i) ** p + c == s5[i] for i in range(5))]
        assert sol; s, c = sol[0]; nxt = (s + 5) ** p + c
    else:
        sol = [(m, c) for m in (2, 3) for c in range(-3, 4) if all(s5[i + 1] == s5[i] * m + c for i in range(4))]
        assert sol; m, c = sol[0]; nxt = s5[4] * m + c
    return num(nxt)

def shift(w, k): return ''.join(chr((ord(ch) - 65 + k) % 26 + 65) for ch in w)
@gen('q_coding')
def _(d, x):
    if d['v'] == 'mirror': return ''.join(chr(ord('Z') - (ord(ch) - ord('A'))) for ch in d['w2'])
    s = shift(d['w2'], d['k']); return s[::-1] if d['v'] == 'revshift' else s

def is_prime(n): return n > 1 and all(n % k for k in range(2, math.isqrt(n) + 1))
@gen('q_odd')
def _(d, x):
    test = {'prime': is_prime, 'square': lambda n: math.isqrt(n) ** 2 == n, 'cube': lambda n: round(n ** (1 / 3)) ** 3 == n, 'mult': lambda n: n % d['k'] == 0}[d['v']]
    vals = [int(o.replace(',', '')) for o in x['options']]; odd = [v for v in vals if not test(v)]
    assert len(odd) == 1, odd
    return ind(odd[0])

def dir_name(dx, dy):
    if dx == 0: return 'North' if dy > 0 else 'South'
    if dy == 0: return 'East' if dx > 0 else 'West'
    return ('North' if dy > 0 else 'South') + '-' + ('East' if dx > 0 else 'West')
@gen('q_direction')
def _(d, x):
    vec = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}; X = Y = 0
    for i, (h, k) in enumerate(d['legs']):
        if i: assert (h - d['legs'][i - 1][0]) % 4 in (1, 3)
        X += vec[h][0] * k; Y += vec[h][1] * k
    if d['ask'] == 'dist':
        r = math.isqrt(X * X + Y * Y); assert r * r == X * X + Y * Y; return f'{r} km'
    return dir_name(X, Y)

def seat_ok(p, c):
    at = p.index
    t = c[0]
    if t == 'end': return at(c[1]) in (0, len(p) - 1)
    if t == 'imleft': return at(c[1]) + 1 == at(c[2])
    if t == 'right2': return at(c[1]) == at(c[2]) + 2
    if t == 'between': return abs(at(c[1]) - at(c[2])) == 1 and abs(at(c[1]) - at(c[3])) == 1
    if t == 'notadj': return abs(at(c[1]) - at(c[2])) >= 2
    if t == 'middle': return at(c[1]) == 2
    if t == 'gap1': return abs(at(c[1]) - at(c[2])) == 2
    raise ValueError(t)
@gen('q_seating')
def _(d, x):
    sols = [p for p in permutations(d['ppl']) if all(seat_ok(list(p), c) for c in d['clues'])]
    assert len(sols) == 1, f'{len(sols)} arrangements'
    s = sols[0]
    return {'middle': s[2], 'left': s[0], 'right': s[4], 'rightof': s[s.index(d['X']) + 1] if d['X'] in s[:4] else None}[d['ask']]

def kin(P, a, b):
    """Relation of a to b, by generation offset and line of descent (independent formulation)."""
    par = lambda p: {q for q in (P[p].get('f'), P[p].get('m')) if q}
    kids = lambda p: {q for q in P if p in (P[q].get('f'), P[q].get('m'))}
    spouse = lambda p: {P[p]['sp']} if P[p].get('sp') else set()
    sibs = lambda p: {q for q in P if q != p and P[p].get('f') and P[q].get('f') == P[p].get('f')}
    up = lambda S: set().union(*[par(s) for s in S]) if S else set()
    down = lambda S: set().union(*[kids(s) for s in S]) if S else set()
    sideways = lambda S: set().union(*[sibs(s) for s in S]) if S else set()
    marry = lambda S: set().union(*[spouse(s) for s in S]) if S else set()
    male = P[a]['g'] == 'M'; w = lambda m, f: m if male else f
    B = {b}
    table = [
        (marry(B), w('husband', 'wife')), (up(B), w('father', 'mother')), (down(B), w('son', 'daughter')), (sideways(B), w('brother', 'sister')),
        (up(up(B)), w('grandfather', 'grandmother')), (down(down(B)), w('grandson', 'granddaughter')),
        (sideways(up(B)) | marry(sideways(up(B))), w('uncle', 'aunt')), (down(sideways(B)) | down(sideways(marry(B))), w('nephew', 'niece')),
        (up(marry(B)), w('father-in-law', 'mother-in-law')), (marry(down(B)), w('son-in-law', 'daughter-in-law')),
        (sideways(marry(B)) | marry(sideways(B)), w('brother-in-law', 'sister-in-law')), (down(sideways(up(B))), 'cousin')]
    for S, name in table:
        if a in S: return name
    return None
@gen('q_blood')
def _(d, x):
    P, path = d['P'], d['path']
    stm = re.findall(r'(\w) is the ([a-z-]+) of (\w)', x['q'])
    assert len(stm) == len(path) - 1
    for (p, rel, q), a, b in zip(stm, path, path[1:]):
        assert kin(P, a, b) == rel, f'statement {p} {rel} {q} false'
    return kin(P, path[0], path[-1])

def grouped(d):
    cl, f = d['cl'], d['f']; N = sum(f); h = cl[0][1] - cl[0][0]; return cl, f, N, h
@gen('q_grouped_avg')
def _(d, x):
    cl, f, N, h = grouped(d)
    if d['v'] == 'mean': return d2(Fr(sum(fi * Fr(a + b, 2) for fi, (a, b) in zip(f, cl)), N))
    if d['v'] == 'median':
        c = 0
        for i, fi in enumerate(f):
            if c + fi >= Fr(N, 2): return d2(cl[i][0] + (Fr(N, 2) - c) / fi * h)
            c += fi
    i = f.index(max(f)); f1, f0, f2 = f[i], f[i - 1], f[i + 1]
    return d2(cl[i][0] + Fr(f1 - f0, 2 * f1 - f0 - f2) * h)

@gen('q_raw_avg')
def _(d, x):
    xs = sorted(d['xs']); n = len(xs)
    if d['v'] == 'mean': return d2(Fr(sum(xs), n))
    if d['v'] == 'median': return num(Fr(xs[n // 2]) if n % 2 else Fr(xs[n // 2 - 1] + xs[n // 2], 2))
    c = collections.Counter(xs).most_common(); assert c[0][1] > c[1][1]; return num(c[0][0])

def quart(xs, p):
    s = sorted(xs); n = len(s); pos = (n + 1) * p; i = math.floor(pos)
    if i < 1: return Fr(s[0])
    if i >= n: return Fr(s[-1])
    return s[i - 1] + (pos - i) * (s[i] - s[i - 1])
@gen('q_quartile')
def _(d, x):
    q1, q3 = quart(d['xs'], Fr(1, 4)), quart(d['xs'], Fr(3, 4))
    return {'q1': num(q1), 'q3': num(q3), 'qd': num((q3 - q1) / 2), 'cqd': d2((q3 - q1) / (q3 + q1) * 100)}[d['v']]

@gen('q_dispersion')
def _(d, x):
    v = d['v']
    if v == 'lin': return num(abs(d['a']) * d['sd'])
    xs = d['xs']; n = len(xs); m = Fr(sum(xs), n); var = sum((Fr(t) - m) ** 2 for t in xs) / n
    if v == 'range': L, S = max(xs), min(xs); return d2(Fr(L - S, L + S) * 100)
    if v == 'md': return d2(sum(abs(Fr(t) - m) for t in xs) / n)
    if v == 'var': return d2(var)
    if v == 'sd': return d2(sqrt_round(var, 2))
    return d2(sqrt_round(var / (m * m) * 10000, 2)) + '%'

@gen('q_prob_dice')
def _(d, x):
    t = d['txt']; tests = [
        (r'the sum is (\d+)$', lambda a, b, k: a + b == k), (r'the sum is at least (\d+)', lambda a, b, k: a + b >= k), (r'same number', lambda a, b, k: a == b),
        (r'prime', lambda a, b, k: is_prime(a + b)), (r'product is even', lambda a, b, k: a * b % 2 == 0), (r'at least one die shows 6', lambda a, b, k: 6 in (a, b)),
        (r'difference of the numbers is (\d+)', lambda a, b, k: abs(a - b) == k)]
    for pat, fn in tests:
        m = re.search(pat, t)
        if m:
            k = int(m.group(1)) if m.groups() else None
            return fr(Fr(sum(1 for a in range(1, 7) for b in range(1, 7) if fn(a, b, k)), 36))
    raise ValueError(t)

def card_pred(t):
    face = lambda c: c[0] in ('jack', 'queen', 'king'); red = lambda c: c[1] in ('hearts', 'diamonds')
    m = re.match(r'a (\w+) or a (\w+)$', t)
    if m: r, s = m.groups(); return lambda c: c[0] == r or c[1] == s + 's'
    if t == 'a face card': return face
    if t == 'a red face card': return lambda c: face(c) and red(c)
    m = re.match(r'a black (\w+)$', t)
    if m: return lambda c: not red(c) and c[0] == m.group(1)
    m = re.match(r'neither a (\w+) nor a (\w+)$', t)
    if m: s, r = m.groups(); return lambda c: c[1] != s + 's' and c[0] != r
    if t == 'a red card or a face card': return lambda c: red(c) or face(c)
    raise ValueError(t)
DECK = [(r, s) for s in ('hearts', 'diamonds', 'clubs', 'spades') for r in ('ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king')]
@gen('q_prob_cards')
def _(d, x):
    t = d['txt']
    if d['one']: p = card_pred(t); return fr(Fr(sum(1 for c in DECK if p(c)), 52))
    face = lambda c: c[0] in ('jack', 'queen', 'king'); red = lambda c: c[1] in ('hearts', 'diamonds')
    pair = {'both are aces': lambda a, b: a[0] == b[0] == 'ace', 'both are red': lambda a, b: red(a) and red(b), 'one is a king and the other a queen': lambda a, b: {a[0], b[0]} == {'king', 'queen'},
            'both are of the same suit': lambda a, b: a[1] == b[1], 'both are face cards': lambda a, b: face(a) and face(b)}[t]
    fav = sum(1 for i in range(52) for j in range(i + 1, 52) if pair(DECK[i], DECK[j]))
    return fr(Fr(fav, comb(52, 2)))

@gen('q_prob_urn')
def _(d, x):
    r, b, g = d['r'], d['b'], d['g']; N = r + b + g
    balls = ['r'] * r + ['b'] * b + ['g'] * g; pairs = [(balls[i], balls[j]) for i in range(N) for j in range(i + 1, N)]
    test = {'bothr': lambda p: p == ('r', 'r'), 'onerb': lambda p: set(p) == {'r', 'b'}, 'atl': lambda p: 'r' in p}[d['v']]
    return fr(Fr(sum(1 for p in pairs if test(p)), len(pairs)))

@gen('q_prob_rules')
def _(d, x):
    D0 = d['D0']; pA, pB, pAB = Fr(d['a'], D0), Fr(d['b'], D0), Fr(d['ab'], D0)
    return fr({'union': pA + pB - pAB, 'cond': pAB / pB, 'neither': 1 - (pA + pB - pAB), 'onlyA': pA - pAB}[d['v']])

@gen('q_expectation')
def _(d, x):
    W = sum(d['w']); ps = [Fr(w, W) for w in d['w']]; E = sum(p * v for p, v in zip(ps, d['xs']))
    return fr(E if d['v'] == 'mean' else sum(p * v * v for p, v in zip(ps, d['xs'])) - E * E)

@gen('q_binomial')
def _(d, x):
    v = d['v']
    if v == 'findn': return num(d['N'])
    n, p = d['n'], F(d['p']); q = 1 - p
    if v == 'params': return fr(n * p if d['ask'] == 'mean' else n * p * q)
    if v == 'atl1': return fr(1 - q ** n)
    return fr(comb(n, d['r']) * p ** d['r'] * q ** (n - d['r']))

@gen('q_poisson')
def _(d, x):
    m = F(d['m']); e = F(d['e']); assert e == rhalf(Fr(math.exp(-float(m))), 4), 'e^-m value'
    P = lambda r: e * m ** r / factorial(r)
    if d['v'] == 'eq': return d4(P(d['r']))
    return d4(P(0) + P(1) if d['v'] == 'le1' else 1 - P(0))

@gen('q_karl_pearson')
def _(d, x):
    if d['v'] == 'cov': return num(F(d['r']))
    xs, ys = d['xs'], d['ys']; n = len(xs)
    sx, sy = sum(xs), sum(ys); sxy = n * sum(a * b for a, b in zip(xs, ys)) - sx * sy; sxx = n * sum(a * a for a in xs) - sx * sx; syy = n * sum(b * b for b in ys) - sy * sy
    r = sqrt_round(Fr(sxy * sxy, sxx * syy), 2)               # computational formula (not the deviation form used in JS)
    return r2s(-r if sxy < 0 else r)

@gen('q_rank_corr')
def _(d, x):
    if d['v'] == 'given': n, d2s = d['n'], d['d2s']
    else: n = len(d['r1']); d2s = sum((a - b) ** 2 for a, b in zip(d['r1'], d['r2']))
    return r2s(rhalf(1 - Fr(6 * d2s, n * (n * n - 1)), 2))

@gen('q_regression')
def _(d, x):
    v = d['v']
    if v == 'lines':
        sg = -1 if d['neg'] else 1; B, D = sg * F(d['b']), sg * F(d['dd'])
        a = d['my'] - B * d['mx']; c = d['mx'] - D * d['my']
        # solve y = a + Bx, x = c + Dy
        X = (c + D * a) / (1 - D * B); Y = a + B * X
        r2 = B * D; r = sqrt_round(r2, 6); assert r * r == r2
        return num({'r': sg * r, 'mx': X, 'my': Y}[d['ask']])
    r, sx, sy = F(d['r']), d['sx'], d['sy']
    if v == 'coef': return num(r * sy / sx if d['ask'] == 'byx' else r * sx / sy)
    return num(d['my'] + r * sy / sx * (d['x0'] - d['mx']))

@gen('q_index_numbers')
def _(d, x):
    R_ = d['rows']; S = lambda f: sum(f(r) for r in R_)
    L = Fr(S(lambda r: r['p1'] * r['q0']), S(lambda r: r['p0'] * r['q0'])) * 100; Pa = Fr(S(lambda r: r['p1'] * r['q1']), S(lambda r: r['p0'] * r['q1'])) * 100
    return d2({'L': L, 'P': Pa, 'F': sqrt_round(L * Pa, 2), 'ME': Fr(S(lambda r: r['p1'] * (r['q0'] + r['q1'])), S(lambda r: r['p0'] * (r['q0'] + r['q1']))) * 100,
               'SA': Fr(S(lambda r: r['p1']), S(lambda r: r['p0'])) * 100}[d['v']])

@gen('q_sampling')
def _(d, x):
    if d['v'] == 'se': return num(Fr(d['sd']) / math.isqrt(d['n']))
    return num(d['N'] ** d['n'] if d['v'] == 'with' else comb(d['N'], d['n']))

@gen('q_class_data')
def _(d, x):
    h, s, k = d['h'], d['s'], d['k']; lo = s + k * h; hi = lo + h - 1; gap = Fr(1, 2)
    return num({'ub': hi + gap, 'lb': lo - gap, 'mark': Fr(lo + hi, 2), 'width': h}[d['v']])

# ===== Paper 4
@gen('e_elasticity')
def _(d, x):
    P1, P2, Q1, Q2 = d['P1'], d['P2'], d['Q1'], d['Q2']
    e = (Fr(Q2 - Q1, (Q1 + Q2)) / Fr(P2 - P1, (P1 + P2))) if d['meth'] == 'arc' else (Fr(Q2 - Q1, Q1) * 100) / (Fr(P2 - P1, P1) * 100)
    return fixed(abs(e), 2) if d['kind'] == 'price' else r2s(rhalf(e, 2))

@gen('e_point_elasticity')
def _(d, x): return d2(Fr(d['b'] * d['P'], d['a'] - d['b'] * d['P']))

@gen('e_utility')
def _(d, x):
    if d['v'] == 'mu': return num(d['mu'][d['i']])
    return rs(sum(m - d['P'] for m in d['mu'] if m >= d['P']))

@gen('e_production')
def _(d, x):
    tp, L = d['tp'], d['L']; return num(rhalf(Fr(tp[L - 1], L), 2)) if d['v'] == 'ap' else num(tp[L - 1] - tp[L - 2])

@gen('e_cost')
def _(d, x):
    tc, q, T = d['tc'], d['q'], d['TFC']
    return rs2({'ac': Fr(tc[q - 1], q), 'avc': Fr(tc[q - 1] - T, q), 'afc': Fr(T, q), 'mc': Fr(tc[q - 1] - tc[q - 2])}[d['v']])

@gen('e_revenue')
def _(d, x):
    if d['v'] == 'formula': return rsS(d['AR'] * (1 - 1 / F(d['e'])))
    p, q = d['p'], d['q']; tr = lambda n: p[n - 1] * n
    return rsS(tr(q) if d['v'] == 'tr' else tr(q) - tr(q - 1))

@gen('e_profit_max')
def _(d, x):
    prof = [d['P'] * (i + 1) - c for i, c in enumerate(d['tc'])]; best = max(prof)
    assert prof.count(best) == 1, 'profit maximum not unique'
    n = prof.index(best) + 1; return f'{n} unit' + ('' if n == 1 else 's')

@gen('e_equilibrium')
def _(d, x):
    a, b, c, dd = d['a'], d['b'], d['c'], d['dd']
    if d['v'] == 'tax': return rs(Fr(a - c + dd * d['t'], b + dd))
    P = Fr(a - c, b + dd); return rs(P) if d['v'] == 'p' else num(a - b * P)

@gen('e_national_income')
def _(d, x):
    v = d['v']
    if v == 'agg':
        G, dep, nf, nit = d['G'], d['dep'], d['nf'], d['it'] - d['sb']; tg = d['tg']
        val = G + (nf if tg.startswith('GN') or tg.startswith('NN') else 0) - (dep if tg.startswith('N') else 0) - (nit if tg.endswith('FC') else 0)
        return crS(val)
    if v == 'exp': return crS(d['C'] + d['I'] + d['Gv'] + d['X'] - d['M'])
    if v == 'inc': return crS(d['W'] + d['Rn'] + d['In'] + d['Pr'] + d['Mx'] + d['nf'])
    return crS(d['O'] - d['IC'] - d['dep'] - d['nit'])

@gen('e_multiplier')
def _(d, x):
    b = F(d['mpc']); k = 1 / (1 - b)
    if d['v'] in ('k', 'mps'): return fixed(k, 2) if dp_of(k) is None or dp_of(k) > 4 else num(k)
    if d['v'] == 'dy': return cr(k * d['dI'])
    return cr((d['a'] + d['I']) * k)

@gen('e_money_multiplier')
def _(d, x):
    r = F(d['r'])
    if d['v'] == 'simple': return num(1 / r)
    if d['v'] == 'cash': c = F(d['c']); return cr((1 + c) / (r + c) * d['H'])
    return rs(d['D0'] / r - d['D0'])

@gen('e_qtm')
def _(d, x):
    if d['v'] == 'pct': return f"rises by {d['g']}%"
    P = Fr(d['M'] * d['V'], d['T'])
    return num(P) if d['v'] == 'p' else num(P * d['T'] / d['M'])

@gen('e_budget')
def _(d, x):
    RR = d['tax'] + d['ntax']; FD = d['rexp'] + d['cexp'] - RR - d['rec'] - d['dis']
    return crS({'FD': FD, 'RD': d['rexp'] - RR, 'PD': FD - d['intr']}[d['v']])

@gen('e_trade')
def _(d, x):
    if d['v'] == 'nbt': return d2(Fr(d['px'], d['pm']) * 100)
    if d['v'] == 'itt': return d2(Fr(d['px'], d['pm']) * d['qx'])
    oa, ob = Fr(d['aX'], d['aY']), Fr(d['bX'], d['bY']); return d['A'] if oa < ob else d['B']

@gen('e_tariff')
def _(d, x):
    P1 = d['Pw'] + d['t']; imp = (d['a'] - d['b'] * P1) - (d['c'] + d['dd'] * P1)
    return f'{ind(imp)} units' if d['v'] == 'imp' else rs(d['t'] * imp)

@gen('e_exchange')
def _(d, x):
    e1, e2 = Fr(d['E1'], 100), Fr(d['E2'], 100)
    ch = (e2 - e1) / e1 * 100 if d['v'] == 'usd' else ((1 / e2) - (1 / e1)) / (1 / e1) * 100
    return f"{'appreciated' if ch > 0 else 'depreciated'} by {fixed(abs(ch), 2)}%"

@gen('e_ppc')
def _(d, x): return num(d['y'][d['i'] - 1] - d['y'][d['i']])

# ---------------------------------------------------------------- generic checks
SUPMAP = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-'}
ARITH = set('0123456789.,+−-×÷/()%₹√!^ ' + ''.join(SUPMAP))
OPS = set('+−×÷/%√!') | set(SUPMAP)

def to_py(e):
    e = e.replace('₹', '').replace('−', '-').replace('×', '*').replace('÷', '/')
    e = re.sub(r'(?<=\d),(?=\d)', '', e)
    e = re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)', lambda m: '**(' + ''.join(SUPMAP[c] for c in m.group(1)) + ')', e)
    e = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', e)
    e = re.sub(r'(\d+)!', r'FACT(\1)', e).replace('^', '**')
    e = re.sub(r'√(\d+(?:\.\d+)?)', r'SQ(\1)', e).replace('√(', 'SQ(')
    e = re.sub(r'(?<![\w.])(\d+(?:\.\d+)?)', r'FR("\1")', e)
    return e

class Ev(ast.NodeVisitor):
    def ev(self, n):
        if isinstance(n, ast.Expression): return self.ev(n.body)
        if isinstance(n, ast.BinOp):
            a, b = self.ev(n.left), self.ev(n.right)
            if isinstance(n.op, ast.Add): return a + b
            if isinstance(n.op, ast.Sub): return a - b
            if isinstance(n.op, ast.Mult): return a * b
            if isinstance(n.op, ast.Div): return a / b
            if isinstance(n.op, ast.Pow):
                if isinstance(b, Fr) and b.denominator == 1 and isinstance(a, Fr): return a ** int(b)
                return float(a) ** float(b)
        if isinstance(n, ast.UnaryOp):
            v = self.ev(n.operand); return -v if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id == 'FR': return Fr(n.args[0].value)
            v = self.ev(n.args[0])
            if n.func.id == 'FACT': return Fr(math.factorial(int(v)))
            if n.func.id == 'SQ':
                v = Fr(v) if not isinstance(v, float) else v
                if isinstance(v, Fr) and v >= 0:
                    a, b = math.isqrt(v.numerator), math.isqrt(v.denominator)
                    if a * a == v.numerator and b * b == v.denominator: return Fr(a, b)
                return math.sqrt(float(v))
        raise ValueError('bad expr')

def evaluate(s):
    s = s.strip()
    if not s or not re.search(r'\d', s) or s[-1] in '+−-×÷/(' or s[0] in '×÷/)%!': return None
    try: return Ev().ev(ast.parse(to_py(s), mode='eval'))
    except Exception: return None

def has_op(s):
    s2 = re.sub(r'^\s*[−-]', '', s.strip())
    return any(c in OPS for c in s2) or bool(re.search(r'\d\s*[−-]\s*[\d(]', s2))

def tail_expr(seg):          # maximal arithmetic suffix, shortened until it parses
    i = len(seg)
    while i > 0 and seg[i - 1] in ARITH: i -= 1
    cand = seg[i:]
    if i > 0 and seg[i - 1].isalnum(): return None, None
    starts = [k for k in range(len(cand)) if (k == 0 or cand[k - 1] == ' ') and cand[k] != ' ']
    for k in starts:
        v = evaluate(cand[k:])
        if v is not None:
            if k > 0 and not has_op(cand[k:]): return None, None          # "Year 5 = ..." style labels are skipped
            return cand[k:], v
    return None, None

def head_expr(seg):          # maximal arithmetic prefix, shortened until it parses
    i = 0
    while i < len(seg) and seg[i] in ARITH: i += 1
    cand = seg[:i]
    if i < len(seg) and (seg[i].isalpha() or seg[i] in '₀₁₂') and (i == 0 or seg[i - 1] != ' '): return None, None
    ends = sorted({k for k in range(1, len(cand) + 1) if k == len(cand) or cand[k] == ' '}, reverse=True)
    for k in ends:
        v = evaluate(cand[:k])
        if v is not None: return cand[:k], v
    return None, None

def close(a, b, approx, rhs_text):
    if isinstance(a, Fr) and isinstance(b, Fr) and not approx: return a == b
    m = re.search(r'\.(\d+)\s*$', rhs_text.replace('%', '').strip()); dp = len(m.group(1)) if m else 0
    tol = 0.5 * 10 ** -dp + 1e-9 + (0.001 * abs(float(b)) if approx else 0)
    return abs(float(a) - float(b)) <= tol

def check_steps(steps):
    errs, n = [], 0
    for st in steps[:-1]:
        for piece in re.split(r'[;:]|\s→\s|, (?=[A-Za-zΣ])', st):
            parts = re.split(r'(=|≈)', piece)
            if len(parts) < 3: continue
            for i in range(0, len(parts) - 2, 2):
                lt, lv = tail_expr(parts[i]) if i == 0 else head_expr(parts[i])
                if i > 0 and lt is not None and lt.strip() != parts[i].strip(): lt = None          # middle of a chain must be all arithmetic
                rt, rv = head_expr(parts[i + 2])
                if lt is None or rt is None: continue
                if i == 0 and not has_op(lt) and not has_op(rt): continue                          # "a = b" with no working
                n += 1
                if not close(lv, rv, parts[i + 1] == '≈', rt): errs.append(f'step arithmetic: "{piece.strip()}" ({lt.strip()} vs {rt.strip()})')
    return errs, n

YEAR_OK = re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December) $')
def check_format(text):
    errs = []
    for m in re.finditer(r'(?<![\d.,])\d{1,3}(?:,\d+)+(?![\d])', text):
        tok = m.group(0)
        if not re.fullmatch(r'\d{1,2}(?:,\d{2})*,\d{3}', tok) and not re.fullmatch(r'\d{1,3},\d{3}', tok): errs.append(f'non-Indian grouping {tok}')
    for m in re.finditer(r'(?<![\d.,⁰¹²³⁴⁵⁶⁷⁸⁹])\d{4,}(?![\d,])', text):
        before = text[max(0, m.start() - 10):m.start()]; after = text[m.end():m.end() + 3]
        if YEAR_OK.search(before) or re.match(r'-\d\d', after): continue
        errs.append(f'bare number {m.group(0)}')
    if re.search(r'(^|[\s(=:,×÷+])-\d', text): errs.append('ASCII hyphen used as minus')
    if re.search(r'undefined|NaN|null|Infinity|\[object', text): errs.append('bad token')
    return errs

def numeric_value(o):
    s = o.replace('₹', '').replace(',', '').replace('−', '-').replace(' crore', '').replace(' units', '').replace(' km', '').replace(' years', '').replace('%', '')
    tag = re.sub(r'[-\d./ ]', '', s)
    ms = re.findall(r'-?\d+(?:\.\d+)?(?:/\d+)?', s)
    if len(ms) != 1: return None
    m = re.search(r'-?\d+(?:\.\d+)?(?:/\d+)?', s)
    try: return tag, Fr(m.group(0))
    except Exception: return None

def main():
    args = sys.argv[1:]; N = 2000; only = None; keep = None
    if args and args[0].isdigit(): N = int(args.pop(0))
    if '--gen' in args: only = args[args.index('--gen') + 1]
    if '--keep' in args: keep = args[args.index('--keep') + 1]
    struct = json.load(open(os.path.join(ROOT, 'content/ca/foundation/structure.json')))
    unit_ids = {u['id'] for p in struct['papers'] for c in p['chapters'] for u in c['units']}
    out = keep or tempfile.mktemp(suffix='.jsonl', dir='/tmp')
    cmd = ['node', os.path.join(ROOT, 'tools/ca_gen_dump.js'), str(N), out] + ([only] if only else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr); sys.exit(2)
    meta = json.loads(r.stderr.strip().splitlines()[-1])
    stats = collections.OrderedDict(); fails = collections.defaultdict(list); nsteps = 0; texts = collections.defaultdict(set)
    for line in open(out):
        x = json.loads(line); g = x['gen']; key = g + (':desc' if x['kind'] == 'desc' else '')
        st = stats.setdefault(key, {'n': 0, 'bad': 0, 'units': set(x['units'])}); st['n'] += 1
        e = []
        if g not in A: e.append('no independent checker')
        for u in x['units']:
            if u not in unit_ids: e.append(f'unknown unit {u}')
        if x['difficulty'] not in ('easy', 'moderate', 'ICAI'): e.append('difficulty')
        if not x.get('concept'): e.append('concept missing')
        try:
            exp = A[g](x['data'], x) if g in A else None
        except Exception as ex:
            exp = None; e.append(f'checker error: {ex!r}')
        if x['kind'] == 'mcq':
            o = x['options']
            if len(o) != 4 or len(set(o)) != 4: e.append('options not 4 distinct')
            if not (0 <= x['answer'] < 4): e.append('answer index')
            key_txt = o[x['answer']]
            if exp is not None and key_txt != exp: e.append(f'KEY MISMATCH: keyed "{key_txt}" but recomputed "{exp}"')
            if exp is not None and o.count(exp) != 1: e.append('correct value not exactly once')
            kv = numeric_value(key_txt)
            if kv:
                for j, oo in enumerate(o):
                    if j != x['answer'] and numeric_value(oo) == kv: e.append(f'option {oo} equals key numerically')
            if x['steps'][-1] != 'Answer: ' + key_txt: e.append('last step is not the answer')
            want = 2 if x['paper'] in ('p1', 'p2') else 1
            if x['marks'] != want: e.append('marks')
            for t in [x['q'], x['explain'], *o, *x['steps']]: e += check_format(t)
            se, ns = check_steps(x['steps']); e += se; nsteps += ns
            texts[g].add(x['q'] + '|' + '|'.join(sorted(o)))
        else:
            if abs(sum(p['m'] for p in x['scheme']) - x['marks']) > 1e-9: e.append('scheme marks do not add up')
            if exp is not None and x['answer'] != exp: e.append(f'DESC MISMATCH: "{x["answer"]}" vs "{exp}"')
            if not x['model']: e.append('no model answer')
            for t in [x['q'], *x['steps'], x['answer']]: e += check_format(t)
            se, ns = check_steps(x['steps'] + ['Answer']); e += se; nsteps += ns
        if e:
            st['bad'] += 1
            if len(fails[key]) < 4: fails[key].append((x['id'], e[:3], x['q'][:160]))
    total = sum(s['n'] for s in stats.values()); bad = sum(s['bad'] for s in stats.values())
    print(f"{'generator':<26}{'unit(s)':<44}{'items':>7}{'unique':>9}{'fail':>6}")
    for k, s in stats.items():
        g = k.split(':')[0]
        print(f"{k:<26}{', '.join(sorted(s['units'])):<44}{s['n']:>7}{(len(texts[g]) if not k.endswith(':desc') else '-'):>9}{s['bad']:>6}")
    for k, fl in fails.items():
        print('\nFAIL', k)
        for i, e, q in fl: print('  ', i, e, '|', q)
    gens = len({k.split(':')[0] for k in stats})
    print(f"\nGenerators: {gens} (harness reports {meta['generators']}); items checked: {total}; arithmetic equalities checked in working: {nsteps}; failures: {bad}; generation failures: {meta['failed']}")
    if not keep: os.remove(out)
    sys.exit(1 if bad or meta['failed'] or gens < 60 else 0)

if __name__ == '__main__':
    main()
