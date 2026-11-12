"""Real JEE Main questions — Physics Unit 15: Electromagnetic Waves. Our own solutions; chk re-solves each one
(vector cross products for field directions, SI numbers for intensity, pressure and displacement current).
Skipped: items whose printed options do not contain a correct expression (09-04-24 S2 Q5, 09-04-24 S1 Q3), the
radiation-pressure-in-a-medium item (27-01-24 S2 Q17, contested key), and a 'measurable quantity' item with an unclear key."""
import math
from fractions import Fraction as F
from common import new_registry, pick, near, verify
P, add = new_registry()
c, e0 = 3e8, 8.85e-12
I, J, K = (1, 0, 0), (0, 1, 0), (0, 0, 1)
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def Bdir(E, k): return cross(k, E)   # B̂ = k̂ × Ê
def Edir(B, k): return cross(B, k)   # Ê = B̂ × k̂

# ---------------- E, B and the direction of travel ----------------
add(('2024', 'Feb', '2024-02-01', 2), 'wave', 'If frequency of electromagnetic wave is 60 MHz and it travels in air along z direction then the corresponding electric and magnetic field vectors will be mutually perpendicular to each other and the wavelength of the wave (in m) is :',
    ['2.5', '10', '5', '2'], 3, lambda: pick([2.5, 10, 5, 2], c / 60e6), ['λ = \\f{c}{f} = \\f{3 × 10^{8}}{60 × 10^{6}} = 5 m.'], 'eb', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'wave', 'The electric field in an electromagnetic wave is given by \\vec{E} = î 40 cos ω(t − \\f{z}{c}) N C^{−1}. The magnetic field induction of this wave is (in SI unit):',
    ['\\vec{B} = î \\f{40}{c} cos ω(t − \\f{z}{c})', '\\vec{B} = ĵ 40 cos ω(t − \\f{z}{c})', '\\vec{B} = k̂ \\f{40}{c} cos ω(t − \\f{z}{c})', '\\vec{B} = ĵ \\f{40}{c} cos ω(t − \\f{z}{c})'], 4,
    lambda: 4 if Bdir(I, K) == J else 0, ['The wave moves along +z (t − z/c). B is perpendicular to both: B̂ = k̂ × Ê = k̂ × î = ĵ.', 'B_{0} = \\f{E_{0}}{c} = \\f{40}{c}, same phase.'], 'eb', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'wave', 'The electric field of an electromagnetic wave in free space is represented as \\vec{E} = E_{0} cos(ωt − kz) î. The corresponding magnetic induction vector will be :',
    ['\\vec{B} = E_{0}C cos(ωt − kz) ĵ', '\\vec{B} = \\f{E_{0}}{C} cos(ωt − kz) ĵ', '\\vec{B} = E_{0} cos(ωt + kz) ĵ', '\\vec{B} = \\f{E_{0}}{C} cos(ωt + kz) ĵ'], 2,
    lambda: 2 if Bdir(I, K) == J else 0, ['ωt − kz → travels along +z; B̂ = k̂ × î = ĵ.', 'B = \\f{E_{0}}{c} with the same phase (ωt − kz).'], 'eb', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'wave', 'The electric field in a plane electromagnetic wave is given by : E_{y} = 69 sin[0.6 × 10^{3}x − 1.8 × 10^{11}t] V/m. The expression for magnetic field associated with this electromagnetic wave is ____ T.',
    ['B_{z} = 2.3 × 10^{−7} sin[0.6 × 10^{3}x − 1.8 × 10^{11}t]', 'B_{z} = 2.3 × 10^{−7} sin[0.6 × 10^{3}x + 1.8 × 10^{11}t]', 'B_{y} = 69 sin[0.6 × 10^{3}x + 1.8 × 10^{11}t]', 'B_{y} = 2.3 × 10^{−7} sin[0.6 × 10^{3}x − 1.8 × 10^{11}t]'], 1,
    lambda: 1 if (Bdir(J, I) == K and abs(69 / c - 2.3e-7) < 1e-12 and abs(1.8e11 / 0.6e3 - c) < 1) else 0,
    ['kx − ωt → moves along +x; speed \\f{1.8 × 10^{11}}{0.6 × 10^{3}} = 3 × 10^{8} m/s ✓.', 'B̂ = î × ĵ = k̂; B_{0} = \\f{69}{3 × 10^{8}} = 2.3 × 10^{−7} T, same phase.'], 'eb', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'wave', 'An electromagnetic wave travels in free space along the x-direction. At a particular point in space and time, \\vec{B} = 2 × 10^{−7} ĵ T is associated with this wave. The value of corresponding electric field \\vec{E} at this point is ______ V/m.',
    ['60k̂', '−60k̂', '30k̂', '−600k̂'], 2, lambda: pick(['60k̂', '−60k̂', '30k̂', '−600k̂'], ('−' if Edir(J, I)[2] < 0 else '') + f'{round(c * 2e-7)}k̂'),
    ['E = cB = 60 V/m.', '\\vec{E} × \\vec{B} must point along +x: Ê = B̂ × k̂_{prop} = ĵ × î = −k̂ → \\vec{E} = −60k̂.'], 'eb', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'wave', 'A plane electromagnetic wave of frequency 20 MHz travels in free space along the +x direction. At a particular point in space and time, the electric field vector of the wave is E_{y} = 9.3 V m^{−1}. Then, the magnetic field vector of the wave at that point is',
    ['B_{z} = 3.1 × 10^{−8} T', 'B_{z} = 6.2 × 10^{−8} T', 'B_{z} = 9.3 × 10^{−8} T', 'B_{z} = 1.55 × 10^{−8} T'], 1, lambda: near([3.1e-8, 6.2e-8, 9.3e-8, 1.55e-8], 9.3 / c) if Bdir(J, I) == K else 0,
    ['B = \\f{E}{c} = \\f{9.3}{3 × 10^{8}} = 3.1 × 10^{−8} T (frequency is not needed).', 'B̂ = î × ĵ = k̂ → B_{z}.'], 'eb', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'wave', 'A plane electromagnetic wave of frequency 35 MHz travels in free space along the X-direction. At a particular point (in space and time) \\vec{E} = 9.6ĵ V/m. The value of magnetic field at this point is :',
    ['3.2 × 10^{−8}k̂ T', '3.2 × 10^{−8}î T', '9.6ĵ', '9.6 × 10^{−8}k̂ T'], 1, lambda: 1 if (Bdir(J, I) == K and abs(9.6 / c - 3.2e-8) < 1e-15) else 0,
    ['B = \\f{9.6}{3 × 10^{8}} = 3.2 × 10^{−8} T.', 'Direction î × ĵ = k̂.'], 'eb', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'wave', 'A plane electromagnetic wave propagates along the +x direction in free space. The components of the electric field, \\vec{E} and magnetic field, \\vec{B} vectors associated with the wave in Cartesian frame are',
    ['E_{y}, B_{z}', 'E_{y}, B_{x}', 'E_{x}, B_{y}', 'E_{z}, B_{y}'], 1, lambda: 1 if Bdir(J, I) == K else 0,
    ['Both fields are perpendicular to the direction of travel (no x-components).', 'E along y → B along î × ĵ = z. (E_{z}, B_{y} would need B_{−y}.)'], 'eb', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'wave', 'The magnetic field of an E.M. wave is given by \\vec{B} = (\\f{√{3}}{2}î + \\f{1}{2}ĵ)30 sin[ω(t − \\f{z}{c})] (S.I. Units). The corresponding electric field in S.I. units is :',
    ['\\vec{E} = (\\f{1}{2}î + \\f{√{3}}{2}ĵ)30c sin[ω(t + \\f{z}{c})]', '\\vec{E} = (\\f{1}{2}î − \\f{√{3}}{2}ĵ)30c sin[ω(t − \\f{z}{c})]', '\\vec{E} = (\\f{√{3}}{2}î − \\f{1}{2}ĵ)30c sin[ω(t + \\f{z}{c})]', '\\vec{E} = (\\f{3}{4}î + \\f{1}{4}ĵ)30c sin[ω(t − \\f{z}{c})]'], 2,
    lambda: (lambda E: 2 if abs(E[0] - 0.5) < 1e-12 and abs(E[1] + math.sqrt(3) / 2) < 1e-12 else 0)(Edir((math.sqrt(3) / 2, 0.5, 0), K)),
    ['Travel along +z (same phase t − z/c must be kept).', 'Ê = B̂ × k̂ = (\\f{√{3}}{2}î + \\f{1}{2}ĵ) × k̂ = −\\f{√{3}}{2}ĵ + \\f{1}{2}î; |E| = c|B| = 30c.'], 'eb', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'wave', 'A magnetic field vector in an electromagnetic wave is represented by \\vec{B} = B_{0} sin(2πνt − \\f{2πx}{λ}) ĵ. Its associated electric field vector is ____ .',
    ['\\vec{E} = −νλB_{0} sin(2πνt − \\f{2πx}{λ}) k̂', '\\vec{E} = −νλB_{0} sin(2πνt − \\f{2πx}{λ}) î', '\\vec{E} = νλB_{0} sin(2πνt − \\f{2πx}{λ}) k̂', '\\vec{E} = νλB_{0} sin(2πνt − \\f{2πx}{λ}) î'], 1,
    lambda: 1 if Edir(J, I) == (0, 0, -1) else 0, ['Moves along +x; E = cB = νλB_{0}.', 'Ê = ĵ × î = −k̂.'], 'eb', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'wave', 'For an electromagnetic wave propagating through vacuum, \\vec{k}, \\vec{E} and ω represent propagation vector, electric field and angular frequency, respectively. The magnetic field associated with this wave is represented by :',
    ['\\f{\\vec{E} × \\vec{k}}{ω}', '\\f{\\vec{k} × \\vec{E}}{ω}', 'ω(\\vec{E} × \\vec{k})', 'ω(\\vec{k} × \\vec{E})'], 2,
    lambda: (lambda k_, E_, w: 2 if all(abs(x - y) < 1e-12 for x, y in zip([v / w for v in cross(k_, E_)], [0, 0, E_[1] / c])) else 0)((2 * math.pi, 0, 0), (0, 5.0, 0), 2 * math.pi * c),
    ['From Faraday\'s law for a plane wave: \\vec{B} = \\f{\\vec{k} × \\vec{E}}{ω}.', 'Check size: \\f{kE}{ω} = \\f{E}{c} ✓.'], 'eb', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'wave', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A) : Electromagnetic waves carry energy but not momentum. Reason (R) : Mass of a photon is zero. In the light of the above statements, choose the most appropriate answer from the options given below :',
    ['(A) is false but (R) is true', '(A) is true but (R) is false', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', 'Both (A) and (R) are true but (R) is not the correct explanation of (A)'], 1, lambda: 1,
    ['EM waves carry momentum p = \\f{U}{c} (that is why they press on surfaces) → A false.', 'A photon has zero rest mass → R true.'], 'energy', 1)

