"""CA Intermediate · Paper 2 Corporate and Other Laws · Part II Chapter 2 Interpretation of Statutes, Deeds and Documents.
Scope follows the ICAI study material; explanations and examples are original."""
from ikit import *

UID = 'int-p2-ii-ch02-u01'
T1 = 'Statutes and why interpretation is needed'
T2 = 'Primary rules: literal, mischief, golden and harmonious construction'
T3 = 'Secondary rules: noscitur a sociis, ejusdem generis, reddendo singula singulis'
T4 = 'Internal aids to interpretation'
T5 = 'External aids and interpretation of deeds and documents'


def build():
    i1 = {'id': 'i1', 'title': 'Which rule applies?', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'Apply the right rule: (a) A law taxes "cars, trucks, buses and other vehicles". Is a bicycle covered? (b) A law prohibits "sleeping on railway platforms". Is a passenger who dozes off while waiting for a late train guilty? (c) Two sections of the same Act appear to conflict. How should a court read them?',
          'solution': [table(['Situation', 'Rule', 'Likely answer'], [
              ['(a) "other vehicles" after motor vehicles', 'Ejusdem generis — general words take the meaning of the specific class before them', 'Covers only motor vehicles; a bicycle is outside'],
              ['(b) Dozing while waiting', 'Mischief rule / golden rule — read in light of the mischief aimed at (vagrants using platforms as beds)', 'Not guilty — the law targets those using platforms as sleeping places'],
              ['(c) Apparent conflict', 'Harmonious construction — read both so each has effect', 'Reconcile them; avoid making either a dead letter']], title='Rules of interpretation')],
          'checks': []}

    i2 = {'id': 'i2', 'title': 'Using aids to interpretation', 'difficulty': 'core', 'minutes': 6,
          'q': 'A section of a tax law is ambiguous. Its heading, an illustration below it and the Finance Minister\'s budget speech all point to one meaning. Which of these are internal and which external aids, and can they be used?',
          'solution': [table(['Aid', 'Type', 'Use'], [
              ['Heading of the section', 'Internal', 'May be used to resolve ambiguity; cannot override clear words'],
              ['Illustration', 'Internal', 'Helps explain the section; cannot narrow or widen clear text'],
              ['Budget speech', 'External (parliamentary material)', 'May be referred to for the purpose and background where the words are ambiguous']], title='Aids')],
          'checks': []}

    concepts = [
        C('c1', T1, [
            'A statute is law enacted by Parliament or a State Legislature. Interpretation is the process by which courts find the true meaning of the words used and the legislature\'s intention; construction goes further, drawing conclusions about matters not directly covered.',
            'Interpretation is needed because language is imperfect, situations unforeseen by the drafters arise, and words may have several meanings.',
            'Statutes, deeds and documents are interpreted by the same broad approach: find the intention from the words used, read as a whole.'],
          'Interpretation finds what the law-maker meant from what the law-maker wrote.',
          'Whether "computer" in an old Act includes a smartphone is a question of interpretation.'),
        C('c2', T2, [
            'Literal rule: words are given their plain, ordinary meaning. If the language is clear, the court applies it even if the result seems harsh; consequences are for the legislature.',
            'Mischief rule (Heydon\'s case): the court asks what the law was before, what mischief it did not cover, what remedy Parliament provided, and the true reason for it — and reads the words to suppress the mischief and advance the remedy.',
            'Golden rule: the literal meaning is modified only so far as needed to avoid absurdity, repugnancy or inconsistency.',
            'Harmonious construction: where two provisions seem to conflict, they are read so that both operate; one should not be read to defeat the other. Where reconciliation is impossible, the specific provision prevails over the general.'],
          'Start with the words; depart only to avoid absurdity, conflict or defeat of the law\'s purpose.',
          'A law against "drawing a weapon at a person" is read to include an unloaded gun because that was the mischief targeted.'),
        C('c3', T3, [
            'Noscitur a sociis: a word is known by the company it keeps — a doubtful word takes colour from words around it.',
            'Ejusdem generis: where general words follow specific words of a distinct class, the general words are limited to things of the same class. The rule applies only if the specific words form a class.',
            'Reddendo singula singulis: where several words are used together referring to several subjects, each word applies to its matching subject.',
            'Strict construction applies to penal and taxing statutes: any reasonable doubt is resolved in favour of the subject. Beneficial (welfare) laws are construed liberally in favour of those they protect.'],
          'Words are read with their neighbours and their class.',
          '"Warehouses, shops and other places" in a licensing law refers to places of business, not private homes.'),
        C('c4', T4, [
            'Internal aids are found within the statute: long title and preamble (to understand purpose when words are unclear), headings of chapters and sections, marginal notes (limited weight), definitions and interpretation clauses ("means" is exhaustive; "includes" is extensive), illustrations, provisos (an exception carved out of the main enactment), explanations (clarify meaning), schedules, and punctuation (minor weight).',
            'Internal aids help resolve ambiguity but cannot control clear words of the enacting provision.'],
          'Look inside the Act first — titles, definitions, provisos and illustrations.',
          'A definition using "includes" enlarges the ordinary meaning rather than limiting it.'),
        C('c5', T5, [
            'External aids come from outside the statute: parliamentary history (bills, statements of objects and reasons, debates, committee reports — used with care), historical background and earlier laws, later social, political and technological developments, dictionaries, foreign decisions on similar laws, textbooks, and other statutes on the same subject (in pari materia).',
            'Deeds and documents are interpreted to find the intention of the parties from the whole document: plain meaning first; where words are ambiguous, the circumstances may be considered; where two clauses truly conflict, the earlier clause generally prevails in a deed, while in a will the later clause prevails (as the last expression of intention); specific words control general ones.'],
          'When the Act itself is unclear, its history and context can help.',
          'Courts have used the Oxford dictionary to decide whether "manufacture" covers a process.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Advising on an unclear provision', 'role': 'Article assistant',
             'situation': 'A client is unsure whether a new GST exemption covering "fruits, vegetables and other produce" applies to dried spices.',
             'steps': ['Read the words literally.', 'Check the definitions and explanations in the Act.', 'Apply ejusdem generis and noscitur a sociis.', 'Look at the notification\'s purpose and any circulars.'],
             'takeaway': 'Use rules and aids together to support a reasoned view.'}]

    mcqs = [
        Q('m1', 'The rule that gives words their plain and ordinary meaning is the:', ['Literal rule', 'Mischief rule', 'Golden rule', 'Rule of harmonious construction'], 0,
          'The literal rule applies the ordinary grammatical meaning of words; if clear, it must be followed even if the outcome is harsh. Other rules come in only when literal reading fails. In practice: start here.', 'c2', T2),
        Q('m2', 'Heydon\'s case is associated with the:', ['Mischief rule', 'Literal rule', 'Golden rule', 'Ejusdem generis rule'], 0,
          'Heydon\'s case laid down the mischief rule: identify the previous law, the mischief, the remedy and its reason, and interpret to suppress the mischief and advance the remedy. In practice: useful for remedial laws.', 'c2', T2),
        Q('m3', 'Where two provisions of the same Act appear to conflict, courts apply:', ['Harmonious construction', 'The literal rule only', 'Ejusdem generis', 'Strict construction'], 0,
          'Harmonious construction reads both provisions so that each has effect; only if they cannot be reconciled does the specific one prevail over the general. In practice: avoid making a provision useless.', 'c2', T2),
        Q('m4', 'General words following particular words of the same class are limited to that class under:', ['Ejusdem generis', 'Noscitur a sociis', 'Reddendo singula singulis', 'The golden rule'], 0,
          'Ejusdem generis limits general words to things of the same kind as the specific words they follow, provided those specific words form a genus. In practice: check that a class exists.', 'c3', T3),
        Q('m5', '"A word is known by the company it keeps" describes:', ['Noscitur a sociis', 'Ejusdem generis', 'Literal rule', 'Mischief rule'], 0,
          'Noscitur a sociis says the meaning of a doubtful word may be found from associated words. It is broader than ejusdem generis. In practice: read lists as a whole.', 'c3', T3),
        Q('m6', 'Taxing and penal statutes are generally construed:', ['Strictly, with doubt resolved in favour of the subject', 'Liberally in favour of the State', 'By the mischief rule only', 'Against the taxpayer'], 0,
          'Because they impose burdens or punishment, taxing and penal laws are read strictly; reasonable doubt benefits the taxpayer or accused. Welfare laws are read liberally. In practice: check exemptions carefully.', 'c3', T3),
        Q('m7', 'A definition clause using the word "means" is generally:', ['Exhaustive', 'Inclusive', 'Illustrative only', 'Of no effect'], 0,
          '"Means" confines the term to the stated meaning; "includes" extends the ordinary meaning to cover more. In practice: read definitions closely.', 'c4', T4),
        Q('m8', 'A proviso to a section normally:', ['Carves out an exception from the main provision', 'Enlarges the main provision', 'Repeals the section', 'Has no legal effect'], 0,
          'A proviso qualifies or excepts something from the enacting part that would otherwise fall within it; it does not usually expand the main provision. In practice: read it with the main section.', 'c4', T4),
        Q('m9', 'Which is an external aid to interpretation?', ['Statement of objects and reasons', 'Long title', 'Illustrations', 'Explanation to a section'], 0,
          'The statement of objects and reasons and parliamentary debates come from outside the statute and are external aids; titles, illustrations and explanations are internal aids. In practice: use external aids with caution.', 'c5', T5),
        Q('m10', 'The golden rule allows modifying the literal meaning to:', ['Avoid absurdity or inconsistency', 'Increase tax collection', 'Give effect to the judge\'s view', 'Ignore the words entirely'], 0,
          'Under the golden rule, the ordinary meaning is departed from only to the extent necessary to avoid absurdity, repugnancy or inconsistency with the rest of the statute. In practice: keep departures minimal.', 'c2', T2),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Ejusdem generis', 2, 'application', 'ejusdem'),
           S('s2', 'Mischief or golden rule', 1.5, 'application', 'mischief|golden'),
           S('s3', 'Harmonious construction', 1.5, 'application', 'harmonious')],
          ['Name the rule and apply it.'], ['Using ejusdem generis without a class.'], ['Table.'], pad='table'),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Internal aids identified', 2, 'concept', 'internal'),
           S('s2', 'External aid and limits', 2, 'concept', 'external')],
          ['Classify each aid.'], ['Treating headings as overriding clear words.'], ['Table.'], pad='table'),
    ]

    viva = [
        V('v1', 'State the mischief rule.', 'The court considers the earlier law, the mischief it failed to cover, the remedy Parliament provided and its reason, and interprets the Act to suppress the mischief and advance the remedy.',
          [P('p1', 'Earlier law and mischief', 5, 'mischief'), P('p2', 'Advance the remedy', 5, 'remedy')], 'c2'),
        V('v2', 'When does ejusdem generis apply?', 'When general words follow specific words that form a distinct class; the general words are then confined to things of that class.',
          [P('p1', 'Specific words form a class', 6, 'class|genus'), P('p2', 'General words limited', 4, 'general')], 'c3'),
        V('v3', 'Give three internal aids to interpretation.', 'Long title, preamble, headings, marginal notes, definitions, illustrations, provisos, explanations, schedules and punctuation.',
          [P('p1', 'Title or preamble', 5, 'title|preamble'), P('p2', 'Other aids', 5, 'definition|illustration|proviso|explanation|heading')], 'c4'),
        V('v4', 'What is the effect of "includes" in a definition?', 'It extends the ordinary meaning of the word to cover the things listed as well.',
          [P('p1', 'Extends', 6, 'extend|enlarg|wider'), P('p2', 'Ordinary meaning', 4, 'ordinary')], 'c4'),
        V('v5', 'Name two external aids.', 'Parliamentary history such as statements of objects and reasons, historical background, dictionaries, foreign decisions, textbooks and statutes in pari materia.',
          [P('p1', 'Parliamentary history', 5, 'parliament|objects'), P('p2', 'Others', 5, 'dictionar|historical|foreign|textbook')], 'c5'),
    ]

    cases = [{'id': 'k1', 'title': 'The "places of entertainment" tax', 'difficulty': 'moderate',
              'case': 'A State law levies tax on "cinemas, theatres, circuses and other places of entertainment". A municipal authority seeks to tax a public library that holds occasional book readings. The law is a taxing statute.',
              'mcqs': [
                  M('k1a', 'The most relevant rule to read "other places of entertainment" is:', ['Ejusdem generis', 'Literal rule alone', 'Reddendo singula singulis', 'Harmonious construction'], 0,
                    'The general words follow a class of commercial entertainment venues, so ejusdem generis confines them to similar places. In practice: identify the common genus.', 'core', topic=T3),
                  M('k1b', 'Is the library likely to be taxable?', ['No, it is not of the same class as cinemas and circuses', 'Yes, any public place is covered', 'Yes, because readings entertain', 'Only on reading days'], 0,
                    'A library is not a commercial entertainment venue like the listed items; applying ejusdem generis and strict construction of taxing laws, it falls outside. In practice: doubt favours the taxpayer.', 'moderate', topic=T3),
                  M('k1c', 'As a taxing statute, any reasonable doubt is resolved:', ['In favour of the subject', 'In favour of the State', 'By the Governor', 'By literal rule against the subject'], 0,
                    'Taxing statutes are construed strictly; if two views are reasonably possible, the one favouring the taxpayer is adopted. In practice: cite this principle in replies to notices.', 'core', topic=T3),
              ]}]

    return unit(UID, 'p2', 'int-p2-ii-ch02', 1, 'Interpretation of Statutes',
                ['Explain why statutes need interpretation.',
                 'Apply primary rules of interpretation.',
                 'Apply secondary rules and strict or beneficial construction.',
                 'Use internal and external aids and interpret deeds and documents.'],
                {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 20}, 'prereq': ['int-p2-ii-ch01-u01'],
                 'exam_tip': 'For problem questions, name the rule, state it in one line, apply it to the facts and conclude.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Interpretation finds legislative intention from words.', 'Literal, mischief, golden and harmonious construction rules.',
                             'Noscitur a sociis, ejusdem generis, reddendo singula singulis.', 'Taxing/penal laws strict; welfare laws liberal.',
                             'Internal aids: title, preamble, headings, definitions, illustrations, provisos, explanations, schedules.', 'External aids: parliamentary history, dictionaries, history, other statutes.'],
                 'remember': ['"Means" is exhaustive; "includes" is extensive.'],
                 'traps': ['Aids cannot override clear words.']},
                [('Primary rules', 'Literal · Mischief · Golden · Harmonious'), ('Secondary rules', 'Noscitur · Ejusdem · Reddendo'), ('Taxing laws', 'Strict construction')],
                viva, cases)
