"""CA Intermediate · Paper 2 Corporate and Other Laws · Chapter 7 Management and Administration (ss. 88–122).
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ch07-u01'
T1 = 'Registers, beneficial interest and annual return (ss. 88–95)'
T2 = 'Annual general meeting (ss. 96–97)'
T3 = 'Extraordinary general meetings, notice and explanatory statement (ss. 98–102)'
T4 = 'Quorum, chairman, proxies and voting (ss. 103–110)'
T5 = 'Resolutions, special notice, filing and minutes (ss. 111–122)'


def build():
    ck = Checks()
    agm1 = ck.add('9', 'First AGM: months from the end of the first financial year')
    gap = ck.add('15', 'Maximum gap between two AGMs (months)')
    sp = ck.add('3*130', 'Minimum votes in favour for a special resolution when 130 vote against')
    i1 = {'id': 'i1', 'title': 'Dates and votes', 'difficulty': 'core', 'minutes': 7,
          'q': '(a) Vriksh Ltd. was incorporated on 10 August 2025 and its first financial year ended on 31 March 2026. By when must its first AGM be held? (b) At a general meeting of another company, 130 votes are cast against a resolution and 380 for it; 40 members abstain. Is it a valid special resolution?',
          'solution': [table(['Point', 'Rule', 'Answer'], [
              ['(a) First AGM', f'Within {R(agm1)} months from close of first financial year', 'By 31 December 2026 (no extension by the Registrar for the first AGM)'],
              ['Later AGMs', f'Within 6 months of year end; gap not over {R(gap)} months', '—'],
              ['(b) Special resolution', f'Votes for must be at least 3 × votes against = {R(sp)}', '380 < 390 — not passed as a special resolution (it passes as ordinary)']], title='AGM and special resolution'),
              note('Abstentions are ignored in counting votes for a special resolution.')],
          'checks': list(ck)}

    ck2 = Checks()
    pm = ck2.add('50', 'Maximum members a proxy may act for')
    q = ck2.add('15', 'Quorum for a public company with 3,000 members')
    i2 = {'id': 'i2', 'title': 'Requisition and quorum', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Members of Aarohan Ltd. (public; 3,000 members; paid-up capital ₹10 crore) holding ₹1.2 crore of paid-up capital requisition an EGM on 1 June. The Board does nothing. (a) Can they call the meeting themselves, and by when? (b) What is the quorum? (c) How many members can one proxy represent?',
          'solution': [legal('Sections 100, 103 and 105',
                             'Requisition by holders of 12% of paid-up capital; Board inactive; 3,000 members.',
                             'Members holding at least one-tenth of paid-up capital carrying voting rights may requisition an EGM. If the Board does not, within 21 days, call a meeting to be held within 45 days of the requisition, the requisitionists may call and hold it within three months of the requisition, recovering expenses from the company. Quorum for a public company with more than 1,000 but up to 5,000 members is 15 personally present. A proxy may act for up to 50 members holding not more than 10% of total share capital with voting rights.',
                             f'(a) Yes — after 22 June and by 1 September. (b) {R(q)} members. (c) Up to {R(pm)} members (and 10% of capital).')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Section 88: every company keeps registers of members, debenture holders and other security holders, indicating classes of shares; for securities held in demat form, the depository\'s records serve as the register.',
            'Section 89: a registered holder who does not hold the beneficial interest must declare it to the company (and the beneficial owner must also declare); the company files a return with the Registrar. Section 90: individuals holding significant beneficial ownership (directly or indirectly) must declare it, and the company keeps a register of significant beneficial owners; the Tribunal may restrict rights where information is withheld.',
            'Section 92: every company files an annual return (MGT-7, or MGT-7A for small and one person companies) within 60 days of the AGM, giving registered office, business, holdings, shareholders, directors and KMP, meetings and remuneration. Listed companies and companies above prescribed thresholds have it certified by a practising company secretary.',
            'Section 94: registers and annual returns are kept at the registered office, or at another place in India where more than one-tenth of members reside if a special resolution approves; members may inspect free and take extracts.'],
          'The registers say who owns the company; the annual return tells the Registrar every year.',
          'A nominee holding shares for a parent must declare the beneficial interest within the prescribed time.'),
        C('c2', T2, [
            'Section 96: every company other than a one person company holds an annual general meeting each year. The first AGM is held within nine months from the close of the first financial year; later AGMs within six months of the year end, and not more than fifteen months between two AGMs.',
            'The Registrar may, for special reasons, extend the time for any AGM other than the first by up to three months.',
            'An AGM is held during business hours (9 a.m. to 6 p.m.) on a day that is not a national holiday, at the registered office or another place in the city, town or village of the registered office (unlisted companies may hold it anywhere in India with consent of all members).',
            'Section 97: if an AGM is not held, the Tribunal may call or direct it on any member\'s application. Ordinary business at an AGM is consideration of financial statements and reports, declaration of dividend, appointment of directors in place of those retiring, and appointment and fixing remuneration of auditors; everything else is special business.'],
          'Once a year, within strict time limits, the members must meet.',
          'A company whose year ends on 31 March must hold its AGM by 30 September.'),
        C('c3', T3, [
            'Section 100: the Board may call an extraordinary general meeting whenever it thinks fit. Members holding at least one-tenth of paid-up capital with voting rights (or, for a company without share capital, one-tenth of voting power) may requisition one. If the Board does not, within 21 days, call it for a date within 45 days, the requisitionists may call and hold it within three months, and the company reimburses reasonable expenses.',
            'Section 98: the Tribunal may order a meeting where it is impracticable to call one in the ordinary way.',
            'Section 101: a general meeting needs at least 21 clear days\' notice in writing or electronically, stating place, date, day, hour and business, sent to every member, legal representative of deceased members, assignee of an insolvent member, auditors and directors. Shorter notice is allowed with written or electronic consent — for an AGM, of at least 95% of members entitled to vote; for other meetings, of a majority in number of members entitled to vote who hold at least 95% of the paid-up capital carrying voting rights.',
            'Section 102: a statement setting out material facts of special business, including the interest of directors, KMP and their relatives, is annexed to the notice.'],
          'Members can force a meeting, but only with enough backing and within set time limits.',
          'Notice posted on 1 May allows a meeting on 25 May only if 21 clear days are counted correctly (excluding dispatch and meeting days).'),
        C('c4', T4, [
            'Section 103: unless the articles require more, quorum for a public company is 5 members personally present if members are up to 1,000; 15 if over 1,000 and up to 5,000; and 30 if over 5,000. For a private company it is 2. If no quorum within half an hour, the meeting stands adjourned to the same day next week (or as the Board decides); at the adjourned meeting, those present form the quorum.',
            'Section 104: members elect a chairman by show of hands unless the articles provide otherwise.',
            'Section 105: a member entitled to vote may appoint a proxy, who need not be a member but cannot speak and votes only on a poll. A person may be proxy for not more than 50 members and holding not more than 10% of total voting capital. Proxy forms are deposited at least 48 hours before the meeting.',
            'Sections 107–110: voting is first by show of hands unless e-voting is used; a poll may be ordered by the chairman or demanded by members holding one-tenth of voting power or shares with paid-up value of at least ₹5 lakh. Prescribed companies must offer e-voting. Some items must be passed by postal ballot.'],
          'Quorum, proxies and polls make sure decisions reflect the members\' real voting strength.',
          'A member holding shares worth ₹6 lakh paid-up can demand a poll on his own.'),
        C('c5', T5, [
            'Section 114: an ordinary resolution needs more votes in favour than against; a special resolution needs votes in favour at least three times votes against, with the intention to propose it as special stated in the notice.',
            'Section 115: where the Act or articles require special notice (such as removal of a director or appointing an auditor other than the retiring one), members holding at least 1% of voting power or shares with paid-up value of ₹5 lakh give notice at least 14 days before the meeting; the company informs members at least 7 days before.',
            'Section 111: members with one-tenth voting power or 100 members holding ₹1 lakh paid-up capital can require circulation of their resolution or statement. Section 116: a resolution passed at an adjourned meeting is treated as passed on that later date.',
            'Section 117: special resolutions and other specified resolutions and agreements are filed with the Registrar within 30 days (MGT-14). Section 118: minutes of every meeting are prepared, signed and kept within 30 days; they are evidence of proceedings. Section 121: listed public companies file a report on each AGM within 30 days. Section 122: a one person company may pass resolutions by entering them in the minute book signed by the sole member.'],
          'Different decisions need different majorities and must be recorded and filed on time.',
          'A special resolution to change the registered office state must be filed in MGT-14 within 30 days.'),
    ]

    jobs = [{'id': 'j1', 'title': 'AGM compliance calendar', 'role': 'Secretarial associate',
             'situation': 'You must plan the AGM of an unlisted public company with 2,500 members and a special business item.',
             'steps': ['Fix the AGM date within six months of year end.', 'Send 21 clear days\' notice with explanatory statement.', 'Prepare proxy and quorum checks (15 members).', 'File MGT-14 and the annual return on time.'],
             'takeaway': 'Every stage of a meeting has its own deadline.'}]

    mcqs = [
        Q('m1', 'The first AGM of a company must be held within:', ['Nine months from the close of its first financial year', 'Six months of incorporation', 'Fifteen months of incorporation', 'Eighteen months of incorporation'], 0,
          'Section 96 requires the first AGM within nine months from the close of the first financial year; later AGMs within six months of year end. The Registrar cannot extend the time for the first AGM. In practice: diarise from incorporation.', 'c2', T2),
        Q('m2', 'The gap between two AGMs must not exceed:', ['Fifteen months', 'Twelve months', 'Eighteen months', 'Nine months'], 0,
          'Section 96 provides that not more than fifteen months shall elapse between the dates of two consecutive AGMs, apart from the six-month rule. In practice: check both limits.', 'c2', T2),
        Q('m3', 'Members can requisition an EGM if they hold at least:', ['One-tenth of paid-up capital with voting rights', 'One-fourth of paid-up capital', '5% of paid-up capital', 'Any amount, if 100 members join'], 0,
          'Section 100 lets members holding at least one-tenth of the paid-up share capital carrying voting rights requisition an EGM. In practice: deposit a signed requisition at the registered office.', 'c3', T3),
        Q('m4', 'Notice of a general meeting must normally be given at least:', ['21 clear days before the meeting', '14 days', '7 clear days', '30 days'], 0,
          'Section 101 requires at least 21 clear days\' notice in writing or electronic mode; shorter notice is possible with the required consent of members. In practice: exclude the day of service and the meeting day.', 'c3', T3, 'core', check=21),
        Q('m5', 'Quorum for a public company with 7,000 members (articles silent):', ['30 members personally present', '15 members', '5 members', '2 members'], 0,
          'Section 103 sets 30 members personally present where members exceed 5,000, 15 for 1,001–5,000, and 5 for up to 1,000. Private companies need 2. In practice: count only those present in person.', 'c4', T4, 'core', check=30),
        Q('m6', 'A proxy can act for at most:', ['50 members holding not more than 10% of voting capital', '100 members', '25 members', 'Unlimited members'], 0,
          'Section 105 and the rules limit a proxy to acting for 50 members, together holding not more than 10% of total share capital carrying voting rights. In practice: check proxy forms 48 hours before.', 'c4', T4),
        Q('m7', 'A special resolution requires votes in favour to be at least:', ['Three times the votes against', 'Twice the votes against', 'More than the votes against', 'Seventy-five per cent of all members'], 0,
          'Under section 114, a special resolution needs votes cast in favour of at least three times the votes cast against, with the intention stated in the notice. Abstentions are ignored. In practice: count valid votes only.', 'c5', T5),
        Q('m8', 'Special notice of a resolution must be given to the company at least:', ['14 days before the meeting', '21 days', '7 days', '30 days'], 0,
          'Section 115 requires the notice of intention to move such a resolution at least 14 days before the meeting; the company then informs members at least 7 days before. In practice: used to remove directors.', 'c5', T5, 'core', check=14),
        Q('m9', 'Special resolutions must be filed with the Registrar within:', ['30 days of passing', '60 days', '15 days', '7 days'], 0,
          'Section 117 requires a copy of every special resolution and other specified resolutions or agreements to be filed with the Registrar within 30 days in Form MGT-14. In practice: attach the explanatory statement.', 'c5', T5, 'core', check=30),
        Q('m10', 'The annual return under section 92 is filed within:', ['60 days from the date of the AGM', '30 days', '6 months of year end', '180 days'], 0,
          'Every company files its annual return within sixty days of the AGM (or the last date it should have been held), in MGT-7 or MGT-7A. In practice: certification is required for larger companies.', 'c1', T1, 'core', check=60),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'First AGM time limit', 2, 'concept', 'nine|9', 'december'),
           S('s2', 'Special resolution test', 2, 'computation', 'three|3 ×', nums=[sp])],
          ['Apply the limits precisely.'], ['Counting abstentions as against.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Requisition right and timeline', 2, 'application', '21 days|45 days', 'three months'),
           S('s2', 'Quorum', 1.5, 'application', '15'),
           S('s3', 'Proxy limit', 1.5, 'application', '50')],
          ['State each rule with numbers.'], ['Confusing 21 days with 45 days.'], ['Provision → facts → analysis → conclusion.'], checks=list(ck2)),
        W('q3', 4, 'Distinguish ordinary business and special business at an AGM.', [table(['Ordinary business', 'Special business'], [
              ['Consideration of financial statements and reports of the Board and auditors', 'Any business other than the four ordinary items'],
              ['Declaration of dividend', 'Needs an explanatory statement under section 102'],
              ['Appointment of directors retiring by rotation', 'Examples: alteration of articles, issue of shares, related party approvals'],
              ['Appointment of auditors and fixing their remuneration', 'Business at any EGM is always special']], title='AGM business')],
          [S('s1', 'Four ordinary items', 2, 'concept', 'dividend', 'auditor'),
           S('s2', 'Special business and statement', 2, 'concept', 'explanatory|102')],
          ['List the four items.'], ['Treating alteration of articles as ordinary.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'Within what time are AGMs held after the first?', 'Within six months after the financial year ends, with no more than fifteen months between two AGMs.',
          [P('p1', 'Six months', 5, 'six months|6 months'), P('p2', 'Fifteen months', 5, 'fifteen|15')], 'c2'),
        V('v2', 'What can requisitionists do if the Board ignores their requisition?', 'If the Board does not within 21 days call a meeting for a date within 45 days, they may themselves call and hold it within three months, recovering expenses.',
          [P('p1', '21 and 45 days', 5, '21|45'), P('p2', 'Within three months', 5, 'three months|3 months')], 'c3'),
        V('v3', 'What is the quorum for a private company?', 'Two members personally present, unless the articles require more.',
          [P('p1', 'Two', 6, 'two|2'), P('p2', 'Personally present', 4, 'personally|present')], 'c4'),
        V('v4', 'Who can demand a poll?', 'Members present in person or by proxy holding at least one-tenth of the total voting power, or shares with paid-up value of at least ₹5 lakh.',
          [P('p1', 'One-tenth voting power', 5, 'one-tenth|10'), P('p2', '₹5 lakh', 5, '5 lakh|five lakh')], 'c4'),
        V('v5', 'Which resolutions need special notice?', 'Those requiring it under the Act or articles, such as removal of a director or appointment of an auditor other than the retiring auditor; notice is given at least 14 days before the meeting.',
          [P('p1', 'Removal of director or auditor change', 5, 'remov|auditor'), P('p2', '14 days', 5, '14|fourteen')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Sumeru Ltd.', 'difficulty': 'moderate',
              'case': 'Sumeru Ltd. (public, 900 members) held its last AGM on 20 August 2025. Its year ends on 31 March 2026. At its 2026 AGM, 4 members are present in person and 20 by proxy; a proxy holder wants to speak against a resolution.',
              'mcqs': [
                  M('k1a', 'The 2026 AGM must be held by:', ['30 September 2026', '20 November 2026', '31 December 2026', '31 March 2027'], 0,
                    'Within six months of year end gives 30 September 2026; fifteen months from the last AGM gives 20 November 2026; the earlier date applies. In practice: check both limits.', 'moderate', topic=T2),
                  M('k1b', 'Is the quorum present?', ['No, 5 members must be personally present', 'Yes, proxies count', 'Yes, 4 is enough', 'Quorum is not needed for an AGM'], 0,
                    'For a public company with up to 1,000 members, quorum is 5 members personally present; proxies do not count. In practice: wait half an hour, then adjourn.', 'core', topic=T4),
                  M('k1c', 'May the proxy speak at the meeting?', ['No, a proxy cannot speak', 'Yes, if a member', 'Yes, always', 'Only on special business'], 0,
                    'Section 105 states that a proxy shall not have a right to speak at the meeting and may vote only on a poll. In practice: the member must attend to speak.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p2', 'int-p2-ch07', 1, 'Management & Administration',
                ['Explain registers, beneficial interest and annual return requirements.',
                 'Apply the rules for AGMs and EGMs, including requisitions and notices.',
                 'Apply quorum, proxy, voting and poll provisions.',
                 'Distinguish resolutions and state filing and minute requirements.'],
                {'difficulty': 'core', 'minutes': {'learn': 60, 'practice': 35}, 'prereq': ['int-p2-ch06-u01'],
                 'exam_tip': 'Numbers carry marks: 9/6/15 months (AGM), 21/45 days and 3 months (requisition), 21 clear days notice, 5/15/30/2 quorum, 50 members proxy, 14 days special notice, 30 days filing.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Registers of members; beneficial interest and SBO declarations; annual return within 60 days of AGM.',
                             'First AGM within 9 months of first year end; then 6 months / 15 months; ROC extension up to 3 months (not first).',
                             'EGM requisition by 1/10 of paid-up capital; Board 21 days / 45 days; requisitionists within 3 months.',
                             'Notice 21 clear days; shorter with 95% consent; explanatory statement for special business.',
                             'Quorum 5/15/30 (public), 2 (private); proxy ≤ 50 members, 10%; poll on 1/10 or ₹5 lakh.',
                             'Special resolution ≥ 3× against; special notice 14 days; MGT-14 in 30 days; minutes in 30 days.'],
                 'remember': ['A proxy cannot speak and votes only on a poll.'],
                 'traps': ['The Registrar cannot extend the first AGM.']},
                [('First AGM', '9 months'), ('Later AGMs', '6 months / 15 months gap'), ('Notice', '21 clear days'), ('Quorum (public)', '5 / 15 / 30'), ('Special resolution', '≥ 3 × against')],
                viva, cases)
