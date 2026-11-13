"""CA Intermediate · Paper 2 Corporate and Other Laws · Part II Chapter 3 The Foreign Exchange Management Act, 1999.
Scope follows the ICAI study material; provisions are explained in original words; examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p2-ii-ch03-u01'
T1 = 'Purpose, extent and key definitions'
T2 = 'Residential status under FEMA'
T3 = 'Regulation of foreign exchange dealings (ss. 3–4, 10)'
T4 = 'Current account transactions and the three Schedules'
T5 = 'Capital account transactions, exports and repatriation (ss. 6–9)'


def build():
    ck = Checks()
    d = ck.add('200', 'Days stayed in India in the preceding financial year')
    i1 = {'id': 'i1', 'title': 'Resident or not?', 'difficulty': 'core', 'minutes': 7,
          'q': 'Determine FEMA residential status for 2026-27: (a) Ravi stayed in India for 200 days in 2025-26 and continues to live here. (b) Neha stayed 250 days in India in 2025-26 but left on 10 April 2026 to take up a job in Dubai. (c) John, a UK citizen, came to India on 1 May 2026 to take up employment here, having stayed nil days in 2025-26.',
          'solution': [table(['Person', 'Test', 'Status'], [
              ['(a) Ravi', f'Stayed {R(d)} days (> 182) in the preceding year; no exclusion', 'Person resident in India'],
              ['(b) Neha', 'Over 182 days, but left India for employment abroad', 'Person resident outside India (from departure)'],
              ['(c) John', 'Under 182 days, but came to India for employment', 'Person resident in India (from arrival)']], title='Section 2(v)')],
          'checks': list(ck)}

    i2 = {'id': 'i2', 'title': 'Can this remittance be made?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Classify the following remittances by individuals: (a) remitting lottery winnings abroad; (b) remitting USD 40,000 for a family holiday in Europe; (c) a film star remitting USD 30,000 for a cultural tour abroad; (d) remitting USD 3,00,000 for a relative\'s medical treatment abroad, as estimated by a hospital.',
          'solution': [table(['Remittance', 'Schedule', 'Treatment'], [
              ['(a) Lottery winnings', 'Schedule I', 'Prohibited'],
              ['(b) Holiday USD 40,000', 'Schedule III (LRS)', 'Allowed within USD 2,50,000 a year without RBI approval'],
              ['(c) Cultural tour', 'Schedule II', 'Needs prior approval of the Government of India (Ministry concerned)'],
              ['(d) Medical treatment USD 3,00,000', 'Schedule III', 'Allowed beyond USD 2,50,000 on the basis of the hospital\'s estimate, without RBI approval']], title='Current account transactions')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'FEMA, 1999 replaced FERA to facilitate external trade and payments and promote orderly development of the foreign exchange market. It is civil in nature, unlike FERA, which was criminal.',
            'Its reach covers all of India, plus any overseas branch, office or agency that an Indian resident owns or controls, and also breaches committed abroad by anyone the Act covers.',
            'Key definitions: an "authorised person" is an authorised dealer, money changer, offshore banking unit or other person authorised under section 10 to deal in foreign exchange or foreign securities. A capital account transaction changes assets or liabilities (including contingent liabilities) outside India of residents, or in India of non-residents. A current account transaction is any other transaction, such as payments for trade, short-term banking, interest on loans, remittances for living expenses, travel, education and medical care.',
            '"Foreign exchange" means foreign currency, including deposits, credits and balances payable in foreign currency, drafts and travellers\' cheques drawn in Indian currency but payable in foreign currency, and similar instruments.'],
          'FEMA manages, not punishes, the flow of foreign exchange.',
          'Paying for an imported machine is a current account transaction; buying shares of a US company is a capital account transaction.'),
        C('c2', T2, [
            'Someone who spent over 182 days in India in the last financial year counts as resident — excluding a person who has gone out of or stays outside India for employment, business or vocation outside India, or for any other purpose indicating an intention to stay outside for an uncertain period.',
            'A person who comes to or stays in India for employment, business or vocation in India, or for any purpose indicating an intention to stay in India for an uncertain period, is resident even without 182 days.',
            'Also resident: every person or company set up or registered under Indian law; a set-up in India (office, branch, agency) that a non-resident owns or controls; and a set-up abroad (office, branch, agency) that an Indian resident owns or controls.',
            'A person resident outside India is one who is not resident in India.'],
          'Days count, but intention to stay or leave can override them.',
          'A student going abroad for a three-year degree becomes resident outside India because the stay is for an uncertain period.'),
        C('c3', T3, [
            'Section 3: except as permitted by the Act or with general or special permission of the RBI, no person may deal in or transfer foreign exchange or foreign securities with anyone other than an authorised person, make payments to or for the credit of a non-resident, receive payments from non-residents other than through an authorised person, or enter into financial transactions in India as consideration for acquiring assets outside India.',
            'Section 4: a person resident in India shall not acquire, hold, own, possess or transfer foreign exchange, foreign securities or immovable property outside India, except as provided in the Act.',
            'Section 10: the RBI may authorise persons to deal in foreign exchange; authorised persons must follow RBI directions and may refuse transactions that seem to contravene the Act.'],
          'Foreign exchange moves only through authorised channels.',
          'A resident cannot keep dollars received abroad indefinitely in a foreign account unless permitted.'),
        C('c4', T4, [
            'Section 5: any person may sell or draw foreign exchange from an authorised person for current account transactions, subject to reasonable restrictions imposed by the Central Government in consultation with the RBI.',
            'Schedule I (prohibited): remittance of lottery winnings; income from racing, riding or other hobbies; purchase of lottery tickets, banned magazines, football pools or sweepstakes; commission on exports towards equity investment in JVs or wholly owned subsidiaries abroad; dividend by companies under dividend balancing; commission on exports under the Rupee State Credit Route (except up to 10% for tea and tobacco); payments for "call back services"; and interest on Non-resident Special Rupee Scheme accounts.',
            'Schedule II (prior Government approval): for example cultural tours (Ministry of Human Resource Development), certain advertisements by State Governments and PSUs abroad, freight of vessels chartered by PSUs, hiring of transponders, and container detention charges above prescribed rates — each with the named Ministry.',
            'Schedule III: individuals may draw foreign exchange up to USD 2,50,000 a year under the Liberalised Remittance Scheme for purposes such as private visits (except Nepal and Bhutan), gifts, employment or emigration abroad, maintenance of relatives, business travel and studies; beyond the limit RBI approval is needed, except that medical treatment and studies abroad may exceed it based on estimates from the institution. Specified limits also apply for some business remittances (such as consultancy services).'],
          'Current account deals are free unless a Schedule says otherwise.',
          'A resident sending USD 50,000 a year to a child studying abroad acts within LRS.'),
        C('c5', T5, [
            'Section 6: capital account transactions are permitted only to the extent specified; the RBI (in consultation with the Central Government) regulates classes of permissible transactions and limits, while the Central Government regulates non-debt instruments. Residents may hold foreign currency, securities or property acquired while non-resident or inherited from a non-resident; non-residents may hold Indian property acquired while resident or inherited from a resident.',
            'Section 7: every exporter of goods furnishes a declaration to the RBI or prescribed authority with the full export value (or expected value) and other particulars, and exporters of services furnish prescribed particulars.',
            'Section 8: residents entitled to foreign exchange take reasonable steps to realise and repatriate it to India within the time and manner specified by the RBI.',
            'Section 9: sections 4 and 8 do not apply to specified items, such as foreign currency up to limits held by individuals, foreign exchange accounts of certain persons, and foreign exchange acquired by way of gift or inheritance.'],
          'Capital account deals need specific permission; exporters must bring their money home.',
          'An exporter who has not received payment within the permitted period must take steps to recover and repatriate it.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Remittance desk advice', 'role': 'Article assistant',
             'situation': 'An individual client wants to send money abroad for a holiday, a child\'s fees, a relative\'s surgery and a lottery purchase.',
             'steps': ['Classify each as current or capital account.', 'Check Schedules I, II and III.', 'Apply the USD 2,50,000 LRS limit and its exceptions.', 'Route through an authorised dealer with documents.'],
             'takeaway': 'Schedule-wise classification answers most remittance questions.'}]

    mcqs = [
        Q('m1', 'Under FEMA, a person is resident in India if he resided in India during the preceding financial year for more than:', ['182 days', '120 days', '90 days', '365 days'], 0,
          'Section 2(v) uses more than 182 days in the preceding financial year, subject to exclusions for those going abroad for employment, business or uncertain stays, and inclusions for those coming to India for such purposes. In practice: also consider intention.', 'c2', T2, 'core', check=182),
        Q('m2', 'A resident who leaves India to take up employment abroad becomes:', ['A person resident outside India', 'Still resident for that year', 'Resident for 182 more days', 'Neither'], 0,
          'The definition excludes from residents a person who goes out of India for employment outside India, so his status changes on departure. In practice: update bank accounts to NRO/NRE.', 'c2', T2),
        Q('m3', 'Which is a capital account transaction?', ['Purchase of immovable property abroad by a resident', 'Payment for imported goods', 'Remittance for a holiday', 'Interest paid on a loan'], 0,
          'A capital account transaction alters assets or liabilities outside India of residents (or in India of non-residents); buying foreign property does so. The others are current account transactions. In practice: check RBI regulations.', 'c1', T1),
        Q('m4', 'Remittance of lottery winnings abroad is:', ['Prohibited under Schedule I', 'Allowed under LRS', 'Allowed with Government approval', 'Allowed with RBI approval'], 0,
          'Schedule I of the Current Account Transactions Rules prohibits drawal of foreign exchange for remittance of lottery winnings, among other items. No approval can permit it. In practice: refuse such requests.', 'c4', T4),
        Q('m5', 'Under the Liberalised Remittance Scheme, an individual may remit up to:', ['USD 2,50,000 per financial year', 'USD 1,00,000', 'USD 5,00,000', 'USD 25,000'], 0,
          'Schedule III allows individuals foreign exchange up to USD 2,50,000 a year for listed purposes; beyond it RBI approval is needed, except medical treatment and studies on estimates. In practice: track total remittances.', 'c4', T4),
        Q('m6', 'Remittance for a cultural tour abroad requires prior approval of:', ['The Government of India (Ministry concerned)', 'The RBI', 'No one', 'SEBI'], 0,
          'Cultural tours appear in Schedule II, needing prior approval of the Ministry of Human Resource Development (Department of Education and Culture). In practice: obtain approval before drawing foreign exchange.', 'c4', T4),
        Q('m7', 'Foreign exchange may be dealt in only through:', ['An authorised person', 'Any bank', 'Any money lender', 'Any company'], 0,
          'Section 3 restricts dealing in foreign exchange to authorised persons — authorised dealers, money changers, offshore banking units and others authorised by the RBI under section 10. In practice: check RBI authorisation.', 'c3', T3),
        Q('m8', 'An exporter of goods must furnish a declaration of the export value to:', ['The RBI or prescribed authority', 'SEBI', 'The Registrar of Companies', 'The Income-tax Department only'], 0,
          'Section 7 requires exporters of goods to furnish a declaration with the full export value or expected value to the RBI or such authority as specified. In practice: realise proceeds within the time allowed.', 'c5', T5),
        Q('m9', 'FEMA applies to:', ['All of India and branches abroad owned or controlled by residents', 'Only foreign nationals', 'Only exporters', 'Only Indian companies'], 0,
          'FEMA covers all of India and also reaches overseas branches, offices or agencies that an Indian resident owns or controls, plus breaches abroad by covered persons. In practice: overseas branches must comply.', 'c1', T1),
        Q('m10', 'For medical treatment abroad beyond USD 2,50,000, an individual:', ['May remit based on the hospital\'s estimate without RBI approval', 'Must seek RBI approval', 'Cannot remit', 'Needs Government approval'], 0,
          'Schedule III allows remittance above the LRS limit for medical treatment abroad on the basis of an estimate from the doctor or hospital, without separate RBI approval. In practice: keep the estimate on file.', 'c4', T4),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', '182-day test', 1.5, 'application', '182'),
           S('s2', 'Exclusion for going abroad', 1.5, 'application', 'employment'),
           S('s3', 'Inclusion for coming to India', 1, 'application', 'came|coming|arrival')],
          ['Apply days, then intention.'], ['Ignoring the purpose of stay.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Schedule I', 1, 'concept', 'prohibited'),
           S('s2', 'LRS limit', 1.5, 'concept', '2,50,000'),
           S('s3', 'Schedule II', 1, 'concept', 'government'),
           S('s4', 'Medical exception', 1.5, 'concept', 'medical|estimate')],
          ['Name the Schedule for each.'], ['Requiring RBI approval for medical treatment.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What is a current account transaction?', 'A transaction other than a capital account transaction, such as payments for foreign trade, short-term banking, interest on loans, family maintenance, travel, education and medical expenses.',
          [P('p1', 'Other than capital account', 5, 'other than|capital'), P('p2', 'Examples', 5, 'trade|travel|education|medical|interest')], 'c1'),
        V('v2', 'Who is a person resident in India under FEMA?', 'Someone who spent over 182 days in India in the last financial year, excluding those who leave for employment, business or an uncertain stay abroad, and including those who come for such purposes.',
          [P('p1', '182 days', 5, '182'), P('p2', 'Purpose-based exclusions', 5, 'employment|business|uncertain')], 'c2'),
        V('v3', 'What are the three Schedules on current account transactions?', 'Schedule I lists prohibited transactions, Schedule II those needing Government of India approval, and Schedule III those needing RBI approval beyond specified limits.',
          [P('p1', 'Prohibited and Government', 5, 'prohibit', 'government'), P('p2', 'RBI limits', 5, 'rbi')], 'c4'),
        V('v4', 'What is an authorised person?', 'An authorised dealer, money changer, offshore banking unit or other person authorised by the RBI under section 10 to deal in foreign exchange or foreign securities.',
          [P('p1', 'Dealer or money changer', 5, 'dealer|money changer'), P('p2', 'Authorised by RBI', 5, 'rbi|section 10')], 'c3'),
        V('v5', 'What duty does section 8 impose?', 'A resident to whom foreign exchange is due must take reasonable steps to realise and repatriate it to India within the specified time.',
          [P('p1', 'Realise', 5, 'realis'), P('p2', 'Repatriate', 5, 'repatriat')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'The Kapoor family', 'difficulty': 'moderate',
              'case': 'Mr. Kapoor (resident) wants to send USD 1,50,000 for his daughter\'s studies in Canada, USD 1,20,000 to buy an apartment in Dubai, and USD 5,000 to buy tickets for a foreign lottery.',
              'mcqs': [
                  M('k1a', 'The remittance for studies is:', ['Allowed under Schedule III (and beyond LRS on the institution\'s estimate)', 'Prohibited', 'Needs Government approval', 'Needs SEBI approval'], 0,
                    'Studies abroad are covered by Schedule III; amounts beyond the LRS limit may be remitted on the basis of the institution\'s estimate. USD 1,50,000 is within the limit anyway. In practice: keep admission and fee documents.', 'core', topic=T4),
                  M('k1b', 'Buying the Dubai apartment is:', ['A capital account transaction, permitted within LRS limits', 'A current account transaction', 'Prohibited under Schedule I', 'Allowed only with Government approval'], 0,
                    'Acquiring property abroad changes assets outside India, so it is a capital account transaction; individuals may do it within the LRS overall limit. In practice: total LRS remittances must stay within USD 2,50,000 a year.', 'moderate', topic=T5),
                  M('k1c', 'The lottery ticket purchase remittance is:', ['Prohibited', 'Allowed under LRS', 'Allowed with RBI approval', 'Allowed with Government approval'], 0,
                    'Remittance for purchase of lottery tickets is listed in Schedule I as prohibited, so no route allows it. In practice: authorised dealers must refuse it.', 'core', topic=T4),
              ]}]

    return unit(UID, 'p2', 'int-p2-ii-ch03', 1, 'The Foreign Exchange Management Act, 1999',
                ['Explain the purpose, extent and key definitions of FEMA.',
                 'Determine residential status under FEMA.',
                 'Explain restrictions on dealing in and holding foreign exchange.',
                 'Classify current and capital account transactions and apply the Schedules.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 20}, 'prereq': ['int-p2-ii-ch02-u01'],
                 'exam_tip': 'For remittance problems, classify the transaction, name the Schedule, and state the approving authority or limit.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['FEMA: civil law managing foreign exchange; extends to residents\' branches abroad.', 'Resident: > 182 days in preceding year, subject to purpose-based exclusions/inclusions.',
                             'Deal only through authorised persons (s. 3); residents\' holding abroad restricted (s. 4).', 'Current account free subject to Schedules I (prohibited), II (Government), III (RBI beyond limits).',
                             'LRS USD 2,50,000; medical and studies may exceed on estimates.', 'Capital account regulated; exporters declare and repatriate (ss. 7–8).'],
                 'remember': ['Capital account changes assets or liabilities across borders.'],
                 'traps': ['Lottery remittances are banned outright.']},
                [('Resident', '> 182 days (with purpose test)'), ('LRS', 'USD 2,50,000 / year'), ('Schedule I', 'Prohibited'), ('Schedule II', 'GoI approval')],
                viva, cases)
