"""CA Final · Paper 4 · Chapter 14 Income-tax Authorities.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch14-u01'
T1 = 'Classes of authorities, instructions and charter'
T2 = 'Jurisdiction and faceless proceedings'
T3 = 'Search, seizure and requisition'
T4 = 'Survey and power to call for information'


def build():
    ck = Checks()
    ex = ck.add('(5000000-500000)+(0-3000000)', 'Excess seized money (₹)')
    it = ck.add('((5000000-500000)+(0-3000000))*0.005*10', 'Interest for 10 months at 0.5% (₹)')
    i1 = {'id': 'i1', 'title': 'Interest on excess seized money', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'In a search, ₹50,00,000 cash was seized from Navin. ₹5,00,000 was released under section 250(2). No assets were sold. Liabilities determined on assessment were ₹30,00,000. The interest period (from the day after 120 days of the last authorisation to completion of assessment) is 10 months. Compute interest payable by the Government.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Excess (A − B) + (C − D)', '(50,00,000 − 5,00,000) + (0 − 30,00,000)', inr(ex)],
              ['Interest', '0.5% per month × 10 months', inr(it)]], title='Section 250(8)')],
          'checks': list(ck)}

    c2 = Checks()
    d = c2.add('15+31+31+30+13', 'Days from 16 June to 13 October 2026')
    i2 = {'id': 'i2', 'title': 'Release of seized assets — timelines', 'difficulty': 'core', 'minutes': 5,
          'q': 'The last authorisation for a search on Seema was executed on 15 June 2026, when jewellery was seized. By when must she apply for release, and by when must the AO release the assets if the conditions are met?',
          'solution': [table(['Step', 'Rule', 'Date'], [
              ['Application', '30 days from end of month of seizure', '30 July 2026'],
              ['Release', '120 days from the last authorisation', f'13 October 2026 ({d} days)'],
              ['Conditions', 'Source explained, liabilities recovered, approval of PCCIT/CCIT/PCIT/CIT', '—']], title='Section 250(2) and (3)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 236 lists income-tax authorities: the CBDT (constituted under the Central Board of Revenue Act, 1963), Principal Directors-General/Principal Chief Commissioners, Directors-General/Chief Commissioners, Principal Directors/Principal Commissioners, Directors/Commissioners including CIT(Appeals), Additional and Joint Directors/Commissioners, Deputy and Assistant Directors/Commissioners, Income-tax Officers, Tax Recovery Officers and Inspectors.',
            'Section 239 lets the CBDT issue orders, instructions and directions to subordinate authorities, which they must follow — but it cannot require any authority to make a particular assessment or dispose of a case in a particular manner, nor interfere with CIT(Appeals). Circulars relaxing provisions for taxpayers are binding on the department.',
            'Section 240 empowers the CBDT to adopt and publish a Taxpayer\'s Charter setting out the department\'s commitments (fairness, courtesy, timely decisions) and taxpayers\' expectations (honesty, compliance, record-keeping).'],
          'The CBDT guides but cannot dictate an assessment.',
          'A CBDT circular extending a filing date binds every AO.'),
        C('c2', T2, [
            'Section 241 lets the CBDT and higher authorities direct which authorities exercise jurisdiction by area, persons, income or cases; higher authorities can exercise lower authorities\' powers. Section 242 confers jurisdiction on AOs; an assessee can question jurisdiction only within prescribed time.',
            'Section 243 permits transfer of cases between AOs after giving an opportunity of being heard (except where transfer is within the same city or locality). Section 244 lets a successor authority continue proceedings from where they stood.',
            'Section 245 enables faceless jurisdiction: the CBDT may notify schemes under which functions are performed electronically with dynamic allocation of cases and no physical interface.'],
          'Jurisdiction flows from directions; faceless schemes remove the face-to-face meeting.',
          'A case transferred from Pune to Mumbai requires a hearing before the order.'),
        C('c3', T3, [
            'Section 246 gives authorities civil-court powers (discovery, summons, production of documents, commissions). Section 247: on information that a person has failed to produce documents, would not produce them, or holds undisclosed money, bullion, jewellery, virtual digital assets or valuables, specified authorities may authorise a search. The authorised officer can enter, break open locks, search persons, seize books and assets (stock-in-trade is only inventoried), and record statements on oath that can be used as evidence. Reasons to believe are not disclosed to the assessee (section 249).',
            'Section 248: requisition of books or assets held by other authorities. Section 251 presumes seized books and assets belong to the person searched and that their contents are true.',
            'Section 250: seized assets may be applied against existing liabilities. The person may apply for release within 30 days from the end of the month of seizure; if source is explained, liabilities recovered and approval obtained, assets are released within 120 days of the last authorisation. The Government pays 0.5% interest per month on excess seized money from 120 days after the last authorisation until assessment.'],
          'Search is the most intrusive power; strict timelines protect the taxpayer.',
          'Excess seized money of ₹15 lakh for 10 months earns interest of ₹75,000.'),
        C('c4', T4, [
            'Section 253 (survey): an authority may enter business, professional or charitable premises within jurisdiction during working hours (business premises) or between sunrise and sunset (other places) to inspect books, verify cash, stock and valuables, place marks of identification, make inventories and record statements on oath that may be relevant to any proceeding under the Act (section 253(5)).',
            'The officer may impound books but not remove cash or stock, recording reasons and retaining them for up to 15 days (excluding holidays) unless approval for longer retention is obtained. A survey can also be conducted after a function or ceremony to check expenditure.',
            'Sections 252, 254 and 255 empower authorities to call for information from any person, collect information for verification and inspect company registers; section 260 enables faceless collection of information.'],
          'Survey verifies on the spot; search takes away.',
          'Books impounded in a survey cannot be kept beyond 15 working days without approval.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Responding to a survey', 'role': 'Tax consultant',
             'situation': 'A client\'s shop is visited by survey officers.',
             'steps': ['Verify the authorisation and timing.', 'Assist with cash and stock verification.', 'Note any impounded books and the 15-day limit.', 'Prepare reconciliation of discrepancies.'],
             'takeaway': 'Knowing the limits of survey powers keeps the process fair.'}]

    mcqs = [
        Q('m1', 'The CBDT cannot direct an AO to:', ['Make a particular assessment', 'Follow a circular', 'Use faceless procedures', 'Grant an extension'], 0,
          'Section 239 restriction. In practice: independence of AO.', 'c1', T1),
        Q('m2', 'The CBDT is constituted under:', ['The Central Board of Revenue Act, 1963', 'The Income-tax Act, 2025', 'The Companies Act, 2013', 'The RBI Act'], 0,
          'Statutory body. In practice: under Ministry of Finance.', 'c1', T1),
        Q('m3', 'Transfer of a case within the same city requires:', ['No opportunity of hearing', 'Hearing and reasons', 'Court approval', 'Assessee consent'], 0,
          'Section 243 exception. In practice: other transfers need a hearing.', 'c2', T2),
        Q('m4', 'During search, stock-in-trade is:', ['Inventoried but not seized', 'Always seized', 'Sold immediately', 'Ignored'], 0,
          'Section 247. In practice: kept with assessee.', 'c3', T3),
        Q('m5', 'Application for release of seized assets must be made within:', ['Thirty days from end of month of seizure', 'Sixty days of search', 'Fifteen days of seizure', 'One hundred and twenty days'], 0,
          'Section 250(2). In practice: explain source.', 'c3', T3),
        Q('m6', 'Interest on excess seized money is paid at:', ['Half percent per month', 'One percent per month', 'Six percent per year', 'Nil'], 0,
          'Section 250(8). In practice: formula-based.', 'c3', T3),
        Q('m7', 'Books impounded in a survey can be retained without approval for:', ['Fifteen days excluding holidays', 'Thirty days', 'Ten days', 'Sixty days'], 0,
          'Section 253. In practice: longer needs approval.', 'c4', T4),
        Q('m8', 'During a survey, the officer can:', ['Verify cash and stock', 'Seize cash', 'Arrest the owner', 'Remove stock'], 0,
          'No seizure. In practice: inventory and marks.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Excess amount', 3, 'computation', 'excess', nums=[ex]), S('s2', 'Interest', 2, 'computation', 'interest', nums=[it])],
          ['State the formula.'], ['Ignoring liabilities.'], ['Formula first.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Application date', 2, 'analysis', 'thirty days'), S('s2', 'Release date', 2, 'analysis', '120 days')],
          ['List conditions.'], ['Counting from date of application.'], ['Timeline.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is the purpose of the Taxpayer\'s Charter?', 'To set out the department\'s commitments to taxpayers and what it expects from taxpayers.',
          [P('p1', 'Commitments', 5, 'commitment'), P('p2', 'Expectations', 5, 'expect')], 'c1'),
        V('v2', 'Can statements be recorded on oath during a survey under the 2025 Act?', 'Yes, section 253(5) allows the authority to record statements on oath useful for any proceeding under the Act.',
          [P('p1', 'On oath', 5, 'on oath'), P('p2', 'Section 253(5)', 5, '253')], 'c4'),
        V('v3', 'What presumption arises about seized books?', 'They are presumed to belong to the person searched and their contents are presumed true.',
          [P('p1', 'Belong', 5, 'belong'), P('p2', 'True', 5, 'true')], 'c3'),
        V('v4', 'What is faceless jurisdiction?', 'Electronic performance of functions with dynamic allocation of cases and no physical interface.',
          [P('p1', 'Electronic', 5, 'electronic'), P('p2', 'Dynamic allocation', 5, 'dynamic')], 'c2'),
        V('v5', 'Within what time must seized assets be released?', 'Within 120 days from the last authorisation, if conditions are met.',
          [P('p1', 'One hundred twenty days', 5, '120'), P('p2', 'Last authorisation', 5, 'authorisation')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Survey at Maple Electronics', 'difficulty': 'core',
              'case': 'Survey officers visit Maple Electronics\' showroom at 11 a.m. They find cash of ₹4,00,000 against a cash book balance of ₹1,50,000, and impound the stock register. The owner asks whether they can take the excess cash.',
              'mcqs': [
                  M('k1a', 'Excess cash found (₹):', ['2,50,000', '4,00,000', '1,50,000', '5,50,000'], 0,
                    '4,00,000 − 1,50,000. In practice: explain source.', 'core', check=250000, topic=T4),
                  M('k1b', 'Can the officers remove the excess cash?', ['No, survey does not permit removal of cash', 'Yes, always', 'Only with consent', 'Only if above ₹1 lakh'], 0,
                    'Section 253. In practice: search needed to seize.', 'core', topic=T4),
                  M('k1c', 'The stock register can be retained without approval for up to (days, excluding holidays):', ['15', '30', '10', '60'], 0,
                    'Section 253. In practice: approval for longer.', 'core', check=15, topic=T4),
                  M('k1d', 'The survey at the showroom may continue:', ['Beyond business hours once started during them', 'Only until 5 p.m.', 'Only on holidays', 'Only at night'], 0,
                    'Business premises rule. In practice: cooperate.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch14', 1, 'Income-tax Authorities',
                ['Identify income-tax authorities and limits on CBDT instructions.',
                 'Apply jurisdiction, transfer and faceless provisions.',
                 'Apply search, seizure and requisition powers and timelines.',
                 'Apply survey and information-gathering powers.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p4-ch13-u01'],
                 'exam_tip': 'Contrast search and survey: seizure, oath, timing and retention limits.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 236 authorities; 239 instructions; 240 charter.', 'Sections 241–245 jurisdiction and faceless.', 'Section 247 search; 250 seized assets: 30 days, 120 days, 0.5% interest.',
                             'Section 253 survey: impound up to 15 days.'],
                 'remember': ['Survey cannot seize cash or stock.'],
                 'traps': ['Assuming cash or stock can be seized in a survey.']},
                [('Authorities', 'Section 236'), ('Search', 'Section 247'), ('Seized assets', 'Section 250'), ('Survey', 'Section 253')],
                viva, cases)
