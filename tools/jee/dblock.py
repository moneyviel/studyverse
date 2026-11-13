"""3d-series data (NCERT tables) and helpers: electron configurations of atoms/ions, unpaired electrons, spin-only
moments. Atomisation enthalpy kJ/mol; E° in V; ionisation enthalpies kJ/mol."""
import math
Z3d = {'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30}
ATOM = {'Sc': 326, 'Ti': 473, 'V': 515, 'Cr': 397, 'Mn': 281, 'Fe': 416, 'Co': 425, 'Ni': 430, 'Cu': 339, 'Zn': 126}
E2 = {'Ti': -1.63, 'V': -1.18, 'Cr': -0.90, 'Mn': -1.18, 'Fe': -0.44, 'Co': -0.28, 'Ni': -0.25, 'Cu': 0.34, 'Zn': -0.76}   # M2+/M
E32 = {'Ti': -0.37, 'V': -0.26, 'Cr': -0.41, 'Mn': 1.57, 'Fe': 0.77, 'Co': 1.97}   # M3+/M2+
IE1 = {'Sc': 631, 'Ti': 656, 'V': 650, 'Cr': 653, 'Mn': 717, 'Fe': 762, 'Co': 758, 'Ni': 737, 'Cu': 745, 'Zn': 906}
IE2 = {'Sc': 1235, 'Ti': 1309, 'V': 1414, 'Cr': 1592, 'Mn': 1509, 'Fe': 1561, 'Co': 1644, 'Ni': 1752, 'Cu': 1958, 'Zn': 1734}
IE3 = {'Sc': 2393, 'Ti': 2657, 'V': 2833, 'Cr': 2990, 'Mn': 3260, 'Fe': 2962, 'Co': 3243, 'Ni': 3402, 'Cu': 3556, 'Zn': 3837}
def d_count(m, q):
    """3d electrons of M^q+ (q ≥ 2 loses both 4s first; q = 0/1 with the Cr/Cu exceptions)"""
    z = Z3d[m] - 18
    if q == 0: return {'Cr': 5, 'Cu': 10}.get(m, z - 2)
    if q == 1: return {'Cr': 5, 'Cu': 10}.get(m, z - 2)   # M+ keeps one 4s electron (Cr+ 3d5, Cu+ 3d10)
    return z - q
def unpaired(d, low_spin=False, geom='oct'):
    if not low_spin: return d if d <= 5 else 10 - d
    t2g = min(d, 6); eg = d - t2g; return (t2g if t2g <= 3 else 6 - t2g) + (eg if eg <= 2 else 4 - eg)
def mu(n): return math.sqrt(n * (n + 2))
