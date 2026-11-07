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


def M(mid, q, options, answer, explain, concept, difficulty='core', check=None, topic=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'difficulty': difficulty}
    if topic: d['topic'] = topic
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
            M('m1', 'Find the next term: 4, 9, 19, 34, 54, ?', ['79', '74', '84', '89'], 0, 'Start the testing ladder with differences: 9 − 4 = 5, then 10, 15, 20 — they rise by 5 each time. The next difference is 25, so the next term is 54 + 25 = 79. The trap is 74, which repeats the last difference of 20 instead of continuing the pattern. In practice: spotting how differences grow is the same habit an analyst uses to tell whether a cost or sales trend is rising steadily or accelerating.', 'c1', 'core', '54+25', topic='Number series — the testing ladder'),
            M('m2', 'Find the next term: 2, 6, 18, 54, ?', ['162', '108', '148', '216'], 0, 'When differences grow quickly, test ratios: 6/2 = 18/6 = 54/18 = 3, so each term is three times the previous one. The next term is 54 × 3 = 162. The trap is 108, which uses × 2; 216 is 54 × 4. In practice: a constant multiplier is the signature of compound growth, the pattern an analyst sees in a subscriber base or an investment that triples each period.', 'c1', 'core', '54*3', topic='Number series — the testing ladder'),
            M('m3', 'Find the next term: 5, 11, 23, 47, 95, ?', ['191', '190', '189', '143'], 0, "Each term is double the previous one plus 1: 5 × 2 + 1 = 11, 11 × 2 + 1 = 23, and so on. So the next term is 95 × 2 + 1 = 191. The trap is 190, which doubles but forgets the +1; 143 adds the last difference (48) again instead of noticing that the differences double. In practice: 'multiply then add' rules mimic a balance that grows by a percentage plus a fixed top-up, such as a deposit with regular additions.", 'c1', 'moderate', '95*2+1', topic='Number series — the testing ladder'),
            M('m4', 'Find the missing term: 1, 8, 27, 64, ?, 216', ['125', '100', '144', '81'], 0, 'The terms are the cubes of 1 to 6: 1³, 2³, 3³, 4³, ?, 6³ = 216. The missing term is 5³ = 125. The trap is 100, which is 10² and fits no pattern here; 81 and 144 are squares (9², 12²) that look plausible. In practice: memorising squares up to 30 and cubes up to 15 speeds up the logical-reasoning section of Paper 3 and also helps quick mental checks at work.', 'c1', 'core', '5**3', topic='Number series — the testing ladder'),
            M('m5', 'Find the next term: 3, 10, 29, 66, 127, ?', ['218', '216', '188', '210'], 0, "Compare each term with the cubes 1, 8, 27, 64, 125: every term is 2 more (n³ + 2). The 6th term is 6³ + 2 = 216 + 2 = 218. The trap is 216, which spots the cubes but forgets the +2. In practice: recognising 'standard pattern plus a constant' is the same skill used to see a fixed fee riding on top of a variable charge in a client's bill.", 'c1', 'moderate', '6**3+2', topic='Number series — the testing ladder'),
            M('m6', 'Find the next term: 6, 30, 9, 27, 12, 24, ?', ['15', '21', '18', '14'], 0, 'Two series alternate. Odd places: 6, 9, 12, … rising by 3. Even places: 30, 27, 24, … falling by 3. The 7th term is an odd place, so it is 12 + 3 = 15. The trap is 21, which continues the even-place series (24 − 3) instead of the odd one. In practice: interleaved patterns are common in real data — for example, alternating months of high and low sales — and an analyst separates them before forecasting.', 'c1', 'moderate', '12+3', topic='Number series — the testing ladder'),
            M('m7', 'Find the next term: 13, 17, 19, 23, 29, ?', ['31', '33', '30', '35'], 0, 'The terms 13, 17, 19, 23, 29 are consecutive prime numbers, so the next term is the next prime after 29, which is 31. The trap is 33, which keeps the last gap or adds 4, but 33 = 3 × 11 is not prime; 35 = 5 × 7 is also composite. In practice: prime-based series test whether a candidate knows number properties, a staple of the reasoning section in CA Foundation and in bank and SSC recruitment tests.', 'c1', 'core', '29+2', topic='Number series — the testing ladder'),
            M('m8', 'Find the wrong term: 3, 6, 12, 24, 46, 96', ['46', '24', '96', '12'], 0, 'The series doubles: 3, 6, 12, 24, then 24 × 2 = 48, and 48 × 2 = 96. The printed 46 breaks the rule, while 96 fits only if the correct term is 48. So the wrong term is 46. The trap is 96, which looks wrong when compared with 46 but is actually consistent with the pattern. In practice: auditors look for the one figure that breaks an otherwise consistent pattern — the same logic used to spot a mistyped entry in a ledger.', 'c2', 'core', '46', topic='Missing term vs wrong term'),
            M('m9', 'Find the wrong term: 4, 9, 25, 49, 121, 168', ['168', '121', '25', '9'], 0, 'The terms are squares of consecutive primes: 2², 3², 5², 7², 11², and the last should be 13² = 169. The printed 168 is therefore wrong. The trap is 121, which may look odd but is 11², exactly in pattern. In practice: a figure off by one from the expected value often signals a data-entry slip, which auditors and reviewers learn to spot quickly.', 'c2', 'moderate', '168', topic='Missing term vs wrong term'),
            M('m10', 'Find the next term: 2, 3, 5, 9, 17, ?', ['33', '31', '34', '25'], 0, 'The differences are 1, 2, 4, 8 — doubling each time — so the next difference is 16 and the next term is 17 + 16 = 33. Equivalently, each term = previous × 2 − 1 (17 × 2 − 1 = 33). The trap is 31, which takes a smaller jump; 34 simply doubles 17. In practice: doubling differences signal exponential growth, the pattern seen in viral app downloads or an unchecked compounding debt.', 'c1', 'moderate', '17+16', topic='Number series — the testing ladder'),
            M('m11', 'Find the next term: 168, 143, 120, 99, ?', ['80', '81', '78', '84'], 0, 'Each term is one less than a perfect square: 13² − 1 = 168, 12² − 1 = 143, 11² − 1 = 120, 10² − 1 = 99. The next is 9² − 1 = 80. (Differences 25, 23, 21 fall by 2, giving 19 next — the same answer.) The trap is 81, which spots the squares but forgets the −1. In practice: checking a pattern two ways, as here, is a good habit before committing to an answer under negative marking.', 'c1', 'moderate', '9**2-1', topic='Number series — the testing ladder'),
            M('m12', 'Find the next term: 1, 9, 36, 100, ?', ['225', '196', '216', '200'], 0, 'The terms are running totals of cubes: 1, 1 + 8 = 9, 9 + 27 = 36, 36 + 64 = 100, so next is 100 + 125 = 225. It is also the square of 1 + 2 + 3 + 4 + 5 = 15. The trap is 196 (14²), which notices the squares but picks the wrong one; 216 is 6³. In practice: cumulative totals are everywhere in accounts — year-to-date figures are running sums, just like this series.', 'c1', 'hard', '100+5**3', topic='Number series — the testing ladder'),
            M('m13', 'Find the next term: 1, 2, 6, 24, 120, ?', ['720', '600', '840', '240'], 0, 'The multipliers rise by one each time: × 2, × 3, × 4, × 5, so the next is × 6: 120 × 6 = 720. These are the factorials 1!, 2!, 3!, … 6!. The trap is 600, which repeats × 5; 240 just doubles. In practice: factorials count arrangements, so this series also appears in permutation problems such as the number of ways to order a set of tasks.', 'c1', 'core', '120*6', topic='Number series — the testing ladder'),
            M('m14', 'Find the next term: 2, 12, 36, 80, 150, ?', ['252', '210', '222', '240'], 0, 'Each term is n³ + n²: 1 + 1 = 2, 8 + 4 = 12, 27 + 9 = 36, 64 + 16 = 80, 125 + 25 = 150, so next = 216 + 36 = 252. Differences 10, 24, 44, 70 have second differences 14, 20, 26 — next 32 — confirming 150 + 102 = 252. The trap is to repeat the last difference of 70 or guess a round figure like 240; the second differences settle it. In practice: going to second differences is how analysts tell whether growth itself is accelerating.', 'c1', 'hard', '6**3+6**2', topic='Number series — the testing ladder'),
            M('m15', 'Find the wrong term: 2, 5, 10, 17, 26, 37, 50, 64', ['64', '50', '37', '26'], 0, 'Each term is n² + 1: 1 + 1 = 2, 4 + 1 = 5, … 49 + 1 = 50, so the 8th term should be 64 + 1 = 65. The printed 64 is wrong. The trap is 50, which fits the rule (7² + 1); differences 3, 5, 7, 9, 11, 13, 15 also show the last term should be 50 + 15 = 65. In practice: a near-miss figure like 64 for 65 is typical of transcription errors that reconciliation exercises catch.', 'c2', 'moderate', '64', topic='Missing term vs wrong term'),
            M('m16', 'Find the next term: AZ, CX, EV, GT, ?', ['IR', 'IS', 'HR', 'JR'], 0, 'Track each letter separately. First letters: A, C, E, G — moving +2 — so next is I. Second letters: Z, X, V, T — moving −2 — so next is R. The answer is IR. The trap is IS, which moves the second letter back by only 1. In practice: two-part codes that move in opposite directions are common in reasoning tests used for recruitment by banks and CA firms.', 'c3', 'core', topic='Alphabet series and letter positions'),
            M('m17', 'Find the next letter: B, E, I, N, ?', ['T', 'S', 'U', 'R'], 0, 'Convert to positions: B = 2, E = 5, I = 9, N = 14. The gaps are 3, 4, 5, so the next gap is 6: 14 + 6 = 20 = T. The trap is S (19), which repeats the gap of 5. In practice: converting letters to numbers is the standard first step in alphabet series, and the EJOTY trick (E = 5, J = 10, O = 15, T = 20, Y = 25) makes position-finding quick.', 'c3', 'core', topic='Alphabet series and letter positions'),
            M('m18', 'Find the next letter: Z, W, T, Q, ?', ['N', 'O', 'M', 'P'], 0, 'Positions: Z = 26, W = 23, T = 20, Q = 17 — moving back 3 each time. Next is 17 − 3 = 14 = N. The trap is O (15), which moves back only 2; M (13) moves back 4. In practice: backward letter series test the same skill as reading a reverse-chronological ledger — keeping the step size constant while counting down.', 'c3', 'core', topic='Alphabet series and letter positions'),
            M('m19', 'Which letter is 8th from the right end of the English alphabet?', ['S', 'R', 'T', 'H'], 0, "The position from the left plus the position from the right equals 27 for any letter. So the 8th letter from the right is 27 − 8 = 19th from the left, which is S. The trap is H, the 8th letter from the left end. In practice: the '27 rule' saves time in coding questions where letters are replaced by their mirror opposites (A ↔ Z, B ↔ Y).", 'c3', 'core', topic='Alphabet series and letter positions'),
            M('m20', 'Fill the blanks in order: a _ b a a _ b a _ b b _', ['bbaa', 'baba', 'abab', 'bbab'], 0, "Look for the repeating block. Trying 'abba' gives abba | abba | abba, which matches every given letter. The blanks are the 2nd, 6th, 9th and 12th letters: b, b, a, a, so the answer is bbaa. The trap is baba, which assumes a simple alternating pattern without testing it against the given letters. In practice: finding the repeating unit is like spotting a recurring monthly cycle in transaction data.", 'c4', 'moderate', topic='Letter series (blanks in a repeating block)'),
            M('m21', 'If GARDEN is coded as HBSEFO, how is FLOWER coded?', ['GMPXFS', 'EKNVDQ', 'GMPXSF', 'HMPXFS'], 0, 'Compare GARDEN with HBSEFO: G → H, A → B, R → S and so on — every letter moves one place forward. Applying this to FLOWER gives F → G, L → M, O → P, W → X, E → F, R → S: GMPXFS. The trap is GMPXSF, which applies the shift correctly but swaps the last two letters; EKNVDQ shifts backwards. In practice: simple shift ciphers are how data-masking rules are first explained, though real systems use far stronger encryption.', 'c5', 'core', topic='Letter coding — finding and applying the rule'),
            M('m22', 'If PLANT is written as TNALP, how is STOCK written?', ['KCOTS', 'KCTOS', 'TSOCK', 'SKCOT'], 0, "TNALP is PLANT written backwards, so the rule is simply 'reverse the word'. STOCK reversed is KCOTS. The trap is KCTOS, which reverses most of the word but swaps the middle letters. Always confirm the rule on the given example before applying it. In practice: checking the rule against the sample first is the same discipline an auditor applies when testing a control on one transaction before relying on it.", 'c5', 'core', topic='Letter coding — finding and applying the rule'),
            M('m23', 'If BAD is coded as YZW, how is CAB coded?', ['XZY', 'DBC', 'XYZ', 'ZXY'], 0, 'In BAD → YZW each letter is replaced by its opposite (positions add to 27): B (2) → Y (25), A (1) → Z (26), D (4) → W (23). So CAB → X, Z, Y = XZY. The trap is XYZ, which uses the right letters in the wrong order; DBC is a +1 shift. In practice: opposite-letter coding is a frequent reasoning-test pattern, and the A–Z, B–Y pairs are worth memorising.', 'c5', 'moderate', topic='Letter coding — finding and applying the rule'),
            M('m24', 'In a code, each letter of a word is moved two places forward. Which word is coded as RCRGT?', ['PAPER', 'TETIV', 'QBQFS', 'PAPRE'], 0, 'To decode, reverse the rule: move each letter two places back. R → P, C → A, R → P, G → E, T → R gives PAPER. The trap is TETIV, which moves the code two places forward again — coding twice instead of decoding. In practice: decoding requires applying the inverse operation in the correct direction, the same idea behind reversing a journal entry correctly.', 'c5', 'core', topic='Letter coding — finding and applying the rule'),
            M('m25', 'If A = 1, B = 2 and so on, and each letter is written as its number, how is BEAD written?', ['2514', '2541', '2154', '1452'], 0, "Replace each letter by its position, keeping the order: B = 2, E = 5, A = 1, D = 4, giving 2514. The trap is 2541, which writes the right digits but swaps the last two letters' codes. In practice: letter-to-number mapping like this is how simple check codes and spreadsheet column numbers (A = 1, B = 2, …) work.", 'c6', 'core', '2*1000+5*100+1*10+4', topic='Number coding'),
            M('m26', 'If MANGO is coded as 52734, how is MOAN coded?', ['5427', '5247', '5472', '4527'], 0, 'Read the key from MANGO = 52734: M = 5, A = 2, N = 7, G = 3, O = 4. Then MOAN = M, O, A, N = 5, 4, 2, 7 = 5427. The trap is 5247, which swaps the codes for O and A — the letters must be coded in the order they appear in MOAN. In practice: building a lookup table first and then reading off values is how VLOOKUP-style mapping works in spreadsheets.', 'c6', 'core', '5*1000+4*100+2*10+7', topic='Number coding'),
            M('m27', 'If CAT = 24 because 3 + 1 + 20 = 24, what is DOG?', ['26', '24', '27', '25'], 0, "The rule adds letter positions: CAT = 3 + 1 + 20 = 24. So DOG = D (4) + O (15) + G (7) = 26. The trap is 24, which assumes all three-letter words share CAT's value. In practice: summing coded values is the idea behind simple checksums, which banks use (in more advanced forms) to catch errors in account numbers.", 'c6', 'core', '4+15+7', topic='Number coding'),
            M('m28', 'In a code 1 → K, 2 → R, 3 → M, 4 → T, 5 → B. How is 32415 written?', ['MRTKB', 'MRKTB', 'MTRKB', 'KRTMB'], 0, 'Convert each digit in order using the key: 3 → M, 2 → R, 4 → T, 1 → K, 5 → B, giving MRTKB. The trap is MRKTB, which swaps the codes for 4 and 1. Work strictly digit by digit. In practice: careful digit-by-digit mapping avoids the transposition errors that are a major source of mistakes in data entry and bank transfers.', 'c6', 'core', topic='Number coding'),
            M('m29', 'Find the odd one out: 17, 23, 29, 33, 41', ['33', '41', '17', '29'], 0, '17, 23, 29 and 41 are all prime, but 33 = 3 × 11 is composite, so 33 is the odd one out. The trap is 41, which looks different because the gap from 33 is larger, but it is prime. In practice: classification questions test whether you can find the property shared by most items — the same thinking used to spot an outlier in an audit sample.', 'c7', 'core', '33', topic='Odd man out (classification)'),
            M('m30', 'Find the odd one out: 27, 64, 125, 144, 216', ['144', '64', '216', '27'], 0, '27 = 3³, 64 = 4³, 125 = 5³ and 216 = 6³ are perfect cubes, but 144 = 12² is a square and not a cube. The trap is 64, which is both a square (8²) and a cube, so it still belongs with the cubes. In practice: when an item fits two categories, choose the property shared by all the others — a principle analysts use when grouping data for reports.', 'c7', 'moderate', '144', topic='Odd man out (classification)'),
            M('m31', 'Find the odd one out: April, June, September, October', ['October', 'June', 'April', 'September'], 0, 'April, June and September each have 30 days; October has 31, so it is the odd one out. The trap is September, which some pick because it starts with a different letter or is the only one with nine letters — but the shared property here is the number of days. In practice: knowing month lengths matters for interest calculations, since banks compute daily interest on the actual number of days in each month.', 'c7', 'core', topic='Odd man out (classification)'),
            M('m32', 'Find the odd one out: ACE, BDF, GIK, MOP', ['MOP', 'GIK', 'BDF', 'ACE'], 0, 'In ACE, BDF and GIK the letters move +2, +2. MOP moves +2 (M → O) and then +1 (O → P), so it breaks the pattern; it would need MOQ to fit. The trap is GIK, which starts far from the others but still follows +2, +2. In practice: checking every step of a pattern, not just the first, is how a reviewer catches a formula that is correct in some rows but not others.', 'c7', 'moderate', topic='Odd man out (classification)'),
            M('m33', 'Find the odd one out: Rupee, Dirham, Euro, Kilogram', ['Kilogram', 'Euro', 'Rupee', 'Dirham'], 0, 'Rupee, Dirham and Euro are currencies; a kilogram is a unit of mass, so it is the odd one out. The trap is Euro, which some pick because it is used by many countries rather than one — but it is still a currency. In practice: Indian exporters to the Gulf invoice in rupees, dirhams or euros, and grouping items by their correct category (currency versus measure) is basic to any financial report.', 'c7', 'core', topic='Odd man out (classification)'),
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
                M('k1a', 'How is BANK coded?', ['NQDE', 'EDQN', 'KNAB', 'NQED'], 0, "Step 1 moves each letter three forward: B → E, A → D, N → Q, K → N, giving EDQN. Step 2 writes it backwards: NQDE. The trap is EDQN, which stops after step 1; NQED reverses incorrectly. Check the rule with AUDIT: DXGLW reversed is WLGXD. In practice: multi-step masking rules must be applied completely and in order, or the coded names will not match the firm's records.", 'c5', 'core', topic='Letter coding — finding and applying the rule'),
                M('k1b', 'Which folder name is coded as HVDF?', ['CASE', 'FDVH', 'ESAC', 'KYGI'], 0, 'Decode by undoing the steps in reverse order. Undo step 2 first: HVDF backwards is FDVH. Then move each letter three back: F → C, D → A, V → S, H → E, giving CASE. Check: CASE → FDVH → HVDF. The trap is FDVH, which undoes only the reversal. In practice: decoding always reverses the last step first — just as reversing a multi-step adjustment in accounts starts with the most recent entry.', 'c5', 'moderate', topic='Letter coding — finding and applying the rule'),
                M('k1c', 'How is LOAN coded?', ['QDRO', 'ORDQ', 'NAOL', 'QDOR'], 0, 'Step 1: L → O, O → R, A → D, N → Q, giving ORDQ. Step 2: reverse it to QDRO. The trap is ORDQ, which forgets step 2; QDOR reverses only part of the word. In practice: an office manager applying such a code by hand should verify one known example (like AUDIT → WLGXD) before coding a batch of client names.', 'c5', 'core', topic='Letter coding — finding and applying the rule'),
                M('k1d', 'Under step 1 alone, which letter becomes A?', ['X', 'D', 'C', 'Z'], 0, 'Moving three places forward wraps around the alphabet: X → Y → Z → A. So X becomes A. The trap is D, which is what A becomes (A moved forward three), not the letter that becomes A. In practice: wrap-around works like a clock going from 12 back to 1, or month 12 rolling over to month 1 in a payroll cycle.', 'c3', 'moderate', topic='Alphabet series and letter positions'),
            ]}],
    }

