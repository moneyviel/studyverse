"""CA Final · Paper 5 · Part II Customs · Chapter 2 Types of Duty.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ii-ch02-u01'
T1 = 'Basic customs duty, IGST and surcharges'
T2 = 'Safeguard measures and emergency powers'
T3 = 'Countervailing and anti-dumping duties'
T4 = 'Computing total import duty'


def build():
    ck = Checks()
    bcd = ck.add('1000000*0.10', 'Basic customs duty at 10% (₹)')
    sws = ck.add('1000000*0.10*0.10', 'Social welfare surcharge at 10% of BCD (₹)')
    add = ck.add('min(600-500,70)*1000', 'Anti-dumping duty: lower of dumping margin and injury margin × units (₹)')
    base = ck.add('1000000+1000000*0.10+1000000*0.10*0.10+min(600-500,70)*1000', 'Value for IGST including BCD, SWS and ADD (₹)')
    igst = ck.add('(1000000+1000000*0.10+1000000*0.10*0.10+min(600-500,70)*1000)*0.18', 'IGST at 18% (₹)')
    tot = ck.add('1000000*0.10+1000000*0.10*0.10+min(600-500,70)*1000+(1000000+1000000*0.10+1000000*0.10*0.10+min(600-500,70)*1000)*0.18', 'Total customs duty and tax (₹)')
    i1 = {'id': 'i1', 'title': 'Total duty with anti-dumping duty', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Orbit Glassware imports 1,000 units with assessable value ₹10,00,000. BCD is 10%, SWS 10%, IGST 18%. The export price is ₹500 per unit against a normal value of ₹600; the injury margin is ₹70 per unit. Compute total duty and IGST.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['BCD', '10% of 10,00,000', inr(bcd)],
              ['SWS', '10% of BCD', inr(sws)],
              ['ADD', 'Lower of ₹100 and ₹70 × 1,000', inr(add)],
              ['Value for IGST', 'AV + BCD + SWS + ADD', inr(base)],
              ['IGST', '18%', inr(igst)],
              ['Total', 'BCD + SWS + ADD + IGST', inr(tot)]], title='Customs Tariff Act')],
          'checks': list(ck)}

    c2 = Checks()
    s1 = c2.add('2.5', 'Share of imports from country A (%)')
    s2 = c2.add('2.5+2.8+3.6', 'Combined share of countries each below 3% (%)')
    i2 = {'id': 'i2', 'title': 'Developing-country exclusion from safeguard duty', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Safeguard duty is imposed on an article. Notified developing countries A, B and C supply 2.5%, 2.8% and 3.6% of India\'s imports respectively. Which countries are excluded?',
          'solution': [table(['Test', 'Rule', 'Result'], [
              ['Individual share', 'Each below 3%', 'A and B qualify; C does not'],
              ['Aggregate of below-3% countries', 'A + B = 5.3%, within 9%', 'A and B excluded'],
              ['Country C', 'Share above 3%', 'Duty applies']], title='Section 8B proviso')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'BCD is levied under section 12 of the Customs Act at rates in the First Schedule (imports, 8-digit, HSN-aligned) or Second Schedule (exports, a short list). Preferential rates apply to imports from notified areas if the importer claims them and proves origin under rules of origin; otherwise the standard rate applies.',
            'IGST under section 3(7) of the Customs Tariff Act applies at the rate on like goods supplied in India (cap 40%), on assessable value plus BCD and other customs duties, excluding IGST itself. GST compensation cess under section 3(9) has been phased out. For warehoused goods sold before clearance, IGST value is the higher of that value and the last transaction value.',
            'Social welfare surcharge is 10% of aggregate customs duties, excluding safeguard duty, CVD, anti-dumping duty and SWS itself; IGST is exempt from SWS. AIDC is levied on specified goods at notified rates. Additional duty under section 3(1) now matters mainly for petroleum and tobacco.'],
          'Layers of duty, each with its own base.',
          'SWS on BCD of ₹1,00,000 is ₹10,000.'),
        C('c2', T2, [
            'Sections 8 and 8A give emergency power to raise export or import duty by notification. Section 8B lets the Government impose safeguard measures — duty, tariff-rate quota or other measures — where increased imports cause or threaten serious injury to the domestic industry.',
            'Safeguard measures last up to 4 years, extendable while the industry adjusts, but not beyond 10 years in total. A provisional measure may last up to 200 days. Tariff-rate quotas ordinarily keep imports at least at the average of the last three representative years.',
            'Exclusions: a developing country with import share not exceeding 3%, provided such countries together do not exceed 9%. Imports by EOU/SEZ units are excluded unless cleared into DTA, when duty applies on the portion cleared.'],
          'Safeguards protect against surges, regardless of fairness of trade.',
          'A sudden import surge of solar glass can trigger a safeguard duty.'),
        C('c3', T3, [
            'Section 9 allows countervailing duty on subsidised imports, capped at the subsidy amount; section 9A allows anti-dumping duty, capped at the margin of dumping (normal value less export price) and in practice the lower of dumping margin and injury margin. Both apply irrespective of other duties and may be provisional.',
            'Both duties last 5 years unless revoked, extendable by up to 5 years on review. Retrospective levy is possible in case of massive dumping or subsidisation causing hard-to-repair injury, but not beyond 90 days before the provisional duty notification.',
            'Section 9B: the same article cannot bear both CVD and ADD for the same situation; no levy merely because of exemption from domestic taxes on exports; provisional duties are restricted for WTO members unless injury is found. Appeals lie to the CESTAT Special Bench within 90 days under section 9C with a fee of ₹15,000.'],
          'Unfair trade remedies need proof of subsidy or dumping plus injury.',
          'An exporter selling at ₹500 when home price is ₹600 is dumping by ₹100.'),
        C('c4', T4, [
            'Sequence for computing duty: assessable value; BCD on assessable value; SWS on BCD (and other duties in its base); safeguard, CVD or ADD as applicable; IGST on assessable value plus all customs duties.',
            'ADD, CVD and safeguard duty enter the IGST base but stay out of the SWS base.',
            'Registered importers may take ITC of IGST paid on imports; BCD, SWS and ADD are costs.'],
          'Order of computation matters.',
          'Importer\'s ITC covers IGST but not BCD.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Landed cost sheet', 'role': 'Import costing analyst',
             'situation': 'Procurement asks for landed cost of a dumped item.',
             'steps': ['Fix assessable value.', 'Apply BCD and SWS.', 'Add ADD per notification.', 'Compute IGST and identify credit.'],
             'takeaway': 'ADD can change sourcing decisions.'}]

    mcqs = [
        Q('m1', 'SWS is excluded from being charged on:', ['Anti-dumping duty', 'Basic customs duty', 'Additional duty under section 3(1)', 'All customs duties'], 0,
          'Excluded list. In practice: also CVD, safeguard.', 'c1', T1),
        Q('m2', 'IGST on imports is computed on:', ['Assessable value plus customs duties', 'Assessable value only', 'BCD only', 'Invoice value only'], 0,
          'Section 3(8). In practice: excludes IGST.', 'c1', T1),
        Q('m3', 'Maximum total duration of safeguard measures is:', ['Ten years', 'Four years', 'Five years', 'Eight years'], 0,
          'Section 8B. In practice: initial four years.', 'c2', T2),
        Q('m4', 'Developing-country exclusion requires individual import share not above:', ['Three percent', 'Five percent', 'Nine percent', 'One percent'], 0,
          'Aggregate cap nine percent. In practice: notified countries.', 'c2', T2),
        Q('m5', 'Anti-dumping duty cannot exceed:', ['Margin of dumping', 'Injury margin plus ten percent', 'Normal value', 'Export price'], 0,
          'Section 9A(1). In practice: lesser duty.', 'c3', T3),
        Q('m6', 'Duration of anti-dumping duty unless revoked:', ['Five years', 'Four years', 'Ten years', 'Three years'], 0,
          'Extendable up to five years. In practice: sunset review.', 'c3', T3),
        Q('m7', 'Appeal against anti-dumping determination lies to:', ['CESTAT', 'High Court', 'Commissioner (Appeals)', 'Designated Authority'], 0,
          'Section 9C. In practice: within 90 days.', 'c3', T3),
        Q('m8', 'Can CVD and ADD both apply to the same article to cover the same situation?', ['No', 'Yes', 'Only for EOU', 'Only provisionally'], 0,
          'Section 9B. In practice: one remedy.', 'c3', T3),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'BCD and SWS', 2, 'computation', 'BCD', nums=[bcd, sws]), S('s2', 'ADD', 2, 'computation', 'injury margin', nums=[add]), S('s3', 'IGST and total', 4, 'computation', '18%', nums=[base, igst, tot])],
          ['Keep ADD out of SWS base.'], ['Charging SWS on ADD.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Individual test', 2, 'analysis', '3%', nums=[s1]), S('s2', 'Aggregate test', 2, 'computation', '9%')],
          ['Apply both tests.'], ['Adding C into aggregate.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is dumping?', 'Export of an article to India at a price below its normal value in the exporting country.',
          [P('p1', 'Normal value', 5, 'normal value'), P('p2', 'Export price', 5, 'price')], 'c3'),
        V('v2', 'What is a tariff-rate quota?', 'A safeguard measure allowing a quantity at lower duty with higher duty beyond it.',
          [P('p1', 'Quantity', 5, 'quantity'), P('p2', 'Higher duty', 5, 'higher duty')], 'c2'),
        V('v3', 'How far back can anti-dumping duty be imposed?', 'Up to 90 days before the provisional duty notification, in case of massive dumping.',
          [P('p1', 'Ninety days', 5, '90 days'), P('p2', 'Provisional', 5, 'provisional')], 'c3'),
        V('v4', 'When does a preferential rate apply?', 'When the importer claims it and proves origin from a notified preferential area under origin rules.',
          [P('p1', 'Origin', 5, 'origin'), P('p2', 'Notified area', 5, 'notified')], 'c1'),
        V('v5', 'Is IGST on imports creditable?', 'Yes, a registered importer can take ITC of IGST paid on imports used in business.',
          [P('p1', 'ITC', 5, 'itc'), P('p2', 'Registered', 5, 'registered')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Subsidised steel imports', 'difficulty': 'moderate',
              'case': 'An exporting government pays a subsidy of ₹40 per kg on steel exported to India; Indian producers suffer injury.',
              'mcqs': [
                  M('k1a', 'The remedy is:', ['Countervailing duty under section 9', 'Safeguard duty', 'Export duty', 'AIDC'], 0,
                    'Subsidy remedy. In practice: DGTR inquiry.', 'moderate', topic=T3),
                  M('k1b', 'Maximum CVD per kg (₹):', ['40', '80', '20', '60'], 0,
                    'Capped at subsidy. In practice: lesser if adequate.', 'moderate', check=40, topic=T3),
                  M('k1c', 'Can ADD also be levied for the same situation?', ['No', 'Yes', 'Only on EOU', 'Only retrospectively'], 0,
                    'Section 9B. In practice: avoid double remedy.', 'moderate', topic=T3),
                  M('k1d', 'Is CVD included in the SWS base?', ['No', 'Yes', 'Half of it', 'Only for steel'], 0,
                    'Excluded. In practice: included in IGST base.', 'moderate', topic=T1),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ii-ch02', 1, 'Types of Duty',
                ['Explain BCD, IGST, SWS and AIDC on imports.',
                 'Apply safeguard measures and emergency powers.',
                 'Apply countervailing and anti-dumping duties.',
                 'Compute total customs duty on imports.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 30}, 'prereq': ['fin-p5-ii-ch01-u01'],
                 'exam_tip': 'Keep two bases separate: SWS excludes trade-remedy duties; the IGST base includes them.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['BCD under section 12; preferential rate needs origin proof.', 'IGST on AV + duties; cap 40%.', 'SWS 10%; excludes safeguard, CVD, ADD.',
                             'Safeguard 4 years, max 10; developing country 3%/9%.', 'CVD/ADD 5 + 5 years; appeal CESTAT 90 days.'],
                 'remember': ['ADD = lower of dumping margin and injury margin.'],
                 'traps': ['Charging SWS on IGST.']},
                [('BCD', 'Section 12'), ('IGST', 'Section 3(7) CTA'), ('Safeguard', 'Section 8B'), ('CVD', 'Section 9'), ('ADD', 'Section 9A')],
                viva, cases)
