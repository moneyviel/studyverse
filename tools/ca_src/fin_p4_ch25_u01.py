"""CA Final · Paper 4 · Chapter 25 Fundamentals of BEPS.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch25-u01'
T1 = 'BEPS project, pillars and minimum standards'
T2 = 'Digital economy and the Two-Pillar solution'
T3 = 'Hybrid mismatches, CFC and interest limitation'
T4 = 'Treaty abuse, PE, transfer pricing and MLI'


def build():
    ck = Checks()
    lim = ck.add('100000000*0.30', '30% of EBITDA (₹)')
    exc = ck.add('50000000-100000000*0.30', 'Interest in excess of 30% of EBITDA (₹)')
    dis = ck.add('min(50000000-100000000*0.30,40000000)', 'Interest disallowed (lower of excess and AE interest) (₹)')
    i1 = {'id': 'i1', 'title': 'Interest limitation under section 177', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Orbit Manufacturing Ltd (not a bank or insurer) has EBITDA of ₹10 crore for T.Y. 2026-27. Its total interest expense is ₹5 crore, of which ₹4 crore is paid on debt from its non-resident parent. Compute the interest disallowed and its treatment.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Threshold', 'Interest on AE debt exceeds ₹1 crore', 'Applies'],
              ['30% of EBITDA', '30% × 10 crore', inr(lim)],
              ['Excess interest', '5 crore − 3 crore', inr(exc)],
              ['Disallowed', 'Lower of excess and AE interest (₹4 crore)', inr(dis)],
              ['Carry forward', 'Up to 8 tax years within the 30% cap', '—']], title='Section 177 (Action 4)')],
          'checks': list(ck)}

    c2 = Checks()
    pr = c2.add('20000000*0.10', 'Tax on patent royalty at 10% (₹)')
    tu = c2.add('1000000000*(0.15-0.09)', 'Simplified Pillar Two top-up tax (₹)')
    i2 = {'id': 'i2', 'title': 'Patent box and minimum tax', 'difficulty': 'core', 'minutes': 5,
          'q': '(a) Medisys Ltd, a resident patentee, earns royalty of ₹2 crore on a patent developed and registered in India. Compute tax at the special rate (ignore surcharge and cess). (b) A multinational group\'s entities in one jurisdiction have GloBE profits of ₹100 crore and an effective tax rate of 9%. Compute the simplified top-up tax under Pillar Two (ignore substance carve-out).',
          'solution': [table(['Item', 'Working', '₹'], [
              ['(a) Patent royalty', '10% × 2 crore (section 194(1) Table Sl. No. 2)', inr(pr)],
              ['(b) Top-up tax', '(15% − 9%) × 100 crore', inr(tu)]], title='Actions 5 and Pillar Two')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Base erosion and profit shifting (BEPS) describes planning that uses gaps and mismatches between tax systems to move profits to low or no-tax locations with little real activity. The OECD/G20 BEPS project produced 15 Actions in 2015, built on three pillars: coherence (Actions 2–5), substance (Actions 6–10) and transparency (Actions 11–14), with Actions 1 and 15 cutting across.',
            'Four Actions are minimum standards that every Inclusive Framework member commits to and is peer-reviewed on: Action 5 (harmful tax practices), Action 6 (treaty abuse), Action 13 (TP documentation and CbCR) and Action 14 (dispute resolution).',
            'Other outputs are reinforced international standards (e.g. TP guidelines, PE definition), common approaches (Actions 2 and 4) and best practices (Actions 3 and 12).'],
          'Fifteen actions; four are non-negotiable.',
          'India adopted CbCR in line with the Action 13 minimum standard.'),
        C('c2', T2, [
            'Action 1 addressed the digital economy: options included a significant economic presence nexus, withholding on digital transactions and an equalisation levy. India introduced SEP in section 9(9) — transactions above ₹2 crore or 3 lakh users — and an equalisation levy, later withdrawn.',
            'The Two-Pillar solution: Pillar One reallocates part of residual profit of the largest, most profitable multinationals to market jurisdictions with a new nexus; Pillar Two (GloBE rules) imposes a 15% global minimum effective tax rate on groups with revenue of €750 million or more, through an income inclusion rule, an undertaxed profits rule and qualified domestic minimum top-up taxes.',
            'Top-up tax is broadly (15% − jurisdictional effective rate) × excess profit after a substance-based carve-out; government entities, international organisations, pension funds and certain investment funds are excluded.'],
          'Market countries gain taxing rights; a 15% floor stops the race to the bottom.',
          'Profits taxed at 9% in a jurisdiction attract a 6% top-up.'),
        C('c3', T3, [
            'Action 2 neutralises hybrid mismatch arrangements that produce deduction without inclusion or double deduction, via linking rules that deny deductions or require inclusion.',
            'Action 3 recommends strong controlled foreign company (CFC) rules to tax passive or mobile income parked in low-tax subsidiaries.',
            'Action 4 limits interest deductions to a fixed ratio of EBITDA (10%–30%). India\'s section 177 disallows interest above 30% of EBITDA (limited to interest on debt from non-resident AEs, including guaranteed third-party debt) where such interest exceeds ₹1 crore; banks, insurers and specified finance companies are excluded; disallowed interest can be carried forward for 8 years. Action 5 requires substantial activity (nexus approach) for preferential regimes — reflected in India\'s 10% tax on royalty from patents developed and registered in India.'],
          'Mismatches, parked profits and excess debt are targeted directly.',
          'Interest of ₹5 crore against EBITDA of ₹10 crore leads to a ₹2 crore disallowance.'),
        C('c4', T4, [
            'Action 6 prevents treaty abuse through a preamble on non-taxation, a principal purpose test (PPT) and optionally limitation of benefits (LOB) rules. Action 7 widens PE to curb commissionaire arrangements and fragmentation of preparatory activities.',
            'Actions 8–10 align transfer pricing outcomes with value creation (intangibles, risk and capital, high-risk transactions); Action 13 introduces the three-tier documentation of master file, local file and CbCR (India: sections 171 and 511); Action 14 improves MAP; Action 12 recommends mandatory disclosure rules; Action 11 measures BEPS.',
            'Action 15 created the Multilateral Instrument (MLI), allowing countries to update many treaties at once with BEPS measures; India has notified 93 jurisdictions and applies the PPT through the MLI where both parties have covered the treaty.'],
          'Treaties get anti-abuse rules; the MLI updates them en masse.',
          'A conduit company set up mainly for treaty benefits fails the PPT.'),
    ]

    jobs = [{'id': 'j1', 'title': 'BEPS impact review', 'role': 'International tax manager',
             'situation': 'A multinational group asks how BEPS rules affect its India operations.',
             'steps': ['Test section 177 on intra-group debt.', 'Review PE exposure after Action 7 changes.', 'Check MLI and PPT on treaty claims.', 'Estimate Pillar Two top-up exposure.'],
             'takeaway': 'BEPS touches financing, presence, treaties and minimum tax together.'}]

    mcqs = [
        Q('m1', 'Which is a BEPS minimum standard?', ['Action 6 — Preventing treaty abuse', 'Action 3 — CFC rules', 'Action 4 — Interest limitation', 'Action 12 — Mandatory disclosure'], 0,
          'Four minimum standards: 5, 6, 13, 14. In practice: peer reviewed.', 'c1', T1),
        Q('m2', 'Pillar Two\'s global minimum effective tax rate is:', ['Fifteen percent', 'Twenty-five percent', 'Ten percent', 'Twenty percent'], 0,
          'GloBE rules. In practice: top-up tax.', 'c2', T2),
        Q('m3', 'Section 177 disallows interest exceeding what share of EBITDA?', ['Thirty percent', 'Ten percent', 'Twenty-five percent', 'Fifty percent'], 0,
          'Action 4. In practice: lower of excess and AE interest.', 'c3', T3),
        Q('m4', 'Section 177 applies only when interest on AE debt exceeds:', ['One crore rupees', 'Ten crore rupees', 'Fifty lakh rupees', 'Five crore rupees'], 0,
          'Threshold. In practice: banks excluded.', 'c3', T3),
        Q('m5', 'Disallowed interest under section 177 can be carried forward for:', ['Eight tax years', 'Four tax years', 'Indefinitely', 'Two tax years'], 0,
          'Within 30% cap. In practice: track yearly.', 'c3', T3),
        Q('m6', 'Royalty from a patent developed and registered in India is taxed at:', ['Ten percent', 'Twenty percent', 'Fifteen percent', 'Thirty percent'], 0,
          'Patent box (Action 5 nexus). In practice: no expenses.', 'c3', T3),
        Q('m7', 'The Multilateral Instrument results from:', ['Action 15', 'Action 1', 'Action 13', 'Action 7'], 0,
          'Treaty updates. In practice: India notified 93 jurisdictions.', 'c4', T4),
        Q('m8', 'The three-tier TP documentation consists of master file, local file and:', ['Country-by-country report', 'Form No. 26', 'Transfer pricing order', 'APA'], 0,
          'Action 13. In practice: section 511.', 'c4', T4),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Cap and excess', 3, 'computation', 'EBITDA', nums=[lim, exc]), S('s2', 'Disallowance', 3, 'computation', 'lower', nums=[dis])],
          ['State threshold and carry forward.'], ['Disallowing all AE interest.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Patent royalty', 2, 'computation', '10%', nums=[pr]), S('s2', 'Top-up', 2, 'computation', 'top-up', nums=[tu])],
          ['Mention simplifications.'], ['Applying 15% to entire profit.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What does BEPS mean?', 'Planning that uses gaps and mismatches between tax systems to move profits to low-tax places where little real activity happens.',
          [P('p1', 'Mismatches', 5, 'mismatch'), P('p2', 'Low-tax', 5, 'low-tax')], 'c1'),
        V('v2', 'What is the nexus approach?', 'Preferential regimes for IP income should be linked to the R&D activity actually carried out by the taxpayer.',
          [P('p1', 'R&D activity', 5, 'r&d'), P('p2', 'IP income', 5, 'ip income')], 'c3'),
        V('v3', 'What is a hybrid mismatch?', 'An arrangement using differences in how two countries treat an entity or instrument, so that one payment is deducted twice or is deducted in one country while escaping inclusion in the other.',
          [P('p1', 'Differences in treatment', 5, 'differences'), P('p2', 'Deducted twice', 5, 'deducted twice')], 'c3'),
        V('v4', 'What is the principal purpose test?', 'Treaty benefits are denied if obtaining them was one of the principal purposes of an arrangement, unless consistent with the treaty\'s object.',
          [P('p1', 'Principal purposes', 5, 'principal purpose'), P('p2', 'Object', 5, 'object')], 'c4'),
        V('v5', 'Which groups are in scope for Pillar Two?', 'Multinational groups with consolidated revenue of €750 million or more.',
          [P('p1', 'Seven hundred fifty million', 5, '750'), P('p2', 'Multinational', 5, 'multinational')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Zeta Holdings', 'difficulty': 'moderate',
              'case': 'Zeta India Pvt Ltd has EBITDA of ₹20 crore and pays interest of ₹9 crore, all on a loan from a third-party bank that is guaranteed by its foreign parent. It is not a bank or NBFC.',
              'mcqs': [
                  M('k1a', 'Is the bank loan treated as debt from an associated enterprise?', ['Yes, because the parent guarantees it', 'No, the lender is unrelated', 'Only if parent deposits funds', 'Only for NBFCs'], 0,
                    'Deeming rule. In practice: section 177.', 'core', topic=T3),
                  M('k1b', '30% of EBITDA (₹ crore):', ['6', '9', '3', '2'], 0,
                    '30% × 20. In practice: cap.', 'core', check=6, topic=T3),
                  M('k1c', 'Interest disallowed (₹ crore):', ['3', '9', '6', '0'], 0,
                    'Lower of (9 − 6) and 9. In practice: carry forward.', 'core', check=3, topic=T3),
                  M('k1d', 'Which BEPS Action underlies this rule?', ['Action 4', 'Action 2', 'Action 6', 'Action 13'], 0,
                    'Interest limitation. In practice: fixed ratio.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch25', 1, 'Fundamentals of BEPS',
                ['Explain the BEPS project, pillars and minimum standards.',
                 'Explain the digital economy measures and Two-Pillar solution.',
                 'Apply hybrid, CFC, interest limitation and patent box measures.',
                 'Explain treaty abuse, PE, TP documentation and MLI measures.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 20}, 'prereq': ['fin-p4-ch24-u01'],
                 'exam_tip': 'Link each Action to India\'s implementing provision where one exists.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['15 Actions; minimum standards 5, 6, 13, 14.', 'Action 1: SEP; Pillar One and Pillar Two (15%).', 'Action 4: section 177 — 30% EBITDA, ₹1 crore, 8 years.',
                             'Action 5: patent box 10%.', 'Actions 6, 7, 8–10, 13, 14, 15: PPT, PE, TP, CbCR, MAP, MLI.'],
                 'remember': ['Section 177 disallows the lower of excess interest and AE interest.'],
                 'traps': ['Calling CFC rules a minimum standard.']},
                [('Interest limitation', 'Section 177'), ('SEP', 'Section 9(9)'), ('Patent royalty', 'Section 194(1)'), ('CbCR', 'Section 511')],
                viva, cases)
