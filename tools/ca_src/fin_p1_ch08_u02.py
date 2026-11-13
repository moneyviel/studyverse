"""CA Final · Paper 1 Financial Reporting · Chapter 8 Unit 2 Ind AS 33 Earnings per Share.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch08-u02'
T1 = 'Basic EPS: earnings and weighted shares'
T2 = 'Bonus, rights and other share changes'
T3 = 'Diluted EPS and potential shares'
T4 = 'Presentation and restatement'


def build():
    ck = Checks()
    w = ck.add('100+30*6/12', 'Weighted average shares (lakh)')
    basic = ck.add('round(1000/(100+30*6/12),2)', 'Basic EPS (₹)')
    opt = ck.add('10*(1-40/50)', 'Shares issued for no consideration under options (lakh)')
    inc = ck.add('round(60*0.75/20,2)', 'Incremental EPS of convertibles (₹)')
    dil = ck.add('round((1000+60*0.75)/(100+30*6/12+10*(1-40/50)+20),2)', 'Diluted EPS (₹)')
    i1 = {'id': 'i1', 'title': 'Basic and diluted EPS', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Zenith Ltd.: profit after tax ₹1,200 lakh; dividend on cumulative preference shares ₹200 lakh. Equity shares: 100 lakh at 1 April; 30 lakh issued at full market price on 1 October. Potential shares: 10 lakh options exercisable at ₹40 (average market price ₹50); convertible debentures with interest of ₹60 lakh this year, convertible into 20 lakh shares. Tax rate 25%. Compute basic and diluted EPS.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Earnings for equity', '1,200 − 200', '₹1,000 lakh'],
              ['Weighted shares', '100 + 30 × 6/12', inr(w) + ' lakh'],
              ['Basic EPS', '1,000 ÷ 115', '₹' + inr(basic)],
              ['Options — free shares', '10 × (50 − 40)/50', inr(opt) + ' lakh'],
              ['Convertibles — incremental EPS', '60 × 75% ÷ 20', '₹' + inr(inc) + ' — dilutive'],
              ['Diluted EPS', '1,045 ÷ 137', '₹' + inr(dil)]], title='Ind AS 33')],
          'checks': list(ck)}

    ck2 = Checks()
    re = ck2.add('round(480/(200*1.25),2)', 'Restated prior-year EPS after 1-for-4 bonus (₹)')
    i2 = {'id': 'i2', 'title': 'A bonus issue', 'difficulty': 'core', 'minutes': 5,
          'q': 'Last year, Quartz Ltd. had 200 lakh shares and earnings of ₹480 lakh (EPS ₹2.40). This year it makes a 1-for-4 bonus issue. Restate last year\'s EPS for comparison.',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Bonus shares', '200 ÷ 4', '50 lakh'],
              ['Adjusted prior-year shares', '200 × 1.25', '250 lakh'],
              ['Restated prior-year EPS', '480 ÷ 250', '₹' + inr(re)]], title='Retrospective adjustment')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Basic EPS takes the parent\'s ordinary shareholders\' share of profit or loss and divides it by the time-weighted count of ordinary shares in issue over the period. It is calculated both for profit from continuing operations and for total profit.',
            'Earnings are adjusted for preference dividends (cumulative: the full year\'s dividend whether declared or not; non-cumulative: only declared amounts), differences on settlement of preference shares, and similar items, all after tax.',
            'Shares are weighted from the date consideration is receivable (generally the issue date). Shares issued for cash count from the cash receivable date; contingently issuable shares count from when all conditions are met; partly paid shares count to the extent of dividend participation.'],
          'EPS is earnings for ordinary shareholders spread over the average shares in issue.',
          'Shares issued halfway through the year count as half.'),
        C('c2', T2, [
            'Bonus issues, share splits and consolidations change the number of shares without changing resources; the number is adjusted as if the event had happened at the start of the earliest period presented, and comparatives are restated.',
            'A rights issue below fair value contains a bonus element. Adjustment factor = fair value per share immediately before exercise ÷ theoretical ex-rights fair value per share. Shares before the issue are multiplied by this factor.',
            'If such changes occur after the reporting period but before approval, the EPS figures are also restated. Share buy-backs at fair value reduce shares from the buy-back date.'],
          'Free shares shrink EPS for all years shown; fully paid issues affect only the period after issue.',
          'A 1-for-4 bonus turns 200 shares into 250 for every year shown.'),
        C('c3', T3, [
            'Diluted EPS adjusts earnings and weighted shares for all dilutive potential ordinary shares — options, warrants, convertible instruments and contingently issuable shares.',
            'Earnings are adjusted for post-tax effects of dividends, interest and other changes from conversion. Options and warrants are treated as exercised; only the shares deemed issued for no consideration (difference between shares issued and those that could be bought at average market price) are dilutive.',
            'Potential shares are dilutive only if conversion would decrease EPS (or increase loss per share) from continuing operations. They are ranked from most dilutive (lowest incremental EPS) to least, and included one by one; anti-dilutive items are excluded.'],
          'Diluted EPS shows the worst realistic case for ordinary shareholders.',
          'Options in the money with no earnings effect are added first.'),
        C('c4', T4, [
            'Basic and diluted EPS appear in the main profit and loss statement itself for each class of ordinary shares with different rights, with equal prominence, for all periods — even if negative (loss per share).',
            'An entity reporting a discontinued operation discloses basic and diluted EPS for it, on the face or in the notes.',
            'Disclosures include the earnings used and their reconciliation to profit, weighted average shares used and their reconciliation, instruments excluded because anti-dilutive, and share transactions after the reporting period. Additional per-share figures using other earnings measures may be shown in the notes using the same share numbers.'],
          'Both EPS figures sit side by side on the face of the statement.',
          'A loss year still shows basic and diluted loss per share.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Preparing EPS for the annual report', 'role': 'Reporting analyst',
             'situation': 'The company had a rights issue, ESOPs and convertibles during the year.',
             'steps': ['Compute earnings for equity holders.', 'Build the weighted share schedule with rights factor.', 'Rank potential shares by incremental EPS.', 'Restate comparatives for bonus elements.'],
             'takeaway': 'Ranking potential shares prevents overstating dilution.'}]

    mcqs = [
        Q('m1', 'Dividends on cumulative preference shares are deducted for basic EPS:', ['For the period whether declared or not', 'Only if declared', 'Never', 'Only if paid'], 0,
          'Cumulative rights accrue each year. In practice: non-cumulative only if declared.', 'c1', T1),
        Q('m2', 'A bonus issue during the year affects EPS by:', ['Adjusting shares as if issued at the start of the earliest period', 'Weighting from the issue date', 'No adjustment', 'Adjusting only the current year'], 0,
          'No resources were received. In practice: restate comparatives.', 'c2', T2),
        Q('m3', 'Options are dilutive when:', ['The exercise price is below the average market price', 'Exercise price exceeds market price', 'Always', 'Never'], 0,
          'Only then are shares effectively issued for nothing. In practice: out-of-the-money options are excluded.', 'c3', T3),
        Q('m4', 'Potential ordinary shares are included in diluted EPS:', ['From most dilutive to least dilutive', 'In issue order', 'From least to most', 'All at once regardless'], 0,
          'Sequencing finds maximum dilution. In practice: compute incremental EPS.', 'c3', T3),
        Q('m5', 'For a rights issue, the adjustment factor equals:', ['Fair value before exercise ÷ theoretical ex-rights value', 'Rights price ÷ fair value', 'New shares ÷ old shares', 'Market price ÷ par'], 0,
          'This captures the bonus element. In practice: apply to pre-issue shares.', 'c2', T2),
        Q('m6', 'Interest on convertible debentures is added back for diluted EPS:', ['Net of tax', 'Gross', 'Not at all', 'Twice'], 0,
          'Conversion saves interest after tax. In practice: include related expenses.', 'c3', T3),
        Q('m7', 'Basic and diluted EPS are presented:', ['On the face with equal prominence', 'Only in notes', 'Only basic on the face', 'Only if positive'], 0,
          'Even for losses. In practice: discontinued EPS may be in notes.', 'c4', T4),
        Q('m8', 'Anti-dilutive potential shares are:', ['Excluded from diluted EPS', 'Included', 'Halved', 'Shown separately in EPS'], 0,
          'They would increase EPS. In practice: disclose them.', 'c3', T3),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Basic', 3, 'computation', 'basic', nums=[w, basic]), S('s2', 'Options', 1.5, 'computation', 'option', nums=[opt]), S('s3', 'Incremental', 1.5, 'computation', 'incremental', nums=[inc]), S('s4', 'Diluted', 2, 'computation', 'diluted', nums=[dil])],
          ['Rank potential shares.'], ['Adding back gross interest.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Adjusted shares', 1.5, 'computation', 'adjusted', nums=[250]), S('s2', 'Restated EPS', 1.5, 'computation', 'restated', nums=[re])],
          ['Explain retrospective effect.'], ['Weighting the bonus.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'How is basic EPS calculated?', 'The parent\'s ordinary shareholders\' share of profit, divided by the weighted average number of ordinary shares in issue.',
          [P('p1', 'Profit to ordinary holders', 5, 'ordinary'), P('p2', 'Weighted average shares', 5, 'weighted')], 'c1'),
        V('v2', 'What is the bonus element in a rights issue?', 'The value given to shareholders by issuing shares below fair value, adjusted using fair value before exercise divided by theoretical ex-rights value.',
          [P('p1', 'Below fair value', 5, 'below fair value'), P('p2', 'Ex-rights value', 5, 'ex-rights')], 'c2'),
        V('v3', 'When is a potential share dilutive?', 'When converting it would lower EPS, or deepen the loss per share, measured on continuing operations.',
          [P('p1', 'Lower EPS', 6, 'lower'), P('p2', 'Continuing operations', 4, 'continuing')], 'c3'),
        V('v4', 'How are options treated in diluted EPS?', 'They are assumed exercised, and only the shares treated as issued free, measured at average market price, are added.',
          [P('p1', 'Assumed exercised', 5, 'exercised'), P('p2', 'Free shares', 5, 'free')], 'c3'),
        V('v5', 'Where are EPS figures presented?', 'In the main profit and loss statement itself, basic and diluted shown with equal prominence for every period.',
          [P('p1', 'Main statement', 5, 'main'), P('p2', 'Equal prominence', 5, 'prominence')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Beryl Ltd.', 'difficulty': 'moderate',
              'case': 'Beryl Ltd. has 50 lakh shares throughout the year and profit of ₹200 lakh. It has 5 lakh options at an exercise price of ₹60; average market price is ₹80. It also has non-cumulative preference shares on which no dividend was declared.',
              'mcqs': [
                  M('k1a', 'Basic EPS (₹):', ['4', '4.4', '3.64', '3.81'], 0,
                    '200 ÷ 50 = 4. In practice: no preference deduction as none declared.', 'core', check=4, topic=T1),
                  M('k1b', 'Shares deemed issued for no consideration (lakh):', ['1.25', '5', '3.75', '1'], 0,
                    '5 × (80 − 60)/80 = 1.25. In practice: use average price.', 'moderate', check=1.25, topic=T3),
                  M('k1c', 'Diluted EPS (₹, rounded to two decimals):', ['3.9', '4', '3.64', '3.5'], 0,
                    '200 ÷ 51.25 = 3.90. In practice: present with basic.', 'moderate', check=3.9, topic=T3),
                  M('k1d', 'Non-cumulative preference dividend deducted from earnings:', ['Nil, as none was declared', 'Full year amount', 'Half', 'Estimated'], 0,
                    'Only declared amounts are deducted for non-cumulative. In practice: check board minutes.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch08', 2, 'Ind AS 33 "Earnings per Share"',
                ['Compute basic EPS with correct earnings and weighted shares.',
                 'Adjust for bonus, rights and other share changes.',
                 'Compute diluted EPS by ranking potential shares.',
                 'Present and disclose EPS.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 35}, 'prereq': ['fin-p1-ch08-u01'],
                 'exam_tip': 'For diluted EPS, compute incremental EPS for each instrument and add them in order, starting with the lowest.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Basic EPS: ordinary earnings ÷ weighted shares.',
                             'Cumulative preference dividend deducted always.',
                             'Bonus: restate all periods.',
                             'Rights: apply adjustment factor.',
                             'Diluted: rank instruments; exclude anti-dilutive.'],
                 'remember': ['Options only add the free-share element.'],
                 'traps': ['Gross interest add-back for convertibles.']},
                [('Basic EPS', 'Earnings ÷ weighted shares'), ('Rights factor', 'FV ÷ TERP'), ('Options', 'Free shares only'), ('Order', 'Most dilutive first')],
                viva, cases)
