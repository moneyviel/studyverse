"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 8 Unit 2 — AS 9 Revenue Recognition.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch08-u02'
T1 = 'Scope and meaning of revenue'
T2 = 'Sale of goods'
T3 = 'Rendering of services'
T4 = 'Interest, royalties and dividends'
T5 = 'Uncertainties and special situations'


def build():
    ck = Checks()
    intr = ck.add('210000-180000', 'Interest element in the instalments (₹)')
    y1 = ck.add('180000', 'Revenue from sale at the date of sale (₹)')
    i1 = {'id': 'i1', 'title': 'An instalment sale', 'difficulty': 'core', 'minutes': 6,
          'q': 'Nayan Electronics Ltd. sold a refrigerator set on 1 April 2026 for 3 annual instalments totalling ₹2,10,000; its cash price was ₹1,80,000. Delivery and title passed on the sale date, and collection is reasonably assured. How is revenue recognised?',
          'solution': [table(['Element', 'When recognised', '₹'], [
              ['Sale price (excluding interest)', 'On the date of sale', inr(y1)],
              ['Interest element', 'Over the 3 years in proportion to the unpaid balance', inr(intr)]], title='AS 9 — instalment sales')],
          'checks': list(ck)}

    ck2 = Checks()
    rec = ck2.add('400000*60/100', 'Revenue on goods sold by the consignee (₹)')
    i2 = {'id': 'i2', 'title': 'Goods on consignment and on approval', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Jasmine Ltd. sent goods with a sale value of ₹4,00,000 to a consignee; 60% were sold by the consignee by 31 March. It also sent goods worth ₹1,00,000 on sale-or-return terms (30 days); 20 days have passed with no response at year end. What revenue is recognised?',
          'solution': [table(['Arrangement', 'Rule', 'Revenue ₹'], [
              ['Consignment', 'Recognised when the consignee sells to a third party', inr(rec)],
              ['Sale or return (within the return period)', 'Recognised only on acceptance or when the return period lapses', 'Nil']], title='AS 9 — special cases')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Revenue means the total cash, receivables or other consideration that flows in from the normal business of selling goods, rendering services, and from others using the enterprise\'s resources yielding interest, royalties and dividends.',
            'It is measured by the charges made to customers; amounts collected for third parties (such as GST) are not revenue, and trade discounts and volume rebates are deducted.',
            'AS 9 does not cover revenue dealt with by other standards (construction contracts, leases, government grants), insurance contracts, or gains on disposal of fixed assets or from changes in foreign exchange rates.'],
          'Revenue is what the business earns from its own trade, measured gross but without taxes collected for others.',
          'GST collected on a sale is a liability to the government, not revenue.'),
        C('c2', T2, [
            'Revenue from a sale of goods is recognised once ownership of the goods has passed to the buyer for a price, together with all significant risks and rewards of ownership, and retains no effective control usually associated with ownership; and when there is no significant uncertainty about the consideration to be received.',
            'Usually title and risks pass together on delivery; where they do not, the transfer of significant risks and rewards decides.',
            'If the seller keeps significant risks — for example under an unusual warranty, or where installation is a significant part of the contract not yet done — revenue is deferred.'],
          'Revenue on goods follows the passing of risks and rewards, with collection reasonably sure.',
          'A sale of machinery where the seller must still install and commission it may be deferred until installation.'),
        C('c3', T3, [
            'Service revenue is normally booked as the work is carried out, by either the proportionate completion method (revenue in proportion to acts performed) or the completed service contract method (on completion or substantial completion).',
            'Proportionate completion: where a service consists of several acts, revenue is recognised as each act is performed; where acts are of a similar nature performed over time, often on a straight-line basis.',
            'Examples: installation fees as installation progresses (or with the sale when installation is incidental), tuition fees over the period of instruction, admission fees for events when the event takes place, subscriptions on a straight-line basis or as items are dispatched.'],
          'Service revenue follows the work done.',
          'Fees for a one-year coaching course received upfront are recognised month by month.'),
        C('c4', T4, [
            'Interest is earned with the passage of time — recognised period by period on the balance outstanding at the agreed rate.',
            'Royalties are recognised on an accrual basis in accordance with the relevant agreement.',
            'Dividends are recognised once the shareholder becomes entitled to be paid, usually on declaration.',
            'These are recognised only when there is no significant uncertainty about measurability or collectability.'],
          'Interest accrues with time, royalties with the contract, dividends with the right.',
          'A dividend declared by an investee on 25 March is income for the year ending 31 March.'),
        C('c5', T5, [
            'If there is significant uncertainty about collection at the time of the transaction, recognition is postponed until it is reasonable to expect ultimate collection.',
            'If uncertainty arises after revenue has been recognised (for example a customer\'s later insolvency), a separate provision is made; the revenue already recognised is not reversed.',
            'Special cases: consignment — revenue when the consignee sells to a third party; sale or return or on approval — when the buyer accepts or the time for rejection lapses; instalment sales — sale price excluding interest at the date of sale, interest over time; bill and hold — when the buyer takes title and accepts billing, goods are ready and the buyer asked for delay; goods sold with a right to cancel — when the risk of return can be reliably estimated; delivery against payment by agents — when delivery is made and cash received.',
            'Disclose circumstances in which revenue recognition has been postponed due to significant uncertainties.'],
          'Doubt at the start delays revenue; doubt later needs a provision.',
          'Goods sent on approval are revenue only after the customer says yes or the trial period ends.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Cut-off testing at year end', 'role': 'Audit assistant',
             'situation': 'A distributor has goods on consignment, goods on approval, a bill-and-hold sale and instalment sales near year end.',
             'steps': ['Identify the arrangement type for each transaction.', 'Apply the AS 9 recognition point.', 'Separate interest from instalment prices.', 'Check uncertainty about collection.'],
             'takeaway': 'The contract terms decide the recognition point.'}]

    mcqs = [
        Q('m1', 'Revenue from sale of goods is recognised when:', ['Significant risks and rewards have passed and collection is reasonably certain', 'The order is received', 'Cash is received', 'Goods are manufactured'], 0,
          'AS 9 requires transfer of property with significant risks and rewards, no effective control retained by the seller, and no significant uncertainty about the consideration. In practice: check delivery terms.', 'c2', T2),
        Q('m2', 'GST collected on sales is:', ['Not revenue, as it is collected for the government', 'Revenue', 'Other income', 'Deducted from expenses'], 0,
          'Revenue excludes amounts collected on behalf of third parties such as indirect taxes; they are liabilities until paid over. In practice: present net of GST.', 'c1', T1),
        Q('m3', 'Goods sent on consignment are recognised as revenue when:', ['The consignee sells them to a third party', 'Goods are dispatched to the consignee', 'The consignee pays an advance', 'The year ends'], 0,
          'The consignor keeps the risks and rewards until the consignee sells to a third party; only then is the sale complete. In practice: unsold consignment stock remains inventory.', 'c5', T5),
        Q('m4', 'Dividend income is recognised when:', ['The right to receive payment is established', 'Cash is received', 'The investee earns profits', 'The financial year ends'], 0,
          'AS 9 recognises dividends when the shareholder\'s right to receive payment is established, typically on declaration. In practice: interim dividends declared before year end are income.', 'c4', T4),
        Q('m5', 'Interest on a loan given is recognised:', ['On a time proportion basis', 'When received', 'At maturity', 'When declared'], 0,
          'Interest accrues over time on the outstanding amount at the applicable rate, so it is recognised on a time proportion basis if collectible. In practice: accrue to the balance sheet date.', 'c4', T4),
        Q('m6', 'A customer becomes insolvent after revenue on a sale was recognised. The seller:', ['Makes a separate provision, without reversing the revenue', 'Reverses the revenue', 'Ignores it', 'Treats it as a prior period item'], 0,
          'When uncertainty arises after recognition, AS 9 requires a provision for the doubtful amount rather than an adjustment to revenue already recognised. In practice: charge bad debts.', 'c5', T5),
        Q('m7', 'Tuition fees received in advance for a 12-month course are recognised:', ['Over the period of instruction', 'On receipt', 'At the end of the course', 'On admission'], 0,
          'AS 9 treats tuition as a service performed over time, so fees are recognised over the period of instruction. Admission fees for a specific event are recognised when it takes place. In practice: defer unearned fees.', 'c3', T3),
        Q('m8', 'Instalment price ₹1,20,000; cash price ₹1,00,000. Revenue at the date of sale:', ['₹1,00,000', '₹1,20,000', '₹20,000', 'Nil'], 0,
          'For instalment sales, the price excluding interest is recognised at the date of sale, and the ₹20,000 interest element is recognised over time. In practice: separate the finance component.', 'c5', T5, 'moderate', check=100000),
        Q('m9', 'In a bill-and-hold sale, revenue is recognised when:', ['The buyer takes title, accepts billing, goods are ready and the buyer asked for the delay', 'The seller issues an invoice only', 'Goods are delivered later', 'Payment is received'], 0,
          'Bill-and-hold revenue is recognised if the buyer takes title and accepts billing, delivery is delayed at the buyer\'s request, and the goods are on hand and ready. In practice: obtain the buyer\'s written request.', 'c5', T5),
        Q('m10', 'Which is outside the scope of AS 9?', ['Revenue from construction contracts', 'Royalty income', 'Sale of goods', 'Interest income'], 0,
          'Revenue covered by other standards — construction contracts (AS 7), leases (AS 19) and government grants (AS 12) — is outside AS 9. In practice: apply the specific standard.', 'c1', T1),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Sale price at date of sale', 2, 'computation', 'date of sale', nums=[y1]),
           S('s2', 'Interest over time', 2, 'computation', 'interest', nums=[intr])],
          ['Separate price and interest.'], ['Recognising all instalments as sales.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Consignment rule', 2, 'computation', 'consignee', nums=[rec]),
           S('s2', 'Sale or return rule', 2, 'concept', 'accept|lapse')],
          ['Name the trigger for each.'], ['Recognising goods dispatched to the consignee.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is revenue under AS 9?', 'The gross inflow of consideration from ordinary activities — sale of goods, rendering of services, and use of the enterprise\'s resources by others yielding interest, royalties and dividends.',
          [P('p1', 'Gross inflow from ordinary activities', 5, 'inflow|ordinary'), P('p2', 'Sources', 5, 'goods|services|interest|royalt|dividend')], 'c1'),
        V('v2', 'When is revenue from sale of goods recognised?', 'When significant risks and rewards of ownership have passed to the buyer, the seller has no effective control left, and collection is reasonably certain.',
          [P('p1', 'Risks and rewards', 6, 'risk'), P('p2', 'Collection certain', 4, 'collect|uncertain')], 'c2'),
        V('v3', 'Name the two methods for service revenue.', 'The proportionate completion method and the completed service contract method.',
          [P('p1', 'Proportionate completion', 5, 'proportionate'), P('p2', 'Completed service contract', 5, 'completed')], 'c3'),
        V('v4', 'When are royalties recognised?', 'As they accrue, following whatever the royalty agreement provides.',
          [P('p1', 'Accrual', 6, 'accrual'), P('p2', 'Agreement', 4, 'agreement')], 'c4'),
        V('v5', 'How is uncertainty arising after a sale handled?', 'A separate provision is made; the revenue already recognised is left unchanged.',
          [P('p1', 'Provision', 6, 'provision'), P('p2', 'Revenue unchanged', 4, 'unchanged|left')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Om Machines Ltd.', 'difficulty': 'moderate',
              'case': 'Om Machines Ltd. sold a machine for ₹30 lakh on 20 March; the contract requires the seller to install and commission it, a significant part of the contract, which will be done in April. It also received ₹6 lakh on 1 January as a 12-month maintenance fee, and its investee declared a dividend of ₹2 lakh on 28 March.',
              'mcqs': [
                  M('k1a', 'Revenue from the machine sale at 31 March:', ['Nil, as installation is a significant part not yet done', '₹30 lakh', '₹15 lakh', '₹27 lakh'], 0,
                    'Where installation is a significant part of the contract and is incomplete, significant risks remain with the seller, so revenue is deferred until installation. In practice: recognise in April.', 'moderate', topic=T2),
                  M('k1b', 'Maintenance fee revenue for the year ending 31 March:', ['₹1.5 lakh', '₹6 lakh', '₹0.5 lakh', 'Nil'], 0,
                    'The service runs evenly over 12 months, so 3 months (January–March) are earned: ₹6 lakh × 3/12 = ₹1.5 lakh. The rest is deferred. In practice: straight-line is suitable.', 'core', check=1.5, topic=T3),
                  M('k1c', 'The dividend of ₹2 lakh is:', ['Income for the current year', 'Income next year on receipt', 'Deducted from investment cost', 'Ignored'], 0,
                    'The right to receive was established on declaration (28 March), before the year end, so it is income of the current year. In practice: show it as other income.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch08', 2, 'Accounting Standard 9 Revenue Recognition',
                ['Explain the meaning and measurement of revenue.',
                 'Apply recognition rules to sale of goods and rendering of services.',
                 'Recognise interest, royalties and dividends.',
                 'Handle uncertainties and special sale arrangements.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 25}, 'prereq': ['int-p1-ch08-u01'],
                 'exam_tip': 'Identify the type of arrangement and state its trigger: risk transfer, acceptance, consignee sale, time, right to receive.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Revenue: gross inflow from ordinary activities; excludes taxes collected.', 'Goods: risks and rewards passed, no control retained, collection certain.',
                             'Services: proportionate completion or completed contract.', 'Interest time-proportion; royalties accrual; dividends on right to receive.',
                             'Initial uncertainty postpones; later uncertainty → provision.', 'Consignment, approval, instalment, bill-and-hold rules.'],
                 'remember': ['Interest in instalment sales is recognised over time.'],
                 'traps': ['Dispatch to a consignee is not a sale.']},
                [('Goods', 'Risks & rewards transferred'), ('Dividend', 'Right to receive'), ('Interest', 'Time proportion')],
                viva, cases)
