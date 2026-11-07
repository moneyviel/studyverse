"""CA Foundation · Paper 3 Quantitative Aptitude · Part B Logical Reasoning · Chapter 12 Blood Relations.
Original puzzles. Every family is built as a small tree in code; each clue and each answer is checked by the relation finder below."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch12-u01'


class Fam:
    def __init__(self): self.sex, self.par, self.sp = {}, {}, {}
    def add(self, *people):
        for spec in people:
            n, s = spec.split(':'); self.sex[n] = s; self.par.setdefault(n, set())
        return self
    def child(self, kid, *parents):
        self.par[kid] |= set(parents); return self
    def marry(self, a, b):
        self.sp[a] = b; self.sp[b] = a; return self
    def parents(self, x): return self.par.get(x, set())
    def kids(self, x): return {k for k, ps in self.par.items() if x in ps}
    def sibs(self, x): return {y for y in self.sex if y != x and self.parents(x) & self.parents(y)}

    def rel(self, a, b):
        """The word that completes 'a is b's ____'."""
        m = self.sex[a] == 'M'
        g = lambda male, female: male if m else female
        if self.sp.get(b) == a: return g('husband', 'wife')
        if a in self.parents(b): return g('father', 'mother')
        if b in self.parents(a): return g('son', 'daughter')
        if a in self.sibs(b): return g('brother', 'sister')
        gp = {q for p_ in self.parents(b) for q in self.parents(p_)}
        if a in gp:
            side = 'paternal ' if any(a in self.parents(p_) and self.sex[p_] == 'M' for p_ in self.parents(b)) else 'maternal '
            return side + g('grandfather', 'grandmother')
        if b in {q for p_ in self.parents(a) for q in self.parents(p_)}: return g('grandson', 'granddaughter')
        if a in {r for q in gp for r in self.parents(q)}: return g('great-grandfather', 'great-grandmother')
        if b in {r for p_ in self.parents(a) for q in self.parents(p_) for r in self.parents(q)}: return g('great-grandson', 'great-granddaughter')
        for p_ in self.parents(b):
            if a in self.sibs(p_) or a in {self.sp.get(s) for s in self.sibs(p_)}:
                side = 'paternal ' if self.sex[p_] == 'M' else 'maternal '
                return side + g('uncle', 'aunt')
        if b in {k for s in self.sibs(a) for k in self.kids(s)} or (self.sp.get(a) and b in {k for s in self.sibs(self.sp[a]) for k in self.kids(s)}):
            return g('uncle', 'aunt')
        if any(a in self.kids(s) for p_ in self.parents(b) for s in self.sibs(p_)): return 'cousin'
        if any(a in self.kids(s) for s in self.sibs(b)) or (self.sp.get(b) and any(a in self.kids(s) for s in self.sibs(self.sp[b]))): return g('nephew', 'niece')
        if self.sp.get(b) and a in self.parents(self.sp[b]): return g('father-in-law', 'mother-in-law')
        if self.sp.get(a) and self.sp[a] in self.kids(b): return g('son-in-law', 'daughter-in-law')
        if (self.sp.get(b) and a in self.sibs(self.sp[b])) or (self.sp.get(a) and self.sp[a] in self.sibs(b)): return g('brother-in-law', 'sister-in-law')
        return None


def chk(f, clues):
    """Every clue (a, word, b) must hold in the family tree f."""
    for a, w, b in clues:
        got = f.rel(a, b)
        assert got is not None and (got == w or got.endswith(' ' + w)), (a, w, b, got)


