"""CA Final · Paper 1 Financial Reporting · Chapter 6 Unit 2 Ind AS 37 Provisions, Contingent Liabilities and Contingent Assets.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch06-u02'
T1 = 'Recognising a provision'
T2 = 'Measuring a provision'
T3 = 'Contingent liabilities and contingent assets'
T4 = 'Applying the rules: onerous contracts, restructuring, future losses'


def build():
    ck = Checks()
    ev = ck.add('0.15*20+0.05*100', 'Warranty provision — expected value (₹ lakh)')
    dec = ck.add('100*0.3855', 'Decommissioning provision at present value (₹ lakh)')
    unw = ck.add('100*0.3855*0.1', 'Unwinding of discount in year 1 (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Warranty and site restoration', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Ray Electronics sells products with a one-year warranty. If all products sold this year had minor defects, repairs would cost ₹20 lakh; if all had major defects, ₹100 lakh. Experience: 80% will have no defects, 15% minor, 5% major. Separately, it must restore a mining site in 10 years at an estimated ₹100 lakh (discount rate 10%, factor 0.3855). Compute both provisions and the year-1 unwinding.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Warranty (expected value of a large population)', '15% × 20 + 5% × 100', inr(ev)],
              ['Decommissioning provision', '100 × 0.3855 — added to the cost of the asset', inr(dec)],
              ['Unwinding year 1 (finance cost)', '38.55 × 10%', inr(unw)]], title='Ind AS 37 measurement')],
          'checks': list(ck)}

    ck2 = Checks()
    fulfil = ck2.add('50-20', 'Net cost of fulfilling (₹ lakh)')
    prov = ck2.add('min(50-20,35)', 'Onerous contract provision (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'A contract that turned sour', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Lumen Ltd. has a firm contract to buy components costing ₹50 lakh, which it no longer needs because a product was discontinued. It can resell the components for ₹20 lakh. Cancelling the contract costs a penalty of ₹35 lakh. Is the contract onerous, and what provision is required?',
          'solution': [table(['Option', 'Working', '₹ lakh'], [
              ['Cost of fulfilling, net of benefits', '50 − 20', inr(fulfil)],
              ['Penalty for exit', 'Given', inr(35)],
              ['Unavoidable cost (lower)', 'Lower of 30 and 35', inr(prov)],
              ['Conclusion', 'Unavoidable cost exceeds benefits — onerous', 'Provide']], title='Onerous contract')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A provision is a liability whose timing or amount is uncertain. It is recognised only when three things are all true: the entity has a present obligation (legal or constructive) arising from a past event; an outflow of resources is probable (more likely than not); and a reliable estimate can be made.',
            'An obligating event leaves the entity with no realistic alternative but to settle. A constructive obligation comes from an established pattern of practice, published policies or a specific current statement that creates valid expectations in others.',
            'Obligations must exist independently of future actions: costs to operate in the future, or fitting filters that the entity could avoid by changing its operations, are not provisions. In rare doubtful cases, a present obligation is assumed if it is more likely than not, taking account of all evidence.'],
          'No past event, no provision — however likely the future cost.',
          'A refund policy the shop always honours is a constructive obligation.'),
        C('c2', T2, [
            'The amount is the best estimate of the spending needed to settle the obligation at the reporting date — what the entity would rationally pay to settle or transfer it.',
            'For a large population, use expected value (weighting outcomes by probability). For a single obligation, the most likely outcome may be best, adjusted if other outcomes are mostly higher or lower. Risks and uncertainties are considered without creating excess provisions.',
            'Where time value is material, discount at a pre-tax rate reflecting current market assessments; the unwinding is a finance cost. Expected future events (e.g. new technology) are reflected if there is sufficient objective evidence. Gains on expected asset disposals are excluded. Reimbursements are recognised separately as an asset only when virtually certain, not exceeding the provision. Provisions are reviewed each reporting date and used only for their original purpose.'],
          'Estimate honestly, discount if material, and never net off expected reimbursements.',
          'A warranty on thousands of units uses expected value.'),
        C('c3', T3, [
            'A contingent liability is either a possible obligation whose existence will be confirmed by uncertain future events outside the entity\'s full control, or a present obligation not recognised because outflow is not probable or cannot be reliably measured. It is disclosed, unless the possibility of outflow is remote.',
            'A contingent asset is a possible asset from past events whose existence depends on uncertain future events. It is not recognised; it is disclosed when an inflow is probable. When realisation becomes virtually certain, the asset is no longer contingent and is recognised.',
            'Contingencies are reassessed continually; when outflow becomes probable, a provision is recognised in that period.'],
          'Liabilities: provide if probable, disclose if possible, ignore if remote. Assets: recognise only if virtually certain.',
          'A lawsuit the company will probably win is a contingent liability disclosed in notes.'),
        C('c4', T4, [
            'Future operating losses are never provided for; they suggest assets may be impaired.',
            'An onerous contract is one where the unavoidable costs of meeting obligations exceed the expected benefits. The unavoidable cost is the lower of the net cost of fulfilling it and any penalty for exiting. Before providing, impairment of dedicated assets is recognised. Costs of fulfilling include incremental costs and an allocation of other directly related costs.',
            'Restructuring provisions require a detailed formal plan and a valid expectation in those affected (by starting implementation or announcing main features). Only direct costs necessarily entailed and not associated with ongoing activities are included — not retraining, relocating staff, marketing or new systems. A sale of an operation creates no obligation until a binding sale agreement exists.'],
          'Provisions cover today\'s obligations, not tomorrow\'s business decisions.',
          'A board decision kept secret creates no restructuring provision.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end legal review', 'role': 'Audit assistant',
             'situation': 'The legal department lists 12 pending cases with lawyers\' assessments.',
             'steps': ['Classify each as probable, possible or remote.', 'Provide for probable cases at best estimate.', 'Disclose possible ones.', 'Check reimbursements from insurers are virtually certain before recognising.'],
             'takeaway': 'Probability bands decide provision, disclosure or silence.'}]

    mcqs = [
        Q('m1', 'A provision is recognised when there is a present obligation, a probable outflow and:', ['A reliable estimate', 'Board approval', 'Cash available', 'An auditor\'s letter'], 0,
          'All three conditions are needed. In practice: estimates are rarely impossible.', 'c1', T1),
        Q('m2', 'Future operating losses are:', ['Not provided for', 'Provided in full', 'Provided if probable', 'Disclosed as contingent'], 0,
          'No present obligation exists. In practice: test assets for impairment.', 'c4', T4),
        Q('m3', 'A contingent asset is recognised when realisation is:', ['Virtually certain', 'Probable', 'Possible', 'Remote'], 0,
          'Then it is no longer contingent. In practice: probable inflows are disclosed only.', 'c3', T3),
        Q('m4', 'For a large population of obligations, the provision uses:', ['Expected value', 'The single most likely outcome', 'The maximum outcome', 'The minimum outcome'], 0,
          'Probability-weighted outcomes. In practice: warranties.', 'c2', T2),
        Q('m5', 'The unavoidable cost of an onerous contract is:', ['Lower of net cost of fulfilling and exit penalty', 'Higher of the two', 'Fulfilment cost only', 'Penalty only'], 0,
          'The entity would choose the cheaper way out. In practice: impair dedicated assets first.', 'c4', T4),
        Q('m6', 'Which cost can be included in a restructuring provision?', ['Redundancy payments to staff being let go', 'Retraining continuing staff', 'Marketing', 'New IT systems'], 0,
          'Only direct, necessary costs unrelated to ongoing activities. In practice: list each cost.', 'c4', T4),
        Q('m7', 'An expected reimbursement from an insurer is:', ['Recognised separately only when virtually certain', 'Netted against the provision', 'Ignored', 'Recognised when probable'], 0,
          'Shown as a separate asset, capped at the provision. In practice: P&L may show net.', 'c2', T2),
        Q('m8', 'A contingent liability with a remote chance of outflow is:', ['Neither recognised nor disclosed', 'Disclosed', 'Provided', 'Recognised in OCI'], 0,
          'Remote items need no disclosure. In practice: guarantees may be an exception under other standards.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Warranty', 2, 'computation', 'expected', nums=[ev]), S('s2', 'Decommissioning', 2, 'computation', 'present value|decommission', nums=[dec]), S('s3', 'Unwinding', 2, 'computation', 'unwinding|finance', nums=[unw])],
          ['Explain expected value.'], ['Using the most likely outcome for a population.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Net fulfilment cost', 2, 'computation', 'fulfil', nums=[fulfil]), S('s2', 'Lower of', 2, 'computation', 'lower', nums=[prov]), S('s3', 'Conclusion', 1, 'concept', 'onerous')],
          ['Compare both routes.'], ['Providing the full purchase cost.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'State the recognition criteria for a provision.', 'A present obligation from a past event, a probable outflow of resources, and a reliable estimate of the amount.',
          [P('p1', 'Present obligation and past event', 5, 'obligation|past'), P('p2', 'Probable and reliable estimate', 5, 'probable|reliable')], 'c1'),
        V('v2', 'What is a constructive obligation?', 'An obligation arising from an entity\'s established practice, published policy or specific statement that creates a valid expectation in others.',
          [P('p1', 'Practice or policy', 5, 'practice|policy'), P('p2', 'Valid expectation', 5, 'expectation')], 'c1'),
        V('v3', 'How are contingent liabilities treated?', 'They are disclosed in the notes unless the possibility of outflow is remote, and are recognised as provisions once outflow becomes probable.',
          [P('p1', 'Disclosed', 5, 'disclos'), P('p2', 'Remote exception', 5, 'remote')], 'c3'),
        V('v4', 'What is an onerous contract?', 'A contract whose unavoidable costs of meeting the obligations exceed the economic benefits expected under it.',
          [P('p1', 'Unavoidable costs', 5, 'unavoidable'), P('p2', 'Exceed benefits', 5, 'exceed')], 'c4'),
        V('v5', 'When is a restructuring provision recognised?', 'When there is a detailed formal plan and those affected have a valid expectation that it will be carried out, through starting it or announcing it.',
          [P('p1', 'Detailed formal plan', 5, 'formal plan|detailed'), P('p2', 'Valid expectation', 5, 'expectation')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Coastal Chemicals Ltd.', 'difficulty': 'moderate',
              'case': 'Coastal Chemicals Ltd. faces: (1) a lawsuit where lawyers say loss is probable, best estimate ₹60 lakh, with insurance cover of ₹25 lakh that the insurer has accepted in writing; (2) a new law requiring smoke filters by next year, not yet fitted; (3) a claim it has filed against a supplier which it will probably win, worth ₹15 lakh; (4) expected operating losses of ₹40 lakh next year.',
              'mcqs': [
                  M('k1a', 'Provision for the lawsuit (₹ lakh):', ['60', '35', '25', 'Nil'], 0,
                    'Provision at gross best estimate; the accepted reimbursement is a separate asset. In practice: do not net.', 'moderate', check=60, topic=T2),
                  M('k1b', 'The filter requirement at year end creates:', ['No provision, as the entity can avoid it by changing operations', 'A provision', 'A contingent asset', 'An onerous contract'], 0,
                    'No obligating event has occurred yet. In practice: penalties for non-compliance may differ.', 'moderate', topic=T1),
                  M('k1c', 'The supplier claim is:', ['A contingent asset disclosed in notes', 'Recognised as income', 'Ignored entirely', 'A provision'], 0,
                    'Probable inflow — disclose only. In practice: recognise once virtually certain.', 'core', topic=T3),
                  M('k1d', 'The expected operating losses are:', ['Not provided for', 'Provided at ₹40 lakh', 'Disclosed as contingent liability', 'Recognised in OCI'], 0,
                    'No present obligation. In practice: impairment test instead.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch06', 2, 'Ind AS 37 "Provisions, Contingent Liabilities and Contingent Assets"',
                ['Apply the recognition criteria for provisions.',
                 'Measure provisions using best estimate, expected value and discounting.',
                 'Distinguish contingent liabilities and contingent assets.',
                 'Apply the rules to onerous contracts, restructurings and future losses.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['fin-p1-ch06-u01'],
                 'exam_tip': 'Start every answer by naming the obligating event — if there isn\'t one, there is no provision.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Provision: obligation + probable outflow + reliable estimate.',
                             'Best estimate; expected value for populations.',
                             'Discount if material; unwinding is finance cost.',
                             'Contingent liability: disclose unless remote.',
                             'Contingent asset: recognise only when virtually certain.'],
                 'remember': ['No provision for future operating losses.'],
                 'traps': ['Netting reimbursements against the provision.']},
                [('Probable', 'Provide'), ('Possible', 'Disclose'), ('Remote', 'Nothing'), ('Onerous', 'Lower of fulfil or exit')],
                viva, cases)