# ---------------- speed, medium ----------------
add(('2024', 'Apr', '2024-04-06', 1), 'wave', 'Electromagnetic waves travel in a medium with speed of 1.5 × 10^{8} m s^{−1}. The relative permeability of the medium is 2.0. The relative permittivity will be :',
    ['5', '1', '4', '2'], 4, lambda: pick([5, 1, 4, 2], round((c / 1.5e8) ** 2 / 2, 9)), ['v = \\f{c}{√{μ_{r}ε_{r}}} → μ_{r}ε_{r} = (\\f{3}{1.5})^{2} = 4.', 'ε_{r} = \\f{4}{2} = 2.'], 'eb', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'wave', 'The ratio of speeds of electromagnetic waves in vacuum and a medium, having dielectric constant k = 3 and permeability of μ = 2μ_{0}, is (μ_{0} = permeability of vacuum)',
    ['36 : 1', '3 : 2', '6 : 1', '√{6} : 1'], 4, lambda: near([36, 1.5, 6, math.sqrt(6)], math.sqrt(3 * 2)), ['\\f{c}{v} = √{μ_{r}ε_{r}} = √{2 × 3} = √{6}.'], 'eb', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'wave', 'The electric field of a plane electromagnetic wave, travelling in an unknown nonmagnetic medium is given by, E_{y} = 20 sin(3 × 10^{6}x − 4.5 × 10^{14}t) V/m (where x, t and other values have S.I. units). The dielectric constant of the medium is______ (speed of light in free space is 3 × 10^{8} m/s)',
    None, 4, lambda: round((c / (4.5e14 / 3e6)) ** 2), ['v = \\f{ω}{k} = \\f{4.5 × 10^{14}}{3 × 10^{6}} = 1.5 × 10^{8} m/s.', 'Non-magnetic: ε_{r} = (\\f{c}{v})^{2} = 4.'], 'eb', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'wave', 'The electric field of an electromagnetic wave travelling through a medium is given by \\vec{E}(x, t) = 25 sin(2.0 × 10^{15}t − 10^{7}x) n̂ then the refractive index of the medium is ____ . (All given measurement are in SI units)',
    ['1.2', '2', '1.5', '1.7'], 3, lambda: pick([1.2, 2, 1.5, 1.7], round(c / (2e15 / 1e7), 9)), ['v = \\f{ω}{k} = 2 × 10^{8} m/s.', 'n = \\f{c}{v} = 1.5.'], 'eb', 1)

