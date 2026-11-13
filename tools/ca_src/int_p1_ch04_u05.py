"""CA Intermediate · Paper 1 Advanced Accounting · Chapter 4 Unit 5 — AS 20 Earnings Per Share.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p1-ch04-u05'
T1 = 'Scope and the earnings figure for basic EPS'
T2 = 'Weighted average number of shares'
T3 = 'Bonus issues, splits and rights issues'
T4 = 'Diluted EPS and anti-dilution'
T5 = 'Presentation and disclosure'


def build():
    ck = Checks()
    earn = ck.add('5500000-1000000*10/100', 'Earnings for equity holders (₹)')
    wan = ck.add('800000*12/12+200000*6/12', 'Weighted shares before bonus')
    wab = ck.add('900000*6/5', 'Weighted shares after 1:5 bonus')
    eps = ck.add('5400000/1080000', 'Basic EPS (₹)')
    i1 = {'id': 'i1', 'title': 'Fresh issue and bonus in one year', 'difficulty': 'core', 'minutes': 8,
          'q': 'Kanchan Ltd. earned profit after tax of ₹55,00,000 in 2026-27. It has 10% cumulative preference shares of ₹10,00,000. Equity shares outstanding on 1 April 2026: 8,00,000. On 1 October 2026 it issued 2,00,000 shares for cash at full market price; on 1 January 2027 it made a 1:5 bonus issue. Compute basic EPS.',
          'solution': [table(['Step', 'Working', 'Figure'], [
              ['Earnings', '55,00,000 − 10% of 10,00,000', inr(earn)],
              ['Weighted shares (before bonus)', '8,00,000 × 12/12 + 2,00,000 × 6/12', R(wan)],
              ['Adjust for bonus (from the start)', '9,00,000 × 6/5', R(wab)],
              ['Basic EPS', '54,00,000 ÷ 10,80,000', f'₹{R(eps)}']], title='AS 20 basic EPS'),
              note('Cumulative preference dividend is deducted whether or not declared. Bonus shares are treated as outstanding from the beginning of the period, without time-weighting.')],
          'checks': list(ck)}

    ck2 = Checks()
    terp = ck2.add('(1000000*100+250000*60)/1250000', 'Theoretical ex-rights fair value (₹)')
    fac = ck2.add('round(100/92, 4)', 'Adjustment factor')
    was = ck2.add('round(1000000*3/12*100/92+1250000*9/12)', 'Weighted average shares')
    eps2 = ck2.add('round(12000000/1209239, 2)', 'Basic EPS (₹)')
    i2 = {'id': 'i2', 'title': 'Rights issue below fair value', 'difficulty': 'hard', 'minutes': 10,
          'q': 'Sagar Ltd. had 10,00,000 equity shares. On 1 July 2026 it made a 1-for-4 rights issue at ₹60 per share; the fair value just before exercise was ₹100. Profit for 2026-27 (April–March) attributable to equity holders is ₹1,20,00,000. Compute basic EPS.',
          'solution': [table(['Step', 'Working', 'Figure'], [
              ['Theoretical ex-rights fair value', '(10,00,000 × 100 + 2,50,000 × 60) ÷ 12,50,000', f'₹{R(terp)}'],
              ['Adjustment factor', '100 ÷ 92', R(fac)],
              ['Weighted shares', '10,00,000 × 3/12 × 100/92 + 12,50,000 × 9/12', R(was)],
              ['Basic EPS', '1,20,00,000 ÷ 12,09,239', f'₹{R(eps2)}']], title='Rights issue with a bonus element'),
              note('Last year\'s EPS is also restated by dividing it by the adjustment factor.')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'AS 20 prescribes how to compute and present EPS so that performance can be compared across periods and enterprises. It is mandatory for enterprises with equity shares listed or in the process of listing, and for others that disclose EPS.',
            'Basic EPS = profit (or loss) belonging to equity holders for the year ÷ the time-weighted count of equity shares in issue.',
            'Earnings are profit after tax for the period less preference dividends for the period and related tax. Cumulative preference dividend for the period is deducted whether or not declared; non-cumulative only if provided for or declared. Arrears of earlier years are not deducted again.'],
          'EPS tells each ordinary share how much of the year\'s profit belongs to it.',
          'Unpaid cumulative preference dividend of the current year still reduces equity earnings.'),
        C('c2', T2, [
            'Shares are counted from the date consideration is receivable — generally the date of issue: for cash, when cash is receivable; on conversion of debt, from when interest stops; in exchange for assets, from recognition of the acquisition.',
            'Time-weighting factor = days (or months) the shares are outstanding ÷ days in the period.',
            'Partly paid shares count as a fraction of a share to the extent they rank for dividend relative to a fully paid share. Contingently issuable shares are included from the date all conditions are met.'],
          'A share issued halfway through the year earns half a share\'s weight.',
          'Shares issued on 1 January in an April–March year carry a weight of 3/12.'),
        C('c3', T3, [
            'Bonus issues, share splits and consolidations change the number of shares without changing resources. They are treated as if they occurred at the start of the earliest period presented, and earlier EPS figures are restated.',
            'A rights issue below fair value has a bonus element. Shares before the issue are multiplied by: fair value per share immediately before exercise ÷ theoretical ex-rights fair value per share.',
            'Theoretical ex-rights fair value = (total fair value of existing shares + rights proceeds) ÷ shares after the issue.',
            'If such changes occur after the balance sheet date but before approval of the statements, EPS is still computed on the new number and this is disclosed.'],
          'Bonus shares are free slices of the same cake, so they are counted from the very beginning.',
          'A 1:1 bonus halves both this year\'s and last year\'s EPS as reported.'),
        C('c4', T4, [
            'Diluted EPS assumes conversion of all dilutive potential equity shares (convertible debentures and preference shares, options, warrants).',
            'Earnings are increased by the after-tax effect of dividends and interest on dilutive potential shares, and any other consequential changes. Shares are increased by the number that would be issued on conversion, from the start of the period or the date of issue if later.',
            'Options and warrants: only the shares deemed issued for no consideration count — shares under option minus the number that the exercise proceeds would buy at fair value.',
            'Potential shares are dilutive only if conversion reduces EPS from continuing ordinary operations. Anti-dilutive ones are ignored; they are tested one by one, starting with the instrument that cuts EPS the most.'],
          'Diluted EPS shows the worst-case sharing of profit if every convertible were converted.',
          'Options for 10,000 shares at ₹60 when fair value is ₹80 add 2,500 shares for diluted EPS.'),
        C('c5', T5, [
            'Basic and diluted EPS appear in the statement of profit and loss itself (not just the notes) for each class of equity shares with different rights, with equal prominence, for all periods presented — even if negative (loss per share).',
            'Disclose the numerators and their reconciliation to profit, the weighted average shares used for basic and diluted EPS and their reconciliation, and the nominal value of shares.',
            'If EPS is also given using other earnings figures, the same share numbers are used and basic and diluted figures shown with equal prominence, in the notes.'],
          'Both figures, side by side, on the face of the profit and loss statement.',
          'A loss of ₹2 per share is still reported as basic and diluted EPS.'),
    ]

    jobs = [{'id': 'j1', 'title': 'EPS working for the annual report', 'role': 'Reporting analyst',
             'situation': 'A listed client issued shares, made a bonus issue and granted employee options during the year.',
             'steps': ['Compute equity earnings after preference dividend.', 'Time-weight new shares; adjust bonus from the start.', 'Test options and convertibles for dilution.', 'Restate prior-year EPS.'],
             'takeaway': 'Get the share count right before worrying about dilution.'}]

    mcqs = [
        Q('m1', 'Profit after tax ₹30 lakh; 12% non-cumulative preference shares ₹20 lakh, no dividend declared. Earnings for basic EPS:', ['₹30 lakh', '₹27.6 lakh', '₹32.4 lakh', '₹28 lakh'], 0,
          'Non-cumulative preference dividend is deducted only if it is provided for or declared for the period. With no dividend declared, all ₹30 lakh belongs to equity holders. In practice: cumulative dividend would have been deducted.', 'c1', T1, 'moderate', check=30),
        Q('m2', 'Arrears of cumulative preference dividend for earlier years paid this year are:', ['Not deducted again in computing current year earnings', 'Deducted in full', 'Added back', 'Deducted only if material'], 0,
          'Only the cumulative preference dividend for the current period is deducted; arrears relating to earlier years were already deducted then. Deducting again would double count. In practice: look at the period the dividend relates to.', 'c1', T1),
        Q('m3', '6,00,000 shares at the start; 1,20,000 issued for cash on 1 January (year April–March). Weighted average shares:', ['6,30,000', '7,20,000', '6,90,000', '6,60,000'], 0,
          'The new shares are outstanding for 3 of 12 months: 6,00,000 + 1,20,000 × 3/12 = 6,30,000. Shares are counted from the date consideration is receivable. In practice: use days if dates are uneven.', 'c2', T2, 'core', check=630000),
        Q('m4', 'A 1:2 bonus issue in the middle of the year is treated as if issued:', ['At the beginning of the earliest period reported', 'On the date of issue', 'At the end of the year', 'Six months before the year end'], 0,
          'Bonus issues change only the number of shares, not resources, so they are adjusted from the start of the earliest period presented and prior EPS is restated. No time-weighting is applied. In practice: restate comparatives.', 'c3', T3),
        Q('m5', 'Fair value before rights ₹120; theoretical ex-rights fair value ₹110. The adjustment factor for shares before the rights issue is:', ['1.0909', '0.9167', '1.10', '1.20'], 0,
          'The factor is fair value just before exercise divided by theoretical ex-rights fair value: 120 ÷ 110 = 1.0909. It is applied to shares before the issue for the period before it. In practice: restate prior EPS by dividing by it.', 'c3', T3, 'hard', check=1.0909),
        Q('m6', 'Options over 20,000 shares at ₹50 each; average fair value ₹80. Shares deemed issued for no consideration:', ['7,500', '20,000', '12,500', 'Nil'], 0,
          'Proceeds of ₹10,00,000 would buy 12,500 shares at ₹80, so the remaining 7,500 shares are treated as issued free and added for diluted EPS. In practice: only in-the-money options dilute.', 'c4', T4, 'hard', check=7500),
        Q('m7', 'Interest on convertible debentures for diluted EPS is:', ['Added back to earnings net of tax', 'Added back gross of tax', 'Deducted from earnings', 'Ignored'], 0,
          'On assumed conversion, interest would no longer be paid, so earnings are increased by the after-tax interest and the shares on conversion are added. In practice: compute the incremental EPS of each instrument.', 'c4', T4),
        Q('m8', 'A potential equity share that increases EPS on conversion is:', ['Anti-dilutive and ignored', 'Dilutive and included', 'Included only in basic EPS', 'Included if the holder chooses'], 0,
          'Potential shares are included only when they reduce EPS from continuing ordinary operations; if conversion would raise EPS, they are anti-dilutive and excluded. In practice: rank from most to least dilutive.', 'c4', T4),
        Q('m9', 'Basic and diluted EPS are presented:', ['On the face of the profit and loss statement with equal prominence', 'Only in the directors\' report', 'Only in notes', 'Only when positive'], 0,
          'AS 20 requires both figures in the profit and loss statement itself for each class of equity shares, with equal prominence for all periods, even when negative. In practice: show a loss per share too.', 'c5', T5),
        Q('m10', 'Shares issued on conversion of a debenture are included in the weighted average from:', ['The date interest ceases to accrue', 'The start of the year', 'The date of the board meeting', 'The year end'], 0,
          'For conversion of debt, shares are counted from the date interest stops accruing, as that is when the consideration is effectively received. In practice: check the conversion date in the terms.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Earnings after preference dividend', 1.5, 'computation', 'preference', nums=[earn]),
           S('s2', 'Time-weighted shares', 1.5, 'computation', '6/12', nums=[wan]),
           S('s3', 'Bonus adjustment and EPS', 2, 'computation', 'bonus', nums=[wab, eps])],
          ['Bonus is not time-weighted.'], ['Time-weighting the bonus shares.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Theoretical ex-rights value', 2, 'computation', 'ex-rights', nums=[terp]),
           S('s2', 'Adjustment factor and weighting', 2, 'computation', 'factor', nums=[was]),
           S('s3', 'EPS', 2, 'computation', 'eps', nums=[eps2])],
          ['Apply the factor only to the pre-issue period.'], ['Ignoring the bonus element.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'How is basic EPS computed?', 'Profit or loss belonging to equity holders, divided by the weighted average count of equity shares in issue over the year.',
          [P('p1', 'Profit to equity holders', 5, 'equity'), P('p2', 'Weighted average shares', 5, 'weighted')], 'c1'),
        V('v2', 'Why are bonus shares not time-weighted?', 'Because a bonus issue splits the same resources over more shares, so it is treated as if it had occurred at the start of the earliest period presented.',
          [P('p1', 'No new resources', 5, 'resource|consideration'), P('p2', 'From the start', 5, 'start|beginning')], 'c3'),
        V('v3', 'What is the bonus element in a rights issue?', 'When rights are offered below fair value, part of the issue is effectively free; it is adjusted by the ratio of fair value before exercise to theoretical ex-rights fair value.',
          [P('p1', 'Below fair value', 5, 'below|less than'), P('p2', 'Ratio of values', 5, 'ex-rights|ratio')], 'c3'),
        V('v4', 'What is anti-dilution?', 'A potential share whose conversion would increase EPS, or reduce loss per share, from continuing operations; it is ignored in diluted EPS.',
          [P('p1', 'Increases EPS', 6, 'increase'), P('p2', 'Ignored', 4, 'ignor|exclud')], 'c4'),
        V('v5', 'How are options treated in diluted EPS?', 'The shares under option are split into those that the proceeds would buy at fair value and the rest, which are treated as issued for no consideration and added to the share count.',
          [P('p1', 'Proceeds at fair value', 5, 'fair value'), P('p2', 'No consideration', 5, 'no consideration|free')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Vasant Ltd.', 'difficulty': 'moderate',
              'case': 'Vasant Ltd. has 10,00,000 equity shares throughout the year and profit attributable to equity holders of ₹40,00,000. It has 50,000 10% convertible debentures of ₹100 each, each convertible into 2 shares, outstanding all year. Tax rate is 25%.',
              'mcqs': [
                  M('k1a', 'Basic EPS:', ['₹4.00', '₹3.64', '₹4.38', '₹3.50'], 0,
                    'Basic EPS is ₹40,00,000 divided by 10,00,000 shares, giving ₹4.00. Convertibles are ignored for basic EPS. In practice: present it alongside diluted EPS.', 'core', check=4, topic=T1),
                  M('k1b', 'Earnings adjustment for diluted EPS:', ['₹3,75,000', '₹5,00,000', '₹1,25,000', 'Nil'], 0,
                    'Interest of 10% on ₹50,00,000 is ₹5,00,000; after 25% tax, ₹3,75,000 is added back because it would not be paid on conversion. In practice: use the after-tax amount.', 'moderate', check=375000, topic=T4),
                  M('k1c', 'Diluted EPS:', ['₹3.98', '₹4.00', '₹3.64', '₹4.38'], 0,
                    'Diluted earnings ₹43,75,000 over 11,00,000 shares (10,00,000 + 1,00,000 on conversion) give ₹3.98, which is below basic EPS, so the debentures are dilutive. In practice: test each instrument.', 'hard', check=round(4375000/1100000, 2), topic=T4),
              ]}]

    return unit(UID, 'p1', 'int-p1-ch04', 5, 'Accounting Standard 20 Earnings Per Share',
                ['Compute earnings attributable to equity shareholders.',
                 'Compute the weighted average number of shares including bonus and rights issues.',
                 'Compute diluted EPS and identify anti-dilutive instruments.',
                 'Present and disclose EPS.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 40}, 'prereq': ['int-p1-ch04-u04'],
                 'exam_tip': 'Write numerator and denominator separately, adjust bonus from the start, apply the rights factor only before the issue date.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Basic EPS = equity earnings ÷ weighted average shares.', 'Deduct current cumulative preference dividend even if undeclared.',
                             'Time-weight issues; bonus, split, consolidation from the start.', 'Rights factor = fair value before ÷ TERP.',
                             'Diluted: add back after-tax interest/dividend; add conversion shares; options via treasury method.', 'Ignore anti-dilutive items; show both EPS with equal prominence.'],
                 'remember': ['Restate prior EPS for bonus and rights.'],
                 'traps': ['Arrears of earlier years are not deducted again.']},
                [('Basic EPS', 'Equity profit ÷ weighted shares'), ('Rights factor', 'FV before ÷ TERP'), ('Options', 'Shares − proceeds ÷ FV')],
                viva, cases)
