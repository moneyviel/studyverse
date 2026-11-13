"""Concept cards for Chemistry Unit 11 — d- and f-Block Elements (written for StudyVerse)."""
TOPICS = {'mag': 'Configurations, unpaired electrons & magnetism', 'trend': 'Trends: IE, atomisation, E°, oxides', 'oxo': 'KMnO₄ and K₂Cr₂O₇', 'lanth': 'Lanthanoids & actinoids'}
CARDS = [
 dict(id='c1', t='Configurations & magnetism', e='🧲', lvl='f', topic='mag',
  body=['<div class="jx-f">M^{q+} of the 3d series: 3d^{(Z − 18 − q)} (4s leaves first);  μ = √(n(n + 2)) BM</div>', 'Exceptions: Cr 3d^{5}4s^{1}, Cu 3d^{10}4s^{1}.',
        'Unpaired n → μ: 1 → 1.73, 2 → 2.83, 3 → 3.87, 4 → 4.90, 5 → 5.92.', 'd^{0} and d^{10} ions (Sc^{3+}, Ti^{4+}, Zn^{2+}, Cu^{+}) are colourless and diamagnetic.'],
  check=dict(q='μ of Fe²⁺ (spin-only) is', o=['4.90 BM', '5.92 BM', '3.87 BM', '2.83 BM'], a=0, why='d⁶ → 4 unpaired.')),
 dict(id='c2', t='Trends across the 3d series', e='📈', lvl='m', topic='trend',
  body=['Atomisation enthalpy peaks mid-series (V 515 kJ/mol), lowest for Zn (126). IE_{2} is high for Cr and Cu; IE_{3} for Mn (d^{5}) and Zn.',
        'E°(M^{2+}/M) is positive only for Cu (+0.34 V). Mn^{3+} and Co^{3+} are oxidants; Cr^{2+}, V^{2+}, Ti^{2+} are reductants.',
        'Low oxidation-state oxides are basic (MnO, CrO), middle amphoteric (Cr_{2}O_{3}, V_{2}O_{5}), highest acidic (Mn_{2}O_{7}, CrO_{3}).', 'Interstitial compounds: hard, high-melting, conducting, inert, non-stoichiometric.'],
  check=dict(q='Which 3d metal has E°(M²⁺/M) > 0?', o=['Cu', 'Zn', 'Fe', 'Ni'], a=0, why='+0.34 V.')),
 dict(id='c3', t='Permanganate & dichromate', e='🟣', lvl='m', topic='oxo',
  body=['<div class="jx-f">MnO_{4}^{−} + 8H^{+} + 5e^{−} → Mn^{2+};  basic/neutral: → MnO_{2} (3e^{−});  Cr_{2}O_{7}^{2−} + 14H^{+} + 6e^{−} → 2Cr^{3+}</div>',
        'KMnO_{4}: MnO_{2} + KOH + oxidant → K_{2}MnO_{4} (green) → KMnO_{4}. K_{2}Cr_{2}O_{7}: chromite + Na_{2}CO_{3}/air → Na_{2}CrO_{4} → dichromate (acid).',
        'Chromate ⇌ dichromate by pH (no redox). Chromyl chloride test: CrO_{2}Cl_{2} (+6).', 'K_{2}Cr_{2}O_{7} is a primary standard; KMnO_{4}, Na_{2}Cr_{2}O_{7}, NaOH are not.'],
  check=dict(q='Moles of KMnO₄ to oxidise 5 mol Fe²⁺ in acid:', o=['1', '5', '0.5', '2'], a=0, why='1 : 5.')),
 dict(id='c4', t='Lanthanoids & actinoids', e='🔬', lvl='m', topic='lanth',
  body=['Common state +3. Ce^{4+} (4f^{0}) and Tb^{4+} (4f^{7}) are oxidants; Eu^{2+} (4f^{7}) and Yb^{2+} (4f^{14}) are reductants.',
        'Lanthanoid contraction: steady shrinkage (poor 4f shielding) → Zr ≈ Hf; basicity of Ln(OH)_{3} falls from La to Lu.', 'f^{0}/f^{14} ions (La^{3+}, Lu^{3+}, Ce^{4+}, Yb^{2+}) are colourless and diamagnetic. Actinoids: more oxidation states, all radioactive, larger contraction.'],
  check=dict(q='Which ion is diamagnetic?', o=['La³⁺', 'Gd³⁺', 'Nd³⁺', 'Eu³⁺'], a=0, why='4f⁰.')),
]
FORMULAS = [('Spin-only', 'μ = √(n(n + 2)) BM'), ('d count', 'd^{Z − 18 − q}'), ('Acid MnO₄⁻', '5e^{−} → Mn^{2+}'), ('Basic MnO₄⁻', '3e^{−} → MnO_{2}'), ('Dichromate', '6e^{−} → 2Cr^{3+}'), ('Fe²⁺', '1e^{−} → Fe^{3+}'), ('Oxalate', '2e^{−} → 2CO_{2}')]
TRAPS = ['Remove 4s electrons before 3d when forming ions.', 'Manganate (+6, d¹) is paramagnetic; permanganate (+7, d⁰) is not.', 'In basic medium MnO₄⁻ takes only 3 electrons.', 'Cm has 8 unpaired electrons (5f⁷6d¹), Am 7.', 'Chromate ⇌ dichromate is NOT a redox change.']
STEPS = [dict(k='s1', t='Electrons', e='🧲', cards=['c1'], need=['mag'], note='Configurations and spin-only moments'),
         dict(k='s2', t='Trends', e='📈', cards=['c2'], need=['trend'], note='IE, atomisation, E°, oxides'),
         dict(k='s3', t='Oxo-salts', e='🟣', cards=['c3'], need=['oxo'], note='KMnO₄ and K₂Cr₂O₇ chemistry and titrations'),
         dict(k='s4', t='f-block', e='🔬', cards=['c4'], need=['lanth'], note='Lanthanoids and actinoids')]
META = dict(unit='chem-u11', subject='chem', n=11, title='d- and f-Block Elements', cls=12, labs=['dbox'],
            syllabus='Transition elements: general introduction, electronic configuration, occurrence and characteristics, general trends in properties of the first row transition elements — physical properties, ionisation enthalpy, oxidation states, atomic radii, colour, catalytic behaviour, magnetic properties, complex formation, interstitial compounds, alloy formation; preparation, properties and uses of K₂Cr₂O₇ and KMnO₄. Inner transition elements: lanthanoids — electronic configuration, oxidation states and lanthanoid contraction; actinoids — electronic configuration and oxidation states.')