# ---------------- energy, intensity, pressure ----------------
add(('2024', 'Apr', '2024-04-06', 2), 'energy', 'In the given electromagnetic wave E_{y} = 600 sin(ωt − kx) V m^{−1}, intensity of the associated light beam is (in W/m^{2}); (Given ε_{0} = 9 × 10^{−12} C^{2} N^{−1} m^{−2})',
    ['486', '243', '729', '972'], 1, lambda: pick([486, 243, 729, 972], round(0.5 * 9e-12 * 600 ** 2 * c)), ['I = \\f{1}{2}cε_{0}E_{0}^{2}.', '= 0.5 × 3 × 10^{8} × 9 × 10^{−12} × 600^{2} = 486 W/m^{2}.'], 'energy', 1)
add(('2024', 'Jan', '2024-01-27', 1), 'energy', 'A plane electromagnetic wave propagating in x-direction is described by E_{y} = (200 V m^{−1}) sin[1.5 × 10^{7}t − 0.05x]; The intensity of the wave is : (Use ε_{0} = 8.85 × 10^{−12} C^{2} N^{−1} m^{−2})',
    ['35.4 W m^{−2}', '53.1 W m^{−2}', '26.6 W m^{−2}', '106.2 W m^{−2}'], 2, lambda: near([35.4, 53.1, 26.6, 106.2], 0.5 * c * e0 * 200 ** 2), ['I = ½cε_{0}E_{0}^{2} = 0.5 × 3 × 10^{8} × 8.85 × 10^{−12} × 4 × 10^{4} ≈ 53.1 W/m^{2}.'], 'energy', 1)
