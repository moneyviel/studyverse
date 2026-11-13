"""CA Final · Paper 4 · Chapter 11 Tax Planning, Tax Avoidance and Tax Evasion.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch11-u01'
T1 = 'Tax planning, avoidance and evasion'
T2 = 'Judicial approach and form versus substance'
T3 = 'Specific anti-avoidance rules on securities'
T4 = 'General Anti-Avoidance Rule'


def build():
    ck = Checks()
    loss = ck.add('1000*(120-100)', 'Loss on sale of units (₹)')
    inc = ck.add('1000*15', 'Exempt distribution received (₹)')
    allow = ck.add('1000*(120-100)-min(1000*(120-100),1000*15)', 'Loss allowed after section 175(8) (₹)')
    i1 = {'id': 'i1', 'title': 'Income stripping in business trust units', 'difficulty': 'core', 'minutes': 6,
          'q': 'Farah buys 1,000 units of an InvIT at ₹120 each six weeks before the record date. She receives an exempt distribution of ₹15 per unit and sells all units at ₹100 each two months after the record date. Compute the allowable loss.',
          'solution': [table(['Step', 'Working', '₹'], [
              ['Loss on sale', '1,000 × (120 − 100)', inr(loss)],
              ['Exempt income received', '1,000 × 15', inr(inc)],
              ['Loss ignored', 'To the extent of exempt income', inr(inc)],
              ['Allowable loss', '', inr(allow)]], title='Section 175(8)')],
          'checks': list(ck)}

    c2 = Checks()
    l2 = c2.add('2000*50-2000*30', 'Loss on original units ignored (₹)')
    dc = c2.add('2000*50-2000*30', 'Deemed cost of bonus units (₹)')
    i2 = {'id': 'i2', 'title': 'Bonus stripping', 'difficulty': 'core', 'minutes': 5,
          'q': 'Gautam buys 2,000 mutual fund units at ₹50 each one month before the record date for a 1:1 bonus. He sells the 2,000 original units at ₹30 each five months later and keeps the bonus units. Explain the tax treatment.',
          'solution': [table(['Item', 'Treatment', '₹'], [
              ['Loss on original units', 'Ignored under section 175(9)', inr(l2)],
              ['Cost of bonus units', 'Ignored loss deemed to be their cost', inr(dc)]], title='Section 175(9)')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'Tax planning arranges affairs within the law to use exemptions, deductions and reliefs the legislature intended — for example choosing between tax regimes, investing in eligible instruments or selecting a business form.',
            'Tax avoidance uses the letter of the law to defeat its intent, often through artificial or circular steps lacking commercial purpose; it is legal in form but countered by anti-avoidance rules. Tax evasion is illegal: suppression of income, inflating expenses, false documents or concealment, attracting penalty and prosecution.',
            'Tax management covers compliance — timely returns, TDS, audits and records — while tax planning looks ahead to structure transactions. Good planning should be natural, documented and backed by business substance.'],
          'Planning is lawful, avoidance is resisted, evasion is punished.',
          'Choosing section 200 rates is planning; recording fake purchases is evasion.'),
        C('c2', T2, [
            'The Westminster principle (UK, 1936) allowed taxpayers to arrange affairs to reduce tax if the form was genuine. Later UK cases like Ramsay looked at a composite series of pre-ordained steps and disregarded inserted artificial steps.',
            'In India, McDowell & Co. (1985) criticised colourable devices, while Azadi Bachao Andolan (2003) upheld treaty-based planning and Vodafone International (2012) held that genuine transactions are to be viewed as a whole and the revenue must establish sham or colourable devices.',
            'Under the doctrine of form and substance, the true nature of a transaction is determined from all its terms, not merely its label; but a genuine legal form is not lightly brushed aside.'],
          'Courts look through shams, not genuine choices.',
          'A circular loan routed through three entities to create interest deductions can be disregarded.'),
        C('c3', T3, [
            'Specific anti-avoidance rules (SAAR) target known schemes: transfer pricing, clubbing, deemed dividends, thin capitalisation limits on interest and others. Section 175 deals with transactions in securities.',
            'Income stripping (section 175(8)): if securities or units are bought within three months before the record date and sold within three months (securities) or nine months (units) after it, and the income received is exempt, the loss is ignored to the extent of that income. Since dividends and mutual fund income are now taxable, it mainly matters for business trust units.',
            'Bonus stripping (section 175(9)): if securities or units are bought within three months before the record date, bonus units are allotted, and the original units are sold within nine months while the bonus units are kept, the loss is ignored and treated as the cost of the bonus units.'],
          'Short-term in-and-out trades around record dates lose their losses.',
          'A ₹40,000 loss on stripped mutual fund units becomes the bonus units\' cost.'),
        C('c4', T4, [
            'GAAR (sections 178 to 184) allows an arrangement to be declared an impermissible avoidance arrangement (IAA) if its main purpose is a tax benefit and it (a) creates rights or obligations not at arm\'s length, (b) results in misuse or abuse of the Act, (c) lacks commercial substance (section 180 — e.g. round-trip financing, accommodating parties, offsetting elements, disguised location) or (d) is not carried out by means ordinarily used for bona fide purposes.',
            'Consequences (section 181): disregarding or recharacterising steps, treating connected parties as one, reallocating income or expenditure, ignoring corporate structures and denying treaty benefits. The AO refers the case to the PCIT/CIT, who may refer it to an Approving Panel.',
            'GAAR does not apply where aggregate tax benefit to all parties in the year is ₹3 crore or less, to specified FIIs and their non-resident investors, or to income from transfer of investments made before 1 April 2017. GAAR and SAAR can co-exist; GAAR is not barred merely because a SAAR applies.'],
          'GAAR attacks arrangements whose main aim is tax and which have a tainted element.',
          'A mid-year shift of profits to a tax-holiday unit with no business reason can be an IAA.'),
    ]

    jobs = [{'id': 'j1', 'title': 'GAAR risk review of a restructuring', 'role': 'Tax advisor',
             'situation': 'A group plans to interpose a holding company in a treaty jurisdiction.',
             'steps': ['Quantify tax benefit for all parties.', 'Assess main purpose and commercial substance.', 'Check tainted elements.', 'Document non-tax reasons.'],
             'takeaway': 'Substance and documentation protect planning from GAAR.'}]

    mcqs = [
        Q('m1', 'Suppressing sales to reduce tax is:', ['Tax evasion', 'Tax planning', 'Tax management', 'Tax mitigation'], 0,
          'Illegal concealment. In practice: penalty and prosecution.', 'c1', T1),
        Q('m2', 'Which case held that colourable devices cannot be part of tax planning?', ['McDowell & Co.', 'Duke of Westminster', 'Azadi Bachao Andolan', 'Vodafone International'], 0,
          'Supreme Court, 1985. In practice: later read narrowly.', 'c2', T2),
        Q('m3', 'Under section 175(8), units must be sold within how long after the record date?', ['Nine months', 'Three months', 'Six months', 'Twelve months'], 0,
          'Securities: three months. In practice: business trust units.', 'c3', T3),
        Q('m4', 'Loss ignored under bonus stripping is treated as:', ['Cost of the bonus units', 'Business loss', 'Capital loss carried forward', 'Exempt income'], 0,
          'Section 175(9). In practice: used on later sale.', 'c3', T3),
        Q('m5', 'GAAR does not apply where aggregate tax benefit in the year does not exceed:', ['Three crore rupees', 'One crore rupees', 'Five crore rupees', 'Ten crore rupees'], 0,
          'Rule 128. In practice: count all parties.', 'c4', T4),
        Q('m6', 'Which is a tainted element under GAAR?', ['Lack of commercial substance', 'Use of a deduction as intended', 'Filing return on time', 'Paying advance tax'], 0,
          'Section 179. In practice: plus main purpose test.', 'c4', T4),
        Q('m7', 'GAAR does not apply to income from transfer of investments made before:', ['1 April 2017', '1 April 2020', '1 April 2026', '1 April 2012'], 0,
          'Grandfathering. In practice: benefits after that date still covered.', 'c4', T4),
        Q('m8', 'Round-trip financing is an example of:', ['An arrangement lacking commercial substance', 'Tax planning', 'A deduction', 'A SAAR'], 0,
          'Section 180. In practice: funds return to origin.', 'c4', T4),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Conditions', 2, 'analysis', 'record date'), S('s2', 'Allowable loss', 3, 'computation', 'ignored', nums=[loss, inc, allow])],
          ['State time limits.'], ['Ignoring the full loss.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Loss ignored', 2, 'computation', 'ignored', nums=[l2]), S('s2', 'Deemed cost', 2, 'computation', 'bonus', nums=[dc])],
          ['Mention the nine-month window.'], ['Allowing the loss as capital loss.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'Distinguish tax avoidance and tax evasion.', 'Avoidance uses the letter of the law against its spirit and is legal in form; evasion uses illegal means such as concealment or falsification.',
          [P('p1', 'Letter of law', 5, 'letter'), P('p2', 'Illegal', 5, 'illegal')], 'c1'),
        V('v2', 'What did Vodafone International hold?', 'Transactions should be viewed as a whole, and the revenue must prove that a structure is a sham or colourable device.',
          [P('p1', 'Whole', 5, 'whole'), P('p2', 'Sham', 5, 'sham')], 'c2'),
        V('v3', 'What is the main purpose test in GAAR?', 'An arrangement whose main purpose is to obtain a tax benefit, combined with a tainted element, can be declared impermissible.',
          [P('p1', 'Main purpose', 5, 'main purpose'), P('p2', 'Tax benefit', 5, 'tax benefit')], 'c4'),
        V('v4', 'Can GAAR and SAAR both apply?', 'Yes, they co-exist and GAAR can be invoked even where a SAAR applies.',
          [P('p1', 'Co-exist', 5, 'co-exist|coexist'), P('p2', 'Invoked', 5, 'invoke')], 'c4'),
        V('v5', 'Who approves GAAR declarations in contested cases?', 'An Approving Panel, on reference by the PCIT or CIT.',
          [P('p1', 'Approving Panel', 5, 'approving panel'), P('p2', 'PCIT', 5, 'pcit|cit')], 'c4'),
    ]

    cases = [{'id': 'k1', 'title': 'Helix Group', 'difficulty': 'moderate',
              'case': 'Helix Group routes a ₹200 crore investment in its Indian subsidiary through a newly formed company in a treaty country with no employees or office, claiming treaty exemption on later capital gains. The expected aggregate tax benefit is ₹18 crore.',
              'mcqs': [
                  M('k1a', 'Does the GAAR monetary threshold bar its application?', ['No, the benefit exceeds three crore rupees', 'Yes', 'Only if below ten crore', 'Only for residents'], 0,
                    'Threshold ₹3 crore. In practice: aggregate benefit.', 'core', topic=T4),
                  M('k1b', 'The intermediate company with no staff or office suggests:', ['Lack of commercial substance', 'Genuine planning', 'Tax management', 'Evasion only'], 0,
                    'Section 180. In practice: substance test.', 'core', topic=T4),
                  M('k1c', 'A possible GAAR consequence is:', ['Denial of treaty benefit', 'Prosecution automatically', 'Cancellation of PAN', 'Refund of tax'], 0,
                    'Section 181. In practice: look-through.', 'core', topic=T4),
                  M('k1d', 'Tax benefit beyond the threshold (₹ crore):', ['15', '18', '3', '21'], 0,
                    '18 − 3. In practice: threshold is a gate, not a deduction.', 'core', check=15, topic=T4),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch11', 1, 'Tax Planning, Tax Avoidance and Tax Evasion',
                ['Distinguish tax planning, avoidance and evasion.',
                 'Apply judicial doctrines including form and substance.',
                 'Apply anti-avoidance rules on dividend, income and bonus stripping.',
                 'Apply GAAR conditions, consequences and exclusions.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['fin-p4-ch10-u01'],
                 'exam_tip': 'For GAAR questions, test threshold, main purpose and each tainted element separately.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Planning vs avoidance vs evasion.', 'Westminster, McDowell, Azadi Bachao, Vodafone.', 'Section 175(8) income stripping; 175(9) bonus stripping.',
                             'GAAR sections 178–184; ₹3 crore threshold; 1 April 2017 grandfathering.'],
                 'remember': ['GAAR needs main purpose plus a tainted element.'],
                 'traps': ['Assuming SAAR excludes GAAR.']},
                [('Stripping', 'Section 175'), ('GAAR', 'Sections 178–184'), ('Threshold', 'Rule 128')],
                viva, cases)
