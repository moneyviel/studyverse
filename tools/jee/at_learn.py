"""Concept cards for Physics Unit 18 — Atoms and Nuclei (written for StudyVerse)."""
TOPICS = {'bohr': 'Bohr model', 'spec': 'Hydrogen spectrum', 'ruth': 'Rutherford scattering & matter waves', 'nuc': 'Nucleus, binding energy, fission & fusion', 'decay': 'Radioactivity'}
CARDS = [
 dict(id='c1', t='Rutherford\'s nucleus', e='🎯', lvl='f', topic='ruth',
  body=['Most α-particles pass straight through gold foil; a very few bounce back → all the positive charge and almost all the mass sit in a tiny nucleus.', '<div class="jx-f">closest approach: K = \\f{k(2e)(Ze)}{r_{0}}</div>',
        'Only particles with a tiny impact parameter (nearly head-on) are thrown back. Thomson\'s "plum pudding" could not explain this.'],
  check=dict(q='Doubling the α energy makes the closest approach :', o=['double', 'half', 'same', '4 times'], a=1, why='r₀ ∝ 1/K.')),
 dict(id='c2', t='Bohr model', e='⚛️', lvl='m', topic='bohr',
  body=['<div class="jx-f">L = \\f{nh}{2π},  r_{n} = 0.529\\f{n^{2}}{Z} Å,  v_{n} = 2.19 × 10^{6}\\f{Z}{n} m/s,  E_{n} = −13.6\\f{Z^{2}}{n^{2}} eV</div>',
        'KE = −E, PE = 2E (so E = \\f{PE}{2}). f ∝ \\f{Z^{2}}{n^{3}}; magnetic moment ∝ n; field at the nucleus ∝ \\f{1}{n^{5}}.', 'Works only for one-electron atoms (H, He^{+}, Li^{2+}) — it ignores electron–electron repulsion.',
        'Same energy for two ions when \\f{Z}{n} is the same.'],
  check=dict(q='He⁺ in n = 2 has the same energy as H in :', o=['n = 1', 'n = 2', 'n = 4', 'n = 3'], a=0, why='Z/n = 1 for both.')),
 dict(id='c3', t='Hydrogen spectrum', e='🌈', lvl='m', topic='spec',
  body=['<div class="jx-f">\\f{1}{λ} = RZ^{2}(\\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}}),  R = 1.097 × 10^{7} m^{−1},  \\f{1}{R} ≈ 91.2 nm</div>',
        'Lyman (→1, UV), Balmer (→2, visible), Paschen (→3, IR). Longest λ = first line; shortest = series limit (n_{2} → ∞).', 'From level n, many atoms give \\f{n(n − 1)}{2} lines.',
        'To see any Balmer line from the ground state, give at least 12.09 eV (reach n = 3). An emitting atom recoils with p = \\f{E}{c}.'],
  check=dict(q='Shortest Balmer λ : shortest Lyman λ =', o=['4 : 1', '1 : 4', '9 : 4', '2 : 1'], a=0, why='4/R vs 1/R.')),
 dict(id='c4', t='The nucleus', e='🧲', lvl='m', topic='nuc',
  body=['<div class="jx-f">R = R_{0}A^{1/3} (R_{0} ≈ 1.2 fm),  Δm = Zm_{p} + (A − Z)m_{n} − M,  BE = Δm × 931.5 MeV</div>', 'Nuclear density is the same for all nuclei (~2.3 × 10^{17} kg/m^{3}).',
        'BE/A is about 8 MeV for 30 < A < 170, peaks near Fe-56, and is low for very light and very heavy nuclei. Nuclear force: strong, short-range, charge-independent.', 'Isotopes: same Z · isobars: same A · isotones: same N.'],
  check=dict(q='A nucleus with 8 times the mass number has radius :', o=['8×', '4×', '2×', 'same'], a=2, why='8^{1/3} = 2.')),
 dict(id='c5', t='Fission and fusion', e='💥', lvl='m', topic='nuc',
  body=['<div class="jx-f">Q = Σ BE(products) − Σ BE(reactants) = (mass before − mass after) × 931.5 MeV</div>', 'Heavy nuclei split (fission, ~200 MeV per U-235) and light ones join (fusion, e.g. 2 ^{2}H → ^{4}He) — both move towards higher BE/A.',
        'Balance A and Z in every reaction (neutrons: A = 1, Z = 0). In a two-body break-up from rest, momenta are equal and opposite: K ∝ \\f{1}{m}; α gets Q\\f{A − 4}{A}.', 'Beta decay: n → p + e^{−} + ν̄.'],
  check=dict(q='Fission of A = 236 (7.6 MeV/nucleon) into two A = 118 (8.5 MeV/nucleon) releases :', o=['212 MeV', '0.9 MeV', '106 MeV', '2006 MeV'], a=0, why='236 × 0.9.')),
 dict(id='c6', t='Radioactive decay', e='☢️', lvl='m', topic='decay',
  body=['<div class="jx-f">N = N_{0}e^{−λt} = N_{0}(\\f{1}{2})^{t/T},  T_{1/2} = \\f{ln 2}{λ},  τ = \\f{1}{λ},  A = λN</div>', 'After n half-lives, \\f{1}{2^{n}} remains. Activity falls the same way.',
        'Chain P → Q → R (stable): P falls, Q rises to a peak and falls, R keeps growing.'],
  check=dict(q='After 3 half-lives the fraction left is :', o=['1/3', '1/6', '1/8', '1/9'], a=2, why='(1/2)³.')),
]
FORMULAS = [('Bohr energy', 'E_{n} = −13.6\\f{Z^{2}}{n^{2}} eV'), ('Bohr radius', 'r_{n} = 0.529\\f{n^{2}}{Z} Å'), ('Angular momentum', 'L = \\f{nh}{2π}'), ('Rydberg', '\\f{1}{λ} = RZ^{2}(\\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}})'),
            ('Nuclear radius', 'R = R_{0}A^{1/3}'), ('Binding energy', 'BE = Δm × 931.5 MeV'), ('Decay', 'N = N_{0}e^{−λt}'), ('Half-life', 'T_{1/2} = \\f{0.693}{λ}'), ('Closest approach', 'r_{0} = \\f{k(2e)(Ze)}{K}'), ('de Broglie', 'λ = \\f{h}{√{2mK}}')]
TRAPS = ['"n-th excited state" is level n + 1.', 'Longest wavelength of a series = its FIRST line; shortest = its limit.', 'L is a multiple of h/2π, not of h.', 'Nuclear density does not depend on A.',
         'Neutrino goes with e⁺, antineutrino with e⁻.', 'Many atoms in level n: n(n − 1)/2 lines; ONE atom: at most n − 1.']
STEPS = [dict(k='s1', t='The atom', e='🎯', cards=['c1', 'c2'], need=['ruth', 'bohr'], note='Rutherford and Bohr'),
         dict(k='s2', t='Spectra', e='🌈', cards=['c3'], need=['spec'], note='Hydrogen spectral series'),
         dict(k='s3', t='The nucleus', e='🧲', cards=['c4', 'c5', 'c6'], need=['nuc', 'decay'], note='Size, binding energy, fission, fusion and decay')]
META = dict(unit='phy-u18', subject='phy', n=18, title='Atoms and Nuclei', cls=12, labs=['spectra'],
            syllabus='Alpha-particle scattering experiment; Rutherford\'s model of atom; Bohr model, energy levels, hydrogen spectrum. Composition and size of nucleus, atomic masses, mass-energy relation, mass defect; binding energy per nucleon and its variation with mass number, nuclear fission and fusion.')
