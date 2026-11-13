"""CA Intermediate · Paper 3B Goods and Services Tax · Chapter 1 GST in India – An Introduction.
Scope follows the ICAI syllabus; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-b-ch01-u01'
T1 = 'Why GST: the problems of the earlier indirect tax system'
T2 = 'Constitutional framework (101st Amendment)'
T3 = 'Dual GST: CGST, SGST/UTGST and IGST'
T4 = 'GST Council, GSTN and the rate structure'


def build():
    ck = Checks()
    cg = ck.add('50000*9/100', 'CGST at 9%')
    sg = ck.add('50000*9/100', 'SGST at 9%')
    ig = ck.add('50000*18/100', 'IGST at 18%')
    i1 = {'id': 'i1', 'title': 'Same sale, two routes', 'difficulty': 'core', 'minutes': 5,
          'q': 'Pune Paints sells goods worth ₹50,000 (18% rate) to (a) a registered dealer in Nagpur, Maharashtra and (b) a registered dealer in Indore, Madhya Pradesh. Which taxes apply and how much?',
          'solution': [table(['Sale', 'Nature', 'Tax', '₹'], [
              ['(a) Nagpur', 'Intra-State (both in Maharashtra)', 'CGST 9% + SGST 9%', inr(cg) + ' + ' + inr(sg)],
              ['(b) Indore', 'Inter-State', 'IGST 18%', inr(ig)]], title='Dual GST in action'),
              note('The total tax is the same; what changes is who collects it. IGST is collected by the Centre and later shared with the consuming State.')],
          'checks': list(ck)}

    ck2 = Checks()
    old = ck2.add('100000*10/100 + (100000+10000+20000)*12.5/100', 'Old system: excise on factory value, then VAT on value including excise and margin')
    i2 = {'id': 'i2', 'title': 'Tax on tax', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Under the pre-GST system a manufacturer paid excise duty at 10% on goods valued at ₹1,00,000, then a trader added a margin of ₹20,000 and paid VAT at 12.5% on the full price including excise; the trader could not set off the excise paid. Compute total tax and explain the cascading effect.',
          'solution': [table(['Stage', 'Working', '₹'], [
              ['Excise', '10% × 1,00,000', inr(10000)],
              ['VAT base', '1,00,000 + 10,000 excise + 20,000 margin', inr(130000)],
              ['VAT', '12.5% × 1,30,000', inr(16250)],
              ['Total tax', '', inr(old)]], title='Cascading before GST'),
              p('₹1,250 of the VAT (12.5% of ₹10,000) is tax on tax. Under GST the trader takes credit of tax paid by the manufacturer, so only value added at each stage is effectively taxed.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Before July 2017 the Centre levied excise duty on manufacture and service tax on services, and the States levied VAT on sale, entry tax, entertainment and luxury taxes. The Centre also levied CST on inter-State sales, which no one could set off.',
            'Problems: cascading (tax on tax) because central taxes were not creditable against State taxes; separate tax bases for goods and services; disputes over whether a transaction was a sale or a service; physical check-posts; and a fragmented national market.',
            'GST is a destination-based tax on consumption: tax follows the goods or services to the State where they are consumed, credit flows through the chain, and only the final consumer bears it.'],
          'GST replaced many toll gates on one road with a single, creditable toll.',
          'A trader in Surat can now take credit of IGST paid on goods bought from Chennai — impossible with CST.'),
        C('c2', T2, [
            'The Constitution (One Hundred and First Amendment) Act, 2016 gave both Parliament and State Legislatures power to make laws on GST (Article 246A), with Parliament alone legislating on inter-State supplies.',
            'Article 269A: IGST on inter-State supply (including imports) is levied and collected by the Centre and apportioned between Centre and States as recommended by the GST Council. Article 279A creates the GST Council.',
            'Article 366(12A): GST means any tax on supply of goods or services or both, except tax on alcoholic liquor for human consumption. Five petroleum products (crude, petrol, high-speed diesel, natural gas and aviation turbine fuel) are within GST in principle but taxed only from a date the Council recommends.',
            'Not subsumed: basic customs duty, stamp duty, electricity duty, State excise on alcohol and taxes on petroleum products until brought under GST.'],
          'The amendment gave the Centre and States a shared, simultaneous power instead of separate silos.',
          'Whisky for drinking stays under State excise; whisky-making machinery is under GST.'),
        C('c3', T3, [
            'Intra-State supply: CGST (Centre) and SGST (State) — or UTGST in a Union Territory without a legislature — are levied together, usually at equal halves of the rate.',
            'Inter-State supply, imports and supplies to or by SEZ units: IGST, levied by the Centre under the IGST Act and later shared with the destination State.',
            'Laws: CGST Act 2017, IGST Act 2017, UTGST Act 2017, each State\'s SGST Act, and rules and notifications under them. Credits are used across taxes in a prescribed order, so tax on an inter-State purchase can pay tax on an intra-State sale.'],
          'Within a State, two partners share the tax; across States, the Centre collects and settles later.',
          'A Delhi supplier selling to a Delhi buyer charges CGST + SGST; selling to a Chandigarh buyer, CGST + UTGST if both are in Chandigarh, else IGST.'),
        C('c4', T4, [
            'The GST Council has the Union Finance Minister as chairperson, the Union Minister of State for Finance and the finance ministers of all States. It recommends rates, exemptions, thresholds, model laws and dispute resolution. Decisions need three-fourths of weighted votes of members present and voting: the Centre\'s vote counts as one-third, the States\' together as two-thirds; quorum is half the members.',
            'The Goods and Services Tax Network (GSTN) runs the IT backbone: registration, returns, payments and invoice matching.',
            'Rates: after the GST 2.0 rationalisation in September 2025, most goods and services fall into a 5% merit slab and an 18% standard slab, with a 40% rate for luxury and sin items, alongside nil, 0.25% and 3% rates for a few items. The compensation cess has been phased out.'],
          'The Council is a federal forum: neither the Centre nor the States can push a decision through alone.',
          'With the Centre at one-third and States at two-thirds of the weighted vote, a 75% majority needs the Centre plus most States.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Explaining GST to a new client', 'role': 'Article assistant',
             'situation': 'A first-time trader asks why his invoices show CGST and SGST for some customers and IGST for others.',
             'steps': ['Show the location of supplier and place of supply.', 'Explain intra-State and inter-State outcomes.', 'Show how credit of both flows.', 'Point to the HSN or SAC rate.'],
             'takeaway': 'Location decides the type of tax; the product decides the rate.'}]

    mcqs = [
        Q('m1', 'GST was introduced by which Constitutional Amendment?', ['101st', '100th', '122nd', '99th'], 0,
          'The Constitution (One Hundred and First Amendment) Act, 2016 brought in Articles 246A, 269A and 279A. The 122nd was the Bill number. In practice: GST took effect from 1 July 2017.', 'c2', T2, check=101),
        Q('m2', 'Which item is outside GST under the Constitution itself?', ['Alcoholic liquor for human consumption', 'Petrol', 'Tobacco', 'Natural gas'], 0,
          'Article 366(12A) excludes only alcoholic liquor for human consumption. Petroleum products are within GST but await a Council date; tobacco is taxed under GST. In practice: alcohol bears State excise and VAT.', 'c2', T2),
        Q('m3', 'Which tax was NOT subsumed in GST?', ['Basic customs duty', 'Central excise on most goods', 'Service tax', 'State VAT'], 0,
          'Basic customs duty continues on imports; IGST is levied in addition to it. Excise (except on specified goods), service tax and VAT were subsumed. In practice: imports bear BCD plus IGST.', 'c1', T1),
        Q('m4', 'Article 279A deals with:', ['The GST Council', 'Levy of IGST', 'Definition of GST', 'Power to levy GST'], 0,
          'Article 279A constitutes the GST Council; 269A deals with IGST, 366(12A) defines GST and 246A gives the power to levy. In practice: Council recommendations are implemented by notifications.', 'c2', T2),
        Q('m5', 'In the GST Council, the Central Government\'s vote carries a weight of:', ['One-third of votes cast', 'Half of votes cast', 'Two-thirds of votes cast', 'One-fourth of votes cast'], 0,
          'The Centre\'s vote is one-third and all States together two-thirds; a decision needs three-fourths of the weighted votes. In practice: neither side can act alone.', 'c4', T4),
        Q('m6', 'A supply from Bengaluru to a registered buyer in Mysuru attracts:', ['CGST and SGST', 'IGST', 'UTGST', 'CGST only'], 0,
          'Supplier and place of supply are both in Karnataka, so it is intra-State, attracting CGST and SGST. In practice: IGST applies only when the two States differ.', 'c3', T3),
        Q('m7', 'Who chairs the GST Council?', ['Union Finance Minister', 'Prime Minister', 'Chief Justice', 'Chairman, CBIC'], 0,
          'The Union Finance Minister chairs it, with the Union Minister of State for Finance and the State finance ministers as members. In practice: the CBIC implements decisions for central tax.', 'c4', T4),
        Q('m8', 'GST is best described as a:', ['Destination-based consumption tax', 'Origin-based production tax', 'Tax on income', 'Tax on manufacture only'], 0,
          'Tax accrues to the State where goods or services are consumed, credit flows through the chain and the final consumer bears the burden. In practice: that is why IGST is settled to the destination State.', 'c1', T1),
    ]

    questions = [
        W('q1', 3, i1['q'], i1['solution'],
          [S('s1', 'Intra-State identified', 1, 'concept', 'intra'), S('s2', 'CGST + SGST', 1, 'computation', 'CGST', nums=[cg]), S('s3', 'IGST', 1, 'computation', 'IGST', nums=[ig])],
          ['State the nature first.'], ['Charging IGST within a State.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Excise', 1, 'computation', 'excise', nums=[10000]), S('s2', 'VAT on excise-inclusive value', 2, 'computation', 'VAT', nums=[16250]), S('s3', 'Cascading explained', 1, 'concept', 'tax on tax|credit')],
          ['Show the VAT base.'], ['Ignoring the excise in the VAT base.'], ['Table and one paragraph.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is cascading and how does GST remove it?', 'Cascading is tax charged on a value that already includes earlier tax that could not be credited; GST removes it by allowing input tax credit at every stage so only value addition is effectively taxed.',
          [P('p1', 'Tax on tax', 5, 'tax on tax|already includes'), P('p2', 'Credit at every stage', 5, 'credit')], 'c1'),
        V('v2', 'What does Article 246A provide?', 'It gives Parliament and State Legislatures simultaneous power to make laws on GST, with Parliament having exclusive power over inter-State supplies.',
          [P('p1', 'Simultaneous power', 5, 'simultaneous|both'), P('p2', 'Inter-State with Parliament', 5, 'inter-state|parliament')], 'c2'),
        V('v3', 'Which taxes apply on an inter-State supply?', 'Integrated GST, levied and collected by the Centre under the IGST Act and later apportioned to the consuming State.',
          [P('p1', 'IGST', 6, 'igst|integrated'), P('p2', 'Centre collects', 4, 'centre|apportion')], 'c3'),
        V('v4', 'Which petroleum products await GST?', 'Crude oil, petrol, high-speed diesel, natural gas and aviation turbine fuel, which will be taxed under GST from a date the Council recommends.',
          [P('p1', 'Five products', 6, 'crude|diesel|turbine'), P('p2', 'Council date', 4, 'council|date')], 'c2'),
        V('v5', 'What is the role of GSTN?', 'It is the technology company that runs the common portal for registration, returns and payments and supports invoice matching for credit.',
          [P('p1', 'IT backbone', 5, 'portal|technology'), P('p2', 'Functions', 5, 'registration|returns|payment')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Coastal Traders goes national', 'difficulty': 'core',
              'case': 'Coastal Traders of Kochi, Kerala, sells spices worth ₹2,00,000 (5% rate) to a hotel in Kochi and ₹3,00,000 to a wholesaler in Chennai. It also imports packing machines from Germany.',
              'mcqs': [
                  M('k1a', 'Tax on the Kochi sale:', ['CGST ₹5,000 + SGST ₹5,000', 'IGST ₹10,000', 'CGST ₹10,000', 'SGST ₹10,000'], 0,
                    'Intra-State supply in Kerala: 5% split equally, ₹5,000 each. In practice: show both on the invoice.', 'core', topic=T3),
                  M('k1b', 'Tax on the Chennai sale:', ['IGST ₹15,000', 'CGST ₹7,500 + SGST ₹7,500', 'Nil', 'IGST ₹7,500'], 0,
                    'Kerala to Tamil Nadu is inter-State, so IGST at 5% on ₹3,00,000 = ₹15,000. In practice: Tamil Nadu ultimately gets the State share.', 'core', topic=T3),
                  M('k1c', 'The import of machines attracts:', ['Basic customs duty and IGST', 'IGST only', 'CGST and SGST', 'No tax'], 0,
                    'Imports are inter-State supplies for GST; IGST is collected with basic customs duty, which GST did not subsume. In practice: IGST on imports is creditable.', 'moderate', topic=T2),
                  M('k1d', 'Who decides the rate for spices?', ['Government on the recommendation of the GST Council', 'Kerala Government alone', 'GSTN', 'Parliament by annual vote'], 0,
                    'Rates are notified by the governments on the Council\'s recommendation. GSTN only runs the IT system. In practice: check the rate notification by HSN.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p3', 'int-p3-b-ch01', 1, 'GST in India - An Introduction',
                ['Explain the problems of the earlier system and the features of GST.',
                 'Describe the constitutional provisions supporting GST.',
                 'Distinguish CGST, SGST/UTGST and IGST.',
                 'Describe the GST Council, GSTN and the current rate structure.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['int-p3-a-ch09-u01'],
                 'exam_tip': 'Article numbers (246A, 269A, 279A, 366(12A)) are favourite MCQ material — learn what each does.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['GST: destination-based tax on supply; credit through the chain.',
                             '101st Amendment: Arts. 246A, 269A, 279A, 366(12A).',
                             'Intra-State: CGST + SGST/UTGST; inter-State and imports: IGST.',
                             'Council: Centre 1/3, States 2/3; decisions by 3/4 weighted vote.',
                             'Rates after GST 2.0: mainly 5%, 18% and 40%.'],
                 'remember': ['Alcohol for human consumption is outside GST.', 'Five petroleum products await a Council date.'],
                 'traps': ['IGST does not replace basic customs duty.', '122nd was the Bill, 101st the Act.']},
                [('Art. 246A', 'Power to levy GST'), ('Art. 269A', 'IGST'), ('Art. 279A', 'GST Council'), ('Art. 366(12A)', 'Definition of GST')],
                viva, cases)
