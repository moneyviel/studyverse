"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 9 Unit 2 — AS 14 Accounting for Amalgamations.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch09-u02'
T1 = 'Amalgamation and its two types'
T2 = 'Purchase consideration'
T3 = 'Pooling of interests method'
T4 = 'Purchase method, goodwill and capital reserve'
T5 = 'Statutory reserves and other matters'


def build():
    ck = Checks()
    sh = ck.add('60000*14', 'Value of shares issued (₹)')
    pc = ck.add('840000+100000', 'Purchase consideration (₹)')
    gw = ck.add('940000-900000', 'Goodwill (₹)')
    i1 = {'id': 'i1', 'title': 'Purchase method and goodwill', 'difficulty': 'core', 'minutes': 7,
          'q': 'Amrit Ltd. takes over Bindu Ltd. in an amalgamation in the nature of purchase. Bindu\'s assets at fair value less liabilities are ₹9,00,000. Amrit pays Bindu\'s shareholders 60,000 equity shares of ₹10 each valued at ₹14, plus ₹1,00,000 in cash. Bindu\'s debentures are taken over separately. Compute the purchase consideration and goodwill.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Shares issued', '60,000 × ₹14', inr(sh)],
              ['Cash', '', inr(100000)],
              ['Purchase consideration', '', inr(pc)],
              ['Net assets taken over (fair value)', '', inr(900000)],
              ['Goodwill', '9,40,000 − 9,00,000', inr(gw)]], title='AS 14 — purchase method'),
              note('Payments to debenture holders are not part of purchase consideration. Goodwill is amortised over its useful life, normally not more than five years unless a longer period is justified.')],
          'checks': list(ck)}

    ck2 = Checks()
    cons = ck2.add('55000*10', 'Consideration in equity shares at par (₹)')
    diff = ck2.add('550000-500000', 'Difference adjusted against reserves (₹)')
    res = ck2.add('300000-50000', 'Transferor\'s reserves carried after adjustment (₹)')
    i2 = {'id': 'i2', 'title': 'Pooling of interests', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Chetan Ltd. and Disha Ltd. merge, meeting all conditions of a merger. Disha has share capital ₹5,00,000 and general reserve ₹3,00,000. Chetan issues 55,000 equity shares of ₹10 at par to Disha\'s shareholders. Show the treatment of the difference.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Consideration (shares at par)', '55,000 × 10', inr(cons)],
              ['Disha\'s share capital', '', inr(500000)],
              ['Excess adjusted against reserves', '5,50,000 − 5,00,000', inr(diff)],
              ['Disha\'s general reserve carried forward', '3,00,000 − 50,000', inr(res)]], title='AS 14 — pooling of interests'),
              note('All assets, liabilities and reserves are taken at book values; no goodwill or capital reserve arises.')],
          'checks': list(ck2)}

    cond = table(['Merger condition', 'Meaning'], [
        ['All assets and liabilities', 'Every asset and liability of the transferor becomes the transferee\'s'],
        ['90% shareholders stay', 'Holders of at least 90% of the transferor\'s equity (by face value), other than the transferee itself, become its shareholders'],
        ['Equity only', 'Consideration to them is equity shares of the transferee, apart from cash for fractions'],
        ['Business continues', 'The transferor\'s business is intended to be carried on'],
        ['Book values kept', 'No change in book values except to unify accounting policies']], title='Amalgamation in the nature of merger')

    concepts = [
        C('c1', T1, [
            'An amalgamation is a merger under the Companies Act or other law in which one company joins another or two or more form a new one. The transferor company is absorbed; the transferee company receives it.',
            'An amalgamation in the nature of merger meets all five conditions in the table; otherwise it is an amalgamation in the nature of purchase.',
            'A merger is a genuine pooling of shareholders\' interests and businesses; a purchase is in effect one company acquiring another, after which the transferor\'s shareholders may not keep a proportionate share.'],
          'If the shareholders and business genuinely continue together, it is a merger; otherwise it is a purchase.',
          'If 15% of the transferor\'s shareholders take cash instead of shares, the deal is a purchase.',
          blocks=[cond]),
        C('c2', T2, [
            'Purchase consideration is the total of shares and other securities issued and cash or other assets paid by the transferee to the shareholders of the transferor.',
            'It is computed by the net payment method (sum of payments to shareholders) or the net assets method (assets taken over less liabilities, at agreed values). Payments to the transferor\'s debenture holders and other creditors are not part of it.',
            'Shares and securities issued are valued at fair value; non-cash assets given at their fair values. Adjustments for contingencies are included when probable and reliably estimable.'],
          'Consideration is what the transferor\'s shareholders get — nothing else.',
          'Debentures of the transferor replaced by the transferee\'s debentures are a liability taken over, not consideration.'),
        C('c3', T3, [
            'The pooling of interests method is used for an amalgamation in the nature of merger.',
            'Assets, liabilities and reserves (whether capital or revenue) of the transferor are recorded at their existing carrying amounts, after adjustments only to bring accounting policies into line.',
            'The identity of reserves is preserved. The difference between the share capital issued (plus other consideration) and the transferor\'s share capital is adjusted in reserves.'],
          'In a merger, both books are simply added together.',
          'A transferor\'s securities premium appears as securities premium in the merged company.'),
        C('c4', T4, [
            'The purchase method is used for an amalgamation in the nature of purchase.',
            'Assets and liabilities are recorded at existing carrying amounts or at fair values (allocating consideration to individual identifiable assets and liabilities). Reserves of the transferor other than statutory reserves are not carried over.',
            'Excess of consideration over net assets is goodwill, amortised systematically over its useful life — normally not exceeding five years unless a longer period can be justified. A shortfall is credited to capital reserve.'],
          'In a purchase, the buyer records what it got at value and the price difference as goodwill or capital reserve.',
          'Paying ₹50 lakh for net assets worth ₹42 lakh creates goodwill of ₹8 lakh.'),
        C('c5', T5, [
            'Under the purchase method, statutory reserves of the transferor (those required by law to be kept for a period, such as certain tax-related reserves) are preserved: they are recorded in the transferee\'s books with a corresponding debit to "Amalgamation Adjustment Reserve", shown as a separate line, and both are reversed when the requirement ends.',
            'If an amalgamation takes place after the year end but before the Board approves the statements, it is disclosed under AS 4 but not incorporated.',
            'Disclose: names and nature of business of the companies, effective date, method of accounting, particulars of the scheme; for mergers, shares issued and the difference treatment; for purchases, consideration and goodwill or capital reserve with the amortisation period.'],
          'Reserves the law requires to be kept survive even a purchase.',
          'A statutory reserve of ₹5 lakh shows up in the transferee balanced by an Amalgamation Adjustment Reserve.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Accounting for an amalgamation scheme', 'role': 'Accounts executive',
             'situation': 'Your company is absorbing a group company under an approved scheme; 92% of shareholders accept shares and the rest receive cash.',
             'steps': ['Test the five merger conditions.', 'Compute purchase consideration excluding debenture holders.', 'Record assets, liabilities and reserves by the right method.', 'Preserve statutory reserves.'],
             'takeaway': 'Classification decides the method and the treatment of reserves.'}]

    mcqs = [
        Q('m1', 'For an amalgamation in the nature of merger, at least what percentage (by face value) of the transferor\'s equity shareholders must become shareholders of the transferee?', ['90%', '75%', '51%', '100%'], 0,
          'One of the five merger conditions requires holders of at least 90% of the face value of the transferor\'s equity shares (excluding those held by the transferee) to become shareholders of the transferee. In practice: count acceptances.', 'c1', T1, 'core', check=90),
        Q('m2', 'Which method applies to an amalgamation in the nature of merger?', ['Pooling of interests', 'Purchase', 'Equity method', 'Proportionate consolidation'], 0,
          'Mergers are accounted for by pooling of interests, combining assets, liabilities and reserves at book values. Purchases use the purchase method. In practice: confirm all five conditions first.', 'c3', T3),
        Q('m3', 'Payment to debenture holders of the transferor company is:', ['Not part of purchase consideration', 'Part of purchase consideration', 'Treated as goodwill', 'Treated as capital reserve'], 0,
          'Purchase consideration includes only what is paid to the transferor\'s shareholders. Debentures discharged or exchanged are liabilities taken over, not consideration. In practice: exclude them in the net payment method.', 'c2', T2),
        Q('m4', 'Under the purchase method, excess of purchase consideration over net assets is:', ['Goodwill', 'Capital reserve', 'Debited to general reserve', 'Charged to profit and loss'], 0,
          'Paying more than the value of net assets acquired creates goodwill, which is amortised; paying less creates capital reserve. In practice: compare consideration with net assets at agreed values.', 'c4', T4),
        Q('m5', 'Goodwill arising on amalgamation is normally amortised over:', ['Not more than five years unless a longer period is justified', 'Twenty years', 'Ten years always', 'It is not amortised'], 0,
          'AS 14 requires systematic amortisation over useful life, usually five years at most, unless a longer period is clearly justified. In practice: document the justification.', 'c4', T4),
        Q('m6', 'Under pooling of interests, reserves of the transferor are:', ['Recorded with their identity preserved', 'Ignored', 'Converted to capital reserve', 'Transferred to goodwill'], 0,
          'In a merger all reserves of the transferor, capital or revenue, keep their identity in the transferee\'s books, after adjusting for any difference between consideration and share capital. In practice: merge reserve heads.', 'c3', T3),
        Q('m7', 'Net assets taken over ₹25 lakh; consideration ₹22 lakh (purchase method). The difference is:', ['Capital reserve of ₹3 lakh', 'Goodwill of ₹3 lakh', 'Debited to profit and loss', 'Ignored'], 0,
          'When the consideration is lower than the net assets acquired, the shortfall of ₹3 lakh is credited to capital reserve, not profit and loss. In practice: it is not distributable.', 'c4', T4, 'moderate'),
        Q('m8', 'Statutory reserves of the transferor under the purchase method are:', ['Recorded with a matching debit to Amalgamation Adjustment Reserve', 'Ignored', 'Transferred to profit and loss', 'Merged with goodwill'], 0,
          'To keep statutory reserves intact as the law requires, they are recorded in the transferee\'s books with a corresponding debit to Amalgamation Adjustment Reserve, reversed when no longer needed. In practice: show separately.', 'c5', T5),
        Q('m9', 'An amalgamation is in the nature of purchase if:', ['Any one of the five merger conditions is not met', 'All conditions are met', 'Shares are issued at a premium', 'The transferee is listed'], 0,
          'Failing any of the five conditions — all assets and liabilities, 90% shareholders, equity-only consideration, business continuity, book values — makes it a purchase. In practice: test each.', 'c1', T1),
        Q('m10', 'An amalgamation effective after the balance sheet date but before approval of accounts is:', ['Disclosed under AS 4, not incorporated', 'Incorporated in the accounts', 'Ignored', 'Treated as a prior period item'], 0,
          'Such an amalgamation is a non-adjusting event; it is disclosed but not incorporated in the financial statements of the year just ended. In practice: account for it next year.', 'c5', T5),
    ]

    questions = [
        W('q1', 4, i1['q'], i1['solution'],
          [S('s1', 'Consideration', 2, 'computation', 'consideration', nums=[pc]),
           S('s2', 'Goodwill', 2, 'computation', 'goodwill', nums=[gw])],
          ['Exclude debenture holders.'], ['Using book values of shares issued.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Consideration at par', 1.5, 'computation', 'consideration', nums=[cons]),
           S('s2', 'Difference against reserves', 1.5, 'computation', 'reserve', nums=[diff]),
           S('s3', 'No goodwill', 1, 'concept', 'goodwill')],
          ['Keep book values.'], ['Creating goodwill in a merger.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Name the conditions for an amalgamation in the nature of merger.', 'All assets and liabilities pass; 90% equity holders become shareholders; consideration only in equity shares except cash for fractions; business continues; book values kept except for uniform policies.',
          [P('p1', 'Assets and 90%', 5, 'assets', '90'), P('p2', 'Equity, continuity, book values', 5, 'equity|continu|book')], 'c1'),
        V('v2', 'What is purchase consideration?', 'The total of shares, securities, cash and other assets given by the transferee to the transferor\'s shareholders.',
          [P('p1', 'Shares and cash', 5, 'shares|cash'), P('p2', 'To shareholders', 5, 'shareholders')], 'c2'),
        V('v3', 'How does pooling of interests treat reserves?', 'All reserves of the transferor are recorded at book value with their identity preserved; the consideration difference is adjusted in reserves.',
          [P('p1', 'Identity preserved', 6, 'identity|preserv'), P('p2', 'Difference adjusted', 4, 'difference|adjust')], 'c3'),
        V('v4', 'How is goodwill on amalgamation treated?', 'It is amortised over its useful life, normally within five years unless a longer period is justified.',
          [P('p1', 'Amortised', 5, 'amortis'), P('p2', 'Five years', 5, 'five|5')], 'c4'),
        V('v5', 'What is the Amalgamation Adjustment Reserve?', 'A debit balance created to match statutory reserves of the transferor carried into the transferee under the purchase method, reversed when the statutory need ends.',
          [P('p1', 'Matches statutory reserves', 6, 'statutory'), P('p2', 'Purchase method', 4, 'purchase')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Ganga Ltd. and Yamuna Ltd.', 'difficulty': 'moderate',
              'case': 'Ganga Ltd. absorbs Yamuna Ltd. Yamuna has equity capital ₹40 lakh, general reserve ₹10 lakh, a statutory investment allowance reserve ₹4 lakh, and net assets at fair value ₹62 lakh. Ganga issues equity shares worth ₹50 lakh and pays ₹8 lakh cash to Yamuna\'s shareholders. 20% of Yamuna\'s shareholders opted for cash only.',
              'mcqs': [
                  M('k1a', 'The amalgamation is in the nature of:', ['Purchase, as fewer than 90% become shareholders and cash is paid', 'Merger', 'Neither', 'Demerger'], 0,
                    'With 20% of shareholders taking cash, the 90% and equity-only conditions fail, so the purchase method applies. In practice: record at fair values.', 'core', topic=T1),
                  M('k1b', 'Purchase consideration:', ['₹58 lakh', '₹50 lakh', '₹62 lakh', '₹54 lakh'], 0,
                    'Consideration is shares ₹50 lakh plus cash ₹8 lakh = ₹58 lakh, all paid to Yamuna\'s shareholders. In practice: compare with net assets next.', 'core', check=58, topic=T2),
                  M('k1c', 'Ganga records:', ['Capital reserve ₹4 lakh, and the statutory reserve with an Amalgamation Adjustment Reserve', 'Goodwill ₹4 lakh', 'General reserve ₹10 lakh', 'Goodwill ₹8 lakh'], 0,
                    'Net assets ₹62 lakh exceed consideration ₹58 lakh, giving capital reserve of ₹4 lakh; the general reserve is not carried over, but the statutory reserve is preserved against an Amalgamation Adjustment Reserve. In practice: disclose both.', 'hard', topic=T5),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch09', 2, 'Accounting Standard 14 Accounting for Amalgamations',
                ['Distinguish amalgamations in the nature of merger and purchase.',
                 'Compute purchase consideration.',
                 'Apply the pooling of interests and purchase methods.',
                 'Treat goodwill, capital reserve and statutory reserves, and give disclosures.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 35}, 'prereq': ['int-p1-ch09-u01'],
                 'exam_tip': 'Test the five merger conditions first; then compute consideration and choose the method.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Merger: all five conditions; otherwise purchase.', 'Consideration: to shareholders only; excludes debenture holders.',
                             'Pooling: book values, reserves preserved, difference to reserves.', 'Purchase: book or fair values; only statutory reserves carried.',
                             'Excess → goodwill (≤ 5 years); shortfall → capital reserve.', 'Amalgamation Adjustment Reserve for statutory reserves.'],
                 'remember': ['After-balance-sheet amalgamations are only disclosed.'],
                 'traps': ['General reserve of the transferor is not carried in a purchase.']},
                [('Merger test', '5 conditions incl. 90%'), ('Purchase excess', 'Goodwill'), ('Purchase shortfall', 'Capital reserve')],
                viva, cases)
