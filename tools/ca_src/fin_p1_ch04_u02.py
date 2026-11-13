"""CA Final · Paper 1 Financial Reporting · Chapter 4 Unit 2 Ind AS 10 Events after the Reporting Period.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch04-u02'
T1 = 'Meaning and period of events after the reporting period'
T2 = 'Adjusting events'
T3 = 'Non-adjusting events and disclosure'
T4 = 'Dividends and going concern'


def build():
    i1 = {'id': 'i1', 'title': 'Adjust or disclose?', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Year end 31 March 2027; statements approved for issue 18 May 2027. Classify: (a) on 20 April a customer owing ₹2 crore at 31 March is declared bankrupt; its financial trouble began in January; (b) on 25 April a fire destroys a warehouse; (c) on 2 May a court confirms that the company must pay ₹80 lakh for a case filed in 2026 (provision at year end: ₹50 lakh); (d) inventory held at 31 March is sold in April below cost; (e) on 10 May the Board proposes a final dividend; (f) on 5 June a major acquisition is agreed.',
          'solution': [table(['Event', 'Type', 'Treatment'], [
              ['(a)', 'Adjusting', 'Evidence of impairment existing at 31 March — recognise loss allowance'],
              ['(b)', 'Non-adjusting', 'Condition arose after year end — disclose nature and estimated effect if material'],
              ['(c)', 'Adjusting', 'Confirms a present obligation at year end — increase provision to ₹80 lakh'],
              ['(d)', 'Adjusting', 'Evidence of net realisable value at year end — write down inventory'],
              ['(e)', 'Non-adjusting', 'No liability at 31 March — disclose in notes'],
              ['(f)', 'Outside Ind AS 10', 'Occurs after approval date — not considered']], title='Ind AS 10')],
          'checks': []}

    ck = Checks()
    w = ck.add('(120-95)*4000/100000', 'Inventory write-down (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Inventory sold below cost after year end', 'difficulty': 'core', 'minutes': 5,
          'q': '4,000 units held at 31 March cost ₹120 each. In April they are sold at ₹100 each with selling costs of ₹5 per unit. Compute the write-down to recognise at 31 March.',
          'solution': [table(['Item', 'Working', 'Answer'], [
              ['Net realisable value per unit', '100 − 5', '₹95'],
              ['Write-down per unit', '120 − 95', '₹25'],
              ['Total write-down', '4,000 × ₹25', '₹' + str(w) + ' lakh']], title='Adjusting event')],
          'checks': list(ck)}

    concepts = [
        C('c1', T1, [
            'Ind AS 10 deals with good and bad events falling after the year-end date but before the Board authorises the statements for issue.',
            'The date of approval is the date the Board (or equivalent) authorises issue — even if shareholders approve later. Entities disclose the approval date and who gave it; if owners can amend statements after issue, that fact is disclosed.',
            'Events after the approval date are outside the standard; the statements are not updated for them.'],
          'Ind AS 10 covers the window between the balance sheet date and Board approval.',
          'For a 31 March year end with Board approval on 20 May, events until 20 May count.'),
        C('c2', T2, [
            'Adjusting events throw light on circumstances already present on the year-end date, so the recognised amounts are changed.',
            'Examples: settlement of a court case confirming an obligation at year end; information that an asset was impaired at year end (a customer\'s bankruptcy, sale of inventory below cost); determination after year end of the cost of assets bought or proceeds of assets sold before year end; profit-sharing or bonus payments for which there was a present obligation; and discovery of fraud or errors showing the statements are incorrect.',
            'Disclosures relating to conditions at year end are updated for new information.'],
          'Adjusting events shed new light on what was already true at year end.',
          'A debtor\'s insolvency in April usually reflects difficulties that existed in March.'),
        C('c3', T3, [
            'Non-adjusting events indicate conditions that arose after the reporting period; amounts are not adjusted.',
            'Examples: a decline in the fair value of investments after year end; major business combinations or disposals; announcing a plan to discontinue an operation; major asset purchases; destruction of a plant by fire; major restructuring announced; large share transactions; abnormal changes in prices or exchange rates; changes in tax rates enacted after year end; entering significant commitments; and litigation arising solely from post-year-end events.',
            'For each material non-adjusting event, the nature and an estimate of the financial effect (or a statement that it cannot be estimated) is disclosed.'],
          'Non-adjusting events are new stories — they are told in the notes, not in the numbers.',
          'A tax rate increase enacted in April does not change deferred tax measured at 31 March.'),
        C('c4', T4, [
            'Dividends declared (proposed) after the reporting period are not recognised as a liability at year end because no obligation existed then; they are disclosed in the notes.',
            'If, after the reporting period, management decides to liquidate or cease trading, or has no realistic alternative, the statements are not prepared on a going concern basis. A deterioration in results and financial position after year end may signal a going concern problem that needs reassessment.',
            'Where the going concern basis is not appropriate, the effect is pervasive — it changes the basis of accounting, not just individual amounts.'],
          'A proposed dividend is a plan, not a debt; a going concern collapse changes everything.',
          'If the Board decides in May to close the company, the March statements cannot use the going concern basis.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Subsequent events review', 'role': 'Audit senior',
             'situation': 'The audit report is due next week; the year ended six weeks ago.',
             'steps': ['Read Board minutes after year end.', 'Review post-year-end sales, receipts and legal letters.', 'Classify each event as adjusting or non-adjusting.', 'Confirm the approval date and update disclosures.'],
             'takeaway': 'The review runs until the approval date, not just the year end.'}]

    mcqs = [
        Q('m1', 'Events after the reporting period cover the period up to:', ['The date the statements are approved for issue', 'The AGM date', 'The tax filing date', 'Three months after year end'], 0,
          'The cut-off is the Board\'s approval for issue. In practice: disclose that date.', 'c1', T1),
        Q('m2', 'Which is an adjusting event?', ['Settlement of a court case confirming a year-end obligation', 'A fire after year end', 'A fall in share prices after year end', 'A new acquisition after year end'], 0,
          'It gives evidence of a condition at year end. In practice: adjust the provision.', 'c2', T2),
        Q('m3', 'A dividend proposed by the Board after year end is:', ['Disclosed, not recognised as a liability', 'Recognised as a liability', 'Charged to profit', 'Ignored'], 0,
          'There was no obligation at the reporting date. In practice: show in notes with per share amount.', 'c4', T4),
        Q('m4', 'A change in tax rate enacted after the reporting date is:', ['Non-adjusting, disclosed if material', 'Adjusting', 'An error', 'Ignored completely'], 0,
          'Measurement uses rates enacted or substantively enacted at year end. In practice: disclose the effect.', 'c3', T3),
        Q('m5', 'Discovery after year end of a fraud that occurred during the year is:', ['Adjusting', 'Non-adjusting', 'Outside the standard', 'A change in estimate'], 0,
          'It shows the statements are incorrect as at year end. In practice: correct the amounts.', 'c2', T2),
        Q('m6', 'If management decides to liquidate the entity after year end:', ['The going concern basis is not used', 'Only disclose it', 'Adjust only inventory', 'Ignore it'], 0,
          'The going concern basis becomes inappropriate. In practice: a different basis is applied and disclosed.', 'c4', T4),
        Q('m7', 'For a material non-adjusting event, the entity discloses:', ['Its nature and an estimate of financial effect', 'Only its date', 'Nothing', 'A restatement'], 0,
          'Or states that an estimate cannot be made. In practice: keep it specific.', 'c3', T3),
        Q('m8', 'An event occurring after the statements are approved for issue is:', ['Outside Ind AS 10', 'Adjusting', 'Non-adjusting', 'A prior period error'], 0,
          'The standard\'s window closes at approval. In practice: may be reported next year.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Bankruptcy and court', 2, 'concept', 'adjusting'), S('s2', 'Fire and dividend', 2, 'concept', 'non-adjusting|disclose'),
           S('s3', 'Inventory', 1, 'concept', 'realisable'), S('s4', 'After approval', 1, 'concept', 'approval')],
          ['Give the condition test each time.'], ['Recognising the proposed dividend.'], ['Table.'], pad='table'),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'NRV', 1, 'computation', 'realisable'), S('s2', 'Write-down', 2, 'computation', 'write', nums=[w])],
          ['Deduct selling costs.'], ['Ignoring selling costs.'], ['Table.'], pad='table', checks=list(ck)),
    ]

    viva = [
        V('v1', 'Define events after the reporting period.', 'Good and bad events occurring after the year-end date and before the Board authorises the statements for issue.',
          [P('p1', 'Good and bad', 4, 'good|bad'), P('p2', 'Up to authorisation', 6, 'authoris')], 'c1'),
        V('v2', 'What distinguishes adjusting from non-adjusting events?', 'Adjusting events give evidence of conditions existing at the reporting date; non-adjusting events show conditions that arose after it.',
          [P('p1', 'Existing conditions', 5, 'existing|existed'), P('p2', 'Arose after', 5, 'arose|after')], 'c2'),
        V('v3', 'Give two non-adjusting events.', 'Destruction of a plant by fire after year end and a major business combination after year end.',
          [P('p1', 'Fire', 5, 'fire'), P('p2', 'Combination', 5, 'combination|acquisition')], 'c3'),
        V('v4', 'Why is a proposed dividend not a liability?', 'Because the duty to pay comes into being only once it is declared after year end, so at the reporting date there was nothing owed.',
          [P('p1', 'Duty arises later', 6, 'duty|declared'), P('p2', 'Reporting date', 4, 'reporting date|year end')], 'c4'),
        V('v5', 'What must be disclosed about approval?', 'The date of authorisation for issue, the body that authorised it (usually the Board), and whether owners have power to amend the statements afterwards.',
          [P('p1', 'Date', 5, 'date'), P('p2', 'Authorising body', 5, 'board|body')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Narmada Chemicals Ltd.', 'difficulty': 'moderate',
              'case': 'Narmada Chemicals Ltd. (year end 31 March 2027; approval 22 May 2027): in April it learns that a key supplier\'s plant was shut by regulators in February, raising its own input costs from June; in April its investment in listed shares falls 30%; on 10 May its insurance claim for a March flood is settled at ₹40 lakh more than the receivable recorded; on 15 May it announces a plan to close one division.',
              'mcqs': [
                  M('k1a', 'The 30% fall in listed shares in April is:', ['Non-adjusting', 'Adjusting', 'An error', 'Outside the standard'], 0,
                    'Market value changes after year end reflect later conditions. In practice: disclose if material.', 'core', topic=T3),
                  M('k1b', 'The higher insurance settlement for the March flood is:', ['Adjusting — it gives evidence of the year-end receivable', 'Non-adjusting', 'A contingent asset only', 'Ignored'], 0,
                    'The claim relates to an event at year end; settlement determines the amount. In practice: update the receivable.', 'moderate', topic=T2),
                  M('k1c', 'Announcing the division closure on 15 May is:', ['Non-adjusting, with disclosure', 'Adjusting', 'Outside Ind AS 10', 'A going concern failure'], 0,
                    'A plan announced after year end does not change year-end amounts. In practice: Ind AS 105/37 apply next year.', 'moderate', topic=T3),
                  M('k1d', 'If instead the Board decided on 15 May to wind up the whole company:', ['The statements would not be prepared on a going concern basis', 'Only disclosure is needed', 'Only the division is affected', 'No impact'], 0,
                    'A decision to liquidate before approval removes the going concern basis. In practice: pervasive change.', 'hard', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch04', 2, 'Ind AS 10 "Events after the Reporting Period"',
                ['Identify the period covered by Ind AS 10.',
                 'Distinguish adjusting and non-adjusting events.',
                 'Account for dividends and going concern issues after year end.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 20}, 'prereq': ['fin-p1-ch04-u01'],
                 'exam_tip': 'Ask "did the condition exist at year end?" — yes means adjust, no means disclose.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Window: reporting date to approval for issue.',
                             'Adjusting: evidence of year-end conditions.',
                             'Non-adjusting: new conditions — disclose nature and effect.',
                             'Proposed dividends: disclose only.',
                             'Liquidation decision → no going concern basis.'],
                 'remember': ['Disclose approval date and authority.'],
                 'traps': ['Post-year-end tax rate changes are non-adjusting.']},
                [('Adjusting', 'Condition existed at year end'), ('Non-adjusting', 'Condition arose later'), ('Proposed dividend', 'Disclose')],
                viva, cases)
