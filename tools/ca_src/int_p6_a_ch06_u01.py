"""CA Intermediate · Paper 6A Financial Management · Chapter 6 Financing Decisions – Leverages.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch06-u01'
T1 = 'Meaning and types of leverage'
T2 = 'Operating leverage (DOL)'
T3 = 'Break-even, margin of safety and operating leverage'
T4 = 'Financial leverage (DFL) and trading on equity'
T5 = 'Combined leverage (DCL) and risk combinations'


def build():
    # i1 — all three leverages from one statement, then the effect of a sales change
    ck = Checks()
    cont = ck.add('60000*(150-90)', 'Contribution = units × (price – variable cost)')
    ebit = ck.add('3600000-2400000', 'EBIT = contribution – fixed cost')
    intr = ck.add('0.11*4000000', 'Interest on ₹40 lakh at 11%')
    ebt = ck.add('1200000-440000', 'EBT')
    pref = ck.add('0.10*1000000', 'Preference dividend')
    dol = ck.add('3600000/1200000', 'DOL = contribution ÷ EBIT')
    dfl = ck.add('round(1200000/(760000-100000/0.75),3)', 'DFL = EBIT ÷ [EBT – PD/(1 – t)]')
    dcl = ck.add('round(3*1.915,3)', 'DCL = DOL × DFL')
    eps = ck.add('round((760000*0.75-100000)/50000,2)', 'EPS')
    eps_up = ck.add('round(((66000*60-2400000-440000)*0.75-100000)/50000,2)', 'EPS after 10% rise in units')
    i1 = {'id': 'i1', 'title': 'Three leverages from one income statement', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Kaveri Appliances Ltd. sells 60,000 units at ₹150 (variable cost ₹90). Fixed operating costs ₹24,00,000. Capital: 11% debt ₹40,00,000; 10% preference ₹10,00,000; 50,000 equity shares. Tax 25%. Compute DOL, DFL, DCL and EPS, and the EPS if units rise by 10%.',
          'solution': [table(['Particulars', '₹'], [
              ['Contribution (60,000 × ₹60)', inr(cont)],
              ['Less fixed costs', inr(2400000)],
              ['EBIT', inr(ebit)],
              ['Less interest', inr(intr)],
              ['EBT', inr(ebt)],
              ['Less tax 25%', inr(190000)],
              ['PAT', inr(570000)],
              ['Less preference dividend', inr(pref)],
              ['Earnings for equity', inr(470000)],
              ['EPS (÷ 50,000)', R(eps)]], title='Income statement'),
              table(['Leverage', 'Working', 'Value'], [
                  ['DOL', '36,00,000 ÷ 12,00,000', dol],
                  ['DFL', '12,00,000 ÷ (7,60,000 – 1,00,000 ÷ 0.75)', dfl],
                  ['DCL', 'DOL × DFL', dcl]], title='Degrees of leverage'),
              p(f'A 10% rise in units should lift EPS by about {dcl} × 10% ≈ {round(dcl*10,1)}%. Check: at 66,000 units, EBIT = 39,60,000 – 24,00,000 = 15,60,000; EBT = 11,20,000; earnings for equity = 8,40,000 – 1,00,000 = 7,40,000; EPS = {R(eps_up)}, a rise of {round((eps_up/eps-1)*100,1)}%.'),
              note('Preference dividend is grossed up by (1 – t) in DFL because it is paid out of post-tax profit.')],
          'checks': list(ck)}

    # i2 — operating leverage and margin of safety
    ck2 = Checks()
    pv = ck2.add('(500-300)/500', 'P/V ratio')
    bep = ck2.add('1600000/0.4', 'Break-even sales = fixed cost ÷ P/V')
    sales = ck2.add('25000*500', 'Sales')
    mos = ck2.add('(12500000-4000000)/12500000', 'Margin of safety ratio')
    dol2 = ck2.add('round(5000000/3400000,3)', 'DOL = contribution ÷ EBIT')
    inv = ck2.add('round(1/0.68,3)', '1 ÷ MOS')
    i2 = {'id': 'i2', 'title': 'Operating leverage is the inverse of margin of safety', 'difficulty': 'core', 'minutes': 6,
          'q': 'Penna Fans sells 25,000 fans at ₹500 (variable cost ₹300); fixed costs are ₹16,00,000. Compute break-even sales, the margin of safety ratio and DOL, and show that DOL = 1 ÷ MOS.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['P/V ratio', '200 ÷ 500', f'{round(pv*100)}%'],
              ['Break-even sales', '16,00,000 ÷ 0.40', inr(bep)],
              ['Sales', '25,000 × 500', inr(sales)],
              ['MOS ratio', '(1,25,00,000 – 40,00,000) ÷ 1,25,00,000', mos],
              ['DOL', 'Contribution 50,00,000 ÷ EBIT 34,00,000', dol2],
              ['1 ÷ MOS', '1 ÷ 0.68', inv]], title='DOL and MOS'),
              note('The further sales are above break-even, the larger the margin of safety and the lower the operating leverage (business risk).')],
          'checks': list(ck2)}

    # i3 — financial leverage as a double-edged sword
    ck3 = Checks()
    roe_a = ck3.add('round(1000000*0.75/5000000*100,2)', 'ROE all-equity at EBIT 10 lakh, %')
    roe_b = ck3.add('round((1000000-250000)*0.75/2500000*100,2)', 'ROE 50% debt at EBIT 10 lakh, %')
    roe_a2 = ck3.add('round(400000*0.75/5000000*100,2)', 'ROE all-equity at EBIT 4 lakh, %')
    roe_b2 = ck3.add('round((400000-250000)*0.75/2500000*100,2)', 'ROE 50% debt at EBIT 4 lakh, %')
    i3 = {'id': 'i3', 'title': 'Leverage cuts both ways', 'difficulty': 'core', 'minutes': 6,
          'q': 'Two firms each employ ₹50,00,000. Firm A is all equity; Firm B has ₹25,00,000 of 10% debt. Tax 25%. Compute return on equity for each at EBIT of ₹10,00,000 (ROI 20%) and at EBIT of ₹4,00,000 (ROI 8%).',
          'solution': [table(['EBIT', 'ROE Firm A', 'ROE Firm B'], [
              ['₹10,00,000 (ROI 20% > 10% interest)', f'{roe_a}%', f'{roe_b}%'],
              ['₹4,00,000 (ROI 8% < 10% interest)', f'{roe_a2}%', f'{roe_b2}%']], title='Return on equity'),
              note('When the return on assets exceeds the cost of debt, leverage magnifies ROE (favourable leverage); when it falls below, leverage depresses ROE (unfavourable).')],
          'checks': list(ck3)}

    lev = table(['Leverage', 'Formula', 'Measures', 'Risk'], [
        ['Operating (DOL)', 'Contribution ÷ EBIT  =  %Δ EBIT ÷ %Δ Sales', 'Effect of sales change on EBIT', 'Business risk'],
        ['Financial (DFL)', 'EBIT ÷ [EBT – PD/(1 – t)]  =  %Δ EPS ÷ %Δ EBIT', 'Effect of EBIT change on EPS', 'Financial risk'],
        ['Combined (DCL)', 'DOL × DFL = Contribution ÷ [EBT – PD/(1 – t)]  =  %Δ EPS ÷ %Δ Sales', 'Effect of sales change on EPS', 'Total risk']],
        title='Leverage formulas')
    combo = table(['DOL', 'DFL', 'Comment'], [
        ['Low', 'Low', 'Low total risk, but little benefit from trading on equity'],
        ['High', 'High', 'Very high total risk — dangerous'],
        ['High', 'Low', 'Moderate risk; weak use of debt — not ideal'],
        ['Low', 'High', 'Moderate risk; the preferred combination']], title='Combining operating and financial leverage')

    concepts = [
        C('c1', T1, [
            'Leverage is the use of fixed costs — operating or financial — to magnify the effect of a change in one figure on another.',
            'Operating leverage links sales to EBIT (business risk), financial leverage links EBIT to EPS (financial risk), and combined leverage links sales to EPS (total risk).'],
          'A lever lets a small push move a heavy load; fixed costs let a small sales change move profits a lot.',
          'Airlines, with large fixed costs, see profits swing sharply with small changes in passenger numbers.',
          blocks=[lev]),
        C('c2', T2, [
            'Operating leverage arises from fixed operating costs. DOL = %Δ EBIT ÷ %Δ sales = contribution ÷ EBIT.',
            'DOL is different at each level of sales: it is very high just above break-even and falls as sales grow. Below break-even it is negative.',
            'High fixed costs mean high break-even, high DOL and greater business risk; low fixed costs mean the reverse.'],
          'Fixed costs act like a spring: they amplify every rise and fall in sales.',
          'With DOL of 3, an 8% fall in sales cuts EBIT by 24%.'),
        C('c3', T3, [
            'Margin of safety (MOS) = (sales – break-even sales) ÷ sales. Multiplying both parts by the P/V ratio turns it into (contribution – fixed cost) ÷ contribution = EBIT ÷ contribution.',
            'Hence DOL = 1 ÷ MOS: the higher the margin of safety, the lower the operating leverage and business risk.'],
          'The farther you stand from the cliff edge (break-even), the less a stumble hurts.',
          'A business with a 25% margin of safety has a DOL of 4.'),
        C('c4', T4, [
            'Financial leverage arises from fixed financing charges — interest and preference dividend. DFL = %Δ EPS ÷ %Δ EBIT = EBIT ÷ [EBT – PD ÷ (1 – t)]; without preference shares, EBIT ÷ EBT.',
            'Using fixed-cost funds to raise equity returns is called trading on equity. It is favourable when return on investment exceeds the cost of those funds, unfavourable when it is lower — hence "double-edged sword".',
            'DFL > 1 means financial leverage exists; a negative DFL means EBIT is below the financial break-even.'],
          'Borrowing at 10% to earn 20% helps shareholders; borrowing at 10% to earn 8% hurts them.',
          'With DFL of 2, a 5% rise in EBIT lifts EPS by 10%.'),
        C('c5', T5, [
            'DCL = DOL × DFL = %Δ EPS ÷ %Δ sales = contribution ÷ [EBT – PD ÷ (1 – t)]. It measures total risk.',
            'Firms usually avoid high operating and high financial leverage together. Low operating leverage with high financial leverage is generally the best mix: stable EBIT can safely support debt.'],
          'Two springs in series multiply each other\'s bounce.',
          'With DCL of 6, an 8% rise in sales lifts EPS by 48%.',
          blocks=[combo]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Stress-testing a budget', 'role': 'FP&A analyst',
         'situation': 'Management asks what a 10% fall in volume would do to EPS.',
         'steps': ['Compute DOL from the budget (contribution ÷ EBIT).', 'Compute DFL with interest and grossed-up preference dividend.', 'Multiply to get DCL; apply to the sales change.', 'Recompute the income statement to confirm.'],
         'takeaway': 'DCL gives a quick estimate; always confirm with a full recomputation.'},
        {'id': 'j2', 'title': 'Advising on new borrowing', 'role': 'Finance manager',
         'situation': 'A high-fixed-cost factory wants to fund expansion with debt.',
         'steps': ['Check existing DOL and MOS.', 'Estimate DFL after the new loan.', 'If both are high, suggest equity or cost restructuring.'],
         'takeaway': 'High operating leverage argues for lower financial leverage.'},
    ]

    mcqs = [
        Q('m1', 'Operating leverage measures the relationship between:', ['Sales and EBIT', 'EBIT and EPS', 'Sales and EPS', 'EBT and PAT'], 0,
          'Operating leverage shows how a change in sales affects EBIT, because of fixed operating costs; it reflects business risk. EBIT-to-EPS is financial leverage and sales-to-EPS is combined leverage. In practice: DOL = contribution ÷ EBIT.', 'c1', T1),
        Q('m2', 'Contribution ₹8,00,000; fixed cost ₹6,00,000. DOL is:', ['4', '1.33', '0.25', '3'], 0,
          'EBIT = 8,00,000 – 6,00,000 = ₹2,00,000. DOL = contribution ÷ EBIT = 8,00,000 ÷ 2,00,000 = 4, so a 1% change in sales changes EBIT by 4%. High fixed costs relative to contribution create this high leverage. In practice: DOL falls as sales grow.', 'c2', T2, 'core', check=4),
        Q('m3', 'If the margin of safety ratio is 20%, DOL is:', ['5', '0.2', '20', '2'], 0,
          'DOL = 1 ÷ MOS = 1 ÷ 0.20 = 5. This follows because MOS can be rewritten as EBIT ÷ contribution, the inverse of DOL. A thin margin of safety means high operating leverage. In practice: raise sales above break-even to lower risk.', 'c3', T3, 'core', check=5),
        Q('m4', 'EBIT ₹5,00,000; interest ₹1,00,000; no preference shares. DFL is:', ['1.25', '5', '0.8', '1.5'], 0,
          'DFL = EBIT ÷ EBT = 5,00,000 ÷ 4,00,000 = 1.25, so a 1% change in EBIT changes EPS by 1.25%. Tax does not affect DFL when there are no preference shares. In practice: more debt raises DFL.', 'c4', T4, 'core', check=1.25),
        Q('m5', 'EBIT ₹6,00,000; interest ₹1,50,000; preference dividend ₹90,000; tax 25%. DFL is:', ['1.82', '1.33', '2', '1.5'], 0,
          'Grossed-up PD = 90,000 ÷ 0.75 = ₹1,20,000. DFL = 6,00,000 ÷ (4,50,000 – 1,20,000) = 6,00,000 ÷ 3,30,000 ≈ 1.82. Ignoring the gross-up gives 6,00,000 ÷ 3,60,000 ≈ 1.67, which is wrong. In practice: preference dividend is post-tax.', 'c4', T4, 'hard', check=1.82),
        Q('m6', 'Financial leverage is favourable when:', ['Return on investment exceeds the cost of debt', 'Cost of debt exceeds return on investment', 'There is no debt', 'Sales are below break-even'], 0,
          'Trading on equity helps shareholders only if assets financed by debt earn more than the interest rate; then the surplus raises ROE. If returns fall below the cost of debt, leverage hurts. In practice: that is why it is called a double-edged sword.', 'c4', T4),
        Q('m7', 'DOL 2.5 and DFL 2. If sales rise by 10%, EPS rises by:', ['50%', '45%', '25%', '20%'], 0,
          'DCL = 2.5 × 2 = 5, so EPS changes by 5 × 10% = 50%. The two leverages multiply, not add. The same applies in reverse when sales fall. In practice: high DCL means volatile EPS.', 'c5', T5, 'core', check=50),
        Q('m8', 'The generally preferred combination of leverages is:', ['Low DOL and high DFL', 'High DOL and high DFL', 'High DOL and low DFL', 'Low DOL and low DFL'], 0,
          'Low operating leverage gives stable EBIT, which can safely support fixed financial charges, so high financial leverage can be used to boost EPS. High–high is very risky; low–low forgoes trading on equity. In practice: utilities often fit this pattern.', 'c5', T5),
        Q('m9', 'A negative DFL indicates that:', ['EBIT is below the financial break-even point', 'The firm has no debt', 'EPS will rise with EBIT', 'DOL is negative'], 0,
          'DFL is negative when EBT (after grossed-up preference dividend) is negative, i.e. EBIT does not cover fixed financial charges. Then EBIT and EPS move in opposite proportions. In practice: such a firm is in financial distress.', 'c4', T4, 'moderate'),
        Q('m10', 'Combined leverage is a measure of:', ['Total risk', 'Business risk only', 'Financial risk only', 'Liquidity'], 0,
          'Combined leverage multiplies operating leverage (business risk) and financial leverage (financial risk), so it captures total risk — the sensitivity of EPS to sales. Liquidity is a separate concept. In practice: lenders watch it closely.', 'c5', T5),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Income statement to EPS', 2, 'computation', 'eps', nums=[ebit, ebt, eps]),
           S('s2', 'DOL', 1.5, 'computation', 'dol|operating', nums=[dol]),
           S('s3', 'DFL with grossed-up PD', 2, 'computation', 'dfl|financial', nums=[dfl]),
           S('s4', 'DCL', 1, 'computation', 'dcl|combined', nums=[dcl]),
           S('s5', 'EPS after change', 1.5, 'computation', '66,000|10%', nums=[eps_up])],
          ['Gross up preference dividend.'], ['Using EBT directly when preference shares exist.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Break-even', 1, 'computation', 'break-even|break even', nums=[bep]),
           S('s2', 'MOS', 1, 'computation', 'margin|mos', nums=[mos]),
           S('s3', 'DOL', 1, 'computation', 'dol', nums=[dol2]),
           S('s4', 'Inverse relation', 1, 'concept', '1 ÷|inverse|reciprocal', nums=[inv])],
          ['Show both sides of the identity.'], ['Using sales instead of contribution.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 4, i3['q'], i3['solution'],
          [S('s1', 'ROE at high EBIT', 1.5, 'computation', 'roe', nums=[roe_a, roe_b]),
           S('s2', 'ROE at low EBIT', 1.5, 'computation', 'roe', nums=[roe_a2, roe_b2]),
           S('s3', 'Conclusion', 1, 'concept', 'favourable|double|cost of debt')],
          ['Compare ROI with the interest rate.'], ['Forgetting tax.'], ['Table + note.'], pad='table', checks=list(ck3)),
    ]

    viva = [
        V('v1', 'Why is DOL highest just above break-even?',
          'Because EBIT is very small there, so contribution divided by EBIT is large; a small change in sales then causes a large percentage change in EBIT.',
          [P('p1', 'Small EBIT', 6, 'small|low'), P('p2', 'Large % change', 4, 'large|big|percentage')], 'c2'),
        V('v2', 'What is trading on equity?',
          'Using fixed-cost funds such as debt and preference capital along with equity to increase the return to equity shareholders.',
          [P('p1', 'Fixed-cost funds', 5, 'fixed|debt'), P('p2', 'Increase return to shareholders', 5, 'return|earnings|eps')], 'c4'),
        V('v3', 'How are DOL and margin of safety related?',
          'DOL is the reciprocal of the margin of safety ratio, so a larger margin of safety means lower operating leverage.',
          [P('p1', 'Reciprocal', 6, 'reciprocal|inverse|1 ÷|one divided'), P('p2', 'Larger MOS lower DOL', 4, 'lower|less')], 'c3'),
        V('v4', 'Why is preference dividend grossed up in DFL?',
          'Because it is paid out of post-tax profit, so it must be converted to a pre-tax equivalent by dividing by one minus the tax rate before comparing with EBIT.',
          [P('p1', 'Paid from post-tax profit', 5, 'post-tax|after tax'), P('p2', 'Divide by (1 – t)', 5, '1 – t|one minus|1-t')], 'c4'),
        V('v5', 'Which leverage reflects total risk and how is it found?',
          'Combined leverage reflects total risk; it is the product of operating and financial leverage, or contribution divided by profit before tax after grossed-up preference dividend.',
          [P('p1', 'Combined leverage', 4, 'combined'), P('p2', 'Product of DOL and DFL', 6, 'product|multipl')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Two bakeries', 'difficulty': 'moderate',
              'case': 'Bakery X: contribution ₹20 lakh, fixed costs ₹15 lakh, no debt. Bakery Y: contribution ₹20 lakh, fixed costs ₹5 lakh, interest ₹10 lakh. Both have no preference shares.',
              'mcqs': [
                  M('k1a', 'DOL of Bakery X is:', ['4', '1.33', '2', '0.25'], 0,
                    'EBIT of X = 20 – 15 = ₹5 lakh; DOL = 20 ÷ 5 = 4. Its large fixed costs give high business risk, so a small change in sales swings EBIT sharply. In practice: X is close to break-even.', 'core', check=4, topic=T2),
                  M('k1b', 'DFL of Bakery Y is:', ['3', '1.5', '1', '0.33'], 0,
                    'EBIT of Y = 20 – 5 = ₹15 lakh; EBT = 15 – 10 = ₹5 lakh; DFL = 15 ÷ 5 = 3. Its heavy interest burden creates high financial risk even though operating risk is low. In practice: lenders would watch interest cover.', 'core', check=3, topic=T4),
                  M('k1c', 'DCL of the two bakeries:', ['Both 4', 'X 4, Y 3', 'X 1, Y 4', 'X 4, Y 1.33'], 0,
                    'X: DOL 4 × DFL 1 = 4. Y: DOL 20 ÷ 15 ≈ 1.33 × DFL 3 = 4. Same total risk reached in different ways: X through operating costs, Y through debt. In practice: the mix matters for flexibility.', 'hard', topic=T5),
                  M('k1d', 'Which bakery has the generally preferred leverage mix?', ['Bakery Y — low DOL, high DFL', 'Bakery X — high DOL, low DFL', 'Both equally', 'Neither has leverage'], 0,
                    'Y has low operating leverage and higher financial leverage, the combination usually preferred because stable EBIT supports fixed financial charges. X has high operating leverage without using cheap debt. In practice: X might lower fixed costs before borrowing.', 'moderate', topic=T5),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch06', 1, 'Financing Decisions – Leverages',
                ['Explain the meaning and types of leverage and the risks they measure.',
                 'Compute and interpret DOL, and relate it to break-even and margin of safety.',
                 'Compute DFL (including preference dividend) and explain trading on equity.',
                 'Compute DCL and evaluate combinations of operating and financial leverage.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': ['int-p6-a-ch05-u01'],
                 'exam_tip': 'Build the income statement first, then read off DOL, DFL and DCL; remember to gross up preference dividend and to use DCL × % change in sales for EPS changes.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['DOL = contribution/EBIT (business risk).', 'DFL = EBIT/[EBT – PD/(1 – t)] (financial risk).', 'DCL = DOL × DFL (total risk).',
                             'DOL = 1/MOS.', 'Trading on equity helps only when ROI > cost of debt.', 'Preferred mix: low DOL, high DFL.'],
                 'remember': ['Leverage values change with the level of activity.', 'Negative DFL → EBIT below financial break-even.'],
                 'traps': ['Multiply, do not add, DOL and DFL.', 'Gross up preference dividend.']},
                [('DOL', 'Contribution/EBIT'), ('DFL', 'EBIT/[EBT – PD/(1–t)]'), ('DCL', 'DOL × DFL'), ('DOL & MOS', 'DOL = 1/MOS')],
                viva, cases,
                topics=['Introduction', 'Meaning and Types of Leverage', 'Operating Leverage', 'Financial Leverage', 'Combined Leverage'])
