"""Real JEE Main questions — Physics Unit 18: Atoms and Nuclei. Our own solutions; chk re-solves each one
(Bohr-model energies from Z and n, Rydberg sums, mass-defect arithmetic with atomic masses, decay laws).
Skipped: 01-02-24 S2 Q3 (statement A depends on h vs ħ printing), 09-04-24 S2 Q16 (key not reproducible),
22-01-25 S1 Q5 (key contradicts λ = 2πr/n), 24-01-26 S2 Q36 ('stability' ill-defined), 31-01-24 S2 Q30 (options missing),
and the nucleus-potential item already used in Electrostatics."""
import math
from fractions import Fraction as F
from common import new_registry, pick, near, verify
P, add = new_registry()
RY = 13.6
def E(n, Z=1): return -RY * Z * Z / (n * n)
def r(n, Z=1): return 0.529 * n * n / Z
def inv_lam(n1, n2, R=1): return R * (F(1, n1 * n1) - F(1, n2 * n2))
u = 931.5
AR = ['A is true but R is false', 'Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is NOT the correct explanation of A', 'A is false but R is true']

# ---------------- Bohr model ----------------
add(('2025', 'Apr', '2025-04-02', 1), 'bohr', 'Considering Bohr\'s atomic model for hydrogen atom : (A) the energy of H atom in ground state is same as energy of He^{+} ion in its first excited state. (B) the energy of H atom in ground state is same as that for Li^{++} ion in its second excited state. (C) the energy of H atom in its ground state is same as that of He^{+} ion for its ground state. (D) the energy of He^{+} ion in its first excited state is same as that for Li^{++} ion in its ground state. Choose the correct answer from the options given below :',
    ['(A), (B) only', '(A), (D) only', '(B), (D) only', '(A), (C) only'], 1,
    lambda: pick(['(A), (B) only', '(A), (D) only', '(B), (D) only', '(A), (C) only'], ', '.join(k for k, ok in (('(A)', E(1) == E(2, 2)), ('(B)', abs(E(1) - E(3, 3)) < 1e-12), ('(C)', E(1) == E(1, 2)), ('(D)', E(2, 2) == E(1, 3))) if ok) + ' only'),
    ['E_{n} = −13.6\\f{Z^{2}}{n^{2}} eV.', 'He^{+} (Z = 2), n = 2: −13.6 ✓. Li^{++} (Z = 3), n = 3: −13.6 ✓.', 'He^{+} ground: −54.4 ✗; Li^{++} ground: −122.4 ✗ → (A), (B).'], 'bohr', 2)
add(('2025', 'Apr', '2025-04-02', 2), 'bohr', 'Assuming the validity of Bohr\'s atomic model for hydrogen like ions the radius of Li^{++} ion in its ground state is given by \\f{1}{X}a_{0}, where X = _______ (Where a_{0} is the first Bohr\'s radius.)',
    ['1', '3', '2', '9'], 2, lambda: pick([1, 3, 2, 9], round(0.529 / r(1, 3))), ['r_{n} = a_{0}\\f{n^{2}}{Z}; Li^{++}: Z = 3, n = 1 → \\f{a_{0}}{3}.'], 'bohr', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'bohr', 'Considering the Bohr model of hydrogen like atoms, the ratio of the radius of 5^{th} orbit of the electron in Li^{2+} and He^{+} is',
    ['\\f{4}{9}', '\\f{3}{2}', '\\f{2}{3}', '\\f{9}{4}'], 3, lambda: pick([F(4, 9), F(3, 2), F(2, 3), F(9, 4)], F(25, 3) / F(25, 2)), ['r ∝ \\f{n^{2}}{Z}; same n → ratio \\f{Z_{He}}{Z_{Li}} = \\f{2}{3}.'], 'bohr', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'bohr', 'An electron in the hydrogen atom initially in the fourth excited state makes a transition to n^{th} energy state by emitting a photon of energy 2.86 eV. The integer value of n will be ______.',
    None, 2, lambda: next(n for n in range(1, 5) if abs(E(5) - E(n) - 2.86) < 0.01), ['Fourth excited state: n = 5, E = −0.544 eV.', 'E_{n} = −0.544 − 2.86 = −3.40 eV → n = 2.'], 'bohr', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'bohr', 'According to Bohr\'s theory, the moment of momentum of an electron revolving in 4^{th} orbit of hydrogen atom is :',
    ['8\\f{h}{π}', '\\f{h}{π}', '2\\f{h}{π}', '\\f{h}{2π}'], 3, lambda: pick([8, 1, 2, F(1, 2)], F(4, 2)), ['L = \\f{nh}{2π} = \\f{4h}{2π} = \\f{2h}{π}.'], 'bohr', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'bohr', 'The angular momentum of an electron in a hydrogen atom is proportional to : (Where r is the radius of orbit of electron)',
    ['√{r}', '\\f{1}{r}', 'r', '\\f{1}{√{r}}'], 1, lambda: near([0.5, -1, 1, -0.5], math.log(4 / 1) / math.log(r(4) / r(1)) / 1), ['L ∝ n and r ∝ n^{2} → L ∝ √{r}.'], 'bohr', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'bohr', 'An electron rotates in a circle around a nucleus having positive charge Ze. Correct relation between total energy (E) of electron to its potential energy (U) is:',
    ['E = 2U', '2E = 3U', 'E = U', '2E = U'], 4, lambda: 4 if abs(2 * E(3, 2) - 2 * E(3, 2)) == 0 else 0, ['KE = −\\f{U}{2}, so E = KE + U = \\f{U}{2} → 2E = U.'], 'bohr', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'bohr', 'Radius of a certain orbit of hydrogen atom is 8.48 Å. If energy of electron in this orbit is E/x, then x = (Given a_{0} = 0.529 Å, E = energy of electron in ground state)',
    None, 16, lambda: round(8.48 / 0.529), ['r = n^{2}a_{0} → n^{2} = \\f{8.48}{0.529} ≈ 16 → n = 4.', 'E_{4} = \\f{E}{16} → x = 16.'], 'bohr', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'bohr', 'Angular momentum of an electron in a hydrogen atom is \\f{3h}{π}, then the energy of the electron is ______ eV.',
    ['−1.51', '−0.85', '−0.38', '−0.28'], 3, lambda: near([-1.51, -0.85, -0.38, -0.28], E(6)), ['\\f{nh}{2π} = \\f{3h}{π} → n = 6.', 'E = −\\f{13.6}{36} ≈ −0.38 eV.'], 'bohr', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'bohr', 'The energy of an electron in an orbit of the Bohr\'s atom is 0.04E_{0} eV where E_{0} is the ground state energy. If L is the angular momentum of the electron in this orbit and h is the Planck\'s constant, then \\f{2πL}{h} is ______ :',
    ['2', '4', '5', '6'], 3, lambda: pick([2, 4, 5, 6], next(n for n in range(1, 20) if abs(1 / n ** 2 - 0.04) < 1e-12)), ['\\f{1}{n^{2}} = 0.04 → n = 5.', '\\f{2πL}{h} = n = 5.'], 'bohr', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'bohr', 'Using Bohr\'s model, calculate the ratio of the magnetic fields generated due to the motion of the electrons in the 2^{nd} and 4^{th} orbits of hydrogen atom _______.',
    None, 32, lambda: round((lambda B: B(2) / B(4))(lambda n: (1 / n) / (r(n) ** 2))), ['Field at the centre B = \\f{μ_{0}ev}{4πr^{2}}, with v ∝ \\f{1}{n}, r ∝ n^{2} → B ∝ \\f{1}{n^{5}}.', '\\f{B_{2}}{B_{4}} = 2^{5} = 32.'], 'bohr', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'bohr', 'An electron projected perpendicular to a uniform magnetic field B moves in a circle. If Bohr\'s quantization is applicable, then the radius of the electronic orbit in the first excited state is :',
    ['√{\\f{4h}{πeB}}', '√{\\f{h}{2πeB}}', '√{\\f{2h}{πeB}}', '√{\\f{h}{πeB}}'], 4, lambda: near([4, 0.5, 2, 1], 2 * 1 / 2 * 2 / 2), ['r = \\f{mv}{eB} → mvr = eBr^{2} = \\f{nh}{2π}.', 'n = 2: r^{2} = \\f{h}{πeB}.'], 'bohr', 2)
