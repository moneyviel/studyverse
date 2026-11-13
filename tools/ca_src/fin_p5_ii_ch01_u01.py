"""CA Final · Paper 5 · Part II Customs · Chapter 1 Levy of and Exemptions from Customs Duty.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ii-ch01-u01'
T1 = 'Customs territory and the taxable event'
T2 = 'Relevant date for rate of duty'
T3 = 'Pilferage, abatement, remission and abandonment'
T4 = 'Exemptions from customs duty'


def build():
    ck = Checks()
    d0 = ck.add('800000*0.20', 'Duty on goods before damage (₹)')
    d1 = ck.add('800000*0.20*500000/800000', 'Abated duty in proportion to value after damage (₹)')
    i1 = {'id': 'i1', 'title': 'Abatement for damaged goods', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Ceramic tiles valued at ₹8,00,000 (effective duty 20%) were damaged during unloading at the port due to a crane failure. The assessable value of the damaged lot is ₹5,00,000. Compute duty payable under section 22.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Duty before damage', '8,00,000 × 20%', inr(d0)],
              ['Abated duty', 'Duty × 5,00,000 / 8,00,000', inr(d1)]], title='Section 22(2)')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Which rate applies?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Kestrel Imports filed a bill of entry for home consumption on 6 July; the vessel entered inwards on 9 July. Duty was 15% until 7 July and 10% from 8 July. For a second lot warehoused on 12 July and cleared ex-warehouse on 20 November, the rate was cut to 7.5% from 1 November. State the applicable rates.',
          'solution': [table(['Lot', 'Relevant date', 'Rate'], [
              ['Home consumption', 'Later of bill of entry (6 July) and entry inwards (9 July) → 9 July', '10%'],
              ['Ex-warehouse', 'Date of bill of entry for home consumption from warehouse → 20 November', '7.5%']], title='Section 15')]}

    concepts = [
        C('c1', T1, [
            'Section 12 levies customs duty on goods imported into or exported from India at rates under the Customs Tariff Act, 1975 or other law; Government goods are not exempt by default. India includes territorial waters up to 12 nautical miles from the baseline, while Indian customs waters extend to the exclusive economic zone (200 nautical miles).',
            'The charge is on the goods. For goods cleared for home consumption, import is completed when goods reach the customs barrier and a bill of entry is filed (Garden Silk Mills). For warehoused goods, import is completed on clearance from the warehouse (Apar Ltd.). Export is complete when goods cross the territorial waters.',
            'Section 20 makes re-imported goods dutiable like fresh imports, though notifications give concessions, e.g. goods exported for repairs pay duty only on the fair cost of repairs plus freight and insurance both ways, when re-imported within the time limits.'],
          'Duty attaches to goods crossing the customs frontier.',
          'Goods on a ship anchored at sea are not yet imported for duty purposes.'),
        C('c2', T2, [
            'Section 15 fixes the date for rate of duty and tariff value. Goods for home consumption: date of presenting the bill of entry, or entry inwards of the vessel or arrival of aircraft or vehicle, whichever is later.',
            'Goods cleared from a warehouse: date of presenting the bill of entry for home consumption for those goods. Any other goods: date of payment of duty.',
            'A bill of entry filed before arrival is treated as presented on entry inwards. Section 15 governs only rate and tariff value; transaction value is under section 14.'],
          'Later of filing or arrival for direct clearance.',
          'A rate cut after warehousing benefits goods cleared later.'),
        C('c3', T3, [
            'Section 13: goods pilfered after unloading and before the clearance or warehousing order are free of duty for the importer unless restored; the custodian pays duty under section 45. It covers petty theft, not loss of whole packages.',
            'Section 22: duty on goods damaged or deteriorated before or during unloading, or damaged by accident after unloading but before examination (or warehoused goods before clearance) without the owner\'s fault, is reduced in proportion of value after damage to value before. Section 23(1): duty is remitted on goods lost (other than by pilferage) or destroyed before clearance for home consumption; this covers warehoused goods too.',
            'Section 23(2): the owner may relinquish title before the clearance or warehousing order and escape duty, unless an offence appears to have been committed. Section 24 permits denaturing or mutilation, duty then being charged as if so imported.'],
          'No duty on what is stolen, lost or abandoned in time.',
          'Total loss of 500 tonnes in port custody is remission, not pilferage.'),
        C('c4', T4, [
            'Section 25(1) lets the Central Government exempt goods generally by notification, absolutely or on conditions. A conditional exemption lapses on 31 March falling immediately after two years from grant or variation, except for trade agreements, international obligations, FTP schemes, re-imports, temporary imports, gifts, baggage and similar listed cases.',
            'Section 25(2) allows special exemptions by order in exceptional cases; section 25(6) waives duty of ₹100 or less. A notification takes effect when issued for publication in the Gazette; courts have stressed actual publication. Clarifications under section 25(2A) within one year apply retrospectively.',
            'Sections 25A and 25B enable exemption for goods imported for processing and re-exported within one year, or exported for processing and re-imported within one year, if identifiable. The claimant proves eligibility; eligibility is read strictly, and once eligible, the benefit is read liberally (Wood Papers). The importer may choose the more beneficial notification.'],
          'Exemptions suspend collection; they do not erase the levy.',
          'A conditional exemption granted in June 2025 lapses on 31 March 2028 unless extended.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Damage claim at port', 'role': 'Customs broker',
             'situation': 'A consignment is found damaged before examination.',
             'steps': ['Record damage before examination.', 'Get surveyor report.', 'Apply for abatement under section 22.', 'Pay proportionate duty.'],
             'takeaway': 'Timing of the damage decides relief.'}]

    mcqs = [
        Q('m1', 'Indian customs waters extend up to:', ['The limit of the exclusive economic zone', 'Twelve nautical miles', 'Twenty-four nautical miles', 'The baseline'], 0,
          'Section 2(28). In practice: 200 nautical miles.', 'c1', T1),
        Q('m2', 'For warehoused goods, the taxable event occurs when:', ['Goods are cleared from the warehouse', 'Goods enter territorial waters', 'The vessel docks', 'The bill of lading is issued'], 0,
          'Apar Ltd. In practice: rate at ex-bond date.', 'c1', T1),
        Q('m3', 'Rate for goods entered for home consumption is the rate on:', ['Later of bill of entry date and entry inwards', 'Date of loading abroad', 'Date of payment only', 'Date of invoice'], 0,
          'Section 15(1)(a). In practice: prior entry allowed.', 'c2', T2),
        Q('m4', 'Section 13 relief applies to goods pilfered:', ['After unloading and before the clearance or warehousing order', 'Before unloading', 'After clearance', 'From a warehouse'], 0,
          'Section 13. In practice: custodian pays.', 'c3', T3),
        Q('m5', 'Abandonment of goods is barred when:', ['An offence appears to have been committed', 'Goods are damaged', 'Goods are perishable', 'Duty exceeds one lakh'], 0,
          'Section 23(2). In practice: before order.', 'c3', T3),
        Q('m6', 'Duty is not collected when the amount is:', ['One hundred rupees or less', 'Five hundred rupees or less', 'One thousand rupees or less', 'Fifty rupees or less'], 0,
          'Section 25(6). In practice: minor amounts.', 'c4', T4),
        Q('m7', 'A conditional exemption under section 25(1) ordinarily lapses on:', ['End of March falling right after two years from grant', 'One year from grant', 'Five years from grant', 'Never'], 0,
          'Sunset clause. In practice: listed exceptions.', 'c4', T4),
        Q('m8', 'Under section 25A, goods must be re-exported within:', ['One year from the clearance order', 'Six months', 'Three years', 'Two years'], 0,
          'Inward processing. In practice: identifiable.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Duty before damage', 1, 'computation', '20%', nums=[d0]), S('s2', 'Abated duty', 3, 'computation', 'proportion', nums=[d1])],
          ['Confirm damage timing.'], ['Deducting damage from duty directly.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Home consumption lot', 2, 'analysis', '9 July'), S('s2', 'Warehoused lot', 2, 'analysis', '20 November')],
          ['Cite section 15.'], ['Using bill of entry date alone.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Who pays duty on pilfered goods?', 'The custodian approved under section 45 bears the duty; the importer is free unless the goods are restored.',
          [P('p1', 'Custodian', 5, 'custodian'), P('p2', 'Restored', 5, 'restored')], 'c3'),
        V('v2', 'How does section 23 differ from section 13?', 'Section 23 covers total loss or destruction, including warehoused goods, proven by the importer; section 13 covers petty theft after unloading.',
          [P('p1', 'Total loss', 5, 'total loss'), P('p2', 'Petty theft', 5, 'petty theft')], 'c3'),
        V('v3', 'What is denaturing?', 'Treating multi-use goods so they become unfit for some uses, after which duty applies as if imported in that form.',
          [P('p1', 'Unfit', 5, 'unfit'), P('p2', 'Multi-use', 5, 'multi-use')], 'c3'),
        V('v4', 'Who bears the burden of proving exemption eligibility?', 'The person claiming the exemption.',
          [P('p1', 'Claiming', 5, 'claiming'), P('p2', 'Person', 5, 'person')], 'c4'),
        V('v5', 'Are Government imports duty-free by default?', 'Section 12(2) applies duty equally to Government goods; relief comes only through specific notifications.',
          [P('p1', 'Section 12(2)', 5, '12(2)'), P('p2', 'Specific notifications', 5, 'specific notification')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Short delivery at the docks', 'difficulty': 'core',
              'case': 'Of 4,000 tonnes of coal imported, 300 tonnes went missing from port custody before clearance; no sign of package tampering.',
              'mcqs': [
                  M('k1a', 'Is this pilferage under section 13?', ['No, it is a large loss, not petty theft', 'Yes', 'Only if insured', 'Only for bulk cargo'], 0,
                    'Pilfer means petty theft. In practice: section 23.', 'core', topic=T3),
                  M('k1b', 'Relief is available under:', ['Section 23(1)', 'Section 22', 'Section 20', 'Section 25'], 0,
                    'Remission for loss. In practice: before clearance.', 'core', topic=T3),
                  M('k1c', 'Who must prove the loss?', ['The importer', 'The custodian', 'The shipping line', 'The Board'], 0,
                    'To the AC/DC. In practice: weighment certificate.', 'core', topic=T3),
                  M('k1d', 'If duty was already paid, the importer gets:', ['A refund after remission', 'Nothing', 'Credit for next import', 'Interest only'], 0,
                    'Refund follows remission. In practice: apply promptly.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ii-ch01', 1, 'Levy of and Exemptions from Customs Duty',
                ['Identify the taxable event for imports and exports.',
                 'Determine the relevant date for rate of duty.',
                 'Apply pilferage, abatement, remission and abandonment.',
                 'Apply exemption provisions and their interpretation.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ch24-u01'],
                 'exam_tip': 'For loss questions, first fix when and how the loss occurred: pilferage, damage or total loss.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 12 charge on goods; Government goods included.', 'Section 15: later of BoE or entry inwards; ex-warehouse BoE date.', 'Section 13 pilferage; 22 abatement; 23 remission and abandonment.',
                             'Section 25 exemptions with two-year sunset for conditional ones.', 'Sections 25A/25B processing within one year.'],
                 'remember': ['Duty of ₹100 or less is not collected.'],
                 'traps': ['Applying section 13 to warehoused goods.']},
                [('Charge', 'Section 12'), ('Rate date', 'Section 15'), ('Pilferage', 'Section 13'), ('Abatement', 'Section 22'), ('Exemption', 'Section 25')],
                viva, cases)
