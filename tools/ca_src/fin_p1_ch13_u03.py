"""CA Final · Paper 1 Financial Reporting · Chapter 13 Unit 3 Consolidated Financial Statements (Ind AS 110 control).
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch13-u03'
T1 = 'Scope of Ind AS 110 and exemptions'
T2 = 'Power: relevant activities and rights'
T3 = 'Variable returns and the link: principal or agent'
T4 = 'Continuous assessment and investment entities'


def build():
    ck = Checks()
    largest_other = ck.add('3', 'Largest other holder (%)')
    needed = ck.add('100-45', 'Votes held by others (%)')
    cast = ck.add('45/60*100', 'Lyra share of votes cast at 60% turnout (%)')
    i1 = {'id': 'i1', 'title': 'De facto control', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Lyra Ltd. holds 45% of the votes in Vega Ltd. The remaining 55% is spread among thousands of shareholders, none holding more than 3%; there are no agreements among them, and past meetings show attendance of about 60%. Does Lyra control Vega?',
          'solution': [table(['Factor', 'Analysis', 'Result'], [
              ['Lyra\'s holding', 'Largest by far', '45%'],
              ['Others', 'Dispersed; largest ' + inr(largest_other) + '%; total ' + inr(needed) + '%', 'Many would need to act together'],
              ['Attendance', '60% turnout: 45 ÷ 60 = ' + inr(cast) + '% of votes cast', 'Practical ability to direct'],
              ['Conclusion', 'Lyra has power without a majority (de facto control)', 'Subsidiary']], title='Size and dispersion of holdings')],
          'checks': list(ck)}

    ck2 = Checks()
    exp = ck2.add('1+0.2*10', 'Fund manager\'s total return per ₹100 crore of fund gain (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Is the fund manager a principal?', 'difficulty': 'hard', 'minutes': 9,
          'q': 'Orion AMC manages a fund with broad decision rights. It earns a market-rate fee of 1% of assets and holds 20% of the fund units. Investors can remove Orion only by a 75% vote of independent investors. For a year where the fund (₹100 crore) gains 10%, what is Orion\'s total return, and is it a principal or an agent?',
          'solution': [table(['Factor', 'Analysis', 'Result'], [
              ['Fee', '1% of ₹100 crore', '₹1 crore'],
              ['Share of gain', '20% × ₹10 crore', '₹2 crore'],
              ['Total return', '1 + 2', '₹' + inr(exp) + ' crore'],
              ['Removal rights', 'Not substantive (high threshold, many investors)', 'No constraint'],
              ['Exposure', '20% stake + fee = significant variability', 'Principal — consolidate']], title='Principal versus agent')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Ind AS 110 requires a parent to present consolidated statements and sets a single control model for all investees, including structured entities.',
            'A parent need not consolidate if: it is itself wholly owned (or partly owned with other owners informed and not objecting); its debt or equity is not publicly traded and it is not in the process of listing; and its ultimate or intermediate parent publishes Ind AS-compliant consolidated statements. Post-employment benefit plans are excluded.',
            'Investment entities do not consolidate most subsidiaries (see later). In India, company law also determines when consolidated statements are prepared.'],
          'One control model for every type of investee.',
          'An unlisted intermediate holding company may be exempt.'),
        C('c2', T2, [
            'An investor has power when its existing rights give it the current ability to direct relevant activities — those that most significantly affect returns (e.g. operating, financing, R&D, budget decisions). Purpose and design of the investee guide the analysis.',
            'Power usually comes from voting rights: a majority, unless another party controls via contract or the votes are not substantive. Without a majority, power can arise from contractual arrangements, rights from other agreements, de facto control (size of holding relative to dispersed others), or substantive potential voting rights (exercisable when decisions are needed and in the money or otherwise beneficial).',
            'Protective rights (e.g. lender covenants, veto over fundamental changes) do not give power. Only substantive rights — those the holder has the practical ability to exercise — count.'],
          'Ask who directs the activities that move the returns.',
          'A franchisor\'s brand-protection rights are protective, not power.'),
        C('c3', T3, [
            'Variable returns are returns that can vary with the investee\'s performance — dividends, changes in value, fees, tax benefits, residual interests, cost savings or synergies.',
            'The link: the investor must be able to use its power to affect its own returns. A decision maker acting as agent for others does not control.',
            'Principal vs agent factors: scope of decision-making authority; rights held by others (substantive removal rights by a single party make the manager an agent); remuneration (market-based or not); and exposure to variability from other interests. The greater the magnitude and variability of total economic interest, the more likely a principal.'],
          'Power must work for your own benefit, not just for others.',
          'A manager with a fee only and removable at will is an agent.'),
        C('c4', T4, [
            'Control is reassessed whenever facts and circumstances indicate a change in any of the three elements — e.g. expiry of rights, new agreements, changes in market conditions that affect de facto control.',
            'An investment entity obtains funds from investors to provide investment management services, commits to investors that its business purpose is investing solely for capital appreciation, investment income or both, and measures and evaluates performance of substantially all investments on a fair value basis.',
            'An investment entity measures its subsidiaries at FVTPL rather than consolidating them, except subsidiaries providing investment-related services. A non-investment-entity parent of an investment entity must consolidate all its subsidiaries, including those held through the investment entity.'],
          'Keep reassessing control; investment entities fair-value their subsidiaries.',
          'A venture capital fund may hold portfolio companies at fair value.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Control memo for a new investee', 'role': 'Technical accounting analyst',
             'situation': 'The company bought 40% of a start-up with board rights and options.',
             'steps': ['Identify relevant activities.', 'Assess votes, potential votes and contracts.', 'Assess exposure to variable returns.', 'Conclude on control and document.'],
             'takeaway': 'Control is judged on substance, not just shareholding.'}]

    mcqs = [
        Q('m1', 'Protective rights:', ['Do not give power', 'Always give power', 'Give joint control', 'Give significant influence'], 0,
          'They protect interests without directing activities. In practice: lender covenants.', 'c2', T2),
        Q('m2', 'Potential voting rights are considered when they are:', ['Substantive', 'Out of the money always', 'Held by anyone', 'Expired'], 0,
          'Practical ability to exercise is needed. In practice: check exercise price and timing.', 'c2', T2),
        Q('m3', 'A decision maker that is an agent:', ['Does not control the investee', 'Controls it', 'Has joint control', 'Consolidates proportionately'], 0,
          'It acts for others. In practice: fund managers.', 'c3', T3),
        Q('m4', 'An investment entity measures most subsidiaries at:', ['Fair value through profit or loss', 'Cost', 'Equity method', 'Consolidation'], 0,
          'Exception to consolidation. In practice: service subsidiaries still consolidated.', 'c4', T4),
        Q('m5', 'De facto control may arise when:', ['A large minority holder faces widely dispersed others', 'Holding is below 5%', 'There are two equal holders', 'Votes are not substantive'], 0,
          'Practical ability to direct. In practice: look at past voting.', 'c2', T2),
        Q('m6', 'Control must be reassessed:', ['When facts indicate a change in any element', 'Only annually', 'Only on acquisition', 'Never'], 0,
          'Continuous assessment. In practice: monitor agreements.', 'c4', T4),
        Q('m7', 'Which is a variable return?', ['Synergies and cost savings', 'Fixed rent from an unrelated party', 'Loan principal only', 'Statutory fees'], 0,
          'Returns can be broad. In practice: also fees and dividends.', 'c3', T3),
        Q('m8', 'A parent of an investment entity that is not itself an investment entity:', ['Consolidates all subsidiaries', 'Uses fair value', 'Uses equity method', 'Excludes them'], 0,
          'The exception does not roll up. In practice: consolidate underlying holdings.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Dispersion', 2, 'concept', 'dispers'), S('s2', 'Turnout', 1.5, 'concept', 'attendance|turnout'), S('s3', 'Conclusion', 1.5, 'concept', 'de facto|control')],
          ['Use voting history.'], ['Concluding no control below 50%.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 6, i2['q'], i2['solution'],
          [S('s1', 'Return', 2, 'computation', 'total return', nums=[exp]), S('s2', 'Removal rights', 2, 'concept', 'removal'), S('s3', 'Conclusion', 2, 'concept', 'principal')],
          ['Weigh all factors.'], ['Ignoring the 20% stake.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'State the three elements of control.', 'Power over the investee, exposure or rights to variable returns, and the ability to use power to affect those returns.',
          [P('p1', 'Power', 4, 'power'), P('p2', 'Variable returns and link', 6, 'variable|affect')], 'c2'),
        V('v2', 'What are relevant activities?', 'Activities of the investee that significantly affect its returns, such as operating, financing and budgeting decisions.',
          [P('p1', 'Significantly affect returns', 6, 'significantly'), P('p2', 'Examples', 4, 'operating|financing')], 'c2'),
        V('v3', 'What makes a decision maker an agent?', 'It acts mainly for others, often with limited authority, removable by others, market-based pay and small exposure to variability.',
          [P('p1', 'Acts for others', 5, 'others'), P('p2', 'Removable or small exposure', 5, 'remov|exposure')], 'c3'),
        V('v4', 'Define an investment entity.', 'An entity that obtains funds to provide investment management, invests solely for capital appreciation or income, and evaluates substantially all investments at fair value.',
          [P('p1', 'Investment purpose', 5, 'capital appreciation|income'), P('p2', 'Fair value evaluation', 5, 'fair value')], 'c4'),
        V('v5', 'When are potential voting rights considered?', 'When they are substantive — the holder has the practical ability to exercise them when decisions need to be made.',
          [P('p1', 'Substantive', 6, 'substantive'), P('p2', 'Practical ability', 4, 'practical')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Pegasus Ltd.', 'difficulty': 'moderate',
              'case': 'Pegasus Ltd. owns 40% of Titan Ltd. and holds call options, currently exercisable and deep in the money, to buy another 15%. Another investor holds 35% and a bank has veto rights over borrowings above ₹100 crore. Pegasus appoints the CEO and approves the budget.',
              'mcqs': [
                  M('k1a', 'Pegasus\'s potential voting interest including options (%):', ['55', '40', '15', '35'], 0,
                    '40 + 15 = 55 substantive. In practice: consider in assessing power.', 'core', check=55, topic=T2),
                  M('k1b', 'The bank\'s veto rights are:', ['Protective rights', 'Power', 'Joint control', 'Variable returns'], 0,
                    'They protect the lender. In practice: ignore for power.', 'core', topic=T2),
                  M('k1c', 'Pegasus most likely:', ['Controls Titan', 'Has significant influence only', 'Has joint control', 'Has no rights'], 0,
                    'Substantive options + budget and CEO rights. In practice: consolidate.', 'moderate', topic=T2),
                  M('k1d', 'If the options later expire unexercised, Pegasus must:', ['Reassess control', 'Do nothing', 'Restate prior years', 'Deconsolidate automatically'], 0,
                    'Change in facts triggers reassessment. In practice: may still have de facto control.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch13', 3, 'Consolidated Financial Statements',
                ['Apply the scope and exemptions of Ind AS 110.',
                 'Assess power through relevant activities and rights.',
                 'Evaluate variable returns and principal-agent relationships.',
                 'Reassess control and apply the investment entity exception.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['fin-p1-ch13-u02'],
                 'exam_tip': 'Write the three control elements as headings and conclude on each.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Control = power + variable returns + link.',
                             'Power from votes, contracts, de facto, potential votes.',
                             'Protective rights ignored.',
                             'Agents do not control.',
                             'Investment entities: FVTPL for subsidiaries.'],
                 'remember': ['Reassess when facts change.'],
                 'traps': ['Equating control with majority shareholding only.']},
                [('Control', 'Power + returns + link'), ('Protective rights', 'Not power'), ('Agent', 'No control'), ('Investment entity', 'FVTPL')],
                viva, cases)
