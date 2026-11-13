"""CA Final · Paper 5 · Chapter 17 Assessment and Audit.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch17-u01'
T1 = 'Self-assessment and provisional assessment'
T2 = 'Scrutiny and best judgement assessment'
T3 = 'Summary assessment and assessment of unregistered persons'
T4 = 'Audit by tax authorities and special audit'


def build():
    ck = Checks()
    d = ck.add('60+60', 'Maximum days to withdraw a best judgement order by filing return (with extra late fee)')
    lf = ck.add('100*20', 'Additional late fee for 20 days beyond 60 days (₹)')
    i1 = {'id': 'i1', 'title': 'Best judgement for a non-filer', 'difficulty': 'core', 'minutes': 6,
          'q': 'Lakshmi Stores did not file GSTR-3B for March 2027 despite a notice. The officer passed a best judgement order served on 1 June 2027. Lakshmi files a valid return 80 days after service. Is the order withdrawn, and what additional late fee applies?',
          'solution': [table(['Step', 'Rule', 'Result'], [
              ['Window', f'Return within 60 days; extendable by 60 days with additional late fee (total {d} days)', 'Within window'],
              ['Additional late fee', '₹100 per day beyond 60 days × 20 days', f'₹{inr(lf)}'],
              ['Effect', 'Order deemed withdrawn; interest and normal late fee still payable', '—']], title='Section 62')],
          'checks': list(ck)}

    c2 = Checks()
    t = c2.add('3+3', 'Maximum months to complete departmental audit')
    s = c2.add('90+90', 'Maximum days for special audit report')
    i2 = {'id': 'i2', 'title': 'Audit timelines', 'difficulty': 'core', 'minutes': 5,
          'q': 'Explain the timelines for (a) audit by tax authorities under section 65 and (b) special audit under section 66.',
          'solution': [table(['Audit', 'Notice / start', 'Completion'], [
              ['Section 65', 'Notice at least 15 working days before', f'3 months, extendable to {t} months'],
              ['Section 66', 'Directed by Assistant Commissioner with Commissioner approval', f'90 days, extendable by 90 (total {s} days)'],
              ['After audit', 'Findings communicated within 30 days (section 65)', 'Demand under section 73/74/74A if needed']], title='Sections 65 and 66')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 59: every registered person self-assesses tax and files returns. Assessment means determination of tax liability and includes self-assessment, reassessment, provisional, summary and best judgement assessments.',
            'Section 60: where the taxpayer cannot determine value or rate, it may request provisional assessment; the officer orders it within 90 days, the taxpayer executes a bond with security, and final assessment follows within six months (extendable by six months and up to four years by higher authorities).',
            'On final assessment, tax due attracts interest from the original due date; excess paid is refunded with interest under section 56 if not paid within 60 days of the final order.'],
          'Taxpayers self-assess; provisional assessment helps when value or rate is uncertain.',
          'A new product with uncertain classification can be provisionally assessed.'),
        C('c2', T2, [
            'Section 61: the officer may scrutinise returns and seek explanations in Form ASMT-10 within up to 30 days; if accepted, proceedings end (ASMT-12), otherwise demand proceedings follow.',
            'Section 62: if a registered person fails to file returns after notice under section 46 (15 days), the officer makes a best judgement assessment within five years from the due date of the annual return. If a valid return is filed within 60 days of service of the order (extendable by 60 days with an additional late fee of ₹100 per day), the order is deemed withdrawn — though interest and late fee remain payable.',
            'Section 63: assessment of unregistered persons liable to register, or whose registration was cancelled, on best judgement within five years of the relevant annual return due date.'],
          'Scrutiny asks; best judgement decides when taxpayers stay silent.',
          'Filing a valid return 80 days after a best judgement order cancels it with extra late fee.'),
        C('c3', T3, [
            'Section 64: on evidence of tax liability, the officer may, with prior permission of the Additional or Joint Commissioner, make a summary assessment to protect revenue where delay would harm it — even before the taxable person is identified (the person in charge of the goods is then deemed the taxable person).',
            'On application by the taxpayer within 30 days, or on the Additional/Joint Commissioner\'s own motion if the order is erroneous, the summary assessment order can be withdrawn and proceedings under section 73/74/74A begin.',
            'Summary assessment is exceptional, used for goods in transit or perishable situations.'],
          'Summary assessment acts fast when revenue is at risk.',
          'Unclaimed goods in transit with no documents can be summarily assessed.'),
        C('c4', T4, [
            'Section 65: the Commissioner may order audit of a registered person, at its premises or the tax office, after at least 15 working days\' notice; it must be completed within three months, extendable by up to six months. Findings are communicated within 30 days, and demands follow if needed.',
            'Section 66: if, during scrutiny, inquiry or investigation, the officer (Assistant Commissioner or above, with Commissioner approval) believes value has not been correctly declared or credit availed is not within limits, considering complexity, he may direct a special audit by a nominated CA or cost accountant, to report within 90 days (extendable by 90).',
            'The taxpayer must be heard on special audit findings; expenses and remuneration are paid by the Commissioner.'],
          'Departmental audit has three to six months; special audit has 90 plus 90 days.',
          'A complex valuation case can be referred to a cost accountant for special audit.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Audit readiness', 'role': 'GST manager',
             'situation': 'A company receives a notice for audit under section 65.',
             'steps': ['Check notice period and scope.', 'Prepare reconciliations and records.', 'Respond to observations promptly.', 'Pay voluntary dues to avoid penalties.'],
             'takeaway': 'Prepared records shorten audits.'}]

    mcqs = [
        Q('m1', 'Provisional assessment order must be passed within:', ['Ninety days of request', 'Thirty days', 'Six months', 'One year'], 0,
          'Rule 98. In practice: bond and security.', 'c1', T1),
        Q('m2', 'Final assessment after provisional assessment must normally be made within:', ['Six months', 'Ninety days', 'One year', 'Three years'], 0,
          'Section 60(3). In practice: extendable up to four years.', 'c1', T1),
        Q('m3', 'Scrutiny discrepancies are communicated in:', ['Form ASMT-10', 'Form DRC-01', 'Form REG-17', 'Form GSTR-9C'], 0,
          'Rule 99. In practice: reply in ASMT-11.', 'c2', T2),
        Q('m4', 'Best judgement order is withdrawn if a valid return is filed within:', ['Sixty days of service, extendable by sixty', 'Thirty days', 'Fifteen days', 'One year'], 0,
          'Section 62(2). In practice: extra late fee.', 'c2', T2),
        Q('m5', 'Best judgement assessment must be made within:', ['Five years from due date of annual return', 'Three years', 'Two years', 'Seven years'], 0,
          'Section 62(1). In practice: same for section 63.', 'c2', T2),
        Q('m6', 'Summary assessment needs prior permission of:', ['Additional or Joint Commissioner', 'Principal Commissioner only', 'Court', 'GST Council'], 0,
          'Section 64. In practice: to protect revenue.', 'c3', T3),
        Q('m7', 'Notice for audit under section 65 must be issued at least:', ['Fifteen working days in advance', 'Seven days', 'Thirty days', 'Three days'], 0,
          'Section 65(3). In practice: ADT-01.', 'c4', T4),
        Q('m8', 'Special audit report is due within:', ['Ninety days, extendable by ninety', 'Thirty days', 'Six months', 'One year'], 0,
          'Section 66(3). In practice: CA or CMA.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Window', 2, 'analysis', '60 days', nums=[d]), S('s2', 'Late fee and effect', 2, 'computation', 'late fee', nums=[lf])],
          ['Mention interest still payable.'], ['Assuming no fee beyond 60 days.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Section 65', 2, 'analysis', '15 working', nums=[t]), S('s2', 'Section 66', 2, 'analysis', '90 days', nums=[s])],
          ['Name forms.'], ['Confusing the two timelines.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'When can a taxpayer seek provisional assessment?', 'When the value of its goods or services, or the applicable tax rate, is uncertain to it.',
          [P('p1', 'Value uncertain', 5, 'uncertain'), P('p2', 'Rate of tax', 5, 'rate')], 'c1'),
        V('v2', 'Who is deemed the taxable person in summary assessment where the owner is unknown?', 'The person in charge of the goods.',
          [P('p1', 'In charge', 5, 'in charge'), P('p2', 'Goods', 5, 'goods')], 'c3'),
        V('v3', 'Who can be nominated for special audit?', 'A chartered accountant or cost accountant nominated by the Commissioner.',
          [P('p1', 'Chartered accountant', 5, 'chartered accountant'), P('p2', 'Cost accountant', 5, 'cost accountant')], 'c4'),
        V('v4', 'What follows if scrutiny explanation is not satisfactory?', 'Action under sections 61(3) leading to audit, inspection or demand under section 73, 74 or 74A.',
          [P('p1', 'Audit or inspection', 5, 'audit'), P('p2', 'Demand', 5, 'demand')], 'c2'),
        V('v5', 'Who bears the cost of special audit?', 'The Commissioner determines and pays the expenses and remuneration of the auditor.',
          [P('p1', 'Commissioner', 5, 'commissioner'), P('p2', 'Pays', 5, 'pays')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Rudra Pharma audit', 'difficulty': 'core',
              'case': 'Rudra Pharma receives an audit notice dated 1 August 2026. Audit begins on 25 August 2026.',
              'mcqs': [
                  M('k1a', 'Minimum notice in working days:', ['15', '7', '30', '10'], 0,
                    'Section 65(3). In practice: check holidays.', 'core', check=15, topic=T4),
                  M('k1b', 'Normal completion period (months):', ['3', '6', '1', '12'], 0,
                    'Section 65(4). In practice: from start of audit.', 'core', check=3, topic=T4),
                  M('k1c', 'Maximum extension up to (months):', ['6', '9', '12', '4'], 0,
                    'Commissioner may extend. In practice: reasons recorded.', 'core', check=6, topic=T4),
                  M('k1d', 'Findings must be communicated within (days):', ['30', '15', '60', '90'], 0,
                    'Section 65(6). In practice: ADT-02.', 'core', check=30, topic=T4),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch17', 1, 'Assessment and Audit',
                ['Apply self-assessment and provisional assessment.',
                 'Apply scrutiny and best judgement assessments.',
                 'Apply summary assessment and assessment of unregistered persons.',
                 'Apply departmental and special audit provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 15}, 'prereq': ['fin-p5-ch16-u01'],
                 'exam_tip': 'Tabulate each assessment with trigger, authority and time limit.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 59 self; 60 provisional (90 days, 6 months).', 'Section 61 scrutiny ASMT-10.', 'Section 62 best judgement; 60 + 60 days withdrawal.',
                             'Section 63 unregistered; 64 summary.', 'Section 65 audit 15 working days, 3 + 3 months; section 66 special audit 90 + 90 days.'],
                 'remember': ['Interest survives withdrawal of best judgement order.'],
                 'traps': ['Mixing section 65 and 66 timelines.']},
                [('Self-assessment', 'Section 59'), ('Provisional', 'Section 60'), ('Best judgement', 'Section 62'), ('Audit', 'Section 65'), ('Special audit', 'Section 66')],
                viva, cases)
