"""CA Foundation · Paper 3 Quantitative Aptitude · Part C Statistics · Chapter 13 Unit 2 Sampling.
Original explanations, data and questions (structure and scope follow the ICAI study material). Every figure is computed below."""
from itertools import combinations, product
from math import comb, sqrt
from lib import *
from ca_viva import P, V, ALT
from ca_cases import M as _CM


def CM(*a, topic=None, **k):
    d = _CM(*a, **k); d['topic'] = topic
    return d

UID = 'fnd-p3-ch13-u02'


def ev(expr): return eval(expr, {'__builtins__': {}}, {'round': round, 'min': min, 'max': max, 'abs': abs})


class Checks(Checks):
    """Records the check as lib.Checks does (value stored to 2 decimals), but returns the value to 4 decimals for display."""
    def add(self, expr, label):
        super().add(expr, label)
        v = round(ev(expr), 4)
        return int(v) if v == int(v) else v


def fm(v, unit=''):
    v = round(v, 4)
    if v == int(v): s = inr(int(v))
    else: s = f'{round(v, 4):.4f}'.rstrip('0').rstrip('.') if abs(v) < 1 else f'{round(v, 2):.2f}'.rstrip('0').rstrip('.')
    return s + (' ' + unit if unit else '')


def mq(mid, q, opts, explain, concept, diff='core', topic=None):
    return {'topic': topic, 'id': mid, 'q': q, 'options': opts, 'answer': 0, 'explain': explain, 'concept': concept, 'difficulty': diff}


def nq(mid, q, check, wrong, explain, concept, diff='core', unit='', topic=None):
    v = ev(check)
    opts = [fm(v, unit)] + [fm(w, unit) for w in wrong]
    assert len(set(opts)) == 4 and all(abs(w - v) > 0.006 for w in wrong), (mid, opts)
    return {'topic': topic, 'id': mid, 'q': q, 'options': opts, 'answer': 0, 'check': check, 'explain': explain.replace('@A', fm(v, unit)), 'concept': concept, 'difficulty': diff}


