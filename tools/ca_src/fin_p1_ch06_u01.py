"""CA Final · Paper 1 Financial Reporting · Chapter 6 Unit 1 Ind AS 19 Employee Benefits.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch06-u01'
T1 = 'Short-term and other long-term benefits'
T2 = 'Defined contribution versus defined benefit plans'
T3 = 'Measuring defined benefit cost: P&L and OCI'
T4 = 'Termination benefits and the asset ceiling'


def build():
    ck = Checks()
    ni = ck.add('(500-420)*0.08', 'Net interest (₹ lakh)')
    pl = ck.add('40+(500-420)*0.08', 'Charge to profit or loss (₹ lakh)')
    dbo_loss = ck.add('560-(500+40+500*0.08-30)', 'Actuarial loss on obligation (₹ lakh)')
    pa_loss = ck.add('(420+420*0.08+50-30)-470', 'Return on assets below interest income (₹ lakh)')
    oci = ck.add('560-(500+40+500*0.08-30)+(420+420*0.08+50-30)-470', 'Remeasurement loss in OCI (₹ lakh)')
    net = ck.add('560-470', 'Closing net defined benefit liability (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'A gratuity plan for one year', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Sigma Ltd.\'s gratuity plan: opening obligation ₹500 lakh, opening plan assets ₹420 lakh, discount rate 8%. Current service cost ₹40 lakh; employer contributions ₹50 lakh; benefits paid from the fund ₹30 lakh. Actuarial valuation at year end: obligation ₹560 lakh, plan assets ₹470 lakh. Compute amounts in profit or loss, OCI and the closing net liability.',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Net interest', '(500 − 420) × 8%', inr(ni)],
              ['Profit or loss', 'Service cost 40 + net interest', inr(pl)],
              ['Expected obligation', '500 + 40 + 40 − 30 = 550; actual 560', inr(dbo_loss)],
              ['Expected assets', '420 + 33.6 + 50 − 30 = 473.6; actual 470', inr(pa_loss)],
              ['OCI remeasurement loss', '10 + 3.6', inr(oci)],
              ['Closing net liability', '560 − 470 (check: 80 + 46.4 + 13.6 − 50)', inr(net)]], title='Ind AS 19 defined benefit')],
          'checks': list(ck)}

    ck2 = Checks()
    acc = ck2.add('200*0.05*1000/100000', 'Leave accrual (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Unused leave that carries forward', 'difficulty': 'core', 'minutes': 5,
          'q': '200 employees each have 5 days of unused casual leave that carries forward for one year. Experience shows only 5% of employees will use their carried-forward days (all 5 days each); the rest will lapse. One day of leave costs ₹1,000. Compute the accrual for accumulating paid absences.',
          'solution': [table(['Item', 'Working', 'Amount'], [
              ['Employees expected to use', '200 × 5% = 10', '10'],
              ['Days expected to be used', '10 × 5', '50'],
              ['Accrual', '50 days × ₹1,000 = ₹50,000', inr(acc) + ' lakh']], title='Accumulating absences')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Employee benefits are all forms of payment given by an entity in exchange for service or for ending employment. Short-term benefits — wages, social security contributions, paid leave and bonuses payable within twelve months after the period end — are recognised undiscounted as the service is rendered.',
            'Paid absences: accumulating absences (carried forward) are accrued when service increases the entitlement, measured at the additional amount expected to be paid; non-accumulating absences (e.g. sick leave that lapses) are recognised only when the absence occurs.',
            'Profit-sharing and bonuses are recognised when there is a present legal or constructive obligation and a reliable estimate. Other long-term benefits (e.g. long-service leave) use a simplified defined benefit method: all remeasurements go to profit or loss.'],
          'Pay for this year\'s service belongs to this year\'s expense.',
          'Unused leave that carries forward is a liability only to the extent it will actually be used.'),
        C('c2', T2, [
            'Post-employment benefits (pensions, gratuity, post-retirement medical) are either defined contribution or defined benefit plans.',
            'In a defined contribution plan, the entity pays fixed contributions to a separate fund and has no further obligation; actuarial and investment risk sits with employees. Contributions are expensed as service is rendered (e.g. provident fund via a government scheme).',
            'In a defined benefit plan, the entity bears the risk that benefits cost more than expected. Multi-employer and state plans are classified by their terms; insured benefits are defined contribution only if the entity has no obligation beyond paying premiums.'],
          'Who carries the risk decides the plan type.',
          'Gratuity under the Payment of Gratuity Act is a defined benefit.'),
        C('c3', T3, [
            'The defined benefit obligation is measured using the projected unit credit method: each period of service gives rise to an extra unit of benefit, measured separately. Actuarial assumptions are unbiased and mutually compatible; the discount rate reflects market yields on high-quality corporate bonds (or government bonds where no deep market exists).',
            'Plan assets are measured at fair value. The balance sheet shows the net defined benefit liability (asset): obligation minus plan assets, subject to the asset ceiling.',
            'Defined benefit cost has three parts: service cost (current, past service cost and settlement gains or losses) and net interest go to profit or loss; remeasurements (actuarial gains and losses, return on plan assets excluding net interest, change in ceiling effect) go to OCI and are never reclassified to profit or loss.'],
          'Service and interest in P&L; surprises in OCI.',
          'Actual returns below the discount rate create an OCI loss.'),
        C('c4', T4, [
            'Termination benefits arise from the entity\'s decision to end employment or an employee\'s acceptance of an offer. They are recognised at the earlier of when the entity can no longer withdraw the offer and when it recognises related restructuring costs under Ind AS 37.',
            'They are measured by their nature: short-term if settled within twelve months, otherwise as other long-term benefits. Benefits conditional on future service are not termination benefits.',
            'Asset ceiling: a net defined benefit asset is limited to the present value of economic benefits available as refunds or reductions in future contributions. Past service cost from amendments or curtailments is recognised immediately in profit or loss.'],
          'A surplus is an asset only if the entity can get value from it.',
          'A voluntary retirement scheme is recognised once offers cannot be withdrawn.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Reviewing the actuary\'s report', 'role': 'Finance manager',
             'situation': 'The actuary sends gratuity and leave encashment valuations at year end.',
             'steps': ['Check assumptions: discount rate, salary escalation, attrition.', 'Split cost into service, net interest and remeasurement.', 'Book remeasurements in OCI for gratuity, in P&L for leave.', 'Reconcile opening to closing net liability.'],
             'takeaway': 'The reconciliation proves the numbers before they reach the accounts.'}]

    mcqs = [
        Q('m1', 'Remeasurements of a net defined benefit liability are recognised in:', ['Other comprehensive income', 'Profit or loss', 'Retained earnings directly without OCI', 'Revenue'], 0,
          'They are never reclassified. In practice: transfer within equity is allowed.', 'c3', T3),
        Q('m2', 'The method used to measure a defined benefit obligation is:', ['Projected unit credit method', 'Straight-line method', 'Accrued benefit valuation', 'Pay-as-you-go'], 0,
          'Each service year adds a unit of benefit. In practice: actuaries apply it.', 'c3', T3),
        Q('m3', 'In a defined contribution plan, investment risk falls on:', ['Employees', 'The employer', 'The government', 'The actuary'], 0,
          'The employer only pays fixed contributions. In practice: expense as service is given.', 'c2', T2),
        Q('m4', 'Non-accumulating paid absences are recognised:', ['When the absence occurs', 'When service is rendered', 'At year end', 'Never'], 0,
          'No entitlement builds up. In practice: sick leave that lapses.', 'c1', T1),
        Q('m5', 'Remeasurements on other long-term benefits such as long-service leave go to:', ['Profit or loss', 'OCI', 'Equity', 'Capital reserve'], 0,
          'The simplified model puts everything in profit or loss. In practice: leave encashment.', 'c1', T1),
        Q('m6', 'Past service cost from a plan amendment is recognised:', ['Immediately in profit or loss', 'Over remaining service', 'In OCI', 'Over five years'], 0,
          'No spreading under Ind AS 19. In practice: note the amendment date.', 'c4', T4),
        Q('m7', 'The discount rate for the obligation reflects:', ['Market yields on high-quality corporate bonds or government bonds', 'The entity\'s borrowing rate', 'Expected return on plan assets', 'Inflation'], 0,
          'Government bond yields are used in India where needed. In practice: match currency and term.', 'c3', T3),
        Q('m8', 'A net defined benefit asset is limited by:', ['The asset ceiling', 'The plan assets value', 'The obligation', 'Nothing'], 0,
          'Only available refunds or contribution reductions count. In practice: changes go to OCI.', 'c4', T4),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Net interest', 1.5, 'computation', 'interest', nums=[ni]), S('s2', 'P&L', 1.5, 'computation', 'profit or loss', nums=[pl]), S('s3', 'OCI', 3, 'computation', 'oci', nums=[oci]), S('s4', 'Closing', 2, 'computation', 'closing', nums=[net])],
          ['Reconcile the net liability.'], ['Using expected return on assets.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Expected use', 2, 'computation', 'expected', nums=[50]), S('s2', 'Accrual', 2, 'computation', 'accrual', nums=[acc])],
          ['Use expected usage.'], ['Accruing all leave.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Distinguish defined contribution and defined benefit plans.', 'In a defined contribution plan the employer pays fixed contributions and employees bear the risk; in a defined benefit plan the employer bears actuarial and investment risk.',
          [P('p1', 'Fixed contributions', 5, 'fixed'), P('p2', 'Employer risk', 5, 'employer')], 'c2'),
        V('v2', 'What are the components of defined benefit cost?', 'Service cost and net interest, recognised in profit or loss, and remeasurements, recognised in OCI.',
          [P('p1', 'Service and interest', 5, 'service|interest'), P('p2', 'Remeasurements in OCI', 5, 'oci')], 'c3'),
        V('v3', 'When are termination benefits recognised?', 'At the earlier of when the entity loses the ability to withdraw the offer and when it recognises related restructuring costs.',
          [P('p1', 'Withdraw offer', 6, 'withdraw'), P('p2', 'Restructuring', 4, 'restructuring')], 'c4'),
        V('v4', 'How are accumulating paid absences measured?', 'At the additional amount expected to be paid because of the unused entitlement built up at the period end.',
          [P('p1', 'Expected additional amount', 6, 'expected'), P('p2', 'Unused entitlement', 4, 'unused')], 'c1'),
        V('v5', 'What is the asset ceiling?', 'The present value of economic benefits available as refunds or reductions in future contributions, which caps a net defined benefit asset.',
          [P('p1', 'Refunds or reductions', 6, 'refund|reduction'), P('p2', 'Caps the asset', 4, 'cap')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Tejas Motors Ltd.', 'difficulty': 'moderate',
              'case': 'Tejas Motors Ltd. contributes 12% of salary to the government provident fund, runs a funded gratuity plan, and pays long-service awards after 15 years. It amends the gratuity plan, increasing benefits for past service by ₹18 lakh. The gratuity fund earned less than the discount rate this year.',
              'mcqs': [
                  M('k1a', 'The provident fund contribution is a:', ['Defined contribution plan expense', 'Defined benefit obligation', 'Termination benefit', 'Long-term benefit'], 0,
                    'Fixed contribution to a state scheme. In practice: expense monthly.', 'core', topic=T2),
                  M('k1b', 'The ₹18 lakh past service cost is recognised:', ['Immediately in profit or loss', 'In OCI', 'Over vesting period', 'Not at all'], 0,
                    'Recognised when the amendment occurs. In practice: part of service cost.', 'core', topic=T4),
                  M('k1c', 'The shortfall in fund returns against the discount rate goes to:', ['OCI as a remeasurement', 'Profit or loss', 'Retained earnings directly', 'Revenue'], 0,
                    'Return on plan assets excluding net interest is a remeasurement. In practice: never recycled.', 'core', topic=T3),
                  M('k1d', 'Actuarial gains on long-service awards are recognised in:', ['Profit or loss', 'OCI', 'Capital reserve', 'Equity directly'], 0,
                    'Other long-term benefits use the simplified model. In practice: different from gratuity.', 'moderate', topic=T1),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch06', 1, 'Ind AS 19 "Employee Benefits"',
                ['Account for short-term and other long-term employee benefits.',
                 'Distinguish defined contribution and defined benefit plans.',
                 'Measure defined benefit cost and split it between profit or loss and OCI.',
                 'Recognise termination benefits and apply the asset ceiling.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': ['fin-p1-ch05-u08'],
                 'exam_tip': 'Build two columns — obligation and plan assets — and reconcile opening to closing; the balancing figures are remeasurements.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Short-term: undiscounted as service is given.',
                             'DC: expense contributions; DB: employer bears risk.',
                             'DBO via projected unit credit; assets at fair value.',
                             'P&L: service cost + net interest; OCI: remeasurements.',
                             'Termination: when offer cannot be withdrawn.'],
                 'remember': ['Long-term benefits: all remeasurements in P&L.'],
                 'traps': ['Using expected return on assets instead of the discount rate.']},
                [('Method', 'Projected unit credit'), ('Net interest', 'Net liability × discount rate'), ('OCI', 'Remeasurements'), ('Past service cost', 'Immediate P&L')],
                viva, cases)
