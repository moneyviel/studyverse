"""Concept cards for Chemistry Unit 3 — Chemical Bonding & Molecular Structure (written for StudyVerse)."""
TOPICS = {'shape': 'VSEPR, shapes & hybridisation', 'polar': 'Dipole moment, polarity & hydrogen bonding', 'mot': 'Molecular orbital theory', 'lewis': 'Lewis structures, formal charge & bond parameters'}
CARDS = [
 dict(id='c1', t='Ionic and covalent bonds', e='🤝', lvl='f', topic='lewis',
  body=['Ionic bond: electron transfer (large electronegativity difference); covalent: electron sharing. Lattice enthalpy measures ionic strength.',
        'Octet rule exceptions: incomplete (BF_{3}, BeCl_{2}), odd-electron (NO, NO_{2}, ClO_{2}), expanded (PCl_{5}, SF_{6}, H_{2}SO_{4}).',
        '<div class="jx-f">Formal charge = valence e^{−} − non-bonding e^{−} − number of bonds</div>',
        'Fajans: small, highly charged cation + large anion → more covalent character (AlCl_{3}, LiI). Bond order up → bond length down, bond energy up.'],
  check=dict(q='FC on N in NH₄⁺ :', o=['0', '+1', '−1', '+2'], a=1, why='5 − 0 − 4.')),
 dict(id='c2', t='VSEPR: count, then place', e='📐', lvl='m', topic='shape',
  body=['<div class="jx-f">lone pairs = ½(valence e^{−} of centre − charge − e^{−} used in bonds)   (F, Cl, H use 1; =O uses 2)</div>',
        'Steric number = σ bonds + lone pairs → 2 linear (sp), 3 trigonal (sp^{2}), 4 tetrahedral (sp^{3}), 5 trigonal bipyramidal (sp^{3}d), 6 octahedral (sp^{3}d^{2}), 7 pentagonal bipyramidal (sp^{3}d^{3}).',
        'Repulsion: lp–lp > lp–bp > bp–bp. In a trigonal bipyramid lone pairs go EQUATORIAL: 4+1 see-saw (SF_{4}), 3+2 T-shape (ClF_{3}), 2+3 linear (XeF_{2}).',
        'In an octahedron: 5+1 square pyramidal (BrF_{5}, XeOF_{4}), 4+2 square planar (XeF_{4}, ICl_{4}^{−}).'],
  check=dict(q='Shape of ClF₃ :', o=['trigonal planar', 'T-shaped', 'pyramidal', 'see-saw'], a=1, why='3 bonds + 2 lone pairs.')),
 dict(id='c3', t='Bond angles', e='🔺', lvl='m', topic='shape',
  body=['More lone pairs squeeze the angle: CH_{4} 109.5° > NH_{3} 107° > H_{2}O 104.5°.',
        'More electronegative outer atoms pull bond pairs away → smaller angle: NF_{3} (102°) < NH_{3}; OF_{2} (103°) < H_{2}O < Cl_{2}O (111°, bulky Cl).',
        'Going down a group (same shape) the angle falls: NH_{3} > PH_{3} > AsH_{3} (≈ 90°, nearly pure p).',
        'BF_{3} 120° > PF_{3} ≈ 98° > ClF_{3} ≈ 87.5°.'],
  check=dict(q='Largest bond angle :', o=['H₂O', 'NH₃', 'CH₄', 'H₂S'], a=2, why='No lone pairs on C.')),
 dict(id='c4', t='Dipole moment and H-bonding', e='🧲', lvl='m', topic='polar',
  body=['μ = q × d (debye; 1 D = 3.336 × 10^{−30} C m). Vector sum of bond dipoles (and lone-pair dipoles).',
        'μ = 0 for symmetric shapes with identical ligands: CO_{2}, BF_{3}, CH_{4}, PCl_{5}, SF_{6}, XeF_{2}, XeF_{4}.',
        'NH_{3} (1.47 D) ≫ NF_{3} (0.24 D): in NH_{3} lone-pair and bond dipoles add; in NF_{3} they oppose.',
        'H-bond: H on N, O, F. Intermolecular raises bp (H_{2}O, HF, NH_{3}); intramolecular (o-nitrophenol) lowers bp and solubility.'],
  check=dict(q='Which has μ = 0?', o=['SO₂', 'CO₂', 'H₂O', 'NH₃'], a=1, why='Linear and symmetric.')),
 dict(id='c5', t='Molecular orbital theory', e='🌀', lvl='h', topic='mot',
  body=['AOs combine when energies are close and they have the SAME symmetry about the bond axis (e.g. 2s with 2p_{z}).',
        'Order up to 14 e^{−} (B_{2}, C_{2}, N_{2}): σ1s σ*1s σ2s σ*2s (π2p_{x} = π2p_{y}) σ2p_{z} (π*) σ*. From O_{2} on, σ2p_{z} drops below π2p.',
        '<div class="jx-f">Bond order = ½(N_{b} − N_{a})</div>',
        'O_{2}, B_{2}, O_{2}^{±}, N_{2}^{±} are paramagnetic. Bond orders: O_{2}^{+} 2.5 > O_{2} 2 > O_{2}^{−} 1.5 > O_{2}^{2−} 1. Isoelectronic CO, NO^{+}, CN^{−}, N_{2}: 3.'],
  check=dict(q='B₂ is', o=['diamagnetic', 'paramagnetic', 'non-existent', 'ionic'], a=1, why='π2p¹ π2p¹ (s–p mixing).')),
]
FORMULAS = [('Lone pairs', 'lp = ½(V − q − Σused)'), ('Steric no.', 'SN = σ + lp'), ('Formal charge', 'FC = V − N − B'), ('Bond order', 'BO = ½(N_{b} − N_{a})'), ('Dipole', 'μ = q × d'),
            ('% ionic', '\\f{μ_{obs}}{e d} × 100'), ('Hybrid', '2 sp, 3 sp^{2}, 4 sp^{3}, 5 sp^{3}d, 6 sp^{3}d^{2}')]
