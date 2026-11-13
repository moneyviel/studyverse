"""CA Final · Paper 4 · Chapter 26 Application and Interpretation of Tax Treaties.
Scope follows the ICAI study material under the Income-tax Act, 2025; explanations, names and figures are original and machine-checked."""
from fkit import *

UID = 'fin-p4-ch26-u01'
T1 = 'Nature of tax treaties and their legal status in India'
T2 = 'Vienna Convention principles of interpretation'
T3 = 'Aids to interpretation: commentaries, protocols and MFN'
T4 = 'Judicial approach in India'


def build():
    ck = Checks()
    a = ck.add('10000000*0.20', 'Tax under the Act at 20% (₹)')
    t = ck.add('10000000*0.10', 'Tax under the treaty at 10% (₹)')
    m = ck.add('10000000*0.05', 'Tax if MFN benefit of 5% is validly available (₹)')
    i1 = {'id': 'i1', 'title': 'Act, treaty or MFN rate?', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'A company resident in Country F (an OECD member) receives dividends of ₹1 crore from an Indian company. The Act rate is 20%; the India–F treaty rate is 10%; its protocol has an MFN clause. India later agreed a 5% rate with Country G, which joined the OECD after signing its treaty with India, and no separate notification importing the MFN benefit has been issued. Compute tax under each view.',
          'solution': [table(['View', 'Basis', '₹'], [
              ['Act', '20% × 1 crore', inr(a)],
              ['Treaty', '10% × 1 crore — more beneficial, applies', inr(t)],
              ['MFN claim', '5% would give', inr(m)],
              ['Conclusion', 'Per Nestle SA: MFN needs notification and the third state must be OECD member when its treaty was signed', 'Treaty rate applies']], title='Section 159 and Protocol')],
          'checks': list(ck)}

    c2 = Checks()
    n = c2.add('3', 'Elements of Article 31(1): good faith, ordinary meaning in context, object and purpose')
    i2 = {'id': 'i2', 'title': 'Interpreting an undefined treaty term', 'difficulty': 'core', 'minutes': 5,
          'q': 'A treaty uses the term "technical services" without defining it, and the Indian Act defines a similar term. Outline the approach to interpretation.',
          'solution': [table(['Step', 'Approach', 'Source'], [
              ['1', f'Apply Article 31(1) — {n} elements: good faith, ordinary meaning in context, object and purpose', 'VCLT'],
              ['2', 'Use context: text, preamble, protocol, related agreements', 'Article 31(2)'],
              ['3', 'Use domestic meaning under Article 3(2) unless context requires otherwise; Government notification under section 159', 'Treaty and Act'],
              ['4', 'Use supplementary means (commentaries, preparatory work) to confirm or resolve ambiguity', 'Article 32']], title='Treaty interpretation')],
          'checks': list(c2)}

    concepts = [
        C('c1', T1, [
            'A tax treaty (DTAA) is an international agreement under which two states allocate taxing rights, eliminate double taxation, prevent fiscal evasion and provide for exchange of information and assistance. It usually comprises the main text, protocol, memorandum of understanding and exchange of letters.',
            'In India, Article 51 of the Constitution encourages respect for international law, and section 159 of the Income-tax Act, 2025 empowers the Government to enter into agreements. The provisions of the Act apply to the extent more beneficial, so a treaty cannot impose tax beyond the Act, but its benefits override the Act. Section 159(4) lets the Government notify meanings for undefined treaty terms.',
            'Treaty benefits remain subject to conditions in the Act, such as a tax residency certificate and GAAR.'],
          'Treaties allocate rights; the more beneficial of Act and treaty applies.',
          'A treaty rate of 10% on dividends overrides the Act\'s 20%.'),
        C('c2', T2, [
            'India is not a party to the Vienna Convention on the Law of Treaties, 1969, but courts treat its principles as customary international law. Article 26 (pacta sunt servanda) requires treaties to be performed in good faith; Article 27 prevents a party from invoking domestic law to justify non-performance.',
            'Article 31: a treaty is interpreted in good faith according to the ordinary meaning of its terms in context and in light of its object and purpose; context includes text, preamble, annexes and related agreements; subsequent agreements and practice are also considered.',
            'Article 32 allows supplementary means — preparatory work and circumstances of conclusion — to confirm the meaning or resolve ambiguity or absurd results; Article 33 deals with treaties authenticated in more than one language.'],
          'Good faith, ordinary meaning, context and purpose — then supplementary aids.',
          'Courts have relied on Article 31 in Indian treaty disputes even though India has not ratified the Convention.'),
        C('c3', T3, [
            'OECD and UN Model Commentaries, and works such as Klaus Vogel and Philip Baker, are persuasive aids; the relevance of later commentaries (ambulatory approach) versus those existing at signing (static approach) is debated.',
            'A protocol is an integral part of the treaty with equal binding force; it often clarifies terms or contains a most-favoured-nation (MFN) clause that extends better terms India grants later to other OECD members.',
            'In AO v. Nestle SA (2023), the Supreme Court held that an MFN benefit requires a separate notification under section 90 of the 1961 Act (now section 159), and that the third state must be an OECD member when its treaty with India was signed; a protocol cannot alter domestic law without notification.'],
          'Protocols bind; MFN benefits need notification.',
          'An MFN claim based on a treaty with a later OECD entrant fails.'),
        C('c4', T4, [
            'In Union of India v. Azadi Bachao Andolan (2003), the Supreme Court upheld CBDT circulars on the India–Mauritius treaty, held that treaty shopping is not illegal per se absent limitation-of-benefit clauses, and accepted that treaties are interpreted liberally to give effect to their purpose.',
            'In Ram Jethmalani v. Union of India (2011), the Court recognised that treaty obligations under the Vienna Convention must be performed in good faith; other rulings have referred to Articles 31 and 32 for interpretation.',
            'Courts have also held that undefined terms take meanings under the domestic law (Article 3(2)) unless the context requires otherwise. Where a treaty refers to domestic law, the meaning in force when the treaty is applied may be relevant (ambulatory), while later Model Commentaries are persuasive but cannot rewrite an earlier bargain.'],
          'Indian courts read treaties purposively and in good faith.',
          'Azadi Bachao Andolan validated reliance on a TRC for treaty benefits at that time.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Treaty position paper', 'role': 'International tax associate',
             'situation': 'A client wants to apply a lower treaty rate via an MFN clause.',
             'steps': ['Read the treaty, protocol and exchange of letters.', 'Check notifications under section 159.', 'Apply Nestle SA conditions.', 'Document interpretation using VCLT principles.'],
             'takeaway': 'Protocol plus notification decide MFN outcomes.'}]

    mcqs = [
        Q('m1', 'Between the Act and a treaty, the assessee is taxed under:', ['Whichever is more beneficial', 'The treaty always', 'The Act always', 'The higher of the two'], 0,
          'Section 159. In practice: subject to TRC and GAAR.', 'c1', T1),
        Q('m2', 'Pacta sunt servanda is in which Article of the Vienna Convention?', ['Article 26', 'Article 31', 'Article 32', 'Article 33'], 0,
          'Good faith performance. In practice: binding effect.', 'c2', T2),
        Q('m3', 'Supplementary means of interpretation appear in:', ['Article 32', 'Article 31', 'Article 26', 'Article 27'], 0,
          'Preparatory work. In practice: confirm or clarify.', 'c2', T2),
        Q('m4', 'India\'s status regarding the Vienna Convention is:', ['Not a party, but its principles are applied as customary law', 'A full party', 'It rejects it', 'Party only for tax'], 0,
          'Courts apply principles. In practice: Article 31.', 'c2', T2),
        Q('m5', 'A protocol to a treaty is:', ['An integral part with equal force', 'Only advisory', 'Valid only if separately ratified', 'Superseded by the Act'], 0,
          'Binding. In practice: read before concluding.', 'c3', T3),
        Q('m6', 'Per Nestle SA, an MFN benefit requires:', ['A separate notification', 'Only the protocol', 'A tribunal order', 'A TRC'], 0,
          'Supreme Court 2023. In practice: OECD status at signing.', 'c3', T3),
        Q('m7', 'Which case upheld circulars on the India–Mauritius treaty?', ['Azadi Bachao Andolan', 'Nestle SA', 'Ram Jethmalani', 'Vodafone'], 0,
          'Supreme Court 2003. In practice: LOB absent then.', 'c4', T4),
        Q('m8', 'Using commentaries existing at the time of signing reflects the:', ['Static approach', 'Ambulatory approach', 'Literal rule', 'Mischief rule'], 0,
          'Interpretation debate. In practice: courts vary.', 'c3', T3),
    ]

    questions = [
        W('q1', 6, i1['q'], i1['solution'],
          [S('s1', 'Act versus treaty', 3, 'computation', 'treaty', nums=[a, t]), S('s2', 'MFN analysis', 3, 'analysis', 'Nestle', nums=[m])],
          ['Cite the case.'], ['Applying MFN without notification.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'General rule', 2, 'analysis', 'ordinary meaning', nums=[n]), S('s2', 'Domestic meaning and aids', 2, 'analysis', 'supplementary')],
          ['Order the steps.'], ['Starting with commentaries.'], ['Table.'], pad='table', checks=list(c2)),
    ]

    viva = [
        V('v1', 'What does Article 31(1) of the VCLT require?', 'Interpretation in good faith according to the ordinary meaning of terms in their context and in light of the treaty\'s object and purpose.',
          [P('p1', 'Good faith', 5, 'good faith'), P('p2', 'Object and purpose', 5, 'object and purpose')], 'c2'),
        V('v2', 'What is an MFN clause?', 'A protocol clause extending to the treaty partner better terms that India later grants to another specified state.',
          [P('p1', 'Protocol', 5, 'protocol'), P('p2', 'Better terms', 5, 'better terms')], 'c3'),
        V('v3', 'Can a treaty impose tax beyond the Act?', 'Tax is limited by the Act; a treaty applies only where it is more beneficial to the assessee.',
          [P('p1', 'More beneficial', 5, 'more beneficial'), P('p2', 'Act', 5, 'act')], 'c1'),
        V('v4', 'What does Article 27 of the VCLT say?', 'A party is barred from citing its internal law to justify failing to perform a treaty.',
          [P('p1', 'Internal law', 5, 'internal law'), P('p2', 'Perform', 5, 'perform')], 'c2'),
        V('v5', 'Name two classic commentaries on tax treaties.', 'Klaus Vogel\'s and Philip Baker\'s commentaries.',
          [P('p1', 'Vogel', 5, 'vogel'), P('p2', 'Baker', 5, 'baker')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'Royalty to Freyja SA', 'difficulty': 'core',
              'case': 'Freyja SA, a resident of a treaty country, receives royalty of ₹2 crore from an Indian company. The Act rate is 20% and the treaty rate is 10%. Freyja has a valid TRC and furnished Form No. 41.',
              'mcqs': [
                  M('k1a', 'Tax at the Act rate (₹):', ['40,00,000', '20,00,000', '10,00,000', '60,00,000'], 0,
                    '20% × 2 crore. In practice: compare with treaty.', 'core', check=4000000, topic=T1),
                  M('k1b', 'Tax at the treaty rate (₹):', ['20,00,000', '40,00,000', '10,00,000', '30,00,000'], 0,
                    '10% × 2 crore. In practice: TRC needed.', 'core', check=2000000, topic=T1),
                  M('k1c', 'Which rate applies?', ['Treaty rate, being more beneficial', 'Act rate', 'Average of both', 'Higher of both'], 0,
                    'Section 159. In practice: subject to GAAR/PPT.', 'core', topic=T1),
                  M('k1d', 'If "royalty" is undefined in the treaty, meaning is first sought from:', ['Domestic law unless context requires otherwise', 'OECD commentary only', 'Dictionary only', 'Tribunal decisions only'], 0,
                    'Article 3(2). In practice: treaties usually define it.', 'core', topic=T2),
              ]}]

    return unit(UID, 'p4', 'fin-p4-ch26', 1, 'Application and Interpretation of Tax Treaties',
                ['Explain the nature and legal status of tax treaties in India.',
                 'Apply Vienna Convention principles of interpretation.',
                 'Use commentaries, protocols and MFN clauses.',
                 'Apply key Indian judicial decisions on treaties.'],
                {'difficulty': 'moderate', 'minutes': {'learn': 30, 'practice': 15}, 'prereq': ['fin-p4-ch25-u01'],
                 'exam_tip': 'Start with Article 31, then move to domestic meaning and supplementary aids.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Section 159: more beneficial of Act and treaty.', 'VCLT Articles 26, 27, 31, 32, 33.', 'Commentaries: static vs ambulatory.',
                             'Protocols binding; MFN needs notification (Nestle SA).', 'Azadi Bachao Andolan; Ram Jethmalani.'],
                 'remember': ['India is not a party to VCLT but applies its principles.'],
                 'traps': ['Claiming MFN benefit without notification.']},
                [('Treaty power', 'Section 159'), ('Interpretation', 'VCLT Art. 31–32'), ('MFN', 'Nestle SA (2023)')],
                viva, cases)
