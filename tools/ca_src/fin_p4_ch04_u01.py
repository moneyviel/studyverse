"""CA Final · Paper 4 · Chapter 4 Capital Gains.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch04-u01'
T1 = 'Capital asset, transfer and period of holding'
T2 = 'Computation of capital gains'
T3 = 'Special cases: depreciable assets, slump sale, firms'
T4 = 'Exemptions from capital gains'
T5 = 'Rates of tax on capital gains'


def build():
    ck = Checks()
    a = ck.add('(12000000-2500000)*0.125', 'A: tax without indexation at 12.5% (₹)')
    ic = ck.add('round(2500000*384/117)', 'Indexed cost of acquisition (₹)')
    b = ck.add('round((12000000-round(2500000*384/117))*0.20)', 'B: tax with indexation at 20% (₹)')
    e = ck.add('(12000000-2500000)*0.125-round((12000000-round(2500000*384/117))*0.20)', 'E: excess ignored (₹)')
    i1 = {'id': 'i1', 'title': 'Land bought before 23 July 2024', 'difficulty': 'moderate', 'minutes': 9,
          'q': 'Nandini, a resident individual, bought a plot in F.Y. 2005-06 (CII 117) for ₹25,00,000 and sold it in T.Y. 2026-27 (CII 384) for ₹1,20,00,000. Her other income exceeds the basic exemption limit. Compute tax on the long-term capital gain (before cess).',
          'solution': [table(['Step', 'Working', '₹'], [
              ['LTCG without indexation', '1,20,00,000 − 25,00,000 = 95,00,000', '—'],
              ['A: tax @ 12.5%', '95,00,000 × 12.5%', inr(a)],
              ['Indexed cost', '25,00,000 × 384/117', inr(ic)],
              ['B: tax @ 20% on indexed gain', '(1,20,00,000 − indexed cost) × 20%', inr(b)],
              ['E = A − B (ignored)', '', inr(e)],
              ['Tax payable', 'Equal to B', inr(b)]], title='Section 197 grandfathering')],
          'checks': list(ck)}

    c2 = Checks()
    s82 = c2.add('min(22000000,30000000,100000000)', 'Exemption under section 82 (₹)')
    s85 = c2.add('min(5000000,30000000-22000000)', 'Exemption under section 85 (₹)')
    tx = c2.add('30000000-22000000-5000000', 'Taxable LTCG (₹)')
    i2 = {'id': 'i2', 'title': 'Reinvesting gains from a house', 'difficulty': 'core', 'minutes': 6,
          'q': 'Karan, a resident individual, earns LTCG of ₹3,00,00,000 on selling a residential house in August 2026. He buys one new house in India for ₹2,20,00,000 in January 2027 and invests ₹50,00,000 in long-term specified bonds within six months of the sale. Compute the taxable LTCG.',
          'solution': [table(['Item', 'Working', '₹'], [
              ['Section 82', 'Lower of gain and cost of new house (cap ₹10 crore)', inr(s82)],
              ['Section 85', 'Bonds, within ₹50 lakh limit', inr(s85)],
              ['Taxable LTCG', '3,00,00,000 − 2,20,00,000 − 50,00,000', inr(tx)]], title='Exemptions')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'A capital asset under section 2(22) is property of any kind held by the assessee, plus securities held by FPIs and specified ULIPs, but excludes stock-in-trade, personal effects (other than jewellery, archaeological collections, drawings, paintings, sculptures and works of art), rural agricultural land, and specified gold bonds and deposit schemes.',
            'Period of holding: listed securities, UTI units, equity-oriented fund units and zero coupon bonds are short-term if held for up to 12 months; other assets for up to 24 months. Holding periods of previous owners are included where the asset was acquired by gift, will, inheritance, amalgamation, demerger and similar modes.',
            'Section 67 charges gains on transfer; section 70 lists transactions not regarded as transfer — e.g. distribution on partition of a HUF, gifts and wills, transfers between a holding company and its wholly-owned Indian subsidiary, amalgamations and demergers meeting conditions, conversion of companies into LLPs meeting conditions, reverse mortgages and conversion of gold into electronic gold receipts.'],
          'Identify the asset, then the holding period, then whether there was a transfer.',
          'Listed shares held for 11 months give short-term gains.'),
        C('c2', T2, [
            'Section 72: capital gain = full value of consideration − expenditure on transfer − cost of acquisition − cost of improvement. Indexation is not allowed when computing income under this head.',
            'For land or building acquired before 23 July 2024 by a resident individual or HUF, tax on the gain is the lower of 12.5% without indexation and 20% with indexation (the excess E = A − B is ignored). Indexed cost uses the CII of the transfer year (384 for 2026-27) over the CII of the first year held or 2001-02, whichever is later.',
            'Section 90 deals with cost: FMV on 1 April 2001 (capped at stamp duty value for land and buildings) may be taken for assets acquired before that date; self-generated assets like goodwill and certain rights have nil cost unless purchased; bonus shares allotted after 1 April 2001 have nil cost. Stamp duty value is deemed consideration for land and buildings, subject to tolerance.'],
          'Sale price minus costs; old property gets a lower-of comparison.',
          'Land bought in 2005-06 for ₹25 lakh and sold for ₹1.2 crore gives tax of about ₹7.59 lakh using indexation.'),
        C('c3', T3, [
            'Depreciable assets (section 74): gains on transfer from a block are always short-term — where sale proceeds exceed opening WDV plus additions, or the block ceases to exist.',
            'Slump sale (section 77): transfer of an undertaking for a lump sum without values for individual assets. Net worth is cost; FMV of the undertaking is deemed consideration; gains are short-term if the undertaking was held for 36 months or less, and a CA report is required.',
            'Firms and partners: when a firm distributes a capital asset to a partner on reconstitution or dissolution, its FMV is the firm\'s consideration (section 67(10) and section 8); gains on excess payments to a retiring partner are taxed in the firm and attributed to remaining assets. Assets introduced by a partner as capital contribution are valued at the amount credited to his capital account.'],
          'Special rules override the general formula.',
          'Selling a whole division for a single price is a slump sale.'),
        C('c4', T4, [
            'Section 82: LTCG on a residential house is exempt if invested in one house in India bought one year before or two years after, or built within three years; if gains do not exceed ₹2 crore, the assessee may once in a lifetime invest in two houses. The exemption is capped at ₹10 crore.',
            'Section 85: LTCG on land or buildings invested within six months in long-term specified bonds is exempt up to ₹50 lakh across years. Section 86: LTCG on any other asset is exempt proportionately when net consideration is invested in a residential house (subject to owning no more than one other house), capped at ₹10 crore. Section 83 covers agricultural land replaced by agricultural land.',
            'Amounts not invested before the return date must be deposited in the Capital Gains Accounts Scheme by the due date. Selling the new asset within three years withdraws the exemption.'],
          'Reinvest in the right asset, within the window, up to the cap.',
          'A ₹3 crore gain reinvested ₹2.2 crore in a house and ₹50 lakh in bonds leaves ₹30 lakh taxable.'),
        C('c5', T5, [
            'Section 196: STCG on STT-paid listed equity shares, equity-oriented fund units and business trust units is taxed at 20%. Other STCG is taxed at slab rates.',
            'Section 198: LTCG on such equity shares (STT paid on acquisition and transfer, with notified exceptions) and fund/business trust units (STT on transfer) above ₹1,25,000 is taxed at 12.5%. Section 197: other LTCG at 12.5%, with the indexation comparison for old land and buildings.',
            'Resident individuals and HUFs may adjust unexhausted basic exemption limit against such gains; Chapter VIII deductions cannot be set against them.'],
          '20% for short-term listed equity; 12.5% for long-term above ₹1.25 lakh.',
          'LTCG of ₹4 lakh on listed shares gives tax of ₹34,375 before cess.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Property sale advisory', 'role': 'Tax consultant',
             'situation': 'A client plans to sell an inherited flat and buy a new home.',
             'steps': ['Determine cost and holding using previous owner.', 'Compare indexed and non-indexed tax.', 'Plan section 82 and 85 reinvestment.', 'Advise on CGAS if purchase is delayed.'],
             'takeaway': 'Timing of reinvestment decides the exemption.'}]

    mcqs = [
        Q('m1', 'Land held for 20 months before transfer is:', ['A short-term capital asset', 'A long-term capital asset', 'Stock-in-trade', 'Not a capital asset'], 0,
          'Needs more than 24 months. In practice: count from acquisition.', 'c1', T1),
        Q('m2', 'Which is NOT a transfer under section 70?', ['Sale of shares on a stock exchange', 'Gift of shares to a son', 'Distribution on HUF partition', 'Transfer to wholly-owned Indian subsidiary'], 0,
          'Sale is a transfer. In practice: check exceptions.', 'c1', T1),
        Q('m3', 'Cost inflation index for F.Y. 2026-27 is:', ['384', '376', '363', '348'], 0,
          'Notified index. In practice: only for old land and buildings.', 'c2', T2, check=384),
        Q('m4', 'Gain on transfer of a depreciable asset from a block is:', ['Always short-term', 'Always long-term', 'Exempt', 'Business income'], 0,
          'Section 74. In practice: block concept.', 'c3', T3),
        Q('m5', 'Slump sale gains are short-term if the undertaking was held for:', ['Thirty-six months or less', 'Twelve months or less', 'Twenty-four months or less', 'Sixty months or less'], 0,
          'Section 77. In practice: CA report needed.', 'c3', T3),
        Q('m6', 'Maximum exemption under section 82 is:', ['Ten crore rupees', 'Two crore rupees', 'Fifty lakh rupees', 'Unlimited'], 0,
          'Cap on cost of new house. In practice: excess taxable.', 'c4', T4),
        Q('m7', 'STCG on STT-paid listed equity shares is taxed at:', ['Twenty percent', 'Fifteen percent', 'Slab rates', 'Twelve and a half percent'], 0,
          'Section 196. In practice: no Chapter VIII deduction.', 'c5', T5),
        Q('m8', 'LTCG on listed equity is taxable only above:', ['One lakh twenty-five thousand rupees', 'One lakh rupees', 'Two lakh rupees', 'Nil'], 0,
          'Section 198. In practice: aggregate per year.', 'c5', T5),
    ]

    questions = [
        W('q1', 7, i1['q'], i1['solution'],
          [S('s1', 'Tax without indexation', 2, 'computation', 'without', nums=[a]), S('s2', 'Indexed computation', 3, 'computation', 'indexed', nums=[ic, b]), S('s3', 'Conclusion', 2, 'judgement', 'lower', nums=[e])],
          ['State E = A − B.'], ['Including indexed gain in gross total income.'], ['Show both.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Section 82', 2.5, 'computation', 'house', nums=[s82]), S('s2', 'Section 85 and taxable gain', 2.5, 'computation', 'bonds', nums=[s85, tx])],
          ['Mention time limits.'], ['Exceeding the ₹50 lakh bond cap.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'How is indexation used for land acquired before 23 July 2024?', 'For resident individuals and HUFs, tax is the lower of 12.5% on unindexed gain and 20% on indexed gain, ignoring the excess.',
          [P('p1', 'Twelve and a half percent', 5, '12.5'), P('p2', 'Twenty percent indexed', 5, '20%')], 'c2'),
        V('v2', 'What is a slump sale?', 'Transfer of an undertaking for a lump sum consideration without assigning values to individual assets and liabilities.',
          [P('p1', 'Lump sum', 5, 'lump sum'), P('p2', 'Undertaking', 5, 'undertaking')], 'c3'),
        V('v3', 'When can two houses be bought under section 82?', 'When the long-term gain is up to ₹2 crore, at the assessee\'s option, once in a lifetime.',
          [P('p1', 'Two crore', 5, '2 crore'), P('p2', 'Once', 5, 'once')], 'c4'),
        V('v4', 'What is the time limit for section 85 bonds?', 'Six months from the date of transfer, with a limit of ₹50 lakh.',
          [P('p1', 'Six months', 5, 'six months'), P('p2', 'Fifty lakh', 5, '50 lakh')], 'c4'),
        V('v5', 'Can Chapter VIII deductions be set against LTCG?', 'Chapter VIII deductions are barred against such gains; only the unexhausted basic exemption limit of residents is adjustable.',
          [P('p1', 'Barred', 5, 'barred'), P('p2', 'Basic exemption', 5, 'basic exemption')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'Tanvi\'s portfolio', 'difficulty': 'core',
              'case': 'Tanvi, a resident with salary well above the basic exemption limit, sells STT-paid listed shares in T.Y. 2026-27: LTCG of ₹4,00,000 and STCG of ₹2,00,000.',
              'mcqs': [
                  M('k1a', 'Taxable LTCG after the threshold (₹):', ['2,75,000', '4,00,000', '3,00,000', '1,25,000'], 0,
                    '4,00,000 − 1,25,000. In practice: section 198.', 'core', check=275000, topic=T5),
                  M('k1b', 'Tax on LTCG (₹):', ['34,375', '50,000', '27,500', '55,000'], 0,
                    '12.5% × 2,75,000. In practice: plus cess.', 'core', check=34375, topic=T5),
                  M('k1c', 'Tax on STCG (₹):', ['40,000', '30,000', '25,000', '60,000'], 0,
                    '20% × 2,00,000. In practice: section 196.', 'core', check=40000, topic=T5),
                  M('k1d', 'Holding period that makes listed shares long-term:', ['More than twelve months', 'More than twenty-four months', 'More than thirty-six months', 'Any period'], 0,
                    'Section 2(101). In practice: 12-month test.', 'core', topic=T1),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch04', 1, 'Capital Gains',
                ['Identify capital assets, transfers and holding periods.',
                 'Compute capital gains including the indexation comparison.',
                 'Apply special provisions for depreciable assets, slump sales and firms.',
                 'Apply exemptions for reinvestment.',
                 'Apply rates under sections 196 to 198.'],
                {'difficulty': 'hard', 'minutes': {'learn': 55, 'practice': 40}, 'prereq': ['fin-p4-ch03-u01'],
                 'exam_tip': 'Classify the asset and holding period first; exemptions and rates follow from that.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 2(22) capital asset; 12/24-month holding.', 'Section 67 charge; section 70 non-transfers.', 'Section 72 computation; old land indexation comparison.',
                             'Sections 74 and 77 special cases.', 'Exemptions sections 82–89; rates sections 196–198.'],
                 'remember': ['CII 2026-27 is 384.'],
                 'traps': ['Applying indexation for computing GTI.']},
                [('Charge', 'Section 67'), ('Computation', 'Section 72'), ('House exemption', 'Section 82'), ('Bonds', 'Section 85'), ('Rates', 'Sections 196–198')],
                viva, cases)
