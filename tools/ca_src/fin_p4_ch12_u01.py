"""CA Final · Paper 4 · Chapter 12 Taxation of Digital Transactions.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch12-u01'
T1 = 'Digital economy and e-commerce models'
T2 = 'Tax challenges of digitalisation'
T3 = 'Taxation of virtual digital assets'
T4 = 'TDS and gifts of virtual digital assets'


def build():
    ck = Checks()
    g = ck.add('300000-200000', 'Gain on token A (₹)')
    t = ck.add('(300000-200000)*0.30', 'Tax at 30% on gain (₹)')
    tc = ck.add('(300000-200000)*0.30*1.04', 'Tax with 4% cess (₹)')
    i1 = {'id': 'i1', 'title': 'Gains and losses on crypto-assets', 'difficulty': 'core', 'minutes': 6,
          'q': 'Rhea, a resident salaried individual, sells token A (cost ₹2,00,000) for ₹3,00,000 and token B (cost ₹1,50,000) for ₹1,00,000 in T.Y. 2026-27. She paid exchange fees of ₹3,000 on these trades. Compute tax on VDA income (no surcharge).',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['Gain on token A', 'Sale price − cost only', inr(g)],
              ['Loss on token B', 'Cannot be set off; not carried forward', '50,000'],
              ['Exchange fees', 'No deduction except cost of acquisition', '—'],
              ['Tax @ 30%', '', inr(t)],
              ['Add cess 4%', '', inr(tc)]], title='Section 194(1) Table Sl. No. 4')],
          'checks': list(ck)}

    c2 = Checks()
    td = c2.add('300000*0.01', 'TDS at 1% on consideration (₹)')
    gf = c2.add('80000', 'Taxable gift of VDA from friend (₹)')
    i2 = {'id': 'i2', 'title': 'TDS and gifts', 'difficulty': 'core', 'minutes': 5,
          'q': 'In the above case, the buyer of token A pays ₹3,00,000 to Rhea. Separately, Rhea receives tokens worth ₹80,000 as a gift from a friend and tokens worth ₹40,000 from her sister. Compute the TDS on token A and the taxable gift.',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['TDS on token A', '1% × 3,00,000 (section 393(1) Table Sl. No. 8(vi))', inr(td)],
              ['Gift from friend', 'Aggregate FMV exceeds ₹50,000 — taxable', inr(gf)],
              ['Gift from sister', 'Relative — excluded', '—']], title='VDA compliance')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 402(12) defines electronic commerce as supply of goods, services or both, including digital products, over a digital or electronic network. Models include B2B, B2C, C2C and platform-based marketplaces, subscription services, digital wallets and the sharing economy.',
            'Features of digital business: mobility of intangibles and users, reliance on data and network effects, multi-sided platforms, and the ability to serve a market with little or no physical presence.',
            'Digital wallets and mobile money enable trusted online payments, widening access for people without traditional banking.'],
          'Value is created where users and data are, not only where offices are.',
          'A ride-hailing app matches drivers and riders without owning cars.'),
        C('c2', T2, [
            'Key issues: nexus (PE rules based on physical presence weaken), data and user-created value, characterisation of payments (business income, royalty or fees for technical services), and allocation of profits between jurisdictions.',
            'BEPS Action 1 considered a significant economic presence test, withholding tax on digital transactions and an equalisation levy; the OECD/G20 Two-Pillar solution followed.',
            'India introduced a 6% equalisation levy on specified online advertising services (2016) and extended it to e-commerce supplies (2020); the e-commerce levy was withdrawn from 1 August 2024 and the levy on specified digital services was abolished by the Finance Act, 2025.'],
          'Tax rules built for factories struggle with platforms.',
          'An overseas ad platform with Indian users but no office tests PE rules.'),
        C('c3', T3, [
            'Virtual digital asset (section 2(111)) covers information, code, number or token generated cryptographically or otherwise that provides a digital representation of value, including crypto-assets on distributed ledgers and non-fungible tokens as notified; Indian and foreign currency and gift cards or vouchers are excluded.',
            'Income from transfer of a VDA is taxed at 30% (section 194(1) Table Sl. No. 4) regardless of the head; only cost of acquisition is deductible; no other expenditure, allowance or set-off of loss is permitted.',
            'Loss from transfer of a VDA cannot be set off against any income, including other VDA gains, and cannot be carried forward. "Transfer" applies to VDAs whether or not they are capital assets.'],
          'Thirty percent on gains, zero relief for losses.',
          'A ₹1 lakh gain on one token and a ₹50,000 loss on another still leaves ₹1 lakh taxable.'),
        C('c4', T4, [
            'Section 393(1) Table Sl. No. 8(vi): the payer for transfer of a VDA deducts tax at 1% of the consideration. Where consideration is in kind or exchanged for another VDA, the payer must ensure the tax is paid before releasing it.',
            'No TDS is needed if consideration in the year does not exceed ₹50,000 where the payer is a specified person (individuals/HUFs with business turnover up to ₹1 crore or professional receipts up to ₹50 lakh, or with no business income) and ₹10,000 for others; specified persons need not obtain TAN. Where both the purchase-of-goods TDS and VDA TDS could apply, VDA TDS prevails.',
            'Gifts of VDAs are "property" under section 92(2)(m): FMV taxable if aggregate exceeds ₹50,000 from non-relatives, with the usual exclusions (relatives, marriage, will).'],
          'Track 1% TDS on each trade and gift thresholds.',
          'A ₹3 lakh token sale bears TDS of ₹3,000.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Crypto investor return', 'role': 'Tax associate',
             'situation': 'A client traded several tokens and received some as gifts.',
             'steps': ['Compute gain or loss token-wise with cost only.', 'Exclude losses from set-off.', 'Reconcile TDS credits.', 'Assess gifts under section 92(2)(m).'],
             'takeaway': 'Each profitable trade is taxed alone; losses are wasted.'}]

    mcqs = [
        Q('m1', 'Income from transfer of a VDA is taxed at:', ['Thirty percent', 'Twenty percent', 'Slab rates', 'Twelve and a half percent'], 0,
          'Flat rate. In practice: plus surcharge and cess.', 'c3', T3),
        Q('m2', 'Which deduction is allowed against VDA income?', ['Cost of acquisition', 'Exchange fees', 'Interest on borrowings', 'Internet charges'], 0,
          'Only cost. In practice: keep purchase records.', 'c3', T3),
        Q('m3', 'Loss on transfer of a VDA can be:', ['Neither set off nor carried forward', 'Set off against other VDA gains', 'Carried forward for eight years', 'Set off against salary'], 0,
          'Strict rule. In practice: no relief.', 'c3', T3),
        Q('m4', 'TDS on consideration for transfer of a VDA is:', ['One percent', 'Ten percent', 'Five percent', 'Thirty percent'], 0,
          'Section 393(1). In practice: payer\'s duty.', 'c4', T4),
        Q('m5', 'For a specified person, no VDA TDS is required if consideration in the year does not exceed:', ['Fifty thousand rupees', 'Ten thousand rupees', 'One lakh rupees', 'Five thousand rupees'], 0,
          'Threshold. In practice: others ₹10,000.', 'c4', T4),
        Q('m6', 'Equalisation levy on e-commerce supply or services was withdrawn from:', ['1 August 2024', '1 April 2026', '1 April 2020', '1 June 2016'], 0,
          'Withdrawn first; online ads levy abolished by Finance Act 2025.', 'c2', T2),
        Q('m7', 'Which is excluded from the definition of VDA?', ['Gift cards and vouchers', 'Non-fungible tokens', 'Crypto-assets', 'Cryptographic tokens'], 0,
          'Section 2(111) exclusion. In practice: check notifications.', 'c3', T3),
        Q('m8', 'A gift of tokens worth ₹80,000 from a friend is:', ['Taxable in the recipient\'s hands', 'Exempt', 'Taxed in the donor\'s hands', 'Taxed at one percent'], 0,
          'Section 92(2)(m). In practice: FMV basis.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Gain and loss treatment', 3, 'analysis', 'set off', nums=[g]), S('s2', 'Tax', 2, 'computation', '30%', nums=[t, tc])],
          ['State no set-off.'], ['Netting the token B loss.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'TDS', 2, 'computation', '1%', nums=[td]), S('s2', 'Gifts', 2, 'analysis', 'relative', nums=[gf])],
          ['Mention threshold.'], ['Taxing gift from sister.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Why are digital businesses hard to tax under PE rules?', 'PE rules look for a fixed place of business or a dependent agent, while such firms earn from a market remotely.',
          [P('p1', 'Fixed place', 5, 'fixed place'), P('p2', 'Market', 5, 'market')], 'c2'),
        V('v2', 'Which BEPS Action dealt with the digital economy?', 'Action 1, which considered significant economic presence, withholding and an equalisation levy.',
          [P('p1', 'Action 1', 5, 'action 1'), P('p2', 'Significant economic presence', 5, 'significant economic presence')], 'c2'),
        V('v3', 'What can be deducted from VDA transfer income?', 'Only the cost of acquisition.',
          [P('p1', 'Cost of acquisition', 5, 'cost of acquisition'), P('p2', 'Only', 5, 'only')], 'c3'),
        V('v4', 'Who must deduct tax on a VDA transfer?', 'The person paying consideration to a resident for the transfer, at 1%.',
          [P('p1', 'Payer', 5, 'paying|payer'), P('p2', 'One percent', 5, '1%')], 'c4'),
        V('v5', 'Does the gift provision apply to VDAs?', 'Yes, VDAs are property for section 92(2)(m), with the usual exclusions.',
          [P('p1', 'Property', 5, 'property'), P('p2', 'Exclusions', 5, 'exclusion')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Kabir\'s NFT sale', 'difficulty': 'core',
              'case': 'Kabir, a salaried individual with no business income, buys a notified NFT from Meghna, a resident, for ₹45,000 in May 2026 and another from her for ₹30,000 in October 2026. Meghna had bought each for ₹20,000.',
              'mcqs': [
                  M('k1a', 'Aggregate consideration paid by Kabir to Meghna (₹):', ['75,000', '45,000', '30,000', '40,000'], 0,
                    '45,000 + 30,000. In practice: yearly aggregate.', 'core', check=75000, topic=T4),
                  M('k1b', 'Is Kabir required to deduct TDS?', ['Yes, aggregate exceeds ₹50,000', 'No, he is salaried', 'No, NFTs are excluded', 'Only on the first purchase'], 0,
                    'Specified person threshold crossed. In practice: no TAN needed.', 'core', topic=T4),
                  M('k1c', 'Meghna\'s taxable VDA income (₹):', ['35,000', '75,000', '40,000', '25,000'], 0,
                    '(45,000 − 20,000) + (30,000 − 20,000). In practice: cost only.', 'core', check=35000, topic=T3),
                  M('k1d', 'Meghna\'s tax before cess (₹):', ['10,500', '7,000', '22,500', '3,500'], 0,
                    '30% × 35,000. In practice: no slab benefit.', 'core', check=10500, topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch12', 1, 'Taxation of Digital Transactions',
                ['Describe e-commerce models and features of the digital economy.',
                 'Identify tax challenges of digitalisation and India\'s response.',
                 'Compute tax on transfer of virtual digital assets.',
                 'Apply TDS and gift provisions to virtual digital assets.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p4-ch11-u01'],
                 'exam_tip': 'Compute VDA gains token by token and state that losses are ignored.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['E-commerce under section 402(12).', 'Nexus and characterisation challenges; BEPS Action 1.', 'Equalisation levy withdrawn (2024) and abolished (Finance Act 2025).',
                             'VDA section 2(111); 30% tax; cost only; no loss set-off.', 'TDS 1%; thresholds ₹50,000/₹10,000; gifts taxed.'],
                 'remember': ['VDA losses vanish.'],
                 'traps': ['Deducting exchange fees from VDA gains.']},
                [('VDA definition', 'Section 2(111)'), ('Rate', 'Section 194(1)'), ('TDS', 'Section 393(1)'), ('Gifts', 'Section 92(2)(m)')],
                viva, cases)
