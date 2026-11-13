"""CA Intermediate · Paper 6A Financial Management · Chapter 7 Investment Decisions.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch07-u01'
T1 = 'Capital budgeting process and cash flows'
T2 = 'Non-discounted techniques: payback and ARR'
T3 = 'Discounted techniques: NPV, PI, discounted payback'
T4 = 'IRR, MIRR and conflicting rankings'


def build():
    ck = Checks()
    pv = ck.add('300000*0.909+400000*0.826+500000*0.751+200000*0.683', 'PV of inflows at 10%')
    npv = ck.add('1115200-1000000', 'NPV')
    pi = ck.add('1115200/1000000', 'Profitability index')
    pb = ck.add('2+300000/500000', 'Payback period (years)')
    dpb = ck.add('3+(1000000-978600)/136600', 'Discounted payback (years)')
    i1 = {'id': 'i1', 'title': 'Evaluating a new line', 'difficulty': 'moderate', 'minutes': 12,
          'q': 'A project costs ₹10,00,000 and is expected to generate cash inflows of ₹3,00,000, ₹4,00,000, ₹5,00,000 and ₹2,00,000 over four years. Cost of capital 10% (PV factors 0.909, 0.826, 0.751, 0.683). Compute NPV, PI, payback and discounted payback.',
          'solution': [table(['Year', 'Inflow ₹', 'PV factor', 'PV ₹', 'Cumulative PV ₹'], [
              ['1', inr(300000), '0.909', inr(272700), inr(272700)],
              ['2', inr(400000), '0.826', inr(330400), inr(603100)],
              ['3', inr(500000), '0.751', inr(375500), inr(978600)],
              ['4', inr(200000), '0.683', inr(136600), inr(1115200)]], title='Discounted cash flows'),
              table(['Measure', 'Answer'], [
                  ['NPV', '₹' + inr(npv)],
                  ['PI', str(round(pi, 4))],
                  ['Payback', str(round(pb, 2)) + ' years (₹3,00,000 of year 3\'s ₹5,00,000 needed)'],
                  ['Discounted payback', str(round(dpb, 2)) + ' years']], title='Results'),
              note('Accept: NPV is positive and PI exceeds 1.')],
          'checks': list(ck)}

    ck2 = Checks()
    p9 = ck2.add('40000*2.531', 'PV at 9%')
    p10 = ck2.add('40000*2.487', 'PV at 10%')
    irr = ck2.add('9+(101240-100000)/(101240-99480)', 'IRR by interpolation (%)')
    i2 = {'id': 'i2', 'title': 'Finding the IRR', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'An investment of ₹1,00,000 yields ₹40,000 a year for 3 years. Annuity factors: 9% — 2.531; 10% — 2.487. Find the IRR and decide if it is acceptable at a cost of capital of 9.5%.',
          'solution': [table(['Rate', 'PV of inflows ₹', 'NPV ₹'], [
              ['9%', inr(p9), inr(1240)],
              ['10%', inr(p10), '(520)']], title='Trial rates'),
              p('IRR = 9% + 1,240 ÷ (1,01,240 − 99,480) × 1% = ' + str(round(irr, 2)) + '%. It exceeds 9.5%, so accept.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Capital budgeting is planning long-term investments whose returns come over several years: identify proposals, screen, evaluate, select, implement and review (post-audit).',
            'Decisions rest on incremental after-tax cash flows, not accounting profits: initial outflow (cost, installation, working capital), operating inflows (profit after tax + depreciation, or (revenue − cash costs)(1 − t) + depreciation × t), and terminal flows (salvage after tax and release of working capital). Sunk costs are ignored; opportunity costs are included; financing costs are excluded because the discount rate captures them.',
            'Types of decisions: expansion, replacement, modernisation, diversification; mutually exclusive, independent and contingent projects; capital rationing.'],
          'Value comes from future cash, measured after tax and only where it changes because of the decision.',
          'Land already owned but saleable for ₹50 lakh is an opportunity cost of using it for a project.'),
        C('c2', T2, [
            'Payback period = time to recover the initial investment from undiscounted inflows; simple and good for liquidity, but ignores time value and cash flows after payback. Payback reciprocal approximates IRR for long-life projects with even flows.',
            'Accounting rate of return = average annual accounting profit after tax ÷ average investment (or initial investment); uses accounting data and ignores timing.',
            'Both are easy to understand but can mislead when projects differ in timing or life.'],
          'Payback answers "how soon do we get our money back?", not "how much value is created?".',
          'Two projects with a 3-year payback can differ widely if one has large flows in years 4 to 10.'),
        C('c3', T3, [
            'Net present value = PV of inflows − PV of outflows at the cost of capital; accept if NPV ≥ 0. NPV measures the increase in shareholders\' wealth and is additive across projects.',
            'Profitability index = PV of inflows ÷ PV of outflows; accept if PI ≥ 1. Useful in capital rationing to rank divisible projects.',
            'Discounted payback = time to recover the investment from discounted inflows; it adds time value to payback but still ignores later flows.'],
          'NPV is the wealth test: positive NPV means the project earns more than investors demand.',
          'A project costing ₹5 lakh with PV of inflows ₹5.6 lakh adds ₹60,000 of value.'),
        C('c4', T4, [
            'Internal rate of return is the discount rate at which NPV = 0; accept if IRR ≥ cost of capital. It is found by trial and interpolation: IRR = lower rate + NPV at lower rate ÷ (difference in NPVs) × difference in rates.',
            'Problems: multiple IRRs with non-conventional cash flows; reinvestment at IRR assumed. Modified IRR assumes reinvestment at the cost of capital: compounding inflows to the terminal year and finding the rate equating their terminal value with the PV of outflows.',
            'NPV and IRR may rank mutually exclusive projects differently due to size, timing or life differences; NPV is preferred because it measures absolute wealth and uses a realistic reinvestment rate.'],
          'IRR gives a percentage; NPV gives rupees — when they disagree, choose rupees of value.',
          'A small project with 30% IRR may add less value than a large one with 18% IRR when cost of capital is 12%.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Project appraisal note', 'role': 'Finance analyst trainee',
             'situation': 'The board asks whether to buy a new packaging machine.',
             'steps': ['Estimate incremental after-tax cash flows.', 'Discount at the cost of capital.', 'Compute NPV, IRR and payback.', 'Recommend with sensitivity to key assumptions.'],
             'takeaway': 'The decision rule is NPV; other measures add context.'}]

    mcqs = [
        Q('m1', 'Which is ignored in project cash flows?', ['Sunk costs', 'Opportunity costs', 'Working capital release', 'Tax savings on depreciation'], 0,
          'Sunk costs are already incurred and do not change with the decision. In practice: past research costs are irrelevant.', 'c1', T1),
        Q('m2', 'Investment ₹6,00,000; equal annual inflows ₹1,50,000. Payback:', ['4 years', '5 years', '3 years', '6 years'], 0,
          '6,00,000 ÷ 1,50,000 = 4 years. In practice: check life beyond payback.', 'c2', T2, check=4),
        Q('m3', 'A project is acceptable under NPV if:', ['NPV ≥ 0', 'NPV < 0', 'IRR < cost of capital', 'PI < 1'], 0,
          'Non-negative NPV means returns meet or exceed the required rate. In practice: rank by NPV for mutually exclusive projects.', 'c3', T3),
        Q('m4', 'PV of inflows ₹2,40,000; investment ₹2,00,000. PI:', ['1.2', '0.83', '1.4', '0.2'], 0,
          '2,40,000 ÷ 2,00,000 = 1.2. In practice: PI above 1 is acceptable.', 'c3', T3, check=1.2),
        Q('m5', 'IRR is the rate at which:', ['NPV equals zero', 'PI equals 2', 'Payback equals life', 'ARR equals cost of capital'], 0,
          'IRR equates PV of inflows with PV of outflows. In practice: found by trial and interpolation.', 'c4', T4),
        Q('m6', 'MIRR assumes reinvestment of intermediate cash flows at:', ['The cost of capital', 'The IRR', 'Zero', 'The risk-free rate always'], 0,
          'MIRR corrects IRR\'s reinvestment assumption. In practice: gives a single rate.', 'c4', T4),
        Q('m7', 'When NPV and IRR conflict for mutually exclusive projects, choose by:', ['NPV', 'IRR', 'Payback', 'ARR'], 0,
          'NPV directly measures wealth added. In practice: conflicts arise from size or timing differences.', 'c4', T4),
        Q('m8', 'Average annual profit ₹30,000; initial investment ₹2,00,000 with nil salvage. ARR on average investment:', ['30%', '15%', '20%', '10%'], 0,
          'Average investment = 1,00,000; 30,000 ÷ 1,00,000 = 30%. In practice: state the base used.', 'c2', T2, check=30),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'PV of inflows', 2, 'computation', 'PV', nums=[pv]), S('s2', 'NPV and PI', 2, 'computation', 'NPV', nums=[npv, pi]),
           S('s3', 'Payback', 2, 'computation', 'payback', nums=[pb]), S('s4', 'Discounted payback', 2, 'computation', 'discounted', nums=[dpb])],
          ['Use a cumulative column.'], ['Using undiscounted flows for discounted payback.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Trial PVs', 2, 'computation', 'PV', nums=[p9, p10]), S('s2', 'Interpolation', 2, 'computation', 'IRR', nums=[irr]), S('s3', 'Decision', 1, 'concept', 'accept')],
          ['Show both trial rates.'], ['Interpolating on PV factors wrongly.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Why use cash flows instead of profits?', 'Because cash, not accounting profit, can be reinvested or distributed, and profits include non-cash items like depreciation and accruals.',
          [P('p1', 'Cash usable', 5, 'cash'), P('p2', 'Non-cash items', 5, 'depreciation|non-cash')], 'c1'),
        V('v2', 'Give two limitations of payback.', 'It ignores the time value of money and cash flows after the payback period.',
          [P('p1', 'Time value', 5, 'time value'), P('p2', 'Later flows', 5, 'after')], 'c2'),
        V('v3', 'What does a positive NPV mean?', 'The project earns more than the cost of capital and increases shareholders\' wealth by that amount in present value terms.',
          [P('p1', 'Above cost of capital', 5, 'cost of capital'), P('p2', 'Wealth', 5, 'wealth')], 'c3'),
        V('v4', 'How is IRR found?', 'By trying discount rates until NPV changes sign and interpolating between the two rates to where NPV is zero.',
          [P('p1', 'Trial rates', 5, 'trial|trying'), P('p2', 'Interpolation', 5, 'interpolat')], 'c4'),
        V('v5', 'Why can NPV and IRR give different rankings?', 'Because of differences in project size, timing of cash flows or life, and different reinvestment assumptions.',
          [P('p1', 'Size or timing', 5, 'size|timing|life'), P('p2', 'Reinvestment', 5, 'reinvest')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Orchid Hotels expansion', 'difficulty': 'moderate',
              'case': 'Orchid Hotels considers a ₹50 lakh spa. Expected after-tax inflows: ₹15 lakh a year for 5 years. Cost of capital 12% (5-year annuity factor 3.605). An alternative café costs ₹20 lakh with inflows of ₹7 lakh a year for 5 years.',
              'mcqs': [
                  M('k1a', 'NPV of the spa (₹ lakh):', ['4.075', '25.00', '3.605', '-4.075'], 0,
                    '15 × 3.605 = 54.075 − 50 = 4.075. In practice: positive, so acceptable.', 'moderate', check=4.075, topic=T3),
                  M('k1b', 'NPV of the café (₹ lakh):', ['5.235', '15.00', '7.00', '2.235'], 0,
                    '7 × 3.605 = 25.235 − 20 = 5.235. In practice: smaller project, higher NPV.', 'moderate', check=5.235, topic=T3),
                  M('k1c', 'PI of the spa:', ['1.08', '1.26', '0.92', '1.50'], 0,
                    '54.075 ÷ 50 = 1.08. In practice: café PI = 1.26.', 'moderate', check=1.08, topic=T3),
                  M('k1d', 'If only one can be chosen (mutually exclusive), choose:', ['The café — higher NPV', 'The spa — larger size', 'Either', 'Neither'], 0,
                    'For mutually exclusive projects, select the higher NPV. In practice: consider strategic fit too.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch07', 1, 'Investment Decisions',
                ['Estimate relevant cash flows for capital budgeting.',
                 'Apply payback and ARR.',
                 'Apply NPV, PI and discounted payback.',
                 'Compute IRR and MIRR and resolve ranking conflicts.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 60}, 'prereq': ['int-p6-a-ch06-u01'],
                 'exam_tip': 'Lay out a year-wise table of cash flows, PV factors and cumulative PV; most answers fall out of it.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Incremental after-tax cash flows; ignore sunk costs, include opportunity costs.',
                             'Payback, ARR: simple but ignore time value or later flows.',
                             'NPV ≥ 0 and PI ≥ 1 to accept.',
                             'IRR by interpolation; MIRR uses cost of capital for reinvestment.',
                             'Conflicts: prefer NPV.'],
                 'remember': ['Depreciation enters only through its tax saving.'],
                 'traps': ['Do not deduct interest from project cash flows.']},
                [('NPV', 'PV inflows − PV outflows'), ('PI', 'PV inflows ÷ PV outflows'), ('IRR', 'Rate where NPV = 0'), ('Payback', 'Time to recover cost')],
                viva, cases)
