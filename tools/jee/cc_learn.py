"""Concept cards for Chemistry Unit 12 — Coordination Compounds (written for StudyVerse)."""
TOPICS = {'mag': 'Spin state, unpaired electrons & magnetism', 'cfs': 'Crystal field splitting, CFSE & colour', 'iso': 'Werner theory & isomerism', 'vbt': 'Bonding (VBT), ligands & uses'}
CARDS = [
 dict(id='c1', t='Werner, ligands & naming', e='🧩', lvl='f', topic='vbt',
  body=['<div class="jx-f">[Co(NH_{3})_{5}Cl]Cl_{2}: inside [ ] = coordination sphere (primary valence +3 shared with 2 free Cl^{−}); secondary valence = coordination number 6</div>',
        'Ionisable ions (outside [ ]) precipitate: free Cl^{−} → AgCl, free SO_{4}^{2−} → BaSO_{4}. Ions per formula decide conductivity and ΔT_{f} = iK_{f}m.',
        'Denticity: en, C_{2}O_{4}^{2−} bidentate; EDTA^{4−} hexadentate. Ambidentate: NO_{2}^{−}/ONO^{−}, SCN^{−}/NCS^{−}. Homoleptic = one kind of ligand.'],
  check=dict(q='Moles of AgCl from 1 mol [Co(NH₃)₄Cl₂]Cl:', o=['1', '2', '3', '0'], a=0, why='Only the Cl outside the bracket ionises.')),
 dict(id='c2', t='Crystal field splitting', e='🌈', lvl='f', topic='cfs',
  body=['<div class="jx-f">Octahedral: t_{2g} (−0.4Δ_{o}) below e_{g} (+0.6Δ_{o}).  Tetrahedral: e below t_{2}, Δ_{t} ≈ (4/9)Δ_{o}</div>',
        'Spectrochemical series: I^{−} < Br^{−} < S^{2−} < SCN^{−} < Cl^{−} < F^{−} < OH^{−} < C_{2}O_{4}^{2−} < H_{2}O < NCS^{−} < EDTA^{4−} < NH_{3} < en < NO_{2}^{−} < CN^{−} < CO.',
        'Δ_{o} also grows with metal charge (M^{3+} > M^{2+}) and down a group (3d < 4d < 5d).', 'Colour: light of energy Δ is absorbed; we see the complementary colour. Bigger Δ → shorter λ absorbed.'],
  check=dict(q='Which absorbs the shortest wavelength?', o=['[Co(CN)₆]³⁻', '[CoF₆]³⁻', '[Co(H₂O)₆]³⁺', '[Co(NH₃)₆]³⁺'], a=0, why='CN⁻ gives the largest Δₒ.')),
 dict(id='c3', t='High spin vs low spin', e='🧲', lvl='m', topic='mag',
  body=['<div class="jx-f">d^{4}–d^{7} octahedral: Δ_{o} > P → low spin (fill t_{2g} first); Δ_{o} < P → high spin.  μ = √(n(n + 2)) BM</div>',
        'Strong field: CN^{−}, CO, NO_{2}^{−} pair electrons. Co^{3+} (d^{6}) pairs even with NH_{3}, en, H_{2}O, C_{2}O_{4}^{2−}; [CoF_{6}]^{3−} stays high spin.',
        'd^{1}–d^{3} and d^{8}–d^{10}: same configuration whatever the ligand. Tetrahedral complexes are always high spin; square planar d^{8} ([Ni(CN)_{4}]^{2−}) is diamagnetic.',
        'CFSE = (−0.4x + 0.6y)Δ_{o} for t_{2g}^{x}e_{g}^{y}. High-spin d^{5} has CFSE 0.'],
  check=dict(q='Unpaired electrons in [Fe(CN)₆]³⁻:', o=['1', '5', '3', '0'], a=0, why='d⁵ low spin, t₂g⁵.')),
 dict(id='c4', t='Valence bond picture', e='🔗', lvl='m', topic='vbt',
  body=['CN 6: d^{2}sp^{3} (inner orbital, uses 3d) when two 3d orbitals are free — low spin or d^{0}–d^{3}; otherwise sp^{3}d^{2} (outer orbital, uses 4d).',
        'CN 4: sp^{3} tetrahedral ([NiCl_{4}]^{2−}, [MnBr_{4}]^{2−}, Ni(CO)_{4}); dsp^{2} square planar ([Ni(CN)_{4}]^{2−}, Pt^{2+}).',
        'Carbonyls: σ donation C → M plus π back-donation M(d) → CO π*. Synergic bonding strengthens M–C and weakens C≡O.', 'VBT gives no quantitative energies and cannot explain colour; CFT treats ligands as point charges.'],
  check=dict(q='Hybridisation in [CoF₆]³⁻:', o=['sp³d²', 'd²sp³', 'dsp²', 'sp³'], a=0, why='Weak F⁻: high spin, outer 4d used.')),
 dict(id='c5', t='Isomerism', e='🪞', lvl='h', topic='iso',
  body=['<div class="jx-f">Structural: ionisation, linkage, coordination, solvate.  Stereo: geometrical (cis/trans, fac/mer) and optical</div>',
        'Octahedral counts: MA_{4}B_{2} 2; MA_{3}B_{3} 2 (fac, mer); M(AA)_{2}B_{2} 3 (trans + cis pair); M(AA)_{3} 2 (Δ, Λ); MA_{2}B_{2}C_{2} 6 (5 geometrical, one chiral).',
        'Tetrahedral MABCD: no geometrical isomers, but chiral. Square planar MA_{2}B_{2}: cis/trans; MABCD: 3.', 'Chelate effect: en, oxalate and EDTA complexes are more stable than unidentate analogues.'],
  check=dict(q='Stereoisomers of [Co(en)₂Cl₂]⁺:', o=['3', '2', '4', '1'], a=0, why='trans + cis (a pair of enantiomers).')),
]
FORMULAS = [('Spin-only', 'μ = √(n(n + 2)) BM'), ('CFSE (oct)', '(−0.4x + 0.6y)Δ_{o}'), ('Tetrahedral', 'Δ_{t} = (4/9)Δ_{o}'), ('Colour', 'E = hc/λ = Δ'), ('Freezing point', 'ΔT_{f} = iK_{f}m'),
            ('Optical isomers', '2 × (chiral geometrical isomers)')]
