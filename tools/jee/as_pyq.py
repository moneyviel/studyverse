"""Real JEE Main questions — Chemistry Unit 2: Atomic Structure. Our own solutions; chk re-solves each."""
from fractions import Fraction as F
import math
from common import new_registry, pick, near, verify
P, add = new_registry()
h, c, NA, me = 6.626e-34, 3e8, 6.022e23, 9.1e-31
ST = ['Statement I is true but Statement II is false', 'Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true']
def wn(n1, n2, Z=1): return F(Z * Z) * (F(1, n1 * n1) - F(1, n2 * n2))       # wave number in units of R
def nodes(n, l): return n - l - 1
CFG = {'Cr': '1s2 2s2 2p6 3s2 3p6 3d5 4s1'}

add(('2024', 'Jan', '2024-02-01', 2), 'qn', 'The number of radial node/s for 3p orbital is:', ['1', '4', '2', '3'], 1, lambda: pick([1, 4, 2, 3], nodes(3, 1)),
    ['Radial nodes = n − l − 1.', 'For 3p: n = 3, l = 1 → 3 − 1 − 1 = 1.'], 'qn', 1)
add(('2025', 'Apr', '2025-04-02', 1), 'bohr', "According to Bohr's model of hydrogen atom, which of the following statement is incorrect?",
    ['Radius of 6^{th} orbit is three times larger than that of 4^{th} orbit', 'Radius of 3^{rd} orbit is nine times larger than that of 1^{st} orbit', 'Radius of 4^{th} orbit is four times larger than that of 2^{nd} orbit', 'Radius of 8^{th} orbit is four times larger than that of 4^{th} orbit'], 1,
    lambda: [i + 1 for i, (a, b, k) in enumerate([(6, 4, 3), (3, 1, 9), (4, 2, 4), (8, 4, 4)]) if F(a * a, b * b) != k][0],
    ['Bohr radius r_{n} ∝ n^{2}.', '6th vs 4th: (6/4)^{2} = 2.25, not 3 → statement 1 is incorrect.', 'Others: 9, 4 and 4 — all correct.'], 'bohr', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'qn', "For electrons in '2s' and '2p' orbitals, the orbital angular momentum values, respectively are :",
    ['\\f{h}{2π} and √{2}\\f{h}{2π}', '√{2}\\f{h}{2π} and 0', '0 and √{2}\\f{h}{2π}', '0 and √{6}\\f{h}{2π}'], 3, lambda: 3 if (0 * 1, 1 * 2) == (0, 2) else 0,
    ['Orbital angular momentum = √{l(l + 1)}\\f{h}{2π}.', '2s (l = 0): 0. 2p (l = 1): √{2}\\f{h}{2π}.'], 'qn', 1)
add(('2025', 'Apr', '2025-04-04', 2), 'config', 'Consider the ground state of chromium atom (Z = 24). How many electrons are with Azimuthal quantum number l = 1 and l = 2 respectively?',
    ['16 and 4', '16 and 5', '12 and 4', '12 and 5'], 4, lambda: pick([(16, 4), (16, 5), (12, 4), (12, 5)], (sum(int(t[2:]) for t in CFG['Cr'].split() if t[1] == 'p'), sum(int(t[2:]) for t in CFG['Cr'].split() if t[1] == 'd'))),
    ['Cr: 1s^{2} 2s^{2} 2p^{6} 3s^{2} 3p^{6} 3d^{5} 4s^{1} (half-filled d is extra stable).', 'l = 1 (p): 6 + 6 = 12. l = 2 (d): 5.'], 'config', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'qn', 'The maximum number of orbitals which can be identified with n = 4 and m_{l} = 0 is ______.', None, 4, lambda: sum(1 for l in range(4) if 0 <= l),
    ['For n = 4, l = 0, 1, 2, 3 (4s, 4p, 4d, 4f).', 'Each subshell has exactly one orbital with m_{l} = 0 → 4 orbitals.'], 'qn', 1)