TRAPS = ['Lone pairs in a trigonal bipyramid sit EQUATORIAL (ClF₃ is T-shaped, not trigonal planar).', 'XeF₂ and XeF₄ have lone pairs yet μ = 0 — symmetry wins.', 'NF₃ has a much smaller dipole than NH₃.',
         'O₂⁺ and O₂⁻ have the same number of unpaired electrons (1).', '[Co(NH₃)₆]³⁺ is d²sp³ (inner d), SF₆ is sp³d² (outer d).', 'o-Nitrophenol: intramolecular H-bond → more volatile than p-nitrophenol.']
STEPS = [dict(k='s1', t='Lewis & VSEPR', e='📐', cards=['c1', 'c2', 'c3'], need=['lewis', 'shape'], note='Formal charge, shapes, hybridisation, bond angles'),
         dict(k='s2', t='Polarity', e='🧲', cards=['c4'], need=['polar'], note='Dipole moment and hydrogen bonding'),
         dict(k='s3', t='MO theory', e='🌀', cards=['c5'], need=['mot'], note='Bond order, magnetism, bond length')]
META = dict(unit='chem-u03', subject='chem', n=3, title='Chemical Bonding & Molecular Structure', cls=11, labs=['vsepr'],
            syllabus="Kossel - Lewis approach to chemical bond formation, the concept of ionic and covalent bonds. Ionic Bonding: Formation of ionic bonds, factors affecting the formation of ionic bonds; calculation of lattice enthalpy. Covalent Bonding: Concept of electronegativity. Fajan's rule, dipole moment: Valence Shell Electron Pair Repulsion (VSEPR) theory and shapes of simple molecules. Quantum mechanical approach to covalent bonding: Valence bond theory - its important features, the concept of hybridization involving s, p, and d orbitals; Resonance. Molecular Orbital Theory - Its important features, LCAOs, types of molecular orbitals (bonding, antibonding), sigma and pi-bonds, molecular orbital electronic configurations of homonuclear diatomic molecules, the concept of bond order, bond length, and bond energy. Elementary idea of metallic bonding. Hydrogen bonding and its applications.")
