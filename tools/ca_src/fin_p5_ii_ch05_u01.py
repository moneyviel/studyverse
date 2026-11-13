"""CA Final · Paper 5 · Part II Customs · Chapter 5 Importation and Exportation of Goods.
Built from the Customs Act, 1962, the Bill of Entry (Electronic Integrated Declaration and Paperless Processing) Regulations, 2018 and the Baggage Rules, 2026 (Notification 14/2026-Cus (NT)); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ii-ch05-u01'
T1 = 'Arrival of conveyances and manifests'
T2 = 'Bill of entry, assessment and clearance'
T3 = 'Export procedure, transit and transhipment'
T4 = 'Baggage'


def build():
    ck = Checks()
    lc1 = ck.add('3*5000+2*10000', 'Late charges for 5 days of default: ₹5,000 × 3 + ₹10,000 × 2 (₹)')
    lc2 = ck.add('min(3*5000+5*10000,50000)', 'Late charges for 8 days where no duty is payable, capped at ₹50,000 (₹)')
    intr = ck.add('730000*0.15*10/365', 'Interest at 15% p.a. on duty paid 10 days late (₹)')
    i1 = {'id': 'i1', 'title': 'Late bill of entry and late payment', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Tapti Polymers files a bill of entry 5 days after the due time without sufficient cause; duty payable is ₹7,30,000 (self-assessed). It pays the duty 10 days after presenting the bill of entry. A second consignment of exempt goods (no duty payable) is filed 8 days late. Compute late presentation charges for both and interest on the first.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Late charges — consignment 1', '₹5,000 × 3 days + ₹10,000 × 2 days (below duty payable)', inr(lc1)],
              ['Late charges — consignment 2', '₹15,000 + ₹10,000 × 5 = ₹65,000, capped at ₹50,000', inr(lc2)],
              ['Interest under section 47(2)', '₹7,30,000 × 15% × 10/365', inr(intr)]], title='Sections 46 and 47')],
          'checks': list(ck)}

    c2 = Checks()
    ex = c2.add('110000-75000', 'Value exceeding the general free allowance (₹)')
    dt = c2.add('(110000-75000)*0.35', 'Duty at 35% on the excess (₹)')
    i2 = {'id': 'i2', 'title': 'Baggage of a returning resident', 'difficulty': 'core', 'minutes': 6,
          'q': 'Ritika, an Indian resident aged 30, returns by air from Singapore after a 10-day holiday with a new laptop (₹90,000) and a smartwatch and perfumes worth ₹1,10,000 together. Compute duty on her baggage, assuming the baggage rate of 35% ad valorem and ignoring any surcharge.',
          'solution': [table(['Item', 'Rule', 'Result'], [
              ['Laptop', 'One new laptop duty-free for passengers aged 18+', 'Free'],
              ['General free allowance', 'Resident arriving by air: up to ₹75,000', '₹75,000'],
              ['Excess value', '₹1,10,000 − ₹75,000', f'₹{inr(ex)}'],
              ['Duty', '35% of excess', f'₹{inr(dt)}']], title='Baggage Rules, 2026')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 7 lets the Board appoint customs ports, airports, land customs stations, inland container depots, international courier terminals and foreign post offices. Under section 29, a conveyance from abroad must arrive only at such a customs port or airport unless forced elsewhere by accident, weather or similar compelling reasons.',
            'Section 30: the person in charge of a vessel or aircraft must deliver the arrival or import manifest electronically before arrival, and of a vehicle, the import report within 12 hours of arrival. If delivered late without sufficient cause, the person responsible faces a penalty of up to ₹50,000.',
            'Goods cannot be unloaded until entry inwards is granted (section 31) and only if listed in the manifest for that station (section 32). Unloaded goods remain with an approved custodian (section 45). Goods not cleared, warehoused or transhipped within 30 days of unloading (or extended time) may be sold by the custodian after notice to the importer (section 48).'],
          'Manifest first, unloading later.',
          'A container left uncleared beyond 30 days can be auctioned after notice.'),
        C('c2', T2, [
            'Section 46: the importer files a bill of entry for home consumption or warehousing, electronically, before the end of the day (including holidays) preceding the day of arrival of the conveyance; the Board may allow later filing in specified cases, but not beyond the end of the day of arrival. Advance filing is allowed up to 30 days before expected arrival. Late filing without sufficient cause attracts charges of ₹5,000 a day for the first 3 days and ₹10,000 a day thereafter, not exceeding the duty payable, and capped at ₹50,000 where no duty is payable.',
            'Section 17: the importer self-assesses duty; the proper officer may verify and reassess, and must pass a speaking order within 15 days if the importer does not accept the reassessment. Section 18 allows provisional assessment against security or bond where testing or documents are pending, with final assessment later.',
            'Section 47(2): duty must be paid on the date of presenting a self-assessed bill of entry, or within one day (excluding holidays) of its return after assessment or reassessment; otherwise interest (currently 15% a year) runs till payment. Notified importers may pay on a deferred basis. On payment and checks, the officer issues an out-of-charge order for home consumption.'],
          'File early, pay the same day.',
          'A bill of entry filed the day after arrival is already late under the current rule.'),
        C('c3', T3, [
            'Exports need a shipping bill (by vessel or aircraft) or bill of export (by vehicle) under section 50, with a declaration of truth and documents. The exporter self-assesses export duty, if any. After assessment and examination, the proper officer gives a let export order under section 51, after which goods may be loaded.',
            'Section 53 — transit: goods shown in the manifest as for transit in the same conveyance to a place outside India or to another customs station may pass without payment of duty, subject to rules.',
            'Section 54 — transhipment: goods brought in for transhipment to another conveyance are allowed without duty on a bill of transhipment, when bound for a place outside India (or, under conditions, for another customs station in India).'],
          'Let export order is the green light to load.',
          'Goods arriving at Mumbai on a ship bound for Colombo pass in transit without duty.'),
        C('c4', T4, [
            'Baggage is governed by sections 77 to 81 and the Baggage Rules, 2026, in force from 2 February 2026. All passengers, including infants, may clear used personal effects and travel souvenirs duty-free. General free allowance (arrival other than by land, not for infants): ₹75,000 for residents, tourists of Indian origin and foreigners on non-tourist visas; ₹25,000 for tourists of foreign origin. Land arrivals get only used personal effects. Allowances cannot be pooled.',
            'Passengers aged 18 or more (other than crew) may bring one new laptop or notepad duty-free in addition. A resident or tourist of Indian origin who has lived abroad for over one year may bring jewellery up to 40 grams (female) or 20 grams (others) duty-free.',
            'Transfer of residence for residents and tourists of Indian origin allows household and personal articles up to ₹1.5 lakh (3–12 months abroad), ₹3 lakh (at least one year in the preceding two years) or ₹7.5 lakh (at least two years abroad), with conditions. Unaccompanied baggage may arrive up to two months before the passenger (or one year where reasons are recorded). Goods beyond allowances attract duty at 35% ad valorem on the excess.'],
          'Allowances rose sharply in 2026.',
          'A resident bringing ₹70,000 of gifts by air pays no duty.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Import clearance planner', 'role': 'Customs broker',
             'situation': 'A client\'s vessel arrives on Thursday.',
             'steps': ['File the bill of entry by end of Wednesday.', 'Self-assess and pay duty the same day.', 'Track reassessment and reply within time.', 'Clear goods well before 30 days.'],
             'takeaway': 'Advance filing avoids late charges and demurrage.'}]

    mcqs = [
        Q('m1', 'Bill of entry must ordinarily be filed:', ['Before the end of the day preceding the day of arrival', 'Within 30 days of arrival', 'Within 7 days of unloading', 'Only after entry inwards'], 0,
          'Section 46(3). In practice: advance filing.', 'c2', T2),
        Q('m2', 'Late presentation charge for the first three days of default is:', ['Five thousand rupees per day', 'Ten thousand rupees per day', 'One thousand rupees per day', 'Fifty thousand rupees flat'], 0,
          'Regulation 4. In practice: then ten thousand.', 'c2', T2),
        Q('m3', 'Self-assessed duty must be paid:', ['On the date the bill of entry is presented', 'Within 5 days', 'Within 15 days', 'At the end of the month'], 0,
          'Section 47(2)(a). In practice: interest otherwise.', 'c2', T2),
        Q('m4', 'Uncleared goods may be sold by the custodian after:', ['Thirty days from unloading, after notice', 'Seven days from arrival', 'One year', 'Ninety days'], 0,
          'Section 48. In practice: extension possible.', 'c1', T1),
        Q('m5', 'Penalty for delay in delivering the import manifest can extend to:', ['Fifty thousand rupees', 'One lakh rupees', 'Ten thousand rupees', 'Five lakh rupees'], 0,
          'Section 30(1). In practice: no sufficient cause.', 'c1', T1),
        Q('m6', 'Loading of export goods is allowed after:', ['The let export order', 'Filing the shipping bill only', 'Payment of IGST', 'Arrival of vessel'], 0,
          'Section 51. In practice: out of charge.', 'c3', T3),
        Q('m7', 'General free allowance for a tourist of foreign origin arriving by air is:', ['Twenty-five thousand rupees', 'Seventy-five thousand rupees', 'Fifty thousand rupees', 'Fifteen thousand rupees'], 0,
          'Baggage Rules 2026. In practice: not pooled.', 'c4', T4),
        Q('m8', 'Passengers arriving by land get:', ['Only used personal effects duty-free', 'Seventy-five thousand rupees allowance', 'Twenty-five thousand rupees allowance', 'No baggage relief at all'], 0,
          'Rule 5. In practice: land borders.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Late charges with duty', 2, 'computation', '5,000', nums=[lc1]), S('s2', 'Cap where no duty', 2, 'computation', '50,000', nums=[lc2]), S('s3', 'Interest', 2, 'computation', '15%', nums=[intr])],
          ['State caps.'], ['Charging ₹10,000 from day one.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Laptop', 1, 'analysis', 'laptop'), S('s2', 'Excess and duty', 3, 'computation', '75,000', nums=[ex, dt])],
          ['Mention rule.'], ['Counting laptop in allowance.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What happens if the importer disputes a reassessment?', 'The proper officer must pass a speaking order within 15 days under section 17(5).',
          [P('p1', 'Speaking order', 5, 'speaking order'), P('p2', 'Fifteen days', 5, '15 days')], 'c2'),
        V('v2', 'When is provisional assessment used?', 'When documents or tests needed for final assessment are pending; the importer gives security or a bond under section 18.',
          [P('p1', 'Security', 5, 'security'), P('p2', 'Pending', 5, 'pending')], 'c2'),
        V('v3', 'What is the difference between transit and transhipment?', 'Transit goods stay on the same conveyance; transhipment goods move to another conveyance.',
          [P('p1', 'Same conveyance', 5, 'same conveyance'), P('p2', 'Another conveyance', 5, 'another conveyance')], 'c3'),
        V('v4', 'Who may bring duty-free jewellery under the 2026 rules?', 'A resident or tourist of Indian origin who has lived abroad for over one year, up to 40 grams for women and 20 grams for others.',
          [P('p1', 'Over one year', 5, 'over one year'), P('p2', 'Forty grams', 5, '40 grams')], 'c4'),
        V('v5', 'Can late presentation charges be waived?', 'Yes, the proper officer may waive them if satisfied that there was sufficient cause for delay.',
          [P('p1', 'Waive', 5, 'waive'), P('p2', 'Sufficient cause', 5, 'sufficient cause')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Family returning from Dubai', 'difficulty': 'core',
              'case': 'Aman (resident, 40), his wife Neha (resident, 36) and their son (1 year old) return by air after two years\' work in Dubai. They carry used clothes, a new laptop each for Aman and Neha, Neha\'s jewellery of 35 grams and Aman\'s of 18 grams, and household goods worth ₹6 lakh. They did not claim transfer-of-residence relief earlier.',
              'mcqs': [
                  M('k1a', 'Is Neha\'s jewellery duty-free?', ['Yes, within 40 grams', 'No', 'Only up to 20 grams', 'Only if under ₹1 lakh'], 0,
                    'Abroad over one year. In practice: female limit.', 'core', topic=T4),
                  M('k1b', 'Household goods of ₹6 lakh under transfer of residence are:', ['Within the ₹7.5 lakh limit', 'Fully dutiable', 'Within ₹3 lakh only', 'Barred'], 0,
                    'Two years abroad. In practice: conditions apply.', 'core', topic=T4),
                  M('k1c', 'The infant\'s general free allowance is:', ['Nil; only personal effects', 'Seventy-five thousand rupees', 'Twenty-five thousand rupees', 'Pooled with parents'], 0,
                    'Infants excluded. In practice: personal effects free.', 'core', topic=T4),
                  M('k1d', 'How many laptops may come in duty-free?', ['Two — one each for Aman and Neha', 'One for the family', 'Three including the infant', 'None'], 0,
                    'One per adult passenger. In practice: 18 or above.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ii-ch05', 1, 'Importation and Exportation of Goods',
                ['Apply provisions on arrival of conveyances and manifests.',
                 'Apply bill of entry, assessment, payment and clearance rules.',
                 'Apply export, transit and transhipment provisions.',
                 'Compute duty on baggage under the Baggage Rules, 2026.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ii-ch04-u01'],
                 'exam_tip': 'Track the timeline: manifest, bill of entry, assessment, payment, out of charge — each has its own deadline.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 30 manifest before arrival; penalty up to ₹50,000.', 'Section 46: BoE by end of day before arrival; late charges ₹5,000/₹10,000.', 'Section 47: pay same day (self-assessed); interest 15%.',
                             'Section 48: sale after 30 days; sections 50–51 export; 53–54 transit/transhipment.', 'Baggage Rules 2026: ₹75,000 / ₹25,000; laptop; jewellery 40g/20g.'],
                 'remember': ['Late charges capped at duty payable, or ₹50,000 where no duty.'],
                 'traps': ['Using the old ₹50,000 baggage allowance.']},
                [('Manifest', 'Section 30'), ('Bill of entry', 'Section 46'), ('Payment', 'Section 47'), ('Export', 'Sections 50–51'), ('Baggage', 'Rules 2026')],
                viva, cases)