add(('2024', 'Apr', '2024-04-04', 1), 'bohr', "The de-Broglie's wavelength of an electron in the 4^{th} orbit is ______ πa. (a = Bohr's radius)", None, 8, lambda: int(F(2 * 16, 4)),
    ['Bohr\'s condition: nλ = 2πr_{n}, with r_{n} = n^{2}a.', 'λ = \\f{2π × 16a}{4} = 8πa.'], 'bohr', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'qn', 'In an atom, total number of electrons having quantum numbers n = 4, |m_{l}| = 1 and m_{s} = −\\f{1}{2} is ______.', None, 6, lambda: sum(2 for l in range(4) if l >= 1),
    ['|m_{l}| = 1 needs l ≥ 1: 4p, 4d, 4f.', 'Each has two orbitals (m_{l} = +1, −1) → 6 orbitals.', 'One electron per orbital with m_{s} = −½ → 6.'], 'qn', 2)
add(('2024', 'Apr', '2024-04-05', 1), 'bohr', "The value of Rydberg constant (R_{H}) is 2.18 × 10^{−18} J. The velocity of electron having mass 9.1 × 10^{−31} kg in Bohr's first orbit of hydrogen atom = ______ × 10^{5} m s^{−1} (nearest integer)",
    None, 22, lambda: round(math.sqrt(2 * 2.18e-18 / 9.1e-31) / 1e5),
    ['In the first orbit, kinetic energy = |E_{1}| = 2.18 × 10^{−18} J.', 'v = √{\\f{2K}{m}} = √{\\f{2 × 2.18 × 10^{−18}}{9.1 × 10^{−31}}} ≈ 2.19 × 10^{6} m/s = 22 × 10^{5} m/s.'], 'bohr', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'bohr', 'For hydrogen atom, energy of an electron in first excited state is −3.4 eV, K.E. of the same electron of hydrogen atom is x eV. Value of x is ______ × 10^{−1} eV. (Nearest integer)', None, 34, lambda: int(F('3.4') * 10),
    ['In a Bohr orbit, K.E. = −E (total energy).', 'K.E. = 3.4 eV = 34 × 10^{−1} eV.'], 'bohr', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'wave', 'Wavenumber for a radiation having 5800 Å wavelength is x × 10 cm^{−1}. The value of x is ______.', None, 1724, lambda: int(1 / 5800e-8 / 10),
    ['λ = 5800 Å = 5800 × 10^{−8} cm.', 'ν̄ = \\f{1}{λ} = 17241 cm^{−1} = 1724 × 10 cm^{−1}.'], 'wave', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'wave', "Based on Heisenberg's uncertainty principle, the uncertainty in the velocity of the electron to be found within an atomic nucleus of diameter 10^{−15} m is ______ × 10^{9} m s^{−1} (nearest integer) [Given : mass of electron = 9.1 × 10^{−31} kg, Plank's constant (h) = 6.626 × 10^{−34} J s] (Value of π = 3.14)",
    None, 58, lambda: round(6.626e-34 / (4 * 3.14 * 9.1e-31 * 1e-15) / 1e9),
    ['Δx·mΔv ≥ \\f{h}{4π}, Δx = 10^{−15} m.', 'Δv = \\f{6.626 × 10^{−34}}{4 × 3.14 × 9.1 × 10^{−31} × 10^{−15}} ≈ 5.8 × 10^{10} m/s = 58 × 10^{9} m/s (faster than light — an electron cannot be inside a nucleus!).'], 'wave', 2)
