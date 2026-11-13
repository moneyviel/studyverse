"""CA Final · Paper 1 Financial Reporting · Chapter 9 Ind AS 115 Revenue from Contracts with Customers.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch09-u01'
T1 = 'Steps 1 and 2: contract and performance obligations'
T2 = 'Step 3: transaction price and variable consideration'
T3 = 'Steps 4 and 5: allocation and satisfaction'
T4 = 'Special topics: costs, agents, licences, concessions'


def build():
    ck = Checks()
    dev = ck.add('35000*30000/(30000+12000)', 'Revenue allocated to the device (₹)')
    svc = ck.add('35000*12000/(30000+12000)', 'Revenue allocated to the service plan (₹)')
    m3 = ck.add('35000*12000/(30000+12000)*3/12', 'Service revenue for 3 months to year end (₹)')
    i1 = {'id': 'i1', 'title': 'A phone with a service plan', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Volt Telecom sells a handset with a 12-month service plan for ₹35,000 paid upfront on 1 January. Stand-alone prices: handset ₹30,000, service plan ₹12,000. The handset is delivered on 1 January. How much revenue is recognised by 31 March?',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Performance obligations', 'Handset (point in time) and service (over time)', '—'],
              ['Allocated to handset', '35,000 × 30/42', inr(dev)],
              ['Allocated to service', '35,000 × 12/42', inr(svc)],
              ['Service revenue to 31 March', '10,000 × 3/12', inr(m3)],
              ['Contract liability at 31 March', '10,000 − 2,500', inr(7500)]], title='Allocation by stand-alone selling prices')],
          'checks': list(ck)}

    ck2 = Checks()
    ev = ck2.add('0.6*100+0.3*90+0.1*80', 'Expected value per unit (₹)')
    rev = ck2.add('1000*(0.6*100+0.3*90+0.1*80)', 'Revenue on 1,000 units (₹)')
    cpct = ck2.add('round(60/(60+90)*100,2)', 'Percentage complete by cost (%)')
    i2 = {'id': 'i2', 'title': 'Variable price and over-time revenue', 'difficulty': 'hard', 'minutes': 10,
          'q': '(a) Fresh Mills sells 1,000 units; the final price depends on a market index: ₹100 (60% likely), ₹90 (30%), ₹80 (10%). Using expected value, what is the transaction price, assuming it is highly probable no significant reversal will occur? (b) Brick Builders has a fixed-price contract of ₹200 lakh; costs incurred ₹60 lakh, further costs ₹90 lakh expected; control passes over time. Compute progress and revenue to date.',
          'solution': [table(['Part', 'Working', 'Result'], [
              ['(a) Expected value per unit', '0.6×100 + 0.3×90 + 0.1×80', '₹' + inr(ev)],
              ['(a) Transaction price', '1,000 × 95', '₹' + inr(rev)],
              ['(b) Progress (input method)', '60 ÷ 150', inr(cpct) + '%'],
              ['(b) Revenue to date', '200 × 40%', '₹80 lakh']], title='Variable consideration and progress')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Ind AS 115 uses a five-step model: identify the contract; identify performance obligations; determine the transaction price; allocate it; recognise revenue when (or as) each obligation is satisfied.',
            'A contract exists when it is approved and parties are committed, rights and payment terms are identifiable, it has commercial substance, and collection is probable. Contracts are combined when negotiated as a package; modifications are separate contracts if they add distinct goods at stand-alone prices.',
            'A performance obligation is a promise to transfer a distinct good or service (or a series of substantially the same distinct items). A good is distinct if the customer can benefit from it on its own or with readily available resources, and the promise is separately identifiable within the contract.'],
          'Five steps, always in order — most errors start in step 2.',
          'A software licence with essential customisation may be one obligation.'),
        C('c2', T2, [
            'The transaction price is the consideration the seller expects to earn for handing over the promised goods or services, excluding amounts collected for third parties such as GST.',
            'Variable consideration (discounts, rebates, refunds, incentives, penalties) is estimated using expected value or most likely amount, and included only to the extent it is highly probable that a significant reversal will not occur when uncertainty resolves. Expected returns create a refund liability and a right-to-recover asset.',
            'A significant financing component adjusts the price for time value (practical expedient where the gap is one year or less). Non-cash consideration is at fair value. Consideration payable to a customer reduces revenue unless for a distinct good or service.'],
          'Price is what you expect to earn, trimmed by the reversal constraint.',
          'A volume rebate likely to be earned reduces revenue now.'),
        C('c3', T3, [
            'The price is allocated to each obligation in proportion to stand-alone selling prices, estimated by adjusted market assessment, expected cost plus margin, or residual approach (only in limited cases). Discounts and variable consideration are allocated to specific obligations only when criteria are met.',
            'Revenue is recognised when control passes. Over time if: the customer simultaneously receives and consumes benefits; the entity\'s work creates or enhances an asset the customer controls; or the asset cannot be redirected to another use and the seller can legally demand payment for performance so far. Otherwise at a point in time, using indicators such as right to payment, legal title, physical possession, risks and rewards, and acceptance.',
            'Progress is measured by output methods (units delivered, milestones) or input methods (costs incurred), excluding costs that do not depict performance such as wasted materials or uninstalled goods.'],
          'Allocate by stand-alone prices; recognise as control moves.',
          'A building on the customer\'s land is satisfied over time.'),
        C('c4', T4, [
            'Incremental costs of obtaining a contract (e.g. sales commissions) are capitalised if expected to be recovered (expedient: expense if amortisation period is a year or less). Costs to fulfil are capitalised if they relate directly to a contract, create resources used in future, and are recoverable. These assets are amortised on a basis consistent with the transfer of goods and tested for impairment.',
            'Principal versus agent: an entity is a principal if it controls the good before transfer (indicators: primary responsibility, inventory risk, pricing discretion) and recognises gross revenue; an agent recognises only its commission.',
            'Other topics: licences (right to access — over time; right to use — point in time); bill-and-hold, consignment, repurchase agreements, customer options for additional goods (material rights), warranties (assurance vs service-type), and service concession arrangements under Appendix D, where the operator recognises a financial asset or an intangible asset depending on who bears demand risk.'],
          'Capitalise costs that win or fulfil contracts; decide gross or net by control.',
          'A travel portal selling flights as an agent records only its commission.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Revenue policy review', 'role': 'Revenue accountant',
             'situation': 'A SaaS company sells subscriptions with setup and support.',
             'steps': ['Identify distinct obligations.', 'Estimate stand-alone prices.', 'Assess over-time recognition for subscriptions.', 'Capitalise sales commissions and amortise them.'],
             'takeaway': 'Contract terms decide the pattern; document every judgement.'}]

    mcqs = [
        Q('m1', 'The third step of the Ind AS 115 model is:', ['Determine the transaction price', 'Identify the contract', 'Allocate the price', 'Recognise revenue'], 0,
          'Contract, obligations, price, allocation, recognition. In practice: follow the order.', 'c1', T1),
        Q('m2', 'Variable consideration is included to the extent that:', ['It is highly probable a significant reversal will not occur', 'It is possible', 'Cash is received', 'The customer agrees'], 0,
          'The constraint prevents overstatement. In practice: reassess each period.', 'c2', T2),
        Q('m3', 'GST collected from customers is:', ['Excluded from the transaction price', 'Included in revenue', 'Other income', 'A contract asset'], 0,
          'It is collected for the government. In practice: show separately as liability.', 'c2', T2),
        Q('m4', 'The price is allocated to obligations based on:', ['Relative stand-alone selling prices', 'Cost', 'Contract labels', 'Equal shares'], 0,
          'Reflects what each would sell for separately. In practice: estimate if not observable.', 'c3', T3),
        Q('m5', 'Revenue is recognised over time when the asset has no alternative use and:', ['There is an enforceable right to payment for work to date', 'Cash is received', 'The asset is large', 'The customer approves'], 0,
          'Both conditions are needed. In practice: check contract termination clauses.', 'c3', T3),
        Q('m6', 'An agent recognises revenue:', ['At the net amount of its fee or commission', 'At the gross amount', 'Never', 'At cost'], 0,
          'It does not control the goods. In practice: e-commerce marketplaces.', 'c4', T4),
        Q('m7', 'Incremental costs of obtaining a contract are:', ['Capitalised if expected to be recovered', 'Always expensed', 'Added to revenue', 'Deferred tax'], 0,
          'Practical expedient for periods of a year or less. In practice: sales commissions.', 'c4', T4),
        Q('m8', 'A good is distinct if the customer can benefit from it and:', ['It is separately identifiable within the contract', 'It has a price list', 'It is physical', 'It is delivered first'], 0,
          'Both criteria apply. In practice: integration or modification fails the second.', 'c1', T1),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Obligations', 1, 'concept', 'obligation'), S('s2', 'Allocation', 3, 'computation', 'allocat', nums=[dev, svc]), S('s3', 'Revenue to date', 2, 'computation', 'service', nums=[m3])],
          ['Show contract liability.'], ['Recognising all upfront.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 8, i2['q'], i2['solution'],
          [S('s1', 'Expected value', 2, 'computation', 'expected', nums=[ev]), S('s2', 'Price', 2, 'computation', 'transaction', nums=[rev]), S('s3', 'Progress', 2, 'computation', 'progress', nums=[cpct]), S('s4', 'Revenue', 2, 'computation', 'revenue', nums=[80])],
          ['Mention the constraint.'], ['Using total contract cost of 90.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'List the five steps of Ind AS 115.', 'Identify the contract, identify performance obligations, determine the transaction price, allocate the price, and recognise revenue as obligations are satisfied.',
          [P('p1', 'Contract and obligations', 5, 'contract|obligation'), P('p2', 'Price, allocation, recognition', 5, 'allocat|price')], 'c1'),
        V('v2', 'What is the constraint on variable consideration?', 'Include it only to the extent it is highly probable that revenue already booked will escape any significant reversal later.',
          [P('p1', 'Highly probable', 6, 'highly probable'), P('p2', 'Reversal', 4, 'reversal')], 'c2'),
        V('v3', 'When is revenue recognised over time?', 'When the customer receives and consumes benefits as performed, controls the asset being created, or the asset has no alternative use with an enforceable right to payment.',
          [P('p1', 'Consumes benefits or controls asset', 5, 'consume|control'), P('p2', 'Alternative use and payment right', 5, 'alternative|payment')], 'c3'),
        V('v4', 'How do you decide principal or agent?', 'By assessing whether the entity controls the good or service before transfer, using indicators like primary responsibility, inventory risk and pricing discretion.',
          [P('p1', 'Control before transfer', 6, 'control'), P('p2', 'Indicators', 4, 'inventory|pricing|responsib')], 'c4'),
        V('v5', 'How does a service concession operator account for its right?', 'As a financial asset if it has an unconditional right to receive cash from the grantor, or as an intangible asset if it has a right to charge users.',
          [P('p1', 'Financial asset', 5, 'financial asset'), P('p2', 'Intangible asset', 5, 'intangible')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Pinnacle Machines Ltd.', 'difficulty': 'moderate',
              'case': 'Pinnacle Machines Ltd. sells a machine for ₹90 lakh with installation (simple, available from others) and a 2-year service-type warranty beyond the standard assurance. Stand-alone prices: machine ₹80 lakh, installation ₹10 lakh, extended warranty ₹10 lakh. Its sales staff earn 2% commission on each contract.',
              'mcqs': [
                  M('k1a', 'Number of performance obligations:', ['Three', 'One', 'Two', 'Four'], 0,
                    'Machine, installation and service-type warranty are distinct. In practice: assurance warranty is not separate.', 'moderate', topic=T1),
                  M('k1b', 'Revenue allocated to the machine (₹ lakh):', ['72', '80', '90', '75'], 0,
                    '90 × 80/100 = 72. In practice: discount spread proportionately.', 'moderate', check=72, topic=T3),
                  M('k1c', 'Revenue for the extended warranty is recognised:', ['Over the 2-year warranty period', 'On delivery', 'At the end', 'When claims arise'], 0,
                    'A stand-ready obligation satisfied over time. In practice: straight-line often fits.', 'core', topic=T3),
                  M('k1d', 'The 2% sales commission is:', ['Capitalised as a cost to obtain the contract, if recoverable', 'Deducted from revenue', 'Always expensed', 'Added to inventory'], 0,
                    'An incremental cost of obtaining the contract. In practice: amortise with the revenue pattern.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch09', 1, 'Ind AS 115 "Revenue from Contracts with Customers"',
                ['Identify contracts and distinct performance obligations.',
                 'Determine the transaction price including variable consideration.',
                 'Allocate the price and recognise revenue over time or at a point in time.',
                 'Account for contract costs, principal-agent issues, licences and concessions.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 40}, 'prereq': ['fin-p1-ch08-u03'],
                 'exam_tip': 'Write the five steps as headings in every revenue answer.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Five-step model.',
                             'Distinct = capable + separately identifiable.',
                             'Variable consideration with reversal constraint.',
                             'Allocate by stand-alone prices.',
                             'Over time or point in time based on control.'],
                 'remember': ['Agents book net commission.'],
                 'traps': ['Recognising bundled prices without allocation.']},
                [('Step 1', 'Contract'), ('Step 2', 'Performance obligations'), ('Step 3', 'Transaction price'), ('Steps 4–5', 'Allocate and recognise')],
                viva, cases)
