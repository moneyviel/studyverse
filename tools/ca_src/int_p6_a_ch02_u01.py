"""CA Intermediate · Paper 6A Financial Management · Chapter 2 Types of Financing.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch02-u01'
T1 = 'Financial needs and matching sources'
T2 = 'Equity and preference share capital'
T3 = 'Retained earnings, debentures and bonds'
T4 = 'Term loans, bridge finance and venture capital'
T5 = 'Debt securitisation'
T6 = 'Lease financing'
T7 = 'Short-term sources and bank credit'
T8 = 'Export finance by banks'
T9 = 'Other, international and contemporary sources'


def build():
    ck = Checks()
    pat_a = ck.add('(4000000)*(1-0.25)', 'Plan A (equity): PAT')
    eps_a = ck.add('3000000/500000', 'Plan A EPS (4,00,000 + 1,00,000 shares)')
    pat_b = ck.add('(4000000-600000)*(1-0.25)', 'Plan B (12% debentures): PAT')
    eps_b = ck.add('2550000/400000', 'Plan B EPS')
    pat_c = ck.add('4000000*(1-0.25)-550000', 'Plan C (11% preference): profit for equity')
    eps_c = ck.add('2450000/400000', 'Plan C EPS')
    i1 = {'id': 'i1', 'title': 'Equity, debentures or preference shares — effect on EPS', 'difficulty': 'core', 'minutes': 10,
          'q': 'Nilgiri Foods Ltd. has 4,00,000 equity shares and no debt. It needs ₹50,00,000 for expansion, after which EBIT is expected to be ₹40,00,000. Tax rate 25%. Options: (A) issue 1,00,000 equity shares at ₹50; (B) issue 12% debentures; (C) issue 11% preference shares. Compute EPS under each plan and comment.',
          'solution': [table(['Particulars', 'Plan A ₹', 'Plan B ₹', 'Plan C ₹'], [
              ['EBIT', inr(4000000), inr(4000000), inr(4000000)],
              ['Less: Interest @ 12% on ₹50,00,000', '—', inr(600000), '—'],
              ['Profit before tax', inr(4000000), inr(3400000), inr(4000000)],
              ['Less: Tax @ 25%', inr(1000000), inr(850000), inr(1000000)],
              ['Profit after tax', inr(pat_a), inr(pat_b), inr(3000000)],
              ['Less: Preference dividend @ 11%', '—', '—', inr(550000)],
              ['Earnings for equity', inr(3000000), inr(2550000), inr(pat_c)],
              ['Number of equity shares', '5,00,000', '4,00,000', '4,00,000'],
              ['EPS', R(eps_a), R(eps_b), R(eps_c)]], title='EPS under three plans'),
              p(f'Debentures give the highest EPS ({R(eps_b)}) because interest is tax-deductible and no new shares are issued. Preference shares avoid dilution but their dividend is paid from after-tax profit, so EPS ({R(eps_c)}) is lower than with debt. Equity gives the lowest EPS ({R(eps_a)}) but adds no fixed burden — a choice to make when business risk is high.'),
              note('Higher EPS with debt comes with higher financial risk: interest and repayment are compulsory.')],
          'checks': list(ck)}

    ck2 = Checks()
    price = ck2.add('round(100000/1.1**5)', 'Issue price of a 5-year deep discount bond yielding 10% (face ₹1,00,000)')
    disc = ck2.add('100000-62092', 'Implicit interest earned over the life')
    i2 = {'id': 'i2', 'title': 'Pricing a deep discount (zero-interest) bond', 'difficulty': 'core', 'minutes': 5,
          'q': 'A company issues deep discount bonds of face value ₹1,00,000 redeemable at par after 5 years, with no periodic interest. Investors want a 10% annual return. At what price should each bond be issued, and what is the investor\'s total return?',
          'solution': [wn('Issue price', f'1,00,000 ÷ (1.10)⁵ = 1,00,000 ÷ 1.61051 = {R(price)}.'),
                       p(f'The investor pays {R(price)} and receives ₹1,00,000 after 5 years — a gain of {R(disc)}, which is the interest earned. The company has no cash outgo until maturity, which suits projects with a long gestation period.')],
          'checks': list(ck2)}

    needs = table(['Need', 'Period', 'Typical uses', 'Matching source'], [
        ['Long-term', 'Generally beyond 5–10 years', 'Land, building, plant; permanent (core) working capital', 'Equity, preference, retained earnings, debentures, term loans'],
        ['Medium-term', 'Over 1 year up to 5 years', 'Critical spares, tools, dies, moulds', 'Medium-term loans, public deposits, leasing'],
        ['Short-term', 'Up to 1 year', 'Stock, debtors, cash (working capital)', 'Trade credit, bank credit, commercial paper'],
    ], title='Financial needs and matching sources')
    stages = table(['Business stage', 'Uncertainty', 'Usual sources'], [
        ['Early', 'High', 'Equity — mainly angel funds'],
        ['Early', 'High to moderate', 'Equity, venture capital, some debt'],
        ['Growth', 'Moderate to low', 'Debt, venture capital, private equity'],
        ['Stable', 'Low', 'Debt'],
    ], title='Stage of business and source of funds')
    eq_pref = table(['Basis', 'Equity shares', 'Preference shares', 'Debentures'], [
        ['Nature', 'Ownership capital', 'Hybrid — features of equity and debt', 'Borrowed capital (loan)'],
        ['Return', 'Dividend, varies; after preference dividend', 'Fixed rate dividend, paid before equity', 'Fixed interest, payable even in loss'],
        ['Tax', 'Dividend not deductible', 'Dividend not deductible', 'Interest deductible — tax shield'],
        ['Voting', 'Full voting rights', 'Limited (mainly when dividend is in arrears)', 'No voting rights'],
        ['Repayment', 'Not redeemable (permanent)', 'Usually redeemable after a stated period', 'Repayable on maturity'],
        ['Cost to company', 'Highest', 'Middle', 'Lowest'],
    ], title='Equity vs preference vs debentures')
    pref_types = table(['Type of preference share', 'Key feature'], [
        ['Cumulative', 'Unpaid dividends accumulate and are paid before equity in later years'],
        ['Non-cumulative', 'Unpaid dividend of a year lapses'],
        ['Redeemable', 'Capital is repaid after a stated period'],
        ['Participating', 'Also shares in surplus profit after equity is paid'],
        ['Non-participating', 'Gets only the fixed dividend'],
        ['Convertible', 'Can be converted into equity shares'],
    ], title='Kinds of preference shares')
    lease = table(['Basis', 'Financial lease', 'Operating lease'], [
        ['Risk and reward of ownership', 'Passed to the lessee; lessor keeps only legal title', 'Stay with the lessor'],
        ['Obsolescence risk', 'Lessee', 'Lessor'],
        ['Cancellation', 'Non-cancellable', 'Usually cancellable with notice'],
        ['Repairs and maintenance', 'Lessee bears', 'Usually lessor bears'],
        ['Period / payout', 'Most of the economic life; full payout', 'Shorter than economic life; non-payout (asset re-leased)'],
    ], title='Financial lease vs operating lease')
    bank = table(['Facility', 'How it works'], [
        ['Short-term loan', 'Whole amount disbursed at once against security; repaid in full or by instalments'],
        ['Overdraft', 'Overdraw the current account up to a limit; interest on daily debit balance'],
        ['Clean overdraft', 'No tangible security — only for sound, reputed borrowers, usually with guarantees'],
        ['Cash credit', 'Draw as needed up to a limit against goods (pledge/hypothecation); interest only on amount used'],
        ['Advances against goods', 'Goods pledged or hypothecated as security'],
        ['Bills purchased / discounted', 'Advance against bills, which the bank holds as security'],
    ], title='Forms of bank credit')

    concepts = [
        C('c1', T1, [
            'A business needs funds for three periods: long-term (generally beyond 5–10 years — fixed assets and the permanent part of working capital), medium-term (more than a year up to 5 years) and short-term (up to a year — stock, debtors, cash).',
            'Matching principle: finance short-term needs from short-term sources, medium-term needs from medium-term sources and long-term needs from long-term sources. Funding a factory with a 90-day loan creates refinancing risk; funding stock with equity is costly.',
            'The stage of the business also matters: high-uncertainty start-ups depend on equity (angels, venture capital); stable firms can carry more debt.',
            'Sources can be classified by basic source (share capital, debt, internal funds), by maturity (long, medium, short) and by ownership and control (owned vs borrowed).'],
          'Match the loan to the life of what it buys — you would not take a 20-year home loan to pay this month\'s grocery bill, nor buy a house with a credit card.',
          'Banks ask for the "means of finance" for a project and check that long-term assets are not funded with short-term borrowings.',
          blocks=[needs, stages]),
        C('c2', T2, [
            'Equity (ordinary) shares are permanent capital. Equity holders bear the highest risk, are paid dividends only after all other claims (an appropriation of profit, not a charge), and in winding up get what remains after others are paid. So they expect the highest return — equity is the costliest source.',
            'Merits of equity: no repayment obligation; no compulsory dividend; widens the capital base and so supports further borrowing; more can be raised later through a rights issue. Demerits: dilutes EPS and control of existing holders; investors see it as risky.',
            'Kinds of equity issue include a fresh issue, a rights issue, bonus shares and sweat equity.',
            'Preference shares get priority over equity for a fixed dividend and for capital repayment in winding up. They are hybrid: like equity, the dividend is not tax-deductible; like debt, the rate is fixed. They are usually cumulative and redeemable; cumulative convertible preference shares convert into equity after some years and suit long-gestation projects.',
            'Merits of preference shares: no EPS dilution, leverage benefit, no takeover risk (limited voting), redeemable. Demerits: dividend gives no tax shield, so costlier than debt; arrears block equity dividends and hurt reputation.'],
          'Equity holders are the owners at the back of the queue who keep whatever is left; preference holders stand in front with a fixed ticket; lenders stand at the very front.',
          'Start-ups issue equity; mature companies use preference shares when they want funds without giving up votes.',
          blocks=[eq_pref, pref_types]),
        C('c3', T3, [
            'Retained earnings (ploughing back profits): belong to equity holders, raise net worth, need no issue cost, dilute no control and carry almost no risk. Whether to retain depends on whether the firm can earn more than shareholders\' required return — covered in the dividend decision.',
            'Debentures are instruments for long-term borrowing, issued under a debenture trust deed, secured or unsecured, listed or unlisted, usually for 3–10 years. Interest is a tax-deductible expense, so debentures are the cheapest long-term source; investors prefer them to preference shares because interest is payable whether or not there is profit.',
            'By convertibility: non-convertible (repaid at maturity), fully convertible (converted into equity on stated terms, so usually lower interest) and partly convertible. Other kinds: bearer, registered, mortgage (secured), naked/simple (unsecured), redeemable and irredeemable.',
            'Merits: lowest cost, no dilution of control, attractive in inflation (fixed outgo falls in real terms). Demerits: interest and principal are compulsory; restrictive covenants; higher financial risk; large cash outflow at maturity. A public issue of debentures must be credit-rated (agencies such as CRISIL, ICRA, CARE).',
            'Bonds are fixed-income securities raised by public issue or private placement. A callable bond lets the issuer redeem early at a call price; a puttable bond lets the investor sell it back early. Indian examples: masala bonds (rupee-denominated, issued abroad), municipal bonds (for urban infrastructure) and government/treasury bonds.'],
          'Retained earnings are your own savings — free of interest and of anyone else\'s say; debentures are a loan with a fixed EMI that you must pay even in a bad month.',
          'Listed companies regularly raise money through non-convertible debentures (NCDs) rated by credit-rating agencies.'),
        C('c4', T4, [
            'Term loans from financial institutions: national institutions (e.g. IFCI, SFCs, IDBI, ICICI — several later became banks) and international ones (World Bank/IBRD, IFC, ADB) provide long-term project finance.',
            'Commercial banks, traditionally short-term lenders, now give long-term loans for expansion and fund the permanent (minimum) level of working capital through a working capital term loan (WCTL).',
            'Bridge finance: a short-term bank loan taken while a sanctioned term loan awaits disbursement, so the project need not wait. It is repaid from the term loan when disbursed, is secured by movable assets and guarantees, and usually costs more than the term loan.',
            'Venture capital: long-term, mainly equity finance for new, high-risk, growth-oriented ventures by qualified entrepreneurs who lack funds and experience. Besides money, the investor adds strategy, networking and management support.',
            'Methods of venture financing: equity (the investor usually keeps a minority stake so control stays with the entrepreneur); conditional loan (no interest; repaid as a royalty on sales once sales begin); income note (low interest plus low royalty); participating debenture (no interest at start-up, low interest next, higher interest later).'],
          'Bridge finance is the temporary plank laid across a stream until the proper bridge (term loan) arrives; venture capital is a mentor who invests money as well as advice.',
          'Indian start-ups raise "Series A/B" rounds from venture funds that take board seats and help with hiring and strategy.'),
        C('c5', T5, [
            'Securitisation converts illiquid assets (such as loans) into marketable securities. The originator sells a pool of loans to a Special Purpose Vehicle (SPV); the SPV pays the originator and issues securities to investors backed by the cash flows from the pool.',
            'Benefits to the originator: immediate cash, loans move off the balance sheet, more lending capacity. Benefits to investors: a liquid investment in a diversified pool of loans.',
            'The original borrowers usually continue paying as before and may not know of the transfer; their payments ultimately flow to the investors.'],
          'Securitisation is like selling your future rent receipts in a bundle today to get cash now — the buyer collects the rent later.',
          'Vehicle-finance NBFCs in India regularly securitise their loan pools to raise funds.'),
        C('c6', T6, [
            'Leasing is a contract under which the lessor buys an asset and lets the lessee use it for periodic rentals. It is an alternative to buying with own or borrowed money and can be arranged faster than term loans.',
            'Operating lease: short period compared to the asset\'s life, usually cancellable, lessor bears maintenance, insurance and obsolescence and re-leases the asset to others — suits firms that want to keep updating equipment.',
            'Financial (capital) lease: long-term, non-cancellable, covering most of the asset\'s useful life; lessee bears maintenance, insurance and obsolescence; the lessor is just a financier — effectively a loan in disguise.',
            'Other leases: sale and lease back (owner sells the asset and leases it back — gets cash, keeps using it); leveraged lease (lessor borrows a large part of the cost from a lender, who is paid from rentals); sales-aid lease (lessor ties up with a manufacturer to market its products and earns from both); close-ended (asset returns to lessor) vs open-ended (lessee may buy at the end).',
            'For the lessee, lease rentals are tax-deductible and there is no large immediate outflow; buying instead gives depreciation and deductible interest — so lease vs buy needs evaluation.'],
          'An operating lease is renting a car for a weekend trip; a financial lease is driving the same car for its whole life while paying the financier instalments.',
          'Airlines commonly use sale and lease back to release cash tied up in aircraft.',
          blocks=[lease]),
        C('c7', T7, [
            'Trade credit: credit from suppliers (often 15–90 days); arises automatically, has no explicit cost and grows with business volume — the most common short-term source.',
            'Accrued expenses (wages, taxes not yet paid) and deferred income (advance receipts for future supplies) are spontaneous sources. Advances from customers, common in long manufacturing or construction contracts, are cost-free.',
            'Money market instruments: commercial paper — an unsecured promissory note issued by highly rated companies (and certain other permitted issuers) under RBI rules, with a credit rating; treasury bills — short-term central government securities with maturities up to 364 days; certificates of deposit — negotiable time-deposit receipts issued by banks for a fixed period from 7 days to 1 year, tradable in the secondary market.',
            'Bank credit takes several forms (table). Inter-corporate deposits are short-term loans from companies with surplus funds. Public deposits, accepted subject to legal limits, are unsecured and should finance working capital, not fixed assets.'],
          'Trade credit is the shop that lets you pay at the month end; cash credit is a credit card limit you draw and repay as needed and pay interest only on what you use.',
          'Large FMCG companies keep working capital low by stretching supplier credit and collecting from customers quickly.',
          blocks=[bank]),
        C('c8', T8, [
            'Banks give short-term export finance in rupees or foreign currency at two stages: pre-shipment and post-shipment.',
            'Pre-shipment (packing credit): an advance to buy, make, process and pack goods against a firm export order or an irrevocable letter of credit; repaid from export proceeds within the period allowed (the study material uses 180 days). Types: clean packing credit (no charge on goods; ECGC cover obtained), against hypothecation of goods, against pledge of goods (bank holds the goods), with ECGC guarantee, and with a forward exchange contract to cover currency risk.',
            'Post-shipment: purchase or discount of export bills backed by shipping documents; ECGC post-shipment guarantee; advances against bills sent for collection; advances against duty drawback or export incentives.',
            'Other help from banks: opening letters of credit for exporters\' purchases, issuing guarantees, financing deferred-payment exports, and providing status reports and market information.'],
          'Pre-shipment finance pays for getting the goods ready; post-shipment finance bridges the wait until the foreign buyer pays.',
          'An exporter of garments typically uses packing credit to buy fabric and post-shipment bill discounting after dispatch.'),
        C('c9', T9, [
            'Other sources: seed capital assistance for qualified entrepreneurs short of funds; internal cash accruals; unsecured loans from promoters (subordinate to institutional loans and treated as quasi-equity); deferred payment guarantee (supplier finances machinery against a bank guarantee); capital incentives/subsidies for backward areas (project must be viable without them).',
            'Special bonds: deep discount and zero coupon bonds (issued at a discount, redeemed at face value — the discount is the interest); secured premium notes with detachable warrants; zero-interest fully convertible debentures; option bonds; inflation-indexed bonds; floating rate bonds; high-yield (junk) bonds rated below investment grade.',
            'International sources: foreign currency loans from banks and development banks, international agencies (IFC, IBRD, ADB), and capital markets — external commercial borrowings (automatic and approval routes), euro bonds (issued in a currency other than that of the country of issue), foreign bonds (in the currency of the country of issue), fully hedged bonds, medium-term notes, floating rate notes, euro commercial paper, euro convertible bonds, and ESG bonds (green, social, sustainability-linked).',
            'Depository receipts: ADRs (listed in the US), GDRs (mainly European markets) and IDRs (foreign companies raising money in India).',
            'Contemporary sources: crowdfunding through online platforms — equity crowdfunding, peer-to-peer (P2P) lending, and donation-based funding.'],
          'Finance today is a buffet — from a promoter\'s own loan to a green bond in London to a thousand small investors online.',
          'Indian companies have raised money through masala bonds, green bonds and sustainability-linked bonds in recent years.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Choosing finance for a new plant', 'role': 'Finance analyst',
         'situation': 'A profitable mid-sized company needs ₹80 crore for a plant with a 2-year construction period; promoters do not want to lose control.',
         'steps': ['Match a long-term need with long-term sources — term loan and debentures plus some internal accruals.', 'Avoid fresh equity to protect control; consider convertible instruments only if control can be preserved.', 'Arrange bridge finance if the term-loan disbursement will be delayed; compare EPS and risk under each mix.'],
         'takeaway': 'Match maturity, protect control and keep financial risk within limits.'},
        {'id': 'j2', 'title': 'Lease or buy for IT equipment', 'role': 'Assistant to the CFO',
         'situation': 'Laptops become obsolete within three years; the company has limited cash.',
         'steps': ['Prefer an operating lease — obsolescence risk stays with the lessor.', 'Compare total rentals with the cost of buying net of tax benefits.', 'Check cancellation and upgrade terms.'],
         'takeaway': 'For fast-ageing assets, an operating lease shifts obsolescence risk away.'},
    ]

    mcqs = [
        Q('m1', 'The basic principle of financing is that:', ['Long-term needs should be met from long-term sources and short-term needs from short-term sources', 'All needs should be met from equity', 'All needs should be met from bank overdraft', 'Short-term needs should be met from long-term sources only'], 0,
          'Funds should match the period for which they are needed: fixed assets and core working capital from long-term sources, seasonal working capital from short-term sources. Funding long-term assets with short-term loans creates refinancing risk. In practice: lenders check this matching when appraising projects.', 'c1', T1),
        Q('m2', 'Which source of long-term finance usually has the highest cost?', ['Equity share capital', 'Debentures', 'Term loans', 'Preference share capital'], 0,
          'Equity shareholders bear the highest risk — they are paid last and have no fixed return — so they expect the highest return, making equity the costliest source. Debentures are cheapest because interest is tax-deductible. In practice: companies with stable cash flows use more debt to lower overall cost.', 'c2', T2),
        Q('m3', 'Preference share capital is called hybrid because:', ['Its dividend is fixed like debt interest but not tax-deductible like equity dividend', 'It is always convertible', 'It carries full voting rights', 'It is repayable on demand'], 0,
          'Preference shares resemble debt in having a fixed rate of return and equity in that the dividend is an appropriation of profit, not a tax-deductible expense. They are not always convertible and carry only limited voting rights. In practice: this is why they cost more than debentures.', 'c2', T2),
        Q('m4', 'Debentures are the cheapest source of long-term finance mainly because:', ['Interest on them is tax-deductible', 'They carry voting rights', 'They never need repayment', 'They are always unsecured'], 0,
          'Debenture interest is deducted before tax, so the effective cost is lower, and investors accept a lower return because debt is safer. They have no voting rights and must be repaid on maturity. In practice: at 25% tax, 12% interest costs the company only 9% after tax.', 'c3', T3),
        Q('m5', 'A bond that gives the issuer the right to redeem it before maturity is a:', ['Callable bond', 'Puttable bond', 'Zero coupon bond', 'Masala bond'], 0,
          'A callable bond has a call option for the issuer to redeem early at a stated call price, usually at a premium. A puttable bond gives the investor the right to sell it back early. In practice: issuers call bonds when interest rates fall, refinancing at lower cost.', 'c3', T3),
        Q('m6', 'A masala bond is:', ['A rupee-denominated bond issued outside India', 'A dollar bond issued in India', 'A bond issued by a municipal body', 'A government treasury bond'], 0,
          'Masala bonds are issued in overseas markets but denominated in Indian rupees, so the currency risk is borne by the foreign investor, not the Indian issuer. Municipal and treasury bonds are domestic instruments. In practice: large Indian companies used masala bonds to tap foreign investors without currency risk.', 'c3', T3, 'moderate'),
        Q('m7', 'Bridge finance refers to:', ['A short-term loan taken pending disbursement of a sanctioned term loan', 'A loan for building a bridge', 'A permanent working capital loan', 'Finance from venture capitalists'], 0,
          'Bridge finance is a short-term bank loan that lets the project proceed while the term loan already sanctioned awaits disbursement; it is repaid from the term loan. Its interest rate is usually higher than the term loan. In practice: it avoids costly delays in starting construction.', 'c4', T4),
        Q('m8', 'Under a conditional loan in venture capital financing:', ['No interest is charged; repayment is by royalty on sales', 'Interest is charged at a fixed high rate from day one', 'The investor takes a majority stake', 'The loan is repayable on demand'], 0,
          'A conditional loan carries no interest; it is repaid as a royalty on sales once the venture starts selling, matching repayment to success. An income note combines low interest with low royalty. In practice: such terms protect a start-up\'s cash flow in its early years.', 'c4', T4, 'moderate'),
        Q('m9', 'In securitisation, the entity that buys the pool of loans and issues securities is the:', ['Special Purpose Vehicle (SPV)', 'Original borrower', 'Credit rating agency', 'Stock exchange'], 0,
          'The originator sells the loan pool to a Special Purpose Vehicle, which issues securities to investors backed by the pool\'s cash flows. Rating agencies may rate the securities but do not buy the loans. In practice: this lets lenders raise cash and move loans off their balance sheet.', 'c5', T5),
        Q('m10', 'In a financial lease, the risk of obsolescence is borne by the:', ['Lessee', 'Lessor', 'Manufacturer', 'Bank'], 0,
          'A financial lease transfers the risks and rewards of ownership to the lessee, including obsolescence, maintenance and insurance; the lessor is merely a financier. In an operating lease the lessor bears obsolescence. In practice: firms lease fast-changing technology on operating leases for this reason.', 'c6', T6),
        Q('m11', 'Under sale and lease back:', ['The owner sells an asset and takes it back on lease', 'The lessor borrows most of the asset cost from a lender', 'The lessor ties up with a manufacturer to market products', 'The lessee must buy the asset at the end'], 0,
          'In sale and lease back, the owner sells the asset to raise cash and immediately leases it back, continuing to use it. Borrowing most of the cost from a lender describes a leveraged lease; a manufacturer tie-up describes a sales-aid lease. In practice: it releases capital locked in buildings or aircraft.', 'c6', T6),
        Q('m12', 'Under a cash credit arrangement, interest is charged on:', ['The amount actually drawn', 'The full sanctioned limit', 'The value of goods pledged', 'The average of the limit and the drawing'], 0,
          'In cash credit the borrower draws only as needed within the sanctioned limit, and interest is charged on the amount actually used. Paying interest on the full limit would defeat the flexibility of the facility. In practice: businesses deposit surplus cash into the account to cut interest cost.', 'c7', T7),
        Q('m13', 'Commercial paper is:', ['An unsecured short-term promissory note issued by highly rated borrowers', 'A secured long-term loan', 'A deposit certificate issued by banks', 'A government security'], 0,
          'Commercial paper is an unsecured money-market instrument in the form of a promissory note, issued by creditworthy borrowers with a credit rating under RBI rules. Certificates of deposit are issued by banks and treasury bills by the government. In practice: large companies use CP to borrow cheaper than bank loans.', 'c7', T7),
        Q('m14', 'Packing credit is a form of:', ['Pre-shipment export finance', 'Post-shipment export finance', 'Long-term project finance', 'Lease finance'], 0,
          'Packing credit is advanced before shipment to buy, process and pack goods for export against a firm order or letter of credit. Discounting export bills after dispatch is post-shipment finance. In practice: the advance is repaid from the export proceeds when the foreign buyer pays.', 'c8', T8),
        Q('m15', 'A zero coupon bond:', ['Pays no periodic interest and is issued at a discount to face value', 'Pays interest monthly', 'Is always convertible into equity', 'Has interest linked to inflation'], 0,
          'A zero coupon bond pays no periodic interest; it is issued below face value and redeemed at face value, the difference being the investor\'s return. Inflation-linked interest describes inflation bonds. In practice: such bonds suit projects that generate cash only after several years.', 'c9', T9),
        Q('m16', 'GDRs are mainly traded in:', ['European markets, especially London', 'Indian stock exchanges only', 'US exchanges only', 'Commodity exchanges'], 0,
          'Global Depository Receipts are negotiable certificates representing shares of a company, mainly traded in European markets such as London; ADRs are listed in the US and IDRs in India. In practice: many Indian companies chose GDRs because US listing brings heavier disclosure duties.', 'c9', T9, 'moderate'),
        Q('m17', 'Peer-to-peer (P2P) lending is a form of:', ['Crowdfunding where lenders give loans to borrowers through an online platform', 'Bank overdraft', 'Equity crowdfunding', 'Donation-based funding'], 0,
          'P2P lending matches individual lenders with borrowers through an online platform; the loans are repaid with interest and carry default risk. Equity crowdfunding gives investors shares, and donation-based funding expects no return. In practice: P2P platforms in India are regulated by the RBI.', 'c9', T9),
    ]
    # EPS MCQ tied to the illustration
    mcqs.append(Q('m18', f'Using the Nilgiri Foods data (EBIT ₹40,00,000, tax 25%, 4,00,000 existing shares, ₹50,00,000 needed), EPS under 12% debentures is:',
                  [R(eps_b), R(eps_a), R(eps_c), '₹8.50'], 0,
                  f'Interest = 12% × 50,00,000 = 6,00,000; PBT = 34,00,000; tax 8,50,000; PAT 25,50,000; EPS = 25,50,000 ÷ 4,00,000 = {R(eps_b)}. The equity plan gives {R(eps_a)} because shares rise to 5,00,000. In practice: debt raises EPS when the return on funds exceeds the after-tax cost of debt.',
                  'c3', T3, 'moderate', check=eps_b))

    questions = [
        W('q1', 5, 'Distinguish between a financial lease and an operating lease.',
          [lease, p('A financial lease is in substance a way of financing the purchase of the asset; an operating lease is a rental for use.')],
          [S('s1', 'Risk and reward / ownership', 1, 'concept', 'risk', 'reward|ownership'),
           S('s2', 'Obsolescence risk', 1, 'concept', 'obsolescence'),
           S('s3', 'Cancellability', 1, 'concept', 'cancel'),
           S('s4', 'Repairs and maintenance', 1, 'concept', 'repair|maintenance'),
           S('s5', 'Period / full payout', 1, 'concept', 'payout|economic life|useful life|period')],
          ['A tabular answer with five points earns full marks.'], ['Saying the lessee owns the asset in a financial lease.'], ['Use a two-column table.'], pad='table'),
        W('q2', 4, 'Explain the methods of venture capital financing.',
          [ul(['Equity financing: long-term equity contribution, kept to a minority stake so that control remains with the entrepreneur.',
               'Conditional loan: no interest; repaid as a royalty on sales once the venture generates sales.',
               'Income note: a hybrid — the entrepreneur pays both interest and royalty, at low rates.',
               'Participating debenture: no interest in the start-up phase, a low rate in the next phase and a higher rate thereafter.'])],
          [S('s1', 'Equity financing', 1, 'concept', 'equity'),
           S('s2', 'Conditional loan — royalty, no interest', 1, 'concept', 'conditional', 'royalty'),
           S('s3', 'Income note — interest plus royalty', 1, 'concept', 'income note', 'interest|royalty'),
           S('s4', 'Participating debenture — phased interest', 1, 'concept', 'participating', 'phase|stage|start')],
          ['Four methods, one line each, is enough.'], ['Confusing income note with conditional loan.'], ['Use a bulleted list.']),
        W('q3', 6, 'Nilgiri Foods Ltd. (4,00,000 equity shares, no debt) needs ₹50,00,000; expected EBIT ₹40,00,000; tax 25%. Compute EPS if funds are raised by (A) 1,00,000 equity shares at ₹50, (B) 12% debentures, (C) 11% preference shares. Which plan maximises EPS?',
          i1['solution'],
          [S('s1', 'Plan A EPS', 2, 'computation', 'plan a|equity', nums=[eps_a]),
           S('s2', 'Plan B EPS', 2, 'computation', 'debenture|plan b', nums=[eps_b]),
           S('s3', 'Plan C EPS', 1, 'computation', 'preference|plan c', nums=[eps_c]),
           S('s4', 'Conclusion — debentures maximise EPS', 1, 'conclusion', 'debenture', 'highest|maximum|maximis|best')],
          ['Show tax and preference dividend clearly.'], ['Deducting preference dividend before tax.'], ['Use a columnar table.'], pad='table', checks=list(ck)),
    ]

    viva = [
        V('v1', 'Why is preference share capital called a hybrid source?',
          'Because its dividend is at a fixed rate like interest on debt, but the dividend is not tax deductible and is paid out of profits like equity dividend.',
          [P('p1', 'Fixed rate like debt', 5, 'fixed'), P('p2', 'Not tax-deductible like equity', 5, 'not tax|non deductible|not deductible|no tax shield|not a tax')], 'c2'),
        V('v2', 'What is bridge finance?',
          'Bridge finance is a short term loan from a bank taken while a term loan already sanctioned by an institution is awaiting disbursement. It is repaid out of the term loan.',
          [P('p1', 'Short-term loan', 3, 'short term|short-term|temporary'), P('p2', 'Pending disbursement of sanctioned term loan', 5, 'term loan', 'sanction|disburse|pending'), P('p3', 'Repaid from term loan', 2, 'repaid|repay|adjust')], 'c4'),
        V('v3', 'Explain debt securitisation in brief.',
          'Securitisation pools illiquid assets such as loans and sells them to a special purpose vehicle, which converts them into marketable securities sold to investors. The originator gets cash and the loans go off its balance sheet.',
          [P('p1', 'Pooling illiquid assets/loans', 3, 'pool|illiquid|loan'), P('p2', 'SPV issues marketable securities', 4, 'spv|special purpose', 'securit|marketable'), P('p3', 'Originator gets cash / off balance sheet', 3, 'cash|fund|off balance|balance sheet')], 'c5'),
        V('v4', 'Distinguish pre-shipment from post-shipment finance.',
          'Pre-shipment finance, mainly packing credit, is given before shipment to buy, process and pack goods for export. Post-shipment finance is given after shipment, mainly by purchasing or discounting export bills, until the buyer pays.',
          [P('p1', 'Pre-shipment — before shipment, packing credit', 5, 'pre', 'before|packing'), P('p2', 'Post-shipment — after shipment, export bills', 5, 'post', 'after|bill|discount')], 'c8'),
        V('v5', 'What is the difference between a euro bond and a foreign bond?',
          'A euro bond is issued in a currency other than the currency of the country where it is issued. A foreign bond is issued by a foreign borrower in the currency of the country where it is issued.',
          [P('p1', 'Euro bond — currency different from country of issue', 5, 'currency', 'other than|different|not denominated'), P('p2', 'Foreign bond — currency of country of issue', 5, 'currency of the country|same currency|local currency|currency of that country')], 'c9'),
    ]

    cases = [{'id': 'k1', 'title': 'Funding plan at Rangoli Textiles', 'difficulty': 'moderate',
              'case': 'Rangoli Textiles, an exporter, plans a ₹30 crore weaving unit. A term loan is sanctioned but disbursement will take four months. It also needs funds to buy yarn for a confirmed US order, and wants to replace computers every three years. Promoters wish to keep control.',
              'mcqs': [
                  M('k1a', 'To start construction without waiting four months, Rangoli should use:', ['Bridge finance', 'Trade credit', 'Commercial paper', 'Donation crowdfunding'], 0,
                    'Bridge finance is a short-term bank loan taken pending disbursement of a sanctioned term loan and repaid from it. Trade credit and commercial paper are working-capital tools. In practice: bridge loans usually cost a little more than the term loan.', 'core', topic=T4),
                  M('k1b', 'Funds to buy yarn for the confirmed export order are best raised through:', ['Packing credit', 'Post-shipment bill discounting', 'Equity shares', 'Deep discount bonds'], 0,
                    'Packing credit is pre-shipment finance to buy, process and pack goods against a firm export order or letter of credit. Bill discounting is post-shipment finance given after dispatch. In practice: it is repaid from the export proceeds.', 'core', topic=T8),
                  M('k1c', 'For computers replaced every three years, the more suitable arrangement is:', ['Operating lease', 'Financial lease', 'Sale and lease back', 'Leveraged lease'], 0,
                    'An operating lease keeps obsolescence risk with the lessor and is usually cancellable, ideal for equipment that becomes outdated quickly. A financial lease would put the obsolescence risk on Rangoli. In practice: IT equipment is often taken on operating leases.', 'moderate', topic=T6),
                  M('k1d', 'To fund the unit without diluting promoters\' control, Rangoli should prefer:', ['Term loans and debentures', 'A fresh public issue of equity', 'Bonus shares', 'Equity crowdfunding'], 0,
                    'Debt (term loans and debentures) carries no voting rights, so control is not diluted, and interest is tax-deductible. A fresh equity issue brings new voting shareholders. In practice: the trade-off is higher financial risk from fixed interest and repayment.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch02', 1, 'Types of Financing',
                ['Classify financial needs and match them with suitable sources.',
                 'Compare equity, preference shares, retained earnings, debentures and bonds and compute EPS under alternative plans.',
                 'Explain term loans, bridge finance, venture capital, securitisation and lease financing.',
                 'Describe short-term sources, bank credit and export finance.',
                 'Explain other, international and contemporary sources of finance.'],
                {'difficulty': 'core', 'minutes': {'learn': 45, 'practice': 35}, 'prereq': ['int-p6-a-ch01-u01'],
                 'exam_tip': 'Frequent theory: lease types, venture capital methods, securitisation, bridge finance, export finance, ADR/GDR and ESG bonds; keep definitions crisp.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Match maturity: long-term needs from long-term sources, short-term from short-term.',
                             'Cost ranking (usual): equity > preference > debt; debt interest is tax-deductible.',
                             'Preference shares are hybrid; debentures are long-term debt under a trust deed.',
                             'Bridge finance covers the gap until a sanctioned term loan is disbursed.',
                             'Venture capital: equity, conditional loan, income note, participating debenture.',
                             'Securitisation: loans → SPV → marketable securities.',
                             'Financial lease = loan in disguise; operating lease = rental, lessor bears obsolescence.',
                             'Export finance: pre-shipment (packing credit) and post-shipment (bills).'],
                 'remember': ['Euro bond: currency ≠ country of issue; foreign bond: currency = country of issue.', 'ADR — US; GDR — mainly Europe; IDR — India.'],
                 'traps': ['Cash credit interest is on the amount used, not the limit.', 'Preference dividend is paid from after-tax profit.']},
                [('Cheapest long-term source', 'Debt (tax-deductible interest)'), ('Bridge finance', 'Gap until term-loan disbursement'),
                 ('Packing credit', 'Pre-shipment export finance'), ('Financial lease', 'Lessee bears risk and obsolescence'),
                 ('Masala bond', 'Rupee bond issued abroad')],
                viva, cases,
                topics=['Financial Needs and Sources of Finance of a Business', 'Classification of Financial Sources', 'Long-term Sources of Finance', 'Venture Capital Financing',
                        'Debt Securitisation', 'Lease Financing', 'Short-term Sources of Finance', 'Other Sources of Financing', 'International Financing', 'Contemporary Sources of Funding'])