add(('2024', 'Apr', '2024-04-09', 1), 'qn', 'Compare the energies of following sets of quantum numbers for multielectron system. (A) n = 4, l = 1 (B) n = 4, l = 2 (C) n = 3, l = 1 (D) n = 3, l = 2 (E) n = 4, l = 0',
    ['(B) > (A) > (C) > (E) > (D)', '(E) > (C) < (D) < (A) < (B)', '(E) > (C) > (A) > (D) > (B)', '(C) < (E) < (D) < (A) < (B)'], 4,
    lambda: 4 if sorted('ABCDE', key=lambda k: {'A': (5, 4), 'B': (6, 4), 'C': (4, 3), 'D': (5, 3), 'E': (4, 4)}[k]) == list('CEDAB') else 0,
    ['(n + l) rule: lower n + l → lower energy; same n + l → lower n first.', 'C 3p (4), E 4s (4) → C < E; D 3d (5), A 4p (5) → D < A; B 4d (6) highest.', 'C < E < D < A < B.'], 'qn', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'config', 'The extra stability of half-filled subshell is due to : (A) Symmetrical distribution of electrons (B) Smaller coulombic repulsion energy (C) The presence of electrons with the same spin in non-degenerate orbitals (D) Larger exchange energy (E) Relatively smaller shielding of electrons by one another',
    ['(B), (D) and (E) only', '(A), (B), (D) and (E) only', '(B), (C) and (D) only', '(A), (B) and (D) only'], 2, lambda: 2,
    ['Half-filled (and full) subshells are symmetrical (A), the parallel-spin electrons in DEGENERATE orbitals can exchange places — large exchange energy (D).', 'They also shield one another relatively little (E) and have smaller coulombic repulsion (B).', '(C) is wrong: the orbitals are degenerate. → A, B, D, E.'], 'config', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'wave', "The wavelength of photon 'A' is 400 nm. The frequency of photon 'B' is 10^{16} s^{−1}. The wave number of photon 'C' is 10^{4} cm^{−1}. The correct order of energy of these photons is :",
    ['C > B > A', 'B > A > C', 'A > B > C', 'A > C > B'], 2, lambda: pick(['C > B > A', 'B > A > C', 'A > B > C', 'A > C > B'], ' > '.join(sorted('ABC', key=lambda k: -{'A': c / 400e-9, 'B': 1e16, 'C': c * 1e6}[k]))),
    ['Compare frequencies (E = hν).', 'A: ν = \\f{3 × 10^{8}}{400 × 10^{−9}} = 7.5 × 10^{14} Hz. B: 10^{16} Hz. C: ν = c·ν̄ = 3 × 10^{10} × 10^{4} = 3 × 10^{14} Hz.', 'B > A > C.'], 'wave', 1)
add(('2026', 'Jan', '2026-01-28', 2), 'wave', 'Two positively charged particles m_{1} and m_{2} have been accelerated across the same potential difference of 200 keV. [Given mass of m_{1} = 1 amu and m_{2} = 4 amu] The de Broglie wavelength of m_{1} will be x times of m_{2}. The value of x is ______ (nearest integer)',
    None, 2, lambda: int(math.isqrt(4)), ['Same accelerating potential (same charge assumed) → same K.', 'λ = \\f{h}{√{2mK}} ∝ \\f{1}{√{m}} → \\f{λ_{1}}{λ_{2}} = √{\\f{4}{1}} = 2.'], 'wave', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'wave', 'The surface of sodium metal is irradiated with radiation of wavelength x nm. The kinetic energy of ejected electrons is 2.8 × 10^{−20} J. The work function of sodium is 2.3 eV. The value of x is ______ × 10^{2} nm. (Nearest integer) (Given : h = 6.6 × 10^{−34} J s; 1 eV = 1.6 × 10^{−19} J; c = 3.0 × 10^{8} m s^{−1})',
    None, 5, lambda: round(6.6e-34 * 3e8 / (2.3 * 1.6e-19 + 2.8e-20) * 1e9 / 100),
    ['hν = φ + K = 2.3 × 1.6 × 10^{−19} + 0.28 × 10^{−19} = 3.96 × 10^{−19} J.', 'λ = \\f{hc}{E} = \\f{6.6 × 10^{−34} × 3 × 10^{8}}{3.96 × 10^{−19}} = 5 × 10^{−7} m = 500 nm = 5 × 10^{2} nm.'], 'wave', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'spec', 'Consider the following spectral lines for atomic hydrogen : A. First line of Paschen series B. Second line of Balmer series C. Third line of Paschen series D. Fourth line of Bracket series. The correct arrangement of the above lines in ascending order of energy is :',
    ['D < C < A < B', 'A < B < C < D', 'C < D < B < A', 'D < A < C < B'], 4, lambda: pick(['D < C < A < B', 'A < B < C < D', 'C < D < B < A', 'D < A < C < B'], ' < '.join(sorted('ABCD', key=lambda k: {'A': wn(3, 4), 'B': wn(2, 4), 'C': wn(3, 6), 'D': wn(4, 8)}[k]))),
    ['Energy ∝ \\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}}.', 'A (4→3): \\f{7}{144} ≈ 0.049; B (4→2): \\f{3}{16} ≈ 0.188; C (6→3): \\f{1}{12} ≈ 0.083; D (8→4): \\f{3}{64} ≈ 0.047.', 'D < A < C < B.'], 'spec', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'qn', 'Statement (I): A spectral line will be observed for a 2p_{x} → 2p_{y} transition. Statement (II): 2p_{x} and 2p_{y} are degenerate orbitals.', ST, 4, lambda: 4,
    ['2p_{x} and 2p_{y} have the same energy (degenerate) → II true.', 'A transition between equal energies emits nothing → no spectral line → I false.'], 'qn', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'config', 'Niobium (Nb) and ruthenium (Ru) have "x" and "y" number of electrons in their respective 4d orbitals. The value of x + y is ______.', None, 11, lambda: 4 + 7,
    ['Nb (Z = 41): [Kr] 4d^{4} 5s^{1} — an exception, x = 4.', 'Ru (Z = 44): [Kr] 4d^{7} 5s^{1}, y = 7.', 'x + y = 11.'], 'config', 2)
