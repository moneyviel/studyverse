"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 3 Employee Cost and Direct Expenses.
Scope follows the ICAI study material (May 2027 onwards); explanations, examples and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch03-u01'
T1 = 'Employee cost and its control'
T2 = 'Time-keeping, time-booking and payroll'
T3 = 'Idle time'
T4 = 'Overtime and its treatment'
T5 = 'Paying for work: time rate, piece rate and premium bonus'
T6 = 'Halsey and Rowan compared'
T7 = 'Wage rate for costing and its components'
T8 = 'Employee turnover'
T9 = 'Direct expenses'


def build():
    ck = Checks()
    base = ck.add('30*120', 'time wages for hours worked')
    h_bonus = ck.add('0.5*(40-30)*120', 'Halsey bonus = 50% × time saved × rate')
    h_tot = ck.add('30*120+0.5*(40-30)*120', 'Halsey earnings')
    r_bonus = ck.add('30/40*(40-30)*120', 'Rowan bonus = time taken/time allowed × time saved × rate')
    r_tot = ck.add('30*120+30/40*(40-30)*120', 'Rowan earnings')
    h_eff = ck.add('(30*120+0.5*(40-30)*120)/30', 'Halsey effective hourly rate')
    r_eff = ck.add('(30*120+30/40*(40-30)*120)/30', 'Rowan effective hourly rate')
    i1 = {'id': 'i1', 'title': 'Halsey vs Rowan for one job', 'difficulty': 'core', 'minutes': 8,
          'q': 'Standard time for a job is 40 hours; Priya completes it in 30 hours. Her time rate is ₹120 an hour. Compute her earnings and effective hourly rate under (a) the Halsey plan (50%) and (b) the Rowan plan.',
          'solution': [table(['Item', 'Halsey ₹', 'Rowan ₹'], [
              ['Time wages (30 h × ₹120)', inr(base), inr(base)],
              ['Bonus', f'{inr(h_bonus)} (50% × 10 h × ₹120)', f'{inr(r_bonus)} (30/40 × 10 h × ₹120)'],
              ['Total earnings', inr(h_tot), inr(r_tot)],
              ['Effective rate per hour', inr(h_eff), inr(r_eff)],
          ], title='Earnings'), note('Rowan pays more here because time taken (30 h) is more than half the standard (20 h); the two plans pay the same bonus when time taken is exactly 50% of standard time.')],
          'checks': list(ck)}

    ck2 = Checks()
    avg = ck2.add('(760+840)/2', 'average number on roll')
    sep = ck2.add('64/((760+840)/2)*100', 'separation method %')
    rep = ck2.add('48/((760+840)/2)*100', 'replacement method %')
    flux = ck2.add('(64+48)/((760+840)/2)*100', 'flux method % (separations + replacements)')
    flux2 = ck2.add('(64+48+40)/((760+840)/2)*100', 'flux method % including new joinings for expansion (accessions)')
    i2 = {'id': 'i2', 'title': 'Measuring employee turnover three ways', 'difficulty': 'core', 'minutes': 7,
          'q': 'A factory had 760 workers at the start and 840 at the end of the year. During the year 64 workers left, 48 were recruited to replace leavers and 40 were recruited for an expansion. Compute employee turnover by the separation, replacement and flux methods, and the flux rate if expansion recruits are also counted.',
          'solution': [wn('Average on roll', f'(760 + 840) ÷ 2 = {inr(avg)}.'),
                       table(['Method', 'Formula', 'Rate'], [
                           ['Separation', 'Separations ÷ average on roll × 100 = 64 ÷ 800 × 100', f'{sep}%'],
                           ['Replacement', 'Replacements ÷ average × 100 = 48 ÷ 800 × 100', f'{rep}%'],
                           ['Flux', '(Separations + replacements) ÷ average × 100 = 112 ÷ 800 × 100', f'{flux}%'],
                           ['Flux with accessions', '(64 + 48 + 40) ÷ 800 × 100', f'{flux2}%'],
                       ], title='Employee turnover'), note('Recruits for expansion are normally excluded; some accountants include all joinings (accessions) in the flux method.')],
          'checks': list(ck2)}

    ck3 = Checks()
    annual = ck3.add('(14000+2800)*12', 'basic + DA for the year')
    pf = ck3.add('(14000+2800)*12*0.12', 'employer PF @ 12% of basic + DA')
    esi = ck3.add('(14000+2800)*12*0.0325', 'employer ESI @ 3.25%')
    bonus = ck3.add('(14000+2800)*1.5', 'bonus = 1.5 months\' basic + DA')
    tot = ck3.add('(14000+2800)*12*(1+0.12+0.0325)+(14000+2800)*1.5', 'total annual employee cost')
    hrs = ck3.add('(300-20)*8*0.95', 'effective hours = (300 − 20 leave days) × 8 × 95% (5% normal idle time)')
    rate = ck3.add('round(((14000+2800)*12*(1+0.12+0.0325)+(14000+2800)*1.5)/((300-20)*8*0.95),2)', 'wage rate per hour for costing')
    i3 = {'id': 'i3', 'title': 'Hourly rate for costing purposes', 'difficulty': 'moderate', 'minutes': 10,
          'q': 'Arjun earns basic pay of ₹14,000 a month and dearness allowance of ₹2,800 a month. The employer contributes 12% of basic + DA to provident fund and 3.25% to ESI, and pays bonus equal to 1.5 months\' basic + DA a year. There are 300 working days of 8 hours; Arjun is entitled to 20 days\' paid leave, and normal idle time is 5% of the hours available. Compute the employee cost per effective hour for costing.',
          'solution': [table(['Component', '₹'], [
              ['Basic + DA (₹16,800 × 12)', inr(annual)], ['Employer PF @ 12%', inr(pf)], ['Employer ESI @ 3.25%', inr(esi)], ['Bonus (1.5 months)', inr(bonus)], ['Total annual cost', inr(tot)]], num=[1], total=True, title='Annual employee cost'),
              wn('Effective hours', f'(300 − 20) days × 8 h = 2,240 h; less 5% normal idle time → {inr(hrs)} h.'),
              wn('Rate for costing', f'{R(tot)} ÷ {inr(hrs)} h = {R(rate)} per hour (used only for costing; it is not the rate paid to the worker).')],
          'checks': list(ck3)}

    plans = table(['Plan', 'Earnings', 'Key feature'], [
        ['Time rate', 'Hours worked × rate', 'Guaranteed; no link to output — suits supervisors, skilled or machine-paced work'],
        ['Piece rate', 'Units produced × rate per unit', 'Pay depends entirely on output'],
        ['Halsey premium plan', 'Hours worked × rate + 50% × (standard time − time taken) × rate', 'Time saved shared equally (sometimes 33⅓% to the worker — Halsey-Weir); minimum time wages guaranteed'],
        ['Rowan premium plan', 'Hours worked × rate + (time taken ÷ standard time) × time saved × rate', 'Bonus is a proportion of time wages; it rises and then falls as time saved grows, protecting against loose standards'],
        ['Group bonus', 'Bonus for a group\'s output, shared among members', 'Encourages teamwork where individual output cannot be measured'],
    ], title='Methods of remunerating employees')

    concepts = [
        C('c1', T1, [
            'Employee (labour) cost is the remuneration — monetary and non-monetary — of employees: basic pay, dearness allowance, overtime, bonus, employer\'s contributions to provident fund, ESI and pension, leave pay, plus benefits such as medical, education, recreation, housing and subsidised canteens.',
            'Direct employee cost can be identified with a cost object economically (a machine operator on a job); indirect employee cost cannot (supervisors, maintenance staff) and becomes overhead.',
            'Controlling employee cost needs: proper manpower planning and recruitment, good working conditions, time-keeping and time-booking, efficient production planning (to avoid idle time), sound wage and incentive schemes, job evaluation and merit rating, and monitoring of labour turnover and productivity. Departments involved: personnel/HR, engineering and work study, time-keeping, payroll and cost accounting.',
            'Employee cost is collected through attendance records, time-booking (job cards), payroll and analysis by cost centre and job.'],
          'Employee cost is not just the salary slip — it is the full cost of keeping a person at work, the way a car\'s cost includes fuel, insurance and servicing, not just the price.',
          'A CA preparing a product cost sheet adds employer\'s PF, ESI, bonus and leave cost to the wage rate — omitting them understates cost by 25–30%.'),
        C('c2', T2, [
            'Time-keeping records the attendance of employees — arrival and departure — for payroll. Manual methods: attendance register, token or disc method. Mechanical/automated: time recording clocks, swipe cards, biometric systems. A good system prevents proxy attendance, records late arrival and early departure, covers piece workers too, and is mechanised as far as possible.',
            'Time-booking records how the time spent in the factory was used — on which job, process or idle — through job cards or daily/weekly time sheets. It lets wages be charged to jobs and shows idle time.',
            'Payroll procedure: attendance and time records → computation of gross wages (time or piece basis, overtime, incentives) → deductions (employee PF, ESI, professional tax, TDS, voluntary contributions, loans) → net pay → disbursement and payroll accounting, with analysis of wages by cost centre and job.'],
          'Time-keeping answers "was the worker here?"; time-booking answers "what did the worker do while here?"',
          'Reconciling attendance hours with booked hours exposes unrecorded idle time and padded job cards.'),
        C('c3', T3, [
            'Idle time is time for which employees are paid but do no productive work. The difference between time-keeping hours and time-booking hours.',
            'Normal idle time is unavoidable — walking from the gate to the department, change-over between jobs, setting up machines, tea breaks, fatigue. Its cost is part of the cost of production: either by inflating the wage rate or by charging it to factory overhead.',
            'Abnormal idle time arises from avoidable causes — machine breakdown, power failure, shortage of material, strikes, lockouts, poor planning. It is not included in product cost and is charged to Costing Profit and Loss Account.',
            'Control: report idle time by cause and department, fix responsibility and remove the causes (preventive maintenance, material planning).'],
          'Normal idle time is the time a cook spends washing hands between dishes; abnormal idle time is the hour lost when the gas supply fails.',
          'Idle-time reports by cause often reveal that "waiting for material" is the biggest loss — a planning problem, not a labour problem.'),
        C('c4', T4, [
            'Overtime is work beyond normal hours. Overtime payment = normal wages for the overtime hours + overtime premium (the extra over the normal rate). The study material cites the Factories Act, 1948 rule: work beyond nine hours a day or forty-eight hours a week earns twice the ordinary rate of wages (ordinary rate = basic + allowances, excluding bonus and overtime).',
            'Treatment of the premium: if overtime is at the customer\'s request for urgency — charge the premium to that job; to meet general production needs or urgent orders — production overhead of the department working overtime; due to another department\'s fault — charge that department; due to abnormal conditions such as flood or earthquake — Costing Profit and Loss Account.',
            'Occasional overtime shows full use of capacity; persistent overtime signals either shortage of capacity or a habit of slowing down during normal hours to earn overtime — it needs control through planning and authorisation.'],
          'Overtime premium is a rush-delivery charge: whoever asked for the rush should pay it.',
          'Plant controllers require prior written approval for overtime and report it weekly by department.'),
        C('c5', T5, [
            'Time rate: wages = hours (including normal idle time) × rate. Suits work where output is hard to measure (supervisors, clerks), highly skilled or quality-critical work, or where the machine sets the pace.',
            'Piece rate: wages = units × rate per unit — pay depends only on output, independent of time taken.',
            'Premium bonus plans fix a standard time; the worker is guaranteed time wages (except under the Barth system), and if he finishes early, the time saved is shared between the employer and the worker.',
            'Group bonus schemes reward a team\'s combined output, and special incentive schemes exist for indirect workers.'],
          'Time rate pays for the ticket, piece rate pays for the distance covered, and a premium bonus pays the fare plus a share of the time you saved by taking the express train.',
          'Incentive design is a common consulting task: the plan must motivate without encouraging poor quality.',
          blocks=[plans]),
        C('c6', T6, [
            'Halsey: bonus = 50% × time saved × rate. The worker\'s share of saving is constant (50%); easy to understand; guarantees time wages. But the employer shares equally even when savings come from loose standards, and workers may rush and hurt quality.',
            'Rowan: bonus = (time taken ÷ time allowed) × time saved × rate. The bonus is a proportion of time wages equal to the proportion of time saved. It rises as time saved grows up to 50% of standard, then falls — so the worker gains little from extreme speed, which protects quality and guards against loosely set standards.',
            'Comparison: when time taken equals exactly 50% of the standard, both plans give the same bonus. When time taken is more than 50% of standard, Rowan pays more; when it is less than 50%, Halsey pays more. Under Rowan the bonus is maximum when time taken is 50% of the standard time.'],
          'Halsey is a fixed 50–50 split of the time saved; Rowan is a sliding scale that rewards moderate speed most and quietly discourages reckless speed.',
          'Where standards are new or doubtful, firms prefer Rowan because a loose standard cannot produce runaway bonuses.'),
        C('c7', T7, [
            'For costing, the wage rate for direct workers can include the related costs (employer\'s PF and ESI, bonus, leave pay, normal idle time) so that these are charged to jobs with the wages. Alternatively, these extras can be treated as overheads.',
            'Rate per hour for costing = total annual employee cost ÷ effective (productive) hours, where effective hours exclude leave, holidays and normal idle time. This rate is for costing only, not for paying the worker.',
            'Components: basic wage (for work measured by time or output), dearness allowance (to meet rising cost of living, linked to a price index), overtime allowance, special allowances, production bonus (incentive for output above standard), statutory bonus (the study material refers to the Payment of Bonus Act: minimum 8.33% of wages or ₹100, whichever is higher, up to 20%), employer\'s contributions, leave pay and the value of non-monetary benefits.',
            'Holiday and leave wages may be charged to departmental overheads (recorded separately from "worked-for" wages) or built into the costing wage rate. Night-shift allowance is usually treated as production overhead unless a job specifically needs night work.',
            'Efficiency rating compares actual output with standard to help fix wages, incentives and promotions, and to identify training needs.'],
          'The costing wage rate is the "all-in" price of an hour of useful work — like a taxi\'s cost per kilometre that includes insurance and idle waiting, not just fuel.',
          'Job quotations built on the bare wage rate are a common cause of under-pricing.'),
        C('c8', T8, [
            'Employee (labour) turnover is the rate of change in the workforce over a period, compared with a norm (industry or past rate).',
            'Separation method = employees separated ÷ average number on roll × 100. Replacement method = employees replaced ÷ average number × 100 (new hires for expansion are excluded). Flux method = (separations + replacements) ÷ average number × 100; some include all accessions (joinings, including for expansion).',
            'Causes: personal (better job elsewhere, family reasons, ill health), unavoidable (seasonal work, retirement, death, discharge for misconduct) and avoidable (low pay, poor working conditions, no prospects, bad relations with supervisors, lack of training).',
            'Effects (costs): preventive costs (to keep workers — welfare, medical, incentives, personnel department) and replacement costs (recruitment, selection, training, lower output and higher scrap from new workers, more breakage and accidents). High turnover raises cost and lowers productivity.'],
          'Turnover is a leaking bucket: every worker who leaves takes training and experience with them, and the new one must be filled up again.',
          'HR and cost teams together compute the "cost of attrition" — a strong argument for retention bonuses.'),
        C('c9', T9, [
            'Direct expenses are costs other than direct material and direct employee cost that can be identified and traced to a cost object economically — for example royalty paid on each unit produced, hire of special equipment for a job, cost of special moulds or patterns, sub-contract or job-work charges, and design or consultancy costs for a specific product.',
            'Direct expenses form part of prime cost (direct material + direct employee cost + direct expenses).',
            'Measurement: at invoice or agreed price plus related costs, net of trade discounts and recoverable taxes; where the benefit spreads over several units or periods (e.g. a mould used over many batches), the cost is spread on a rational basis (per unit or per batch).'],
          'Direct expenses are the special tools rented for one particular job — they belong to that job just like its material.',
          'Royalty per unit to a technology licensor is a classic direct expense in the product cost sheet.'),
    ]

    jobs = [
        {'id': 'j1', 'title': 'Choosing an incentive scheme', 'role': 'Cost accountant advising an HR head',
         'situation': 'A plant wants to introduce incentives; time standards were set recently and may be loose.',
         'steps': ['Explain Halsey (50% of time saved) and Rowan (proportional bonus).', 'Show with figures that Rowan limits bonus when time taken falls below half the standard.', 'Recommend Rowan until standards are verified by work study; revisit later.'],
         'takeaway': 'The right incentive depends on how reliable the standards are.'},
        {'id': 'j2', 'title': 'Overtime spike in the paint shop', 'role': 'Plant controller',
         'situation': 'Paint shop overtime premium doubled this quarter. Investigation shows the press shop delivered panels late on most days.',
         'steps': ['Overtime caused by another department\'s fault: charge the premium to the press shop.', 'Report idle time in the paint shop while waiting for panels as abnormal.', 'Recommend production planning changes to remove the root cause.'],
         'takeaway': 'Charging overtime to the department that caused it puts pressure where it belongs.'},
    ]

    mcqs = [
        Q('m1', 'The difference between hours recorded by time-keeping and hours booked to jobs represents:', ['Idle time', 'Overtime', 'Labour turnover', 'Efficiency'], 0,
          'Time-keeping records hours present; time-booking records how those hours were spent on jobs. The unbooked difference is idle time — paid but unproductive. Overtime is work beyond normal hours, a different measure. In practice: the daily idle-time report is built exactly from this comparison.', 'c2', T2),
        Q('m2', 'Idle time caused by a machine breakdown is treated in cost accounts as:', ['Abnormal — charged to Costing Profit and Loss Account', 'Normal — included in the wage rate', 'Production overhead of all departments', 'Selling overhead'], 0,
          'Breakdowns are avoidable causes, so the idle time is abnormal and its cost is kept out of product cost by charging Costing Profit and Loss. Normal idle time (walking to the machine, set-ups, breaks) is the item included in cost — the trap. In practice: repeated breakdown idle time is evidence for a preventive maintenance budget.', 'c3', T3),
        Q('m3', 'Which of these is NORMAL idle time?', ['Time taken to set up the machine for a new job', 'Strike by workers', 'Power failure', 'Waiting for raw material due to poor planning'], 0,
          'Set-up time between jobs is inherent in production, so it is normal idle time and its cost forms part of production cost. Strikes, power failures and material shortages are avoidable causes, so they are abnormal. In practice: normal idle time is often built into the costing wage rate.', 'c3', T3),
        Q('m4', 'Overtime is worked at a customer\'s request to complete an urgent job. The overtime premium is:', ['Charged directly to that job', 'Treated as general production overhead', 'Charged to Costing Profit and Loss', 'Charged to administration overhead'], 0,
          'When the customer asks for the urgency, the premium is caused by that job and is charged to it directly (and usually billed to the customer). Overtime for general production needs goes to the department\'s overhead, and overtime due to abnormal events goes to Costing P&L. In practice: quotations for rush orders include an overtime premium line.', 'c4', T4),
        Q('m5', 'Overtime arising from a flood in the factory area is charged to:', ['Costing Profit and Loss Account', 'The jobs worked on', 'Production overhead', 'The department that was flooded as overhead'], 0,
          'Overtime caused by abnormal conditions such as floods or earthquakes is not a normal cost of production and is charged to Costing Profit and Loss. Charging it to jobs or overhead would overstate product cost. In practice: such costs may be partly recovered through insurance.', 'c4', T4),
        Q('m6', 'Under the Halsey plan (50%), a worker with standard time 40 hours finishes in 30 hours at ₹120 per hour. The bonus is:', ['₹600', '₹900', '₹1,200', '₹450'], 0,
          'Halsey bonus = 50% × time saved × rate = 50% × 10 × 120 = ₹600. ₹900 is the Rowan bonus (30/40 × 10 × 120) and ₹1,200 is the whole time saved at full rate. In practice: Halsey earnings are ₹3,600 + ₹600 = ₹4,200.', 'c6', T6, check='0.5*(40-30)*120'),
        Q('m7', 'Under the Rowan plan, same facts (standard 40 h, taken 30 h, ₹120/h), the bonus is:', ['₹900', '₹600', '₹1,200', '₹300'], 0,
          'Rowan bonus = (time taken ÷ time allowed) × time saved × rate = 30/40 × 10 × 120 = ₹900. ₹600 is the Halsey bonus. In practice: Rowan pays more than Halsey here because time taken is more than half the standard.', 'c6', T6, check='30/40*(40-30)*120'),
        Q('m8', 'Bonus under Halsey (50%) equals bonus under Rowan when the time taken is:', ['50% of standard time', '75% of standard time', 'Equal to standard time', '25% of standard time'], 0,
          'Halsey bonus = ½ × (S − T) × R and Rowan bonus = (T ÷ S) × (S − T) × R; they are equal when T ÷ S = ½, i.e. time taken is 50% of standard. At equal to standard there is no time saved and both bonuses are zero, but that is a trivial case. In practice: workers faster than 50% of standard earn more under Halsey.', 'c6', T6, 'moderate'),
        Q('m9', 'A feature of the Rowan plan is that:', ['The bonus falls once time taken goes below half the standard time', 'The worker gets 50% of time saved always', 'Minimum wages are not guaranteed', 'Bonus keeps rising as time taken falls'], 0,
          'Rowan\'s bonus is maximum when time taken is 50% of standard and falls for even faster work, discouraging hurried work and protecting against loosely set standards. The constant 50% share describes Halsey. Rowan guarantees time wages. In practice: this self-limiting feature makes Rowan attractive where standards are uncertain.', 'c6', T6, 'moderate'),
        Q('m10', 'Time rate is most suitable where:', ['Output cannot be measured easily or the machine sets the pace', 'Work is highly repetitive and easily counted', 'Workers are paid for units produced', 'Quality is unimportant'], 0,
          'Time rate suits work whose output is hard to measure (supervisors, clerks), highly skilled or quality-critical work, and automatic processes where the operator cannot change speed. Easily counted repetitive work suits piece rates — the trap. In practice: chemical plant operators are on time rates for exactly this reason.', 'c5', T5),
        Q('m11', 'A firm has 800 workers on average; 64 separations and 48 replacements in the year. Employee turnover by the flux method is:', ['14%', '8%', '6%', '2%'], 0,
          'Flux method = (separations + replacements) ÷ average on roll × 100 = (64 + 48) ÷ 800 × 100 = 14%. 8% is the separation rate and 6% the replacement rate. In practice: HR dashboards often report the separation rate as "attrition".', 'c8', T8, check='(64+48)/800*100'),
        Q('m12', 'Under the replacement method of employee turnover, new hires for an expansion are:', ['Excluded', 'Included', 'Doubled', 'Deducted from separations'], 0,
          'The replacement method counts only those hired to replace leavers; workers hired for expansion are not replacements and are excluded. Some accountants include all joinings (accessions) in the flux method — that variant is the trap. In practice: separating expansion hiring prevents growth from looking like attrition.', 'c8', T8),
        Q('m13', 'Which is a REPLACEMENT cost of employee turnover?', ['Training cost of new recruits', 'Welfare and medical schemes to retain workers', 'Personnel department expenses to keep workers satisfied', 'Pension schemes'], 0,
          'Replacement costs arise because workers leave and must be replaced — recruitment, selection, training, lower output and higher scrap from new hands. Welfare, medical and pension schemes are preventive costs incurred to keep workers. In practice: these replacement costs are what make attrition expensive.', 'c8', T8, 'moderate'),
        Q('m14', 'Effective hours are 2,128 and total annual employee cost is ₹2,47,094. The wage rate for costing is about:', ['₹116.12 per hour', '₹103.00 per hour', '₹110.31 per hour', '₹120.00 per hour'], 0,
          'Costing wage rate = total employee cost ÷ effective hours = 2,47,094 ÷ 2,128 ≈ ₹116.12 per hour. Dividing by gross hours (2,400) instead of effective hours understates the rate. In practice: this rate charges leave, idle time and employer contributions to jobs automatically.', 'c7', T7, 'moderate'),
        Q('m15', 'Night-shift allowance paid for general production is usually treated as:', ['Production overhead', 'Direct employee cost of each job', 'Administration overhead', 'Costing Profit and Loss item'], 0,
          'A night shift that serves general production cannot be traced to particular jobs, so the allowance is a production overhead. Only if a job specifically requires night work would it be charged to that job. In practice: shift allowances are spread through the departmental overhead rate.', 'c7', T7),
        Q('m16', 'Royalty paid per unit of a product manufactured is:', ['A direct expense', 'Administration overhead', 'Selling overhead', 'Indirect material'], 0,
          'A royalty that varies with each unit produced can be traced directly to the product, so it is a direct expense and part of prime cost. Royalty based on sales value would be a selling cost — that variation is the trap. In practice: licensed-technology products show royalty as a separate line in the cost sheet.', 'c9', T9),
        Q('m17', 'Persistent overtime in a department most likely indicates:', ['Shortage of capacity or a tendency to delay normal work to earn overtime', 'Full and efficient use of capacity', 'Low labour turnover', 'Accurate standards'], 0,
          'Occasional overtime shows full use of capacity, but persistent overtime suggests either that more men and machines are needed or that workers are slowing down in normal hours to earn overtime. In practice: management responds with capacity planning and strict authorisation of overtime.', 'c4', T4),
    ]
    mcqs[13]['check'] = '247094/2128'

    ckq = Checks()
    qh = ckq.add('36*150+0.5*(48-36)*150', 'Halsey earnings'); qr = ckq.add('36*150+36/48*(48-36)*150', 'Rowan earnings')
    qhe = ckq.add('(36*150+0.5*(48-36)*150)/36', 'Halsey effective rate'); qre = ckq.add('(36*150+36/48*(48-36)*150)/36', 'Rowan effective rate')
    questions = [
        W('q1', 6, 'Standard time for a job is 48 hours. A worker paid ₹150 per hour completes it in 36 hours. Calculate his earnings and effective hourly rate under (i) the Halsey plan (50%) and (ii) the Rowan plan. Which plan gives him more, and why?',
          [table(['Item', 'Halsey ₹', 'Rowan ₹'], [
              ['Time wages (36 × ₹150)', '5,400', '5,400'], ['Bonus', '50% × 12 × ₹150 = 900', '36/48 × 12 × ₹150 = 1,350'],
              ['Total earnings', inr(qh), inr(qr)], ['Effective rate per hour', inr(qhe), inr(qre)]]),
           p('Rowan gives more because the time taken (36 hours) is more than 50% of the standard time (24 hours); the two plans give equal bonus only when time taken is exactly half the standard.')],
          [S('s1', 'Time wages ₹5,400', 1, 'computation', nums=[5400]), S('s2', 'Halsey earnings ₹6,300 and rate ₹175', 2, 'computation', nums=[qh, qhe]),
           S('s3', 'Rowan earnings ₹6,750 and rate ₹187.50', 2, 'computation', nums=[qr, qre]),
           S('s4', 'Reason — time taken more than 50% of standard', 1, 'analysis', 'rowan', '50|half')],
          ['Show bonus formulas in words before figures.'], ['Using standard hours instead of actual hours for time wages.'], ['A side-by-side table is fastest.'], pad='table', checks=list(ckq)),
        W('q2', 5, 'Explain the treatment of overtime premium in cost accounts under different circumstances.',
          [ul(['If overtime is worked at the customer\'s request to get urgent delivery, the premium is charged directly to that job.',
               'If overtime is needed to cope with general production programmes or urgent orders, the premium is treated as production overhead of the department working overtime.',
               'If overtime is worked in a department because of the fault of another department, the premium is charged to the department responsible.',
               'If overtime is due to abnormal conditions such as flood or earthquake, it is not charged to cost but to Costing Profit and Loss Account.']),
           p('Overtime payment consists of normal wages for the overtime hours plus the premium; only the premium is treated as above, the normal wages being charged as usual.')],
          [S('s1', 'Customer request — charge to job', 1.5, 'provision', 'customer', 'job'),
           S('s2', 'General production — departmental overhead', 1.5, 'provision', 'general|production programme|urgent order', 'overhead'),
           S('s3', 'Another department\'s fault — that department', 1, 'provision', 'fault|another department|other department', 'charg'),
           S('s4', 'Abnormal conditions — Costing P&L', 1, 'provision', 'abnormal|flood|earthquake', 'costing profit|costing p&l')],
          ['Four circumstances, one mark each, plus the split of payment into normal wages and premium.'], ['Charging all overtime premium to Costing P&L.'], ['Number each circumstance with its treatment.']),
        W('q3', 5, 'What is employee turnover? State the methods of measuring it and its main causes.',
          [p('Employee turnover is the rate of change in the composition of the workforce during a period, measured against a suitable norm such as the industry rate or a past rate.'),
           ul(['Separation method: employees separated ÷ average number on roll × 100.', 'Replacement method: employees replaced ÷ average number on roll × 100 (excluding hiring for expansion).', 'Flux method: (separations + replacements) ÷ average number on roll × 100.']),
           p('Causes: personal causes (better prospects elsewhere, family or health reasons), unavoidable causes (seasonal work, retirement, death, discharge for misconduct) and avoidable causes (low pay, poor working conditions, lack of growth, bad relations with supervisors).')],
          [S('s1', 'Meaning', 1, 'concept', 'change', 'composition|workforce|employee force|labour force'),
           S('s2', 'Separation method', 1, 'provision', 'separat', 'average'), S('s3', 'Replacement method', 1, 'provision', 'replac', 'average|expansion'),
           S('s4', 'Flux method', 1, 'provision', 'flux', 'separat', 'replac'), S('s5', 'Causes — personal, unavoidable, avoidable', 1, 'concept', 'personal', 'unavoidable', 'avoidable', n=2)],
          ['Formulas earn the marks; write them with the ×100.'], ['Including expansion hiring under the replacement method.'], ['Group causes under three headings.']),
    ]

    viva = [
        V('v1', 'Distinguish normal and abnormal idle time and their treatment.',
          'Normal idle time is unavoidable, such as setting up machines or breaks, and its cost is included in production cost through the wage rate or factory overhead. Abnormal idle time arises from avoidable causes such as breakdowns, power failure or strikes and is charged to the costing profit and loss account.',
          [P('p1', 'Normal — unavoidable, part of production cost', 5, 'normal', 'unavoidable|inherent|setting|break', 'production cost|wage rate|overhead', min=2),
           P('p2', 'Abnormal — avoidable, Costing P&L', 5, 'abnormal', 'breakdown|power|strike|avoidable', 'costing profit|costing p&l', min=2)], 'c3'),
        V('v2', 'State the Halsey and Rowan bonus formulas.',
          'Under the Halsey plan bonus is fifty percent of the time saved multiplied by the rate. Under the Rowan plan bonus is time taken divided by time allowed, multiplied by time saved and the rate.',
          [P('p1', 'Halsey — 50% of time saved × rate', 5, 'halsey', 'fifty|50|half', 'time saved'), P('p2', 'Rowan — time taken ÷ time allowed × time saved × rate', 5, 'rowan', 'time taken', 'time allowed|standard time')], 'c6'),
        V('v3', 'How is overtime premium treated when overtime is worked at a customer\'s request, and when it is due to a flood?',
          'At the customer\'s request the overtime premium is charged directly to that job. When it is due to a flood or other abnormal condition it is charged to the costing profit and loss account.',
          [P('p1', 'Customer request — charged to the job', 5, 'customer', 'job'), P('p2', 'Flood — Costing P&L', 5, 'flood|abnormal', 'costing profit|costing p&l')], 'c4'),
        V('v4', 'Give the three methods of measuring employee turnover.',
          'The separation method divides separations by the average number on roll, the replacement method divides replacements by the average number, and the flux method adds separations and replacements and divides by the average number, each multiplied by one hundred.',
          [P('p1', 'Separation method', 3, 'separat'), P('p2', 'Replacement method', 3, 'replac'), P('p3', 'Flux method', 2, 'flux'), P('p4', 'Divided by average number on roll', 2, 'average')], 'c8'),
        V('v5', 'What are direct expenses? Give two examples.',
          'Direct expenses are costs other than direct material and direct employee cost that can be traced to a cost object economically, for example royalty paid per unit produced and hire charges of special equipment for a job.',
          [P('p1', 'Other than material and labour, traceable', 5, 'traced|traceable|identified|identifi', 'cost object|product|job'), P('p2', 'Examples', 5, 'royalt|hire|mould|pattern|sub contract|subcontract|job work|design')], 'c9'),
    ]

    cases = [{'id': 'k1', 'title': 'Payroll review at Vardhan Castings', 'difficulty': 'moderate',
              'case': 'At Vardhan Castings, standard time for a casting job is 20 hours; worker Imran took 16 hours at ₹100 per hour. The fettling shop worked overtime because the moulding shop delivered late. The factory had 450 workers at the start and 550 at the end of the year; 30 left and 25 were replaced, and 90 were hired for a new line.',
              'mcqs': [
                  M('k1a', 'Imran\'s earnings under the Rowan plan are:', ['₹1,920', '₹1,800', '₹2,000', '₹1,600'], 0,
                    'Time wages = 16 × 100 = ₹1,600; Rowan bonus = 16/20 × 4 × 100 = ₹320; total ₹1,920. ₹1,800 is the Halsey total (bonus ₹200). In practice: Rowan pays more here because time taken (80% of standard) exceeds half the standard.', 'moderate', check='16*100+16/20*(20-16)*100', topic=T6),
                  M('k1b', 'The fettling shop\'s overtime premium should be charged to:', ['The moulding shop', 'The fettling shop overhead', 'Costing Profit and Loss', 'The customer'], 0,
                    'When overtime is caused by another department\'s fault, the premium is charged to that department — here the moulding shop that delivered late. Charging the fettling shop would punish the wrong manager. In practice: this treatment is a strong lever for inter-departmental discipline.', 'core', topic=T4),
                  M('k1c', 'Employee turnover by the separation method is:', ['6%', '5%', '11%', '29%'], 0,
                    'Average on roll = (450 + 550) ÷ 2 = 500; separation rate = 30 ÷ 500 × 100 = 6%. 5% is the replacement rate (25 ÷ 500) and 11% is the flux rate. In practice: a 6% separation rate would be compared with the industry norm.', 'moderate', check='30/((450+550)/2)*100', topic=T8),
                  M('k1d', 'The 90 workers hired for the new line are:', ['Excluded from the replacement method', 'Counted as replacements', 'Counted as separations', 'Ignored in all measures of workforce change'], 0,
                    'Recruitment for expansion is not replacement of leavers, so it is excluded from the replacement method; only some variants of the flux method count all accessions. In practice: excluding expansion hiring stops growth from inflating attrition statistics.', 'core', topic=T8),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch03', 1, 'Employee Cost and Direct Expenses',
                ['Explain the elements and control of employee cost, time-keeping, time-booking and payroll.',
                 'Treat normal and abnormal idle time and overtime premium in cost accounts.',
                 'Compute earnings under time rate, piece rate, Halsey and Rowan plans and compare them.',
                 'Compute the wage rate for costing purposes including statutory and fringe costs.',
                 'Measure employee turnover by the separation, replacement and flux methods; explain its causes and costs; identify direct expenses.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 50, 'practice': 45}, 'prereq': ['int-p4-ch01-u01'],
                 'exam_tip': 'Halsey vs Rowan, costing wage rate and labour turnover are standard numericals; overtime and idle time treatment are frequent theory questions.'},
                concepts, [i1, i2, i3], jobs, mcqs, questions,
                {'summary': ['Employee cost = all monetary and non-monetary remuneration; direct vs indirect.', 'Time-keeping (attendance) vs time-booking (use of time); difference = idle time.',
                             'Normal idle time → production cost; abnormal → Costing P&L.', 'Overtime premium: customer → job; general → overhead; other dept fault → that dept; abnormal → Costing P&L.',
                             'Halsey bonus = 50% × saved × rate; Rowan bonus = (taken/allowed) × saved × rate; equal at 50%.', 'Costing wage rate = total cost ÷ effective hours.',
                             'Turnover: separation, replacement, flux; causes personal/unavoidable/avoidable; preventive and replacement costs.', 'Direct expenses: traceable costs other than material and labour (royalty per unit, hire of special equipment).'],
                 'remember': ['Rowan bonus is maximum at 50% time taken.', 'Expansion hiring excluded from replacement method.', 'Overtime at twice the ordinary rate beyond 9 h/day or 48 h/week (as cited in the study material).'],
                 'traps': ['Time wages use ACTUAL hours, not standard hours.', 'Night shift allowance is normally overhead.', 'Wage rate for costing is not the rate paid to the worker.']},
                [('Halsey', 'T × R + 50% × (S − T) × R'), ('Rowan', 'T × R + (T ÷ S) × (S − T) × R'), ('Separation', 'Separations ÷ average on roll × 100'),
                 ('Replacement', 'Replacements ÷ average × 100'), ('Flux', '(Separations + replacements) ÷ average × 100'), ('Costing wage rate', 'Total employee cost ÷ effective hours')],
                viva, cases,
                topics=['Introduction', 'Employee (Labour) Cost', 'Employee Cost Control', 'Attendance & Payroll Procedures', 'Idle Time', 'Overtime', 'Labour Utilisation',
                        'Remunerating Employees', 'Absorption of Wages', 'Efficiency Rating Procedures', 'Employee (Labour) Turnover', 'Direct Expenses'])
