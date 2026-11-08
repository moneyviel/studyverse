"""Shared helpers for the extra MCQ banks (content/ca/<level>/<paper>/bank/<unit-id>.json).

A template is a function f(r) -> dict that builds ONE question from a seeded random.Random r and
computes its answer with exact arithmetic. Keys of the dict:
  q       question text
  a       the correct option text (formatted)
  w       wrong options (distractors built from typical mistakes), at least 3 usable ones
  ex      explanation (35+ words, simple English)
  fast    the quickest exam method
  secs    target time in seconds
  d       difficulty core | moderate | hard
  topic   concept-card title of the unit (exact)
  check   arithmetic expression for numeric answers (re-evaluated by tools/ca_validate.py)
  k, data verification kind + inputs: tools/ca_bank/p3_verify.py re-solves the question independently
Templates return None when the random numbers are unsuitable; the builder then tries the next seed.
"""
from fractions import Fraction as F
import math, re

SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')


def sup(n): return str(n).translate(SUP)


def inr(n):
    """Indian grouping of an integer: 1234567 -> 12,34,567"""
    neg = n < 0; s = str(abs(int(n)))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]; parts = []
        while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ','.join(parts + [tail])
    return ('-' if neg else '') + s


def num(v, dp=2):
    """plain number, Indian grouping, at most dp decimals, trailing zeros dropped"""
    v = float(v); q = round(v, dp)
    if abs(q - round(q)) < 1e-9: return inr(int(round(q)))
    s = f'{abs(q):.{dp}f}'.rstrip('0').rstrip('.')
    w, d = s.split('.')
    return ('-' if q < 0 else '') + inr(int(w)) + '.' + d


def numf(v, dp=2):
    """number with exactly dp decimals (for money and rates that must keep the paise)"""
    q = round(float(v), dp); s = f'{abs(q):.{dp}f}'; w, d = s.split('.')
    return ('-' if q < 0 else '') + inr(int(w)) + ('.' + d if dp else '')


def rs(v, dp=2):
    """₹ amount: whole rupees without decimals, otherwise two decimals"""
    q = round(float(v), dp)
    return '₹' + (inr(int(round(q))) if abs(q - round(q)) < 1e-9 else numf(q, dp))


def pct(v, dp=2): return num(v, dp) + '%'


def fr(x):
    """Fraction -> '3/8', '-3/4', '5'"""
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def frx(x):
    """Fraction as a check expression"""
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def poly(coefs, var='x'):
    """[a_n, ..., a_0] -> '3x² − 5x + 7' (ASCII hyphen kept out of terms; minus shown as −)"""
    n = len(coefs) - 1; out = []
    for i, c in enumerate(coefs):
        p = n - i; c = F(c)
        if c == 0: continue
        sign = '-' if c < 0 else '+'; a = abs(c)
        cs = '' if (a == 1 and p > 0) else (f'({fr(a)})' if a.denominator != 1 and p > 0 else fr(a))
        term = cs + (var + (sup(p) if p > 1 else '') if p > 0 else '')
        out.append((sign, term))
    if not out: return '0'
    s = ('−' if out[0][0] == '-' else '') + out[0][1]
    for sg, t in out[1:]: s += (' − ' if sg == '-' else ' + ') + t
    return s


def signed(c, s=''):
    """'+ 3x' / '− 3x' for building expressions"""
    return ('+ ' if c >= 0 else '− ') + (fr(abs(c)) if not (abs(c) == 1 and s) else '') + s


def words(s): return len(re.findall(r'\S+', s))


ORD = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth'}


def ordn(n):
    if 10 < n % 100 < 14: return f'{n}th'
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }"
