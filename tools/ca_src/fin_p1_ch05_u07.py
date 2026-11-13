"""CA Final · Paper 1 Financial Reporting · Chapter 5 Unit 7 Ind AS 105 Non-current Assets Held for Sale and Discontinued Operations.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch05-u07'
T1 = 'Held-for-sale classification criteria'
T2 = 'Measurement of held-for-sale items'
T3 = 'Disposal groups and impairment allocation'
T4 = 'Discontinued operations and presentation'


def build():
    ck = Checks()
    fv = ck.add('300-12', 'Fair value minus selling costs (₹ lakh)')
    imp = ck.add('320-(300-12)', 'Impairment loss on classification (₹ lakh)')
    rev = ck.add('305-12-(300-12)', 'Later gain recognised (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'A factory put up for sale', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'On 1 January, Delta Ltd. commits to sell a factory with a carrying amount of ₹320 lakh; all held-for-sale criteria are met that day. Fair value is ₹300 lakh and selling costs are ₹12 lakh. At 31 March, fair value rises to ₹305 lakh with selling costs unchanged. Compute the impairment at classification and the gain at 31 March. Is depreciation charged after 1 January?',
          'solution': [table(['Step', 'Working', '₹ lakh'], [
              ['Fair value minus selling costs', '300 − 12', inr(fv)],
              ['Carrying amount', 'Before classification (after updating per Ind AS 16)', inr(320)],
              ['Impairment on classification', '320 − 288', inr(imp)],
              ['Fair value minus selling costs at 31 March', '305 − 12 = 293', inr(293)],
              ['Gain recognised (capped at cumulative impairment of 32)', '293 − 288', inr(rev)],
              ['Depreciation after 1 January', 'Stops once classified as held for sale', 'Nil']], title='Ind AS 105 measurement')],
          'checks': list(ck)}

    ck2 = Checks()
    ga = ck2.add('40', 'Impairment absorbed by goodwill (₹ lakh)')
    ppe = ck2.add('(60-40)*300/(300+100)', 'Share to PPE (₹ lakh)')
    ri = ck2.add('(60-40)*100/(300+100)', 'Share to right-of-use asset (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Allocating loss in a disposal group', 'difficulty': 'hard', 'minutes': 10,
          'q': 'A disposal group contains goodwill ₹40 lakh, PPE ₹300 lakh, a right-of-use asset ₹100 lakh, inventory ₹80 lakh and financial assets ₹50 lakh (all remeasured under their own standards). Fair value minus selling costs of the group is ₹510 lakh. Allocate the impairment.',
          'solution': [table(['Asset', 'Working', '₹ lakh'], [
              ['Total carrying amount', '40 + 300 + 100 + 80 + 50 = 570', inr(570)],
              ['Impairment', '570 − 510', inr(60)],
              ['Goodwill first', 'Fully written off', inr(ga)],
              ['PPE (pro rata among in-scope assets)', '20 × 300/400', inr(ppe)],
              ['Right-of-use asset', '20 × 100/400', inr(ri)],
              ['Inventory and financial assets', 'Outside the measurement scope — no allocation', 'Nil']], title='Disposal group impairment')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Ind AS 105 labels a non-current asset, or a disposal group, as held for sale when its carrying amount will be recovered mainly by selling it, not by using it. Two conditions: it must be ready to be sold now in its current state on normal terms, and the sale must be highly probable.',
            'Highly probable means: management at an appropriate level is committed to a plan; an active programme to find a buyer has begun; it is marketed at a reasonable price; sale is expected to complete within one year of classification (extensions allowed for events beyond the entity\'s control); and significant changes to the plan are unlikely. Shareholder approval, if required, is part of the probability assessment.',
            'Assets acquired solely for resale are classified at acquisition if the one-year test is met and other criteria are highly likely to be met shortly. Assets to be abandoned are not held for sale. The same principles apply to items held for distribution to owners.'],
          'Held for sale means "on its way out" — ready, marketed and likely to go within a year.',
          'A plant still needing major repairs before a buyer will take it is not yet ready.'),
        C('c2', T2, [
            'Just before first classification, carrying amounts are measured under the applicable standards. After that, the item is carried at whichever is lower: its carrying amount, or fair value minus selling costs.',
            'Write-downs to fair value minus selling costs are impairment losses in profit or loss. Later increases are recognised as gains, but not beyond cumulative impairment previously recognised (under Ind AS 105 or Ind AS 36).',
            'Depreciation and amortisation stop while held for sale; interest and other expenses of liabilities in a disposal group continue. If the sale is expected beyond one year, selling costs are discounted. If the plan changes, the asset is measured at the lower of its adjusted carrying amount (as if never classified) and recoverable amount.'],
          'Freeze depreciation; carry at the lower figure; gains only up to past losses.',
          'An asset written down by 32 can recover at most 32.'),
        C('c3', T3, [
            'A disposal group is a group of assets (and directly associated liabilities) to be disposed of together in one transaction. It may include goodwill and current assets.',
            'The measurement rules apply to the group as a whole, but certain assets inside it — deferred tax assets, employee benefit assets, financial assets under Ind AS 109, investment property under the fair value model elsewhere, biological assets, insurance contract rights — keep their own measurement rules.',
            'The group\'s impairment loss reduces goodwill before anything else; any balance is spread proportionately over the non-current assets within the measurement scope, in the order set by Ind AS 36.'],
          'The group is tested as one; the loss lands on goodwill first.',
          'Inventory in a disposal group is measured under Ind AS 2, not written down by the group loss.'),
        C('c4', T4, [
            'A discontinued operation is a component of the entity that has been disposed of or is held for sale and is a distinct major business line or a major region of operations, belongs to one coordinated plan to exit such a line or region, or is a subsidiary acquired only to resell.',
            'Presentation: one combined figure in profit or loss for the after-tax result of discontinued operations plus the after-tax gain or loss on remeasurement or disposal; analysis in the notes or on the face. Comparatives are re-presented.',
            'In the balance sheet, held-for-sale assets and liabilities of a disposal group are presented separately and not offset; comparatives for the balance sheet are not re-presented. Cumulative OCI relating to the group is shown separately in equity.'],
          'Discontinued operations get their own line so investors can see continuing performance.',
          'Selling the entire hotels division is a discontinued operation; selling one hotel usually is not.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Divestment year-end', 'role': 'Group reporting manager',
             'situation': 'The board approved selling a division in February; the year ends in March.',
             'steps': ['Test each held-for-sale criterion at year end.', 'Remeasure assets under their own standards first.', 'Compare with fair value minus selling costs.', 'Present discontinued results and re-present comparatives.'],
             'takeaway': 'Classification date drives depreciation stop and presentation.'}]

    mcqs = [
        Q('m1', 'A held-for-sale asset is measured at:', ['The lower of carrying amount and fair value minus selling costs', 'Fair value', 'Carrying amount', 'Higher of the two'], 0,
          'Conservative measurement. In practice: compare at classification and each reporting date.', 'c2', T2),
        Q('m2', 'Depreciation on an asset classified as held for sale:', ['Stops', 'Continues', 'Doubles', 'Is charged to OCI'], 0,
          'Its value will come from selling it. In practice: note the classification date.', 'c2', T2),
        Q('m3', 'An asset to be abandoned is:', ['Not classified as held for sale', 'Held for sale', 'A discontinued operation always', 'Inventory'], 0,
          'Its value comes from use until abandonment. In practice: a closed line may still be discontinued.', 'c1', T1),
        Q('m4', 'Impairment of a disposal group is allocated first to:', ['Goodwill', 'Inventory', 'Financial assets', 'Deferred tax assets'], 0,
          'Then pro rata to in-scope non-current assets. In practice: excluded assets keep their own rules.', 'c3', T3),
        Q('m5', 'A sale is ordinarily expected to be completed within:', ['One year of classification', 'Three months', 'Two years', 'Five years'], 0,
          'Extensions are allowed for events beyond control. In practice: document the timeline.', 'c1', T1),
        Q('m6', 'Results of discontinued operations are shown:', ['As a single amount after tax', 'Within revenue', 'In OCI', 'In retained earnings directly'], 0,
          'A separate line in profit or loss. In practice: re-present comparatives.', 'c4', T4),
        Q('m7', 'A later increase in fair value minus selling costs is recognised:', ['As a gain up to cumulative impairment', 'Without limit', 'In OCI', 'Not at all'], 0,
          'The cap prevents gains above original carrying amount. In practice: track cumulative impairment.', 'c2', T2),
        Q('m8', 'Balance sheet comparatives for held-for-sale assets are:', ['Not re-presented', 'Re-presented', 'Deleted', 'Shown as discontinued'], 0,
          'Only profit or loss comparatives are re-presented. In practice: note this asymmetry.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Fair value minus costs', 1, 'computation', 'selling', nums=[fv]), S('s2', 'Impairment', 2, 'computation', 'impairment', nums=[imp]), S('s3', 'Gain capped', 2, 'computation', 'gain', nums=[rev]), S('s4', 'Depreciation stops', 1, 'concept', 'depreciation')],
          ['State the cap.'], ['Continuing depreciation.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Total impairment', 1, 'computation', 'impairment', nums=[60]), S('s2', 'Goodwill', 1.5, 'computation', 'goodwill', nums=[ga]), S('s3', 'Pro rata', 2.5, 'computation', 'pro rata', nums=[ppe, ri]), S('s4', 'Excluded assets', 1, 'concept', 'inventory|financial')],
          ['Exclude out-of-scope assets.'], ['Allocating to inventory.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are the two main conditions for held-for-sale classification?', 'The asset must be ready for immediate sale in its current state and the sale must be highly probable.',
          [P('p1', 'Ready for sale', 5, 'ready'), P('p2', 'Highly probable', 5, 'probable')], 'c1'),
        V('v2', 'Why does depreciation stop on held-for-sale assets?', 'Because their value will be recovered through selling them, so the measurement basis becomes sale value rather than use.',
          [P('p1', 'Recovery by sale', 6, 'sell|sale'), P('p2', 'Measurement basis', 4, 'measurement')], 'c2'),
        V('v3', 'What is a discontinued operation?', 'A component disposed of or held for sale that is a distinct major line of business or a major geographical region, part of a plan to exit one, or a subsidiary bought only to resell.',
          [P('p1', 'Component', 4, 'component'), P('p2', 'Major line or area', 6, 'major line|geographical')], 'c4'),
        V('v4', 'How is a disposal group impairment allocated?', 'First to goodwill, then pro rata to the in-scope non-current assets.',
          [P('p1', 'Goodwill first', 6, 'goodwill'), P('p2', 'Pro rata', 4, 'pro rata')], 'c3'),
        V('v5', 'How are discontinued results presented?', 'As one after-tax amount in profit or loss, with comparatives re-presented and an analysis given.',
          [P('p1', 'Single after-tax amount', 6, 'after-tax|single'), P('p2', 'Comparatives', 4, 'comparative')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Orion Industries Ltd.', 'difficulty': 'moderate',
              'case': 'Orion Industries Ltd. decides in January to sell its entire textiles division, a separate major line of business. A broker is appointed, the price is reasonable, and sale is expected by October. Division net assets carry ₹900 lakh; fair value is ₹850 lakh and selling costs ₹20 lakh. Division loss after tax for the year is ₹45 lakh.',
              'mcqs': [
                  M('k1a', 'Impairment on classification (₹ lakh):', ['70', '50', '20', 'Nil'], 0,
                    '900 − (850 − 20) = 70. In practice: book in profit or loss.', 'core', check=70, topic=T2),
                  M('k1b', 'The textiles division is:', ['A discontinued operation', 'Continuing', 'An abandoned asset', 'Inventory'], 0,
                    'A separate major line held for sale. In practice: show a single line in profit or loss.', 'core', topic=T4),
                  M('k1c', 'Total loss in the discontinued operations line (₹ lakh):', ['115', '45', '70', '25'], 0,
                    '45 operating loss + 70 remeasurement loss = 115 (after tax, assuming no tax effect). In practice: analyse in notes.', 'moderate', check=115, topic=T4),
                  M('k1d', 'Prior year profit and loss comparatives are:', ['Re-presented to show the division as discontinued', 'Left unchanged', 'Restated under Ind AS 8', 'Omitted'], 0,
                    'Re-presentation aids comparison. In practice: not an error correction.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch05', 7, 'Ind AS 105 "Non-current Assets Held for Sale and Discontinued Operations"',
                ['Apply the held-for-sale classification criteria.',
                 'Measure held-for-sale assets and disposal groups.',
                 'Allocate impairment within a disposal group.',
                 'Identify and present discontinued operations.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['fin-p1-ch05-u06'],
                 'exam_tip': 'Remeasure under the asset\'s own standard first, then apply the lower-of test, and stop depreciation.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Ready for sale + highly probable within one year.',
                             'Lower of carrying amount and fair value minus selling costs.',
                             'No depreciation while held for sale.',
                             'Group loss: goodwill first, then pro rata.',
                             'Discontinued results: single after-tax line; re-present comparatives.'],
                 'remember': ['Gains capped at cumulative impairment.'],
                 'traps': ['Re-presenting balance sheet comparatives.']},
                [('Measure', 'Lower of CA and FV − costs'), ('Depreciation', 'Stops'), ('Time limit', 'One year'), ('Discontinued', 'Single P&L line')],
                viva, cases)
