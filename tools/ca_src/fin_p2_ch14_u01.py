"""CA Final · Paper 2 Advanced Financial Management · Chapter 14 Mergers, Acquisitions and Corporate Restructuring.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch14-u01'
T1 = 'Types of mergers and their rationale'
T2 = 'Synergy, exchange ratios and financial evaluation'
T3 = 'Takeover tactics, defences and reverse mergers'
T4 = 'Divestitures and financial and ownership restructuring'
T5 = 'Cross-border deals, SPACs and why M&A fails'


def build():
    ck = Checks()
    ratio = ck.add('round(50/150,4)', 'Exchange ratio by market price')
    issued = ck.add('round(4*50/150,4)', 'New shares issued (lakh)')
    eps = ck.add('round((100+20)/(10+4*50/150),2)', 'Post-merger EPS (₹)')
    maxr = ck.add('5/10', 'Maximum exchange ratio with no EPS dilution')
    i1 = {'id': 'i1', 'title': 'Share exchange ratio and EPS', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Acquirer A: earnings ₹100 lakh, 10 lakh shares, EPS ₹10, price ₹150. Target T: earnings ₹20 lakh, 4 lakh shares, EPS ₹5, price ₹50. (a) Compute the exchange ratio based on market prices, shares issued and post-merger EPS (no synergy). (b) What is the highest ratio A can offer without diluting its EPS?',
          'solution': [table(['Item', 'Working', 'Result'], [
              ['Exchange ratio', '50 ÷ 150', inr(ratio) + ' share of A per T share'],
              ['Shares issued', '4 lakh × 1/3', inr(issued) + ' lakh'],
              ['Post-merger EPS', '120 ÷ 11.3333', '₹' + inr(eps)],
              ['No-dilution ratio', 'EPS_T ÷ EPS_A = 5 ÷ 10', inr(maxr)]], title='Swap ratio')],
          'checks': list(ck)}

    ck2 = Checks()
    syn = ck2.add('1900-(1500+200)', 'Synergy (₹ crore)')
    prem = ck2.add('280-200', 'Premium paid (₹ crore)')
    npv = ck2.add('1900-(1500+200)-(280-200)', 'NPV to acquirer\'s shareholders (₹ crore)')
    i2 = {'id': 'i2', 'title': 'Who gains from the deal?', 'difficulty': 'core', 'minutes': 6,
          'q': 'A is worth ₹1,500 crore and T ₹200 crore as separate firms. Combined, they would be worth ₹1,900 crore. A pays ₹280 crore cash for T. Compute the synergy, premium, and the NPV of the deal to A\'s shareholders.',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Synergy', '1,900 − (1,500 + 200)', inr(syn)],
              ['Premium to T shareholders', '280 − 200', inr(prem)],
              ['NPV to A', '200 − 80', inr(npv)]], title='Gains split')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Mergers combine two firms into one (absorption or consolidation); acquisitions gain control through shares or assets. Types: horizontal (same industry and stage), vertical (supplier-customer chain, backward or forward), conglomerate (unrelated), congeneric (related but not same product) and reverse mergers.',
            'Rationale: synergy (operating economies, revenue gains, financial benefits like lower cost of capital or tax shields), market power, diversification, growth and capability acquisition, access to technology or markets, using surplus cash, and tax benefits such as carry-forward of losses under conditions.',
            'Legal frameworks in India include the Companies Act (schemes under NCLT), SEBI takeover regulations (SAST), the Competition Act and Income-tax Act provisions.'],
          'Mergers should make 2 + 2 = 5.',
          'A cement company buying a limestone mine is a vertical merger.'),
        C('c2', T2, [
            'Synergy = value of combined firm − (value of acquirer + value of target). Premium = price paid − target\'s standalone value. NPV to acquirer = synergy − premium; target shareholders gain the premium.',
            'Share exchange ratio can be based on EPS, market price, book value or intrinsic values. Post-merger EPS = combined earnings ÷ (acquirer\'s shares + new shares issued). Maximum ratio for acquirer (no EPS dilution) and minimum acceptable ratio for target (no loss to target holders) set the bargaining range; P/E of the combined firm also affects market price.',
            'Financial evaluation also considers cash versus share payment, funding of the acquisition (internal funds, debt, equity, LBO structures) and the impact on control and risk.'],
          'Pay less than the synergy, or the deal destroys value.',
          'Paying ₹80 crore premium for ₹200 crore synergy leaves ₹120 crore for the acquirer.'),
        C('c3', T3, [
            'Takeover strategies: street sweep (buying shares in the market), bear hug (offer so attractive the board must consider), strategic alliance, brand power, and tender/open offers to shareholders.',
            'Defensive tactics: poison pills (rights making takeover costly), golden parachutes, crown jewel sale, white knight (friendly bidder), white squire (friendly block holder), Pac-Man defence (counter-bid), greenmail (buying back the raider\'s stake at a premium), and changes in charter. Many are restricted under Indian law.',
            'A reverse merger occurs when a smaller (often unlisted or loss-making) company acquires a larger or listed one, or a healthy firm merges into a loss-making firm, to gain listing, tax losses or other benefits; conditions apply.'],
          'Raiders have strategies; boards have defences.',
          'Finding a friendlier buyer is a white knight defence.'),
        C('c4', T4, [
            'Divestitures sell or separate parts of a business: sell-off (sale of a division), spin-off (shares of a new company distributed to existing shareholders), split-up (company splits into several, parent ceases), equity carve-out (IPO of a minority stake in a subsidiary), and demergers (including family business separations).',
            'Financial restructuring reorganises the capital structure — reducing equity and debt claims, conversion of debt into equity, reduction of capital, typically to wipe out accumulated losses and restore viability, with sacrifices shared by stakeholders.',
            'Ownership restructuring: going private (delisting), management buy-outs (managers buy the business), leveraged buy-outs (financed largely by debt secured on target assets), and buy-backs (returning cash, signalling undervaluation, raising EPS).'],
          'Sometimes value comes from getting smaller.',
          'A spin-off gives shareholders shares in the separated business.'),
        C('c5', T5, [
            'Value can be unlocked through M&A when markets misprice parts of a group; control premiums and minority discounts and marketability discounts adjust values.',
            'Cross-border M&A brings access to markets, technology and brands, but adds currency, regulatory, tax, political and cultural risks.',
            'SPACs (special purpose acquisition companies) raise money via IPO to acquire an unidentified private company within a set period, offering a faster route to listing. M&A failures stem from overpaying, poor due diligence, cultural clashes, integration problems and overestimated synergies.'],
          'Global and creative deals carry extra risks — integration is where most fail.',
          'An overpaid acquisition with clashing cultures often destroys value.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Advising on a share-swap merger', 'role': 'M&A analyst',
             'situation': 'Two listed firms in the same industry plan a share-swap merger.',
             'steps': ['Estimate standalone values and synergy.', 'Compute swap ratio range on EPS and market price.', 'Model post-merger EPS and price.', 'Check SEBI, Companies Act and Competition Act requirements.'],
             'takeaway': 'The swap ratio decides who captures the synergy.'}]

    mcqs = [
        Q('m1', 'A merger between firms at different stages of the same supply chain is:', ['Vertical', 'Horizontal', 'Conglomerate', 'Reverse'], 0,
          'Backward or forward integration. In practice: control of inputs.', 'c1', T1),
        Q('m2', 'NPV of an acquisition to the acquirer equals:', ['Synergy − premium', 'Premium − synergy', 'Price paid', 'Target value'], 0,
          'Gains shared. In practice: avoid overpaying.', 'c2', T2),
        Q('m3', 'Post-merger EPS equals:', ['Combined earnings ÷ total shares after issue', 'Acquirer EPS + target EPS', 'Target EPS × ratio', 'Price ÷ earnings'], 0,
          'Weighted by new share count. In practice: check dilution.', 'c2', T2),
        Q('m4', 'A white knight is:', ['A friendly bidder invited to rescue the target', 'A hostile raider', 'A regulator', 'An auditor'], 0,
          'Defensive tactic. In practice: preferred acquirer.', 'c3', T3),
        Q('m5', 'In a spin-off:', ['Shares of the new company are distributed to existing shareholders', 'The division is sold for cash', 'The company goes private', 'Debt is converted to equity'], 0,
          'No cash changes hands. In practice: focus.', 'c4', T4),
        Q('m6', 'An LBO is financed mainly by:', ['Debt secured on the target\'s assets and cash flows', 'New equity only', 'Government grants', 'Retained earnings'], 0,
          'High leverage. In practice: repaid from target cash.', 'c4', T4),
        Q('m7', 'A SPAC:', ['Raises IPO money to acquire a private company later', 'Is a mutual fund', 'Is a bank', 'Is a sovereign fund'], 0,
          'Blank-cheque company. In practice: time-bound.', 'c5', T5),
        Q('m8', 'A common cause of M&A failure is:', ['Overpaying and poor integration', 'Too much due diligence', 'Low premiums', 'Strong cultural fit'], 0,
          'Winner\'s curse. In practice: realistic synergies.', 'c5', T5),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Ratio', 2, 'computation', 'ratio', nums=[ratio]), S('s2', 'Shares', 2, 'computation', 'shares', nums=[issued]), S('s3', 'EPS', 2, 'computation', 'eps', nums=[eps]), S('s4', 'Maximum', 2, 'computation', 'dilution|maximum', nums=[maxr])],
          ['Show bargaining range.'], ['Adding EPS figures.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Synergy', 1.5, 'computation', 'synergy', nums=[syn]), S('s2', 'Premium', 1, 'computation', 'premium', nums=[prem]), S('s3', 'NPV', 1.5, 'computation', 'npv', nums=[npv])],
          ['Split gains.'], ['Treating premium as gain to acquirer.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is synergy?', 'The extra value created when two firms combine, beyond the sum of their separate values.',
          [P('p1', 'Extra value', 5, 'extra'), P('p2', 'Sum of separate values', 5, 'separate')], 'c2'),
        V('v2', 'Name four types of mergers.', 'Horizontal, vertical, conglomerate and congeneric mergers.',
          [P('p1', 'Horizontal and vertical', 5, 'horizontal|vertical'), P('p2', 'Conglomerate and congeneric', 5, 'conglomerate|congeneric')], 'c1'),
        V('v3', 'What is a poison pill?', 'A defence giving existing shareholders rights that make a hostile takeover very costly to the raider.',
          [P('p1', 'Rights to shareholders', 5, 'rights'), P('p2', 'Costly takeover', 5, 'costly')], 'c3'),
        V('v4', 'Distinguish spin-off and equity carve-out.', 'A spin-off distributes shares of the unit to existing shareholders; a carve-out sells a minority stake in the unit to the public through an IPO.',
          [P('p1', 'Distribute shares', 5, 'distribut'), P('p2', 'IPO of minority stake', 5, 'ipo')], 'c4'),
        V('v5', 'What is a reverse merger?', 'A merger in which a smaller or loss-making company effectively takes over a larger or healthy one, often to gain listing or tax benefits.',
          [P('p1', 'Smaller acquires larger', 5, 'smaller'), P('p2', 'Listing or tax benefits', 5, 'listing|tax')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Kaveri–Narmada merger', 'difficulty': 'moderate',
              'case': 'Kaveri Ltd. (earnings ₹60 crore, 6 crore shares, P/E 20) plans to acquire Narmada Ltd. (earnings ₹20 crore, 4 crore shares, P/E 12) by issuing shares. Synergy will raise combined earnings by ₹5 crore. The combined P/E is expected to be 18.',
              'mcqs': [
                  M('k1a', 'Narmada\'s market price per share (₹):', ['60', '200', '100', '50'], 0,
                    'EPS 5 × P/E 12. In practice: Kaveri price is 200.', 'core', check=60, topic=T2),
                  M('k1b', 'Exchange ratio on market prices:', ['0.3', '0.5', '3.33', '0.25'], 0,
                    '60 ÷ 200. In practice: 1.2 crore new shares.', 'core', check=0.3, topic=T2),
                  M('k1c', 'Post-merger EPS with synergy (₹, two decimals):', ['11.81', '10', '8.5', '12.5'], 0,
                    '(60 + 20 + 5) ÷ (6 + 1.2) crore shares. In practice: EPS accretion for Kaveri.', 'moderate', check=11.81, topic=T2),
                  M('k1d', 'Expected post-merger share price at P/E 18 (₹, one decimal):', ['212.5', '200', '180', '240'], 0,
                    '(85 ÷ 7.2) × 18 = 212.5. In practice: gain for both.', 'moderate', check=212.5, topic=T2),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch14', 1, 'Mergers, Acquisitions and Corporate Restructuring',
                ['Classify mergers and explain their rationale.',
                 'Compute synergy, premiums, exchange ratios and post-merger EPS.',
                 'Describe takeover tactics, defences and reverse mergers.',
                 'Explain divestitures and financial and ownership restructuring.',
                 'Discuss cross-border deals, SPACs and M&A failures.'],
                {'difficulty': 'hard', 'minutes': {'learn': 45, 'practice': 45}, 'prereq': ['fin-p2-ch13-u01'],
                 'exam_tip': 'For swap-ratio sums, compute the acquirer\'s maximum and target\'s minimum ratios to show the bargaining range.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Horizontal, vertical, conglomerate, congeneric, reverse.',
                             'Synergy − premium = acquirer NPV.',
                             'Swap ratio on EPS, MPS, BV or intrinsic value.',
                             'Defences: poison pill, white knight, Pac-Man, crown jewel.',
                             'Spin-off, split-up, carve-out; LBO, MBO, buy-back.'],
                 'remember': ['Post-merger EPS = combined earnings ÷ total shares.'],
                 'traps': ['Adding EPS figures instead of earnings.']},
                [('Synergy', 'VAT − (VA + VT)'), ('NPV to acquirer', 'Synergy − premium'), ('Max ratio (no dilution)', 'EPS_T ÷ EPS_A'), ('LBO', 'Debt-funded')],
                viva, cases)