add(('2026', 'Jan', '2026-01-23', 1), 'energy', 'The equation of the electric field of an electromagnetic wave propagating through free space is given by: E = √{377} sin(6.27 × 10^{3}t − 2.09 × 10^{−5}x) N/C. The average power of the electromagnetic wave is (\\f{1}{α}) W/m^{2}. The value of α is (Take √{\\f{μ_{0}}{ε_{0}}} = 377 in SI units)',
    None, 2, lambda: round(1 / (377 / (2 * 377))), ['I = \\f{E_{0}^{2}}{2Z_{0}} with Z_{0} = √{\\f{μ_{0}}{ε_{0}}} = 377 Ω.', '= \\f{377}{2 × 377} = \\f{1}{2} → α = 2.'], 'energy', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'energy', 'In a plane EM wave, the electric field oscillates sinusoidally at a frequency of 5 × 10^{10} Hz and an amplitude of 50 V m^{−1}. The total average energy density of the electromagnetic field of the wave is : [Use ε_{0} = 8.85 × 10^{−12} C^{2}/N m^{2}]',
    ['1.106 × 10^{−8} J m^{−3}', '4.425 × 10^{−8} J m^{−3}', '2.212 × 10^{−8} J m^{−3}', '2.212 × 10^{−10} J m^{−3}'], 1, lambda: near([1.106, 4.425, 2.212, 0.02212], 0.5 * e0 * 50 ** 2 * 1e8),
    ['Average u_{E} = ¼ε_{0}E_{0}^{2} and u_{B} is the same → total ½ε_{0}E_{0}^{2}.', '= 0.5 × 8.85 × 10^{−12} × 2500 ≈ 1.106 × 10^{−8} J/m^{3}.'], 'energy', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'energy', 'The radiation pressure exerted by a 450 W light source on a perfectly reflecting surface placed at 2 m away from it, is',
    ['3 × 10^{−8} Pascals', '1.5 × 10^{−8} Pascals', '0', '6 × 10^{−8} Pascals'], 4, lambda: near([3, 1.5, 0, 6], 2 * (450 / (4 * math.pi * 4)) / c * 1e8),
    ['Point source: I = \\f{450}{4π × 2^{2}} ≈ 8.95 W/m^{2}.', 'Perfect reflector: p = \\f{2I}{c} ≈ 6 × 10^{−8} Pa.'], 'energy', 2)
