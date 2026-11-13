"""CA Final · Paper 2 Advanced Financial Management · Chapter 3 Advanced Capital Budgeting Decisions.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch03-u01'
T1 = 'Current trends: inflation, technology and government policy'
T2 = 'Statistical measures of project risk'
T3 = 'Risk-adjusted discount rate and certainty equivalents'
T4 = 'Sensitivity, scenario and simulation analysis'
T5 = 'Replacement decisions and adjusted present value'


def build():
    ck = Checks()
    nom = ck.add('round((1.08*1.05-1)*100,2)', 'Nominal discount rate (%)')
    ce = ck.add('round(120*0.9/1.06+150*0.8/1.06**2-180,2)', 'NPV using certainty equivalents (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Inflation and certainty equivalents', 'difficulty': 'moderate', 'minutes': 9,
          'q': '(a) The real required return is 8% and inflation is expected at 5%. What nominal rate should be used to discount money cash flows? (b) A project costs ₹180 lakh and is expected to return ₹120 lakh in year 1 and ₹150 lakh in year 2. Certainty-equivalent coefficients are 0.9 and 0.8; the risk-free rate is 6%. Compute NPV.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Nominal rate (Fisher)', '1.08 × 1.05 − 1', inr(nom) + '%'],
              ['Certain cash flow year 1', '120 × 0.9 = 108; ÷ 1.06', '101.89'],
              ['Certain cash flow year 2', '150 × 0.8 = 120; ÷ 1.06²', '106.80'],
              ['NPV', '101.89 + 106.80 − 180', '₹' + inr(ce) + ' lakh']], title='Fisher effect and CE approach')],
          'checks': list(ck)}

    ck2 = Checks()
    cf = ck2.add('4*(100-60)-60', 'Annual cash flow (₹ lakh)')
    npv = ck2.add('round((4*(100-60)-60)*3.7908-300,2)', 'Base-case NPV (₹ lakh)')
    sens = ck2.add('round(((4*(100-60)-60)-300/3.7908)/4/100*100,2)', 'Fall in selling price that makes NPV zero (%)')
    i2 = {'id': 'i2', 'title': 'Sensitivity of NPV to price', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'A project costs ₹300 lakh and runs 5 years. It sells 4 lakh units a year at ₹100 with variable cost ₹60 per unit and annual fixed costs of ₹60 lakh. Ignore tax; discount rate 10% (5-year annuity factor 3.7908). Compute the NPV and the percentage fall in selling price that would make NPV zero.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Annual cash flow', '4 × (100 − 60) − 60', '₹' + inr(cf) + ' lakh'],
              ['NPV', '100 × 3.7908 − 300', '₹' + inr(npv) + ' lakh'],
              ['Break-even annual cash flow', '300 ÷ 3.7908 = 79.14', '—'],
              ['Allowed fall per unit', '(100 − 79.14) ÷ 4 lakh units = ₹5.21', '—'],
              ['Sensitivity of selling price', '5.21 ÷ 100', inr(sens) + '%']], title='Sensitivity analysis')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Inflation must be treated consistently: discount nominal (money) cash flows at a nominal rate, or real cash flows at a real rate. The Fisher relation links them: (1 + nominal) = (1 + real) × (1 + inflation). Different items may inflate at different rates, and tax depreciation is not inflated, which reduces real value.',
            'Technological change shortens asset lives, raises obsolescence risk and may favour flexible or modular investments; it also creates opportunities for automation and cost savings.',
            'Government policy — tax rates, incentives, subsidies, import duties, environmental rules, foreign investment rules, repatriation limits — changes cash flows and risk, both for domestic and cross-border projects.'],
          'Match nominal with nominal and real with real.',
          'At 8% real and 5% inflation, the nominal rate is 13.4%, not 13%.'),
        C('c2', T2, [
            'Risk means variability of returns where probabilities can be estimated; uncertainty exists where they cannot. Risk in project returns arises from project-specific, company-specific, industry, market, competition, economic and international factors.',
            'Probability-based tools: expected cash flow = Σ (cash flow × probability); expected NPV; variance and standard deviation measure dispersion; the coefficient of variation (standard deviation ÷ expected value) compares risk per unit of return across projects of different sizes.',
            'Decision trees map sequential decisions and chance events, evaluating expected values backward from final outcomes.'],
          'Expected value tells you the average; standard deviation tells you the spread.',
          'A project with a lower coefficient of variation offers less risk per rupee of return.'),
        C('c3', T3, [
            'Risk-adjusted discount rate (RADR): add a risk premium to the risk-free rate (or WACC) for riskier projects, then discount expected cash flows. Simple and intuitive, but it assumes risk grows over time at a compound rate and the premium is subjective.',
            'Certainty equivalent (CE) approach: convert each risky cash flow into the certain amount the decision-maker would accept instead (multiply by a CE coefficient between 0 and 1), then discount at the risk-free rate. It separates time value from risk and allows different risk adjustments by year.',
            'Both approaches rely on judgement in setting the premium or coefficients; consistency across projects is essential.'],
          'Either raise the rate or shrink the cash flows — never both.',
          'A CE coefficient of 0.8 means ₹100 risky is worth ₹80 certain.'),
        C('c4', T4, [
            'Sensitivity analysis changes one variable at a time (sales volume, price, costs, discount rate, project life) to see how far it can move before NPV turns zero; the smaller the margin, the more critical the variable. It ignores interdependence and probabilities.',
            'Scenario analysis changes several variables together to build consistent best, base and worst cases, giving a range of possible NPVs.',
            'Simulation (Monte Carlo) assigns probability distributions to variables, draws random values many times and builds a distribution of NPVs. It handles complex interactions but needs good data and computing effort, and the output still needs judgement.'],
          'One variable at a time, a few stories, or thousands of runs.',
          'If NPV turns negative with a 5% price fall, price is a critical variable.'),
        C('c5', T5, [
            'Replacement decisions compare keeping an existing asset with replacing it, using incremental cash flows: new cost less sale value of old asset, changes in operating costs, tax effects of depreciation and differences in terminal values.',
            'Optimum replacement cycle: when an asset will be replaced repeatedly, compare alternatives with different lives using equivalent annual cost (EAC) — present value of costs ÷ annuity factor for the life; choose the lowest EAC.',
            'Adjusted present value (APV) separates investment and financing: APV = base-case NPV (discounting at the unlevered cost of equity, as if all-equity financed) + present value of financing side-effects, mainly the tax shield on interest (less issue costs, plus subsidised loan benefits).'],
          'Compare unequal lives by annual cost; value financing benefits separately with APV.',
          'A project with a slightly negative base NPV can be worthwhile once the debt tax shield is added.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Board paper for a new plant', 'role': 'Project finance analyst',
             'situation': 'The board must approve a ₹500 crore plant with uncertain demand.',
             'steps': ['Build nominal cash flows with consistent inflation.', 'Compute expected NPV and its spread.', 'Run sensitivity and scenario analysis.', 'Add financing effects using APV if subsidised debt is offered.'],
             'takeaway': 'A good appraisal shows not just NPV but how fragile it is.'}]

    mcqs = [
        Q('m1', 'Money cash flows should be discounted at:', ['The nominal rate', 'The real rate', 'The inflation rate', 'Zero'], 0,
          'Consistency rule. In practice: Fisher relation.', 'c1', T1),
        Q('m2', 'The coefficient of variation equals:', ['Standard deviation ÷ expected value', 'Expected value ÷ variance', 'Variance × probability', 'NPV ÷ cost'], 0,
          'Risk per unit of return. In practice: compares projects of different size.', 'c2', T2),
        Q('m3', 'Under the certainty equivalent approach, certain cash flows are discounted at:', ['The risk-free rate', 'WACC plus premium', 'Cost of equity', 'Inflation rate'], 0,
          'Risk is already removed from cash flows. In practice: avoid double counting.', 'c3', T3),
        Q('m4', 'A drawback of the risk-adjusted discount rate is that it:', ['Assumes risk compounds over time', 'Ignores time value', 'Needs no judgement', 'Uses certain cash flows'], 0,
          'Premium applies every year. In practice: may over-penalise distant flows.', 'c3', T3),
        Q('m5', 'Sensitivity analysis changes:', ['One variable at a time', 'All variables together', 'Only the discount rate', 'Nothing'], 0,
          'Shows critical variables. In practice: ignores interactions.', 'c4', T4),
        Q('m6', 'Monte Carlo simulation produces:', ['A probability distribution of NPVs', 'A single NPV', 'Only IRR', 'Payback only'], 0,
          'Many random runs. In practice: needs distributions for inputs.', 'c4', T4),
        Q('m7', 'For assets with unequal lives replaced repeatedly, choose the one with:', ['Lowest equivalent annual cost', 'Lowest purchase price', 'Longest life', 'Highest payback'], 0,
          'EAC equalises lives. In practice: replacement cycle analysis.', 'c5', T5),
        Q('m8', 'APV equals:', ['Base-case NPV plus PV of financing side-effects', 'NPV at WACC', 'IRR minus cost', 'Payback plus tax'], 0,
          'Separates investment and financing. In practice: base case at unlevered Ke.', 'c5', T5),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Nominal rate', 2, 'computation', 'nominal', nums=[nom]), S('s2', 'CE flows', 2, 'concept', 'certain'), S('s3', 'NPV', 2, 'computation', 'npv', nums=[ce])],
          ['Discount CE at risk-free rate.'], ['Adding real rate and inflation.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Cash flow and NPV', 2, 'computation', 'npv', nums=[cf, npv]), S('s2', 'Break-even', 2, 'computation', 'break-even', nums=[]), S('s3', 'Sensitivity %', 2, 'computation', 'sensitivity', nums=[sens])],
          ['Show per-unit effect.'], ['Ignoring fixed costs.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'State the Fisher relation.', 'One plus the nominal rate equals one plus the real rate multiplied by one plus the inflation rate.',
          [P('p1', 'Nominal and real', 5, 'nominal|real'), P('p2', 'Inflation', 5, 'inflation')], 'c1'),
        V('v2', 'Distinguish risk and uncertainty.', 'Risk exists when probabilities of outcomes can be estimated; uncertainty is when they cannot.',
          [P('p1', 'Probabilities known', 6, 'probabilit'), P('p2', 'Cannot estimate', 4, 'cannot')], 'c2'),
        V('v3', 'Explain the certainty equivalent approach.', 'Risky cash flows are converted to certain equivalents using coefficients and then discounted at the risk-free rate.',
          [P('p1', 'Coefficients', 5, 'coefficient'), P('p2', 'Risk-free rate', 5, 'risk-free')], 'c3'),
        V('v4', 'What is the main limitation of sensitivity analysis?', 'It changes one variable at a time, ignoring how variables move together and how likely each change is.',
          [P('p1', 'One at a time', 5, 'one variable|one at a time'), P('p2', 'Interdependence', 5, 'together|likely')], 'c4'),
        V('v5', 'How is APV computed?', 'Base-case NPV at the unlevered cost of equity plus the present value of financing benefits such as interest tax shields.',
          [P('p1', 'Base-case NPV', 5, 'base-case'), P('p2', 'Tax shield', 5, 'tax shield')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Rapid Pack Ltd.', 'difficulty': 'moderate',
              'case': 'Rapid Pack Ltd. must choose between machine A (cost ₹100 lakh, life 3 years, running cost ₹20 lakh a year) and machine B (cost ₹140 lakh, life 5 years, running cost ₹18 lakh a year); discount rate 10% (annuity factors: 3 years 2.4869, 5 years 3.7908). It also evaluates a separate project with base-case NPV of −₹5 lakh, financed by a 5-year ₹100 lakh loan at 10% interest; tax rate 30%.',
              'mcqs': [
                  M('k1a', 'EAC of machine A (₹ lakh, two decimals):', ['60.21', '53.33', '40.21', '73.33'], 0,
                    '100 ÷ 2.4869 + 20. In practice: compare like with like.', 'moderate', check=60.21, topic=T5),
                  M('k1b', 'EAC of machine B (₹ lakh, two decimals):', ['54.93', '46', '36.93', '64'], 0,
                    '140 ÷ 3.7908 + 18. In practice: lower EAC wins.', 'moderate', check=54.93, topic=T5),
                  M('k1c', 'PV of interest tax shield on the loan, discounted at 10% (₹ lakh, two decimals):', ['11.37', '15', '3', '30'], 0,
                    '100 × 10% × 30% = 3 a year × 3.7908. In practice: discount at cost of debt.', 'moderate', check=11.37, topic=T5),
                  M('k1d', 'APV of the separate project (₹ lakh, two decimals):', ['6.37', '−5', '11.37', '16.37'], 0,
                    '−5 + 11.37. In practice: financing makes it acceptable.', 'moderate', check=6.37, topic=T5),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch03', 1, 'Advanced Capital Budgeting Decisions',
                ['Adjust project appraisal for inflation, technology and policy changes.',
                 'Measure project risk with probability and dispersion tools.',
                 'Apply risk-adjusted discount rates and certainty equivalents.',
                 'Use sensitivity, scenario and simulation analysis.',
                 'Evaluate replacement decisions and apply APV.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 50}, 'prereq': ['fin-p2-ch02-u01'],
                 'exam_tip': 'State the method (RADR, CE, sensitivity, EAC or APV) first and keep rates and cash flows consistent.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Fisher: (1+n) = (1+r)(1+i).',
                             'Expected NPV, SD, coefficient of variation.',
                             'RADR or CE — not both.',
                             'Sensitivity: % change to make NPV zero.',
                             'EAC for unequal lives; APV = base NPV + financing effects.'],
                 'remember': ['CE flows discount at risk-free rate.'],
                 'traps': ['Mixing real cash flows with nominal rates.']},
                [('Fisher', '(1+n)=(1+r)(1+i)'), ('CV', 'σ ÷ E'), ('EAC', 'PV cost ÷ annuity factor'), ('APV', 'Base NPV + PV tax shield')],
                viva, cases)
