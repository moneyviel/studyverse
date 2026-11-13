"""CA Final · Paper 1 Financial Reporting · Chapter 10 Unit 3 Ind AS 102 Share-based Payment.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch10-u03'
T1 = 'Scope and types of share-based payment'
T2 = 'Equity-settled: grant-date fair value and vesting'
T3 = 'Cash-settled and choice-of-settlement plans'
T4 = 'Modifications, cancellations and group plans'


def build():
    ck = Checks()
    y1 = ck.add('90*100*30*1/3', 'Cumulative expense year 1 (₹)')
    y2c = ck.add('85*100*30*2/3', 'Cumulative expense year 2 (₹)')
    y2 = ck.add('85*100*30*2/3-90*100*30*1/3', 'Expense year 2 (₹)')
    y3 = ck.add('88*100*30-85*100*30*2/3', 'Expense year 3 (₹)')
    i1 = {'id': 'i1', 'title': 'An employee stock option plan', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Lotus Tech grants 100 options each to 100 employees, vesting after 3 years of service. Grant-date fair value per option is ₹30. Expected employees at vesting: 90 (end of year 1), 85 (end of year 2); actually 88 vest. Compute the expense each year (credit to equity).',
          'solution': [table(['Year', 'Working', 'Expense ₹'], [
              ['1', '90 × 100 × 30 × 1/3 = ' + inr(y1), inr(y1)],
              ['2', '85 × 100 × 30 × 2/3 = ' + inr(y2c) + ' − ' + inr(y1), inr(y2)],
              ['3', '88 × 100 × 30 = 2,64,000 − ' + inr(y2c), inr(y3)]], title='Equity-settled — true-up for service conditions')],
          'checks': list(ck)}

    ck2 = Checks()
    l1 = ck2.add('50*100*12*1/2', 'Liability at end of year 1 (₹)')
    l2 = ck2.add('48*100*15', 'Liability at end of year 2 (₹)')
    e2 = ck2.add('48*100*15-50*100*12*1/2', 'Expense year 2 (₹)')
    i2 = {'id': 'i2', 'title': 'Share appreciation rights', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Lotus Tech grants 100 cash-settled share appreciation rights each to 50 managers, vesting after 2 years. Fair value per SAR: ₹12 at end of year 1, ₹15 at end of year 2. All 50 were expected to stay at year 1; 48 actually vest. Compute the liability and expense.',
          'solution': [table(['Year', 'Working', '₹'], [
              ['1 — liability', '50 × 100 × 12 × 1/2', inr(l1)],
              ['2 — liability', '48 × 100 × 15', inr(l2)],
              ['2 — expense', inr(l2) + ' − ' + inr(l1), inr(e2)]], title='Cash-settled — remeasure each date')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A share-based payment arrangement gives a counterparty (employee or supplier) the right to receive equity instruments of the entity, or cash or assets based on the price of those instruments, provided vesting conditions are met.',
            'Three types: equity-settled (entity issues shares or options), cash-settled (entity pays cash based on share price, e.g. share appreciation rights), and those with a choice of settlement. Transactions where the group settles for a subsidiary\'s employees are also in scope.',
            'Excluded: transactions with shareholders acting as shareholders (rights issues), shares issued in a business combination for control (Ind AS 103), and contracts within Ind AS 32/109. Goods or services received are recognised when received; expense arises unless they qualify as assets.'],
          'If the payment is in, or measured by, the entity\'s shares, Ind AS 102 applies.',
          'ESOPs and phantom share plans are both share-based payments.'),
        C('c2', T2, [
            'Equity-settled transactions are measured at the fair value of goods or services received, if reliably measurable; for employees, by reference to the fair value of equity instruments granted at grant date (using market prices or an option pricing model). The credit goes to equity.',
            'If instruments vest immediately, the expense is recognised in full at grant. Otherwise, it is recognised over the vesting period, based on the best estimate of instruments expected to vest. Service conditions and non-market performance conditions are trued up to actual outcomes; market conditions and non-vesting conditions are built into grant-date fair value and not trued up.',
            'After vesting, no reversal is made if options lapse unexercised, though a transfer within equity is permitted.'],
          'Fix the price at grant date; adjust only the number expected to vest.',
          'A share price target missed does not reverse the expense if service was given.'),
        C('c3', T3, [
            'Cash-settled transactions create a liability measured at fair value initially and remeasured at each reporting date and at settlement, with changes in profit or loss. Vesting conditions other than market conditions are reflected in the number of awards expected to vest.',
            'Where the counterparty has a choice of settlement, the entity has granted a compound instrument: a debt component (cash right) and an equity component. Where the entity has the choice, it accounts as cash-settled if it has a present obligation to pay cash (e.g. past practice), otherwise as equity-settled.',
            'Net settlement for withholding tax obligations is classified wholly as equity-settled if it would otherwise have been.'],
          'Cash plans are remeasured every year end; equity plans are not.',
          'SAR liability grows as the share price rises.'),
        C('c4', T4, [
            'Modifications: at minimum, the grant-date fair value continues to be recognised. If modification increases total fair value (e.g. repricing), the incremental fair value is recognised over the remaining vesting period. Decreases are ignored.',
            'Cancellation or settlement during vesting is an acceleration of vesting: the remaining amount is recognised immediately. Payments on settlement up to fair value at that date are a repurchase of equity; any excess is an expense. Replacement awards are treated as modifications.',
            'Group plans: the subsidiary receiving services accounts as equity-settled if it has no obligation to settle or the award is in its own shares; otherwise cash-settled. The parent recognises an increase in investment in the subsidiary.'],
          'Modifications can only add cost, never remove it.',
          'Repricing underwater options adds the incremental value going forward.'),
    ]

    jobs = [{'id': 'j1', 'title': 'ESOP accounting cycle', 'role': 'Payroll and reporting accountant',
             'situation': 'A listed company runs an ESOP and a SAR plan.',
             'steps': ['Obtain grant-date valuations.', 'Estimate forfeitures each year end.', 'Remeasure SAR liabilities at fair value.', 'Record modifications and exercise entries.'],
             'takeaway': 'Equity-settled uses fixed grant value; cash-settled floats with the share price.'}]

    mcqs = [
        Q('m1', 'Equity-settled awards to employees are measured at fair value at:', ['Grant date', 'Vesting date', 'Exercise date', 'Each reporting date'], 0,
          'Fixed at grant. In practice: use an option pricing model.', 'c2', T2),
        Q('m2', 'Cash-settled share appreciation rights are measured:', ['At fair value at each reporting date until settled', 'At grant date only', 'At intrinsic value at grant', 'At cost'], 0,
          'They are liabilities. In practice: changes go to profit or loss.', 'c3', T3),
        Q('m3', 'Market performance conditions are:', ['Included in grant-date fair value and not trued up', 'Trued up each year', 'Ignored', 'Recognised in OCI'], 0,
          'Only non-market conditions are trued up. In practice: share price targets.', 'c2', T2),
        Q('m4', 'Options that lapse unexercised after vesting:', ['Do not reverse the expense', 'Reverse the expense', 'Create income', 'Increase liabilities'], 0,
          'Services were received. In practice: transfer within equity allowed.', 'c2', T2),
        Q('m5', 'Cancellation of an award during the vesting period results in:', ['Immediate recognition of the remaining expense', 'Reversal of expense', 'No entry', 'OCI entry'], 0,
          'Treated as acceleration of vesting. In practice: excess payment is expense.', 'c4', T4),
        Q('m6', 'A modification that reduces fair value is:', ['Ignored — original cost continues', 'Recognised as income', 'Reversed', 'Charged to OCI'], 0,
          'Minimum cost is the original grant value. In practice: favourable changes add cost.', 'c4', T4),
        Q('m7', 'If the employee can choose cash or shares, the entity has granted:', ['A compound instrument', 'Only equity', 'Only debt', 'Nothing'], 0,
          'Debt and equity components. In practice: measure the debt first.', 'c3', T3),
        Q('m8', 'Shares issued in a business combination to obtain control are accounted for under:', ['Ind AS 103', 'Ind AS 102', 'Ind AS 32', 'Ind AS 19'], 0,
          'They are consideration, not payment for services. In practice: replacement awards may differ.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Year 1', 2, 'computation', 'year 1|1/3', nums=[y1]), S('s2', 'Year 2', 2, 'computation', 'year 2|2/3', nums=[y2]), S('s3', 'Year 3', 2, 'computation', 'year 3|actual', nums=[y3])],
          ['Show cumulative amounts.'], ['Using year-end fair value.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Year 1 liability', 1.5, 'computation', 'liability', nums=[l1]), S('s2', 'Year 2 liability', 1.5, 'computation', 'liability', nums=[l2]), S('s3', 'Expense', 2, 'computation', 'expense', nums=[e2])],
          ['Remeasure.'], ['Using grant-date value.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Name the types of share-based payment.', 'Equity-settled, cash-settled, and arrangements with a choice of settlement in cash or equity.',
          [P('p1', 'Equity and cash-settled', 6, 'equity-settled|cash-settled'), P('p2', 'Choice', 4, 'choice')], 'c1'),
        V('v2', 'How is the expense for an equity-settled plan spread?', 'Over the vesting period, based on the best estimate of awards expected to vest, trued up for service and non-market conditions.',
          [P('p1', 'Vesting period', 5, 'vesting period'), P('p2', 'True-up', 5, 'trued up|estimate')], 'c2'),
        V('v3', 'How does a cash-settled plan differ?', 'It creates a liability remeasured at fair value at each reporting date and at settlement, with changes in profit or loss.',
          [P('p1', 'Liability', 5, 'liability'), P('p2', 'Remeasured', 5, 'remeasur')], 'c3'),
        V('v4', 'What happens on a beneficial modification?', 'The incremental fair value at the modification date is recognised over the remaining vesting period, in addition to the original cost.',
          [P('p1', 'Incremental fair value', 6, 'incremental'), P('p2', 'Remaining period', 4, 'remaining')], 'c4'),
        V('v5', 'How does a subsidiary account for a parent-granted equity plan?', 'As equity-settled, recognising expense and a capital contribution from the parent.',
          [P('p1', 'Equity-settled', 5, 'equity-settled'), P('p2', 'Contribution from parent', 5, 'contribution')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Prism Software Ltd.', 'difficulty': 'moderate',
              'case': 'Prism Software Ltd. grants 1,000 options to its CTO with a grant-date fair value of ₹50 each, vesting in 2 years if revenue grows 20% (non-market) and the share price reaches ₹500 (market). After year 1 it reprices the options, raising fair value by ₹10 each. At the end of year 2, revenue grew 25% but the share price is ₹450.',
              'mcqs': [
                  M('k1a', 'Expense in year 1 (₹), before repricing:', ['25,000', '50,000', '30,000', 'Nil'], 0,
                    '1,000 × 50 × 1/2. In practice: assumes vesting expected.', 'core', check=25000, topic=T2),
                  M('k1b', 'The repricing adds expense of (₹) over the remaining period:', ['10,000', '60,000', '5,000', 'Nil'], 0,
                    '1,000 × 10 incremental. In practice: spread over year 2.', 'moderate', check=10000, topic=T4),
                  M('k1c', 'The share price target being missed:', ['Does not reverse the expense', 'Reverses all expense', 'Halves the expense', 'Creates a liability'], 0,
                    'Market conditions are not trued up. In practice: service and revenue tests were met.', 'moderate', topic=T2),
                  M('k1d', 'Credit side of the ESOP expense entry is:', ['Equity (share-based payment reserve)', 'Liability', 'Cash', 'Revenue'], 0,
                    'Equity-settled plan. In practice: transfer to share capital on exercise.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch10', 3, 'Ind AS 102 "Share-based Payment"',
                ['Identify share-based payment transactions and their types.',
                 'Measure equity-settled plans at grant-date fair value over the vesting period.',
                 'Account for cash-settled plans and settlement choices.',
                 'Handle modifications, cancellations and group plans.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 35}, 'prereq': ['fin-p1-ch10-u02'],
                 'exam_tip': 'Use the formula: number expected to vest × fair value × elapsed fraction − previous cumulative.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Equity-settled: grant-date fair value; credit equity.',
                             'Spread over vesting; true-up for service and non-market.',
                             'Market conditions in fair value only.',
                             'Cash-settled: liability remeasured each date.',
                             'Modifications add, never reduce, cost.'],
                 'remember': ['No reversal after vesting.'],
                 'traps': ['Truing up market conditions.']},
                [('Equity-settled', 'Grant-date FV'), ('Cash-settled', 'Remeasure'), ('Market condition', 'No true-up'), ('Cancellation', 'Accelerate')],
                viva, cases)
