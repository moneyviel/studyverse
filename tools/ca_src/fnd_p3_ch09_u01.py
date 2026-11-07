"""CA Foundation · Paper 3 Quantitative Aptitude · Part B Logical Reasoning · Chapter 9 Number Series, Coding and Decoding and Odd Man Out.
Original explanations and problems. Every series term, code and position below is generated in Python and asserted before it is written."""
from lib import *
from ca_viva import P, V, ALT

UID = 'fnd-p3-ch09-u01'


def pos(ch): return ord(ch.upper()) - 64                       # A=1 ... Z=26
def let(n): return chr(64 + (n - 1) % 26 + 1)                 # wraps round: 27 -> A
def shift(word, k): return ''.join(let(pos(c) + k) for c in word)
def mirror(word): return ''.join(let(27 - pos(c)) for c in word)   # A<->Z, B<->Y ...
def is_prime(n): return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def M(mid, q, options, answer, explain, concept, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if check is not None: d['check'] = check
    return d


def build():
    # ---------------- computed facts used below ----------------
    # Illustration 1: second differences
    s1 = [3, 8, 17, 30]
    d1 = [5, 9, 13, 17, 21]
    t5 = 30 + d1[3]; assert t5 == 47 and t5 + d1[4] == 68
    c_i1 = Checks()
    c_i1.add('30+17', 'missing fifth term')
    c_i1.add('47+21', 'sixth term confirms the pattern (68)')
    # Illustration 2: wrong term in n^3 - 1
    true2 = [n ** 3 - 1 for n in range(2, 8)]; given2 = [7, 26, 63, 124, 214, 342]
    wrong = [g for g, t in zip(given2, true2) if g != t]; assert wrong == [214]
    c_i2 = Checks(); c_i2.add('6**3-1', 'correct fifth term')
    # Illustration 3: alphabet series DPK, GNL, JLM, ?
    terms3 = ['DPK']
    for _ in range(3):
        a, b, c = terms3[-1]; terms3.append(let(pos(a) + 3) + let(pos(b) - 2) + let(pos(c) + 1))
    assert terms3 == ['DPK', 'GNL', 'JLM', 'MJN']
    # Illustration 4: coding with shift and decoding
    assert shift('LEDGER', 2) == 'NGFIGT' and shift('NGFIGT', -2) == 'LEDGER'
    assert shift('VCZ', -2) == 'TAX'
    # Illustration 5: substitution number code
    code5 = dict(zip('CREDIT', '742593'))
    debit_code = ''.join(code5[ch] if ch in code5 else '1' for ch in 'DEBIT'); assert debit_code == '52193'
    code5['B'] = '1'
    tired = ''.join(code5[ch] for ch in 'TIRED'); assert tired == '39425'
    c_i5 = Checks(); c_i5.add('3*10000+9*1000+4*100+2*10+5', 'code of TIRED read off the key: T3 I9 R4 E2 D5')
    # Illustration 6: odd one out
    set6 = [21, 35, 49, 63, 74, 91]
    odd6 = [x for x in set6 if x % 7]; assert odd6 == [74]

    # MCQ arithmetic checks
    assert [4, 9, 19, 34, 54][-1] + 25 == 79
    s_m3 = [5]; [s_m3.append(s_m3[-1] * 2 + 1) for _ in range(5)]; assert s_m3 == [5, 11, 23, 47, 95, 191]
    assert [n ** 3 + 2 for n in range(1, 7)] == [3, 10, 29, 66, 127, 218]
    assert [n ** 3 + n ** 2 for n in range(1, 7)] == [2, 12, 36, 80, 150, 252]
    assert [p_ for p_ in range(13, 32) if is_prime(p_)] == [13, 17, 19, 23, 29, 31]
    assert [n * n + 1 for n in range(1, 9)] == [2, 5, 10, 17, 26, 37, 50, 65]
    assert [sum(k ** 3 for k in range(1, n + 1)) for n in range(1, 6)] == [1, 9, 36, 100, 225]
    assert [p_ * p_ for p_ in (2, 3, 5, 7, 11, 13)] == [4, 9, 25, 49, 121, 169]
    assert [(14 - n) ** 2 - 1 for n in range(1, 6)] == [168, 143, 120, 99, 80]
    assert shift('GARDEN', 1) == 'HBSEFO' and shift('FLOWER', 1) == 'GMPXFS'
    assert mirror('BAD') == 'YZW' and mirror('CAB') == 'XZY'
    assert shift('PAPER', 2) == 'RCRGT'
    assert let(27 - 8) == 'S' and let(pos('T') + 0) == 'T'
    assert ['AZ', 'CX', 'EV', 'GT', 'IR'] == [let(1 + 2 * i) + let(26 - 2 * i) for i in range(5)]
    seq15 = [2]; [seq15.append(seq15[-1] + k) for k in (3, 4, 5, 6)]; assert ''.join(let(x) for x in seq15) == 'BEINT'
    assert ''.join(let(26 - 3 * i) for i in range(5)) == 'ZWTQN'
    assert pos('C') + pos('A') + pos('T') == 24 and pos('D') + pos('O') + pos('G') == 26
    mango = dict(zip('MANGO', '52734')); assert ''.join(mango[c] for c in 'MOAN') == '5427'
    assert [x for x in (17, 23, 29, 33, 41) if not is_prime(x)] == [33]
    assert [x for x in (27, 64, 125, 144, 216) if round(x ** (1 / 3)) ** 3 != x] == [144]
    # letter series: block 'abba' repeated three times with blanks at positions 2, 6, 9 and 12 (1-based)
    full = 'abba' * 3; blanks = [2, 6, 9, 12]
    shown = ''.join('_' if i + 1 in blanks else ch for i, ch in enumerate(full))
    fill = ''.join(full[i - 1] for i in blanks); assert shown == 'a_baa_ba_bb_' and fill == 'bbaa'
    # case: folder code = shift +3 then reverse
    def folder(w): return shift(w, 3)[::-1]
    assert folder('AUDIT') == 'WLGXD' and folder('BANK') == 'NQDE'
    assert folder('LOAN') == 'QDRO'
    # decode 'HVDF' : reverse -> 'FDVH', shift -3 -> 'CASE'
    assert shift('HVDF'[::-1], -3) == 'CASE'

    qa = [10, 13, 19, 28, 40]; assert [qa[i + 1] - qa[i] for i in range(4)] == [3, 6, 9, 12]
    qb_true = [n ** 3 + 1 for n in range(1, 7)]; qb = [2, 9, 28, 67, 126, 217]
    assert [g for g, t in zip(qb, qb_true) if g != t] == [67] and qb_true[3] == 65
    c_q1 = Checks(); c_q1.add('40+15', 'missing term (difference 15)'); c_q1.add('4**3+1', 'correct value in place of the wrong term 67')
    assert mirror('MONEY') == 'NLMVB' and pos('C') + pos('O') + pos('S') + pos('T') == 57
    assert shift('SALES', 3)[::-1] == 'VHODV' and shift('VHODV'[::-1], -3) == 'SALES'
    c_q2 = Checks(); c_q2.add('3+15+19+20', 'letter-sum code of COST (3 + 15 + 19 + 20)')
    assert [x for x in (11, 13, 17, 21, 23) if not is_prime(x)] == [21] and let(20 - 9) == 'K'
    c_q3 = Checks(); c_q3.add('20-9', 'position of the letter 9 places left of T (20th)')
    assert shift('X', 3) == 'A'

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch09', 'n': 1,
        'title': 'Number Series, Coding and Decoding and Odd Man Out',
        'outcomes': ['Find a missing term or a wrong term in a number series by testing differences, ratios, powers, primes and alternate-term patterns in a fixed order.',
                     'Work with alphabet and letter series using letter positions (A = 1 … Z = 26), reverse positions (27 − n) and wrap-around.',
                     'Detect a letter-coding or number-coding rule from one example, apply it to a new word (coding) and run it backwards (decoding).',
                     'Pick the odd man out from groups of numbers, letters or words by naming the property that the rest share.'],
        'meta': {'difficulty': 'core', 'minutes': {'learn': 35, 'practice': 50}, 'prereq': [],
                 'exam_tip': 'Logical reasoning carries about 20 marks in Paper 3 and these questions are the fastest marks in the paper: aim for 30–40 seconds each. If no pattern appears within a minute, mark it for review and move on — every wrong answer costs ¼ mark.'},
        'concepts': [
            {'id': 'c1', 'title': 'Number series — the testing ladder', 'body': [
                'A number series is a list of numbers produced by one hidden rule. The examiner hides one term (missing-term question) or plants one incorrect term (wrong-term question).',
                'Test the rules in this order, stopping at the first one that fits every term: (1) first differences — constant means an arithmetic series; (2) second differences — differences of the differences are constant or themselves form a simple pattern; (3) ratios — each term is a fixed multiple of the previous one; (4) mixed operations such as ×2 + 1 or ×3 − 2; (5) squares, cubes and their neighbours (n² ± k, n³ ± k, n² + n, n³ + n²); (6) prime numbers; (7) two series interleaved (look at the 1st, 3rd, 5th … terms separately from the 2nd, 4th, 6th …); (8) running totals such as 1, 1+2, 1+2+3 … or sums of squares and cubes.',
                'Rough guide: slow, steady growth points to differences; growth that roughly doubles or triples points to multiplication; numbers sitting next to perfect squares or cubes (8, 26, 63, 124 …) point to powers ± 1.'],
             'blocks': [table(['Pattern', 'Sample series', 'Clue'], [
                 ['Constant difference', '7, 12, 17, 22, 27', 'add 5 every time'],
                 ['Differences in A.P.', '3, 8, 17, 30, 47', 'differences 5, 9, 13, 17'],
                 ['Constant ratio', '2, 6, 18, 54, 162', 'multiply by 3'],
                 ['Mixed operation', '5, 11, 23, 47, 95', '× 2 + 1'],
                 ['Powers ± k', '3, 10, 29, 66, 127', 'n³ + 2'],
                 ['Primes', '13, 17, 19, 23, 29', 'consecutive primes'],
                 ['Interleaved', '6, 30, 9, 27, 12, 24', 'odd places +3, even places −3'],
             ], title='Common number-series patterns')],
             'analogy': 'Like a doctor running tests in a fixed order — temperature, pulse, blood test — you check the cheapest pattern first and go deeper only if it fails.',
             'work': 'Auditors test sequences every day: invoice numbers, cheque numbers and GRN numbers should run without a break. A missing number may be a cancelled document or an unrecorded sale; a number out of place may be a duplicate or a backdated entry.'},
            {'id': 'c2', 'title': 'Missing term vs wrong term', 'body': [
                'Missing term: the rule is complete except for a blank. Find the rule from the terms on both sides of the blank and confirm the answer also produces the next given term.',
                'Wrong term: all terms are shown but one breaks the rule. Build the rule from the majority of terms, then compute what each term should be; the one that differs is the wrong term. The answer is the term that is printed, not the corrected value — read the options carefully.',
                'If a wrong term sits early in the series, the first differences all look broken after it. Try the power and ratio tests on individual terms instead of relying on differences.'],
             'analogy': 'A missing term is an empty chair in a class photo; a wrong term is a stranger standing in the line who looks almost like the others.',
             'work': 'In analytical review a CA compares each month\'s figure with the trend; a month that does not fit (the "wrong term") is the one sent for investigation.'},
            {'id': 'c3', 'title': 'Alphabet series and letter positions', 'body': [
                'Give every letter its position: A = 1, B = 2 … Z = 26. The reverse position (counting from Z) is 27 − forward position, so M (13) is 14th from the end and N (14) is 13th from the end.',
                'Memory aid for quick positions: E-J-O-T-Y stand at 5, 10, 15, 20 and 25. Any other letter is one or two steps from these anchors.',
                'In multi-letter terms (for example DPK, GNL, JLM) each letter position follows its own rule — one may move +3, another −2, another +1. Positions wrap round: one step after Z is A.',
                'Opposite-letter pairs add to 27: A–Z, B–Y, C–X … M–N.'],
             'blocks': [table(['Letter', 'A', 'E', 'J', 'M', 'N', 'O', 'T', 'Y', 'Z'], [
                 ['Forward position', '1', '5', '10', '13', '14', '15', '20', '25', '26'],
                 ['Reverse position (27 − n)', '26', '22', '17', '14', '13', '12', '7', '2', '1'],
             ], title='Anchor letters')],
             'analogy': 'The alphabet is a 26-seat circular bus: after seat 26 you are back at seat 1.',
             'work': 'Column letters in spreadsheets (A … Z, AA …) and alpha-numeric document codes use the same counting logic, so being quick with positions helps when tracing references in large working files.'},
            {'id': 'c4', 'title': 'Letter series (blanks in a repeating block)', 'body': [
                'A string of small letters repeats a short block (such as "abba" or "aabb") with some letters removed. The options give the missing letters in order.',
                'Method: guess the block length (try 3, 4 and 5), write the string in groups of that length, and fill the gaps so that every group is identical (or grows in a clear way, e.g. a, aa, aaa). Then read the filled letters from left to right.',
                'Check the chosen option by writing out the full string — two options often fit the first half only.'],
             'analogy': 'It is a beaded necklace with a few beads missing: once you see the repeating colour pattern, the missing beads are obvious.',
             'work': 'Spotting a repeating block in data — such as a standing instruction that posts the same amount every quarter — helps a CA separate routine entries from unusual ones.'},
            {'id': 'c5', 'title': 'Letter coding — finding and applying the rule', 'body': [
                'In letter coding each letter of a word is replaced by another letter under a fixed rule. Write the word above its code and compare letter by letter.',
                'Common rules: every letter shifted the same number of places (+1, −2 …); shifts that change by position (+1, +2, +3 …); the whole word written backwards; pairs of letters swapped; each letter replaced by its opposite (A↔Z, sum of positions 27); or a mix — for example shift then reverse.',
                'Coding means applying the rule to a plain word. Decoding means running the rule backwards — a +2 shift becomes −2, a reversal is reversed again.'],
             'blocks': [table(['Rule', 'Word', 'Code'], [
                 ['Each letter +1', 'GARDEN', 'HBSEFO'],
                 ['Each letter +2', 'LEDGER', 'NGFIGT'],
                 ['Opposite letter (27 − n)', 'BAD', 'YZW'],
                 ['Shift +3, then reverse', 'AUDIT', 'WLGXD'],
             ], title='Rules seen in this unit (generated by code)')],
             'analogy': 'A coding rule is a lock; decoding is turning the same key in the opposite direction.',
             'work': 'Client names and PAN numbers are often masked or encoded in shared files and data requests. Understanding simple substitution helps a CA judge whether masking is real protection or just a cosmetic change.'},
            {'id': 'c6', 'title': 'Number coding', 'body': [
                'Letters to numbers: a word is coded by letter positions (A = 1, B = 2 …), by the sum of positions, or by a digit fixed for each letter in a given example.',
                'Substitution key: when two coded words are given (for example CREDIT and DEBIT), list each letter with its digit; letters common to both words must get the same digit, which confirms the key. Then read the code of a new word straight from the key.',
                'Numbers to letters: a table such as 2 → P, 3 → N is given; convert each digit of the number in turn. Do not reorder digits unless the question says so.'],
             'analogy': 'A substitution key is a phone\'s contact list — once you know who is behind each number, any new call is easy to name.',
             'work': 'Ledger account codes, GL mapping keys and HSN/SAC codes are all number codes. Reading a mapping key accurately is a daily task in audits and system migrations.'},
            {'id': 'c7', 'title': 'Odd man out (classification)', 'body': [
                'Four or five items are given; all but one share a property. Name the property first, then the odd one is the item that lacks it.',
                'Numbers: even/odd, prime/composite, perfect squares or cubes, multiples of a number, n² + 1 type forms, digit sums. Letters: equal gaps between letters, vowels, positions. Words: category (currencies vs units), number of days in a month, function.',
                'If two items seem odd, look for a stronger property that only one of them breaks — the examiner intends a single answer.'],
             'analogy': 'In a basket of mangoes one apple stands out only once you have said the word "mango".',
             'work': 'Exception reporting — a vendor without a GSTIN, a payment without a purchase order — is classification in practice: define the normal group, then flag the item that does not belong.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Missing term by second differences', 'difficulty': 'core', 'minutes': 2,
             'q': 'Find the missing term: 3, 8, 17, 30, ?, 68',
             'solution': [table(['Terms', '3', '8', '17', '30', '?', '68'], [['First difference', '', '5', '9', '13', '17', '21']], title='Working'),
                          p('The first differences 5, 9, 13 … increase by 4 each time, so the next differences are 17 and 21.'),
                          p(f'Missing term = 30 + 17 = {t5}. Check: {t5} + 21 = 68, which matches the last term. Answer: {t5}.')],
             'checks': c_i1},
            {'id': 'i2', 'title': 'Wrong term near a cube', 'difficulty': 'moderate', 'minutes': 2,
             'q': 'Find the wrong term: 7, 26, 63, 124, 214, 342',
             'solution': [table(['n', '2', '3', '4', '5', '6', '7'], [['n³ − 1', *map(str, true2)], ['Given', *map(str, given2)]], title='Test n³ − 1'),
                          p(f'Every term is one less than a cube except the fifth: 6³ − 1 = {true2[4]}, but {given2[4]} is printed. The wrong term is {given2[4]}.')],
             'checks': c_i2},
            {'id': 'i3', 'title': 'Three-letter alphabet series', 'difficulty': 'core', 'minutes': 2,
             'q': 'Find the next term: DPK, GNL, JLM, ?',
             'solution': [table(['Position', '1st letter', '2nd letter', '3rd letter'], [['DPK', 'D (4)', 'P (16)', 'K (11)'], ['GNL', 'G (7)', 'N (14)', 'L (12)'], ['JLM', 'J (10)', 'L (12)', 'M (13)'], ['Rule', '+3', '−2', '+1'], ['Next', 'M (13)', 'J (10)', 'N (14)']], title='Letter positions'),
                          p(f'Applying +3, −2 and +1 to J, L and M gives {terms3[3]}.')]},
            {'id': 'i4', 'title': 'Coding and decoding with a +2 shift', 'difficulty': 'core', 'minutes': 2,
             'q': 'In a code language LEDGER is written as NGFIGT. (a) How is TAX written? (b) Which word is written as VCZ?',
             'solution': [table(['Word', 'L', 'E', 'D', 'G', 'E', 'R'], [['Code', 'N', 'G', 'F', 'I', 'G', 'T'], ['Shift', '+2', '+2', '+2', '+2', '+2', '+2']], title='Find the rule'),
                          p(f'(a) Each letter moves 2 places forward, so TAX → {shift("TAX", 2)}.'),
                          p(f'(b) Decoding reverses the rule: move each letter of VCZ 2 places back → {shift("VCZ", -2)}. Notice that the code for TAX and the word behind VCZ differ — decoding is not the same as coding again.')]},
            {'id': 'i5', 'title': 'Substitution number code from two words', 'difficulty': 'moderate', 'minutes': 3,
             'q': 'If CREDIT is coded 742593 and DEBIT is coded 52193, how is TIRED coded?',
             'solution': [table(['Letter', 'C', 'R', 'E', 'D', 'I', 'T'], [['Digit', '7', '4', '2', '5', '9', '3']], title='Step 1 — key from CREDIT'),
                          p('Step 2 — confirm with DEBIT: D = 5, E = 2, I = 9 and T = 3 agree with the key, and the only new letter, B, takes the remaining digit 1. The key is consistent.'),
                          p(f'Step 3 — read TIRED from the key: T 3, I 9, R 4, E 2, D 5. Code = {tired}.'),
                          note('Always confirm a substitution key with the second word before using it; if a common letter gets two different digits, the rule is not simple substitution.')],
             'checks': c_i5},
            {'id': 'i6', 'title': 'Odd one out among multiples', 'difficulty': 'core', 'minutes': 1,
             'q': 'Find the odd one out: 21, 35, 49, 63, 74, 91',
             'solution': [p(f'21 = 7 × 3, 35 = 7 × 5, 49 = 7 × 7, 63 = 7 × 9, 91 = 7 × 13 — all multiples of 7. 74 = 7 × 10 + 4 is not. Odd one out: {odd6[0]}.')]},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Gaps in an invoice series', 'role': 'Articled assistant on a statutory audit', 'situation': 'The sales register of a distributor shows invoice numbers INV-2401 to INV-2460 for March, but only 57 invoices are listed.',
             'steps': ['Sort the register by invoice number and compute the first difference between consecutive numbers; every difference should be 1.', 'List the numbers where the difference is 2 or more — those are the missing invoices (the "missing terms").', 'Ask for the cancelled copies or system logs of the missing numbers; a cancelled invoice should show the reason and approval.', 'Look also for a number appearing twice or out of date order — the audit version of a "wrong term".'],
             'takeaway': 'A continuous number series is a control. Testing it is the same skill as a missing-term question, only with real money behind it.',
             'think': 'Sixty numbers are issued and 57 appear. If two cancelled copies are produced, what remains to be explained?', 'answer': 'One invoice number is still unexplained; it could be an unrecorded sale, so it must be traced before the auditor signs off on completeness of revenue.'},
            {'id': 'j2', 'title': 'Is this "masked" client data really masked?', 'role': 'CA in a consulting team handling client data', 'situation': 'A junior has "masked" client names in a file shared with a vendor by moving every letter two places forward (so LEDGER Ltd appears as NGFIGT Ltd).',
             'steps': ['Recognise the rule from one known name — a constant shift is found in seconds, exactly as in a coding question.', 'Note that anyone can decode every other name by shifting two places back.', 'Replace the names with random reference numbers kept in a separate key file with restricted access.', 'Record the change in the data-sharing log.'],
             'takeaway': 'A simple coding rule hides nothing from someone who has seen one example. Real masking needs a key that cannot be worked out from the data.',
             'think': 'Why is a random reference number safer than any letter-shift rule?', 'answer': 'A random number has no rule linking it to the name, so knowing one pair tells you nothing about the others.'},
            {'id': 'j3', 'title': 'The month that does not fit', 'role': 'CA in industry preparing a monthly MIS', 'situation': 'Electricity cost of a plant for six months (₹ lakh): 4.2, 4.4, 4.6, 6.9, 5.0, 5.2. Production rose steadily each month.',
             'steps': ['Look for the pattern: costs rise by about 0.2 lakh a month in line with production.', 'The fourth month (6.9) breaks the pattern — the "odd man out" or "wrong term".', 'Check whether the bill includes arrears, a penalty for low power factor, or a mis-posting of another plant\'s bill.', 'Correct or explain the variance in the MIS.'],
             'takeaway': 'Reasoning patterns help analytical review: define the normal pattern, then investigate the item that does not fit it.',
             'think': 'If the pattern had held, what would the fourth month\'s cost have been?', 'answer': 'About ₹4.8 lakh (4.6 + 0.2), so roughly ₹2.1 lakh needs explaining.',
             'checks': [{'expr': '4.6+0.2', 'value': 4.8, 'label': 'expected fourth-month cost'}, {'expr': '6.9-4.8', 'value': 2.1, 'label': 'unexplained excess'}]},
        ],
        'mcqs': [
            M('m1', 'Find the next term: 4, 9, 19, 34, 54, ?', ['79', '74', '84', '89'], 0, 'Differences are 5, 10, 15, 20, so the next difference is 25: 54 + 25 = 79.', 'c1', 'core', '54+25'),
            M('m2', 'Find the next term: 2, 6, 18, 54, ?', ['162', '108', '148', '216'], 0, 'Each term is 3 times the previous one: 54 × 3 = 162. 108 comes from wrongly using × 2.', 'c1', 'core', '54*3'),
            M('m3', 'Find the next term: 5, 11, 23, 47, 95, ?', ['191', '190', '189', '143'], 0, 'Rule × 2 + 1: 95 × 2 + 1 = 191. 190 forgets the +1; 143 adds the last difference 48 instead of doubling the difference.', 'c1', 'moderate', '95*2+1'),
            M('m4', 'Find the missing term: 1, 8, 27, 64, ?, 216', ['125', '100', '144', '81'], 0, 'Cubes of 1 to 6: 5³ = 125.', 'c1', 'core', '5**3'),
            M('m5', 'Find the next term: 3, 10, 29, 66, 127, ?', ['218', '216', '188', '210'], 0, 'Each term is n³ + 2: 1+2, 8+2, 27+2, 64+2, 125+2, so next = 216 + 2 = 218. 216 forgets the +2.', 'c1', 'moderate', '6**3+2'),
            M('m6', 'Find the next term: 6, 30, 9, 27, 12, 24, ?', ['15', '21', '18', '14'], 0, 'Two series are interleaved: odd places 6, 9, 12, 15 (+3) and even places 30, 27, 24 (−3). The 7th term is an odd place: 15. 21 continues the even series by mistake.', 'c1', 'moderate', '12+3'),
            M('m7', 'Find the next term: 13, 17, 19, 23, 29, ?', ['31', '33', '30', '35'], 0, 'Consecutive prime numbers; the prime after 29 is 31. 33 = 3 × 11 and 35 = 5 × 7 are not prime.', 'c1', 'core', '29+2'),
            M('m8', 'Find the wrong term: 3, 6, 12, 24, 46, 96', ['46', '24', '96', '12'], 0, 'Each term doubles: 24 × 2 = 48, not 46; and 48 × 2 = 96 fits. Wrong term: 46.', 'c2', 'core', '46'),
            M('m9', 'Find the wrong term: 4, 9, 25, 49, 121, 168', ['168', '121', '25', '9'], 0, 'Squares of primes 2, 3, 5, 7, 11, 13 — the last should be 13² = 169. The printed 168 is wrong.', 'c2', 'moderate', '168'),
            M('m10', 'Find the next term: 2, 3, 5, 9, 17, ?', ['33', '31', '34', '25'], 0, 'Differences 1, 2, 4, 8 double each time, so the next difference is 16: 17 + 16 = 33. (Equivalently, each term = previous × 2 − 1.)', 'c1', 'moderate', '17+16'),
            M('m11', 'Find the next term: 168, 143, 120, 99, ?', ['80', '81', '78', '84'], 0, 'Terms are 13² − 1, 12² − 1, 11² − 1, 10² − 1, so next = 9² − 1 = 80. 81 forgets the −1.', 'c1', 'moderate', '9**2-1'),
            M('m12', 'Find the next term: 1, 9, 36, 100, ?', ['225', '196', '216', '200'], 0, 'Running totals of cubes: 1, 1+8, 1+8+27, 1+8+27+64, so next = 100 + 125 = 225 (also the square of 1+2+3+4+5 = 15).', 'c1', 'hard', '100+5**3'),
            M('m13', 'Find the next term: 1, 2, 6, 24, 120, ?', ['720', '600', '840', '240'], 0, 'Multipliers increase: × 2, × 3, × 4, × 5, so next = 120 × 6 = 720.', 'c1', 'core', '120*6'),
            M('m14', 'Find the next term: 2, 12, 36, 80, 150, ?', ['252', '210', '222', '240'], 0, 'Each term is n³ + n²: 1+1, 8+4, 27+9, 64+16, 125+25, so next = 216 + 36 = 252. Differences 10, 24, 44, 70 have second differences 14, 20, 26, so the next second difference is 32, the next difference 102, and 150 + 102 = 252 — the same answer.', 'c1', 'hard', '6**3+6**2'),
            M('m15', 'Find the wrong term: 2, 5, 10, 17, 26, 37, 50, 64', ['64', '50', '37', '26'], 0, 'Terms are n² + 1: the 8th term should be 8² + 1 = 65, so 64 is wrong.', 'c2', 'moderate', '64'),
            M('m16', 'Find the next term: AZ, CX, EV, GT, ?', ['IR', 'IS', 'HR', 'JR'], 0, 'First letters move +2 (A, C, E, G, I); second letters move −2 (Z, X, V, T, R).', 'c3', 'core'),
            M('m17', 'Find the next letter: B, E, I, N, ?', ['T', 'S', 'U', 'R'], 0, 'Positions 2, 5, 9, 14 have gaps 3, 4, 5, so the next gap is 6: 14 + 6 = 20 = T.', 'c3', 'core'),
            M('m18', 'Find the next letter: Z, W, T, Q, ?', ['N', 'O', 'M', 'P'], 0, 'Moving back 3 each time: 26, 23, 20, 17, 14 = N.', 'c3', 'core'),
            M('m19', 'Which letter is 8th from the right end of the English alphabet?', ['S', 'R', 'T', 'H'], 0, 'Reverse position rule: forward position = 27 − 8 = 19, which is S. H is 8th from the left end.', 'c3', 'core'),
            M('m20', 'Fill the blanks in order: a _ b a a _ b a _ b b _', ['bbaa', 'baba', 'abab', 'bbab'], 0, f'The block "abba" repeats three times: abba | abba | abba. The blanks are letters 2, 6, 9 and 12, i.e. b, b, a, a.', 'c4', 'moderate'),
            M('m21', 'If GARDEN is coded as HBSEFO, how is FLOWER coded?', ['GMPXFS', 'EKNVDQ', 'GMPXSF', 'HMPXFS'], 0, 'Each letter moves one place forward. EKNVDQ moves backwards; GMPXSF swaps the last two letters.', 'c5', 'core'),
            M('m22', 'If PLANT is written as TNALP, how is STOCK written?', ['KCOTS', 'KCTOS', 'TSOCK', 'SKCOT'], 0, 'The word is written in reverse order.', 'c5', 'core'),
            M('m23', 'If BAD is coded as YZW, how is CAB coded?', ['XZY', 'DBC', 'XYZ', 'ZXY'], 0, 'Each letter is replaced by its opposite (positions add to 27): C → X, A → Z, B → Y. DBC is a +1 shift, a common slip.', 'c5', 'moderate'),
            M('m24', 'In a code, each letter of a word is moved two places forward. Which word is coded as RCRGT?', ['PAPER', 'TETIV', 'QBQFS', 'PAPRE'], 0, 'Decode by moving each letter two places back: R→P, C→A, R→P, G→E, T→R. TETIV is the result of coding again instead of decoding.', 'c5', 'core'),
            M('m25', 'If A = 1, B = 2 and so on, and each letter is written as its number, how is BEAD written?', ['2514', '2541', '2154', '1452'], 0, 'B = 2, E = 5, A = 1, D = 4, written in the same order: 2514.', 'c6', 'core', '2*1000+5*100+1*10+4'),
            M('m26', 'If MANGO is coded as 52734, how is MOAN coded?', ['5427', '5247', '5472', '4527'], 0, 'From the key M = 5, A = 2, N = 7, G = 3, O = 4: MOAN = 5-4-2-7.', 'c6', 'core', '5*1000+4*100+2*10+7'),
            M('m27', 'If CAT = 24 because 3 + 1 + 20 = 24, what is DOG?', ['26', '24', '27', '25'], 0, 'D 4 + O 15 + G 7 = 26.', 'c6', 'core', '4+15+7'),
            M('m28', 'In a code 1 → K, 2 → R, 3 → M, 4 → T, 5 → B. How is 32415 written?', ['MRTKB', 'MRKTB', 'MTRKB', 'KRTMB'], 0, 'Convert each digit in order: 3 M, 2 R, 4 T, 1 K, 5 B.', 'c6', 'core'),
            M('m29', 'Find the odd one out: 17, 23, 29, 33, 41', ['33', '41', '17', '29'], 0, 'All are prime except 33 = 3 × 11.', 'c7', 'core', '33'),
            M('m30', 'Find the odd one out: 27, 64, 125, 144, 216', ['144', '64', '216', '27'], 0, 'All are perfect cubes (3³, 4³, 5³, 6³) except 144, which is 12², a square. 64 is both a square and a cube, so it still belongs to the cubes.', 'c7', 'moderate', '144'),
            M('m31', 'Find the odd one out: April, June, September, October', ['October', 'June', 'April', 'September'], 0, 'April, June and September have 30 days; October has 31.', 'c7', 'core'),
            M('m32', 'Find the odd one out: ACE, BDF, GIK, MOP', ['MOP', 'GIK', 'BDF', 'ACE'], 0, 'In the others the letters move +2, +2 (A C E, B D F, G I K). MOP moves +2 then +1 — it would need MOQ.', 'c7', 'moderate'),
            M('m33', 'Find the odd one out: Rupee, Dirham, Euro, Kilogram', ['Kilogram', 'Euro', 'Rupee', 'Dirham'], 0, 'Three are currencies; a kilogram is a unit of mass.', 'c7', 'core'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': '(a) Find the next term of 10, 13, 19, 28, 40, ? (2 marks)  (b) Find the wrong term in 2, 9, 28, 67, 126, 217 and state the correct value. (2 marks) Show your working.',
             'model': [p('(a) Differences: 3, 6, 9, 12 — they increase by 3, so the next difference is 15. Next term = 40 + 15 = 55.'),
                       table(['n', '1', '2', '3', '4', '5', '6'], [['n³ + 1', *map(str, qb_true)], ['Given', *map(str, qb)]], title='(b) Test n³ + 1'),
                       p('(b) Every term is one more than a cube except the 4th: 4³ + 1 = 65, but 67 is printed. Wrong term = 67; correct value = 65.')],
             'scheme': [{'id': 's1', 'pt': '(a) differences found and their pattern (+3) stated', 'm': 1, 'skill': 'analysis'},
                        {'id': 's2', 'pt': '(a) next term 55', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': '(b) rule n³ + 1 identified', 'm': 1, 'skill': 'analysis'},
                        {'id': 's4', 'pt': '(b) wrong term 67 and correct value 65 both stated', 'm': 1, 'skill': 'conclusion'}],
             'remarks': ['In (b) many students compute differences (7, 19, 39, 59, 91) and get lost; when terms sit next to cubes, test the cube rule directly.', 'Full marks need both the wrong term and the value that should replace it.'],
             'mistakes': ['Giving 65 as "the wrong term" — 65 is the correction; 67 is the wrong term.', 'Adding 12 again in (a) instead of the next difference 15.'],
             'tips': ['Write the differences under the series in a second row — the pattern becomes visible at a glance.', 'In the MCQ paper, test the most likely option by putting it back into the series.'],
             'checks': c_q1},
            {'id': 'q2', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'moderate', 'pad': 'text',
             'q': '(a) If each letter is replaced by its opposite letter (A ↔ Z, B ↔ Y …), how is MONEY coded? (1 mark)  (b) If CAT = 24 and DOG = 26 under a letter-sum code, what is COST? (1 mark)  (c) Under a rule "move each letter three places forward, then write the result backwards", decode VHODV. (2 marks)',
             'model': [p(f'(a) Opposite letter = 27 − position: M (13) → 14 N; O (15) → 12 L; N (14) → 13 M; E (5) → 22 V; Y (25) → 2 B. Code = {mirror("MONEY")}.'),
                       p('(b) C 3 + O 15 + S 19 + T 20 = 57.'),
                       p(f'(c) Undo the steps in reverse order. Step 1 — undo the reversal: VHODV → VDOHV. Step 2 — move each letter three places back: V→S, D→A, O→L, H→E, V→S. Decoded word = {shift("VDOHV", -3)}. Check by coding SALES: +3 gives VDOHV, reversed VHODV ✓.')],
             'scheme': [{'id': 's1', 'pt': '(a) opposite-letter rule applied; NLMVB', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': '(b) letter positions added correctly', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': '(c) steps undone in reverse order (reverse first)', 'm': 1, 'skill': 'concept'},
                        {'id': 's4', 'pt': '(c) shift of three places back applied to every letter', 'm': 1, 'skill': 'computation'}],
             'remarks': ['Part (c) separates good candidates: the second step must be undone first.'],
             'mistakes': ['Shifting forward again while decoding.', 'Using 26 − position for the opposite letter (gives the wrong letter by one).', 'Adding S as 18 (that is R).'],
             'tips': ['Keep a written A–Z strip with positions on your rough sheet for the whole reasoning section.'],
             'checks': c_q2},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': '(a) Find the odd one out: 11, 13, 17, 21, 23 and give the reason. (1 mark)  (b) Which letter is 9th to the left of the 20th letter from the left end of the alphabet? (1 mark)  (c) Fill the blanks of the letter series a _ b a a _ b a _ b b _ and state the block. (2 marks)',
             'model': [p('(a) 11, 13, 17 and 23 are prime numbers; 21 = 3 × 7 is not. Odd one out: 21.'),
                       p(f'(b) 20th letter from the left is T. Nine places to its left: 20 − 9 = 11 → {let(11)}.'),
                       p(f'(c) Try a block of four letters: a b b a | a b b a | a b b a. The blanks are positions 2, 6, 9 and 12 → {fill}. Block = "abba".')],
             'scheme': [{'id': 's1', 'pt': '(a) 21 with the reason (not prime)', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': '(b) 20 − 9 = 11 → K', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': '(c) repeating block identified', 'm': 1, 'skill': 'analysis'},
                        {'id': 's4', 'pt': '(c) blanks filled in order: b, b, a, a', 'm': 1, 'skill': 'computation'}],
             'remarks': ['In (b) "to the left" means subtract; candidates who add get 29 → wrap-around confusion.'],
             'mistakes': ['Calling 23 odd because it is "the largest".', 'Filling the blanks without writing out the whole string to confirm.'],
             'tips': ['For position questions write the arithmetic (20 − 9 = 11) — it avoids left/right slips.'],
             'checks': c_q3},
        ],
        'revision': {
            'summary': ['Number series: test differences → second differences → ratios → mixed operations (×2+1) → powers ± k → primes → alternate terms → running totals.',
                        'Missing term: find the rule and confirm it with the next given term. Wrong term: build the rule from the majority; the printed term that breaks it is the answer.',
                        'Letters: A = 1 … Z = 26; reverse position = 27 − n; anchors E J O T Y = 5, 10, 15, 20, 25; opposite pairs add to 27; positions wrap after Z.',
                        'Coding: compare word and code letter by letter; common rules — constant shift, varying shift, reversal, pair swap, opposite letter, combinations. Decoding runs the rule backwards and undoes the last step first.',
                        'Number coding: letter positions, letter sums, or a substitution key confirmed by a second word.',
                        'Odd man out: name the shared property first; the odd item lacks it.'],
            'remember': ['Squares 1–20 and cubes 1–10 by heart (e.g. 13² = 169, 17² = 289, 7³ = 343, 9³ = 729).', 'Primes up to 100: 25 of them, starting 2, 3, 5, 7, 11, 13, 17, 19, 23, 29.', 'Each wrong MCQ answer costs ¼ mark — skip if you cannot see the rule in about a minute.'],
            'traps': ['Answering the corrected value in a wrong-term question.', 'Coding again instead of decoding.', 'Treating 1 or 9 as prime; forgetting 2 is prime.', 'Counting the reverse position as 26 − n instead of 27 − n.']},
        'quickref': [{'k': 'Reverse letter position', 'v': '27 − forward position (M 13 ↔ 14 from right)'},
                     {'k': 'Opposite letters', 'v': 'Positions add to 27: A–Z, B–Y, C–X … M–N'},
                     {'k': 'Anchor letters', 'v': 'E 5 · J 10 · O 15 · T 20 · Y 25'},
                     {'k': 'Series test order', 'v': 'Differences · second differences · ratio · mixed (×a ± b) · n² ± k, n³ ± k · primes · alternate terms · running totals'},
                     {'k': 'Decoding', 'v': 'Reverse the rule; undo the last step first'},
                     {'k': 'Substitution key', 'v': 'Common letters of two coded words must carry the same digit'}],
        'viva': [
            V('v1', 'How do you attack a number series where one term is missing?',
              'First I check the differences between consecutive terms, and if they are not constant I look at the second differences. If the terms grow fast I test a ratio or a multiplication such as times two plus one. Then I check squares, cubes and prime numbers, and finally I see whether alternate terms form two separate series. The answer must fit every given term.',
              [P('p1', 'Check first and second differences', 3, 'difference|subtract|gap between|minus the previous'),
               P('p2', 'Test ratios / multiplication', 2, 'ratio|multipl|times|product|divid|doubl|tripl'),
               P('p3', 'Check squares, cubes and primes', 2, 'square|cube|prime|power'),
               P('p4', 'Check alternate terms (two interleaved series)', 2, 'alternate|two series|two separate|interleav|odd position|every second|altern|two different series'),
               P('p5', 'Confirm the answer fits every term', 1, 'fit every|fits all|every term|all terms|all the terms|verify|confirm|check against|cross check')], 'c1'),
            V('v2', 'How do you find the position of a letter counted from the right end of the alphabet, and which letters form opposite pairs?',
              'Subtract the forward position from twenty seven. For example M is thirteenth from the left and fourteenth from the right. Opposite letters are pairs whose positions add up to twenty seven, like A and Z, B and Y, and M and N. The anchor letters E J O T Y sit at five, ten, fifteen, twenty and twenty five.',
              [P('p1', 'Reverse position = 27 − forward position', 4, '27|20 7', 'subtract|minus|less|take away|deduct|reduc'),
               P('p2', 'Opposite letters add up to 27 (A–Z, B–Y, M–N)', 3, 'opposite|pair|mirror|partner', 'z|m n|b y|add|sum|total', min=2),
               P('p3', 'Anchor letters E J O T Y = 5, 10, 15, 20, 25', 3, 'ejoty|e j o t y|5 10 15 20 25|5 10 15|e 5 j 10')], 'c3'),
            V('v3', 'What is the difference between coding and decoding? Give an example.',
              'Coding means applying the rule to a plain word to get its code, while decoding means working back from the code to the original word by reversing the rule. If the rule is move each letter two places forward, then to decode we move each letter two places backward. So LEDGER becomes NGFIGT, and VCZ decodes to TAX.',
              [P('p1', 'Coding: apply the rule to the word to get the code', 3, 'coding|encod|code', 'word|plain|original|actual', 'rule|appl|convert|turn|chang|transform'),
               P('p2', 'Decoding: go back from code to word by reversing the rule', 4, 'decod', 'revers|backward|opposite|back|undo|invert'),
               P('p3', 'Example: +2 forward to code, −2 back to decode', 3, 'forward|ahead|plus|add|next', 'backward|back|minus|subtract|behind|previous')], 'c5'),
            V('v4', 'What is an odd man out question and how should you solve it?',
              'All the items except one share a common property. First identify that common property, such as all being prime numbers or all being multiples of seven, and then the item that does not have the property is the odd one out. If two items look odd, look for a stronger property so that only one answer remains.',
              [P('p1', 'All but one share a common property', 4, 'common|share|same|similar|alike', 'propert|feature|quality|rule|characteristic|pattern|trait|thing'),
               P('p2', 'Identify the property first; the item lacking it is odd', 4, 'identif|find|name|spot|first|figure out', 'not have|does not|doesn t|lack|break|differ|not fit|fail|not share|not follow|not satisf|without|missing'),
               P('p3', 'If two look odd, use a stronger property — one answer', 2, 'two|more than one|both|several', 'stronger|stricter|specific|single|only one|one answer|unique|narrow|better')], 'c7'),
            V('v5', 'How is a wrong-term question different from a missing-term question?',
              'In a missing term question one place is blank and we find the value that fits the rule. In a wrong term question every term is printed but one of them breaks the rule. We find the rule from the majority of terms, compute what each term should be, and the term that differs is the wrong one. The answer is the printed wrong term, not the corrected value.',
              [P('p1', 'Missing term: a blank place to be filled', 3, 'blank|gap|empty|question mark|not given|left out', 'fill|find|fits|value|calculat|compute|work out'),
               P('p2', 'Wrong term: all terms shown, one breaks the rule', 3, 'all|every|each', 'break|not fit|doesn t fit|does not fit|violat|differ|incorrect|not follow|odd'),
               P('p3', 'Build the rule from the majority of terms', 2, 'majority|most|rest|others|remaining|other terms'),
               P('p4', 'Answer the printed term, not the corrected value', 2, 'print|given|shown|appear|actual|written|stated', 'not the correct|not correct|rather than|instead|not the right|not the value|never the correct')], 'c2'),
            V('v6', 'If a coding rule shifts each letter three places forward and then writes the result backwards, how do you decode a code?',
              'Undo the steps in reverse order. First write the code backwards to undo the reversal, then move every letter three places back. For example HVDF reversed is FDVH, and moving each letter three back gives CASE.',
              [P('p1', 'Undo the reversal first (reverse order of steps)', 4, 'revers|backward|back to front|flip|undo', 'first|start|begin|order|initially'),
               P('p2', 'Then move every letter three places back', 4, '3 back|3 place back|3 step back|3 backward|minus 3|subtract 3|back 3|back by 3|3 behind|3 letters back|3 position back|3 earlier'),
               P('p3', 'Example worked', 2, 'case|example|instance|e g|eg|like|say')], 'c5'),
        ],
        'cases': [{
            'id': 'k1', 'title': 'Folder codes at a CA firm', 'difficulty': 'moderate',
            'case': 'To keep client folder names off shared screens, a CA firm\'s office manager codes each name in two steps: Step 1 — move every letter three places forward in the alphabet (X → A, Y → B, Z → C); Step 2 — write the result backwards. Under this rule AUDIT appears as WLGXD.',
            'mcqs': [
                M('k1a', 'How is BANK coded?', ['NQDE', 'EDQN', 'KNAB', 'NQED'], 0, 'Step 1: B A N K → E D Q N. Step 2: reverse → NQDE. EDQN stops after step 1.', 'c5', 'core'),
                M('k1b', 'Which folder name is coded as HVDF?', ['CASE', 'FDVH', 'ESAC', 'KYGI'], 0, 'Undo step 2 first: HVDF → FDVH. Then move each letter three back: F→C, D→A, V→S, H→E → CASE.', 'c5', 'moderate'),
                M('k1c', 'How is LOAN coded?', ['QDRO', 'ORDQ', 'NAOL', 'QDOR'], 0, 'L O A N → O R D Q (+3), reversed → QDRO.', 'c5', 'core'),
                M('k1d', 'Under step 1 alone, which letter becomes A?', ['X', 'D', 'C', 'Z'], 0, 'Moving three places forward from X gives Y, Z, A. D is what A becomes, the opposite direction.', 'c3', 'moderate'),
            ]}],
    }
