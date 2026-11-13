"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 8 Unit 1 — AS 7 Construction Contracts.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch08-u01'
T1 = 'Types of contracts; combining and segmenting'
T2 = 'Contract revenue and contract costs'
T3 = 'Percentage of completion and reliable estimates'
T4 = 'Expected losses and uncertain outcomes'
T5 = 'Amounts due from or to customers and disclosure'


def build():
    ck = Checks()
    tot = ck.add('36+54', 'Total estimated cost (₹ lakh)')
    stage = ck.add('36*100/90', 'Stage of completion (%)')
    rev = ck.add('100*40/100', 'Revenue recognised (₹ lakh)')
    prof = ck.add('40-36', 'Profit recognised (₹ lakh)')
    due = ck.add('36+4-30', 'Amount due from customer (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'A profitable fixed-price contract', 'difficulty': 'core', 'minutes': 8,
          'q': 'Setu Builders Ltd. has a fixed-price contract for ₹100 lakh. In year 1 it incurred costs of ₹36 lakh and expects further costs of ₹54 lakh. Progress billings are ₹30 lakh. Using the cost-to-cost method, compute revenue, profit and the amount due from the customer.',
          'solution': [table(['Step', 'Working', '₹ lakh / %'], [
              ['Total estimated cost', '36 + 54', R(tot)],
              ['Stage of completion', '36 ÷ 90', f'{R(stage)}%'],
              ['Revenue recognised', '40% × 100', R(rev)],
              ['Profit recognised', '40 − 36', R(prof)],
              ['Due from customer', 'Costs 36 + profit 4 − billings 30', R(due)]], title='Percentage of completion')],
          'checks': list(ck)}

    ck2 = Checks()
    loss = ck2.add('50-(21+39)', 'Expected loss on the contract (₹ lakh)')
    st2 = ck2.add('21*100/60', 'Stage of completion (%)')
    rev2 = ck2.add('50*35/100', 'Revenue recognised (₹ lakh)')
    prov = ck2.add('10-(21-17.5)', 'Provision for future loss (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'When the contract turns loss-making', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Varun Infra Ltd.\'s contract price is ₹50 lakh. Costs to date are ₹21 lakh; estimated costs to complete ₹39 lakh. Compute the expected loss and show how it is recognised this year.',
          'solution': [table(['Step', 'Working', '₹ lakh / %'], [
              ['Expected loss', '50 − 60', R(loss)],
              ['Stage of completion', '21 ÷ 60', f'{R(st2)}%'],
              ['Revenue recognised', '35% × 50', R(rev2)],
              ['Loss from revenue less costs to date', '17.5 − 21', '(3.5)'],
              ['Provision for remaining expected loss', '10 − 3.5', R(prov)],
              ['Total loss recognised this year', '', '10']], title='Expected loss recognised at once')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A construction contract is negotiated for building an asset, or a group of closely related assets, such as a bridge, dam, ship or building.',
            'Fixed price contracts set an agreed price (sometimes with cost escalation clauses); cost plus contracts reimburse allowable costs plus a percentage or fixed fee.',
            'Contracts are usually accounted for separately. A single contract covering several assets is split (segmented) when separate proposals were made, each part was negotiated separately and the costs and revenues of each can be identified. A group of contracts is combined when negotiated as a package, closely interrelated and performed together or in sequence. An option for an extra asset is a separate contract if it differs significantly or its price is negotiated separately.'],
          'Account for the economic unit of the deal — split it or combine it as the substance requires.',
          'Three flyovers negotiated as one package with one overall margin are combined.'),
        C('c2', T2, [
            'Contract revenue comprises the initial agreed amount and variations, claims and incentive payments to the extent that they will probably result in revenue and can be measured reliably.',
            'Contract costs comprise costs directly related to the contract (site labour, materials, depreciation of plant used, design and technical assistance, rectification and warranty costs, third-party claims), costs attributable to contract activity in general that can be allocated (insurance, design not directly related, construction overheads), and other costs specifically chargeable to the customer under the contract.',
            'Not contract costs: general administration and research costs not reimbursable, selling costs, and depreciation of idle plant not used on the contract. Costs to secure a contract are included if separately identifiable and the contract is probable.'],
          'Revenue includes likely extras; cost includes everything the contract really uses.',
          'A ₹5 lakh variation approved by the client is added to contract revenue.'),
        C('c3', T3, [
            'When the outcome can be estimated reliably, revenue and costs are recognised by reference to the stage of completion at the balance sheet date — the percentage of completion method.',
            'For a fixed price contract the outcome is reliable when total revenue can be measured reliably, economic benefits are probable, costs to complete and the stage of completion can be measured reliably, and costs can be identified and compared with estimates. For cost plus, when benefits are probable and attributable costs can be identified and measured.',
            'Stage of completion may be measured by the proportion of costs incurred to date to total estimated costs, surveys of work performed, or completion of a physical proportion of work. Costs that do not reflect work done (materials not yet used, advances to subcontractors) are excluded from the cost-to-cost ratio.',
            'Estimates are revised each period; the effect is a change in estimate.'],
          'Recognise profit as the work progresses, measured reliably.',
          'Cement delivered to site but not yet used does not count towards the stage of completion.'),
        C('c4', T4, [
            'Once total costs are likely to run above total revenue, the expected loss is recognised as an expense immediately, whether or not work has begun, regardless of the stage of completion and of profits on other contracts (unless combined).',
            'When the outcome cannot be estimated reliably, revenue is recognised only to the extent of costs incurred that are probably recoverable, and costs are expensed when incurred. No profit is recognised. Costs not probable of recovery are expensed at once.'],
          'Profits wait for reliable evidence; losses are booked as soon as they are expected.',
          'In the early stages of a novel project, revenue equals recoverable costs and no profit is shown.'),
        C('c5', T5, [
            'Gross amount due from customers = costs incurred + recognised profits − recognised losses − progress billings, for contracts where this is positive (an asset). Where negative, it is the gross amount due to customers (a liability).',
            'Disclose contract revenue recognised, methods used to determine revenue and stage of completion, and for contracts in progress: aggregate costs incurred and profits recognised (less losses), advances received and retentions.'],
          'The balance sheet shows the gap between work valued and work billed.',
          'If billings exceed costs plus profit, the excess is a liability to the customer.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Contract review at year end', 'role': 'Audit assistant',
             'situation': 'A contractor has five projects in progress, one now expected to lose money.',
             'steps': ['Check reliability of estimates for each contract.', 'Compute stage of completion excluding unused materials.', 'Recognise the full expected loss immediately.', 'Work out amounts due from and to customers.'],
             'takeaway': 'Stage of completion is the engine; losses bypass it.'}]

    mcqs = [
        Q('m1', 'Under the percentage of completion method, revenue is recognised:', ['By reference to the stage of completion at the balance sheet date', 'Only on completion', 'When cash is received', 'Equally each year'], 0,
          'When the outcome can be estimated reliably, AS 7 matches revenue and costs with the stage of completion reached at the balance sheet date. This shows profit as work progresses. In practice: measure stage carefully.', 'c3', T3),
        Q('m2', 'Costs to date ₹60 lakh; estimated costs to complete ₹90 lakh; contract price ₹200 lakh. Revenue to recognise:', ['₹80 lakh', '₹60 lakh', '₹120 lakh', '₹200 lakh'], 0,
          'Stage = 60 ÷ 150 = 40%; revenue = 40% × ₹200 lakh = ₹80 lakh, giving a profit of ₹20 lakh to date. In practice: exclude unused materials from costs to date.', 'c3', T3, 'moderate', check=80),
        Q('m3', 'Materials purchased for the contract but not yet used are:', ['Excluded from costs used to measure stage of completion', 'Included in the stage calculation', 'Expensed immediately', 'Shown as revenue'], 0,
          'Cost-to-cost measurement includes only costs reflecting work performed; materials delivered but not yet installed and advances to subcontractors are excluded until used. In practice: count them as inventory or advances.', 'c3', T3),
        Q('m4', 'An expected loss on a construction contract is recognised:', ['Immediately as an expense', 'In proportion to stage of completion', 'Only on completion', 'Not at all if other contracts make profit'], 0,
          'AS 7 requires the full expected loss to be expensed as soon as it is probable that total costs will exceed total revenue, whatever the stage of completion. Profits on other separate contracts do not offset it. In practice: provide for the balance.', 'c4', T4),
        Q('m5', 'If the outcome of a contract cannot be estimated reliably, revenue is recognised:', ['Only to the extent of recoverable costs incurred', 'On percentage of completion', 'At the contract price', 'Not at all'], 0,
          'Where reliability is lacking, revenue equals costs incurred that are probably recoverable, and those costs are expensed, so no profit is shown. When reliability returns, the normal method resumes. In practice: common in early stages.', 'c4', T4),
        Q('m6', 'Which is NOT a contract cost?', ['Selling costs', 'Site supervision', 'Depreciation of plant used on the contract', 'Design costs directly related'], 0,
          'AS 7 excludes selling costs, unreimbursable general administration and research costs, and depreciation of idle plant from contract costs. Direct site costs and related design count. In practice: separate overhead pools.', 'c2', T2),
        Q('m7', 'A variation in contract work is included in revenue when:', ['It is probable the customer will approve it and the amount can be measured reliably', 'Work on it starts', 'The contractor requests it', 'It is billed'], 0,
          'Variations, claims and incentives enter contract revenue to the extent they will probably result in revenue and can be measured reliably — usually on customer approval. In practice: keep approval letters.', 'c2', T2),
        Q('m8', 'Costs incurred ₹50 lakh; profits recognised ₹8 lakh; progress billings ₹65 lakh. The balance sheet shows:', ['Amount due to customers ₹7 lakh', 'Amount due from customers ₹7 lakh', 'Amount due from customers ₹58 lakh', 'Nil'], 0,
          'Costs plus profit (₹58 lakh) less billings (₹65 lakh) is negative ₹7 lakh, so it is a gross amount due to customers, shown as a liability. In practice: present each contract on its own.', 'c5', T5, 'hard'),
        Q('m9', 'Contracts are combined when they are:', ['Negotiated as a single package and closely interrelated', 'With the same customer only', 'Of similar size', 'In the same city'], 0,
          'A group of contracts is treated as one when negotiated as a package, so interrelated that they form a single project with an overall margin, and performed together or in sequence. In practice: look at the pricing.', 'c1', T1),
        Q('m10', 'A cost plus contract\'s outcome can be estimated reliably when:', ['Benefits are probable and attributable costs can be identified and measured reliably', 'The contract is complete', 'The customer has paid half', 'The contract price is fixed'], 0,
          'For cost plus contracts, reliability needs probable economic benefits and contract costs that can be clearly identified and reliably measured, whether reimbursable or not. In practice: maintain cost records.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Stage of completion', 1.5, 'computation', 'stage', nums=[stage]),
           S('s2', 'Revenue and profit', 2, 'computation', 'revenue', nums=[rev, prof]),
           S('s3', 'Amount due from customer', 1.5, 'computation', 'due', nums=[due])],
          ['Show the stage first.'], ['Using billings to measure stage.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Expected loss', 1.5, 'computation', 'loss', nums=[loss]),
           S('s2', 'Revenue at stage', 1.5, 'computation', 'stage', nums=[rev2]),
           S('s3', 'Provision for remainder', 2, 'computation', 'provision', nums=[prov])],
          ['Recognise the whole loss.'], ['Recognising only 35% of the loss.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a construction contract?', 'A contract specifically negotiated for building an asset or a group of closely interrelated assets such as a bridge, dam or building.',
          [P('p1', 'Negotiated for building', 6, 'negotiat|build|construct'), P('p2', 'Asset examples', 4, 'bridge|dam|building|asset')], 'c1'),
        V('v2', 'How is stage of completion measured?', 'By the proportion of costs incurred to total estimated costs, by surveys of work done, or by completion of a physical proportion of work.',
          [P('p1', 'Cost proportion', 5, 'cost'), P('p2', 'Surveys or physical proportion', 5, 'survey|physical')], 'c3'),
        V('v3', 'How is an expected loss treated?', 'It is recognised as an expense immediately in full, irrespective of the stage of completion.',
          [P('p1', 'Immediately', 6, 'immediate'), P('p2', 'In full', 4, 'full|whole')], 'c4'),
        V('v4', 'What if the outcome cannot be estimated reliably?', 'Revenue is recognised only to the extent of recoverable costs incurred and those costs are expensed, so profit waits until the outcome is reliable.',
          [P('p1', 'Recoverable costs', 6, 'recoverable'), P('p2', 'Profit deferred', 4, 'profit')], 'c4'),
        V('v5', 'How is the gross amount due from customers computed?', 'Costs incurred plus recognised profits less recognised losses less progress billings.',
          [P('p1', 'Costs plus profits', 5, 'costs', 'profit'), P('p2', 'Less billings', 5, 'billing')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Harit Constructions Ltd.', 'difficulty': 'moderate',
              'case': 'Harit Constructions Ltd. has a contract for ₹120 lakh. Costs incurred to date are ₹48 lakh, including ₹8 lakh of steel lying unused at site. Total estimated contract cost (including that steel) is ₹100 lakh. Progress billings: ₹40 lakh.',
              'mcqs': [
                  M('k1a', 'Stage of completion (cost-to-cost):', ['40%', '46%', '50%', '33%'], 0,
                    'Costs of work actually done are ₹48 − 8 = ₹40 lakh; set against the total estimated cost of ₹100 lakh, the stage is 40%. Unused steel does not reflect work performed. In practice: exclude unused materials from the numerator.', 'hard', check=40, topic=T3),
                  M('k1b', 'Revenue recognised:', ['₹48 lakh', '₹40 lakh', '₹60 lakh', '₹55 lakh'], 0,
                    'Revenue = 40% × ₹120 lakh = ₹48 lakh, matched with work-related costs of ₹40 lakh, giving profit of ₹8 lakh to date. In practice: unused steel is shown as an asset.', 'moderate', check=48, topic=T3),
                  M('k1c', 'Unused steel at site is shown as:', ['An asset (materials for the contract), not a cost of work done', 'Contract revenue', 'An expense', 'Amount due to customers'], 0,
                    'Materials not yet used do not reflect work performed, so they are carried as an asset until consumed, and excluded from the stage calculation. In practice: verify at the site.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch08', 1, 'Accounting Standard 7 Construction Contracts',
                ['Identify types of contracts and apply combining and segmenting rules.',
                 'Determine contract revenue and contract costs.',
                 'Apply the percentage of completion method and recognise expected losses.',
                 'Compute amounts due from or to customers and give disclosures.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 35}, 'prereq': ['int-p1-ch07-u04'],
                 'exam_tip': 'Compute total estimated cost, stage, revenue, profit — then check for an expected loss before anything else.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Fixed price vs cost plus; combine or segment by substance.', 'Revenue includes probable, measurable variations, claims, incentives.',
                             'Contract costs: direct + allocable + chargeable; exclude selling, unreimbursable admin, idle plant.', 'Percentage of completion when reliable.',
                             'Expected loss: recognise immediately.', 'Due from/to customers = costs + profits − losses − billings.'],
                 'remember': ['Unused materials are excluded from stage of completion.'],
                 'traps': ['Billings do not measure stage of completion.']},
                [('Method', 'Percentage of completion'), ('Expected loss', 'Immediately'), ('Due from customers', 'Costs + profit − losses − billings')],
                viva, cases)
