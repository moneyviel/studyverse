"""CA Final · Paper 4 · Chapter 9 Assessment of Various Entities.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch09-u01'
T1 = 'Taxation of companies and concessional regimes'
T2 = 'Minimum alternate tax and MAT credit'
T3 = 'Alternate minimum tax for non-corporates'
T4 = 'Firms, LLPs, AOPs and HUFs'
T5 = 'Tonnage tax and succession'


def build():
    ck = Checks()
    nt = ck.add('40000000*0.30', 'Tax on total income at 30% (₹)')
    mt = ck.add('300000000*0.14', 'MAT at 14% on book profit (₹)')
    ms = ck.add('300000000*0.14*1.12', 'MAT with 12% surcharge (₹)')
    mc = ck.add('round(300000000*0.14*1.12*1.04)', 'MAT with surcharge and 4% cess (₹)')
    i1 = {'id': 'i1', 'title': 'Does MAT apply?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Kestrel Industries Ltd, a domestic company with turnover above ₹400 crore in T.Y. 2024-25, has not opted for section 200 or 201. For T.Y. 2026-27 its total income is ₹4 crore and its book profit is ₹30 crore. Compute its tax liability.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Tax on total income', '30% × 4,00,00,000', inr(nt)],
              ['MAT', '14% × 30,00,00,000', inr(mt)],
              ['Comparison', 'Normal tax is lower, so MAT applies', '—'],
              ['Add surcharge 12%', 'Book profit above ₹10 crore', inr(ms)],
              ['Add cess 4%', 'Tax liability', inr(mc)]], title='Section 206(1)')],
          'checks': list(ck)}

    c2 = Checks()
    tx = c2.add('5000000*0.22*1.10*1.04', 'Tax under section 200 incl. surcharge and cess (₹)')
    so = c2.add('5000000*0.22*1.10*1.04*0.25', 'MAT credit set-off at 25% (₹)')
    np_ = c2.add('5000000*0.22*1.10*1.04*0.75', 'Net tax payable (₹)')
    bal = c2.add('800000-5000000*0.22*1.10*1.04*0.25', 'Credit carried forward (₹)')
    i2 = {'id': 'i2', 'title': 'Old MAT credit after moving to section 200', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Pelican Foods Ltd opts for section 200 from T.Y. 2026-27. Its total income is ₹50,00,000 and it carries MAT credit of ₹8,00,000 under section 115JAA of the 1961 Act as on 31 March 2026. Compute tax payable and credit carried forward.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Tax u/s 200', '22% + 10% surcharge + 4% cess', inr(tx)],
              ['Credit set off', '25% of tax payable', inr(so)],
              ['Net tax', '', inr(np_)],
              ['Credit carried forward', '8,00,000 − set-off (within 15 years)', inr(bal)]], title='Section 206(3)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Domestic companies pay 25% where turnover in T.Y. 2024-25 did not exceed ₹400 crore and 30% otherwise; foreign companies pay 35%. Surcharge for domestic companies is 7% above ₹1 crore and 12% above ₹10 crore of income (2% and 5% for foreign companies), plus 4% cess.',
            'Section 200 lets a domestic company opt for 22% plus a flat 10% surcharge, giving up specified exemptions and deductions; section 201 offers 15% to new manufacturing or electricity-generating companies meeting conditions. Once exercised, the option cannot be withdrawn and MAT does not apply.',
            'Income of these companies from special sources (e.g. capital gains) is taxed at the rates applicable to them; deemed income under section 201 attracts 30%.'],
          'Choose between the regular rate with deductions and a flat concessional rate.',
          'A company opting for section 200 pays an effective rate of about 25.17%.'),
        C('c2', T2, [
            'Section 206(1): if tax on total income is lower than 14% of book profit (9% for IFSC units earning solely in convertible foreign exchange), book profit is deemed the total income and MAT is payable, plus surcharge and cess. Book profit starts from the net profit in the statement of profit and loss prepared under the Companies Act and is adjusted for specified items.',
            'MAT does not apply to life insurance companies, companies opting for sections 200 or 201, and specified foreign companies without a permanent establishment or not required to register in India, or taxed only on presumptive income.',
            'MAT credit carried forward on 31 March 2026 under section 115JAA: a domestic company that switches to section 200/201 can set off up to 25% of its tax payable each year (section 206(3)); a foreign company may use it to the extent normal tax exceeds MAT (section 206(4)); in both cases within 15 years from when the credit first arose. No credit passes to an LLP on conversion.'],
          'MAT ensures companies pay at least 14% of book profit.',
          'Old credit of ₹8 lakh can absorb ₹3.15 lakh of a ₹12.58 lakh liability.'),
        C('c3', T3, [
            'Section 206(2): non-corporate assessees claiming profit-linked deductions in Chapter VIII-C (other than co-operatives\' section 149 deduction) or investment-linked deductions under section 46 pay AMT at 18.5% of adjusted total income (9% for IFSC units; 15% for co-operatives) if regular tax is lower.',
            'Adjusted total income adds back these deductions (with depreciation substituted for section 46 deductions).',
            'AMT does not apply to persons taxed under the default regime of section 202(1), to those opting for concessional co-operative regimes, or to individuals, HUFs, AOPs, BOIs and artificial juridical persons whose adjusted total income does not exceed ₹20 lakh.'],
          'Profit-linked deductions cannot drive tax below 18.5%.',
          'An LLP start-up deducting all profits under section 140 still pays AMT.'),
        C('c4', T4, [
            'A firm or LLP is taxed at 30% (plus surcharge and cess); remuneration and interest to partners are deductible within section 35(e) limits and taxed in partners\' hands, while the profit share is exempt. Partners of a firm are jointly and severally liable for its tax; partners of an LLP are liable on liquidation unless they prove no gross neglect (section 331).',
            'AOPs and BOIs: if member shares are unknown, tax is at the maximum marginal rate (section 311). Section 309 computes each member\'s share after adjusting payments to members; under section 310, if the AOP paid at maximum marginal or higher rate, the share is excluded from the member\'s income.',
            'HUFs: a Hindu undivided family continues to be assessed until a partition is recorded under section 315; partial partitions are ignored. Income from property converted into HUF property by a member is clubbed with him (section 99(3)).'],
          'Each entity type has its own rate and pass-through rules.',
          'An AOP with unknown member shares pays tax at the maximum marginal rate.'),
        C('c5', T5, [
            'Tonnage tax (sections 225 to 234): an Indian shipping company may opt to have profits from qualifying ships computed on a notional basis linked to net tonnage, instead of actual profits. The option runs for 10 years and requires conditions such as training cadets and transferring a portion of profits to a reserve.',
            'Section 313: where a business is succeeded, the predecessor is assessed up to the date of succession and the successor thereafter; the AO may recover tax from the successor if the predecessor cannot be found.',
            'Section 323: directors of a private company are jointly and severally liable for its unrecoverable tax unless they prove non-recovery is not due to their gross neglect, misfeasance or breach of duty.'],
          'Special schemes and recovery rules apply to particular situations.',
          'A shipowner can pay tax on notional tonnage income regardless of actual profits.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Regime decision for a company', 'role': 'Tax manager',
             'situation': 'A listed company with MAT credit considers moving to section 200.',
             'steps': ['Compute tax under normal provisions and MAT.', 'Compute tax under section 200.', 'Model 25% credit utilisation within 15 years.', 'Recommend and file the option in time.'],
             'takeaway': 'Old MAT credit slows but rarely blocks the switch.'}]

    mcqs = [
        Q('m1', 'MAT rate for a company outside IFSC is:', ['Fourteen percent of book profit', 'Fifteen percent', 'Eighteen and a half percent', 'Nine percent'], 0,
          'Section 206(1). In practice: plus surcharge and cess.', 'c2', T2),
        Q('m2', 'MAT does not apply to a company that:', ['Has opted for section 200', 'Has book profit above ₹10 crore', 'Is listed', 'Has foreign shareholders'], 0,
          'Concessional regime. In practice: irreversible option.', 'c2', T2),
        Q('m3', 'Old MAT credit can be set off by a domestic company under section 200 up to:', ['Twenty-five percent of tax payable', 'The full tax payable', 'Ten percent of tax payable', 'Nil'], 0,
          'Section 206(3). In practice: balance carried forward.', 'c2', T2),
        Q('m4', 'AMT rate for a non-corporate assessee (non-IFSC, non-co-operative) is:', ['Eighteen and a half percent', 'Fourteen percent', 'Thirty percent', 'Fifteen percent'], 0,
          'Section 206(2). In practice: on adjusted total income.', 'c3', T3),
        Q('m5', 'AMT does not apply to an individual whose adjusted total income does not exceed:', ['Twenty lakh rupees', 'Fifty lakh rupees', 'One crore rupees', 'Ten lakh rupees'], 0,
          'Threshold for individuals and similar persons. In practice: also not in default regime.', 'c3', T3),
        Q('m6', 'An AOP whose members\' shares are unknown pays tax at:', ['The maximum marginal rate', 'Slab rates', 'Twenty-two percent', 'Thirty percent always'], 0,
          'Section 311. In practice: draft clear deeds.', 'c4', T4),
        Q('m7', 'Section 200 rate for domestic companies is:', ['Twenty-two percent plus ten percent surcharge', 'Twenty-five percent', 'Fifteen percent', 'Thirty percent'], 0,
          'Concessional option. In practice: forgo deductions.', 'c1', T1),
        Q('m8', 'Directors of a private company are liable for unrecovered tax unless they prove:', ['No gross neglect, misfeasance or breach of duty', 'They resigned before assessment', 'They held no shares', 'The company was audited'], 0,
          'Section 323. In practice: document diligence.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Compare normal tax and MAT', 3, 'computation', 'book profit', nums=[nt, mt]), S('s2', 'Surcharge and cess', 3, 'computation', 'surcharge', nums=[ms, mc])],
          ['State why MAT applies.'], ['Using 30% rate on book profit.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Tax u/s 200', 2, 'computation', 'surcharge', nums=[tx]), S('s2', 'Credit set-off and balance', 3, 'computation', 'credit', nums=[so, np_, bal])],
          ['Mention 15-year limit.'], ['Setting off the entire credit.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is book profit for MAT?', 'The net profit shown in the Companies Act profit and loss statement, then adjusted for the items listed in section 206.',
          [P('p1', 'Net profit', 5, 'net profit'), P('p2', 'Adjusted', 5, 'adjust')], 'c2'),
        V('v2', 'Who pays AMT?', 'Non-corporate assessees claiming profit-linked Chapter VIII-C or section 46 deductions whose regular tax is lower than 18.5% of adjusted total income.',
          [P('p1', 'Profit-linked deductions', 5, 'profit-linked|section 46'), P('p2', 'Eighteen and a half', 5, '18.5')], 'c3'),
        V('v3', 'How is a member\'s share in an AOP taxed if the AOP paid at the maximum marginal rate?', 'It is excluded from the member\'s total income.',
          [P('p1', 'Excluded', 5, 'exclude'), P('p2', 'Total income', 5, 'total income')], 'c4'),
        V('v4', 'Is partial partition of a HUF recognised?', 'Partial partitions are ignored for tax; the HUF continues to be assessed as before.',
          [P('p1', 'Ignored', 5, 'ignore'), P('p2', 'Continues', 5, 'continue')], 'c4'),
        V('v5', 'For how long does a tonnage tax option run?', 'Ten years, subject to conditions.',
          [P('p1', 'Ten years', 5, 'ten years|10 years'), P('p2', 'Conditions', 5, 'condition')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Quill Labs LLP', 'difficulty': 'moderate',
              'case': 'Quill Labs LLP, an eligible start-up, earns ₹2,00,00,000 of eligible business profits in T.Y. 2026-27 and claims a 100% deduction under section 140. It has no other income.',
              'mcqs': [
                  M('k1a', 'Regular income-tax payable (₹):', ['0', '60,00,000', '37,00,000', '30,00,000'], 0,
                    'Total income is nil after deduction. In practice: AMT check.', 'core', check=0, topic=T3),
                  M('k1b', 'Adjusted total income (₹):', ['2,00,00,000', 'Nil', '1,00,00,000', '20,00,000'], 0,
                    'Deduction added back. In practice: section 206(2).', 'core', check=20000000, topic=T3),
                  M('k1c', 'AMT before surcharge and cess (₹):', ['37,00,000', '28,00,000', '60,00,000', '30,00,000'], 0,
                    '18.5% × 2 crore. In practice: credit for future years.', 'core', check=3700000, topic=T3),
                  M('k1d', 'If Quill were a company, the corresponding levy would be:', ['MAT on book profit', 'AMT', 'No minimum tax', 'Tonnage tax'], 0,
                    'Companies face MAT. In practice: 14% of book profit.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch09', 1, 'Assessment of Various Entities',
                ['Apply company tax rates and concessional regimes.',
                 'Compute MAT and old MAT credit.',
                 'Compute AMT for non-corporates.',
                 'Assess firms, LLPs, AOPs and HUFs.',
                 'Apply tonnage tax and succession provisions.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 35}, 'prereq': ['fin-p4-ch08-u01'],
                 'exam_tip': 'Compute tax on normal provisions first, then the minimum tax, and pay the higher.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Company rates 25%/30%/35%; sections 200 and 201.', 'MAT 14% of book profit.', 'Old MAT credit: 25% set-off; 15 years.',
                             'AMT 18.5% for non-corporates; ₹20 lakh threshold.', 'Firms, AOPs, HUFs; tonnage tax; succession.'],
                 'remember': ['Section 200/201 companies are outside MAT.'],
                 'traps': ['Applying AMT under the default regime.']},
                [('Concessional rates', 'Sections 200–201'), ('MAT / AMT', 'Section 206'), ('AOP share', 'Sections 309–311'), ('HUF partition', 'Section 315')],
                viva, cases)
