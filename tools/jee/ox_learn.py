"""Concept cards for Chemistry Unit 17 — Organic Compounds Containing Oxygen (written for StudyVerse)."""
TOPICS = {'alc': 'Alcohols, phenols & ethers', 'carb': 'Aldehydes & ketones', 'acid': 'Carboxylic acids'}
CARDS = [
 dict(id='c1', t='Alcohols', e='🍶', lvl='f', topic='alc',
  body=['Classes by the carbinol carbon: 1°, 2°, 3°. Lucas (HCl/ZnCl_{2}): 3° turbid at once, 2° in ~5 min, 1° only on heating. Ceric ammonium nitrate: red.',
        'Oxidation: 1° → aldehyde (PCC) → acid (K_{2}Cr_{2}O_{7}, KMnO_{4}); 2° → ketone; 3° resist. Cu at 573 K: 1° → aldehyde, 2° → ketone, 3° → alkene.',
        'Dehydration (conc. H_{2}SO_{4}): 3° > 2° > 1°; 443 K → alkene, 413 K (excess alcohol) → ether. Iodoform: CH_{3}CH(OH)– (ethanol is the only 1° one).'],
  check=dict(q='Immediate turbidity with Lucas reagent:', o=['2-methylpropan-2-ol', 'butan-1-ol', 'butan-2-ol', 'methanol'], a=0, why='3° carbocation forms fast.')),
 dict(id='c2', t='Phenols & ethers', e='⬡', lvl='m', topic='alc',
  body=['Phenol (pKa 10) is more acidic than alcohols (~16): the phenoxide is resonance-stabilised. −R/−I groups (o/p-NO_{2}) raise acidity; p-nitrophenol 7.15, picric acid 0.4.',
        'Ring is very activated: Br_{2} water → 2,4,6-tribromophenol; dilute HNO_{3} → o-/p-nitrophenol (o is steam volatile). Kolbe (CO_{2}/NaOH) → salicylic acid; Reimer–Tiemann (CHCl_{3}/NaOH) → salicylaldehyde.',
        'Zn dust → benzene; FeCl_{3} → violet; phthalein test. Ethers: Williamson (RONa + 1° RX). HI cleaves R–O: alkyl aryl ethers give phenol + RI; 3° alkyl leaves as R–I (S_{N}1).'],
  check=dict(q='Anisole + HI gives', o=['phenol + CH₃I', 'iodobenzene + CH₃OH', 'benzene + CH₃OH', 'iodobenzene + CH₃I'], a=0, why='The Ar–O bond is not cleaved.')),
 dict(id='c3', t='Making aldehydes & ketones', e='🧴', lvl='m', topic='carb',
  body=['Rosenmund (RCOCl + H_{2}/Pd–BaSO_{4}), Stephen (RCN + SnCl_{2}/HCl), Etard (toluene + CrO_{2}Cl_{2}), Gattermann–Koch (benzene + CO/HCl), ozonolysis, alkyne hydration (Hg^{2+}).',
        'Ketones: RCN + R′MgX → ketone; Friedel–Crafts acylation; 2° alcohol oxidation.'],
  check=dict(q='Toluene + CrO₂Cl₂, then H₃O⁺ is the', o=['Etard reaction', 'Stephen reaction', 'Rosenmund reduction', 'Gattermann–Koch reaction'], a=0, why='Chromyl chloride.')),
 dict(id='c4', t='Reactions of C=O', e='🎯', lvl='h', topic='carb',
  body=['Nucleophilic addition: HCHO > RCHO > ArCHO > RCOR > ArCOR (steric + electronic). HCN, NaHSO_{3}, ROH (acetals), NH_{2}–Z (oxime, hydrazone, 2,4-DNP, semicarbazone).',
        'With α-H: aldol (dil. NaOH) → β-hydroxy carbonyl → α,β-unsaturated; Claisen–Schmidt (ArCHO + ketone). No α-H aldehydes: Cannizzaro (conc. NaOH) → acid salt + alcohol.',
        'Tests: Tollens — all aldehydes (and HCOOH); Fehling/Benedict — aliphatic aldehydes and α-hydroxy ketones, not ArCHO. Iodoform — CH_{3}CO–. Reductions: Clemmensen (Zn-Hg/HCl), Wolff–Kishner (N_{2}H_{4}/KOH) → CH_{2}.'],
  check=dict(q='Gives Tollens but not Fehling:', o=['benzaldehyde', 'acetaldehyde', 'acetone', 'propanal'], a=0, why='Aromatic aldehyde.')),
 dict(id='c5', t='Carboxylic acids', e='🍋', lvl='m', topic='acid',
  body=['Acidity: −I groups raise it (Cl_{3}CCOOH > Cl_{2}CHCOOH > ClCH_{2}COOH > CH_{3}COOH); the effect fades with distance; alkyl groups lower it. HCOOH > CH_{3}COOH; benzoic acid 4.2.',
        'Preparation: oxidation of 1° alcohols/aldehydes/alkylbenzenes, nitrile hydrolysis, RMgX + CO_{2}. Reactions: NaHCO_{3} → CO_{2}; esterification; HVZ (X_{2}/red P → α-halo acid); soda-lime decarboxylation; LiAlH_{4} → RCH_{2}OH.'],
  check=dict(q='Strongest acid:', o=['Cl₃CCOOH', 'ClCH₂COOH', 'CH₃COOH', 'HCOOH'], a=0, why='Three −I chlorines.')),
]
FORMULAS = [('Iodoform', 'CH₃CO– or CH₃CH(OH)–'), ('Aldol', 'needs α-H'), ('Cannizzaro', 'no α-H, conc. NaOH'), ('Decarboxylation', 'RCOONa → RH'), ('Grignard + CO₂', 'RMgX → RCOOH')]
TRAPS = ['Fehling does not react with aromatic aldehydes.', 'Methanol does NOT give iodoform; ethanol does.', 'HCOOH reduces Tollens (it has an H–C=O).', 'Anisole + HI gives phenol, never iodobenzene.', 'Bromination of phenol needs no Lewis acid.', 'Tertiary alcohols resist mild oxidation.']
STEPS = [dict(k='s1', t='Alcohols', e='🍶', cards=['c1'], need=['alc'], note='Classes, Lucas, oxidation, dehydration'),
         dict(k='s2', t='Phenols', e='⬡', cards=['c2'], need=['alc'], note='Acidity, ring reactions, ethers'),
         dict(k='s3', t='Make C=O', e='🧴', cards=['c3'], need=['carb'], note='Name reactions for aldehydes and ketones'),
         dict(k='s4', t='C=O reactions', e='🎯', cards=['c4'], need=['carb'], note='Addition, aldol, Cannizzaro, tests'),
         dict(k='s5', t='Acids', e='🍋', cards=['c5'], need=['acid'], note='Acidity and reactions of carboxylic acids')]
META = dict(unit='chem-u17', subject='chem', n=17, title='Organic Compounds Containing Oxygen', cls=12, labs=['carbtest'],
            syllabus='Alcohols — identification of primary, secondary and tertiary alcohols, mechanism of dehydration. Phenols — acidic nature, electrophilic substitution reactions: halogenation, nitration and sulphonation, Reimer–Tiemann reaction. Ethers — structure. Aldehydes and ketones — nature of carbonyl group; nucleophilic addition to >C=O group, relative reactivities of aldehydes and ketones; important reactions such as nucleophilic addition reactions (addition of HCN, NH3 and its derivatives), Grignard reagent; oxidation; reduction (Wolff-Kishner and Clemmensen); acidity of α-hydrogen, aldol condensation, Cannizzaro reaction, haloform reaction; chemical tests to distinguish between aldehydes and ketones. Carboxylic acids — acidic strength and factors affecting it.')
