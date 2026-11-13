"""CA Intermediate · Paper 3A Income-tax Law · Chapter 5 Set off, or Carry Forward and Set off of Losses (Income-tax Act, 2025; tax year 2026-27).
Scope follows the ICAI study material; section numbers are taken from it; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p3-a-ch05-u01'
T1 = 'Set-off within the same head (s. 108)'
T2 = 'Set-off across heads (s. 109)'
T3 = 'House property and capital losses carried forward (ss. 110-111)'
T4 = 'Business losses carried forward (s. 112)'
T5 = 'Speculation, specified business and race horses (ss. 113-115)'
T6 = 'Order of set-off and unabsorbed depreciation'
T7 = 'Return of loss (s. 121) and the default regime'


def build():
    # i1 — inter-source and inter-head set-off under both regimes
    ck = Checks()
    biz = ck.add('90000-130000', 'Net business result after inter-source set-off')
    sal = ck.add('650000-200000', 'Salary after house property loss (capped at ₹2,00,000)')
    hpcf = ck.add('260000-200000', 'House property loss carried forward')
    bcf = ck.add('40000-30000', 'Business loss carried forward after set-off against FD interest')
    gti_o = ck.add('450000+0', 'GTI, optional regime')
    gti_d = ck.add('650000+0', 'GTI, default regime')
    i1 = {'id': 'i1', 'title': 'Two businesses, one let-out flat', 'difficulty': 'core', 'minutes': 8,
          'q': 'Ms. Rekha has for tax year 2026-27: salary (computed) ₹6,50,000; loss from a let-out flat ₹2,60,000; profit from a bakery ₹90,000; loss from a catering business ₹1,30,000; FD interest ₹30,000. Compute her gross total income and the losses carried forward (a) if she opts out of the default regime and (b) under the default regime.',
          'solution': [table(['Step', '(a) Optional ₹', '(b) Default ₹'], [
              ['Business: bakery profit less catering loss (same head)', inr(biz), inr(biz)],
              ['Salary', inr(650000), inr(650000)],
              ['Less: house property loss against salary', '(2,00,000)', 'Not allowed'],
              ['Salary after set-off', inr(sal), inr(650000)],
              ['FD interest less business loss (not against salary)', '30,000 − 30,000 = Nil', '30,000 − 30,000 = Nil'],
              ['Gross total income', inr(gti_o), inr(gti_d)],
              ['House property loss carried forward', inr(hpcf), 'Lapses'],
              ['Business loss carried forward', inr(bcf), inr(bcf)]], title='Sections 108, 109 and 110'),
              note('Business loss is never set off against salary, so ₹10,000 waits for future business income in both regimes.')],
          'checks': list(ck)}

    # i2 — capital losses
    ck2 = Checks()
    st = ck2.add('70000-40000', 'STCG after brought forward short-term loss')
    lt = ck2.add('110000-110000', 'LTCG after brought forward long-term loss (set off to the extent of gain)')
    ltcf = ck2.add('150000-110000', 'Long-term loss still carried forward')
    i2 = {'id': 'i2', 'title': 'Old capital losses meet new gains', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'For tax year 2026-27 Mr. Jacob has short-term capital gain ₹70,000 and long-term capital gain on land ₹1,10,000. Brought forward: long-term capital loss of tax year 2023-24 ₹1,50,000 and short-term capital loss of tax year 2025-26 ₹40,000. Both losses were declared in returns filed on time. Compute the taxable capital gains and the loss carried forward.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Short-term gain', '70,000 − b/f short-term loss 40,000', inr(st)],
              ['Long-term gain', '1,10,000 − b/f long-term loss used 1,10,000', inr(lt)],
              ['Taxable capital gains', '', inr(st)],
              ['Long-term loss carried forward', '1,50,000 − 1,10,000', inr(ltcf)]], title='Section 111'),
              p('The remaining long-term loss cannot touch the short-term gain. It may be carried forward until tax year 2031-32, that is 8 tax years after 2023-24, but only against long-term gains.')],
          'checks': list(ck2)}

    # i3 — order of set-off
    ck3 = Checks()
    b1 = ck3.add('300000-80000', 'Business income after current depreciation')
    b2 = ck3.add('220000-150000', 'After brought forward business loss')
    ud = ck3.add('120000-70000', 'Unabsorbed depreciation left after business income')
    hp = ck3.add('50000-50000', 'House property after unabsorbed depreciation')
    g3 = ck3.add('400000+0+0', 'Gross total income (salary only)')
    i3 = {'id': 'i3', 'title': 'Which deduction goes first?', 'difficulty': 'hard', 'minutes': 8,
          'q': 'Mr. Nair (optional regime) has for tax year 2026-27: business profit before depreciation ₹3,00,000; current depreciation ₹80,000; brought forward business loss of tax year 2022-23 ₹1,50,000; unabsorbed depreciation ₹1,20,000; income from house property ₹50,000; salary ₹4,00,000. Compute his gross total income.',
          'solution': [table(['Order', 'Item', '₹'], [
              ['1', 'Business profit less current depreciation', inr(b1)],
              ['2', 'Less brought forward business loss (s. 112)', inr(b2)],
              ['3', 'Less unabsorbed depreciation ₹70,000', 'Nil'],
              ['', 'Unabsorbed depreciation still left', inr(ud)],
              ['4', 'House property ₹50,000 less unabsorbed depreciation ₹50,000', inr(hp)],
              ['5', 'Salary (unabsorbed depreciation cannot be set off)', inr(400000)],
              ['', 'Gross total income', inr(g3)]], title='Order of set-off'),
              p('Brought forward business loss has a time limit, so it is absorbed before unabsorbed depreciation, which has none. Depreciation then behaves like current depreciation and may reduce any head except salary.')],
          'checks': list(ck3)}

    cf = table(['Loss', 'Set off later against', 'Years'], [
        ['House property (optional regime only)', 'House property income', '8'],
        ['Short-term capital loss', 'Any capital gain', '8'],
        ['Long-term capital loss', 'Long-term capital gain only', '8'],
        ['Business loss (non-speculative)', 'Business or profession income', '8'],
        ['Speculation loss', 'Speculation income', '4'],
        ['Race horses (specified activity)', 'Same activity', '4'],
        ['Specified business u/s 46 (optional regime)', 'Any specified business', 'No limit'],
        ['Unabsorbed depreciation', 'Any head except salary', 'No limit']], title='Carry forward at a glance')

    concepts = [
        C('c1', T1, [
            'Set-off means adjusting a loss against eligible income of the same tax year. If income is not enough, the remaining loss may be carried forward to later years within the limits in the Act.',
            'Section 108: a loss from one source can absorb income from another source under the same head — loss from a rented shop against rent of another house, or loss of a garment trade against profit of a printing press.',
            'Exceptions: long-term capital loss only against long-term gain (short-term loss may absorb either kind); speculation loss only against speculation profit (other business losses may absorb speculation profit); race horse losses only against race horse income; under the optional regime, a specified business loss u/s 46 only against another specified business.'],
          'Within one head, sources usually share a single pool — but a few sources are fenced off.',
          'A loss of ₹50,000 from a printing press reduces a ₹80,000 profit of a stationery shop to ₹30,000.'),
        C('c2', T2, [
            'Section 109: a loss left after inter-source set-off can be set off against income under another head, subject to exceptions.',
            'Business or profession loss cannot be set off against salary. Capital loss cannot be set off against any other head. Speculation and race horse losses stay within their own activity.',
            'House property loss: under the optional regime, only up to ₹2,00,000 may reduce other heads; under the default regime of section 202(1), none, and it cannot be carried forward either.',
            'No loss may be set off against casual income such as lottery, crossword, card game or betting winnings (s. 94). A loss from a source whose income is exempt cannot be set off against taxable income.'],
          'Salary and lottery winnings are protected islands that most losses cannot reach.',
          'A ₹3,00,000 business loss can wipe out rent and interest income, but not a single rupee of salary.'),
        C('c3', T3, [
            'Section 110 (optional regime): house property loss not absorbed in the year is carried forward up to 8 tax years and set off only against house property income. Filing the return on time is not a condition for this loss.',
            'Section 111: a short-term capital loss carried forward may absorb any capital gain; a long-term capital loss carried forward may absorb only long-term gain. Each can be carried forward up to 8 tax years after the year it first arose.',
            'Long-term loss on STT-paid equity shares or equity-oriented fund units is also eligible, because gains on them above ₹1,25,000 are taxable under section 198.'],
          'Old capital losses keep their label: long-term stays long-term.',
          'A ₹60,000 long-term loss from 2025-26 cannot reduce a 2026-27 short-term gain.'),
        C('c4', T4, [
            'Section 112: a business loss not absorbed in the year may be carried forward and set off only against business or professional income of later years, up to 8 tax years.',
            'The business need not be the same one that made the loss, and it need not continue.',
            'Only the person who suffered the loss can carry it forward. A successor cannot, unless the business passed by inheritance.'],
          'The loss travels with the taxpayer, not with the shop.',
          'A loss from a closed hardware store can absorb next year\'s consulting fees of the same person.'),
        C('c5', T5, [
            'Speculation (s. 113): its loss is set off only against speculation profit and may be carried forward 4 tax years. Loss on trading in derivatives is not a speculation loss.',
            'A company whose business partly consists of buying and selling shares of other companies is deemed to carry on speculation business to that extent. This does not apply if its gross total income is mainly from house property, capital gains or other sources, or its principal business is trading in shares, banking or granting loans and advances.',
            'Specified business u/s 46 (s. 114, optional regime): loss set off only against profit of any specified business, eligible or not, and carried forward indefinitely. Under the default regime the s. 46 deduction is not claimed, so any loss is an ordinary business loss.',
            'Specified activity (s. 115) means owning and maintaining race horses. Loss = stake money less revenue expenses of maintaining the horses; it is set off only against income from the same activity and carried forward 4 tax years. It is different from betting on races, which is casual income.'],
          'Risky ventures are ring-fenced so their losses cannot shelter ordinary income.',
          'A ₹40,000 loss from keeping race horses cannot reduce a ₹1,00,000 lottery win or a business profit.'),
        C('c6', T6, [
            'Order of set-off: (1) current year depreciation and current year scientific research and family planning expenditure; (2) brought forward business loss; (3) unabsorbed depreciation (s. 33(11)); (4) unabsorbed scientific research capital expenditure (s. 45(7)); (5) unabsorbed family planning expenditure (s. 32(i)).',
            'Unabsorbed depreciation is added to the current year\'s depreciation and treated as part of it. It is therefore not a business loss: it may reduce any head except salary and has no time limit.',
            'Sequence within a year: inter-source set-off first, then inter-head set-off, then brought forward losses.'],
          'Use the loss with an expiry date before the one that never expires.',
          'With profit of ₹1,00,000, a b/f loss of ₹60,000 and unabsorbed depreciation of ₹70,000, the b/f loss goes first and ₹30,000 depreciation remains.',
          blocks=[cf]),
        C('c7', T7, [
            'Section 121: capital loss, business loss, speculation loss, specified business loss and race horse loss can be carried forward only if determined in a return of loss filed within the time allowed by section 263(1).',
            'The condition does not apply to house property loss under section 110 or to unabsorbed depreciation under section 33(11).',
            'Under the default regime, these cannot be set off: brought forward loss from self-occupied house property; brought forward loss of a specified business u/s 46; brought forward loss arising from deductions u/s 45(3)(a), (b), (c); and unabsorbed depreciation from additional depreciation u/s 33(8).'],
          'A late return can cost you the right to use most old losses.',
          'A trader who files late keeps unabsorbed depreciation of ₹1,00,000 but loses a business loss of ₹55,000.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Loss schedule for a client', 'role': 'Tax associate',
         'situation': 'A client has a salary, a rented flat, two small businesses and old losses from earlier returns.',
         'steps': ['Group income by head and do inter-source set-off.', 'Apply inter-head set-off with the salary and capital gains barriers.', 'Set off brought forward losses in the correct order and check their age.', 'Confirm that earlier returns were filed on time.'],
         'takeaway': 'A clear loss schedule prevents both missed relief and wrong claims.'},
        {'id': 'j2', 'title': 'Regime choice', 'role': 'Article assistant',
         'situation': 'A client with a large house property loss asks whether to stay in the default regime.',
         'steps': ['Show the ₹2,00,000 set-off and carry forward under the optional regime.', 'Show that the loss lapses under the default regime.', 'Compare the final tax under both.'],
         'takeaway': 'House property loss is a major factor in choosing the regime.'},
    ]

    mcqs = [
        Q('m1', 'Loss from a rented shop can be set off against rent of another let-out house of the same person because:', ['Both sources fall under one head', 'Losses can absorb any income', 'Both are exempt', 'Rent is casual income'], 0,
          'Section 108 allows a loss from one source to absorb income from another source under the same head, since each head is computed by pooling all its sources. Both properties fall under house property. In practice: net all sources within a head first.', 'c1', T1),
        Q('m2', 'A long-term capital loss of the current year can be set off against:', ['Long-term capital gain only', 'Any capital gain', 'Salary', 'Business income'], 0,
          'Long-term capital loss is fenced: it can only absorb long-term capital gain. Short-term loss, by contrast, can absorb both short-term and long-term gains. In practice: set off the short-term loss where it saves most tax.', 'c1', T1),
        Q('m3', 'Profit from speculation business can be reduced by:', ['A loss from a non-speculative business', 'A long-term capital loss', 'A house property loss of any amount', 'Nothing at all'], 0,
          'Losses from ordinary business can absorb speculation profits, though speculation losses cannot absorb ordinary business profits. House property loss is limited and capital loss stays in its head. In practice: the fence works one way only.', 'c1', T1),
        Q('m4', 'A business loss cannot be set off against income under the head:', ['Salaries', 'Income from house property', 'Capital gains', 'Income from other sources'], 0,
          'Section 109 bars business or professional losses from reducing salary, though they can reduce every other head, including capital gains. In practice: such loss left over is carried forward.', 'c2', T2),
        Q('m5', 'Under the optional regime, a house property loss of ₹3,10,000 can reduce salary in the same year by at most:', ['₹2,00,000', '₹3,10,000', '₹1,10,000', 'Nil'], 0,
          'Only ₹2,00,000 of house property loss may be set off against other heads in a year; the remaining ₹1,10,000 is carried forward against house property income for up to 8 tax years. In practice: the cap applies per year.', 'c2', T2, 'moderate', check=200000),
        Q('m6', 'Under the default regime, a loss from a let-out house property:', ['Can neither be set off against other heads nor be carried forward', 'Can reduce other heads up to ₹2,00,000', 'Can be carried forward 8 years', 'Can reduce only salary'], 0,
          'For a taxpayer paying tax under section 202(1), house property loss is not allowed against any other head and cannot be carried forward. It can still be netted within the house property head. In practice: this often decides the regime.', 'c2', T2),
        Q('m7', 'A loss cannot be set off against which income?', ['Winnings from a lottery', 'Interest on a fixed deposit', 'Rent from a shop', 'Long-term capital gain on land'], 0,
          'Section 94 provides that no loss of any kind can be set off against casual income such as lotteries, crossword puzzles, card games, races and betting. The other incomes listed can absorb eligible losses. In practice: tax winnings in full.', 'c2', T2),
        Q('m8', 'A short-term capital loss carried forward can be set off against:', ['Short-term or long-term capital gains', 'Short-term capital gains only', 'Business income', 'Any head except salary'], 0,
          'Section 111 lets a brought forward short-term loss absorb any capital gain, while a brought forward long-term loss absorbs only long-term gain. Neither can cross into another head. In practice: both may be carried for 8 years.', 'c3', T3),
        Q('m9', 'Business loss of tax year 2020-21 not yet absorbed can last be set off in tax year:', ['2028-29', '2024-25', '2026-27', 'Any year without limit'], 0,
          'Business loss can be carried forward for 8 tax years immediately after the year it first arose: 2021-22 to 2028-29. After that it lapses. In practice: keep an age-wise register of losses.', 'c4', T4, 'moderate'),
        Q('m10', 'Mr. Shah buys a running business from Mr. Rao, which carries an unabsorbed business loss. The loss can be used by:', ['Mr. Rao only, against his own business income', 'Mr. Shah', 'Both equally', 'Neither'], 0,
          'Only the person who incurred the loss can carry it forward. A buyer or other successor cannot use it, except where the business passes by inheritance. In practice: losses do not transfer with a sale.', 'c4', T4),
        Q('m11', 'Loss on trading in derivatives on a recognised exchange is treated as:', ['An ordinary business loss', 'A speculation loss', 'A capital loss', 'Casual loss'], 0,
          'Trading in eligible derivatives is excluded from speculative transactions, so its loss is a normal business loss set off and carried forward under section 112. In practice: it can absorb other business income.', 'c5', T5),
        Q('m12', 'Unabsorbed loss from owning and maintaining race horses can be carried forward for:', ['4 tax years, only against income from the same activity', '8 tax years, against any income', 'Indefinitely', 'Not at all'], 0,
          'Section 115 ring-fences the specified activity: loss goes only against income from owning and maintaining race horses, for up to 4 tax years. Betting wins are casual income and cannot absorb it. In practice: track it separately.', 'c5', T5),
        Q('m13', 'Which comes first when setting off against business income?', ['Brought forward business loss', 'Unabsorbed depreciation', 'Unabsorbed scientific research expenditure', 'Unabsorbed family planning expenditure'], 0,
          'After current depreciation, brought forward business loss is absorbed before unabsorbed depreciation and the other unabsorbed items, because it has a time limit while unabsorbed depreciation does not. In practice: this preserves relief.', 'c6', T6),
        Q('m14', 'Unabsorbed depreciation carried forward can be set off against:', ['Any head other than salaries', 'Business income only', 'Salary only', 'Capital gains only'], 0,
          'Unabsorbed depreciation is treated as part of the current year\'s depreciation, so like any current business deduction it can reduce every head except salary, without a time limit. In practice: it is not a business loss.', 'c6', T6),
        Q('m15', 'A taxpayer files the return after the due date. Which can still be carried forward?', ['Unabsorbed depreciation', 'Business loss', 'Speculation loss', 'Short-term capital loss'], 0,
          'Section 121 requires a return of loss filed on time for capital, business, speculation, specified business and race horse losses. House property loss and unabsorbed depreciation are outside that rule. In practice: file on time.', 'c7', T7),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Inter-source set-off of businesses', 1, 'computation', 'same head|inter-source', nums=[biz]),
           S('s2', 'House property cap and carry forward', 2, 'computation', '2,00,000', nums=[sal, hpcf]),
           S('s3', 'Business loss not against salary', 1, 'concept', 'salary', nums=[bcf]),
           S('s4', 'Default regime treatment', 1, 'concept', 'lapse|default', nums=[gti_d])],
          ['Net within heads before crossing heads.'], ['Setting business loss against salary.'], ['Two-column table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Short-term loss against short-term gain', 1, 'computation', 'short', nums=[st]),
           S('s2', 'Long-term loss against long-term gain only', 2, 'computation', 'long-term', nums=[ltcf]),
           S('s3', 'Period of carry forward', 1, 'concept', '8|2031-32')],
          ['Keep the loss labels.'], ['Using long-term loss against short-term gain.'], ['Table.'], pad='table', checks=list(ck2)),
        W('q3', 5, i3['q'], i3['solution'],
          [S('s1', 'Current depreciation first', 1, 'computation', 'current', nums=[b1]),
           S('s2', 'B/f loss before unabsorbed depreciation', 2, 'computation', 'brought forward', nums=[b2]),
           S('s3', 'Depreciation against house property, not salary', 2, 'computation', 'salary', nums=[ud, g3])],
          ['Follow the order strictly.'], ['Setting depreciation against salary.'], ['Ordered table.'], pad='table', checks=list(ck3)),
    ]

    viva = [
        V('v1', 'What is the difference between set-off and carry forward?',
          'Set-off adjusts a loss against eligible income of the same tax year. Carry forward takes the loss that remains to later years, where it can be set off only against specified income within the time limit.',
          [P('p1', 'Same year', 5, 'same year|same tax year'), P('p2', 'Later years', 5, 'later|next|subsequent|following')], 'c1'),
        V('v2', 'Which incomes can a business loss not reduce in the year it arises?',
          'Salary income stays protected from it, and like every loss it is barred from casual income such as lottery or betting winnings.',
          [P('p1', 'Salary', 6, 'salar'), P('p2', 'Casual income', 4, 'lottery|casual|betting')], 'c2'),
        V('v3', 'Why is brought forward business loss set off before unabsorbed depreciation?',
          'Business loss can be carried forward only for 8 tax years, while unabsorbed depreciation lasts indefinitely, so using the business loss first prevents it from lapsing.',
          [P('p1', 'Time limit on business loss', 5, '8|time limit|lapse'), P('p2', 'Depreciation indefinite', 5, 'indefinite|unlimited|time limit')], 'c6'),
        V('v4', 'How does the default regime affect house property loss?',
          'Under the default regime the loss can only be adjusted within the house property head; it cannot reduce other heads and cannot be carried forward, whereas the optional regime allows ₹2,00,000 against other heads and carry forward of the rest.',
          [P('p1', 'Not against other heads', 5, 'other head'), P('p2', 'Optional regime ₹2 lakh', 5, '2,00,000|2 lakh')], 'c2'),
        V('v5', 'Which losses survive a late return?',
          'House property loss and unabsorbed depreciation can still be carried forward; capital, business, speculation, specified business and race horse losses need a return of loss filed in time.',
          [P('p1', 'House property and depreciation', 6, 'depreciation'), P('p2', 'Others need timely return', 4, 'time|due date')], 'c7'),
    ]

    cases = [{'id': 'k1', 'title': 'Mr. Kohli\'s mixed year', 'difficulty': 'moderate',
              'case': 'Mr. Kohli opts out of the default regime for tax year 2026-27. He has salary ₹5,00,000; profit from a hardware shop ₹1,20,000; loss from intraday share trading (speculation) ₹45,000; income from keeping race horses ₹20,000 with a brought forward race horse loss of tax year 2024-25 of ₹35,000; short-term capital loss ₹30,000; long-term capital gain on land ₹50,000; lottery winnings ₹60,000.',
              'mcqs': [
                  M('k1a', 'The speculation loss of ₹45,000 is:', ['Carried forward against future speculation profit', 'Set off against the hardware shop profit', 'Set off against salary', 'Set off against lottery winnings'], 0,
                    'A speculation loss can only absorb speculation profit. With no such profit this year, it is carried forward for up to 4 tax years, provided the return is filed on time. In practice: keep it in a separate column.', 'core', topic=T5),
                  M('k1b', 'Race horse loss carried forward to tax year 2027-28:', ['₹15,000', '₹35,000', 'Nil', '₹55,000'], 0,
                    'The ₹35,000 brought forward race horse loss absorbs the ₹20,000 income from the same activity, leaving ₹15,000 to carry forward within the 4-year limit. It cannot touch lottery or other income. In practice: watch the expiry year.', 'moderate', check=15000, topic=T5),
                  M('k1c', 'Net capital gains for the year:', ['₹20,000', '₹50,000', 'Nil', '₹80,000'], 0,
                    'Short-term capital loss can absorb long-term gain, so ₹50,000 less ₹30,000 leaves ₹20,000. The capital loss could not have reduced any other head. In practice: show the set-off in the capital gains schedule.', 'core', check=20000, topic=T1),
                  M('k1d', 'Gross total income of Mr. Kohli:', ['₹7,00,000', '₹6,55,000', '₹7,20,000', '₹6,40,000'], 0,
                    'Salary 5,00,000 plus business 1,20,000 plus capital gains 20,000 plus lottery 60,000 gives ₹7,00,000. Race horse income is fully absorbed, and the speculation loss is carried forward. In practice: casual income stays in full.', 'hard', check=700000, topic=T2),
              ]}]

    return unit(UID, 'p3', 'int-p3-a-ch05', 1, 'Set off, or Carry Forward and Set off of Losses',
                ['Apply inter-source and inter-head set-off and their exceptions.',
                 'Carry forward house property, capital, business, speculation, specified business and race horse losses within their limits.',
                 'Follow the order of set-off, including unabsorbed depreciation.',
                 'Apply the return-of-loss condition and the default regime restrictions.'],
                {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': ['int-p3-a-ch04-u01'],
                 'exam_tip': 'Work in a fixed sequence — within each head, then across heads, then brought forward losses — and keep a separate column for losses carried forward.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['s. 108: same-head set-off; LTCL, speculation, race horse and s. 46 losses fenced.',
                             's. 109: cross-head set-off; business loss not against salary; capital loss stays in its head.',
                             'House property loss: ₹2,00,000 cap and 8-year carry forward (optional regime); none under default regime.',
                             'Business 8 years; speculation and race horses 4 years; s. 46 and unabsorbed depreciation indefinite.',
                             'Order: current depreciation → b/f business loss → unabsorbed depreciation.',
                             's. 121: return of loss on time, except house property loss and unabsorbed depreciation.'],
                 'remember': ['No loss against casual income.', 'Successor cannot use the loss, except by inheritance.'],
                 'traps': ['Unabsorbed depreciation is not a business loss.', 'Derivative trading loss is not speculative.']},
                [('House property cap', '₹2,00,000 (optional regime)'), ('Capital loss', '8 years'), ('Speculation / race horses', '4 years'), ('Unabsorbed depreciation', 'No limit')],
                viva, cases)
