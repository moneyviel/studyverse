"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 7 Unit 4 — AS 22 Accounting for Taxes on Income.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch07-u04'
T1 = 'Accounting income, taxable income and tax expense'
T2 = 'Timing and permanent differences'
T3 = 'Recognising deferred tax liabilities and assets'
T4 = 'Measurement, review and tax holidays'
T5 = 'Presentation and disclosure'


def build():
    ck = Checks()
    ti = ck.add('1000000-100000+50000', 'Taxable income (₹)')
    ct = ck.add('950000*25/100', 'Current tax at 25% (₹)')
    dtl = ck.add('100000*25/100', 'Deferred tax liability on the timing difference (₹)')
    te = ck.add('237500+25000', 'Total tax expense (₹)')
    i1 = {'id': 'i1', 'title': 'Current and deferred tax together', 'difficulty': 'core', 'minutes': 8,
          'q': 'Divit Ltd.\'s accounting profit before tax is ₹10,00,000. Book depreciation is ₹2,00,000 and tax depreciation ₹3,00,000. A penalty of ₹50,000 debited to profit and loss is not deductible for tax. Tax rate 25%. Compute current tax, deferred tax and total tax expense.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Taxable income', '10,00,000 − 1,00,000 (extra tax depreciation) + 50,000 (penalty)', inr(ti)],
              ['Current tax', '25% × 9,50,000', inr(ct)],
              ['Deferred tax liability', '25% × 1,00,000 timing difference', inr(dtl)],
              ['Total tax expense', '', inr(te)]], title='AS 22'),
              note('The penalty is a permanent difference — it never reverses — so no deferred tax arises on it.')],
          'checks': list(ck)}

    ck2 = Checks()
    dta = ck2.add('800000*25/100', 'Potential deferred tax asset on carried-forward loss (₹)')
    i2 = {'id': 'i2', 'title': 'Deferred tax on losses', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Ekta Ltd. has business losses of ₹8,00,000 carried forward for tax. Tax rate 25%. Management "reasonably expects" profits next year, but there are no firm orders or contracts. Should a deferred tax asset be recognised? What if signed contracts assure taxable profits of ₹12,00,000 next year?',
          'solution': [table(['Situation', 'Test', 'Result'], [
              ['Only management expectation', 'Virtual certainty with convincing evidence is needed for losses', 'Not recognised'],
              ['Signed contracts assuring profits', 'Virtual certainty supported by convincing evidence', f'Recognise DTA of {inr(dta)}']], title='Prudence for deferred tax assets')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Accounting income is net profit before tax per the statement of profit and loss; taxable income is income on which tax is payable under the tax laws.',
            'Tax expense (or saving) is the sum of the year\'s current tax and its deferred tax charge or credit in profit and loss. Current tax is tax payable on taxable income for the period; deferred tax captures the tax impact of items that are timed differently in the books and the return.',
            'AS 22 follows the matching concept: tax expense is matched with the accounting income of the period, not just the tax actually payable.'],
          'Tax expense in the accounts follows book profit, not just the tax bill.',
          'A company paying low tax because of accelerated tax depreciation still shows a normal tax charge via deferred tax.'),
        C('c2', T2, [
            'Timing differences arise when income or expenses enter accounting income and taxable income in different periods; they originate in one period and reverse in later periods. Examples: depreciation at different rates, expenses allowed for tax only on payment (such as some statutory dues), provisions allowed when paid.',
            'Permanent differences arise in one period and never reverse — for example expenses disallowed forever, such as penalties, or income exempt from tax. No deferred tax arises on them.',
            'Unabsorbed depreciation and carried-forward losses also give rise to timing differences, as they reduce future taxable income.'],
          'Ask whether the difference will reverse; only reversing differences create deferred tax.',
          'Dividend income exempt from tax is a permanent difference; extra tax depreciation is a timing difference.'),
        C('c3', T3, [
            'Deferred tax is recognised for all timing differences, subject to prudence for deferred tax assets.',
            'Deferred tax assets (except for unabsorbed depreciation and losses) are recognised only if there is reasonable certainty of sufficient future taxable income to realise them.',
            'Where there is unabsorbed depreciation or carried-forward business loss, deferred tax assets are recognised only to the extent there is virtual certainty, supported by convincing evidence, of sufficient future taxable income. Profitable firm contracts or orders can be convincing evidence; a projection alone is not.'],
          'Liabilities are always provided; assets need certainty — and losses need near-proof.',
          'A firm with years of losses cannot book a deferred tax asset just because its budget shows profit.'),
        C('c4', T4, [
            'Current tax is measured at the amount expected to be paid, using applicable rates and laws. Deferred tax is measured using rates and laws enacted or substantively enacted by the balance sheet date. Deferred tax is not discounted.',
            'The carrying amount of deferred tax assets is reviewed at each balance sheet date and written down if reasonable (or virtual) certainty no longer exists; the write-down is reversed if certainty returns. Unrecognised deferred tax assets are reassessed each year.',
            'Tax holiday: deferred tax is not recognised on timing differences that originate and reverse within the tax holiday period. Those that originate in the holiday but reverse after it are recognised in the year they originate (using the first-in, first-out approach for reversals).'],
          'Use enacted rates, no discounting, and keep testing the assets.',
          'If a lower tax rate is enacted, the existing deferred tax liability is remeasured downward.'),
        C('c5', T5, [
            'Deferred tax assets and liabilities are shown separately from current tax and from other assets and liabilities. They may be netted only where the law gives the enterprise a right to net them and both arise under one and the same income-tax law.',
            'Current tax assets and liabilities may be set off where there is a legal right and an intention to settle on a net basis.',
            'Disclose the break-up of deferred tax assets and liabilities into major components and, where deferred tax assets on losses are recognised, the nature of the evidence supporting them.'],
          'Keep deferred tax separate from current tax and explain where it comes from.',
          'A company shows "Deferred tax liability (net)" with a note splitting depreciation and other items.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Deferred tax working', 'role': 'Accounts executive',
             'situation': 'You must prepare the year-end tax provision for a company with accelerated tax depreciation, disallowed penalties and brought-forward losses.',
             'steps': ['Reconcile book profit to taxable income.', 'Separate timing from permanent differences.', 'Compute DTL/DTA at enacted rates.', 'Test DTA on losses for virtual certainty.'],
             'takeaway': 'The reconciliation is the backbone of the deferred tax note.'}]

    mcqs = [
        Q('m1', 'Which is a permanent difference?', ['A penalty debited to profit and loss but never allowed for tax', 'Higher tax depreciation', 'Bonus allowed on payment', 'Provision for gratuity allowed on payment'], 0,
          'A permanent difference arises in one period and does not reverse, such as a penalty disallowed forever. The other items are allowed in a different period, so they are timing differences. In practice: no deferred tax on permanent items.', 'c2', T2),
        Q('m2', 'Deferred tax is measured using tax rates:', ['Enacted or substantively enacted by the balance sheet date', 'Expected in five years', 'Of the current year only, always', 'Chosen by management'], 0,
          'AS 22 measures deferred tax using rates and laws enacted or substantively enacted at the balance sheet date. Expected future changes not yet enacted are ignored. In practice: remeasure when a new rate is enacted.', 'c4', T4),
        Q('m3', 'Deferred tax assets on carried-forward business losses are recognised only if there is:', ['Virtual certainty supported by convincing evidence of future taxable income', 'Reasonable certainty', 'A board resolution', 'A tax refund claim'], 0,
          'For unabsorbed depreciation and carried-forward losses, AS 22 requires virtual certainty backed by convincing evidence. Other deferred tax assets need only reasonable certainty. In practice: firm contracts help.', 'c3', T3),
        Q('m4', 'Book depreciation ₹4 lakh, tax depreciation ₹6 lakh, rate 30%. Deferred tax for the year:', ['DTL of ₹60,000', 'DTA of ₹60,000', 'DTL of ₹1,80,000', 'Nil'], 0,
          'Taxable income is lower by ₹2 lakh now and will be higher when the difference reverses, so a liability of 30% × ₹2 lakh = ₹60,000 arises. In practice: track the cumulative difference.', 'c3', T3, 'moderate'),
        Q('m5', 'Deferred tax assets and liabilities are:', ['Not discounted', 'Discounted at the bank rate', 'Discounted at the government bond rate', 'Discounted if over five years'], 0,
          'Under AS 22, deferred tax balances are carried at their full undiscounted amounts. This keeps measurement simple and comparable. In practice: use undiscounted amounts.', 'c4', T4),
        Q('m6', 'Timing differences that originate and reverse within a tax holiday period:', ['Do not give rise to deferred tax', 'Create deferred tax liability', 'Create deferred tax asset', 'Are permanent differences recognised in reserves'], 0,
          'Since no tax is payable during the holiday, differences arising and reversing within it have no tax effect, so no deferred tax is recognised. Those reversing after the holiday are recognised. In practice: schedule reversals.', 'c4', T4),
        Q('m7', 'Deferred tax assets and liabilities may be set off when:', ['There is a legally enforceable right and they relate to the same tax laws', 'Management chooses', 'They are of equal amounts', 'Always'], 0,
          'Offset is allowed only where the enterprise has a legal right to set off and the items relate to income taxes under the same governing laws. Otherwise they are shown gross. In practice: check jurisdiction.', 'c5', T5),
        Q('m8', 'Accounting profit ₹20 lakh; exempt dividend ₹2 lakh; tax rate 25%; no timing differences. Current tax:', ['₹4.5 lakh', '₹5 lakh', '₹5.5 lakh', '₹4 lakh'], 0,
          'Exempt dividend is a permanent difference reducing taxable income to ₹18 lakh; 25% gives current tax of ₹4.5 lakh, and no deferred tax arises. In practice: reconcile the effective rate.', 'c2', T2, 'moderate', check=4.5),
        Q('m9', 'The carrying amount of deferred tax assets is reviewed:', ['At each balance sheet date', 'Every five years', 'Only when losses lapse', 'Never'], 0,
          'AS 22 requires a review at each balance sheet date; the asset is written down if certainty of future taxable income no longer exists, and the write-down reversed if it returns. In practice: document the evidence yearly.', 'c4', T4),
        Q('m10', 'Tax expense in the statement of profit and loss is:', ['Current tax plus deferred tax', 'Current tax only', 'Advance tax paid', 'Deferred tax only'], 0,
          'Under AS 22, tax expense is the year\'s current tax plus its deferred tax charge or credit, so that tax matches book profit. In practice: show both lines.', 'c1', T1),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Taxable income', 1.5, 'computation', 'taxable', nums=[ti]),
           S('s2', 'Current tax', 1, 'computation', 'current', nums=[ct]),
           S('s3', 'Deferred tax on timing difference only', 1.5, 'computation', 'timing', nums=[dtl]),
           S('s4', 'Total', 1, 'computation', 'total', nums=[te])],
          ['Separate permanent and timing items.'], ['Creating deferred tax on the penalty.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Virtual certainty test', 2, 'concept', 'virtual'),
           S('s2', 'DTA amount', 2, 'computation', 'recognise', nums=[dta])],
          ['Name the right test for losses.'], ['Using reasonable certainty for losses.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What are timing differences?', 'Gaps between book profit and taxable income that begin in one year and later reverse in one or more following years.',
          [P('p1', 'Begin in one year', 5, 'begin|one year'), P('p2', 'Reverse', 5, 'revers')], 'c2'),
        V('v2', 'What are permanent differences?', 'Differences that arise in one period and never reverse later, such as disallowed penalties or exempt income.',
          [P('p1', 'One period', 5, 'one period|arise'), P('p2', 'Examples', 5, 'penalt|exempt')], 'c2'),
        V('v3', 'What test applies to deferred tax assets on losses?', 'Virtual certainty, supported by convincing evidence, of sufficient future taxable income.',
          [P('p1', 'Virtual certainty', 6, 'virtual'), P('p2', 'Convincing evidence', 4, 'convincing')], 'c3'),
        V('v4', 'Which tax rates measure deferred tax?', 'Rates and laws enacted or substantively enacted by the balance sheet date.',
          [P('p1', 'Enacted', 6, 'enacted'), P('p2', 'Balance sheet date', 4, 'balance sheet')], 'c4'),
        V('v5', 'What is tax expense?', 'The year\'s current tax plus its deferred tax charge or credit, as shown in profit and loss.',
          [P('p1', 'Current tax', 5, 'current'), P('p2', 'Deferred tax', 5, 'deferred')], 'c1'),
    ]

    cases = [{'id': 'k1', 'title': 'Falguni Plastics Ltd.', 'difficulty': 'moderate',
              'case': 'Falguni Plastics Ltd. (tax rate 25%) has a cumulative excess of tax depreciation over book depreciation of ₹40 lakh at year end, and a provision for leave encashment of ₹8 lakh deductible only on payment. In the year a new law, enacted before the balance sheet date, cuts the tax rate to 22% from next year.',
              'mcqs': [
                  M('k1a', 'Deferred tax liability on depreciation, using the enacted future rate:', ['₹8.8 lakh', '₹10 lakh', '₹1.76 lakh', '₹2 lakh'], 0,
                    'The difference will reverse when the 22% rate applies, and the rate is already enacted: 22% × ₹40 lakh = ₹8.8 lakh. In practice: remeasure the opening balance too.', 'moderate', check=8.8, topic=T4),
                  M('k1b', 'The leave encashment provision gives rise to:', ['A deferred tax asset, subject to reasonable certainty', 'A deferred tax liability', 'A permanent difference', 'Nothing'], 0,
                    'The expense is in book profit now but deductible later, so future taxable income will be lower: a deferred tax asset arises, recognised with reasonable certainty of future taxable income. In practice: compute at 22%.', 'core', topic=T3),
                  M('k1c', 'Deferred tax asset on the leave provision at 22%:', ['₹1.76 lakh', '₹2 lakh', '₹8 lakh', '₹1.6 lakh'], 0,
                    'At the enacted rate that will apply on reversal, the asset is 22% × ₹8 lakh = ₹1.76 lakh. In practice: present it net with the DTL only if offset conditions are met.', 'moderate', check=1.76, topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch07', 4, 'Accounting Standard 22 Accounting for Taxes on Income',
                ['Distinguish accounting income, taxable income and tax expense.',
                 'Identify timing and permanent differences.',
                 'Recognise and measure deferred tax assets and liabilities, including on losses and tax holidays.',
                 'Present and disclose deferred taxes.'],
                {'difficulty': 'hard', 'minutes': {'learn': 30, 'practice': 35}, 'prereq': ['int-p1-ch07-u03'],
                 'exam_tip': 'Draw up a reconciliation from book profit to taxable income and mark each item T (timing) or P (permanent).'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Tax expense = current + deferred.', 'Timing differences reverse; permanent do not.',
                             'DTL always; DTA with reasonable certainty; on losses, virtual certainty with convincing evidence.',
                             'Enacted rates; no discounting; review each year.', 'Tax holiday reversals within the holiday ignored.', 'Separate presentation; offset only with legal right and same laws.'],
                 'remember': ['Projections alone are not convincing evidence.'],
                 'traps': ['No deferred tax on permanent differences.']},
                [('Tax expense', 'Current + deferred'), ('DTA on losses', 'Virtual certainty'), ('Rates', 'Enacted at BS date')],
                viva, cases)
