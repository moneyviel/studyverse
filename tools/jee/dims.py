"""Dimension algebra for the JEE Units & Measurements unit.
Two INDEPENDENT sources for every quantity:
  TABLE - typed by hand as [M L T A K] exponents
  DEFS  - built only from defining equations, starting from the 5 base quantities
check() asserts they agree, so a typo in either one fails the build."""
from fractions import Fraction as F
B = ('M', 'L', 'T', 'A', 'K')

class D(tuple):
    def __new__(c, *e): return tuple.__new__(c, tuple(F(x) for x in (list(e) + [0] * 5)[:5]))
    def __mul__(a, b): return D(*[x + y for x, y in zip(a, b)])
    def __truediv__(a, b): return D(*[x - y for x, y in zip(a, b)])
    def __pow__(a, n): return D(*[x * F(n) for x in a])
    def fmt(a, html=True, zero=False):
        out = []
        for s, x in zip(B, a):
            if x == 0 and not (zero and s in 'MLT'): continue
            e = '' if x == 1 else (str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}')
            out.append(s + (f'^{{{e}}}' if e else ''))
        return '[' + ' '.join(out) + ']' if out else '[M^{0} L^{0} T^{0}]'

ONE = D()
TABLE = {
 'mass': D(1), 'length': D(0, 1), 'time': D(0, 0, 1), 'current': D(0, 0, 0, 1), 'temperature': D(0, 0, 0, 0, 1),
 'area': D(0, 2), 'volume': D(0, 3), 'speed': D(0, 1, -1), 'acceleration': D(0, 1, -2), 'frequency': D(0, 0, -1),
 'angular velocity': D(0, 0, -1), 'angular acceleration': D(0, 0, -2), 'density': D(1, -3),
 'momentum': D(1, 1, -1), 'impulse': D(1, 1, -1), 'force': D(1, 1, -2), 'work': D(1, 2, -2), 'energy': D(1, 2, -2),
 'power': D(1, 2, -3), 'pressure': D(1, -1, -2), 'stress': D(1, -1, -2), "Young's modulus": D(1, -1, -2),
 'energy density': D(1, -1, -2), 'strain': ONE, 'angle': ONE, 'refractive index': ONE, 'Poisson ratio': ONE,
 'torque': D(1, 2, -2), 'angular momentum': D(1, 2, -1), "Planck's constant": D(1, 2, -1), 'angular impulse': D(1, 2, -1),
 'moment of inertia': D(1, 2), 'surface tension': D(1, 0, -2), 'spring constant': D(1, 0, -2),
 'coefficient of viscosity': D(1, -1, -1), 'gravitational constant G': D(-1, 3, -2), 'gravitational potential': D(0, 2, -2),
 'latent heat': D(0, 2, -2), 'specific heat': D(0, 2, -2, 0, -1), 'heat capacity': D(1, 2, -2, 0, -1),
 'gas constant R (per mole)': D(1, 2, -2, 0, -1), 'Boltzmann constant': D(1, 2, -2, 0, -1), 'thermal conductivity': D(1, 1, -3, 0, -1),
 'Stefan constant': D(1, 0, -3, 0, -4), 'compressibility': D(-1, 1, 2), 'velocity gradient': D(0, 0, -1), 'intensity of wave': D(1, 0, -3),
 'charge': D(0, 0, 1, 1), 'electric potential': D(1, 2, -3, -1), 'electric field': D(1, 1, -3, -1), 'resistance': D(1, 2, -3, -2),
 'resistivity': D(1, 3, -3, -2), 'conductance': D(-1, -2, 3, 2), 'capacitance': D(-1, -2, 4, 2), 'inductance': D(1, 2, -2, -2),
 'magnetic field': D(1, 0, -2, -1), 'magnetic flux': D(1, 2, -2, -1), 'electric flux': D(1, 3, -3, -1),
 'permittivity ε₀': D(-1, -3, 4, 2), 'permeability μ₀': D(1, 1, -2, -2), 'magnetic intensity H': D(0, -1, 0, 1),
 'electric dipole moment': D(0, 1, 1, 1), 'magnetic dipole moment': D(0, 2, 0, 1), 'current density': D(0, -2, 0, 1),
 'surface charge density': D(0, -2, 1, 1), 'emf': D(1, 2, -3, -1), 'time constant': D(0, 0, 1), 'Rydberg constant': D(0, -1),
 'wavelength': D(0, 1), 'wave number': D(0, -1), 'pressure gradient': D(1, -2, -2), 'force per unit mass': D(0, 1, -2),
 'energy per unit mass': D(0, 2, -2), 'power per unit area': D(1, 0, -3), 'linear mass density': D(1, -1), 'torsional constant': D(1, 2, -2),
}

