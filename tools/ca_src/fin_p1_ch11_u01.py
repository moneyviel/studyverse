"""CA Final · Paper 1 Financial Reporting · Chapter 11 Unit 1 Financial Instruments: Scope and Definitions.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch11-u01'
T1 = 'Financial instrument and financial asset'
T2 = 'Financial liability and equity instrument'
T3 = 'Scope of Ind AS 32, 109 and 107'
T4 = 'Contracts to buy or sell non-financial items'


def build():
    i1 = {'id': 'i1', 'title': 'Is it a financial instrument?', 'difficulty': 'core', 'minutes': 8,
          'q': 'Classify for Coral Ltd.: (a) trade receivables; (b) prepaid rent; (c) investment in another company\'s shares; (d) income tax payable; (e) bank loan; (f) obligation to deliver goods for advance received; (g) a forward contract to buy USD; (h) own equity shares issued; (i) a constructive obligation for warranties.',
          'solution': [table(['Item', 'Classification', 'Reason'], [
              ['(a)', 'Financial asset', 'Contractual right to receive cash'],
              ['(b)', 'Not financial', 'Right to receive a service, not cash'],
              ['(c)', 'Financial asset', 'Equity instrument of another entity'],
              ['(d)', 'Not financial', 'Statutory, not contractual'],
              ['(e)', 'Financial liability', 'Contractual obligation to pay cash'],
              ['(f)', 'Not financial', 'Obligation to deliver goods (Ind AS 115 contract liability)'],
              ['(g)', 'Derivative — financial asset or liability', 'Exchange under potentially favourable/unfavourable terms'],
              ['(h)', 'Equity instrument', 'Residual interest'],
              ['(i)', 'Not financial', 'Constructive, not contractual (Ind AS 37)']], title='Definitions')],
          'checks': []}

    ck = Checks()
    der = ck.add('1000*(53000-50000)/100000', 'Derivative asset at year end (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Own-use or derivative?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Coral Ltd. contracts to buy 1,000 tonnes of copper at ₹50,000 per tonne in 3 months. In the past it has usually closed out comparable contracts for cash before delivery. At year end the forward price for that date is ₹53,000. Is the contract in Ind AS 109 scope, and what is its value (ignore discounting)?',
          'solution': [table(['Point', 'Analysis', 'Result'], [
              ['Net settlement practice', 'Similar contracts settled net — own-use exemption fails', 'In scope of Ind AS 109'],
              ['Classification', 'Derivative at fair value through profit or loss', '—'],
              ['Fair value', '1,000 × (53,000 − 50,000)', inr(der) + ' lakh asset']], title='Own-use exemption')],
          'checks': list(ck)}

    concepts = [
        C('c1', T1, [
            'Any contract that puts a financial asset on one party\'s books and, on the other party\'s books, a financial liability or an equity instrument, is a financial instrument.',
            'A financial asset is: cash; an equity instrument of another entity; a right under contract to collect cash or some other financial asset, or to swap financial assets or liabilities on potentially favourable terms; or certain contracts settled in the entity\'s own equity instruments.',
            'Items that are not financial assets include physical assets, intangibles, prepaid expenses (giving rise to goods or services), and statutory rights such as tax refunds. Contracts must exist — statutory obligations are not financial instruments.'],
          'Financial instruments are contracts about cash or shares, not about goods or services.',
          'A debtor is a financial asset; a prepayment is not.'),
        C('c2', T2, [
            'A financial liability is a duty under contract to hand over cash or some other financial asset, or to swap financial assets or liabilities on potentially unfavourable terms; or certain contracts settled in the entity\'s own equity (e.g. a variable number of own shares).',
            'An equity instrument is a contract showing a claim on whatever remains of the entity\'s assets once every liability is subtracted. The fixed-for-fixed test: delivering a fixed number of own shares for a fixed amount of cash is equity.',
            'Puttable instruments and obligations arising on liquidation are equity only in specified narrow cases. Substance, not legal form, decides: redeemable preference shares with mandatory redemption are liabilities.'],
          'A liability is a contract you cannot avoid paying; equity is what is left over.',
          'Preference shares redeemable at a fixed date are debt.'),
        C('c3', T3, [
            'Ind AS 32 deals with presentation (liability vs equity, offsetting); Ind AS 109 with recognition, classification, measurement, impairment, derecognition and hedging; Ind AS 107 with disclosures.',
            'Excluded from Ind AS 109 (with own-standard treatment): interests in subsidiaries, associates and joint ventures (unless standards permit); rights and obligations under leases (partly included); employee benefit plans; own equity instruments; insurance contracts; forward contracts between acquirer and seller for a business combination; most loan commitments; share-based payments.',
            'Financial guarantee contracts issued are within Ind AS 109. Derivatives on interests in subsidiaries, associates or joint ventures are generally within scope.'],
          'Know which standard answers which question.',
          'Investment in a subsidiary in separate accounts may be at cost under Ind AS 27.'),
        C('c4', T4, [
            'Contracts to buy or sell non-financial items that are capable of net settlement (in cash or other financial instruments) are treated as if they were financial instruments — unless held for the entity\'s expected purchase, sale or usage requirements (own-use exemption).',
            'Net settlement can arise when: the terms permit net settlement; the entity habitually closes out comparable contracts net; it habitually takes delivery and resells quickly for a trading margin; or the item is readily convertible to cash.',
            'An entity may irrevocably designate an own-use contract as at fair value through profit or loss at inception if doing so eliminates or significantly reduces an accounting mismatch. Written options that can be net settled cannot qualify for own use.'],
          'Commodity contracts are derivatives unless genuinely for own use.',
          'A steel mill buying iron ore for its furnaces uses the own-use exemption.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Financial instrument inventory', 'role': 'Treasury accountant',
             'situation': 'First-time review of all contracts for Ind AS 109.',
             'steps': ['List all contracts involving cash or shares.', 'Exclude statutory and non-financial items.', 'Test commodity contracts for own use.', 'Classify issued instruments as liability or equity.'],
             'takeaway': 'Scope comes first: if it is not a financial instrument, Ind AS 109 does not apply.'}]

    mcqs = [
        Q('m1', 'Prepaid expenses are:', ['Not financial assets', 'Financial assets', 'Derivatives', 'Equity'], 0,
          'They give rise to goods or services, not cash. In practice: exclude from Ind AS 107 tables.', 'c1', T1),
        Q('m2', 'Income tax payable is:', ['Not a financial liability, being statutory', 'A financial liability', 'A derivative', 'Equity'], 0,
          'Not contractual. In practice: Ind AS 12 applies.', 'c1', T1),
        Q('m3', 'Preference shares with mandatory redemption for cash are classified as:', ['Financial liabilities', 'Equity', 'Compound always', 'Provisions'], 0,
          'There is a contractual obligation to pay. In practice: dividends become interest.', 'c2', T2),
        Q('m4', 'A contract to issue a fixed number of own shares for fixed cash is:', ['Equity', 'A financial liability', 'A derivative asset', 'Outside scope'], 0,
          'It passes the fixed-for-fixed test. In practice: variable shares fail.', 'c2', T2),
        Q('m5', 'The own-use exemption fails when:', ['It habitually closes out comparable contracts net in cash', 'The contract is long', 'The price is fixed', 'Delivery is physical'], 0,
          'Net settlement practice taints the class. In practice: review trading patterns.', 'c4', T4),
        Q('m6', 'Financial guarantee contracts issued are within:', ['Ind AS 109', 'Ind AS 37 only', 'Ind AS 117 only', 'No standard'], 0,
          'They are financial instruments. In practice: measured at higher of ECL and amortised premium.', 'c3', T3),
        Q('m7', 'Which standard governs offsetting financial assets and liabilities?', ['Ind AS 32', 'Ind AS 109', 'Ind AS 107', 'Ind AS 1'], 0,
          'Ind AS 32 covers presentation. In practice: requires enforceable right and intent.', 'c3', T3),
        Q('m8', 'A forward contract to buy USD is:', ['A derivative financial instrument', 'A non-financial asset', 'Equity', 'Outside scope'], 0,
          'Exchange on potentially favourable or unfavourable terms. In practice: at FVTPL unless hedging.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Financial assets', 2, 'concept', 'financial asset'), S('s2', 'Liabilities and equity', 2, 'concept', 'liability|equity'), S('s3', 'Non-financial', 2, 'concept', 'not financial|statutory')],
          ['Give the reason for each.'], ['Treating tax payable as financial.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Own-use test', 2, 'concept', 'own-use|net'), S('s2', 'Value', 2, 'computation', 'fair value', nums=[der])],
          ['State the trigger.'], ['Applying own-use despite net settlement.'], ['Table.'], pad='table', checks=list(ck)),
    ]

    viva = [
        V('v1', 'Define a financial instrument.', 'A contract that creates a financial asset for one party and a financial liability or equity instrument for the other.',
          [P('p1', 'Contract', 4, 'contract'), P('p2', 'Asset and liability or equity', 6, 'financial asset|liability|equity')], 'c1'),
        V('v2', 'What is the fixed-for-fixed test?', 'A contract settled by issuing a fixed number of own shares for a fixed amount of cash is classified as equity.',
          [P('p1', 'Fixed number of shares', 5, 'fixed number'), P('p2', 'Equity', 5, 'equity')], 'c2'),
        V('v3', 'Why is income tax payable outside Ind AS 32?', 'Because it arises from statute, which is outside any contract between the parties.',
          [P('p1', 'Statute', 6, 'statut'), P('p2', 'Contract', 4, 'contract')], 'c1'),
        V('v4', 'What is the own-use exemption?', 'Contracts for non-financial items held to meet expected purchase, sale or usage needs are excluded from Ind AS 109 even if net-settleable.',
          [P('p1', 'Expected usage needs', 6, 'usage|purchase'), P('p2', 'Excluded', 4, 'exclud')], 'c4'),
        V('v5', 'Which standards cover financial instruments?', 'Ind AS 32 for presentation, Ind AS 109 for recognition and measurement, and Ind AS 107 for disclosures.',
          [P('p1', 'Ind AS 32 and 109', 6, '32|109'), P('p2', 'Ind AS 107', 4, '107')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Quill Ltd.', 'difficulty': 'moderate',
              'case': 'Quill Ltd. issues: (1) 10% preference shares redeemable at the holder\'s option after 5 years; (2) a bond convertible into a fixed number of shares; (3) a contract to deliver shares worth exactly ₹1 crore at a future date. It also buys wheat under forward contracts which it always takes delivery of and mills.',
              'mcqs': [
                  M('k1a', 'Preference shares redeemable at the holder\'s option are:', ['A financial liability', 'Equity', 'Outside scope', 'A provision'], 0,
                    'The issuer cannot avoid paying. In practice: dividends as interest.', 'core', topic=T2),
                  M('k1b', 'The convertible bond is:', ['A compound instrument with liability and equity parts', 'Pure equity', 'Pure liability', 'A derivative asset'], 0,
                    'Fixed-for-fixed conversion creates an equity component. In practice: split at issue.', 'moderate', topic=T2),
                  M('k1c', 'The contract to deliver shares worth ₹1 crore is:', ['A financial liability', 'Equity', 'Revenue', 'Outside scope'], 0,
                    'A variable number of shares is like cash. In practice: fails fixed-for-fixed.', 'moderate', topic=T2),
                  M('k1d', 'The wheat forward contracts are:', ['Outside Ind AS 109 under own use', 'Derivatives at FVTPL', 'Equity', 'Financial liabilities'], 0,
                    'Held for usage requirements and physically settled. In practice: executory contracts.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch11', 1, 'Financial Instruments: Scope and Definitions',
                ['Define financial instruments, financial assets and liabilities, and equity.',
                 'Distinguish contractual from non-contractual items.',
                 'Identify the scope of Ind AS 32, 109 and 107.',
                 'Apply the own-use exemption to commodity contracts.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 20}, 'prereq': ['fin-p1-ch10-u03'],
                 'exam_tip': 'Ask first: is there a contract, and is it about cash, financial assets or own shares?'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Financial instrument: contract creating asset and liability/equity.',
                             'Statutory items and prepayments excluded.',
                             'Equity: residual interest; fixed-for-fixed.',
                             'Ind AS 32 presentation; 109 measurement; 107 disclosure.',
                             'Own-use exemption for commodity contracts.'],
                 'remember': ['Substance over legal form for preference shares.'],
                 'traps': ['Treating advance from customers as a financial liability.']},
                [('Financial asset', 'Right to cash'), ('Liability', 'Obligation to pay'), ('Equity', 'Residual'), ('Own use', 'Exempt')],
                viva, cases)
