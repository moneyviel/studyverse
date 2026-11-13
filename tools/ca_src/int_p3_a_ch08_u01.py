"""CA Intermediate · Paper 3A Income-tax Law · Chapter 8 Return of Income and Self-Assessment (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers are taken from it; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch08-u01'
T1 = 'Who must file and by when (s. 263(1))'
T2 = 'Belated, revised and defective returns (s. 263(4), (5), (7))'
T3 = 'Updated return and additional tax (ss. 263(6), 267)'
T4 = 'Interest and fee for late filing (ss. 423, 428) and self-assessment (s. 266)'
T5 = 'Tax return preparers, verification, PAN and Aadhaar (ss. 262, 264, 265, 430, 467)'


def build():
    # i1 — late return: interest and fee
    ck = Checks()
    bal = ck.add('190000-120000-40000', 'Tax still unpaid')
    intr = ck.add('30000*1/100*4', 'Interest u/s 423: 1% × 4 months (Aug–Nov)')
    tot = ck.add('5000+1200+30000', 'Total self-assessment payment')
    i1 = {'id': 'i1', 'title': 'Filing in November instead of July', 'difficulty': 'core', 'minutes': 7,
          'q': 'Mr. Sanjay, a salaried individual with no business income, files his return for tax year 2026-27 on 10 November 2027. Tax on his total income of ₹14,20,000 is ₹1,90,000; TDS was ₹1,20,000 and advance tax ₹40,000. Compute interest under section 423, the fee under section 428 and the amount he must pay with the return. Ignore interest under sections 424 and 425.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Due date', 'Any other assessee: 31 July 2027', '—'],
              ['Tax unpaid', '1,90,000 − 1,20,000 − 40,000', inr(bal)],
              ['Months of delay', '1 August to 10 November: August, September, October and part of November', '4'],
              ['Interest u/s 423', '1% × 30,000 × 4', inr(intr)],
              ['Fee u/s 428(a)', 'Total income above ₹5,00,000', inr(5000)],
              ['Total payable u/s 266', 'Fee + interest + tax', inr(tot)]], title='Late return'),
              note('Under section 266, whatever he pays is applied first to the fee, then to interest, and only the balance to tax.')],
          'checks': list(ck)}

    # i2 — updated return
    ck2 = Checks()
    base = ck2.add('80000+20000', 'Tax and interest on the updated return')
    add = ck2.add('100000*50/100', 'Additional tax at 50%')
    pay = ck2.add('100000+50000', 'Total payable before filing the updated return')
    i2 = {'id': 'i2', 'title': 'Correcting a return three years late', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Ms. Priya filed her return for tax year 2026-27 on time but left out rental income. In February 2030 she decides to file an updated return. Extra tax on the omitted income is ₹80,000 and interest on it is ₹20,000. Compute the additional income-tax and the total she must pay.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Financial year after the tax year', '2027-28, ending 31 March 2028', '—'],
              ['Time band', 'February 2030 is after 12 months but within 24 months from 31 March 2028', '50%'],
              ['Tax + interest', '80,000 + 20,000', inr(base)],
              ['Additional tax u/s 267', '50% × 1,00,000', inr(add)],
              ['Total to pay first', '', inr(pay)]], title='Section 267'),
              note('The last date for an updated return for tax year 2026-27 is 31 March 2032 (48 months after 31 March 2028).')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A return is the prescribed statement in which a person reports total income, tax, taxes paid and other details for a tax year.',
            'Always required: companies, firms, specified universities and institutions, and a resident and ordinarily resident person who holds, has signing authority over, or benefits from any asset or account outside India — even with a loss or nil income.',
            'Others must file if total income, before Chapter VIII deductions and capital-gain deductions under sections 82–86, exceeds the basic exemption limit (₹4,00,000 under the default regime; ₹2,50,000, ₹3,00,000 or ₹5,00,000 under the optional regime), or if a Rule 163 condition is met: current-account deposits above ₹1 crore; foreign travel spending above ₹2 lakh; electricity bills above ₹1 lakh; business turnover above ₹60 lakh; professional receipts above ₹10 lakh; or TDS/TCS of ₹25,000 or more (₹50,000 for residents aged 60+).',
            'Due dates (financial year after the tax year): 30 November where transfer pricing reports apply (s. 172); 31 October for companies, audited assessees and partners of audited firms; 31 August for non-audited business or professional income and partners of such firms; 31 July for everyone else. Business, capital gains, speculation, specified-business and race-horse losses are carried forward only if the loss return is filed by the due date; house-property loss and unabsorbed depreciation are not affected.'],
          'The due date depends on whether books are audited — salaried people file first, audited businesses later.',
          'A shopkeeper with non-audited accounts files by 31 August 2027; his salaried brother by 31 July 2027.'),
        C('c2', T2, [
            'Belated return (s. 263(4)): if the due date is missed, a return may still be filed by 31 December of the financial year after the tax year, or before assessment is completed, whichever is earlier.',
            'Revised return (s. 263(5)): an original or belated return with an omission or wrong statement may be revised within 12 months from the end of the tax year (31 March 2028 for tax year 2026-27) or before assessment, whichever is earlier. A revised return can itself be revised, and a loss return can be revised too.',
            'Defective return (s. 263(7)): if a return does not meet the prescribed requirements — for example, fields left blank or the tax audit report not filed before the return — the Assessing Officer may give 15 days (extendable) to rectify it. If not rectified, it is treated as never filed; if rectified late but before assessment, the delay may be condoned.'],
          'Belated returns fix lateness; revised returns fix mistakes; defect notices fix incompleteness.',
          'A return filed on 20 July 2027 can be revised on 15 February 2028, but with a fee, because nine months have passed.'),
        C('c3', T3, [
            'Section 263(6): any person may file an updated return within 48 months counted from the close of the financial year that follows the tax year, whether or not an earlier return was filed. For tax year 2026-27 the last date is 31 March 2032.',
            'It is not allowed if it is a loss return (unless it reduces a loss shown in a loss return filed by the due date), reduces tax, creates or increases a refund, or if an updated return has already been filed for that year.',
            'Section 267: before filing, the person pays tax and interest on the updated income plus additional tax of 25%, 50%, 60% or 70% of that tax and interest, depending on whether filing falls within 12, 24, 36 or 48 months from the end of the following financial year (the 25% band starts after the belated/revised time is over).'],
          'An updated return is a paid second chance — the longer you wait, the higher the price.',
          'Filing in the third band costs 60% of the extra tax and interest on top of them.'),
        C('c4', T4, [
            'Section 423: simple interest at 1% per month (a part month counting as whole) from the day after the due date to the date of filing (or of assessment if no return is filed), on tax on total income less advance tax, TDS/TCS, relief u/s 157 and tax credits. Additional tax u/s 267 is excluded from the base.',
            'Section 428: a fixed fee for filing after the due date — ₹1,000 if total income is up to ₹5,00,000, otherwise ₹5,000. The same fee applies to a revised return filed more than nine months after the end of the tax year.',
            'Section 266: tax and interest due on the return must be paid before filing. Payments are applied first to the fee, then to interest, and the balance to tax; if anything remains unpaid, the person is in default for that amount.'],
          'Lateness has two price tags: interest that grows each month and a flat fee.',
          'Total income ₹4,60,000, return filed in September: the fee is ₹1,000.'),
        C('c5', T5, [
            'Section 264: under a notified scheme, individuals and HUFs not subject to tax audit (or audit under another law), and not companies, may file through an authorised tax return preparer.',
            'Section 265: an individual signs his own return (a guardian or competent person if mentally incapacitated, or a power-of-attorney holder if otherwise unable); an HUF by the karta or, if absent or incapacitated, another adult member; a company by its managing director, or any director if there is none.',
            'Section 262 governs PAN: a person who must file a return or pay tax and who meets the prescribed conditions applies for one, and PAN and Aadhaar must be quoted in specified transactions. A person eligible for Aadhaar who does not link it has his PAN made inoperative; section 430 provides a fee of up to ₹1,000 for late intimation, and section 467 a penalty of ₹10,000 for specified PAN defaults.'],
          'The right signatory makes a return valid; the right PAN makes it traceable.',
          'A karta abroad for the whole of July can have his son, an adult member, sign the HUF\'s return.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Due-date calendar', 'role': 'Article assistant',
         'situation': 'The firm wants a filing calendar for 40 clients.',
         'steps': ['Classify each client: salaried, non-audit business, audit case, transfer pricing.', 'Map the due date for each class.', 'Flag clients with losses to carry forward.', 'Set reminders 15 days before each date.'],
         'takeaway': 'Missing the date for a loss return costs the carry-forward, not just a fee.'},
        {'id': 'j2', 'title': 'Missed income discovered late', 'role': 'Tax associate',
         'situation': 'A client finds an unreported capital gain from two years ago.',
         'steps': ['Check whether revision is still possible.', 'If not, compute tax and interest for an updated return.', 'Apply the correct additional-tax band.', 'Pay before filing and keep the challan.'],
         'takeaway': 'Act early: each passing year raises the additional-tax rate.'},
    ]

    mcqs = [
        Q('m1', 'Due date for a non-audited proprietor with business income, tax year 2026-27:', ['31 August 2027', '31 July 2027', '31 October 2027', '30 November 2027'], 0,
          'Business or professional income without a tax-audit requirement gives a due date of 31 August of the following financial year; salaried people file by 31 July. In practice: audited cases get 31 October.', 'c1', T1),
        Q('m2', 'A resident individual under the default regime has total income of ₹3,80,000 after a deduction of ₹50,000 for employer NPS. Must she file a return?', ['Yes, because income before the deduction is ₹4,30,000', 'No, because total income is below ₹4,00,000', 'No, salaried people never need to', 'Only if tax is payable'], 0,
          'The test uses income before Chapter VIII deductions. ₹4,30,000 exceeds the ₹4,00,000 limit, so filing is compulsory even if rebate makes tax nil. In practice: add back deductions first.', 'c1', T1, 'moderate'),
        Q('m3', 'Which loss can be carried forward even if the return is filed late?', ['House property loss', 'Business loss', 'Capital loss', 'Speculation loss'], 0,
          'House-property loss and unabsorbed depreciation survive a late return; business, capital, speculation, specified-business and race-horse losses need the return by the due date. In practice: file loss returns on time.', 'c1', T1),
        Q('m4', 'Last date for a belated return for tax year 2026-27 (no assessment yet):', ['31 December 2027', '31 March 2028', '31 July 2027', '31 March 2027'], 0,
          'A belated return may be filed up to 31 December of the financial year following the tax year, or before assessment, whichever is earlier. In practice: a fee applies.', 'c2', T2),
        Q('m5', 'Mr. Aman\'s original return was assessed on 10 November 2027. He wants to revise it on 20 November 2027. He can:', ['Not revise it, as assessment is complete', 'Revise it till 31 March 2028', 'Revise it with a fee', 'Revise it only with the AO\'s approval'], 0,
          'Revision is allowed within 12 months from the end of the tax year or before assessment is completed, whichever is earlier. Once assessed, the window closes. In practice: raise the issue in rectification or appeal instead.', 'c2', T2),
        Q('m6', 'A belated return filed on 30 November 2027 can be revised up to:', ['31 March 2028', '31 December 2027', 'It cannot be revised', '30 November 2028'], 0,
          'Belated returns can also be revised, within 12 months from the end of the tax year (31 March 2028 for tax year 2026-27) or before assessment. In practice: a fee arises if revised after 31 December 2027.', 'c2', T2),
        Q('m7', 'The time to rectify a defect notified by the Assessing Officer is ordinarily:', ['15 days, extendable on application', '30 days, not extendable', '7 days', '60 days'], 0,
          'The AO allows 15 days from service of the intimation and can extend it if the assessee applies. An unrectified return is treated as not filed. In practice: respond promptly on the portal.', 'c2', T2),
        Q('m8', 'An updated return is NOT allowed where it:', ['Increases the refund', 'Increases the tax', 'Adds omitted income', 'Is the first updated return for the year'], 0,
          'It cannot reduce tax, create or increase a refund, or be a second updated return for the same year. Adding income is exactly its purpose. In practice: use the revised return to claim refunds.', 'c3', T3),
        Q('m9', 'Additional tax on an updated return filed between 24 and 36 months after the end of the following financial year:', ['60%', '50%', '70%', '25%'], 0,
          'The bands are 25%, 50%, 60% and 70% for up to 12, 24, 36 and 48 months from the end of the financial year following the tax year. In practice: count from 31 March after the tax year\'s following year.', 'c3', T3, check=60),
        Q('m10', 'Fee u/s 428 for a late return with total income of ₹4,80,000:', ['₹1,000', '₹5,000', 'Nil', '₹500'], 0,
          'The fee is ₹1,000 for total income up to ₹5,00,000; above that it is ₹5,000. Lateness alone triggers it; it is not discretionary. In practice: pay it before filing.', 'c4', T4, check=1000),
        Q('m11', 'Self-assessment payments under section 266 are applied in which order?', ['Fee, then interest, then tax', 'Tax, then interest, then fee', 'Interest, then tax, then fee', 'In any order the assessee chooses'], 0,
          'The law applies amounts first towards the fee, then interest, and only the balance towards tax, so underpayment shows up as unpaid tax. In practice: compute all three before paying.', 'c4', T4),
        Q('m12', 'Who verifies the return of a company that has no managing director?', ['Any director', 'The company secretary', 'The chief financial officer', 'The auditor'], 0,
          'A company\'s return is verified by its managing director; where there is none, any director may verify it. In practice: check the signatory\'s DSC is valid.', 'c5', T5),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Due date identified', 1, 'concept', '31 july'),
           S('s2', 'Unpaid tax', 1, 'computation', 'unpaid', nums=[bal]),
           S('s3', 'Interest months', 1, 'computation', '4', nums=[intr]),
           S('s4', 'Fee and total', 2, 'computation', '428', nums=[tot])],
          ['Part of a month counts as a full month.'], ['Charging fee of ₹1,000 when income exceeds ₹5 lakh.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Band identified', 2, 'concept', '50%'),
           S('s2', 'Additional tax', 1, 'computation', '267', nums=[add]),
           S('s3', 'Total payable', 1, 'computation', 'total', nums=[pay])],
          ['Count from the end of the following financial year.'], ['Counting from the end of the tax year.'], ['Step table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Which persons must file a return even with a loss or nil income?',
          'Companies, firms, specified institutions, and resident and ordinarily resident persons holding or benefiting from any asset or account outside India.',
          [P('p1', 'Companies and firms', 5, 'compan|firm'), P('p2', 'Foreign asset holders', 5, 'outside india|foreign')], 'c1'),
        V('v2', 'What is the time limit for a revised return?',
          'Twelve months from the end of the tax year, or before completion of assessment, whichever is earlier; a fee applies if filed more than nine months after the year end.',
          [P('p1', 'Twelve months', 6, 'twelve|12'), P('p2', 'Assessment', 4, 'assessment')], 'c2'),
        V('v3', 'How long is the window for an updated return?',
          'Forty-eight months from the end of the financial year following the tax year, with additional tax rising from 25% to 70% the later it is filed.',
          [P('p1', '48 months', 6, '48|forty-eight'), P('p2', 'Additional tax', 4, 'additional|25%|70%')], 'c3'),
        V('v4', 'How is interest for late filing worked out?',
          'Simple interest at 1% per month, with a part month counted as a full one, from the day after the due date to the date of filing, on tax payable after advance tax, TDS, TCS and reliefs.',
          [P('p1', '1% per month', 6, '1%'), P('p2', 'Net tax base', 4, 'advance tax|tds')], 'c4'),
        V('v5', 'Who cannot file through a tax return preparer?',
          'Companies and persons whose accounts must be audited under section 63 or any other law; the scheme is for other individuals and HUFs.',
          [P('p1', 'Companies', 5, 'compan'), P('p2', 'Audited persons', 5, 'audit')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'The Kapoor family returns', 'difficulty': 'moderate',
              'case': 'For tax year 2026-27: Kapoor Industries Ltd. (audited); Mr. Kapoor, a partner in a non-audited firm; his wife Neha, a salaried employee with total income of ₹4,40,000 who filed on 5 September 2027; and their son Arjun, a resident who holds shares in a US company but earns no taxable income.',
              'mcqs': [
                  M('k1a', 'Due date for Kapoor Industries Ltd.:', ['31 October 2027', '31 July 2027', '31 August 2027', '30 November 2027'], 0,
                    'A company whose accounts are audited, with no transfer-pricing report, files by 31 October of the following year. In practice: the audit report must be filed before the return.', 'core', topic=T1),
                  M('k1b', 'Due date for Mr. Kapoor:', ['31 August 2027', '31 July 2027', '31 October 2027', '31 December 2027'], 0,
                    'A partner in a firm that needs no audit gets the 31 August due date. In practice: partners of audited firms get 31 October.', 'core', topic=T1),
                  M('k1c', 'Fee payable by Neha:', ['₹1,000', '₹5,000', 'Nil', '₹2,000'], 0,
                    'She filed after 31 July, and her total income does not exceed ₹5,00,000, so the fee is ₹1,000. In practice: interest also applies if tax was unpaid.', 'core', check=1000, topic=T4),
                  M('k1d', 'Must Arjun file a return?', ['Yes, because he holds a foreign asset', 'No, as he has no taxable income', 'Only if his income exceeds ₹4,00,000', 'Only if he sells the shares'], 0,
                    'A resident and ordinarily resident person holding any asset outside India must file even without taxable income. In practice: report it in the foreign assets schedule.', 'moderate', topic=T1),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch08', 1, 'Provisions for filing Return of Income and Self Assessment',
                ['Identify who must file a return and the due date for each class of assessee.',
                 'Apply the rules for belated, revised, defective and updated returns.',
                 'Compute interest and fee for late filing and the additional tax on an updated return.',
                 'Identify verification, tax return preparer, PAN and Aadhaar requirements.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 40}, 'prereq': ['int-p3-a-ch07-u01'],
                 'exam_tip': 'Write the due date first; every other answer — fee, interest, revision window — flows from it.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Filing test uses income before Chapter VIII and ss. 82–86 deductions.',
                             'Due dates: 31 July / 31 August / 31 October / 30 November.',
                             'Belated: 31 December; revised: 12 months from year end (fee after 9 months).',
                             'Updated: 48 months; additional tax 25/50/60/70%.',
                             's. 423: 1% p.m.; s. 428: ₹1,000 / ₹5,000.',
                             's. 266 payments: fee → interest → tax.'],
                 'remember': ['Loss returns must be on time to carry forward most losses.', 'A revised return can be revised again.'],
                 'traps': ['Updated return cannot increase a refund.', 'Part of a month counts as a month for interest.']},
                [('Belated return', '31 December'), ('Revised return', '31 March (12 months)'), ('Updated return', '48 months'), ('Late fee', '₹1,000 / ₹5,000')],
                viva, cases)
