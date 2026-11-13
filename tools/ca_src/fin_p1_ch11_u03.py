"""CA Final · Paper 1 Financial Reporting · Chapter 11 Unit 3 Financial Instruments: Equity and Financial Liabilities.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch11-u03'
T1 = 'Obligation to deliver cash: the core test'
T2 = 'Settlement in own equity instruments'
T3 = 'Compound financial instruments'
T4 = 'Treasury shares, distributions and offsetting'


def build():
    ck = Checks()
    liab = ck.add('5*2.5313+100*0.7722', 'Liability component at 9% (₹ lakh)')
    eq = ck.add('100-(5*2.5313+100*0.7722)', 'Equity component (₹ lakh)')
    int1 = ck.add('(5*2.5313+100*0.7722)*0.09', 'Interest expense year 1 (₹ lakh)')
    cl1 = ck.add('(5*2.5313+100*0.7722)*1.09-5', 'Liability at end of year 1 (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Splitting a convertible bond', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Falcon Ltd. issues 3-year convertible bonds for ₹100 lakh with a 5% annual coupon. Each bond converts into a fixed number of shares at maturity. Similar bonds without conversion carry 9% (3-year annuity factor 2.5313; discount factor year 3: 0.7722). Split the instrument and compute year-1 interest and closing liability.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Liability component', '5 × 2.5313 + 100 × 0.7722', inr(liab)],
              ['Equity component (residual)', '100 − 89.88', inr(eq)],
              ['Interest expense year 1', '89.8765 × 9%', inr(int1)],
              ['Liability at end of year 1', '89.8765 + 8.09 − 5', inr(cl1)],
              ['Equity component', 'Not remeasured', inr(eq)]], title='Split accounting')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Liability or equity?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Classify: (a) non-redeemable preference shares with discretionary dividends; (b) preference shares redeemable at a fixed date; (c) perpetual bonds with mandatory interest; (d) a written call on own shares — fixed shares for fixed cash; (e) a contract to deliver shares worth ₹10 lakh; (f) preference shares redeemable at the issuer\'s option with dividends that become mandatory if ordinary dividends are paid.',
          'solution': [table(['Item', 'Classification', 'Reason'], [
              ['(a)', 'Equity', 'No contractual obligation to pay'],
              ['(b)', 'Liability', 'Must pay cash on redemption'],
              ['(c)', 'Liability', 'Interest is unavoidable for ever'],
              ['(d)', 'Equity', 'Fixed for fixed'],
              ['(e)', 'Liability', 'Variable number of shares'],
              ['(f)', 'Equity', 'Issuer can avoid payment by not paying ordinary dividends']], title='Ind AS 32 classification')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'The key feature of a financial liability is a contractual obligation that the issuer cannot avoid to deliver cash or another financial asset. If the issuer has an unconditional right to avoid payment, the instrument is equity.',
            'Substance over form: preference shares mandatorily redeemable, or redeemable at the holder\'s option, are liabilities; dividends on them are interest expense. Perpetual instruments with mandatory interest are liabilities. Economic compulsion (pressure to pay) does not by itself create a liability.',
            'Contingent settlement provisions — paying cash on uncertain future events beyond both parties\' control — make the instrument a liability unless the provision is not genuine or applies only on liquidation.'],
          'Ask: can the issuer legally refuse to pay? If not, it is a liability.',
          'Dividend-discretionary perpetual preference shares are equity.'),
        C('c2', T2, [
            'A contract settled by delivering a variable number of own shares equal to a fixed amount (or an amount varying with something other than share price) is a financial liability — shares are used like currency.',
            'A derivative settled by exchanging a fixed number of own shares for a fixed amount of cash (fixed-for-fixed) is equity. Settlement options (net cash or net shares) make a derivative a financial asset or liability unless all alternatives give equity.',
            'An obligation to buy back own shares for cash (a written put) creates a financial liability measured at the discounted amount payable on buy-back, even if the derivative itself is equity. Rights issues offered pro rata to all owners for a fixed amount in any currency are equity.'],
          'Fixed shares for fixed cash is equity; anything that floats is a liability.',
          'A promise to issue shares worth exactly ₹10 lakh is debt in disguise.'),
        C('c3', T3, [
            'A compound instrument contains both a liability and an equity component, such as a bond convertible into a fixed number of shares. The issuer presents them separately (split accounting).',
            'The liability component is measured first at the fair value of a similar liability without the equity feature; the equity component is the residual. No gain or loss arises at issue. Transaction costs are allocated in proportion.',
            'Classification is not revised for changes in likelihood of conversion. On conversion at maturity, the liability is transferred to equity with no gain or loss; early redemption allocates the payment between components using fair values at that date.'],
          'Value the debt first; equity is what is left.',
          'A 5% convertible issued where debt yields 9% has a sizeable equity part.'),
        C('c4', T4, [
            'Treasury shares (own shares reacquired) are deducted from equity; no gain or loss is recognised on purchase, sale, issue or cancellation, and consideration is recognised directly in equity.',
            'Interest, dividends, gains and losses on financial liabilities go to profit or loss; distributions to holders of equity instruments are recognised directly in equity. Transaction costs of equity transactions are deducted from equity.',
            'A financial asset and liability are offset only when the entity currently has a legally enforceable right to set off and intends either to settle net or to realise and settle simultaneously. The right must not depend on future events and must be enforceable in normal business, default and insolvency.'],
          'Own-share dealings never hit profit; offsetting needs both a right and an intent.',
          'A bank deposit and an overdraft with different banks cannot be offset.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Reviewing an instrument term sheet', 'role': 'Corporate finance analyst',
             'situation': 'The board plans to issue convertible preference shares to an investor.',
             'steps': ['Identify any unavoidable payment obligations.', 'Apply fixed-for-fixed to the conversion feature.', 'Split compound elements at issue.', 'Assess presentation of dividends.'],
             'takeaway': 'Term-sheet wording drives balance sheet classification.'}]

    mcqs = [
        Q('m1', 'The deciding feature of a financial liability is:', ['An unavoidable contractual obligation to deliver cash or financial assets', 'Its legal name', 'Its maturity', 'The holder\'s intention'], 0,
          'Substance over form. In practice: read the contract terms.', 'c1', T1),
        Q('m2', 'In a compound instrument, the component measured first is:', ['The liability', 'The equity', 'Both at fair value', 'Neither'], 0,
          'Equity is the residual. In practice: discount at market rate for similar debt.', 'c3', T3),
        Q('m3', 'Dividends on mandatorily redeemable preference shares are:', ['Interest expense in profit or loss', 'Distributions in equity', 'OCI items', 'Capital reserve'], 0,
          'They follow the liability classification. In practice: include in finance costs.', 'c1', T1),
        Q('m4', 'Gains on resale of treasury shares are:', ['Recognised directly in equity', 'Profit or loss', 'OCI', 'Revenue'], 0,
          'No profit from own equity. In practice: adjust securities premium.', 'c4', T4),
        Q('m5', 'Offsetting a financial asset and liability requires:', ['A legally enforceable right and intention to settle net', 'Same counterparty only', 'Same currency only', 'Auditor approval'], 0,
          'Both conditions are needed. In practice: master netting alone may not suffice.', 'c4', T4),
        Q('m6', 'Economic compulsion to pay dividends:', ['Does not by itself create a liability', 'Creates a liability', 'Creates a provision', 'Is equity reserve'], 0,
          'Only contractual obligations count. In practice: step-up clauses need analysis.', 'c1', T1),
        Q('m7', 'A written put on own shares creates:', ['A liability at the discounted buy-back amount', 'Only equity', 'Nothing', 'An asset'], 0,
          'The entity may have to pay cash. In practice: reclassify from equity.', 'c2', T2),
        Q('m8', 'Classification of a convertible\'s components is revised when conversion becomes likely:', ['No, it is not revised', 'Yes', 'Only at maturity', 'Only if exercised'], 0,
          'Initial split stands. In practice: transfer on conversion.', 'c3', T3),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Liability', 2, 'computation', 'liability', nums=[liab]), S('s2', 'Equity', 2, 'computation', 'equity', nums=[eq]), S('s3', 'Interest', 1.5, 'computation', 'interest', nums=[int1]), S('s4', 'Closing', 1.5, 'computation', 'closing', nums=[cl1])],
          ['Value debt first.'], ['Using the coupon rate.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Equity items', 3, 'concept', 'equity'), S('s2', 'Liability items', 3, 'concept', 'liability')],
          ['Reason each.'], ['Ignoring the issuer option.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'When is an instrument classified as equity under Ind AS 32?', 'When the issuer has an unconditional right to avoid delivering cash or financial assets, and any share settlement is fixed-for-fixed.',
          [P('p1', 'Unconditional right to avoid', 6, 'unconditional|avoid'), P('p2', 'Fixed-for-fixed', 4, 'fixed')], 'c1'),
        V('v2', 'How is a compound instrument split?', 'The liability is measured at the fair value of similar debt without conversion, and the equity component is the residual amount.',
          [P('p1', 'Liability at fair value', 5, 'liability|fair value'), P('p2', 'Equity residual', 5, 'residual')], 'c3'),
        V('v3', 'How are treasury shares accounted for?', 'They are deducted from equity, and any difference on buying, reselling or cancelling them stays within equity rather than profit.',
          [P('p1', 'Deducted from equity', 5, 'deduct'), P('p2', 'Stays in equity', 5, 'within equity')], 'c4'),
        V('v4', 'Why is a contract to deliver shares worth a fixed amount a liability?', 'Because the shares are used as currency: the holder receives a fixed value and does not share in residual risk.',
          [P('p1', 'Shares as currency', 5, 'currency'), P('p2', 'Fixed value', 5, 'fixed value')], 'c2'),
        V('v5', 'What are the offsetting conditions?', 'A set-off right that the law will enforce today, plus a plan to settle net or at the same moment.',
          [P('p1', 'Enforceable right', 5, 'enforce'), P('p2', 'Intention to settle net', 5, 'net|simultaneous')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Summit Infra Ltd.', 'difficulty': 'moderate',
              'case': 'Summit Infra Ltd. issues ₹50 crore of 8% preference shares, redeemable at the holder\'s option after 3 years. It buys back 1 lakh of its own shares at ₹200 each and later resells them at ₹230. It holds a ₹10 crore deposit with Bank A and owes ₹6 crore to Bank A, with a legal set-off right but plans to settle separately.',
              'mcqs': [
                  M('k1a', 'The preference shares are:', ['A financial liability', 'Equity', 'Compound', 'Outside scope'], 0,
                    'Holder can demand cash. In practice: dividends as interest.', 'core', topic=T1),
                  M('k1b', 'The ₹30 lakh gain on resale of treasury shares goes to:', ['Equity', 'Profit or loss', 'OCI', 'Revenue'], 0,
                    'No gain is recognised on own shares. In practice: credit securities premium.', 'core', topic=T4),
                  M('k1c', 'The deposit and loan with Bank A are:', ['Not offset, as there is no intention to settle net', 'Offset to ₹4 crore', 'Offset only in notes', 'Shown as equity'], 0,
                    'Both conditions are needed. In practice: disclose the right.', 'moderate', topic=T4),
                  M('k1d', 'Amount deducted from equity on buy-back (₹ lakh):', ['200', '230', '30', 'Nil'], 0,
                    '1 lakh × ₹200 = ₹200 lakh. In practice: shown as treasury shares.', 'core', check=200, topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch11', 3, 'Financial Instruments: Equity and Financial Liabilities',
                ['Apply the obligation-to-deliver-cash test.',
                 'Classify contracts settled in own equity instruments.',
                 'Split and account for compound instruments.',
                 'Account for treasury shares, distributions and offsetting.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['fin-p1-ch11-u02'],
                 'exam_tip': 'Look for any feature that forces the issuer to pay — one such clause makes the whole instrument, or a component, a liability.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Liability: unavoidable obligation to pay.',
                             'Equity: fixed-for-fixed; issuer can avoid paying.',
                             'Compound: debt at fair value, equity residual.',
                             'Treasury shares: deduct from equity.',
                             'Offset: enforceable right + intent.'],
                 'remember': ['Economic compulsion is not an obligation.'],
                 'traps': ['Treating redeemable preference shares as equity.']},
                [('Core test', 'Can issuer avoid paying?'), ('Fixed-for-fixed', 'Equity'), ('Compound', 'Debt first'), ('Treasury', 'Equity, no P&L')],
                viva, cases)
