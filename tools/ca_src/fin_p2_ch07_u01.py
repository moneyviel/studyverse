"""CA Final · Paper 2 Advanced Financial Management · Chapter 7 Securitization.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p2-ch07-u01'
T1 = 'Concept, benefits and participants'
T2 = 'Mechanism of securitization'
T3 = 'Instruments, pricing and risks'
T4 = 'Problems, tokenization and the Indian framework'


def build():
    ck = Checks()
    spread = ck.add('100*(12-9-1)/100', 'Annual excess spread retained (₹ crore)')
    sen = ck.add('max(0,10-15)', 'Loss borne by senior PTC holders (₹ crore)')
    sub = ck.add('min(10,15)', 'Loss absorbed by the subordinated tranche (₹ crore)')
    i1 = {'id': 'i1', 'title': 'Excess spread and tranching', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Swift Finance pools ₹100 crore of vehicle loans yielding 12% and sells them to an SPV. The SPV issues senior PTCs of ₹85 crore and a subordinated tranche of ₹15 crore (retained by Swift). Investors receive 9%; servicing costs 1%. Compute the annual excess spread. If pool losses are ₹10 crore, who bears them?',
          'solution': [table(['Item', 'Working', '₹ crore'], [
              ['Excess spread', '100 × (12% − 9% − 1%)', inr(spread)],
              ['Loss absorbed by subordinated tranche', 'First-loss up to 15', inr(sub)],
              ['Loss to senior PTC holders', 'Loss 10 within cushion of 15', inr(sen)]], title='Credit enhancement')],
          'checks': list(ck)}

    ck2 = Checks()
    price = ck2.add('round(30/1.1+30/1.1**2+50/1.1**3,2)', 'Price of PTC at 10% (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Pricing a PTC', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'A pass-through certificate is expected to pay ₹30 lakh at the end of years 1 and 2 and ₹50 lakh at the end of year 3 (principal and interest from the pool). The investor requires 10%. What would they pay?',
          'solution': [table(['Year', 'Working', '₹ lakh'], [
              ['1', '30 ÷ 1.1', '27.27'], ['2', '30 ÷ 1.21', '24.79'], ['3', '50 ÷ 1.331', '37.57'],
              ['Price', 'Sum', inr(price)]], title='PV of expected pass-through flows')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Securitization converts illiquid assets with predictable cash flows (loans, receivables, rentals) into marketable securities. The originator sells the pool to a special purpose vehicle (SPV), which issues securities to investors backed by the pool\'s cash flows.',
            'Benefits to originators: off-balance sheet funding, better liquidity, lower funding cost via credit enhancement, risk transfer, improved capital ratios and specialised focus on origination. Benefits to investors: diversified, rated, often higher-yield instruments, matched maturities.',
            'Primary participants: originator, SPV, investors. Secondary participants: obligors (borrowers), rating agencies, servicers (collect payments), receiving and paying agents, credit enhancers, structurers and trustees.'],
          'Turn a pile of loans into tradable paper.',
          'A housing finance company securitises home loans to raise fresh funds.'),
        C('c2', T2, [
            'Steps: create a homogeneous pool of assets with similar features; transfer them to the SPV through a true sale (so they are bankruptcy-remote from the originator); the SPV issues and sells securities; a servicer (often the originator) administers the assets and collects cash; recourse to the originator is limited to agreed credit enhancement; investors are repaid from collections.',
            'Credit rating of the instruments depends on pool quality and credit enhancement (subordination, over-collateralisation, cash collateral, excess spread, guarantees).',
            'Tranching creates senior and subordinated classes so losses hit junior holders first.'],
          'Pool, sell, issue, service, repay — with credit support in between.',
          'A 15% subordinated tranche protects seniors from the first 15% of losses.'),
        C('c3', T3, [
            'Pass-through certificates (PTCs): investors receive pool cash flows as collected, including prepayments — reinvestment and prepayment risk sits with investors. Pay-through securities: the SPV restructures cash flows into bonds with different maturities, allowing tranches. Stripped securities separate interest-only (IO) and principal-only (PO) flows.',
            'Pricing: originators consider the cost versus other funding; investors value the expected cash flows (after prepayment and default assumptions) at a required yield, often referenced to benchmark yields plus a spread.',
            'Risks: credit or counterparty risk (borrower defaults, servicer failure), legal risk (true sale challenged), market risk — interest rate, prepayment, reinvestment and liquidity risks.'],
          'Who bears prepayment and default risk depends on the structure.',
          'Falling rates trigger prepayments, hurting PTC holders who must reinvest lower.'),
        C('c4', T4, [
            'Problems in India have included stamp duty on transfer of receivables, tax uncertainty on SPV income, accounting treatment (derecognition under Ind AS 109), lack of standardisation, a shallow debt market and slow foreclosure laws.',
            'Tokenization represents real-world assets (property, bonds, receivables) as digital tokens on a blockchain, enabling fractional ownership, faster settlement and wider access; it overlaps with securitization but adds technology and new risks (regulation, cyber security, smart contract errors).',
            'India\'s framework includes the SARFAESI Act, RBI directions on securitisation of standard assets (minimum holding and retention requirements), and SEBI regulations on listing of securitised debt instruments.'],
          'Regulation and technology are reshaping securitization.',
          'RBI rules require originators to retain part of the risk.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Structuring a deal', 'role': 'Structured finance analyst',
             'situation': 'An NBFC wants ₹500 crore by securitising gold loans.',
             'steps': ['Select a homogeneous pool and test its history.', 'Design tranches and credit enhancement.', 'Obtain rating and set pricing.', 'Check RBI retention and true sale requirements.'],
             'takeaway': 'Pool quality and enhancement drive the rating and the price.'}]

    mcqs = [
        Q('m1', 'In securitization, the originator transfers assets to:', ['A special purpose vehicle', 'The rating agency', 'Investors directly always', 'The RBI'], 0,
          'SPV isolates the assets. In practice: true sale.', 'c2', T2),
        Q('m2', 'In a pass-through certificate, prepayment risk is borne by:', ['Investors', 'The originator only', 'The rating agency', 'The government'], 0,
          'Cash flows pass straight through. In practice: reinvestment risk.', 'c3', T3),
        Q('m3', 'A subordinated tranche provides:', ['Credit enhancement to senior investors', 'Higher priority', 'No risk', 'Tax benefit'], 0,
          'Absorbs first losses. In practice: often retained by originator.', 'c2', T2),
        Q('m4', 'Stripped securities separate:', ['Interest and principal flows', 'Equity and debt', 'Tax and fees', 'Assets and liabilities'], 0,
          'IO and PO strips. In practice: different rate sensitivity.', 'c3', T3),
        Q('m5', 'A key benefit of securitization to the originator is:', ['Improved liquidity and funding', 'Higher taxes', 'More borrowers', 'Lower credit rating'], 0,
          'Converts loans into cash. In practice: reuse capital.', 'c1', T1),
        Q('m6', 'Tokenization uses:', ['Blockchain-based digital tokens to represent assets', 'Paper certificates', 'Cash only', 'Physical gold'], 0,
          'Fractional ownership. In practice: regulatory uncertainty.', 'c4', T4),
        Q('m7', 'The servicer\'s role is to:', ['Collect payments from obligors and pass them on', 'Rate the securities', 'Buy all securities', 'Set interest rates'], 0,
          'Administers the pool. In practice: often the originator.', 'c1', T1),
        Q('m8', 'A pay-through security allows:', ['Restructuring cash flows into tranches of different maturities', 'Only single maturity', 'Equity conversion', 'No credit rating'], 0,
          'SPV reshapes flows. In practice: investor choice.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Spread', 2, 'computation', 'excess spread', nums=[spread]), S('s2', 'Loss allocation', 3, 'computation', 'subordinated|senior', nums=[sub])],
          ['Show waterfall.'], ['Giving losses to seniors first.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Discounting', 2, 'concept', 'discount|present value'), S('s2', 'Price', 2, 'computation', 'price', nums=[price])],
          ['Discount each flow.'], ['Ignoring timing.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is securitization?', 'Converting a pool of illiquid assets with predictable cash flows into marketable securities issued through an SPV.',
          [P('p1', 'Pool of assets', 5, 'pool'), P('p2', 'Marketable securities via SPV', 5, 'spv|securities')], 'c1'),
        V('v2', 'Why must the transfer be a true sale?', 'So that the assets are bankruptcy-remote and investors are protected if the originator fails.',
          [P('p1', 'Bankruptcy-remote', 6, 'bankruptcy'), P('p2', 'Investors protected', 4, 'investor')], 'c2'),
        V('v3', 'Distinguish PTCs and pay-through securities.', 'PTCs pass collections directly to investors; pay-through securities restructure cash flows into tranches with different maturities.',
          [P('p1', 'Direct pass', 5, 'pass'), P('p2', 'Restructure tranches', 5, 'restructure|tranche')], 'c3'),
        V('v4', 'Name three risks in securitization.', 'Credit risk, legal risk and market risks such as prepayment, interest rate and reinvestment risk.',
          [P('p1', 'Credit and legal', 5, 'credit|legal'), P('p2', 'Market risks', 5, 'prepayment|interest|reinvestment')], 'c3'),
        V('v5', 'List two problems facing securitization in India.', 'Stamp duty on transfer of receivables and slow foreclosure laws, along with tax and accounting uncertainty.',
          [P('p1', 'Stamp duty', 5, 'stamp'), P('p2', 'Foreclosure or tax', 5, 'foreclosure|tax')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Pinnacle Housing Finance', 'difficulty': 'moderate',
              'case': 'Pinnacle Housing Finance securitises ₹400 crore of home loans yielding 10.5%. Senior PTCs of ₹340 crore pay 8%; the remainder is a subordinated tranche it retains. Servicing costs are 0.5% of the pool. Interest rates then fall sharply.',
              'mcqs': [
                  M('k1a', 'Size of the subordinated tranche (₹ crore):', ['60', '340', '400', '40'], 0,
                    '400 − 340. In practice: first-loss piece.', 'core', check=60, topic=T2),
                  M('k1b', 'Credit enhancement as a share of the pool (%):', ['15', '85', '10', '8'], 0,
                    '60 ÷ 400. In practice: higher enhancement, higher rating.', 'core', check=15, topic=T2),
                  M('k1c', 'Falling interest rates mainly raise:', ['Prepayment risk for PTC holders', 'Default risk', 'Stamp duty', 'Legal risk'], 0,
                    'Borrowers refinance. In practice: reinvestment at lower yields.', 'core', topic=T3),
                  M('k1d', 'The ₹340 crore senior PTCs suffer loss only if pool losses exceed (₹ crore):', ['60', '340', '0', '400'], 0,
                    'Subordination absorbs first. In practice: tranche cushion.', 'moderate', check=60, topic=T2),
              ]}]

    return unit(UID, 'p2', 'fin-p2-ch07', 1, 'Securitization',
                ['Explain securitization, its benefits and participants.',
                 'Describe the mechanism and credit enhancement.',
                 'Distinguish instruments, price them and identify risks.',
                 'Discuss problems, tokenization and the Indian framework.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 15}, 'prereq': ['fin-p2-ch06-u01'],
                 'exam_tip': 'Use the participants and mechanism lists to structure theory answers.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Pool → SPV → securities → investors.',
                             'True sale and bankruptcy remoteness.',
                             'PTC, pay-through, stripped securities.',
                             'Credit enhancement: subordination, excess spread, collateral.',
                             'Risks: credit, legal, market.'],
                 'remember': ['PTC holders bear prepayment risk.'],
                 'traps': ['Assuming seniors absorb first losses.']},
                [('PTC', 'Direct pass-through'), ('Pay-through', 'Restructured tranches'), ('IO/PO', 'Stripped'), ('Enhancement', 'Subordination')],
                viva, cases)
