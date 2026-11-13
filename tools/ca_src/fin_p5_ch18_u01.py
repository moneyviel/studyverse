"""CA Final · Paper 5 · Chapter 18 Inspection, Search, Seizure and Arrest.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch18-u01'
T1 = 'Inspection'
T2 = 'Search and seizure'
T3 = 'Arrest and its safeguards'
T4 = 'Summons, access and production of records'


def build():
    ck = Checks()
    m = ck.add('6+6', 'Maximum months to issue notice for seized goods')
    i1 = {'id': 'i1', 'title': 'Seized goods and release', 'difficulty': 'core', 'minutes': 6,
          'q': 'During a search on 1 May 2026, officers seize goods of Navin Traders. No notice has been issued by 1 November 2026. What happens? Can Navin get the goods released earlier?',
          'solution': [table(['Point', 'Rule', 'Result'], [
              ['Notice deadline', f'Six months from seizure, extendable by six months (maximum {m} months)', 'Return unless extended'],
              ['Provisional release', 'On bond and security, or on payment of tax, interest and penalty', 'Available'],
              ['Perishable goods', 'May be disposed of after seizure as notified', '—']], title='Section 67')],
          'checks': list(ck)}

    c2 = Checks()
    a = c2.add('25000000', 'Tax evaded by Mehul (₹)')
    i2 = {'id': 'i2', 'title': 'Can the person be arrested?', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Commissioner has reason to believe (a) Mehul issued fake invoices evading ₹2.5 crore of tax; (b) Seema evaded ₹1.2 crore for the first time; (c) Ajay, earlier convicted, evaded ₹40 lakh. Examine arrest powers and safeguards.',
          'solution': [table(['Person', 'Analysis', 'Arrest?'], [
              ['Mehul', f'Offence under section 132 with tax of ₹{inr(a)} above ₹2 crore', 'Yes — non-cognizable and bailable, as tax is not above ₹5 crore'],
              ['Seema', 'Below ₹2 crore, first offence', 'No'],
              ['Ajay', 'Repeat offender — monetary limit does not apply', 'Yes'],
              ['Safeguards', 'Inform grounds; produce before Magistrate within 24 hours for cognizable offence; bail by Deputy/Assistant Commissioner for bailable', '—']], title='Section 69 read with 132')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 67(1): an officer not below Joint Commissioner may authorise inspection of a business place, or a transporter\'s or warehouse premises, on reasons to believe that a taxpayer hid supplies or stock, claimed excess ITC, contravened the Act to evade tax, or a transporter or warehouse keeper is handling goods that escaped tax or keeps accounts so as to aid evasion.',
            'Authorisation is given in writing (INS-01). Inspection is less intrusive than search and is directed at verifying records and goods.',
            'Reasons to believe must be based on credible material, not mere suspicion.'],
          'Inspection is a look; search is a hunt.',
          'Suspected stock suppression can lead to inspection of a godown.'),
        C('c2', T2, [
            'Section 67(2): where the Joint Commissioner has reasons to believe goods liable to confiscation or documents relevant to proceedings are hidden, he may authorise search and seizure. Goods may be seized; if seizure is not practicable, a prohibitory order (INS-04) may be issued.',
            'Safeguards: seized documents are retained only as long as needed; the person may take copies; a notice regarding seized goods must be issued within six months (extendable by six months) or the goods returned; goods may be released provisionally on bond and security or on payment of tax, interest and penalty; searches follow the Bharatiya Nagarik Suraksha Sanhita provisions, with witnesses and an inventory.',
            'Perishable or hazardous goods may be disposed of; section 68 empowers inspection of goods in movement with prescribed documents.'],
          'Search requires strong reasons and comes with safeguards.',
          'Goods seized on 1 May must get a notice by 1 November unless the period is extended.'),
        C('c3', T3, [
            'Section 69: the Commissioner may authorise arrest if he has reason to believe a person committed offences under section 132(1)(a) to (d) (fake invoices, supplies without invoice, wrongful ITC or refunds) involving tax above ₹2 crore, or a repeat offender regardless of amount.',
            'Offences with tax above ₹5 crore are cognizable and non-bailable; others are non-cognizable and bailable. For cognizable offences, the person is informed of the grounds and produced before a Magistrate within 24 hours; for bailable offences, the Deputy or Assistant Commissioner can release on bail.',
            'Procedural safeguards include recording reasons, informing a nominated person, and medical examination where needed.'],
          'Arrest is reserved for serious or repeat fraud.',
          'An evasion of ₹1.2 crore by a first offender does not justify arrest.'),
        C('c4', T4, [
            'Section 70: a proper officer may summon any person to give evidence or produce documents in an inquiry; the proceedings are judicial proceedings for IPC/BNS purposes, and persons summoned may appear through authorised representatives where permitted.',
            'Section 71: an officer authorised by the Joint Commissioner may access any business place of a registered person to inspect books, documents, computers and records; the person must produce records such as audited accounts, cost audit reports, income-tax audit reports and other prescribed documents within 15 working days.',
            'Section 72 requires government officers, police, railways and others to assist GST officers.'],
          'Summons and access support investigation without search.',
          'An officer may visit a business and ask for audited accounts under section 71.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Search response protocol', 'role': 'In-house counsel',
             'situation': 'GST officers arrive with a search authorisation.',
             'steps': ['Verify authorisation and identity.', 'Ensure witnesses and inventory.', 'Seek copies of seized documents.', 'Track six-month notice deadline and seek provisional release.'],
             'takeaway': 'Knowing the safeguards protects the business during searches.'}]

    mcqs = [
        Q('m1', 'Inspection under section 67 must be authorised by an officer not below:', ['Joint Commissioner', 'Assistant Commissioner', 'Superintendent', 'Inspector'], 0,
          'Section 67(1). In practice: INS-01.', 'c1', T1),
        Q('m2', 'If no notice is issued within six months of seizure, seized goods must be:', ['Returned, unless the period is extended', 'Confiscated', 'Auctioned', 'Held indefinitely'], 0,
          'Section 67(7). In practice: extension up to six months.', 'c2', T2),
        Q('m3', 'Where seizure is not practicable, the officer may:', ['Issue a prohibitory order', 'Arrest the owner', 'Destroy goods', 'Close the business'], 0,
          'Section 67(2). In practice: INS-04.', 'c2', T2),
        Q('m4', 'Arrest under section 69 generally requires tax involved to exceed:', ['Two crore rupees', 'Five crore rupees', 'One crore rupees', 'Fifty lakh rupees'], 0,
          'Section 132. In practice: repeat offenders excepted.', 'c3', T3),
        Q('m5', 'Offences with tax above ₹5 crore under section 132(1)(a)–(d) are:', ['Cognizable and non-bailable', 'Non-cognizable and bailable', 'Civil only', 'Compoundable only'], 0,
          'Section 132(5). In practice: Magistrate within 24 hours.', 'c3', T3),
        Q('m6', 'A person arrested for a cognizable offence must be produced before a Magistrate within:', ['Twenty-four hours', 'Forty-eight hours', 'Seven days', 'Twelve hours'], 0,
          'Section 69(2). In practice: excluding journey time.', 'c3', T3),
        Q('m7', 'Summons proceedings under section 70 are deemed:', ['Judicial proceedings', 'Administrative only', 'Civil suits', 'Arbitration'], 0,
          'Section 70(2). In practice: false evidence punishable.', 'c4', T4),
        Q('m8', 'Records demanded under section 71 must be produced within:', ['Fifteen working days', 'Seven days', 'Thirty days', 'Twenty-four hours'], 0,
          'Section 71(2). In practice: extendable.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Notice deadline', 2, 'analysis', 'six months', nums=[m]), S('s2', 'Provisional release', 2, 'analysis', 'bond')],
          ['Cite section 67(7).'], ['Assuming automatic confiscation.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Threshold and repeat offence', 3, 'analysis', '2 crore', nums=[a]), S('s2', 'Safeguards', 2, 'analysis', '24 hours')],
          ['Classify offence.'], ['Arresting for ₹1.2 crore first offence.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is the difference between inspection and search?', 'Inspection verifies records and goods; search looks for hidden goods or documents and allows seizure.',
          [P('p1', 'Verify', 5, 'verif'), P('p2', 'Seizure', 5, 'seizure')], 'c2'),
        V('v2', 'How can seized goods be released provisionally?', 'On executing a bond with security, or on payment of tax, interest and penalty.',
          [P('p1', 'Bond', 5, 'bond'), P('p2', 'Security', 5, 'security')], 'c2'),
        V('v3', 'Who can grant bail for a bailable GST offence?', 'The Deputy or Assistant Commissioner.',
          [P('p1', 'Deputy', 5, 'deputy'), P('p2', 'Assistant Commissioner', 5, 'assistant commissioner')], 'c3'),
        V('v4', 'Which law governs search procedure?', 'The Bharatiya Nagarik Suraksha Sanhita, 2023 provisions on searches.',
          [P('p1', 'BNSS', 5, 'nagarik'), P('p2', 'Searches', 5, 'search')], 'c2'),
        V('v5', 'Name two records producible under section 71.', 'Audited annual accounts and the income-tax audit report.',
          [P('p1', 'Audited accounts', 5, 'audited'), P('p2', 'Income-tax audit', 5, 'income-tax audit')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Fake invoice racket', 'difficulty': 'moderate',
              'case': 'Investigations show Prakash issued fake invoices passing ITC of ₹6 crore without any supply.',
              'mcqs': [
                  M('k1a', 'Is the offence cognizable?', ['Yes, above ₹5 crore', 'No', 'Only if repeated', 'Only after conviction'], 0,
                    'Section 132(5). In practice: non-bailable.', 'core', topic=T3),
                  M('k1b', 'Amount by which it exceeds the cognizable threshold (₹ crore):', ['1', '4', '6', '2'], 0,
                    '6 − 5. In practice: any excess suffices.', 'core', check=1, topic=T3),
                  M('k1c', 'Who authorises the arrest?', ['The Commissioner', 'Any inspector', 'The Magistrate first', 'The GST Council'], 0,
                    'Section 69(1). In practice: reasons to believe.', 'core', topic=T3),
                  M('k1d', 'Production before Magistrate within (hours):', ['24', '48', '72', '12'], 0,
                    'Safeguard. In practice: excluding travel time.', 'core', check=24, topic=T3),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch18', 1, 'Inspection, Search, Seizure and Arrest',
                ['Apply inspection powers.',
                 'Apply search and seizure powers and safeguards.',
                 'Apply arrest provisions and safeguards.',
                 'Apply summons and access provisions.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 15}, 'prereq': ['fin-p5-ch17-u01'],
                 'exam_tip': 'Name the authorising officer, the threshold and the safeguard for each power.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 67 inspection/search by JC authorisation.', 'Seized goods: notice in 6 + 6 months; provisional release.', 'Section 69 arrest: > ₹2 crore or repeat; > ₹5 crore cognizable.',
                             'Section 70 summons; section 71 access; 15 working days.'],
                 'remember': ['Bail by Deputy/Assistant Commissioner for bailable offences.'],
                 'traps': ['Treating every evasion as arrestable.']},
                [('Inspection/search', 'Section 67'), ('Arrest', 'Section 69'), ('Summons', 'Section 70'), ('Access', 'Section 71')],
                viva, cases)
