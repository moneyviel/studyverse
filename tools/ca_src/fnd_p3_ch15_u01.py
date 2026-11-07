"""CA Foundation · Paper 3 Quantitative Aptitude · Part C Statistics · Chapter 15 Probability.
Original explanations, data and questions (structure and scope follow the ICAI study material). Every figure is computed below;
fractions are computed exactly with fractions.Fraction and asserted."""
from fractions import Fraction as F
from itertools import product
from math import comb
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M as CM

UID = 'fnd-p3-ch15-u01'


def ev(expr): return eval(expr, {'__builtins__': {}}, {'round': round, 'min': min, 'max': max, 'abs': abs})


class Checks(Checks):
    """Records the check as lib.Checks does (value stored to 2 decimals), but returns the value to 4 decimals for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = round(ev(expr), 4)
        return int(v) if v == int(v) else v


def fm(v, unit=''):
    v = round(v, 4)
    s = inr(int(v)) if v == int(v) else f'{v:.4f}'.rstrip('0').rstrip('.')
    return s + (' ' + unit if unit else '')


def fr(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def mq(mid, q, opts, explain, concept, diff='core'):
    return {'id': mid, 'q': q, 'options': opts, 'answer': 0, 'explain': explain, 'concept': concept, 'difficulty': diff}


def nq(mid, q, check, wrong, explain, concept, diff='core', unit=''):
    v = ev(check)
    opts = [fm(v, unit)] + [fm(w, unit) for w in wrong]
    assert len(set(opts)) == 4 and all(abs(w - v) > 0.006 for w in wrong), (mid, opts)
    return {'id': mid, 'q': q, 'options': opts, 'answer': 0, 'check': check, 'explain': explain.replace('@A', fm(v, unit)), 'concept': concept, 'difficulty': diff}


def fq(mid, q, ans, wrong, explain, concept, diff='core'):
    """MCQ whose answer is an exact fraction (computed by the caller with Fraction)."""
    opts = [fr(ans)] + [fr(w) for w in wrong]
    assert len(set(opts)) == 4 and all(F(w) != F(ans) for w in wrong), (mid, opts)
    return {'id': mid, 'q': q, 'options': opts, 'answer': 0, 'explain': explain.replace('@A', fr(ans)), 'concept': concept, 'difficulty': diff}


DICE = list(product(range(1, 7), repeat=2))
def pd(cond): return F(sum(1 for a, b in DICE if cond(a, b)), 36)


def build():
    # sanity checks of the dice helper
    assert pd(lambda a, b: a + b == 7) == F(1, 6)

    # ---------------- Illustration 1: classical probability ----------------
    c1 = Checks()
    p8 = pd(lambda a, b: a + b == 8); p10 = pd(lambda a, b: a + b >= 10); pdb = pd(lambda a, b: a == b)
    c1.add('5/36', 'P(sum 8)'); c1.add('6/36', 'P(sum at least 10)'); c1.add('6/36', 'P(doublet)')
    pkh = F(4 + 13 - 1, 52); c1.add('(4+13-1)/52', 'P(king or heart)')
    assert p8 == F(5, 36) and p10 == F(1, 6) and pdb == F(1, 6) and pkh == F(4, 13)
    p2h = F(comb(3, 2), 8); c1.add('3/8', 'P(exactly two heads in three tosses)')
    pcom = F(comb(4, 2) * comb(6, 1), comb(10, 3)); c1.add('(6*6)/120', 'P(2 red, 1 black from 4 red 6 black, 3 drawn)')
    assert pcom == F(3, 10)
    c1.add('5/(5+31)', 'odds 5:31 to probability')

    # ---------------- Illustration 2: addition, conditional, independence ----------------
    c2 = Checks()
    pu = c2.add('0.5+0.4-0.2', 'P(A or B)')
    pab = c2.add('0.2/0.4', 'P(A|B)')
    pn = c2.add('1-0.7', 'P(neither)')
    pao = c2.add('0.5-0.2', 'P(A only)')
    c2.add('0.5*0.4', 'P(A)P(B) equals P(A and B), so independent')

    # ---------------- Illustration 3: compound probability ----------------
    c3 = Checks()
    atl = c3.add('1-(1-0.6)*(1-0.5)*(1-0.4)', 'P(at least one detects)')
    allx = c3.add('0.6*0.5*0.4', 'P(all three detect)')
    ex1 = c3.add('0.6*0.5*0.6+0.4*0.5*0.6+0.4*0.5*0.4', 'P(exactly one detects)')
    prr = F(3, 8) * F(2, 7); c3.add('3/8*2/7', 'both red without replacement')
    prw = F(3, 8) * F(3, 8); c3.add('3/8*3/8', 'both red with replacement')
    assert prr == F(3, 28)

    # ---------------- Illustration 4: expectation ----------------
    c4 = Checks()
    xs, ps = [0, 1, 2, 3, 4], [0.1, 0.2, 0.4, 0.2, 0.1]
    Ex = c4.add('0*0.1+1*0.2+2*0.4+3*0.2+4*0.1', 'E(X)')
    Ex2 = c4.add('0*0.1+1*0.2+4*0.4+9*0.2+16*0.1', 'E(X^2)')
    Vx = c4.add('5.2-2**2', 'V(X)')
    Ey = c4.add('3*2-4', 'E(3X - 4)'); Vy = c4.add('9*1.2', 'V(3X - 4)')
    rows4 = [[str(x), fm(pp), fm(x * pp), fm(x * x * pp)] for x, pp in zip(xs, ps)] + [['Total', '1', fm(Ex), fm(Ex2)]]
    t4 = table(['x (orders per hour)', 'P(x)', 'x·P(x)', 'x²·P(x)'], rows4, num=[1, 2, 3], total=True)
    eg = c4.add('500*1/4+200*3/4-250', 'expected gain of the game (net of fee)')

    # ---------------- Question 1 ----------------
    q1c = Checks()
    qa = pd(lambda a, b: a + b in (5, 9)); qb = pd(lambda a, b: a * b == 12); qc = pd(lambda a, b: a != b)
    q1c.add('(4+4)/36', 'P(sum 5 or 9)'); q1c.add('4/36', 'P(product 12)'); q1c.add('30/36', 'P(different faces)')
    assert qa == F(2, 9) and qb == F(1, 9) and qc == F(5, 6)
    qd = F(comb(4, 2), comb(52, 2)); q1c.add('6/1326', 'P(two aces)')
    assert qd == F(1, 221)

    # ---------------- Question 2 ----------------
    q2c = Checks()
    q2u = q2c.add('0.45+0.35-0.15', 'P(A or B)')
    q2ab = q2c.add('round(0.15/0.35,4)', 'P(A|B)')
    q2ba = q2c.add('round(0.15/0.45,4)', 'P(B|A)')
    q2c.add('round(0.45*0.35,4)', 'P(A)P(B)')
    q2n = q2c.add('1-0.65', 'P(neither)')

    # ---------------- Question 3 ----------------
    q3c = Checks()
    k = q3c.add('1/(1+2+3+4)', 'k')
    q3e = q3c.add('1*0.1+2*0.2+3*0.3+4*0.4', 'E(X)')
    q3e2 = q3c.add('1*0.1+4*0.2+9*0.3+16*0.4', 'E(X^2)')
    q3v = q3c.add('10-3**2', 'V(X)')
    q3c.add('2*3+5', 'E(2X+5)'); q3c.add('4*1', 'V(2X+5)')

    # ---------------- Case ----------------
    kc = Checks()
    kc.add('0.6*0.02', 'P(salaried and default)')
    pdft = kc.add('0.6*0.02+0.4*0.05', 'P(default)')
    kc.add('1000*0.032*500000', 'expected number x exposure')
    cases = [{
        'id': 'k1', 'title': 'Default risk in a small loan book', 'difficulty': 'hard',
        'case': ('A cooperative bank has 1,000 personal loans of ₹5,00,000 each. 60% of borrowers are salaried and 40% self-employed. Past data show that 2% of salaried borrowers and 5% of self-employed borrowers default. '
                 'A borrower is chosen at random from the book. Assume that a defaulted loan is fully lost.'),
        'mcqs': [
            CM('k1a', 'What is the probability that the borrower is salaried and defaults?', ['0.012', '0.02', '0.6', '0.032'], 0,
               'Multiplication theorem: P(S and D) = P(S) × P(D|S) = 0.6 × 0.02 = 0.012.', 'moderate', '0.6*0.02'),
            CM('k1b', 'What is the probability that the borrower defaults?', ['0.032', '0.07', '0.05', '0.02'], 0,
               f'Default happens either with a salaried or with a self-employed borrower (mutually exclusive): 0.6 × 0.02 + 0.4 × 0.05 = 0.012 + 0.020 = {fm(pdft)}. 0.07 simply adds the two rates; 0.05 is the self-employed rate alone.', 'hard', '0.6*0.02+0.4*0.05'),
            CM('k1c', 'What are the odds against a randomly chosen borrower defaulting?', ['121 : 4', '4 : 121', '968 : 1,000', '32 : 1,000'], 0,
               'P(D) = 0.032 = 4/125, so P(not D) = 121/125. Odds against = 121 : 4.', 'hard'),
            CM('k1d', 'What is the expected loss on the whole book?', ['₹1,60,00,000', '₹1,00,00,000', '₹3,50,00,000', '₹16,00,000'], 0,
               'Expected number of defaults = 1,000 × 0.032 = 32; expected loss = 32 × ₹5,00,000 = ₹1.6 crore.', 'moderate', '1000*0.032*500000'),
        ]}]

    viva = [
        V('v1', 'State the classical definition of probability and its limitations.',
          'When an experiment can end in n equally likely, mutually exclusive and exhaustive ways, and m of those ways favour the event A, the probability of A is m divided by n. Its limitations are that it needs equally likely outcomes, it cannot be used when the total number of outcomes is infinite, and it applies only to simple situations like coins, dice and cards where no prior knowledge is needed.',
          [P('p1', 'P(A) = favourable outcomes ÷ total outcomes', 4, 'favourable|favorable', 'total|exhaustive|all possible|number of outcome', min=2),
           P('p2', 'Outcomes must be mutually exclusive, exhaustive and equally likely', 2, 'equally likely|equiprobable|equi probable|equally probable'),
           P('p3', 'Limitations: needs equally likely outcomes; fails for infinite outcomes; limited field', 4, 'infinite|countless|unlimited|cannot count|cannot handle infinite|cannot deal with infinite|cannot be used infinite|cannot apply infinite|not for infinite|not when infinite|not work infinite|not applicable infinite|not valid infinite|not equally likely or infinite|not equally likely infinite', 'limited|coin|dice|card|equally likely|not equally likely|only|simple', min=2)], 'c2'),
        V('v2', 'What is the difference between mutually exclusive events and independent events?',
          'Mutually exclusive events cannot occur together; the occurrence of one rules out the other, so the probability of A and B together is zero. Independent events can occur together, and the occurrence of one does not change the probability of the other, so the probability of A and B is P of A times P of B. Two events with non-zero probabilities cannot be both mutually exclusive and independent.',
          [P('p1', 'Mutually exclusive: cannot occur together; P(AandB) = 0', 4, ALT('mutually exclusive {x}', x=('cannot occur together', 'cannot happen together', 'not occur together', 'not happen together', 'cannot occur simultaneously', 'not occur simultaneously', 'cannot both', 'no common', 'zero', 'rules out', 'prevents', 'excludes', 'never occur together', 'never happen together', 'cannot happen at the same time', 'cannot occur at the same time'))),
           P('p2', 'Independent: one does not affect the probability of the other; P(AandB) = P(A)P(B)', 4, ALT('independent {x}', x=('does not affect', 'not affect', 'no effect', 'does not change', 'not change', 'not influence', 'does not influence', 'unaffected', 'product', 'multiply', 'times', 'not depend', 'does not depend', 'can occur together', 'can happen together'))),
           P('p3', 'They are different ideas (cannot be both, if probabilities are non-zero)', 2, 'cannot be both|not both|different|not the same|not same|distinct|differ', min=1)], 'c3'),
        V('v3', 'State the addition theorem of probability.',
          'For any two events A and B, the probability of A or B equals P of A plus P of B minus P of A and B. If A and B are mutually exclusive, the last term is zero, so the probability of A or B is simply P of A plus P of B.',
          [P('p1', 'P(A or B) = P(A) + P(B) − P(A and B)', 6, ALT('p a plus p b minus p a {a} b', 'p a p b minus p a {a} b', 'a plus b minus a {a} b', 'p a plus p b minus p a b', a=('and', 'intersection', 'intersect', 'both', 'n', ''))),
           P('p2', 'For mutually exclusive events: P(A or B) = P(A) + P(B)', 4, 'mutually exclusive|cannot occur together|disjoint', min=1)], 'c4'),
        V('v4', 'Define conditional probability and state the multiplication (compound) theorem.',
          'The conditional probability of B given A is the probability that B occurs when we know A has occurred; it equals P of A and B divided by P of A, provided P of A is not zero. The compound theorem says P of A and B equals P of A times P of B given A. If A and B are independent, P of B given A equals P of B, so P of A and B equals P of A times P of B.',
          [P('p1', 'P(B|A) = P(A and B)/P(A), given A has occurred', 4, ALT('p a {a} b {d} p a', 'p of a and b over p of a', 'p a b {d} p a', 'p b given a {e} p a {a} b', a=('and', 'intersection', 'both', 'intersect', 'n'), d=('divided by', 'by', 'over', 'upon'), e=('equals', 'is', 'equal to', '')), 'given|already occurred|has occurred|happened', min=2),
           P('p2', 'P(A and B) = P(A) × P(B|A)', 4, ALT('p a {x} p b given a', 'p a {x} p of b given a', 'p a into p b given a', 'p a p b given a', x=('times', 'multiplied by', 'into', 'x'))),
           P('p3', 'Independent events: P(A and B) = P(A) P(B)', 2, 'independent')], 'c5'),
        V('v5', 'What is the expected value of a random variable, and what are its main properties?',
          'The expected value, or mathematical expectation, is the sum of each value of the random variable multiplied by its probability: E of X equals sigma p x. Properties: the expectation of a constant is the constant; the expectation of a sum is the sum of the expectations; E of a plus b X equals a plus b times E of X; and for independent variables the expectation of the product is the product of the expectations. The variance is E of X squared minus the square of E of X.',
          [P('p1', 'E(X) = Σ p·x (sum of values × probabilities)', 4, 'sum|sigma|total|add', 'probabilit', 'value|x', min=3),
           P('p2', 'E(constant) = constant; E(X + Y) = E(X) + E(Y); E(a + bX) = a + bE(X)', 3, 'constant|sum of the expectation|sum of expectation|e x plus e y|a plus b', min=1),
           P('p3', 'E(XY) = E(X)E(Y) for independent variables', 1, 'independent|product'),
           P('p4', 'V(X) = E(X²) − [E(X)]²', 2, 'variance|e x square minus|square minus|minus square|e x2', min=1)], 'c7'),
        V('v6', 'What do odds in favour and odds against an event mean? If the odds in favour are 3 to 5, what is the probability?',
          'Odds in favour of an event are the ratio of favourable cases to unfavourable cases, and odds against are the ratio of unfavourable cases to favourable cases. If the odds in favour are 3 to 5, there are 3 favourable out of 8 cases, so the probability is 3 by 8, or 0.375.',
          [P('p1', 'Odds in favour = favourable : unfavourable', 4, ALT('{o} {f} {t} {u}', o=('in favour', 'in favor', 'favour', 'favor'), f=('favourable', 'favorable', 'success', 'happening'), t=('to', 'is to', 'ratio to', 'against', 'versus', 'by', ':', ''), u=('unfavourable', 'unfavorable', 'not favourable', 'failure', 'not happening', 'non favourable'))),
           P('p2', 'Odds against = unfavourable : favourable', 3, ALT('against {u} {t} {f}', u=('unfavourable', 'unfavorable', 'not favourable', 'failure', 'not happening', 'non favourable'), t=('to', 'is to', 'ratio to', 'versus', 'by', ''), f=('favourable', 'favorable', 'success', 'happening')), 'reverse|inverse|opposite|other way', min=1),
           P('p3', 'Probability = 3/8 = 0.375', 3, '3 by 8|3 8|0.375|3 out of 8|three eighth|3 over 8|3 upon 8|3 divided by 8')], 'c2'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch15', 'n': 1,
        'title': 'Probability',
        'outcomes': [
            'Describe random experiments, sample spaces and events — simple, compound, mutually exclusive, exhaustive, equally likely and complementary.',
            'Compute probabilities by the classical, statistical (relative frequency) and axiomatic approaches, and convert between odds and probability.',
            'Apply the addition theorems, conditional probability, the compound (multiplication) theorem and the test of independence.',
            'Build the probability distribution of a discrete random variable and find its expected value and variance, using the properties of expectation.',
        ],
        'meta': {'difficulty': 'hard', 'minutes': {'learn': 50, 'practice': 70}, 'prereq': ['fnd-p3-ch05-u01', 'fnd-p3-ch07-u01'],
                 'exam_tip': 'Probability carries several MCQs every attempt. The classic marks: dice (36 cases), cards (52), coins (2ⁿ), "at least one" = 1 − P(none), P(A or B) formula, conditional probability and E(X). Write the sample space size first — that alone removes most errors.'},
        'concepts': [
            {'id': 'c1', 'title': 'Random experiments, sample space and events',
             'body': ['A random experiment can be repeated under the same conditions; all its outcomes are known in advance but the actual outcome cannot be predicted (tossing a coin, drawing a card). The set of all outcomes is the sample space S; each outcome is a sample point. An event is any subset of S.',
                      'Simple (elementary) event: a single outcome. Compound (composite) event: made of two or more outcomes — "an even number on a die".',
                      'Mutually exclusive (incompatible) events: no two can occur together (head and tail on one toss); P(A and B) = 0. Exhaustive events: together they cover every possible outcome; P(A or B or …) = 1. Equally likely (equi-probable) events: no reason to expect one more than another.',
                      'Complementary event A′ (or Ā): "A does not occur". A and A′ are mutually exclusive and exhaustive, so P(A′) = 1 − P(A).',
                      'Counting reminders: n coins → 2ⁿ outcomes; two dice → 36; a pack → 52 cards (4 suits × 13; 26 red, 26 black; 12 face cards; 4 aces); selections use ⁿCᵣ.'],
             'analogy': 'The sample space is the full menu; an event is your order — one dish (simple) or a combo (compound).',
             'work': 'Risk registers list possible outcomes (events) of a project; making sure the list is exhaustive and the categories mutually exclusive is the same discipline.'},
            {'id': 'c2', 'title': 'Definitions of probability and odds',
             'body': ['Classical (a priori) definition — Bernoulli and Laplace: if an experiment has n mutually exclusive, exhaustive and equally likely outcomes and m are favourable to A, P(A) = m/n. Limitations: needs equally likely outcomes; fails when the number of outcomes is infinite; limited to coins, dice, cards and similar cases where no prior knowledge is required.',
                      'Statistical (empirical / relative frequency) definition: if A occurs f times in n trials, P(A) = limit of f/n as n becomes very large — provided the limit exists and is finite.',
                      'Set-theoretic form: P(A) = n(A)/n(S) for equally likely sample points. Axiomatic (modern) definition: P is a function on events with (i) P(A) ≥ 0, (ii) P(S) = 1, (iii) for mutually exclusive events, P(A₁ or A₂ or …) = P(A₁) + P(A₂) + …. Consequences: 0 ≤ P(A) ≤ 1, P(∅) = 0, P(A′) = 1 − P(A).',
                      'Odds in favour of A = m : (n − m) (favourable : unfavourable). Odds against A = (n − m) : m. If odds in favour are a : b, P(A) = a/(a + b).'],
             'analogy': 'Classical probability reads the rule book of the game; statistical probability watches the game played thousands of times.',
             'work': 'Insurance premiums rest on the relative-frequency definition — claim rates from past data. Credit-rating default probabilities are also empirical.'},
            {'id': 'c3', 'title': 'Mutually exclusive vs independent',
             'body': ['Mutually exclusive: A and B cannot happen together — P(A and B) = 0.',
                      'Independent: the occurrence of one does not change the probability of the other — P(B|A) = P(B), equivalently P(A and B) = P(A) × P(B). This product rule is the necessary and sufficient condition. For three events, all pairwise products and the triple product must hold.',
                      'If A and B are independent, so are (A, B′), (A′, B) and (A′, B′). Two events with non-zero probabilities cannot be both mutually exclusive and independent.'],
             'analogy': 'Mutually exclusive: two people who cannot sit on the same chair. Independent: two people in different cities flipping coins.',
             'work': 'Auditors relying on two controls assume they fail independently — if both depend on the same IT system, they are not independent and the combined assurance is overstated.'},
            {'id': 'c4', 'title': 'Addition theorems',
             'body': ['Theorem 1 (mutually exclusive): P(A or B) = P(A) + P(B). Theorem 2: for k mutually exclusive events, add all k probabilities.',
                      'Theorem 3 (any two events): P(A or B) = P(A) + P(B) − P(A and B). It is the general rule — use it unless you are sure the events are mutually exclusive.',
                      'Theorem 4 (three events): P(at least one of A, B, C) = S₁ − S₂ + S₃, where S₁ is the sum of the three single probabilities, S₂ the sum of the three pairwise joint probabilities [P(A and B) + P(B and C) + P(C and A)], and S₃ = P(all three together).',
                      'Useful forms: P(A only) = P(A) − P(A and B); P(neither) = 1 − P(A or B); expected frequency = N × probability.'],
             'blocks': [table(['Probability', 'Value'], [['P(A)', '0.5'], ['P(B)', '0.4'], ['P(A and B)', '0.2'], ['P(A or B)', fm(pu)], ['P(neither)', fm(pn)], ['P(A only)', fm(pao)]], title='One Venn diagram, many answers')],
             'analogy': 'Counting people who like tea or coffee: add both lists, then remove those you counted twice.',
             'work': 'If 30% of invoices lack a PO and 20% lack approval, and 8% lack both, then 42% have at least one control gap — the addition theorem in audit sampling.'},
            {'id': 'c5', 'title': 'Conditional probability and compound probability',
             'body': ['Conditional probability of B given A: P(B|A) = P(A and B)/P(A), P(A) > 0. It revises probability using the information that A has happened (e.g. drawing without replacement changes the composition).',
                      'Compound (multiplication) theorem: P(A and B) = P(A) × P(B|A) = P(B) × P(A|B). For three events: P(A, B, C together) = P(A) P(B|A) P(C|A and B).',
                      'For independent events: P(A and B) = P(A) P(B); P(A, B, C together) = P(A) P(B) P(C).',
                      '"At least one" of independent events: 1 − P(A′) P(B′) P(C′).'],
             'analogy': 'Conditional probability is weather forecasting after seeing dark clouds — the clouds (A) change the chance of rain (B).',
             'work': 'Probability that a customer pays on time given he paid late last quarter is a conditional probability that credit teams use for collection priorities.'},
            {'id': 'c6', 'title': 'Random variable and probability distribution',
             'body': ['A random (stochastic) variable assigns a real number to every sample point (number of heads in three tosses). Discrete: takes isolated values (heads, accidents, defects). Continuous: takes any value in an interval (height, weight).',
                      'Probability distribution of a discrete X: the list of values xᵢ with probabilities pᵢ, where every pᵢ ≥ 0 and Σpᵢ = 1 (probability mass function). For a continuous X, a density function f(x) ≥ 0 with total area 1 gives probabilities over intervals.'],
             'analogy': 'A frequency distribution describes what happened; a probability distribution describes what is expected to happen.',
             'work': 'Demand forecasts for inventory are often a probability distribution of daily demand rather than one number.'},
            {'id': 'c7', 'title': 'Expected value and variance',
             'body': ['Expected value (mathematical expectation, mean): E(X) = μ = Σpᵢxᵢ. E(X²) = Σpᵢxᵢ²; for any function, E[g(X)] = Σpᵢ g(xᵢ).',
                      'Variance: V(X) = σ² = E(X − μ)² = E(X²) − [E(X)]²; SD = √V(X).',
                      'Properties: E(k) = k; E(X + Y) = E(X) + E(Y); E(kX) = kE(X); E(XY) = E(X)E(Y) if X and Y are independent. For y = a + bX: E(y) = a + bE(X), V(y) = b²V(X), SD(y) = |b| SD(X).'],
             'blocks': [t4],
             'analogy': 'Expected value is the long-run average pay-out per play if a game is repeated many times.',
             'work': 'Expected credit loss, expected warranty cost and expected value of a contingent liability are all Σ probability × amount.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Dice, cards, coins and selections', 'difficulty': 'core', 'minutes': 12,
             'q': 'Find: (a) with two dice, P(sum = 8), P(sum ≥ 10) and P(doublet); (b) P(a king or a heart) from a pack of 52; (c) P(exactly two heads) in three tosses; (d) from a bag of 4 red and 6 black balls, three are drawn: P(2 red and 1 black); (e) the probability when odds in favour are 5 : 31.',
             'solution': [wn('(a) 36 outcomes', f'Sum 8: first die 2, 3, 4, 5 or 6 with the second die making up 8 — five cases → {fr(p8)}. Sum ≥ 10: 3 + 2 + 1 = 6 cases → {fr(p10)}. Doublets: 6 → {fr(pdb)}.'),
                          wn('(b)', f'Kings 4 + hearts 13 − king of hearts 1 = 16 → 16/52 = {fr(pkh)}.'),
                          wn('(c)', f'2³ = 8 outcomes; HHT, HTH, THH → {fr(p2h)}.'),
                          wn('(d)', f'⁴C₂ × ⁶C₁ / ¹⁰C₃ = 6 × 6/120 = {fr(pcom)}.'),
                          wn('(e)', '5/(5 + 31) = 5/36.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Addition theorem and a test of independence', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'P(A) = 0.5, P(B) = 0.4 and P(A and B) = 0.2. Find P(A or B), P(A|B), P(neither) and P(A only). Are A and B independent?',
             'solution': [wn('Working', f'P(A or B) = 0.5 + 0.4 − 0.2 = {fm(pu)}. P(A|B) = 0.2/0.4 = {fm(pab)}. P(neither) = 1 − 0.7 = {fm(pn)}. P(A only) = 0.5 − 0.2 = {fm(pao)}.'),
                          p('P(A) × P(B) = 0.5 × 0.4 = 0.2 = P(A and B), so A and B are independent (equivalently, P(A|B) = P(A) = 0.5). They are not mutually exclusive, since P(A and B) ≠ 0.')],
             'checks': c2},
            {'id': 'i3', 'title': '"At least one", "exactly one" and drawing without replacement', 'difficulty': 'moderate', 'minutes': 10,
             'q': '(a) Three reviewers independently spot a particular error with probabilities 0.6, 0.5 and 0.4. Find P(at least one spots it), P(all three) and P(exactly one). (b) A box has 3 defective and 5 good parts. Two are drawn one after another. P(both defective) without and with replacement?',
             'solution': [wn('(a)', f'At least one = 1 − 0.4 × 0.5 × 0.6 = {fm(atl)}. All three = 0.6 × 0.5 × 0.4 = {fm(allx)}. Exactly one = 0.6 × 0.5 × 0.6 + 0.4 × 0.5 × 0.6 + 0.4 × 0.5 × 0.4 = {fm(ex1)}.'),
                          wn('(b)', f'Without replacement: 3/8 × 2/7 = {fr(prr)} (conditional probability — the second draw depends on the first). With replacement: 3/8 × 3/8 = {fr(prw)} (independent draws).')],
             'checks': c3},
            {'id': 'i4', 'title': 'Expected value and variance of a distribution', 'difficulty': 'moderate', 'minutes': 10,
             'q': '(a) Orders per hour X at a help desk: 0, 1, 2, 3, 4 with probabilities 0.1, 0.2, 0.4, 0.2, 0.1. Find E(X), V(X), and the mean and variance of Y = 3X − 4. (b) A player pays ₹250 to draw one ball from a bag of 1 white and 3 red balls; he gets ₹500 for white and ₹200 for red. Expected net gain?',
             'solution': [t4, wn('(a)', f'E(X) = {fm(Ex)}; E(X²) = {fm(Ex2)}; V(X) = 5.2 − 4 = {fm(Vx)}. E(Y) = 3 × 2 − 4 = {fm(Ey)}; V(Y) = 9 × 1.2 = {fm(Vy)}.'),
                          wn('(b)', f'E(pay-out) = 500 × 1/4 + 200 × 3/4 = ₹275; net gain = 275 − 250 = ₹{fm(eg)} per game.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'How much assurance do two controls give?', 'role': 'IT audit associate',
             'situation': 'A payment is released only after a system check (fails to catch an error 10% of the time) and a manager review (misses 20% of errors). Management claims a 98% catch rate.',
             'steps': ['If the two controls work independently, P(both miss) = 0.1 × 0.2 = 0.02, so P(at least one catches) = 0.98.',
                       'Test independence: the manager reviews only payments the system has passed, using the same vendor master. If the vendor master is wrong, both miss together.',
                       'Where controls share a common cause, P(both miss) > 0.02 and the 98% claim is overstated.',
                       'Report the dependency and recommend an independent check of vendor-master changes.'],
             'takeaway': 'Multiplying failure probabilities is valid only for independent controls.',
             'checks': [{'expr': '1-0.1*0.2', 'value': 0.98, 'label': 'P(at least one control catches the error)'}]},
            {'id': 'j2', 'title': 'Expected value for a provision decision', 'role': 'Finance manager',
             'situation': 'A customer dispute: legal counsel estimates 50% chance of paying ₹0, 30% of paying ₹8 lakh and 20% of paying ₹20 lakh.',
             'steps': ['Expected outflow = 0.5 × 0 + 0.3 × 8 + 0.2 × 20 = ₹6.4 lakh.',
                       'Check the probabilities sum to 1 (a valid distribution).',
                       'Accounting standards may require the most likely outcome or the expected value depending on the situation — the statistics give the input, the standard decides the measure.'],
             'takeaway': 'Expected value = Σ probability × amount; it is the long-run average, not the amount that will actually be paid.',
             'checks': [{'expr': '0.5*0+0.3*8+0.2*20', 'value': 6.4, 'label': 'expected outflow (₹ lakh)'}]},
        ],
        'mcqs': [
            fq('m1', 'Two fair dice are thrown. The probability that the sum is 7 is:', pd(lambda a, b: a + b == 7), [F(7, 36), F(5, 36), F(1, 12)],
               'Six of the 36 outcomes give 7 — (6,1), (5,2), (4,3), (3,4), (2,5), (1,6) — so 6/36 = @A.', 'c2'),
            fq('m2', 'Two dice are thrown. The probability of getting a doublet is:', pdb, [F(1, 36), F(1, 3), F(5, 36)],
               'Doublets (1,1) … (6,6) are 6 of 36 → @A.', 'c2'),
            fq('m3', 'Two dice are thrown. The probability that the sum is at least 10 is:', p10, [F(1, 12), F(5, 36), F(1, 4)],
               'Sum 10: 3 cases, 11: 2, 12: 1 → 6/36 = @A.', 'c2', 'moderate'),
            fq('m4', 'One card is picked at random from a well-shuffled pack of 52. The probability that it is a king or a heart is:', pkh, [F(17, 52), F(1, 52), F(1, 4)],
               'P(K) + P(H) − P(K of hearts) = 4/52 + 13/52 − 1/52 = 16/52 = @A. 17/52 double-counts the king of hearts.', 'c4'),
            fq('m5', 'A card is drawn from a pack of 52. The probability that it is a face card (J, Q, K) is:', F(12, 52), [F(1, 13), F(1, 4), F(3, 52)],
               '12 face cards → 12/52 = @A.', 'c2'),
            fq('m6', 'Three fair coins are tossed. The probability of getting at least one head is:', F(7, 8), [F(1, 8), F(3, 8), F(1, 2)],
               'P(no head) = 1/8, so P(at least one) = 1 − 1/8 = @A.', 'c2'),
            fq('m7', 'Three coins are tossed. The probability of exactly two heads is:', p2h, [F(1, 4), F(1, 2), F(7, 8)],
               'HHT, HTH, THH: 3 of 8 outcomes → @A.', 'c2'),
            fq('m8', 'Two cards are drawn together from a pack of 52. The probability that both are aces is:', qd, [F(1, 169), F(1, 13), F(2, 13)],
               '⁴C₂/⁵²C₂ = 6/1,326 = @A. (1/169 = (1/13)² assumes replacement.)', 'c5', 'moderate'),
            fq('m9', 'A bag has 5 white and 4 black balls. Two balls are drawn at random together. The probability that both are white is:', F(comb(5, 2), comb(9, 2)), [F(25, 81), F(5, 9), F(4, 9)],
               '⁵C₂/⁹C₂ = 10/36 = @A. (25/81 would be with replacement.)', 'c5', 'moderate'),
            fq('m10', 'The odds in favour of an event are 4 : 7. The probability of the event is:', F(4, 11), [F(4, 7), F(7, 11), F(3, 11)],
               'P = 4/(4 + 7) = @A.', 'c2'),
            mq('m11', 'If P(A) = 0.35, the odds against A are:', ['13 : 7', '7 : 13', '35 : 100', '65 : 100'],
               'P(A′) = 0.65. Odds against = 0.65 : 0.35 = 13 : 7.', 'c2', 'moderate'),
            nq('m12', 'If P(A) = 0.42, then P(A′) is:', '1-0.42', [0.42, 0.5, 1.42],
               'P(A′) = 1 − P(A) = @A.', 'c1'),
            mq('m13', 'The classical definition of probability fails when:', ['The outcomes are not equally likely or are infinite in number', 'The outcomes are equally likely', 'A coin is tossed', 'The sample space is finite'],
               'It needs a finite number of equally likely outcomes.', 'c2'),
            mq('m14', 'The statistical (relative frequency) definition of probability is based on:', ['The limit of the relative frequency f/n as the number of trials becomes very large', 'Equally likely outcomes only', 'Personal belief', 'Three axioms only'],
               'P(A) = lim f/n as n → ∞, provided the limit exists and is finite.', 'c2'),
            mq('m15', 'Under the axiomatic approach, which of the following is NOT an axiom?', ['P(A′) = 1 − P(A)', 'P(A) ≥ 0', 'P(S) = 1', 'P(A₁ or A₂ or …) = ΣP(Aᵢ) for mutually exclusive events'],
               'P(A′) = 1 − P(A) is a consequence (theorem) derived from the axioms, not an axiom.', 'c2', 'hard'),
            mq('m16', 'Events A, B, C are mutually exclusive, exhaustive and equally likely. P(A) is:', ['1/3', '1', '0', '1/2'],
               'Exhaustive: P(A) + P(B) + P(C) = 1; equally likely: each = 1/3.', 'c1', 'moderate'),
            nq('m17', 'P(A) = 0.6, P(B) = 0.5, P(A and B) = 0.3. P(A or B) is:', '0.6+0.5-0.3', [1.1, 0.3, 0.9],
               '0.6 + 0.5 − 0.3 = @A. (1.1 forgets to subtract the overlap — a probability above 1 is impossible.)', 'c4'),
            nq('m18', 'P(A or B) = 0.8, P(A) = 0.5, P(B) = 0.45. P(A and B) is:', '0.5+0.45-0.8', [0.25, 0.35, 0.225],
               'P(A and B) = P(A) + P(B) − P(A or B) = 0.95 − 0.8 = @A.', 'c4', 'moderate'),
            nq('m19', 'A and B are mutually exclusive with P(A) = 0.25 and P(B) = 0.4. P(neither A nor B) is:', '1-(0.25+0.4)', [0.45, 0.65, 0.1],
               'P(A or B) = 0.65 (no overlap), so P(neither) = @A.', 'c4'),
            nq('m20', 'P(A) = 0.4, P(B) = 0.5 and A, B are independent. P(A or B) is:', '0.4+0.5-0.4*0.5', [0.9, 0.2, 0.5],
               'P(A and B) = 0.2, so P(A or B) = 0.9 − 0.2 = @A.', 'c3', 'moderate'),
            nq('m21', 'P(A and B) = 0.12 and P(B) = 0.3. P(A|B) is:', '0.12/0.3', [0.036, 0.12, 0.25],
               'P(A|B) = P(A and B)/P(B) = @A.', 'c5'),
            mq('m22', 'Two events A and B with P(A) = 0.3, P(B) = 0.4 and P(A and B) = 0.12 are:', ['Independent', 'Mutually exclusive', 'Exhaustive', 'Complementary'],
               'P(A)P(B) = 0.12 = P(A and B) → independent. They are not mutually exclusive (overlap ≠ 0).', 'c3', 'moderate'),
            mq('m23', 'If A and B are independent, which pair is NOT necessarily independent?', ['A and the event (A or B)', 'A and B′', 'A′ and B', 'A′ and B′'],
               'Independence carries over to complements; A and (A or B) are generally dependent.', 'c3', 'hard'),
            nq('m24', 'Three students solve a problem independently with probabilities 1/2, 1/3 and 1/4. The probability that the problem is solved is:', '1-(1/2)*(2/3)*(3/4)', [0.25, 1.0833, 0.0417],
               'P(none solves) = 1/2 × 2/3 × 3/4 = 1/4; P(solved) = 1 − 1/4 = @A. (1.0833 adds the probabilities; 0.0417 is all three solving it.)', 'c5', 'moderate'),
            fq('m25', 'A box has 4 defective and 6 good items. Two are drawn one by one without replacement. The probability that both are defective is:', F(4, 10) * F(3, 9), [F(4, 25), F(1, 5), F(6, 25)],
               '4/10 × 3/9 = @A. (4/25 = (4/10)² assumes replacement.)', 'c5', 'moderate'),
            mq('m26', 'Which of these can be a probability distribution of X taking values 1, 2, 3?', ['0.2, 0.5, 0.3', '0.4, 0.4, 0.4', '0.5, −0.1, 0.6', '0.3, 0.3, 0.3'],
               'Probabilities must be non-negative and add to 1. Only 0.2 + 0.5 + 0.3 = 1 qualifies.', 'c6'),
            nq('m27', 'X takes values 1, 2, 3 with probabilities 0.3, 0.5, 0.2. E(X) is:', '1*0.3+2*0.5+3*0.2', [2, 2.1, 1.5],
               'E(X) = 0.3 + 1.0 + 0.6 = @A.', 'c7'),
            nq('m28', 'For the distribution in the previous question (values 1, 2, 3 with probabilities 0.3, 0.5, 0.2), V(X) is:', '(1*0.3+4*0.5+9*0.2)-(1.9)**2', [4.1, 3.61, 0.7],
               'E(X²) = 0.3 + 2 + 1.8 = 4.1; V(X) = 4.1 − 1.9² = @A.', 'c7', 'hard'),
            nq('m29', 'E(X) = 5 and V(X) = 4. For Y = 2X − 3, the variance of Y is:', '2**2*4', [5, 13, 8],
               'V(a + bX) = b²V(X) = 4 × 4 = @A. The constant −3 does not affect variance.', 'c7', 'moderate'),
            nq('m30', 'An unbiased coin is tossed three times. The expected number of heads is:', '3*0.5', [3, 1, 0.5],
               'Values 0, 1, 2, 3 with probabilities 1/8, 3/8, 3/8, 1/8 → E = 12/8 = @A.', 'c7'),
            nq('m31', 'A trader expects a profit of ₹40,000 with probability 0.6 and a loss of ₹15,000 with probability 0.4. His expected profit is:', '40000*0.6-15000*0.4', [30000, 25000, 24000],
               '0.6 × 40,000 − 0.4 × 15,000 = @A.', 'c7', 'moderate', 'rupees'),
            fq('m32', 'One number is chosen at random from 1 to 30. The probability that it is a multiple of 3 or 5 is:', F(len([n for n in range(1, 31) if n % 3 == 0 or n % 5 == 0]), 30), [F(16, 30), F(1, 3), F(1, 2)],
               'Multiples of 3: 10; of 5: 6; of 15: 2. 10 + 6 − 2 = 14 → 14/30 = @A.', 'c4', 'moderate'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'core', 'pad': 'text',
             'q': 'Two fair dice are thrown. Find the probability that (a) the sum is 5 or 9, (b) the product of the numbers is 12, (c) the two faces are different. (d) Two cards are drawn together from a pack of 52; find the probability that both are aces.',
             'model': [wn('(a)', f'Sum 5: 4 cases; sum 9: 4 cases; mutually exclusive → 8/36 = {fr(qa)}.'),
                       wn('(b)', f'Product 12: (2,6), (3,4), (4,3), (6,2) → 4/36 = {fr(qb)}.'),
                       wn('(c)', f'Doublets 6, so different faces = 30/36 = {fr(qc)}.'),
                       wn('(d)', f'⁴C₂/⁵²C₂ = 6/1,326 = {fr(qd)}.')],
             'scheme': [{'id': 's1', 'pt': 'Sample space of 36 stated', 'm': 0.5, 'skill': 'concept'},
                        {'id': 's2', 'pt': '(a) 2/9 by addition of mutually exclusive events', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': '(b) 1/9', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': '(c) 5/6 via complement', 'm': 1, 'skill': 'application'},
                        {'id': 's5', 'pt': '(d) 1/221 using combinations', 'm': 1, 'skill': 'computation'}],
             'remarks': ['List favourable pairs explicitly — it prevents missing (4,3) after (3,4).'],
             'mistakes': ['Counting (3,4) and (4,3) as one outcome.', 'Using (4/52)² for drawing together.'],
             'tips': ['Ordered pairs for dice; combinations for cards drawn together.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'text',
             'q': 'In a firm, 45% of employees use the metro (A), 35% use the firm\'s bus (B) and 15% use both on different days. For an employee chosen at random find (a) P(A or B), (b) P(A|B), (c) P(B|A), (d) P(neither). (e) Are A and B independent?',
             'model': [wn('(a)', f'0.45 + 0.35 − 0.15 = {fm(q2u)}.'), wn('(b)', f'0.15/0.35 = {fm(q2ab)}.'), wn('(c)', f'0.15/0.45 = {fm(q2ba)}.'),
                       wn('(d)', f'1 − 0.65 = {fm(q2n)}.'), wn('(e)', 'P(A) × P(B) = 0.1575 ≠ 0.15 = P(A and B), so A and B are not independent (they are slightly negatively associated).')],
             'scheme': [{'id': 's1', 'pt': 'Addition theorem: 0.65', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'Conditional probabilities 0.4286 and 0.3333', 'm': 2, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'P(neither) 0.35', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'Independence tested with P(A)P(B)', 'm': 1, 'skill': 'analysis'}],
             'remarks': ['Some candidates confuse P(A|B) with P(B|A); write which event is known.'],
             'mistakes': ['Dividing by P(A) for P(A|B).', 'Calling the events mutually exclusive because they are not independent.'],
             'tips': ['Draw a quick Venn diagram: A only 0.30, both 0.15, B only 0.20, neither 0.35.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'A random variable X takes values 1, 2, 3, 4 with probabilities k, 2k, 3k, 4k. Find k, E(X), V(X), and the mean and variance of 2X + 5.',
             'model': [wn('k', f'k + 2k + 3k + 4k = 1 ⇒ k = {fm(k)}.'),
                       table(['x', 'P(x)', 'xP', 'x²P'], [['1', '0.1', '0.1', '0.1'], ['2', '0.2', '0.4', '0.8'], ['3', '0.3', '0.9', '2.7'], ['4', '0.4', '1.6', '6.4'], ['Total', '1', '3', '10']], num=[1, 2, 3], total=True),
                       wn('Moments', f'E(X) = {fm(q3e)}; E(X²) = {fm(q3e2)}; V(X) = 10 − 9 = {fm(q3v)}.'),
                       wn('2X + 5', 'E = 2 × 3 + 5 = 11; V = 2² × 1 = 4.')],
             'scheme': [{'id': 's1', 'pt': 'k = 0.1 from Σp = 1', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'E(X) = 3', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'E(X²) = 10 and V(X) = 1', 'm': 2, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'E(2X + 5) = 11, V(2X + 5) = 4', 'm': 2, 'skill': 'application'}],
             'remarks': ['Adding 5 to the variance is the most common error.'],
             'mistakes': ['V(2X + 5) = 2 × 1 + 5.', 'Forgetting to square E(X).'],
             'tips': ['A four-column table (x, P, xP, x²P) answers everything at once.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Events: simple/compound; mutually exclusive (P(AandB) = 0); exhaustive (union = S); equally likely; complementary.',
                        'Classical P = m/n (needs equally likely, finite outcomes); statistical = limit of f/n; axiomatic: P ≥ 0, P(S) = 1, additivity.',
                        'Odds in favour m : (n − m); P = a/(a + b).',
                        'P(A or B) = P(A) + P(B) − P(A and B); three-event version adds back P(AandBandC).',
                        'P(B|A) = P(A and B)/P(A); P(A and B) = P(A)P(B|A); independent ⇔ P(A and B) = P(A)P(B).',
                        'E(X) = Σpx; V(X) = E(X²) − [E(X)]²; E(a + bX) = a + bE(X); V(a + bX) = b²V(X).'],
            'remember': ['Two dice → 36; n coins → 2ⁿ; pack → 52.', 'At least one = 1 − P(none).', 'Drawing together = without replacement → combinations.', 'Mutually exclusive ≠ independent.'],
            'traps': ['A probability can never exceed 1 — check your addition.', 'P(A′) = 1 − P(A) is a theorem, not an axiom.', 'Constants do not change variance.', 'King of hearts is both a king and a heart — subtract it once.']},
        'quickref': [
            {'k': 'Classical', 'v': 'P(A) = favourable/total = n(A)/n(S)'},
            {'k': 'Odds', 'v': 'In favour m : (n − m); against (n − m) : m; P = a/(a + b) for odds a : b'},
            {'k': 'Addition (2 events)', 'v': 'P(A or B) = P(A) + P(B) − P(A and B)'},
            {'k': 'Addition (3 events)', 'v': 'ΣP(A) − ΣP(A and B) + P(A, B, C together)'},
            {'k': 'Conditional', 'v': 'P(B|A) = P(A and B)/P(A)'},
            {'k': 'Compound', 'v': 'P(A and B) = P(A) P(B|A); independent: P(A)P(B)'},
            {'k': 'At least one (independent)', 'v': '1 − P(A′)P(B′)P(C′)'},
            {'k': 'Expectation', 'v': 'E(X) = Σpx; V(X) = Σpx² − (Σpx)²'},
            {'k': 'Linear change', 'v': 'E(a + bX) = a + bE(X); V(a + bX) = b²V(X)'},
        ],
        'viva': viva, 'cases': cases,
    }
