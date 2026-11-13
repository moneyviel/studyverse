"""Concept cards for Chemistry Unit 14 — Some Basic Principles of Organic Chemistry (written for StudyVerse)."""
TOPICS = {'nom': 'Classification & IUPAC naming', 'iso': 'Isomerism (structural & stereo)', 'eff': 'Electronic effects, intermediates, acids & bases', 'mech': 'Bond cleavage, reagents & reaction types'}
CARDS = [
 dict(id='c1', t='IUPAC naming', e='🏷️', lvl='f', topic='nom',
  body=['<div class="jx-f">Principal group (suffix): acid > anhydride > ester > acid halide > amide > nitrile > aldehyde > ketone > alcohol > amine > alkene/alkyne</div>',
        'Parent = longest chain holding the principal group (and most multiple bonds). Number for the lowest locant to the suffix, then C=C/C≡C, then prefixes.',
        'Prefixes (halo, nitro, alkyl, alkoxy) are listed alphabetically, ignoring di/tri. On a tie in locants, the group first in the alphabet gets the lower number.',
        'Classes: acyclic (open chain), alicyclic (non-aromatic rings), aromatic (benzenoid and heterocyclic like pyridine, furan, pyrrole).'],
  check=dict(q='HC≡C–CH₂–CH(OH)–CH₂–CH=CH₂ is', o=['hept-1-en-6-yn-4-ol', 'hept-6-en-1-yn-4-ol', '4-hydroxyhept-1-en-6-yne', 'hept-1-yn-6-en-4-ol'], a=0, why='-ol is principal; on a tie the ene gets the lower number.')),
 dict(id='c2', t='Structural isomers', e='🔀', lvl='f', topic='iso',
  body=['Chain (skeleton differs), position (group/bond position), functional (different groups: aldehyde/ketone, alcohol/ether, acid/ester, cyanide/isocyanide), metamers (different alkyl groups on either side of –O–, –CO–, –NH–), tautomers (keto ⇌ enol, needs α-H).',
        'Alkane isomers: C_{4} 2, C_{5} 3, C_{6} 5, C_{7} 9, C_{8} 18. Monochlorides = number of different kinds of H.'],
  check=dict(q='Ethoxyethane and methoxypropane are', o=['metamers', 'chain isomers', 'functional isomers', 'tautomers'], a=0, why='Same –O–, different alkyl groups.')),
 dict(id='c3', t='Stereoisomers', e='🪞', lvl='m', topic='iso',
  body=['<div class="jx-f">Stereoisomers ≤ 2^{n}, n = chiral centres + stereo C=C. Two identical chiral centres (2,3-dichlorobutane) → 3 (RR, SS, meso)</div>',
        'Chiral carbon: four different groups. Cis/trans needs two different groups on EACH alkene carbon (propene and 2-methylbut-2-ene have none).',
        'cis-But-2-ene has a dipole moment; trans is more stable and has a higher melting point.'],
  check=dict(q='Stereoisomers of CH₃CH(OH)CH=CHCH₃:', o=['4', '2', '3', '8'], a=0, why='1 chiral C × 1 stereo C=C.')),
 dict(id='c4', t='Electronic effects', e='⚡', lvl='m', topic='eff',
  body=['Inductive (σ, permanent, fades with distance): −I NO_{2} > CN > F > Cl > Br > I > OH; +I alkyl groups.',
        'Resonance/mesomeric (π, permanent): +R –OH, –OR, –NH_{2}, –X; −R –NO_{2}, –CN, –CHO, –COOH. Electromeric: temporary, only when a reagent attacks (+E: electrons move towards the reagent).',
        'Hyperconjugation: σ(C–H) ↔ adjacent p/π; number of α-H. Explains 3° > 2° > 1° cations and alkene stability (more substituted = more stable, lower heat of hydrogenation).'],
  check=dict(q='Strongest acid:', o=['ClCH₂COOH', 'CH₃COOH', 'ClCH₂CH₂COOH', 'CH₃CH₂COOH'], a=0, why='−I of Cl, closest to COOH.')),
 dict(id='c5', t='Reactive intermediates', e='🧨', lvl='m', topic='eff',
  body=['Carbocation: sp^{2}, planar, 6 e^{−}, electrophile. Order: tropylium/trityl > benzyl ≈ allyl > 3° > 2° > 1° > CH_{3}^{+} > vinyl.',
        'Carbanion: sp^{3}, pyramidal, 8 e^{−}, nucleophile; stabilised by −I/−R groups and by more s-character (sp > sp^{2} > sp^{3}).',
        'Radical: 7 e^{−}, from homolysis; stability like carbocations. Aromatic: planar, cyclic, conjugated, 4n + 2 π e^{−}; 4n → antiaromatic.'],
  check=dict(q='Hückel aromatic:', o=['cyclopentadienyl anion', 'cyclobutadiene', 'cyclooctatetraene', 'cyclopentadienyl cation'], a=0, why='6π.')),
 dict(id='c6', t='Reagents & reaction types', e='🔧', lvl='f', topic='mech',
  body=['Homolysis → radicals; heterolysis → ions. Nucleophiles donate a pair (OH^{−}, NH_{3}, CN^{−}, H_{2}O, π bonds); electrophiles accept (H^{+}, NO_{2}^{+}, BF_{3}, AlCl_{3}, C=O carbon).',
        'Types: substitution (S_{N}, S_{E}, free radical), addition (electrophilic to C=C, nucleophilic to C=O), elimination, rearrangement.',
        'Nucleophilicity: same atom → follows basicity; in protic solvents larger, less solvated ions win (I^{−} > Br^{−} > Cl^{−} > F^{−}).'],
  check=dict(q='BF₃ is', o=['an electrophile', 'a nucleophile', 'a free radical', 'a carbanion'], a=0, why='Empty orbital on B.')),
]
FORMULAS = [('Stereoisomers', '2^{n} (n = chiral C + stereo C=C)'), ('Aromatic', '(4n + 2) π e^{−}'), ('Hyperconjugation', 'count α C–H'), ('Alkane isomers', 'C_{5} 3 · C_{6} 5 · C_{7} 9 · C_{8} 18')]
TRAPS = ['Trans-alkenes: higher m.p., lower dipole moment.', 'CH₃⁺ has zero hyperconjugation.', 'H⁺ attack causes +E (not −E).', 'More substituted alkenes have LOWER heat of hydrogenation.', 'Cyclooctatetraene is non-aromatic (tub), not antiaromatic.', 'Halogens: −I beats +R (deactivating but o/p directing).']
STEPS = [dict(k='s1', t='Names', e='🏷️', cards=['c1'], need=['nom'], note='Classification and IUPAC rules'),
         dict(k='s2', t='Isomers', e='🔀', cards=['c2', 'c3'], need=['iso'], note='Structural and stereoisomerism'),
         dict(k='s3', t='Effects', e='⚡', cards=['c4', 'c5'], need=['eff'], note='Inductive, resonance, hyperconjugation; intermediates'),
         dict(k='s4', t='Reactions', e='🔧', cards=['c6'], need=['mech'], note='Cleavage, nucleophiles/electrophiles, reaction types')]
META = dict(unit='chem-u14', subject='chem', n=14, title='Some Basic Principles of Organic Chemistry', cls=11, labs=['acidtune'],
            syllabus='Tetravalency of carbon; shapes of simple molecules — hybridisation (s and p); classification of organic compounds based on functional groups and those containing halogens, oxygen, nitrogen and sulphur; homologous series; isomerism — structural and stereoisomerism. Nomenclature (trivial and IUPAC). Covalent bond fission — homolytic and heterolytic: free radicals, carbocations and carbanions; stability of carbocations and free radicals, electrophiles and nucleophiles. Electronic displacement in a covalent bond — inductive effect, electromeric effect, resonance and hyperconjugation. Common types of organic reactions — substitution, addition, elimination and rearrangement.')
