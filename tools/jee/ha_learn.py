"""Concept cards for Chemistry Unit 16 — Organic Compounds Containing Halogens (written for StudyVerse)."""
TOPICS = {'sn': 'Substitution, elimination & haloarenes', 'prep': 'Preparation, name reactions & uses'}
CARDS = [
 dict(id='c1', t='Making haloalkanes & haloarenes', e='🧪', lvl='f', topic='prep',
  body=['From alcohols: SOCl_{2} (best — SO_{2}, HCl escape), PCl_{5}, PCl_{3}, HCl/ZnCl_{2} (Groves). Phenols do NOT react this way (C–O has double-bond character).',
        'Halogen exchange: Finkelstein (NaI in acetone → RI), Swarts (AgF, SbF_{3}, Hg_{2}F_{2} → RF). From alkenes: HX (Markovnikov), HBr + peroxide (anti-Markovnikov).',
        'Arenes: Cl_{2}/FeCl_{3} in the dark (ring); toluene + Cl_{2}/hν → benzyl chloride (side chain). Diazonium: Sandmeyer (CuCl, CuBr, CuCN), Gattermann (Cu/HX), Balz–Schiemann (ArF).'],
  check=dict(q='R–Cl + NaI/acetone → R–I is', o=['Finkelstein', 'Swarts', 'Sandmeyer', 'Wurtz'], a=0, why='NaCl precipitates and drives it.')),
 dict(id='c2', t='S_N1 vs S_N2', e='🔄', lvl='m', topic='sn',
  body=['<div class="jx-f">S_{N}2: rate = k[RX][Nu], one step, back-side attack → inversion.  S_{N}1: rate = k[RX], carbocation → racemisation</div>',
        'S_{N}2: CH_{3} > 1° > 2° > 3°; strong nucleophile, polar aprotic solvent; neopentyl is very slow (crowded).',
        'S_{N}1: 3° > 2° > 1°; benzyl and allyl (resonance) fast; polar protic solvent. Leaving group: I^{−} > Br^{−} > Cl^{−} > F^{−}.',
        'Ambident nucleophiles: KCN → R–CN, AgCN → R–NC; KNO_{2} → R–ONO, AgNO_{2} → R–NO_{2}.'],
  check=dict(q='Optically active 2-bromobutane + OH⁻ (S_N2) gives', o=['the inverted alcohol', 'a racemic alcohol', 'the retained alcohol', 'no reaction'], a=0, why='Back-side attack.')),
 dict(id='c3', t='Elimination & other reactions', e='↩️', lvl='m', topic='sn',
  body=['alc. KOH (heat) → alkene (β-elimination); Saytzeff: the more substituted alkene. aq. KOH → alcohol.',
        'Wurtz (Na/ether) R–R; Wurtz–Fittig Ar–R; Fittig Ar–Ar. Grignard: R–X + Mg (dry ether) → RMgX; with water → RH.'],
  check=dict(q='2-Bromobutane + alc. KOH gives mainly', o=['but-2-ene', 'but-1-ene', 'butan-2-ol', 'butane'], a=0, why='Saytzeff.')),
 dict(id='c4', t='Haloarenes', e='⬡', lvl='h', topic='sn',
  body=['C–X in Ar–X: partial double bond (resonance), sp^{2} carbon, shorter and less polar → resists substitution; phenyl cation is unstable; electron-rich ring repels nucleophiles.',
        'Dow: chlorobenzene + NaOH, 623 K, 300 atm → phenol. o/p-NO_{2} groups make it easy (2,4-dinitrochlorobenzene: warm water).',
        'Electrophilic substitution: halogens deactivate but direct o/p. Uses/hazards: CHCl_{3} (dark bottles, phosgene), CHI_{3} antiseptic, CCl_{4} extinguisher, freons (ozone), DDT (non-biodegradable).'],
  check=dict(q='Fastest with aq. NaOH:', o=['2,4,6-trinitrochlorobenzene', 'chlorobenzene', 'p-chlorotoluene', 'p-chloroanisole'], a=0, why='−R groups stabilise the anionic intermediate.')),
]
FORMULAS = [('S_N2 rate', 'k[RX][Nu⁻]'), ('S_N1 rate', 'k[RX]'), ('Leaving group', 'I > Br > Cl > F'), ('S_N2 order', 'CH₃ > 1° > 2° > 3°'), ('S_N1 order', '3° > 2° > 1°; benzyl, allyl fast')]
TRAPS = ['AgCN gives isocyanides; KCN gives nitriles.', 'aq. KOH substitutes; alc. KOH eliminates.', 'Phenol + HCl does NOT give chlorobenzene.', 'Gattermann gives ArCl/ArBr, not ArCN.', 'Neopentyl halides are primary but very slow by S_N2.', 'C–Cl in chlorobenzene is SHORTER than in CH₃Cl.']
STEPS = [dict(k='s1', t='Make', e='🧪', cards=['c1'], need=['prep'], note='Preparations and name reactions'),
         dict(k='s2', t='S_N1/S_N2', e='🔄', cards=['c2'], need=['sn'], note='Mechanisms, stereochemistry, nucleophiles'),
         dict(k='s3', t='Eliminate', e='↩️', cards=['c3'], need=['sn'], note='Elimination, Wurtz, Grignard'),
         dict(k='s4', t='Haloarenes', e='⬡', cards=['c4'], need=['sn', 'prep'], note='Aryl halides, uses and environment')]
META = dict(unit='chem-u16', subject='chem', n=16, title='Organic Compounds Containing Halogens', cls=12, labs=['snarena'],
            syllabus='General methods of preparation, properties and reactions; nature of C–X bond; mechanisms of substitution reactions. Uses; environmental effects of chloroform, iodoform, freons and DDT.')