def _defs():
    m, l, t, i, k = TABLE['mass'], TABLE['length'], TABLE['time'], TABLE['current'], TABLE['temperature']
    d = {}
    d['area'] = l * l; d['volume'] = l * l * l; d['speed'] = l / t; d['acceleration'] = d['speed'] / t
    d['frequency'] = ONE / t; d['angular velocity'] = ONE / t; d['angular acceleration'] = d['angular velocity'] / t
    d['density'] = m / d['volume']; d['momentum'] = m * d['speed']; d['force'] = m * d['acceleration']
    d['impulse'] = d['force'] * t; d['work'] = d['force'] * l; d['energy'] = d['work']; d['power'] = d['work'] / t
    d['pressure'] = d['force'] / d['area']; d['stress'] = d['pressure']; d['strain'] = l / l; d["Young's modulus"] = d['stress'] / d['strain']
    d['energy density'] = d['energy'] / d['volume']; d['angle'] = l / l; d['refractive index'] = d['speed'] / d['speed']; d['Poisson ratio'] = ONE
    d['torque'] = d['force'] * l; d['angular momentum'] = l * d['momentum']; d['moment of inertia'] = m * l * l
    d["Planck's constant"] = d['energy'] / d['frequency']; d['angular impulse'] = d['torque'] * t
    d['surface tension'] = d['force'] / l; d['spring constant'] = d['force'] / l
    d['velocity gradient'] = d['speed'] / l; d['coefficient of viscosity'] = d['force'] / (d['area'] * d['velocity gradient'])
    d['gravitational constant G'] = d['force'] * l * l / (m * m); d['gravitational potential'] = d['energy'] / m
    d['latent heat'] = d['energy'] / m; d['specific heat'] = d['energy'] / (m * k); d['heat capacity'] = d['energy'] / k
    d['gas constant R (per mole)'] = d['pressure'] * d['volume'] / k   # PV = nRT, n counted as a pure number here
    d['Boltzmann constant'] = d['energy'] / k; d['thermal conductivity'] = d['power'] * l / (d['area'] * k)
    d['Stefan constant'] = d['power'] / (d['area'] * k ** 4); d['compressibility'] = ONE / d['pressure']
    d['intensity of wave'] = d['power'] / d['area']; d['charge'] = i * t; d['electric potential'] = d['work'] / d['charge']
    d['emf'] = d['electric potential']; d['electric field'] = d['force'] / d['charge']; d['resistance'] = d['electric potential'] / i
    d['resistivity'] = d['resistance'] * d['area'] / l; d['conductance'] = ONE / d['resistance']
    d['capacitance'] = d['charge'] / d['electric potential']; d['magnetic field'] = d['force'] / (d['charge'] * d['speed'])
    d['magnetic flux'] = d['magnetic field'] * d['area']; d['inductance'] = d['magnetic flux'] / i
    d['electric flux'] = d['electric field'] * d['area']; d['permittivity ε₀'] = d['charge'] ** 2 / (d['force'] * l * l)
    d['permeability μ₀'] = d['force'] / (i * i)          # F/L = μ0 I1 I2 /(2π d): force per length × length / I²
    d['magnetic intensity H'] = d['magnetic field'] / d['permeability μ₀']; d['electric dipole moment'] = d['charge'] * l
    d['magnetic dipole moment'] = i * d['area']; d['current density'] = i / d['area']; d['surface charge density'] = d['charge'] / d['area']
    d['time constant'] = d['resistance'] * d['capacitance']; d['wavelength'] = l; d['wave number'] = ONE / l; d['Rydberg constant'] = ONE / l
    d['pressure gradient'] = d['pressure'] / l; d['force per unit mass'] = d['force'] / m; d['energy per unit mass'] = d['energy'] / m
    d['power per unit area'] = d['power'] / d['area']; d['linear mass density'] = m / l; d['torsional constant'] = d['torque'] / d['angle']
    return d
DEFS = _defs()

def check():
    bad = [k for k in TABLE if k not in ('mass', 'length', 'time', 'current', 'temperature') and (k not in DEFS or DEFS[k] != TABLE[k])]
    assert not bad, ('dimension table and definitions disagree', [(k, TABLE[k], DEFS.get(k)) for k in bad])
    # c^2 = 1/(μ0 ε0) and Z0 = sqrt(μ0/ε0) is an impedance: two physics identities as an extra cross-check
    assert ONE / (TABLE['permeability μ₀'] * TABLE['permittivity ε₀']) == TABLE['speed'] ** 2
    assert (TABLE['permeability μ₀'] / TABLE['permittivity ε₀']) ** F(1, 2) == TABLE['resistance']
    assert TABLE['inductance'] / TABLE['resistance'] == TABLE['time'] and (TABLE['inductance'] * TABLE['capacitance']) ** F(1, 2) == TABLE['time']
    return len(TABLE)

Q = TABLE
if __name__ == '__main__': print('dimension table OK:', check(), 'quantities')
