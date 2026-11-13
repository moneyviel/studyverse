"""Concept cards for Chemistry Unit 20 — Principles Related to Practical Chemistry (written for StudyVerse)."""
TOPICS = {'cat': 'Salt analysis: cations, group reagents, flame tests', 'ani': 'Anions, gases and detection of elements', 'titr': 'Titrations and preparations'}
CARDS = [
 dict(id='c1', t='Cation group ladder', e='🪜', lvl='m', topic='cat',
  body=['Group 0: NH_{4}^{+} (warm with NaOH → NH_{3}; Nessler → brown ppt). I: dil. HCl → PbCl_{2}, AgCl, Hg_{2}Cl_{2}. II: H_{2}S in dil. HCl → CuS, CdS, As_{2}S_{3}, Bi_{2}S_{3} (low [S^{2−}] catches only very insoluble sulphides).',
        'III: NH_{4}Cl + NH_{4}OH → Fe(OH)_{3} (reddish brown), Al(OH)_{3} (white gelatinous), Cr(OH)_{3} (green). NH_{4}Cl (common ion) lowers [OH^{−}] so group IV–VI hydroxides stay dissolved. IV: H_{2}S in NH_{4}OH → ZnS (white), MnS (buff), NiS/CoS (black).',
        'V: (NH_{4})_{2}CO_{3} + NH_{4}OH → BaCO_{3}, SrCO_{3}, CaCO_{3}. VI: Mg^{2+} (Na_{2}HPO_{4} → white ppt), Na^{+}, K^{+}. Precipitation order from K_{sp}: the salt needing the smaller [OH^{−}] or [S^{2−}] comes out first.'],
  check=dict(q='Group reagent for Zn²⁺:', o=['H₂S in NH₄OH', 'H₂S in dil. HCl', 'dil. HCl', '(NH₄)₂CO₃'], a=0, why='ZnS needs the high [S²⁻] of alkaline medium.')),
 dict(id='c2', t='Flame & confirmatory tests', e='🔥', lvl='m', topic='cat',
  body=['Flame: Ca brick red, Sr crimson, Ba apple green, Cu green-blue, Na golden yellow, K lilac. Zn, Fe, Al, Mg give no characteristic flame.',
        'K_{4}[Fe(CN)_{6}]: Fe^{3+} Prussian blue, Cu^{2+} chocolate brown, Zn^{2+} bluish white. Ni^{2+} + dimethylglyoxime (NH_{4}OH) → rose-red. Ba^{2+} + K_{2}CrO_{4} → yellow BaCrO_{4}; Ca^{2+} + ammonium oxalate → white.',
        'Borax bead (coloured ions only): Cu blue (cold), Fe yellow/green, Co deep blue, Mn violet, Ni brown, Cr green. Pb^{2+}: KI → yellow PbI_{2}; PbCrO_{4} dissolves in NaOH as [Pb(OH)_{4}]^{2−}.'],
  check=dict(q='Apple-green flame shows', o=['Ba²⁺', 'Ca²⁺', 'Sr²⁺', 'Cu²⁺'], a=0, why='Barium.')),
 dict(id='c3', t='Anions & elements', e='🧪', lvl='m', topic='ani',
  body=['Dil. H_{2}SO_{4}: CO_{3}^{2−} → CO_{2} (lime water milky); S^{2−} → H_{2}S (lead acetate paper black, PbS); SO_{3}^{2−} → SO_{2} (acidified dichromate green); NO_{2}^{−} → brown fumes.',
        'AgNO_{3} (after dil. HNO_{3}): Cl^{−} white, soluble in NH_{4}OH; Br^{−} pale yellow, sparingly soluble; I^{−} yellow, insoluble. NO_{3}^{−}: brown ring with FeSO_{4}/conc. H_{2}SO_{4}. SO_{4}^{2−}: BaCl_{2} white. PO_{4}^{3−}: canary-yellow (NH_{4})_{3}PO_{4}·12MoO_{3}.',
        'Lassaigne (Na fusion): N → NaCN → Prussian blue; S → Na_{2}S → black PbS / violet with nitroprusside; N + S → NaSCN → blood red with Fe^{3+}; halogens → AgX (boil with HNO_{3} first). Compounds with N but no C (e.g. N_{2}H_{4}) fail the N test.'],
  check=dict(q='Lead acetate paper turns black because of', o=['PbS', 'PbSO₃', 'PbSO₄', 'PbO'], a=0, why='H₂S + Pb²⁺.')),
 dict(id='c4', t='Titrations & preparations', e='⚗️', lvl='h', topic='titr',
  body=['KMnO_{4} (acidic, dil. H_{2}SO_{4}, never HCl) is its own indicator: endpoint = first permanent pink. 2MnO_{4}^{−} + 5C_{2}O_{4}^{2−} + 16H^{+}; MnO_{4}^{−} + 5Fe^{2+} + 8H^{+}. Use M_{1}n_{1}V_{1} = M_{2}n_{2}V_{2} (n: MnO_{4}^{−} 5, oxalate 2, Fe^{2+} 1).',
        'Oxalic acid needs warming to 50–60 °C (slow start; Mn^{2+} formed then autocatalyses). Mohr\'s salt is titrated cold (warming lets air oxidise Fe^{2+}). Oxalic acid dihydrate 126, Mohr\'s salt 392 g mol^{−1}.',
        'Preparations: Mohr\'s salt and potash alum — add a little dil. H_{2}SO_{4} to stop hydrolysis; acetanilide from aniline + acetic anhydride; p-nitroacetanilide by nitrating acetanilide; aniline yellow by diazo coupling; iodoform from ethanol/acetone + I_{2}/NaOH.'],
  check=dict(q='Indicator in KMnO₄ vs Mohr\'s salt titration', o=['KMnO₄ itself', 'phenolphthalein', 'methyl orange', 'starch'], a=0, why='Self-indicator.')),
]
FORMULAS = [('Equivalents', 'M₁n₁V₁ = M₂n₂V₂'), ('n-factors', 'MnO₄⁻ 5 · C₂O₄²⁻ 2 · Fe²⁺ 1 · Cr₂O₇²⁻ 6'), ('Precipitation pH', '[OH⁻] = (Ksp/[Mⁿ⁺])^{1/n}'), ('Group order', '0 · I HCl · II H₂S/H⁺ · III NH₄OH/NH₄Cl · IV H₂S/NH₄OH · V (NH₄)₂CO₃')]
TRAPS = ['NH₄Cl lowers [OH⁻] (common ion) — it is not added to supply Cl⁻.', 'Group II uses H₂S in ACID, group IV in ALKALI.', 'Lead acetate paper turns black due to PbS, not PbSO₃.', 'Never acidify KMnO₄ with HCl.',
         'Heat oxalic acid titrations, not Fe²⁺ titrations.', 'Zn²⁺ gives no flame colour and a colourless borax bead.', 'Mohr\'s salt: dil. H₂SO₄ stops hydrolysis of FeSO₄.']
