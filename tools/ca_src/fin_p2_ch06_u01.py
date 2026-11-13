"""CA Final · Paper 2 Advanced Financial Management · Chapter 6 Portfolio Management.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch06-u01'
T1 = 'Portfolio process, risk types and diversification'
T2 = 'Portfolio return and risk; Markowitz efficient frontier'
T3 = 'CAPM, single index model and APT'
T4 = 'Evaluating portfolio performance'
T5 = 'Portfolio strategies, revision and alternative investments'


def build():
    ck = Checks()
    er = ck.add('0.6*12+0.4*18', 'Expected portfolio return (%)')
    var = ck.add('0.36*225+0.16*625+2*0.6*0.4*0.3*15*25', 'Portfolio variance')
    sd = ck.add('round((0.36*225+0.16*625+2*0.6*0.4*0.3*15*25)**0.5,2)', 'Portfolio standard deviation (%)')
    wmin = ck.add('round((625-0.3*15*25)/(225+625-2*0.3*15*25),2)', 'Minimum-variance weight of A')
    i1 = {'id': 'i1', 'title': 'A two-share portfolio', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Share A: expected return 12%, standard deviation 15%. Share B: expected return 18%, standard deviation 25%. Correlation 0.3. Compute the return and risk of a 60:40 portfolio, and the weight of A in the minimum-variance portfolio.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Expected return', '0.6 × 12 + 0.4 × 18', inr(er) + '%'],
              ['Covariance', '0.3 × 15 × 25', '112.5'],
              ['Variance', '0.36×225 + 0.16×625 + 2×0.6×0.4×112.5', inr(var)],
              ['Standard deviation', '√235', inr(sd) + '%'],
              ['Minimum-variance weight of A', '(625 − 112.5) ÷ (225 + 625 − 225)', inr(wmin)]], title='Two-asset portfolio')],
          'checks': list(ck)}

    ck2 = Checks()
    sh = ck2.add('(16-6)/20', 'Sharpe ratio')
    tr = ck2.add('round((16-6)/1.2,2)', 'Treynor ratio (%)')
    ja = ck2.add('round(16-(6+1.2*(13-6)),2)', 'Jensen\'s alpha (%)')
    msh = ck2.add('round((13-6)/14,2)', 'Market Sharpe ratio')
    i2 = {'id': 'i2', 'title': 'Judging a fund manager', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Fund F earned 16% with standard deviation 20% and beta 1.2. The market earned 13% with standard deviation 14%. Risk-free rate 6%. Compute Sharpe, Treynor and Jensen measures and conclude.',
          'solution': [table(['Measure', 'Working', 'Result'], [
              ['Sharpe (fund)', '(16 − 6) ÷ 20', inr(sh)],
              ['Sharpe (market)', '(13 − 6) ÷ 14', inr(msh)],
              ['Treynor (fund)', '(16 − 6) ÷ 1.2', inr(tr) + '% (market 7%)'],
              ['Jensen\'s alpha', '16 − [6 + 1.2 × 7]', inr(ja) + '%'],
              ['Conclusion', 'Equal on total risk; better on systematic risk', 'Positive alpha']], title='Performance measures')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Portfolio management builds and manages a mix of investments to meet an investor\'s objectives — safety, stable income, capital growth, liquidity, tax efficiency — within their risk tolerance. Phases: security analysis, portfolio analysis, selection, revision and evaluation.',
            'Total risk = systematic risk (market-wide: interest rates, inflation, economic cycles, currency — cannot be diversified away) + unsystematic risk (company or industry specific: management, labour, competition — diversifiable).',
            'Diversification reduces unsystematic risk as more securities with less-than-perfect correlation are added; beyond a point only systematic risk remains, which is why markets reward only systematic (beta) risk.'],
          'Diversify away what you can; get paid only for what you cannot.',
          'Holding 25 well-chosen shares removes most company-specific risk.'),
        C('c2', T2, [
            'A portfolio\'s expected return is simply each security\'s expected return multiplied by its weight, summed. Portfolio risk for two assets: σp² = wA²σA² + wB²σB² + 2wAwBρσAσB, where covariance = ρσAσB. Lower correlation means more risk reduction; with ρ = −1 risk can be eliminated.',
            'Minimum-variance weight of A = (σB² − Cov) ÷ (σA² + σB² − 2Cov). For more than two securities, risk sums over all pairs of covariances.',
            'Markowitz model: investors are risk-averse and judge portfolios by mean and variance; efficient portfolios give the highest return for each risk level, forming the efficient frontier. Combining the risk-free asset with the market portfolio gives the capital market line: E(Rp) = Rf + [(Rm − Rf) ÷ σm] × σp.'],
          'Correlation is the secret ingredient of diversification.',
          'Two shares with correlation 0.3 give a portfolio less risky than their average risk.'),
        C('c3', T3, [
            'CAPM: E(Ri) = Rf + βi (Rm − Rf). Beta = Cov(i, m) ÷ σm², the sensitivity to market movements. The security market line plots required return against beta; a stock above the line is undervalued (expected return exceeds required) and below it is overvalued.',
            'Single index (Sharpe) model: return = α + βRm + e; total risk = β²σm² + residual variance; reduces the inputs needed versus full covariance. Portfolio beta is the weighted average of betas.',
            'Arbitrage pricing theory: expected return depends on several macro factors (inflation, GDP, interest rates, etc.) with factor sensitivities; no single market portfolio is required. CAPM limitations: unrealistic assumptions, beta instability, and difficulty identifying the true market portfolio.'],
          'Required return rises with beta, not total risk.',
          'Beta 1.5 means the stock tends to move 1.5% for a 1% market move.'),
        C('c4', T4, [
            'Sharpe ratio = (Rp − Rf) ÷ σp — reward per unit of total risk; suits undiversified portfolios. Treynor ratio = (Rp − Rf) ÷ βp — reward per unit of systematic risk; suits well-diversified portfolios.',
            'Jensen\'s alpha = Rp − [Rf + βp(Rm − Rf)] — return above what CAPM predicts; positive alpha indicates superior performance.',
            'Sharpe\'s optimal portfolio: rank securities by excess return to beta, compute a cut-off point C*, and include securities whose ratio exceeds the cut-off, weighting them by their excess over C*.'],
          'Use Sharpe for total risk, Treynor for beta, Jensen for value added.',
          'A fund with alpha of 1.6% beat its CAPM benchmark.'),
        C('c5', T5, [
            'Active strategies try to beat the market (market timing, sector rotation, security selection); passive strategies track an index (buy and hold, index funds). Asset allocation can be strategic (long-term mix) or tactical (short-term tilts).',
            'Revision and rebalancing: buy-and-hold (no rebalancing), constant mix (sell winners, buy losers to keep weights), and constant proportion portfolio insurance (CPPI): equity = multiplier × (portfolio value − floor). Formula plans include constant rupee value, constant ratio and dollar-cost averaging.',
            'Fixed income portfolios use passive (buy and hold, indexing, immunisation) or active (interest rate anticipation, swaps, credit) strategies. Alternative investments include real estate (valued by cost, sales comparison or income approach), gold, private equity, hedge funds, commodities and distressed securities.'],
          'Choose a strategy, then rebalance with discipline.',
          'CPPI with floor ₹75 lakh, multiplier 2 and value ₹100 lakh invests ₹50 lakh in equity.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Advising an HNI client', 'role': 'Portfolio manager',
             'situation': 'A client with ₹5 crore wants growth with limited drawdowns.',
             'steps': ['Assess objectives and risk tolerance.', 'Build an efficient mix of equity, debt and gold.', 'Choose a rebalancing rule such as CPPI.', 'Report performance using Sharpe, Treynor and alpha.'],
             'takeaway': 'Process and discipline matter as much as security selection.'}]

    mcqs = [
        Q('m1', 'Unsystematic risk can be:', ['Reduced by diversification', 'Eliminated only by hedging', 'Never reduced', 'Increased by diversification'], 0,
          'Company-specific risks cancel out. In practice: 20–30 stocks.', 'c1', T1),
        Q('m2', 'With correlation of −1 between two assets, portfolio risk:', ['Can be reduced to zero', 'Doubles', 'Is unchanged', 'Equals the larger risk'], 0,
          'Perfect hedge possible. In practice: rare.', 'c2', T2),
        Q('m3', 'Under CAPM, a stock plotting above the security market line is:', ['Undervalued', 'Overvalued', 'Fairly valued', 'Risk-free'], 0,
          'Expected return exceeds required. In practice: buy signal.', 'c3', T3),
        Q('m4', 'The Treynor ratio measures excess return per unit of:', ['Beta', 'Standard deviation', 'Variance', 'Alpha'], 0,
          'Systematic risk. In practice: diversified portfolios.', 'c4', T4),
        Q('m5', 'Jensen\'s alpha is:', ['Actual return minus CAPM-predicted return', 'Return ÷ beta', 'Return ÷ σ', 'Beta − 1'], 0,
          'Value added by manager. In practice: positive is good.', 'c4', T4),
        Q('m6', 'In CPPI, equity exposure equals:', ['Multiplier × (portfolio value − floor)', 'Floor × multiplier', 'Portfolio value ÷ floor', 'Constant amount'], 0,
          'Cushion-based. In practice: sells as markets fall.', 'c5', T5),
        Q('m7', 'The capital market line relates expected return to:', ['Total risk (standard deviation) of efficient portfolios', 'Beta of single stocks', 'Dividend yield', 'Book value'], 0,
          'CML vs SML. In practice: risk-free + market mix.', 'c2', T2),
        Q('m8', 'APT differs from CAPM in using:', ['Multiple macro-economic factors', 'Only beta', 'No risk', 'Only dividends'], 0,
          'Factor sensitivities. In practice: inflation, GDP, rates.', 'c3', T3),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Return', 1.5, 'computation', 'expected', nums=[er]), S('s2', 'Variance and SD', 4, 'computation', 'standard deviation|variance', nums=[var, sd]), S('s3', 'Min variance', 2.5, 'computation', 'minimum', nums=[wmin])],
          ['Compute covariance first.'], ['Ignoring the covariance term.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Sharpe', 2, 'computation', 'sharpe', nums=[sh, msh]), S('s2', 'Treynor', 2, 'computation', 'treynor', nums=[tr]), S('s3', 'Jensen', 2, 'computation', 'jensen|alpha', nums=[ja])],
          ['Compare with market.'], ['Using total risk in Treynor.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Distinguish systematic and unsystematic risk.', 'Systematic risk affects the whole market and cannot be diversified; unsystematic risk is specific to a company or industry and can be diversified away.',
          [P('p1', 'Market-wide', 5, 'market'), P('p2', 'Diversifiable', 5, 'diversif')], 'c1'),
        V('v2', 'What is the efficient frontier?', 'The set of portfolios offering the highest expected return for each level of risk.',
          [P('p1', 'Highest return', 5, 'highest'), P('p2', 'Each risk level', 5, 'risk')], 'c2'),
        V('v3', 'State the CAPM equation.', 'Expected return equals the risk-free rate plus beta times the market risk premium.',
          [P('p1', 'Risk-free rate', 5, 'risk-free'), P('p2', 'Beta and premium', 5, 'beta')], 'c3'),
        V('v4', 'When is the Sharpe ratio preferred to the Treynor ratio?', 'When the portfolio is concentrated in a few holdings, so total risk matters rather than only beta.',
          [P('p1', 'Concentrated', 6, 'concentrated'), P('p2', 'Total risk', 4, 'total risk')], 'c4'),
        V('v5', 'Explain the constant mix strategy.', 'Rebalancing to fixed weights by selling assets that have risen and buying those that have fallen.',
          [P('p1', 'Fixed weights', 5, 'fixed weight'), P('p2', 'Sell winners buy losers', 5, 'selling|buying')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Arjun\'s portfolio', 'difficulty': 'moderate',
              'case': 'Arjun holds shares X (β 1.4, 40%), Y (β 0.8, 35%) and Z (β 1.0, 25%). Risk-free rate 6.5%; market return 12.5%. Share X is expected to return 15%. His portfolio is ₹40 lakh; he wants a floor of ₹30 lakh with a CPPI multiplier of 3.',
              'mcqs': [
                  M('k1a', 'Portfolio beta:', ['1.09', '1.07', '1.00', '1.20'], 0,
                    '0.4×1.4 + 0.35×0.8 + 0.25×1.0 = 1.09. In practice: weighted average.', 'core', check=1.09, topic=T3),
                  M('k1b', 'Required return on X under CAPM (%):', ['14.9', '15', '12.5', '8.4'], 0,
                    '6.5 + 1.4 × 6. In practice: compare with 15%.', 'core', check=14.9, topic=T3),
                  M('k1c', 'X with expected return 15% is:', ['Slightly undervalued', 'Overvalued', 'Risk-free', 'Fairly priced exactly'], 0,
                    'Above the SML by 0.1%. In practice: marginal buy.', 'moderate', topic=T3),
                  M('k1d', 'CPPI equity exposure (₹ lakh):', ['30', '10', '40', '12'], 0,
                    '3 × (40 − 30). In practice: rest in safe assets.', 'core', check=30, topic=T5),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch06', 1, 'Portfolio Management',
                ['Explain the portfolio process, risk types and diversification.',
                 'Compute portfolio return and risk and explain the efficient frontier.',
                 'Apply CAPM, the single index model and APT.',
                 'Evaluate performance with Sharpe, Treynor and Jensen measures.',
                 'Describe portfolio strategies, rebalancing and alternative investments.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 50}, 'prereq': ['fin-p2-ch05-u01'],
                 'exam_tip': 'Write every formula before substituting — examiners award method marks.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Total risk = systematic + unsystematic.',
                             'σp² includes 2wAwBρσAσB.',
                             'CML uses σ; SML uses β.',
                             'Sharpe, Treynor, Jensen.',
                             'Buy-and-hold, constant mix, CPPI.'],
                 'remember': ['Beta = Cov(i,m) ÷ σm².'],
                 'traps': ['Using Treynor for undiversified portfolios.']},
                [('CAPM', 'Rf + β(Rm − Rf)'), ('Sharpe', '(Rp − Rf) ÷ σ'), ('Treynor', '(Rp − Rf) ÷ β'), ('CPPI', 'm × (V − F)')],
                viva, cases)
