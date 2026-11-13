"""CA Intermediate · Paper 2 Corporate and Other Laws · Part II Chapter 1 The General Clauses Act, 1897.
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ii-ch01-u01'
T1 = 'Purpose of the Act and important definitions (s. 3)'
T2 = 'Commencement, repeal and revival (ss. 5–8)'
T3 = 'Time, distance and number (ss. 9–13)'
T4 = 'Powers and functionaries (ss. 14–24)'
T5 = 'Miscellaneous: offences, service by post and citation (ss. 25–30)'


def build():
    ck = Checks()
    d = ck.add('30', 'Days to count: excluding 1 October and including 31 October')
    i1 = {'id': 'i1', 'title': 'Counting days under section 9 and 10', 'difficulty': 'core', 'minutes': 6,
          'q': 'A notice dated 1 October 2026 gives a party "30 days from 1 October" to file a reply with a government office. The 31st of October is a Saturday and the office is closed on Saturdays and Sundays. By when must the reply be filed?',
          'solution': [table(['Step', 'Rule', 'Result'], [
              ['Exclude the first day', 'Section 9: "from" excludes the first day', 'Counting starts on 2 October'],
              ['Include the last day', '"to" or the last of a period is included', f'{R(d)} days end on 31 October'],
              ['Office closed', 'Section 10: if the office is closed on the last day, act may be done on the next day it is open', 'File on Monday, 2 November 2026']], title='Computation of time')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Effect of repeal', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'An Act imposing a cess was repealed on 1 April 2026 without any saving clause. An inquiry into evasion of the cess for 2024-25 had started in February 2026. The taxpayer argues that the inquiry must stop. Advise.',
          'solution': [legal('Section 6, General Clauses Act, 1897',
                             'Repeal of an Act without a saving clause; inquiry into liabilities incurred before repeal.',
                             'Unless a different intention appears, repeal of a Central Act does not affect the previous operation of the repealed law or anything done under it, any right, privilege, obligation or liability already acquired or incurred, any penalty or punishment incurred, or any investigation, legal proceeding or remedy in respect of them; these may be continued or enforced as if the law had not been repealed.',
                             'The inquiry may continue, and the cess liability for 2024-25 can be enforced.')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'The General Clauses Act consolidates definitions and rules of construction that apply to all Central Acts and Regulations unless the context requires otherwise, avoiding repetition in each statute.',
            'Key definitions in section 3: "affidavit" includes affirmation and declaration by those allowed to affirm; "immovable property" includes land, benefits arising out of land and things attached to the earth; "movable property" means property of every description except immovable property; "person" includes any company, association or body of individuals, incorporated or not; "good faith" means a thing done honestly, whether negligently or not.',
            'Also: "month" and "year" are reckoned by the British calendar; "financial year" runs from 1 April; "document" includes any matter written or expressed on any substance by letters, figures or marks; "sign" includes a mark for a person unable to write; "writing" includes printing, lithography and photography; "will" includes a codicil; "oath" includes affirmation; "offence" means any act or omission made punishable by law.'],
          'One Act gives common meanings to words used across all Central laws.',
          'A company can be a "person" who commits an offence under a Central Act.'),
        C('c2', T2, [
            'Section 5: a Central Act takes effect on the date the President (Governor-General for older Acts) gives assent, unless otherwise provided; it takes effect from the immediate start of that day.',
            'Section 6: repeal does not revive anything not in force at the time of repeal, affect the previous operation of the repealed law, or affect rights, liabilities, penalties, investigations, legal proceedings or remedies already accrued — these continue as if the law were not repealed, unless a different intention appears.',
            'Section 6A: repeal of an amending Act does not undo the textual amendments it made in the principal Act.',
            'Section 7: a repealed enactment is revived only if expressly stated. Section 8: where an Act is repealed and re-enacted, references in other laws to the repealed provisions are read as references to the re-enacted ones.'],
          'Repeal looks forward; it does not wipe out what happened before.',
          'A penalty incurred under a repealed tax law can still be recovered.'),
        C('c3', T3, [
            'Section 9: in any Central Act, "from" excludes the first day of a period, and "to" includes the last day.',
            'Section 10: if a court or office is closed on the last day for doing an act, the act is in time if done on the next day it is open. This does not apply to acts under the Limitation Act.',
            'Section 11: distances are taken as the direct straight-line span over level ground (as the crow flies).',
            'Section 12: duties are charged proportionately on any greater or less quantity. Section 13: words importing the masculine gender include females, and singular includes plural and vice versa, unless the context indicates otherwise.'],
          'Exclude the first day, include the last, and roll over to the next open day.',
          'A rule against selling liquor within 100 metres of a school is measured in a straight line.'),
        C('c4', T4, [
            'Section 14: powers conferred by a Central Act can be used again and again whenever the need arises.',
            'Sections 15 and 16: a power to appoint includes the power to appoint ex-officio, and to suspend or dismiss the person appointed.',
            'Section 17: references to a functionary include whoever holds that office for the time being; section 18: references to a person include successors; section 19: official chiefs include their subordinates.',
            'Section 21: whoever can issue a notification, order, rule or bye-law can also add to, amend, vary or rescind them in the same manner. Section 22: rules may be made between passing and commencement of an Act, taking effect on commencement. Section 23: rules made after previous publication follow a prescribed procedure. Section 24: orders and rules under a repealed and re-enacted law continue so far as consistent, until superseded.'],
          'Powers given by a statute come with the incidental powers needed to use them sensibly.',
          'An authority empowered to appoint an inspector can also suspend him.'),
        C('c5', T5, [
            'Section 25: provisions of the Indian Penal Code (now the corresponding criminal law) on recovery of fines apply to fines imposed under Central Acts.',
            'Section 26: where an act or omission is an offence under two or more enactments, the offender may be prosecuted and punished under any of them, but not punished twice for the same offence.',
            'Section 27: where an Act requires a document to be served by post, service is deemed made by properly addressing, pre-paying and posting it by registered post, and is treated as served at the time a letter would normally arrive by post, unless shown otherwise.',
            'Section 28: an enactment may be cited by its short title or by its year and number. Section 29: earlier laws and rules are saved unless the Act provides otherwise. Section 30: the Act applies to Ordinances as it applies to Acts.'],
          'Same offence, two laws — prosecute under either, punish only once.',
          'A notice sent by registered post with a correct address is presumed served even if the addressee avoids it.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Deadline and service check', 'role': 'Article assistant',
             'situation': 'A client received a notice by registered post and must reply within 30 days "from" the notice date.',
             'steps': ['Apply section 9 to count days.', 'Check if the last day falls on a holiday (section 10).', 'Confirm deemed service under section 27.', 'Advise the filing date.'],
             'takeaway': 'Counting rules and deemed service decide whether a reply is in time.'}]

    mcqs = [
        Q('m1', 'Under section 9, the word "from" in a time period:', ['Excludes the first day', 'Includes the first day', 'Includes both first and last days', 'Excludes the last day'], 0,
          'Section 9 excludes the first day of a period described with "from" and includes the last day of a period described with "to". This avoids disputes about fractional days. In practice: count carefully.', 'c3', T3),
        Q('m2', 'A Central Act without a commencement provision comes into force:', ['On the day it receives the President\'s assent', 'On publication in the Gazette', 'Thirty days after assent', 'From the next financial year'], 0,
          'Section 5 provides that, unless otherwise stated, a Central Act comes into operation on the day it receives assent, from the beginning of that day. In practice: check the Act for a different date.', 'c2', T2),
        Q('m3', 'Under the General Clauses Act, "person" includes:', ['A company or association, incorporated or not', 'Only natural persons', 'Only registered companies', 'Only citizens'], 0,
          'Section 3(42) defines person to include any company, association or body of individuals, whether incorporated or not. In practice: companies can be prosecuted as persons.', 'c1', T1),
        Q('m4', 'A thing is done in "good faith" when it is done:', ['Honestly, whether negligently or not', 'Carefully and honestly', 'With due care only', 'Without any negligence'], 0,
          'Section 3(22) treats an act as done in good faith if done honestly, even if negligently. Honesty, not care, is the test. In practice: negligence does not destroy good faith.', 'c1', T1),
        Q('m5', 'Repeal of a Central Act without a saving clause:', ['Does not affect liabilities already incurred', 'Wipes out all past liabilities', 'Revives the earlier law', 'Cancels pending proceedings'], 0,
          'Section 6 preserves previous operation, rights, liabilities, penalties and proceedings, unless a different intention appears. Repeal does not revive anything not in force. In practice: pending cases continue.', 'c2', T2),
        Q('m6', 'Distances under a Central Act are measured:', ['As a straight line over level ground', 'By road', 'By the shortest route of travel', 'As decided by the authority'], 0,
          'Section 11 measures distance as the direct straight-line span over level ground unless a different intention appears. In practice: use map distance, not road distance.', 'c3', T3),
        Q('m7', 'A power to make rules under a Central Act includes the power to:', ['Add to, amend, vary or rescind them', 'Make them with retrospective effect always', 'Delegate them to anyone', 'Ignore them'], 0,
          'Under section 21, an authority able to issue notifications, orders, rules or bye-laws may also add to, amend, vary or rescind them in the same manner and subject to the same conditions. In practice: follow the same procedure.', 'c4', T4),
        Q('m8', 'When an act is an offence under two enactments, the offender may be:', ['Prosecuted under either, but not punished twice', 'Punished under both', 'Prosecuted only under the older law', 'Acquitted'], 0,
          'Section 26 permits prosecution and punishment under either enactment but bars double punishment for the same offence. In practice: choose the more suitable law.', 'c5', T5),
        Q('m9', 'Service by registered post is deemed effected:', ['When a normally posted letter would reach the addressee', 'When the addressee signs', 'When posted', 'Only on actual receipt'], 0,
          'Section 27 deems service effected by properly addressing, pre-paying and registering the letter, at the time a letter would normally arrive, unless the contrary is proved. In practice: keep postal proof.', 'c5', T5),
        Q('m10', 'The power to appoint includes the power to:', ['Suspend or dismiss the person appointed', 'Fix any salary', 'Delegate the appointment', 'Appoint for life'], 0,
          'Section 16 states that a power to make an appointment includes the power to suspend or dismiss the appointee, unless a different intention appears. In practice: follow natural justice.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Section 9 counting', 2, 'application', 'exclude|31 october'),
           S('s2', 'Section 10 next open day', 2, 'application', 'next|2 november')],
          ['Apply both sections in order.'], ['Counting the first day.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Section 6 rule', 2, 'concept', 'repeal|previous operation'),
           S('s2', 'Application and conclusion', 2, 'conclusion', 'continue|enforced')],
          ['State the saving effect of repeal.'], ['Assuming repeal ends all proceedings.'], ['Provision → facts → analysis → conclusion.']),
    ]

    viva = [
        V('v1', 'What does section 6 provide on repeal?', 'Repeal leaves the earlier working of the law intact: rights, liabilities, penalties, investigations and proceedings already accrued continue; nothing dead is revived, unless a different intention appears.',
          [P('p1', 'Earlier working intact', 5, 'earlier|intact'), P('p2', 'Liabilities and proceedings continue', 5, 'liabilit|proceeding')], 'c2'),
        V('v2', 'How is time computed under section 9?', 'The first day is excluded where "from" is used and the last day is included where "to" is used.',
          [P('p1', 'Exclude first', 5, 'first'), P('p2', 'Include last', 5, 'last')], 'c3'),
        V('v3', 'What is "movable property"?', 'Property of every description except immovable property.',
          [P('p1', 'Every description', 5, 'every'), P('p2', 'Except immovable', 5, 'except|immovable')], 'c1'),
        V('v4', 'What does section 21 empower?', 'The authority that can issue notifications, orders, rules or bye-laws can also add to, amend, vary or rescind them in the same manner.',
          [P('p1', 'Amend or rescind', 6, 'amend|rescind'), P('p2', 'Same manner', 4, 'same manner|same')], 'c4'),
        V('v5', 'How is a repealed enactment revived?', 'Only where the later law expressly says it is revived.',
          [P('p1', 'Express provision', 6, 'express'), P('p2', 'Later law', 4, 'later law|revived')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Notice to Malhotra Traders', 'difficulty': 'moderate',
              'case': 'A tax officer sent a notice by registered post to Malhotra Traders\' correct address. The firm refused to accept delivery. The notice required a reply "within 15 days from" 5 March. The last day was a public holiday.',
              'mcqs': [
                  M('k1a', 'Is service valid despite the refusal?', ['Yes, service is deemed effected under section 27', 'No, actual receipt is required', 'Only if served again by hand', 'Only if published in a newspaper'], 0,
                    'Proper addressing, pre-payment and registered posting create a presumption of service at the time of normal delivery, unless the contrary is proved; refusal does not defeat it. In practice: keep the postal record.', 'core', topic=T5),
                  M('k1b', 'Counting "15 days from 5 March":', ['Starts on 6 March and ends on 20 March', 'Starts on 5 March and ends on 19 March', 'Ends on 21 March', 'Ends on 4 April'], 0,
                    'Section 9 excludes the first day (5 March), so the 15 days run from 6 March to 20 March inclusive. In practice: then check holidays.', 'moderate', topic=T3),
                  M('k1c', 'As the last day is a public holiday, the reply is in time if filed:', ['On the next day the office is open', 'Only on the holiday itself', 'Within 7 more days', 'Never — the time has lapsed'], 0,
                    'Section 10 allows an act due on a day when the office is closed to be done on the next day it is open, except under the Limitation Act. In practice: file early anyway.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p2', 'int-p2-ii-ch01', 1, 'The General Clauses Act, 1897',
                ['Explain the purpose of the General Clauses Act and its key definitions.',
                 'Apply rules on commencement, repeal and revival of enactments.',
                 'Apply rules on time, distance, gender and number.',
                 'Explain powers, functionaries, offences under two laws and service by post.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['int-p2-ch12-u01'],
                 'exam_tip': 'Quote the section number with each rule: 3 (definitions), 5, 6, 9, 10, 11, 13, 16, 21, 26, 27.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Definitions apply to all Central Acts unless context differs.', 'Act in force on assent unless stated otherwise.',
                             'Repeal preserves past operation, rights, liabilities and proceedings; revival needs express words.', '"From" excludes first day; "to" includes last; next open day if office closed.',
                             'Distance in a straight line; singular includes plural.', 'Power to appoint includes suspend/dismiss; power to make rules includes amend/rescind; no double punishment; deemed service by post.'],
                 'remember': ['Good faith = honesty, even if negligent.'],
                 'traps': ['Section 10 does not apply to the Limitation Act.']},
                [('Commencement', 'Date of assent'), ('Time', 'Exclude first, include last'), ('Distance', 'Straight line'), ('Service', 'Registered post deemed')],
                viva, cases)
