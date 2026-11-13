"""Helpers for CA Final units: same as ikit, but units are tagged level 'final'."""
from ikit import *          # noqa: F401,F403  (Q, W, S, C, V, P, M, table, p, ul, note, inr, Checks, legal ...)
import ikit as _ikit


def unit(*a, **k):
    d = _ikit.unit(*a, **k)
    d['level'] = 'final'
    return d
