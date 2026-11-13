"""CA Final · Paper 5 · Part II Customs · Chapter 6 Warehousing.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ii-ch06-u01'
T1 = 'Types of warehouses, licensing and bond'
T2 = 'Warehousing period and interest'
T3 = 'Owner\'s rights and manufacture in a warehouse'
T4 = 'Removal, improper removal and relinquishment'


def build():
    ck = Checks()
    bond = ck.add('200000*3', 'Warehousing bond at thrice the assessed duty (₹)')
    days = ck.add('1+30+31+11', 'Days from 31 August to 11 November (interest period)')
    intr = ck.add('200000*0.15*73/365', 'Interest at 15% p.a. on duty for 73 days (₹)')
    i1 = {'id': 'i1', 'title': 'Interest on warehoused goods', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Polaris Electronics warehoused imported goods in a public warehouse; the order under section 60 was made on 1 June. The goods were cleared for home consumption on 11 November, paying duty of ₹2,00,000. Compute the bond amount and the interest payable. Treat the 90-day interest-free period as ending on 30 August.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Bond', 'Thrice the duty assessed', f'₹{inr(bond)}'],
              ['Interest-free period', '90 days from the section 60 order', 'Up to 30 August'],
              ['Interest days', '31 August to 11 November', f'{inr(days)} days'],
              ['Interest', '₹2,00,000 × 15% × 73/365', f'₹{inr(intr)}']], title='Sections 59 and 61')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Goods left after the permitted period', 'difficulty': 'hard', 'minutes': 6,
          'q': 'Goods warehoused on 10 March of year 1 (no extension) remained in the warehouse. The duty rate was 12% up to 31 March of year 2 and 15% thereafter. A demand was issued in June of year 2. Which rate applies?',
          'solution': [table(['Point', 'Rule', 'Result'], [
              ['Permitted period', 'One year from the section 60 order', 'Ends 10 March of year 2'],
              ['Status after expiry', 'Deemed improper removal under section 72 (Kesoram Rayon)', 'Removal on 10 March of year 2'],
              ['Rate', 'Rate on date of deemed removal; demand date irrelevant', '12%']], title='Section 72')]}

    concepts = [
        C('c1', T1, [
            'Warehousing lets importers defer duty by keeping goods in a customs bonded warehouse. Public warehouses (section 57) store anyone\'s goods; private warehouses (section 58) store only the licensee\'s goods; special warehouses (section 58A) are under customs lock and hold goods like gold, ship stores and duty-free shop goods.',
            'Licences are not renewed annually, are not transferable, and last until cancellation or surrender. Under section 58B the Commissioner may cancel a licence for contravention after a hearing; goods must then be moved within 7 days of service of the order or as allowed.',
            'Section 59: the importer files an into-bond bill of entry and executes a bond for thrice the assessed duty, undertaking to pay duty, interest and penalties. A consignment-wise or general bond may be executed; the bond continues on transfer, and a transferee executes a fresh bond.'],
          'Defer duty by keeping goods under bond.',
          'A trader can store imported machines in a public warehouse and pay duty on sale.'),
        C('c2', T2, [
            'Section 61: goods may stay until ex-bonding or consumption (capital goods until ex-bonding) in warehouses with section 65 permission; in other cases, one year from the section 60 order, extendable by the Commissioner by up to one year at a time. Perishable goods may get a shorter period.',
            'Interest at 15% p.a. is charged in other cases on duty deferred beyond 90 days from the section 60 order, till payment. No interest arises in section 65 warehouses. The Board may waive interest or notify goods on which interest runs from day one.',
            'Interest follows duty: if no duty is payable on clearance (e.g. goods re-exported or exempt), no interest is payable (Pratibha Processors).'],
          'Ninety days free, then fifteen percent a year.',
          'Goods re-exported from a warehouse after six months pay no interest.'),
        C('c3', T3, [
            'Section 64 lets the owner inspect, deal with containers to prevent loss or damage, sort, and show the goods for sale.',
            'Section 65 permits manufacturing and other operations in a warehouse with permission. Duty on imported inputs is payable only when resulting goods are cleared for home consumption; no duty on exports. Waste or refuse from operations is either destroyed or charged as if imported in that form; remission is allowed for waste linked to exported products when destroyed.',
            'Since 2016, EOUs, EHTPs and STPs are no longer licensed warehouses and section 65 does not apply to them, though clearances still need approval and duty.'],
          'Process goods under bond and pay only for domestic clearances.',
          'Imported steel strips turned into knives for export bear no duty.'),
        C('c4', T4, [
            'Warehoused goods may be moved to another warehouse (section 67), cleared for home consumption on payment of duty, interest and charges with an ex-bond bill of entry (section 68), or exported without import duty (section 69), e.g. ship stores and duty-free supplies.',
            'Before an order for home clearance, the owner may relinquish title on paying penalties, escaping duty, unless an offence appears to have been committed. Section 71 bars removal except as provided.',
            'Section 72 lets the officer demand full duty, interest and penalties where goods are removed in contravention, not removed after the permitted period, not accounted for, or taken out improperly; the rate is the rate on the date of deemed removal. Section 73 cancels the bond once obligations are met, and section 73A places custody with the warehouse keeper.'],
          'Three exits: transfer, home clearance or export.',
          'Missing goods found at stock-taking face demand under section 72.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Warehouse ageing review', 'role': 'Supply chain finance analyst',
             'situation': 'Bonded stock includes items near the end of the one-year period.',
             'steps': ['List goods by section 60 order date.', 'Estimate interest beyond 90 days.', 'Seek extension or plan clearance.', 'Consider re-export for slow movers.'],
             'takeaway': 'Expiry triggers deemed removal at that date\'s rate.'}]

    mcqs = [
        Q('m1', 'Goods of only the licensee can be stored in a:', ['Private warehouse', 'Public warehouse', 'Special warehouse', 'Any warehouse'], 0,
          'Section 58. In practice: own imports.', 'c1', T1),
        Q('m2', 'Warehousing bond is ordinarily for:', ['Thrice the duty assessed', 'Twice the duty', 'Equal to duty', 'Half the duty'], 0,
          'Section 59. In practice: plus security.', 'c1', T1),
        Q('m3', 'Interest on warehoused goods (other cases) starts after:', ['Ninety days from the section 60 order', 'Thirty days', 'One year', 'Arrival of vessel'], 0,
          'Section 61(2). In practice: 15%.', 'c2', T2),
        Q('m4', 'Rate of interest on deferred duty is:', ['Fifteen percent per annum', 'Eighteen percent', 'Twelve percent', 'Nine percent'], 0,
          'Section 47 notification. In practice: simple.', 'c2', T2),
        Q('m5', 'Warehousing period in ordinary cases is:', ['One year, extendable a year at a time', 'Six months', 'Three years', 'Until ex-bonding'], 0,
          'Section 61(1)(b). In practice: perishables shorter.', 'c2', T2),
        Q('m6', 'Waste arising in section 65 operations is:', ['Destroyed or charged as imported in that form', 'Always duty-free', 'Always fully dutiable at input value', 'Ignored'], 0,
          'Section 65(2). In practice: destruction.', 'c3', T3),
        Q('m7', 'Goods not removed after the permitted period are:', ['Deemed improperly removed', 'Confiscated automatically', 'Exempt', 'Auctioned free'], 0,
          'Section 72. In practice: Kesoram Rayon.', 'c4', T4),
        Q('m8', 'If goods are re-exported from the warehouse, interest is:', ['Nil because no duty is payable', '15% for full period', 'Payable at half rate', 'Payable only on bond'], 0,
          'Pratibha Processors. In practice: accessory.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Bond', 1, 'computation', 'thrice', nums=[bond]), S('s2', 'Interest period', 2, 'computation', '90 days', nums=[days]), S('s3', 'Interest', 2, 'computation', '15%', nums=[intr])],
          ['Show the day count.'], ['Charging interest from day one.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Deemed removal', 2, 'analysis', 'section 72'), S('s2', 'Rate', 2, 'analysis', '12%')],
          ['Cite Kesoram Rayon.'], ['Applying rate on demand date.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What may a warehouse owner do with warehoused goods?', 'Inspect, sort, deal with containers to prevent damage, and show them for sale.',
          [P('p1', 'Inspect', 5, 'inspect'), P('p2', 'Sort', 5, 'sort')], 'c3'),
        V('v2', 'When can a licence be cancelled?', 'When the licensee contravenes the Act or licence conditions, after a hearing by the Commissioner.',
          [P('p1', 'Contravenes', 5, 'contravene'), P('p2', 'Hearing', 5, 'hearing')], 'c1'),
        V('v3', 'Who has custody of warehoused goods?', 'The warehouse keeper under section 73A.',
          [P('p1', 'Warehouse keeper', 5, 'warehouse keeper'), P('p2', '73A', 5, '73a')], 'c4'),
        V('v4', 'What goods typically go to special warehouses?', 'High-value or sensitive goods like gold and duty-free or ship stores, kept under customs lock.',
          [P('p1', 'Customs lock', 5, 'customs lock'), P('p2', 'Gold', 5, 'gold')], 'c1'),
        V('v5', 'Can the owner relinquish warehoused goods?', 'Yes, before the home-clearance order, on paying penalties, unless an offence appears committed.',
          [P('p1', 'Penalties', 5, 'penalties'), P('p2', 'Before order', 5, 'before')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Processing in bond', 'difficulty': 'moderate',
              'case': 'Arya Tools manufactures cutlery in a section 65 warehouse from imported steel. 80% of output is exported; 20% is sold in India.',
              'mcqs': [
                  M('k1a', 'Import duty on steel used in exported cutlery:', ['Nil', 'Full', 'Half', 'At export duty rate'], 0,
                    'Section 65. In practice: exports duty-free.', 'moderate', topic=T3),
                  M('k1b', 'On domestic sales, duty is paid on:', ['Imported inputs used in them', 'Nothing', 'The whole output value', 'Only waste'], 0,
                    'Clearance for home use. In practice: input-based.', 'moderate', topic=T3),
                  M('k1c', 'Interest on deferred duty in this warehouse:', ['Not chargeable', '15% after 90 days', '18%', 'From day one'], 0,
                    'Section 61(2) excludes section 65 units. In practice: none.', 'moderate', topic=T2),
                  M('k1d', 'Warehousing period for non-capital goods here is:', ['Until ex-bonding or consumption', 'One year', 'Two years', 'Ninety days'], 0,
                    'Section 61(1)(a). In practice: open-ended.', 'moderate', topic=T2),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ii-ch06', 1, 'Warehousing',
                ['Distinguish types of warehouses and licensing rules.',
                 'Apply warehousing period and interest provisions.',
                 'Apply owner\'s rights and manufacture in a warehouse.',
                 'Apply removal, improper removal and relinquishment rules.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p5-ii-ch05-u01'],
                 'exam_tip': 'Start every warehousing question by fixing the date of the section 60 order.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Public, private, special warehouses.', 'Bond thrice the duty.', 'Period one year (+1 year at a time); section 65 till ex-bond.',
                             'Interest 15% after 90 days; nil if no duty.', 'Section 72 deemed removal at that date\'s rate.'],
                 'remember': ['Licence cancellation: goods out within 7 days.'],
                 'traps': ['Applying section 15 rate for goods kept beyond period.']},
                [('Licensing', 'Sections 57–58B'), ('Bond', 'Section 59'), ('Period', 'Section 61'), ('Manufacture', 'Section 65'), ('Improper removal', 'Section 72')],
                viva, cases)
