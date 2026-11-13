"""CA Intermediate · Paper 6A Financial Management · Chapter 4 Cost of Capital.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch04-u01'
T1 = 'Meaning, significance and determinants of cost of capital'
T2 = 'Cost of debt — irredeemable and redeemable'
T3 = 'Cost of debt — YTM, zero coupon, amortised and convertible bonds'
T4 = 'Cost of preference share capital'
T5 = 'Cost of equity — dividend, earnings and growth approaches'
T6 = 'Cost of equity — realised yield and CAPM'
T7 = 'Cost of retained earnings'
T8 = 'Weighted average cost of capital (book and market weights)'
T9 = 'Marginal cost of capital'


def build():
    # i1 — cost of debt: irredeemable, redeemable (approximation) and YTM
    ck = Checks()
    kd1 = ck.add('round(11*0.75/92*100,2)', 'Irredeemable: I(1–t)/NP, %')
    np2 = ck.add('96-2', 'Net proceeds = issue price – flotation')
    kd2 = ck.add('round((12*0.75+(105-94)/6)/((105+94)/2)*100,2)', 'Redeemable (approximation), %')
    pv_lo = ck.add('round(9*4.355+105*0.564-94,2)', 'NPV at 10% (PVAF 4.355, PVF 0.564)')
    pv_hi = ck.add('round(9*4.111+105*0.507-94,2)', 'NPV at 12% (PVAF 4.111, PVF 0.507)')
    ytm = ck.add('round(10+ (4.42/(4.42+3.77))*2,2)', 'YTM by interpolation, %')
    i1 = {'id': 'i1', 'title': 'Three ways to measure the cost of debt', 'difficulty': 'core', 'minutes': 12,
          'q': 'Tapti Textiles Ltd. (tax 25%) has (a) 11% irredeemable debentures of ₹100 quoted at ₹92, and (b) plans to issue 12% debentures of ₹100 at ₹96 with flotation cost ₹2, redeemable at ₹105 after 6 years. Compute the post-tax cost of (a), and of (b) by the approximation method and by the YTM (IRR) method using 10% and 12%.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['(a) Irredeemable', '11 × (1 – 0.25) ÷ 92', f'{kd1}%'],
              ['(b) Net proceeds', '96 – 2', R(np2)],
              ['(b) Approximation', '[9 + (105 – 94) ÷ 6] ÷ [(105 + 94) ÷ 2] = 10.83 ÷ 99.5', f'{kd2}%'],
              ['NPV at 10%', '9 × 4.355 + 105 × 0.564 – 94', R(pv_lo)],
              ['NPV at 12%', '9 × 4.111 + 105 × 0.507 – 94', R(pv_hi)],
              ['(b) YTM', f'10% + {pv_lo} ÷ ({pv_lo} + {-pv_hi}) × 2%', f'{ytm}%']], title='Cost of debt'),
              note('The post-tax interest is ₹12 × 0.75 = ₹9. YTM is the more exact figure; the shortcut drifts when redemption value and net proceeds are far apart.')],
          'checks': list(ck)}

    # i2 — cost of equity: growth model (existing and new issue) and CAPM
    ck2 = Checks()
    d1 = ck2.add('4*1.08', 'Next dividend D1 = D0(1 + g)')
    ke_old = ck2.add('round((4.32/60+0.08)*100,2)', 'Ke (existing shares / retained earnings) = D1/P0 + g, %')
    ke_new = ck2.add('round((4.32/(60-3)+0.08)*100,2)', 'Ke on a new issue = D1/(P0 – F) + g, %')
    capm = ck2.add('7+1.3*(13-7)', 'CAPM: Rf + β(Rm – Rf), %')
    i2 = {'id': 'i2', 'title': 'Cost of equity two ways', 'difficulty': 'core', 'minutes': 8,
          'q': 'Godavari Pumps Ltd. has just paid a dividend of ₹4 a share; dividends are expected to grow at 8% a year. The share trades at ₹60. A new issue would cost ₹3 a share in flotation. Its beta is 1.3, the risk-free rate is 7% and the market return is 13%. Compute the cost of retained earnings, the cost of new equity, and the CAPM cost of equity.',
          'solution': [table(['Measure', 'Working', 'Result'], [
              ['D1', '4 × 1.08', R(d1)],
              ['Cost of retained earnings (no flotation)', '4.32 ÷ 60 + 8%', f'{ke_old}%'],
              ['Cost of new equity', '4.32 ÷ (60 – 3) + 8%', f'{ke_new}%'],
              ['CAPM Ke', '7% + 1.3 × (13% – 7%)', f'{capm}%']], title='Cost of equity'),
              note('Retained earnings cost slightly less than a fresh issue only because no flotation cost is paid; the shareholders\' required return is the same.')],
          'checks': list(ck2)}

    # i3 — WACC with book-value and market-value weights
    ck3 = Checks()
    bv = ck3.add('round((3000000*15+2000000*15+1000000*11.5+4000000*7.5)/10000000,2)', 'WACC on book weights, %')
    mvt = ck3.add('9000000+900000+3800000', 'Total market value')
    mv = ck3.add('round((9000000*15+900000*11.5+3800000*7.5)/13700000,2)', 'WACC on market weights, %')
    i3 = {'id': 'i3', 'title': 'WACC — book versus market weights', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Krishna Cables Ltd.: equity capital ₹30 lakh (3,00,000 shares of ₹10), retained earnings ₹20 lakh, 11% preference ₹10 lakh, 10% debentures ₹40 lakh. Costs: equity and retained earnings 15%, preference 11.5%, debt 7.5% after tax. Market values: equity ₹30 a share, preference ₹9 lakh, debentures ₹38 lakh. Compute WACC on book and market weights.',
          'solution': [table(['Source', 'Book ₹', 'Market ₹', 'Cost %'], [
              ['Equity capital', inr(3000000), inr(9000000) + ' (3,00,000 × ₹30, covers retained earnings too)', '15'],
              ['Retained earnings', inr(2000000), '—', '15'],
              ['Preference', inr(1000000), inr(900000), '11.5'],
              ['Debentures', inr(4000000), inr(3800000), '7.5'],
              ['Total', inr(10000000), inr(mvt), '']], title='Weights'),
              p(f'Book-value WACC = (50 × 15 + 10 × 11.5 + 40 × 7.5) ÷ 100 = {bv}%. Market-value WACC = (90 × 15 + 9 × 11.5 + 38 × 7.5) ÷ 137 = {mv}%.'),
              note('The market price of equity already reflects retained earnings, so retained earnings get no separate market weight.')],
          'checks': list(ck3)}

    kd_t = table(['Instrument', 'Post-tax cost (approximation)'], [
        ['Irredeemable debt', 'I(1 – t) ÷ NP'],
        ['Redeemable debt', '[I(1 – t) + (RV – NP) ÷ n] ÷ [(RV + NP) ÷ 2]'],
        ['Irredeemable preference', 'PD ÷ NP'],
        ['Redeemable preference', '[PD + (RV – NP) ÷ n] ÷ [(RV + NP) ÷ 2]'],
        ['Equity — constant dividend', 'D ÷ P0'],
        ['Equity — growth (Gordon)', 'D1 ÷ P0 + g  (new issue: D1 ÷ (P0 – F) + g)'],
        ['Equity — CAPM', 'Rf + β(Rm – Rf)']], title='Formula sheet (NP = issue price – flotation, or market price for existing securities)')

    concepts = [
        C('c1', T1, [
            'Cost of capital is the return that providers of funds expect for supplying capital; it is the minimum return a project must earn, also called the hurdle, cut-off or required rate.',
            'Uses: discounting cash flows in capital budgeting, comparing sources in financing decisions, and pricing credit periods in receivables policy.',
            'It is measured from investors\' expectations, adjusted for flotation costs paid to intermediaries and for the tax saving on interest. A security priced below its face value tells you investors want more than its coupon.',
            'Factors: supply and demand for funds, savings habits, risk of the business, inflation and, for multinationals, exchange-rate risk.',
            'Exact cost = the IRR that equates net inflow at issue with the post-tax outflows; the shortcut formulas give approximations.'],
          'Cost of capital is the rent a business pays for using other people\'s money.',
          'A finance head rejects a project yielding 11% when the firm\'s cost of capital is 12.5%.'),
        C('c2', T2, [
            'Interest is tax-deductible, so the post-tax cost of debt = pre-tax cost × (1 – t). The saving is called the tax shield.',
            'Irredeemable debt: Kd = I(1 – t) ÷ NP, where NP is issue price less flotation (or the current market price for existing debt).',
            'Redeemable debt (approximation): spread the gap between redemption value and net proceeds evenly over the remaining life and divide by the average of the two values (formula sheet). If discount on issue or premium on redemption is also tax-deductible, a variant applies the (1 – t) to the whole numerator.',
            'Accuracy falls as RV and NP move apart; the shortcut also does not suit bonds repaid in instalments.'],
          'The government pays part of your interest bill through lower tax.',
          'At a 25% tax rate, 12% debt really costs about 9% before adjusting for discount and premium.',
          blocks=[kd_t]),
        C('c3', T3, [
            'YTM (present-value) method: Kd is the IRR at which NP = PV of post-tax interest + PV of redemption value. Try two rates, then interpolate: L + NPV_L ÷ (NPV_L – NPV_H) × (H – L). Preferred in practice.',
            'Zero coupon/deep discount bonds: solve RV = NP × (1 + r)ⁿ by trial; use trial and error rather than the shortcut because RV and NP differ widely.',
            'Amortised bonds repay part of principal each year, so cash flows (principal + falling interest) are uneven; value = Σ Ct ÷ (1 + Kd)ᵗ.',
            'Convertible debentures: take the redemption value as the higher of the cash amount and the expected value of shares on conversion, then compute Kd as for redeemable debt.'],
          'YTM is simply the IRR seen from the issuer\'s side — an inflow today followed by outflows.',
          'A bond issued at ₹2,500 and repaid at ₹1,00,000 after 25 years needs trial and error, not the shortcut.'),
        C('c4', T4, [
            'Preference dividend is paid from post-tax profit, so no tax adjustment is made.',
            'Irredeemable: Kp = PD ÷ NP. Redeemable: same shape as redeemable debt without (1 – t) (formula sheet), or the IRR of the issue cash flows.',
            'Net proceeds deduct flotation costs; if issue price is not given, use the market price.'],
          'Preference shares cost more after tax than debt of the same coupon because there is no tax shield.',
          'A 10% preference share issued at ₹95 costs about 10.5% even with no redemption premium.'),
        C('c5', T5, [
            'Equity has no fixed return, so its cost is inferred from price and expected payouts.',
            'Dividend price approach (constant dividend): Ke = D ÷ P0. Earnings price approach (all earnings paid or EPS constant): Ke = EPS ÷ P0.',
            'Growth (Gordon) approach: Ke = D1 ÷ P0 + g, where D1 = D0(1 + g). For new shares use D1 ÷ (P0 – F) + g, F being flotation per share.',
            'Growth can be estimated from the past trend of dividends or EPS (compound growth) or as g = b × r (retention ratio × return on equity).'],
          'Value = performance ÷ expectation, so if you know value and performance you can back out the expectation.',
          'A share at ₹60 paying ₹4.32 next year and growing 8% implies investors want about 15.2%.'),
        C('c6', T6, [
            'Realised yield approach: Ke is the return shareholders actually earned (dividends plus price change) over past years, used where history is a fair guide to the future.',
            'CAPM: Ke = Rf + β(Rm – Rf). Rf is the risk-free rate, Rm the market return, and β measures how sensitive the share is to market movements; only systematic risk is priced.',
            'CAPM assumes efficient markets, borrowing and lending at the risk-free rate, homogeneous investor expectations and a single period.'],
          'CAPM charges investors only for the risk they cannot diversify away.',
          'A share with β 1.3 needs 7% + 1.3 × 6% = 14.8% when the market premium is 6%.'),
        C('c7', T7, [
            'Retained earnings are not free: shareholders could have invested the dividend elsewhere, so their opportunity cost applies.',
            'Kr equals Ke without flotation cost (no issue expenses). Where shareholders would pay personal tax and brokerage to reinvest a dividend, some texts adjust Kr down for these.'],
          'Profit kept in the business still belongs to shareholders, who expect it to earn their required return.',
          'A company that ignores the cost of retained earnings may accept projects that destroy shareholder value.'),
        C('c8', T8, [
            'WACC = Σ (weight × after-tax cost of each source). It is the discount rate for projects of average risk.',
            'Book-value weights come from the balance sheet — simple and stable, but historical. Market-value weights use current prices — closer to investors\' view but change daily. Target weights use the planned capital structure.',
            'With market weights, equity\'s market value already includes retained earnings; either do not weight retained earnings separately, or split equity market value in the ratio of book values.'],
          'WACC blends the price of each slice of funding by how big that slice is.',
          'Rising share prices increase the equity weight and usually raise market-value WACC.'),
        C('c9', T9, [
            'Marginal cost of capital (MCC) is the WACC of the next rupee raised, using the proportions in which new funds will be raised (marginal weights), so the book-versus-market choice does not arise.',
            'MCC stays flat while component costs are constant, then jumps at break points — for example, when retained earnings run out and costlier new equity is needed, or when cheap debt limits are exhausted.',
            'Break point = funds available at a given cost ÷ that source\'s weight in the target mix.'],
          'The first slices of funding are cheapest; the bill rises as you reach deeper into the market.',
          'With ₹12 lakh of retained earnings and equity at 80% of the mix, MCC rises once total new funds exceed ₹15 lakh.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Setting a hurdle rate', 'role': 'Finance analyst',
         'situation': 'The CFO asks for the company\'s WACC for next year\'s capital budget.',
         'steps': ['List each long-term source with book and market values.', 'Compute post-tax Kd (YTM), Kp and Ke (Gordon and CAPM as a cross-check).', 'Use target or market weights and compute WACC.', 'Flag break points where marginal cost will rise.'],
         'takeaway': 'Present one hurdle rate, with a note on how it rises if new equity is needed.'},
        {'id': 'j2', 'title': 'Choosing between bond and preference issue', 'role': 'Treasury assistant',
         'situation': 'Management compares a 10% bond with a 9.5% preference issue.',
         'steps': ['Compute post-tax cost of each, including flotation and redemption premium.', 'Note that preference dividend gets no tax shield.', 'Add qualitative points: financial risk, covenants, control.'],
         'takeaway': 'Compare post-tax costs, not coupon rates.'},
    ]

    mcqs = [
        Q('m1', 'Which cost of capital is adjusted for tax?', ['Cost of debentures', 'Cost of equity', 'Cost of preference shares', 'Cost of retained earnings'], 0,
          'Only interest on debt is a tax-deductible expense, so the cost of debt is multiplied by (1 – t). Preference and equity dividends are paid from post-tax profit, so no tax adjustment applies to them or to retained earnings. In practice: always state Kd after tax.', 'c2', T2),
        Q('m2', '10% irredeemable debentures of ₹100 quoted at ₹80; tax 30%. Post-tax Kd is:', ['8.75%', '7%', '12.5%', '10%'], 0,
          'Kd = I(1 – t) ÷ NP = 10 × 0.70 ÷ 80 = 8.75%. The market price stands in for net proceeds because the debt already exists, and the low price pushes the cost above the coupon after tax. In practice: use the current price for existing debt.', 'c2', T2, 'core', check=8.75),
        Q('m3', 'The approximation formula for redeemable debt becomes unreliable when:', ['Redemption value and net proceeds differ widely', 'The tax rate is high', 'Interest is paid annually', 'The bond is issued at par'], 0,
          'The shortcut spreads the redemption gap evenly and uses an average base; when RV and NP are far apart (deep discount bonds) the error grows large, so the IRR (YTM) method should be used instead. In practice: use trial and error for zero coupon bonds.', 'c3', T3, 'moderate'),
        Q('m4', 'For a convertible debenture, the redemption value used in computing cost is:', ['The higher of cash redemption value and expected value of shares on conversion', 'Always the face value', 'The lower of the two values', 'The current market price'], 0,
          'Investors are assumed to choose the more valuable option at maturity, so the higher of the cash amount and the expected value of the shares receivable is taken as RV. The rest of the computation is as for redeemable debt. In practice: project the share price with its growth rate.', 'c3', T3),
        Q('m5', '12% irredeemable preference shares of ₹100 issued at ₹100 with 4% flotation cost. Kp is:', ['12.5%', '12%', '11.52%', '8.4%'], 0,
          'Net proceeds = ₹100 – ₹4 = ₹96, so Kp = 12 ÷ 96 = 12.5%. No tax adjustment is made because preference dividend is an appropriation of profit, not an expense. In practice: flotation pushes cost above the coupon.', 'c4', T4, 'core', check=12.5),
        Q('m6', 'D0 ₹2, growth 5%, market price ₹30. Cost of equity by the growth model is:', ['12%', '11.67%', '6.67%', '10%'], 0,
          'D1 = 2 × 1.05 = ₹2.10; Ke = 2.10 ÷ 30 + 5% = 7% + 5% = 12%. Using D0 instead of D1 would understate the cost. In practice: check whether the dividend given is just paid or next expected.', 'c5', T5, 'core', check=12),
        Q('m7', 'For a new equity issue, the growth-model cost of equity is computed as:', ['D1 ÷ (P0 – F) + g', 'D1 ÷ P0 + g', 'D0 ÷ P0', 'EPS ÷ P0'], 0,
          'New shares bring in only the price less flotation cost per share, so the denominator is P0 – F; this makes new equity costlier than retained earnings. The other forms apply to existing shares or to no-growth cases. In practice: note flotation per share, not per issue.', 'c5', T5),
        Q('m8', 'Risk-free rate 6%, market return 12%, β 1.5. CAPM cost of equity is:', ['15%', '18%', '9%', '13.5%'], 0,
          'Ke = Rf + β(Rm – Rf) = 6% + 1.5 × (12% – 6%) = 6% + 9% = 15%. The market risk premium of 6% is scaled by beta. In practice: CAPM prices only systematic risk.', 'c6', T6, 'core', check=15),
        Q('m9', 'Which is NOT an assumption of CAPM?', ['Investors have different expectations about risk and return', 'Investors can borrow and lend at the risk-free rate', 'Markets are efficient', 'Decisions are made for a single period'], 0,
          'CAPM assumes homogeneous expectations — all investors see the same risk and return — along with risk-free borrowing and lending, efficient markets and a single-period horizon. Different expectations contradict the model. In practice: real markets only approximate these assumptions.', 'c6', T6, 'moderate'),
        Q('m10', 'The cost of retained earnings is usually taken as:', ['Cost of equity without flotation cost', 'Zero, since no payment is made', 'Cost of debt', 'Cost of preference shares'], 0,
          'Retained profits belong to shareholders, who could have invested them elsewhere; their required return applies, but no issue expenses are incurred, so Kr equals Ke excluding flotation. Treating it as free overstates project returns. In practice: Kr is slightly below the cost of new equity.', 'c7', T7),
        Q('m11', 'Equity is 70% of capital (Ke 10%) and debt 30% (pre-tax 5%); tax 30%. WACC is:', ['8.05%', '8.5%', '7.55%', '8.70%'], 0,
          'Post-tax Kd = 5% × 0.70 = 3.5%. WACC = 0.70 × 10% + 0.30 × 3.5% = 7% + 1.05% = 8.05%. Forgetting the tax shield gives 8.5%. In practice: weights must add up to 100%.', 'c8', T8, 'core', check=8.05),
        Q('m12', 'Market-value weights for WACC are preferred mainly because they:', ['Reflect the current opportunity cost of investors', 'Never change', 'Are taken directly from the balance sheet', 'Ignore retained earnings'], 0,
          'Market values show what investors would pay for the firm\'s securities today, so they align with current required returns. Book values are historical; market values change with prices but are more relevant. In practice: many firms use target weights based on market values.', 'c8', T8),
        Q('m13', 'Marginal cost of capital is the cost of:', ['Raising an additional rupee of funds', 'Existing capital at book value', 'Only new equity', 'Debt alone'], 0,
          'MCC is the weighted cost of new funds using the proportions in which they will be raised. It rises at break points when cheaper sources are exhausted. In practice: it is the relevant rate for new projects.', 'c9', T9),
        Q('m14', 'Retained earnings available ₹9,00,000; equity is 60% of the target mix. The break point beyond which new equity is needed is:', ['₹15,00,000', '₹9,00,000', '₹5,40,000', '₹22,50,000'], 0,
          'Break point = funds available at the lower cost ÷ weight of that source = ₹9,00,000 ÷ 0.60 = ₹15,00,000. Beyond that total, the equity part must come from a costlier new issue. In practice: compute one break point per source.', 'c9', T9, 'hard', check=1500000),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Irredeemable Kd', 1, 'computation', '0.75|25%', nums=[kd1]),
           S('s2', 'Net proceeds', 0.5, 'computation', 'net proceeds|94', nums=[np2]),
           S('s3', 'Approximation', 2, 'computation', 'approximation|average', nums=[kd2]),
           S('s4', 'NPV at two rates', 1.5, 'computation', 'npv', nums=[pv_lo, pv_hi]),
           S('s5', 'YTM', 1, 'computation', 'ytm|irr', nums=[ytm])],
          ['Show post-tax interest first.'], ['Using face value instead of net proceeds.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'D1', 1, 'computation', 'd1', nums=[d1]),
           S('s2', 'Kr', 1, 'computation', 'retained', nums=[ke_old]),
           S('s3', 'New equity', 1, 'computation', 'new|flotation', nums=[ke_new]),
           S('s4', 'CAPM', 1, 'computation', 'capm|beta', nums=[capm])],
          ['Grow D0 to D1.'], ['Deducting flotation for retained earnings.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 6, i3['q'], i3['solution'],
          [S('s1', 'Book weights', 2, 'computation', 'book', nums=[bv]),
           S('s2', 'Market values', 1.5, 'computation', 'market', nums=[mvt]),
           S('s3', 'Market WACC', 2, 'computation', 'market', nums=[mv]),
           S('s4', 'Retained earnings in market weights', 0.5, 'concept', 'retained')],
          ['Keep retained earnings out of market weights.'], ['Adding retained earnings to market value of equity.'], ['Table + working.'], pad='table', checks=list(ck3)),
        W('q4', 4, 'Explain the marginal cost of capital and why it rises in steps.',
          [p('The marginal cost of capital is the weighted average cost of each additional rupee raised, using the proportions in which the new funds will be raised. While each source can be obtained at an unchanged cost, the MCC equals the existing WACC. It rises at break points: when cheap sources run out — for example retained earnings are exhausted and new shares with flotation cost must be issued, or a lender charges more beyond a borrowing limit. Break point = funds available at a cost ÷ that source\'s proportion in the mix. New projects should be judged against the MCC at the level of funding they need.')],
          [S('s1', 'Definition', 1, 'concept', 'additional|next rupee|new funds'),
           S('s2', 'Marginal weights', 1, 'concept', 'proportion|weights'),
           S('s3', 'Break points', 1.5, 'concept', 'break point|exhausted|run out'),
           S('s4', 'Use for projects', 0.5, 'concept', 'project')],
          ['Define, then explain steps.'], ['Confusing MCC with book WACC.'], ['Short paragraph.']),
    ]

    viva = [
        V('v1', 'Why is the cost of debt lower than the cost of equity?',
          'Lenders bear less risk because interest and repayment are contractual and rank first, and interest is tax-deductible, which further lowers the effective cost.',
          [P('p1', 'Lower risk for lenders', 5, 'risk|priority|first'), P('p2', 'Tax-deductible interest', 5, 'tax')], 'c2'),
        V('v2', 'How is the cost of a new equity issue different from the cost of retained earnings?',
          'New equity bears flotation costs, so the company receives the price less those costs and its cost is higher; retained earnings have no flotation cost.',
          [P('p1', 'Flotation cost', 6, 'flotation|issue cost'), P('p2', 'New equity costs more', 4, 'higher|more')], 'c7'),
        V('v3', 'What does beta measure in CAPM?',
          'Beta measures the sensitivity of a share\'s returns to market returns, that is, its systematic or non-diversifiable risk.',
          [P('p1', 'Sensitivity to market', 6, 'sensitiv|market'), P('p2', 'Systematic risk', 4, 'systematic|non-diversifiable')], 'c6'),
        V('v4', 'Why is YTM preferred to the approximation formula for debt?',
          'YTM finds the exact rate that equates net proceeds with the present value of post-tax interest and redemption, while the shortcut is only an average and loses accuracy when values differ widely.',
          [P('p1', 'Exact IRR', 6, 'exact|irr|present value'), P('p2', 'Shortcut inaccurate', 4, 'approximate|accuracy|differ')], 'c3'),
        V('v5', 'Which weights can be used for WACC?',
          'Book-value weights from the balance sheet, market-value weights from current prices, and target or marginal weights for planned financing.',
          [P('p1', 'Book value', 3, 'book'), P('p2', 'Market value', 4, 'market'), P('p3', 'Target or marginal', 3, 'target|marginal')], 'c8'),
    ]

    cases = [{'id': 'k1', 'title': 'Sahyog Agro\'s expansion', 'difficulty': 'moderate',
              'case': 'Sahyog Agro Ltd. plans ₹20 lakh of new investment in a 40% debt / 60% equity mix. It has ₹6 lakh of retained earnings. Debt costs 10% before tax (tax 25%). Its share sells at ₹50, the next dividend is ₹3 and growth is 6%. A new issue would cost ₹2.50 a share in flotation.',
              'mcqs': [
                  M('k1a', 'Cost of retained earnings is:', ['12%', '12.32%', '6%', '7.5%'], 0,
                    'Kr = D1 ÷ P0 + g = 3 ÷ 50 + 6% = 6% + 6% = 12%. No flotation cost applies to retained earnings, which makes them cheaper than a fresh issue. In practice: use D1, the next dividend.', 'core', check=12, topic=T7),
                  M('k1b', 'Cost of new equity is about:', ['12.32%', '12%', '13%', '6.32%'], 0,
                    'Ke = 3 ÷ (50 – 2.50) + 6% = 6.32% + 6% = 12.32%. The flotation cost reduces what the company receives per share and so raises the cost. In practice: compute it per share.', 'moderate', check=12.32, topic=T5),
                  M('k1c', 'The break point for retained earnings is:', ['₹10,00,000', '₹6,00,000', '₹15,00,000', '₹3,60,000'], 0,
                    'Retained earnings of ₹6 lakh can finance the equity part of total funding up to ₹6 lakh ÷ 0.60 = ₹10 lakh. Beyond that, new equity at the higher cost is needed. In practice: MCC jumps at this point.', 'hard', check=1000000, topic=T9),
                  M('k1d', 'MCC for the first ₹10 lakh is:', ['10.2%', '10.39%', '9.2%', '11%'], 0,
                    'Post-tax Kd = 10% × 0.75 = 7.5%. MCC = 0.40 × 7.5% + 0.60 × 12% = 3% + 7.2% = 10.2%. Beyond ₹10 lakh it becomes 0.40 × 7.5% + 0.60 × 12.32% ≈ 10.39%. In practice: report both slabs.', 'hard', check=10.2, topic=T9),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch04', 1, 'Cost of Capital',
                ['Explain the meaning, significance and determinants of cost of capital.',
                 'Compute the cost of debt (irredeemable, redeemable, YTM, zero coupon, convertible) and of preference shares.',
                 'Compute the cost of equity by dividend, earnings, growth, realised yield and CAPM approaches, and the cost of retained earnings.',
                 'Compute WACC on book and market weights.',
                 'Compute marginal cost of capital and its break points.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 55}, 'prereq': ['int-p6-a-ch03-u01'],
                 'exam_tip': 'Expect a full WACC sum: Kd by YTM, Kp, Ke by Gordon or CAPM, then book and market weights; MCC with break points is a favourite follow-up.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Cost of capital = investors\' required return; the hurdle rate for projects.', 'Kd after tax = I(1 – t)/NP; redeemable adds (RV – NP)/n over average value; YTM is exact.',
                             'Kp = PD/NP (no tax adjustment).', 'Ke: D/P0, EPS/P0, D1/P0 + g, realised yield, CAPM.',
                             'New equity: D1/(P0 – F) + g; retained earnings: no flotation.', 'WACC = Σ weight × cost; book, market or target weights.',
                             'MCC rises at break points = funds at a cost ÷ weight.'],
                 'remember': ['Use D1, not D0, in Gordon\'s model.', 'Market value of equity already includes retained earnings.'],
                 'traps': ['No tax adjustment for preference dividend.', 'Shortcut formula fails for deep discount bonds.']},
                [('Irredeemable Kd', 'I(1–t)/NP'), ('Gordon Ke', 'D1/P0 + g'), ('New equity', 'D1/(P0–F) + g'), ('CAPM', 'Rf + β(Rm–Rf)'),
                 ('Kp', 'PD/NP'), ('Break point', 'Funds ÷ weight')],
                viva, cases,
                topics=['Introduction', 'Meaning of Cost of Capital', 'Significance of Cost of Capital', 'Determination of Cost of Capital', 'Cost of Long-term Debt',
                        'Cost of Preference Share Capital', 'Cost of Equity Share Capital', 'Cost of Retained Earnings', 'Weighted Average Cost of Capital', 'Marginal Cost of Capital'])
