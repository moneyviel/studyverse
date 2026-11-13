"""Concept cards for Chemistry Unit 15 — Hydrocarbons (written for StudyVerse)."""
TOPICS = {'alk': 'Alkanes, alkenes & alkynes', 'aro': 'Aromatic hydrocarbons'}
CARDS = [
 dict(id='c1', t='Alkanes', e='⛽', lvl='f', topic='alk',
  body=['<div class="jx-f">C_{n}H_{2n+2} + (3n + 1)/2 O_{2} → n CO_{2} + (n + 1) H_{2}O</div>',
        'Preparation: hydrogenation of alkenes/alkynes (Pt, Pd, Ni); RX + Zn/H^{+}; Wurtz 2RX + 2Na → R–R (even C); decarboxylation RCOONa + NaOH/CaO → R–H (one C less); Kolbe electrolysis 2RCOONa → R–R.',
        'Free-radical halogenation (Cl_{2}/hν): number of monochlorides = kinds of H. Conformations of ethane: staggered (60°, most stable) vs eclipsed (12.5 kJ/mol higher).',
        'Branching lowers b.p. Isomerisation (AlCl_{3}/HCl), aromatisation (n-hexane → benzene, heptane → toluene), pyrolysis/cracking.'],
  check=dict(q='Sodium propanoate + soda lime gives', o=['ethane', 'propane', 'butane', 'methane'], a=0, why='Loses CO₂: one carbon fewer.')),
 dict(id='c2', t='Alkenes', e='🔗', lvl='m', topic='alk',
  body=['Prepared by dehydrohalogenation (alc. KOH, Saytzeff: more substituted alkene), dehydration of alcohols (conc. H_{2}SO_{4}), partial reduction of alkynes (Lindlar → cis; Na/liq. NH_{3} → trans).',
        'Electrophilic addition. HX: Markovnikov (via the more stable carbocation). HBr + peroxide: anti-Markovnikov (radical); not with HCl or HI.',
        'Ozonolysis (O_{3}, then Zn/H_{2}O): each C=C → two C=O. Baeyer test: cold dil. alkaline KMnO_{4} decolourises (glycol). Hot acidic KMnO_{4} cleaves to acids/ketones.'],
  check=dict(q='Propene + HBr (peroxide) →', o=['1-bromopropane', '2-bromopropane', '1,2-dibromopropane', 'propan-2-ol'], a=0, why='Br• adds to the CH₂ end.')),
 dict(id='c3', t='Alkynes', e='⚡', lvl='m', topic='alk',
  body=['Prepared from vicinal dihalides with alc. KOH then NaNH_{2}; ethyne from CaC_{2} + H_{2}O.',
        'Terminal ≡C–H is acidic (sp C): reacts with Na, NaNH_{2}, ammoniacal AgNO_{3}/Cu_{2}Cl_{2} (but-2-yne does not).',
        'Hydration (HgSO_{4}/H_{2}SO_{4}, 333 K): ethyne → ethanal, other alkynes → ketones. Red-hot iron tube: 3 HC≡CH → benzene; propyne → mesitylene.'],
  check=dict(q='Propyne + H₂O (Hg²⁺/H⁺) →', o=['propanone', 'propanal', 'propan-1-ol', 'propene'], a=0, why='Markovnikov enol → ketone.')),
 dict(id='c4', t='Benzene & substitution', e='⬡', lvl='h', topic='aro',
  body=['Aromatic: planar, 6π, resonance-stabilised → substitution (keeps the ring) rather than addition. Electrophiles: NO_{2}^{+} (HNO_{3}/H_{2}SO_{4}), Br^{+} (Br_{2}/FeBr_{3}), SO_{3}, R^{+}/RCO^{+} (AlCl_{3}).',
        'o/p directors & activators: –OH, –NH_{2}, –OR, –NHCOR, –R. Halogens: o/p but deactivating. m directors & deactivators: –NO_{2}, –CN, –CHO, –COR, –COOH, –SO_{3}H.',
        'Friedel–Crafts fails on strongly deactivated rings (nitrobenzene) and on aniline (–NH_{2} binds AlCl_{3}). Alkylation rearranges (n-PrCl → cumene) and over-alkylates. Benzpyrene-type PAHs are carcinogenic.'],
  check=dict(q='Nitration of toluene gives mainly', o=['o- and p-nitrotoluene', 'm-nitrotoluene', 'nitrobenzene', 'no reaction'], a=0, why='–CH₃ is o/p directing.')),
]
FORMULAS = [('Combustion', 'C_{x}H_{y} needs x + y/4 mol O_{2}'), ('Alkene', 'C_{n}H_{2n}'), ('Alkyne', 'C_{n}H_{2n−2}'), ('Decarboxylation', 'RCOONa → RH (one C less)'), ('Kolbe', '2RCOONa → R–R')]
TRAPS = ['Peroxide effect only with HBr.', 'Kolbe electrolysis of CH₃COONa gives ETHANE, not methane.', 'Lindlar → cis; Na/NH₃ → trans.', 'Benzene does not decolourise bromine water.', 'Nitrobenzene does not undergo Friedel–Crafts.', 'n-Propyl chloride + benzene/AlCl₃ gives mostly cumene.']
STEPS = [dict(k='s1', t='Alkanes', e='⛽', cards=['c1'], need=['alk'], note='Preparation, halogenation, conformations'),
         dict(k='s2', t='Alkenes', e='🔗', cards=['c2'], need=['alk'], note='Additions, Markovnikov, ozonolysis'),
         dict(k='s3', t='Alkynes', e='⚡', cards=['c3'], need=['alk'], note='Acidity, hydration, reductions'),
         dict(k='s4', t='Benzene', e='⬡', cards=['c4'], need=['aro'], note='Aromaticity, EAS, directing groups')]
META = dict(unit='chem-u15', subject='chem', n=15, title='Hydrocarbons', cls=11, labs=['eas'],
            syllabus='Classification, isomerism, IUPAC nomenclature, general methods of preparation, properties and reactions. Alkanes — conformations: Sawhorse and Newman projections (of ethane); mechanism of halogenation of alkanes. Alkenes — geometrical isomerism; mechanism of electrophilic addition: addition of hydrogen, halogens, water, hydrogen halides (Markownikoff\'s and peroxide effect); ozonolysis and polymerization. Alkynes — acidic character; addition of hydrogen, halogens, water and hydrogen halides; polymerization. Aromatic hydrocarbons — nomenclature, benzene: structure and aromaticity; mechanism of electrophilic substitution: halogenation, nitration, Friedel-Crafts alkylation and acylation, directive influence of the functional group in mono-substituted benzene.')