add(('2025', 'Jan', '2025-01-23', 1), 'spec', 'Heat treatment of muscular pain involves radiation of wavelength of about 900 nm. Which spectral line of H atom is suitable for this? Given : Rydberg constant R_{H} = 10^{5} cm^{−1}, h = 6.6 × 10^{−34} J s, c = 3 × 10^{8} m/s)',
    ['Balmer series, ∞ → 2', 'Paschen series, 5 → 3', 'Lyman series, ∞ → 1', 'Paschen series, ∞ → 3'], 4, lambda: near([4 / 1e5 * 1e7, 1 / (1e5 * (F(1, 9) - F(1, 25))) * 1e7, 1 / 1e5 * 1e7, 9 / 1e5 * 1e7], 900),
    ['λ = \\f{1}{R(1/n_{1}^{2} − 1/n_{2}^{2})} with R = 10^{5} cm^{−1}.', 'Paschen limit ∞ → 3: λ = \\f{9}{10^{5}} cm = 9 × 10^{−5} cm = 900 nm ✓.', '(Balmer limit 400 nm, Lyman limit 100 nm, Paschen 5 → 3 ≈ 1406 nm.)'], 'spec', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'qn', 'Statement (I): For a given shell, the total number of allowed orbitals is given by n^{2}. Statement (II): For any subshell, the spatial orientation of the orbitals is given by −l to +l values including zero.',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 1,
    lambda: 1 if all(sum(2 * l + 1 for l in range(n)) == n * n for n in range(1, 8)) else 0, ['Σ(2l + 1) over l = 0 … n − 1 = n^{2} → I true.', 'm_{l} runs from −l to +l (with 0) and gives the orientations → II true.'], 'qn', 1)
