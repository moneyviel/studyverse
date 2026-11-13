"""CA Final · Paper 5 · Part II Customs · Chapter 3 Classification of Imported and Export Goods.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ii-ch03-u01'
T1 = 'Structure of the Customs Tariff'
T2 = 'Rules 1 and 2: legal text, incomplete goods and mixtures'
T3 = 'Rules 3 to 6: competing headings, akin goods, containers'
T4 = 'Parts and project imports'


def build():
    ck = Checks()
    sp = ck.add('50000000*0.10', 'Maximum spares, raw materials and consumables under project imports at 10% of specified goods (₹)')
    i1 = {'id': 'i1', 'title': 'Project imports limit', 'difficulty': 'core', 'minutes': 5,
          'q': 'Meridian Cement registers a contract for project imports of machinery valued at ₹5 crore for substantial expansion. It also wants to import spares worth ₹60 lakh under heading 9801. Advise.',
          'solution': [table(['Point', 'Rule', 'Result'], [
              ['Specified goods', 'Machinery for substantial expansion', '₹5,00,00,000 eligible'],
              ['Spares limit', '10% of specified goods value', f'₹{inr(sp)}'],
              ['Excess spares', '₹60 lakh − ₹50 lakh', '₹10 lakh assessed under own headings']], title='Heading 9801')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Applying the interpretative rules', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Classify: (a) a bicycle imported in knocked-down kit form; (b) a pencil with an eraser tip; (c) a reusable steel gas cylinder containing gas; (d) a fitted case supplied with a violin.',
          'solution': [table(['Item', 'Rule', 'Result'], [
              ['(a) CKD bicycle', 'Rule 2(a): unassembled article having essential character', 'As a bicycle'],
              ['(b) Pencil with eraser', 'Rule 3(b): essential character', 'As a pencil'],
              ['(c) Gas cylinder', 'Rule 5(b) exception: repetitive use', 'Cylinder classified separately'],
              ['(d) Violin case', 'Rule 5(a): specially fitted case', 'With the violin']], title='General Rules for Interpretation')]}

    concepts = [
        C('c1', T1, [
            'The First Schedule to the Customs Tariff Act, 1975 follows the Harmonized System: 21 sections and 98 chapters (97 HSN chapters plus India\'s Chapter 98 for special items like project imports). Codes are 8 digits in India against the 6-digit international level.',
            'Each chapter has chapter notes with statutory force, then headings (4 digits), sub-headings (6 digits) and tariff items (8 digits). Columns show unit, standard rate and preferential rate.',
            'The three General Explanatory Notes: dashes show the level of sub-classification; "%" means percentage of value under section 14; if no preferential rate is shown, the standard rate applies. The six General Rules for Interpretation (GRI) form part of the schedule and are applied in sequence.'],
          'An 8-digit address for every good.',
          'One dash marks a first-level split of a heading; two dashes split that further.'),
        C('c2', T2, [
            'Rule 1: section, chapter and sub-chapter titles are for reference only; legal classification follows the terms of headings and the related section or chapter notes. Notes of one chapter cannot be used to read another unless they say so.',
            'Rule 2(a): a heading covering an article includes it in incomplete or unfinished form if it has the essential character of the finished article, and also unassembled or disassembled forms (CKD/SKD).',
            'Rule 2(b): a reference to a material includes mixtures and combinations with other materials; goods of more than one material are classified under rule 3.'],
          'Legal text first, titles never.',
          'A car body shell without wheels still classifies as a car if it has its essential character.'),
        C('c3', T3, [
            'Rule 3(a): the most specific heading wins (an electric shaver under 8510 rather than domestic appliances 8509), but headings each covering only part of a composite good are equally specific. Rule 3(b): mixtures, composite goods and retail sets go by the component giving essential character, judged by nature, bulk, weight, value or role. Rule 3(c): if still undecided, the heading last in numerical order applies (Mahindra and Mahindra — 8704 over 8703).',
            'Rule 4: goods not classifiable under the earlier rules go to the heading of goods they are most akin to, e.g. sun-control films treated like plastic blinds.',
            'Rule 5(a): cases specially shaped for an article and suitable for long-term use are classified with it when presented together, unless the case gives the whole its essential character. Rule 5(b): normal packing goes with the goods, except packing clearly suitable for repeated use. Rule 6 limits comparison to sub-headings of equal rank within a heading.'],
          'Specific, then essential character, then the last heading.',
          'A gift set of perfume and soap takes the classification of the item giving the set its character.'),
        C('c4', T4, [
            'Parts suitable solely for a machine generally follow the machine\'s heading, but parts of general use (screws, springs) go to their own headings, and a separate parts heading takes priority where it exists, all subject to section and chapter notes.',
            'Project imports under heading 9801 give one rate for all machinery, instruments, components and raw materials needed for initial setting up or substantial expansion of specified projects (industrial plants, irrigation, power and others), easing assessment of many diverse items.',
            'Spares, raw materials and consumables up to 10% of the value of the specified goods may be imported under the project, subject to conditions such as contract registration. Individual exemption notifications can still apply to items under 9801.'],
          'Parts follow the machine unless they are general-use or have their own heading.',
          'Bolts imported for a turbine are still classified as bolts.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Classification memo', 'role': 'Customs classification specialist',
             'situation': 'A new composite product must be classified before import.',
             'steps': ['Read heading text and notes (Rule 1).', 'Check incomplete or mixture issues (Rule 2).', 'Resolve competing headings (Rule 3).', 'Document essential character evidence.'],
             'takeaway': 'Follow the rules in order and record why each step resolved.'}]

    mcqs = [
        Q('m1', 'Titles of sections and chapters in the tariff are:', ['For reference only', 'Legally binding', 'Decisive in disputes', 'Applicable only to exports'], 0,
          'Rule 1. In practice: rely on headings.', 'c2', T2),
        Q('m2', 'An unassembled article having essential character of the finished article is classified:', ['As the finished article', 'As parts', 'Under residual heading', 'Under Chapter 98'], 0,
          'Rule 2(a). In practice: CKD kits.', 'c2', T2),
        Q('m3', 'When goods equally merit two headings after rules 3(a) and 3(b), choose:', ['The heading occurring last in numerical order', 'The first heading', 'The lower-duty heading', 'The higher-duty heading'], 0,
          'Rule 3(c). In practice: Mahindra case.', 'c3', T3),
        Q('m4', 'The akin rule is:', ['Rule 4', 'Rule 2', 'Rule 5', 'Rule 6'], 0,
          'Most similar goods. In practice: last resort.', 'c3', T3),
        Q('m5', 'Packing containers clearly suitable for repetitive use are:', ['Classified separately', 'Classified with the goods', 'Exempt', 'Classified under Chapter 98'], 0,
          'Rule 5(b) exception. In practice: gas cylinders.', 'c3', T3),
        Q('m6', 'Rule 6 provides that:', ['Only sub-headings at the same level are compared', 'Specific beats general', 'Titles are binding', 'Parts follow machines'], 0,
          'Sub-heading comparison. In practice: same level.', 'c3', T3),
        Q('m7', 'Spares under project imports are allowed up to:', ['Ten percent of specified goods value', 'Twenty-five percent', 'Five percent', 'Fifteen percent'], 0,
          'Heading 9801. In practice: conditions apply.', 'c4', T4),
        Q('m8', 'The Indian tariff classifies goods at what digit level?', ['Eight', 'Six', 'Four', 'Ten'], 0,
          'HS international six. In practice: tariff item.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Eligibility', 1, 'analysis', 'substantial expansion'), S('s2', 'Spares limit', 3, 'computation', '10%', nums=[sp])],
          ['State excess treatment.'], ['Applying project rate to all spares.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Rule 2(a)', 1, 'analysis', 'unassembled'), S('s2', 'Rule 3(b)', 2, 'analysis', 'essential character'), S('s3', 'Rule 5', 3, 'analysis', 'repetitive')],
          ['Name each rule.'], ['Classifying cylinders with gas.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What decides essential character?', 'Factors like nature, bulk, quantity, weight, value and the role of each component.',
          [P('p1', 'Bulk', 5, 'bulk'), P('p2', 'Role', 5, 'role')], 'c3'),
        V('v2', 'Why does India have Chapter 98?', 'It holds special items such as project imports beyond the 97 HSN chapters.',
          [P('p1', 'Project imports', 5, 'project imports'), P('p2', 'Special items', 5, 'special')], 'c1'),
        V('v3', 'How are parts of general use classified?', 'Under their own headings, separately from the machine they serve.',
          [P('p1', 'Own headings', 5, 'own heading'), P('p2', 'Separately', 5, 'separately')], 'c4'),
        V('v4', 'What does a double dash before a description mean?', 'A further split of the immediately preceding single-dash item.',
          [P('p1', 'Preceding', 5, 'preceding'), P('p2', 'Single-dash', 5, 'single-dash')], 'c1'),
        V('v5', 'When does Rule 5(a) stop applying to a case?', 'When the case itself gives the whole its essential character.',
          [P('p1', 'Essential character', 5, 'essential character'), P('p2', 'Case itself', 5, 'case itself')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Composite fitness device', 'difficulty': 'moderate',
              'case': 'A smart skipping rope with a step counter is imported. The rope is the main part by weight and use; the counter is a small add-on.',
              'mcqs': [
                  M('k1a', 'Which rule resolves this composite?', ['Rule 3(b)', 'Rule 4', 'Rule 6', 'Rule 2(a)'], 0,
                    'Essential character. In practice: weigh role.', 'moderate', topic=T3),
                  M('k1b', 'Essential character comes from:', ['The rope', 'The counter', 'The packing', 'The battery'], 0,
                    'Dominant role. In practice: evidence of use.', 'moderate', topic=T3),
                  M('k1c', 'Is the chapter title decisive?', ['No', 'Yes', 'Only for sports goods', 'Only with notes'], 0,
                    'Rule 1. In practice: heading text governs.', 'moderate', topic=T2),
                  M('k1d', 'If two headings still equally apply, choose:', ['The one last in numerical order', 'The first', 'The cheaper', 'Either'], 0,
                    'Rule 3(c). In practice: rare.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ii-ch03', 1, 'Classification of Imported and Export Goods',
                ['Explain the structure of the Customs Tariff.',
                 'Apply Rules 1 and 2 of interpretation.',
                 'Apply Rules 3 to 6 of interpretation.',
                 'Classify parts and project imports.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p5-ii-ch02-u01'],
                 'exam_tip': 'Apply the rules in sequence and stop at the first rule that resolves classification.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['21 sections, 98 chapters; 8-digit codes.', 'Rule 1 headings and notes; Rule 2 incomplete and mixtures.', 'Rule 3: specific, essential character, last heading.',
                             'Rule 4 akin; Rule 5 cases and packing; Rule 6 same-level sub-headings.', 'Project imports heading 9801; spares 10%.'],
                 'remember': ['Three General Explanatory Notes: dashes, %, standard rate.'],
                 'traps': ['Jumping to Rule 3(c) before 3(a) and 3(b).']},
                [('Rule 1', 'Headings and notes'), ('Rule 2', 'Incomplete/mixtures'), ('Rule 3', 'Competing headings'), ('Rule 4', 'Akin'), ('Rule 5', 'Containers')],
                viva, cases)
