"""Concept cards for Chemistry Unit 10 — p-Block Elements, groups 13 to 18 (written for StudyVerse)."""
TOPICS = {'g1314': 'Groups 13 & 14 (boron and carbon families)', 'g15': 'Group 15 (nitrogen family)', 'g1618': 'Groups 16, 17 & 18', 'gen': 'Octet rule & shapes of p-block species'}
CARDS = [
 dict(id='c1', t='Group 13: boron family', e='🧱', lvl='m', topic='g1314',
  body=['Radius: B < Ga < Al < In < Tl (Ga is smaller than Al — 3d shielding is poor). IE_{1}: B ≫ Tl > Ga > Al > In.',
        'Inert-pair effect: +1 grows stable down the group; Tl^{+} is stable, Tl^{3+} is a strong oxidant (E° +1.26 V).',
        'Boron: very high m.p. (giant covalent lattice), forms only covalent compounds; boric acid is a weak MONObasic Lewis acid; diborane has two 3c–2e B−H−B bonds.',
        'Al: amphoteric Al_{2}O_{3}; passive in conc. HNO_{3}; Al + NaOH → Na[Al(OH)_{4}] + H_{2}; [Al(H_{2}O)_{6}]^{3+} is octahedral (sp^{3}d^{2}).'],
  check=dict(q='Most stable oxidation state of Tl :', o=['+3', '+1', '+2', '0'], a=1, why='Inert pair 6s².')),
 dict(id='c2', t='Group 14: carbon family', e='💎', lvl='m', topic='g1314',
  body=['Catenation: C ≫ Si > Ge ≈ Sn; carbon also makes pπ−pπ multiple bonds → diamond, graphite, fullerenes.',
        'Oxides: CO_{2}, SiO_{2}, GeO_{2} acidic; SnO, SnO_{2}, PbO, PbO_{2} amphoteric; CO neutral.',
        '+2 becomes more stable down the group: Sn^{2+} reducing, Pb^{4+} oxidising.',
        'Lowest m.p. in the group: Sn (505 K). IE_{1}: Pb > Sn (4f shielding). Graphite conducts, diamond (sp^{3}) does not.'],
  check=dict(q='Amphoteric oxide :', o=['SiO₂', 'SnO₂', 'CO₂', 'CO'], a=1, why='Down the group oxides turn basic.')),
 dict(id='c3', t='Group 15: nitrogen family', e='🌫️', lvl='m', topic='g15',
  body=['N: max covalency 4, no d orbitals, strong pπ−pπ (N≡N, oxides N_{2}O … N_{2}O_{5}); N−N single bond is weaker than P−P.',
        'Hydrides EH_{3}: stability and basicity DEcrease, reducing power INcreases down the group; bond angle 107.8° → 93.6° → 91.8°; b.p.: PH_{3} lowest, NH_{3} high (H-bonds).',
        '+5 becomes less stable down the group; Bi^{3+} is the stable state.',
        'Oxoacids of P: basicity = number of P−OH. H_{3}PO_{4} 3, H_{3}PO_{3} 2, H_{3}PO_{2} 1; P−H bonds make H_{3}PO_{2}, H_{3}PO_{3} reducing.'],
  check=dict(q='Basicity of H₃PO₃ :', o=['3', '2', '1', '0'], a=1, why='One H is on P.')),
 dict(id='c4', t='Groups 16, 17 and 18', e='💨', lvl='m', topic='g1618',
  body=['O: diatomic (big m.p. gap with S_{8}); shows −2, −1, +2 (OF_{2}); ozone is bent, diamagnetic, has 6 lone pairs.',
        'Down group 16: +4 more stable, +6 less; H_{2}Te is the strongest reducing agent and acid among H_{2}E.',
        'Halogens: Cl has the most negative Δ_{eg}H; F−F bond is weaker than Cl−Cl; oxidising power F_{2} > Cl_{2} > Br_{2} > I_{2}; HF is weak but has the highest b.p.',
        'Noble gases: very low b.p.; Xe forms XeF_{2} (linear), XeF_{4} (square planar), XeF_{6} (distorted octahedral), XeO_{3} (pyramidal), XeOF_{4} (square pyramidal).'],
  check=dict(q='Strongest acid :', o=['HF', 'HI', 'HCl', 'HBr'], a=1, why='Weakest H−I bond.')),
 dict(id='c5', t='Octet rule and its exceptions', e='🎯', lvl='f', topic='gen',
  body=['Obey: CO_{2}, CCl_{4}, CH_{4}. Incomplete octet: BF_{3}, BCl_{3}, AlCl_{3}, BeCl_{2}. Odd electron: NO, NO_{2}, ClO_{2}.',
        'Expanded octet (needs d orbitals, 3rd period on): PCl_{5}, SF_{6}, H_{2}SO_{4}, IF_{7}.',
        'Linear species: BeCl_{2}, CO_{2}, N_{3}^{−}, NO_{2}^{+}, XeF_{2}, I_{3}^{−}; SO_{2}, O_{3}, NO_{2} are bent.'],
  check=dict(q='Odd-electron molecule :', o=['CO₂', 'NO₂', 'SO₂', 'O₃'], a=1, why='17 valence electrons.')),
]
FORMULAS = [('Basicity', 'P−OH groups'), ('P oxidation state', '+2 (P=O) + n_{OH} − n_{H}'), ('Inert pair', 'lower state ↑ down the group'), ('Oleum', 'H_{2}S_{2}O_{7}')]
TRAPS = ['Ga < Al in size; Tl has higher IE than In.', 'H₃PO₃ is dibasic, H₃PO₂ monobasic — P−H hydrogens are not acidic.', 'NH₃ boils higher than PH₃, but PH₃ is the lowest; after that b.p. rises.',
         'Down group 16 the +4 state gets MORE stable, +6 LESS.', 'Al + NaOH gives [Al(OH)₄]⁻, not [Al(OH)₆]³⁻.', 'Noble gases have very LOW boiling points.']
STEPS = [dict(k='s1', t='Groups 13–14', e='🧱', cards=['c1', 'c2'], need=['g1314'], note='Boron and carbon families'),
         dict(k='s2', t='Group 15', e='🌫️', cards=['c3'], need=['g15'], note='Nitrogen family, hydrides and oxoacids'),
         dict(k='s3', t='Groups 16–18', e='💨', cards=['c4', 'c5'], need=['g1618', 'gen'], note='Oxygen family, halogens, noble gases, octet exceptions')]
META = dict(unit='chem-u10', subject='chem', n=10, title='p-Block Elements', cls=12, labs=['oxoacid'],
            syllabus="Group-13 to Group 18 Elements: General Introduction: Electronic configuration and general trends in physical and chemical properties of elements across the periods and down the groups; unique behaviour of the first element in each group.")
