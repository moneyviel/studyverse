"""Concept cards for Chemistry Unit 2 — Atomic Structure (written for StudyVerse)."""
TOPICS = {'bohr': "Bohr's model", 'spec': 'Hydrogen spectrum', 'qn': 'Quantum numbers & orbitals', 'config': 'Electronic configuration', 'wave': 'Light, matter waves & uncertainty'}
CARDS = [
 dict(id='c1', t='Light as wave and photon', e='🌈', lvl='f', topic='wave',
  body=['c = νλ, wave number ν̄ = \\f{1}{λ} (usually in cm^{−1}). E = hν = \\f{hc}{λ} = hcν̄.', 'One mole of photons ("einstein") carries N_{A}hν. A 242 nm mole of photons ≈ 494 kJ — just enough to ionise sodium.',
        'Photoelectric effect: hν = φ + \\f{1}{2}mv^{2}. No emission below the threshold frequency, however bright the light.'],
  check=dict(q='Wave number of 5000 Å light :', o=['2000 cm^{−1}', '20000 cm^{−1}', '200 cm^{−1}', '2 × 10^{6} cm^{−1}'], a=1, why='1/(5000 × 10^{−8} cm) = 20000 cm^{−1}.')),
 dict(id='c2', t="Bohr's model", e='🪐', lvl='m', topic='bohr',
  body=['Postulates: electrons move in fixed circular orbits without radiating; angular momentum is quantised mvr = n\\f{h}{2π}; energy is emitted/absorbed only when jumping between orbits.',
        'For H-like species (one electron, nuclear charge Z): <div class="jx-f">r_{n} = 52.9\\f{n^{2}}{Z} pm,  v_{n} = 2.18 × 10^{6}\\f{Z}{n} m/s,  E_{n} = −13.6\\f{Z^{2}}{n^{2}} eV = −2.18 × 10^{−18}\\f{Z^{2}}{n^{2}} J</div>',
        'K.E. = −E, P.E. = 2E. Ionisation energy from n = 1: 13.6Z^{2} eV.', 'de Broglie fits the orbit: 2πr_{n} = nλ → λ = 2πna_{0} for hydrogen.',
        'Limits: works only for one-electron species; cannot explain fine structure, Zeeman/Stark effects or chemical bonding.'],
  check=dict(q='Radius of He^{+} in its 2nd orbit compared with H in its 1st :', o=['equal', '2 times', '4 times', 'half'], a=1, why='r ∝ n^{2}/Z = 4/2 = 2.')),
 dict(id='c3', t='The hydrogen spectrum', e='📊', lvl='m', topic='spec',
  body=['<div class="jx-f">ν̄ = \\f{1}{λ} = RZ^{2}(\\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}}),  R = 109677 cm^{−1}</div>',
        'Series by the LOWER level n_{1}: Lyman 1 (UV), Balmer 2 (visible), Paschen 3, Brackett 4, Pfund 5 (IR).', 'First line (longest λ, lowest energy): n_{2} = n_{1} + 1. Series limit (shortest λ): n_{2} = ∞ → ν̄ = R/n_{1}^{2}.',
        'Number of lines from level n down to level m in many atoms: \\f{(n − m)(n − m + 1)}{2}.', 'He^{+} lines are hydrogen lines × Z^{2} = 4: He^{+} (4 → 2) equals H (2 → 1).'],
  check=dict(q='The longest wavelength of the Balmer series comes from :', o=['∞ → 2', '3 → 2', '2 → 1', '4 → 2'], a=1, why='Smallest energy gap within the series.')),
 dict(id='c4', t='Uncertainty and the quantum model', e='🎲', lvl='m', topic='wave',
  body=['Heisenberg: <div class="jx-f">Δx·Δp ≥ \\f{h}{4π}</div> — position and momentum cannot both be exact. Important only for tiny masses (electrons).',
        'So orbits are replaced by ORBITALS: regions where the probability |ψ|^{2} of finding the electron is high.', 'Nodes: radial = n − l − 1, angular = l, total = n − 1. 1s has no node; 2s has one radial node; every p orbital has one nodal plane.'],
  check=dict(q='Radial nodes in 4d :', o=['0', '1', '2', '3'], a=1, why='4 − 2 − 1 = 1.')),
 dict(id='c5', t='Quantum numbers', e='🔢', lvl='f', topic='qn',
  body=['n (principal: shell, size, energy) = 1, 2, 3 …', 'l (azimuthal: subshell shape) = 0 … n − 1 → s, p, d, f. Orbital angular momentum √{l(l + 1)}\\f{h}{2π}.',
        'm_{l} (magnetic: orientation) = −l … +l → 2l + 1 orbitals. m_{s} = ±½.', 'A shell has n subshells, n^{2} orbitals and 2n^{2} electrons.',
        'Counting trick: "electrons with n = 4, |m_{l}| = 1" → l can be 1, 2, 3 → 6 orbitals → 12 electrons (6 if m_{s} is also fixed).'],
  check=dict(q='Maximum electrons with n = 3 :', o=['9', '18', '6', '32'], a=1, why='2n^{2} = 18.')),
 dict(id='c6', t='Filling orbitals: Aufbau, Pauli, Hund', e='🧱', lvl='f', topic='config',
  body=['<b>Aufbau</b>: fill in order of increasing (n + l); equal n + l → lower n first: 1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s …',
        '<b>Pauli</b>: no two electrons have all four quantum numbers equal → max 2 per orbital, opposite spins. <b>Hund</b>: in degenerate orbitals pair only after each has one electron.',
        'Exceptions from extra stability of half-filled/filled d: Cr 3d^{5}4s^{1}, Cu 3d^{10}4s^{1} (also Mo, Ag, Au; Nb 4d^{4}5s^{1}, Ru 4d^{7}5s^{1}, Pd 4d^{10}).',
        'In HYDROGEN energy depends only on n (2s = 2p). In many-electron atoms it depends on n and l.'],
  check=dict(q='Ground state of Cu :', o=['[Ar]3d^{9}4s^{2}', '[Ar]3d^{10}4s^{1}', '[Ar]3d^{10}', '[Ar]3d^{8}4s^{2}4p^{1}'], a=1, why='Filled 3d is extra stable.')),
]
FORMULAS = [('Photon', 'E = hν = \\f{hc}{λ},  ν̄ = \\f{1}{λ}'), ('Bohr radius', 'r_{n} = 52.9\\f{n^{2}}{Z} pm'), ('Bohr speed', 'v_{n} = 2.18 × 10^{6}\\f{Z}{n} m/s'), ('Bohr energy', 'E_{n} = −13.6\\f{Z^{2}}{n^{2}} eV'),
            ('Spectrum', 'ν̄ = RZ^{2}(\\f{1}{n_{1}^{2}} − \\f{1}{n_{2}^{2}})'), ('Lines', 'N = \\f{Δn(Δn + 1)}{2}'), ('de Broglie', 'λ = \\f{h}{mv};  orbit: 2πr = nλ'), ('Uncertainty', 'Δx·Δp ≥ \\f{h}{4π}'),
            ('Nodes', 'radial n − l − 1, angular l'), ('Orbital momentum', '√{l(l + 1)}\\f{h}{2π}'), ('Capacity', 'shell: n^{2} orbitals, 2n^{2} e^{−}')]
