"""CA Final · Paper 2 Advanced Financial Management · Chapter 5 Security Valuation.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch05-u01'
T1 = 'Return concepts and the required return on equity'
T2 = 'Valuing equity: dividends, earnings, free cash flows and EV'
T3 = 'Rights, preference shares and warrants'
T4 = 'Bond valuation, duration and the yield curve'
T5 = 'Money market instruments and the role of valuers'


def build():
    ck = Checks()
    ke = ck.add('7+1.2*6', 'Cost of equity by CAPM (%)')
    val = ck.add('round(50/((7+1.2*6)/100-0.06),2)', 'Equity value using FCFE (₹ crore)')
    terp = ck.add('(4*150+100)/5', 'Theoretical ex-rights price (₹)')
    rv = ck.add('((4*150+100)/5-100)/4', 'Value of a right per existing share (₹)')
    i1 = {'id': 'i1', 'title': 'FCFE valuation and a rights issue', 'difficulty': 'moderate', 'minutes': 10,
          'q': '(a) Prism Ltd. expects free cash flow to equity of ₹50 crore next year, growing at 6% forever. Risk-free rate 7%, beta 1.2, equity risk premium 6%. Value the equity. (b) Its shares trade at ₹150 cum-rights; it offers 1 new share for every 4 held at ₹100. Compute the theoretical ex-rights price and value of a right per existing share.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Cost of equity', '7% + 1.2 × 6%', inr(ke) + '%'],
              ['Equity value', '50 ÷ (0.142 − 0.06)', '₹' + inr(val) + ' crore'],
              ['TERP', '(4 × 150 + 100) ÷ 5', '₹' + inr(terp)],
              ['Value of right per existing share', '(140 − 100) ÷ 4', '₹' + inr(rv)]], title='Equity valuation')],
          'checks': list(ck)}

    ck2 = Checks()
    price = ck2.add('round(80/1.1+80/1.1**2+1080/1.1**3,2)', 'Bond price at 10% YTM (₹)')
    mac = ck2.add('round((80/1.1+2*80/1.1**2+3*1080/1.1**3)/(80/1.1+80/1.1**2+1080/1.1**3),4)', 'Macaulay duration (years)')
    mod = ck2.add('round((80/1.1+2*80/1.1**2+3*1080/1.1**3)/(80/1.1+80/1.1**2+1080/1.1**3)/1.1,4)', 'Modified duration')
    i2 = {'id': 'i2', 'title': 'Bond price and duration', 'difficulty': 'hard', 'minutes': 10,
          'q': 'A ₹1,000 bond pays an 8% annual coupon and matures in 3 years. The market yield is 10%. Compute its price, Macaulay duration and modified duration, and estimate the % price change if yield rises by 0.5%.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['PV of cash flows', '80/1.1 + 80/1.1² + 1,080/1.1³', '72.73 + 66.12 + 811.42'],
              ['Price', 'Sum', '₹' + inr(price)],
              ['Macaulay duration', '(1×72.73 + 2×66.12 + 3×811.42) ÷ 950.26', inr(mac) + ' years'],
              ['Modified duration', '2.7774 ÷ 1.10', inr(mod)],
              ['Price change for +0.5% yield', '−2.525 × 0.5%', 'about −1.26%']], title='Duration')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Valuation estimates what an asset is worth from its expected cash flows and risk. Return concepts: required return (minimum acceptable return for the risk), discount rate (rate used to compute present values) and internal rate of return (rate equating price with expected cash flows).',
            'The equity risk premium is the extra return investors demand for holding equities over risk-free assets; estimated historically (average past excess returns) or forward-looking (e.g. implied from dividend yields and growth).',
            'Required return on equity is often estimated with CAPM: Ke = Rf + β (Rm − Rf); alternatives include build-up methods and the dividend growth model. Discount rates must match cash flows: nominal with nominal, real with real; FCFF with WACC; FCFE and dividends with cost of equity.'],
          'The right discount rate depends on whose cash flow you are valuing.',
          'With Rf 7%, β 1.2 and ERP 6%, Ke = 14.2%.'),
        C('c2', T2, [
            'Dividend discount models: constant growth P₀ = D₁ ÷ (Ke − g); multi-stage models for high-growth then stable phases. Earnings models use P/E multiples or the earnings yield.',
            'Free cash flow models: FCFF = EBIT(1 − t) + depreciation − capital expenditure − increase in working capital, discounted at WACC to value the firm; FCFE = FCFF − interest(1 − t) + net borrowing, discounted at Ke to value equity. FCFE suits firms that pay little dividend relative to capacity.',
            'Enterprise value = market value of equity + debt + preference capital + minority interest − cash and equivalents. EV/Sales suits loss-making or early-stage firms; EV/EBITDA neutralises capital structure and depreciation differences.'],
          'Value the firm with FCFF and WACC, or equity with FCFE and Ke.',
          'EV/EBITDA lets you compare firms with different debt levels.'),
        C('c3', T3, [
            'Theoretical ex-rights price (TERP) = (existing shares × cum-rights price + subscription money) ÷ total shares after issue. Value of a right per existing share = (TERP − subscription price) ÷ number of existing shares needed for one new share.',
            'Preference shares: irredeemable value = dividend ÷ required return; redeemable value = PV of dividends + PV of redemption amount.',
            'Warrants give the right to buy shares at a fixed price: theoretical value = (market price of share − exercise price) × shares per warrant (minimum value), with actual value usually higher due to time value. Convertible debentures are valued as straight debt plus the conversion option; conversion value = conversion ratio × share price.'],
          'Rights shift value from old shares to the new subscription — wealth is unchanged if rights are used or sold.',
          'A 1-for-4 issue at ₹100 when shares trade at ₹150 gives a TERP of ₹140.'),
        C('c4', T4, [
            'Bond value = PV of coupons + PV of redemption value at the required yield. Yield to maturity is the IRR of the bond. Prices and yields move inversely; discount bonds rise toward par as maturity nears; longer and lower-coupon bonds are more price-sensitive.',
            'Macaulay duration is the weighted average time to receive the bond\'s cash flows (weights = PV of each cash flow ÷ price). Modified duration = Macaulay ÷ (1 + yield) and estimates % price change ≈ −modified duration × change in yield. Convexity corrects for curvature. Immunisation matches portfolio duration with the investment horizon so price and reinvestment effects offset.',
            'The yield curve shows yields across maturities (normal upward, inverted, flat, humped). Term structure theories: expectations, liquidity preference and market segmentation. Zero-coupon bonds have duration equal to maturity; refunding replaces old high-coupon bonds when rates fall, if NPV is positive.'],
          'Duration is the bond\'s interest-rate sensitivity in years.',
          'A 3-year 8% bond at 10% YTM has duration of about 2.78 years.'),
        C('c5', T5, [
            'Money market instruments have maturities up to one year: call/notice money (interbank, overnight to 14 days), treasury bills (91, 182, 364 days, issued at discount), commercial bills, certificates of deposit (issued by banks), commercial paper (unsecured short-term notes of corporates), and repo/reverse repo (sale and repurchase of securities, used for liquidity management).',
            'Yield on a discount instrument = (face value − price) ÷ price × (365 ÷ days).',
            'Registered valuers (under the Companies Act and IBBI rules) must be independent, competent, follow valuation standards, document assumptions, avoid conflicts of interest and maintain confidentiality; their reports support transactions, insolvency proceedings and regulatory filings.'],
          'Short-term instruments manage liquidity; valuers bring independence to value.',
          'A 91-day T-bill bought at ₹98 for ₹100 face yields about 8.2% a year.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Valuing a listed company', 'role': 'Valuation analyst',
             'situation': 'An investor wants a fair value for a mid-sized engineering firm.',
             'steps': ['Estimate Ke and WACC.', 'Forecast FCFF and FCFE.', 'Value using DCF and EV/EBITDA comparables.', 'Reconcile and present a range.'],
             'takeaway': 'Use more than one method and explain the differences.'}]

    mcqs = [
        Q('m1', 'FCFF is discounted at:', ['WACC', 'Cost of equity', 'Risk-free rate', 'Cost of debt'], 0,
          'It belongs to all capital providers. In practice: subtract debt for equity.', 'c2', T2),
        Q('m2', 'Enterprise value equals:', ['Equity + debt + preference + minority − cash', 'Equity only', 'Assets − liabilities', 'Sales × margin'], 0,
          'Value of operating business. In practice: EV/EBITDA.', 'c2', T2),
        Q('m3', 'Modified duration equals:', ['Macaulay duration ÷ (1 + yield)', 'Maturity × coupon', 'Price ÷ yield', 'Coupon ÷ price'], 0,
          'Measures price sensitivity. In practice: % change ≈ −MD × Δy.', 'c4', T4),
        Q('m4', 'A higher coupon rate, other things equal, makes duration:', ['Shorter', 'Longer', 'Unchanged', 'Infinite'], 0,
          'More cash comes earlier. In practice: zero-coupon duration = maturity.', 'c4', T4),
        Q('m5', 'The liquidity preference theory says long-term yields include:', ['A premium for holding longer bonds', 'No premium', 'Only expected rates', 'Negative premium'], 0,
          'Investors want compensation. In practice: normal upward curve.', 'c4', T4),
        Q('m6', 'Commercial paper is:', ['An unsecured short-term note issued by corporates', 'A bank deposit', 'A government bond', 'A share'], 0,
          'Money market instrument. In practice: issued at discount.', 'c5', T5),
        Q('m7', 'Value of an irredeemable preference share equals:', ['Dividend ÷ required return', 'Face value', 'Dividend × years', 'Market price ÷ yield'], 0,
          'A perpetuity. In practice: redeemable adds redemption PV.', 'c3', T3),
        Q('m8', 'The equity risk premium is:', ['Extra return expected on equities over risk-free assets', 'Bond coupon', 'Inflation rate', 'Dividend yield only'], 0,
          'Key CAPM input. In practice: historical or implied.', 'c1', T1),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Ke', 1.5, 'computation', 'cost of equity', nums=[ke]), S('s2', 'Value', 2, 'computation', 'equity value', nums=[val]), S('s3', 'TERP', 2, 'computation', 'terp', nums=[terp]), S('s4', 'Right value', 1.5, 'computation', 'right', nums=[rv])],
          ['Use Ke for FCFE.'], ['Discounting FCFE at WACC.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 8, i2['q'], i2['solution'],
          [S('s1', 'Price', 2, 'computation', 'price', nums=[price]), S('s2', 'Macaulay', 3, 'computation', 'macaulay', nums=[mac]), S('s3', 'Modified', 2, 'computation', 'modified', nums=[mod]), S('s4', 'Price change', 1, 'concept', 'change')],
          ['Show weights.'], ['Forgetting to divide by price.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'State the CAPM formula.', 'Required return equals the risk-free rate plus beta times the market risk premium.',
          [P('p1', 'Risk-free plus', 5, 'risk-free'), P('p2', 'Beta times premium', 5, 'beta')], 'c1'),
        V('v2', 'Distinguish FCFF and FCFE.', 'FCFF is cash available to all capital providers, discounted at WACC; FCFE is cash available to equity after debt flows, discounted at the cost of equity.',
          [P('p1', 'All providers and WACC', 5, 'wacc'), P('p2', 'Equity after debt', 5, 'cost of equity')], 'c2'),
        V('v3', 'How is the theoretical ex-rights price computed?', 'Existing shares times the cum-rights price plus subscription money, divided by total shares after the issue.',
          [P('p1', 'Cum-rights price and subscription', 5, 'subscription'), P('p2', 'Total shares', 5, 'total shares')], 'c3'),
        V('v4', 'What is immunisation?', 'Matching the duration of a bond portfolio with the investment horizon so that price and reinvestment effects offset.',
          [P('p1', 'Match duration', 5, 'duration'), P('p2', 'Offset effects', 5, 'offset')], 'c4'),
        V('v5', 'What is a repo?', 'A sale of securities with an agreement to buy them back at a set price and date, used to borrow short term.',
          [P('p1', 'Sale and buy back', 5, 'buy them back|repurchase'), P('p2', 'Short-term borrowing', 5, 'borrow')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Granite Infra Ltd.', 'difficulty': 'moderate',
              'case': 'Granite Infra Ltd. has market capitalisation ₹2,400 crore, debt ₹900 crore, cash ₹300 crore and EBITDA ₹500 crore. Peers trade at 7× EV/EBITDA. It also issues a 91-day commercial paper of face value ₹100 at ₹98.',
              'mcqs': [
                  M('k1a', 'Enterprise value of Granite (₹ crore):', ['3,000', '3,300', '2,400', '3,600'], 0,
                    '2,400 + 900 − 300. In practice: add preference and minority if any.', 'core', check=3000, topic=T2),
                  M('k1b', 'Granite\'s EV/EBITDA multiple:', ['6', '7', '4.8', '6.6'], 0,
                    '3,000 ÷ 500. In practice: below peers.', 'core', check=6, topic=T2),
                  M('k1c', 'Implied equity value at peer multiple (₹ crore):', ['2,900', '3,500', '2,400', '3,200'], 0,
                    '7 × 500 = 3,500 EV − 900 + 300. In practice: suggests undervaluation.', 'moderate', check=2900, topic=T2),
                  M('k1d', 'Annualised yield on the CP (%, two decimals):', ['8.19', '2.04', '8', '7.84'], 0,
                    '(2 ÷ 98) × (365 ÷ 91). In practice: discount instrument yield.', 'moderate', check=8.19, topic=T5),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch05', 1, 'Security Valuation',
                ['Explain return concepts and estimate the required return on equity.',
                 'Value equity with dividend, earnings, free cash flow and EV methods.',
                 'Value rights, preference shares, warrants and convertibles.',
                 'Value bonds and measure duration, convexity and yield curves.',
                 'Describe money market instruments and the role of valuers.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 50}, 'prereq': ['fin-p2-ch04-u01'],
                 'exam_tip': 'Match each cash flow with its rate: FCFF–WACC, FCFE/dividends–Ke, bonds–YTM.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Ke = Rf + β(ERP).',
                             'DDM, FCFF/WACC, FCFE/Ke, EV multiples.',
                             'TERP and value of rights.',
                             'Bond price, YTM, duration, convexity, immunisation.',
                             'Money market instruments; valuers\' duties.'],
                 'remember': ['%ΔP ≈ −MD × Δy.'],
                 'traps': ['Forgetting to deduct cash in EV.']},
                [('FCFF', 'WACC'), ('FCFE', 'Ke'), ('TERP', '(nP + S) ÷ (n + n₁)'), ('MD', 'MacD ÷ (1 + y)')],
                viva, cases)
