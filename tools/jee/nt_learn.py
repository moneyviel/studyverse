"""Concept cards for Chemistry Unit 18 — Organic Compounds Containing Nitrogen (written for StudyVerse)."""
TOPICS = {'amine': 'Amines: classes, basicity, preparation & tests', 'diaz': 'Diazonium salts, azo dyes & ring reactions'}
CARDS = [
 dict(id='c1', t='Making amines', e='🏭', lvl='f', topic='amine',
  body=['Nitro reduction (Sn/HCl, Fe/HCl, H_{2}/Pd) → ArNH_{2}. Nitriles (LiAlH_{4}, H_{2}/Ni) → RCH_{2}NH_{2} (one C more). Amides (LiAlH_{4}) → RCH_{2}NH_{2}.',
        'Hofmann bromamide: RCONH_{2} + Br_{2} + 4NaOH → RNH_{2} + Na_{2}CO_{3} + 2NaBr + 2H_{2}O (one C fewer). Gabriel: phthalimide/KOH + RX → pure 1° aliphatic amines (not aryl amines).',
        'Ammonolysis of RX gives a mixture (1°, 2°, 3°, R_{4}N^{+}X^{−}); excess NH_{3} favours 1°.'],
  check=dict(q='Hofmann degradation of propanamide gives', o=['ethylamine', 'propylamine', 'butylamine', 'ethanamide'], a=0, why='One carbon is lost as CO₃²⁻.')),
 dict(id='c2', t='Basicity', e='⚖️', lvl='m', topic='amine',
  body=['Aliphatic amines > NH_{3} > aniline (lone pair delocalised into the ring). In water (ethyl): 2° > 3° > 1° > NH_{3}; (methyl): 2° > 1° > 3°.',
        'Ring substituents: donors (CH_{3}, OCH_{3}) raise basicity of anilines; acceptors (NO_{2}, Cl) lower it. Benzylamine behaves like an aliphatic amine.',
        'Piperidine (sp^{3} N) > pyridine (sp^{2} N) ≫ pyrrole (lone pair in the aromatic sextet).'],
  check=dict(q='Weakest base:', o=['p-nitroaniline', 'aniline', 'p-toluidine', 'methylamine'], a=0, why='−R nitro group.')),
 dict(id='c3', t='Telling amines apart', e='🔍', lvl='m', topic='amine',
  body=['Hinsberg (C_{6}H_{5}SO_{2}Cl): 1° → sulphonamide soluble in alkali (acidic N–H); 2° → insoluble solid; 3° → no reaction.',
        'Carbylamine (CHCl_{3} + alc. KOH): only 1° amines → foul-smelling isocyanide. HNO_{2}: 1° aliphatic → alcohol + N_{2}; 1° aromatic (273–278 K) → diazonium salt; 2° → N-nitrosamine (yellow oil).',
        'Aniline + Br_{2} water → 2,4,6-tribromoaniline at once; acetylate first (acetanilide) to get mono-substitution. Nitration in strong acid gives much meta (anilinium ion).'],
  check=dict(q='Gives an alkali-insoluble product with Hinsberg reagent:', o=['N-methylaniline', 'aniline', 'N,N-dimethylaniline', 'ethylamine'], a=0, why='Secondary amine.')),
 dict(id='c4', t='Diazonium salts', e='🌈', lvl='h', topic='diaz',
  body=['ArNH_{2} + NaNO_{2}/HCl, 273–278 K → ArN_{2}^{+}Cl^{−} (stabilised by resonance; aliphatic ones decompose).',
        'Replace N_{2}: CuCl/CuBr/CuCN (Sandmeyer), Cu/HX (Gattermann), KI → ArI, HBF_{4}/heat → ArF, H_{2}O (warm) → ArOH, H_{3}PO_{2} or ethanol → ArH, HBF_{4} then NaNO_{2}/Cu → ArNO_{2}.',
        'Coupling (N_{2} kept): with phenol (alkaline) → p-hydroxyazobenzene (orange); with aniline (mild acid) → aniline yellow; with 2-naphthol → scarlet dye.'],
  check=dict(q='ArN₂⁺Cl⁻ + CuCN gives', o=['ArCN', 'ArNC', 'ArCl', 'ArOH'], a=0, why='Sandmeyer cyanation.')),
]
FORMULAS = [('Hofmann', 'RCONH₂ → RNH₂ (−1 C)'), ('Nitrile reduction', 'RCN → RCH₂NH₂ (+1 C)'), ('HNO₂ (1° aliphatic)', 'RNH₂ → ROH + N₂'), ('Diazotisation', '273–278 K'), ('Tribromination', 'aniline + 3Br₂')]
TRAPS = ['Gabriel cannot make aniline.', 'Hinsberg: 1° product dissolves in alkali, 2° does not.', 'Carbylamine is only for 1° amines.', 'Aniline is a weaker base than NH₃.', 'Sandmeyer gives ArCl, ArBr, ArCN — not ArF or ArI.', 'Hofmann uses ONE Br₂ and FOUR NaOH per amide.']
STEPS = [dict(k='s1', t='Make', e='🏭', cards=['c1'], need=['amine'], note='Preparation of amines'),
         dict(k='s2', t='Basicity', e='⚖️', cards=['c2'], need=['amine'], note='Comparing amine basicity'),
         dict(k='s3', t='Tests', e='🔍', cards=['c3'], need=['amine'], note='Hinsberg, carbylamine, HNO₂, bromination'),
         dict(k='s4', t='Diazonium', e='🌈', cards=['c4'], need=['diaz'], note='Replacement and coupling reactions')]
META = dict(unit='chem-u18', subject='chem', n=18, title='Organic Compounds Containing Nitrogen', cls=12, labs=['amineid'],
            syllabus='Amines: nomenclature, classification, structure, basic character and identification of primary, secondary and tertiary amines and their basic character. Diazonium salts: importance in synthetic organic chemistry.')