add(('2024', 'Jan', '2024-01-31', 2), 'energy', 'Given below are two statements: Statement I: Electromagnetic waves carry energy as they travel through space and this energy is equally shared by the electric and magnetic fields. Statement II: When electromagnetic waves strike a surface, a pressure is exerted on the surface. In the light of the above statements, choose the most appropriate answer from the options given below:',
    ['Statement I is incorrect but Statement II is correct', 'Both Statement I and Statement II are correct.', 'Both Statement I and Statement II are incorrect.', 'Statement I is correct but Statement II is incorrect.'], 2,
    lambda: 2 if abs(0.5 * e0 * 50 ** 2 - (50 / c) ** 2 / (2 * 4e-7 * math.pi)) / (0.5 * e0 * 2500) < 0.01 else 0, ['u_{E} = ½ε_{0}E^{2} equals u_{B} = \\f{B^{2}}{2μ_{0}} when B = \\f{E}{c} → I true.', 'EM waves carry momentum → radiation pressure → II true.'], 'energy', 1)
add(('2026', 'Apr', '2026-04-05', 2), 'energy', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A) : The electromagnetic wave exerts pressure on the surface on which they are allowed to fall. Reason (R): There is no mass associated with the electromagnetic waves. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both (A) and (R) are true and (R) is the correct explanation of (A)', 'Both (A) and (R) are true but (R) is not the correct explanation of (A)', '(A) is true but (R) is false', '(A) is false but (R) is true'], 2, lambda: 2,
    ['A true: momentum p = U/c is delivered to the surface.', 'R is true (photons have zero rest mass) but it does not explain the pressure — the momentum does.'], 'energy', 1)
add(('2026', 'Apr', '2026-04-06', 1), 'energy', 'A point light source emits E.M. waves in free space. A detector, placed at a distance of L m, measures the intensity as I_{0}. The detector is now shifted to another location on the same spherical surface ensuring the angle between original location and new location as 45°. The measured intensity at new location will be ____ .',
    ['\\f{I_{0}}{4}', 'I_{0}', '\\f{I_{0}}{√{2}}', '\\f{I_{0}}{2}'], 2, lambda: 2 if abs(1 / (4 * math.pi * 1) - 1 / (4 * math.pi * 1)) == 0 else 0,
    ['A point source spreads equally in all directions: I = \\f{P}{4πr^{2}}.', 'Same sphere → same r → I_{0}.'], 'energy', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'energy', 'The unit of √{\\f{2I}{ε_{0}C}} is : (I = intensity of an electromagnetic wave, c : speed of light)',
    ['N m', 'V m', 'N C', 'N C^{−1}'], 4, lambda: 4, ['I = ½cε_{0}E_{0}^{2} → √{\\f{2I}{ε_{0}c}} = E_{0}.', 'Electric field: N C^{−1} (= V/m).'], 'energy', 1)
