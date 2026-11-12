"""Tiny first-principles helpers for bonding questions: VSEPR from a formula and MO filling for diatomics.
Used as the independent checker for Chemistry Unit 3 (they compute — they don't look answers up)."""
VAL = {'H': 1, 'Be': 2, 'B': 3, 'Al': 3, 'C': 4, 'Si': 4, 'Sn': 4, 'N': 5, 'P': 5, 'As': 5, 'Sb': 5, 'O': 6, 'S': 6, 'Se': 6, 'F': 7, 'Cl': 7, 'Br': 7, 'I': 7, 'Xe': 8, 'Kr': 8}
USE = {'H': 1, 'F': 1, 'Cl': 1, 'Br': 1, 'I': 1, 'O': 2, 'S': 2, 'CH3': 1, 'OH': 1}   # electrons the central atom spends per ligand
SHAPE = {(2, 0): 'linear', (3, 0): 'trigonal planar', (2, 1): 'bent', (4, 0): 'tetrahedral', (3, 1): 'trigonal pyramidal', (2, 2): 'bent',
         (5, 0): 'trigonal bipyramidal', (4, 1): 'see-saw', (3, 2): 'T-shaped', (2, 3): 'linear', (6, 0): 'octahedral', (5, 1): 'square pyramidal', (4, 2): 'square planar',
         (7, 0): 'pentagonal bipyramidal', (6, 1): 'distorted octahedral', (5, 2): 'pentagonal planar'}
HYB = {2: 'sp', 3: 'sp^{2}', 4: 'sp^{3}', 5: 'sp^{3}d', 6: 'sp^{3}d^{2}', 7: 'sp^{3}d^{3}'}
SYM = {'linear', 'trigonal planar', 'tetrahedral', 'trigonal bipyramidal', 'octahedral', 'square planar', 'pentagonal bipyramidal', 'pentagonal planar'}
def vsepr(center, ligs, charge=0):
    """ligs: {'F': 4, 'O': 1}; returns dict(sigma, lp, steric, shape, hyb, polar)"""
    e = VAL[center] - charge - sum(USE[k] * n for k, n in ligs.items())
    assert e >= 0 and e % 2 == 0, (center, ligs, charge, e)
    lp = e // 2; sig = sum(ligs.values()); st = sig + lp; shp = SHAPE[(sig, lp)]
    polar = not (shp in SYM and len(ligs) == 1)
    if shp in ('trigonal bipyramidal',) and len(ligs) > 1: polar = True
    return dict(sigma=sig, lp=lp, steric=st, shape=shp, hyb=HYB[st], polar=polar)
ORD_LIGHT = ['s1', 's1*', 's2', 's2*', 'pi', 'pi', 's2p', 'pi*', 'pi*', 's2p*']   # ≤ 14 electrons (s–p mixing)
ORD_HEAVY = ['s1', 's1*', 's2', 's2*', 's2p', 'pi', 'pi', 'pi*', 'pi*', 's2p*']
Z = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'S': 16, 'Cl': 17}
def mo(a, b, charge=0):
    """diatomic a–b (S/Cl treated as their 2nd-period analogues O/F for the valence shell)"""
    core = 0
    za, zb = Z[a], Z[b]
    if za > 10: core += 8; za -= 8
    if zb > 10: core += 8; zb -= 8
    n = za + zb - charge; order = ORD_LIGHT if n <= 14 else ORD_HEAVY
    occ = [0] * len(order); left = n; i = 0
    while left > 0:
        if order[i] in ('pi', 'pi*'):   # Hund: fill the degenerate pair one electron each first
            j = i; pair = [i, i + 1]; take = min(left, 4)
            for k in range(take): occ[pair[k % 2]] += 1
            left -= take; i += 2
        else:
            take = min(left, 2); occ[i] += take; left -= take; i += 1
    bond = sum(o for o, nme in zip(occ, order) if not nme.endswith('*')); anti = sum(o for o, nme in zip(occ, order) if nme.endswith('*'))
    unp = sum(1 for o in occ if o == 1)
    pistar = sum(o for o, nme in zip(occ, order) if nme == 'pi*')
    return dict(bo=(bond - anti) / 2, unpaired=unp, pistar=pistar, electrons=n)
