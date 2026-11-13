"""CA Final · Paper 4 · Chapter 28 Latest Developments in International Taxation.
Scope follows the ICAI study material for May/Nov 2026 attempts; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch28-u01'
T1 = 'BEPS monitoring and the Inclusive Framework'
T2 = 'Pillar One: Amount A and Amount B'
T3 = 'Pillar Two: GloBE rules and STTR'
T4 = 'Recent GloBE guidance and safe harbours'


def build():
    ck = Checks()
    rp = ck.add('4500-30000*0.10', 'Residual profit above 10% of revenue (EUR million)')
    aa = ck.add('(4500-30000*0.10)*0.25', 'Amount A reallocated (EUR million)')
    i1 = {'id': 'i1', 'title': 'Amount A arithmetic', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'A multinational group has global revenue of EUR 30,000 million and profit before tax of EUR 4,500 million. Assuming it is in scope of Amount A, compute the residual profit and the amount reallocated to market jurisdictions.',
          'solution': [table(['Step', 'Working', 'EUR million'], [
              ['Scope', 'Revenue > EUR 20 billion; profitability 15% > 10%', 'In scope'],
              ['Residual profit', '4,500 − 10% × 30,000', inr(rp)],
              ['Amount A', '25% × residual profit', inr(aa)]], title='Pillar One')],
          'checks': list(ck)}

    c2 = Checks()
    st = c2.add('100000000*(0.09-0.04)', 'STTR tax on ₹10 crore royalty (₹)')
    i2 = {'id': 'i2', 'title': 'Subject to tax rule', 'difficulty': 'core', 'minutes': 5,
          'q': 'An Indian company pays royalty of ₹10 crore to a connected company resident in a treaty country where the adjusted nominal rate on such royalty is 4%. Assuming the STTR is in force in that treaty, compute the additional tax India may levy under the STTR.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['STTR minimum rate', '9%', '—'],
              ['Shortfall', '9% − 4%', '5%'],
              ['STTR tax', '5% × 10 crore', inr(st)]], title='Pillar Two — STTR')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'After the 2015 BEPS package of 15 Actions, OECD and G20 countries committed to monitor implementation, especially of the four minimum standards, through peer reviews.',
            'The Inclusive Framework on BEPS, set up in 2016, lets non-OECD and non-G20 jurisdictions participate on an equal footing in developing and monitoring standards; it had 148 members by January 2026.',
            'The Inclusive Framework agreed the Two-Pillar solution (BEPS 2.0) in 2021 — the July statement backed by 130 jurisdictions and the October 2021 statement with a detailed implementation plan, later supported by 139.'],
          'BEPS moved from design to monitoring and BEPS 2.0.',
          'Developing countries now help set international tax standards.'),
        C('c2', T2, [
            'Pillar One has two parts. Amount A reallocates 25% of residual profit (profit above 10% of revenue) of very large and profitable groups — revenue above EUR 20 billion and profitability above 10% — to market jurisdictions using a revenue-based nexus. Amount A is not presently in force.',
            'Amount B provides a simplified and streamlined approach to pricing baseline marketing and distribution activities, using a pricing matrix based on industry grouping and asset and expense intensity. It was integrated into the OECD Transfer Pricing Guidelines; jurisdictions may choose to apply it, and it has effect only where adopted.',
            'Further Amount B materials, including pricing FAQs and an automation tool, were released in February 2026.'],
          'Amount A reallocates profit; Amount B simplifies distributor pricing.',
          'A group earning 15% on EUR 30 billion revenue would reallocate EUR 375 million under Amount A.'),
        C('c3', T3, [
            'Pillar Two has two components. The GloBE rules require in-scope groups (consolidated revenue of at least EUR 750 million) to bear tax of at least 15% (effective rate), measured jurisdiction by jurisdiction, via a qualified domestic minimum top-up tax (QDMTT), an income inclusion rule (IIR) at the parent level, and an undertaxed profits rule (UTPR) as backstop. A substance-based income exclusion reduces the profit subject to top-up.',
            'The Subject to Tax Rule (STTR) is treaty-based: where specified intra-group payments such as interest, royalties and certain service fees are taxed below 9% (adjusted nominal rate) in the recipient\'s jurisdiction, the source state may levy tax up to the shortfall. STTR tax is counted as a covered tax for GloBE, so it applies first.',
            'The STTR can be implemented through a multilateral instrument or bilateral treaty amendments and is designed to benefit developing countries.'],
          'A 15% floor for groups and a 9% treaty test for payments.',
          'Royalty taxed at 4% in the recipient jurisdiction may face a 5% STTR charge at source.'),
        C('c4', T4, [
            'On 5 January 2026 the Inclusive Framework agreed a Side-by-Side Package that includes a new safe harbour based on a simplified ETR, an extra year for the transitional CbCR safe harbour, a safe harbour for substance-based tax incentives, and a side-by-side system with safe harbours for groups headquartered in eligible jurisdictions.',
            'Administrative guidance in May 2026 addressed the transitional UTPR safe harbour for groups with 52/53-week years; a common understanding on central filing and exchange of the GloBE Information Return together with a refreshed central list of qualifying IIR and domestic top-up regimes, followed in May–June 2026.',
            'The 2026 Consolidated Commentary to the GloBE Model Rules, published on 28 May 2026, merges the Commentary with all agreed administrative guidance.'],
          'Safe harbours and central filing ease GloBE compliance.',
          'A group meeting the simplified ETR safe harbour may avoid full GloBE computations in a jurisdiction.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Pillar Two readiness', 'role': 'Global tax analyst',
             'situation': 'An Indian-headquartered group with EUR 900 million revenue reviews its subsidiaries.',
             'steps': ['Confirm scope at EUR 750 million.', 'Compute jurisdictional ETRs.', 'Test safe harbours.', 'Plan GIR filing and QDMTT exposure.'],
             'takeaway': 'Safe harbours can save heavy computations if tested early.'}]

    mcqs = [
        Q('m1', 'The Inclusive Framework on BEPS was established in:', ['2016', '2013', '2015', '2021'], 0,
          'Equal footing. In practice: 148 members by 2026.', 'c1', T1, check=2016),
        Q('m2', 'Amount A applies to groups with revenue above:', ['EUR twenty billion', 'EUR seven hundred fifty million', 'EUR one billion', 'EUR five billion'], 0,
          'And profitability above 10%. In practice: not yet in force.', 'c2', T2),
        Q('m3', 'Amount A reallocates what share of residual profit?', ['Twenty-five percent', 'Ten percent', 'Fifteen percent', 'Fifty percent'], 0,
          'Residual = profit above 10% of revenue. In practice: market jurisdictions.', 'c2', T2),
        Q('m4', 'Amount B deals with:', ['Pricing of baseline distribution activities', 'Global minimum tax', 'Digital services tax', 'Treaty abuse'], 0,
          'Simplified TP. In practice: optional adoption.', 'c2', T2),
        Q('m5', 'GloBE rules apply to groups with consolidated revenue of at least:', ['EUR seven hundred fifty million', 'EUR twenty billion', 'EUR one hundred million', 'EUR five hundred million'], 0,
          '15% minimum ETR. In practice: per jurisdiction.', 'c3', T3),
        Q('m6', 'The STTR minimum rate is:', ['Nine percent', 'Fifteen percent', 'Ten percent', 'Five percent'], 0,
          'Treaty-based. In practice: covered tax for GloBE.', 'c3', T3),
        Q('m7', 'Which applies first among GloBE charging mechanisms?', ['Qualified domestic minimum top-up tax', 'Undertaxed profits rule', 'Income inclusion rule', 'STTR is ignored'], 0,
          'QDMTT reduces IIR/UTPR. In practice: STTR before GloBE.', 'c3', T3),
        Q('m8', 'The Side-by-Side Package was agreed on:', ['5 January 2026', '28 May 2026', '1 July 2021', '8 October 2021'], 0,
          'Safe harbours. In practice: simplifies compliance.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Scope and residual profit', 3, 'computation', 'residual', nums=[rp]), S('s2', 'Amount A', 2, 'computation', '25%', nums=[aa])],
          ['State status of Amount A.'], ['Applying 25% to total profit.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Shortfall', 2, 'computation', '9%'), S('s2', 'STTR tax', 2, 'computation', 'STTR', nums=[st])],
          ['Mention interaction with GloBE.'], ['Using 15% instead of 9%.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is BEPS 2.0?', 'The Two-Pillar solution agreed in 2021: Pillar One on reallocation of taxing rights and Pillar Two on a global minimum tax.',
          [P('p1', 'Two-Pillar', 5, 'two-pillar|pillar'), P('p2', 'Minimum tax', 5, 'minimum tax')], 'c1'),
        V('v2', 'What is the substance-based income exclusion?', 'A carve-out based on payroll and tangible assets that reduces the profit subject to top-up tax.',
          [P('p1', 'Payroll', 5, 'payroll'), P('p2', 'Tangible assets', 5, 'tangible')], 'c3'),
        V('v3', 'Is Amount B mandatory?', 'It applies only in jurisdictions that choose to adopt it; it has no effect otherwise.',
          [P('p1', 'Adopt', 5, 'adopt'), P('p2', 'Choose', 5, 'choose')], 'c2'),
        V('v4', 'Why does the STTR apply before GloBE?', 'STTR tax counts as a covered tax in the GloBE effective tax rate, giving it practical priority.',
          [P('p1', 'Covered tax', 5, 'covered tax'), P('p2', 'Priority', 5, 'priority')], 'c3'),
        V('v5', 'What did the 2026 Consolidated Commentary do?', 'It merged the GloBE Commentary with all agreed administrative guidance into one document.',
          [P('p1', 'Merged', 5, 'merged'), P('p2', 'Administrative guidance', 5, 'administrative guidance')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Saffron Group', 'difficulty': 'moderate',
              'case': 'Saffron Group (revenue EUR 900 million) has subsidiaries in Country Q with GloBE income of ₹250 crore, a substance-based income exclusion of ₹50 crore and an effective tax rate of 11%. Country Q has a qualified domestic minimum top-up tax.',
              'mcqs': [
                  M('k1a', 'Is Saffron in scope of GloBE?', ['Yes, revenue exceeds EUR 750 million', 'No', 'Only for Amount A', 'Only if listed'], 0,
                    'Scope threshold. In practice: consolidated revenue.', 'core', topic=T3),
                  M('k1b', 'Excess profit after exclusion (₹ crore):', ['200', '250', '50', '300'], 0,
                    '250 − 50. In practice: top-up base.', 'core', check=200, topic=T3),
                  M('k1c', 'Top-up tax (₹ crore):', ['8', '22', '30', '10'], 0,
                    '(15% − 11%) × 200. In practice: simplified.', 'core', check=8, topic=T3),
                  M('k1d', 'Which jurisdiction collects it first?', ['Country Q via its QDMTT', 'Parent via IIR', 'Any via UTPR', 'India via STTR'], 0,
                    'QDMTT priority. In practice: reduces IIR.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch28', 1, 'Latest Developments in International Taxation',
                ['Describe BEPS monitoring and the Inclusive Framework.',
                 'Explain Pillar One: Amount A and Amount B.',
                 'Apply Pillar Two: GloBE rules and STTR.',
                 'Summarise recent GloBE guidance and safe harbours.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 15}, 'prereq': ['fin-p4-ch27-u01'],
                 'exam_tip': 'Keep the thresholds straight: EUR 20 billion and 10% for Amount A; EUR 750 million and 15% for GloBE; 9% for STTR.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Inclusive Framework (2016); 148 members by Jan 2026.', 'Amount A: EUR 20 billion, 10%, 25% of residual — not in force.', 'Amount B: simplified distribution pricing — optional.',
                             'GloBE: EUR 750 million; 15%; QDMTT, IIR, UTPR.', 'STTR 9%; Side-by-Side Package (Jan 2026); Consolidated Commentary (May 2026).'],
                 'remember': ['STTR is counted before GloBE top-up.'],
                 'traps': ['Mixing the Amount A and GloBE thresholds.']},
                [('Pillar One', 'Amount A / B'), ('Pillar Two', 'GloBE / STTR'), ('2026 updates', 'Side-by-Side Package')],
                viva, cases)