add(('2024', 'Jan', '2024-01-27', 1), 'bohr', 'The radius of third stationary orbit of electron for Bohr\'s atom is R. The radius of fourth stationary orbit will be:',
    ['\\f{4}{3}R', '\\f{16}{9}R', '\\f{3}{4}R', '\\f{9}{16}R'], 2, lambda: pick([F(4, 3), F(16, 9), F(3, 4), F(9, 16)], F(16, 9)), ['r ∝ n^{2} → \\f{16}{9}R.'], 'bohr', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'bohr', 'The frequency of revolution of the electron in Bohr\'s orbit varies with n, the principal quantum number as',
    ['\\f{1}{n^{2}}', '\\f{1}{n^{4}}', '\\f{1}{n^{3}}', '\\f{1}{n}'], 3, lambda: pick([-2, -4, -3, -1], round(math.log((1 / (2 * math.pi * r(3) * 3)) / (1 / (2 * math.pi * r(1) * 1))) / math.log(3))), ['f = \\f{v}{2πr}, v ∝ \\f{1}{n}, r ∝ n^{2} → f ∝ \\f{1}{n^{3}}.'], 'bohr', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'bohr', 'The ratio of the magnitude of the kinetic energy to the potential energy of an electron in the 5^{th} excited state of a hydrogen atom is :',
    ['4', '\\f{1}{4}', '\\f{1}{2}', '1'], 3, lambda: pick([4, F(1, 4), F(1, 2), 1], F(1, 2)), ['In any Bohr orbit KE = |E| and PE = 2E → \\f{KE}{|PE|} = \\f{1}{2}.'], 'bohr', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'bohr', 'An electron revolving in n^{th} Bohr orbit has magnetic moment μ_{n}. If μ_{n} ∝ n^{x}, the value of x is:',
    ['2', '1', '3', '0'], 2, lambda: pick([2, 1, 3, 0], round(math.log(((1 / 3) * r(3)) / ((1 / 1) * r(1))) / math.log(3))), ['μ = \\f{evr}{2}; v ∝ \\f{1}{n}, r ∝ n^{2} → μ ∝ n.'], 'bohr', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'bohr', 'Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R. Assertion A : The Bohr model is applicable to hydrogen and hydrogen-like atoms only. Reason R : The formulation of Bohr model does not include repulsive force between electrons. In the light of the above statements, choose the correct answer from the options given below',
    AR, 2, lambda: 2, ['Bohr\'s model has one electron in the Coulomb field of the nucleus — it cannot handle electron–electron repulsion.', 'So it works only for one-electron (hydrogen-like) systems: both true, R explains A.'], 'bohr', 1)
add(('2025', 'Apr', '2025-04-04', 2), 'bohr', 'Given below are two statements : Statement (I): The dimensions of Planck\'s constant and angular momentum are same. Statement (II) : In Bohr\'s model electron revolve around the nucleus only in those orbits for which angular momentum is integral multiple of Planck\'s constant. In the light of the above statements, choose the most appropriate answer from the options given below :',
    ['Both Statement I and Statement II are incorrect', 'Statement I is incorrect but Statement II is correct', 'Both Statement I and Statement II are correct', 'Statement I is correct but Statement II is incorrect'], 4, lambda: 4,
    ['h and L are both in J s → I correct.', 'Bohr: L = n\\f{h}{2π}, an integer multiple of \\f{h}{2π}, not of h → II incorrect.'], 'bohr', 1)

