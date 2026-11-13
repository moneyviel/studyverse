"""CA Final · Paper 5 · Chapter 21 Offences and Penalties and Ethical Aspects under GST.
Scope follows the ICAI study material (May/Nov 2027); explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p5-ch21-u01'
T1 = 'Penalties under section 122 and general penalty'
T2 = 'Detention and confiscation of goods in transit'
T3 = 'Prosecution and compounding'
T4 = 'Principles of penalty and ethical aspects'


def build():
    ck = Checks()
    a = ck.add('90000*2', 'Penalty when owner comes forward: 200% of tax (₹)')
    b = ck.add('max(500000*0.50,90000*2)', 'Penalty when owner does not come forward (₹)')
    i1 = {'id': 'i1', 'title': 'Goods detained without documents', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Goods worth ₹5,00,000 on which total tax payable is ₹90,000 are detained in transit without valid documents. Using the section 129 formulas on total tax, compute penalty if (a) the owner comes forward and (b) the owner does not come forward.',
          'solution': [table(['Case', 'Rule', '₹'], [
              ['(a) Owner comes forward', '200% of tax payable', inr(a)],
              ['(b) Owner does not come forward', 'Higher of 50% of value and 200% of tax', inr(b)],
              ['Release', 'On payment or security equivalent to the penalty', '—']], title='Section 129')],
          'checks': list(ck)}

    c2 = Checks()
    lo = c2.add('30000000*0.25', 'Minimum compounding amount at 25% of tax (₹)')
    hi = c2.add('30000000*1.00', 'Maximum compounding amount at 100% of tax (₹)')
    i2 = {'id': 'i2', 'title': 'Prosecution and compounding', 'difficulty': 'moderate', 'minutes': 6,
          'q': 'Raj Enterprises wrongly availed ITC of ₹3 crore using fake invoices (first offence). State the punishment and the compounding range.',
          'solution': [table(['Point', 'Rule', 'Result'], [
              ['Punishment', 'Amount above ₹2 crore up to ₹5 crore', 'Imprisonment up to 3 years and fine'],
              ['Nature', 'Not above ₹5 crore', 'Non-cognizable and bailable'],
              ['Compounding range', '25% to 100% of tax involved', f'₹{inr(lo)} to ₹{inr(hi)}']], title='Sections 132 and 138')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Section 122(1) lists 21 offences by taxable persons — e.g. supplying without invoice or with false invoice, issuing invoices without supply, collecting tax but not paying within three months, wrongly availing ITC or refund, not deducting or collecting tax, evading registration, obstructing officers, and dealing in goods liable to confiscation. Penalty is the higher of ₹10,000 (₹20,000 under IGST) and the tax evaded, ITC wrongly availed or refund wrongly obtained.',
            'Section 122(1A) penalises any person who retains the benefit of or causes specified offences (fake invoices, wrongful ITC) with an amount equal to the tax evaded or ITC passed on. Section 122(1B) penalises ECOs for allowing supplies by unregistered or ineligible persons. Section 122(2) covers registered persons short paying tax for non-fraud (higher of ₹10,000 and 10% of tax) or fraud reasons (higher of ₹10,000 and tax).',
            'Section 122(3) penalises those who aid, abet or deal in goods liable to confiscation with up to ₹25,000. Section 125 imposes a general penalty up to ₹25,000 for contraventions with no specific penalty. Section 122B (track and trace) penalises a person who breaches the track and trace mechanism of section 148A with an extra penalty of ₹1 lakh or 10% of tax payable on the goods, whichever is higher.'],
          'Penalties scale with tax evaded, with fixed minimums.',
          'Issuing invoices without supply attracts penalty at least equal to ITC passed on.'),
        C('c2', T2, [
            'Section 129: goods and conveyances in transit in contravention of the law may be detained or seized and released on payment of penalty: if the owner comes forward, 200% of tax payable (for exempt goods, lower of 2% of value and ₹25,000); if the owner does not, the higher of 50% of value and 200% of tax (exempt goods: lower of 5% of value and ₹25,000). IGST amounts are doubled correspondingly.',
            'A notice must be issued within seven days of detention and an order passed within seven days of notice; if penalty is not paid within 15 days of the order, the goods or conveyance may be sold or disposed of.',
            'Section 130: goods or conveyances used to evade tax with intent are liable to confiscation; the owner may pay a fine in lieu of confiscation not exceeding market value minus tax, plus tax and penalty; a conveyance owner who did not know of its use may pay a fine equal to tax on the goods.'],
          'Transit violations cost 200% of tax or more.',
          'Goods worth ₹5 lakh with ₹90,000 tax detained without bills can attract ₹2.5 lakh penalty if no owner appears.'),
        C('c3', T3, [
            'Section 132: offences like supply without invoice, fake invoices, fraudulent ITC or refund are punishable with imprisonment up to 5 years (amount above ₹5 crore), 3 years (₹2–5 crore), 1 year (₹1–2 crore), plus fine; falsification and obstruction up to 6 months. Repeat offences carry up to 5 years. Offences above ₹5 crore under specified clauses are cognizable and non-bailable; others non-cognizable and bailable. Prosecution needs prior sanction of the Commissioner.',
            'Section 138: offences (except specified serious ones and repeat cases) may be compounded by the Commissioner, before or after prosecution, on payment of a compounding amount between 25% and 100% of tax involved, as per rule 162, after paying tax, interest and penalty.',
            'Compounding is not available to a person who has been allowed compounding earlier for certain offences, or who has committed specified offences (like supplying without invoice) above specified amounts.'],
          'Serious fraud may lead to prosecution; compounding offers settlement.',
          'Fake ITC of ₹3 crore can attract imprisonment up to three years.'),
        C('c4', T4, [
            'Section 126: no penalty for minor breaches (tax involved below ₹5,000) or easily rectifiable procedural mistakes without fraudulent intent or gross negligence; penalty must depend on facts and be proportionate; a person must be heard and reasons recorded; voluntary disclosure is considered a mitigating factor.',
            'Section 127 lets the officer impose penalty where it is not covered by other proceedings after giving a hearing. Section 128 enables waiver of penalty and late fee by notification.',
            'Ethical aspects: professionals must avoid facilitating fake invoices, ensure correct ITC claims, and maintain integrity — misuse of GST for fraudulent ITC harms the system and attracts personal liability under section 122(1A).'],
          'Penalties must be fair, reasoned and proportionate.',
          'A spelling error in an invoice with no tax effect should not be penalised.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Transit detention response', 'role': 'GST consultant',
             'situation': 'A client\'s truck is detained for an expired e-way bill.',
             'steps': ['Check notice within 7 days.', 'Determine penalty under section 129.', 'Arrange payment or security for release.', 'Contest if procedural lapse only.'],
             'takeaway': 'Quick action prevents disposal of goods.'}]

    mcqs = [
        Q('m1', 'Minimum penalty under section 122(1) under CGST law is:', ['Ten thousand rupees', 'Twenty-five thousand rupees', 'Five thousand rupees', 'One lakh rupees'], 0,
          'Or tax evaded if higher. In practice: IGST ₹20,000.', 'c1', T1),
        Q('m2', 'General penalty under section 125 extends to:', ['Twenty-five thousand rupees', 'Ten thousand rupees', 'One lakh rupees', 'Fifty thousand rupees'], 0,
          'Residual. In practice: proportionate.', 'c1', T1),
        Q('m3', 'Penalty under section 129 when owner comes forward for taxable goods is:', ['Two hundred percent of tax payable', 'Fifty percent of value', 'One hundred percent of tax', 'Ten percent of tax'], 0,
          'Section 129(1)(a). In practice: release on payment.', 'c2', T2),
        Q('m4', 'Notice under section 129 must be issued within how many days of detention?', ['Seven', 'Fifteen', 'Thirty', 'Three'], 0,
          'Section 129(3). In practice: order within 7 days.', 'c2', T2),
        Q('m5', 'Imprisonment for fraudulent ITC above ₹5 crore may extend to:', ['Five years', 'Three years', 'One year', 'Seven years'], 0,
          'Section 132(1)(i). In practice: minimum six months.', 'c3', T3),
        Q('m6', 'Compounding amount ranges between:', ['Twenty-five and one hundred percent of tax', 'Ten and fifty percent', 'Fifty and two hundred percent', 'Nil and twenty-five percent'], 0,
          'Section 138(2). In practice: rule 162.', 'c3', T3),
        Q('m7', 'No penalty for minor breaches where tax involved is below:', ['Five thousand rupees', 'Ten thousand rupees', 'One thousand rupees', 'Twenty-five thousand rupees'], 0,
          'Section 126. In practice: no fraudulent intent.', 'c4', T4),
        Q('m8', 'Penalty on a person who retains benefit of fake-invoice ITC is under:', ['Section 122(1A)', 'Section 125', 'Section 129', 'Section 130'], 0,
          'Beneficiary liability. In practice: equal to ITC passed.', 'c1', T1),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Owner comes forward', 2, 'computation', '200%', nums=[a]), S('s2', 'Owner absent', 3, 'computation', '50%', nums=[b])],
          ['Mention release on security.'], ['Applying 50% when owner comes forward.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 5, i2['q'], i2['solution'],
          [S('s1', 'Punishment', 2, 'analysis', '3 years'), S('s2', 'Compounding', 3, 'computation', '25%', nums=[lo, hi])],
          ['Classify the offence.'], ['Treating it as cognizable.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What is fine in lieu of confiscation?', 'A fine up to market value minus tax, paid in addition to tax and penalty, to redeem confiscated goods.',
          [P('p1', 'Market value', 5, 'market value'), P('p2', 'Redeem', 5, 'redeem')], 'c2'),
        V('v2', 'Who sanctions GST prosecution?', 'The Commissioner must give prior sanction.',
          [P('p1', 'Commissioner', 5, 'commissioner'), P('p2', 'Sanction', 5, 'sanction')], 'c3'),
        V('v3', 'What penalty applies to an ECO allowing ineligible suppliers?', 'Under section 122(1B), the higher of ₹10,000 and the tax involved.',
          [P('p1', '122(1B)', 5, '1b'), P('p2', 'Tax involved', 5, 'tax involved')], 'c1'),
        V('v4', 'Is voluntary disclosure relevant to penalty?', 'Yes, section 126 treats it as a mitigating factor.',
          [P('p1', 'Mitigating', 5, 'mitigat'), P('p2', 'Section 126', 5, '126')], 'c4'),
        V('v5', 'What happens if penalty under section 129 is unpaid within 15 days of the order?', 'The goods or conveyance may be sold or disposed of to recover the amount.',
          [P('p1', 'Sold', 5, 'sold'), P('p2', 'Disposed', 5, 'dispos')], 'c2'),
    ]

    cases = [{'id': 'k1', 'title': 'Exempt goods detained', 'difficulty': 'core',
              'case': 'Exempt goods worth ₹20,00,000 are detained for missing documents; the owner comes forward.',
              'mcqs': [
                  M('k1a', '2% of value (₹):', ['40,000', '25,000', '20,000', '1,00,000'], 0,
                    '2% × 20 lakh. In practice: compare with cap.', 'core', check=40000, topic=T2),
                  M('k1b', 'Penalty under CGST law (₹):', ['25,000', '40,000', '50,000', 'Nil'], 0,
                    'Lower of 2% and ₹25,000. In practice: equal SGST penalty.', 'core', check=25000, topic=T2),
                  M('k1c', 'If the owner did not come forward, penalty under CGST law (₹):', ['25,000', '1,00,000', '50,000', '2,00,000'], 0,
                    'Lower of 5% (₹1 lakh) and ₹25,000. In practice: cap applies.', 'core', check=25000, topic=T2),
                  M('k1d', 'Is the detention lawful if documents were genuinely missing?', ['Yes', 'No', 'Only for taxable goods', 'Only with a court order'], 0,
                    'Section 129 covers contravention. In practice: procedural nature considered.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p5', 'fin-p5-ch21', 1, 'Offences and Penalties and Ethical Aspects under GST',
                ['Apply penalties under section 122 and the general penalty.',
                 'Compute penalties for goods in transit and confiscation.',
                 'Apply prosecution and compounding provisions.',
                 'Apply principles of penalty and ethical aspects.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 40, 'practice': 25}, 'prereq': ['fin-p5-ch20-u01'],
                 'exam_tip': 'For section 129, first ask whether the owner came forward and whether goods are taxable.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 122: 21 offences; higher of ₹10,000 and tax.', 'Section 122(1A), (1B), (2), (3); section 125 ₹25,000.', 'Section 129: 200%; higher of 50% of value and 200%.',
                             'Section 130 confiscation; fine in lieu.', 'Section 132: 5/3/1 years; section 138 compounding 25–100%.'],
                 'remember': ['No penalty for minor breaches below ₹5,000.'],
                 'traps': ['Mixing section 129 and 130 consequences.']},
                [('Penalties', 'Section 122'), ('General penalty', 'Section 125'), ('Detention', 'Section 129'), ('Prosecution', 'Section 132'), ('Compounding', 'Section 138')],
                viva, cases)