STEPS = [dict(k='s1', t='Groups', e='🪜', cards=['c1'], need=['cat'], note='Group reagents and precipitation order'),
         dict(k='s2', t='Confirm', e='🔥', cards=['c2'], need=['cat'], note='Flame, bead and confirmatory tests'),
         dict(k='s3', t='Anions', e='🧪', cards=['c3'], need=['ani'], note='Anion tests and Lassaigne\'s test'),
         dict(k='s4', t='Titrate', e='⚗️', cards=['c4'], need=['titr'], note='Redox titrations and lab preparations')]
META = dict(unit='chem-u20', subject='chem', n=20, title='Principles Related to Practical Chemistry', cls=12, labs=['saltlad'],
            syllabus="Detection of extra elements (N, S, halogens) in organic compounds; detection of functional groups. Chemistry involved in the preparation of Mohr's salt, potash alum, acetanilide, p-nitroacetanilide, aniline yellow, iodoform. Chemistry involved in titrimetric exercises: acids, bases and indicators, oxalic acid vs KMnO4, Mohr's salt vs KMnO4. Chemical principles involved in qualitative salt analysis: cations Pb2+, Cu2+, Al3+, Fe3+, Zn2+, Ni2+, Ca2+, Ba2+, Mg2+, NH4+; anions CO3^2-, S2-, SO4^2-, NO3-, NO2-, Cl-, Br-, I-. Enthalpy of solution and neutralisation experiments.")
