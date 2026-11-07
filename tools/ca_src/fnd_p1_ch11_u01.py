"""CA Foundation · Paper 1 Accounting · Chapter 11 Company Accounts · Unit 1 Introduction to Company Accounts.
Original explanations, names and numbers (structure and scope follow the ICAI study material)."""
from lib import *
from ca_viva import P, ALT, V
from ca_cases import M

UID = 'fnd-p1-ch11-u01'


def mcq(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check: d['check'] = check
    return d


def S(sid, pt, m, skill): return {'id': sid, 'pt': pt, 'm': m, 'skill': skill}


def build():
    # ---------------- Illustration 1: balance sheet in Schedule III (Division I) format ----------------
    c1 = Checks()
    sc = c1.add('50000*10', 'Share capital: 50,000 equity shares of ₹10 fully paid')
    rs = c1.add('60000+120000+85000', 'Reserves and surplus = securities premium + general reserve + surplus')
    ppe = c1.add('250000+310000', 'Property, plant and equipment = land + plant')
    cash = c1.add('175000+15000', 'Cash and cash equivalents = bank + cash in hand')
    el = c1.add('500000+265000+200000+95000+15000+30000', 'Total of equity and liabilities')
    asst = c1.add('560000+40000+100000+125000+90000+190000', 'Total of assets')
    bs1 = table(['Particulars', 'Note', '₹'], [
        ['EQUITY AND LIABILITIES', '', ''],
        ['1. Shareholders\' funds', '', ''],
        ['   (a) Share capital', '1', inr(sc)],
        ['   (b) Reserves and surplus', '2', inr(rs)],
        ['2. Non-current liabilities', '', ''],
        ['   Long-term borrowings (10% Debentures)', '3', inr(200000)],
        ['3. Current liabilities', '', ''],
        ['   (a) Trade payables', '', inr(95000)],
        ['   (b) Other current liabilities (outstanding salary)', '', inr(15000)],
        ['   (c) Short-term provisions (provision for tax)', '', inr(30000)],
        ['Total', '', inr(el)],
        ['ASSETS', '', ''],
        ['1. Non-current assets', '', ''],
        ['   (a) Property, plant and equipment and intangible assets', '', ''],
        ['       (i) Property, plant and equipment', '4', inr(ppe)],
        ['       (ii) Intangible assets (goodwill)', '', inr(40000)],
        ['   (b) Non-current investments', '', inr(100000)],
        ['2. Current assets', '', ''],
        ['   (a) Inventories', '', inr(125000)],
        ['   (b) Trade receivables', '', inr(90000)],
        ['   (c) Cash and cash equivalents', '5', inr(cash)],
        ['Total', '', inr(asst)],
    ], title='Nirmal Polymers Ltd — Balance Sheet as at 31 March 2027')
    notes1 = table(['Note', 'Particulars', '₹'], [
        ['1', 'Share capital — Authorised: 1,20,000 equity shares of ₹10 each = ₹12,00,000. Issued, subscribed and fully paid: 50,000 equity shares of ₹10 each', inr(sc)],
        ['2', 'Reserves and surplus — Securities premium ₹60,000; General reserve ₹1,20,000; Surplus (balance in statement of profit and loss) ₹85,000', inr(rs)],
        ['3', 'Long-term borrowings — 10% Debentures (bonds/debentures sub-head)', inr(200000)],
        ['4', 'Property, plant and equipment — Land ₹2,50,000; Plant and equipment ₹3,10,000', inr(ppe)],
        ['5', 'Cash and cash equivalents — Balances with banks ₹1,75,000; Cash in hand ₹15,000', inr(cash)],
    ], title='Notes to accounts')

    # ---------------- Illustration 2: share capital note with calls unpaid ----------------
    c2 = Checks()
    auth = c2.add('200000*10', 'Authorised capital: 2,00,000 shares × ₹10')
    issued = c2.add('120000*10', 'Issued and subscribed: 1,20,000 shares × ₹10')
    called = c2.add('120000*8', 'Called up: 1,20,000 shares × ₹8')
    unpaid = c2.add('3000*(8-5)', 'Calls unpaid: 3,000 shares × ₹3')
    paid = c2.add('960000-9000', 'Paid-up capital = called up − calls unpaid')
    note2 = table(['Particulars', '₹', '₹'], [
        ['Authorised share capital: 2,00,000 equity shares of ₹10 each', inr(auth), ''],
        ['Issued share capital: 1,20,000 equity shares of ₹10 each', inr(issued), ''],
        ['Subscribed share capital: 1,20,000 equity shares of ₹10 each', inr(issued), ''],
        ['Called up: 1,20,000 equity shares of ₹10 each, ₹8 per share called', inr(called), ''],
        ['Less: Calls unpaid (3,000 shares × ₹3)', '(' + inr(unpaid) + ')', inr(paid)],
    ], title='Note 1 — Share capital of Vedika Paints Ltd as at 31 March 2027')
    bs2 = table(['Particulars', 'Note', '₹'], [
        ['EQUITY AND LIABILITIES', '', ''],
        ['Shareholders\' funds — Share capital', '1', inr(paid)],
        ['Total', '', inr(paid)],
        ['ASSETS', '', ''],
        ['Current assets — Cash and cash equivalents (balance with bank)', '2', inr(paid)],
        ['Total', '', inr(paid)],
    ], title='Vedika Paints Ltd — Balance Sheet as at 31 March 2027 (extract)')

    # ---------------- Illustration 3: classify companies ----------------
    c3 = Checks()
    govt = c3.add('30+25', 'Government holding = Central 30% + State 25%')
    c3.add('8000*100/15000', 'Holding of Delta Ltd in Kiran Ltd (%) = 8,000 / 15,000 shares')
    cls = table(['Company and facts', 'Test applied', 'Conclusion'], [
        ['Ankur Seeds Ltd — Central Government holds 30% and a State Government 25% of the paid-up share capital', f'Government holding {govt}% — at least 51%? Yes (Central and State holdings are added)', 'Government company — s. 2(45)'],
        ['Kiran Ltd — Delta Ltd holds 8,000 of its 15,000 shares (about 53.3% of total share capital)', 'More than one-half of total share capital held by Delta Ltd', 'Kiran Ltd is a subsidiary of Delta Ltd — s. 2(87); Delta Ltd is its holding company — s. 2(46)'],
        ['Pixel Prints Pvt Ltd — paid-up capital ₹6 crore, last-year turnover ₹80 crore, not a holding or subsidiary company', 'Private; paid-up capital within ₹10 crore AND turnover within ₹100 crore', 'Small company — s. 2(85)'],
        ['Orbit Tools Pvt Ltd — paid-up capital ₹4 crore, last-year turnover ₹120 crore', 'Turnover exceeds ₹100 crore — both limits must be met', 'Not a small company'],
        ['Zenith Motors Inc. — incorporated in Japan, runs a sales office in Pune', 'Incorporated outside India + place of business in India + business activity in India', 'Foreign company — s. 2(42)'],
        ['Sonal Exports (OPC) Pvt Ltd — one member only', 'Only one person as member', 'One Person Company — s. 2(62)'],
    ], title='Which type of company?')

    # ---------------- Question 2 model ----------------
    q2c = Checks()
    q2_called = q2c.add('80000*7', 'Called up: 80,000 shares × ₹7')
    q2_unpaid = q2c.add('2500*2', 'Calls unpaid: 2,500 shares × ₹2')
    q2_paid = q2c.add('560000-5000', 'Paid-up capital')
    q2_auth = q2c.add('150000*10', 'Authorised capital')
    q2_iss = q2c.add('80000*10', 'Issued/subscribed capital')

    # ---------------- Question 3 model: classification ----------------
    q3rows = [
        ['Calls in arrears', 'Shareholders\' funds — Share capital (deducted from called-up capital)'],
        ['Securities premium', 'Shareholders\' funds — Reserves and surplus'],
        ['12% Debentures repayable after 6 years', 'Non-current liabilities — Long-term borrowings'],
        ['Instalment of a term loan payable within 12 months', 'Current liabilities — Short-term borrowings (current maturities of long-term borrowings, shown separately)'],
        ['Unpaid dividend', 'Current liabilities — Other current liabilities'],
        ['Provision for gratuity (payable after many years)', 'Non-current liabilities — Long-term provisions'],
        ['Computer software', 'Non-current assets — Intangible assets'],
        ['Loose tools', 'Current assets — Inventories'],
        ['Share application money received, allotment pending (not refundable)', 'Share application money pending allotment (separate head after shareholders\' funds)'],
        ['Cheques in hand', 'Current assets — Cash and cash equivalents'],
    ]

    viva = [
        V('v1', 'What is a company? Explain its meaning in law.',
          'In law, a company is an association of persons formed and incorporated under the Companies Act, 2013, or under an earlier company law. Once incorporated it becomes an artificial person with a separate legal entity, distinct from its members. It has perpetual succession, so its existence is not affected when members die or change, and it acts through a board of directors elected by the shareholders.',
          [P('p1', 'Formed and incorporated (registered) under the Companies Act, 2013 or an earlier company law', 3, 'incorporat|regist|formed under', 'companies act|company law|act 2013|previous law|earlier law', min=2),
           P('p2', 'An artificial (legal) person — separate legal entity distinct from its members', 4, 'artificial|legal person|juristic|separate legal|separate entity|distinct|separate from', min=1),
           P('p3', 'Perpetual succession — not affected by death or change of members', 3, 'perpetual|not affected|unaffected|continu|never end|surviv|goes on|carries on|keeps going|keeps existing|go on existing|even if member|even when member|regardless', min=1)], 'c1'),
        V('v2', 'Define a Government company under the Companies Act, 2013.',
          'Under section 2(45), a Government company is one where at least fifty-one per cent of its paid-up share capital is owned by the Central Government, by one or more State Governments, or by the Central and State Governments together. A subsidiary of such a Government company is also a Government company.',
          [P('p1', 'At least 51% of the paid-up share capital', 5, '51|fifty one', 'paid up|share capital|capital', min=2),
           P('p2', 'Held by the Central Government and/or State Government(s), alone or together', 3, 'central', 'state'),
           P('p3', 'Includes a subsidiary of a Government company', 2, 'subsidiar')], 'c3'),
        V('v3', 'What are the three restrictions that a private company must place in its articles?',
          'A private company must, by its articles, first restrict the right to transfer its shares; second, limit its members to two hundred, except in a One Person Company, not counting present and past employees who are members; and third, prohibit any invitation to the public to subscribe for its securities.',
          [P('p1', 'Restricts the right to transfer its shares', 3, ALT('{r} transfer', 'transfer {r}', r=('restrict', 'restriction', 'limit', 'limits', 'restricted'))),
           P('p2', 'Limits members to 200 (excluding employee-members; OPC excepted)', 4, '200|two hundred|cannot have more than 200|not more than 200|no more than 200|cannot exceed 200|cannot have more than two hundred|not more than two hundred|no more than two hundred|not exceed 200'),
           P('p3', 'Prohibits invitation to the public to subscribe for its securities', 3, 'prohibit invitation public|prohibit public|prohibits public|prohibit inviting public|cannot invite public|can not invite public|not invite public|no invitation public|no public invitation|bar public|forbid public|not allowed invite public|cannot ask public|not ask public|cannot approach public|not approach public|cannot call public|public not invited|public cannot be invited')], 'c4'),
        V('v4', 'What does section 128 require about the books of account of a company?',
          'Section 128 requires every company to prepare and keep books of account for every financial year at its registered office. The books must show a true and fair picture of the company\'s affairs, including branches, and must be kept on the accrual basis and according to the double entry system. They may also be kept in electronic mode.',
          [P('p1', 'Kept at the registered office', 3, 'registered office'),
           P('p2', 'Give a true and fair view (including branches)', 2, 'true and fair|true fair|true'),
           P('p3', 'Accrual basis and double entry system', 4, 'accrual|mercantile', 'double entry'),
           P('p4', 'May be kept in electronic mode', 1, 'electronic|digital|computer|soft copy')], 'c6'),
        V('v5', 'What do financial statements include under section 2(40), and which companies may leave out the cash flow statement?',
          'Under section 2(40), financial statements include a balance sheet at the end of the year, a profit and loss account or an income and expenditure account, a cash flow statement, a statement of changes in equity if applicable, and explanatory notes. A One Person Company, a small company and a dormant company may leave out the cash flow statement.',
          [P('p1', 'Balance sheet and profit and loss account (or income and expenditure account)', 3, 'balance sheet', 'profit loss|profit and loss|income and expenditure|income expenditure', min=2),
           P('p2', 'Cash flow statement, statement of changes in equity (if applicable) and notes', 3, 'cash flow', 'change in equity|changes in equity|equity', 'note|explanatory', min=2),
           P('p3', 'OPC, small company and dormant company may omit the cash flow statement', 4, 'one person|opc', 'small', 'dormant', min=2)], 'c7'),
    ]

    cases = [{
        'id': 'k1', 'title': 'Sarthak Agro — choosing and presenting', 'difficulty': 'moderate',
        'case': ('Sarthak Agro Pvt Ltd was incorporated in 2024. Its articles restrict share transfers and bar any public invitation for securities. It has 140 members, of whom '
                 '25 are employees. Its paid-up capital is ₹3 crore and its turnover for 2025-26 was ₹42 crore; it is not a holding or subsidiary company. On 31 March 2027 its '
                 'ledger shows, among others: 20,000 equity shares of ₹100 each, ₹80 called up; calls unpaid on 600 shares at ₹30 per share; securities premium ₹1,50,000; '
                 'and 9% debentures of ₹5,00,000 repayable in 2032.'),
        'mcqs': [
            M('k1a', 'Which description fits Sarthak Agro Pvt Ltd for 2026-27?', ['A private company that is also a small company', 'A public company because it has more than 50 members', 'A listed company', 'A Government company'], 0,
              'It meets all three private-company conditions (and 140 members is within 200 anyway). Paid-up capital ₹3 crore ≤ ₹10 crore and turnover ₹42 crore ≤ ₹100 crore, and it is not a holding or subsidiary — so it is also a small company.', 'moderate'),
            M('k1b', 'What paid-up share capital will appear on the face of the balance sheet?', [R(20000 * 80 - 600 * 30), R(1600000), R(2000000), R(1600000 + 18000)], 0,
              'Called up 20,000 × ₹80 = ₹16,00,000, less calls unpaid 600 × ₹30 = ₹18,000. Paid-up = ₹15,82,000.', 'moderate', '20000*80-600*30'),
            M('k1c', 'Under which head will the 9% debentures appear?', ['Non-current liabilities — Long-term borrowings', 'Shareholders\' funds — Share capital', 'Current liabilities — Short-term borrowings', 'Reserves and surplus'], 0,
              'Debentures repayable after more than 12 months are long-term borrowings (sub-head bonds/debentures).', 'core'),
            M('k1d', 'Which statement may Sarthak Agro leave out of its financial statements?', ['The cash flow statement', 'The balance sheet', 'The notes to accounts', 'The statement of profit and loss'], 0,
              'Section 2(40) allows a One Person Company, a small company and a dormant company to omit the cash flow statement.', 'core'),
        ]}]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p1', 'chapter': 'fnd-p1-ch11', 'n': 1,
        'title': 'Introduction to Company Accounts',
        'outcomes': [
            'Explain what a company is in law and why the company form suits large businesses.',
            'List and explain the salient features of a company, including the present position on the common seal.',
            'Identify the main types of companies under the Companies Act, 2013 (Government, foreign, private, public, OPC, small, listed, unlimited, limited by shares or guarantee, holding and subsidiary) and apply their tests to facts.',
            'State the requirements of section 128 on books of account and section 129 / section 2(40) on financial statements.',
            'Place common items under the correct heads of the Division I, Schedule III balance sheet and statement of profit and loss.',
        ],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 40, 'practice': 45}, 'prereq': ['fnd-p1-ch01-u01'],
                 'exam_tip': 'Theory from this unit appears as short notes, true/false with reasons and "distinguish" questions; the Schedule III format is needed in every company-accounts problem that asks for a balance sheet.'},
        'concepts': [
            {'id': 'c1', 'title': 'Why companies exist, and what "company" means in law',
             'body': ['Big projects — a steel plant, an airline, a software platform — need more money and more people than a sole trader or a partnership can bring together. The company form lets thousands of investors pool money while professional managers run the business.',
                      'The word comes from the Latin "com" (together) and "panis" (bread) — people sharing a meal. In law, a company is one formed and incorporated under the Companies Act, 2013, or registered under an earlier company law.',
                      'Once incorporated, it is an artificial person: it has its own name, owns property, signs contracts and can sue or be sued. Judges have described it as an artificial being that exists only in the eyes of the law and has perpetual succession.'],
             'analogy': 'A company is like a cricket franchise: players and owners change every season, but the team keeps its name, its contracts and its trophies.',
             'work': 'When a client asks "Should I convert my firm into a company?", a CA explains limited liability, easier fund-raising and continuity — and also the extra compliance (audit, filings, Schedule III accounts) that comes with it.'},
            {'id': 'c2', 'title': 'Salient features of a company',
             'body': ['Incorporated association — it comes into existence only by registration under the Act. Separate legal entity — it is distinct from its members, so it contracts and is sued in its own name. Perpetual existence — death, insolvency or change of members does not end it.',
                      'Common seal — earlier essential for signing documents; it is now optional. Documents that needed the seal may instead be signed by two directors, or by one director and the company secretary. Every company gets a Corporate Identification Number (CIN) from the Registrar of Companies.',
                      'Limited liability — a member is liable only for the amount unpaid on his shares; once shares are fully paid, nothing more can be demanded. Ownership is separate from management — shareholders elect a board that runs the business.',
                      'Other features — a company is not a citizen (it has legal existence but no citizenship rights); shares are transferable (a private company restricts this); it must keep prescribed books, get them audited periodically by chartered accountants appointed by the shareholders, and give members access to information through meetings and reports (inspection of books beyond what the statute allows is governed by the articles).'],
             'analogy': 'Limited liability works like a fixed ticket price: once you have paid for your ticket (your shares), the organiser cannot ask you to pay for the stadium\'s debts.',
             'work': 'Bankers and creditors look beyond the promoters to the company\'s own assets because of the separate-entity rule — which is why they often ask directors for personal guarantees. Explaining this is a routine part of loan advisory work.'},
            {'id': 'c3', 'title': 'Types of companies (1): by control — Government, foreign, holding and subsidiary',
             'body': ['Government company — s. 2(45): the Central Government, one or more State Governments, or the Centre and the States together own not less than 51% of its paid-up share capital. A subsidiary of a Government company is also a Government company.',
                      'Foreign company — s. 2(42): incorporated outside India, having a place of business in India (itself, through an agent, physically or electronically) and carrying on business activity in India in any other manner.',
                      'Holding and subsidiary — s. 2(46) and 2(87): Company H is the holding company of S if H controls the composition of S\'s board of directors (power to appoint or remove most or all of the directors), or exercises or controls more than one-half of S\'s total share capital, alone or together with its other subsidiaries. Control through another subsidiary (indirect control) also counts. Note: the study material (and the exam) uses "more than one-half of the total share capital"; since 7 May 2018 the Act itself (as amended by the Companies (Amendment) Act, 2017) reads "more than one-half of the total voting power". For ordinary equity shares carrying one vote each, both tests give the same answer.'],
             'analogy': 'Holding and subsidiary are like a parent and child on a family plan: the parent decides who is in charge of the child\'s account.',
             'work': 'Group structure decides whether consolidated accounts are needed and which related-party disclosures apply. Auditors map holding–subsidiary chains at the start of every group audit.'},
            {'id': 'c4', 'title': 'Types of companies (2): by public access and size — private, public, OPC, small, listed',
             'body': ['Private company — s. 2(68): its articles (i) restrict the right to transfer shares, (ii) limit members to 200 (except a One Person Company) — joint holders count as one, and present employees, and former employees who were members while employed and continue as members, are not counted — and (iii) prohibit any invitation to the public to subscribe for its securities. Its shares are not listed.',
                      'Public company — s. 2(71): a company that is not a private company. If a private company becomes the subsidiary of a public company, it counts as public for the Act even though its articles still say private. A listed public company that gets delisted remains public. The old minimum paid-up capital (₹1 lakh private, ₹5 lakh public) has been removed.',
                      'One Person Company — s. 2(62): only one person as member. Small company — s. 2(85): a company other than a public company whose paid-up capital does not exceed ₹10 crore and whose turnover for the preceding year does not exceed ₹100 crore (as given in the study material); a holding or subsidiary company, a section 8 company or a company under a special Act cannot be a small company.',
                      'Listed company — s. 2(52): any of its securities are listed on a recognised stock exchange. A company with no securities listed is unlisted — and an unlisted company may be public or private. So not every public company is listed.'],
             'analogy': 'A private company is a members-only club with a guest list and no public ticket counter; a listed company sells tickets at the stock exchange window.',
             'work': 'Small companies and OPCs enjoy lighter compliance (for example, no cash flow statement). Testing both the capital and the turnover limit every year is a common CA task — crossing either one changes the reporting obligations.'},
            {'id': 'c5', 'title': 'Types of companies (3): by liability — shares, guarantee, unlimited',
             'body': ['Company limited by shares — s. 2(22): the memorandum caps each member\'s liability at whatever is still unpaid on his shares. This is the usual form for business companies.',
                      'Company limited by guarantee — s. 2(21): members promise in the memorandum to contribute a fixed amount to the company\'s assets if it is wound up. Common for clubs, chambers of commerce and charitable bodies.',
                      'Unlimited company — s. 2(92): no limit on the members\' liability.'],
             'analogy': 'Shares = you pay what is left on your ticket; guarantee = you promise a fixed amount only if the show closes; unlimited = you are on the hook for everything.',
             'work': 'In a winding up the liquidator calls on members according to these limits — an auditor or insolvency professional must read the memorandum first.'},
            {'id': 'c6', 'title': 'Maintenance of books of account — section 128',
             'body': ['For every financial year, every company must maintain books of account, related books and papers and its financial statements, and keep them at its registered office.',
                      'They must show a true and fair picture of the company\'s affairs, branch offices included, and explain transactions at the registered office and branches.',
                      'Books must be kept on the accrual basis and under the double entry system. They may be kept in electronic mode as prescribed.'],
             'analogy': 'The registered office is the company\'s home address — the law wants its diary (the books) kept at home, whether on paper or on a server.',
             'work': 'A company that keeps books on a cash basis breaks section 128 — an auditor would report it. Statutory auditors also check where the books (or their electronic back-up) are kept.'},
            {'id': 'c7', 'title': 'Preparation of financial statements — section 129, section 2(40) and Schedule III',
             'body': ['Section 129: financial statements must present a true and fair picture, comply with the notified accounting standards and be in the form prescribed in Schedule III. The board lays them before every annual general meeting.',
                      'Section 2(40): financial statements include (i) balance sheet at the year end, (ii) profit and loss account (income and expenditure account for a not-for-profit company), (iii) cash flow statement, (iv) statement of changes in equity, if applicable, and (v) explanatory notes. A One Person Company, small company and dormant company may omit the cash flow statement.',
                      'Insurance, banking and electricity companies, and any class for which another Act prescribes a format, follow that Act. All others follow Schedule III: Division I — companies applying the notified Accounting Standards; Division II — companies applying Ind AS; Division III — NBFCs applying Ind AS. Each division has Part I (balance sheet) and Part II (statement of profit and loss). Foundation uses Division I.'],
             'analogy': 'Schedule III is a standard exam answer sheet: everyone writes in the same boxes, so the examiner (investor) can compare answers quickly.',
             'work': 'Converting a trial balance into Schedule III statements — grouping ledgers, splitting current and non-current, writing notes — is the core of year-end finalisation work in any CA firm.'},
            {'id': 'c8', 'title': 'The Division I balance sheet and statement of profit and loss',
             'body': ['Balance sheet, Equity and Liabilities side: 1. Shareholders\' funds — share capital, reserves and surplus, money received against share warrants; 2. Share application money pending allotment; 3. Non-current liabilities — long-term borrowings, deferred tax liabilities (net), other long-term liabilities, long-term provisions; 4. Current liabilities — short-term borrowings, trade payables (MSE dues shown separately), other current liabilities, short-term provisions.',
                      'Assets side: 1. Non-current assets — property, plant and equipment and intangible assets (PPE, intangible assets, capital work-in-progress, intangible assets under development), non-current investments, deferred tax assets (net), long-term loans and advances, other non-current assets; 2. Current assets — current investments, inventories, trade receivables, cash and cash equivalents, short-term loans and advances, other current assets.',
                      'Share capital note shows, for each class: shares authorised; issued, subscribed and fully paid / not fully paid; par value; reconciliation of shares at the start and end of the year; calls unpaid; forfeited shares. Only paid-up capital enters the total. Reserves and surplus sub-heads include capital reserve, capital redemption reserve, securities premium, debenture redemption reserve, revaluation reserve, share options outstanding, surplus and other reserves.',
                      'Statement of profit and loss: Revenue from operations + Other income = Total income; less expenses (materials consumed, purchases of stock-in-trade, changes in inventories, employee benefits, finance costs, depreciation and amortisation, other expenses); then exceptional and extraordinary items, tax, profit from continuing and discontinuing operations, and basic and diluted earnings per share.'],
             'blocks': [bs1],
             'analogy': 'The balance sheet reads like a family\'s list: "where the money came from" on top (owners, long-term lenders, short-term dues) and "where it is now" below (long-life assets, then items that turn into cash within a year).',
             'work': 'Misclassifying the current portion of a term loan as non-current makes liquidity ratios look better than they are — lenders and auditors check this split carefully.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Balance sheet of a company in Schedule III format', 'difficulty': 'moderate', 'minutes': 15,
             'q': 'From the following balances of Nirmal Polymers Ltd on 31 March 2027, prepare the balance sheet as per Schedule III (Division I) with notes: Equity share capital — 50,000 shares of ₹10 each fully paid (authorised 1,20,000 shares) ₹5,00,000; Securities premium ₹60,000; General reserve ₹1,20,000; Surplus (profit and loss) ₹85,000; 10% Debentures ₹2,00,000; Trade payables ₹95,000; Outstanding salary ₹15,000; Provision for tax ₹30,000; Land ₹2,50,000; Plant ₹3,10,000; Goodwill ₹40,000; Non-current investments ₹1,00,000; Inventories ₹1,25,000; Trade receivables ₹90,000; Balance with bank ₹1,75,000; Cash in hand ₹15,000.',
             'solution': [bs1, notes1, wn('Totals', f'Equity and liabilities = {inr(sc)} + {inr(rs)} + 2,00,000 + 95,000 + 15,000 + 30,000 = ₹{inr(el)}. Assets = {inr(ppe)} + 40,000 + 1,00,000 + 1,25,000 + 90,000 + {inr(cash)} = ₹{inr(asst)}.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Share capital note when calls are unpaid', 'difficulty': 'core', 'minutes': 8,
             'q': 'Vedika Paints Ltd has an authorised capital of 2,00,000 equity shares of ₹10 each. It offered 1,20,000 shares to the public, received applications for 1,50,000 shares, allotted 1,20,000 shares and returned the excess money. By 31 March 2027 it had called ₹8 per share. All money was received except from one holder of 3,000 shares, who paid only ₹5 per share. Show the share capital note and the balance sheet extract (all money is in the bank).',
             'solution': [note2, bs2, wn('Working', f'Called up = 1,20,000 × ₹8 = ₹{inr(called)}. Calls unpaid = 3,000 × (8 − 5) = ₹{inr(unpaid)}. Paid-up = ₹{inr(paid)}.'),
                          note('Authorised, issued and subscribed figures are disclosed in the note but are not added into the balance sheet total — only paid-up capital is.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Applying the definitions: which type of company?', 'difficulty': 'core', 'minutes': 8,
             'q': 'Classify each company: (a) Ankur Seeds Ltd — Central Government 30% and a State Government 25% of paid-up capital; (b) Kiran Ltd — Delta Ltd holds 8,000 of its 15,000 shares; (c) Pixel Prints Pvt Ltd — paid-up ₹6 crore, turnover ₹80 crore, not in a group; (d) Orbit Tools Pvt Ltd — paid-up ₹4 crore, turnover ₹120 crore; (e) Zenith Motors Inc. — incorporated in Japan with a sales office in Pune; (f) Sonal Exports (OPC) Pvt Ltd — one member.',
             'solution': [cls, note('For a Government company the holdings of the Central and State Governments are added. For a small company both limits must be satisfied together.')],
             'checks': c3},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'First finalisation: grouping a trial balance into Schedule III', 'role': 'Articled assistant in a CA firm (accounts finalisation of a manufacturing company)',
             'situation': 'Your manager hands you the trial balance of a private company and asks for a draft Schedule III balance sheet. The ledger has a "Term loan — HDFC" of ₹30 lakh, of which ₹6 lakh is repayable in the next 12 months, a "Calls in arrears" balance and an "Unpaid dividend" account.',
             'steps': ['Map each ledger to a Schedule III head and sub-head; keep a mapping sheet so it can be reviewed.',
                       'Split the term loan: ₹24 lakh under long-term borrowings, ₹6 lakh as current maturities of long-term borrowings under short-term borrowings.',
                       'Deduct calls in arrears from called-up capital inside the share capital note — do not show it as an asset.',
                       'Show unpaid dividend under other current liabilities.',
                       'Check that the share capital note gives authorised, issued, subscribed, called-up and paid-up figures and the reconciliation of number of shares.'],
             'takeaway': 'Schedule III is not just a format — the current/non-current split and the notes change how lenders and investors read the company.',
             'think': 'Why is calls in arrears not shown as a current asset (a receivable)?',
             'answer': 'Because it is capital that was called but never received; Schedule III requires paid-up capital to be shown, so unpaid calls are deducted from called-up capital.'},
            {'id': 'j2', 'title': 'Advising a founder on the right type of company', 'role': 'Practising CA advising a start-up founder',
             'situation': 'A founder plans to start alone, later bring in 10 friends as investors, and perhaps list in 8 years. She asks whether to form an OPC, a private company or a public company.',
             'steps': ['Explain an OPC: one member, lighter compliance, but it must convert if more members join.',
                       'Explain a private company: up to 200 members, share transfers restricted, no public invitation — suits friends-and-family funding.',
                       'Explain a public company and listing: needed to raise money from the public; heavier compliance and disclosure.',
                       'Point out that a private company can later convert into a public company before an IPO.',
                       'Mention small-company relief while capital and turnover stay within the limits.'],
             'takeaway': 'The type of company drives compliance cost, fund-raising options and even the format of financial statements.',
             'think': 'If the founder\'s private company becomes a subsidiary of a public company, what is its status?',
             'answer': 'It is deemed to be a public company under the proviso to s. 2(71), even if its articles still call it private.'},
        ],
        'mcqs': [
            mcq('m1', 'A company in which the Central Government holds 26% and two State Governments together hold 27% of the paid-up share capital is:', ['A Government company', 'Not a Government company, because no single government holds 51%', 'A foreign company', 'A small company'], 0,
                'Section 2(45) counts holdings of the Central and State Governments together: 26% + 27% = 53%, which is not less than 51%.', 'c3', 'moderate'),
            mcq('m2', 'A company incorporated in Singapore that has an office in Chennai and does business in India is:', ['A foreign company', 'A Government company', 'A subsidiary company', 'A private company'], 0,
                'Section 2(42): incorporated outside India, with a place of business and business activity in India.', 'c3'),
            mcq('m3', 'Which of the following is NOT a condition in the articles of a private company?', ['It may invite the public to subscribe for its shares', 'It restricts the right to transfer its shares', 'It limits its members to 200 (except an OPC)', 'It prohibits invitation to the public to subscribe for securities'], 0,
                'A private company must prohibit public invitation; the other three are its conditions.', 'c4'),
            mcq('m4', 'Which statement is correct?', ['An unlisted company may be either public or private', 'Every public company is a listed company', 'A private company can list its equity shares', 'A listed company that is delisted becomes a private company'], 0,
                'Listing is about securities on a recognised stock exchange; many public companies are unlisted, and a delisted public company stays public.', 'c4', 'moderate'),
            mcq('m5', 'A private company (not part of any group) has paid-up capital of ₹8 crore and turnover of ₹105 crore. As per the limits in the study material it is:', ['Not a small company, because turnover exceeds ₹100 crore', 'A small company, because paid-up capital is within ₹10 crore', 'A small company, because it is private', 'A One Person Company'], 0,
                'Both conditions must be met: paid-up capital ≤ ₹10 crore AND turnover ≤ ₹100 crore. Turnover fails.', 'c4', 'moderate'),
            mcq('m6', 'Books of account of a company must be kept at:', ['Its registered office', 'The office of its statutory auditor', 'The residence of the managing director', 'Its largest branch'], 0,
                'Section 128 requires books to be kept at the registered office (electronic mode is allowed).', 'c6'),
            mcq('m7', 'Under section 128, books of account must be maintained on:', ['Accrual basis under the double entry system', 'Cash basis under the double entry system', 'Cash or accrual basis, as the board decides', 'Single entry, if the company is small'], 0,
                'Accrual basis and double entry are both mandatory for every company.', 'c6'),
            mcq('m8', 'Which companies may omit the cash flow statement from their financial statements?', ['One Person Company, small company and dormant company', 'All private companies', 'Listed companies', 'Government companies'], 0,
                'The proviso to s. 2(40) gives this relief only to OPCs, small companies and dormant companies.', 'c7'),
            mcq('m9', 'Division II of Schedule III applies to:', ['Companies required to follow Ind AS (other than NBFCs)', 'Companies following the notified Accounting Standards', 'NBFCs following Ind AS', 'Banking companies'], 0,
                'Division I — Accounting Standards; Division II — Ind AS companies; Division III — NBFCs on Ind AS.', 'c7', 'moderate'),
            mcq('m10', 'Called-up capital ₹9,00,000; calls unpaid ₹12,000. The share capital shown in the balance sheet total is:', ['₹8,88,000', '₹9,00,000', '₹9,12,000', '₹12,000'], 0,
                'Paid-up capital = called up − calls unpaid = 9,00,000 − 12,000.', 'c8', 'core', '900000-12000'),
            mcq('m11', 'Securities premium is shown in the balance sheet under:', ['Shareholders\' funds — Reserves and surplus', 'Shareholders\' funds — Share capital', 'Non-current liabilities', 'Other current liabilities'], 0,
                'Securities premium is a capital reserve-type balance shown under reserves and surplus, not as share capital.', 'c8'),
            mcq('m12', 'Use of the common seal under the Companies Act today is:', ['Optional; documents may be signed by two directors or a director and the company secretary', 'Compulsory on every document', 'Compulsory only for private companies', 'Abolished, and no company may have a seal'], 0,
                'The seal is optional. Where a document needed the seal, two directors or one director and the CS may sign instead.', 'c2', 'moderate'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
             'q': 'Explain any five salient features of a company.',
             'model': [ul(['Incorporated association: a company exists only after registration under the Companies Act, 2013; it is an artificial legal person created by law.',
                           'Separate legal entity: it is distinct from its members, so it owns property, makes contracts and sues or is sued in its own name.',
                           'Perpetual existence: death, insolvency or change of members does not affect its existence.',
                           'Limited liability: a member\'s liability is limited to the amount unpaid on his shares; fully paid shares carry no further liability.',
                           'Separation of ownership and management: shareholders elect a board of directors which manages the company.',
                           'Also acceptable: common seal (now optional — two directors or a director and CS may sign), transferability of shares (restricted in a private company), statutory books, periodic audit, right of access to information, not a citizen.'])],
             'scheme': [S('s1', 'Feature 1 named and explained', 1, 'concept'), S('s2', 'Feature 2 named and explained', 1, 'concept'), S('s3', 'Feature 3 named and explained', 1, 'concept'),
                        S('s4', 'Feature 4 named and explained', 1, 'concept'), S('s5', 'Feature 5 named and explained', 1, 'concept')],
             'remarks': ['Half a mark is lost when a feature is only named — each needs one line of explanation.', 'Many candidates still write that the common seal is compulsory; the current position is that it is optional.'],
             'mistakes': ['Saying members have unlimited liability.', 'Saying a private company\'s shares are freely transferable.', 'Writing the same point twice under two headings (separate entity and perpetual existence are different features).'],
             'tips': ['Use a bold heading for each feature followed by one or two lines.', 'Write exactly the number asked; extra points earn nothing but take time.']},
            {'id': 'q2', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Sparsh Textiles Ltd has an authorised capital of 1,50,000 equity shares of ₹10 each. It issued 80,000 shares, all of which were subscribed. Up to 31 March 2027, ₹7 per share has been called. All calls have been received except from one shareholder holding 2,500 shares, who has not paid the last call of ₹2 per share. Prepare the balance sheet (only the share capital and cash items) and the share capital note as per Schedule III.',
             'model': [table(['Particulars', '₹', '₹'], [
                 ['Authorised: 1,50,000 equity shares of ₹10 each', inr(q2_auth), ''],
                 ['Issued and subscribed: 80,000 equity shares of ₹10 each', inr(q2_iss), ''],
                 ['Called up: 80,000 equity shares of ₹10 each, ₹7 called', inr(q2_called), ''],
                 ['Less: Calls unpaid (2,500 × ₹2)', '(' + inr(q2_unpaid) + ')', inr(q2_paid)],
             ], title='Note 1 — Share capital'),
                 table(['Particulars', 'Note', '₹'], [
                     ['Shareholders\' funds — Share capital', '1', inr(q2_paid)], ['Total', '', inr(q2_paid)],
                     ['Current assets — Cash and cash equivalents', '2', inr(q2_paid)], ['Total', '', inr(q2_paid)]], title='Balance Sheet of Sparsh Textiles Ltd as at 31 March 2027 (extract)')],
             'checks': q2c,
             'scheme': [S('s1', 'Authorised, issued and subscribed capital disclosed in the note', 1.5, 'presentation'),
                        S('s2', 'Called-up capital ₹5,60,000 computed', 1, 'computation'),
                        S('s3', 'Calls unpaid ₹5,000 deducted', 1, 'computation'),
                        S('s4', 'Paid-up ₹5,55,000 shown under shareholders\' funds', 1, 'classification'),
                        S('s5', 'Cash and cash equivalents ₹5,55,000 under current assets; Schedule III headings and note reference', 1.5, 'presentation')],
             'remarks': ['Most errors come from adding authorised or issued capital into the total.', 'Some candidates show calls unpaid as a current asset — it must be deducted from called-up capital.'],
             'mistakes': ['Showing ₹5,60,000 as share capital and ₹5,000 as a receivable.', 'Omitting the note reference column.', 'Calling it "Share Capital A/c" in the balance sheet — use Schedule III wording.'],
             'tips': ['Put all capital details in the note and only the paid-up figure on the face.', 'Show the deduction in brackets in the inner column and the net figure outside.']},
            {'id': 'q3', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'Under which head and sub-head of the Schedule III (Division I) balance sheet will each item be shown? (i) Calls in arrears (ii) Securities premium (iii) 12% Debentures repayable after 6 years (iv) Instalment of a term loan payable within 12 months (v) Unpaid dividend (vi) Provision for gratuity (vii) Computer software (viii) Loose tools (ix) Share application money pending allotment (x) Cheques in hand.',
             'model': [table(['Item', 'Head / sub-head'], q3rows)],
             'scheme': [S(f's{i + 1}', f'Item ({["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"][i]}) correctly placed', 0.5, 'classification') for i in range(10)],
             'remarks': ['Items (iv) and (ix) separate strong answers from average ones.', 'Writing only "liability" or "asset" earns nothing — the head and sub-head are needed.'],
             'mistakes': ['Showing loose tools as PPE.', 'Treating share application money pending allotment as share capital.', 'Showing the current instalment of a long-term loan under long-term borrowings.'],
             'tips': ['Answer in a two-column table: item | head — sub-head.', 'Remember the 12-month test for current vs non-current.']},
            {'id': 'q4', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'table',
             'q': 'Distinguish between a private company and a public company (any four points).',
             'model': [table(['Basis', 'Private company', 'Public company'], [
                 ['Definition', 's. 2(68) — articles restrict transfer, limit members, prohibit public invitation', 's. 2(71) — not a private company'],
                 ['Number of members', 'Maximum 200 (employee-members excluded); OPC has one', 'No maximum limit'],
                 ['Transfer of shares', 'Restricted by the articles', 'Freely transferable'],
                 ['Invitation to public', 'Prohibited', 'May invite the public through a prospectus'],
                 ['Listing', 'Shares are not listed', 'May list its securities on a recognised stock exchange'],
                 ['Subsidiary status', '—', 'A subsidiary of a public company is deemed public even if its articles say private'],
             ])],
             'scheme': [S('s1', 'Point 1 with both sides', 1, 'concept'), S('s2', 'Point 2 with both sides', 1, 'concept'), S('s3', 'Point 3 with both sides', 1, 'concept'), S('s4', 'Point 4 with both sides', 1, 'concept')],
             'remarks': ['Strong answers quote the section numbers and the 200-member limit correctly.'],
             'mistakes': ['Writing that a public company must have minimum paid-up capital of ₹5 lakh — this requirement no longer exists.', 'Saying a private company may have 50 members (an outdated limit).'],
             'tips': ['Use a three-column table: basis | private | public.']},
        ],
        'viva': viva,
        'cases': cases,
        'revision': {
            'summary': ['A company is incorporated under the Companies Act, 2013 (or earlier law): an artificial person, separate from its members, with perpetual succession.',
                        'Features: incorporated association, separate entity, perpetual existence, common seal (optional now), limited liability, ownership separate from management, not a citizen, transferable shares, statutory books, periodic audit, access to information.',
                        'Types: Government (≥51% paid-up capital with governments), foreign, private (restrict transfer, ≤200 members, no public invitation), public, OPC, small (₹10 crore capital and ₹100 crore turnover as per material), listed, unlimited, limited by shares or guarantee, holding and subsidiary (board control or > ½ total share capital).',
                        'Section 128: books at registered office, true and fair, accrual basis, double entry; electronic mode allowed.',
                        'Section 129 + 2(40): balance sheet, P&L, cash flow (not needed for OPC/small/dormant), SOCE if applicable, notes; formats in Schedule III Division I/II/III.'],
            'remember': ['Only paid-up capital enters the balance sheet total; authorised, issued and subscribed are disclosed in the note.', 'Calls unpaid are deducted from called-up capital.', 'Securities premium, CRR, DRR, capital reserve, revaluation reserve → Reserves and surplus.', 'Share application money pending allotment is a separate head between shareholders\' funds and non-current liabilities.'],
            'traps': ['Not every public company is listed.', 'Government holdings — Central and State — are added for the 51% test.', 'Small company needs BOTH limits; a public, holding or subsidiary company can never be small.', 'The common seal is optional, not compulsory.'],
        },
        'quickref': [
            {'k': 'Government company', 'v': 's. 2(45) — ≥51% paid-up share capital held by Central and/or State Government(s); includes its subsidiary'},
            {'k': 'Foreign company', 'v': 's. 2(42) — incorporated outside India; place of business and business activity in India'},
            {'k': 'Private company', 'v': 's. 2(68) — restricts transfer; ≤200 members (except OPC); prohibits public invitation'},
            {'k': 'Public company', 'v': 's. 2(71) — not private; subsidiary of a public company is deemed public'},
            {'k': 'OPC / Small / Listed', 'v': 's. 2(62) one member · s. 2(85) paid-up ≤ ₹10 crore and turnover ≤ ₹100 crore (not public/holding/subsidiary/s.8) · s. 2(52) securities listed'},
            {'k': 'Liability types', 'v': 's. 2(22) limited by shares · s. 2(21) limited by guarantee · s. 2(92) unlimited'},
            {'k': 'Holding / subsidiary', 'v': 's. 2(46), 2(87) — controls board composition or > one-half of total share capital as per study material (the amended Act says total voting power); direct or through subsidiaries'},
            {'k': 'Books of account', 'v': 's. 128 — registered office, accrual, double entry, true and fair, electronic allowed'},
            {'k': 'Financial statements', 'v': 's. 129 and s. 2(40) — BS, P&L, CFS (not for OPC/small/dormant), SOCE if applicable, notes; Schedule III'},
            {'k': 'Paid-up capital', 'v': 'Called-up capital − calls unpaid (calls in advance are not part of share capital)'},
        ],
    }