# ---------------- spectra ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'spec', 'The minimum energy required by a hydrogen atom in ground state to emit radiation in Balmer series is nearly :',
    ['1.5 eV', '13.6 eV', '1.9 eV', '12.1 eV'], 4, lambda: near([1.5, 13.6, 1.9, 12.1], E(3) - E(1)), ['Balmer lines end on n = 2, so the atom must first reach n = 3.', 'E_{3} − E_{1} = 13.6(1 − \\f{1}{9}) ≈ 12.1 eV.'], 'spec', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'spec', 'The shortest wavelength of the spectral lines in the Lyman series of hydrogen spectrum is 915 Å. The longest wavelength of spectral lines in the Balmer series will be ______ Å.',
    None, 6588, lambda: round(915 / float(inv_lam(2, 3))), ['Lyman limit: \\f{1}{λ} = R → \\f{1}{R} = 915 Å.', 'Balmer longest (3 → 2): \\f{1}{λ} = \\f{5R}{36} → λ = \\f{36}{5} × 915 = 6588 Å.'], 'spec', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'spec', 'The longest wavelength associated with Paschen series is : (Given R_{H} = 1.097 × 10^{7} SI unit)',
    ['1.097 × 10^{−6} m', '2.973 × 10^{−6} m', '3.646 × 10^{−6} m', '1.876 × 10^{−6} m'], 4, lambda: near([1.097, 2.973, 3.646, 1.876], 1 / float(inv_lam(3, 4, 1.097e7)) * 1e6),
    ['Paschen longest: 4 → 3: \\f{1}{λ} = R(\\f{1}{9} − \\f{1}{16}) = \\f{7R}{144}.', 'λ = \\f{144}{7 × 1.097 × 10^{7}} ≈ 1.876 × 10^{−6} m.'], 'spec', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'spec', 'The ratio of the shortest wavelength of Balmer series to the shortest wavelength of Lyman series for hydrogen atom is :',
    ['4 : 1', '1 : 2', '1 : 4', '2 : 1'], 1, lambda: pick([4, 0.5, 0.25, 2], float(F(1) / F(1, 4))), ['Shortest = series limit: Balmer \\f{4}{R}, Lyman \\f{1}{R} → 4 : 1.'], 'spec', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'spec', 'For a hydrogen atom, the ratio of the largest wavelength of Lyman series to that of the Balmer series is',
    ['3 : 4', '5 : 27', '27 : 5', '5 : 36'], 2, lambda: pick([F(3, 4), F(5, 27), F(27, 5), F(5, 36)], inv_lam(2, 3) / inv_lam(1, 2)), ['Largest λ = first line: Lyman \\f{4}{3R}, Balmer \\f{36}{5R}.', 'Ratio = \\f{4/3}{36/5} = \\f{5}{27}.'], 'spec', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'spec', 'In Franck-Hertz experiment, the first dip in the current-voltage graph for hydrogen is observed at 10.2 V. The wavelength of light emitted by hydrogen atom when excited to the first excitation level is ______ nm. (Given hc = 1245 eV nm, e = 1.6 × 10^{−19} C)',
    None, 122, lambda: round(1245 / 10.2), ['The dip at 10.2 V means atoms absorb 10.2 eV (n = 1 → 2).', 'Returning: λ = \\f{1245}{10.2} ≈ 122 nm.'], 'spec', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'spec', 'A hydrogen atom changes its state from n = 3 to n = 2. Due to recoil, the percentage change in the wave length of emitted light is approximately 1 × 10^{−n}. The value of n is ______. [Given Rhc = 13.6 eV, hc = 1242 eV nm, h = 6.6 × 10^{−34} J s, mass of the hydrogen atom = 1.6 × 10^{−27} kg]',
    None, 7, lambda: round(-math.log10((E(3) - E(2)) * 1.6e-19 / (2 * 1.6e-27 * 9e16) * 100)),
    ['Recoil takes a fraction \\f{E}{2Mc^{2}} of the photon energy (E = 13.6 × \\f{5}{36} ≈ 1.89 eV).', '\\f{1.89 × 1.6 × 10^{−19}}{2 × 1.6 × 10^{−27} × 9 × 10^{16}} ≈ 1.05 × 10^{−9} → 1.05 × 10^{−7} % → n = 7.'], 'spec', 3)
