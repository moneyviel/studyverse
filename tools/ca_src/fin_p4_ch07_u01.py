"""CA Final · Paper 4 · Chapter 7 Set off and Carry Forward of Losses.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch07-u01'
T1 = 'Inter-source and inter-head set-off'
T2 = 'Carry forward of losses by head'
T3 = 'Losses on amalgamation, succession and change in shareholding'
T4 = 'Return of loss and restrictions'


def build():
    ck = Checks()
    sal = ck.add('900000-200000', 'Salary after house property loss set-off (₹)')
    hp = ck.add('300000-200000', 'House property loss carried forward (₹)')
    bl = ck.add('150000-50000', 'Business loss carried forward (₹)')
    i1 = {'id': 'i1', 'title': 'Set-off for an individual outside the default regime', 'difficulty': 'core', 'minutes': 8,
          'q': 'Deepa, who has opted out of the default regime, has for T.Y. 2026-27: salary ₹9,00,000; loss from let-out house property ₹3,00,000; non-speculative business loss ₹1,50,000; STCG ₹50,000; long-term capital loss ₹80,000. Compute gross total income and losses carried forward.',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['House property loss', 'Set off against salary up to ₹2,00,000', inr(sal)],
              ['HP loss carried forward', 'Balance, for 8 years', inr(hp)],
              ['Business loss', 'Set off against STCG ₹50,000 (not salary)', '—'],
              ['Business loss carried forward', 'Balance', inr(bl)],
              ['Long-term capital loss', 'Cannot be set off against STCG or other heads; carried forward', '80,000'],
              ['Gross total income', 'Salary after set-off', inr(sal)]], title='Sections 108–112')],
          'checks': list(ck)}

    c2 = Checks()
    cont = c2.add('min(60,35)+min(40,40)', 'Voting power held by the same persons on both dates (%)')
    i2 = {'id': 'i2', 'title': 'Change in shareholding of a closely held company', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Brightloom Pvt Ltd (not an eligible start-up) incurred a business loss in T.Y. 2023-24. On 31 March 2024 its shares were held by Ajay 60% and Bina 40%. During T.Y. 2026-27 Ajay sold 25% to Chetan; on 31 March 2027 the holding is Ajay 35%, Bina 40%, Chetan 25%. Can the loss be set off in T.Y. 2026-27?',
          'solution': [table(['Test', 'Working', 'Result'], [
              ['Same persons on both last days', 'Ajay 35% + Bina 40%', f'{inr(cont)}%'],
              ['Threshold', 'At least 51% of voting power', 'Met'],
              ['Conclusion', 'Loss can be set off', '—']], title='Section 119')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 108: a loss from one source can be set off against income from another source under the same head, except that long-term capital loss is set off only against LTCG, speculation loss only against speculation income, loss from specified businesses under section 46 only against such businesses, and loss from owning race horses only against that activity. Losses from exempt sources cannot be set off.',
            'Section 109: a loss under one head may be set off against income under another head, but business loss cannot be set off against salary, and capital loss cannot be set off against any other head.',
            'House property loss: outside the default regime, set off against other heads up to ₹2,00,000 a year (section 110); under the default regime of section 202, it cannot be set off against other heads at all.'],
          'Same head first, then other heads, subject to fences.',
          'A long-term capital loss cannot absorb short-term gains.'),
        C('c2', T2, [
            'House property loss (section 110): carried forward 8 years, set off only against house property income. Capital loss (section 111): 8 years — short-term loss against any capital gain, long-term loss only against LTCG.',
            'Business loss (section 112): 8 years against business income; the business need not continue. Speculation loss (section 113): 4 years against speculation income. Specified business loss under section 46 (section 114): indefinitely against specified business income. Race-horse loss (section 115): 4 years against that activity.',
            'Unabsorbed depreciation (section 33(11)) is carried forward indefinitely and can be set off against any head other than salary. Order: current depreciation, brought-forward business loss, unabsorbed depreciation.'],
          'Eight years for most, four for speculation and race horses, no limit for depreciation.',
          'A speculation loss of T.Y. 2026-27 expires after T.Y. 2030-31.'),
        C('c3', T3, [
            'Section 116: on qualifying amalgamations (companies owning industrial undertakings, ships or hotels; banks with specified banks; PSUs; erstwhile PSUs after strategic disinvestment) and on specified business reorganisations, the amalgamating company\'s losses and unabsorbed depreciation pass to the successor. The amalgamating company must have carried on the business for 3 years and held three-fourths of its fixed assets for 2 years; the successor must hold three-fourths of those assets and continue the business for 5 years.',
            'Carry forward in the successor\'s hands is restricted to the remaining part of the eight years counted from the year the loss was first computed for the original predecessor. Section 117 covers bank and government company amalgamations; section 118 cooperative banks.',
            'Section 119: on change in constitution of a firm, the loss share of a retired or deceased partner (beyond his profit share) lapses; on succession other than by inheritance the successor cannot use the predecessor\'s loss; for a closely held company, losses carry forward only if persons holding at least 51% of voting power on the last day of the loss year continue to hold it — with relief for eligible start-ups (all original shareholders continue, within 10 years of incorporation), death, gifts to relatives and IBC resolutions.'],
          'Losses follow continuity of ownership or business.',
          'A 75% common holding on both last days preserves the loss.'),
        C('c4', T4, [
            'Section 121: capital, business, speculation, specified business and race-horse losses can be carried forward only if determined in a return filed within the time under section 263(1).',
            'House property loss and unabsorbed depreciation are not subject to this condition.',
            'Section 120: income brought to tax as undisclosed after a search, requisition or survey cannot be reduced by any loss or unabsorbed depreciation.'],
          'File on time or lose most losses.',
          'A belated return of business loss forfeits its carry-forward.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Loss memo for a start-up', 'role': 'Tax manager',
             'situation': 'A private company raising a new funding round has accumulated losses.',
             'steps': ['Check start-up eligibility and shareholder continuity.', 'Compute 51% common holding.', 'Track expiry years of each loss.', 'Ensure timely return filing.'],
             'takeaway': 'Funding rounds can wipe out losses if continuity breaks.'}]

    mcqs = [
        Q('m1', 'Business loss cannot be set off against:', ['Salary', 'House property income', 'Capital gains', 'Other sources'], 0,
          'Section 109. In practice: carry forward.', 'c1', T1),
        Q('m2', 'House property loss set off against other heads (outside default regime) is limited to:', ['Two lakh rupees', 'One lakh rupees', 'Nil', 'Unlimited'], 0,
          'Section 110. In practice: balance carried forward.', 'c1', T1),
        Q('m3', 'Speculation loss can be carried forward for:', ['Four tax years', 'Eight tax years', 'Indefinitely', 'Two tax years'], 0,
          'Section 113. In practice: only against speculation income.', 'c2', T2),
        Q('m4', 'Unabsorbed depreciation can be carried forward for:', ['An unlimited period', 'Eight tax years', 'Four tax years', 'Ten tax years'], 0,
          'Section 33(11). In practice: not against salary.', 'c2', T2),
        Q('m5', 'Long-term capital loss can be set off against:', ['Long-term capital gains only', 'Any capital gains', 'Salary', 'Business income'], 0,
          'Sections 108 and 111. In practice: 8 years.', 'c2', T2),
        Q('m6', 'For a closely held company, continuity of voting power required is at least:', ['Fifty-one percent', 'Seventy-five percent', 'Twenty-six percent', 'One hundred percent'], 0,
          'Section 119. In practice: start-up relief differs.', 'c3', T3),
        Q('m7', 'In the successor company after amalgamation, the predecessor\'s loss can be carried forward:', ['For the remaining part of eight years from first computation', 'For a fresh eight years', 'Indefinitely', 'Not at all'], 0,
          'Section 116. In practice: no reset.', 'c3', T3),
        Q('m8', 'Which loss can be carried forward even if the return is filed late?', ['House property loss', 'Business loss', 'Speculation loss', 'Capital loss'], 0,
          'Section 121 exception. In practice: also unabsorbed depreciation.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'House property loss', 2, 'computation', 'two lakh|2,00,000', nums=[sal, hp]), S('s2', 'Business loss', 2, 'computation', 'salary', nums=[bl]), S('s3', 'Capital loss', 2, 'analysis', 'long-term')],
          ['State carry forward periods.'], ['Setting business loss against salary.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Common holding', 3, 'computation', 'voting', nums=[cont]), S('s2', 'Conclusion', 2, 'judgement', '51%')],
          ['Compare both last days.'], ['Looking only at changes during the year.'], ['Ratio test.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Can house property loss be set off under the default regime?', 'Inter-head set-off of house property loss is barred under the default regime of section 202.',
          [P('p1', 'Barred', 5, 'barred'), P('p2', 'Default regime', 5, 'default')], 'c1'),
        V('v2', 'What is the order of set-off for business losses and depreciation?', 'Current depreciation first, then brought-forward business loss, then unabsorbed depreciation.',
          [P('p1', 'Current depreciation', 5, 'current'), P('p2', 'Unabsorbed last', 5, 'unabsorbed')], 'c2'),
        V('v3', 'What happens to a retiring partner\'s share of loss?', 'The portion of loss proportionate to his share, beyond his profit share, lapses for the firm.',
          [P('p1', 'Lapses', 5, 'lapse'), P('p2', 'Proportionate share', 5, 'proportion|share')], 'c3'),
        V('v4', 'Can heirs use a deceased proprietor\'s business loss?', 'Yes, succession by inheritance allows legal heirs, even as a firm, to set off the loss.',
          [P('p1', 'Inheritance', 5, 'inherit'), P('p2', 'Legal heirs', 5, 'heir')], 'c3'),
        V('v5', 'Can losses be set off against undisclosed income found in a search?', 'Section 120 bars it: neither losses nor unabsorbed depreciation may reduce income detected that way.',
          [P('p1', 'Section 120', 5, '120'), P('p2', 'Bars set-off', 5, 'bar')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Orion Traders', 'difficulty': 'moderate',
              'case': 'Orion, a firm, has for T.Y. 2026-27: business income ₹6,00,000; speculation loss ₹1,20,000; brought-forward business loss of T.Y. 2017-18 ₹2,00,000; brought-forward business loss of T.Y. 2022-23 ₹3,00,000; unabsorbed depreciation ₹1,50,000. It filed all returns on time.',
              'mcqs': [
                  M('k1a', 'Can the T.Y. 2017-18 business loss be set off in T.Y. 2026-27?', ['No, eight years have expired', 'Yes, fully', 'Yes, against speculation income only', 'Yes, half'], 0,
                    'Eight years end with T.Y. 2025-26. In practice: track expiry.', 'core', topic=T2),
                  M('k1b', 'Business income after setting off the T.Y. 2022-23 loss (₹):', ['3,00,000', '6,00,000', '1,00,000', '4,80,000'], 0,
                    '6,00,000 − 3,00,000. In practice: before unabsorbed depreciation.', 'core', check=300000, topic=T2),
                  M('k1c', 'Income after unabsorbed depreciation (₹):', ['1,50,000', '3,00,000', '30,000', 'Nil'], 0,
                    '3,00,000 − 1,50,000. In practice: depreciation set off last.', 'core', check=150000, topic=T2),
                  M('k1d', 'The speculation loss of ₹1,20,000:', ['Is carried forward for four years', 'Is set off against business income', 'Lapses', 'Is carried forward indefinitely'], 0,
                    'Sections 108 and 113. In practice: speculation only.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch07', 1, 'Set off and Carry Forward of Losses',
                ['Apply inter-source and inter-head set-off rules.',
                 'Carry forward and set off losses by head.',
                 'Apply rules on amalgamation, succession and change in shareholding.',
                 'Apply return-of-loss and undisclosed-income restrictions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['fin-p4-ch06-u01'],
                 'exam_tip': 'Set off within the head first, then across heads, and show expiry years for carried-forward losses.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 108 inter-source; 109 inter-head.', 'HP loss ₹2 lakh outside default regime; 8 years.', 'Business 8, speculation 4, race horses 4; depreciation indefinite.',
                             'Section 116 remaining period after amalgamation.', 'Section 119 51% test; section 121 timely return.'],
                 'remember': ['Capital loss never crosses heads.'],
                 'traps': ['Resetting the 8-year clock on amalgamation.']},
                [('Inter-source', 'Section 108'), ('Inter-head', 'Section 109'), ('Business loss', 'Section 112'), ('Closely held company', 'Section 119'), ('Return of loss', 'Section 121')],
                viva, cases)