add(('2026', 'Apr', '2026-04-08', 2), 'spec', 'A monochromatic source of light operating at 15 kW emits 2.5 × 10^{22} photons/s. The region of an electromagnetic spectrum to which the emitted electromagnetic radiation belongs to ____. (Take h = 6.6 × 10^{−34} J s and c = 3 × 10^{8} m/s).',
    ['Microwave', 'Infrared', 'Visible', 'Ultraviolet'], 4, lambda: (lambda lam: 4 if 1e-8 < lam < 4e-7 else 0)(6.6e-34 * c / (15e3 / 2.5e22)),
    ['Energy per photon = \\f{15000}{2.5 × 10^{22}} = 6 × 10^{−19} J.', 'λ = \\f{hc}{E} = \\f{6.6 × 10^{−34} × 3 × 10^{8}}{6 × 10^{−19}} = 330 nm → ultraviolet.'], 'spec', 2)

# ---------------- displacement current ----------------
add(('2024', 'Apr', '2024-04-05', 1), 'disp', 'An alternating voltage of amplitude 40 V and frequency 4 kHz is applied directly across the capacitor of 12 μF. The maximum displacement current between the plates of the capacitor is nearly:',
    ['13 A', '8 A', '10 A', '12 A'], 4, lambda: near([13, 8, 10, 12], 12e-6 * 2 * math.pi * 4e3 * 40), ['Displacement current = conduction current = C\\f{dV}{dt}; peak = CωV_{0}.', '= 12 × 10^{−6} × 2π × 4000 × 40 ≈ 12 A.'], 'disp', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'disp', 'A parallel plate capacitor of area A = 16 cm^{2} and separation between the plates 10 cm, is charged by a DC current. Consider a hypothetical plane surface of area A_{0} = 3.2 cm^{2} inside the capacitor and parallel to the plates. At an instant, the current through the circuit is 6 A. At the same instant the displacement current through A_{0} is ______ mA.',
    None, 1200, lambda: round(6 * 3.2 / 16 * 1000), ['Total displacement current = 6 A, spread uniformly over the plate area.', 'Through A_{0}: 6 × \\f{3.2}{16} = 1.2 A = 1200 mA.'], 'disp', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'disp', 'A time varying potential difference is applied between the plates of a parallel plate capacitor of capacitance 2.5 μF. The dielectric constant of the medium between the capacitor plates is 1. It produces an instantaneous displacement current of 0.25 mA in the intervening space between the capacitor plates, the magnitude of the rate of change of the potential difference will be ______ V s^{−1}.',
    None, 100, lambda: round(0.25e-3 / 2.5e-6), ['I_{d} = C\\f{dV}{dt}.', '\\f{dV}{dt} = \\f{0.25 × 10^{−3}}{2.5 × 10^{−6}} = 100 V/s.'], 'disp', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'disp', 'A displacement current of 4.0 A can be set up in the space between two parallel plates of 6 μF capacitor. The rate of change of potential difference across the plates of the capacitor is nearly α × 10^{6} V/s. The value of α is _____.',
    ['0.58', '0.67', '0.82', '0.75'], 2, lambda: near([0.58, 0.67, 0.82, 0.75], 4 / 6e-6 / 1e6), ['\\f{dV}{dt} = \\f{I_{d}}{C} = \\f{4}{6 × 10^{−6}} ≈ 0.67 × 10^{6} V/s.'], 'disp', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'disp', 'An electromagnetic wave of frequency 100 MHz propagates through a medium of conductivity, σ = 10 mho/m. The ratio of maximum conduction current density to maximum displacement current density is ______. [Take \\f{1}{4πε_{0}} = 9 × 10^{9} N m^{2}/C^{2}]',
    None, 1800, lambda: round(10 / (2 * math.pi * 1e8 * (1 / (4 * math.pi * 9e9)))), ['J_{c} = σE_{0}; J_{d} = ε_{0}\\f{∂E}{∂t} → peak ε_{0}ωE_{0}.', 'Ratio = \\f{σ}{ωε_{0}} = \\f{10 × 4π × 9 × 10^{9}}{2π × 10^{8}} = 1800.'], 'disp', 2)