def build():
    # ---------------- Illustration 1: sampling distribution WOR, verify SE with fpc ----------------
    c1 = Checks()
    pop = [3, 5, 9, 11]
    mu = c1.add('(3+5+9+11)/4', 'population mean')
    var = c1.add('((3-7)**2+(5-7)**2+(9-7)**2+(11-7)**2)/4', 'population variance')
    ns = c1.add('4*3/2', 'number of samples of size 2 without replacement = 4C2')
    smp = list(combinations(pop, 2)); assert len(smp) == comb(4, 2)
    rows1 = [[f'{a}, {b}', fm((a + b) / 2), fm((a + b) / 2 - mu), fm(((a + b) / 2 - mu) ** 2)] for a, b in smp]
    means = [(a + b) / 2 for a, b in smp]
    assert sum(means) / 6 == mu
    vbar = sum((m - mu) ** 2 for m in means) / 6
    rows1.append(['Total', fm(sum(means)), '0', fm(sum((m - mu) ** 2 for m in means))])
    t1 = table(['Sample', 'Sample mean', 'Deviation from 7', 'Squared deviation'], rows1, num=[1, 2, 3], total=True, title='All samples of size 2 drawn without replacement from 3, 5, 9, 11')
    c1.add('42/6', 'mean of the six sample means')
    c1.add('20/6', 'variance of sample mean by enumeration')
    c1.add('10/2*(4-2)/(4-1)', 'variance of sample mean by formula sigma^2/n x (N-n)/(N-1)')
    assert abs(vbar - 10 / 2 * 2 / 3) < 1e-9
    c1.add('10/2', 'variance of sample mean with replacement = sigma^2/n')
    c1.add('4**2', 'number of samples with replacement = N^n')

    # ---------------- Illustration 2: stratified allocation ----------------
    c2 = Checks()
    Ns, Ss, n2 = [1200, 800, 500], [10, 30, 18], 150
    NT = c2.add('1200+800+500', 'population size')
    prop = [c2.add(f'150*{x}/2500', f'proportional allocation stratum {i+1}') for i, x in enumerate(Ns)]
    NS = c2.add('1200*10+800*30+500*18', 'sum of N_i S_i')
    ney = [c2.add(f'150*{x}*{s}/45000', f'Neyman allocation stratum {i+1}') for i, (x, s) in enumerate(zip(Ns, Ss))]
    rows2 = [[f'Stratum {i+1}', inr(x), str(s), inr(x * s), fm(pa), fm(na)] for i, (x, s, pa, na) in enumerate(zip(Ns, Ss, prop, ney))]
    rows2.append(['Total', inr(NT), '', inr(NS), fm(sum(prop)), fm(sum(ney))])
    t2 = table(['Stratum', 'Size N(i)', 'SD S(i)', 'N(i) × S(i)', 'Proportional n(i)', 'Neyman n(i)'], rows2, num=[1, 3, 4, 5], total=True)

    # ---------------- Illustration 3: standard errors ----------------
    c3 = Checks()
    se_wr = c3.add('15/100**0.5', 'SE of mean, SRSWR (or infinite population)')
    fpc = c3.add('round(((2000-100)/(2000-1))**0.5,4)', 'finite population correction')
    se_wor = c3.add('round(15/100**0.5*((2000-100)/(2000-1))**0.5,4)', 'SE of mean, SRSWOR')
    se_p = c3.add('(0.2*0.8/400)**0.5', 'SE of proportion')

    # ---------------- Illustration 4: systematic sampling ----------------
    c4 = Checks()
    k4 = c4.add('600/40', 'sampling interval k = N/n')
    last = c4.add('7+39*15', 'serial number of the 40th unit with random start 7')
    kc = c4.add('50//8', 'interval for circular systematic sampling, N = 50, n = 8')
    c4.add('50-8*6', 'remainder p')

    # ---------------- Question 1: WR sampling distribution ----------------
    q1c = Checks()
    pop1 = [1, 4, 7]
    mu1 = q1c.add('(1+4+7)/3', 'population mean'); var1 = q1c.add('((1-4)**2+0+(7-4)**2)/3', 'population variance')
    q1c.add('3**2', 'number of samples WR')
    allm = [(a + b) / 2 for a, b in product(pop1, repeat=2)]
    dist = sorted(set(allm))
    rows_q1 = [[fm(m), f'{allm.count(m)}/9', fm(m * allm.count(m) / 9), f'{fm(m * m * allm.count(m))}/9'] for m in dist]
    e1 = sum(allm) / 9; e2 = sum(m * m for m in allm) / 9
    assert abs(e1 - 4) < 1e-9 and abs(e2 - 19) < 1e-9
    rows_q1.append(['Total', '1', fm(e1), '171/9 = 19'])
    tq1 = table(['Sample mean x̄', 'Probability', 'x̄ × P', 'x̄² × P'], rows_q1, num=[2], total=True, title='Sampling distribution of the mean (n = 2, with replacement)')
    q1c.add('171/9', 'E(xbar^2)')
    q1c.add('19-4**2', 'variance of xbar')
    q1c.add('6/2', 'sigma^2/n')

    # ---------------- Question 2: allocation ----------------
    q2c = Checks()
    N2s, S2s = [3000, 2000, 1000], [6, 12, 15]
    q2p = [q2c.add(f'240*{x}/6000', f'proportional stratum {i+1}') for i, x in enumerate(N2s)]
    q2ns = q2c.add('3000*6+2000*12+1000*15', 'sum N_i S_i')
    q2n = [q2c.add(f'240*{x}*{s}/57000', f'Neyman stratum {i+1} (unrounded)') for i, (x, s) in enumerate(zip(N2s, S2s))]
    q2r = [round(x) for x in q2n]
    assert sum(q2r) == 240
    rows_q2 = [[f'Stratum {i+1}', inr(x), str(s), inr(x * s), fm(a), fm(b), str(r)] for i, (x, s, a, b, r) in enumerate(zip(N2s, S2s, q2p, q2n, q2r))]
    rows_q2.append(['Total', '6,000', '', inr(q2ns), '240', fm(sum(q2n)), str(sum(q2r))])
    tq2 = table(['Stratum', 'N(i)', 'S(i)', 'N(i)S(i)', 'Proportional', 'Neyman (exact)', 'Neyman (rounded)'], rows_q2, num=[1, 3, 4, 6], total=True)

    # ---------------- Question 3: SE and required n ----------------
    q3c = Checks()
    q3a = q3c.add('20/64**0.5', 'SE with n = 64')
    q3b = q3c.add('round(20/64**0.5*((800-64)/(800-1))**0.5,2)', 'SE with fpc, N = 800')
    q3n = q3c.add('(20/2)**2', 'n needed for SE = 2')
    q3c.add('(20/1.25)**2', 'n needed for SE = 1.25')

    # ---------------- Case ----------------
    kc_ = Checks()
    kse = kc_.add('120/64**0.5', 'SE of mean life')
    cases = [{
        'id': 'k1', 'title': 'Testing the life of LED lamps', 'difficulty': 'moderate',
        'case': ('Prakash Lighting claims its LED lamps last at least 15,000 hours. A buyer\'s quality team tests 64 lamps picked at random from a large production lot until each lamp fails. '
                 'From past records the standard deviation of lamp life is 120 hours. One inspector, finding a carton hard to reach, replaced the selected lamp with one from the top of another carton.'),
        'mcqs': [
            CM('k1a', 'Why must the buyer use a sample rather than test every lamp?', ['Testing destroys the lamps (destructive testing)', 'A census is always less accurate', 'The population is too small', 'Sampling has no errors'], 0,
               "Finding a lamp's life means running it until it fails, so each tested lamp is destroyed. Testing every lamp would leave nothing to sell, so sampling is a necessity. 'A census is always less accurate' is the trap: a census avoids sampling error; the reason here is destruction. In practice: buyers of LED lamps, tyres or batteries in India rely on sample-based life tests for this reason.", 'core', topic='Sample survey vs complete enumeration (census)'),
            CM('k1b', 'What is the standard error of the sample mean life?', ['15', '120', '1.875', '7.5'], 0,
               'The lot is large, so treat it as infinite and ignore the correction: SE = σ/√n = 120 ÷ √64 = 120 ÷ 8 = 15 hours. The trap is 120, the population SD itself, not the standard error of the mean. In practice: a 15-hour SE tells the buyer how precisely the sample estimates the true average life against the claimed 15,000 hours.', 'moderate', '120/64**0.5', topic='Key terms, sampling distribution and standard error'),
            CM('k1c', 'If the team had tested 256 lamps instead, the standard error would:', ['Be halved', 'Be quartered', 'Double', 'Stay the same'], 0,
               "SE = σ/√n. Testing 256 lamps instead of 64 multiplies n by 4, so √n doubles and the SE halves, from 15 to 120 ÷ 16 = 7.5 hours. 'Be quartered' is the trap: it assumes SE falls in line with n rather than √n. In practice: quality teams weigh this gain in precision against destroying four times as many lamps.", 'moderate', topic='Key terms, sampling distribution and standard error'),
            CM('k1d', 'The inspector\'s replacement of the selected lamp introduces:', ['A sampling error arising from substitution', 'A non-sampling error that only a census can have', 'No error, as one lamp is as good as another', 'An error of the finite population correction'], 0,
               "Replacing a selected lamp with a convenient one breaks the random design. ICAI lists such substitution as a source of sampling error (bias). 'No error, as one lamp is as good as another' is the trap: lamps at the top of a carton may differ systematically. In practice: audit teams are trained never to replace a selected item for convenience, and to document any genuine replacement.", 'hard', topic='Errors in sample surveys'),
        ]}]

    viva = [
        V('v1', 'What are the basic principles of a sample survey?',
          'There are four principles. The law of statistical regularity says a reasonably large sample drawn at random will, on average, show the characteristics of the population. The principle of inertia of large numbers says results become more reliable as the sample size increases. The principle of optimisation says the design should give maximum efficiency for a given cost or a given efficiency at minimum cost. The principle of validity says the design must give valid estimates and tests, which only probability sampling ensures.',
          [P('p1', 'Law of statistical regularity (large random sample reflects the population)', 3, 'statistical regularity|regularity'),
           P('p2', 'Principle of inertia of large numbers (larger sample → more reliable)', 3, 'inertia|large number'),
           P('p3', 'Principle of optimisation (efficiency vs cost)', 2, 'optimi|optimum|efficiency'),
           P('p4', 'Principle of validity (valid estimates; probability sampling)', 2, 'valid')], 'c1'),
        V('v2', 'Why is a sample survey usually preferred to a complete enumeration, and when must we go for a census?',
          'A sample survey is faster, its total cost is lower, and it can be more reliable because trained staff and better supervision are used. Sampling error can be controlled, and sampling is a necessity in destructive testing or for a hypothetical population. But when we need information on every single unit, when the population is small, or when even one defect is critical, as in aircraft parts, we must use complete enumeration.',
          [P('p1', 'Speed and lower total cost', 3, 'speed|faster|quick|time', 'cost|cheap|expens|economical', min=1),
           P('p2', 'More reliable (trained staff, supervision)', 2, 'reliab|trained|supervis|accura', min=1),
           P('p3', 'Necessary for destructive testing / hypothetical population', 2, 'destruct|destroy|hypothetical|infinite', min=1),
           P('p4', 'Census when every unit needed, small population or one defect is critical', 3, 'census|complete enumeration|every unit|each unit|all unit|small population|aircraft|critical|every item|each item', min=1)], 'c2'),
        V('v3', 'Distinguish between sampling errors and non-sampling errors.',
          'Sampling errors arise only because a part of the population is studied, so they occur in sample surveys and not in a census. They come from a defective design, substitution of units, faulty demarcation, a wrong choice of statistic and variability of the population, and they fall as the sample size increases. Non-sampling errors such as recording mistakes, non-response, bias of enumerators and wrong measurement occur in both a census and a sample survey.',
          [P('p1', 'Sampling errors arise because only part of the population is studied; absent in a census', 4, ALT('sampling error {x}', x=('only part', 'part of the population', 'only in sample', 'not in census', 'absent in census', 'census free', 'only a part', 'only sample', 'only because', 'part'))),
           P('p2', 'Non-sampling errors occur in both census and sample survey', 4, 'non sampling|nonsampling', 'both|census as well|census too|even in census|census and sample'),
           P('p3', 'Examples (substitution, design / non-response, recording, bias)', 2, 'substitut|design|demarcat|wrong statistic|variabil|non response|recording|bias|memory|measurement', min=1)], 'c3'),
        V('v4', 'What is the difference between a parameter and a statistic? Give one example of each.',
          'A parameter is a characteristic of the population worked out from all its units, like the population mean mu or population proportion P. A statistic is a measure computed from sample observations, like the sample mean x bar or sample proportion p, and it is used to estimate the parameter. A parameter is fixed, but a statistic varies from sample to sample.',
          [P('p1', 'Parameter: measure of the population (all units), e.g. population mean', 4, ALT('parameter {x}', x=('population', 'all unit', 'whole population', 'universe', 'mu', 'fixed'))),
           P('p2', 'Statistic: measure from the sample, e.g. sample mean', 4, ALT('statistic {x}', x=('sample', 'x bar', 'xbar', 'estimate', 'varies', 'vary'))),
           P('p3', 'Statistic estimates the parameter / varies from sample to sample', 2, 'estimat|vary|varies|fluctuat|sample to sample', min=1)], 'c4'),
        V('v5', 'What is the standard error of the sample mean, and how does it change with sample size?',
          'The standard error is the standard deviation of the sampling distribution of a statistic. For the sample mean it is sigma divided by the square root of n under simple random sampling with replacement, multiplied by the finite population correction, the square root of N minus n over N minus 1, when sampling is without replacement. It is inversely proportional to the square root of the sample size, so four times the sample halves the standard error.',
          [P('p1', 'SD of the sampling distribution of the statistic', 3, 'standard deviation|sd', 'sampling distribution|statistic|sample mean', min=2),
           P('p2', 'σ/√n (with replacement)', 3, ALT('sigma {d} {r} n', 'sigma {d} root n', 'sigma {d} square root', d=('divided by', 'by', 'over'), r=('square root', 'root', 'under root', 'sqrt'))),
           P('p3', 'Finite population correction √((N−n)/(N−1)) without replacement', 2, 'finite population|correction|fpc|n minus 1|minus 1', min=1),
           P('p4', 'Inversely proportional to √n — larger sample, smaller SE', 2, 'inverse|inversely|decreas|smaller|fall|reduc|halve|less', min=1)], 'c4'),
        V('v6', 'Explain stratified sampling and the two ways of allocating the sample among strata.',
          'In stratified sampling a large, heterogeneous population is divided into strata so that units within a stratum are alike and the strata differ from each other, and a sample is drawn from every stratum. Under proportional or Bowley\'s allocation the sample size of each stratum is proportional to its population size. Under Neyman\'s allocation it is proportional to the population size multiplied by the standard deviation of the stratum.',
          [P('p1', 'Divide a heterogeneous population into homogeneous strata; sample from each', 4, 'strata|stratum|subgroup|sub population|group', 'homogeneous|alike|similar|heterogeneous|each|every', min=2),
           P('p2', "Proportional (Bowley's) allocation: n(i) ∝ N(i)", 3, 'proportional|bowley'),
           P('p3', "Neyman allocation: n(i) ∝ N(i) × S(i)", 3, 'neyman', 'standard deviation|sd|variability|s i|times', min=2)], 'c5'),
    ]

    return {
        'schema': 'ca-unit/1', 'id': UID, 'level': 'foundation', 'paper': 'p3', 'chapter': 'fnd-p3-ch13', 'n': 2,
        'title': 'Sampling',
        'outcomes': [
            'State the four principles of sample survey and compare a sample survey with complete enumeration.',
            'Separate sampling errors from non-sampling errors and name their sources.',
            'Use the language of sampling correctly — population, sample, sampling unit, frame, parameter, statistic, sampling distribution and standard error.',
            'Compute the number of possible samples, a sampling distribution of the mean and the standard error of a mean or proportion, with and without the finite population correction.',
            'Choose among simple random, stratified (proportional / Neyman), multistage, systematic and purposive sampling, and allocate a stratified sample.',
        ],
        'meta': {'difficulty': 'moderate', 'minutes': {'learn': 35, 'practice': 40}, 'prereq': ['fnd-p3-ch13-u01'],
                 'exam_tip': 'Paper 3 asks 2–4 MCQs from sampling: principles, census vs sample, errors, NCn vs N^n, σ/√n and the fpc, and which method suits a situation. Memorise the vocabulary exactly — options are often near-synonyms.'},
        'concepts': [
            {'id': 'c1', 'title': 'Why sample, and the principles behind it',
             'body': ['Time, cost and the sheer size of many populations make it impossible to examine every unit. We study a representative part and infer about the whole. Sampling theory deals with three problems: drawing a representative sample, estimating population values (parameters) from it, and testing claims (hypotheses) to take decisions.',
                      'Law of statistical regularity: a reasonably large sample drawn at random will, on average, possess the characteristics of the population. Reliability of an estimate grows with the square root of the sample size, so the size is a compromise with cost and time.',
                      'Principle of inertia of large numbers: other things equal, results become more stable and precise as the sample grows — a direct consequence of the first law.',
                      'Principle of optimisation: choose a design that gives maximum efficiency for a given cost, or a given efficiency at minimum cost. Principle of validity: a design is valid only if it yields valid estimates and tests — only probability sampling assures this.'],
             'analogy': 'You taste one spoonful of a well-stirred pot of dal to judge the whole pot. Stirring is randomness; a bigger spoon is a bigger sample.',
             'work': 'Statutory auditors rarely check every voucher. Standards on auditing allow sampling precisely because a well-designed random sample tells you about the whole population at a fraction of the cost.'},
            {'id': 'c2', 'title': 'Sample survey vs complete enumeration (census)',
             'body': ['Speed: a sample survey is usually much faster. Cost: cost per unit may be higher (better-trained staff), but total cost is lower. Reliability: trained enumerators, better supervision and modern methods can make sample data more reliable than census data.',
                      'Accuracy: every sample has sampling error (sampling fluctuation) which a census does not, but sampling error can be reduced by a larger sample and a proper probability design; non-sampling errors affect both and are easier to control in a survey.',
                      'Necessity: destructive testing (life of bulbs, crash tests) and hypothetical populations (all tosses of a coin) leave no choice but sampling.',
                      'A census is preferred when information on every unit is needed, when the population is small, or when one defect can be disastrous (aircraft components).'],
             'analogy': 'A blood test samples a few millilitres; nobody drains a patient to test all of his blood.',
             'work': 'Physical verification of inventory at a jeweller is usually 100% (high value, small count), while a FMCG warehouse with lakhs of low-value items is test-counted on a sample basis.'},
            {'id': 'c3', 'title': 'Errors in sample surveys',
             'body': ['Error = difference between the true population value and the value obtained from the survey.',
                      'Sampling errors exist only because a part is studied. Sources listed by ICAI: defective sampling design (non-probability methods let the sampler\'s bias in), substitution of a convenient unit for a selected one, faulty demarcation of sampling units (e.g. field boundaries in crop surveys), wrong choice of statistic, and high variability in the population (handled by stratified or multistage designs).',
                      'Non-sampling errors arise in both census and sample surveys: lapse of memory, preference for certain digits, ignorance, vanity, non-response, wrong measurement, communication gaps, incomplete coverage and enumerator bias.'],
             'analogy': 'Sampling error is the uncertainty of judging a film from its trailer; non-sampling error is a projector fault that would spoil the trailer and the full film alike.',
             'work': 'When a survey-based report shows a figure "±2%", that margin covers only sampling error. A good reviewer also asks about non-response and questionnaire wording — the non-sampling side.'},
            {'id': 'c4', 'title': 'Key terms, sampling distribution and standard error',
             'body': ['Population (universe): all units under study; size N. Finite (people in a town) or infinite (lamps a factory will ever make, stars); existent (real objects) or hypothetical (heads in endless coin tosses). Sample: a part chosen to represent the population; size n. Sampling unit: each unit that can be selected. Sampling frame: the complete, up-to-date list of sampling units — needed before drawing.',
                      'Parameter: a measure based on all population units — population mean μ = ΣX/N, proportion P = X/N, variance σ² = Σ(X − μ)²/N. Statistic: a function of sample observations — x̄ = Σx/n, p = x/n, s² = Σ(x − x̄)²/n (ICAI\'s definition) — used to estimate the parameter.',
                      'Number of possible samples of size n: Nⁿ with replacement; ᴺCₙ without replacement. Values of a statistic vary from sample to sample (sampling fluctuation); arranged with their probabilities they form its sampling distribution. Its mean is the expectation and its standard deviation is the standard error (SE), a measure of precision.',
                      'SE(x̄) = σ/√n (SRSWR); σ/√n × √((N − n)/(N − 1)) (SRSWOR). SE(p) = √(PQ/n) (SRSWR); √(PQ/n) × √((N − n)/(N − 1)) (SRSWOR). The factor √((N − n)/(N − 1)) is the finite population correction (fpc); it tends to 1 for a very large or infinite population and may be ignored. Unknown parameters are replaced by sample values.'],
             'blocks': [t1],
             'analogy': 'The parameter is the true weight of a bag; each weighing (sample) gives a statistic. The standard error tells you how much the readings wobble.',
             'work': 'In audit sampling the "precision" or "allowance for sampling risk" is built on exactly this standard-error idea: bigger samples, tighter precision.'},
            {'id': 'c5', 'title': 'Types of sampling',
             'body': ['Probability sampling: every unit has a fixed, pre-assigned chance of selection — simple random, stratified, multistage, multiphase, cluster. Non-probability sampling: selection rests on the sampler\'s judgement (purposive or judgement sampling). Mixed sampling: partly probability, partly a fixed rule — systematic sampling.',
                      'Simple random sampling (SRS): units selected independently, each with an equal chance; best done with random number tables. With replacement (SRSWR) the population stays unchanged; without replacement (SRSWOR) a drawn unit is not returned — the two become nearly identical for a very large population. SRS suits a population that is not very large and not heterogeneous, with a sample that is not very small; it is free from sampler\'s bias and underlies all tests of significance.',
                      'Stratified sampling: for a large, heterogeneous population — divide it into strata, homogeneous within and different between, and draw a sub-sample from each (stratified random sampling if SRS is used in each). It represents every sub-group, gives estimates for each stratum and overall, and improves precision. Allocation: proportional (Bowley) nᵢ ∝ Nᵢ when stratum variances are similar; Neyman nᵢ ∝ NᵢSᵢ when they differ. Not advisable for a small or homogeneous population or without prior information.',
                      'Multistage sampling: select first-stage units (States), then second-stage units within them (districts), and so on to the ultimate units (households). Wide coverage, cost-effective, flexible — but usually less accurate than stratified sampling.',
                      'Systematic sampling: pick the first unit at random from the first k, then every kth unit. Linear when N = nk (k = N/n, the sample interval); circular when N = nk + p, p < k, continuing cyclically. Simple, quick and cheap with a good frame, but badly biased if the frame has a hidden periodicity matching k; since it is not a pure probability method, valid inference is not possible.',
                      'Purposive (judgement) sampling: entirely the sampler\'s choice — subjective, varies from person to person, and no hypothesis can be tested from it.'],
             'blocks': [t2],
             'analogy': 'Stratified sampling is a thali — a little from every bowl. Systematic sampling is picking every 10th person in a queue after a random start.',
             'work': 'Auditors stratify receivables by size: every balance above a threshold is confirmed (100% stratum), smaller ones are sampled. Systematic selection (every kth invoice after a random start) is common when a numbered register is available.'},
        ],
        'illustrations': [
            {'id': 'i1', 'title': 'Sampling distribution of the mean without replacement', 'difficulty': 'moderate', 'minutes': 12,
             'q': 'A population has four units: 3, 5, 9, 11. Draw all samples of size 2 without replacement, find the sampling distribution of the mean, and verify that SE² = σ²/n × (N − n)/(N − 1).',
             'solution': [wn('Population', f'μ = 28 ÷ 4 = {fm(mu)}. σ² = (16 + 4 + 4 + 16) ÷ 4 = {fm(var)}. Number of samples = ⁴C₂ = {ns}.'), t1,
                          wn('Mean and SE by enumeration', 'Mean of the six sample means = 42 ÷ 6 = 7 = μ (the sample mean is unbiased). Variance of x̄ = 20 ÷ 6 = 10/3 ≈ 3.33.'),
                          wn('By formula', 'σ²/n × (N − n)/(N − 1) = 10/2 × 2/3 = 10/3 — the same. SE = √(10/3) ≈ 1.83. With replacement there would be 4² = 16 samples and SE² = σ²/n = 5.')],
             'checks': c1},
            {'id': 'i2', 'title': 'Proportional vs Neyman allocation', 'difficulty': 'moderate', 'minutes': 8,
             'q': 'A population of 2,500 shops is split into three strata of 1,200, 800 and 500 shops with standard deviations of monthly sales of 10, 30 and 18 (₹ thousand). A sample of 150 is to be drawn. Allocate it by (a) proportional and (b) Neyman allocation.',
             'solution': [t2, wn('Working', 'Proportional: nᵢ = 150 × Nᵢ/2,500 → 72, 48, 30. Neyman: ΣNᵢSᵢ = 45,000; nᵢ = 150 × NᵢSᵢ/45,000 → 40, 80, 30.'),
                          note('Neyman gives the second stratum more units because its sales vary most; proportional allocation ignores variability.')],
             'checks': c2},
            {'id': 'i3', 'title': 'Standard error of a mean and a proportion', 'difficulty': 'core', 'minutes': 6,
             'q': '(a) A sample of 100 is drawn from 2,000 accounts whose balances have SD ₹15 (thousand). Find SE of the mean with and without replacement. (b) In a sample of 400 invoices, 20% have errors. Estimate the SE of the proportion (large population).',
             'solution': [wn('(a)', f'SRSWR: SE = 15/√100 = {fm(se_wr)}. fpc = √(1,900/1,999) = {fm(fpc)}. SRSWOR: SE = 1.5 × {fm(fpc)} = {fm(se_wor)} (₹ thousand).'),
                          wn('(b)', f'P is unknown, so use p = 0.2: SE(p) = √(0.2 × 0.8/400) = {fm(se_p)}, i.e. 2 percentage points.')],
             'checks': c3},
            {'id': 'i4', 'title': 'Linear and circular systematic sampling', 'difficulty': 'core', 'minutes': 5,
             'q': '(a) Select 40 invoices systematically from a register numbered 1 to 600, the random start being 7. (b) What interval is used to select 8 units from 50?',
             'solution': [wn('(a) Linear', f'k = 600/40 = {fm(k4)}. Sample: 7, 22, 37, …, 7 + 39 × 15 = {last}.'),
                          wn('(b) Circular', f'50 = 8 × 6 + 2, so k = {kc}. Pick a random start from 1–6 and take every 6th unit, going round the list cyclically until 8 units are chosen.')],
             'checks': c4},
        ],
        'jobs': [
            {'id': 'j1', 'title': 'Designing a sample for a receivables confirmation', 'role': 'Audit senior, statutory audit of an engineering company',
             'situation': '2,400 customer balances total ₹96 crore. 30 balances above ₹50 lakh make up ₹48 crore. You have budget for about 130 confirmations.',
             'steps': ['Stratify: confirm all 30 large balances (a 100% stratum — a census where one error matters a lot).',
                       'Split the rest by size into two or three strata; sizes vary a lot, so Neyman-type allocation gives more letters to the more variable stratum.',
                       'Use the debtors ledger as the sampling frame — first check it agrees with the trial balance (complete and up to date).',
                       'Within each stratum use random numbers or systematic selection with a random start; never let staff "replace" a hard-to-reach customer (substitution bias).',
                       'Chase non-replies and perform alternative procedures — non-response is a non-sampling error that a bigger sample does not cure.'],
             'takeaway': 'Stratified selection, a reliable frame and no substitution are what make an audit sample defensible.',
             'think': 'Why is a sample drawn only from customers who replied quickly last year a bad idea?',
             'answer': 'It is a judgement (non-probability) choice that systematically excludes slow or disputed accounts — exactly where misstatement is likely. Results cannot be projected validly.'},
            {'id': 'j2', 'title': 'Reading a survey margin of error', 'role': 'Research analyst at a broking firm',
             'situation': 'A dealer survey of 400 shops says 30% expect higher demand next quarter. Your manager asks how precise that is.',
             'steps': ['Treat the population of dealers as large, so ignore the fpc.',
                       'SE(p) = √(0.3 × 0.7/400) ≈ 0.023, about 2.3 percentage points.',
                       'Point out non-sampling risks — leading questions, only large dealers responding.',
                       'If the manager needs half the SE, the sample must be four times larger (1,600 shops).'],
             'takeaway': 'SE shrinks only with √n — halving the error costs four times the sample.',
             'checks': [{'expr': 'round((0.3*0.7/400)**0.5,4)', 'value': round((0.3 * 0.7 / 400) ** 0.5, 4), 'label': 'SE of proportion'}]},
        ],
        'mcqs': [
            mq('m1', 'According to the law of statistical regularity:', ['A moderately large random sample, on average, shows the characteristics of the population', 'Results are always exact for small samples', 'Only purposive samples represent the population', 'Larger samples always cost less'],
               "The law of statistical regularity says that a reasonably large sample chosen at random will, on average, show the characteristics of the population. Both conditions matter: size and randomness. 'Only purposive samples represent the population' is the trap: judgement selection breaks the randomness the law needs. In practice: auditors rely on this law when they test a random sample of vouchers instead of every entry.", 'c1', topic='Why sample, and the principles behind it'),
            mq('m2', 'The principle stating that results become more reliable as the sample size increases, other things remaining the same, is the principle of:', ['Inertia of large numbers', 'Optimisation', 'Validity', 'Statistical regularity'],
               'The principle of inertia of large numbers says that, other things equal, results become more stable and reliable as the sample size grows, because extreme values tend to cancel out. Statistical regularity is the trap: it is the parent law about random samples representing the population, not specifically about stability with size. In practice: opinion polls and audit samples gain reliability with larger sizes.', 'c1', 'moderate', topic='Why sample, and the principles behind it'),
            mq('m3', 'Under the principle of validity, a sample design can be called valid only when:', ['It yields valid estimates and valid tests about parameters', 'It is cheapest', 'The sample is very large', 'The sampler uses judgement'],
               "The principle of validity says a sample design is valid only if it allows valid estimates of population parameters and valid tests of significance. This needs probability (random) sampling. 'It is cheapest' is the trap: cost relates to the principle of optimisation, not validity. In practice: statistical sampling in audit is accepted because it lets the auditor project errors to the whole population.", 'c1', topic='Why sample, and the principles behind it'),
            mq('m4', 'Maximum efficiency at a given cost, or a given efficiency at minimum cost, is the principle of:', ['Optimisation', 'Validity', 'Inertia', 'Statistical regularity'],
               'The principle of optimisation aims at the best efficiency (lowest standard error) for a given cost, or a given efficiency at the lowest cost. Validity is the trap: it concerns whether valid estimates and tests are possible, not cost. In practice: an audit manager choosing a sample size balances the cost of testing against the precision needed, which is this principle at work.', 'c1', topic='Why sample, and the principles behind it'),
            mq('m5', 'Testing the life of electric bulbs requires sampling because:', ['The testing destroys the items', 'Sampling has no error', 'The population is small', 'A census is always cheaper'],
               "To find a bulb's life, it must be burned until it fails, so testing destroys the item. A complete enumeration would leave nothing to sell, so sampling is the only option. 'A census is always cheaper' is the trap: a census is usually costlier. In practice: food, pharma and electronics manufacturers in India test destructive quality parameters only on samples from each batch.", 'c2', topic='Sample survey vs complete enumeration (census)'),
            mq('m6', 'Complete enumeration is preferred when:', ['One defect could be disastrous, as with aircraft components', 'Testing destroys the item', 'The population is hypothetical', 'Speed is the main concern'],
               "When even one defective unit could be disastrous, such as aircraft parts, every unit must be inspected, so complete enumeration (census) is preferred. 'Testing destroys the item' is the trap: that makes a census impossible, not preferable. In practice: banks verify every high-value loan file or every cash vault item rather than sampling, because the risk of one error is too high.", 'c2', topic='Sample survey vs complete enumeration (census)'),
            mq('m7', 'Compared with a census, the cost per unit of a sample survey is usually ____ but the total cost is ____.', ['higher; lower', 'lower; higher', 'lower; lower', 'higher; higher'],
               "A sample survey uses better-trained staff and closer supervision, so the cost per unit is usually higher, but far fewer units are covered, so the total cost is lower. 'Lower; higher' is the trap: it reverses both. In practice: NSSO surveys use skilled field staff for a sample of households instead of reaching every household as the Census of India does.", 'c2', 'moderate', topic='Sample survey vs complete enumeration (census)'),
            mq('m8', 'Which error is completely absent in a complete enumeration?', ['Sampling error', 'Non-sampling error', 'Recording error', 'Non-response error'],
               'Sampling error arises only because a part of the population is studied instead of the whole, so it is absent in a complete enumeration. Non-sampling error is the trap: errors like recording mistakes, non-response or bias occur in both censuses and samples. In practice: even a 100% stock count can contain counting or recording errors, which are non-sampling errors.', 'c3', topic='Errors in sample surveys'),
            mq('m9', 'An enumerator replaces a selected household with a nearby one because the selected one was locked. The error is due to:', ['Substitution (a sampling error)', 'Wrong choice of statistic', 'Faulty demarcation', 'Lapse of memory'],
               "The enumerator replaced the selected household with a convenient one. This is substitution, which ICAI lists among the sources of sampling error because it changes the sample actually studied. Lapse of memory is the trap: that is a respondent's error, a non-sampling error. In practice: an auditor must not swap a selected voucher for an easier one; the selection must be followed exactly.", 'c3', 'moderate', topic='Errors in sample surveys'),
            mq('m10', 'Non-response by respondents is an example of:', ['Non-sampling error', 'Sampling error', 'Standard error', 'Finite population correction'],
               'Non-response arises from respondents not replying, not from the fact that only a sample was studied, so it is a non-sampling error. It can occur even in a census. Sampling error is the trap: that comes only from studying a part instead of the whole. In practice: unreturned debtor confirmations in audit are a non-response problem that needs alternative procedures.', 'c3', topic='Errors in sample surveys'),
            mq('m11', 'Sampling error can be reduced by:', ['Increasing the sample size and following a probability design strictly', 'Using purposive sampling', 'Reducing the sample size', 'Allowing substitution'],
               "Sampling error falls when the sample size is increased and the probability design is followed strictly, with no substitution. 'Using purposive sampling' is the trap: judgement selection introduces bias and does not allow the error to be measured. In practice: Standards on Auditing guide auditors to increase sample sizes where risk is higher, to reduce sampling risk.", 'c3', topic='Errors in sample surveys'),
            mq('m12', 'The population of heads obtained when a coin is tossed endlessly is:', ['Hypothetical and infinite', 'Existent and finite', 'Existent and infinite', 'Hypothetical and finite'],
               "The heads from endlessly tossing a coin do not physically exist as a fixed group, so the population is hypothetical, and since tossing can go on forever, it is infinite. 'Existent and finite' is the trap: that describes real, countable groups such as employees of a company. In practice: models of repeated events, like daily price moves, treat outcomes as a hypothetical infinite population.", 'c4', 'moderate', topic='Key terms, sampling distribution and standard error'),
            mq('m13', 'A complete and up-to-date list of all sampling units is called the:', ['Sampling frame', 'Sampling distribution', 'Sample space', 'Stratum'],
               "A sampling frame is the complete and up-to-date list of all sampling units, from which the sample is drawn. A sampling distribution is the trap: that is the distribution of a statistic across all possible samples. In practice: in an audit, the frame might be the debtors' ledger listing or the voucher register, and it must be complete before sampling begins.", 'c4', topic='Key terms, sampling distribution and standard error'),
            mq('m14', 'A characteristic computed from all units of the population is a:', ['Parameter', 'Statistic', 'Standard error', 'Sampling unit'],
               'A value computed from all units of the population is a parameter, such as the true population mean. A statistic is the trap: that is computed from a sample and used to estimate the parameter. In practice: the true average balance of all savings accounts at a bank is a parameter; the average from a sample of 500 accounts is a statistic.', 'c4', topic='Key terms, sampling distribution and standard error'),
            mq('m15', 'The standard deviation of the sampling distribution of a statistic is called its:', ['Standard error', 'Variance', 'Expectation', 'Sampling fluctuation'],
               'The standard deviation of the sampling distribution of a statistic is its standard error. It measures how much the statistic varies from sample to sample, i.e. its precision. Variance is the trap: variance is the square of a standard deviation, not this specific measure. In practice: survey reports by agencies like RBI quote a margin of error based on the standard error.', 'c4', topic='Key terms, sampling distribution and standard error'),
            nq('m16', 'How many samples of size 3 can be drawn without replacement from a population of 6 units?', '6*5*4/(3*2*1)', [216, 120, 18],
               'Without replacement, and order not mattering, the number of samples is ⁶C₃ = (6 × 5 × 4) ÷ (3 × 2 × 1) = 20. 216 is the trap: 6³ counts samples drawn with replacement. 120 counts ordered selections. In practice: knowing how many different samples are possible helps an auditor appreciate that each random sample is just one of many.', 'c4', topic='Key terms, sampling distribution and standard error'),
            nq('m17', 'How many samples of size 2 can be drawn with replacement from a population of 5 units?', '5**2', [10, 20, 32],
               'With replacement, each of the 2 draws can be any of the 5 units, so the count is Nⁿ = 5² = 25. 10 is the trap: ⁵C₂ = 10 is the count without replacement. In practice: with-replacement sampling is assumed in many statistical formulas, such as SE = σ/√n, because it keeps each draw independent.', 'c4', topic='Key terms, sampling distribution and standard error'),
            nq('m18', 'A population has SD 24. The standard error of the mean for a random sample of 36 drawn with replacement is:', '24/36**0.5', [0.67, 24, 6],
               'With replacement, the standard error of the mean is σ/√n = 24 ÷ √36 = 24 ÷ 6 = 4. 24 is the trap: that is the population SD, not the standard error of the sample mean. In practice: an analyst estimating average invoice value from a sample quotes this standard error to show how close the estimate is likely to be.', 'c4', topic='Key terms, sampling distribution and standard error'),
            nq('m19', 'From a population of 101 units with SD 10, a sample of 25 is drawn without replacement. The SE of the mean is:', 'round(10/25**0.5*((101-25)/(101-1))**0.5,2)', [2, 1.52, 0.4],
               'Without replacement, apply the finite population correction: SE = (σ/√n) × √((N − n)/(N − 1)) = (10 ÷ 5) × √(76 ÷ 100) = 2 × 0.8718 ≈ 1.74. The trap is 2, which ignores the correction. 1.52 forgets the square root. In practice: auditors sampling from a small population of invoices benefit from this correction, which reduces the required sample size.', 'c4', 'hard', topic='Key terms, sampling distribution and standard error'),
            nq('m20', 'In a large population 40% of firms are loss-making. For a random sample of 600, the standard error of the sample proportion is:', 'round((0.4*0.6/600)**0.5,2)', [0.0004, 0.04, 0.24],
               'For a proportion, SE = √(PQ/n) = √(0.4 × 0.6 ÷ 600) = √0.0004 = 0.02. The trap is 0.0004, which forgets to take the square root. In practice: a survey of 600 firms reporting a 40% loss-making share would quote a margin of about ±2 percentage points per standard error.', 'c4', 'moderate', topic='Key terms, sampling distribution and standard error'),
            mq('m21', 'If the sample size is increased from 100 to 400, the standard error of the mean becomes:', ['Half', 'One-fourth', 'Double', 'Unchanged'],
               "SE = σ/√n, so it varies inversely with the square root of n. Multiplying n by 4 multiplies √n by √4 = 2, so the SE halves. 'One-fourth' is the trap: it assumes SE falls in proportion to n, not √n. In practice: to halve the margin of error of a survey or audit sample, you need four times as many items, which is costly.", 'c4', 'moderate', topic='Key terms, sampling distribution and standard error'),
            mq('m22', 'The finite population correction √((N − n)/(N − 1)) may be ignored when:', ['The population is very large or infinite relative to the sample', 'The sample equals the population', 'Sampling is purposive', 'The population is small'],
               "The factor √((N − n)/(N − 1)) is close to 1 when N is very large compared with n, so it can be ignored for very large or infinite populations. 'The population is small' is the trap: that is exactly when the correction matters most. In practice: national surveys drawn from crores of households ignore the correction; a sample from a 200-item ledger should not.", 'c4', topic='Key terms, sampling distribution and standard error'),
            mq('m23', 'Systematic sampling is classed by ICAI as:', ['Mixed sampling', 'Pure probability sampling', 'Purposive sampling', 'Stratified sampling'],
               'In systematic sampling only the first unit is chosen at random and every k-th unit after it follows a fixed rule. Because it combines random and non-random selection, ICAI classes it as mixed sampling. Pure probability sampling is the trap: not every later unit is chosen at random. In practice: auditors often pick every 50th voucher after a random start.', 'c5', 'moderate', topic='Types of sampling'),
            mq('m24', 'Which sampling method is most suitable for a large and heterogeneous population?', ['Stratified sampling', 'Simple random sampling', 'Purposive sampling', 'Systematic sampling'],
               'In a large heterogeneous population, stratified sampling first divides it into groups that are internally similar, then samples from each. This gives better representation and precision. Simple random sampling is the trap: it can miss small but important groups. In practice: auditors stratify debtors by balance size so that large balances are always tested.', 'c5', topic='Types of sampling'),
            mq('m25', 'Under Neyman allocation, the sample size of a stratum is proportional to:', ['Product of its size and its standard deviation', 'Its size only', 'Its standard deviation only', 'The square of its size'],
               "Neyman (optimum) allocation gives each stratum a sample proportional to NᵢSᵢ, the product of its size and its standard deviation, so larger and more variable strata get more units. 'Its size only' is the trap: that is proportional (Bowley's) allocation. In practice: more variable strata, such as high-value receivables, get larger samples in audit to control risk.", 'c5', topic='Types of sampling'),
            nq('m26', 'Strata of sizes 600, 300 and 100 share a sample of 50 by proportional allocation. The first stratum gets:', '50*600/1000', [25, 16.67, 20],
               "Under proportional allocation, each stratum's share = n × Nᵢ ÷ N. Total N = 600 + 300 + 100 = 1,000, so the first stratum gets 50 × 600 ÷ 1,000 = 30. The trap is 16.67, which splits the sample equally among the three strata. In practice: a bank sampling branches across regions uses proportional allocation so that bigger regions get more sampled branches.", 'c5', topic='Types of sampling'),
            nq('m27', 'A systematic sample of 25 is to be selected from 500 units. The sampling interval is:', '500/25', [25, 12.5, 475],
               'The sampling interval k = N ÷ n = 500 ÷ 25 = 20, so every 20th unit is chosen after a random start between 1 and 20. The trap is 25, which is the sample size, not the interval. In practice: an auditor selecting 25 of 500 sales invoices picks a random start and then every 20th invoice.', 'c5', topic='Types of sampling'),
            mq('m28', 'Selecting States, then districts within them, then villages and finally households is:', ['Multistage sampling', 'Stratified sampling', 'Systematic sampling', 'Cluster-free sampling'],
               "Selection proceeds in stages: States, then districts, then villages, then households (the ultimate units). That is multistage sampling. Stratified sampling is the trap: there, every stratum is sampled directly, not through successive stages. In practice: NSSO and the National Family Health Survey use multistage designs to cover India's vast population economically.", 'c5', topic='Types of sampling'),
            mq('m29', 'A major drawback of systematic sampling is that:', ['A hidden periodicity in the frame matching the interval gives a badly biased sample', 'It needs no sampling frame', 'It is very costly', 'It always gives larger errors than SRS'],
               "If the list has a hidden pattern that repeats at the same interval as the sampling interval, every selected unit may share the same feature, giving a badly biased sample. 'It needs no sampling frame' is the trap: systematic sampling does need a list. In practice: picking every 7th day's sales would always land on the same weekday, distorting the result.", 'c5', 'moderate', topic='Types of sampling'),
            mq('m30', 'Which statement about purposive sampling is correct?', ['It is subjective and no statistical hypothesis can be tested from it', 'Every unit has an equal chance of selection', 'It is the basis of all tests of significance', 'It is a mixed sampling method'],
               "In purposive (judgement) sampling, units are chosen by the sampler's own judgement, so the sample is subjective and no valid tests of significance can be made from it. 'Every unit has an equal chance' is the trap: that describes simple random sampling. In practice: an auditor's judgement sample of unusual entries is useful, but its results cannot be projected statistically to all entries.", 'c5', topic='Types of sampling'),
            mq('m31', 'Compared with stratified sampling, multistage sampling is generally:', ['Less accurate but cheaper and more flexible', 'More accurate and more expensive', 'Equally accurate and equally costly', 'Not a probability method'],
               "Multistage sampling saves cost and is flexible because units are selected stage by stage, but it is usually less accurate than stratified sampling of the same size. 'More accurate and more expensive' is the trap: that describes stratified sampling relative to multistage. In practice: large consumer surveys accept the slight loss of accuracy to cover rural India affordably.", 'c5', 'moderate', topic='Types of sampling'),
        ],
        'questions': [
            {'id': 'q1', 'marks': 6, 'minutes': minutes(6), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'A population consists of three units 1, 4 and 7. (a) How many samples of size 2 can be drawn with replacement? (b) Obtain the sampling distribution of the sample mean. (c) Find E(x̄) and SE(x̄) from the distribution and verify them with μ and σ/√n.',
             'model': [wn('(a)', 'Nⁿ = 3² = 9 samples: (1,1), (1,4), (1,7), (4,1), (4,4), (4,7), (7,1), (7,4), (7,7).'), tq1,
                       wn('(c)', f'E(x̄) = 4 = μ (μ = 12/3 = {fm(mu1)}). E(x̄²) = 171/9 = 19, so V(x̄) = 19 − 16 = 3 and SE = √3 ≈ 1.73. Formula: σ² = (9 + 0 + 9)/3 = {fm(var1)}, σ²/n = 6/2 = 3 — verified.')],
             'scheme': [{'id': 's1', 'pt': 'Nine samples listed (Nⁿ)', 'm': 1, 'skill': 'concept'},
                        {'id': 's2', 'pt': 'Sampling distribution with correct probabilities', 'm': 2, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'E(x̄) = 4 = μ', 'm': 1, 'skill': 'computation'},
                        {'id': 's4', 'pt': 'V(x̄) = 3 from distribution and from σ²/n', 'm': 2, 'skill': 'computation'}],
             'remarks': ['Ordered samples (1,4) and (4,1) are different under WR — many candidates list only 6.', 'Show σ² with divisor N for a population.'],
             'mistakes': ['Using ³C₂ = 3 samples for with-replacement sampling.', 'Applying the fpc to WR sampling.'],
             'tips': ['Tabulate x̄, P, x̄P and x̄²P — the totals give everything.'],
             'checks': q1c},
            {'id': 'q2', 'marks': 5, 'minutes': minutes(5), 'difficulty': 'moderate', 'pad': 'table',
             'q': 'A population of 6,000 households is divided into three strata of 3,000, 2,000 and 1,000 with SDs of monthly spending 6, 12 and 15 (₹ hundred). Allocate a sample of 240 by (a) proportional and (b) Neyman allocation (round to whole households).',
             'model': [tq2, wn('Working', f'(a) nᵢ = 240 × Nᵢ/6,000 → 120, 80, 40. (b) ΣNᵢSᵢ = {inr(q2ns)}; nᵢ = 240 × NᵢSᵢ/57,000 → 75.79, 101.05, 63.16 → 76, 101, 63 (total 240).')],
             'scheme': [{'id': 's1', 'pt': 'Proportional allocation formula and figures', 'm': 2, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'ΣNᵢSᵢ = 57,000', 'm': 1, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'Neyman figures, rounded to total 240', 'm': 2, 'skill': 'computation'}],
             'remarks': ['Rounding must preserve the total sample size.'],
             'mistakes': ['Using Sᵢ alone for Neyman allocation.', 'Using Nᵢ²'],
             'tips': ['State the formula nᵢ = n × NᵢSᵢ/ΣNᵢSᵢ before substituting.'],
             'checks': q2c},
            {'id': 'q3', 'marks': 4, 'minutes': minutes(4), 'difficulty': 'core', 'pad': 'text',
             'q': 'Monthly sales of a population of 800 outlets have SD ₹20 thousand. (a) Find the SE of the sample mean for n = 64 drawn with replacement, and without replacement. (b) What sample size (with replacement) gives an SE of ₹2 thousand?',
             'model': [wn('(a)', f'WR: SE = 20/√64 = {fm(q3a)}. WOR: SE = 2.5 × √(736/799) = {fm(q3b)}.'),
                       wn('(b)', f'σ/√n = 2 ⇒ √n = 10 ⇒ n = {fm(q3n)}.')],
             'scheme': [{'id': 's1', 'pt': 'SE with replacement = 2.5', 'm': 1, 'skill': 'computation'},
                        {'id': 's2', 'pt': 'fpc applied correctly, SE = 2.4', 'm': 1.5, 'skill': 'computation'},
                        {'id': 's3', 'pt': 'n = (σ/SE)² = 100', 'm': 1.5, 'skill': 'application'}],
             'remarks': ['Most candidates get (a); in (b) many forget to square.'],
             'mistakes': ['Writing the fpc without the square root.', 'n = σ/SE = 10.'],
             'tips': ['n = (σ/SE)² — memorise it.'],
             'checks': q3c},
        ],
        'revision': {
            'summary': ['Principles: statistical regularity, inertia of large numbers, optimisation, validity.',
                        'Sample survey: faster, cheaper overall, more reliable; census: no sampling error, needed for small / critical populations.',
                        'Sampling errors (design, substitution, demarcation, wrong statistic, variability) vs non-sampling errors (both census and sample).',
                        'Parameter (population) vs statistic (sample); sampling distribution; SE = SD of a statistic.',
                        'Types: probability (SRS, stratified, multistage), non-probability (purposive), mixed (systematic).'],
            'remember': ['Samples: Nⁿ (WR), ᴺCₙ (WOR).', 'SE(x̄) = σ/√n; × √((N − n)/(N − 1)) for WOR.', 'SE(p) = √(PQ/n).', 'Proportional nᵢ ∝ Nᵢ; Neyman nᵢ ∝ NᵢSᵢ.', 'Systematic interval k = N/n.'],
            'traps': ['Substitution is a SAMPLING error in ICAI\'s list.', 'Systematic sampling is MIXED, not pure probability sampling.', 'Quadrupling n only halves SE.', 'Non-sampling errors are present in a census too.']},
        'quickref': [
            {'k': 'Number of samples', 'v': 'With replacement Nⁿ; without replacement ᴺCₙ'},
            {'k': 'SE of mean', 'v': 'σ/√n (SRSWR); σ/√n × √((N − n)/(N − 1)) (SRSWOR)'},
            {'k': 'SE of proportion', 'v': '√(PQ/n); × fpc for SRSWOR'},
            {'k': 'Population mean / variance', 'v': 'μ = ΣX/N; σ² = Σ(X − μ)²/N'},
            {'k': 'Proportional (Bowley) allocation', 'v': 'nᵢ = n × Nᵢ/N'},
            {'k': 'Neyman allocation', 'v': 'nᵢ = n × NᵢSᵢ/ΣNᵢSᵢ'},
            {'k': 'Systematic sampling', 'v': 'k = N/n (linear); N = nk + p (circular)'},
            {'k': 'Sample size for target SE', 'v': 'n = (σ/SE)²'},
        ],
        'viva': viva, 'cases': cases,
    }