TRAPS = ['In hydrogen 2s = 2p; in multi-electron atoms 2s < 2p.', 'K.E. in a Bohr orbit equals −E; P.E. = 2E.', 'First line of a series = LONGEST wavelength.', 'Fifth excited state means n = 6.',
         'Cr and Cu break the simple Aufbau order.', 'A transition between degenerate orbitals emits no line.', 'Orbital angular momentum depends on l only, not on n.']
STEPS = [dict(k='s1', t='Light and Bohr', e='🪐', cards=['c1', 'c2', 'c3'], need=['wave', 'bohr', 'spec'], note='Photons, Bohr orbits and the hydrogen spectrum'),
         dict(k='s2', t='Quantum model', e='🎲', cards=['c4', 'c5'], need=['qn'], note='Uncertainty, orbitals, quantum numbers and nodes'),
         dict(k='s3', t='Configurations', e='🧱', cards=['c6'], need=['config'], note='Aufbau, Pauli, Hund and the exceptions')]
META = dict(unit='chem-u02', subject='chem', n=2, title='Atomic Structure', cls=11, labs=['bohr', 'orbital'],
            syllabus="Nature of electromagnetic radiation; photoelectric effect; spectrum of hydrogen atom; Bohr model and its limitations; dual behaviour of matter; de Broglie relationship; Heisenberg uncertainty principle; quantum numbers; shapes of s, p and d orbitals; nodes; rules for filling electrons (Aufbau, Pauli, Hund); electronic configuration; extra stability of half-filled and completely filled orbitals.")
