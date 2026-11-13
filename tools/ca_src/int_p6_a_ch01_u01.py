"""CA Intermediate · Paper 6A Financial Management · Chapter 1 Scope and Objectives of Financial Management.
Scope follows the ICAI study material; explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p6-a-ch01-u01'
T1 = 'What financial management means'
T2 = 'How the subject evolved'
T3 = 'The three finance decisions'
T4 = 'Importance and scope'
T5 = 'Profit maximisation vs wealth maximisation'
T6 = 'Role of the finance executive (CFO)'
T7 = 'Financial distress and insolvency'
T8 = 'Finance, accounting and other disciplines'
T9 = 'Agency problem and agency cost'


def build():
    ck = Checks()
    pa = ck.add('600000+600000', 'Project A: total accounting profit (₹6 lakh in years 1 and 2)')
    pb = ck.add('0+1300000', 'Project B: total profit (all in year 2)')
    pva = ck.add('round(600000/1.12+600000/1.12**2)', 'Project A: present value at 12%')
    pvb = ck.add('round(1300000/1.12**2)', 'Project B: present value at 12%')
    i1 = {'id': 'i1', 'title': 'Why timing makes profit a poor yardstick', 'difficulty': 'core', 'minutes': 7,
          'q': 'Kalyani Ltd. can choose one of two projects of equal risk costing the same. Project A gives cash profit of ₹6,00,000 at the end of year 1 and ₹6,00,000 at the end of year 2. Project B gives nothing in year 1 and ₹13,00,000 at the end of year 2. Shareholders require 12%. Which project is better under (a) profit maximisation and (b) wealth maximisation?',
          'solution': [table(['Measure', 'Project A ₹', 'Project B ₹'], [
              ['Total profit (ignores timing)', inr(pa), inr(pb)],
              ['Present value at 12%', inr(pva), inr(pvb)]], title='Comparison'),
              wn('Working', 'A: 6,00,000 ÷ 1.12 + 6,00,000 ÷ 1.12² ; B: 13,00,000 ÷ 1.12².'),
              p(f'(a) Profit maximisation prefers B ({R(pb)} > {R(pa)}). (b) Wealth maximisation prefers A because its present value ({R(pva)}) is higher — money received earlier is worth more. The extra ₹1,00,000 of B does not compensate for waiting a year for the whole amount.')],
          'checks': list(ck)}

    functions = table(['Decision', 'Question it answers', 'Examples'], [
        ['Investment (I)', 'Where should funds be invested?', 'Capital budgeting for fixed assets; working capital levels; inventory and credit policy'],
        ['Financing (F)', 'From where and in what mix should funds be raised?', 'Equity vs debt, capital structure, hedging currency risk'],
        ['Dividend (D)', 'How much of the profit should be distributed and how much retained?', 'Dividend payout, bonus issues, buy-backs'],
        ['Liquidity (short-term)', 'Is there enough cash to meet obligations as they fall due?', 'Cash budgets, credit lines, cash management'],
    ], title='Finance functions — V = f(I, F, D)')
    goals = table(['Goal', 'Advantages', 'Disadvantages'], [
        ['Profit maximisation', 'Easy to compute; clear link between decisions and profit', 'Short-term focus; ignores risk; ignores timing of returns; vague (which profit?)'],
        ['Wealth (value) maximisation', 'Long-term focus; considers risk and timing (present value); reflects shareholders\' return through share price', 'No clear direct link between a decision and the share price; market swings can frustrate managers'],
    ], title='Profit vs wealth maximisation')
    agency = table(['Agency cost', 'Meaning'], [
        ['Monitoring', 'Cost of watching managers — audits, board oversight, reporting systems'],
        ['Bonding', 'Cost managers bear to assure owners — e.g. contracts restricting their actions, guarantees'],
        ['Opportunity', 'Value lost because monitoring rules stop managers from seizing good opportunities quickly'],
        ['Structuring', 'Cost of designing compensation and control structures that align interests'],
    ], title='Four types of agency cost')

    concepts = [
        C('c1', T1, [
            'Financial management is the managerial activity of planning and controlling a firm\'s financial resources — acquiring, financing and managing assets to achieve the firm\'s goal, mainly maximising shareholders\' wealth. Because positive cash flow often matters more than book profit, it is also described as planning the future of the business to keep cash flows positive.',
            'A broader description: forecasting, planning, organising, directing, coordinating and controlling all activities relating to the acquisition and application of an undertaking\'s financial resources, in line with its financial objective.',
            'Two basic aspects: procurement of funds and effective utilisation of funds.',
            'Procurement: funds come from equity (owners\' risk capital, no fixed return), debt (fixed interest, repayment obligation, cheaper because tax-deductible but riskier for the firm), and, increasingly, international sources such as external commercial borrowings, ADRs/GDRs and foreign direct investment. Each source differs in cost, risk and control, so the mix must be chosen carefully.',
            'Utilisation: funds raised at a cost must earn more than that cost — in fixed assets through careful capital budgeting, and in working capital through managing receivables, inventory and cash so that funds are neither idle nor short.'],
          'Financial management is running a household budget on a large scale: decide where the money will come from (salary, loan), where it will go (house, education) and keep enough cash for monthly bills.',
          'A CFO\'s board presentation usually covers exactly these two aspects: the funding plan and how the money will be deployed and earn more than its cost.'),
        C('c2', T2, [
            'Traditional phase: financial management was needed only for occasional events — mergers, expansions, liquidation, takeovers — and decisions were viewed from the angle of outsiders such as lenders and investment bankers.',
            'Transitional phase: attention shifted to the finance manager\'s day-to-day problems — funds analysis, planning and control.',
            'Modern phase (continuing): analytical and decision-oriented — theories on efficient markets, capital budgeting, option pricing, valuation and dividend and capital structure policies, applied to decisions inside the firm.'],
          'Finance moved from being the fire brigade called for big events, to the daily housekeeper, to the strategist at the planning table.',
          'Today\'s finance teams run valuation models and scenario analyses for every major decision — the modern phase in action.'),
        C('c3', T3, [
            'The value of a firm depends on three long-term decisions: V = f(I, F, D).',
            'Investment decision (I): which assets to invest in — through capital budgeting for long-term projects, and policies on working capital (inventory, receivables, cash). Inventory policy is set jointly by production and finance considering requirements, price outlook and fund availability.',
            'Financing decision (F): raising the optimum finance at the lowest cost with acceptable risk — a sound capital structure balancing equity and debt; understanding that profit is useless without cash; evaluating risks such as excessive debt and currency fluctuations, and using hedging (like insuring a shop against fire) to reduce them.',
            'Dividend decision (D): how much of the profit to distribute and how much to retain for growth, keeping shareholders\' expectations, liquidity and future investment needs in view.',
            'Short-term (liquidity) decisions: managing working capital so that current obligations are met — balancing liquidity against profitability.'],
          'I, F and D are three legs of a stool: where to put the money, where to get it, and what to give back to the owners — remove one and the value topples.',
          'Every big corporate announcement — a new plant, a bond issue, a dividend — is one of these three decisions.',
          blocks=[functions]),
        C('c4', T4, [
            'Importance: financial management helps take sound decisions on investment, financing and dividends; improves profitability and value; ensures that funds are available when needed and used efficiently; supports survival and growth; and helps in planning and control through budgets and analysis.',
            'Scope: it draws on economics (micro: demand, pricing, marginal analysis; macro: interest rates, inflation, monetary and fiscal policy), on accounting (data on performance and position), and on other disciplines such as production, marketing, quantitative methods and law.',
            'Key questions it answers: how large should the business be and how fast should it grow? In what form should assets be held? How should funds be raised? How should profits be shared?'],
          'Financial management is the dashboard and the steering of the business car: it shows how fast you are going and decides which way to turn.',
          'Credit-rating agencies essentially assess the quality of a firm\'s financial management.'),
        C('c5', T5, [
            'Profit maximisation: increase the amount of profit. Easy to compute and to link with decisions — but it focuses on the short term, ignores risk and the timing of returns, and "profit" itself is ambiguous (before or after tax, total or per share).',
            'Wealth (value) maximisation: maximise the market value of shares, i.e. the present value of future cash flows to shareholders. It considers long-term gains, risk and timing, and reflects shareholders\' return. Its drawbacks: no clear direct link between a decision and the share price, and price swings can frustrate managers.',
            'Example of conflict: a firm can boost short-term profit by postponing repairs or cutting R&D, which lowers long-term value.',
            'Wealth maximisation is broadly consistent with the interests of employees, creditors and society and with management\'s own survival, so it is the better objective in an uncertain, multi-period world. Where periods are short and uncertainty low, the two objectives practically coincide.'],
          'Profit maximisation counts the harvest; wealth maximisation values the whole orchard, including next year\'s fruit and the risk of a storm.',
          'Investor presentations talk about "shareholder value" and returns above the cost of capital — the language of wealth maximisation.',
          blocks=[goals]),
        C('c6', T6, [
            'Traditional role: raising funds and keeping accounts — the finance executive was mainly a fund-raiser and record-keeper.',
            'Modern role: the CFO is a strategic partner of the CEO — involved in investment decisions, financing mix, dividend policy, working capital, risk management (including hedging), mergers and acquisitions, investor relations, compliance, technology and data-driven decision support. The CFO helps shape and execute strategy, not just report results.',
            'The finance function also coordinates with other departments (production, marketing, HR) because every operational decision has financial consequences.'],
          'The finance executive has moved from being the team\'s treasurer to being its vice-captain.',
          'Many CAs in industry follow this path from controller to CFO, increasingly measured on value creation, not just clean books.'),
        C('c7', T7, [
            'A firm must continuously manage prices, demand, input costs and especially the proportion of debt. Higher debt means higher fixed interest; if cash inflows fall short, creditors press the firm.',
            'Financial distress: cash inflows are inadequate to meet all current obligations. Prolonged distress may force asset sales, often at low prices.',
            'Insolvency: inability to repay debts — the end result of continued financial distress.',
            'So financing decisions must weigh the tax benefit of debt against the risk of distress and insolvency.'],
          'Distress is a high fever; insolvency is when the patient can no longer get out of bed.',
          'Lenders track interest coverage and cash flow cover precisely to spot distress early.'),
        C('c8', T8, [
            'Finance and accounting are closely linked — accounting provides the data finance uses — but they differ in emphasis: accounting recognises revenue and expenses on accrual, while finance focuses on cash flows; accounting mainly collects and presents data, while finance uses data to evaluate and take decisions.',
            'Finance also draws on economics (micro and macro), quantitative methods, production, marketing and law — e.g. marketing\'s sales forecasts feed working-capital plans, and production\'s capacity plans feed capital budgeting.'],
          'Accounting is the camera that records the game; finance is the coach who uses the footage to plan the next move.',
          'In a project appraisal the CA converts accounting profits into cash flows — the bridge between the two disciplines.'),
        C('c9', T9, [
            'In companies, owners (shareholders) are separated from managers. Managers should act for shareholders but may pursue personal goals (salary, perks, empire-building). This principal–agent conflict is the agency problem.',
            'Agency cost is the additional cost shareholders bear to monitor and control managers so that they maximise shareholders\' wealth. It is of four types — monitoring, bonding, opportunity and structuring (table).',
            'Lenders also face an agency problem with managers; it is addressed through negative covenants (e.g. limits on further borrowing). The idea is applied in banks\' credit-risk management, fund raising and valuing distressed companies.',
            'Aligning managers and shareholders: link managerial pay to profits and long-term objectives; employee stock options (ESOPs) tied to share price; and effective monitoring by boards and auditors.'],
          'Owners are like house-owners who hire a caretaker; locks, cameras and performance bonuses cost money but keep the caretaker working for the owner.',
          'Independent directors, statutory audit and ESOP schemes are everyday tools for reducing agency costs.',
          blocks=[agency]),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Explaining the dividend vs growth trade-off', 'role': 'Finance manager briefing the board',
         'situation': 'Shareholders want a higher dividend; the CEO wants to retain profits for a new plant expected to earn 18% against a cost of capital of 13%.',
         'steps': ['Show that retained funds invested above the cost of capital increase share value (wealth maximisation).', 'Check liquidity: can the firm pay a modest dividend and still fund the plant?', 'Recommend a balanced payout and explain it to investors.'],
         'takeaway': 'Dividend, investment and financing decisions are linked — decide them together.'},
        {'id': 'j2', 'title': 'Spotting an agency problem', 'role': 'Audit committee adviser',
         'situation': 'Management proposes an acquisition that increases company size (and management pay) but at a price above estimated value.',
         'steps': ['Identify the agency problem — size-based pay rewards empire-building.', 'Recommend independent valuation and board scrutiny (monitoring cost).', 'Suggest linking pay to return on capital rather than size (structuring).'],
         'takeaway': 'Incentives drive decisions; align them with shareholder value.'},
    ]

    mcqs = [
        Q('m1', 'The two basic aspects of financial management are:', ['Procurement of funds and effective utilisation of funds', 'Recording and reporting of transactions', 'Production and marketing', 'Auditing and taxation'], 0,
          'Financial management is about raising funds from appropriate sources and using them effectively to meet the firm\'s objectives. Recording and reporting describe accounting, which supplies data but is not the core of finance. In practice: every funding plan is matched by a deployment plan showing returns above the cost of funds.', 'c1', T1),
        Q('m2', 'In the expression V = f(I, F, D), D stands for:', ['Dividend decision', 'Debt decision', 'Depreciation decision', 'Diversification decision'], 0,
          'The value of the firm depends on investment (I), financing (F) and dividend (D) decisions. Debt is part of the financing decision, so "debt decision" is the tempting trap. In practice: the dividend decision balances payouts to owners against retention for growth.', 'c3', T3),
        Q('m3', 'Which of these is a financing decision?', ['Deciding the mix of equity and debt', 'Selecting a new plant through capital budgeting', 'Fixing the dividend payout ratio', 'Setting the credit period for customers'], 0,
          'Choosing the capital structure — how much equity and how much debt — is the financing decision. Selecting projects and setting credit policy are investment decisions, and the payout ratio is a dividend decision. In practice: a rights issue versus a term loan is a classic financing decision.', 'c3', T3),
        Q('m4', 'The main criticism of profit maximisation as an objective is that it:', ['Ignores risk and the timing of returns', 'Is impossible to calculate', 'Considers the long term too much', 'Considers cash flows rather than profits'], 0,
          'Profit maximisation looks at the amount of profit but ignores when it is received and how risky it is, and the term profit is itself vague. It is easy to calculate, so that option is wrong, and it is short-term rather than long-term focused. In practice: postponing maintenance raises this year\'s profit but destroys value.', 'c5', T5),
        Q('m5', 'Wealth maximisation means maximising:', ['The market value of the shares — the present value of returns to shareholders', 'The accounting profit for the year', 'The size of the firm\'s assets', 'Sales revenue'], 0,
          'Wealth maximisation aims at the highest market value of shares, which reflects the present value of future returns after considering risk and timing. Accounting profit, asset size and sales are not adjusted for risk and timing. In practice: managers test decisions by asking whether they earn more than the cost of capital.', 'c5', T5),
        Q('m6', 'Project A gives ₹6,00,000 in each of years 1 and 2; Project B gives ₹13,00,000 in year 2 only. At 12%, the project with higher present value is:', ['Project A', 'Project B', 'Both equal', 'Cannot be determined'], 0,
          'PV of A = 6,00,000 ÷ 1.12 + 6,00,000 ÷ 1.2544 ≈ ₹10,14,031; PV of B = 13,00,000 ÷ 1.2544 ≈ ₹10,36,352. Wait — compute carefully: B\'s PV is higher here, so B wins on wealth. This question tests that you actually compute rather than assume earlier money always wins.', 'c5', T5, 'hard'),
        Q('m7', 'In the traditional phase of financial management, the subject was concerned mainly with:', ['Occasional events such as mergers, expansion and liquidation, viewed from outsiders\' angle', 'Day-to-day funds analysis and control', 'Option pricing and efficient markets', 'Managing working capital daily'], 0,
          'In the traditional phase, finance was needed only for special events — mergers, takeovers, expansion, liquidation — and decisions were seen from the viewpoint of lenders and investment bankers. Daily funds analysis belongs to the transitional phase, and theories such as option pricing to the modern phase. In practice: today finance is involved in every major decision, not just events.', 'c2', T2),
        Q('m8', 'Financial distress is best described as a situation where:', ['Cash inflows are inadequate to meet current obligations', 'The firm is legally declared bankrupt', 'Profits are lower than last year', 'The share price falls on a single day'], 0,
          'Financial distress means cash inflows are not enough to meet current obligations; if it continues it may lead to insolvency — the inability to repay debts. Legal bankruptcy is the end stage, not distress itself. In practice: covenant breaches and delayed payments are early signs of distress.', 'c7', T7),
        Q('m9', 'Which is NOT one of the four types of agency cost?', ['Depreciation cost', 'Monitoring cost', 'Bonding cost', 'Structuring cost'], 0,
          'The four agency costs are monitoring, bonding, opportunity and structuring costs. Depreciation is an accounting allocation of asset cost, unrelated to the principal–agent relationship. In practice: audit fees, internal reporting systems and board oversight are all monitoring costs.', 'c9', T9),
        Q('m10', 'The agency problem between lenders and managers is commonly addressed by:', ['Negative covenants, such as limits on further borrowing', 'Paying higher dividends', 'Issuing bonus shares', 'Changing the auditor'], 0,
          'Lenders protect themselves by putting negative covenants in loan agreements — for example forbidding borrowing beyond a limit or restricting asset sales. Higher dividends can actually hurt lenders by taking cash out of the firm. In practice: term-loan agreements contain such covenants and banks monitor them quarterly.', 'c9', T9, 'moderate'),
        Q('m11', 'Linking managers\' pay to the company\'s share price through stock options mainly aims to:', ['Align managers\' interests with shareholders\' interests', 'Reduce the tax liability', 'Increase the firm\'s debt', 'Avoid statutory audit'], 0,
          'Stock options give managers a stake in the share price, aligning their interest with shareholders\' wealth and reducing the agency problem. They do not primarily reduce tax or change debt. In practice: listed companies grant ESOPs with vesting periods to encourage long-term thinking.', 'c9', T9),
        Q('m12', 'Compared with accounting, finance mainly focuses on:', ['Cash flows and decision-making', 'Accrual-based recording only', 'Statutory formats', 'Historical cost of assets'], 0,
          'Accounting recognises revenue and expenses on accrual and presents data; finance focuses on cash flows and uses data to take decisions. Statutory formats and historical cost are accounting concerns. In practice: in project appraisal, depreciation is added back because it is not a cash outflow.', 'c8', T8),
        Q('m13', 'The modern role of the finance executive is best described as:', ['A strategic partner involved in investment, financing, risk and value creation', 'Only a fund raiser', 'Only a record keeper', 'Only a tax filer'], 0,
          'Today\'s CFO works with the CEO on strategy, investments, capital structure, dividends, risk management and value creation. Fund raising and record keeping describe the narrower traditional role. In practice: CFOs lead acquisition evaluations and investor communication.', 'c6', T6),
        Q('m14', 'When the time horizon is short and uncertainty is low:', ['Profit maximisation and wealth maximisation give essentially the same result', 'Profit maximisation is always wrong', 'Wealth maximisation cannot be applied', 'Neither objective applies'], 0,
          'The main weaknesses of profit maximisation — ignoring timing and risk — matter little when the period is short and uncertainty is low, so both objectives lead to much the same decisions. In uncertain multi-period settings wealth maximisation is better. In practice: a one-month trading decision can safely be judged on profit.', 'c5', T5, 'moderate'),
    ]
    # m6: present value comparison — computed answer decides the key
    pvA = 600000 / 1.12 + 600000 / 1.12 ** 2; pvB = 1300000 / 1.12 ** 2
    mcqs[5] = Q('m6', 'Project A gives ₹6,00,000 at the end of each of years 1 and 2; Project B gives ₹13,00,000 at the end of year 2 only. At 12%, which project has the higher present value?',
                ['Project B', 'Project A', 'Both equal', 'Cannot be determined without taxes'], 0 if pvB > pvA else 1,
                f'PV of A = 6,00,000 ÷ 1.12 + 6,00,000 ÷ 1.12² ≈ ₹{inr(round(pvA))}; PV of B = 13,00,000 ÷ 1.12² ≈ ₹{inr(round(pvB))}. B\'s extra ₹1,00,000 more than compensates for waiting, so B has the higher PV here. The trap is assuming earlier money always wins — you must discount and compare. In practice: always compute; intuition about timing can mislead.', 'c5', T5, 'hard')
    i1['solution'][2] = p(f'(a) Profit maximisation prefers B ({R(pb)} > {R(pa)}). (b) Wealth maximisation compares present values: A {R(pva)} vs B {R(pvb)}, so it also prefers {"B" if pvb > pva else "A"} — here the extra ₹1,00,000 of B more than compensates for the one-year wait. Change the rate to 18% and A would win: timing and risk can reverse a profit-based ranking.')
    ck18 = Checks()
    a18 = ck18.add('round(600000/1.18+600000/1.18**2)', 'A at 18%'); b18 = ck18.add('round(1300000/1.18**2)', 'B at 18%')
    i1['solution'].append(wn('At 18%', f'A = {R(a18)}; B = {R(b18)} → {"A" if a18 > b18 else "B"} is preferred.'))
    i1['checks'] += list(ck18)

    questions = [
        W('q1', 5, 'Discuss the conflict between profit maximisation and wealth maximisation. Which is the better objective and why?',
          [goals, p('Profit maximisation can be achieved in the short run at the cost of long-run value — e.g. by postponing repairs or cutting research. Wealth maximisation considers risk, timing (present value) and the long term, and is broadly consistent with the interests of employees, creditors, society and management\'s survival.'),
           p('Hence wealth maximisation is the better objective in an uncertain, multi-period world; where the period is short and uncertainty low, both lead to similar decisions.')],
          [S('s1', 'Profit maximisation — merits and limits (risk, timing, short-term)', 1.5, 'concept', 'profit maximi', 'risk', 'timing|time', 'short term|short-term', n=3),
           S('s2', 'Wealth maximisation — value of shares, risk and timing considered', 1.5, 'concept', 'wealth maximi', 'share|market value|present value'),
           S('s3', 'Example of conflict', 1, 'application', 'postpon|repair|research|r&d|short run|short term'),
           S('s4', 'Conclusion — wealth maximisation better', 1, 'conclusion', 'wealth', 'better|superior|preferred|appropriate')],
          ['Tabulate merits and demerits; examiners reward a clear conclusion.'], ['Saying wealth maximisation ignores risk.'], ['End with a one-line conclusion.']),
        W('q2', 4, 'What is the agency problem? Name the types of agency cost and state how the problem can be addressed.',
          [p('In companies, shareholders (principals) are separate from managers (agents). Managers may pursue their own goals such as salary, perks or empire-building instead of maximising shareholders\' wealth — this is the agency problem.'),
           p('Agency cost is the additional cost borne by shareholders to monitor and control managers: monitoring, bonding, opportunity and structuring costs.'),
           p('Addressing it: link managerial compensation to profits and long-term goals; stock options for employees and managers; effective monitoring by the board and auditors. For lenders, negative covenants (e.g. borrowing limits) are used.')],
          [S('s1', 'Meaning — separation of ownership and management; managers\' personal goals', 1, 'concept', 'separat|principal|agent', 'manager', 'personal|own goal|perks|salary', n=2),
           S('s2', 'Four agency costs', 1.5, 'concept', 'monitoring', 'bonding', 'opportunity', 'structuring', n=3),
           S('s3', 'Remedies — compensation, stock options, monitoring, covenants', 1.5, 'application', 'compensation|pay|remuneration', 'stock option|esop|option', 'monitor|covenant', n=2)],
          ['Name all four costs for full marks.'], ['Treating agency cost as the salary of managers.'], ['Three short paragraphs: meaning, costs, remedies.']),
        W('q3', 5, 'Explain the three finance decisions and their effect on the value of the firm.',
          [functions, p('Value of the firm, V = f(I, F, D): good investment decisions earn returns above the cost of funds; good financing decisions lower the cost of capital at acceptable risk; good dividend decisions balance shareholders\' expectations with retention for profitable growth. Short-term liquidity decisions keep the firm able to meet its obligations.')],
          [S('s1', 'Investment decision', 1.5, 'concept', 'investment', 'asset|capital budget|project'),
           S('s2', 'Financing decision', 1.5, 'concept', 'financing', 'debt|equity|capital structure|source'),
           S('s3', 'Dividend decision', 1, 'concept', 'dividend', 'retain|retention|distribut|payout'),
           S('s4', 'Link with value — V = f(I, F, D)', 1, 'concept', 'value', 'f i f d|v f|v = f|depends')],
          ['Write V = f(I, F, D) — it earns the link mark.'], ['Mixing up investment and financing examples.'], ['Use a three-row table.'], pad='table'),
    ]

    viva = [
        V('v1', 'What are the two basic aspects of financial management?',
          'The two basic aspects are procurement of funds from suitable sources and the effective utilisation of those funds to achieve the business objective.',
          [P('p1', 'Procurement of funds', 5, 'procure|raising|acquir', 'fund'), P('p2', 'Effective utilisation of funds', 5, 'utilis|utiliz|use|deploy', 'fund|effective')], 'c1'),
        V('v2', 'Name the three finance decisions.',
          'They are the investment decision, the financing decision and the dividend decision, and the value of the firm depends on all three.',
          [P('p1', 'Investment', 3, 'investment'), P('p2', 'Financing', 3, 'financing'), P('p3', 'Dividend', 3, 'dividend'), P('p4', 'Value depends on them', 1, 'value')], 'c3'),
        V('v3', 'Why is wealth maximisation considered better than profit maximisation?',
          'Profit maximisation ignores risk and the timing of returns and is short term. Wealth maximisation considers risk, timing through present value and long term value of shares, so it is the better objective.',
          [P('p1', 'Profit max ignores risk and timing', 5, 'profit', 'risk', 'timing|time'), P('p2', 'Wealth max considers risk, timing, long term', 5, 'wealth', 'present value|long term|value of share|share value|market value')], 'c5'),
        V('v4', 'What is the agency problem and what are the types of agency cost?',
          'The agency problem is the chance that managers put their own goals ahead of shareholders because ownership and management are separate. Agency costs are monitoring, bonding, opportunity and structuring costs.',
          [P('p1', 'Managers\' goals vs shareholders', 4, 'manager', 'shareholder|owner'), P('p2', 'Monitoring', 2, 'monitor'), P('p3', 'Bonding', 2, 'bonding'), P('p4', 'Opportunity and structuring', 2, 'opportunity|structuring')], 'c9'),
        V('v5', 'Distinguish financial distress from insolvency.',
          'Financial distress is a position where cash inflows are inadequate to meet current obligations. Insolvency is the inability to repay debts, which results from continued financial distress.',
          [P('p1', 'Distress — inflows inadequate for current obligations', 5, 'distress', 'inadequate|insufficient|not enough|short', 'obligation'), P('p2', 'Insolvency — inability to repay debts', 5, 'insolven', 'unable|inability|cannot', 'debt|repay')], 'c7'),
    ]

    cases = [{'id': 'k1', 'title': 'Board meeting at Ujala Appliances', 'difficulty': 'moderate',
              'case': 'Ujala Appliances\' CEO wants to cut maintenance spending to show a 15% profit jump this year, which would trigger his size-linked bonus. The CFO warns that equipment failures next year could halve output. Lenders have a covenant limiting total debt to 1.5 times equity. Shareholders demand higher dividends.',
              'mcqs': [
                  M('k1a', 'Cutting maintenance to boost this year\'s profit is an example of:', ['Profit maximisation conflicting with wealth maximisation', 'A financing decision', 'Wealth maximisation', 'A dividend decision'], 0,
                    'Postponing maintenance raises short-term profit but harms future output and value — the classic conflict between profit and wealth maximisation. It is not a financing or dividend decision. In practice: boards look at maintenance capex trends to spot such short-termism.', 'core', topic=T5),
                  M('k1b', 'The CEO\'s size-linked bonus creating this temptation reflects:', ['An agency problem', 'Financial distress', 'Insolvency', 'A liquidity decision'], 0,
                    'The CEO\'s personal incentive diverges from shareholders\' interest in long-term value — an agency problem. Distress and insolvency relate to inability to meet obligations. In practice: linking bonus to multi-year return on capital would reduce this conflict.', 'core', topic=T9),
                  M('k1c', 'The lenders\' debt limit is a:', ['Negative covenant addressing the lender–manager agency problem', 'Dividend policy', 'Monitoring cost borne by shareholders only', 'Structuring of employee pay'], 0,
                    'A limit on borrowing is a negative covenant — the standard way lenders guard against managers taking actions that raise default risk. In practice: breaching such a covenant can let lenders recall the loan, which can itself trigger distress.', 'moderate', topic=T9),
                  M('k1d', 'The shareholders\' demand for higher dividends must be weighed under the:', ['Dividend decision, balancing payout against retention for growth', 'Investment decision only', 'Accounting policy decision', 'Inventory policy'], 0,
                    'How much profit to distribute and how much to retain is the dividend decision; it interacts with investment and financing needs. In practice: if retained funds can earn above the cost of capital, a moderate payout may serve shareholders better.', 'moderate', topic=T3),
              ]}]

    return unit(UID, 'p6', 'int-p6-a-ch01', 1, 'Scope and Objectives of Financial Management',
                ['Explain the meaning, two aspects and evolution of financial management.',
                 'Describe the investment, financing and dividend decisions and their link with the value of the firm.',
                 'Compare profit maximisation and wealth maximisation and apply present value to rank alternatives.',
                 'Explain the role of the finance executive, financial distress and insolvency, and the link with accounting.',
                 'Explain the agency problem, the four agency costs and the ways to address them.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 30}, 'prereq': [],
                 'exam_tip': 'Short theory questions: profit vs wealth maximisation, finance functions, agency problem and role of the CFO; write crisp points with a conclusion.'},
                concepts, [i1], jobs, mcqs, questions,
                {'summary': ['FM = planning and controlling financial resources; two aspects: procurement and utilisation of funds.', 'Evolution: traditional → transitional → modern.',
                             'V = f(I, F, D): investment, financing, dividend (plus short-term liquidity).', 'Wealth maximisation (share value, risk, timing) beats profit maximisation (short-term, ignores risk and timing).',
                             'CFO: from record-keeper to strategic partner.', 'Distress = inflows short of current obligations; insolvency = inability to repay.',
                             'Agency problem: managers vs owners; costs: monitoring, bonding, opportunity, structuring; remedies: pay linkage, stock options, monitoring, covenants.'],
                 'remember': ['Hedging = protecting against risk (like insurance).', 'Finance focuses on cash; accounting on accrual.'],
                 'traps': ['Debt is part of the financing decision, not a separate decision.', 'Wealth maximisation does consider risk.']},
                [('Value of firm', 'V = f(I, F, D)'), ('Better objective', 'Wealth (value) maximisation'), ('Agency costs', 'Monitoring · Bonding · Opportunity · Structuring'),
                 ('Distress vs insolvency', 'Inflows short of obligations → inability to repay')],
                viva, cases,
                topics=['Introduction', 'Meaning of Financial Management', 'Evolution of Financial Management', 'Finance Functions/Finance Decision', 'Importance of Financial Management',
                        'Scope of Financial Management', 'Objectives of Financial Management', 'Conflicts in Profit versus Value Maximisation Principle', 'Role of Finance Executive',
                        'Financial Distress and Insolvency', 'Relationship of Financial Management with Related Disciplines', 'Agency Problem and Agency Cost'])