def M(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check is not None: d['check'] = check
    return d


def build():
    # ---------------- illustrations ----------------
    f1 = Fam().add('Ravi:M', 'Meena:F', 'Kiran:M', 'Tara:F', 'GP:M').child('Meena', 'GP').child('Kiran', 'GP').child('Ravi', 'Meena').child('Tara', 'Kiran')
    chk(f1, [('Ravi', 'son', 'Meena'), ('Meena', 'sister', 'Kiran'), ('Tara', 'daughter', 'Kiran')]); assert f1.rel('Tara', 'Ravi') == 'cousin'
    f2 = Fam().add('P:M', 'Q:F', 'R:F', 'S:M', 'T:M').child('P', 'R', 'S').child('Q', 'R', 'S').child('S', 'T').marry('R', 'S')
    chk(f2, [('P', 'brother', 'Q'), ('Q', 'daughter', 'R'), ('R', 'wife', 'S'), ('T', 'father', 'S')]); assert f2.rel('P', 'T') == 'grandson'
    # i3: Neha points to a man: "His mother is the only daughter of my mother" -> Neha is his mother
    f3 = Fam().add('Neha:F', 'NM:F', 'Man:M').child('Neha', 'NM').child('Man', 'Neha'); assert f3.rel('Man', 'Neha') == 'son'
    # i4: Leela: "He is the son of the only brother of my mother" -> cousin
    f4 = Fam().add('Leela:F', 'LM:F', 'Uncle:M', 'Boy:M', 'G:M').child('LM', 'G').child('Uncle', 'G').child('Leela', 'LM').child('Boy', 'Uncle')
    assert f4.rel('Uncle', 'Leela') == 'maternal uncle' and f4.rel('Boy', 'Leela') == 'cousin'
    # i5: A husband of B; C is B's brother -> C is A's brother-in-law
    f5 = Fam().add('A:M', 'B:F', 'C:M', 'BP:M').child('B', 'BP').child('C', 'BP').marry('A', 'B'); assert f5.rel('C', 'A') == 'brother-in-law'
    # i6: coded  A × B + C − D  (× father, + sister, − brother)
    f6 = Fam().add('A:M', 'B:F', 'C:M', 'D:M').child('B', 'A').child('C', 'A').child('D', 'A')
    chk(f6, [('A', 'father', 'B'), ('B', 'sister', 'C'), ('C', 'brother', 'D')]); assert f6.rel('A', 'D') == 'father' and f6.rel('B', 'A') == 'daughter'

    # ---------------- MCQ families ----------------
    fm9 = Fam().add('Amit:M', 'Bela:F', 'Charu:F', 'Dinesh:M').child('Amit', 'Bela').child('Bela', 'Charu', 'Dinesh').marry('Charu', 'Dinesh')
    chk(fm9, [('Amit', 'son', 'Bela'), ('Bela', 'daughter', 'Charu'), ('Charu', 'wife', 'Dinesh')]); assert fm9.rel('Dinesh', 'Amit') == 'maternal grandfather'
    fm10 = Fam().add('Lata:F', 'Mohan:M', 'Nisha:F', 'G:M').child('Lata', 'G').child('Mohan', 'G').child('Nisha', 'Mohan')
    assert fm10.rel('Lata', 'Nisha') == 'paternal aunt'
    fm11 = Fam().add('Sunil:M', 'X:M', 'Tanu:F', 'Raj:M').child('X', 'Sunil').child('Raj', 'X', 'Tanu').marry('X', 'Tanu')
    assert fm11.rel('Tanu', 'Sunil') == 'daughter-in-law'
    fm12 = Fam().add('P:M', 'Q:M', 'R:F', 'S:M', 'G:M').child('P', 'G').child('Q', 'G').child('R', 'P').child('S', 'Q'); assert fm12.rel('S', 'R') == 'cousin'
    fm13 = Fam().add('X:F', 'Y:M', 'Z:F', 'W:M').child('X', 'Z', 'W').marry('X', 'Y').marry('Z', 'W')
    chk(fm13, [('X', 'wife', 'Y'), ('Z', 'mother', 'X'), ('W', 'husband', 'Z')]); assert fm13.rel('W', 'Y') == 'father-in-law'
    fm14 = Fam().add('K:M', 'L:F', 'Mo:F', 'N:M').child('K', 'Mo').child('L', 'Mo').child('Mo', 'N')
    chk(fm14, [('K', 'brother', 'L'), ('Mo', 'mother', 'L'), ('N', 'father', 'Mo')]); assert fm14.rel('K', 'N') == 'grandson'
    fm15 = Fam().add('Rohit:M', 'RM:F', 'Lady:F').child('Rohit', 'RM').marry('Rohit', 'Lady'); assert fm15.rel('Lady', 'Rohit') == 'wife'
    fm16 = Fam().add('Seema:F', 'H:M', 'HB:M', 'Boy:M', 'G:M').child('H', 'G').child('HB', 'G').child('Boy', 'HB').marry('Seema', 'H'); assert fm16.rel('Boy', 'Seema') == 'nephew'
    fm17 = Fam().add('Priya:F', 'PF:M', 'Man:M').child('Priya', 'PF').marry('Priya', 'Man'); assert fm17.rel('Man', 'Priya') == 'husband'
    fm18 = Fam().add('M:F', 'N:M', 'O:F').child('N', 'M').child('O', 'M'); chk(fm18, [('M', 'mother', 'N'), ('N', 'brother', 'O')]); assert fm18.rel('M', 'O') == 'mother'
    fm19 = Fam().add('P:M', 'Q:F', 'R:M').child('Q', 'P').child('R', 'P'); chk(fm19, [('P', 'father', 'Q'), ('Q', 'sister', 'R')]); assert fm19.rel('Q', 'P') == 'daughter'
    fm20 = Fam().add('A:F', 'B:M', 'C:M', 'G:M').child('A', 'G').child('B', 'G').child('C', 'B'); chk(fm20, [('A', 'sister', 'B'), ('B', 'father', 'C')]); assert fm20.rel('A', 'C') == 'paternal aunt'
    fm21 = Fam().add('D:M', 'E:F', 'F:F', 'G:M', 'O:M').child('D', 'O').child('E', 'O').child('F', 'E').child('G', 'E')
    chk(fm21, [('D', 'brother', 'E'), ('F', 'daughter', 'E'), ('G', 'brother', 'F')]); assert fm21.rel('D', 'G') == 'maternal uncle'
    fm22 = Fam().add('R:M', 'S:F', 'T:M', 'U:M').child('S', 'R').child('T', 'R').child('U', 'T')
    chk(fm22, [('R', 'father', 'S'), ('S', 'sister', 'T'), ('U', 'son', 'T')]); assert fm22.rel('R', 'U') == 'paternal grandfather'
    fm23 = Fam().add('You:M', 'Mum:F', 'Dad:M', 'GF:M').child('You', 'Mum', 'Dad').child('Dad', 'GF').marry('Mum', 'Dad')
    assert fm23.rel('GF', 'Mum') == 'father-in-law' and fm23.rel('Dad', 'You') == 'father'
    fm25 = Fam().add('Woman:F', 'WF:M', 'Bro:M', 'Man:M').child('Woman', 'WF').child('Bro', 'WF').child('Man', 'Bro'); assert fm25.rel('Man', 'Woman') == 'nephew'
    fm26 = Fam().add('Raman:M', 'Sis:F', 'SisH:M', 'Sohan:M', 'G:M').child('Raman', 'G').child('Sis', 'G').child('Sohan', 'Sis', 'SisH').marry('Sis', 'SisH'); assert fm26.rel('Sohan', 'Raman') == 'nephew'

    # ---------------- case family ----------------
    fk = (Fam().add('Hari:M', 'Leela:F', 'Ajay:M', 'Bina:F', 'Kavita:F', 'Rohan:M', 'Sia:F', 'Dev:M', 'Kabir:M')
          .marry('Hari', 'Leela').child('Ajay', 'Hari', 'Leela').child('Bina', 'Hari', 'Leela').marry('Ajay', 'Kavita')
          .child('Rohan', 'Ajay', 'Kavita').child('Sia', 'Ajay', 'Kavita').marry('Bina', 'Dev').child('Kabir', 'Bina', 'Dev'))
    assert fk.rel('Kabir', 'Sia') == 'cousin' and fk.rel('Dev', 'Ajay') == 'brother-in-law' and fk.rel('Leela', 'Rohan') == 'paternal grandmother' and fk.rel('Kavita', 'Bina') == 'sister-in-law'
    females = sum(1 for s in fk.sex.values() if s == 'F'); assert females == 4
    assert fk.rel('Hari', 'Kabir') == 'maternal grandfather'

    # ---------------- questions ----------------
    fq1 = Fam().add('Arvind:M', 'Bhavna:F', 'Chirag:M', 'Deepti:F', 'Esha:F').child('Arvind', 'Bhavna').child('Bhavna', 'Esha').child('Chirag', 'Esha').child('Deepti', 'Chirag')
    chk(fq1, [('Arvind', 'son', 'Bhavna'), ('Chirag', 'brother', 'Bhavna'), ('Deepti', 'daughter', 'Chirag'), ('Esha', 'mother', 'Bhavna')])
    assert [fq1.rel('Deepti', 'Arvind'), fq1.rel('Esha', 'Deepti'), fq1.rel('Chirag', 'Arvind'), fq1.rel('Arvind', 'Esha')] == ['cousin', 'paternal grandmother', 'maternal uncle', 'grandson']
    # q2 (a) Mohit about a girl: "Her father is the only son of my mother" -> Mohit is her father
    fq2a = Fam().add('Mohit:M', 'MM:F', 'Girl:F').child('Mohit', 'MM').child('Girl', 'Mohit'); assert fq2a.rel('Girl', 'Mohit') == 'daughter'
    # q2 (b) Anita about a man: "He is the father-in-law of my only brother's wife's... " -> simpler: "His sister is my mother's mother" -> man is Anita's mother's maternal uncle? use: "His only daughter is my mother" -> maternal grandfather
    fq2b = Fam().add('Anita:F', 'AM:F', 'Man:M').child('Anita', 'AM').child('AM', 'Man'); assert fq2b.rel('Man', 'Anita') == 'maternal grandfather'
    # q3 coded: P ÷ Q (P mother of Q), P × Q (P father of Q), P + Q (P sister of Q), P − Q (P brother of Q)
    fq3 = Fam().add('J:F', 'K:M', 'L:F', 'N:M').child('K', 'J').child('L', 'J').child('N', 'L')
    chk(fq3, [('J', 'mother', 'K'), ('K', 'brother', 'L'), ('L', 'mother', 'N')])
    assert fq3.rel('K', 'N') == 'maternal uncle' and fq3.rel('J', 'N') == 'maternal grandmother' and fq3.rel('N', 'J') == 'grandson'

    tree = lambda rows, title: table(['Generation', 'Members (M = male, F = female)', 'Links'], rows, title=title)

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch12', 'n': 1, 'title': 'Blood Relations',
        'outcomes': ['Name relations on the paternal and maternal sides and the in-law relations created by marriage.',
                     'Turn a chain of relation clues into a family tree with generations, sexes and marriages marked, and read any relation from it.',
                     'Solve "pointing / photograph / introducing" statements by working from the speaker outwards.',
                     'Decode symbol-based relation statements (coded relations).'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 30, 'practice': 45}, 'prereq': [],
                 'exam_tip': 'Never assume a person\'s sex from a name alone — use only words such as son, sister, husband or mother. If the sex cannot be fixed, the right option is often the neutral one (child, sibling, cousin).'},
        'concepts': [
            {'id': 'c1', 'title': 'What is a blood relation?', 'body': [
                'A blood relation is a person related to another by birth (descent), as opposed to by marriage. Reasoning tests use both: relations by birth (father, sister, cousin) and relations by marriage (husband, mother-in-law, brother-in-law).',
                'Questions give relations in a jumbled chain; you must link them and name the relation between two persons in the chain.'],
             'analogy': 'A family tree is a company\'s group structure chart: parent, subsidiaries, fellow subsidiaries — and a marriage is like a joint venture linking two groups.',
             'work': 'Identifying relatives is a legal task for a CA: "relative" under the Companies Act, 2013 (for related-party transactions) and under the Income-tax Act, 1961 (for gifts and clubbing) has specific lists. Being quick and precise with relations avoids missing a related party.'},
            {'id': 'c2', 'title': 'Paternal and maternal side', 'body': [
                'Paternal side (the father\'s family): his parents are your grandparents; his brothers are your uncles and his sisters your aunts; an uncle\'s wife is also called aunt and an aunt\'s husband uncle; the children of all of them are your cousins.',
                'Maternal side (the mother\'s family): her parents are your maternal grandparents; her brother is your maternal uncle (his wife, your maternal aunt); her sister is your aunt; and their children are again your cousins.'],
             'blocks': [table(['Relation of…', 'Paternal side', 'Maternal side'], [
                 ['Parent\'s father', 'Grandfather', 'Maternal grandfather'], ['Parent\'s mother', 'Grandmother', 'Maternal grandmother'],
                 ['Parent\'s brother', 'Uncle', 'Maternal uncle'], ['Parent\'s sister', 'Aunt', 'Aunt'], ['Children of the above', 'Cousins', 'Cousins']], title='Two sides of the family')],
             'analogy': 'Two branches of the same tree — the father\'s branch and the mother\'s branch — meet at you.',
             'work': 'Succession and HUF questions (in tax and law papers) depend on which side a relative belongs to, so the vocabulary matters beyond reasoning.'},
            {'id': 'c3', 'title': 'Key relation words', 'body': [
                'Grandfather\'s (or grandmother\'s) son = father or uncle; grandfather\'s ONLY son = father. Mother\'s or father\'s son = brother (or yourself); mother\'s or father\'s daughter = sister (or yourself).',
                'Brother\'s / sister\'s son = nephew; daughter = niece. Uncle\'s or aunt\'s child = cousin.',
                'Son\'s wife = daughter-in-law; daughter\'s husband = son-in-law; husband\'s or wife\'s father = father-in-law; mother = mother-in-law.',
                'Sister\'s husband or spouse\'s brother = brother-in-law; brother\'s wife or spouse\'s sister = sister-in-law.',
                'Son\'s or daughter\'s son = grandson; daughter = granddaughter; grandchild\'s daughter = great-granddaughter.'],
             'analogy': 'Learn these like the multiplication table — once automatic, every puzzle is just two or three look-ups.',
             'work': 'When preparing a related-party schedule, a CA lists a director\'s spouse, parents, children, siblings and their spouses — the very words of this card.'},
            {'id': 'c4', 'title': 'Drawing the family tree', 'body': [
                'Use a symbol for sex (for example a square or "+" for male, a circle or "−" for female, "?" if unknown).',
                'Keep each generation on its own level: grandparents on top, then parents, then children. Join a married couple with a double horizontal line (=), siblings with a single horizontal line, and parent to child with a vertical line.',
                'Fix a person\'s sex only from relation words (son, brother, husband → male; daughter, sister, wife, mother → female). A name proves nothing.',
                'Then read the required relation along the shortest path in the tree.'],
             'blocks': [tree([['1', 'Esha (F)', 'Mother of Bhavna and Chirag'], ['2', 'Bhavna (F), Chirag (M)', 'Siblings'], ['3', 'Arvind (M), Deepti (F)', 'Arvind is Bhavna\'s son; Deepti is Chirag\'s daughter']], 'Tree for Question 1 (generation levels)')],
             'analogy': 'Just as a consolidation worksheet keeps the holding company, subsidiaries and sub-subsidiaries on separate levels, a family tree keeps generations apart.',
             'work': 'Ownership-structure charts used in group audits and transfer-pricing documentation are drawn with the same discipline: levels, links and clear labels.'},
            {'id': 'c5', 'title': 'Pointing, photograph and introduction statements', 'body': [
                'Form: "Pointing to X, A says, \'…\'". Start from the speaker ("my") and work outwards one link at a time, replacing each phrase with a person.',
                'Common short cuts: "my mother\'s only daughter" = the speaker herself (if female); "my father\'s only son" = the speaker himself (if male); "my grandfather\'s only son" = my father (paternal side).',
                'Write the result as "X is A\'s …" — check the direction of the relation asked (X to A or A to X).'],
             'analogy': 'It is like peeling an onion from the inside: "my" is the core, each "\'s" is one more layer.',
             'work': 'Declarations by directors ("my HUF", "my spouse\'s firm") have to be decoded link by link in the same way when compiling interests in other entities.'},
            {'id': 'c6', 'title': 'Coded relations', 'body': [
                'Symbols stand for relations, for example P × Q for "P is Q\'s father", P ÷ Q for "P is Q\'s mother", P + Q for "P is Q\'s sister" and P − Q for "P is Q\'s brother".',
                'Translate each symbol in turn, noting the sex it reveals (× and − give a male, ÷ and + give a female), draw the tree, then answer.',
                'The last person in a chain often has unknown sex; the answer may then be "child" or "nephew or niece".'],
             'analogy': 'Coded relations are shorthand notes — expand them before you reason, just as you expand "Dr." and "Cr." in a journal.',
             'work': 'Translating compact codes (GL codes, HSN codes, relation codes in a client master) into words is routine work for a CA.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Cousins through a brother and sister', 'difficulty': 'core', 'minutes': 2,
             'q': 'Ravi is Meena\'s son. Meena is Kiran\'s sister. Tara is Kiran\'s daughter. How is Tara related to Ravi?',
             'solution': [tree([['1', 'Meena (F), Kiran (M)', 'Siblings'], ['2', 'Ravi (M), Tara (F)', 'Ravi is Meena\'s son; Tara is Kiran\'s daughter']], 'Family tree'),
                          p('Kiran is Ravi\'s maternal uncle; the child of an uncle is a cousin. Tara is Ravi\'s cousin.')]},
            {'id': 'i2', 'title': 'Three generations', 'difficulty': 'core', 'minutes': 2,
             'q': 'P is Q\'s brother. Q is R\'s daughter. R is S\'s wife. T is S\'s father. How is P related to T?',
             'solution': [tree([['1', 'T (M)', 'Father of S'], ['2', 'S (M) = R (F)', 'Married couple'], ['3', 'P (M), Q (F)', 'Children of R and S']], 'Family tree'),
                          p('P is the son of S, and S is the son of T. So P is T\'s grandson.')]},
            {'id': 'i3', 'title': 'Pointing statement — "only daughter of my mother"', 'difficulty': 'moderate', 'minutes': 2,
             'q': 'Showing a man to a friend, Neha remarks, "My mother has just one daughter, and she is this man\'s mother." How is the man related to Neha?',
             'solution': [p('Start from "my mother": a mother with just one daughter, when the speaker Neha is female, means that daughter is Neha herself.'),
                          p('So the man\'s mother is Neha. The man is Neha\'s son.')]},
            {'id': 'i4', 'title': 'Introduction — maternal uncle\'s son', 'difficulty': 'core', 'minutes': 2,
             'q': 'Introducing a boy, Leela says, "He is the son of the only brother of my mother." How is the boy related to Leela?',
             'solution': [p('The only brother of Leela\'s mother is Leela\'s maternal uncle.'), p('The son of a maternal uncle is a cousin. The boy is Leela\'s cousin.')]},
            {'id': 'i5', 'title': 'Relation by marriage', 'difficulty': 'core', 'minutes': 1,
             'q': 'A is the husband of B. C is B\'s brother. How is C related to A?',
             'solution': [p('C is the brother of A\'s wife. A wife\'s brother is a brother-in-law. C is A\'s brother-in-law.')]},
            {'id': 'i6', 'title': 'Coded relations', 'difficulty': 'moderate', 'minutes': 2,
             'q': 'P × Q stands for "P is Q\'s father"; P + Q stands for "P is Q\'s sister"; P − Q stands for "P is Q\'s brother". If A × B + C − D, how is A related to D, and how is B related to A?',
             'solution': [p('A × B: A is the father of B. B + C: B is the sister of C (B is female). C − D: C is the brother of D.'),
                          p('B, C and D are siblings, all children of A. So A is D\'s father, and B (female) is A\'s daughter.')]},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Related-party schedule from a director\'s declaration', 'role': 'Audit senior reviewing related-party disclosures', 'situation': 'A director declares: "My wife\'s brother is a partner in Shree Traders, and my son\'s father-in-law owns Ganga Fabrics." Both firms supply the company.',
             'steps': ['Decode each phrase: wife\'s brother = brother-in-law; son\'s father-in-law = the father of the son\'s wife.', 'Compare each person with the definition of "relative" in the law that applies (for example the list notified under the Companies Act, 2013) — the definition, not common usage, decides.', 'Where the person is a relative, check whether the firm is a related party and whether approvals and disclosures were made.', 'Record the analysis in the working papers.'],
             'takeaway': 'Relation puzzles become legal questions in practice: first decode the relation exactly, then apply the statutory definition.',
             'think': 'Is the son\'s father-in-law a "relative" in everyday language? Why must the auditor still check the statute?', 'answer': 'In everyday speech he is a relative by marriage, but statutory lists are specific and may not include him; only the definition in the relevant law decides the treatment.'},
            {'id': 'j2', 'title': 'Clubbing of income — who is who?', 'role': 'Tax associate preparing an individual\'s return', 'situation': 'A client has gifted money to "my daughter-in-law" and to "my brother\'s wife".',
             'steps': ['Identify the relations: daughter-in-law = son\'s wife; brother\'s wife = sister-in-law.', 'Note that income-tax provisions treat different relatives differently for gifts and clubbing.', 'Look up the treatment for each relation under the relevant sections before computing the client\'s income.'],
             'takeaway': 'A precise relation word is the first step of a correct tax computation.'},
        ],
        'mcqs': [
            M('m1', 'Your father\'s brother\'s wife is your:', ['Aunt', 'Sister-in-law', 'Mother-in-law', 'Cousin'], 0, 'Father\'s brother = uncle; uncle\'s wife = aunt.', 'c2'),
            M('m2', 'Your mother\'s brother is your:', ['Maternal uncle', 'Paternal uncle', 'Brother-in-law', 'Cousin'], 0, 'A brother on the mother\'s side is a maternal uncle.', 'c2'),
            M('m3', 'Your grandfather\'s only son (paternal side) is your:', ['Father', 'Uncle', 'Brother', 'Cousin'], 0, 'With only one son, that son must be your father. (If there were more sons, one could be an uncle.)', 'c3'),
            M('m4', 'Your brother\'s daughter is your:', ['Niece', 'Nephew', 'Cousin', 'Granddaughter'], 0, 'A sibling\'s daughter is a niece; a sibling\'s son is a nephew.', 'c3'),
            M('m5', 'Your sister\'s husband is your:', ['Brother-in-law', 'Son-in-law', 'Uncle', 'Cousin'], 0, 'Sister\'s husband = brother-in-law.', 'c3'),
            M('m6', 'Your son\'s wife is your:', ['Daughter-in-law', 'Sister-in-law', 'Niece', 'Daughter'], 0, 'Son\'s wife = daughter-in-law.', 'c3'),
            M('m7', 'A woman\'s husband\'s mother is her:', ['Mother-in-law', 'Aunt', 'Grandmother', 'Sister-in-law'], 0, 'Spouse\'s mother = mother-in-law.', 'c3'),
            M('m8', 'Your granddaughter\'s daughter is your:', ['Great-granddaughter', 'Granddaughter', 'Niece', 'Grandniece'], 0, 'One generation below a granddaughter is a great-granddaughter.', 'c3'),
            M('m9', 'Amit is Bela\'s son. Bela is Charu\'s daughter. Charu is Dinesh\'s wife. How is Dinesh related to Amit?', ['Maternal grandfather', 'Paternal grandfather', 'Uncle', 'Father'], 0, 'Dinesh is Bela\'s father and Bela is Amit\'s mother: Dinesh is Amit\'s maternal grandfather.', 'c2'),
            M('m10', 'Lata is Mohan\'s sister. Mohan is Nisha\'s father. How is Lata related to Nisha?', ['Aunt', 'Mother', 'Sister', 'Cousin'], 0, 'The father\'s sister is an aunt (paternal side).', 'c2'),
            M('m11', 'Raj\'s father is Sunil\'s only son. Tanu is Raj\'s mother. How is Tanu related to Sunil?', ['Daughter-in-law', 'Daughter', 'Wife', 'Sister'], 0, 'Tanu is the wife of Sunil\'s son: daughter-in-law.', 'c3', 'moderate'),
            M('m12', 'P and Q are brothers. R is P\'s daughter and S is Q\'s son. How is S related to R?', ['Cousin', 'Brother', 'Nephew', 'Uncle'], 0, 'Children of brothers are cousins.', 'c3'),
            M('m13', 'X is Y\'s wife. Z is X\'s mother. W is Z\'s husband. How is W related to Y?', ['Father-in-law', 'Father', 'Brother-in-law', 'Grandfather'], 0, 'W is X\'s father; X is Y\'s wife, so W is Y\'s father-in-law.', 'c3', 'moderate'),
            M('m14', 'K is L\'s brother. M is L\'s mother. N is M\'s father. How is K related to N?', ['Grandson', 'Son', 'Great-grandson', 'Nephew'], 0, 'K is M\'s son and M is N\'s daughter, so K is N\'s grandson.', 'c3'),
            M('m15', 'Pointing to a lady, Rohit says, "She is the wife of my mother\'s only son." How is the lady related to Rohit?', ['Wife', 'Sister', 'Sister-in-law', 'Mother'], 0, 'Rohit\'s mother\'s only son is Rohit himself, so the lady is his wife.', 'c5', 'moderate'),
            M('m16', 'Pointing to a boy, Seema says, "He is the son of my husband\'s only brother." How is the boy related to Seema?', ['Nephew', 'Son', 'Cousin', 'Brother-in-law'], 0, 'Husband\'s brother\'s son is Seema\'s nephew (by marriage).', 'c5', 'moderate'),
            M('m17', 'At a party Priya introduces a man: "My father has one daughter only, and this man is married to her." How is the man related to Priya?', ['Husband', 'Brother', 'Brother-in-law', 'Father'], 0, 'Priya\'s father\'s one daughter is Priya herself, so the man is her husband.', 'c5', 'moderate'),
            M('m18', 'P ÷ Q stands for "P is Q\'s mother"; P − Q stands for "P is Q\'s brother". If M ÷ N − O, how is M related to O?', ['Mother', 'Aunt', 'Sister', 'Grandmother'], 0, 'M is the mother of N, and N is the brother of O, so M is O\'s mother too.', 'c6', 'moderate'),
            M('m19', 'P × Q stands for "P is Q\'s father"; P + Q stands for "P is Q\'s sister". If P × Q + R, how is Q related to P?', ['Daughter', 'Son', 'Sister', 'Wife'], 0, 'Q is P\'s child, and "+" shows Q is female: daughter.', 'c6', 'moderate'),
            M('m20', 'P × Q stands for "P is Q\'s father"; P + Q stands for "P is Q\'s sister". If A + B × C, how is A related to C?', ['Aunt', 'Mother', 'Sister', 'Grandmother'], 0, 'A is the sister of B, and B is C\'s father: A is C\'s (paternal) aunt.', 'c6', 'hard'),
            M('m21', 'D is E\'s brother. F is E\'s daughter. G is F\'s brother. How is D related to G?', ['Uncle', 'Father', 'Brother', 'Grandfather'], 0, 'G is E\'s child and D is E\'s brother, so D is G\'s uncle (whether E is G\'s father or mother).', 'c3', 'moderate'),
            M('m22', 'R is S\'s father. S is T\'s sister. U is T\'s son. How is R related to U?', ['Grandfather', 'Father', 'Uncle', 'Great-grandfather'], 0, 'R is the father of S and T; U is T\'s son, so R is U\'s grandfather.', 'c3'),
            M('m23', 'Who is the only son of your mother\'s father-in-law?', ['Your father', 'Your uncle', 'Your grandfather', 'Your brother'], 0, 'Your mother\'s father-in-law is your paternal grandfather; his only son is your father.', 'c3', 'hard'),
            M('m24', 'Mira\'s brother\'s father\'s wife\'s daughter, other than Mira, is Mira\'s:', ['Sister', 'Cousin', 'Niece', 'Aunt'], 0, 'Brother\'s father = Mira\'s father; his wife = Mira\'s mother; her daughter other than Mira = Mira\'s sister.', 'c5', 'hard'),
            M('m25', 'A woman says about a man, "His father is the only son of my father." How is the man related to the woman?', ['Nephew', 'Son', 'Brother', 'Cousin'], 0, 'The only son of her father is her brother; the man\'s father is her brother, so the man is her nephew.', 'c5', 'hard'),
            M('m26', 'Sohan is the son of the husband of Raman\'s only sister. How is Sohan related to Raman?', ['Nephew', 'Son', 'Cousin', 'Brother-in-law'], 0, 'Raman\'s sister\'s son is Raman\'s nephew.', 'c3', 'moderate'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'Arvind is the son of Bhavna. Chirag is Bhavna\'s brother. Deepti is Chirag\'s daughter. Esha is Bhavna\'s mother. Draw the family tree and state: (a) Deepti\'s relation to Arvind, (b) Esha\'s relation to Deepti, (c) Chirag\'s relation to Arvind, (d) Arvind\'s relation to Esha.',
             'model': [tree([['1', 'Esha (F)', 'Mother of Bhavna and Chirag'], ['2', 'Bhavna (F), Chirag (M)', 'Siblings'], ['3', 'Arvind (M), Deepti (F)', 'Arvind — Bhavna\'s son; Deepti — Chirag\'s daughter']], 'Family tree'),
                       ul(['(a) Cousin — children of a brother and sister.', '(b) Grandmother — Esha is the mother of Deepti\'s father (paternal grandmother).', '(c) Maternal uncle — the brother of Arvind\'s mother.', '(d) Grandson — Arvind is the son of Esha\'s daughter.'])],
             'scheme': [{'id': 's1', 'pt': '(a) cousin', 'm': 1, 'skill': 'application'}, {'id': 's2', 'pt': '(b) grandmother', 'm': 1, 'skill': 'application'},
                        {'id': 's3', 'pt': '(c) maternal uncle', 'm': 1, 'skill': 'application'}, {'id': 's4', 'pt': '(d) grandson', 'm': 1, 'skill': 'application'}],
             'remarks': ['A neat three-level tree makes all four answers immediate.'], 'mistakes': ['Calling Chirag a "paternal" uncle of Arvind.', 'Reversing the direction in (d) and writing "grandmother".'],
             'tips': ['Underline the two names in each part and read the relation in the direction asked.']},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': '(a) Pointing to a girl, Mohit says, "Her father is the only son of my mother." How is the girl related to Mohit? (2 marks)  (b) Pointing to an old man, Anita says, "His only daughter is my mother." How is the man related to Anita? (2 marks)',
             'model': [p('(a) The only son of Mohit\'s mother is Mohit himself (Mohit is male, as the statement treats him as the son). So the girl\'s father is Mohit: the girl is Mohit\'s daughter.'),
                       p('(b) The man\'s only daughter is Anita\'s mother, so the man is the father of Anita\'s mother: Anita\'s maternal grandfather.')],
             'scheme': [{'id': 's1', 'pt': '(a) "only son of my mother" = Mohit', 'm': 1, 'skill': 'analysis'}, {'id': 's2', 'pt': '(a) daughter', 'm': 1, 'skill': 'conclusion'},
                        {'id': 's3', 'pt': '(b) man is father of Anita\'s mother', 'm': 1, 'skill': 'analysis'}, {'id': 's4', 'pt': '(b) maternal grandfather', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['Work from "my" outwards; most errors come from starting at the far end of the sentence.'], 'mistakes': ['Answering "sister" in (a) by treating "only son of my mother" as Mohit\'s brother.', 'Writing "grandfather" without "maternal" when options distinguish the side.'],
             'tips': ['Replace each phrase with a name as you go: "only son of my mother" → Mohit.']},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'P ÷ Q stands for "P is Q\'s mother"; P × Q stands for "P is Q\'s father"; P + Q stands for "P is Q\'s sister"; P − Q stands for "P is Q\'s brother". Given J ÷ K − L ÷ N: (a) translate the statement, (b) how is K related to N? (c) how is J related to N? (d) how is N related to J, if N is male?',
             'model': [p('(a) J is the mother of K; K is the brother of L; L is the mother of N.'),
                       p('(b) K is the brother of N\'s mother: K is N\'s maternal uncle.'),
                       p('(c) J is the mother of L, who is N\'s mother: J is N\'s maternal grandmother.'),
                       p('(d) N (male) is J\'s grandson.')],
             'scheme': [{'id': 's1', 'pt': '(a) correct translation of all three symbols', 'm': 1, 'skill': 'concept'}, {'id': 's2', 'pt': '(b) maternal uncle', 'm': 1, 'skill': 'application'},
                        {'id': 's3', 'pt': '(c) maternal grandmother', 'm': 1, 'skill': 'application'}, {'id': 's4', 'pt': '(d) grandson', 'm': 1, 'skill': 'application'}],
             'remarks': ['Translate first, then draw — reasoning directly from symbols causes slips.'], 'mistakes': ['Reading K − L as "L is the brother of K".', 'Taking L to be male; ÷ shows L is a mother.'],
             'tips': ['Write the sex revealed by each symbol next to the person: J (F), K (M), L (F).']},
        ],
        'revision': {
            'summary': ['Blood relation = related by birth; puzzles also use relations by marriage (in-laws).',
                        'Paternal side via the father, maternal side via the mother; parent\'s brother = uncle (maternal uncle on the mother\'s side), parent\'s sister = aunt, their children = cousins.',
                        'Sibling\'s son/daughter = nephew/niece; son\'s wife = daughter-in-law; daughter\'s husband = son-in-law; spouse\'s parents = in-laws; sister\'s husband / spouse\'s brother = brother-in-law; brother\'s wife / spouse\'s sister = sister-in-law.',
                        'Draw a tree: generations on levels, = for marriage, − for siblings, | for parent–child, sex marked only from relation words.',
                        'Pointing statements: start from "my" and replace each phrase with a person; "my mother\'s only daughter" = the speaker (female).',
                        'Coded relations: translate every symbol and note the sex it reveals before drawing.'],
            'remember': ['Grandfather\'s son = father or uncle; grandfather\'s only son = father.', 'Answer in the direction asked: "X is Y\'s …".'],
            'traps': ['Assuming sex from a name.', 'Reversing the direction of the relation.', 'Forgetting that "only son/daughter" can be the speaker himself/herself.', 'Ignoring paternal/maternal when the options distinguish them.']},
        'quickref': [{'k': 'Parent\'s brother / sister', 'v': 'Uncle / aunt (mother\'s brother = maternal uncle)'}, {'k': 'Sibling\'s son / daughter', 'v': 'Nephew / niece'},
                     {'k': 'Uncle\'s or aunt\'s child', 'v': 'Cousin'}, {'k': 'Son\'s wife / daughter\'s husband', 'v': 'Daughter-in-law / son-in-law'},
                     {'k': 'Sister\'s husband, spouse\'s brother', 'v': 'Brother-in-law'}, {'k': 'Brother\'s wife, spouse\'s sister', 'v': 'Sister-in-law'},
                     {'k': 'Grandfather\'s only son', 'v': 'Father'}, {'k': 'Tree symbols', 'v': '= marriage · − siblings · | parent–child · M/F from relation words only'}],
        'viva': [
            V('v1', 'What is meant by a blood relation, and what is the difference between the paternal and the maternal side?',
              'A blood relation is a person related by birth rather than by marriage. The paternal side is the father\'s side of the family and the maternal side is the mother\'s side. For example, the father\'s brother is an uncle, while the mother\'s brother is a maternal uncle.',
              [P('p1', 'Related by birth, not by marriage', 4, 'birth|born|descent', 'not marriage|not by marriage|rather than marriage|rather than by marriage|instead of marriage|not through marriage|than marriage|not married'),
               P('p2', 'Paternal = father\'s side', 3, 'paternal father|paternal side father|paternal mean father|paternal is father'),
               P('p3', 'Maternal = mother\'s side', 3, 'maternal mother|maternal side mother|maternal mean mother|maternal is mother')], 'c2'),
            V('v2', 'Who could your grandfather\'s son be, and how does the answer change if he is your grandfather\'s only son?',
              'My grandfather\'s son could be my father or my uncle. If he is my grandfather\'s only son, he must be my father.',
              [P('p1', 'Grandfather\'s son = father or uncle', 5, 'father', 'uncle'),
               P('p2', 'Only son = father', 5, 'only son father|only son must be father|only son is father|only son is my father|only son has to be father|only son would be father|only son definitely father|only son means father|only one son father')], 'c3'),
            V('v3', 'How do you draw a family tree to solve a blood relation puzzle?',
              'I mark each person\'s sex with a symbol, keep each generation on its own level, join married couples with a double line, siblings with a single horizontal line and parents to children with vertical lines. I fix a person\'s sex only from relation words like son or sister, never from the name, and then read the relation along the tree.',
              [P('p1', 'Mark sex with symbols', 2, 'sex|gender|male|female|square|circle|symbol'),
               P('p2', 'One level per generation', 3, 'generation|level|row|layer'),
               P('p3', 'Lines: double for marriage, single for siblings, vertical for parent–child', 2, 'line|link|connect|join'),
               P('p4', 'Sex only from relation words, never from names', 3, 'never from name|not from name|not from the name|names do not|name does not|not assume|never assume|don t assume|do not assume|not by name|not the name|name alone|only from relation|only from words|only relation word')], 'c4'),
            V('v4', 'Who are a nephew, a niece and a cousin?',
              'A nephew is the son of one\'s brother or sister, and a niece is the daughter of one\'s brother or sister. A cousin is the child of one\'s uncle or aunt.',
              [P('p1', 'Nephew = sibling\'s son', 3, 'nephew son|nephew is son|nephew is the son|nephew mean son|nephew brother son|nephew sister son|nephew sibling son|nephew boy'),
               P('p2', 'Niece = sibling\'s daughter', 3, 'niece daughter|niece is daughter|niece is the daughter|niece mean daughter|niece brother daughter|niece sister daughter|niece sibling daughter|niece girl'),
               P('p3', 'Cousin = child of uncle or aunt', 4, 'cousin child|cousin son|cousin daughter|cousin is child|cousin kid|cousin children', 'uncle|aunt', min=2)], 'c3'),
            V('v5', 'Neha says about a man, "My mother has just one daughter, and she is this man\'s mother." How do you solve this, and what is the answer?',
              'Start from the speaker and work outwards. My mother\'s one daughter means Neha herself, because Neha is female. So the man\'s mother is Neha, and the man is Neha\'s son.',
              [P('p1', 'Start from the speaker ("my") and work outwards', 3, 'speaker|start from|begin with|start with|my side|outward|step by step|one link|piece by piece|break'),
               P('p2', '"Only daughter of my mother" = Neha herself', 4, 'neha herself|herself|she herself|means neha|mean neha|neha is the only daughter|neha is that daughter|neha is that only daughter'),
               P('p3', 'So the man is Neha\'s son', 3, 'son|neha s son|her son|his mother is neha|mother is neha')], 'c5'),
            V('v6', 'Who is a brother-in-law and who is a sister-in-law?',
              'A brother-in-law is one\'s sister\'s husband or one\'s spouse\'s brother. A sister-in-law is one\'s brother\'s wife or one\'s spouse\'s sister.',
              [P('p1', 'Brother-in-law = sister\'s husband or spouse\'s brother', 5, ALT('brother in law {r}', r=['sister husband', 'sister s husband', 'is sister husband', 'is the sister husband', 'spouse brother', 'wife brother', 'husband brother', 'is spouse brother', 'mean sister husband', 'means sister husband', 'is my sister husband', 'is your sister husband'])),
               P('p2', 'Sister-in-law = brother\'s wife or spouse\'s sister', 5, ALT('sister in law {r}', r=['brother wife', 'brother s wife', 'is brother wife', 'is the brother wife', 'spouse sister', 'husband sister', 'wife sister', 'is spouse sister', 'mean brother wife', 'means brother wife', 'is my brother wife', 'is your brother wife']))], 'c3'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'The Hari family', 'difficulty': 'moderate',
            'case': 'Hari and Leela are married and have two children, Ajay and Bina. Kavita is Ajay\'s wife; Rohan and Sia are Kavita\'s children (Rohan a boy, Sia a girl). Bina is married to Dev, and their only child Kabir is a boy.',
            'mcqs': [
                M('k1a', 'How is Kabir related to Sia?', ['Cousin', 'Brother', 'Nephew', 'Uncle'], 0, 'Kabir is Bina\'s son and Sia is Ajay\'s daughter; Ajay and Bina are siblings, so their children are cousins.', 'c3', 'core'),
                M('k1b', 'How is Dev related to Ajay?', ['Brother-in-law', 'Brother', 'Son-in-law', 'Cousin'], 0, 'Dev is the husband of Ajay\'s sister.', 'c3', 'moderate'),
                M('k1c', 'How is Leela related to Rohan?', ['Grandmother', 'Mother', 'Aunt', 'Great-grandmother'], 0, 'Leela is the mother of Ajay, Rohan\'s father: his (paternal) grandmother.', 'c2', 'core'),
                M('k1d', 'How is Kavita related to Bina?', ['Sister-in-law', 'Sister', 'Daughter-in-law', 'Aunt'], 0, 'Kavita is the wife of Bina\'s brother.', 'c3', 'moderate'),
                M('k1e', 'How many female members does the family have?', ['4', '3', '5', '2'], 0, 'Leela, Bina, Kavita and Sia.', 'c4', 'core', '1+1+1+1'),
            ]}],
    }
