"""CA Final · Paper 4 · Chapter 19 Provisions to Counteract Unethical Tax Practices.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch19-u01'
T1 = 'Penalty for under-reporting and misreporting'
T2 = 'Reduction, waiver and immunity'
T3 = 'Offences and prosecution'
T4 = 'Black Money Act'


def build():
    ck = Checks()
    tx = ck.add('(12000000-8000000)*0.25', 'Tax on under-reported income at 25% (₹)')
    p50 = ck.add('(12000000-8000000)*0.25*0.50', 'Penalty for under-reporting at 50% (₹)')
    p200 = ck.add('(12000000-8000000)*0.25*2', 'Penalty if misreporting at 200% (₹)')
    i1 = {'id': 'i1', 'title': 'Under-reporting versus misreporting', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Arcadia Pvt Ltd (tax rate 25%; ignore surcharge and cess) returned income of ₹80,00,000. The assessment determines ₹1,20,00,000. Compute the penalty if (a) the addition is a mere under-reporting and (b) it arises from recording false entries in books.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Under-reported income', '1,20,00,000 − 80,00,000', '40,00,000'],
              ['Tax on it', '25% × 40,00,000', inr(tx)],
              ['(a) Penalty — 50%', '', inr(p50)],
              ['(b) Penalty — 200% (misreporting)', '', inr(p200)]], title='Section 439')],
          'checks': list(ck)}

    c2 = Checks()
    t = c2.add('10000000*0.30', 'Tax at 30% on undisclosed foreign asset (₹)')
    p = c2.add('10000000*0.30*3', 'Penalty at three times the tax (₹)')
    tot = c2.add('10000000*0.30*4', 'Total tax and penalty (₹)')
    i2 = {'id': 'i2', 'title': 'Undisclosed foreign asset', 'difficulty': 'core', 'minutes': 5,
          'q': 'Varun, a resident and ordinarily resident, is found to hold an undisclosed foreign bank account valued at ₹1,00,00,000. Compute tax and penalty under the Black Money Act.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Tax', '30% × 1,00,00,000', inr(t)],
              ['Penalty', '3 × tax', inr(p)],
              ['Total', '', inr(tot)]], title='Black Money Act, sections 3 and 41')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 439 levies penalty on under-reported income: broadly, assessed income exceeding returned income (or the basic exemption limit where no return is filed), and reduced deemed total income in MAT/AMT cases. The penalty is 50% of tax payable on under-reported income.',
            'Where under-reporting results from misreporting — misrepresentation or suppression of facts, unrecorded investments, unsubstantiated expenditure, false entries, unrecorded receipts, unreported international or specified domestic transactions, or unexplained income taxed under section 195(1)(b) — the penalty is 200%.',
            'Excluded from under-reported income are amounts explained with bona fide disclosure, estimates where accounts are correct and complete, transfer-pricing adjustments where documentation was maintained and disclosed, and additions based on disclosures in a search. Tax on under-reported income uses formulae that differ for returned, unreturned and deemed-income cases.'],
          'Fifty percent for honest error; two hundred percent for dishonesty.',
          'A ₹40 lakh addition from false entries in a 25% company brings penalty of ₹20 lakh.'),
        C('c2', T2, [
            'Section 469: the PCIT/CIT may reduce or waive penalty if the person made a full and true disclosure voluntarily before detection, co-operated, and paid tax and interest due; orders are discretionary and appealable restrictions apply.',
            'Section 440: an assessee may apply within one month after the close of the month of receiving the assessment order for immunity from penalty and prosecution, if it pays tax and interest within the demand period, does not appeal, and — where the penalty would be for misreporting — pays additional income-tax of 100% (or 120% for unexplained-income cases) of the tax on under-reported income in lieu of penalty.',
            'Section 470: no penalty for specified defaults if reasonable cause is proved. Penalty orders follow a hearing (section 471) and must be passed within time limits in section 472.'],
          'Come clean early or pay extra to buy peace.',
          'Paying 100% additional tax can replace a 200% misreporting penalty.'),
        C('c3', T3, [
            'Chapter XXII lists offences: contravening search orders, failure to afford facilities, removal of seized assets, false statements in verification, abetment, and failure to pay TDS or TCS deducted or collected.',
            'Section 478 (wilful attempt to evade tax or under-report, or to evade payment): simple imprisonment up to 2 years and/or fine if the amount exceeds ₹50 lakh; up to 6 months and/or fine if above ₹10 lakh up to ₹50 lakh; fine only otherwise. TDS/TCS non-payment carries similar graded punishment, with no prosecution if paid by the return due date.',
            'Offences by companies and HUFs make persons in charge liable unless they prove lack of knowledge or due diligence (sections 487, 488); culpable mental state is presumed (section 490). Offences may be compounded and immunity tendered to co-accused (section 519).'],
          'Prosecution now scales with the tax at stake.',
          'Evasion of ₹30 lakh exposes a person to up to 6 months\' simple imprisonment.'),
        C('c4', T4, [
            'The Black Money Act of 2015 taxes undisclosed foreign income and assets of residents at 30% on their value (FMV for assets) in the year they come to notice, with no deductions, exemptions or set-off.',
            'Penalty is three times the tax. Failure to file a return or disclose foreign assets or income by a resident (not ordinarily resident excluded) attracts ₹10 lakh per default; this does not apply to assets other than immovable property whose aggregate value is up to ₹20 lakh.',
            'Wilful failure to disclose or attempt to evade tax under the Act is punishable with rigorous imprisonment of 3 to 10 years (wilful evasion) or 6 months to 7 years (wilful non-filing or non-disclosure), with fine; repeat offences carry 3 to 10 years and fines of ₹5 lakh to ₹1 crore.'],
          'Hidden foreign money costs 30% tax plus 90% penalty.',
          'An undisclosed ₹1 crore foreign account can cost ₹1.2 crore.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Penalty defence file', 'role': 'Tax litigation associate',
             'situation': 'A client faces a penalty notice after additions in scrutiny.',
             'steps': ['Classify additions as under-reporting or misreporting.', 'Check exclusions and bona fide explanations.', 'Evaluate immunity under section 440.', 'Reply with evidence and computations.'],
             'takeaway': 'Classification decides whether the rate is 50% or 200%.'}]

    mcqs = [
        Q('m1', 'Penalty for under-reporting (not misreporting) is:', ['Fifty percent of tax on under-reported income', 'Two hundred percent', 'One hundred percent', 'Ten percent'], 0,
          'Section 439. In practice: on tax, not income.', 'c1', T1),
        Q('m2', 'Which is a case of misreporting?', ['Recording a false entry in books', 'An estimate where accounts are complete', 'A bona fide disclosed claim', 'A rounding difference'], 0,
          'Section 439(11). In practice: 200%.', 'c1', T1),
        Q('m3', 'Immunity application under section 440 is filed within:', ['One month after the month of receiving the order', 'Six months', 'Thirty days of the return', 'Two months'], 0,
          'Time limit. In practice: no appeal.', 'c2', T2),
        Q('m4', 'Additional tax in lieu of misreporting penalty (non-unexplained cases) is:', ['One hundred percent of tax on under-reported income', 'Fifty percent', 'Two hundred percent', 'Twenty percent'], 0,
          'Section 440. In practice: 120% for unexplained income.', 'c2', T2),
        Q('m5', 'Wilful evasion above ₹50 lakh is punishable with simple imprisonment up to:', ['Two years', 'Seven years', 'Six months', 'Ten years'], 0,
          'Section 478. In practice: and/or fine.', 'c3', T3),
        Q('m6', 'Wilful evasion of ₹8 lakh is punishable with:', ['Fine only', 'Two years', 'Six months', 'Seven years'], 0,
          'Below ₹10 lakh. In practice: graded.', 'c3', T3),
        Q('m7', 'Tax rate under the Black Money Act is:', ['Thirty percent', 'Sixty percent', 'Forty percent', 'Twenty percent'], 0,
          'On value of undisclosed asset. In practice: no deductions.', 'c4', T4),
        Q('m8', 'Penalty for undisclosed foreign income and assets is:', ['Three times the tax', 'Equal to the tax', 'Twice the tax', 'Ten lakh rupees only'], 0,
          'Section 41. In practice: plus prosecution.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Under-reported income and tax', 2, 'computation', 'under-reported', nums=[tx]), S('s2', 'Penalties', 4, 'computation', 'misreporting', nums=[p50, p200])],
          ['State classification.'], ['Applying penalty on income instead of tax.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Tax', 2, 'computation', '30%', nums=[t]), S('s2', 'Penalty', 2, 'computation', 'three times', nums=[p, tot])],
          ['Cite sections.'], ['Allowing cost of acquisition.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Name two cases treated as misreporting.', 'Recording false entries in books and claiming expenditure unsupported by evidence.',
          [P('p1', 'False entries', 5, 'false entries'), P('p2', 'Unsupported expenditure', 5, 'expenditure')], 'c1'),
        V('v2', 'What conditions apply for section 469 waiver?', 'Voluntary full and true disclosure before detection, co-operation, and payment of tax and interest.',
          [P('p1', 'Voluntary disclosure', 5, 'disclosure'), P('p2', 'Payment', 5, 'payment')], 'c2'),
        V('v3', 'Who is liable for an offence by a company?', 'Persons in charge of and responsible for its business, unless they prove lack of knowledge or due diligence.',
          [P('p1', 'In charge', 5, 'in charge'), P('p2', 'Due diligence', 5, 'due diligence')], 'c3'),
        V('v4', 'Is culpable mental state presumed in prosecutions?', 'Yes, the court presumes it, and the accused may prove its absence beyond reasonable doubt.',
          [P('p1', 'Presumed', 5, 'presume'), P('p2', 'Accused proves', 5, 'accused')], 'c3'),
        V('v5', 'What is the penalty for not disclosing foreign assets in the return?', 'Ten lakh rupees per default for a resident and ordinarily resident, except where non-immovable foreign assets total ₹20 lakh or less.',
          [P('p1', 'Ten lakh', 5, '10 lakh|ten lakh'), P('p2', 'Resident', 5, 'resident')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Prosecution exposure', 'difficulty': 'core',
              'case': 'Three taxpayers are found to have wilfully attempted to evade tax: P (₹65 lakh), Q (₹30 lakh) and R (₹6 lakh).',
              'mcqs': [
                  M('k1a', 'Maximum imprisonment for P (years):', ['2', '7', '0.5', '10'], 0,
                    'Above ₹50 lakh. In practice: simple imprisonment.', 'core', check=2, topic=T3),
                  M('k1b', 'Maximum imprisonment for Q (months):', ['6', '24', '12', '3'], 0,
                    '₹10–50 lakh band. In practice: and/or fine.', 'core', check=6, topic=T3),
                  M('k1c', 'Punishment for R:', ['Fine only', 'Six months', 'Two years', 'Three years'], 0,
                    'Up to ₹10 lakh. In practice: penalty still applies.', 'core', topic=T3),
                  M('k1d', 'Does prosecution bar penalty under section 439?', ['No, it is without prejudice to penalty', 'Yes', 'Only for companies', 'Only above ₹50 lakh'], 0,
                    'Section 478(3). In practice: both may apply.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch19', 1, 'Provisions to Counteract Unethical Tax Practices',
                ['Compute penalty for under-reporting and misreporting.',
                 'Apply reduction, waiver and immunity provisions.',
                 'Identify offences and graded prosecution.',
                 'Apply the Black Money Act provisions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p4-ch18-u01'],
                 'exam_tip': 'Classify the addition first; then compute tax on under-reported income and apply 50% or 200%.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 439: 50% under-reporting; 200% misreporting.', 'Section 469 waiver; section 440 immunity with 100%/120% additional tax.', 'Section 478 graded prosecution: ₹10 lakh/₹50 lakh bands.',
                             'Black Money Act: 30% tax; 3x penalty; ₹10 lakh for non-disclosure.'],
                 'remember': ['Penalty is on tax, not on income.'],
                 'traps': ['Treating all additions as misreporting.']},
                [('Penalty', 'Section 439'), ('Immunity', 'Section 440'), ('Waiver', 'Section 469'), ('Evasion', 'Section 478')],
                viva, cases)
