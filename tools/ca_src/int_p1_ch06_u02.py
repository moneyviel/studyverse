"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 6 Unit 2 — AS 29 (Revised) Provisions, Contingent Liabilities and Contingent Assets.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch06-u02'
T1 = 'Provisions, liabilities and contingencies — the definitions'
T2 = 'When to recognise a provision'
T3 = 'Contingent liabilities and contingent assets'
T4 = 'Measuring provisions; reimbursements; changes and use'
T5 = 'Future losses and restructuring'


def build():
    ck = Checks()
    per = ck.add('15/100*500+5/100*2000', 'Expected repair cost per unit sold (₹)')
    prov = ck.add('10000*175', 'Warranty provision (₹)')
    i1 = {'id': 'i1', 'title': 'Warranty on 10,000 units', 'difficulty': 'core', 'minutes': 6,
          'q': 'Raghav Appliances Ltd. sold 10,000 mixers with a one-year warranty. Past data: 80% need no repair, 15% need minor repairs costing ₹500 and 5% need major repairs costing ₹2,000. Compute the warranty provision.',
          'solution': [table(['Outcome', 'Probability', 'Cost ₹', 'Weighted ₹'], [
              ['No repair', '80%', '0', '0'],
              ['Minor repair', '15%', '500', '75'],
              ['Major repair', '5%', '2,000', '100'],
              ['Expected cost per unit', '', '', R(per)],
              ['Provision for 10,000 units', '', '', inr(prov)]], title='Expected value for a large population')],
          'checks': list(ck)}

    ck2 = Checks()
    net = ck2.add('1200000-800000', 'Net charge to profit and loss (₹)')
    i2 = {'id': 'i2', 'title': 'A claim covered by insurance', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'A customer sued Chhaya Chemicals Ltd. for damage caused by a leak. Lawyers say the company will probably lose; the best estimate of damages is ₹12,00,000. The insurer has accepted the claim in writing for ₹8,00,000. Show the accounting.',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['Provision for damages', 'Liability', inr(1200000)],
              ['Reimbursement from insurer', 'Separate asset — virtually certain, not above the provision', inr(800000)],
              ['Charge to profit and loss', 'May be shown net of the reimbursement', inr(net)]], title='Provision with reimbursement'),
              note('The provision and the reimbursement are not netted in the balance sheet.')],
          'checks': list(ck2)}

    tbl = table(['Situation', 'Treatment'], [
        ['Present obligation; outflow probable; reliable estimate', 'Recognise a provision'],
        ['Possible obligation, or present obligation where outflow is not probable or cannot be estimated reliably', 'Disclose a contingent liability'],
        ['Outflow remote', 'No disclosure'],
        ['Inflow virtually certain', 'Recognise the asset (it is no longer contingent)'],
        ['Inflow probable but not virtually certain', 'Do not recognise; mention in the Board\'s (approving authority\'s) report, not the financial statements'],
        ['Inflow not probable', 'Nothing']], title='Decision table')

    concepts = [
        C('c1', T1, [
            'A provision is a liability whose amount can be measured only with substantial estimation. A liability is a present obligation from past events whose settlement is expected to cause an outflow of resources.',
            'An obligating event creates an obligation that leaves the enterprise no realistic alternative to settling it.',
            'A contingent liability is either a possible obligation from past events whose existence will be confirmed only by uncertain future events outside the enterprise\'s full control, or a present obligation not recognised because outflow is not probable or cannot be estimated reliably.',
            'A contingent asset is a possible asset from past events whose existence depends on uncertain future events outside the enterprise\'s full control.',
            'AS 29 does not cover financial instruments at fair value, executory contracts (unless onerous), insurance contracts with policyholders, or matters dealt with by other standards (AS 7, AS 9, AS 15, AS 19, AS 22).'],
          'A provision is a real debt of uncertain size; a contingency is a "maybe".',
          'Trade creditors are liabilities, a warranty is a provision, and a court case the company will probably win is a contingent liability.',
          blocks=[tbl]),
        C('c2', T2, [
            'A provision is recognised when all three hold: a present obligation exists as a result of a past event; an outflow of resources is probable; and a reliable estimate can be made.',
            'Present obligation: if, on all available evidence (including expert opinion), it is more likely than not that an obligation exists at the balance sheet date.',
            'Only obligations existing independently of the enterprise\'s future actions qualify — such as fines or clean-up costs for environmental damage already caused. Costs needed only to operate in future (such as fitting smoke filters) are not provided for.',
            'Probable means more likely than not. For many similar obligations (warranties), probability is assessed for the class as a whole. A reliable estimate is almost always possible; in the extremely rare case it is not, a contingent liability is disclosed.'],
          'Past event, likely payout, measurable amount — all three, or no provision.',
          'Damage already caused to land creates an obligation once a law requiring clean-up is enacted or virtually certain to be enacted.'),
        C('c3', T3, [
            'Contingent liabilities are not recognised. They are disclosed unless the possibility of outflow is remote, and are reassessed continually; if an outflow becomes probable, a provision is recognised in that period.',
            'Contingent assets are not recognised because that might record income that may never be realised. When realisation becomes virtually certain, the asset is no longer contingent and is recognised.',
            'Revised AS 29 keeps contingent assets out of the financial statements altogether; they are usually mentioned in the report of the approving authority (the Board for a company) when an inflow is probable.'],
          'Disclose the possible debts; keep quiet about possible gains until they are almost sure.',
          'A pending claim against a supplier, likely but uncertain, appears in the directors\' report, not in the notes.'),
        C('c4', T4, [
            'A provision is measured at the best estimate of the expenditure needed to settle the obligation at the balance sheet date, based on management judgement, experience and, where needed, expert reports.',
            'For a large population of items, the expected value (weighting outcomes by probability) is used; for a single obligation, the most likely outcome, adjusted if other outcomes are mostly higher or lower.',
            'Provisions are not discounted, except decommissioning, restoration and similar liabilities recognised in the cost of PPE (pre-tax rate). Future events such as new technology or legislation are reflected only with sufficient objective evidence; expected gains on disposal of assets are ignored.',
            'Reimbursements (insurance, indemnities, supplier warranties) are recognised as a separate asset only when virtually certain, and not above the provision; in profit and loss the expense may be shown net.',
            'Provisions are reviewed at each balance sheet date and reversed if an outflow is no longer probable. A provision is used only for the expenditure for which it was originally recognised.'],
          'Estimate the best settlement amount today, and do not offset hoped-for recoveries unless they are virtually certain.',
          'A provision made for a lawsuit cannot be used to absorb an unrelated repair bill.'),
        C('c5', T5, [
            'Losses expected from future trading are never provided for, since no present obligation exists yet. An expectation of losses may indicate impairment under AS 28.',
            'Restructuring includes selling or ending a business line, closing locations, changing management structure, or reorganising operations fundamentally.',
            'A restructuring provision is recognised only when the general criteria are met — there is a detailed formal plan, and those affected have been given a valid reason to expect it to happen (for example by starting implementation or announcing main features). A board decision alone is not enough. No obligation arises on sale of an operation until there is a binding sale agreement.',
            'The provision includes only direct expenditure that is necessarily entailed and not associated with ongoing activities. It excludes retraining or relocating continuing staff, marketing, and investment in new systems and distribution networks.'],
          'Provide for the cost of leaving the past behind, not for running the future.',
          'Redundancy pay for closing a plant is provided; training staff for the new plant is not.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Litigation and claims review', 'role': 'Audit assistant',
             'situation': 'A client has five pending cases, one insurance claim and a planned plant closure.',
             'steps': ['Get legal opinions on each case.', 'Classify each as provision, contingent liability or remote.', 'Recognise reimbursement only if virtually certain.', 'Test the closure for a detailed plan and valid expectation.'],
             'takeaway': 'Evidence on probability and obligation drives the classification.'}]

    mcqs = [
        Q('m1', 'A provision is recognised when there is a present obligation from a past event, a probable outflow and:', ['A reliable estimate of the amount', 'Board approval', 'A written contract', 'Cash available to pay'], 0,
          'AS 29 requires all three conditions: present obligation from a past event, probable outflow of resources and a reliable estimate. Board approval or a contract is not itself required. In practice: document each condition.', 'c2', T2),
        Q('m2', '"Probable" in AS 29 means:', ['More likely than not', 'Virtually certain', 'Possible', 'Remote'], 0,
          'An outflow is regarded as probable if the event is more likely than not to occur, i.e. the probability is greater than it is not. Virtually certain is a much higher threshold used for assets. In practice: weigh the evidence.', 'c2', T2),
        Q('m3', 'A contingent liability where the possibility of outflow is remote is:', ['Not disclosed', 'Disclosed in notes', 'Provided for', 'Shown as a liability'], 0,
          'Contingent liabilities are disclosed unless the possibility of an outflow is remote; remote contingencies need neither provision nor disclosure. In practice: reassess every year.', 'c3', T3),
        Q('m4', 'Under revised AS 29, a contingent asset where an inflow is probable is:', ['Not disclosed in the financial statements but usually mentioned in the Board\'s report', 'Recognised as an asset', 'Disclosed in the notes', 'Netted against provisions'], 0,
          'Revised AS 29 states that contingent assets are neither recognised nor disclosed in the financial statements; where an inflow is probable they are usually disclosed in the approving authority\'s report. In practice: recognise once virtually certain.', 'c3', T3),
        Q('m5', 'Provisions under AS 29 are generally:', ['Not discounted, except for decommissioning-type liabilities included in PPE', 'Always discounted', 'Discounted at the bank rate', 'Measured at face value of claims'], 0,
          'Revised AS 29 states that provisions are not discounted, except decommissioning, restoration and similar liabilities recognised as part of the cost of PPE, which use a pre-tax discount rate. In practice: check for site restoration duties.', 'c4', T4),
        Q('m6', 'For a warranty covering many similar products, the provision is measured using:', ['Expected value', 'The most likely single outcome', 'The worst possible outcome', 'Nil until claims arrive'], 0,
          'For a large population of items, the obligation is estimated by weighting all possible outcomes by their probabilities — the expected value method. A single obligation uses the most likely outcome. In practice: use past claim data.', 'c4', T4),
        Q('m7', 'A reimbursement expected from an insurer is recognised as an asset when:', ['Its receipt is virtually certain', 'It is probable', 'The claim is filed', 'Never'], 0,
          'AS 29 recognises reimbursements only when it is virtually certain that they will be received if the obligation is settled, as a separate asset not exceeding the provision. In practice: get written acceptance.', 'c4', T4),
        Q('m8', 'A provision for expected operating losses of the next year is:', ['Not allowed', 'Required', 'Allowed if material', 'Allowed for listed companies'], 0,
          'Losses expected from future trading are not present obligations and fail the recognition tests, so nothing is provided. The expectation may signal impairment under AS 28. In practice: test related assets instead.', 'c5', T5),
        Q('m9', 'Which cost is included in a restructuring provision?', ['Redundancy payments to employees whose jobs end', 'Retraining continuing staff', 'Marketing the reorganised business', 'New IT systems'], 0,
          'Only direct costs necessarily entailed by the restructuring and not linked to ongoing activities are included, such as redundancy payments. Costs of the future business are excluded. In practice: separate past-facing and future-facing costs.', 'c5', T5),
        Q('m10', 'A provision made for warranty claims can be used to meet:', ['Only warranty expenditure', 'Any expenditure', 'Bad debts', 'Future losses'], 0,
          'A provision may be used only for the expenditure for which it was originally recognised; setting other costs against it would hide two different events. In practice: track utilisation separately.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Expected value method', 2, 'computation', 'expected', nums=[per]),
           S('s2', 'Provision', 2, 'computation', 'provision', nums=[prov])],
          ['Weight each outcome.'], ['Using only the most likely outcome.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Provision for probable loss', 1.5, 'concept', 'provision'),
           S('s2', 'Reimbursement as separate asset', 1.5, 'concept', 'virtually certain|separate'),
           S('s3', 'Net charge', 1, 'computation', 'net', nums=[net])],
          ['Do not net in the balance sheet.'], ['Recording only ₹4 lakh as provision.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a provision?', 'A liability whose amount involves a high degree of estimation.',
          [P('p1', 'Liability', 5, 'liability'), P('p2', 'Substantial estimation', 5, 'estimat')], 'c1'),
        V('v2', 'What are the three conditions for recognising a provision?', 'A present obligation from a past event, a probable outflow of resources, and a reliable estimate of the amount.',
          [P('p1', 'Present obligation, past event', 4, 'obligation'), P('p2', 'Probable outflow', 3, 'probable'), P('p3', 'Reliable estimate', 3, 'reliable')], 'c2'),
        V('v3', 'How are contingent liabilities treated?', 'They stay off the balance sheet; the notes describe them unless an outflow is remote, and they are reassessed continually.',
          [P('p1', 'Described in notes', 5, 'notes'), P('p2', 'Unless remote', 5, 'remote')], 'c3'),
        V('v4', 'When is a restructuring provision recognised?', 'When the general criteria are met and there is a detailed formal plan and those affected have been led to expect it to go ahead, for example by starting implementation or announcing it.',
          [P('p1', 'Detailed plan', 5, 'detailed|plan'), P('p2', 'Valid expectation', 5, 'expectation|announc')], 'c5'),
        V('v5', 'Are provisions discounted?', 'Generally no; only decommissioning, restoration and similar liabilities included in the cost of PPE are discounted, at a pre-tax rate.',
          [P('p1', 'Generally not', 5, 'generally|only'), P('p2', 'Decommissioning exception', 5, 'decommission|restoration')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Vimal Mining Ltd.', 'difficulty': 'moderate',
              'case': 'Vimal Mining Ltd. has: (1) a claim by a contractor for ₹3 crore that lawyers say the company will probably lose, best estimate ₹2.4 crore; (2) a tax demand of ₹1 crore that experts say is unlikely to be upheld; (3) a claim it has filed against an equipment supplier for ₹80 lakh, likely but not certain to succeed.',
              'mcqs': [
                  M('k1a', 'The contractor\'s claim is:', ['A provision of ₹2.4 crore', 'A contingent liability of ₹3 crore', 'Not recognised', 'A provision of ₹3 crore'], 0,
                    'A present obligation exists, outflow is probable and the best estimate is ₹2.4 crore, so a provision at that amount is recognised. The claimed amount is not the measure. In practice: update as the case progresses.', 'core', topic=T4),
                  M('k1b', 'The tax demand is:', ['Disclosed as a contingent liability', 'Provided for', 'Ignored', 'Netted against tax assets'], 0,
                    'An outflow is not probable but not remote either, so the demand is disclosed as a contingent liability without a provision. If it became remote, disclosure would stop. In practice: describe the matter in notes.', 'moderate', topic=T3),
                  M('k1c', 'The claim against the supplier is:', ['Not recognised or disclosed in the statements; mentioned in the Board\'s report', 'Recognised as income', 'Disclosed in notes', 'Netted with the contractor provision'], 0,
                    'It is a contingent asset with a probable inflow; under revised AS 29 it is neither recognised nor disclosed in the financial statements, but usually mentioned in the Board\'s report. In practice: recognise only when virtually certain.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch06', 2, 'AS 29 (Revised) Provisions, Contingent Liabilities and Contingent Assets',
                ['Define provisions, contingent liabilities and contingent assets.',
                 'Apply the recognition criteria for provisions.',
                 'Measure provisions, including reimbursements, and review and use them correctly.',
                 'Apply the rules for future losses and restructuring.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': ['int-p1-ch06-u01'],
                 'exam_tip': 'Use the decision table: obligation → probability → estimate; for assets, ask "virtually certain?".'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Provision: present obligation + probable outflow + reliable estimate.', 'Contingent liability: disclose unless remote.',
                             'Contingent asset: not recognised or disclosed in FS; Board\'s report if probable; recognise when virtually certain.',
                             'Best estimate; expected value for many items; not discounted except decommissioning.', 'Reimbursement only if virtually certain, as separate asset.',
                             'No provision for future operating losses; restructuring needs detailed plan + valid expectation.'],
                 'remember': ['Use a provision only for its original purpose.'],
                 'traps': ['Board approval alone does not create a restructuring obligation.']},
                [('Recognise', 'Obligation + probable + reliable'), ('Contingent liability', 'Disclose unless remote'), ('Reimbursement', 'Virtually certain only')],
                viva, cases)
