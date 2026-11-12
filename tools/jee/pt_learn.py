"""Concept cards for Chemistry Unit 9 — Classification of Elements & Periodicity (written for StudyVerse)."""
TOPICS = {'ie': 'Ionisation enthalpy', 'eg': 'Electron gain enthalpy & electronegativity', 'rad': 'Atomic & ionic radii', 'pt': 'Periodic law, table & nomenclature'}
CARDS = [
 dict(id='c1', t='The modern periodic table', e='🗂️', lvl='f', topic='pt',
  body=['Modern periodic law: properties are periodic functions of ATOMIC NUMBER (Mendeleev used atomic mass).',
        'Period = principal quantum number of the outer shell; a period holds 2 × (number of orbitals being filled) elements: 2, 8, 8, 18, 18, 32, 32.',
        'Blocks by last subshell: s (groups 1–2), p (13–18), d (3–12), f (lanthanoids/actinoids placed below).',
        'Elements beyond 100: digit roots nil 0, un 1, bi 2, tri 3, quad 4, pent 5, hex 6, sept 7, oct 8, enn 9 + "-ium" (111 = Unununium).'],
  check=dict(q='Z = 113 is in group', o=['3', '13', '11', '15'], a=1, why='…7s² 5f¹⁴ 6d¹⁰ 7p¹.')),
 dict(id='c2', t='Atomic and ionic radius', e='📏', lvl='m', topic='rad',
  body=['Across a period: radius falls (more Z_{eff}). Down a group: rises (new shells).',
        'Exceptions to remember: Ga (135 pm) < Al (143 pm) — 3d electrons shield poorly; the As → Bi steps are small for the same reason.',
        'Cations are smaller than their atoms, anions larger. Isoelectronic species: more protons → smaller (N^{3−} > O^{2−} > F^{−} > Na^{+} > Mg^{2+} > Al^{3+}).',
        'Noble-gas radii are van der Waals radii — not comparable with covalent ones.'],
  check=dict(q='Larger: Al or Ga?', o=['Ga', 'Al', 'equal', 'cannot say'], a=1, why='d-contraction in Ga.')),
 dict(id='c3', t='Ionisation enthalpy', e='⚡', lvl='m', topic='ie',
  body=['Energy to remove the outermost electron from an isolated gaseous atom — always endothermic; IE_{2} > IE_{1}.',
        'Rises across a period, falls down a group. Kinks: Be > B (2s full vs 2p^{1}), N > O (half-filled 2p); Mg > Al, P > S.',
        'Group 13: B ≫ Tl > Ga > Al > In. Group 14: C > Si > Ge > Pb > Sn.',
        'A huge jump between IE_{n} and IE_{n+1} means the core has been reached (Na: 496 → 4562).'],
  check=dict(q='Higher IE₁ :', o=['O', 'N', 'equal', 'depends'], a=1, why='Half-filled 2p.')),
 dict(id='c4', t='Electron gain enthalpy and electronegativity', e='🧲', lvl='m', topic='eg',
  body=['Δ_{eg}H: usually negative for halogens; positive for noble gases (and N, Be, Mg) — adding the electron is uphill.',
        'Most negative: Cl (−349) > F (−328) > Br (−325) > I. O (−141) is less negative than S (−200): small, crowded 2p.',
        'Electronegativity (Pauling): F 4.0 > O 3.5 > N = Cl 3.0 > Br 2.8 > C = S = I 2.5. Rises across, falls down.',
        'Metallic character ~ low IE/EN: increases down and to the left. Oxides: left basic, right acidic, middle amphoteric (Al_{2}O_{3}).'],
  check=dict(q='Most negative Δ_eg H :', o=['F', 'Cl', 'Br', 'O'], a=1, why='F is too small and crowded.')),
]
FORMULAS = [('H-like IE', 'E = 2.18 × 10^{−18} \\f{Z^{2}}{n^{2}} J'), ('Period size', '2 × orbitals filled'), ('IUPAC', 'nil un bi tri quad pent hex sept oct enn + ium'), ('Isoelectronic', 'more Z → smaller radius')]
TRAPS = ['Ga is smaller than Al; Tl has higher IE₁ than In.', 'Cl, not F, has the most negative electron gain enthalpy.', 'B has lower IE₁ than Be; O lower than N.', 'Anions are bigger than their atoms — "ions are always smaller" is false.',
         'Mg is more metallic than Al (K > Mg > Al > B).', 'Period n holds 2 × (orbitals being filled), not n² elements.']
STEPS = [dict(k='s1', t='The table', e='🗂️', cards=['c1'], need=['pt'], note='Periodic law, blocks, IUPAC names'),
         dict(k='s2', t='Size', e='📏', cards=['c2'], need=['rad'], note='Atomic and ionic radii'),
         dict(k='s3', t='Energies', e='⚡', cards=['c3', 'c4'], need=['ie', 'eg'], note='Ionisation enthalpy, electron gain, electronegativity')]
META = dict(unit='chem-u09', subject='chem', n=9, title='Classification of Elements & Periodicity', cls=11, labs=['ptrend'],
            syllabus="Modern periodic law and present form of the periodic table, s, p, d and f block elements, periodic trends in properties of elements atomic and ionic radii, ionization enthalpy, electron gain enthalpy, valence, oxidation states, and chemical reactivity.")
