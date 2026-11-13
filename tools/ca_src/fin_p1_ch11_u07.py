"""CA Final · Paper 1 Financial Reporting · Chapter 11 Unit 7 Financial Instruments: Disclosures (Ind AS 107).
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch11-u07'
T1 = 'Significance: balance sheet disclosures'
T2 = 'Significance: profit or loss and other disclosures'
T3 = 'Risks: credit and liquidity'
T4 = 'Risks: market risk and sensitivity'


def build():
    ck = Checks()
    pre = ck.add('500*0.01', 'Extra interest from a 1% rise (₹ lakh)')
    post = ck.add('500*0.01*(1-0.25)', 'Effect on profit after tax (₹ lakh)')
    fx = ck.add('20*84*0.05/100', 'Effect of 5% INR depreciation on USD payables (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Market risk sensitivity', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Tern Ltd. has floating-rate borrowings of ₹500 lakh and USD payables of USD 20 thousand (closing rate ₹84). Tax rate 25%. Prepare sensitivity disclosures for a 1% rise in interest rates and a 5% depreciation of the rupee.',
          'solution': [table(['Risk', 'Working', '₹ lakh'], [
              ['Interest — pre-tax', '500 × 1%', inr(pre)],
              ['Interest — after tax', '5 × 75%', inr(post)],
              ['Currency — loss on USD payables', '20,000 × 84 × 5% (in lakh)', inr(fx)]], title='Ind AS 107 sensitivity analysis')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Liquidity maturity table', 'difficulty': 'core', 'minutes': 6,
          'q': 'Tern Ltd. has: trade payables ₹80 lakh due in 2 months; a term loan of ₹300 lakh repayable ₹100 lakh a year for 3 years with interest; and lease liabilities. How should the maturity analysis be prepared?',
          'solution': [table(['Point', 'Guidance'], [
              ['Basis', 'Contractual undiscounted cash flows, including interest'],
              ['Time bands', 'Entity\'s choice, e.g. up to 1 year, 1–3 years, over 3 years'],
              ['Trade payables', 'Up to 1 year band'],
              ['Term loan', 'Principal plus interest in each band'],
              ['Narrative', 'Explain how liquidity risk is managed']], title='Maturity analysis')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'Ind AS 107 requires disclosures that let users assess the significance of financial instruments for the entity\'s position and performance, and the nature and extent of risks arising and how they are managed.',
            'Balance sheet: carrying amounts of each category (FVTPL — mandatory and designated; amortised cost; FVOCI debt; FVOCI equity; liabilities at amortised cost and FVTPL). For liabilities designated at FVTPL, own-credit changes. Details of FVOCI equity investments and reasons for the election.',
            'Also: reclassifications, offsetting (gross amounts, amounts set off, net amounts, master netting arrangements), collateral pledged and held, loss allowance reconciliation for FVOCI debt, compound instruments with multiple embedded derivatives, and defaults and breaches on loans payable.'],
          'Show what you hold by category and what strings are attached.',
          'A breach of a loan covenant at year end must be disclosed.'),
        C('c2', T2, [
            'Profit or loss and OCI: net gains or losses by category; total interest income and expense for amortised cost and FVOCI items; fee income and expense; and gains or losses on derecognition of amortised cost assets.',
            'Accounting policies: measurement bases and other relevant policies. Hedge accounting: risk management strategy, how it affects the amount, timing and uncertainty of future cash flows, and the effects on position and performance.',
            'Fair value: for each class, fair values for comparison with carrying amounts (exemptions where carrying amount approximates fair value), and Ind AS 113 hierarchy disclosures. Day-one gains or losses deferred are explained.'],
          'Explain how instruments drove income, expense and hedging results.',
          'Interest on bonds at amortised cost is disclosed separately.'),
        C('c3', T3, [
            'For each type of risk, qualitative disclosures (exposures, how they arise, objectives, policies, measurement methods, changes from prior period) and quantitative summary data based on information given to key management.',
            'Credit risk: credit risk management practices, ECL inputs and assumptions, reconciliations of the loss allowance, explanations of significant changes in gross carrying amounts, credit risk exposure by credit rating grades, collateral and modifications.',
            'Liquidity risk: maturity analysis of non-derivative financial liabilities (and derivative liabilities where needed) based on remaining contractual maturities, using undiscounted cash flows, and description of how liquidity risk is managed.'],
          'Credit risk asks "who might not pay us"; liquidity risk asks "can we pay others".',
          'Maturity tables use undiscounted contractual cash flows.'),
        C('c4', T4, [
            'Market risk comprises currency risk, interest rate risk and other price risk (equity and commodity prices).',
            'A sensitivity analysis for each type of market risk shows the impact on profit or loss and on equity of reasonably possible changes in the relevant risk variable at the reporting date, with methods and assumptions, and changes from the previous period.',
            'An entity using value-at-risk or similar models reflecting interdependencies may present that instead, explaining the method, parameters and limitations. Concentrations of risk are disclosed where not apparent.'],
          'Show what a plausible shock would do to profit and equity.',
          'A one percentage point rise on floating debt is a common scenario.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Drafting the risk note', 'role': 'Reporting manager',
             'situation': 'The annual report needs a financial risk management note.',
             'steps': ['List categories and carrying amounts.', 'Prepare credit risk tables and ECL reconciliation.', 'Prepare maturity analysis.', 'Run sensitivity for interest, FX and price risks.'],
             'takeaway': 'Disclosures follow what management actually monitors.'}]

    mcqs = [
        Q('m1', 'The liquidity maturity analysis is prepared on:', ['Undiscounted contractual cash flows', 'Carrying amounts', 'Fair values', 'Discounted cash flows'], 0,
          'Shows actual cash needed. In practice: include interest.', 'c3', T3),
        Q('m2', 'Market risk includes:', ['Currency, interest rate and other price risk', 'Credit risk only', 'Liquidity risk only', 'Operational risk'], 0,
          'Three sub-types. In practice: sensitivity for each.', 'c4', T4),
        Q('m3', 'A sensitivity analysis shows the effect of:', ['Reasonably possible changes in risk variables', 'Worst-case scenarios', 'Historical averages', 'Budgeted figures'], 0,
          'At the reporting date. In practice: state assumptions.', 'c4', T4),
        Q('m4', 'A reconciliation of the loss allowance is part of:', ['Credit risk disclosures', 'Market risk', 'Liquidity risk', 'Hedging'], 0,
          'Shows ECL movements. In practice: by stage.', 'c3', T3),
        Q('m5', 'Defaults and breaches on loans payable at year end are:', ['Disclosed', 'Ignored', 'Recognised as income', 'Only in directors\' report'], 0,
          'Users need to know. In practice: include whether remedied.', 'c1', T1),
        Q('m6', 'Instead of sensitivity analysis, an entity may present:', ['Value-at-risk if used to manage risk', 'Nothing', 'Ratios only', 'Budget variances'], 0,
          'Explain its limitations. In practice: common in banks.', 'c4', T4),
        Q('m7', 'Fair value disclosure is not required when:', ['Carrying amount is a reasonable approximation of fair value', 'Fair value is high', 'The asset is current', 'Auditors agree'], 0,
          'E.g. short-term receivables. In practice: state this.', 'c2', T2),
        Q('m8', 'Quantitative risk data are based on:', ['Information provided internally to key management', 'External ratings only', 'Tax filings', 'Industry averages'], 0,
          'Management approach. In practice: consistent with internal reports.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Pre-tax', 1.5, 'computation', 'pre-tax|interest', nums=[pre]), S('s2', 'After tax', 1.5, 'computation', 'after tax', nums=[post]), S('s3', 'Currency', 2, 'computation', 'currency', nums=[fx])],
          ['State assumptions.'], ['Ignoring tax.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Undiscounted', 2, 'concept', 'undiscounted'), S('s2', 'Bands and interest', 2, 'concept', 'band|interest')],
          ['Include interest.'], ['Using carrying amounts.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are the two broad aims of Ind AS 107?', 'To show how significant financial instruments are for position and performance, and the nature and extent of risks arising and how they are managed.',
          [P('p1', 'Significance', 5, 'significan'), P('p2', 'Risks', 5, 'risk')], 'c1'),
        V('v2', 'What does credit risk disclosure include?', 'Credit risk practices, ECL inputs, loss allowance reconciliations, exposure by credit grade and collateral.',
          [P('p1', 'ECL and allowance', 5, 'ecl|allowance'), P('p2', 'Credit grades', 5, 'grade')], 'c3'),
        V('v3', 'How is the maturity analysis prepared?', 'On remaining contractual maturities using undiscounted cash flows, with a description of liquidity management.',
          [P('p1', 'Undiscounted', 5, 'undiscounted'), P('p2', 'Contractual maturities', 5, 'contractual')], 'c3'),
        V('v4', 'What is a sensitivity analysis?', 'A disclosure of how profit and equity would change from reasonably possible movements in each market risk variable at the reporting date.',
          [P('p1', 'Reasonably possible change', 5, 'reasonably possible'), P('p2', 'Profit and equity', 5, 'profit|equity')], 'c4'),
        V('v5', 'What offsetting disclosures are needed?', 'Gross amounts, amounts set off, net amounts presented, and amounts subject to master netting arrangements not set off.',
          [P('p1', 'Gross and net', 5, 'gross|net'), P('p2', 'Master netting', 5, 'master netting')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Lark Retail Ltd.', 'difficulty': 'moderate',
              'case': 'Lark Retail Ltd. has floating-rate loans of ₹800 lakh, equity investments at FVOCI of ₹120 lakh, trade receivables with ECL allowance, and breached a debt covenant at year end which the lender waived after year end.',
              'mcqs': [
                  M('k1a', 'Pre-tax effect of a 0.5% rate rise on the loans (₹ lakh):', ['4', '8', '0.5', '40'], 0,
                    '800 × 0.5%. In practice: disclose increase and decrease.', 'core', check=4, topic=T4),
                  M('k1b', 'Effect of a 10% fall in equity prices on OCI (₹ lakh):', ['12', '1.2', '120', 'Nil'], 0,
                    '120 × 10%, through OCI not profit. In practice: other price risk.', 'core', check=12, topic=T4),
                  M('k1c', 'The covenant breach must be:', ['Disclosed, including that it was waived after year end', 'Ignored as waived', 'Recognised as expense', 'Shown as contingent asset'], 0,
                    'Breaches at year end are disclosed. In practice: classification of loan may also be affected.', 'moderate', topic=T1),
                  M('k1d', 'The ECL movement is disclosed in:', ['A loss allowance reconciliation under credit risk', 'Market risk note', 'Liquidity table', 'Hedging note'], 0,
                    'Credit risk disclosures. In practice: opening to closing.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch11', 7, 'Disclosures',
                ['Present balance sheet disclosures by category.',
                 'Disclose income, expense, hedging and fair value information.',
                 'Prepare credit and liquidity risk disclosures.',
                 'Prepare market risk sensitivity analysis.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['fin-p1-ch11-u06'],
                 'exam_tip': 'For sensitivity questions, show the effect on profit and on equity separately and state the tax effect.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Ind AS 107: significance + risks.',
                             'Categories, collateral, offsetting, defaults.',
                             'Credit risk: ECL reconciliation and grades.',
                             'Liquidity: undiscounted maturity analysis.',
                             'Market risk: sensitivity or VaR.'],
                 'remember': ['Quantitative data mirror internal reports.'],
                 'traps': ['Discounting the maturity table.']},
                [('Liquidity', 'Undiscounted maturities'), ('Credit', 'ECL reconciliation'), ('Market', 'Sensitivity'), ('Breach', 'Disclose')],
                viva, cases)