TRAPS = ['[Co(H₂O)₆]³⁺ is low spin and diamagnetic (Co³⁺ has a large Δₒ).', 'Tetrahedral MABCD shows NO geometrical isomerism.', 'Ni(CO)₄ is diamagnetic (3d¹⁰), not d⁸.', 'cis-[Co(en)₂Cl₂]⁺ gives 2 optical isomers; total stereoisomers 3.',
         'Δₜ CFSE is in units of Δₜ, not Δₒ.', 'Synergic bonding STRENGTHENS the M–C bond.', 'Only ions OUTSIDE the square bracket react with AgNO₃.']
STEPS = [dict(k='s1', t='Werner', e='🧩', cards=['c1'], need=['vbt'], note='Coordination sphere, ligands, AgCl and conductivity'),
         dict(k='s2', t='Splitting', e='🌈', cards=['c2'], need=['cfs'], note='Δ, spectrochemical series and colour'),
         dict(k='s3', t='Spin', e='🧲', cards=['c3'], need=['mag'], note='Low/high spin, CFSE and magnetic moments'),
         dict(k='s4', t='VBT', e='🔗', cards=['c4'], need=['vbt'], note='Hybridisation, inner/outer orbital, carbonyls'),
         dict(k='s5', t='Isomers', e='🪞', cards=['c5'], need=['iso'], note='Structural and stereoisomerism')]
META = dict(unit='chem-u12', subject='chem', n=12, title='Coordination Compounds', cls=12, labs=['cfbox'],
            syllabus="Introduction to coordination compounds. Werner's theory; ligands, coordination number, denticity, chelation; IUPAC nomenclature of mononuclear co-ordination compounds, isomerism; Bonding — Valence bond approach and basic ideas of Crystal field theory, colour and magnetic properties; importance of co-ordination compounds (in qualitative analysis, extraction of metals and in biological systems).")
