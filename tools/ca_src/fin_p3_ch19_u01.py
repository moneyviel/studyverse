"""CA Final · Paper 3 Advanced Auditing, Assurance and Professional Ethics · Chapter 19 Professional Ethics & Liabilities of Auditors.
Scope follows the ICAI study material (Guidelines on Ethical Issues, 2026); explanations and cases are original."""
from fkit import *

UID = 'fin-p3-ch19-u01'
T1 = 'Code of Ethics: principles, threats and NOCLAR'
T2 = 'Membership, certificate of practice and deemed practice'
T3 = 'Misconduct under the Schedules and disciplinary procedure'
T4 = 'Guidelines on Ethical Issues, 2026 and self-regulatory measures'


def build():
    ck = Checks()
    lim_firm = ck.add('3*40', 'Company audit limit for a 3-partner firm (assignments)')
    tax_lim = ck.add('3*60', 'Tax audit limit for a 3-partner firm in a year (assignments)')
    i1 = {'id': 'i1', 'title': 'How many audits can the firm take?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'R & Co. has three full-time practising partners. Under the Guidelines on Ethical Issues, 2026, compute the firm\'s ceiling on company audits and on tax audits in a financial year. Do OPC audits or tax audits of 44AD/44ADA/44AE assessees count?',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Company audit limit', '40 per partner × 3', inr(lim_firm) + ' (OPCs and dormant companies excluded)'],
              ['Tax audit limit', '60 per partner × 3', inr(tax_lim) + ' per financial year'],
              ['44AD/44ADA/44AE audits', 'Specifically excluded from the count', 'Not counted'],
              ['Branches', 'HO and branches of one entity count as one assignment', '—']], title='Specified number of assignments')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Is this misconduct?', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Decide: (a) CA A accepts audit of a company whose previous auditor\'s undisputed audit fee is unpaid; the company\'s net worth is positive. (b) CA B allows his non-CA brother to sign certificates in B\'s name. (c) CA C, in practice, does not keep books of account for his practice since his income is below section 44AA limits. (d) CA D discloses client information to a regulator as required by law.',
          'solution': [table(['Case', 'Position'], [
              ['(a)', 'Misconduct under the 2026 Guidelines (Chapter IV) — exemption only for sick units or insolvency cases'],
              ['(b)', 'Misconduct — First Schedule Part I, clause (1): allowing a non-CA to practise in his name'],
              ['(c)', 'Misconduct — Guidelines require cash book, ledger and bill register regardless of 44AA'],
              ['(d)', 'Not misconduct — disclosure required by law is permitted']], title='Professional ethics cases')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'The ICAI Code of Ethics (based on the IESBA Code) sets fundamental principles — integrity, objectivity, competence with due care, confidentiality and professional behaviour — and a conceptual framework to identify, evaluate and address threats (self-interest, self-review, advocacy, familiarity, intimidation).',
            'Independence of mind and in appearance is required for audit and assurance engagements; safeguards or refusal apply where threats cannot be reduced to an acceptable level.',
            'NOCLAR (non-compliance with laws and regulations) provisions guide professional accountants who become aware of actual or suspected non-compliance: understand the matter, discuss with management and TCWG, consider further action including disclosure to authorities where appropriate, and document.'],
          'Principles plus a threat-safeguard method govern every ethical decision.',
          'A CA learning of a client\'s environmental violation follows NOCLAR steps.'),
        C('c2', T2, [
            'A person becomes a member on registration with ICAI; disabilities include being under 21, unsound mind, undischarged insolvent, conviction of certain offences, or removal for misconduct. Members are associates (ACA) or fellows (FCA). Names may be removed (death, request, non-payment of fees, misconduct) and restored.',
            'A member in practice must hold a certificate of practice; members are deemed to be in practice if they hold themselves out, offer services, or render professional services including those permitted by the Council (e.g. management consultancy).',
            'Companies cannot engage in accountancy; practising members cannot use designations other than CA (except permitted ones) and must follow rules on branch offices and KYC norms for clients.'],
          'The certificate of practice defines who can practise as a CA.',
          'A CA offering tax services publicly without a certificate of practice breaches the Act.'),
        C('c3', T3, [
            'Section 22 defines professional or other misconduct by reference to the Schedules. First Schedule: Part I (members in practice), Part II (members in service), Part III (members generally), Part IV (other misconduct). Second Schedule: Part I (in practice), Part II (generally), Part III (other misconduct) — graver matters such as gross negligence and false certification.',
            'Examples: allowing a non-CA to practise in one\'s name; sharing fees with non-members; soliciting clients; advertising beyond guidelines; accepting audit without communicating with the previous auditor in writing; certifying without proper examination; disclosing client information without consent.',
            'Disciplinary mechanism: Director (Discipline) forms a prima facie opinion; First Schedule matters go to the Board of Discipline and Second Schedule or both to the Disciplinary Committee; penalties include reprimand, removal and fines, with appeals to the Appellate Authority.'],
          'Know which Schedule, which part and which clause.',
          'Not writing to the previous auditor before accepting is professional misconduct.'),
        C('c4', T4, [
            'The Guidelines on Ethical Issues, 2026 include: employees must exercise due diligence; practising members must maintain cash book, ledger and bill register; not accepting audit where the previous auditor\'s undisputed audit fee is unpaid (except sick units and insolvency cases); a ceiling of 40 company audit assignments per practising partner (excluding OPCs and dormant companies); and restrictions on non-audit fees for statutory audits of PSUs, government companies, listed companies and public companies with turnover of ₹250 crore or more.',
            'The Limit on Number of Tax Audits Guidelines, 2025 cap tax audits at 60 per practising partner per financial year, excluding audits under section 44AB clauses (c), (d) and (e) for 44AE, 44ADA and 44AD cases; revised reports and branches do not add assignments.',
            'Recommended self-regulatory measures cover branch and joint audits, ratio of qualified to unqualified staff, disclosure of interests in other firms, and receiving audit fees through banking channels or digital modes. Auditors also face civil liability (negligence), criminal liability (false statements) and Companies Act penalties.'],
          'Specific numeric limits are favourite exam traps.',
          'A three-partner firm can hold up to 120 company audits under the 2026 Guidelines.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Ethics compliance at a CA firm', 'role': 'Practice manager',
             'situation': 'A growing firm with five partners and many tax audits.',
             'steps': ['Maintain register of company and tax audit assignments.', 'Check previous auditor communication and fees before acceptance.', 'Keep proper books of the practice.', 'Review non-audit fees for restricted clients.'],
             'takeaway': 'Ethical limits must be tracked like any other compliance.'}]

    mcqs = [
        Q('m1', 'Under the 2026 Guidelines, the limit on company audit assignments per practising partner is:', ['Forty, excluding OPCs and dormant companies', 'Twenty', 'Sixty', 'Thirty including all companies'], 0,
          'Chapter V. In practice: maintain a register.', 'c4', T4),
        Q('m2', 'The limit on tax audit assignments per practising partner per year is:', ['Sixty', 'Forty', 'Forty-five', 'Unlimited'], 0,
          'Tax audit guidelines. In practice: 44AD/44ADA/44AE excluded.', 'c4', T4),
        Q('m3', 'Allowing a non-member to practise in one\'s name is misconduct under:', ['First Schedule, Part I, clause (1)', 'Second Schedule Part III', 'Section 141', 'No provision'], 0,
          'Professional misconduct. In practice: Board of Discipline.', 'c3', T3),
        Q('m4', 'A practising CA must maintain at minimum:', ['Cash book, ledger and bill register', 'Only bank statements', 'Only a ledger', 'Nothing if income is small'], 0,
          'Guidelines Chapter III. In practice: regardless of 44AA.', 'c4', T4),
        Q('m5', 'Accepting audit where the previous auditor\'s undisputed fee is unpaid is permitted for:', ['A sick unit or a company under insolvency resolution', 'Any listed company', 'Any private company', 'Never'], 0,
          'Exceptions. In practice: check net worth.', 'c4', T4),
        Q('m6', 'NOCLAR provisions deal with:', ['Responding to non-compliance with laws and regulations', 'Audit fees', 'Advertising', 'Peer review'], 0,
          'Code of Ethics. In practice: may disclose to authorities.', 'c1', T1),
        Q('m7', 'Second Schedule matters are referred to:', ['The Disciplinary Committee', 'The Board of Discipline only', 'The QRB', 'NFRA only'], 0,
          'Graver misconduct. In practice: heavier penalties.', 'c3', T3),
        Q('m8', 'A member is deemed to be in practice when he:', ['Holds himself out as a practising CA or offers professional services', 'Is employed full time only', 'Teaches accounting', 'Holds shares'], 0,
          'Section 2(2). In practice: needs COP.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Company audit limit', 2, 'computation', 'company audit', nums=[lim_firm]), S('s2', 'Tax audit limit', 2, 'computation', 'tax audit', nums=[tax_lim]), S('s3', 'Exclusions', 1, 'concept', 'excluded|44ad')],
          ['Count per partner.'], ['Using the old 30 limit.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 8, i2['q'], i2['solution'],
          [S('s1', 'Unpaid fees', 2, 'concept', 'undisputed|sick'), S('s2', 'Practising in name', 2, 'concept', 'clause \\(1\\)|name'), S('s3', 'Books', 2, 'concept', 'cash book|ledger'), S('s4', 'Legal disclosure', 2, 'concept', 'required by law')],
          ['Cite provisions.'], ['Treating legal disclosure as misconduct.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is NOCLAR?', 'Guidance in the Code of Ethics on responding to actual or suspected non-compliance with laws and regulations, including discussion and possible disclosure to authorities.',
          [P('p1', 'Non-compliance with laws', 5, 'non-compliance'), P('p2', 'Disclosure to authorities', 5, 'authorit')], 'c1'),
        V('v2', 'Who is deemed to be in practice?', 'A member who holds out as a practising CA, offers or renders professional services, or performs services permitted by the Council.',
          [P('p1', 'Holds out', 5, 'holds out'), P('p2', 'Professional services', 5, 'services')], 'c2'),
        V('v3', 'How are First and Second Schedule matters handled?', 'First Schedule matters go to the Board of Discipline; Second Schedule or combined matters go to the Disciplinary Committee.',
          [P('p1', 'Board of Discipline', 5, 'board of discipline'), P('p2', 'Disciplinary Committee', 5, 'disciplinary committee')], 'c3'),
        V('v4', 'What are the audit assignment limits under current guidelines?', 'Forty company audits and sixty tax audits a year per practising partner, with specified exclusions.',
          [P('p1', 'Forty company audits', 5, 'forty'), P('p2', 'Sixty tax audits', 5, 'sixty')], 'c4'),
        V('v5', 'Name auditors\' liabilities beyond ICAI discipline.', 'Civil liability for negligence, criminal liability for false statements and penalties under the Companies Act.',
          [P('p1', 'Civil negligence', 5, 'civil|negligence'), P('p2', 'Criminal and penalties', 5, 'criminal|penalt')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Mehta & Co.', 'difficulty': 'moderate',
              'case': 'Mehta & Co. has two practising partners and one part-time practising partner. It holds 75 company audits including 10 OPC audits, and 115 tax audits including 20 under section 44AD. It is offered the statutory audit of a listed company where it already earns consultancy fees above the proposed audit fee.',
              'mcqs': [
                  M('k1a', 'Company audit ceiling for the firm (the part-time partner excluded):', ['80', '120', '60', '40'], 0,
                    '2 × 40. In practice: 65 counted (OPCs excluded).', 'moderate', check=80, topic=T4),
                  M('k1b', 'Tax audits counted towards the limit:', ['95', '115', '120', '20'], 0,
                    '115 − 20 (44AD excluded). In practice: limit 120.', 'moderate', check=95, topic=T4),
                  M('k1c', 'Accepting the listed company audit while consultancy fees exceed audit fees is:', ['Not permitted under the 2026 Guidelines', 'Allowed', 'Required', 'Allowed if disclosed'], 0,
                    'Chapter VI restriction. In practice: also Companies Act section 144.', 'core', topic=T4),
                  M('k1d', 'Before accepting any new audit, the firm must:', ['Communicate in writing with the previous auditor', 'Only phone the client', 'Ignore predecessor', 'Get SEBI approval'], 0,
                    'First Schedule Part I clause (8). In practice: proof of delivery.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p3', 'fin-p3-ch19', 1, 'Professional Ethics & Liabilities of Auditors',
                ['Apply the Code of Ethics, threats and NOCLAR.',
                 'Explain membership and certificate of practice rules.',
                 'Identify misconduct under the Schedules and disciplinary procedure.',
                 'Apply the Guidelines on Ethical Issues, 2026 and tax audit limits.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 30}, 'prereq': ['fin-p3-ch18-u01'],
                 'exam_tip': 'Answer ethics cases in four steps: provision, facts, analysis, conclusion.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Code of Ethics: five principles, threats, NOCLAR.',
                             'COP and deemed practice.',
                             'First and Second Schedule; Board of Discipline vs Disciplinary Committee.',
                             '2026 Guidelines: 40 company audits per partner; books; unpaid fees.',
                             'Tax audits: 60 per partner (44AD/ADA/AE excluded).'],
                 'remember': ['Legal disclosure is not a breach of confidentiality.'],
                 'traps': ['Using older audit limits.']},
                [('Company audits', '40 per partner'), ('Tax audits', '60 per partner'), ('Unpaid fee', 'Except sick/insolvency'), ('Books', 'Cash book, ledger, bill register')],
                viva, cases)
