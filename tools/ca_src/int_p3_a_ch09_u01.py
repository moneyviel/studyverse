"""CA Intermediate · Paper 3A Income-tax Law · Chapter 9 Income-tax Liability – Computation and Optimisation (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers are taken from it; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch09-u01'
T1 = 'From gross total income to total income: the computation steps'
T2 = 'Rates, rebate (s. 156), surcharge and cess'
T3 = 'Alternate Minimum Tax (s. 206(2))'
T4 = 'Choosing between the default and optional regimes'


def build():
    # i1 — rebate with marginal relief
    ck = Checks()
    tax = ck.add('20000+40000+40000*15/100', 'Tax on ₹12,40,000 under the default regime')
    reb = ck.add('66000-40000', 'Rebate: tax minus income above ₹12 lakh')
    pay = ck.add('(66000-26000)*104/100', 'Tax after rebate, with 4% cess')
    i1 = {'id': 'i1', 'title': 'Just above ₹12 lakh', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Ms. Tara, a resident aged 34, earns gross salary of ₹13,15,000 and has no other income. She stays in the default regime. Compute her tax for tax year 2026-27.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Total income', '13,15,000 − standard deduction 75,000', inr(1240000)],
              ['Tax on slabs', '4–8 lakh @5% = 20,000; 8–12 lakh @10% = 40,000; 12–12.4 lakh @15% = 6,000', inr(tax)],
              ['Rebate u/s 156', 'Income above ₹12 lakh is 40,000; tax 66,000 exceeds it, so rebate = 66,000 − 40,000', inr(reb)],
              ['Tax after rebate', '', inr(40000)],
              ['Add: cess @4%', '', inr(1600)],
              ['Tax payable', '', inr(pay)]], title='Default regime with marginal relief'),
              note('The rebate makes sure that crossing ₹12 lakh never costs more tax than the extra income itself.')],
          'checks': list(ck)}

    # i2 — regime comparison
    ck2 = Checks()
    opt_ti = ck2.add('1500000-50000-120000-200000-150000-25000', 'Total income, optional regime')
    opt_tax = ck2.add('(12500+(955000-500000)*20/100)*104/100', 'Tax with cess, optional regime')
    def_ti = ck2.add('1500000-75000', 'Total income, default regime')
    def_tax = ck2.add('(20000+40000+(1425000-1200000)*15/100)*104/100', 'Tax with cess, default regime')
    save = ck2.add('107640-97500', 'Saving by staying in the default regime')
    i2 = {'id': 'i2', 'title': 'Which regime wins?', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Mr. Arvind (45, resident, salaried, no business income) has gross salary of ₹15,00,000, including HRA of which ₹1,20,000 would be exempt under the optional regime. He pays interest of ₹2,00,000 on a loan for his self-occupied house, invests ₹1,50,000 in PPF and pays a health premium of ₹25,000 for his family. Compute his tax under both regimes and advise.',
          'solution': [table(['Item', 'Optional ₹', 'Default ₹'], [
              ['Gross salary', inr(1500000), inr(1500000)],
              ['Less: standard deduction', '(50,000)', '(75,000)'],
              ['Less: HRA exemption', '(1,20,000)', '—'],
              ['House property: interest on self-occupied house', '(2,00,000)', '—'],
              ['Chapter VIII: s. 123 and s. 126', '(1,75,000)', '—'],
              ['Total income', inr(opt_ti), inr(def_ti)],
              ['Tax including 4% cess', inr(opt_tax), inr(def_tax)]], title='Side-by-side computation'),
              p('The default regime costs ₹' + inr(save) + ' less, so he should not opt out. Without business income he can make this choice afresh each year when filing his return by the due date.')],
          'checks': list(ck2)}

    # i3 — AMT
    ck3 = Checks()
    reg = ck3.add('(12500+100000+(2050000-1000000)*30/100)*104/100', 'Regular tax on ₹20,50,000 with cess (optional regime)')
    amt = ck3.add('2350000*18.5/100*104/100', 'AMT on adjusted total income with cess')
    cr = ck3.add('452140-444600', 'AMT credit carried forward')
    i3 = {'id': 'i3', 'title': 'A patent holder and the minimum tax', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Ms. Rina, a resident inventor who has opted out of the default regime, has gross total income of ₹25,00,000, including patent royalty of ₹3,00,000 eligible for deduction under section 152. She claims ₹1,50,000 under section 123. Compute her tax liability for tax year 2026-27 and any AMT credit.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Total income', '25,00,000 − 1,50,000 − 3,00,000', inr(2050000)],
              ['Regular tax with cess', '12,500 + 1,00,000 + 30% of 10,50,000 = 4,27,500; + 4%', inr(reg)],
              ['Adjusted total income', '20,50,000 + section 152 deduction 3,00,000 (above ₹20 lakh, so AMT applies)', inr(2350000)],
              ['AMT with cess', '18.5% × 23,50,000 = 4,34,750; + 4%', inr(amt)],
              ['Tax payable', 'Higher of the two', inr(amt)],
              ['AMT credit', '4,52,140 − 4,44,600', inr(cr)]], title='Section 206(2)'),
              note('The credit can be set off in a later year when regular tax exceeds AMT, up to that excess, for 15 tax years.')],
          'checks': list(ck3)}

    concepts = [
        C('c1', T1, [
            'Steps to total income: decide residential status; classify income under the five heads; compute each head with its charging, deeming, exemption and deduction rules; club income of spouse, minor child and others where required; set off and carry forward losses; reach gross total income; subtract Chapter VIII deductions.',
            'An individual\'s income can arise personally, as a partner (salary and interest allowed to the firm are business income; the share of profit is exempt), as an HUF member (share of HUF income is exempt) and through clubbing of income of other persons.',
            'Regime matters at every step: the default regime allows a ₹75,000 standard deduction but no HRA, no house-property interest on a self-occupied house and almost no Chapter VIII deductions; the optional regime allows ₹50,000 standard deduction and the usual exemptions and deductions.',
            'An Indian citizen not liable to tax elsewhere because of domicile or residence, with Indian income above ₹15 lakh, is deemed resident — and treated as not ordinarily resident.'],
          'Total income is built step by step — skipping clubbing or set-off changes everything that follows.',
          'A partner\'s ₹4 lakh share of firm profit stays out of his total income, but his ₹1 lakh salary from the firm is taxed as business income.'),
        C('c2', T2, [
            'Default regime slabs (s. 202(1)): up to ₹4 lakh nil; ₹4–8 lakh 5%; ₹8–12 lakh 10%; ₹12–16 lakh 15%; ₹16–20 lakh 20%; ₹20–24 lakh 25%; above ₹24 lakh 30%. Optional regime: up to ₹2.5 lakh nil (₹3 lakh at 60+, ₹5 lakh at 80+); ₹2.5–5 lakh 5%; ₹5–10 lakh 20%; above ₹10 lakh 30%.',
            'Rebate u/s 156 for residents: default regime — up to ₹60,000 where total income is up to ₹12 lakh; just above ₹12 lakh, tax is limited to the income above ₹12 lakh (marginal relief). Optional regime — up to ₹12,500 where total income is up to ₹5 lakh. The default-regime rebate is not available against tax on special-rate capital gains; the optional-regime rebate is not available against tax on gains under section 198.',
            'Surcharge on income-tax: 10% above ₹50 lakh, 15% above ₹1 crore, 25% above ₹2 crore (the maximum under the default regime), and 37% above ₹5 crore under the optional regime; dividend and special-rate capital gains bear at most 15%. Marginal relief applies at each threshold.',
            'Health and education cess of 4% is added to income-tax plus surcharge for every assessee.'],
          'Slabs, then rebate, then surcharge, then cess — in that order every time.',
          'Total income of ₹11,90,000 under the default regime: tax ₹59,000, fully wiped out by the rebate.'),
        C('c3', T3, [
            'Section 206(2): a non-corporate person who claims a Part C Chapter VIII deduction (other than section 149) or the investment-linked deduction under section 46 must pay at least Alternate Minimum Tax — 18.5% of adjusted total income plus surcharge and cess.',
            'Adjusted total income = total income + such Part C deductions (at this level: sections 144, 146, 151 and 152) + the section 46 deduction less the normal depreciation that would have been allowed on that asset.',
            'AMT does not apply to anyone taxed under the default regime, or to individuals, HUFs, AOPs, BOIs and artificial juridical persons whose adjusted total income is ₹20 lakh or less.',
            'Credit: the excess of AMT over regular tax is carried forward for 15 tax years and set off in a year when regular tax exceeds AMT, but only up to that excess.'],
          'AMT is a floor: incentives may lower tax, but not below 18.5% of the income before those incentives.',
          'Adjusted total income of ₹19 lakh means no AMT at all for an individual, whatever deductions are claimed.'),
        C('c4', T4, [
            'An individual without business or professional income can compare both regimes every year and choose by filing the return by the due date.',
            'One with business or professional income who wants to leave the default regime must exercise the option in the prescribed form by the due date; having opted out, he can return to the default regime only once.',
            'Optimisation is lawful planning within the Act: compare tax including AMT under the optional regime with tax under the default regime, and pick the lower — not reduce income artificially.'],
          'The best regime is a calculation, not a guess.',
          'A salaried person with large home-loan interest and deductions may save under the optional regime; most others save under the default one.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Regime advice for employees', 'role': 'Article assistant',
         'situation': 'An HR team asks for a simple tool to tell employees which regime to choose.',
         'steps': ['List each employee\'s exemptions and deductions available only in the optional regime.', 'Compute tax both ways, with rebate and cess.', 'Show the difference.', 'Remind them the choice can be made again when filing.'],
         'takeaway': 'The break-even depends on how many optional-regime deductions a person actually has.'},
        {'id': 'j2', 'title': 'AMT check for a business client', 'role': 'Tax associate',
         'situation': 'A proprietor claims a large section 46 deduction.',
         'steps': ['Confirm he has opted out of the default regime.', 'Compute adjusted total income.', 'Compare AMT with regular tax.', 'Record any credit for future years.'],
         'takeaway': 'Always test AMT when a Part C or section 46 deduction is claimed.'},
    ]

    mcqs = [
        Q('m1', 'Under the default regime, tax on total income of ₹16,00,000 (before rebate and cess) is:', ['₹1,20,000', '₹1,00,000', '₹1,40,000', '₹60,000'], 0,
          '₹20,000 (4–8 lakh at 5%) + ₹40,000 (8–12 lakh at 10%) + ₹60,000 (12–16 lakh at 15%) = ₹1,20,000. No rebate, as income is well above ₹12 lakh. In practice: add 4% cess.', 'c2', T2, 'moderate', check=120000),
        Q('m2', 'A resident under the default regime has total income of ₹11,80,000, all salary. Tax payable:', ['Nil', '₹58,000', '₹60,320', '₹2,000'], 0,
          'Tax is ₹58,000, and total income does not exceed ₹12 lakh, so the rebate of up to ₹60,000 removes it entirely. In practice: cess also becomes nil.', 'c2', T2, 'moderate'),
        Q('m3', 'Under the optional regime, the rebate u/s 156 is available when total income does not exceed:', ['₹5,00,000', '₹7,00,000', '₹12,00,000', '₹3,00,000'], 0,
          'In the optional regime a resident individual gets a rebate of the tax or ₹12,500, whichever is lower, if total income is up to ₹5 lakh. In practice: the default regime limit is ₹12 lakh.', 'c2', T2, check=500000),
        Q('m4', 'The highest surcharge rate under the default regime is:', ['25%', '37%', '15%', '10%'], 0,
          'Under the default regime, surcharge stops at 25% for income above ₹2 crore; 37% applies above ₹5 crore only under the optional regime. In practice: dividends and special-rate gains bear at most 15%.', 'c2', T2, check=25),
        Q('m5', 'Health and education cess is levied at:', ['4% of income-tax plus surcharge', '4% of income-tax only', '2% of total income', '3% of tax'], 0,
          'Cess is 4% on income-tax as increased by surcharge, for all assessees. In practice: compute it last.', 'c2', T2),
        Q('m6', 'AMT is levied at what rate of adjusted total income (before surcharge and cess)?', ['18.5%', '15%', '20%', '30%'], 0,
          'AMT for non-corporate persons is 18.5% of adjusted total income, plus surcharge and cess. In practice: compare it with regular tax.', 'c3', T3, check=18.5),
        Q('m7', 'AMT does NOT apply to an individual whose adjusted total income does not exceed:', ['₹20 lakh', '₹50 lakh', '₹12 lakh', '₹10 lakh'], 0,
          'Individuals, HUFs, AOPs, BOIs and artificial juridical persons are outside AMT if adjusted total income is up to ₹20 lakh. Default-regime taxpayers are outside it altogether. In practice: test this first.', 'c3', T3, check=20),
        Q('m8', 'AMT credit can be carried forward for:', ['15 tax years', '8 tax years', '10 tax years', 'Indefinitely'], 0,
          'Credit of AMT over regular tax is carried forward for the 15 tax years after the year it arises and set off when regular tax exceeds AMT. In practice: keep a credit register.', 'c3', T3, check=15),
        Q('m9', 'Which is NOT allowed to a salaried employee under the default regime?', ['HRA exemption', 'Standard deduction of ₹75,000', 'Employer\'s NPS contribution deduction', 'Rebate up to ₹60,000'], 0,
          'HRA exemption needs the optional regime. The default regime still gives ₹75,000 standard deduction, the employer NPS deduction and the ₹60,000 rebate. In practice: compare both before choosing.', 'c4', T4),
        Q('m10', 'An individual with business income who has opted out of the default regime may return to it:', ['Only once', 'Every year', 'Never', 'Twice'], 0,
          'Business taxpayers opt out through a prescribed form by the due date; after that they may come back to the default regime only once. Salaried people can switch each year. In practice: plan the switch carefully.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Total income', 1, 'computation', 'standard deduction', nums=[1240000]),
           S('s2', 'Slab tax', 1, 'computation', 'slab|15%', nums=[tax]),
           S('s3', 'Marginal relief rebate', 1, 'computation', 'rebate', nums=[reb]),
           S('s4', 'Tax with cess', 1, 'computation', 'cess', nums=[pay])],
          ['Apply marginal relief just above ₹12 lakh.'], ['Denying the rebate completely.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Optional total income', 2, 'computation', 'optional', nums=[opt_ti]),
           S('s2', 'Optional tax', 1, 'computation', 'optional', nums=[opt_tax]),
           S('s3', 'Default total income and tax', 2, 'computation', 'default', nums=[def_ti, def_tax]),
           S('s4', 'Advice', 1, 'concept', 'default')],
          ['Show both columns.'], ['Allowing house-loan interest in the default regime.'], ['Two-column table.'], pad='table', checks=list(ck2)),
        W('q3', 5, i3['q'], i3['solution'],
          [S('s1', 'Regular tax', 1, 'computation', 'regular', nums=[reg]),
           S('s2', 'Adjusted total income', 1, 'computation', 'adjusted', nums=[2350000]),
           S('s3', 'AMT', 2, 'computation', '18.5%', nums=[amt]),
           S('s4', 'Credit', 1, 'computation', 'credit', nums=[cr])],
          ['Check the ₹20 lakh limit first.'], ['Forgetting to add back the deduction.'], ['Step table.'], pad='table', checks=list(ck3)),
    ]

    viva = [
        V('v1', 'What is the order of steps after computing total income?',
          'Apply the slab or special rates, give the rebate under section 156 if eligible, add surcharge where income exceeds ₹50 lakh, then add 4% health and education cess.',
          [P('p1', 'Rebate before surcharge', 5, 'rebate'), P('p2', 'Cess last', 5, 'cess')], 'c2'),
        V('v2', 'How does marginal relief work just above ₹12 lakh in the default regime?',
          'If tax on income slightly above ₹12 lakh is more than the income in excess of ₹12 lakh, the rebate equals the difference, so tax payable equals that excess income.',
          [P('p1', 'Excess over 12 lakh', 6, '12 lakh|12,00,000'), P('p2', 'Difference as rebate', 4, 'difference|rebate')], 'c2'),
        V('v3', 'What is adjusted total income for AMT?',
          'Total income increased by the Part C deductions claimed (other than section 149) and by the section 46 deduction less depreciation that would otherwise be allowed.',
          [P('p1', 'Part C added back', 5, 'part c|deduction'), P('p2', 'Section 46 adjustment', 5, '46|depreciation')], 'c3'),
        V('v4', 'Who is outside the AMT provisions?',
          'Persons taxed under the default regime, and individuals, HUFs, AOPs, BOIs and artificial juridical persons with adjusted total income up to ₹20 lakh.',
          [P('p1', 'Default regime', 5, 'default'), P('p2', '₹20 lakh', 5, '20 lakh')], 'c3'),
        V('v5', 'How often can a salaried person change regime?',
          'Every year, since a person without business income chooses the regime each time he files the return by the due date.',
          [P('p1', 'Every year', 6, 'every year|each year'), P('p2', 'Return by due date', 4, 'due date|return')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'The Iyer siblings', 'difficulty': 'moderate',
              'case': 'For tax year 2026-27 (all residents, default regime unless stated): Deepa, 29, has total income of ₹9,00,000; Karthik, 41, has total income of ₹26,00,000; and Meera, 66, has opted out of the default regime with total income of ₹4,70,000.',
              'mcqs': [
                  M('k1a', 'Deepa\'s tax payable:', ['Nil', '₹30,000', '₹31,200', '₹10,000'], 0,
                    'Tax on ₹9 lakh is ₹30,000 (₹20,000 + ₹10,000), which the rebate of up to ₹60,000 removes, since income is not above ₹12 lakh. In practice: she must still file, as income exceeds ₹4 lakh.', 'core', topic=T2),
                  M('k1b', 'Karthik\'s tax before cess:', ['₹3,60,000', '₹3,00,000', '₹4,20,000', '₹3,30,000'], 0,
                    'Slab tax: 20,000 + 40,000 + 60,000 + 80,000 + 1,00,000 = 3,00,000 up to ₹24 lakh, plus 30% of ₹2 lakh = 60,000; total ₹3,60,000. No surcharge below ₹50 lakh. In practice: cess takes it to ₹3,74,400.', 'moderate', check=360000, topic=T2),
                  M('k1c', 'Meera\'s tax under the optional regime:', ['Nil', '₹8,500', '₹11,000', '₹12,500'], 0,
                    'As a senior citizen her exemption limit is ₹3 lakh; tax is 5% of ₹1,70,000 = ₹8,500, and the rebate (income up to ₹5 lakh) wipes it out. In practice: the rebate is the lower of tax and ₹12,500.', 'moderate', topic=T2),
                  M('k1d', 'Would AMT apply to Karthik?', ['No, he is taxed under the default regime', 'Yes, as income exceeds ₹20 lakh', 'Yes, at 18.5%', 'Only if he has business income'], 0,
                    'AMT never applies to a person whose tax is computed under the default regime, whatever his income. In practice: AMT is an optional-regime issue.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch09', 1, 'Income Tax Liability - Computation and Optimisation',
                ['Compute total income of an individual by following the prescribed steps.',
                 'Apply slab rates, rebate with marginal relief, surcharge and cess under both regimes.',
                 'Apply AMT and compute the tax credit.',
                 'Compare both regimes and advise the lower-tax option.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 60}, 'prereq': ['int-p3-a-ch08-u01'],
                 'exam_tip': 'In comparison questions, set up two columns from the start; the examiner rewards a clear side-by-side presentation.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Status → heads → clubbing → set-off → GTI → deductions → total income.',
                             'Default slabs 0/5/10/15/20/25/30%; rebate ₹60,000 up to ₹12 lakh with marginal relief.',
                             'Optional slabs 0/5/20/30%; rebate ₹12,500 up to ₹5 lakh.',
                             'Surcharge 10/15/25% (37% only in optional regime); cess 4%.',
                             'AMT 18.5% of adjusted total income; not for default regime or ATI ≤ ₹20 lakh; credit 15 years.'],
                 'remember': ['Share of firm profit and HUF income are exempt for the partner or member.', 'Business taxpayers can return to the default regime only once.'],
                 'traps': ['Default-regime rebate not against special-rate capital gains tax.', 'House-loan interest on self-occupied property only in the optional regime.']},
                [('Default rebate', '₹60,000; TI ≤ ₹12 lakh'), ('Optional rebate', '₹12,500; TI ≤ ₹5 lakh'), ('AMT', '18.5%; ATI > ₹20 lakh'), ('Cess', '4%')],
                viva, cases)
