"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 7 Unit 1 — AS 4 Contingencies and Events Occurring after the Balance Sheet Date.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch07-u01'
T1 = 'What is left of contingencies in AS 4'
T2 = 'The period covered by events after the balance sheet date'
T3 = 'Adjusting events'
T4 = 'Non-adjusting events and going concern'
T5 = 'Dividends and disclosure'


def build():
    ck = Checks()
    prov = ck.add('800000*60/100', 'Provision for the debtor (₹)')
    i1 = {'id': 'i1', 'title': 'A customer goes bankrupt in May', 'difficulty': 'core', 'minutes': 6,
          'q': 'Ishaan Ltd.\'s accounts for the year to 31 March 2027 are approved on 10 June 2027. A customer owing ₹8,00,000 at 31 March was declared insolvent on 5 May 2027 after losses it had been making for over a year; only 40% is expected to be recovered. A second customer, who was sound at 31 March, lost its factory in a flood on 20 May 2027. How should each be treated?',
          'solution': [table(['Event', 'Type', 'Treatment'], [
              ['First customer insolvent', 'Adjusting — its weak condition existed at 31 March', f'Provide {inr(prov)} (60% of ₹8,00,000)'],
              ['Second customer\'s flood', 'Non-adjusting — the condition arose after 31 March', 'No adjustment; disclose in the Board\'s report if material']], title='AS 4 classification')],
          'checks': list(ck)}

    ck2 = Checks()
    d = ck2.add('3000000*15/100', 'Dividend declared after year end (₹)')
    i2 = {'id': 'i2', 'title': 'Dividend and a fire', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'On 25 April 2027 the Board of Kalyan Ltd. (paid-up equity ₹30,00,000) proposed a 15% dividend for 2026-27. On 2 May a fire destroyed its only plant, and the company has no insurance or plan to rebuild. Accounts are approved on 15 May. Advise.',
          'solution': [table(['Matter', 'Treatment'], [
              ['Proposed dividend', f'Not a liability at 31 March; disclose {inr(d)} in the notes'],
              ['Fire with no rebuild', 'Going concern no longer appropriate — the statements are not prepared on the going concern basis; this is an adjusting matter in effect']], title='AS 4')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'The contingency paragraphs of AS 4 apply only so far as no other standard covers the matter. With AS 29 handling provisions and contingent liabilities, AS 4 contingencies now matter mainly for items such as impairment of receivables.',
            'A contingency is a condition at the balance sheet date whose final outcome, gain or loss, depends on uncertain future events.',
            'A contingent loss is provided for if it is probable that a future event will confirm the impairment of an asset (or a liability) at the balance sheet date and the amount can be estimated reasonably. Contingent gains are not recognised.'],
          'Provide for likely losses that already exist; never book hoped-for gains.',
          'Doubtful debts are a classic contingency still dealt with by AS 4.'),
        C('c2', T2, [
            'Events after the balance sheet date are significant events, favourable or unfavourable, that happen between the balance sheet date and the date the financial statements are approved by the Board (or the approving authority for non-companies).',
            'Events after approval are outside AS 4.'],
          'The window runs from the year end to the Board\'s approval.',
          'For a 31 March year end approved on 4 September, April to 4 September events are covered.'),
        C('c3', T3, [
            'Adjusting events give further evidence about conditions that existed at the balance sheet date. Assets and liabilities are adjusted for them.',
            'Examples: a debtor\'s insolvency after the year end where its weakness existed earlier; sale of inventory below cost soon after the year end, showing net realisable value at the year end; settlement of a court case confirming an obligation that existed at the year end; discovery of fraud or errors showing the statements were wrong.'],
          'If the event explains how things already stood on the year end date, adjust.',
          'Stock sold in April at 30% below cost shows its year-end value was already lower.'),
        C('c4', T4, [
            'Non-adjusting events relate to conditions that arose after the balance sheet date. No adjustment is made, but material ones are disclosed in the report of the approving authority so users can judge their effect.',
            'Examples: a fall in market value of investments after the year end, destruction of a plant by fire after the year end, a major share issue or acquisition after the year end.',
            'Exception — going concern: if events after the year end show that the going concern assumption is no longer appropriate (for example the main plant is destroyed with no plan to continue), the statements are not prepared on the going concern basis.'],
          'New conditions after the year end are reported, not booked — unless they threaten survival.',
          'A sharp market crash in April does not change the 31 March investment values.'),
        C('c5', T5, [
            'Dividends declared or proposed after the balance sheet date are not a liability at that date, because no obligation then existed (unless a statute says otherwise). They are disclosed in the notes.',
            'For each event disclosed, describe what happened and roughly how much it affects the accounts — or say plainly that the effect cannot yet be worked out.'],
          'A dividend becomes a debt only when it is declared, not when the year closes.',
          'A dividend proposed in May for the previous year appears only in a note.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Subsequent events review', 'role': 'Audit assistant',
             'situation': 'Between year end and Board approval, a lawsuit was settled, a debtor failed and a warehouse burned down.',
             'steps': ['List events up to the approval date.', 'Classify each as adjusting or non-adjusting.', 'Adjust the accounts for adjusting events.', 'Draft disclosures and check going concern.'],
             'takeaway': 'The key question is when the underlying condition arose.'}]

    mcqs = [
        Q('m1', 'Events after the balance sheet date are those occurring between the balance sheet date and:', ['The date the Board approves the financial statements', 'The date of the AGM', 'The due date of filing the return', 'The end of the next quarter'], 0,
          'AS 4 covers significant events between the year end and the date on which the Board (or other approving authority) approves the statements. Later events are outside its scope. In practice: note the approval date.', 'c2', T2),
        Q('m2', 'Which is an adjusting event?', ['Inventory held at year end sold soon after below cost', 'A fire after the year end', 'A fall in share prices after the year end', 'Issue of new shares after the year end'], 0,
          'Sale of year-end inventory below cost gives evidence of its net realisable value at the balance sheet date, so the inventory is adjusted. The others arise from conditions after the year end. In practice: test year-end values.', 'c3', T3),
        Q('m3', 'A plant destroyed by fire after the year end, with the business continuing, is:', ['A non-adjusting event, disclosed if material', 'An adjusting event', 'Ignored', 'A prior period item'], 0,
          'The fire is a new condition arising after the balance sheet date, so assets are not adjusted, but a material effect is disclosed in the approving authority\'s report. In practice: estimate the loss.', 'c4', T4),
        Q('m4', 'A dividend proposed after the year end is:', ['Disclosed in the notes, not recognised as a liability', 'Recognised as a liability', 'Debited to profit and loss', 'Ignored'], 0,
          'No obligation exists at the balance sheet date for a dividend declared or proposed later, so it is not a liability unless statute requires; it is disclosed in the notes. In practice: this follows the 2016 amendment.', 'c5', T5),
        Q('m5', 'Events after the year end show the company will be wound up. The statements are:', ['Not prepared on the going concern basis', 'Prepared as usual with disclosure', 'Delayed for a year', 'Prepared on cash basis'], 0,
          'If going concern is no longer appropriate, the basis of accounting changes; this is an exception to the non-adjusting rule because the whole basis is affected. In practice: assets move towards realisable values.', 'c4', T4),
        Q('m6', 'Contingent gains under AS 4 are:', ['Not recognised', 'Recognised when probable', 'Recognised when possible', 'Recognised at fair value'], 0,
          'Recognising contingent gains could record income that may never be realised, so AS 4 does not allow it. Contingent losses are provided if probable and reasonably estimable. In practice: AS 29 adds detail for most cases.', 'c1', T1),
        Q('m7', 'A court ruling after the year end confirms a damages claim relating to an incident before the year end. It is:', ['An adjusting event', 'A non-adjusting event', 'A contingent gain', 'Irrelevant'], 0,
          'The ruling gives evidence about an obligation that existed at the balance sheet date, so the liability is adjusted to the settled amount. In practice: update the provision.', 'c3', T3),
        Q('m8', 'Disclosure of a material non-adjusting event includes:', ['What happened and its likely money effect (or that it cannot be estimated)', 'Only its date', 'Only the auditor\'s view', 'Nothing'], 0,
          'AS 4 asks what happened and roughly what it does to the accounts; if no estimate is possible, the disclosure must say so. In practice: be specific about amounts where possible.', 'c5', T5),
        Q('m9', 'Discovery after year end of a fraud committed during the year is:', ['An adjusting event', 'A non-adjusting event', 'Outside AS 4', 'A contingent gain'], 0,
          'Fraud or errors discovered later show that the statements were incorrect at the balance sheet date, so they are adjusted. In practice: investigate the extent before approval.', 'c3', T3),
        Q('m10', 'A debtor owing ₹5 lakh at year end becomes insolvent after year end due to a weakness existing at year end; 30% is recoverable. Provision:', ['₹3.5 lakh', '₹1.5 lakh', '₹5 lakh', 'Nil'], 0,
          'The insolvency confirms the debtor was already impaired at the year end, so 70% of ₹5 lakh, i.e. ₹3.5 lakh, is provided. In practice: update the expected recovery.', 'c3', T3, 'moderate', check=3.5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'First debtor adjusting', 2, 'computation', 'adjusting', nums=[prov]),
           S('s2', 'Flood non-adjusting', 2, 'concept', 'non-adjusting')],
          ['Ask when the condition arose.'], ['Adjusting for the flood.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Dividend not liability', 2, 'concept', 'not a liability|disclose', nums=[d]),
           S('s2', 'Going concern exception', 2, 'concept', 'going concern')],
          ['Treat going concern separately.'], ['Recording the dividend as a liability.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are adjusting events?', 'Events after the balance sheet date that give further evidence of conditions existing at that date, requiring adjustment of assets and liabilities.',
          [P('p1', 'Evidence of existing conditions', 6, 'existing|existed|evidence'), P('p2', 'Adjust', 4, 'adjust')], 'c3'),
        V('v2', 'What are non-adjusting events?', 'Events reflecting conditions that arose after the balance sheet date; they are disclosed if material but the accounts are not changed.',
          [P('p1', 'Arose after', 6, 'after'), P('p2', 'Disclosed', 4, 'disclos')], 'c4'),
        V('v3', 'When does the AS 4 period end?', 'On the date the Board of Directors or other approving authority approves the financial statements.',
          [P('p1', 'Approval', 6, 'approv'), P('p2', 'Board', 4, 'board|authority')], 'c2'),
        V('v4', 'How are dividends proposed after the year end treated?', 'They are disclosed in the notes; the obligation to pay arises only on declaration, after the balance sheet date.',
          [P('p1', 'Notes', 6, 'notes'), P('p2', 'No obligation', 4, 'obligation')], 'c5'),
        V('v5', 'Why is going concern an exception?', 'If later events show the enterprise must close down, the whole basis of preparing the statements changes, so they cannot be prepared on the going concern basis.',
          [P('p1', 'Must close', 5, 'close'), P('p2', 'Basis changes', 5, 'basis')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Pooja Traders Ltd.', 'difficulty': 'moderate',
              'case': 'Pooja Traders Ltd. (year end 31 March 2027, approval 20 May 2027): (1) on 15 April a debtor of ₹6 lakh with year-long losses was declared insolvent, 50% recoverable; (2) on 10 May investments worth ₹20 lakh at 31 March fell 25% in a market crash; (3) on 18 May the Board proposed a dividend of ₹4 lakh.',
              'mcqs': [
                  M('k1a', 'Provision for the insolvent debtor:', ['₹3 lakh', '₹6 lakh', 'Nil', '₹1.5 lakh'], 0,
                    'The debtor\'s weakness existed at the year end, so this is adjusting; 50% of ₹6 lakh = ₹3 lakh is provided. In practice: adjust before approval.', 'core', check=3, topic=T3),
                  M('k1b', 'The market fall in investments is:', ['Non-adjusting; disclosed if material', 'Adjusting; write down by ₹5 lakh', 'Ignored completely', 'A prior period item'], 0,
                    'The fall reflects market conditions after the balance sheet date, so values at 31 March stand; a material effect is disclosed in the Board\'s report. In practice: quantify it.', 'moderate', topic=T4),
                  M('k1c', 'The proposed dividend of ₹4 lakh is:', ['Disclosed in notes only', 'Shown as a current liability', 'Debited to retained earnings at 31 March', 'Ignored'], 0,
                    'Dividends proposed after the year end are not liabilities at the balance sheet date and are disclosed in the notes. In practice: show the amount per share too.', 'core', topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch07', 1, 'Accounting Standard 4 Contingencies and Events occurring after the Balance Sheet Date',
                ['Explain the residual role of contingencies under AS 4.',
                 'Identify the period for events after the balance sheet date.',
                 'Classify events as adjusting or non-adjusting and apply the going concern exception.',
                 'Treat dividends and make the required disclosures.'],
                {'difficulty': 'core', 'minutes': {'learn': 20, 'practice': 20}, 'prereq': ['int-p1-ch06-u02'],
                 'exam_tip': 'For each event ask: did the condition exist on the year-end date? Yes → adjust; no → disclose.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Contingency rules apply only where no other standard covers.', 'Window: year end to Board approval.',
                             'Adjusting: evidence of year-end conditions → adjust.', 'Non-adjusting: new conditions → disclose in approving authority\'s report.',
                             'Going concern failure overrides.', 'Dividends after year end: notes only.'],
                 'remember': ['Contingent gains are never recognised.'],
                 'traps': ['Proposed dividends are not liabilities.']},
                [('Window', 'Year end → approval'), ('Adjusting', 'Year-end conditions'), ('Dividend', 'Disclose only')],
                viva, cases)
