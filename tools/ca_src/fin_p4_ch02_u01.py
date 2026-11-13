"""CA Final · Paper 4 · Chapter 2 Incomes which do not form part of Total Income.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch02-u01'
T1 = 'Exemption framework under section 11'
T2 = 'Agricultural income'
T3 = 'Partial integration of agricultural income'
T4 = 'Other exemptions in Schedules III and VII'
T5 = 'Disallowance of expenditure on exempt income'


def build():
    ck = Checks()
    xn = ck.add('400000*0.05+400000*0.10+400000*0.15', 'Xn: tax on aggregate income ₹16,00,000 (₹)')
    yn = ck.add('300000*0.05', 'Yn: tax on ₹7,00,000 (agri + basic limit) (₹)')
    zn = ck.add('(400000*0.05+400000*0.10+400000*0.15)-300000*0.05', 'Zn = Xn - Yn (₹)')
    tl = ck.add('((400000*0.05+400000*0.10+400000*0.15)-300000*0.05)*1.04', 'Tax with 4% cess (₹)')
    i1 = {'id': 'i1', 'title': 'Partial integration under the default regime', 'difficulty': 'core', 'minutes': 8,
          'q': 'Priya, a resident aged 50, has non-agricultural total income of ₹13,00,000 and net agricultural income of ₹3,00,000. She has not opted out of the default regime for T.Y. 2026-27. Compute her tax liability.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Conditions', 'Net agri income > ₹5,000; non-agri income > ₹4,00,000', 'Met'],
              ['Xn', 'Tax on ₹16,00,000: 20,000 + 40,000 + 60,000', inr(xn)],
              ['Yn', 'Tax on ₹7,00,000 (3,00,000 + 4,00,000): 5% × 3,00,000', inr(yn)],
              ['Zn', 'Xn − Yn (no rebate: total income above ₹12 lakh)', inr(zn)],
              ['Add cess @4%', '1,05,000 × 1.04', inr(tl)]], title='Zn = Xn − Yn')],
          'checks': list(ck)}

    c2 = Checks()
    ag = c2.add('1000000*0.65', 'Agricultural part of rubber income (₹)')
    bi = c2.add('1000000*0.35', 'Business part of rubber income (₹)')
    ind = c2.add('4000000*0.01', 'Indirect expenditure at 1% (₹)')
    dis = c2.add('min(50000+4000000*0.01,75000)', 'Disallowance capped at expenditure claimed (₹)')
    i2 = {'id': 'i2', 'title': 'Composite income and section 14', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Vardhan Plantations (a firm) earns ₹10,00,000 from selling rubber products it processes from its own plantation in India. Separately, it holds tax-free bonds; the AO is not satisfied with its claim and applies the prescribed method. Direct expenditure on exempt income is ₹50,000; the annual average of monthly averages of investments yielding exempt income is ₹40,00,000; total expenditure claimed in its accounts is ₹75,000. Compute the agricultural/business split and the disallowance.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Agricultural income (exempt)', '65% × 10,00,000', inr(ag)],
              ['Business income (taxable)', '35% × 10,00,000', inr(bi)],
              ['Indirect expenditure', '1% × 40,00,000', inr(ind)],
              ['Disallowance', 'Lower of (50,000 + 40,000) and 75,000 claimed', inr(dis)]], title='Rule-based apportionment')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 11 of the Income-tax Act, 2025 excludes specified incomes from total income through Schedules II to VII. Schedules II to VI list types of income that are exempt subject to conditions; Schedule VII lists persons whose entire total income is exempt.',
            'Exempt income never enters gross total income. Contrast deductions under Chapter VIII: that income is first included in gross total income and then deducted, so it still matters for things like aggregation tests.',
            'Several exemptions are studied with the related head — for example, life insurance receipts, NPS and Sukanya Samriddhi withdrawals, minor\'s income clubbing relief, and income of investment funds and business trusts.'],
          'Exempt income is kept out; deductible income goes in and comes out.',
          'Interest on a tax-free bond is excluded under a Schedule; a Chapter VIII deduction is claimed against gross total income.'),
        C('c2', T2, [
            'Agricultural income is exempt (Schedule II, Sl. No. 1) because the Constitution leaves its taxation to the States. Section 2(5) covers (a) rent or revenue from land in India used for agriculture; (b) income from agriculture, from processes ordinarily used by a cultivator to make produce marketable, and from selling such produce; (c) income from farm buildings meeting conditions; and (d) income from saplings or seedlings grown in a nursery.',
            'Farm-building income qualifies only if the building is on or near the land, is needed by the cultivator or rent receiver because of their connection with the land, and the land is assessed to land revenue or a local rate or, if not, lies outside urban limits in section 2(22)(iii). Land is urban if within a municipality or cantonment with population of 10,000 or more, or within 2 km, 6 km or 8 km aerially of one with population above 10,000, 1 lakh or 10 lakh respectively.',
            'Indirect connection with land is not enough: dairy farming, poultry, butter-making in a factory, commission computed on a company\'s profits, regular commercial milk sales, film-shooting rent and forest trees of spontaneous growth do not give agricultural income. Gains on transferring urban agricultural land are capital gains. Composite incomes are split by rules: rubber 65% agricultural; coffee grown and cured 75%; coffee grown, cured, roasted and ground 60%; tea grown and manufactured 60%.'],
          'Real tilling, basic operations and a link with Indian land are the core.',
          'Rent for letting a field to a film crew is taxable.'),
        C('c3', T3, [
            'Partial integration applies to individuals, HUFs, AOPs, BOIs and artificial juridical persons when net agricultural income exceeds ₹5,000 and non-agricultural income exceeds the basic exemption limit (₹4 lakh default; under the optional regime ₹2.5 lakh, ₹3 lakh for residents aged 60–79, ₹5 lakh for residents aged 80 or more).',
            'Tax = Xn − Yn, where Xn is tax on total income plus net agricultural income, and Yn is tax on net agricultural income plus the basic exemption limit, both at the applicable regime\'s rates.',
            'The result is increased by surcharge where applicable, reduced by the section 156 rebate if available, and then increased by 4% cess. Companies, firms, LLPs, co-operatives and local authorities are outside this method.'],
          'Agricultural income pushes other income into higher slabs.',
          'Non-agri ₹13 lakh plus agri ₹3 lakh gives tax of ₹1,05,000 before cess under the default regime.'),
        C('c4', T4, [
            'Schedule III examples: a partner\'s share in a separately assessed firm\'s income (exempt even if the firm\'s taxable income is nil due to exemptions or deductions); disaster compensation from the Central or State Government or a local authority, except for loss already deducted; daily allowances of MPs and MLAs and specified constituency allowances.',
            'Further: pension and family pension of gallantry award winners who were government employees; disability pension of armed forces members invalided out due to service; income of Scheduled Tribe members in specified areas and of Sikkimese individuals from those regions or from dividend/interest; Board subsidies for replanting tea, rubber, coffee, cardamom; specified income of local authorities.',
            'Schedule VII makes the whole income of persons exempt — e.g. universities, educational institutions and hospitals existing solely for non-profit purposes that are wholly or substantially Government-financed, or whose aggregate annual receipts do not exceed ₹5 crore (with anonymous donations taxed under section 337).'],
          'Some schedules exempt an income; Schedule VII exempts a person.',
          'A small non-profit school with receipts of ₹3 crore pays no income-tax.'),
        C('c5', T5, [
            'Section 14(1): no deduction is allowed for expenditure incurred in relation to income not forming part of total income. Section 14(3) applies the rule even where the exempt income did not accrue or was not received in that year.',
            'Under section 14(2), if the AO is not satisfied with the assessee\'s claim, having regard to its accounts, he computes the expenditure under Rule 14: direct expenditure plus 1% of the annual average of monthly averages of opening and closing values of exempt-income investments, capped at the total expenditure claimed.',
            'The disallowance relates only to income excluded under the exemption provisions, not to income included and then deducted under Chapter VIII.'],
          'No double benefit: exempt income and a deduction for its cost.',
          'Interest paid on borrowings used to buy tax-free bonds is disallowed.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Return for a farmer-professional', 'role': 'Tax associate',
             'situation': 'A doctor also owns a mango orchard and a farmhouse near a town.',
             'steps': ['Test each receipt against section 2(5).', 'Check urban-land limits for the farmhouse.', 'Apply partial integration.', 'Disclose agricultural income in the return.'],
             'takeaway': 'Exempt yet relevant for rate purposes.'}]

    mcqs = [
        Q('m1', 'Schedule VII to section 11 deals with:', ['Persons whose total income is exempt', 'Incomes of salaried employees', 'Deductions from GTI', 'Rates of surcharge'], 0,
          'Person-based exemptions. In practice: check conditions yearly.', 'c1', T1),
        Q('m2', 'Which is agricultural income?', ['Income from saplings grown in a nursery', 'Income from poultry farming', 'Rent for film shooting on farmland', 'Profit on sale of urban farmland'], 0,
          'Section 2(5)(d). In practice: nursery income qualifies.', 'c2', T2),
        Q('m3', 'Land outside municipal limits is urban if the municipality has population above one lakh up to ten lakh and the land is within (aerially):', ['Six kilometres', 'Two kilometres', 'Eight kilometres', 'Ten kilometres'], 0,
          'Section 2(22)(iii)(B). In practice: aerial, not road distance.', 'c2', T2),
        Q('m4', 'Agricultural share of income from rubber grown and processed in India is:', ['Sixty-five percent', 'Sixty percent', 'Seventy-five percent', 'Forty percent'], 0,
          'Composite income rule. In practice: rest is business income.', 'c2', T2),
        Q('m5', 'Partial integration does NOT apply to:', ['A company', 'An individual', 'A HUF', 'A BOI'], 0,
          'Entities with flat rates are excluded. In practice: check status first.', 'c3', T3),
        Q('m6', 'For partial integration, net agricultural income must exceed:', ['Five thousand rupees', 'Fifty thousand rupees', 'Four lakh rupees', 'Nil'], 0,
          'First condition. In practice: plus non-agri threshold.', 'c3', T3),
        Q('m7', 'Disaster compensation from a State Government to an individual is:', ['Exempt, except for loss already deducted', 'Fully taxable', 'Taxable as capital gains', 'Exempt only for companies'], 0,
          'Schedule III. In practice: no double benefit.', 'c4', T4),
        Q('m8', 'Indirect expenditure under Rule 14 is computed at:', ['One percent of average exempt-income investments', 'Half percent of total assets', 'Two percent of exempt income', 'Ten percent of interest'], 0,
          'Plus direct expenditure, capped at total claimed. In practice: monthly averages.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Conditions and Xn', 3, 'computation', 'aggregate', nums=[xn]), S('s2', 'Yn, Zn and cess', 3, 'computation', 'cess', nums=[yn, zn, tl])],
          ['State both conditions.'], ['Adding agricultural income to total income for cess.'], ['Formula first.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Rubber split', 3, 'computation', 'rubber', nums=[ag, bi]), S('s2', 'Section 14 disallowance', 3, 'computation', 'disallowance', nums=[dis])],
          ['Apply the cap.'], ['Ignoring the cap at expenditure claimed.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Why is agricultural income exempt from central income-tax?', 'Because the Constitution gives the power to tax agricultural income to the States, so Parliament leaves it out of total income.',
          [P('p1', 'Constitution', 5, 'constitution'), P('p2', 'States', 5, 'state')], 'c2'),
        V('v2', 'Is income from regular sale of milk from a farm agricultural income?', 'It is business income when sales are regular and commercial, since dairy activity is only indirectly connected with land.',
          [P('p1', 'Business income', 5, 'business'), P('p2', 'Indirect link', 5, 'indirect')], 'c2'),
        V('v3', 'State the partial integration formula.', 'Tax equals tax on aggregate income minus tax on net agricultural income increased by the basic exemption limit.',
          [P('p1', 'Aggregate income', 5, 'aggregate'), P('p2', 'Basic exemption limit', 5, 'exemption limit|basic')], 'c3'),
        V('v4', 'Is a partner\'s profit share taxable when the firm pays nil tax due to deductions?', 'It remains exempt in the partner\'s hands because the firm\'s income is taxed only in the firm.',
          [P('p1', 'Exempt', 5, 'exempt'), P('p2', 'Taxed in firm', 5, 'firm')], 'c4'),
        V('v5', 'Does section 14 apply if no exempt income was earned in the year?', 'Yes, section 14(3) applies the disallowance even where the exempt income did not accrue or was received in another year.',
          [P('p1', 'Applies', 5, 'yes|applies'), P('p2', 'Section 14(3)', 5, '14\\(3\\)|accrue')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Kaveri Estates', 'difficulty': 'moderate',
              'case': 'Kaveri, a resident individual, grows coffee in Karnataka. She sells coffee grown, cured, roasted and ground by her, earning ₹20,00,000. She also lets a farmhouse on her rural land to a resort for ₹3,00,000 and receives a Coffee Board replanting subsidy under a notified scheme.',
              'mcqs': [
                  M('k1a', 'Business income from the coffee sale (₹):', ['8,00,000', '5,00,000', '12,00,000', '20,00,000'], 0,
                    '40% of ₹20 lakh. In practice: 60% agricultural.', 'core', check=800000, topic=T2),
                  M('k1b', 'Agricultural income from the coffee sale (₹):', ['12,00,000', '15,00,000', '8,00,000', 'Nil'], 0,
                    '60% of ₹20 lakh. In practice: used for partial integration.', 'core', check=1200000, topic=T2),
                  M('k1c', 'Rent from letting the farmhouse to a resort is:', ['Not agricultural income', 'Agricultural income', 'Exempt under Schedule VII', 'A capital receipt'], 0,
                    'Building used for non-agricultural purposes. In practice: taxable.', 'core', topic=T2),
                  M('k1d', 'The Coffee Board replanting subsidy is:', ['Exempt with the Board certificate', 'Taxable business income', 'Agricultural income', 'Deductible from GTI'], 0,
                    'Schedule III. In practice: file certificate with return.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch02', 1, 'Incomes which do not form part of Total Income',
                ['Distinguish exemptions under section 11 from Chapter VIII deductions.',
                 'Determine agricultural income under section 2(5).',
                 'Compute tax using partial integration.',
                 'Apply key exemptions in Schedules III and VII.',
                 'Compute disallowance under section 14 and Rule 14.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['fin-p4-ch01-u01'],
                 'exam_tip': 'For agricultural income, test each limb of section 2(5) before applying partial integration.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 11 with Schedules II–VII.', 'Agricultural income under section 2(5).', 'Partial integration Zn = Xn − Yn.',
                             'Composite income rules: rubber 65%, coffee 75%/60%, tea 60% agricultural.', 'Section 14: Rule 14 at 1% plus direct, capped.'],
                 'remember': ['Urban land distance is measured aerially.'],
                 'traps': ['Treating poultry or dairy income as agricultural.']},
                [('Agricultural income', 'Section 2(5)'), ('Exemptions', 'Section 11'), ('Exempt-income expenses', 'Section 14')],
                viva, cases)
