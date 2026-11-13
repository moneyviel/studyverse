"""Concept cards for Chemistry Unit 13 — Purification and Characterisation of Organic Compounds (written for StudyVerse)."""
TOPICS = {'sep': 'Purification methods & chromatography', 'det': 'Detection (Lassaigne) & nitrogen estimation', 'est': 'Estimation of C, H, halogens, S, P; formulae'}
CARDS = [
 dict(id='c1', t='Choosing a purification method', e='⚗️', lvl='f', topic='sep',
  body=['<div class="jx-f">Sublimation: solid → vapour → solid.  Crystallisation: solubility difference.  Distillation: boiling-point difference</div>',
        'Simple distillation: large b.p. gap (chloroform + aniline). Fractional: close b.p. (crude oil). Reduced pressure: decomposes at its b.p. (glycerol from spent-lye).',
        'Steam distillation: steam-volatile and water-IMMISCIBLE (aniline, essential oils, o-nitrophenol); it distils when p_{water} + p_{organic} = 1 atm, below 373 K.',
        'Differential extraction: shake with an immiscible solvent in which the compound is more soluble. Purity check: sharp m.p./b.p.'],
  check=dict(q='Glycerol is recovered from spent-lye by', o=['distillation under reduced pressure', 'steam distillation', 'sublimation', 'simple distillation'], a=0, why='It decomposes at its normal b.p.')),
 dict(id='c2', t='Chromatography', e='🧪', lvl='m', topic='sep',
  body=['<div class="jx-f">R_{f} = distance moved by the compound / distance moved by the solvent front  (0 < R_{f} < 1)</div>',
        'Adsorption chromatography (column, TLC): silica gel or alumina. Polar compounds stick more → lower R_{f}; in a column the least adsorbed comes out first.',
        'Partition chromatography (paper): water trapped in the paper is the stationary phase. Colourless spots: UV light, iodine vapour, or a spraying reagent (ninhydrin for amino acids).'],
  check=dict(q='Spot 2.4 cm, front 6 cm → R_f =', o=['0.4', '2.5', '0.6', '4'], a=0, why='2.4/6.')),
 dict(id='c3', t="Lassaigne's test", e='🔥', lvl='m', topic='det',
  body=['Fuse with Na: N → NaCN, S → Na_{2}S, X → NaX, P → Na_{3}PO_{4}. N needs C too, so hydrazine gives no test.',
        'N: FeSO_{4}, boil, then FeCl_{3}/H_{2}SO_{4} → Prussian blue Fe_{4}[Fe(CN)_{6}]_{3}. S: sodium nitroprusside → violet; or lead acetate → black PbS.',
        'N + S together: NaSCN → blood red with Fe^{3+}. Halogens: boil with HNO_{3} (destroy CN^{−}, S^{2−}), then AgNO_{3}: AgCl white (NH_{3}-soluble), AgBr pale yellow, AgI yellow. P: ammonium molybdate → yellow.'],
  check=dict(q='Blood-red colour with Fe³⁺ shows', o=['N and S together', 'only N', 'only S', 'a halogen'], a=0, why='SCN⁻.')),
 dict(id='c4', t='Estimating nitrogen', e='🧮', lvl='h', topic='det',
  body=['<div class="jx-f">Dumas: % N = (28/22400) × V_{STP}(mL)/w × 100, with V_{STP} from (P − aqueous tension)V/T.  Kjeldahl: % N = 1.4 × (milli-equivalents of acid used)/w</div>',
        "Dumas heats the compound with CuO (in CO_{2}); N_{2} is collected over KOH. Kjeldahl digests with conc. H_{2}SO_{4} (CuSO_{4} catalyst, K_{2}SO_{4}) → (NH_{4})_{2}SO_{4} → NH_{3} into standard acid.",
        'Kjeldahl fails for nitro, azo and ring nitrogen (pyridine). 1 mol H_{2}SO_{4} neutralises 2 mol NH_{3}.'],
  check=dict(q='NH₃ from 0.5 g neutralised 10 mL 1 M H₂SO₄. % N =', o=['56', '28', '14', '42'], a=0, why='0.02 mol NH₃ × 14 = 0.28 g.')),
 dict(id='c5', t='Gravimetric estimations', e='⚖️', lvl='m', topic='est',
  body=['<div class="jx-f">% C = 12/44 × m(CO_{2})/w × 100;  % H = 2/18 × m(H_{2}O)/w × 100;  % X = (X/AgX) × m(AgX)/w × 100;  % S = 32/233 × m(BaSO_{4})/w × 100;  % P = 62/222 × m(Mg_{2}P_{2}O_{7})/w × 100</div>',
        'Combustion: H_{2}O absorbed in anhydrous CaCl_{2}, CO_{2} in KOH. Carius: heat with fuming HNO_{3} (+AgNO_{3} for halogens). O is found by difference.',
        'Empirical formula: % ÷ atomic mass → divide by smallest → whole numbers. Molecular formula = n × empirical, n = M/empirical mass.'],
  check=dict(q='0.188 g AgBr contains Br =', o=['0.080 g', '0.108 g', '0.188 g', '0.040 g'], a=0, why='80/188 of it.')),
]
FORMULAS = [('R_f', 'distance(spot)/distance(front)'), ('Dumas', '% N = 28 × n(N_{2})/w × 100'), ('Kjeldahl', '% N = 1.4 × meq/w'), ('Carbon', '% C = (12/44)·m(CO_{2})/w × 100'), ('Hydrogen', '% H = (2/18)·m(H_{2}O)/w × 100'),
            ('Halogen', '% X = (X/AgX)·m(AgX)/w × 100'), ('Sulphur', '% S = (32/233)·m(BaSO_{4})/w × 100'), ('Phosphorus', '% P = (62/222)·m(Mg_{2}P_{2}O_{7})/w × 100')]
TRAPS = ['Subtract aqueous tension in Dumas before using PV = nRT.', 'H₂SO₄ is dibasic: 1 mol neutralises 2 mol NH₃.', 'Kjeldahl does not work for pyridine, nitro or azo compounds.', 'Steam distillation needs a water-IMMISCIBLE liquid.',
         'Paper chromatography is partition, not adsorption.', 'Reducing pressure LOWERS the boiling point.', 'N and S together give blood red, not Prussian blue.']
STEPS = [dict(k='s1', t='Purify', e='⚗️', cards=['c1'], need=['sep'], note='Distillation types, sublimation, crystallisation, extraction'),
         dict(k='s2', t='Chromatography', e='🧪', cards=['c2'], need=['sep'], note='Adsorption vs partition, R_f'),
         dict(k='s3', t='Detect', e='🔥', cards=['c3'], need=['det'], note="Lassaigne's test for N, S, X, P"),
         dict(k='s4', t='Nitrogen', e='🧮', cards=['c4'], need=['det'], note='Dumas and Kjeldahl'),
         dict(k='s5', t='Estimate', e='⚖️', cards=['c5'], need=['est'], note='C, H, X, S, P and empirical formulae')]
META = dict(unit='chem-u13', subject='chem', n=13, title='Purification and Characterisation of Organic Compounds', cls=11, labs=['tlc'],
            syllabus='Purification — crystallisation, sublimation, distillation, differential extraction and chromatography — principles and their applications. Qualitative analysis — detection of nitrogen, sulphur, phosphorus and halogens. Quantitative analysis (basic principles only) — estimation of carbon, hydrogen, nitrogen, halogens, sulphur, phosphorus. Calculations of empirical formulae and molecular formulae; numerical problems in organic quantitative analysis.')
