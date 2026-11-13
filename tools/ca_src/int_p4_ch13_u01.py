"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 13 Standard Costing.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch13-u01'
T1 = 'Standards, standard costing and variance analysis'
T2 = 'Material and labour variances'
T3 = 'Overhead and sales variances'
T4 = 'Reporting and controlling variances'


def build():
    ck = Checks()
    mcv = ck.add('2000*50 - 2100*48', 'Material cost variance (negative = adverse)')
    mpv = ck.add('2100*(50-48)', 'Material price variance')
    muv = ck.add('50*(2000-2100)', 'Material usage variance')
    lcv = ck.add('3000*100 - 3300*95', 'Labour cost variance')
    lrv = ck.add('3300*(100-95)', 'Labour rate variance')
    lidle = ck.add('-100*100', 'Idle time variance')
    lev = ck.add('100*(3000-3200)', 'Labour efficiency variance')
    i1 = {'id': 'i1', 'title': 'Where did the cost go?', 'difficulty': 'moderate', 'minutes': 12,
          'q': 'Standard per unit: 2 kg of material at ₹50/kg; 3 labour hours at ₹100/hour. Actual output 1,000 units used 2,100 kg bought at ₹48/kg; workers were paid for 3,300 hours at ₹95/hour, of which 100 hours were idle due to a power failure. Compute material and labour variances.',
          'solution': [table(['Variance', 'Working', '₹'], [
              ['Material price', 'AQ × (SP − AP) = 2,100 × 2', inr(mpv) + ' F'],
              ['Material usage', 'SP × (SQ − AQ) = 50 × (2,000 − 2,100)', inr(-muv) + ' A'],
              ['Material cost', 'SC − AC = 1,00,000 − 1,00,800', inr(-mcv) + ' A'],
              ['Labour rate', 'AH paid × (SR − AR) = 3,300 × 5', inr(lrv) + ' F'],
              ['Idle time', '100 × ₹100', inr(-lidle) + ' A'],
              ['Labour efficiency', 'SR × (SH − AH worked) = 100 × (3,000 − 3,200)', inr(-lev) + ' A'],
              ['Labour cost', 'SC − AC = 3,00,000 − 3,13,500', inr(-lcv) + ' A']], title='Material and labour variances'),
              note('Check: 4,200 F − 5,000 A = 800 A; 16,500 F − 10,000 A − 20,000 A = 13,500 A.')],
          'checks': list(ck)}

    ck2 = Checks()
    focv = ck2.add('1000*200 - 250000', 'Fixed overhead cost variance')
    fexp = ck2.add('240000-250000', 'Fixed overhead expenditure variance')
    fvol = ck2.add('1000*200 - 240000', 'Fixed overhead volume variance')
    i2 = {'id': 'i2', 'title': 'Fixed overheads', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Budgeted fixed overheads ₹2,40,000 for 1,200 units (₹200 per unit). Actual fixed overheads ₹2,50,000; actual output 1,000 units. Compute the fixed overhead cost, expenditure and volume variances.',
          'solution': [table(['Variance', 'Working', '₹'], [
              ['Cost', 'Absorbed 2,00,000 − actual 2,50,000', inr(-focv) + ' A'],
              ['Expenditure', 'Budgeted 2,40,000 − actual 2,50,000', inr(-fexp) + ' A'],
              ['Volume', 'Absorbed 2,00,000 − budgeted 2,40,000', inr(-fvol) + ' A']], title='Fixed overhead variances')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'A standard is a predetermined measure of what cost should be under efficient conditions; standard costing compares actual costs with standards, finds variances, and analyses causes for corrective action.',
            'Types of standards: ideal (perfect conditions), basic (unchanged long-term base), currently attainable (achievable with efficient effort — most useful), and normal (average over a cycle).',
            'Setting standards needs input from purchasing (prices), engineering (quantities, times), HR (wage rates) and accounts (overhead rates), usually summarised on a standard cost card.',
            'Variance = standard cost of actual output − actual cost; favourable when actual is lower, adverse when higher. Variances help apply management by exception.'],
          'Standards are the "should" against which the "did" is measured.',
          'If standard material per chair is ₹500 and actual is ₹540, the ₹40 adverse variance triggers a check on price and usage.'),
        C('c2', T2, [
            'Material: cost variance = SQ × SP − AQ × AP; price variance = AQ × (SP − AP) (on purchase or on usage); usage variance = SP × (SQ − AQ), which splits into mix variance = SP × (revised SQ − AQ) and yield variance = SP × (SQ − revised SQ) when several materials are mixed.',
            'Labour: cost variance = SH × SR − AH paid × AR; rate variance = AH paid × (SR − AR); idle time variance = idle hours × SR (always adverse); efficiency variance = SR × (SH − AH worked), which can be split into mix (gang) and yield (sub-efficiency) variances.',
            'Causes: price — market changes, poor buying; usage — wastage, poor quality material; rate — wage revisions, wrong grade; efficiency — poor supervision, machine breakdown, untrained staff.'],
          'Every variance splits into a price effect and a quantity effect.',
          'Buying cheaper but poorer material can give a favourable price variance and an adverse usage variance.'),
        C('c3', T3, [
            'Variable overheads: cost variance = standard VOH for actual output − actual VOH; expenditure variance = AH × standard rate − actual VOH; efficiency variance = standard rate × (SH − AH).',
            'Fixed overheads: cost variance = absorbed (actual output × standard rate per unit) − actual; expenditure (budget) variance = budgeted − actual; volume variance = absorbed − budgeted, which splits into capacity, efficiency and calendar variances when hours are used.',
            'Sales variances (turnover or margin basis): sales price variance = AQ × (AP − SP); sales volume variance = SP (or standard margin) × (AQ − BQ), splitting into mix and quantity variances for multiple products.'],
          'Overhead variances separate overspending from under-use of capacity.',
          'Producing 1,000 units against a 1,200-unit budget leaves fixed overheads under-absorbed — an adverse volume variance.'),
        C('c4', T4, [
            'Variances are reported regularly to the managers responsible — purchase manager for price, production manager for usage and efficiency.',
            'Not all variances are controllable; uncontrollable ones (e.g. a statutory wage increase) may call for revising standards.',
            'Advantages of standard costing: cost control, efficient pricing, budgeting support, simpler stock valuation; limitations: cost of setting standards, standards becoming outdated, and possible demotivation if standards are unrealistic.'],
          'Variance analysis is valuable only if someone acts on it.',
          'A recurring adverse labour efficiency variance points to training or equipment problems.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Monthly variance report', 'role': 'Cost accountant trainee',
             'situation': 'The plant head wants a one-page explanation of why actual cost exceeded standard.',
             'steps': ['Compute material, labour and overhead variances.', 'Check that sub-variances add up.', 'Assign each to a responsible manager.', 'Note likely causes and actions.'],
             'takeaway': 'Reconcile totals first — a variance report that does not add up loses credibility.'}]

    mcqs = [
        Q('m1', 'The most useful standard for control is:', ['Currently attainable standard', 'Ideal standard', 'Basic standard', 'Historical average'], 0,
          'Attainable standards are achievable with efficient effort, motivating staff while revealing real inefficiency. In practice: review them periodically.', 'c1', T1),
        Q('m2', 'AQ 500 kg at ₹22; SP ₹20. Material price variance:', ['₹1,000 adverse', '₹1,200 favourable', '₹500 adverse', '₹2,000 adverse'], 0,
          '500 × (20 − 22) = −1,000: adverse. In practice: check supplier prices.', 'c2', T2, check=1000),
        Q('m3', 'SQ 1,000 kg, AQ 950 kg, SP ₹10. Usage variance:', ['₹500 favourable', '₹600 adverse', '₹950 favourable', '₹50 favourable'], 0,
          '10 × (1,000 − 950) = ₹500 F. In practice: may reflect better material quality.', 'c2', T2, check=500),
        Q('m4', 'Idle time variance is:', ['Always adverse', 'Always favourable', 'Either', 'Part of rate variance'], 0,
          'Paid hours not worked cost money with no output. In practice: separate normal idle time in the standard.', 'c2', T2),
        Q('m5', 'SH 2,000; AH worked 2,200; SR ₹50. Labour efficiency variance:', ['₹10,000 adverse', '₹12,000 favourable', '₹11,000 adverse', '₹1,000 adverse'], 0,
          '50 × (2,000 − 2,200) = −10,000. In practice: investigate supervision.', 'c2', T2, check=10000),
        Q('m6', 'Fixed overhead volume variance arises from:', ['Difference between actual and budgeted output', 'Overspending on overheads', 'Wage rate changes', 'Material price rises'], 0,
          'It is absorbed minus budgeted fixed overheads, due to output differing from budget. In practice: it reflects capacity use.', 'c3', T3),
        Q('m7', 'Budgeted FOH ₹1,00,000; actual ₹95,000. Expenditure variance:', ['₹5,000 favourable', '₹4,000 adverse', 'Nil', '₹95,000'], 0,
          'Spent less than budget: favourable. In practice: check whether savings are sustainable.', 'c3', T3, check=5000),
        Q('m8', 'Actual 900 units sold at ₹105 vs standard price ₹100. Sales price variance:', ['₹4,500 favourable', '₹5,500 adverse', '₹5,000 favourable', '₹500 favourable'], 0,
          '900 × (105 − 100) = 4,500 F. In practice: volume variance is separate.', 'c3', T3, check=4500),
    ]

    questions = [
        W('q1', 8, i1['q'], i1['solution'],
          [S('s1', 'Material price and usage', 2, 'computation', 'price|usage', nums=[mpv]), S('s2', 'Material cost check', 1, 'computation', 'cost', nums=[-mcv]),
           S('s3', 'Labour rate and idle', 2, 'computation', 'rate|idle', nums=[lrv]), S('s4', 'Labour efficiency and total', 3, 'computation', 'efficiency', nums=[-lev, -lcv])],
          ['Mark F/A every time.'], ['Using paid hours for efficiency.'], ['Variance table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Cost', 1, 'computation', 'absorbed', nums=[-focv]), S('s2', 'Expenditure', 1, 'computation', 'budget', nums=[-fexp]), S('s3', 'Volume', 2, 'computation', 'volume', nums=[-fvol])],
          ['Check: expenditure + volume = cost.'], ['Using budgeted output for absorption.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is standard costing?', 'A technique that sets predetermined costs, compares actual costs with them, analyses the variances and takes corrective action.',
          [P('p1', 'Predetermined', 5, 'predetermined|standard'), P('p2', 'Variance analysis', 5, 'variance')], 'c1'),
        V('v2', 'How is material usage variance computed?', 'Standard price multiplied by the difference between standard quantity for actual output and actual quantity used.',
          [P('p1', 'Standard price', 5, 'standard price'), P('p2', 'SQ vs AQ', 5, 'quantity')], 'c2'),
        V('v3', 'Why separate idle time variance?', 'Because paying for hours not worked has different causes, such as power failure, from inefficiency in hours actually worked.',
          [P('p1', 'Different cause', 5, 'cause|power'), P('p2', 'Hours not worked', 5, 'not worked|idle')], 'c2'),
        V('v4', 'What does fixed overhead volume variance show?', 'The over- or under-absorption of fixed overheads because actual output differs from budgeted output.',
          [P('p1', 'Absorption', 5, 'absorb'), P('p2', 'Output difference', 5, 'output')], 'c3'),
        V('v5', 'Name two limitations of standard costing.', 'Standards are costly to set and may become outdated; unrealistic standards can demotivate staff.',
          [P('p1', 'Cost or outdated', 5, 'cost|outdated'), P('p2', 'Demotivation', 5, 'demotiv|unrealistic')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Crisp Snacks', 'difficulty': 'moderate',
              'case': 'Crisp Snacks: standard for one packet — 0.5 kg potato at ₹30/kg. In March it made 4,000 packets using 2,100 kg bought at ₹28/kg. Standard labour 0.1 hour at ₹120; actual 420 hours at ₹125.',
              'mcqs': [
                  M('k1a', 'Material price variance:', ['₹4,200 F', '₹3,800 A', '₹4,000 F', '₹3,000 A'], 0,
                    '2,100 × (30 − 28) = 4,200 F. In practice: seasonal prices.', 'core', check=4200, topic=T2),
                  M('k1b', 'Material usage variance:', ['₹3,000 A', '₹3,500 F', '₹2,800 A', '₹6,000 A'], 0,
                    'SQ 2,000 kg; 30 × (2,000 − 2,100) = 3,000 A. In practice: check peeling wastage.', 'core', check=3000, topic=T2),
                  M('k1c', 'Labour rate variance:', ['₹2,100 A', '₹1,900 F', '₹2,000 A', '₹2,400 A'], 0,
                    '420 × (120 − 125) = 2,100 A. In practice: overtime may explain it.', 'core', check=2100, topic=T2),
                  M('k1d', 'Labour efficiency variance:', ['₹2,400 A', '₹2,600 F', '₹2,500 A', '₹4,500 A'], 0,
                    'SH 400; 120 × (400 − 420) = 2,400 A. In practice: total labour variance ₹4,500 A.', 'core', check=2400, topic=T2),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch13', 1, 'Standard Costing',
                ['Explain standards and the purpose of variance analysis.',
                 'Compute material and labour variances.',
                 'Compute overhead and sales variances.',
                 'Report and interpret variances.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 60}, 'prereq': ['int-p4-ch12-u01'],
                 'exam_tip': 'Compute the total variance first, then sub-variances, and show that they reconcile.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['MCV = SQ·SP − AQ·AP; MPV = AQ(SP − AP); MUV = SP(SQ − AQ).',
                             'LCV = SH·SR − AH·AR; LRV = AH paid(SR − AR); idle = idle hrs × SR; LEV = SR(SH − AH worked).',
                             'FOH: expenditure = budget − actual; volume = absorbed − budget.',
                             'Sales price = AQ(AP − SP); volume = SP(AQ − BQ).'],
                 'remember': ['Standard quantity is for actual output.'],
                 'traps': ['Idle time variance is always adverse.']},
                [('MPV', 'AQ(SP − AP)'), ('MUV', 'SP(SQ − AQ)'), ('LRV', 'AH(SR − AR)'), ('LEV', 'SR(SH − AH)')],
                viva, cases)