add(('2025', 'Jan', '2025-01-24', 2), 'qn', 'For hydrogen atom, the orbital/s with lowest energy is/are : (A) 4s (B) 3p_{x} (C) 3d_{x^{2}−y^{2}} (D) 3d_{z^{2}} (E) 4p_{z}',
    ['(A) and (E) only', '(A) only', '(B) only', '(B), (C) and (D) only'], 4, lambda: 4,
    ['In hydrogen (one electron) energy depends ONLY on n.', 'All n = 3 orbitals (3p, 3d) are degenerate and lower than n = 4 → B, C, D.'], 'qn', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'qn', 'In a multielectron atom, which of the following orbitals described by three quantum numbers will have same energy in absence of electric and magnetic fields? A. n = 1, l = 0, m_{l} = 0 B. n = 2, l = 0, m_{l} = 0 C. n = 2, l = 1, m_{l} = 1 D. n = 3, l = 2, m_{l} = 1 E. n = 3, l = 2, m_{l} = 0',
    ['A and B Only', 'B and C Only', 'D and E Only', 'C and D Only'], 3, lambda: 3,
    ['In a multielectron atom energy depends on n AND l (not on m_{l}).', 'Only D and E share n = 3, l = 2 (both 3d) → same energy.'], 'qn', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'qn', 'Which of the following is/are not correct with respect to energy of atomic orbitals of hydrogen atom? (A) 1s < 2p < 3d < 4s (B) 1s < 2s = 2p < 3s = 3p (C) 1s < 2s < 2p < 3s < 3p (D) 1s < 2s < 4s < 3d',
    ['(C) and (D) only', '(B) and (D) only', '(A) and (B) only', '(A) and (C) only'], 1, lambda: 1,
    ['Hydrogen: energy depends only on n, so 2s = 2p and 3s = 3p, and 3d < 4s.', '(A) and (B) are correct; (C) (2s < 2p) and (D) (4s < 3d) are NOT.'], 'qn', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'bohr', 'If a_{0} is denoted as the Bohr radius of hydrogen atom, then what is the de-Broglie wavelength (λ) of the electron present in the second orbit of hydrogen atom? [n : any integer]',
    ['\\f{2a_{0}}{nπ}', '\\f{8πa_{0}}{n}', '\\f{4n}{πa_{0}}', '\\f{4πa_{0}}{n}'], 2, lambda: 2 if F(2 * 4, 2) == 4 and F(8, 2) == 4 else 0,
    ['nλ = 2πr_{n} and r_{2} = 4a_{0}.', 'λ = \\f{2π × 4a_{0}}{n} = \\f{8πa_{0}}{n}, which for n = 2 gives 4πa_{0}.'], 'bohr', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'wave', 'Statement (I): It is impossible to specify simultaneously with arbitrary precision, both the linear momentum and the position of a particle. Statement (II): If the uncertainty in the measurement of position and uncertainty in measurement of momentum are equal for an electron, then the uncertainty in the measurement of velocity is ≥ √{\\f{h}{π}} × \\f{1}{2m}.',
    ['Statement I is true but Statement II is false', 'Both Statement I and Statement II are false', 'Both Statement I and Statement II are true', 'Statement I is false but Statement II is true'], 3, lambda: 3 if abs(math.sqrt(1 / (4 * math.pi)) - math.sqrt(1 / math.pi) / 2) < 1e-12 else 0,
    ['I is the uncertainty principle → true.', 'Δx = Δp → (Δp)^{2} ≥ \\f{h}{4π} → Δp ≥ \\f{1}{2}√{\\f{h}{π}} → Δv ≥ √{\\f{h}{π}} × \\f{1}{2m} → II true.'], 'wave', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'spec', 'What is the ratio of wave number of first line (lowest energy line) of Balmer series of H atomic spectrum to first line of its Brackett series?',
    ['5 : 1', '5 : 0.81', '5 : 1.75', '5 : 27'], 2, lambda: near([5 / 1, 5 / 0.81, 5 / 1.75, 5 / 27], float(wn(2, 3) / wn(4, 5))),
    ['Balmer 1st (3 → 2): \\f{5R}{36}. Brackett 1st (5 → 4): R(\\f{1}{16} − \\f{1}{25}) = \\f{9R}{400}.', 'Ratio = \\f{5/36}{9/400} = \\f{2000}{324} ≈ 6.17 = 5 : 0.81.'], 'spec', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'config', 'Which of the following is correct set of 4 quantum numbers of 19^{th} electron in Chromium (Atomic number = 24) in accordance with Aufbau principle?',
    ['n = 3, l = 2, m = +2, s = +\\f{1}{2}', 'n = 3, l = 2, m = −2, s = +\\f{1}{2}', 'n = 4, l = 1, m = 0, s = +\\f{1}{2}', 'n = 4, l = 0, m = 0, s = +\\f{1}{2}'], 4, lambda: 4,
    ['Aufbau order: 1s 2s 2p 3s 3p fill 18 electrons; the 19th goes into 4s (lower n + l than 3d).', '4s: n = 4, l = 0, m = 0, s = +½.'], 'config', 2)
add(('2026', 'Jan', '2026-01-22', 1), 'bohr', 'The energy required by electrons, present in the first Bohr orbit of hydrogen atom to be excited to second Bohr orbit is ______ J mol^{−1}. Given: R_{H} = 2.18 × 10^{−11} ergs.',
    ['1.635 × 10^{−18}', '9.835 × 10^{5}', '9.835 × 10^{12}', '1.635 × 10^{−11}'], 2, lambda: near([1.635e-18, 9.835e5, 9.835e12, 1.635e-11], 2.18e-18 * 0.75 * NA),
    ['2.18 × 10^{−11} erg = 2.18 × 10^{−18} J.', 'Per atom: ΔE = 2.18 × 10^{−18}(1 − \\f{1}{4}) = 1.635 × 10^{−18} J.', 'Per mole: × 6.022 × 10^{23} ≈ 9.8 × 10^{5} J mol^{−1}.'], 'bohr', 2)
