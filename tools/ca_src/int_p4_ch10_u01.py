"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 10 Process & Operation Costing.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch10-u01'
T1 = 'Features of process costing and the process account'
T2 = 'Normal loss, abnormal loss and abnormal gain'
T3 = 'Equivalent production: FIFO and weighted average'
T4 = 'Inter-process profit and operation costing'


def build():
    ck = Checks()
    scrap = ck.add('1000*5', 'Scrap value of normal loss')
    rate = ck.add('(302000-5000)/9000', 'Cost per normal unit')
    ab = ck.add('200*33', 'Abnormal loss')
    out = ck.add('8800*33', 'Value of good output transferred')
    i1 = {'id': 'i1', 'title': 'A process with losses', 'difficulty': 'moderate', 'minutes': 9,
          'q': '10,000 units were put into Process I at a total cost of ₹3,02,000 (materials, labour and overheads). Normal loss is 10% of input; loss units sell as scrap at ₹5 each. Actual output was 8,800 units. Prepare the Process I account and value the abnormal loss.',
          'solution': [table(['Item', 'Units', '₹'], [
              ['Total cost charged (Dr)', '10,000', inr(302000)],
              ['Normal loss (scrap value, Cr)', '1,000', inr(scrap)],
              ['Abnormal loss (Cr) @ ₹' + inr(rate), '200', inr(ab)],
              ['Output to Process II (Cr) @ ₹33', '8,800', inr(out)]], title='Process I account'),
              note('Cost per unit = (total cost − scrap of normal loss) ÷ normal output = 2,97,000 ÷ 9,000 = ₹33. The abnormal loss account is then credited with ₹1,000 scrap value and the balance ₹5,600 goes to Costing P&L.')],
          'checks': list(ck)}

    ck2 = Checks()
    eum = ck2.add('15000+3000', 'Equivalent units — materials (FIFO)')
    euc = ck2.add('2000*40/100+15000+3000*40/100', 'Equivalent units — conversion (FIFO)')
    cfin = ck2.add('70000+800*30+15000*50', 'Cost of units completed')
    cwip = ck2.add('3000*20+1200*30', 'Closing WIP')
    i2 = {'id': 'i2', 'title': 'Finishing what was started last month', 'difficulty': 'hard', 'minutes': 12,
          'q': 'Opening WIP 2,000 units (materials 100%, conversion 60%) valued at ₹70,000. Units introduced 18,000; completed and transferred 17,000; closing WIP 3,000 (materials 100%, conversion 40%). Current costs: materials ₹3,60,000; conversion ₹5,10,000. Using FIFO, compute equivalent units, cost per EU, cost of completed units and closing WIP.',
          'solution': [table(['Item', 'Materials', 'Conversion'], [
              ['Completing opening WIP', '0', '800'],
              ['Started and completed (17,000 − 2,000)', '15,000', '15,000'],
              ['Closing WIP', '3,000', '1,200'],
              ['Equivalent units', inr(eum), inr(euc)],
              ['Current cost ₹', inr(360000), inr(510000)],
              ['Cost per EU ₹', '20', '30']], title='FIFO statement of equivalent production'),
              table(['Valuation', '₹'], [
                  ['Completed units: opening 70,000 + 800 × 30 + 15,000 × 50', inr(cfin)],
                  ['Closing WIP: 3,000 × 20 + 1,200 × 30', inr(cwip)],
                  ['Total (= 70,000 + 3,60,000 + 5,10,000)', inr(cfin + cwip)]], title='Valuation')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Process costing suits continuous, mass production of identical units passing through sequential processes — chemicals, textiles, paper, oil refining, food processing. Costs are collected per process for a period and averaged over output.',
            'Each process account is debited with materials, labour, direct expenses and overheads, and with the cost of units transferred from the previous process; it is credited with normal loss scrap, abnormal loss and output transferred to the next process or finished stock.',
            'Unlike job costing, costs are not traced to individual orders; work-in-progress is common at period ends and must be converted into equivalent finished units.'],
          'Costs follow the product through each stage, like water flowing through connected tanks.',
          'A paper mill has pulping, forming and finishing processes, each with its own account.'),
        C('c2', T2, [
            'Normal loss is the expected, unavoidable loss (evaporation, shrinkage). Its cost is absorbed by good output; scrap value of normal loss is credited to the process.',
            'Abnormal loss is loss beyond normal, from inefficiency or accident. It is valued at the same cost per unit as good output — (total cost − normal scrap) ÷ (input − normal loss) — and credited to the process and debited to an Abnormal Loss Account, which in turn is credited with its scrap value and the balance written off to Costing P&L.',
            'Abnormal gain arises when actual loss is less than normal. It is debited to the process at the normal cost per unit and credited to an Abnormal Gain Account; that account is debited with the scrap value forgone and the balance credited to Costing P&L.'],
          'Expected losses raise unit cost; unexpected ones are isolated and reported.',
          'Normal loss 5%, actual loss 3%: the 2% difference is an abnormal gain.'),
        C('c3', T3, [
            'Equivalent units express partly completed units as whole units: units × percentage complete, computed separately for each cost element because materials often enter at the start while conversion accrues gradually.',
            'FIFO: opening WIP is completed first; current-period cost per EU uses only current costs and current work (opening WIP\'s remaining work + units started and completed + closing WIP work). Opening WIP cost is added only to completed units.',
            'Weighted average: opening WIP cost and current cost are pooled; EU = completed units + closing WIP work; one average rate values both completed units and closing WIP.',
            'Losses in EU: normal loss gets zero EU (its cost spreads to good units); abnormal loss gets EU to the stage of loss, usually 100%.'],
          'Half-done units are counted as fractions of whole ones so costs can be shared fairly.',
          '1,000 units 50% converted equal 500 equivalent units of conversion work.'),
        C('c4', T4, [
            'Inter-process profit: when output is transferred between processes at market price or cost plus a percentage, process accounts show profit at each stage. Unrealised profit in closing stock must be eliminated through a provision so that final profit is not overstated.',
            'Operation costing is a refinement of process costing used where each operation is costed (cost per operation), such as in engineering units or bottle filling; it aids control at each step.',
            'Process costing contrasts with job costing: continuous vs. order-based; average costs vs. specific costs; period accumulation vs. job completion.'],
          'Transfer profits motivate managers but must be removed from unsold stock before reporting.',
          'Process I transfers at cost + 25%; profit on goods still in Process II stock is unrealised.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Yield monitoring', 'role': 'Cost accountant trainee',
             'situation': 'A chemicals plant\'s losses have crept above the normal rate.',
             'steps': ['Compute normal loss from input.', 'Compare with actual loss to find abnormal loss.', 'Value it at the process cost per unit.', 'Report causes and cost to production management.'],
             'takeaway': 'Separating abnormal loss puts a rupee value on inefficiency.'}]

    mcqs = [
        Q('m1', 'Process costing suits:', ['Continuous production of identical units', 'Custom orders', 'Construction projects', 'Consulting assignments'], 0,
          'Process costing averages costs over homogeneous output. In practice: refineries and textile mills use it.', 'c1', T1),
        Q('m2', 'Scrap value of normal loss is:', ['Credited to the process account', 'Debited to the process account', 'Credited to Costing P&L', 'Ignored'], 0,
          'It reduces the cost borne by good output. In practice: it is a recovery, not income.', 'c2', T2),
        Q('m3', 'Input 5,000 units costing ₹1,00,000; normal loss 10% (scrap nil); output 4,400. Abnormal loss value:', ['₹2,222', '₹2,000', '₹4,000', '₹2,400'], 0,
          'Cost per unit = 1,00,000 ÷ 4,500 = ₹22.22; abnormal loss 100 units = ₹2,222. In practice: round consistently.', 'c2', T2, 'moderate', check=2222),
        Q('m4', 'Abnormal gain occurs when:', ['Actual loss is less than normal loss', 'Actual loss exceeds normal loss', 'There is no scrap value', 'Output exceeds input'], 0,
          'Fewer units lost than expected gives an abnormal gain. In practice: it is credited, net of scrap forgone, to Costing P&L.', 'c2', T2),
        Q('m5', 'Under FIFO, cost per EU is based on:', ['Current-period costs and current work only', 'Opening WIP cost plus current cost', 'Standard costs', 'Last period\'s rate'], 0,
          'FIFO separates opening WIP; weighted average pools. In practice: FIFO gives current efficiency.', 'c3', T3),
        Q('m6', '2,000 units in closing WIP are 30% complete for conversion. Conversion EU:', ['600', '2,000', '1,400', '300'], 0,
          '2,000 × 30% = 600. In practice: materials may be 100% complete.', 'c3', T3, check=600),
        Q('m7', 'Normal loss is given equivalent units of:', ['Zero', '100%', '50%', 'Same as closing WIP'], 0,
          'Its cost is absorbed by good units, so no EU is assigned. In practice: abnormal loss gets EU.', 'c3', T3),
        Q('m8', 'Unrealised inter-process profit in closing stock is:', ['Eliminated through a provision', 'Added to profit', 'Ignored', 'Charged to the next process'], 0,
          'Only profit on goods sold outside is realised. In practice: compute the profit element in each stock layer.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Normal loss scrap', 1, 'computation', 'scrap', nums=[scrap]), S('s2', 'Cost per unit', 2, 'computation', 'per unit', nums=[rate]),
           S('s3', 'Abnormal loss and output', 2, 'computation', 'abnormal', nums=[ab, out])],
          ['Divide by normal output.'], ['Dividing by actual output.'], ['Process account.'], pad='table', checks=list(ck)),
        W('q2', 7, i2['q'], i2['solution'],
          [S('s1', 'EU materials', 1, 'computation', 'materials', nums=[eum]), S('s2', 'EU conversion', 2, 'computation', 'conversion', nums=[euc]),
           S('s3', 'Completed units', 2, 'computation', 'completed', nums=[cfin]), S('s4', 'Closing WIP', 2, 'computation', 'closing', nums=[cwip])],
          ['Separate opening WIP under FIFO.'], ['Using weighted average when FIFO is asked.'], ['Two tables.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is normal loss?', 'The expected and unavoidable loss inherent in a process, whose cost is absorbed by good output after crediting scrap value.',
          [P('p1', 'Expected', 5, 'expected|unavoidable'), P('p2', 'Absorbed', 5, 'absorb|good output')], 'c2'),
        V('v2', 'How is abnormal loss valued?', 'At the cost per unit of normal output: total cost less scrap of normal loss, divided by input less normal loss units.',
          [P('p1', 'Normal output basis', 6, 'normal'), P('p2', 'Scrap deducted', 4, 'scrap')], 'c2'),
        V('v3', 'What is an equivalent unit?', 'A notional whole unit representing partly completed work, found by multiplying units by their percentage of completion.',
          [P('p1', 'Notional whole unit', 5, 'whole|notional'), P('p2', 'Percentage completion', 5, 'percentage|complet')], 'c3'),
        V('v4', 'How do FIFO and weighted average differ?', 'FIFO uses only current costs and work and keeps opening WIP separate; weighted average pools opening and current costs into one rate.',
          [P('p1', 'FIFO separate', 5, 'separate|current'), P('p2', 'Average pools', 5, 'pool|average')], 'c3'),
        V('v5', 'What is operation costing?', 'A form of process costing that determines the cost of each operation rather than each process, for closer control.',
          [P('p1', 'Each operation', 6, 'operation'), P('p2', 'Control', 4, 'control')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'PureJuice', 'difficulty': 'moderate',
              'case': 'PureJuice puts 20,000 litres into its pressing process at a cost of ₹4,00,000. Normal loss is 5% (sold as pulp at ₹2 per litre). Output is 19,400 litres.',
              'mcqs': [
                  M('k1a', 'Normal loss in litres:', ['1,000', '600', '400', '2,000'], 0,
                    '5% of 20,000 = 1,000. In practice: computed on input.', 'core', check=1000, topic=T2),
                  M('k1b', 'Abnormal gain in litres:', ['400', '600', '1,000', 'Nil'], 0,
                    'Expected output 19,000; actual 19,400 — gain 400. In practice: loss was only 600.', 'core', check=400, topic=T2),
                  M('k1c', 'Cost per litre of normal output:', ['₹20.95', '₹20.00', '₹20.62', '₹21.05'], 0,
                    '(4,00,000 − 2,000) ÷ 19,000 = ₹20.95 (rounded). In practice: value the gain at this rate.', 'moderate', check=20.95, topic=T2),
                  M('k1d', 'Net abnormal gain credited to Costing P&L:', ['₹7,580', '₹8,380', '₹800', '₹8,000'], 0,
                    'Gain 400 × 20.95 = 8,380 less pulp value forgone 400 × 2 = 800 → ₹7,580. In practice: show it in the abnormal gain account.', 'hard', check=7580, topic=T2),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch10', 1, 'Process & Operation Costing',
                ['Prepare process accounts with normal and abnormal losses or gains.',
                 'Compute equivalent production under FIFO and weighted average.',
                 'Explain inter-process profit and operation costing.'],
                {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 60}, 'prereq': ['int-p4-ch09-u01'],
                 'exam_tip': 'Always build the units reconciliation first (input = output + losses + closing WIP) before any rupee figure.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Process A/c: debit costs; credit normal scrap, abnormal loss, output.',
                             'Cost per unit = (cost − normal scrap) ÷ normal output.',
                             'Abnormal loss/gain valued at that rate; net to Costing P&L.',
                             'EU: FIFO (current only) vs weighted average (pooled).',
                             'Eliminate unrealised inter-process profit.'],
                 'remember': ['Normal loss gets zero EU.'],
                 'traps': ['Abnormal gain account is debited with scrap value forgone.']},
                [('Cost per unit', '(Cost − scrap) ÷ normal output'), ('Abnormal loss', 'At normal unit cost'), ('FIFO EU', 'Current work only')],
                viva, cases)
