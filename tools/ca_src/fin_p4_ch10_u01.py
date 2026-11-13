"""CA Final · Paper 4 · Chapter 10 Assessment of RNPOs, Political Parties and Other Special Entities.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch10-u01'
T1 = 'Registration of non-profit organisations'
T2 = 'Application and accumulation of income'
T3 = 'Specified income, anonymous donations and violations'
T4 = 'Political parties, electoral trusts and private trusts'
T5 = 'Business trusts, investment funds and securitisation trusts'


def build():
    ck = Checks()
    req = ck.add('5000000*0.85', 'Required application at 85% (₹)')
    dee = ck.add('5000000*0.15', 'Deemed accumulation at 15% (₹)')
    sh = ck.add('5000000-3800000-5000000*0.15', 'Unapplied amount needing section 342 accumulation (₹)')
    tx = ck.add('(5000000-3800000-5000000*0.15)*0.30', 'Tax at 30% if not accumulated (₹)')
    i1 = {'id': 'i1', 'title': 'Shortfall in application', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Seva Sankalp Foundation, a registered NPO, has regular income of ₹50,00,000 for T.Y. 2026-27 and applies ₹38,00,000 to its objects in India. Compute the amount it must accumulate under section 342 to avoid tax, and the tax if it does not.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Required application', '85% × 50,00,000', inr(req)],
              ['Deemed accumulated', '15% × 50,00,000 (section 343)', inr(dee)],
              ['To accumulate under section 342', '50,00,000 − 38,00,000 − 7,50,000', inr(sh)],
              ['Tax if not accumulated', '30% as specified income', inr(tx)]], title='Sections 341–343')],
          'checks': list(ck)}

    c2 = Checks()
    ex = c2.add('max(5000000*0.05,100000)', 'Exclusion: higher of 5% of total donations and ₹1 lakh (₹)')
    ta = c2.add('600000-max(5000000*0.05,100000)', 'Anonymous donations taxable (₹)')
    t2 = c2.add('(600000-max(5000000*0.05,100000))*0.30', 'Tax at 30% (₹)')
    i2 = {'id': 'i2', 'title': 'Anonymous donations', 'difficulty': 'core', 'minutes': 5,
          'q': 'Prakash Vidya Trust, a registered educational NPO, receives total donations of ₹50,00,000 in T.Y. 2026-27, including anonymous donations of ₹6,00,000. Compute the tax on anonymous donations.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Exclusion', 'Higher of 5% × 50,00,000 and ₹1,00,000', inr(ex)],
              ['Taxable anonymous donations', '6,00,000 − exclusion', inr(ta)],
              ['Tax @ 30%', '', inr(t2)]], title='Section 337')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Under the Income-tax Act, 2025, charitable and religious trusts and institutions are "registered non-profit organisations" (RNPOs). Registration under section 332 is granted by the PCIT/CIT; new entities first get provisional registration (valid three years), and regular registration is valid for five years, renewable on application within the specified time.',
            'Charitable purpose (section 2(23)) includes relief of the poor, education, yoga, medical relief, preservation of environment and monuments, and other objects of general public utility — the last subject to limits on receipts from trade, commerce or business.',
            'Before granting registration, the authority examines the genuineness of activities and compliance with other laws; registration can be cancelled for specified violations under section 351.'],
          'Registration is the gateway to exemption.',
          'A new school trust gets provisional registration before commencing activities.'),
        C('c2', T2, [
            'An RNPO must apply at least 85% of its regular income to its objects in India during the year (section 341). Amounts applied from corpus, loans or borrowings are not application when spent, but reinvestment into corpus or repayment of the loan within five years counts then. Donations to another RNPO count only at 85% of the amount given; corpus donations to another RNPO are not application.',
            'Section 343 deems 15% of regular income accumulated. Any further unapplied income can be accumulated under section 342 for up to five years by stating the purpose in a statement filed before the return due date, and investing in permitted modes (section 350). Unutilised or misused accumulation becomes taxable.',
            'Expenditure paid in cash above ₹10,000 per day, TDS defaults (30% disallowed) and capital expenditure claimed twice are not treated as application.'],
          'Spend 85%, park 15%, and formally accumulate the rest.',
          'Applying ₹38 lakh out of ₹50 lakh leaves ₹4.5 lakh to accumulate under section 342.'),
        C('c3', T3, [
            'Specified income of an RNPO — such as income not applied or accumulated, income on violation of conditions, and benefits to related persons — is taxed at 30% (section 334).',
            'Anonymous donations above the higher of 5% of total donations and ₹1,00,000 are taxed at 30%, except for wholly religious trusts (fully exempt) and religious-cum-charitable trusts (taxed only on anonymous donations earmarked for educational or medical purposes).',
            'Specified violations under section 351 — application for non-objects, business beyond limits, false claims, non-compliance with other laws — can lead to cancellation of registration. On cancellation, merger with a non-RNPO or dissolution, accreted income (assets less liabilities at FMV) is taxed at the maximum marginal rate under section 352 ("exit tax").'],
          'Breaking the rules costs exemption and can trigger exit tax.',
          'Anonymous donations of ₹6 lakh out of ₹50 lakh total leave ₹3.5 lakh taxable at 30%.'),
        C('c4', T4, [
            'A political party holding registration under section 29A of the 1951 election law is exempt (section 12 with Schedule VIII) on house property, capital gains, other sources and voluntary contributions, if they keep books, record contributions above ₹20,000, get accounts audited, accept no donation above ₹2,000 other than by banking channels, submit the contribution report to the Election Commission and file the return.',
            'Electoral trusts are exempt on voluntary contributions if they distribute at least 95% of contributions received during the year to registered political parties.',
            'Private discretionary trusts are taxed at the maximum marginal rate on their entire income, except where beneficiaries have no other taxable income above the exemption limit, for the only trust declared by will, for specified pre-1970 trusts for dependants, and for employee welfare funds — which are taxed as an AOP. Oral trusts are taxed at the maximum marginal rate (section 308).'],
          'Parties must keep records; private discretionary trusts face top rates.',
          'Rent earned by a compliant political party is exempt.'),
        C('c5', T5, [
            'Business trusts (REITs and InvITs) under section 223: interest and dividend from the SPV and rental income of a REIT pass through to unit holders, who are taxed on those components; the trust is taxed on other income, mainly capital gains, at applicable rates. Distributions as repayment of debt are treated as income of the unit holder in specified cases.',
            'Investment funds (Category I and II AIFs) under section 224: income other than business income passes through to unit holders and is taxed as if earned directly; business income is taxed in the fund\'s hands at the applicable rate.',
            'Securitisation trusts under section 221: income is exempt in the trust and taxed in the investors\' hands as if they had invested directly, with TDS by the trust.'],
          'Pooling vehicles are largely tax-transparent.',
          'Rent earned by a REIT is taxed in unit holders\' hands, not the REIT\'s.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end compliance for an NPO', 'role': 'Audit manager',
             'situation': 'A trust has unspent funds and anonymous donations at year-end.',
             'steps': ['Compute application against 85%.', 'File accumulation statement for any balance.', 'Quantify taxable anonymous donations.', 'Confirm registration validity and filing dates.'],
             'takeaway': 'Missing a statement can turn surplus into taxable income.'}]

    mcqs = [
        Q('m1', 'An RNPO must apply to its objects at least:', ['Eighty-five percent of regular income', 'Seventy-five percent', 'Fifteen percent', 'One hundred percent'], 0,
          'Section 341. In practice: deemed 15% accumulation.', 'c2', T2),
        Q('m2', 'Income accumulated under section 342 must be used within:', ['Five years', 'Three years', 'Ten years', 'Two years'], 0,
          'Purpose stated in advance. In practice: invest in permitted modes.', 'c2', T2),
        Q('m3', 'Regular registration of an RNPO is valid for:', ['Five years', 'Three years', 'Ten years', 'Permanently'], 0,
          'Section 332. In practice: renew in time.', 'c1', T1),
        Q('m4', 'Specified income of an RNPO is taxed at:', ['Thirty percent', 'Maximum marginal rate', 'Slab rates', 'Fifteen percent'], 0,
          'Flat rate. In practice: no deductions.', 'c3', T3),
        Q('m5', 'Accreted income on cancellation of registration is taxed at:', ['The maximum marginal rate', 'Thirty percent', 'Twenty-two percent', 'Nil'], 0,
          'Section 352 exit tax. In practice: on net FMV of assets.', 'c3', T3),
        Q('m6', 'A political party must record contributions exceeding:', ['Twenty thousand rupees', 'Two thousand rupees', 'Ten thousand rupees', 'One lakh rupees'], 0,
          'Schedule VIII. In practice: name and address.', 'c4', T4),
        Q('m7', 'An electoral trust must distribute at least:', ['Ninety-five percent of contributions', 'Eighty-five percent', 'Seventy-five percent', 'All income'], 0,
          'Condition for exemption. In practice: within the year.', 'c4', T4),
        Q('m8', 'Rental income of a REIT is taxed in the hands of:', ['Unit holders', 'The REIT', 'The SPV', 'The sponsor only'], 0,
          'Pass-through. In practice: TDS on distribution.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Application test', 2, 'computation', '85%', nums=[req]), S('s2', 'Deemed and actual accumulation', 2, 'computation', 'accumulat', nums=[dee, sh]), S('s3', 'Tax if not accumulated', 2, 'computation', '30%', nums=[tx])],
          ['Cite sections.'], ['Ignoring the deemed 15%.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Exclusion', 2, 'computation', 'higher', nums=[ex]), S('s2', 'Taxable and tax', 2, 'computation', 'anonymous', nums=[ta, t2])],
          ['Mention religious trust exception.'], ['Using lower of the two limits.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Are anonymous donations to a wholly religious trust taxed?', 'They are fully exempt for a wholly religious trust.',
          [P('p1', 'Exempt', 5, 'exempt'), P('p2', 'Wholly religious', 5, 'religious')], 'c3'),
        V('v2', 'When is spending from a loan treated as application?', 'It counts in the year the loan is repaid out of income, provided this happens within five years.',
          [P('p1', 'Repaid', 5, 'repaid'), P('p2', 'Five years', 5, 'five years')], 'c2'),
        V('v3', 'What is accreted income?', 'The aggregate fair market value of assets less liabilities of the RNPO on the specified date, taxed at the maximum marginal rate.',
          [P('p1', 'Fair market value', 5, 'fair market'), P('p2', 'Liabilities', 5, 'liabilit')], 'c3'),
        V('v4', 'How is a private discretionary trust taxed?', 'At the maximum marginal rate on its whole income, subject to specified exceptions taxed as an AOP.',
          [P('p1', 'Maximum marginal rate', 5, 'maximum marginal'), P('p2', 'Exceptions', 5, 'exception')], 'c4'),
        V('v5', 'How is business income of a Category I or II AIF taxed?', 'In the hands of the fund; other income passes through to unit holders.',
          [P('p1', 'Fund', 5, 'fund'), P('p2', 'Pass through', 5, 'pass')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Jan Shakti Party', 'difficulty': 'core',
              'case': 'Jan Shakti Party, a party registered with the Election Commission under section 29A, earns rent of ₹15,00,000 from letting part of its office and receives voluntary contributions of ₹2 crore during T.Y. 2026-27. It maintains books, gets them audited, files its contribution report and return on time, but accepted one cash donation of ₹5,000.',
              'mcqs': [
                  M('k1a', 'Is rent from the office building eligible for exemption?', ['Yes, house property income of a party qualifies', 'No, it is business income', 'Only half', 'Only if spent on elections'], 0,
                    'Schedule VIII. In practice: conditions must be met.', 'core', topic=T4),
                  M('k1b', 'The cash donation of ₹5,000:', ['Breaches the condition on donations above ₹2,000', 'Is acceptable', 'Is exempt separately', 'Must be refunded only'], 0,
                    'Banking channels required. In practice: risks exemption.', 'core', topic=T4),
                  M('k1c', 'Contributions it must record with donor details are those exceeding (₹):', ['20,000', '2,000', '10,000', '50,000'], 0,
                    'Record-keeping condition. In practice: name and address.', 'core', check=20000, topic=T4),
                  M('k1d', 'If it were an electoral trust, it would need to distribute at least (₹) of ₹2 crore:', ['1,90,00,000', '1,70,00,000', '2,00,00,000', '1,50,00,000'], 0,
                    '95% × 2 crore. In practice: to registered parties.', 'core', check=19000000, topic=T4),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch10', 1, 'Assessment of RNPOs, Political Parties and Other Special Entities',
                ['Apply registration rules for non-profit organisations.',
                 'Compute application and accumulation of income.',
                 'Tax specified income, anonymous donations and accreted income.',
                 'Apply provisions for political parties, electoral trusts and private trusts.',
                 'Apply pass-through rules for business trusts, investment funds and securitisation trusts.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 45, 'practice': 30}, 'prereq': ['fin-p4-ch09-u01'],
                 'exam_tip': 'For RNPOs, compute regular income, then 85% application, then accumulation and specified income.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 332 registration.', 'Section 341: 85% application; 343 deemed 15%; 342 accumulation 5 years.', 'Specified income and anonymous donations at 30%.',
                             'Section 352 exit tax at MMR.', 'Political parties Schedule VIII; electoral trusts 95%.', 'Sections 221, 223, 224 pass-through.'],
                 'remember': ['Anonymous donation exclusion: higher of 5% and ₹1 lakh.'],
                 'traps': ['Treating corpus donations to another RNPO as application.']},
                [('Registration', 'Section 332'), ('Application', 'Section 341'), ('Accumulation', 'Section 342'), ('Exit tax', 'Section 352'), ('Business trusts', 'Section 223')],
                viva, cases)