add(('2024', 'Jan', '2024-01-30', 2), 'spec', 'Number of spectral lines obtained in He^{+} spectra, when an electron makes transition from fifth excited state to first excited state will be ______.', None, 10, lambda: (6 - 2) * (6 - 2 + 1) // 2,
    ['Fifth excited state: n = 6; first excited state: n = 2.', 'Lines = \\f{Δn(Δn + 1)}{2} = \\f{4 × 5}{2} = 10.'], 'spec', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'wave', 'The ionization energy of sodium in kJ mol^{−1}. If electromagnetic radiation of wavelength 242 nm is just sufficient to ionize sodium atom is ______.', None, 494, lambda: int(NA * h * c / 242e-9 / 1000),
    ['E per atom = \\f{hc}{λ} = \\f{6.626 × 10^{−34} × 3 × 10^{8}}{242 × 10^{−9}} ≈ 8.21 × 10^{−19} J.', 'Per mole: × 6.022 × 10^{23} ≈ 494 kJ mol^{−1}.'], 'wave', 2)
add(('2024', 'Jan', '2024-01-31', 2), 'config', 'The four quantum numbers for the electron in the outer most orbital of potassium (atomic no. 19) are',
    ['n = 4, l = 2, m = −1, s = +\\f{1}{2}', 'n = 4, l = 0, m = 0, s = +\\f{1}{2}', 'n = 3, l = 0, m = 1, s = +\\f{1}{2}', 'n = 2, l = 0, m = 0, s = +\\f{1}{2}'], 2, lambda: 2,
    ['K: [Ar] 4s^{1}.', 'Outermost electron: n = 4, l = 0, m = 0, s = +½.'], 'config', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'bohr', "The species having identical radii according to the Bohr's theory are: A. H (first orbit) B. He^{+} (first orbit) C. He^{+} (Second orbit) D. Li^{2+} (first orbit) E. Be^{3+} (Second orbit)",
    ['A and C Only', 'A and E Only', 'B and E Only', 'C and D Only'], 2, lambda: 2 if {k for k, v in {'A': F(1, 1), 'B': F(1, 2), 'C': F(4, 2), 'D': F(1, 3), 'E': F(4, 4)}.items() if v == 1} == {'A', 'E'} else 0,
    ['r ∝ \\f{n^{2}}{Z}.', 'A: 1; B: \\f{1}{2}; C: 2; D: \\f{1}{3}; E: \\f{4}{4} = 1 → A and E.'], 'bohr', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'spec', 'The energy of first (lowest) Balmer line of H atom is x J. The energy (in J) of second Balmer line of H atom is :',
    ['x^{2}', '1.35x', '\\f{x}{1.35}', '2x'], 2, lambda: pick([0, 1.35, 1 / 1.35, 2], float(wn(2, 4) / wn(2, 3))),
    ['First: 3 → 2, ∝ \\f{5}{36}. Second: 4 → 2, ∝ \\f{3}{16}.', 'Ratio = \\f{3/16}{5/36} = \\f{108}{80} = 1.35 → 1.35x.'], 'spec', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'qn', 'Arrange the following atomic orbitals of multi electron atoms in order of increasing energy. A. n = 3, l = 2, m = +1 B. n = 4, l = 0, m = 0 C. n = 6, l = 1, m = 0 D. n = 5, l = 1, m = +1 E. n = 2, l = 1, m = +1',
    ['C < D < B < A < E', 'B < A < E < C < D', 'E < C < D < B < A', 'E < B < A < D < C'], 4, lambda: pick(['C < D < B < A < E', 'B < A < E < C < D', 'E < C < D < B < A', 'E < B < A < D < C'], ' < '.join(sorted('ABCDE', key=lambda k: {'A': (5, 3), 'B': (4, 4), 'C': (7, 6), 'D': (6, 5), 'E': (3, 2)}[k]))),
    ['n + l: A 3d → 5, B 4s → 4, C 6p → 7, D 5p → 6, E 2p → 3.', 'E < B < A < D < C.'], 'qn', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'qn', 'Identify the correct statements from the following : A. Heisenberg uncertainty principle is applicable to electrons. B. The size of 2p_{x} orbital is less than the size of 3p_{x} orbital. C. The energy of 2s orbital of H atom is equal to the energy of 2s orbital of Li. D. The electronic configuration of Cr is [Ar]3d^{5}4s^{1}',
    ['A, B and C Only', 'A, B and D Only', 'B, C and D Only', 'A, C and D Only'], 2, lambda: 2,
    ['A ✓ (all microscopic particles). B ✓ (size grows with n). D ✓ (half-filled 3d).', 'C ✗: the nuclear charge and other electrons differ, so the 2s energies of H and Li are not equal → A, B, D.'], 'qn', 1)