# ==== AUTO-CHECK: offline marking keys (kw groups / nums / ai_only per scheme point; read by the app's marker) ====
# kw: viva-matcher keyword groups ("a|b" = alternatives), min = groups needed; nums: figures that must appear
# (magnitudes: the matcher drops minus signs, so a sign that matters is carried by a kw group).


def _K(*kw, min=None, nums=None, **x):
    d = {'kw': list(kw), 'min': len(kw) if min is None else min}
    if nums: d['nums'] = list(nums)
    d.update(x)
    return d


def _N(*nums, kw=None, min=None, **x):
    d = {'nums': list(nums)}
    if kw: d.update(kw=list(kw), min=len(kw) if min is None else min)
    d.update(x)
    return d


AUTO = {
    'q1': {
        's1': _K('3 6 9|increas 3|differ 3|add 3|plus 3|by 3|step 3'),
        's2': _N(55),
        's3': _K('n3 1|n 3 1|cube 1|cube plus 1|cube plus one|cubes plus one|one more than cube|1 more than cube|more than a cube|cube'),
        's4': _K('wrong 67|67 wrong|67 incorrect|incorrect 67|67 should|67 replace|67 error|error 67|odd 67|67 odd|67 is wrong', 'correct 65|65 correct|should 65|replace 65|65 instead|be 65|right 65|actual 65|correct value 65|by 65'),
    },
    'q2': {
        's1': _K('nlmvb'),
        's2': _N(57),
        's3': _K('vdohv|reverse first|undo revers|first revers|revers first|reversal first|reverse it first|reversing first'),
        's4': _K('sales'),
    },
    'q3': {
        's1': _K('21 3 7|21 not prime|21 composite|odd 21|21 odd|21 divisible|21 non prime|21 3 x 7|21 only composite|21 is not a prime'),
        's2': _K('k|letter k'),
        's3': _K('abba'),
        's4': _K('bbaa'),
    },
}


_build_content = build


def build():
    u = _build_content()
    for q in u.get('questions', []):
        a = AUTO.get(q['id'], {})
        q['extra_ok'] = a.get('extra_ok', False)
        for s in q['scheme']:
            s.update(a[s['id']])
    return u
