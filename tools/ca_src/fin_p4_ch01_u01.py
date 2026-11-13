"""CA Final · Paper 4 Direct Tax Laws & International Taxation · Chapter 1 Basic Concepts.
Scope follows the ICAI study material under the Income-tax Act, 2025 (T.Y. 2026-27); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch01-u01'
T1 = 'Components of income-tax law and the 2025 Act'
T2 = 'Rules of interpretation'
T3 = 'Charge of tax, tax year and key definitions'
T4 = 'Rates of tax, surcharge, cess and marginal relief'


def build():
    ck = Checks()
    d = ck.add('0+400000*0.05+400000*0.10+300000*0.15', 'Tax under default regime on ₹15 lakh (₹)')
    dc = ck.add('(0+400000*0.05+400000*0.10+300000*0.15)*1.04', 'Tax with 4% cess, default regime (₹)')
    o = ck.add('112500+500000*0.30', 'Tax under optional regime on ₹15 lakh (₹)')
    oc = ck.add('(112500+500000*0.30)*1.04', 'Tax with 4% cess, optional regime (₹)')
    i1 = {'id': 'i1', 'title': 'Default or optional regime?', 'difficulty': 'core', 'minutes': 8,
          'q': 'Asha, a resident individual aged 45, has total income of ₹15,00,000 for T.Y. 2026-27 under both regimes (assume no deductions differ). Compute tax including health and education cess under the default regime (section 202) and the optional regime.',
          'solution': [table(['Regime', 'Working', '₹'], [
              ['Default — slabs', '4L nil; 4–8L 5% = 20,000; 8–12L 10% = 40,000; 12–15L 15% = 45,000', inr(d)],
              ['Default — with cess', '1,05,000 × 1.04', inr(dc)],
              ['Optional — slabs', '1,12,500 + 30% × (15L − 10L)', inr(o)],
              ['Optional — with cess', '2,62,500 × 1.04', inr(oc)],
              ['Conclusion', 'Default regime is cheaper here', '—']], title='T.Y. 2026-27 rates')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Capital or revenue? Diversion or application?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Classify: (a) compensation received for cancellation of a business agency that was the main source of income; (b) compensation for loss of profit in a normal year; (c) a son paying, out of his salary, maintenance to his mother under a court decree; (d) a portion of family business income charged by a court decree in favour of a widow before it reaches the karta.',
          'solution': [table(['Item', 'Treatment'], [
              ['(a)', 'Capital receipt — loss of the source of income (subject to specific charging provisions)'],
              ['(b)', 'Revenue receipt — replaces profit'],
              ['(c)', 'Application of income — taxable in son\'s hands'],
              ['(d)', 'Diversion by overriding title — not income of the HUF']], title='Basic concepts')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Article 265 of the Constitution requires taxes to be levied only by authority of law; Parliament taxes income other than agricultural income under Entry 82 of the Union List.',
            'From 1 April 2026, income-tax is governed by the Income-tax Act, 2025 (23 chapters, 536 sections, 16 schedules), which replaced the Income-tax Act, 1961. Under section 536 (repeal and savings), proceedings, rights, assessments and appeals for tax years beginning before 1 April 2026 continue under the 1961 Act, while carried-forward losses, MAT/AMT credit and certain deductions continue subject to conditions.',
            'Other components: the annual Finance Act (rates in its First Schedule — Part IB for the current tax year, Part II for TDS, Part III for salary TDS and advance tax under the optional regime, Part IV for agricultural income), Income-tax Rules, 2026, notifications and circulars (binding on the department), and case laws.'],
          'The 2025 Act is the new law; the 1961 Act still governs older years.',
          'An assessment for T.Y. 2025-26 continues under the 1961 Act.'),
        C('c2', T2, [
            'Rules of interpretation help courts find the lawmakers\' intention. Literal rule: clear words are given their plain meaning. Mischief (Heydon\'s) rule: read the law to suppress the mischief it was meant to cure. Golden rule: depart from literal meaning only to avoid absurdity.',
            'Harmonious construction reconciles conflicting provisions; beneficial provisions are read liberally; taxing provisions are construed strictly, with doubts resolved in favour of the assessee; procedural provisions may operate retrospectively.',
            'Internal aids (definitions, explanations, provisos, headings) and external aids (speeches, committee reports, circulars) also assist interpretation.'],
          'Courts read tax law strictly but sensibly.',
          'An ambiguous charging provision is resolved in the taxpayer\'s favour.'),
        C('c3', T3, [
            'Section 4 is the charging section: every person\'s total income for a tax year bears income-tax at the rates fixed by the Finance Act or by the Act itself (for example section 202(1)), subject to its other provisions.',
            'Tax year (section 3) is the twelve-month financial year beginning 1 April; for a new business or source, it runs from setting up or commencement to 31 March. Income of a tax year is assessed after it ends, except for non-resident shipping, persons leaving India, AOPs formed for a particular event, persons likely to transfer property to avoid tax, and discontinued businesses.',
            'Key distinctions: capital vs revenue receipts and expenditure; diversion of income by overriding title (not income of the assessee) vs application of income (taxable). Definitions in section 2 cover person, assessee, income and others.'],
          'Charge, period and the nature of receipts set the base.',
          'A CA setting up practice on 1 July 2026 has tax year 1.7.2026 to 31.3.2027.'),
        C('c4', T4, [
            'Default regime (section 202) for individuals, HUFs, AOPs, BOIs and artificial juridical persons: nil up to ₹4 lakh; 5% to ₹8 lakh; 10% to ₹12 lakh; 15% to ₹16 lakh; 20% to ₹20 lakh; 25% to ₹24 lakh; 30% above, with certain exemptions and deductions foregone. Those opting out under section 202(4) use the optional regime slabs (nil to ₹2.5 lakh; 5% to ₹5 lakh; 20% to ₹10 lakh; 30% above; higher exemption for senior and very senior citizens).',
            'Rebate under section 156 reduces tax for resident individuals with lower incomes (e.g. up to ₹60,000 under the default regime for total income up to ₹12 lakh), not available against certain special-rate income.',
            'Surcharge applies above income thresholds; health and education cess is 4% of tax plus surcharge for all assessees. Marginal relief ensures extra tax and surcharge caused by crossing a threshold does not exceed the extra income.'],
          'Compute slab tax, then rebate, surcharge, cess and marginal relief.',
          'At ₹15 lakh, default regime tax with cess is ₹1,09,200.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Regime choice for salaried clients', 'role': 'Tax consultant',
             'situation': 'Several salaried clients ask whether to opt out of the default regime.',
             'steps': ['Compute income under both regimes.', 'Apply rebate, surcharge and cess.', 'Compare and recommend.', 'Explain transition rules under the 2025 Act.'],
             'takeaway': 'Run both computations before choosing a regime.'}]

    mcqs = [
        Q('m1', 'The Income-tax Act, 2025 came into force on:', ['1 April 2026', '1 April 2025', '1 January 2026', '1 April 2027'], 0,
          'Replaced the 1961 Act. In practice: older years still under 1961 Act.', 'c1', T1),
        Q('m2', 'The charging section under the 2025 Act is:', ['Section 4', 'Section 2', 'Section 202', 'Section 536'], 0,
          'Charge on total income of the tax year. In practice: rates via Finance Act.', 'c3', T3),
        Q('m3', '"Tax year" is defined in:', ['Section 3', 'Section 4', 'Section 2(77)', 'Section 156'], 0,
          'Replaces previous year and assessment year. In practice: FY basis.', 'c3', T3),
        Q('m4', 'Under the default regime, income up to which amount is taxed at nil rate?', ['Four lakh rupees', 'Two and a half lakh rupees', 'Three lakh rupees', 'Five lakh rupees'], 0,
          'Section 202 slabs. In practice: rebate up to ₹12 lakh.', 'c4', T4),
        Q('m5', 'Health and education cess is levied at:', ['Four percent of tax plus surcharge', 'Two percent', 'Three percent of income', 'Ten percent'], 0,
          'All assessees. In practice: last step.', 'c4', T4),
        Q('m6', 'Income charged by a decree before it reaches the assessee is:', ['Diversion by overriding title', 'Application of income', 'Capital receipt', 'Exempt by statute'], 0,
          'Not the assessee\'s income. In practice: test timing.', 'c3', T3),
        Q('m7', 'The mischief rule is also known as:', ['Heydon\'s rule', 'Golden rule', 'Literal rule', 'Harmonious rule'], 0,
          'Purposive construction. In practice: legislative intent.', 'c2', T2),
        Q('m8', 'Proceedings for tax years beginning before 1 April 2026 are governed by:', ['The Income-tax Act, 1961', 'The 2025 Act only', 'Neither', 'GST law'], 0,
          'Section 536 savings. In practice: dual systems for some years.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Default regime', 3, 'computation', 'default', nums=[d, dc]), S('s2', 'Optional regime', 3, 'computation', 'optional', nums=[o, oc])],
          ['Show slabs.'], ['Applying rebate above ₹12 lakh.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Capital vs revenue', 2.5, 'concept', 'capital|revenue'), S('s2', 'Diversion vs application', 2.5, 'concept', 'diversion|application')],
          ['Give reasons.'], ['Treating decree payments out of salary as diversion.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What does section 536 provide?', 'Repeal of the 1961 Act with savings, so proceedings and rights for tax years beginning before 1 April 2026 continue under the old Act.',
          [P('p1', 'Repeal', 5, 'repeal'), P('p2', 'Savings for earlier years', 5, 'earlier|before')], 'c1'),
        V('v2', 'Name three rules of interpretation.', 'The literal rule, the mischief rule and the golden rule.',
          [P('p1', 'Literal and mischief', 5, 'literal|mischief'), P('p2', 'Golden', 5, 'golden')], 'c2'),
        V('v3', 'What is the tax year for a newly set-up business?', 'From the date of setting up to the following 31 March.',
          [P('p1', 'Date of setting up', 5, 'setting up'), P('p2', '31 March', 5, 'march')], 'c3'),
        V('v4', 'Distinguish diversion and application of income.', 'Diversion by overriding title means income never reaches the assessee and is excluded; application means the assessee spends its own income, which remains taxable.',
          [P('p1', 'Overriding title', 5, 'overriding'), P('p2', 'Remains taxable', 5, 'taxable')], 'c3'),
        V('v5', 'What is marginal relief?', 'Relief ensuring that additional tax and surcharge on crossing a threshold do not exceed the additional income.',
          [P('p1', 'Threshold', 5, 'threshold'), P('p2', 'Not exceed extra income', 5, 'additional income|exceed')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Rohan Mehta', 'difficulty': 'moderate',
              'case': 'Rohan, a resident individual aged 30, earns total income of ₹11,80,000 for T.Y. 2026-27 under the default regime, all taxable at normal slab rates. He also asks whether his T.Y. 2025-26 reassessment will be under the new Act.',
              'mcqs': [
                  M('k1a', 'Tax on ₹11,80,000 before rebate (₹):', ['58,000', '60,000', '78,000', '38,000'], 0,
                    '20,000 + 10% × 3,80,000 = 58,000. In practice: rebate next.', 'core', check=58000, topic=T4),
                  M('k1b', 'Rebate under section 156 (₹):', ['58,000', '60,000', '12,500', 'Nil'], 0,
                    'Income ≤ ₹12 lakh; rebate limited to tax. In practice: resident individuals only.', 'core', check=58000, topic=T4),
                  M('k1c', 'Net tax payable (₹):', ['0', '2,320', '58,000', '60,320'], 0,
                    'Tax fully rebated, so no cess. In practice: file return anyway if required.', 'core', check=0, topic=T4),
                  M('k1d', 'The T.Y. 2025-26 reassessment is governed by:', ['The Income-tax Act, 1961', 'The 2025 Act', 'Both equally', 'Neither'], 0,
                    'Section 536. In practice: older year rules.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch01', 1, 'Basic Concepts',
                ['Describe the components of income-tax law and the transition to the 2025 Act.',
                 'Apply rules of interpretation.',
                 'Apply the charge of tax, tax year and key definitions.',
                 'Compute tax using rates, rebate, surcharge, cess and marginal relief.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 25}, 'prereq': [],
                 'exam_tip': 'State the regime first; compute slab tax, rebate, surcharge, cess in that order.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Income-tax Act, 2025 from 1 April 2026; section 536 savings.',
                             'Section 4 charge; section 3 tax year.',
                             'Default regime u/s 202; opt out u/s 202(4).',
                             'Rebate u/s 156; surcharge; 4% cess; marginal relief.',
                             'Capital vs revenue; diversion vs application.'],
                 'remember': ['Older tax years stay under the 1961 Act.'],
                 'traps': ['Using "previous year/assessment year" for new-Act questions.']},
                [('Charging section', 'Section 4'), ('Tax year', 'Section 3'), ('Default regime', 'Section 202'), ('Rebate', 'Section 156')],
                viva, cases)
