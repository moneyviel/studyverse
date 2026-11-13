"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 6 Unit 1 — AS 15 Employee Benefits.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch06-u01'
T1 = 'Scope and the four categories of employee benefits'
T2 = 'Short-term benefits, paid absences and bonus'
T3 = 'Defined contribution and defined benefit plans'
T4 = 'Measuring defined benefit cost and liability'
T5 = 'Other long-term and termination benefits'


def build():
    ck = Checks()
    days = ck.add('100*5*80/100', 'Leave days expected to be used from carried-forward balance')
    liab = ck.add('400*2000', 'Liability for accumulating paid leave (₹)')
    i1 = {'id': 'i1', 'title': 'Unused leave at the year end', 'difficulty': 'core', 'minutes': 6,
          'q': 'Pankaj Ltd. lets 100 employees carry forward unused leave for one year (non-vesting). At 31 March each has 5 unused days; experience shows 80% of carried-forward days are actually taken. Average daily pay is ₹2,000. What liability is recognised?',
          'solution': [table(['Step', 'Working', 'Amount'], [
              ['Days expected to be used', '100 × 5 × 80%', R(days)],
              ['Liability', '400 × ₹2,000', inr(liab)]], title='Accumulating compensated absences'),
              note('The leave is accumulating, so the obligation arises as service is rendered — even though it is non-vesting. The expected usage is what is measured. Non-accumulating leave would be expensed only when taken.')],
          'checks': list(ck)}

    ck2 = Checks()
    ic = ck2.add('5000000*8/100', 'Interest cost (₹)')
    er = ck2.add('4000000*9/100', 'Expected return on plan assets (₹)')
    exp = ck2.add('600000+400000-360000+140000', 'Expense for the year (₹)')
    dbo = ck2.add('5000000+600000+400000-300000+140000', 'Closing defined benefit obligation (₹)')
    pa = ck2.add('4000000+360000+700000-300000', 'Closing plan assets (₹)')
    net = ck2.add('5840000-4760000', 'Net liability in balance sheet (₹)')
    i2 = {'id': 'i2', 'title': 'A gratuity plan for the year', 'difficulty': 'hard', 'minutes': 12,
          'q': 'For Anand Ltd.\'s funded gratuity plan: opening obligation ₹50,00,000; opening plan assets ₹40,00,000; current service cost ₹6,00,000; discount rate 8%; expected return on assets 9%; contributions paid ₹7,00,000; benefits paid ₹3,00,000; actuarial loss on the obligation ₹1,40,000 (actual return equals expected). Compute the expense and the closing net liability.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Current service cost', '', inr(600000)],
              ['Interest cost', '8% × 50,00,000', inr(ic)],
              ['Expected return on plan assets', '9% × 40,00,000', f'({inr(er)})'],
              ['Actuarial loss', 'Recognised immediately', inr(140000)],
              ['Expense', '', inr(exp)],
              ['Closing obligation', '50,00,000 + 6,00,000 + 4,00,000 − 3,00,000 + 1,40,000', inr(dbo)],
              ['Closing plan assets', '40,00,000 + 3,60,000 + 7,00,000 − 3,00,000', inr(pa)],
              ['Net liability', '', inr(net)]], title='Defined benefit plan'),
              note('Check: opening net liability ₹10,00,000 + expense ₹7,80,000 − contributions ₹7,00,000 = ₹10,80,000.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Employee benefits are all forms of consideration an enterprise gives in exchange for service rendered by employees, whether under formal plans, laws, industry arrangements or informal practices that create an obligation.',
            'AS 15 has four categories: short-term benefits (due wholly within twelve months after the period in which service is rendered); post-employment benefits (gratuity, pension, provident fund, post-retirement medical care); other long-term benefits (long-service leave, deferred bonus, long-term disability benefits); and termination benefits (payable on ending employment, such as VRS).',
            'The standard covers employers, not the plans themselves, and does not deal with share-based payments.'],
          'Every rupee promised for staff service fits one of four boxes, each with its own rule.',
          'Monthly salary is short-term; gratuity is post-employment; a VRS payout is a termination benefit.'),
        C('c2', T2, [
            'Short-term benefits are recognised as an expense (unless capitalised under another standard) at the undiscounted amount expected to be paid for service rendered in the period, with any unpaid amount as a liability.',
            'Paid absences are accumulating (unused leave can be carried forward) or non-accumulating (lapses). Accumulating absences are recognised as employees render service that increases their entitlement, measured at the extra amount expected to be paid because of the unused entitlement — whether vesting (cash on leaving) or non-vesting. Non-accumulating absences are recognised only when the absence occurs.',
            'Profit-sharing and bonus are recognised when the enterprise has a present obligation (legal or from past practice) and can reliably estimate it. Informal practices can create such an obligation when the enterprise has no realistic alternative but to pay.'],
          'Pay what is due for this year\'s work this year, including leave earned but not yet taken.',
          'A customary Diwali bonus paid every year without fail is provided for even without a written contract.'),
        C('c3', T3, [
            'Defined contribution plans: the enterprise pays fixed contributions into a fund and has no obligation to pay more if the fund falls short. Actuarial and investment risk fall on the employee. The expense is the contribution payable for the period; amounts due beyond twelve months are discounted.',
            'Defined benefit plans: the enterprise promises a level of benefits, so actuarial and investment risk fall on it. Gratuity and pension promising a formula benefit are typical.',
            'Multi-employer and state plans are classified by their terms; insured benefits are treated as defined contribution if the employer has no further obligation.'],
          'In a contribution plan you promise a payment in; in a benefit plan you promise a payment out.',
          'Employer\'s 12% PF contribution to the government fund is a defined contribution; gratuity of 15 days\' salary per year is defined benefit.'),
        C('c4', T4, [
            'The obligation is measured using the projected unit credit method — each period of service gives rise to an extra unit of benefit — with unbiased and mutually compatible actuarial assumptions about mortality, staff turnover, salary growth and so on.',
            'The discount rate comes from current government bond yields (as at the balance sheet date) for a period matching when the benefits will be paid.',
            'The balance sheet shows the present value of the obligation less the fair value of plan assets (adjusted for unrecognised past service cost); any net asset is limited.',
            'The expense comprises current service cost, interest cost, expected return on plan assets, actuarial gains and losses (recognised immediately in profit and loss), past service cost (immediately if vested, otherwise straight-line until vesting) and the effect of curtailments or settlements.'],
          'Value the promise with actuarial tools, net off the fund, and show the gap.',
          'A rise in bond yields lowers the obligation and produces an actuarial gain in profit and loss.'),
        C('c5', T5, [
            'Other long-term employee benefits are measured like defined benefit obligations, but actuarial gains and losses and past service cost are all recognised immediately in profit and loss.',
            'Termination benefits are recognised as a liability and expense only when the enterprise has a present obligation from a past event, an outflow is probable and a reliable estimate can be made. Amounts due beyond twelve months are discounted. For voluntary schemes, measurement is based on the number of employees expected to accept.',
            'Where the number accepting is uncertain, a contingent liability may exist and is disclosed.'],
          'Long-term and exit benefits are provided when they are real obligations, without smoothing.',
          'A VRS offered in March with 60 expected acceptances is provided for on that basis at year end.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end employee benefit provisions', 'role': 'Accounts executive',
             'situation': 'You receive an actuary\'s report for gratuity and leave encashment and HR data on bonus and VRS.',
             'steps': ['Classify each benefit into the four categories.', 'Post the actuarial expense components.', 'Provide for accumulating leave and customary bonus.', 'Check VRS for a present obligation.'],
             'takeaway': 'Classification first, measurement second.'}]

    mcqs = [
        Q('m1', 'Short-term employee benefits are measured at:', ['The undiscounted amount expected to be paid', 'Present value using bond yields', 'Fair value of plan assets', 'Actuarial value'], 0,
          'Because they fall due within twelve months after the period of service, short-term benefits are recognised at the undiscounted amount the enterprise expects to pay in exchange for that service. In practice: no actuary is needed.', 'c2', T2),
        Q('m2', 'Non-accumulating paid absences are recognised:', ['When the absences occur', 'As employees render service', 'At the year end only', 'When the employee retires'], 0,
          'Leave that lapses if not used creates no obligation as service is rendered; the cost is recognised only when the absence actually occurs. Accumulating leave is recognised as service is rendered. In practice: sick leave is often non-accumulating.', 'c2', T2),
        Q('m3', 'In a defined contribution plan, investment risk falls on:', ['The employee', 'The employer', 'The fund manager', 'The government'], 0,
          'The employer\'s obligation is limited to the contributions it agrees to pay, so actuarial and investment risks are borne by employees through the benefits they finally receive. In practice: expense the contribution payable.', 'c3', T3),
        Q('m4', 'The method used to measure a defined benefit obligation is:', ['Projected unit credit method', 'Straight-line method', 'Accumulated benefit method', 'Pay-as-you-go'], 0,
          'AS 15 requires the projected unit credit method, which treats each period of service as earning an extra unit of benefit and measures each unit separately to build up the final obligation. In practice: actuaries apply it.', 'c4', T4),
        Q('m5', 'The discount rate for post-employment obligations is based on:', ['Market yields on government bonds at the balance sheet date', 'The enterprise\'s borrowing rate', 'Expected return on plan assets', 'The RBI repo rate'], 0,
          'AS 15 ties the discount rate to year-end government bond yields whose maturity matches the expected payment dates. In practice: longer obligations use longer bond yields.', 'c4', T4),
        Q('m6', 'Under AS 15, actuarial gains and losses on defined benefit plans are recognised:', ['Immediately in the statement of profit and loss', 'Over the remaining service life', 'In reserves only', 'When benefits are paid'], 0,
          'AS 15 requires actuarial gains and losses to be recognised immediately in profit and loss, which keeps the balance sheet at the full net obligation. In practice: they can make profits volatile.', 'c4', T4),
        Q('m7', 'Current service cost ₹4 lakh; interest cost ₹3 lakh; expected return on assets ₹2.5 lakh; actuarial gain ₹0.5 lakh. Expense:', ['₹4 lakh', '₹5 lakh', '₹10 lakh', '₹4.5 lakh'], 0,
          'Expense = 4 + 3 − 2.5 − 0.5 = ₹4 lakh: service and interest add cost, while expected return and the actuarial gain reduce it. In practice: list components separately in the note.', 'c4', T4, 'moderate', check=4),
        Q('m8', 'Past service cost that has already vested is:', ['Recognised immediately', 'Spread over the remaining service life', 'Ignored', 'Charged to reserves'], 0,
          'Vested past service cost is recognised immediately; non-vested past service cost is recognised on a straight-line basis over the average period until the benefits become vested. In practice: plan amendments trigger this.', 'c4', T4),
        Q('m9', 'Actuarial gains and losses on other long-term benefits such as long-service leave are:', ['Recognised immediately in profit and loss', 'Deferred', 'Ignored', 'Taken to equity'], 0,
          'Other long-term benefits are measured like defined benefit obligations but with a simpler rule: actuarial gains and losses and past service cost are all recognised immediately in profit and loss. In practice: actuarial valuation is still needed.', 'c5', T5),
        Q('m10', 'Termination benefits under a voluntary scheme are measured based on:', ['The number of employees expected to accept the offer', 'All eligible employees', 'Only those who have signed', 'Nil until paid'], 0,
          'Where an offer encourages voluntary separation, AS 15 bases the measurement on how many staff are likely to take up the offer. Uncertainty about numbers may also require a contingent liability disclosure. In practice: use HR estimates.', 'c5', T5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Accumulating leave recognised as service is rendered', 1.5, 'concept', 'accumulating'),
           S('s2', 'Expected usage', 1, 'computation', '80', nums=[days]),
           S('s3', 'Liability', 1.5, 'computation', 'liability', nums=[liab])],
          ['Measure expected use.'], ['Ignoring non-vesting leave.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Expense components', 2, 'computation', 'interest', nums=[ic, er, exp]),
           S('s2', 'Closing obligation', 1.5, 'computation', 'obligation', nums=[dbo]),
           S('s3', 'Closing plan assets', 1.5, 'computation', 'plan assets', nums=[pa]),
           S('s4', 'Net liability', 1, 'computation', 'net', nums=[net])],
          ['Reconcile both sides.'], ['Netting contributions into the expense.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Name the four categories of employee benefits.', 'Short-term benefits, post-employment benefits, other long-term benefits and termination benefits.',
          [P('p1', 'Short-term and post-employment', 5, 'short-term', 'post-employment'), P('p2', 'Long-term and termination', 5, 'long-term', 'termination')], 'c1'),
        V('v2', 'Distinguish defined contribution from defined benefit plans.', 'In a defined contribution plan the employer pays fixed contributions and bears no further risk; in a defined benefit plan the employer promises the benefit and bears actuarial and investment risk.',
          [P('p1', 'Fixed contributions', 5, 'contribution'), P('p2', 'Risk on employer for benefit plans', 5, 'risk')], 'c3'),
        V('v3', 'When is a customary bonus provided for?', 'When the enterprise has a present obligation, legal or arising from past practice with no realistic alternative but to pay, and the amount can be reliably estimated.',
          [P('p1', 'Present obligation from practice', 6, 'practice|obligation'), P('p2', 'Reliable estimate', 4, 'reliab|estimate')], 'c2'),
        V('v4', 'What are the components of defined benefit expense?', 'Current service cost, interest cost, expected return on plan assets, actuarial gains and losses, past service cost and effects of curtailments or settlements.',
          [P('p1', 'Service and interest cost', 5, 'service', 'interest'), P('p2', 'Return and actuarial items', 5, 'return|actuarial')], 'c4'),
        V('v5', 'How is accumulating paid absence measured?', 'At the additional amount the enterprise expects to pay because of the unused entitlement that has built up at the balance sheet date.',
          [P('p1', 'Additional amount expected', 6, 'expect'), P('p2', 'Unused entitlement', 4, 'unused')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Unnati Steel Ltd.', 'difficulty': 'moderate',
              'case': 'Unnati Steel Ltd. contributes 12% of basic pay to the government provident fund (₹48 lakh for the year, ₹4 lakh unpaid at year end). It runs a gratuity plan valued by an actuary, and in March announced a VRS; 40 employees are expected to accept at ₹5 lakh each.',
              'mcqs': [
                  M('k1a', 'The provident fund expense for the year is:', ['₹48 lakh, with ₹4 lakh shown as a liability', '₹44 lakh', 'Actuarially valued', 'Nil until paid'], 0,
                    'A defined contribution plan is expensed at the contribution payable for the period, ₹48 lakh, and the unpaid ₹4 lakh is a liability. No actuarial valuation is needed. In practice: pay dues on time.', 'core', topic=T3),
                  M('k1b', 'The gratuity plan is:', ['A defined benefit plan', 'A defined contribution plan', 'A short-term benefit', 'A termination benefit'], 0,
                    'Gratuity promises a benefit based on salary and years of service, so the employer bears actuarial and investment risk: it is a defined benefit plan. In practice: use the projected unit credit method.', 'core', topic=T3),
                  M('k1c', 'Provision for the VRS at year end:', ['₹2 crore', '₹5 crore', 'Nil', '₹40 lakh'], 0,
                    'With a present obligation from the announced scheme, termination benefits are measured on the number expected to accept: 40 × ₹5 lakh = ₹2 crore. In practice: discount if payable beyond twelve months.', 'moderate', check=2, topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch06', 1, 'Accounting Standard 15 Employee Benefits',
                ['Classify employee benefits into the four AS 15 categories.',
                 'Account for short-term benefits including paid absences and bonus.',
                 'Distinguish defined contribution and defined benefit plans and measure defined benefit cost and liability.',
                 'Account for other long-term and termination benefits.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 35}, 'prereq': ['int-p1-ch05-u07'],
                 'exam_tip': 'For defined benefit questions, prepare separate movements for the obligation and plan assets, then reconcile the net liability.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Four categories: short-term, post-employment, other long-term, termination.', 'Short-term: undiscounted; accumulating leave as service is rendered.',
                             'Bonus when a present obligation exists (including practice).', 'DC: expense contribution; DB: projected unit credit, gov bond discount rate.',
                             'DB expense: service + interest − expected return ± actuarial + past service ± curtailment.', 'Long-term: immediate recognition; termination: when obligation exists.'],
                 'remember': ['Actuarial gains/losses go to profit and loss immediately.'],
                 'traps': ['Non-vesting accumulating leave still creates a liability.']},
                [('Short-term', 'Undiscounted'), ('DB method', 'Projected unit credit'), ('Discount rate', 'Government bond yields')],
                viva, cases)
