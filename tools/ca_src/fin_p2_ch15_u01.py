"""CA Final · Paper 2 Advanced Financial Management · Chapter 15 Startup Finance.
Scope follows the ICAI study material (updated for the DPIIT startup framework notified 4 February 2026); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch15-u01'
T1 = 'Startup financing basics and innovative sources'
T2 = 'Pitch presentation and unicorns'
T3 = 'Bootstrapping, angels and venture capital'
T4 = 'Startup India framework and succession planning'


def build():
    ck = Checks()
    post = ck.add('4+1', 'Post-money value after angel round (₹ crore)')
    stake = ck.add('1/(4+1)*100', 'Angel\'s stake (%)')
    newsh = ck.add('10*0.2/0.8', 'New shares issued to angel (lakh)')
    price = ck.add('100/(10*0.2/0.8)', 'Price per share in angel round (₹)')
    founders = ck.add('round(0.8*(20/(20+5))*100,2)', 'Founders\' stake after Series A (%)')
    i1 = {'id': 'i1', 'title': 'Dilution across rounds', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Founders of Leaf Labs own all 10 lakh shares. An angel invests ₹1 crore at a pre-money value of ₹4 crore. Later, a VC invests ₹5 crore at a pre-money value of ₹20 crore. Compute post-money value and angel stake, new shares and price in the angel round, and the founders\' stake after Series A.',
          'solution': [table(['Step', 'Working', 'Result'], [
              ['Post-money (angel round)', '4 + 1', '₹' + inr(post) + ' crore'],
              ['Angel stake', '1 ÷ 5', inr(stake) + '%'],
              ['New shares', '10 lakh × 20/80', inr(newsh) + ' lakh'],
              ['Price per share', '₹1 crore ÷ 2.5 lakh', '₹' + inr(price)],
              ['Founders after Series A', '80% × 20/25', inr(founders) + '%']], title='Pre-money, post-money, dilution')],
          'checks': list(ck)}

    ck2 = Checks()
    run = ck2.add('600/50', 'Cash runway (months)')
    i2 = {'id': 'i2', 'title': 'Burn rate and runway', 'difficulty': 'core', 'minutes': 5,
          'q': 'Leaf Labs has ₹6 crore cash and a net monthly burn of ₹50 lakh. How many months of runway does it have, and when should it start raising the next round if fund-raising takes about six months?',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Runway', '600 ÷ 50 (₹ lakh)', inr(run) + ' months'],
              ['Start raising', '12 − 6', 'Within the next 6 months — ideally now']], title='Runway')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Startups need money for product development, market entry and scaling, usually before profits. Early funding comes mostly from founders\' savings, family and friends, then angels, venture capital and later private equity or IPOs.',
            'Innovative sources include crowdfunding, startup incubators and accelerators, government grants and seed funds, bank and Mudra loans, revenue-based financing, and selling or licensing intellectual property.',
            'Key metrics: burn rate (monthly cash spent), runway (cash ÷ net burn), customer acquisition cost, lifetime value and unit economics. Valuation at each round sets pre-money and post-money values, which drive dilution.'],
          'Startups buy time with money — runway is life.',
          'Six crore of cash burning fifty lakh a month lasts a year.'),
        C('c2', T2, [
            'A pitch presentation sells the business to investors: problem, solution, market size, business model, traction, competition, team, financials and funding ask, and use of funds. It should be concise, evidence-based and honest about risks.',
            'Investors look for a large addressable market, a capable team, product-market fit, scalable unit economics and a clear path to exit.',
            'A unicorn is a privately held startup valued at USD 1 billion or more; India has one of the largest unicorn populations, though valuations can fall sharply when funding conditions tighten.'],
          'Tell a clear story backed by numbers.',
          'A fintech reaching a USD 1 billion valuation before listing becomes a unicorn.'),
        C('c3', T3, [
            'Bootstrapping uses personal savings and internal cash flows (sweat equity, customer advances, lean operations) — keeps control but limits growth speed.',
            'Angel investors are wealthy individuals or networks investing early in exchange for equity or convertibles, often adding mentoring and contacts.',
            'Venture capital funds invest in high-growth startups in stages (seed, early, growth), taking equity, board seats and protective rights. VC process: deal origination, screening, due diligence, valuation and term sheet, structuring, post-investment monitoring and exit (IPO, strategic sale, secondary sale, buy-back). In India, VC funds are usually trusts or companies registered as Alternative Investment Funds (Category I) with SEBI.'],
          'Each funding stage trades ownership for growth.',
          'A Series A investor typically takes a board seat and minority protections.'),
        C('c4', T4, [
            'Startup India (launched 16 January 2016) supports startups through recognition, tax and compliance benefits, funds of funds via SIDBI, the Startup India Seed Fund Scheme and credit guarantees.',
            'Under the DPIIT framework notified on 4 February 2026 (replacing the 2019 rules covered in the ICAI material), a startup must be up to 10 years old with turnover not exceeding ₹200 crore in any year (previously ₹100 crore); a new Deep Tech Startup category allows up to 20 years and ₹300 crore; cooperatives are now eligible; entities formed by splitting or reconstructing an existing business are excluded. The section 80-IAC tax holiday has its own conditions, and angel tax has been abolished.',
            'Succession planning identifies and develops future leaders and plans ownership transfer for family and founder-led businesses — through family governance, wills and trusts, management development or sale — overcoming challenges such as family conflict, lack of capable successors and tax issues.'],
          'Government support helps; planning for the next leader keeps the business alive.',
          'A five-year-old company with ₹150 crore turnover still qualifies as a startup under the 2026 rules.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Preparing for a Series A raise', 'role': 'Startup CFO',
             'situation': 'A SaaS startup with 14 months of runway plans its first VC round.',
             'steps': ['Prepare metrics: burn, runway, CAC, LTV, growth.', 'Build the pitch deck and financial model.', 'Negotiate valuation and dilution in the term sheet.', 'Check DPIIT recognition and tax benefits.'],
             'takeaway': 'Raise before you need to, with numbers investors trust.'}]

    mcqs = [
        Q('m1', 'Post-money valuation equals:', ['Pre-money valuation + new investment', 'Pre-money − investment', 'Investment ÷ stake', 'Revenue × 10'], 0,
          'Basis for ownership. In practice: investor stake = investment ÷ post-money.', 'c1', T1),
        Q('m2', 'Runway is:', ['Cash ÷ net monthly burn', 'Revenue ÷ costs', 'Profit × months', 'Burn × cash'], 0,
          'Months until cash runs out. In practice: raise early.', 'c1', T1),
        Q('m3', 'A unicorn is a startup valued at:', ['USD 1 billion or more', 'USD 100 million', 'INR 100 crore', 'USD 10 billion only'], 0,
          'Privately held. In practice: decacorn is USD 10 billion.', 'c2', T2),
        Q('m4', 'Bootstrapping means:', ['Funding from founders\' own resources and internal cash', 'Raising VC money', 'Bank loans only', 'An IPO'], 0,
          'Keeps control. In practice: slower growth.', 'c3', T3),
        Q('m5', 'Venture capital funds in India are typically registered with SEBI as:', ['Alternative Investment Funds', 'Mutual funds', 'NBFCs', 'Banks'], 0,
          'Category I AIFs. In practice: trusts or companies.', 'c3', T3),
        Q('m6', 'Under the DPIIT framework of February 2026, the general startup turnover ceiling is:', ['₹200 crore', '₹100 crore', '₹50 crore', '₹25 crore'], 0,
          'Raised from ₹100 crore; deep tech ₹300 crore. In practice: verify current notifications.', 'c4', T4, check=200),
        Q('m7', 'An entity formed by splitting an existing business:', ['Is not a startup', 'Is always a startup', 'Is a deep tech startup', 'Gets tax holiday automatically'], 0,
          'Excluded by definition. In practice: genuine new ventures only.', 'c4', T4),
        Q('m8', 'Succession planning mainly aims to:', ['Ensure leadership and ownership continuity', 'Raise VC money', 'Reduce taxes only', 'Increase burn rate'], 0,
          'Business continuity. In practice: family businesses.', 'c4', T4),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Post-money and stake', 2, 'computation', 'post-money|stake', nums=[post, stake]), S('s2', 'Shares and price', 2.5, 'computation', 'shares|price', nums=[newsh, price]), S('s3', 'Founders', 2.5, 'computation', 'founders', nums=[founders])],
          ['Show each round.'], ['Using pre-money for stake.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 3, i2['q'], i2['solution'],
          [S('s1', 'Runway', 2, 'computation', 'runway', nums=[run]), S('s2', 'Timing', 1, 'concept', 'raising|now')],
          ['Allow fund-raising time.'], ['Waiting until cash runs out.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a pitch presentation?', 'A short presentation to investors covering problem, solution, market, business model, traction, team, financials and the funding ask.',
          [P('p1', 'Problem and solution', 5, 'problem|solution'), P('p2', 'Funding ask', 5, 'funding|ask')], 'c2'),
        V('v2', 'Describe the VC investment process.', 'Deal origination, screening, due diligence, valuation and term sheet, structuring, monitoring and exit.',
          [P('p1', 'Screening and diligence', 5, 'screening|diligence'), P('p2', 'Monitoring and exit', 5, 'monitor|exit')], 'c3'),
        V('v3', 'What are the current DPIIT startup criteria?', 'Up to 10 years from incorporation with turnover up to ₹200 crore in any year, or 20 years and ₹300 crore for deep tech startups, and not formed by splitting an existing business.',
          [P('p1', 'Age and turnover', 5, 'turnover'), P('p2', 'Deep tech limits', 5, 'deep tech')], 'c4'),
        V('v4', 'Name three innovative ways to finance a startup.', 'Crowdfunding, incubators and accelerators, and government seed funds or grants.',
          [P('p1', 'Crowdfunding', 5, 'crowdfunding'), P('p2', 'Incubators or grants', 5, 'incubator|grant|seed')], 'c1'),
        V('v5', 'Why is succession planning challenging?', 'Because of family conflicts, lack of capable successors, emotional attachment and tax or legal complexity.',
          [P('p1', 'Family conflict', 5, 'family'), P('p2', 'Successors', 5, 'successor')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'GreenGrid Energy Tech', 'difficulty': 'moderate',
              'case': 'GreenGrid, a 12-year-old company developing grid battery technology recognised as deep tech, has turnover of ₹250 crore. It seeks ₹40 crore at a pre-money value of ₹160 crore. Founders currently own 70%.',
              'mcqs': [
                  M('k1a', 'Post-money value (₹ crore):', ['200', '160', '120', '240'], 0,
                    '160 + 40. In practice: basis for stake.', 'core', check=200, topic=T1),
                  M('k1b', 'Investor\'s stake (%):', ['20', '25', '40', '16'], 0,
                    '40 ÷ 200. In practice: dilutes everyone.', 'core', check=20, topic=T1),
                  M('k1c', 'Founders\' stake after the round (%):', ['56', '70', '50', '60'], 0,
                    '70 × 80%. In practice: proportional dilution.', 'core', check=56, topic=T3),
                  M('k1d', 'Can GreenGrid still be a recognised startup?', ['Yes, as a deep tech startup (within 20 years and ₹300 crore)', 'No, over 10 years old', 'No, turnover above ₹200 crore', 'Only if a cooperative'], 0,
                    'Deep tech limits apply under the 2026 framework. In practice: recognition needed.', 'moderate', topic=T4),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch15', 1, 'Startup Finance',
                ['Explain startup financing needs and innovative sources.',
                 'Prepare a pitch and explain unicorns.',
                 'Compare bootstrapping, angels and venture capital and compute dilution.',
                 'Apply the Startup India framework and explain succession planning.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 20}, 'prereq': ['fin-p2-ch14-u01'],
                 'exam_tip': 'Dilution sums: stake = investment ÷ post-money; earlier holders shrink proportionately.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Post-money = pre-money + investment.',
                             'Runway = cash ÷ net burn.',
                             'Bootstrapping → angels → VC → PE/IPO.',
                             'Startup: ≤10 years, ≤₹200 crore (deep tech ≤20 years, ≤₹300 crore) from Feb 2026.',
                             'Succession planning for continuity.'],
                 'remember': ['ICAI text shows the older ₹100 crore limit; the 2026 notification raised it.'],
                 'traps': ['Computing stake on pre-money value.']},
                [('Post-money', 'Pre + investment'), ('Stake', 'Investment ÷ post'), ('Runway', 'Cash ÷ burn'), ('Startup limit (2026)', '10 yrs, ₹200 cr')],
                viva, cases)
