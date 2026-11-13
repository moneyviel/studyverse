"""Concept cards for Chemistry Unit 19 — Biomolecules (written for StudyVerse)."""
TOPICS = {'carb': 'Carbohydrates: glucose, fructose, di- and polysaccharides', 'prot': 'Amino acids, peptides, proteins & enzymes', 'nucl': 'Nucleic acids: DNA and RNA', 'vit': 'Vitamins'}
CARDS = [
 dict(id='c1', t='Glucose', e='🍬', lvl='f', topic='carb',
  body=['Glucose C_{6}H_{12}O_{6} is an aldohexose. Evidence for its open chain: HI/heat → n-hexane (straight chain); NH_{2}OH → oxime and HCN → cyanohydrin (C=O); Br_{2} water → gluconic acid (–CHO); Ac_{2}O → pentaacetate (five –OH); HNO_{3} → saccharic acid (–CH_{2}OH at the other end).',
        'But glucose gives no Schiff\'s test and no NaHSO_{3} adduct, and its pentaacetate does not react with NH_{2}OH: it is mostly a six-membered ring (pyranose) hemiacetal.',
        'α and β glucose differ only at C1 — they are ANOMERS (α +112°, β +19°; in water both slowly reach +52.5°: mutarotation). D/L describes the –OH at the lowest stereocentre, NOT the sign of rotation.'],
  check=dict(q='Glucose + Br₂ water gives', o=['gluconic acid', 'saccharic acid', 'n-hexane', 'sorbitol'], a=0, why='Mild oxidation of –CHO only.')),
 dict(id='c2', t='Disaccharides & polysaccharides', e='🌾', lvl='m', topic='carb',
  body=['Sucrose = α-glucose C1 – β-fructose C2: both anomeric carbons used → NON-reducing. Hydrolysis gives invert sugar (laevorotatory: fructose −92.4° beats glucose +52.5°).',
        'Maltose (α1→4, glucose + glucose) and lactose (β1→4, galactose + glucose; milk sugar) keep a free hemiacetal → reducing.',
        'Starch = amylose (α1→4, unbranched, ~15–20%) + amylopectin (α1→4 with α1→6 branches). Glycogen ("animal starch") is like amylopectin but more branched. Cellulose = β1→4 glucose (cannot be digested by humans).'],
  check=dict(q='The non-reducing sugar is', o=['sucrose', 'maltose', 'lactose', 'glucose'], a=0, why='No free anomeric carbon.')),
 dict(id='c3', t='Amino acids & peptides', e='🔗', lvl='m', topic='prot',
  body=['α-amino acids H_{2}N–CHR–COOH exist as zwitterions. All except glycine are chiral (natural ones are L). Essential (must be eaten): valine, leucine, isoleucine, phenylalanine, tryptophan, threonine, methionine, lysine, arginine, histidine.',
        'Peptide bond = –CO–NH– formed by losing water. Gly-Ala means glycine\'s C=O is joined to alanine\'s N–H (N-terminus written first). n different residues used once give n! sequences; n residues have n − 1 peptide bonds.',
        'HNO_{2} turns –NH_{2} into –OH (alanine → lactic acid). Tyrosine has a phenolic –OH (violet with FeCl_{3}); cysteine\'s –SH forms –S–S– bridges; proline has a five-membered ring; histidine an imidazole ring.'],
  check=dict(q='Number of peptide bonds in a pentapeptide', o=['4', '5', '6', '3'], a=0, why='n − 1.')),
 dict(id='c4', t='Protein structure & enzymes', e='🥚', lvl='m', topic='prot',
  body=['Primary: amino-acid sequence. Secondary: α-helix / β-pleated sheet (backbone H-bonds). Tertiary: overall fold of one chain (fibrous or globular; H-bonds, –S–S–, ionic, van der Waals). Quaternary: several subunits (haemoglobin).',
        'Denaturation (heat, pH change, acids) breaks secondary and tertiary structure; the PRIMARY structure survives. Boiling egg white (albumin) coagulates it.',
        'Enzymes are mostly globular proteins, highly specific, and lower the activation energy (more than H^{+} does). Maltase: maltose → glucose; invertase: sucrose → glucose + fructose; ninhydrin turns violet with proteins.'],
  check=dict(q='α-helix belongs to which structure level?', o=['secondary', 'primary', 'tertiary', 'quaternary'], a=0, why='Backbone H-bonding pattern.')),
 dict(id='c5', t='Nucleic acids', e='🧬', lvl='h', topic='nucl',
  body=['Nucleoside = base + sugar (glycosidic bond). Nucleotide = nucleoside + phosphate. Nucleotides join by 5′–3′ PHOSPHODIESTER links.',
        'DNA: 2-deoxyribose; bases A, G (purines) and C, T (pyrimidines); double helix, A=T (2 H-bonds), G≡C (3 H-bonds); carries genetic information and self-duplicates. RNA: ribose, U replaces T, usually single-stranded; makes proteins (m-, r-, t-RNA).',
        'Chargaff: in double-stranded DNA %A = %T and %G = %C, so %A + %G = 50%. Chirality of DNA/RNA comes from the D-sugar.'],
  check=dict(q='H-bonds in a DNA segment with 3 G–C and 2 A–T pairs', o=['13', '10', '15', '12'], a=0, why='3×3 + 2×2.')),
 dict(id='c6', t='Vitamins', e='💊', lvl='f', topic='vit',
  body=['Fat-soluble: A, D, E, K — stored in liver and adipose tissue. Water-soluble: B-group and C — must be taken regularly; of these only B_{12} is stored.',
        'Names: A retinol, B_{1} thiamine, B_{2} riboflavin, B_{6} pyridoxine, B_{12} cyanocobalamin, C ascorbic acid, D calciferol, E tocopherol, K phylloquinone, H biotin.',
        'Deficiency: A night blindness; B_{1} beriberi; B_{2} cheilosis; B_{6} convulsions; B_{12} pernicious anaemia; C scurvy; D rickets; E fragile RBCs; K slow clotting.'],
  check=dict(q='Which vitamin is water-soluble yet stored in the body?', o=['B₁₂', 'C', 'B₁', 'B₆'], a=0, why='Stored in the liver.')),
]
FORMULAS = [('Peptide bonds', 'n residues → n − 1'), ('Sequences', 'n different, each once → n!'), ('DNA H-bonds', '3 × (G–C) + 2 × (A–T)'), ('Chargaff', '%A = %T, %G = %C, %A + %G = 50'), ('Dipeptide mass', 'M₁ + M₂ − 18'), ('Invert sugar', '+66.5° → about −20°')]
TRAPS = ['Sucrose is NON-reducing (both anomeric carbons are tied up).', 'Fructose reduces Tollens even though it is a ketose.', 'D/L is not the sign of rotation.', 'Denaturation keeps the primary structure.',
         'Gly-Ala ≠ Ala-Gly: N-terminus is written first.', 'Nucleotides are joined by phosphodiester bonds, not glycosidic bonds.', 'Tyrosine is NOT essential; arginine and histidine are (NCERT list).', 'Proline\'s ring is five-membered.']
STEPS = [dict(k='s1', t='Glucose', e='🍬', cards=['c1'], need=['carb'], note='Structure, reactions and anomers'),
         dict(k='s2', t='Sugars', e='🌾', cards=['c2'], need=['carb'], note='Sucrose, maltose, lactose, starch, cellulose'),
         dict(k='s3', t='Proteins', e='🔗', cards=['c3', 'c4'], need=['prot'], note='Amino acids, peptides, structure, enzymes'),
         dict(k='s4', t='DNA & vitamins', e='🧬', cards=['c5', 'c6'], need=['nucl', 'vit'], note='Nucleic acids and vitamins')]
META = dict(unit='chem-u19', subject='chem', n=19, title='Biomolecules', cls=12, labs=['dnapair'],
            syllabus='Carbohydrates: classification (aldoses and ketoses), monosaccharides (glucose and fructose) and constituent monosaccharides of oligosaccharides (sucrose, lactose and maltose). Proteins: elementary idea of α-amino acids, peptide bond, polypeptides; primary, secondary, tertiary and quaternary structure (qualitative idea only), denaturation of proteins. Vitamins: classification and functions. Nucleic acids: chemical constitution of DNA and RNA; biological functions of nucleic acids. Hormones: general introduction.')