# ---------------- spectrum ----------------
add(('2024', 'Apr', '2024-04-04', 2), 'spec', 'Arrange the following in the ascending order of wavelength : (A) Gamma rays (λ_{1}) (B) x-ray (λ_{2}) (C) Infrared waves (λ_{3}) (D) Microwaves (λ_{4}). Choose the most appropriate answer from the options given below :',
    ['λ_{4} < λ_{3} < λ_{1} < λ_{2}', 'λ_{4} < λ_{3} < λ_{2} < λ_{1}', 'λ_{1} < λ_{2} < λ_{3} < λ_{4}', 'λ_{2} < λ_{1} < λ_{4} < λ_{3}'], 3,
    lambda: (lambda L: pick(['λ_{4} < λ_{3} < λ_{1} < λ_{2}', 'λ_{4} < λ_{3} < λ_{2} < λ_{1}', 'λ_{1} < λ_{2} < λ_{3} < λ_{4}', 'λ_{2} < λ_{1} < λ_{4} < λ_{3}'], ' < '.join(f'λ_{{{i}}}' for i in sorted(L, key=L.get))))({1: 1e-12, 2: 1e-10, 3: 1e-5, 4: 1e-2}),
    ['Typical λ: gamma ~10^{−12} m, X-ray ~10^{−10} m, infrared ~10^{−5} m, microwave ~10^{−2} m.', 'λ_{1} < λ_{2} < λ_{3} < λ_{4}.'], 'spec', 1)
add(('2025', 'Jan', '2025-01-24', 2), 'spec', 'Arrange the following in the ascending order of wavelength (λ) : (A) Microwaves (λ_{1}) (B) Ultraviolet rays (λ_{2}) (C) Infrared rays (λ_{3}) (D) X-rays (λ_{4}). Choose the most appropriate answer from the options given below :',
    ['λ_{4} < λ_{3} < λ_{1} < λ_{2}', 'λ_{3} < λ_{4} < λ_{2} < λ_{1}', 'λ_{4} < λ_{3} < λ_{2} < λ_{1}', 'λ_{4} < λ_{2} < λ_{3} < λ_{1}'], 4,
    lambda: (lambda L: pick(['λ_{4} < λ_{3} < λ_{1} < λ_{2}', 'λ_{3} < λ_{4} < λ_{2} < λ_{1}', 'λ_{4} < λ_{3} < λ_{2} < λ_{1}', 'λ_{4} < λ_{2} < λ_{3} < λ_{1}'], ' < '.join(f'λ_{{{i}}}' for i in sorted(L, key=L.get))))({1: 1e-2, 2: 1e-7, 3: 1e-5, 4: 1e-10}),
    ['X-rays < ultraviolet < infrared < microwaves.'], 'spec', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'spec', 'Match List-I with List-II :- List - I (EM-Wave): (A) Infra-red (B) Ultraviolet (C) X-rays (D) Gamma rays. List-II (Wavelength Range): (I) < 10^{−3} nm (II) 400 nm to 1 nm (III) 1 mm to 700 nm (IV) 1 nm to 10^{−3} nm. Choose the correct answer from the options given below :',
    ['(A)-(II), (B)-(I), (C)-(IV), (D)-(III)', '(A)-(III), (B)-(II), (C)-(IV), (D)-(I)', '(A)-(IV), (B)-(III), (C)-(II), (D)-(I)', '(A)-(I), (B)-(III), (C)-(II), (D)-(IV)'], 2,
    lambda: pick(['(A)-(II), (B)-(I), (C)-(IV), (D)-(III)', '(A)-(III), (B)-(II), (C)-(IV), (D)-(I)', '(A)-(IV), (B)-(III), (C)-(II), (D)-(I)', '(A)-(I), (B)-(III), (C)-(II), (D)-(IV)'], '(A)-(III), (B)-(II), (C)-(IV), (D)-(I)'),
    ['Infrared just beyond red (700 nm) up to 1 mm; UV from violet (400 nm) down to ~1 nm.', 'X-rays 1 nm to 10^{−3} nm; gamma rays shorter still.'], 'spec', 1)
