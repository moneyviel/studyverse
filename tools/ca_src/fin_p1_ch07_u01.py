"""CA Final · Paper 1 Financial Reporting · Chapter 7 Unit 1 Ind AS 12 Income Taxes.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch07-u01'
T1 = 'Current tax and tax base'
T2 = 'Temporary differences and deferred tax'
T3 = 'Recognition limits and exceptions'
T4 = 'Presentation, offsetting and special topics'


def build():
    ck = Checks()
    ttd = ck.add('800-600', 'Taxable temporary difference on plant (₹ lakh)')
    dtl = ck.add('(800-600)*0.25', 'Deferred tax liability (₹ lakh)')
    dta = ck.add('40*0.25', 'Deferred tax asset on warranty provision (₹ lakh)')
    loss = ck.add('120*0.25', 'Deferred tax asset on tax losses (₹ lakh)')
    net = ck.add('(800-600)*0.25-40*0.25-120*0.25', 'Net deferred tax liability (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Building a deferred tax schedule', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Cirrus Ltd. (tax rate 25%) has: plant with carrying amount ₹800 lakh and tax written-down value ₹600 lakh; a warranty provision ₹40 lakh deductible only when paid; unused tax losses ₹120 lakh which it is probable will be used against future taxable profits; and fines ₹10 lakh accrued that are never deductible. All items relate to the same tax authority. Compute deferred tax balances.',
          'solution': [table(['Item', 'Carrying / tax base', 'Temporary difference', 'Deferred tax ₹ lakh'], [
              ['Plant', '800 / 600', 'Taxable ' + inr(ttd), 'DTL ' + inr(dtl)],
              ['Warranty provision', '40 / 0', 'Deductible 40', 'DTA ' + inr(dta)],
              ['Unused tax losses', '—', 'Carry-forward 120', 'DTA ' + inr(loss)],
              ['Fines', '10 / 10', 'None — permanent difference', 'Nil'],
              ['Net (offset — same authority, legal right)', '', '', 'DTL ' + inr(net)]], title='Ind AS 12 balance sheet approach')],
          'checks': list(ck)}

    ck2 = Checks()
    oci = ck2.add('100*0.25', 'Deferred tax on revaluation, charged to OCI (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Where does the tax go?', 'difficulty': 'core', 'minutes': 5,
          'q': 'Cirrus Ltd. revalues land upwards by ₹100 lakh through OCI; the tax base is unchanged. It also gets a deduction for share options measured differently. Where is the deferred tax on the revaluation recognised and how much?',
          'solution': [table(['Item', 'Working', 'Treatment'], [
              ['Revaluation temporary difference', '100 taxable', 'DTL'],
              ['Deferred tax', '100 × 25% = ' + inr(oci), 'Charged to OCI, following the item'],
              ['Principle', 'Tax follows the underlying transaction', 'P&L, OCI or equity']], title='Tax follows the item')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Ind AS 12 uses a balance sheet approach. Current tax is the tax payable (recoverable) on taxable profit (loss) of the period; unpaid amounts are liabilities and excess payments are assets. Benefits of tax losses carried back are assets.',
            'Current and deferred tax are measured using rates and laws enacted or substantively enacted by the reporting date.',
            'The tax base of an asset is the amount deductible for tax against future taxable benefits from it (if the benefits are not taxable, the tax base equals carrying amount). For a liability, the tax base equals the book figure minus whatever will be deductible later; for revenue received in advance, it is the carrying amount less revenue not taxable in future.'],
          'Tax base is how the tax authority sees the item.',
          'A machine with tax WDV of 600 has a tax base of 600.'),
        C('c2', T2, [
            'Temporary differences are differences between carrying amount and tax base. Taxable temporary differences (asset carrying amount above tax base, e.g. accelerated tax depreciation) create deferred tax liabilities; deductible temporary differences (e.g. provisions deductible when paid) create deferred tax assets.',
            'Permanent items such as non-deductible fines create no temporary differences. Unused tax losses and credits create deferred tax assets to the extent future taxable profit is probable.',
            'Deferred tax is measured at rates expected to apply when the asset is realised or liability settled, reflecting the manner of recovery, and is not discounted. Changes in deferred tax are recognised in the same place as the underlying item — profit or loss, OCI or equity.'],
          'Deferred tax is tomorrow\'s tax on today\'s differences.',
          'A 200 gap at 25% means 50 of future tax.'),
        C('c3', T3, [
            'Initial recognition exception: no deferred tax arises on goodwill\'s initial recognition, or when an asset or liability is first booked in a deal that is not a business combination, affects neither accounting nor taxable profit, and creates no matching pair of taxable and deductible differences of equal size (so leases and decommissioning now give rise to deferred tax).',
            'Deferred tax assets are recognised only to the extent that taxable profit will probably be available — supported by taxable temporary differences reversing in time, forecasts or tax planning. A history of losses calls for convincing evidence. Carrying amounts are reviewed each reporting date.',
            'For investments in subsidiaries, branches, associates and joint arrangements, a DTL is not recognised when the parent controls the timing of reversal and reversal is not probable in the foreseeable future. Under the Pillar Two amendment, entities do not recognise or disclose deferred tax relating to Pillar Two income taxes.'],
          'Exceptions stop mechanical deferred tax where it would mislead.',
          'Undistributed profits of a subsidiary the parent won\'t distribute need no DTL.'),
        C('c4', T4, [
            'Current tax assets and liabilities are offset only with a legally enforceable right and intention to settle net. Deferred tax assets and liabilities are offset when one tax authority levies both and they concern one taxpayer (or taxpayers planning net settlement), with an enforceable right to set off current tax.',
            'Deferred tax is always non-current in the balance sheet. Tax expense is shown in profit or loss; a numerical reconciliation between tax expense and accounting profit times the applicable rate is disclosed.',
            'Uncertain tax treatments (Appendix C) are measured at the most likely amount or expected value, depending on which better predicts resolution, assuming the authority examines with full knowledge. In business combinations, deferred tax on fair value adjustments affects goodwill.'],
          'Net only when the law lets you; always explain the effective rate.',
          'MAT credit is a deferred tax asset when future normal tax is probable.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Year-end tax computation', 'role': 'Tax accountant',
             'situation': 'The accounts close at 31 March; the tax computation is drafted.',
             'steps': ['Compute current tax.', 'List carrying amounts and tax bases of all items.', 'Apply exceptions and recoverability tests.', 'Allocate deferred tax between P&L, OCI and equity; prepare rate reconciliation.'],
             'takeaway': 'A full balance sheet comparison avoids missed differences.'}]

    mcqs = [
        Q('m1', 'Ind AS 12 computes deferred tax using:', ['The balance sheet approach', 'The income statement approach', 'Cash basis', 'Timing differences only'], 0,
          'It compares carrying amounts and tax bases. In practice: wider than the old AS 22.', 'c2', T2),
        Q('m2', 'A provision deductible only when paid creates:', ['A deductible temporary difference', 'A taxable temporary difference', 'A permanent difference', 'No difference'], 0,
          'Carrying amount exceeds its tax base of nil. In practice: a DTA results.', 'c2', T2),
        Q('m3', 'Deferred tax balances are:', ['Not discounted', 'Discounted at market rate', 'Discounted at tax rate', 'Discounted if long-term'], 0,
          'Discounting is prohibited. In practice: simplifies measurement.', 'c2', T2),
        Q('m4', 'Deferred tax on the initial recognition of goodwill is:', ['Not recognised', 'Recognised as DTL', 'Recognised as DTA', 'Recognised in OCI'], 0,
          'It would only increase goodwill circularly. In practice: tax-deductible goodwill differs later.', 'c3', T3),
        Q('m5', 'A deferred tax asset on tax losses requires:', ['Probable future taxable profit', 'Certain profit', 'Board approval', 'Cash reserves'], 0,
          'Convincing evidence is needed after losses. In practice: review forecasts.', 'c3', T3),
        Q('m6', 'Deferred tax on a revaluation surplus is recognised in:', ['OCI', 'Profit or loss', 'Revenue', 'Goodwill'], 0,
          'Tax follows the item. In practice: also applies to OCI hedges.', 'c2', T2),
        Q('m7', 'In the balance sheet, deferred tax is classified as:', ['Non-current', 'Current', 'Split by reversal date', 'Equity'], 0,
          'Always non-current. In practice: current tax is separate.', 'c4', T4),
        Q('m8', 'Tax rates used to measure deferred tax are those:', ['Enacted or substantively enacted by the reporting date', 'Proposed in the budget', 'Expected by management', 'Of the prior year'], 0,
          'Announcements with law-like effect count. In practice: check enactment status.', 'c1', T1),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Plant DTL', 2, 'computation', 'dtl|taxable', nums=[dtl]), S('s2', 'Warranty DTA', 2, 'computation', 'dta|deductible', nums=[dta]), S('s3', 'Losses', 2, 'computation', 'loss', nums=[loss]), S('s4', 'Net', 2, 'computation', 'net', nums=[net])],
          ['Show tax bases.'], ['Creating deferred tax on fines.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Amount', 1.5, 'computation', 'deferred', nums=[oci]), S('s2', 'OCI', 1.5, 'concept', 'oci')],
          ['State the principle.'], ['Charging to P&L.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a temporary difference?', 'The gap between the carrying amount of an asset or liability and its tax base.',
          [P('p1', 'Carrying amount', 5, 'carrying'), P('p2', 'Tax base', 5, 'tax base')], 'c2'),
        V('v2', 'When is a deferred tax asset recognised?', 'Only up to the amount of future taxable profit that is probable and can absorb the deductible difference or loss.',
          [P('p1', 'Probable', 5, 'probable'), P('p2', 'Taxable profit', 5, 'taxable profit')], 'c3'),
        V('v3', 'Where is deferred tax recognised?', 'In the same place as the underlying transaction: profit or loss, OCI or equity.',
          [P('p1', 'Follows the item', 5, 'same|underlying'), P('p2', 'OCI or equity', 5, 'oci|equity')], 'c2'),
        V('v4', 'When can deferred tax assets and liabilities be offset?', 'When one tax authority and one taxpayer are involved, with a legally enforceable right to set off current tax.',
          [P('p1', 'Same authority', 5, 'authority'), P('p2', 'Enforceable right', 5, 'enforceable')], 'c4'),
        V('v5', 'What is the Pillar Two exception?', 'Entities are temporarily exempted, by mandate, from recognising and disclosing deferred tax tied to the global minimum top-up tax.',
          [P('p1', 'Temporary exemption', 5, 'exempt'), P('p2', 'Minimum top-up tax', 5, 'minimum|top-up')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Nimbus Textiles Ltd.', 'difficulty': 'moderate',
              'case': 'Nimbus Textiles Ltd. (tax rate 25%) has gratuity provision ₹80 lakh (deductible on payment), interest receivable ₹20 lakh taxed on receipt, and a subsidiary with undistributed profits of ₹300 lakh that the parent will not distribute in the foreseeable future. It has incurred losses for three years with no firm plans to return to profit.',
              'mcqs': [
                  M('k1a', 'Deferred tax asset arising on the gratuity provision, before the recoverability test (₹ lakh):', ['20', '80', '5', 'Nil'], 0,
                    '80 × 25% deductible difference. In practice: recoverability is doubtful here.', 'moderate', check=20, topic=T2),
                  M('k1b', 'Deferred tax liability on the interest receivable (₹ lakh):', ['5', '20', '15', 'Nil'], 0,
                    'Carrying amount 20, tax base nil → taxable difference. In practice: reverses on receipt.', 'core', check=5, topic=T2),
                  M('k1c', 'Deferred tax on the subsidiary\'s undistributed profits:', ['Not recognised, as the parent controls timing and reversal is not probable', 'Recognised in full', 'Recognised as DTA', 'Recognised in OCI'], 0,
                    'The investment exception applies. In practice: document the dividend policy.', 'core', topic=T3),
                  M('k1d', 'Given the loss history, net DTAs are recognised:', ['Only to the extent of DTLs reversing or convincing evidence', 'In full', 'Never', 'At half value'], 0,
                    'Recent losses demand convincing evidence. In practice: disclose unrecognised amounts.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch07', 1, 'Ind AS 12 "Income Taxes"',
                ['Compute current tax and determine tax bases.',
                 'Identify temporary differences and measure deferred tax.',
                 'Apply the recognition exceptions and recoverability tests.',
                 'Present, offset and disclose income taxes.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': ['fin-p1-ch06-u02'],
                 'exam_tip': 'Use a three-column table — carrying amount, tax base, difference — then apply the rate.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Balance sheet approach: carrying amount vs tax base.',
                             'Taxable differences → DTL; deductible → DTA.',
                             'DTA only if future taxable profit probable.',
                             'Enacted rates; no discounting.',
                             'Tax follows the item: P&L, OCI or equity.'],
                 'remember': ['Pillar Two: no deferred tax recognised or disclosed.'],
                 'traps': ['Deferred tax on permanent differences.']},
                [('Taxable difference', 'DTL'), ('Deductible difference', 'DTA'), ('Discounting', 'Not allowed'), ('Offset', 'Same authority + right')],
                viva, cases)
