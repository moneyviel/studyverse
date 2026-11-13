"""CA Final · Paper 1 Financial Reporting · Chapter 16 Professional and Ethical Duty of a Chartered Accountant.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch16-u01'
T1 = 'The Code of Ethics and its conceptual framework'
T2 = 'Fundamental principles'
T3 = 'Threats and safeguards for accountants in business'
T4 = 'Misconduct under the Chartered Accountants Act'


def build():
    ck = Checks()
    infl = ck.add('12-8', 'Overstatement of profit from deferring the write-down (₹ crore)')
    bonus = ck.add('(12-8)*0.02', 'Extra bonus to the CFO from the overstatement (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Pressure to delay a write-down', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Ritu, a CA and CFO of Arrow Ltd., estimates that inventory needs a write-down of ₹12 crore. The MD wants only ₹8 crore booked this year "to meet analyst targets", and Ritu\'s bonus is 2% of profit. Quantify the effect and set out her ethical analysis.',
          'solution': [table(['Step', 'Analysis', 'Result'], [
              ['Overstatement of profit', '12 − 8', '₹' + inr(infl) + ' crore'],
              ['Personal gain to Ritu', '2% × 4', '₹' + inr(bonus) + ' crore — self-interest threat'],
              ['Other threat', 'MD pressure — intimidation threat', 'Integrity and objectivity at risk'],
              ['Safeguards', 'Discuss with MD; escalate to audit committee; document; consult', '—'],
              ['If unresolved', 'Refuse to be associated with misleading information; consider resigning', '—']], title='Conceptual framework applied')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Which principle is at stake?', 'difficulty': 'core', 'minutes': 6,
          'q': 'Name the main principle involved: (a) a CA in industry shares the company\'s unreleased results with a friend; (b) she prepares lease accounting without understanding Ind AS 116; (c) she signs off revenue she knows is fictitious; (d) she accepts expensive gifts from a supplier whose invoices she approves; (e) she posts derogatory comments about a competitor firm.',
          'solution': [table(['Item', 'Principle'], [
              ['(a)', 'Confidentiality'],
              ['(b)', 'Professional competence and due care'],
              ['(c)', 'Integrity'],
              ['(d)', 'Objectivity'],
              ['(e)', 'Professional behaviour']], title='Fundamental principles')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'ICAI\'s Code of Ethics (effective 1 July 2020) is based on the IESBA Code issued by IFAC. It sets fundamental principles reflecting the profession\'s duty to act in the public interest.',
            'The conceptual framework requires an accountant to identify threats to compliance with the fundamental principles, evaluate whether they are at an acceptable level, and address them by eliminating the circumstances, applying safeguards, or declining or ending the activity.',
            'A reasonable and informed third party test is used to judge whether a threat is acceptable. Requirements for audit independence are covered in the auditing paper.'],
          'Identify, evaluate, address — the three-step ethical method.',
          'Pressure to hit targets is a threat to evaluate, not a reason to comply.'),
        C('c2', T2, [
            'Integrity: being straightforward and honest; not being knowingly associated with reports that contain materially false or misleading statements, are furnished recklessly, or omit information so as to mislead.',
            'Objectivity: not compromising judgement because of bias, conflict of interest or undue influence. Professional competence and due care: maintaining knowledge and skill, and acting diligently under applicable standards.',
            'Confidentiality: respecting information acquired through work, not disclosing it without proper authority or a legal or professional duty, and not using it for personal advantage. Professional behaviour: complying with laws and avoiding conduct that discredits the profession.'],
          'Five principles: integrity, objectivity, competence and due care, confidentiality, professional behaviour.',
          'Using inside information to trade breaches confidentiality.'),
        C('c3', T3, [
            'Threat categories: self-interest (financial or other interests influencing judgement), self-review (evaluating own previous work), advocacy (promoting a position so far that objectivity suffers), familiarity (long or close relationships), and intimidation (actual or perceived pressure).',
            'For accountants in business, typical situations: pressure to manipulate figures, incentive schemes linked to results, conflicts of interest, preparing information that is misleading, and inducements such as gifts.',
            'Safeguards and responses: discussing with superiors, escalating to those charged with governance, consulting professional bodies or legal advisers, documenting the matter, and if needed refusing to remain associated or resigning. Responding to non-compliance with laws and regulations (NOCLAR) may require reporting to appropriate authorities.'],
          'Name the threat, then pick a response proportionate to it.',
          'A bonus tied to profit creates a self-interest threat for the CFO.'),
        C('c4', T4, [
            'Under section 22 of the Chartered Accountants Act, 1949, "professional or other misconduct" includes acts or omissions in the Schedules. Section 21 provides for disciplinary action.',
            'First Schedule: Part I (members in practice), Part II (members in service), Part III (members generally) and Part IV (other misconduct). Second Schedule: Part I (in practice), Part II (members generally) and Part III (other misconduct). Second Schedule matters are graver.',
            'Other misconduct covers conduct outside professional work that brings disrepute to the profession, reflecting the expectation of integrity in personal affairs as well.'],
          'Both work and personal conduct can lead to disciplinary action.',
          'A CA in service who knowingly certifies false accounts faces Second Schedule charges.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Handling management override', 'role': 'Financial controller (CA)',
             'situation': 'The CEO instructs that a large customer\'s sales be recognised before delivery.',
             'steps': ['Identify the threat and principle at risk.', 'Explain the Ind AS 115 requirement to the CEO.', 'Escalate to the audit committee if pressure continues.', 'Document and consider resignation if unresolved.'],
             'takeaway': 'Ethical duty comes before employer instructions.'}]

    mcqs = [
        Q('m1', 'ICAI\'s Code of Ethics is derived from:', ['The IESBA Code issued by IFAC', 'SEBI regulations', 'Companies Act', 'US GAAP'], 0,
          'International alignment. In practice: effective 1 July 2020.', 'c1', T1),
        Q('m2', 'Being knowingly associated with misleading financial information breaches:', ['Integrity', 'Confidentiality', 'Competence', 'Professional behaviour only'], 0,
          'Integrity requires honesty. In practice: refuse association.', 'c2', T2),
        Q('m3', 'Pressure from a superior threatening dismissal is a:', ['Intimidation threat', 'Self-review threat', 'Advocacy threat', 'Familiarity threat'], 0,
          'Actual or perceived pressure. In practice: escalate.', 'c3', T3),
        Q('m4', 'A profit-linked bonus for the CFO creates a:', ['Self-interest threat', 'Self-review threat', 'Familiarity threat', 'Advocacy threat'], 0,
          'Financial interest in outcomes. In practice: governance oversight.', 'c3', T3),
        Q('m5', 'The conceptual framework requires an accountant to:', ['Identify, evaluate and address threats', 'Ignore minor threats', 'Report all threats to police', 'Resign immediately'], 0,
          'Three steps. In practice: document evaluation.', 'c1', T1),
        Q('m6', 'Professional or other misconduct is defined by reference to the Schedules under:', ['Section 22 of the CA Act, 1949', 'Section 129 of the Companies Act', 'SEBI LODR', 'Income-tax Act'], 0,
          'Section 21 covers disciplinary action. In practice: schedules list acts.', 'c4', T4),
        Q('m7', 'Other misconduct relates to:', ['Conduct outside professional work bringing disrepute', 'Only audit work', 'Only tax work', 'Only practice'], 0,
          'Personal conduct counts. In practice: First Schedule Part IV.', 'c4', T4),
        Q('m8', 'Using employer\'s confidential data for personal share trading breaches:', ['Confidentiality', 'Competence', 'Objectivity only', 'No principle'], 0,
          'Information must not be used for personal advantage. In practice: also insider trading law.', 'c2', T2),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Quantification', 1.5, 'computation', 'overstatement|bonus', nums=[infl, bonus]), S('s2', 'Threats', 1.5, 'concept', 'self-interest|intimidation'), S('s3', 'Safeguards', 2, 'concept', 'escalat|audit committee'), S('s4', 'Outcome', 1, 'concept', 'resign|refuse')],
          ['Name threats and principles.'], ['Agreeing to a compromise figure.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Confidentiality and integrity', 2, 'concept', 'confidential|integrity'), S('s2', 'Competence and objectivity', 2, 'concept', 'competence|objectiv'), S('s3', 'Behaviour', 1, 'concept', 'behaviour')],
          ['One principle each.'], ['Mixing integrity and objectivity.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Name the five fundamental principles.', 'Integrity, objectivity, professional competence and due care, confidentiality, and professional behaviour.',
          [P('p1', 'Integrity and objectivity', 5, 'integrity|objectivity'), P('p2', 'Competence, confidentiality, behaviour', 5, 'competence|confidential|behaviour')], 'c2'),
        V('v2', 'What are the steps of the conceptual framework?', 'Identify threats, evaluate whether they are acceptable, and address them by removing causes, applying safeguards or declining the activity.',
          [P('p1', 'Identify and evaluate', 5, 'identify|evaluate'), P('p2', 'Address', 5, 'address|safeguard')], 'c1'),
        V('v3', 'List the five threat categories.', 'Self-interest, self-review, advocacy, familiarity and intimidation.',
          [P('p1', 'Self-interest and self-review', 5, 'self-interest|self-review'), P('p2', 'Advocacy, familiarity, intimidation', 5, 'advocacy|familiarity|intimidation')], 'c3'),
        V('v4', 'What should a CA in business do under pressure to misstate?', 'Discuss with management, escalate to those charged with governance, consult, document, and if unresolved refuse association or resign.',
          [P('p1', 'Escalate', 5, 'escalat|governance'), P('p2', 'Refuse or resign', 5, 'resign|refuse')], 'c3'),
        V('v5', 'Which section of the CA Act defines misconduct?', 'Section 22, by reference to acts or omissions listed in the Schedules, with discipline under section 21.',
          [P('p1', 'Section 22', 5, '22'), P('p2', 'Schedules', 5, 'schedule')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Vertex Pharma Ltd.', 'difficulty': 'moderate',
              'case': 'Kunal, a CA, heads accounts at Vertex Pharma Ltd. His brother owns a firm bidding for a logistics contract that Kunal evaluates. The CEO asks Kunal to classify a ₹15 crore one-off litigation settlement as "other expenses" spread over two years. Kunal recently qualified and has not studied Ind AS 37 in depth.',
              'mcqs': [
                  M('k1a', 'The brother\'s bid creates mainly a:', ['Self-interest threat to objectivity', 'Self-review threat', 'Advocacy threat', 'No threat'], 0,
                    'Family interest in the outcome. In practice: declare and withdraw from evaluation.', 'core', topic=T3),
                  M('k1b', 'Spreading the settlement over two years would breach:', ['Integrity', 'Confidentiality', 'Professional behaviour only', 'No principle'], 0,
                    'It misstates profit knowingly. In practice: Ind AS 37 requires recognition when obligation arises.', 'core', topic=T2),
                  M('k1c', 'Kunal\'s gap in Ind AS 37 knowledge relates to:', ['Professional competence and due care', 'Objectivity', 'Integrity', 'Confidentiality'], 0,
                    'He must obtain advice or training. In practice: consult experts.', 'core', topic=T2),
                  M('k1d', 'If the CEO insists, Kunal\'s appropriate step is to:', ['Escalate to the audit committee', 'Comply quietly', 'Post on social media', 'Inform competitors'], 0,
                    'Those charged with governance oversee reporting. In practice: document.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch16', 1, 'Professional and Ethical Duty of a Chartered Accountant',
                ['Explain the Code of Ethics and its conceptual framework.',
                 'Apply the five fundamental principles.',
                 'Identify threats and safeguards for accountants in business.',
                 'Describe professional and other misconduct under the CA Act.'],
                {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 25}, 'prereq': ['fin-p1-ch15-u01'],
                 'exam_tip': 'In ethics cases: name the principle, name the threat, propose safeguards, conclude.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['ICAI Code based on IESBA; effective 1 July 2020.',
                             'Identify, evaluate, address threats.',
                             'Five fundamental principles.',
                             'Five threat categories.',
                             'Misconduct under section 22; discipline under section 21.'],
                 'remember': ['Escalate to those charged with governance.'],
                 'traps': ['Treating pressure as a valid reason to comply.']},
                [('Principles', 'I, O, C&DC, C, PB'), ('Threats', 'SI, SR, A, F, I'), ('Method', 'Identify → evaluate → address'), ('CA Act', 'Sections 21, 22')],
                viva, cases)
