"""CA Foundation · Paper 1 Accounting · Chapter 1 Theoretical Framework · Unit 4 Contingent Assets and Contingent Liabilities.
Original explanations, figures and questions (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M

UID = 'fnd-p1-ch01-u04'


def build():
    # ---------------- Illustration 1: year-end review of Orion Ltd ----------------
    c1 = Checks()
    prov = c1.add('900000', 'Provision for the customer suit (best estimate)')
    cl = c1.add('600000+2500000+400000', 'Contingent liabilities disclosed in notes')
    asset = c1.add('300000', 'Insurance claim admitted in writing — recognised')
    eff = c1.add('-900000+300000', 'Net effect on profit for the year')
    rev_tbl = table(['Item', 'Amount (₹)', 'Assessment', 'Treatment', 'Recognised in books (₹)', 'Disclosed in notes (₹)'], [
        ['Customer suit for ₹12,00,000; lawyers say loss is probable, best estimate ₹9,00,000', '12,00,000', 'Present obligation, outflow probable, reliable estimate', 'Provision', '9,00,000', '0'],
        ['GST demand under appeal; company expects to win', '6,00,000', 'Possible obligation; outflow not probable', 'Contingent liability', '0', '6,00,000'],
        ['Guarantee for a group company\'s bank loan; borrower is paying regularly', '25,00,000', 'Obligation depends on a future default', 'Contingent liability', '0', '25,00,000'],
        ['Bills receivable discounted with the bank, not yet due', '4,00,000', 'Liability arises only if the drawee dishonours', 'Contingent liability', '0', '4,00,000'],
        ['Company\'s claim against a supplier; outcome uncertain, inflow probable', '8,00,000', 'Possible asset', 'Contingent asset — not recognised; mentioned in Board\'s report', '0', '0'],
        ['Insurance claim admitted in writing; payment due next month', '3,00,000', 'Inflow virtually certain', 'Asset and income recognised', '3,00,000', '0'],
        ['Ex-employee\'s claim lawyers call baseless', '50,000', 'Possibility of outflow remote', 'Nothing — neither provided nor disclosed', '0', '0'],
        ['Total', '58,50,000', '', '', '12,00,000', inr(cl)],
    ], num=[1, 4, 5], total=True, title='Orion Ltd — year-end review (31 March 2027)')
    j1 = journal([
        je('Mar 31', [('Legal Claims Expense A/c', 900000)], [('Provision for Legal Claims A/c', 900000)], 'Being provision made for the probable loss in the customer suit'),
        je('Mar 31', [('Insurance Claim Receivable A/c', 300000)], [('Insurance Claim (Income) A/c', 300000)], 'Being insurance claim admitted in writing recognised as virtually certain'),
    ], 'Journal of Orion Ltd', 'j1')

    # ---------------- Illustration 2: a contingent liability over three years ----------------
    c2 = Checks()
    extra = c2.add('820000-750000', 'Further loss charged in Year 3 on settlement')
    c2.add('750000+70000', 'Total paid on settlement')
    life_tbl = table(['Year ending', 'Situation', 'Treatment', 'Charged to P&L (₹)'], [
        ['31 Mar 2026', 'Supplier sues for ₹10,00,000; lawyers think the company will probably win', 'Disclose ₹10,00,000 as a contingent liability', '0'],
        ['31 Mar 2027', 'New evidence: loss now probable, best estimate ₹7,50,000', 'Recognise a provision in this year', '7,50,000'],
        ['31 Mar 2028', 'Case settled for ₹8,20,000 paid by cheque', 'Use the provision; charge the shortfall', inr(extra)],
        ['Total', '', '', '8,20,000'],
    ], num=[3], total=True, title='Kiran Pumps Ltd — one claim, three years')
    j2 = journal([
        je('Mar 31, 2027', [('Legal Claims Expense A/c', 750000)], [('Provision for Legal Claims A/c', 750000)], 'Being provision recognised as outflow has become probable'),
        je('2027-28', [('Provision for Legal Claims A/c', 750000), ('Legal Claims Expense A/c', extra)], [('Bank A/c', 820000)], 'Being claim settled; provision utilised and shortfall charged'),
    ], 'Journal of Kiran Pumps Ltd', 'j2')

    # ---------------- Distinctions ----------------
    lia_tbl = table(['Basis', 'Liability', 'Contingent liability'], [
        ['Nature', 'Present obligation arising from past events', 'Possible obligation, or a present obligation that fails the recognition tests'],
        ['Outflow of resources', 'Settlement will result in an outflow', 'Outflow not probable, or amount cannot be measured reliably'],
        ['Accounting', 'Recognised in the balance sheet', 'Not recognised; disclosed by way of notes (unless remote)'],
        ['Examples', 'Trade payables, loans, outstanding expenses', 'Claims not acknowledged as debts, guarantees for third parties, bills discounted, disputed statutory dues'],
    ], title='Liability vs contingent liability')
    prov_tbl = table(['Basis', 'Provision', 'Contingent liability'], [
        ['Nature', 'Present liability of uncertain amount that can be measured reliably by substantial estimation', 'Possible obligation which may or may not turn into an actual liability, depending on uncertain future events'],
        ['Recognition criteria', 'Meets them', 'Does not meet them'],
        ['Conditions', 'Present obligation from past events, outflow probable, reliable estimate possible', 'Outflow not probable, or amount cannot be estimated reliably'],
        ['Management\'s estimate', 'Settlement probably needs an outflow → provision recognised', 'Outflow less likely → only disclosed'],
        ['Shown in', 'Balance sheet (and charge to P&L)', 'Notes to accounts'],
    ], title='Provision vs contingent liability')

    concepts = [
        {'id': 'c1', 'title': 'Contingent asset',
         'body': ['A contingent asset is a possible asset, arising out of past events, whose existence can be confirmed only when one or more uncertain future events, not fully under the enterprise\'s control, happen or fail to happen. It usually comes from unplanned or unexpected events that give a possibility of inflow of economic benefits — for example, a claim the enterprise is pursuing in court with an uncertain result.',
                  'Treatment: a contingent asset is not recognised in the accounts — recognising it could mean recording income that may never be realised (prudence and the accounting standards). It need not be disclosed in the financial statements; it is commonly mentioned in the approving authority\'s report (the Board of Directors\' report for a company) if an inflow is probable.',
                  'Contingent assets are reviewed continually. When the inflow becomes virtually certain, it is no longer contingent: both the asset and the income it brings are booked in the period when that change takes place.'],
         'analogy': 'A lottery ticket you have bought: you may win, but you do not add the prize to your bank balance until the result is declared and the money is certain.',
         'work': 'Clients often want a pending insurance or legal claim shown as income. The CA must hold back until it is virtually certain — for instance, the insurer has admitted the claim in writing.'},
        {'id': 'c2', 'title': 'Contingent liability',
         'body': ['A contingent liability is (a) a possible obligation, arising out of past events, whose existence can be confirmed only when uncertain future events, not fully under the enterprise\'s control, happen or fail to happen; or (b) a present obligation arising from past events that is not recognised because an outflow of resources is not probable, or because the amount cannot be estimated reliably.',
                  'Treatment: not recognised in the balance sheet, but disclosed in the notes to accounts — unless the possibility of an outflow is remote, in which case nothing is disclosed. Contingent liabilities are reassessed continually; if an outflow becomes probable, a provision is recognised in the period in which the probability changes (except in the extremely rare case where no reliable estimate can be made).',
                  'Common examples: claims made against the enterprise that it has not accepted as debts, guarantees it has given for third parties, liability on bills discounted, and statutory dues under dispute.'],
         'analogy': 'Standing guarantor for a friend\'s loan: you owe nothing today, but you will have to pay if your friend defaults. You should tell anyone assessing your finances about it.',
         'work': 'The "contingent liabilities" note is one of the first things a banker or analyst reads in an annual report — a large guarantee or tax dispute can change the credit decision.'},
        {'id': 'c3', 'title': 'Liability versus contingent liability',
         'body': ['A liability is a present financial obligation arising from past events, whose settlement will cause an outflow of resources embodying economic benefits. It is recognised in the balance sheet.',
                  'A contingent liability lacks one of these: either the outflow is not probable, or the amount cannot be measured reliably (or the obligation is only possible). It is disclosed in notes, not recognised. The line between the two often depends on management\'s judgement.'],
         'blocks': [lia_tbl],
         'analogy': 'A bill you have received is a liability. A bill that may arrive if a dispute goes against you is a contingent liability.',
         'work': 'Auditors send confirmation letters to the client\'s lawyers to understand pending cases and judge whether they are liabilities, provisions or merely contingent.'},
        {'id': 'c4', 'title': 'Provision versus contingent liability',
         'body': ['Provision means an amount written off or retained to provide for depreciation, renewal or fall in value of assets, or retained to provide for a known liability whose amount cannot be determined with substantial accuracy.',
                  'A provision is recognised when (a) there is a present obligation from past events, (b) an outflow of resources is probable, and (c) a reliable estimate of the amount can be made. If any test fails, there is no provision — the item is disclosed as a contingent liability (unless remote).',
                  'Example: an excise penalty under appeal. If management thinks it will probably have to pay, it recognises a provision; if it expects the appeal to succeed and payment is less likely, it discloses a contingent liability.'],
         'blocks': [prov_tbl],
         'analogy': 'An umbrella you carry because rain is forecast (provision) versus a note in your diary that it might rain later in the week (contingent liability).',
         'work': 'Warranty provisions, provisions for pending litigation and for doubtful debts are all estimates that auditors test. Over- or under-providing directly changes profit.'},
    ]

    illustrations = [
        {'id': 'i1', 'title': 'Year-end review of claims, guarantees and disputes', 'difficulty': 'moderate', 'minutes': 14,
         'q': 'Orion Ltd is finalising accounts for the year ending 31 March 2027. (a) A customer has sued it for ₹12,00,000; its lawyers think a loss is probable and estimate it at ₹9,00,000. (b) A GST demand of ₹6,00,000 is under appeal and the company expects to win. (c) It has guaranteed a group company\'s bank loan of ₹25,00,000; the borrower is paying regularly. (d) Bills receivable of ₹4,00,000 discounted with the bank are not yet due. (e) It has a claim of ₹8,00,000 against a supplier; the outcome is uncertain but an inflow is probable. (f) An insurer has admitted a claim of ₹3,00,000 in writing, payable next month. (g) An ex-employee\'s claim of ₹50,000 is described by lawyers as baseless. State the treatment of each item, give the journal entries required and the effect on profit.',
         'solution': [rev_tbl, j1,
                      wn('Totals', f'Provision recognised ₹{inr(prov)}; asset recognised ₹{inr(asset)}; contingent liabilities disclosed 6,00,000 + 25,00,000 + 4,00,000 = ₹{inr(cl)}. Net effect on profit = −9,00,000 + 3,00,000 = −₹{inr(-eff)}.'),
                      note('The contingent asset in (e) is not shown in the financial statements; because an inflow is probable, it may be mentioned in the Board\'s report.')],
         'checks': c1},
        {'id': 'i2', 'title': 'When a contingent liability turns into a provision', 'difficulty': 'moderate', 'minutes': 10,
         'q': 'Kiran Pumps Ltd was sued by a supplier for ₹10,00,000 in 2025-26; its lawyers then thought the company would probably win. In 2026-27 new evidence made a loss probable, with a best estimate of ₹7,50,000. In 2027-28 the case was settled for ₹8,20,000, paid by cheque. Show the treatment in each year and the journal entries.',
         'solution': [life_tbl, j2,
                      wn('Why no entry in 2025-26', 'Outflow was not probable, so the claim failed the recognition test — it was only disclosed as a contingent liability.'),
                      wn('Settlement', f'Provision of ₹7,50,000 is used; the shortfall 8,20,000 − 7,50,000 = ₹{inr(extra)} is charged in 2027-28, the year in which it becomes known. Earlier years are not reopened — the earlier figure was a reasonable estimate.')],
         'checks': c2},
        {'id': 'i3', 'title': 'Liability, provision or contingent liability?', 'difficulty': 'core', 'minutes': 6,
         'q': 'Classify: (1) electricity bill for March received but unpaid; (2) estimated warranty repairs on goods sold this year, based on past experience; (3) a demand from the income-tax department that the company is contesting and expects to win; (4) a claim by a neighbour that the company considers frivolous with only a remote chance of success.',
         'solution': [table(['Item', 'Classification', 'Treatment'], [
             ['(1) March electricity bill unpaid', 'Liability', 'Recognise as outstanding expense'],
             ['(2) Warranty repairs estimate', 'Provision', 'Present obligation from sales made, outflow probable, reliable estimate from past data — recognise'],
             ['(3) Disputed tax demand, expected to win', 'Contingent liability', 'Disclose in notes'],
             ['(4) Frivolous claim, remote', 'Neither', 'No provision, no disclosure'],
         ])]},
    ]

    jobs = [
        {'id': 'j1', 'title': 'Reading the lawyer\'s confirmation letter', 'role': 'Audit senior on a company audit',
         'situation': 'The company\'s legal counsel lists three cases: a customer claim of ₹40 lakh ("loss probable, likely settlement ₹25 lakh"), a labour dispute of ₹8 lakh ("unlikely to succeed"), and a trademark suit filed by the company for ₹60 lakh ("strong case").',
         'steps': ['Customer claim: present obligation, probable outflow, reliable estimate → check that a provision of about ₹25 lakh is recognised.',
                   'Labour dispute: outflow not probable → check that it is disclosed as a contingent liability (not provided).',
                   'Trademark suit by the company: a contingent asset — must not be recognised as income; it may be mentioned in the Board\'s report if an inflow is probable.',
                   'Document the lawyer\'s opinion and management\'s assessment in the working papers.'],
         'takeaway': 'Probability decides everything: probable outflow → provision; possible → disclose; remote → ignore; and gains wait until virtually certain.',
         'think': 'If the company\'s trademark suit were decided in its favour after the year end and the defendant paid in full, would the asset be recognised?',
         'answer': 'Once the inflow is virtually certain, the asset and income are recognised in the period in which that change occurs — not by pretending it was certain earlier.'},
        {'id': 'j2', 'title': 'Explaining a guarantee to a promoter', 'role': 'CA advising a family-owned company',
         'situation': 'The promoter has made the company guarantee a ₹2 crore loan of his cousin\'s firm and asks why it must appear in the accounts when "nothing has been paid".',
         'steps': ['Explain that a guarantee is a possible obligation depending on a future default — a contingent liability.',
                   'It is not recognised as a liability, but it must be disclosed in the notes so that lenders and shareholders know the risk.',
                   'If the cousin\'s firm starts defaulting and payment becomes probable, a provision will be needed.'],
         'takeaway': 'Disclosure protects users from hidden risks; a guarantee can turn into a real liability overnight.'},
    ]

    mcqs = [
        {'id': 'm1', 'q': 'A contingent asset is usually:', 'options': ['Not recognised in the financial statements', 'Recognised as soon as the claim is filed', 'Shown as a current asset at the claimed amount', 'Credited to capital reserve'], 'answer': 0, 'explain': 'A contingent asset is a possible asset whose existence depends on uncertain future events, such as a pending claim. It is not recognised, because recording it could mean showing income that may never be received; it is recognised only when the inflow becomes virtually certain. The trap is recognising it when the claim is filed — filing a claim does not mean it will succeed. In practice: a company that has sued a supplier for damages does not book the claim as income until it wins or the supplier admits it.', 'topic': 'Contingent Asset', 'concept': 'c1', 'difficulty': 'core'},
        {'id': 'm2', 'q': 'Where is a contingent asset with a probable inflow normally disclosed?', 'options': ['In the report of the approving authority (Board\'s report)', 'In the notes to accounts as a contingent asset', 'On the face of the balance sheet', 'In the profit and loss account'], 'answer': 0, 'explain': "A contingent asset is not disclosed in the financial statements; where an inflow is probable, it is usually mentioned in the report of the approving authority, such as the Board's report of a company. The tempting option is the notes to accounts — that is where contingent liabilities are disclosed, not contingent assets. The asymmetry follows prudence: possible losses are disclosed, possible gains are not. In practice: a company expecting to win an arbitration award may mention it in the directors' report.", 'topic': 'Contingent Asset', 'concept': 'c1', 'difficulty': 'moderate'},
        {'id': 'm3', 'q': 'A contingent liability is normally:', 'options': ['Disclosed in notes, not recognised', 'Recognised in the balance sheet', 'Ignored completely', 'Charged to the profit and loss account'], 'answer': 0, 'explain': 'A contingent liability is a possible obligation depending on uncertain future events, or a present obligation where outflow is not probable or cannot be measured reliably. It is not recognised in the balance sheet but is disclosed in the notes to accounts, unless the chance of outflow is remote. The tempting option, recognising it in the balance sheet, applies only to liabilities and provisions. In practice: Indian annual reports have a note listing contingent liabilities such as disputed tax demands and guarantees.', 'topic': 'Contingent Liabilities', 'concept': 'c2', 'difficulty': 'core'},
        {'id': 'm4', 'q': 'Which of these is NOT a contingent liability?', 'options': ['Outstanding salary for March', 'Guarantee given for a third party\'s loan', 'Bills discounted but not yet matured', 'Claims against the company not acknowledged as debts'], 'answer': 0, 'explain': 'Outstanding salary for March is a definite present obligation for services already received, with a known amount, so it is a liability, not a contingent liability. The other three depend on uncertain future events: a guarantee is payable only if the borrower defaults, discounted bills only if the drawee fails to pay, and unacknowledged claims only if they succeed. The tempting option is bills discounted, which look settled but still carry a risk. In practice: outstanding salaries appear under current liabilities in every year-end balance sheet.', 'topic': 'Distinction between Contingent Liabilities and Liabilities', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm5', 'q': 'A provision is recognised when there is a present obligation from past events, a probable outflow, and:', 'options': ['A reliable estimate of the amount can be made', 'The amount is exactly known', 'The lawyer has filed a reply', 'The board has approved a dividend'], 'answer': 0, 'explain': "A provision is recognised when three conditions are met: a present obligation from a past event, a probable outflow of resources, and a reliable estimate of the amount. The tempting option, 'the amount is exactly known', is wrong because a provision by nature involves estimation; if the amount were exact, it would be a liability. In practice: companies provide for product warranty costs every year on the basis of past claim experience, without knowing the exact amount of future claims.", 'topic': 'Distinction between Contingent Liabilities and Provisions', 'concept': 'c4', 'difficulty': 'core'},
        {'id': 'm6', 'q': 'If the possibility of an outflow on a claim is remote, the claim is:', 'options': ['Neither provided for nor disclosed', 'Provided for at the full amount', 'Disclosed as a contingent liability', 'Recognised as a liability'], 'answer': 0, 'explain': 'When the possibility of an outflow is remote, the item is neither recognised as a provision nor disclosed as a contingent liability; reporting it would clutter the accounts with claims that will almost certainly never cost anything. The tempting option, disclosing it as a contingent liability, applies only when the outflow is possible but not probable — not when it is remote. In practice: companies facing obviously frivolous legal notices do not list them in the contingent liabilities note.', 'topic': 'Contingent Liabilities', 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm7', 'q': 'A penalty of ₹5,00,000 is under appeal. Management believes the appeal will probably fail. The company should:', 'options': ['Recognise a provision of ₹5,00,000', 'Disclose a contingent liability of ₹5,00,000', 'Show a contingent asset', 'Make no entry until the appeal is decided'], 'answer': 0, 'explain': 'There is a present obligation (the penalty already imposed), the appeal is expected to fail so outflow is probable, and the amount of ₹5,00,000 can be estimated reliably. All three conditions are met, so a provision of ₹5,00,000 is recognised. The tempting option, disclosure as a contingent liability, fits only when outflow is not probable. In practice: Indian companies often provide for tax or GST penalties under appeal when legal advice says the appeal is likely to fail.', 'topic': 'Distinction between Contingent Liabilities and Provisions', 'concept': 'c4', 'difficulty': 'moderate'},
        {'id': 'm8', 'q': 'An item previously disclosed as a contingent liability becomes probable. A provision is recognised in:', 'options': ['The period in which the change in probability occurs', 'The period in which the claim was first made, by reopening it', 'The period in which payment is finally made', 'No period — it stays a contingent liability'], 'answer': 0, 'explain': "Contingent liabilities are reassessed at each balance sheet date. When an outflow that was earlier not probable becomes probable, a provision is recognised in the period in which the change in probability occurs; earlier accounts are not reopened, because they were correct on the information then available. The tempting option is reopening the period of the original claim. In practice: when a long-running tax case turns against a company, it books the provision in that quarter's results.", 'topic': 'Contingent Liabilities', 'concept': 'c2', 'difficulty': 'moderate'},
        {'id': 'm9', 'q': 'Claim filed by a company for ₹6,00,000 and an insurer\'s written admission of another claim of ₹2,50,000 (to be paid next month). The amount recognised as an asset is:', 'options': ['₹2,50,000', '₹8,50,000', '₹6,00,000', 'Nil'], 'answer': 0, 'check': '250000', 'explain': "The insurer's written admission of ₹2,50,000 makes that inflow virtually certain, so it is recognised as an asset (a claim receivable). The pending claim of ₹6,00,000 is only a contingent asset and is not recognised. The tempting ₹8,50,000 adds both, treating a mere filed claim as if it were certain. In practice: companies book insurance claims for fire or flood losses as receivable only after the surveyor's assessment is accepted and the insurer confirms.", 'topic': 'Contingent Asset', 'concept': 'c1', 'difficulty': 'hard'},
        {'id': 'm10', 'q': 'Disputed claims: (a) ₹3,00,000 — loss probable, estimate ₹2,40,000; (b) ₹1,80,000 — loss not probable; (c) ₹90,000 — remote. The amount to be disclosed as contingent liability is:', 'options': ['₹1,80,000', '₹2,70,000', '₹4,20,000', '₹5,70,000'], 'answer': 0, 'check': '180000', 'explain': 'Claim (a): loss probable and estimable, so a provision of ₹2,40,000 is recognised, not disclosed as contingent. Claim (b): outflow not probable but possible, so ₹1,80,000 is a contingent liability. Claim (c): remote, so ignored. Disclosed contingent liability = ₹1,80,000. The tempting ₹2,70,000 wrongly adds the remote claim (c). In practice: legal teams classify each pending case as probable, possible or remote so that accountants know whether to provide, disclose or ignore it.', 'topic': 'Distinction between Contingent Liabilities and Provisions', 'concept': 'c4', 'difficulty': 'hard'},
        {'id': 'm11', 'q': 'Whether an item is a liability or only a contingent liability is usually decided by:', 'options': ['The judgement of management', 'The amount involved', 'The age of the claim', 'The legal form of the creditor'], 'answer': 0, 'explain': "Deciding whether an outflow is probable and can be measured reliably requires judgement, so whether an item is a liability or only a contingent liability is usually decided by management's judgement, supported by evidence such as legal opinions. The tempting option, the amount involved, is irrelevant — a small definite obligation is a liability while a large doubtful claim may be contingent. In practice: auditors review management's assessment and obtain lawyers' confirmations for significant cases.", 'topic': 'Distinction between Contingent Liabilities and Liabilities', 'concept': 'c3', 'difficulty': 'core'},
        {'id': 'm12', 'q': 'Provision for doubtful debts is an example of an amount retained to provide for:', 'options': ['Diminution in the value of an asset', 'A contingent asset', 'A capital receipt', 'A known liability of exact amount'], 'answer': 0, 'explain': "Provisions are amounts set aside out of profits to cover a fall in asset values (such as depreciation or bad debts) or a known liability whose exact amount cannot yet be measured. Provision for doubtful debts reduces receivables to the amount expected to be collected — a diminution in asset value. The tempting option, 'a known liability of exact amount', describes a liability, not a provision. In practice: banks and NBFCs make large provisions for loans that may not be recovered.", 'topic': 'Distinction between Contingent Liabilities and Provisions', 'concept': 'c4', 'difficulty': 'moderate'},
    ]

    questions = [
        {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'table',
         'q': 'Distinguish between a provision and a contingent liability, and give an example showing how the same event may be treated either way.',
         'model': [prov_tbl, p('Example: a company appeals against a penalty of ₹4,00,000. If management estimates that it will probably have to pay, it recognises a provision of ₹4,00,000; if it expects to win and payment is less likely, it discloses ₹4,00,000 as a contingent liability in the notes.')],
         'scheme': [
             {'id': 's1', 'pt': 'Provision = present liability of uncertain amount, reliably estimable', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Contingent liability = possible obligation depending on uncertain future events (or fails tests)', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Recognition criteria (present obligation, probable outflow, reliable estimate) met vs not met', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Provision recognised in balance sheet; contingent liability disclosed in notes', 'm': 1, 'skill': 'concept'},
             {'id': 's5', 'pt': 'Example showing both treatments based on management\'s estimate', 'm': 1, 'skill': 'application'},
         ],
         'remarks': ['Candidates often describe a provision only as "an amount set aside" without the recognition conditions — this costs the third mark.', 'The example must show the switch between the two treatments.'],
         'mistakes': ['Saying contingent liabilities are shown on the liabilities side.', 'Saying provisions are made only for depreciation.'],
         'tips': ['A four-row table plus a two-line example is ideal.']},
        {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
         'q': 'Vega Ltd, year ending 31 March 2027: (i) a customer\'s suit for ₹15,00,000 — lawyers estimate a probable loss of ₹11,00,000; (ii) guarantee given for a supplier\'s overdraft of ₹20,00,000; (iii) a sales-tax demand of ₹3,50,000 under appeal, appeal likely to succeed; (iv) the company\'s own claim against a contractor for ₹7,00,000, outcome uncertain; (v) a claim of ₹40,000 by a former agent, which lawyers say has no chance. State the treatment of each item, the amount recognised as provision and the total contingent liabilities to be disclosed.',
         'model': [table(['Item', 'Treatment', 'Provision (₹)', 'Contingent liability (₹)'], [
             ['(i) Customer suit', 'Provision — probable outflow, reliable estimate', '11,00,000', '0'],
             ['(ii) Guarantee for supplier', 'Contingent liability — depends on future default', '0', '20,00,000'],
             ['(iii) Sales-tax demand under appeal', 'Contingent liability — outflow not probable', '0', '3,50,000'],
             ['(iv) Own claim against contractor', 'Contingent asset — not recognised; may be mentioned in Board\'s report if inflow probable', '0', '0'],
             ['(v) Former agent\'s claim', 'Remote — no provision, no disclosure', '0', '0'],
             ['Total', '', '11,00,000', '23,50,000'],
         ], num=[2, 3], total=True)],
         'scheme': [
             {'id': 's1', 'pt': 'Provision of ₹11,00,000 for (i), with reason', 'm': 1.5, 'skill': 'application'},
             {'id': 's2', 'pt': 'Guarantee disclosed as contingent liability', 'm': 1, 'skill': 'classification'},
             {'id': 's3', 'pt': 'Tax demand under appeal disclosed as contingent liability', 'm': 1, 'skill': 'classification'},
             {'id': 's4', 'pt': 'Own claim = contingent asset, not recognised', 'm': 1, 'skill': 'classification'},
             {'id': 's5', 'pt': 'Remote claim ignored; totals ₹11,00,000 and ₹23,50,000', 'm': 1.5, 'skill': 'computation'},
         ],
         'remarks': ['Most errors come from providing the full ₹15,00,000 claimed instead of the best estimate.', 'Several candidates disclose the remote claim — it should be left out.'],
         'mistakes': ['Recognising the contractor claim as income.', 'Adding the provision amount to contingent liabilities as well.'],
         'tips': ['Columns: Item | Treatment | Provision | Contingent liability — then total each column.']},
        {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
         'q': 'What is a contingent asset? How is it treated in the accounts, and when does it cease to be contingent?',
         'model': [p('A contingent asset is a possible asset, arising out of past events, whose existence will be settled only when certain uncertain future events, which the enterprise does not fully control, either take place or do not — for example, a claim being pursued in court.'),
                   p('Treatment: it is not recognised, because that could mean recognising income that may never be realised. It need not be disclosed in the financial statements; it is commonly mentioned in the approving authority\'s report (Board of Directors for a company) if an inflow of economic benefits is probable.'),
                   p('It is assessed continually. When the inflow becomes virtually certain, it is no longer a contingent asset — both the asset and the income it brings are booked in the period when that change takes place.')],
         'scheme': [
             {'id': 's1', 'pt': 'Definition with example', 'm': 1, 'skill': 'concept'},
             {'id': 's2', 'pt': 'Not recognised (prudence)', 'm': 1, 'skill': 'concept'},
             {'id': 's3', 'pt': 'Disclosure in Board\'s/approving authority\'s report if inflow probable', 'm': 1, 'skill': 'concept'},
             {'id': 's4', 'pt': 'Recognised when virtually certain, in the period of change', 'm': 1, 'skill': 'concept'},
         ],
         'remarks': ['Many answers wrongly say contingent assets are disclosed in notes like contingent liabilities.'],
         'mistakes': ['Treating "probable" as enough for recognition — the test is "virtually certain".'],
         'tips': ['Three short paragraphs: meaning, treatment, when it stops being contingent.']},
    ]

    viva = [
        V('v1', 'What is a contingent asset and how is it treated?',
          'A contingent asset is a possible asset, arising out of past events, whose existence will be confirmed only by uncertain future events which the enterprise does not fully control, like a claim pending in court. It is not recognised in the accounts. It is usually disclosed in the Board\'s report if an inflow is probable, and it is recognised only when the inflow becomes virtually certain.',
          [P('p1', 'Possible asset from past events, confirmed by uncertain future events', 3, 'possible|uncertain|may or may not|depend|future event|pending|claim', min=1),
           P('p2', 'Not recognised in the accounts', 3, ALT('{n} recognis', '{n} record', '{n} shown', '{n} book', '{n} account', n=('not', 'no', 'never', 'isn t', 'aren t', 'shouldn t', 'don t', 'without'))),
           P('p3', 'Disclosed in the Board\'s (approving authority\'s) report if inflow probable', 2, 'board|director|approving authority|report'),
           P('p4', 'Recognised when virtually certain', 2, 'virtually certain|virtual certain|certain|confirm|sure')], 'c1'),
        V('v2', 'Define a contingent liability.',
          'A contingent liability is a possible obligation, arising out of past events, whose existence will be confirmed only by uncertain future events which the enterprise does not fully control. It can also be a present obligation that is not recognised because an outflow of resources is not probable or because the amount cannot be estimated reliably.',
          [P('p1', 'Possible obligation from past events', 3, 'possible|may arise|might|potential|may or may not', 'obligation|liabilit|pay', 'past event|past', min=2),
           P('p2', 'Confirmed only by uncertain future events not wholly in control', 3, 'uncertain|future event|future|depend|not wholly|outside control|not in control|beyond control', min=1),
           P('p3', 'Or present obligation not recognised: outflow not probable or no reliable estimate', 4, 'present obligation|current obligation|existing obligation', 'not probable|improbable|unlikely|less likely|reliabl|cannot be estimat|can t be estimat|cannot be measur|not measur|no reliable|estimate', min=1)], 'c2'),
        V('v3', 'How is a contingent liability shown in the financial statements?',
          'A contingent liability is not recognised in the balance sheet. It is disclosed by way of notes to the accounts, unless the possibility of an outflow is remote, in which case it is not disclosed. If the outflow later becomes probable, a provision is recognised.',
          [P('p1', 'Not recognised in the balance sheet', 4, ALT('{n} recognis', '{n} record', '{n} shown in balance', '{n} show in balance', '{n} part of balance', '{n} book', '{n} included', n=('not', 'no', 'never', 'isn t', 'aren t', 'don t', 'shouldn t'))),
           P('p2', 'Disclosed in notes to accounts', 4, 'note|footnote|disclos'),
           P('p3', 'Unless remote; provision if it becomes probable', 2, 'remote|unlikely|probable|provision', min=1)], 'c2'),
        V('v4', 'Distinguish between a provision and a contingent liability.',
          'A provision is a present liability of uncertain amount that can be measured reliably by estimation; it meets the recognition criteria of a present obligation, probable outflow and reliable estimate, so a provision is recognised in the balance sheet. A contingent liability is only a possible obligation — it may or may not arise, depending on uncertain future events, or one where outflow is not probable or cannot be measured reliably, so it is only disclosed in the notes.',
          [P('p1', 'Provision = present liability, uncertain amount, reliable estimate', 3,
             ALT('provision {x}', 'provision mean {x}', x=('present', 'existing', 'current', 'actual', 'reliabl', 'estimat', 'liabilit uncertain amount', 'liabilit of uncertain', 'probable'))),
           P('p2', 'Provision is recognised in the books / balance sheet', 2, ALT('provision {r}', 'provision is {r}', '{r} provision', r=('recognis', 'record', 'shown in balance', 'balance sheet', 'booked', 'created', 'made'))),
           P('p3', 'Contingent liability = possible obligation depending on future events / outflow not probable', 3,
             ALT('contingent {x}', 'contingent liabilit {x}', 'contingent liabilit only {x}', 'contingent liabilit mean {x}', x=('possible', 'may or may not', 'depend', 'uncertain', 'future', 'not probable', 'less likely', 'unlikely', 'potential', 'may arise', 'might'))),
           P('p4', 'Contingent liability only disclosed in notes', 2, 'note|disclos')], 'c4'),
        V('v5', 'How does a liability differ from a contingent liability?',
          'A liability is a present obligation arising from past events whose settlement will result in an outflow of resources, so it is recognised in the balance sheet. In a contingent liability either the outflow is not probable or the amount cannot be measured reliably, so it is not recognised but disclosed in the notes.',
          [P('p1', 'Liability: present obligation from past events with outflow on settlement', 4, 'present|existing|current|definite|certain', 'obligation|outflow|pay|settle', min=2),
           P('p2', 'Liability recognised in the balance sheet', 2, 'balance sheet|recognis|recorded'),
           P('p3', 'Contingent: outflow not probable or not reliably measurable', 2, 'not probable|improbable|unlikely|uncertain|possible|reliabl|cannot be measur|can t be measur|not measur', min=1),
           P('p4', 'Contingent: disclosed in notes, not recognised', 2, 'note|disclos')], 'c3'),
        V('v6', 'Give four examples of contingent liabilities.',
          'Examples of contingent liabilities are claims made against the enterprise that it has not accepted as debts, guarantees it has given for third parties, liability on bills of exchange discounted with the bank, and statutory liabilities such as tax demands under dispute.',
          [P('p1', 'Claims against the enterprise not acknowledged as debts', 3, 'claim|suit|lawsuit|case|litigation|court|legal action'),
           P('p2', 'Guarantees given for third parties', 3, 'guarantee|guarantor|surety'),
           P('p3', 'Bills discounted', 2, 'bill discount|discounted bill|bills discount|bill of exchange|bills of exchange|bill'),
           P('p4', 'Disputed statutory liabilities (tax demands under appeal)', 2, 'tax|statutory|dispute|appeal|duty|demand', min=1)], 'c2'),
    ]

    c = Checks()
    cases = [{
        'id': 'k1', 'title': 'Sunrise Hospitals Ltd — four uncertain matters', 'difficulty': 'hard',
        'case': ('At 31 March 2027 Sunrise Hospitals Ltd faces: (A) a negligence suit for ₹50,00,000 where its lawyers advise that a loss is probable and that ₹32,00,000 is the best estimate; (B) a municipal tax demand of ₹9,00,000 under appeal, which lawyers expect the hospital to win; '
                 '(C) its own claim of ₹14,00,000 against an equipment supplier for a defective scanner — the supplier has not responded and the outcome is uncertain; and (D) a ₹1,00,000 claim by a visitor that lawyers say is frivolous with a remote chance of success.'),
        'mcqs': [
            dict(M('k1a', 'What amount should be recognised as a provision?', ['₹32,00,000', '₹50,00,000', '₹41,00,000', '₹91,00,000'], 0,
              "Only suit (A) meets all three tests: a present obligation from past treatment, a probable outflow and a reliable estimate. The provision is the best estimate of ₹32,00,000, not the ₹50,00,000 claimed. The tempting ₹50,00,000 uses the claim amount; a plaintiff's claim is not a measure of the likely outflow. In practice: hospitals and insurers rely on legal counsel's best estimate when providing for negligence suits.", 'moderate', '3200000'), topic='Distinction between Contingent Liabilities and Provisions'),
            dict(M('k1b', 'What total should be disclosed as contingent liabilities in the notes?', ['₹9,00,000', '₹10,00,000', '₹59,00,000', '₹41,00,000'], 0,
              "Demand (B) is a present dispute where lawyers expect to win, so outflow is possible but not probable — a contingent liability of ₹9,00,000. Claim (D) is remote and is not disclosed, and suit (A) is a provision, not a contingent liability. The tempting ₹10,00,000 adds the remote visitor claim. In practice: disputed municipal and tax demands under appeal are the most common items in Indian companies' contingent liability notes.", 'hard', '900000'), topic='Contingent Liabilities'),
            dict(M('k1c', 'How is the hospital\'s ₹14,00,000 claim against the supplier treated?', ['Not recognised; may be mentioned in the Board\'s report if inflow is probable', 'Recognised as income of ₹14,00,000', 'Shown as a receivable in the balance sheet', 'Netted off against the provision for (A)'], 0,
              "The hospital's ₹14,00,000 claim against the supplier is a possible asset whose outcome depends on uncertain future events, so it is a contingent asset. It is not recognised; if inflow is probable it may be mentioned in the Board's report. The tempting option shows it as a receivable, which would record income that may never arrive. In practice: claims against suppliers for defective equipment stay off the books until the supplier admits liability or an award is made.", 'moderate'), topic='Contingent Asset'),
            dict(M('k1d', 'In April 2027 the supplier admits the claim in writing and promises payment. What follows?', ['The asset and income are recognised in the period in which this change occurs', 'The 2026-27 accounts are reopened to show the income', 'It remains a contingent asset until cash is received', 'It is credited to capital reserve'], 0,
              "Contingent assets are reviewed continually. Once the supplier admits the claim in writing, inflow is virtually certain, so the asset and income are recognised in the period in which this change occurs — April 2027, that is, 2027-28. The 2026-27 accounts are not reopened. The tempting option waits for cash, but recognition depends on virtual certainty, not receipt. In practice: the hospital's accountant books a claim receivable in the quarter when the written admission arrives.", 'hard'), topic='Contingent Asset'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch01', 'n': 4,
        'title': 'Contingent Assets and Contingent Liabilities',
        'outcomes': [
            'Define contingent assets and contingent liabilities in your own words and recognise them in practical situations.',
            'State how each is treated — recognised, disclosed in notes, mentioned in the Board\'s report, or ignored.',
            'Distinguish contingent liabilities from liabilities and from provisions, applying the recognition tests.',
            'Account for a contingent liability that later becomes a provision.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 35}, 'prereq': ['fnd-p1-ch01-u02'],
                 'exam_tip': 'Remember the ladder: virtually certain → recognise asset; probable outflow → provision; possible → disclose; remote → nothing. Most questions are a list of situations to sort with this ladder.'},
        'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions,
        'revision': {
            'summary': ['Contingent asset: possible asset from past events, confirmed by uncertain future events. Not recognised; usually disclosed in the Board\'s report if inflow probable; recognised when virtually certain.',
                        'Contingent liability: possible obligation, or present obligation where outflow is not probable or not reliably measurable. Not recognised; disclosed in notes unless remote; becomes a provision when outflow turns probable.',
                        'Liability: present obligation, outflow on settlement — recognised.',
                        'Provision: present liability of uncertain amount, reliably estimable — recognised when present obligation + probable outflow + reliable estimate.'],
            'remember': ['Examples of contingent liabilities: unacknowledged claims, guarantees for third parties, bills discounted, disputed statutory dues.', 'Provide the best estimate, not the amount claimed.', 'Change of probability is dealt with in the period in which it occurs.'],
            'traps': ['Do not disclose contingent assets in notes the way contingent liabilities are disclosed.', 'Do not disclose remote contingent liabilities.', 'Do not add a recognised provision to the contingent liabilities note as well.'],
        },
        'quickref': [
            {'k': 'Virtually certain inflow', 'v': 'Recognise asset and income'},
            {'k': 'Probable inflow', 'v': 'Contingent asset — not recognised; Board\'s report'},
            {'k': 'Probable outflow + reliable estimate', 'v': 'Provision (recognise)'},
            {'k': 'Possible outflow / no reliable estimate', 'v': 'Contingent liability (disclose in notes)'},
            {'k': 'Remote outflow', 'v': 'Nothing — no provision, no disclosure'},
            {'k': 'Provision (definition)', 'v': 'Amount written off/retained for depreciation, renewal, diminution of assets, or a known liability not determinable with substantial accuracy'},
        ],
        'viva': viva, 'cases': cases,
    }


# ---------- Auto-check data for the Write tab ----------
# Per scheme point: kw (viva-matcher keyword groups, "|" = alternatives) + min (groups needed), nums (figures that must
# appear), rows ([particular keywords, side, amount] for table answers; side may be dr/cr/add/less or a column-header
# keyword such as "provision"), wrong (common wrong statements → remark), ai_only (not checkable offline).
# Per question: extra_ok (may points beyond the model earn credit).
def _item(keys, verdict):
    """item keywords next to its verdict, in either order (one table row / one sentence)"""
    return '|'.join([f'{k} {verdict}' for k in keys] + [f'{verdict} {k}' for k in keys])


AUTO = {
    'q1': {'extra_ok': True,
           's1': {'kw': ['provision', 'present liabilit|present obligation|existing liabilit|uncertain amount|estimat'], 'min': 2},
           's2': {'kw': ['contingent liabilit', 'possible obligation|possible liabilit|may or may not|uncertain future|future event|depend'], 'min': 2},
           's3': {'kw': ['recognition|recognis|recogniz|criteria|condition', 'probable|reliable estimat|reliabl|past event'], 'min': 2},
           's4': {'kw': ['balance sheet|recognised books|recorded books|charge profit|charged profit|booked|liability side', 'notes|disclosed|disclosure|footnote|foot note'], 'min': 2,
                  'wrong': [{'kw': ['contingent liabilit shown balance sheet|contingent liabilit recorded balance sheet|contingent liabilit recognised balance sheet|contingent liabilit provided'],
                             'say': 'A contingent liability is not recognised in the balance sheet — it is only disclosed in the notes.'}]},
           's5': {'kw': ['example|e g|suit|penalty|claim|case|court|appeal|litigation', 'probable|likely|expect|estimat|chance'], 'min': 2}},
    'q2': {'extra_ok': False,
           's1': {'rows': [['suit|customer|claim', 'provision', 1100000]], 'kw': ['probable|reliable|likely|estimate'], 'min': 1},
           's2': {'rows': [['guarantee', 'contingent', 2000000]]},
           's3': {'rows': [['tax|demand|appeal', 'contingent', 350000]]},
           's4': {'kw': [_item(['contractor', 'own claim', 'claim against', 'iv'], 'contingent asset'),
                         'not recognis|not recogniz|not recorded|ignored|not shown|no entry|not booked|board report|directors report|not accounted'], 'min': 2,
                  'wrong': [{'kw': ['contractor contingent liabilit|contractor provision|own claim contingent liabilit'], 'say': "The company's own claim is a contingent asset, not a liability — it is not recognised."}]},
           's5': {'kw': [_item(['agent', 'former agent', 'no chance', 'v'], 'remote|ignored|ignore|no provision|no disclosure|not disclosed|nothing|not provided|not required')],
                  'nums': [1100000, 2350000]}},
    'q3': {'extra_ok': False,
           's1': {'kw': ['possible asset', 'past event', 'uncertain future|future event|not wholly control|not fully control|outside control|beyond control|not control', 'claim|court|suit|example|e g|lawsuit|litigation'], 'min': 3},
           's2': {'kw': ['not recognis|not recogniz|not recorded|not booked|never recognis|not accounted|not shown books|no entry|not brought books'], 'min': 1,
                  'wrong': [{'kw': ['contingent asset recognised|contingent asset recorded|contingent asset shown balance sheet|recognised asset balance sheet'], 'say': 'A contingent asset is never recognised; it may only be mentioned in the approving authority\'s (Board\'s) report.'}]},
           's3': {'kw': ['board|directors report|approving authority|report', 'probable|likely'], 'min': 2},
           's4': {'kw': ['virtually certain|virtual certain|virtually sure|certain', 'period|recognis|recogniz|recorded|booked|accounted'], 'min': 2}},
}


def _attach_auto(u):
    """Merge AUTO into the questions: every scheme point gets its auto-check fields; every question gets extra_ok."""
    for q in u.get('questions', []):
        a = AUTO[q['id']]
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']: s.update(a[s['id']])
        extra = set(a) - {'extra_ok'} - {s['id'] for s in q['scheme']}
        assert not extra, f"AUTO[{q['id']}] has unknown scheme ids {extra}"
    return u


_build_core = build


def build(): return _attach_auto(_build_core())