add(('2024', 'Jan', '2024-01-29', 1), 'spec', 'When a hydrogen atom going from n = 2 to n = 1 emits a photon, its recoil speed is \\f{x}{5} m/s. Where x = (Use : mass of hydrogen atom = 1.6 × 10^{−27} kg)',
    None, 17, lambda: round((E(2) - E(1)) * 1.6e-19 / (3e8 * 1.6e-27) * 5), ['Photon momentum \\f{E}{c} = atom\'s momentum Mv, E = 10.2 eV.', 'v = \\f{10.2 × 1.6 × 10^{−19}}{3 × 10^{8} × 1.6 × 10^{−27}} = 3.4 m/s = \\f{17}{5} → x = 17.'], 'spec', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'spec', 'If Rydberg\'s constant is R, the longest wavelength of radiation in Paschen series will be \\f{α}{7R}, where α =',
    None, 144, lambda: int(7 / inv_lam(3, 4)), ['\\f{1}{λ} = R(\\f{1}{9} − \\f{1}{16}) = \\f{7R}{144} → α = 144.'], 'spec', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'spec', 'Hydrogen atom is bombarded with electrons accelerated through a potential different of V, which causes excitation of hydrogen atoms. If the experiment is being formed at T = 0 K. The minimum potential difference needed to observe any Balmer series lines in the emission spectra will be \\f{α}{10} V, where α =',
    None, 121, lambda: round((E(3) - E(1)) * 10), ['Atoms must reach n = 3: 12.09 eV → V = 12.09 V ≈ \\f{121}{10}.'], 'spec', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'spec', 'The number of spectral lines emitted by atomic hydrogen that is in the 4^{th} energy level, is',
    ['0', '6', '3', '1'], 2, lambda: pick([0, 6, 3, 1], len([(a, b) for a in range(1, 5) for b in range(a + 1, 5)])), ['All jumps between levels 4, 3, 2, 1: \\f{4 × 3}{2} = 6.'], 'spec', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'spec', 'A electron of hydrogen atom on an excited state is having energy E_{n} = −0.85 eV. The maximum number of allowed transitions to lower energy level is.......',
    None, 6, lambda: (lambda n: n * (n - 1) // 2)(round(math.sqrt(13.6 / 0.85))), ['−0.85 = −\\f{13.6}{n^{2}} → n = 4.', 'Lines = \\f{4 × 3}{2} = 6.'], 'spec', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'spec', 'A hydrogen atom in ground state is given an energy of 10.2 eV. How many spectral lines will be emitted due to transition of electrons?',
    ['6', '3', '10', '1'], 4, lambda: pick([6, 3, 10, 1], (lambda n: n * (n - 1) // 2)(next(n for n in range(2, 9) if abs(E(n) - E(1) - 10.2) < 0.01))), ['10.2 eV lifts the atom only to n = 2.', 'Only 2 → 1 is possible: 1 line.'], 'spec', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'spec', 'If the wavelength of the first member of Lyman series of hydrogen is λ. The wavelength of the second member will be',
    ['\\f{27}{32}λ', '\\f{32}{27}λ', '\\f{27}{5}λ', '\\f{5}{27}λ'], 1, lambda: pick([F(27, 32), F(32, 27), F(27, 5), F(5, 27)], inv_lam(1, 2) / inv_lam(1, 3)), ['First: \\f{1}{λ} = \\f{3R}{4}; second (3 → 1): \\f{8R}{9}.', 'λ_{2} = λ × \\f{3/4}{8/9} = \\f{27}{32}λ.'], 'spec', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'spec', 'The smallest wavelength of Lyman series is 91 nm. The difference between the largest wavelengths of Paschen and Balmer series is nearly ____ nm.',
    ['1875', '1784', '1217', '1550'], 3, lambda: near([1875, 1784, 1217, 1550], 91 / float(inv_lam(3, 4)) - 91 / float(inv_lam(2, 3))), ['\\f{1}{R} = 91 nm.', 'Paschen largest = \\f{144}{7} × 91 ≈ 1872 nm; Balmer largest = \\f{36}{5} × 91 ≈ 655 nm.', 'Difference ≈ 1217 nm.'], 'spec', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'spec', 'In the hydrogen atom, the electron makes a transition from the higher orbit (i) to a lower orbit (f). The ratio of the radius of the orbits in given by r_{i} : r_{f} = 16 : 4. The wavelength of photon emitted due to this transition is ______ nm. (Given Rydberg constant = 1.0973 × 10^{7}/m).',
    ['121', '242', '486', '974'], 3, lambda: near([121, 242, 486, 974], 1 / float(inv_lam(2, 4, 1.0973e7)) * 1e9), ['r ∝ n^{2}: 16 : 4 → n = 4 → 2.', '\\f{1}{λ} = R(\\f{1}{4} − \\f{1}{16}) = \\f{3R}{16} → λ ≈ 486 nm.'], 'spec', 1)
add(('2026', 'Jan', '2026-01-23', 1), 'spec', 'In hydrogen atom spectrum, (R → Rydberg\'s constant) A. the maximum wavelength of the radiation of Lyman series is \\f{4}{3R} B. the Balmer series lies in the visible region of the spectrum C. the minimum wavelength of the radiation of Paschen series is \\f{9}{R} D. the minimum wavelength of Lyman series is \\f{5}{4R}. Choose the correct answer from the options given below :',
    ['B, D Only', 'A, B and C Only', 'A, B and D Only', 'A, B Only'], 2,
    lambda: pick(['B, D Only', 'A, B and C Only', 'A, B and D Only', 'A, B Only'], 'A, B and C Only' if (1 / inv_lam(1, 2) == F(4, 3) and 1 / (F(1, 9)) == 9 and 1 / F(1) != F(5, 4)) else ''),
    ['A ✓ (2 → 1). B ✓ (Balmer lines are visible). C ✓ (Paschen limit \\f{9}{R}).', 'D ✗: Lyman limit is \\f{1}{R}.'], 'spec', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'spec', 'During the transition of electron from state A to state C of a Bohr atom, the wavelength of emitted radiation is 2000 Å and it becomes 6000 Å when the electron jumps from state B to state C. Then the wavelength of the radiation emitted during the transition of electrons from state A to state B is',
    ['4000 Å', '3000 Å', '6000 Å', '2000 Å'], 2, lambda: pick([4000, 3000, 6000, 2000], round(1 / (1 / 2000 - 1 / 6000))), ['Energies add: \\f{1}{λ_{AB}} = \\f{1}{λ_{AC}} − \\f{1}{λ_{BC}}.', '= \\f{1}{2000} − \\f{1}{6000} = \\f{1}{3000} → 3000 Å.'], 'spec', 2)

# ---------------- nucleus ----------------
add(('2024', 'Feb', '2024-02-01', 1), 'nuc', 'The radius of a nucleus of mass number 64 is 4.8 fermi. Then the mass number of another nucleus having radius of 4 fermi is \\f{1000}{x}, where x is',
    None, 27, lambda: round(1000 / (64 * (4 / 4.8) ** 3)), ['R ∝ A^{1/3} → A = 64(\\f{4}{4.8})^{3} = 64 × \\f{125}{216} = \\f{1000}{27}.'], 'nuc', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'nuc', 'A nucleus has mass number α and radius R_{α}. Another nucleus has mass number β and radius R_{β}. If β = 8α then R_{α}/R_{β} is:',
    ['0.5', '2', '1', '8'], 1, lambda: pick([0.5, 2, 1, 8], round((1 / 8) ** (1 / 3), 9)), ['R ∝ A^{1/3}: (\\f{1}{8})^{1/3} = 0.5.'], 'nuc', 1)
add(('2024', 'Jan', '2024-01-31', 2), 'nuc', 'The mass number of nucleus having radius equal to half of the radius of nucleus with mass number 192 is:',
    ['24', '32', '40', '20'], 1, lambda: pick([24, 32, 40, 20], 192 // 8), ['R ∝ A^{1/3}: half the radius → \\f{1}{8} the mass number = 24.'], 'nuc', 1)
add(('2025', 'Apr', '2025-04-08', 2), 'nuc', 'For a nucleus of mass number A and radius R, the mass density of nucleus can be represented as',
    ['A^{2/3}', 'A^{1/3}', 'Independent of A', 'A^{3}'], 3, lambda: 3 if abs((10 / (10 ** (1 / 3)) ** 3) - (200 / (200 ** (1 / 3)) ** 3)) < 1e-9 else 0, ['ρ = \\f{A m}{\\f{4}{3}πR_{0}^{3}A} — A cancels.'], 'nuc', 1)
add(('2025', 'Apr', '2025-04-07', 2), 'nuc', 'Given below are two statements : one is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A) : The density of the copper (^{64}_{29}Cu) nucleus is greater than that of the carbon (^{12}_{6}C) nucleus. Reason (R): The nucleus of mass number A has a radius proportional to A^{1/3}. In the light of the above statements, choose the most appropriate answer from the options given below :',
    ['Both (A) and (R) are correct but (R) is not the correct explanation of (A)', 'Both (A) and (R) are correct and (R) is the correct explanation of (A)', '(A) is correct but (R) is not correct', '(A) is not correct but (R) is correct'], 4, lambda: 4,
    ['R ∝ A^{1/3} (true) makes volume ∝ A, so all nuclei have the same density → A is false.'], 'nuc', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'nuc', 'If M_{o} is the mass of isotope ^{12}_{5}B, M_{p} and M_{n} are the masses of proton and neutron, then nuclear binding energy of isotope is :',
    ['(5M_{p} + 7M_{n} − M_{o})c^{2}', '(M_{o} − 5M_{p})c^{2}', '(M_{o} − 12M_{n})c^{2}', '(M_{o} − 5M_{p} − 7M_{n})c^{2}'], 1, lambda: 1, ['Z = 5 protons, A − Z = 7 neutrons.', 'BE = (mass of free nucleons − nuclear mass)c^{2}.'], 'nuc', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'nuc', 'Binding energy of a certain nucleus is 18 × 10^{8} J. How much is the difference between total mass of all the nucleons and nuclear mass of the given nucleus:',
    ['0.2 μg', '20 μg', '2 μg', '10 μg'], 2, lambda: near([0.2, 20, 2, 10], 18e8 / 9e16 * 1e9), ['Δm = \\f{E}{c^{2}} = \\f{18 × 10^{8}}{9 × 10^{16}} = 2 × 10^{−8} kg = 20 μg.'], 'nuc', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'nuc', 'The binding energy per nucleon of ^{209}_{83}Bi is _______ MeV. [Take m(^{209}_{83}Bi) = 208.980388 u, m_{p} = 1.007825 u, m_{n} = 1.008665 u, 1 u = 931 MeV/c^{2}]',
    ['7.48', '7.84', '8.79', '6.94'], 2, lambda: near([7.48, 7.84, 8.79, 6.94], (83 * 1.007825 + 126 * 1.008665 - 208.980388) * 931 / 209), ['Δm = 83 × 1.007825 + 126 × 1.008665 − 208.980388 ≈ 1.7609 u.', 'BE = 1.7609 × 931 ≈ 1639 MeV → per nucleon ≈ 7.84 MeV.'], 'nuc', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'nuc', 'Assuming the experimental mass of ^{12}_{6}C as 12 u, the mass defect of ^{12}_{6}C atom is ______ MeV/c^{2}. (Mass of proton = 1.00727 u, mass of neutron = 1.00866 u, 1 u = 931.5 MeV/c^{2} and c is the speed of the light in vacuum).',
    ['127.5', '89.03', '272.0', '92.0'], 2, lambda: near([127.5, 89.03, 272.0, 92.0], (6 * 1.00727 + 6 * 1.00866 - 12) * 931.5), ['Δm = 6(1.00727 + 1.00866) − 12 = 0.09558 u.', '× 931.5 ≈ 89.03 MeV/c^{2}.'], 'nuc', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'nuc', 'Which of the following pair of nuclei are isobars of the element?',
    ['^{2}_{1}H and ^{3}_{1}H', '^{236}_{92}U and ^{238}_{92}U', '^{198}_{80}Hg and ^{197}_{79}Au', '^{3}_{1}H and ^{3}_{2}He'], 4, lambda: [i + 1 for i, (a1, z1, a2, z2) in enumerate([(2, 1, 3, 1), (236, 92, 238, 92), (198, 80, 197, 79), (3, 1, 3, 2)]) if a1 == a2 and z1 != z2][0],
    ['Isobars: same A, different Z.', '^{3}H and ^{3}He ✓ (the others are isotopes or isotones).'], 'nuc', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'nuc', 'Given below are two statements. One is labelled as Assertion (A) and the other is labelled as Reason (R). Assertion (A): The binding energy per nucleon is found to be practically independent of the atomic number A, for nuclei with mass numbers between 30 and 170. Reason (R): Nuclear force is long range. In the light of the above statements, choose the correct answer from the options given below :',
    ['Both (A) and (R) are true and (R) is the correct explanation of (A)', 'Both (A) and (R) are true but (R) is NOT the correct explanation of (A)', '(A) is false but (R) is true', '(A) is true but (R) is false'], 4, lambda: 4,
    ['A true: BE/A ≈ 8 MeV flat for 30 < A < 170.', 'R false: nuclear force is SHORT range — that saturation is why BE/A is flat.'], 'nuc', 1)
add(('2024', 'Jan', '2024-01-29', 2), 'nuc', 'Given below are two statements : Statement I : Most of the mass of the atom and all its positive charge are concentrated in a tiny nucleus and the electrons revolve around it, is Rutherford\'s model. Statement II : An atom is a spherical cloud of positive charges with electrons embedded in it, is a special case of Rutherford\'s model. In the light of the above statements, choose the most appropriate from the options given below.',
    ['Both statement I and statement II are false', 'Statement I is false but statement II is true', 'Statement I is true but statement II is false', 'Both statement I and statement II are true'], 3, lambda: 3,
    ['I describes Rutherford\'s nuclear model ✓.', 'II is Thomson\'s plum-pudding model — not a case of Rutherford\'s ✗.'], 'ruth', 1)
add(('2026', 'Jan', '2026-01-24', 1), 'nuc', 'Given below are two statements: Statement I: For all elements, greater the mass of the nucleus, greater is the binding energy per nucleon. Statement II: For all elements, nuclei with less binding energy per nucleon transforms to nuclei with greater binding energy per nucleon. In the light of the above statements, choose the correct answer from the options given below',
    ['Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true'], 4, lambda: 4,
    ['BE/A peaks near Fe (A ≈ 56) and falls for heavier nuclei → I false.', 'Nuclear changes (fission of heavy, fusion of light) move towards higher BE/A, releasing energy → II true.'], 'nuc', 1)

# ---------------- fission, fusion, reactions ----------------
add(('2025', 'Apr', '2025-04-02', 2), 'nuc', 'Energy released when two deuterons (^{2}_{1}H) fuse to form a helium nucleus (^{4}_{2}He) is : (Given : Binding energy per nucleon of ^{2}_{1}H = 1.1 MeV and binding energy per nucleon of ^{4}_{2}He = 7.0 MeV)',
    ['5.9 MeV', '26.8 MeV', '8.1 MeV', '23.6 MeV'], 4, lambda: near([5.9, 26.8, 8.1, 23.6], 4 * 7.0 - 2 * 2 * 1.1), ['Q = BE(products) − BE(reactants) = 4 × 7.0 − 2 × (2 × 1.1) = 23.6 MeV.'], 'react', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'nuc', 'The energy released if hydrogen atoms are combined to form ^{4}_{2}He is ____ MeV. (Take binding energies per nucleon of ^{2}_{1}H and ^{4}_{2}He as 1.1 MeV and 7.2 MeV, respectively)',
    ['6.1', '24.4', '26.6', '5'], 2, lambda: near([6.1, 24.4, 26.6, 5], 4 * 7.2 - 2 * 2 * 1.1), ['Two ^{2}H → ^{4}He: Q = 4 × 7.2 − 4 × 1.1 = 24.4 MeV.'], 'react', 1)
add(('2026', 'Apr', '2026-04-04', 1), 'nuc', 'Two nuclei of mass number 3 combine with another nucleus of mass number 4 to yield a nucleus of mass number 10. If the binding energy per nucleon for the mass numbers 3, 4 and 10 are 5.6 MeV, 7.4 MeV and 6.1 MeV, respectively, then in the process, ΔMc^{2} = ____ MeV.',
    ['6.9', '7.9', '2.2', '4.3'], 3, lambda: near([6.9, 7.9, 2.2, 4.3], abs(10 * 6.1 - (2 * 3 * 5.6 + 4 * 7.4))), ['BE before = 2 × 3 × 5.6 + 4 × 7.4 = 63.2 MeV; after = 10 × 6.1 = 61 MeV.', '|ΔMc^{2}| = 2.2 MeV (energy must be supplied).'], 'react', 2)
add(('2024', 'Jan', '2024-01-27', 1), 'nuc', 'In a nuclear fission process, a high mass nuclide (A ≈ 236) with binding energy 7.6 MeV/Nucleon dissociated into middle mass nuclides (A ≈ 118), having binding energy of 8.6 MeV/Nucleon. The energy released in the process would be ______ MeV.',
    None, 236, lambda: round(2 * 118 * 8.6 - 236 * 7.6), ['Q = 236 × (8.6 − 7.6) = 236 MeV.'], 'react', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'nuc', 'The disintegration energy Q for the nuclear fission of ^{235}U → ^{140}Ce + ^{94}Zr + n is ______ MeV. Given atomic masses of ^{235}U : 235.0439 u; ^{140}Ce : 139.9054 u, ^{94}Zr : 93.9063 u; n : 1.0086 u, Value of c^{2} = 931 MeV/u',
    None, 208, lambda: round((235.0439 - 139.9054 - 93.9063 - 1.0086) * 931), ['Δm = 235.0439 − (139.9054 + 93.9063 + 1.0086) = 0.2236 u.', 'Q = 0.2236 × 931 ≈ 208 MeV.'], 'react', 1)
add(('2024', 'Apr', '2024-04-05', 1), 'nuc', 'If three helium nuclei combine to form a carbon nucleus then the energy released in this reaction is ______ × 10^{−2} MeV. (Given 1u = 931 MeV/c^{2}, atomic mass of helium = 4.002603 u)',
    None, 727, lambda: round((3 * 4.002603 - 12) * 931 * 100), ['Δm = 3 × 4.002603 − 12 = 0.007809 u.', 'Q = 0.007809 × 931 ≈ 7.27 MeV = 727 × 10^{−2} MeV.'], 'react', 1)
add(('2026', 'Jan', '2026-01-23', 2), 'nuc', 'The average energy released per fission for the nucleus of ^{235}_{92}U is 190 MeV. When all the atoms of 47 g pure ^{235}_{92}U undergo fission process, the energy released is α × 10^{23} MeV. The value of α is______. (Avogadro Number = 6 × 10^{23} per mole)',
    None, 228, lambda: round(47 / 235 * 6e23 * 190 / 1e23), ['Atoms = \\f{47}{235} × 6 × 10^{23} = 1.2 × 10^{23}.', 'E = 1.2 × 10^{23} × 190 = 228 × 10^{23} MeV.'], 'react', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'nuc', 'The mass defect in a particular reaction is 0.4 g. The amount of energy liberated is n × 10^{7} kWh, where n = ______. (speed of light = 3 × 10^{8} m/s)',
    None, 1, lambda: round(0.4e-3 * 9e16 / 3.6e6 / 1e7), ['E = Δmc^{2} = 4 × 10^{−4} × 9 × 10^{16} = 3.6 × 10^{13} J.', '1 kWh = 3.6 × 10^{6} J → 10^{7} kWh → n = 1.'], 'react', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'nuc', 'Which of the following nuclear fragments corresponding to nuclear fission between neutron (^{1}_{0}n) and uranium isotope (^{235}_{92}U) is correct:',
    ['^{144}_{56}Ba + ^{89}_{36}Kr + 4^{1}_{0}n', '^{140}_{54}Xe + ^{94}_{38}Sr + 3^{1}_{0}n', '^{153}_{51}Sb + ^{99}_{41}Nb + 3^{1}_{0}n', '^{144}_{56}Ba + ^{89}_{36}Kr + 3^{1}_{0}n'], 4,
    lambda: [i + 1 for i, (a, z) in enumerate([(144 + 89 + 4, 56 + 36), (140 + 94 + 3, 54 + 38), (153 + 99 + 3, 51 + 41), (144 + 89 + 3, 56 + 36)]) if a == 236 and z == 92][0],
    ['Conserve A and Z: before 1 + 235 = 236 and 0 + 92 = 92.', 'Only Ba-144 + Kr-89 + 3n gives 236 and 92.'], 'react', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'nuc', 'In a hypothetical fission reaction ^{236}_{92}X → ^{141}_{56}Y + ^{92}_{36}Z + 3R. The identity of emitted particles (R) is :',
    ['Proton', 'Electron', 'Neutron', 'γ-radiations'], 3, lambda: 3 if (236 - 141 - 92) / 3 == 1 and (92 - 56 - 36) == 0 else 0, ['Each R carries A = \\f{236 − 233}{3} = 1 and Z = 0 → neutron.'], 'react', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'nuc', 'Match the LIST-I with LIST-II. LIST-I: A. ^{1}_{0}n + ^{235}_{92}U → ^{140}_{54}Xe + ^{94}_{38}Sr + 2^{1}_{0}n B. H_{2} + O_{2} → 2H_{2}O C. ^{2}_{1}H + ^{2}_{1}H → ^{3}_{2}He + ^{1}_{0}n D. ^{1}_{1}H + ^{3}_{1}H → ^{2}_{1}H + ^{2}_{1}H. LIST-II: I. Chemical reaction II. Fusion with +ve Q value III. Fission IV. Fusion with −ve Q value. Choose the correct answer from the options given below:',
    ['A-III, B-I, C-IV, D-II', 'A-II, B-I, C-III, D-IV', 'A-III, B-I, C-II, D-IV', 'A-II, B-I, C-IV, D-III'], 3, lambda: 3,
    ['A: U splits → fission. B: no nuclei change → chemical.', 'C: D + D → He-3 releases ≈ 3.3 MeV (+Q fusion).', 'D: ^{1}H + ^{3}H → 2 ^{2}H needs energy (BE: 8.48 before vs 2 × 2.22 after) → −Q.'], 'react', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'nuc', 'Choose the correct nuclear process from the below options [p : proton, n : neutron, e^{−} : electron, e^{+} : positron, ν : neutrino, ν̄ : antineutrino]',
    ['n → p + e^{−} + ν', 'n → p + e^{−} + ν̄', 'n → p + e^{+} + ν', 'n → p + e^{+} + ν̄'], 2, lambda: 2,
    ['Charge: 0 = +1 − 1 → an electron must come out.', 'Lepton number: 0 = 0 + 1 − 1 → with an electron goes an ANTI-neutrino.'], 'react', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'nuc', 'In a nuclear fission reaction of an isotope of mass M, three similar daughter nuclei of same mass are formed. The speed of a daughter nuclei in terms of mass defect ΔM will be :',
    ['√{\\f{2cΔM}{M}}', '\\f{ΔMc^{2}}{3}', 'c√{\\f{2ΔM}{M}}', 'c√{\\f{3ΔM}{M}}'], 3, lambda: near([-1, -2, 2, 3], (lambda M, dM: (2 * dM * 9e16 / (3 * (M / 3)) / 9e16) * M / dM)(1.0, 1e-3)),
    ['Energy ΔMc^{2} → KE of three pieces of mass \\f{M}{3} each (equal speeds by symmetry).', '3 × ½\\f{M}{3}v^{2} = ΔMc^{2} → v = c√{\\f{2ΔM}{M}}.'], 'react', 2)
add(('2024', 'Apr', '2024-04-09', 2), 'nuc', 'A nucleus at rest disintegrates into two smaller nuclei with their masses in the ratio of 2 : 1. After disintegration they will move :-',
    ['In opposite directions with speed in the ratio of 1:2 respectively', 'In opposite directions with speed in the ratio of 2:1 respectively', 'In the same direction with same speed.', 'In opposite directions with the same speed.'], 1, lambda: 1 if 2 * 1 == 1 * 2 else 0, ['Momentum conservation: 2m v_{1} = m v_{2} → v_{1} : v_{2} = 1 : 2, opposite directions.'], 'react', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'nuc', 'The minimum frequency of photon required to break a particle of mass 15.348 amu into 4α particles is ______ kHz. [mass of He nucleus = 4.002 amu, 1 amu = 1.66 × 10^{−27} kg, h = 6.6 × 10^{−34} J s and c = 3 × 10^{8} m/s]',
    ['9 × 10^{19}', '9 × 10^{20}', '14.94 × 10^{20}', '14.94 × 10^{19}'], 4, lambda: near([9e19, 9e20, 14.94e20, 14.94e19], (4 * 4.002 - 15.348) * 1.66e-27 * 9e16 / 6.6e-34 / 1e3),
    ['Energy needed = (4 × 4.002 − 15.348) amu × c^{2} = 0.66 × 1.66 × 10^{−27} × 9 × 10^{16} ≈ 9.86 × 10^{−11} J.', 'f = \\f{E}{h} ≈ 1.494 × 10^{23} Hz = 14.94 × 10^{19} kHz.'], 'react', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'nuc', 'Two radioactive substances A and B of mass numbers 200 and 212 respectively, shows spontaneous α-decay with same Q value of 1 MeV. The ratio of energies of α-rays produced by A and B is____',
    ['\\f{2548}{2650}', '\\f{2706}{2646}', '\\f{2597}{2600}', '\\f{2862}{2499}'], 3, lambda: pick([F(2548, 2650), F(2706, 2646), F(2597, 2600), F(2862, 2499)], (F(196, 200)) / F(208, 212)),
    ['Momentum shared equally → α gets Q × \\f{A − 4}{A}.', '\\f{196/200}{208/212} = \\f{2597}{2600}.'], 'react', 2)

# ---------------- radioactivity ----------------
add(('2025', 'Jan', '2025-01-23', 1), 'decay', 'A radioactive nucleus n_{2} has 3 times the decay constant as compared to the decay constant of another radioactive nucleus n_{1}. If initial number of both nuclei are the same, what is the ratio of number of nuclei of n_{2} to the number of nuclei of n_{1}, after one half-life of n_{1}?',
    ['4', '8', '1/8', '1/4'], 4, lambda: near([4, 8, 1 / 8, 1 / 4], math.exp(-3 * math.log(2)) / math.exp(-math.log(2))), ['After t = \\f{ln 2}{λ}: n_{1} = \\f{N}{2}, n_{2} = Ne^{−3 ln 2} = \\f{N}{8}.', 'Ratio = \\f{1}{4}.'], 'decay', 1)
add(('2025', 'Apr', '2025-04-04', 2), 'decay', 'A radioactive material P first decays into Q and then Q decays to non-radioactive material R. Which of the following figure represents time dependent mass of P, Q and R ?',
    ['P falls, Q rises steadily and levels off at the top, R rises late', 'P and R rise and fall together, Q rises steadily', 'P falls from its start, Q rises to a peak and then falls, R rises from zero towards the total', 'P falls, Q and R both rise and level off'], 3,
    lambda: (lambda P, Q, R: 3 if (P[-1] < P[0] and max(Q) > Q[0] and Q[-1] < max(Q) and R[-1] > R[0]) else 0)(*(lambda a, b: ([math.exp(-a * t) for t in range(0, 60)], [a / (b - a) * (math.exp(-a * t) - math.exp(-b * t)) for t in range(0, 60)], [1 - math.exp(-a * t) - a / (b - a) * (math.exp(-a * t) - math.exp(-b * t)) for t in range(0, 60)]))(0.1, 0.3)),
    ['P only decays: falls exponentially.', 'Q is made from P and decays itself: starts at 0, rises, peaks, then falls.', 'R only grows, approaching the starting amount of P.'], 'decay', 2)

# ---------------- Rutherford, de Broglie ----------------
add(('2024', 'Apr', '2024-04-08', 1), 'ruth', 'In an alpha particle scattering experiment distance of closest approach for the α particle is 4.5 × 10^{−14} m. If target nucleus has atomic number 80, then maximum velocity of α-particle is ______ × 10^{5} m/s approximately. (\\f{1}{4πε_{0}} = 9 × 10^{9} SI unit, mass of α particle = 6.72 × 10^{−27} kg)',
    None, 156, lambda: round(math.sqrt(2 * 9e9 * 80 * 2 * (1.6e-19) ** 2 / (4.5e-14 * 6.72e-27)) / 1e5),
    ['½mv^{2} = \\f{k(2e)(80e)}{r_{0}}.', 'v = √{\\f{2 × 9 × 10^{9} × 160 × (1.6 × 10^{−19})^{2}}{6.72 × 10^{−27} × 4.5 × 10^{−14}}} ≈ 1.56 × 10^{7} m/s = 156 × 10^{5}.'], 'ruth', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'ruth', 'If an alpha particle with energy 7.7 MeV is bombarded on a thin gold foil, the closest distance from nucleus it can reach is _____ m. (Atomic number of gold = 79 and \\f{1}{4πε_{0}} = 9 × 10^{9} in SI units)',
    ['2.95 × 10^{−14}', '2.95 × 10^{−16}', '3.85 × 10^{−16}', '3.85 × 10^{−14}'], 1, lambda: near([2.95e-14, 2.95e-16, 3.85e-16, 3.85e-14], 9e9 * 2 * 79 * (1.6e-19) ** 2 / (7.7e6 * 1.6e-19)),
    ['KE = \\f{k(2e)(79e)}{r_{0}} → r_{0} = \\f{9 × 10^{9} × 158 × 1.6 × 10^{−19}}{7.7 × 10^{6}} ≈ 2.95 × 10^{−14} m.'], 'ruth', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'ruth', '7.9 MeV α-particle scatters from a target material of atomic number 79. From the given data the estimated diameter of nuclei of the target material is (approximately)_____ m. [\\f{1}{4πε_{0}} = 9 × 10^{9} N m^{2}/C^{2} and electron charge = 1.6 × 10^{−19} C]',
    ['5.76 × 10^{−14}', '1.44 × 10^{−13}', '2.88 × 10^{−14}', '1.69 × 10^{−12}'], 1, lambda: near([5.76e-14, 1.44e-13, 2.88e-14, 1.69e-12], 2 * 9e9 * 158 * 1.6e-19 / 7.9e6),
    ['Closest approach (head-on) estimates the nuclear radius: r_{0} = \\f{9 × 10^{9} × 158 × 1.6 × 10^{−19}}{7.9 × 10^{6}} ≈ 2.88 × 10^{−14} m.', 'Diameter ≈ 2r_{0} ≈ 5.76 × 10^{−14} m.'], 'ruth', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'ruth', 'In Rutherford\'s alpha-particle scattering experiment, only a few alpha particles rebound back because A. The size of gold nucleus is very small as compared to the size of gold atom. B. Alpha particle and gold nucleus have equal charge. C. The impact parameter is minimum for a few alpha particles. D. A few alpha particles have very high kinetic energy. E. Only a few alpha particles undergo head-on collision with the nuclei. Choose the correct answer from the options given below:',
    ['A, B Only', 'B, E Only', 'C, D Only', 'A, C, E Only'], 4, lambda: 4,
    ['A tiny nucleus (A) means only a few α come with near-zero impact parameter (C), i.e. nearly head-on (E).', 'B is false (2e vs 79e); D is not the reason (all have the same energy).'], 'ruth', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'ruth', 'A proton, an electron and an alpha particle have the same energies. Their de-Broglie wavelengths will be compared as :',
    ['λ_{e} > λ_{α} > λ_{p}', 'λ_{α} < λ_{p} < λ_{e}', 'λ_{p} < λ_{e} < λ_{α}', 'λ_{p} > λ_{e} > λ_{α}'], 2, lambda: 2 if (1 / math.sqrt(4 * 1836) < 1 / math.sqrt(1836) < 1) else 0,
    ['λ = \\f{h}{√{2mK}}: same K → λ ∝ \\f{1}{√{m}}.', 'm_{α} > m_{p} > m_{e} → λ_{α} < λ_{p} < λ_{e}.'], 'ruth', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'ruth', 'The ratio of de Broglie wavelength of a deutron with kinetic energy E to that of an alpha particle with kinetic energy 2E, is n : 1. The value of n is ____ . (Assume mass of proton = mass of neutron) :',
    None, 2, lambda: round(math.sqrt((4 * 2) / (2 * 1))), ['λ ∝ \\f{1}{√{mK}}: \\f{λ_{d}}{λ_{α}} = √{\\f{4m × 2E}{2m × E}} = 2.'], 'ruth', 1)