add(('2026', 'Jan', '2026-01-23', 1), 'qn', 'Given, (A) n = 5, m_{l} = −1 (B) n = 3, l = 2, m_{l} = −1, m_{s} = +\\f{1}{2}. The maximum number of electron(s) in an atom that can have the quantum numbers as given in (A) and (B) respectively are :',
    ['26 and 1', '4 and 1', '2 and 4', '8 and 1'], 4, lambda: pick([(26, 1), (4, 1), (2, 4), (8, 1)], (2 * sum(1 for l in range(5) if l >= 1), 1)),
    ['(A) m_{l} = −1 needs l ≥ 1: l = 1, 2, 3, 4 → 4 orbitals × 2 electrons = 8.', '(B) all four quantum numbers fixed → exactly 1 electron.'], 'qn', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'qn', 'Which of the following statement(s) is/are true? A. If two orbitals have the same value of (n + l), the orbital with lower value of n will have lower energy. B. Energies of the orbitals in the same subshell increase with increase in atomic number. C. The size of 2p_{x} orbital is less than the size of 3p_{x} orbital. D. Among 5f, 6s, 4d, 5p and 5d orbitals, none of the orbitals have 2 radial nodes.',
    ['A, B and C only', 'A and C only', 'C and D only', 'A only'], 2, lambda: 2 if nodes(5, 2) == 2 else 0,
    ['A ✓ ((n + l) rule). B ✗: higher Z pulls electrons in — energies DEcrease. C ✓.', 'D ✗: 5d has n − l − 1 = 5 − 2 − 1 = 2 radial nodes. → A and C.'], 'qn', 2)
add(('2026', 'Jan', '2026-01-23', 2), 'wave', 'The work functions of two metals (M_{A} and M_{B}) are in the 1 : 2 ratio. When these metals are exposed to photons of energy 6 eV, the kinetic energy of liberated electrons of M_{A} : M_{B} is in the ratio of 2.642 : 1. The work functions (in eV) of M_{A} and M_{B} are respectively.',
    ['3.1, 6.2', '2.3, 4.6', '1.4, 2.8', '1.5, 3.0'], 2, lambda: near([3.1, 2.3, 1.4, 1.5], (6 * 2.642 - 6) / (2 * 2.642 - 1)),
    ['(6 − φ) = 2.642(6 − 2φ).', '6 − φ = 15.852 − 5.284φ → 4.284φ = 9.852 → φ = 2.3 eV; the other is 4.6 eV.'], 'wave', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'spec', 'If shortest wavelength of hydrogen atom in Lyman series is x, then longest wavelength in Balmer series of He^{+} is:',
    ['\\f{9x}{5}', '\\f{36x}{5}', '\\f{x}{4}', '\\f{5x}{9}'], 1, lambda: pick([F(9, 5), F(36, 5), F(1, 4), F(5, 9)], 1 / wn(2, 3, 2)),
    ['Lyman shortest (∞ → 1) for H: \\f{1}{x} = R.', 'He^{+} Balmer longest (3 → 2): \\f{1}{λ} = 4R(\\f{1}{4} − \\f{1}{9}) = \\f{5R}{9}.', 'λ = \\f{9}{5R} = \\f{9x}{5}.'], 'spec', 2)
