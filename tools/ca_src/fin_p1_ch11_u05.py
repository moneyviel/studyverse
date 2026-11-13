"""CA Final · Paper 1 Financial Reporting · Chapter 11 Unit 5 Recognition and Derecognition of Financial Instruments.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch11-u05'
T1 = 'Initial recognition and regular-way trades'
T2 = 'Derecognition of financial assets: the decision tree'
T3 = 'Transfers, continuing involvement and factoring'
T4 = 'Derecognition and modification of financial liabilities'


def build():
    ck = Checks()
    loss = ck.add('100-95', 'Loss on sale without recourse (₹ lakh)')
    liab = ck.add('95', 'Financial liability recognised with full recourse (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Factoring receivables', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Raven Ltd. transfers trade receivables of ₹100 lakh to a factor for ₹95 lakh. Case A: no recourse; the factor bears all credit risk. Case B: Raven must reimburse the factor for every default (full recourse) and expected losses are significant. Account for each case.',
          'solution': [table(['Case', 'Analysis', '₹ lakh'], [
              ['A — derecognise', 'Substantially all risks and rewards transferred', '—'],
              ['A — loss on sale', '100 − 95', inr(loss)],
              ['B — keep receivables', 'Credit risk retained — risks and rewards kept', inr(100)],
              ['B — collateralised borrowing', 'Cash received recognised as liability', inr(liab)]], title='Derecognition test')],
          'checks': list(ck)}

    ck2 = Checks()
    diff = ck2.add('(100-88)/100*100', 'Difference in present values (%)')
    gain = ck2.add('100-88', 'Gain on extinguishment if new loan fair value equals PV (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Renegotiating a loan', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Raven Ltd. has a ₹100 lakh loan at amortised cost. It renegotiates terms with the same lender. The present value of new cash flows (including fees) discounted at the original effective interest rate is ₹88 lakh. Is this a substantial modification? If the new loan\'s fair value is ₹88 lakh, what is the gain?',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Present value difference', '(100 − 88) ÷ 100', inr(diff) + '%'],
              ['10% test', '12% ≥ 10%', 'Substantial — extinguishment'],
              ['Derecognise old, recognise new at fair value', '100 − 88', '₹' + inr(gain) + ' lakh gain']], title='Quantitative 10% test')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A financial asset or liability is recognised when the entity becomes party to the contractual provisions. Firm commitments to buy or sell goods are generally not recognised until one party performs; forwards and other derivatives are recognised at commitment.',
            'Regular-way purchases or sales (delivery within the market\'s standard timeframe) are recognised using trade-date or settlement-date accounting, applied consistently for each category of assets.',
            'Under settlement-date accounting for assets measured at fair value, changes in value between trade and settlement dates are still recognised (in profit or loss or OCI by category); for amortised cost assets they are ignored.'],
          'Recognise when you sign the contract — except for ordinary goods orders.',
          'Shares bought on T and delivered on T+1 may be booked on either date, consistently.'),
        C('c2', T2, [
            'The derecognition decision follows steps: consolidate subsidiaries first; decide whether the test applies to the whole asset or a part; then ask whether contractual rights to cash flows have expired — if yes, derecognise.',
            'If not expired, ask whether the asset has been transferred (rights to cash flows transferred, or a qualifying pass-through arrangement where the entity collects and passes on cash without material delay, cannot sell or pledge the asset, and pays only what it collects).',
            'If transferred: if substantially all risks and rewards are transferred, derecognise; if substantially all are retained, continue to recognise; if neither, consider control — if the transferee can practically sell the asset unilaterally, derecognise; otherwise continue to recognise to the extent of continuing involvement.'],
          'Expired? Transferred? Risks and rewards? Control? — in that order.',
          'Selling a bond outright with no strings attached is a clean derecognition.'),
        C('c3', T3, [
            'On full derecognition, the difference between the carrying amount and consideration received (plus any cumulative OCI gain or loss on debt at FVOCI) is recognised in profit or loss.',
            'Where risks and rewards are retained (e.g. sale with full recourse, repo at a fixed price, total return swap), the asset stays and consideration received is a financial liability.',
            'Continuing involvement: the asset remains to the extent of exposure (e.g. guarantee: lower of carrying amount and maximum guaranteed amount), with an associated liability. Servicing rights retained may create a servicing asset or liability.'],
          'Credit risk kept means the receivable stays on the books.',
          'Factoring with recourse is a borrowing, not a sale.'),
        C('c4', T4, [
            'A financial liability is removed when extinguished — the obligation is discharged, cancelled or expires. The difference between carrying amount and consideration paid is recognised in profit or loss.',
            'An exchange with the same lender on substantially different terms, or a substantial modification, is an extinguishment of the old liability and recognition of a new one. The quantitative test: terms differ substantially if the present value of new cash flows, including fees net of fees received, discounted at the original effective rate differs by at least 10% from the remaining cash flows of the original liability. Qualitative factors may also indicate substantial modification.',
            'If not substantial, the liability is adjusted to the revised present value at the original rate, with the difference in profit or loss; costs adjust the carrying amount and are amortised. Settling debt by issuing equity is accounted for under Appendix D of Ind AS 109 (equity at fair value).'],
          'The 10% test decides whether a renegotiated loan is new or old.',
          'A waiver of part of a loan by the lender creates a gain.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Reviewing a securitisation', 'role': 'Group reporting accountant',
             'situation': 'A subsidiary sells loan receivables to a trust and provides a first-loss guarantee.',
             'steps': ['Check whether the trust is consolidated.', 'Apply the pass-through test.', 'Assess risks and rewards retained via the guarantee.', 'Measure continuing involvement if partial.'],
             'takeaway': 'Consolidation comes before derecognition.'}]

    mcqs = [
        Q('m1', 'Regular-way purchases may be recognised using:', ['Trade date or settlement date accounting, consistently', 'Only trade date', 'Only settlement date', 'Payment date'], 0,
          'A policy choice per category. In practice: disclose it.', 'c1', T1),
        Q('m2', 'The first step in the derecognition tree after consolidation is:', ['Whether rights to cash flows have expired', 'Risks and rewards', 'Control', 'Fair value'], 0,
          'Expiry ends the analysis. In practice: then check transfer.', 'c2', T2),
        Q('m3', 'Receivables sold with full recourse are:', ['Not derecognised; proceeds are a liability', 'Derecognised', 'Partially derecognised', 'Written off'], 0,
          'Credit risk retained. In practice: collateralised borrowing.', 'c3', T3),
        Q('m4', 'When neither substantially all risks and rewards are transferred nor retained, the entity considers:', ['Control', 'Fair value', 'Legal form', 'Tax effect'], 0,
          'Control decides. In practice: transferee\'s practical ability to sell.', 'c2', T2),
        Q('m5', 'The quantitative test for substantial modification of a liability uses a threshold of:', ['Ten percent of present value', 'Five percent', 'Twenty percent', 'Any change'], 0,
          'Discount at the original EIR. In practice: include fees.', 'c4', T4),
        Q('m6', 'A gain or loss on extinguishing a liability is recognised in:', ['Profit or loss', 'OCI', 'Equity', 'Deferred income'], 0,
          'Difference between carrying amount and amount paid. In practice: include fees.', 'c4', T4),
        Q('m7', 'Firm commitments to buy goods are recognised:', ['Generally when one party performs', 'At signing', 'Never', 'At fair value always'], 0,
          'Executory contracts. In practice: onerous ones fall under Ind AS 37.', 'c1', T1),
        Q('m8', 'On derecognising debt at FVOCI, accumulated OCI is:', ['Reclassified to profit or loss', 'Left in equity', 'Transferred to retained earnings', 'Reversed'], 0,
          'Debt FVOCI recycles. In practice: part of the gain.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Case A', 3, 'computation', 'derecognis|loss', nums=[loss]), S('s2', 'Case B', 3, 'computation', 'liability|borrowing', nums=[liab])],
          ['Name the test.'], ['Derecognising under recourse.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Test', 2.5, 'computation', '10%|test', nums=[diff]), S('s2', 'Gain', 2.5, 'computation', 'gain', nums=[gain])],
          ['Use original EIR.'], ['Using new rate for the test.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'When is a financial instrument first recognised?', 'At the moment the entity signs up to the instrument\'s contractual terms and becomes a party to them.',
          [P('p1', 'Party to contract', 6, 'party'), P('p2', 'Contractual terms', 4, 'contractual')], 'c1'),
        V('v2', 'Describe a pass-through arrangement.', 'The entity keeps the right to receive cash but must pay it on to others without material delay, is barred from selling or pledging the asset, and pays only what it collects.',
          [P('p1', 'Pass on cash', 5, 'pay|pass'), P('p2', 'Barred from pledging', 5, 'barred')], 'c2'),
        V('v3', 'What happens if risks and rewards are retained?', 'The asset stays on the balance sheet and any consideration received is booked as a financial liability.',
          [P('p1', 'Asset stays', 5, 'stays'), P('p2', 'Liability', 5, 'liability')], 'c3'),
        V('v4', 'What is the role of control in derecognition?', 'If risks and rewards are partly kept, the transferee\'s practical ability to sell the asset unilaterally means control passed and the asset is derecognised.',
          [P('p1', 'Ability to sell', 6, 'sell'), P('p2', 'Unilaterally', 4, 'unilateral')], 'c2'),
        V('v5', 'How is a non-substantial modification of a loan treated?', 'The carrying amount is recalculated at the original effective rate and the difference goes to profit or loss.',
          [P('p1', 'Original effective rate', 6, 'original'), P('p2', 'Profit or loss', 4, 'profit or loss')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Crest Bank Ltd.', 'difficulty': 'moderate',
              'case': 'Crest Bank Ltd. sells government bonds (carrying ₹500 lakh) to a counterparty for ₹510 lakh under an agreement to repurchase them in 30 days at ₹512 lakh. It also sells a loan portfolio of ₹200 lakh outright for ₹198 lakh, retaining no exposure. A borrower\'s ₹40 lakh loan is waived by Crest\'s lender on Crest\'s own borrowings.',
              'mcqs': [
                  M('k1a', 'The repo of bonds is:', ['A collateralised borrowing; bonds stay on the books', 'A sale', 'A derivative only', 'Equity'], 0,
                    'Fixed-price repurchase retains risks and rewards. In practice: interest of ₹2 lakh.', 'core', topic=T3),
                  M('k1b', 'Loss on the outright loan sale (₹ lakh):', ['2', '0', '198', '10'], 0,
                    '200 − 198. In practice: derecognise fully.', 'core', check=2, topic=T3),
                  M('k1c', 'The ₹40 lakh waiver on Crest\'s borrowing results in:', ['A gain in profit or loss', 'Equity credit', 'OCI', 'No entry'], 0,
                    'Extinguishment of part of a liability. In practice: unless lender is a shareholder acting as such.', 'moderate', topic=T4),
                  M('k1d', 'Liability recognised on the repo (₹ lakh):', ['510', '512', '500', 'Nil'], 0,
                    'Cash received is the liability, accreting to 512. In practice: the 2 is interest.', 'moderate', check=510, topic=T3),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch11', 5, 'Recognition and Derecognition of Financial Instruments',
                ['Apply initial recognition rules including regular-way trades.',
                 'Follow the derecognition decision tree for financial assets.',
                 'Account for transfers with retained risks or continuing involvement.',
                 'Derecognise and modify financial liabilities.'],
                {'difficulty': 'hard', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['fin-p1-ch11-u04'],
                 'exam_tip': 'Walk the derecognition tree step by step in your answer — examiners look for the sequence.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Recognise on becoming party to the contract.',
                             'Derecognition: expired → transferred → risks and rewards → control.',
                             'Retained risks: asset stays, proceeds are a liability.',
                             'Liabilities: extinguished when discharged, cancelled or expired.',
                             '10% test for substantial modification.'],
                 'remember': ['Consolidate before testing derecognition.'],
                 'traps': ['Derecognising receivables factored with recourse.']},
                [('Recourse', 'Borrowing'), ('Repo', 'Borrowing'), ('Control', 'Can transferee sell?'), ('Modification', '10% test')],
                viva, cases)
