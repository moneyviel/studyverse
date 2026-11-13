"""CA Final · Paper 1 Financial Reporting · Chapter 12 Ind AS 103 Business Combinations.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch12-u01'
T1 = 'Identifying a business combination and the acquirer'
T2 = 'Recognising and measuring identifiable net assets'
T3 = 'Consideration, goodwill and bargain purchase'
T4 = 'Special cases: step acquisitions, measurement period, common control'


def build():
    ck = Checks()
    cons = ck.add('600+50+150', 'Consideration transferred (₹ crore)')
    gw1 = ck.add('600+50+150+0.2*700-700', 'Goodwill — NCI at proportionate share (₹ crore)')
    gw2 = ck.add('600+50+150+190-700', 'Goodwill — NCI at fair value (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Computing goodwill', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Apex Ltd. acquires 80% of Beta Ltd. for cash ₹600 crore, shares with fair value ₹150 crore, and contingent consideration with acquisition-date fair value ₹50 crore. Acquisition-related legal fees ₹5 crore. Fair value of Beta\'s identifiable net assets is ₹700 crore. Fair value of the 20% NCI is ₹190 crore. Compute goodwill under both NCI measurement options.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Consideration', '600 + 150 + 50 (legal fees expensed)', inr(cons)],
              ['NCI — proportionate', '20% × 700 = 140', inr(140)],
              ['Goodwill — proportionate method', '800 + 140 − 700', inr(gw1)],
              ['NCI — fair value', 'Given', inr(190)],
              ['Goodwill — full goodwill method', '800 + 190 − 700', inr(gw2)]], title='Ind AS 103 goodwill')],
          'checks': list(ck)}

    ck2 = Checks()
    reval = ck2.add('25*12-200', 'Gain on remeasuring previous 25% stake (₹ crore)')
    gw = ck2.add('900+25*12-1100', 'Goodwill after step acquisition (₹ crore)')
    i2 = {'id': 'i2', 'title': 'A step acquisition', 'difficulty': 'hard', 'minutes': 9,
          'q': 'Apex holds 25% of Gamma Ltd. (equity-accounted carrying amount ₹200 crore). It buys the remaining 75% for ₹900 crore; the fair value of the 25% stake at that date is ₹300 crore (₹12 crore per 1%). Gamma\'s identifiable net assets are ₹1,100 crore. Compute the remeasurement gain and goodwill.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Remeasure previously held interest', '300 − 200 → profit or loss', inr(reval)],
              ['Consideration + previously held interest', '900 + 300', inr(1200)],
              ['Net identifiable assets', 'Given (100% acquired, no NCI)', inr(1100)],
              ['Goodwill', '1,200 − 1,100', inr(gw)]], title='Step acquisition')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A business combination happens when one party (the acquirer) gains control over one business or several. A business is an integrated set of activities and assets capable of being conducted and managed to provide goods or services to customers or generate investment or other income; at minimum it must combine an input with a substantive process, which jointly make a significant contribution to producing outputs.',
            'An optional concentration test: if nearly the whole fair value of the gross assets bought sits in one identifiable asset (or a group of similar ones), the set is not a business (asset acquisition).',
            'The acquisition method requires: identifying the acquirer (the entity obtaining control, per Ind AS 110 — considering relative voting rights, board composition, size, and who issues equity); determining the acquisition date (when control passes); recognising and measuring assets, liabilities and NCI; and recognising goodwill or a bargain purchase gain. Reverse acquisitions occur when the legal acquirer is the accounting acquiree.'],
          'No business, no business combination — test the set first.',
          'Buying a single building with leases only may fail the concentration test.'),
        C('c2', T2, [
            'Identifiable assets acquired and liabilities assumed are recognised if they meet the Conceptual Framework definitions at the acquisition date and are part of the exchange, even if not previously recognised by the acquiree (e.g. brands, customer relationships).',
            'They are measured at acquisition-date fair value. Exceptions: contingent liabilities are recognised if a present obligation exists and fair value is reliable, even if outflow is not probable; deferred taxes (Ind AS 12), employee benefits (Ind AS 19), indemnification assets, reacquired rights, share-based payment awards (Ind AS 102), held-for-sale assets (Ind AS 105), leases where the acquiree is lessee (Ind AS 116) follow their own rules.',
            'NCI is measured either at fair value or at the proportionate share of identifiable net assets — choice per transaction.'],
          'Bring everything onto the balance sheet at fair value, including intangibles the target never showed.',
          'A pending lawsuit with a possible loss may still be recognised in a combination.'),
        C('c3', T3, [
            'Consideration transferred is measured at fair value: cash, other assets, liabilities incurred to former owners and equity issued, including contingent consideration at acquisition-date fair value. Acquisition-related costs are expensed (except debt or equity issue costs).',
            'Goodwill = consideration + NCI + fair value of previously held interest − net identifiable assets. Goodwill is not amortised; it is tested annually for impairment.',
            'A bargain purchase arises when net assets exceed that total. After reassessing identification and measurement, the gain is recognised in OCI and accumulated in equity as capital reserve where there is clear evidence of the underlying reasons; otherwise it is recognised directly in equity as capital reserve.'],
          'Goodwill is the balancing figure; a negative one becomes capital reserve.',
          'Legal fees on the deal are expensed, not added to goodwill.'),
        C('c4', T4, [
            'In a step acquisition, the previously held equity interest is remeasured to fair value at the acquisition date, with any gain or loss in profit or loss (or OCI where appropriate). Amounts previously in OCI are treated as if the interest were disposed of.',
            'Measurement period: provisional amounts can be adjusted retrospectively for new information about facts at acquisition date, within one year. Contingent consideration changes after this — if classified as a liability — are remeasured through profit or loss; if equity, not remeasured.',
            'Common control combinations (Appendix C) use the pooling of interests method: assets and liabilities at carrying amounts, no new goodwill, financial statements restated as if combined from the start of the earliest period presented (or from when common control began), and differences adjusted in capital reserve.'],
          'Old stakes are revalued; new information has a one-year window; group restructurings use pooling.',
          'Merging two fellow subsidiaries uses book values.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Purchase price allocation', 'role': 'Valuation and reporting team member',
             'situation': 'The group acquired a company in Q3; numbers are needed for the year-end accounts.',
             'steps': ['Confirm business, acquirer and date.', 'Value identifiable intangibles and contingent liabilities.', 'Measure consideration including earn-outs.', 'Compute goodwill and flag provisional amounts.'],
             'takeaway': 'PPA is where most goodwill errors originate.'}]

    mcqs = [
        Q('m1', 'Acquisition-related costs such as legal fees are:', ['Expensed', 'Added to goodwill', 'Added to consideration', 'Deducted from equity'], 0,
          'They are not part of the exchange. In practice: share issue costs follow Ind AS 32.', 'c3', T3),
        Q('m2', 'Contingent liabilities of the acquiree are recognised in a combination if:', ['A present obligation exists and fair value is reliable', 'Outflow is probable', 'Never', 'Always'], 0,
          'An exception to Ind AS 37. In practice: possible obligations excluded.', 'c2', T2),
        Q('m3', 'A bargain purchase gain with clear evidence of reasons is recognised in:', ['OCI and accumulated as capital reserve', 'Profit or loss', 'Goodwill', 'Revenue'], 0,
          'Indian modification. In practice: reassess first.', 'c3', T3),
        Q('m4', 'Goodwill is subsequently:', ['Tested annually for impairment, not amortised', 'Amortised over 10 years', 'Written off', 'Revalued'], 0,
          'Ind AS 36 applies. In practice: allocate to CGUs.', 'c3', T3),
        Q('m5', 'In a step acquisition, the previously held interest is:', ['Remeasured to fair value', 'Kept at carrying amount', 'Ignored', 'Added at cost'], 0,
          'Gain or loss in profit or loss. In practice: recycle related OCI.', 'c4', T4),
        Q('m6', 'Combinations under common control use:', ['The pooling of interests method', 'The acquisition method', 'Fair value', 'Proportionate consolidation'], 0,
          'Appendix C. In practice: no new goodwill.', 'c4', T4),
        Q('m7', 'The measurement period cannot exceed:', ['One year from acquisition date', 'Six months', 'Two years', 'The financial year end'], 0,
          'Adjustments are retrospective. In practice: disclose provisional amounts.', 'c4', T4),
        Q('m8', 'Contingent consideration classified as a liability is subsequently:', ['Remeasured at fair value through profit or loss', 'Not remeasured', 'Adjusted against goodwill', 'Recognised in OCI'], 0,
          'Changes after the measurement period are not goodwill adjustments. In practice: earn-outs.', 'c4', T4),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Consideration', 2, 'computation', 'consideration', nums=[cons]), S('s2', 'Proportionate', 3, 'computation', 'proportionate', nums=[gw1]), S('s3', 'Full goodwill', 3, 'computation', 'fair value|full', nums=[gw2])],
          ['Expense legal fees.'], ['Adding fees to goodwill.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Remeasurement', 3, 'computation', 'remeasure', nums=[reval]), S('s2', 'Goodwill', 3, 'computation', 'goodwill', nums=[gw])],
          ['Remeasure the old stake.'], ['Using carrying amount of the old stake.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a business under Ind AS 103?', 'An integrated set of activities and assets that, at minimum, combines an input with a substantive process which jointly make a significant contribution to producing outputs.',
          [P('p1', 'Input and process', 6, 'input|process'), P('p2', 'Outputs', 4, 'output')], 'c1'),
        V('v2', 'State the goodwill formula.', 'Consideration transferred plus NCI plus fair value of any previously held interest, less fair value of identifiable net assets.',
          [P('p1', 'Consideration and NCI', 5, 'consideration|nci'), P('p2', 'Less net assets', 5, 'net assets')], 'c3'),
        V('v3', 'How may NCI be measured?', 'At fair value, or at its proportionate share of the acquiree\'s identifiable net assets, chosen per transaction.',
          [P('p1', 'Fair value', 5, 'fair value'), P('p2', 'Proportionate share', 5, 'proportionate')], 'c2'),
        V('v4', 'How is a bargain purchase gain treated in India?', 'It goes to OCI and capital reserve if the reasons are clearly evidenced; otherwise directly to capital reserve in equity.',
          [P('p1', 'Capital reserve', 6, 'capital reserve'), P('p2', 'OCI with evidence', 4, 'oci')], 'c3'),
        V('v5', 'Describe the pooling of interests method.', 'Assets and liabilities are combined at carrying amounts, with no new goodwill, and comparatives restated as if combined from the earliest period.',
          [P('p1', 'Carrying amounts', 5, 'carrying'), P('p2', 'Restated', 5, 'restat')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Nova Holdings Ltd.', 'difficulty': 'moderate',
              'case': 'Nova Holdings Ltd. buys 100% of Rio Ltd. for ₹500 crore. Rio\'s book net assets are ₹350 crore; fair value uplifts: land +₹40 crore, an unrecognised brand ₹60 crore; a contingent liability (possible obligation, fair value reliable) ₹10 crore. Ignore deferred tax. Six months later, a valuation shows the brand was worth ₹70 crore at acquisition.',
              'mcqs': [
                  M('k1a', 'Fair value of identifiable net assets initially (₹ crore):', ['440', '450', '350', '390'], 0,
                    '350 + 40 + 60 − 10 = 440. In practice: include contingent liability.', 'moderate', check=440, topic=T2),
                  M('k1b', 'Initial goodwill (₹ crore):', ['60', '150', '50', '110'], 0,
                    '500 − 440 = 60. In practice: test for impairment.', 'core', check=60, topic=T3),
                  M('k1c', 'After the brand revaluation, goodwill becomes (₹ crore):', ['50', '60', '70', '40'], 0,
                    'Measurement period adjustment: 60 − 10. In practice: retrospective.', 'moderate', check=50, topic=T4),
                  M('k1d', 'The brand, never recognised by Rio, is:', ['Recognised as an identifiable intangible', 'Part of goodwill', 'Ignored', 'Expensed'], 0,
                    'Identifiable intangibles are recognised in the combination. In practice: separate from goodwill.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch12', 1, 'Ind AS 103 "Business Combinations"',
                ['Identify business combinations, the acquirer and acquisition date.',
                 'Recognise and measure identifiable assets, liabilities and NCI.',
                 'Measure consideration, goodwill and bargain purchase gains.',
                 'Apply step acquisition, measurement period and common control rules.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 40}, 'prereq': ['fin-p1-ch11-u07'],
                 'exam_tip': 'Write the goodwill formula and fill each component — consideration, NCI, previous stake, net assets.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Business: input + substantive process.',
                             'Acquisition method: acquirer, date, net assets, goodwill.',
                             'Fair value with listed exceptions.',
                             'Costs expensed; contingent consideration at fair value.',
                             'Common control: pooling of interests.'],
                 'remember': ['Bargain purchase → capital reserve.'],
                 'traps': ['Capitalising acquisition costs.']},
                [('Goodwill', 'Consideration + NCI + old stake − net assets'), ('Costs', 'Expense'), ('Bargain', 'Capital reserve'), ('Common control', 'Pooling')],
                viva, cases)
