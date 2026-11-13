"""CA Final · Paper 1 Financial Reporting · Chapter 11 Unit 6 Hedge Accounting.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p1-ch11-u06'
T1 = 'Hedged items and hedging instruments'
T2 = 'Qualifying criteria and effectiveness'
T3 = 'Fair value hedges'
T4 = 'Cash flow and net investment hedges; discontinuation'


def build():
    ck = Checks()
    oci = ck.add('min(12,10)', 'Amount in cash flow hedge reserve (₹ lakh)')
    ineff = ck.add('12-min(12,10)', 'Ineffectiveness in profit or loss (₹ lakh)')
    i1 = {'id': 'i1', 'title': 'Hedging a forecast import', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Pulse Ltd. designates a forward to buy EUR as a cash flow hedge of a highly probable machine import. By year end, the forward has gained ₹12 lakh, while the change in present value of the hedged cash flows (expected cost increase) is ₹10 lakh. Allocate the gain. What happens when the machine is bought?',
          'solution': [table(['Item', 'Working', '₹ lakh'], [
              ['Effective portion to OCI (lower of cumulative changes)', 'Lower of 12 and 10', inr(oci)],
              ['Ineffective portion to profit or loss', '12 − 10', inr(ineff)],
              ['On purchase of the machine', 'Reserve removed and included in the machine\'s initial cost (basis adjustment)', inr(oci)]], title='Cash flow hedge')],
          'checks': list(ck)}

    ck2 = Checks()
    net = ck2.add('4.8-5', 'Net effect in profit or loss (₹ lakh)')
    i2 = {'id': 'i2', 'title': 'Swapping a fixed-rate bond', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Pulse Ltd. holds a fixed-rate bond at amortised cost and enters a pay-fixed, receive-floating interest rate swap, designated as a fair value hedge of interest rate risk. Interest rates fall: the bond\'s fair value attributable to interest rate risk rises by ₹4.8 lakh and the swap loses ₹5 lakh. Show the accounting.',
          'solution': [table(['Item', 'Treatment', '₹ lakh'], [
              ['Swap loss', 'Profit or loss; swap liability', inr(-5)],
              ['Bond — hedging adjustment', 'Carrying amount increased; gain in profit or loss', inr(4.8)],
              ['Net (ineffectiveness)', 'Profit or loss', inr(net)]], title='Fair value hedge')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Hedge accounting is optional. It aligns the timing of gains and losses on a hedging instrument and a hedged item, reflecting risk management activities in the accounts.',
            'Hedged items can be recognised assets or liabilities, unrecognised firm commitments, highly probable forecast transactions or net investments in foreign operations — individually, as groups (with conditions) or as components (risk components that are separately identifiable and reliably measurable). Aggregated exposures including derivatives can be hedged items.',
            'Hedging instruments: derivatives measured at FVTPL (except most written options), and non-derivative financial assets or liabilities at FVTPL; for foreign currency risk, non-derivatives can also be used. Only contracts with external parties qualify in consolidated statements. The instrument is designated in its entirety, though the time value of options or forward points may be excluded.'],
          'Pair a risk with an instrument that moves the opposite way.',
          'A forecast USD sale can be hedged with a USD forward.'),
        C('c2', T2, [
            'Qualifying criteria: the relationship consists only of eligible items and instruments; there is formal designation and documentation at inception of the risk management objective, strategy, items, risk hedged and how effectiveness is assessed.',
            'Effectiveness requirements: an economic relationship exists between item and instrument (values move in opposite directions due to the same risk); credit risk does not dominate value changes; and the hedge ratio matches the quantities actually used for risk management.',
            'No bright-line 80–125% test applies. If the hedge ratio drifts but the objective stays the same, the entity rebalances. Ineffectiveness is measured and recognised in profit or loss.'],
          'Document first, then show an economic link and a sensible hedge ratio.',
          'Hedging diesel with crude oil futures needs proof of correlation.'),
        C('c3', T3, [
            'A fair value hedge guards against movements in the fair value of an asset or liability already on the books, or of an unrecognised firm commitment, attributable to a particular risk that could affect profit or loss.',
            'The gain or loss on the hedging instrument goes to profit or loss (OCI if hedging an equity investment at FVOCI). The hedged item\'s carrying amount is adjusted for the hedged risk with the gain or loss in profit or loss — even if it is normally measured at cost or amortised cost.',
            'For amortised cost items, the hedging adjustment is amortised to profit or loss. For firm commitments, the cumulative change is recognised as an asset or liability and later adjusts the acquired asset\'s carrying amount.'],
          'Both sides hit profit or loss, so they largely cancel.',
          'A fixed-rate loan swapped to floating uses a fair value hedge.'),
        C('c4', T4, [
            'A cash flow hedge protects against variability in cash flows of a recognised item or highly probable forecast transaction. The effective portion of the instrument\'s gain or loss goes to OCI (cash flow hedge reserve) — the lower of the cumulative gain or loss on the instrument and the cumulative change in present value of the hedged cash flows; the rest goes to profit or loss.',
            'If the forecast transaction results in a non-financial asset or liability, the reserve is removed and included in its initial cost (basis adjustment, not OCI reclassification). Otherwise it is reclassified to profit or loss when the hedged cash flows affect profit.',
            'Net investment hedges follow cash flow hedge mechanics, with the reserve recycled on disposal. Hedge accounting is discontinued prospectively only when the relationship no longer meets criteria (after rebalancing) — voluntary de-designation is not allowed. If a forecast transaction is no longer expected, the reserve goes immediately to profit or loss.'],
          'Cash flow hedges park gains in OCI until the hedged flow arrives.',
          'A hedged machine purchase gets the reserve added to its cost.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Setting up a hedge program', 'role': 'Treasury manager',
             'situation': 'An exporter wants to hedge forecast USD receipts for 12 months.',
             'steps': ['Write the risk management objective.', 'Document designation at inception.', 'Assess economic relationship and hedge ratio.', 'Track effective portion in OCI and reclassify on sale.'],
             'takeaway': 'Without contemporaneous documentation, no hedge accounting.'}]

    mcqs = [
        Q('m1', 'In a cash flow hedge, the effective portion of the instrument\'s gain goes to:', ['OCI', 'Profit or loss', 'Retained earnings', 'Revenue'], 0,
          'Parked until the hedged item affects profit. In practice: cash flow hedge reserve.', 'c4', T4),
        Q('m2', 'In a fair value hedge, the hedged item\'s carrying amount:', ['Is adjusted for the hedged risk with the change in profit or loss', 'Is unchanged', 'Changes through OCI', 'Is written off'], 0,
          'Both sides hit P&L. In practice: amortise the adjustment.', 'c3', T3),
        Q('m3', 'Which is not an effectiveness requirement under Ind AS 109?', ['Results within 80–125%', 'Economic relationship', 'Credit risk not dominating', 'Appropriate hedge ratio'], 0,
          'The bright line was removed. In practice: qualitative assessment may suffice.', 'c2', T2),
        Q('m4', 'Voluntary de-designation of a qualifying hedge is:', ['Not allowed', 'Allowed anytime', 'Allowed annually', 'Required at year end'], 0,
          'Discontinue only when criteria fail. In practice: rebalance where possible.', 'c4', T4),
        Q('m5', 'When a hedged forecast purchase of inventory occurs, the reserve is:', ['Included in the inventory\'s cost', 'Recycled to profit immediately', 'Left in OCI', 'Transferred to retained earnings'], 0,
          'Basis adjustment for non-financial items. In practice: flows to P&L via cost of sales.', 'c4', T4),
        Q('m6', 'Formal documentation of a hedge must be made:', ['At inception of the relationship', 'At year end', 'When gains arise', 'At settlement'], 0,
          'Hindsight designation is not allowed. In practice: keep a hedge file.', 'c2', T2),
        Q('m7', 'A net investment hedge accumulates effective gains in OCI, recycled:', ['On disposal of the foreign operation', 'Each year', 'Never', 'On hedge expiry'], 0,
          'Like translation differences. In practice: foreign borrowings often used.', 'c4', T4),
        Q('m8', 'Written options generally:', ['Do not qualify as hedging instruments', 'Always qualify', 'Qualify only for FX', 'Qualify for net investments'], 0,
          'Unless offsetting a purchased option. In practice: they expand risk.', 'c1', T1),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'OCI portion', 2, 'computation', 'oci|effective', nums=[oci]), S('s2', 'Ineffective', 1.5, 'computation', 'ineffective', nums=[ineff]), S('s3', 'Basis adjustment', 1.5, 'concept', 'basis|cost')],
          ['Use the lower of test.'], ['Putting all 12 in OCI.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Swap', 1.5, 'concept', 'swap'), S('s2', 'Bond adjustment', 1.5, 'concept', 'hedging adjustment|carrying'), S('s3', 'Net', 1, 'computation', 'net', nums=[net])],
          ['Both to P&L.'], ['Ignoring bond adjustment.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'Name the three types of hedge relationship.', 'Fair value hedge, cash flow hedge and hedge of a net investment in a foreign operation.',
          [P('p1', 'Fair value and cash flow', 6, 'fair value|cash flow'), P('p2', 'Net investment', 4, 'net investment')], 'c1'),
        V('v2', 'What are the effectiveness requirements?', 'An economic relationship between item and instrument, credit risk that does not dominate, and a hedge ratio matching actual risk management.',
          [P('p1', 'Economic relationship', 5, 'economic'), P('p2', 'Hedge ratio', 5, 'ratio')], 'c2'),
        V('v3', 'How is the effective portion of a cash flow hedge measured?', 'As the lower of the cumulative gain or loss on the instrument and the cumulative change in present value of the hedged cash flows.',
          [P('p1', 'Lower of', 5, 'lower'), P('p2', 'Cumulative', 5, 'cumulative')], 'c4'),
        V('v4', 'What is rebalancing?', 'Adjusting the quantities of the hedged item or instrument to restore the hedge ratio while keeping the same risk management objective.',
          [P('p1', 'Adjust quantities', 5, 'quantit'), P('p2', 'Same objective', 5, 'objective')], 'c2'),
        V('v5', 'What happens to the reserve if a forecast transaction is no longer expected?', 'It is reclassified immediately to profit or loss.',
          [P('p1', 'Reclassified', 6, 'reclassif'), P('p2', 'Immediately', 4, 'immediate')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Atlas Exports Ltd.', 'difficulty': 'moderate',
              'case': 'Atlas Exports Ltd. hedges highly probable USD sales due in 6 months with forwards. Cumulative forward loss at year end ₹8 lakh; cumulative change in PV of hedged cash flows ₹9 lakh (gain). It also hedges a fixed-rate borrowing with a receive-fixed, pay-floating swap.',
              'mcqs': [
                  M('k1a', 'Amount debited to the cash flow hedge reserve (₹ lakh):', ['8', '9', '1', '17'], 0,
                    'Lower of 8 and 9 in absolute terms; no ineffectiveness since the instrument moved less. In practice: under-hedge.', 'moderate', check=8, topic=T4),
                  M('k1b', 'When the USD sales occur, the reserve is:', ['Reclassified to profit or loss', 'Added to inventory cost', 'Left in OCI', 'Moved to retained earnings'], 0,
                    'Sales affect profit; no non-financial asset arises. In practice: adjusts revenue.', 'core', topic=T4),
                  M('k1c', 'The swap on the fixed-rate borrowing is a:', ['Fair value hedge', 'Cash flow hedge', 'Net investment hedge', 'Not a hedge'], 0,
                    'Protects fair value of the fixed debt. In practice: adjust borrowing carrying amount.', 'core', topic=T3),
                  M('k1d', 'Documentation prepared after the year end allows hedge accounting:', ['Not for the past period', 'Retrospectively', 'From signing', 'If auditors agree'], 0,
                    'Designation must be at inception. In practice: prospective only.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p1', 'fin-p1-ch11', 6, 'Hedge Accounting',
                ['Identify eligible hedged items and hedging instruments.',
                 'Apply qualifying criteria and effectiveness requirements.',
                 'Account for fair value hedges.',
                 'Account for cash flow and net investment hedges and discontinuation.'],
                {'difficulty': 'hard', 'minutes': {'learn': 40, 'practice': 30}, 'prereq': ['fin-p1-ch11-u05'],
                 'exam_tip': 'Name the hedge type first; it decides whether gains go to profit or to OCI.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Hedge accounting is optional and needs documentation.',
                             'Effectiveness: economic link, credit risk, hedge ratio.',
                             'Fair value hedge: both sides to P&L.',
                             'Cash flow hedge: effective part in OCI; lower-of test.',
                             'Basis adjustment for non-financial items.'],
                 'remember': ['No voluntary de-designation.'],
                 'traps': ['Applying the old 80–125% test.']},
                [('FV hedge', 'Both in P&L'), ('CF hedge', 'Effective in OCI'), ('NI hedge', 'OCI, recycle on disposal'), ('Documentation', 'At inception')],
                viva, cases)