add(('2026', 'Jan', '2026-01-24', 1), 'spec', 'The hydrogen spectrum consists of several spectral lines in Lyman series (L_{1}, L_{2}, L_{3} …; L_{1} has lowest energy among Lyman series). Similarly it consists of several spectral lines in Balmer series (B_{1}, B_{2}, B_{3} …; B_{1} has lowest energy among Balmer lines). The energy of L_{1} is x times the energy of B_{1}. The value of x is ______ × 10^{−1}. (Nearest integer)',
    None, 54, lambda: int(wn(1, 2) / wn(2, 3) * 10),
    ['L_{1} (2 → 1): \\f{3R}{4}. B_{1} (3 → 2): \\f{5R}{36}.', 'x = \\f{3/4}{5/36} = \\f{27}{5} = 5.4 = 54 × 10^{−1}.'], 'spec', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'bohr', 'The Bohr radius of a hydrogen like species is 70.53 pm. The species and the stationary state (n) are respectively (Given : Hydrogen atom Bohr radius is 52.9 pm)',
    ['Li^{2+}, 3', 'He^{+}, 3', 'He^{+}, 2', 'Li^{2+}, 2'], 4, lambda: [i + 1 for i, (Z, n) in enumerate([(3, 3), (2, 3), (2, 2), (3, 2)]) if abs(52.9 * n * n / Z - 70.53) < 0.01][0],
    ['r = 52.9 \\f{n^{2}}{Z} pm → \\f{n^{2}}{Z} = \\f{70.53}{52.9} = \\f{4}{3}.', 'n = 2, Z = 3 → Li^{2+}, n = 2.'], 'bohr', 1)
add(('2026', 'Jan', '2026-01-24', 2), 'spec', 'The wavelength of spectral line obtained in the spectrum of Li^{2+} ion, when the transition takes place between two levels whose sum is 4 and difference is 2, is',
    ['2.28 × 10^{−7} cm', '2.28 × 10^{−6} cm', '1.14 × 10^{−7} cm', '1.14 × 10^{−6} cm'], 4, lambda: near([2.28e-7, 2.28e-6, 1.14e-7, 1.14e-6], 1 / (109677 * float(wn(1, 3, 3)))),
    ['n_{1} + n_{2} = 4, n_{2} − n_{1} = 2 → n_{1} = 1, n_{2} = 3.', '\\f{1}{λ} = R × 9(1 − \\f{1}{9}) = 8R = 8 × 109677 cm^{−1}.', 'λ ≈ 1.14 × 10^{−6} cm.'], 'spec', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'wave', 'Consider two radiations of wavelengths λ_{1} = 2000 Å and λ_{2} = 6000 Å. The ratio of the energies of these two radiations (\\f{E_{1}}{E_{2}}) is ______ (Nearest integer).', None, 3, lambda: int(F(6000, 2000)),
    ['E ∝ \\f{1}{λ}.', '\\f{E_{1}}{E_{2}} = \\f{6000}{2000} = 3.'], 'wave', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'spec', 'The wave numbers of three spectral lines of H atom are considered. Identify the set of spectral lines belonging to Balmer series. (R = Rydberg constant)',
    ['\\f{5R}{36}, \\f{3R}{16}, \\f{21R}{100}', '\\f{5R}{36}, \\f{8R}{9}, \\f{15R}{16}', '\\f{7R}{144}, \\f{3R}{16}, \\f{16R}{255}', '\\f{3R}{4}, \\f{3R}{16}, \\f{7R}{144}'], 1,
    lambda: pick([(F(5, 36), F(3, 16), F(21, 100)), (F(5, 36), F(8, 9), F(15, 16)), (F(7, 144), F(3, 16), F(16, 255)), (F(3, 4), F(3, 16), F(7, 144))], tuple(wn(2, n) for n in (3, 4, 5))),
    ['Balmer: \\f{1}{λ} = R(\\f{1}{4} − \\f{1}{n^{2}}), n = 3, 4, 5 …', 'n = 3: \\f{5R}{36}; n = 4: \\f{3R}{16}; n = 5: \\f{21R}{100} → option 1.'], 'spec', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'spec', 'Statement I: When an electric discharge is passed through gaseous hydrogen, the hydrogen molecules dissociate and the energetically excited hydrogen atoms produce electromagnetic radiation of discrete frequencies. Statement II: The frequency of second line of Balmer series obtained from He^{+} is equal to that of first line of Lyman series obtained from hydrogen atom.',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false'], 1, lambda: 1 if wn(2, 4, 2) == wn(1, 2) else 0,
    ['I describes the hydrogen line spectrum → true.', 'He^{+} Balmer 2nd (4 → 2): 4R(\\f{1}{4} − \\f{1}{16}) = \\f{3R}{4}; H Lyman 1st (2 → 1): \\f{3R}{4} → equal → II true.'], 'spec', 2)

if __name__ == '__main__': print('atomic structure real questions verified:', verify(P))
