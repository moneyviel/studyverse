/* ================= CA speed kit (js/ca-speed.js) — loaded after js/ca-tools.js =================
   CA Foundation Papers 3 and 4: 100 MCQs in 2 hours = 72 seconds a question. This file adds:
   1. ⚡ Fast way    — a button on every CA MCQ: q.fast (optional, string or list of steps) or a smart tip from the
                       question type (numbers in the options → estimate / back-solve; NOT/EXCEPT → odd one out;
                       statements → cut options with one wrong statement), the target time and related tricks.
   2. Pacing chip    — time on this question vs the target (q.secs or 72 s). Correct but slower than the target goes
                       into the ⚡ Speed drill list: ST.ca.speed = { "<unit>#<qid>": { d, s (secs), t (target), n } }.
                       A question leaves the list when it is answered correctly within its target.
   3. Shortcut tricks — an original library (QA, Economics, Accounting, Law, exam technique, calculator), each with a
                       worked mini example, linked to chapters so MCQs show the tricks that fit them.
   4. Calculator replay — when an MCQ has q.keys (list of calculator keys, q.keysMode 'basic' | 'sci'), a key-by-key
                       replay on the real calculator (js/calc.js hooks: open, reset, hint, coach, _press, _sciPress).
   5. 3-pass exam strategy — guide and pass breakdown (the runner itself is runSet in js/ca-tools.js, opts.passes).
   6. Speed report card — for the CA dashboard: average seconds per subject vs 72 s, minutes lost/gained over 100 Qs.
   7. 📌 Exam focus list — CA Foundation Paper 1 Accounting, chapter by chapter, with "Practise now".
   Everything here is StudyVerse's own wording (no ICAI text). */
(function () {
  'use strict';
  if (!window.Ca || !Ca._) return;
  const D = document, X = Ca._;
  const TARGET = 72;
  const C = () => { const c = X.C(); c.speed = c.speed || {}; c.mlog = c.mlog || []; return c; };
  const tap = k => { try { sfx(k); } catch (e) {} };
  const say = m => { try { if (window.A11Y) A11Y.announce(m); } catch (e) {} };
  const T = () => window.CaTools || null;
  const target = q => { const s = q && +q.secs; return s >= 10 && s <= 600 ? Math.round(s) : TARGET; };
  const paperOf = key => (String(key || '').match(/^([a-z]+-p\d+)/) || [])[1] || '';
  const chOf = key => String(key || '').split('#')[0].replace(/-u\d+$/, '');
  const SUBJ = { 'fnd-p1': ['acc', 'Accounting'], 'fnd-p2': ['law', 'Business Laws'], 'fnd-p3': ['qa', 'Quantitative Aptitude'], 'fnd-p4': ['eco', 'Business Economics'] };
  const reduced = () => { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };

  /* ================= 3. Shortcut tricks (original) ================= */
  const GROUPS = [['qa', 'Quantitative Aptitude'], ['eco', 'Economics'], ['acc', 'Accounting'], ['law', 'Law'], ['gen', 'Exam technique'], ['calc', 'Calculator']];
  /* { id, s: group, n: name, r: the rule, ex: [question, [steps], answer], ch: chapters it helps with } */
  const TRICKS = [
    { id: 'qa-72', s: 'qa', n: 'Rule of 72', r: 'Money doubles in about 72 ÷ (interest rate %) years. Use 69 for continuous compounding.', ex: ['At 8% a year compound, about how long until ₹50,000 becomes ₹1,00,000?', ['72 ÷ 8 = 9'], 'About 9 years (exact: 9.01 years).'], ch: ['fnd-p3-ch04'] },
    { id: 'qa-units', s: 'qa', n: 'Units-digit check', r: 'The last digit of a product depends only on the last digits of the numbers. Use it to cut options without multiplying.', ex: ['37 × 43 = ? Options: 1,581 · 1,591 · 1,593 · 1,597', ['Last digits: 7 × 3 = 21 → ends in 1', 'Only 1,591 ends in 1'], '1,591'], ch: ['fnd-p3-ch01', 'fnd-p3-ch02', 'fnd-p3-ch09'] },
    { id: 'qa-back', s: 'qa', n: 'Back-substitute the options', r: 'When options are numbers, put each one into the question instead of solving. Start with the middle option — if it is too big, go smaller.', ex: ['Roots of x² − 5x + 6 = 0? (a) 1, 6 (b) 2, 3 (c) −2, −3 (d) 1, 5', ['Try 2: 4 − 10 + 6 = 0 ✓', 'Try 3: 9 − 15 + 6 = 0 ✓'], '(b) 2, 3 — no formula needed.'], ch: ['fnd-p3-ch02', 'fnd-p3-ch03', 'fnd-p3-ch06'] },
    { id: 'qa-pct', s: 'qa', n: 'Percentage-change chain', r: 'Two changes of a% and b% in a row = a + b + (a × b ÷ 100). Use minus signs for falls.', ex: ['A price rises 20% and then falls 10%. Net change?', ['20 + (−10) + (20 × −10 ÷ 100)', '= 10 − 2 = 8'], 'Net rise of 8%.'], ch: ['fnd-p3-ch01', 'fnd-p3-ch04', 'fnd-p3-ch18'] },
    { id: 'qa-ratio', s: 'qa', n: 'Ratio split in one line', r: 'Share = Total × (its part ÷ sum of parts). Find one part first: Total ÷ sum = value of 1 part.', ex: ['Divide ₹9,000 in the ratio 2 : 3 : 4.', ['Sum of parts = 9, so 1 part = ₹1,000', 'Shares: 2,000 · 3,000 · 4,000'], '₹2,000, ₹3,000 and ₹4,000.'], ch: ['fnd-p3-ch01'] },
    { id: 'qa-ap', s: 'qa', n: 'AP sum = n × average', r: 'In an AP the average is (first + last) ÷ 2, so Sum = n × (first + last) ÷ 2. The middle term is also the average.', ex: ['Sum of 1 + 2 + … + 100?', ['Average = (1 + 100) ÷ 2 = 50.5', '100 × 50.5'], '5,050'], ch: ['fnd-p3-ch06'] },
    { id: 'qa-gp', s: 'qa', n: 'GP sum checks', r: 'Sum to infinity of a GP = a ÷ (1 − r) when −1 < r < 1. A finite sum can never be more than this.', ex: ['1 + ½ + ¼ + … = ?', ['a = 1, r = ½', '1 ÷ (1 − ½) = 2'], '2'], ch: ['fnd-p3-ch06'] },
    { id: 'qa-mmm', s: 'qa', n: 'Mean–median–mode link', r: 'For a moderately skewed distribution: Mode ≈ 3 Median − 2 Mean. Know any two, get the third.', ex: ['Mean 40, median 38. Mode?', ['3 × 38 − 2 × 40', '= 114 − 80'], '34'], ch: ['fnd-p3-ch14'] },
    { id: 'qa-sd', s: 'qa', n: 'Change of origin and scale', r: 'Adding a constant changes the mean but not the SD. Multiplying by b multiplies the SD by |b|. So SD of (a + bX) = |b| × SD of X.', ex: ['SD of X is 4. SD of Y = 10 − 3X?', ['Ignore the 10 (origin)', '|−3| × 4'], '12'], ch: ['fnd-p3-ch14'] },
    { id: 'qa-npv', s: 'qa', n: 'NPV sign check', r: 'For normal cash flows (outflow first): if the discount rate is below the IRR, NPV is positive; above the IRR, NPV is negative. At 0% the NPV is just the plain sum of the cash flows.', ex: ['IRR is 14%. Is NPV at 10% positive or negative?', ['10% < 14% (IRR)'], 'Positive — cut every negative option at once.'], ch: ['fnd-p3-ch04'] },
    { id: 'qa-cisi', s: 'qa', n: 'CI − SI for 2 years', r: 'For 2 years, Compound interest − Simple interest = P × (r ÷ 100)².', ex: ['P = ₹10,000, r = 10% a year. CI − SI for 2 years?', ['10,000 × (0.1)²', '= 10,000 × 0.01'], '₹100'], ch: ['fnd-p3-ch04'] },
    { id: 'qa-ncr', s: 'qa', n: 'nCr symmetry', r: 'nCr = nC(n − r). Always work with the smaller r. nC1 = n and nC2 = n(n − 1) ÷ 2.', ex: ['20C18 = ?', ['20C18 = 20C2', '20 × 19 ÷ 2'], '190'], ch: ['fnd-p3-ch05'] },
    { id: 'qa-log', s: 'qa', n: 'Digits from logs', r: 'Number of digits in N = (whole part of log N) + 1. Remember log 2 ≈ 0.3010 and log 3 ≈ 0.4771.', ex: ['How many digits does 2¹⁰ have?', ['log 2¹⁰ = 10 × 0.3010 = 3.010', 'Whole part 3, plus 1'], '4 digits (2¹⁰ = 1,024).'], ch: ['fnd-p3-ch01'] },
    { id: 'qa-prob', s: 'qa', n: '"At least one" = 1 − none', r: 'P(at least one) = 1 − P(none). Much faster than adding every case.', ex: ['Three fair coins are tossed. P(at least one head)?', ['P(no head) = ½ × ½ × ½ = ⅛', '1 − ⅛'], '⅞'], ch: ['fnd-p3-ch15', 'fnd-p3-ch16'] },
    { id: 'qa-reg', s: 'qa', n: 'r from the two regression coefficients', r: 'r = ±√(byx × bxy), with the same sign as the coefficients. Both coefficients have the same sign, and their product cannot be more than 1.', ex: ['byx = 0.8 and bxy = 0.45. Find r.', ['0.8 × 0.45 = 0.36', '√0.36 = 0.6, sign positive'], 'r = 0.6'], ch: ['fnd-p3-ch17'] },
    { id: 'qa-dir', s: 'qa', n: 'Direction: use 3-4-5', r: 'Draw the moves as arrows and cancel opposite moves. The straight distance is √(east–west² + north–south²); 3-4-5 and 6-8-10 come up often.', ex: ['Walk 6 km north, 5 km east, 2 km south, 2 km west. Distance from start?', ['North–south: 6 − 2 = 4 km north', 'East–west: 5 − 2 = 3 km east', '√(4² + 3²)'], '5 km (north-east of the start).'], ch: ['fnd-p3-ch10'] },
    { id: 'qa-blood', s: 'qa', n: 'Blood relations: draw a mini tree', r: 'Draw generations as rows, use + for male and − for female, and = for a married couple. Never solve blood relations in your head.', ex: ['"A is the only son of B\'s father." How is A related to B?', ['B\'s father has only one son, A', 'B is not that son, so B must be a daughter'], 'A is B\'s brother.'], ch: ['fnd-p3-ch12', 'fnd-p3-ch11'] },
    { id: 'qa-index', s: 'qa', n: 'Index number quick check', r: 'Price index = (current price ÷ base price) × 100. An index of 125 means prices are up 25% from the base, not 125%.', ex: ['Base year price ₹80, current ₹100. Index?', ['100 ÷ 80 × 100'], '125 (a 25% rise).'], ch: ['fnd-p3-ch18'] },

    { id: 'eco-elas', s: 'eco', n: 'Elasticity: sign and size', r: 'Price elasticity of demand is negative for normal goods — compare the size (ignore the minus). More than 1 = elastic, less than 1 = inelastic, exactly 1 = unitary, 0 = perfectly inelastic.', ex: ['Price falls 10%, demand rises 5%. Type of demand?', ['e = 5 ÷ 10 = 0.5 (size)', '0.5 < 1'], 'Inelastic.'], ch: ['fnd-p4-ch02'] },
    { id: 'eco-outlay', s: 'eco', n: 'Total outlay test', r: 'Watch total spending (P × Q): price and spending move in opposite directions → elastic; same direction → inelastic; spending unchanged → unitary.', ex: ['Price rises; total spending on the good stays the same.', ['Spending unchanged'], 'Unitary elastic demand.'], ch: ['fnd-p4-ch02'] },
    { id: 'eco-cross', s: 'eco', n: 'Cross and income elasticity signs', r: 'Cross elasticity: + means substitutes, − means complements, 0 means unrelated. Income elasticity below 0 means an inferior good.', ex: ['Price of tea up, demand for coffee up. Relation?', ['Positive cross elasticity'], 'Substitutes.'], ch: ['fnd-p4-ch02'] },
    { id: 'eco-mr', s: 'eco', n: 'MR = AR (1 − 1/e)', r: 'With e as a positive number: at e = 1, MR = 0; when e < 1, MR is negative. So a monopolist never produces on the inelastic part of demand.', ex: ['Price ₹20, elasticity 2. MR?', ['20 × (1 − ½)'], '₹10'], ch: ['fnd-p4-ch04'] },
    { id: 'eco-cost', s: 'eco', n: 'Cost curve shortcuts', r: 'MC cuts AVC and AC at their lowest points. AFC keeps falling as output rises. AC − AVC = AFC.', ex: ['At 10 units AC is ₹15 and AVC is ₹12. Total fixed cost?', ['AFC = 15 − 12 = ₹3', 'TFC = 3 × 10'], '₹30'], ch: ['fnd-p4-ch03'] },
    { id: 'eco-mult', s: 'eco', n: 'Investment multiplier', r: 'k = 1 ÷ (1 − MPC) = 1 ÷ MPS. Change in income = k × change in investment.', ex: ['MPC = 0.8. Investment rises ₹100 crore. Income rises by?', ['k = 1 ÷ 0.2 = 5', '5 × 100'], '₹500 crore'], ch: ['fnd-p4-ch05'] },
    { id: 'eco-ni', s: 'eco', n: 'National income chain', r: 'GDP at MP − depreciation = NDP at MP. NDP at MP − net indirect taxes = NDP at FC. NDP at FC + net factor income from abroad = NNP at FC (national income).', ex: ['NDP at MP 900, net indirect taxes 100, NFIA −20. National income?', ['900 − 100 = 800 (NDP at FC)', '800 + (−20)'], '780'], ch: ['fnd-p4-ch05'] },
    { id: 'eco-money', s: 'eco', n: 'Simple money multiplier', r: 'In the simple version (no extra cash held by people), money multiplier = 1 ÷ reserve ratio. A higher reserve ratio means less credit.', ex: ['Reserve ratio 10%. New deposit ₹1,000. Maximum total deposits?', ['Multiplier = 1 ÷ 0.10 = 10', '10 × 1,000'], '₹10,000'], ch: ['fnd-p4-ch08'] },

    { id: 'acc-eqn', s: 'acc', n: 'Accounting equation filter', r: 'Assets = Liabilities + Capital after every transaction. Any option that makes one side change without the other is wrong.', ex: ['Owner withdraws ₹5,000 cash. Effect?', ['Cash (asset) −5,000', 'Capital −5,000'], 'Assets and capital both fall by ₹5,000.'], ch: ['fnd-p1-ch02', 'fnd-p1-ch01'] },
    { id: 'acc-dep', s: 'acc', n: 'SLM and WDV in one line', r: 'SLM: (Cost − scrap) ÷ life, the same every year. WDV: book value after n years = Cost × (1 − rate)ⁿ.', ex: ['Machine ₹1,00,000, WDV 10%. Book value after 2 years?', ['1,00,000 × 0.9 × 0.9'], '₹81,000'], ch: ['fnd-p1-ch05'] },
    { id: 'acc-gp', s: 'acc', n: 'Profit on cost ↔ on sales', r: 'x% on cost = x ÷ (100 + x) on sales. y% on sales = y ÷ (100 − y) on cost. 25% on cost = 20% on sales.', ex: ['Goods costing ₹80,000 sold at 25% profit on cost. Profit as % of sales?', ['25 ÷ 125 = 20%'], '20% of sales (₹20,000 on ₹1,00,000).'], ch: ['fnd-p1-ch09', 'fnd-p1-ch07', 'fnd-p1-ch04'] },
    { id: 'acc-brs', s: 'acc', n: 'BRS add or less', r: 'Starting from the cash book (debit) balance: anything that makes the bank balance higher than the book is added; anything that makes it lower is subtracted.', ex: ['Cheques issued ₹3,000 not yet presented. Starting from the cash book balance?', ['Bank has not paid them yet → bank balance is higher'], 'Add ₹3,000.'], ch: ['fnd-p1-ch03'] },
    { id: 'acc-ratio', s: 'acc', n: 'Sacrificing and gaining ratio', r: 'Sacrificing ratio = old share − new share (used on admission). Gaining ratio = new share − old share (used on retirement or death).', ex: ['A : B were 3 : 2; after C joins, A : B : C = 5 : 3 : 2. Sacrifice of A?', ['3/5 − 5/10 = 6/10 − 5/10'], '1/10'], ch: ['fnd-p1-ch10'] },
    { id: 'acc-tb', s: 'acc', n: 'Errors the trial balance hides', r: 'Errors of omission, commission (right amount, wrong account of the same side), principle and compensating errors do NOT disturb the trial balance. One-sided errors do.', ex: ['A credit purchase is not recorded at all. Will the trial balance agree?', ['Both sides are missing equally'], 'Yes — it still agrees.'], ch: ['fnd-p1-ch02'] },
    { id: 'acc-forf', s: 'acc', n: 'Forfeiture and re-issue', r: 'Forfeited amount = money received on the forfeited shares towards share capital. Loss on re-issue is met from it; what is left on re-issued shares goes to capital reserve.', ex: ['100 shares forfeited after ₹6 a share received; re-issued at ₹8 as ₹10 paid up. Capital reserve?', ['Forfeited: 100 × 6 = ₹600', 'Loss on re-issue: 100 × 2 = ₹200', '600 − 200'], '₹400'], ch: ['fnd-p1-ch11'] },
    { id: 'acc-npo', s: 'acc', n: 'NPO: capital or revenue first', r: 'Decide the nature of every receipt before drawing up accounts: legacies and specific donations go to the balance sheet (capital); subscriptions and general donations go to income and expenditure.', ex: ['A club receives a legacy of ₹50,000. Where does it go?', ['Legacy = capital receipt'], 'Added to the capital fund in the balance sheet.'], ch: ['fnd-p1-ch08'] },

    { id: 'law-void', s: 'law', n: 'Void or voidable? Trigger words', r: 'Coercion, undue influence, fraud, misrepresentation → voidable at the option of the person wronged. Minor, unlawful object, uncertain terms, wagering, restraint of marriage or trade → void.', ex: ['A signs a contract because B threatens to harm him. Status?', ['Trigger: threat = coercion'], 'Voidable at A\'s option.'], ch: ['fnd-p2-ch02'] },
    { id: 'law-minor', s: 'law', n: 'Minor\'s agreement', r: 'An agreement with a minor is void from the start and cannot be ratified on becoming major. For necessaries supplied, the supplier is paid only from the minor\'s property — the minor is not personally liable.', ex: ['A minor borrows money and, on turning 18, promises to repay. Is the promise enforceable?', ['Original agreement void', 'Void agreements cannot be ratified'], 'No.'], ch: ['fnd-p2-ch02'] },
    { id: 'law-cw', s: 'law', n: 'Condition or warranty?', r: 'Breach of a condition (goes to the root) → buyer may reject the goods. Breach of a warranty (side term) → damages only. "Sale" = ownership passes now; "agreement to sell" = it passes later.', ex: ['A car sold as "diesel" turns out to be petrol. Remedy?', ['Fuel type goes to the root of the deal → condition'], 'The buyer may reject the car.'], ch: ['fnd-p2-ch03'] },
    { id: 'law-ni', s: 'law', n: 'Count the parties', r: 'Bill of exchange: 3 parties (drawer, drawee, payee). Promissory note: 2 parties (maker, payee). Cheque: a bill drawn on a named banker, payable on demand.', ex: ['An instrument with a maker and a payee only is a…', ['2 parties'], 'Promissory note.'], ch: ['fnd-p2-ch07'] },
    { id: 'law-agency', s: 'law', n: 'True test of partnership', r: 'Sharing profits alone does not make a partnership. The real test is mutual agency: the business is carried on by all or any of them acting for all.', ex: ['A lender takes a share of profits instead of interest. Is he a partner?', ['No mutual agency'], 'No.'], ch: ['fnd-p2-ch04', 'fnd-p2-ch05'] },

    { id: 'gen-odd', s: 'gen', n: 'NOT / EXCEPT = odd one out', r: 'Three options are true and alike; find the one that is different. Mark each option T or F — the single F is the answer. Circle the word NOT before you start.', ex: ['Which is NOT a feature of a company? (a) separate legal entity (b) perpetual succession (c) unlimited liability of members (d) common seal', ['(a), (b), (d) are features', '(c) is the odd one'], '(c)'], ch: [] },
    { id: 'gen-stmt', s: 'gen', n: 'Statement questions: one wrong statement kills options', r: 'Judge one statement at a time. As soon as one statement is false, cut every option that includes it. Usually you need to check only two statements.', ex: ['(i) GST is an indirect tax. (ii) Income tax is an indirect tax. Options: (a) both (b) only i (c) only ii (d) neither', ['(ii) is false → cut (a) and (c)', '(i) is true → cut (d)'], '(b)'], ch: [] },
    { id: 'gen-last', s: 'gen', n: 'Read the last line first', r: 'Long question? Read the final line (what is asked) first, then read the data looking only for what you need. Saves 10–20 seconds a question.', ex: ['A 6-line case ends with "Find the gaining ratio".', ['Look only for old and new ratios'], 'Ignore the rest of the figures.'], ch: [] },
    { id: 'gen-est', s: 'gen', n: 'Estimate before you calculate', r: 'Round the figures and get a rough answer. If the options are far apart, the estimate alone picks the answer.', ex: ['₹4,96,000 × 9.8% ≈ ? Options: 4,861 · 48,608 · 4,86,080 · 486', ['≈ 5,00,000 × 10% = 50,000'], '48,608'], ch: [] },
    { id: 'gen-neg', s: 'gen', n: 'Negative marking maths (−¼)', r: 'A pure guess between 4 options gains only about 0.06 marks on average. Cut 1 option: +0.17. Cut 2 options: +0.38. So guess when you can cut at least 2 options; otherwise skip and use the time elsewhere.', ex: ['You can rule out two options and are unsure between the other two.', ['½ × 1 − ½ × ¼ = 0.375'], 'Guess — it is worth about +0.38 marks on average.'], ch: [] },

    { id: 'calc-mem', s: 'calc', n: 'M+ for totals of products', r: 'Sums like Σfx: multiply each pair and press M+ instead of =. At the end press MR for the total. No paper needed.', ex: ['Σfx for (x 10, f 3), (x 20, f 5)?', ['10 × 3 M+', '20 × 5 M+', 'MR'], '130'], ch: ['fnd-p3-ch14', 'fnd-p3-ch13', 'fnd-p3-ch17'] },
    { id: 'calc-pow', s: 'calc', n: 'Powers with repeat =', r: 'On StudyVerse\'s calculator (and most desk calculators): type 1.1 × = to get 1.1², then each = multiplies by 1.1 again. Great for (1 + r)ⁿ.', ex: ['(1.1)⁴ = ?', ['1.1 × = → 1.21', '= → 1.331', '= → 1.4641'], '1.4641'], ch: ['fnd-p3-ch04', 'fnd-p3-ch06'] },
    { id: 'calc-pv', s: 'calc', n: 'Discount factors with ÷ =', r: 'Type 1.1 ÷ = to get 1 ÷ 1.1; each further = divides by 1.1 again. Each display is the next year\'s discount factor at 10%.', ex: ['Discount factors at 10% for years 1–3?', ['1.1 ÷ = → 0.9091', '= → 0.8264', '= → 0.7513'], '0.9091, 0.8264, 0.7513'], ch: ['fnd-p3-ch04'] },
    { id: 'calc-pct', s: 'calc', n: 'Add or remove % in one go', r: 'Amount + 18% = amount × 1.18. To remove 18% GST from a price that includes it, divide by 1.18 (not × 0.82).', ex: ['Price including 18% GST is ₹1,180. Price before GST?', ['1,180 ÷ 1.18'], '₹1,000'], ch: ['fnd-p3-ch04', 'fnd-p1-ch02'] },
  ];
  const trickById = id => TRICKS.find(t => t.id === id);
  const GNAME = Object.fromEntries(GROUPS);

  /* ================= 1. ⚡ Fast way: question type → smart tip ================= */
  const isNum = o => { const s = String(o).replace(/₹|rs\.?|inr|crore|lakhs?|years?|months?|days?|units?|times|km|per cent|%|,|\s/gi, ''); return /^[-−+]?\d*\.?\d+(\/\d+)?$/.test(s) || /^\d+(:\d+)+$/.test(s); };
  function kind(q, key) {
    const s = String(q.q || ''), opts = (q.options || []).map(String);
    if (/\bstatements?\b|\(i\)|\(ii\)|\bassertion\b/i.test(s) || opts.filter(o => /\b(both|neither|only)\b.*\b(i|ii|1|2|a|b)\b/i.test(o)).length >= 2) return 'stmt';
    if (/\b(NOT|EXCEPT)\b/.test(s) || /\b(not|except|incorrect|false|untrue|odd one|wrong)\b/i.test(s)) return 'not';
    if (opts.filter(isNum).length >= 3) return 'num';
    if (paperOf(key) === 'fnd-p2') return 'law';
    return 'concept';
  }
  const TIPS = {
    num: ['Numbers in the options — do not solve from scratch.', ['Estimate: round the figures; often only one option is close.', 'Back-solve: put an option into the question and check it. Start with the middle value.', 'Check the last digit of a product to cut options fast.']],
    not: ['NOT / EXCEPT question — find the odd one out.', ['Circle the word NOT so you do not flip it.', 'Mark each option T or F.', 'The single F (or the one that does not fit) is the answer.']],
    stmt: ['Statement question — one wrong statement cuts options.', ['Judge one statement at a time.', 'If a statement is wrong, cut every option that includes it.', 'Often two checks are enough.']],
    law: ['Law MCQ — find the trigger word in the facts.', ['Look for words like minor, coercion, fraud, consideration, delivery, condition.', 'Each trigger points to one rule (e.g. coercion → voidable, minor → void).', 'Cut options that use the wrong rule.']],
    concept: ['Concept question — read what is asked, then cut.', ['Read the last line first: what exactly is asked?', 'Cut the two options that are clearly off.', 'Pick between the last two using the key word of the definition.']],
  };
  const KIND_TRICK = { num: ['qa-back', 'gen-est', 'qa-units'], not: ['gen-odd'], stmt: ['gen-stmt'], law: ['law-void'], concept: ['gen-last'] };
  function related(q, key) {
    const ch = chOf(key), k = kind(q, key);
    const ids = TRICKS.filter(t => t.ch.includes(ch)).map(t => t.id);
    (KIND_TRICK[k] || []).forEach(id => { if (!ids.includes(id)) ids.push(id); });
    return ids.slice(0, 4);
  }
  function fastHTML(q, key, tgt) {
    const k = kind(q, key), own = q.fast, t = tgt || target(q);
    const body = own ? (Array.isArray(own) ? `<ol class="sp-ol">${own.map(x => `<li>${esc(x)}</li>`).join('')}</ol>` : `<p class="sp-p">${esc(own)}</p>`)
      : `<p class="sp-p"><b>${esc(TIPS[k][0])}</b></p><ol class="sp-ol">${TIPS[k][1].map(x => `<li>${esc(x)}</li>`).join('')}</ol>`;
    const rel = related(q, key);
    return `<div class="sp-fastin"><span class="ca-k">⚡ Fast way${own ? '' : ' · smart tip'}</span>${body}
      <p class="sp-tgt">Target: <b>${t} s</b> for this question${t === TARGET ? ' (100 MCQs in 2 hours = 72 s each)' : ''}.</p>
      ${rel.length ? `<div class="sp-rel"><span class="ca-note">Tricks that help:</span> ${rel.map(id => `<button type="button" class="sp-tchip" data-sptrick="${id}">💡 ${esc(trickById(id).n)}</button>`).join('')}</div>` : ''}</div>`;
  }

  /* ================= 2. pacing chip ================= */
  let tick = null;
  const paceTxt = (s, t) => `⏱ <b>${s}</b> s / ${t} s`;
  function bar(q, ctx = {}) {
    const t = ctx.target || target(q);
    return `<div class="sp-row" data-sp data-t="${t}"><span class="sp-pace" role="timer" aria-label="Seconds on this question, target ${t}">${paceTxt(0, t)}</span>
      <button type="button" class="sp-btn" data-spfast aria-expanded="false" aria-label="Fast way: a quick method for this question${ctx.answered ? '' : ' (no penalty)'}">⚡ Fast way</button>
      ${Array.isArray(q.keys) && q.keys.length ? '<button type="button" class="sp-btn" data-spkeys aria-label="Watch the calculator keys for this question">🧮 Watch the keys</button>' : ''}</div>
      <div class="sp-fastbox" data-spbox hidden></div>`;
  }
  function paint(row, secs) {
    const t = +row.dataset.t, chip = row.querySelector('.sp-pace'); if (!chip) return;
    chip.innerHTML = paceTxt(secs, t);
    chip.classList.toggle('warn', secs > t * .75 && secs <= t); chip.classList.toggle('over', secs > t);
  }
  /* ctx: { key, base: ms already spent, done: final ms (answered) or null, target? } */
  function wire(host, q, ctx = {}) {
    const row = host && host.querySelector('[data-sp]'); if (!row) return;
    const box = host.querySelector('[data-spbox]'), fb = row.querySelector('[data-spfast]'), kb = row.querySelector('[data-spkeys]');
    const t0 = Date.now() - (ctx.base || 0);
    clearInterval(tick); tick = null;
    if (ctx.done != null) { paint(row, Math.round(ctx.done / 1000)); row.querySelector('.sp-pace').classList.add('done'); }
    else { paint(row, Math.round((ctx.base || 0) / 1000)); tick = setInterval(() => { if (!row.isConnected || row.dataset.frozen) { clearInterval(tick); tick = null; return; } paint(row, Math.floor((Date.now() - t0) / 1000)); }, 1000); }
    fb.onclick = () => { const open = box.hidden; if (open && !box.firstChild) box.innerHTML = fastHTML(q, ctx.key, +row.dataset.t); box.hidden = !open; fb.setAttribute('aria-expanded', String(open)); tap('tap'); if (open) wireBox(box); };
    if (kb) kb.onclick = () => replay(q);
  }
  function wireBox(box) { box.querySelectorAll('[data-sptrick]').forEach(b => b.onclick = () => tricks(b.dataset.sptrick)); }
  /* after an answer: freeze the chip, say how the time compares, open the fast way when it was slow or wrong */
  function answered(host, q, ctx = {}) {
    const row = host && host.querySelector('[data-sp]'); if (!row) return;
    clearInterval(tick); tick = null; row.dataset.frozen = 1;
    const t = +row.dataset.t, s = Math.round((ctx.ms || 0) / 1000); paint(row, s);
    const chip = row.querySelector('.sp-pace'); chip.classList.add('done');
    const slow = s > t;
    chip.insertAdjacentHTML('afterend', `<span class="sp-verdict ${slow ? 'slow' : 'fast'}">${slow ? `🐢 ${s - t} s over${ctx.ok ? ' — added to ⚡ Speed drill' : ''}` : `✓ within ${t} s`}</span>`);
    if (!ctx.ok || slow) { const fb = row.querySelector('[data-spfast]'), box = host.querySelector('[data-spbox]'); if (fb && box && box.hidden) fb.click(); }
  }

  /* ---------- speed list (correct but slow) ---------- */
  function note(key, ok, ms, q, noSave) {
    if (!key || /#gen-/.test(key) || !ok) return;               // wrong answers already go to "Revise these"
    const c = C(), t = target(q), s = Math.round((ms || 0) / 1000);
    if (s > t) { const e = c.speed[key] || { n: 0 }; c.speed[key] = { d: today(), s, t, n: e.n + 1 }; }
    else if (c.speed[key]) delete c.speed[key];
    if (!noSave) save();
  }
  async function findQ(key) {
    if (window.CaKeys && /#ky-/.test(key)) { const o = CaKeys.ownQ(key); return o ? { q: o.q, uid: o.uid } : null; }   // key-rule MCQs (js/ca-keys.js)
    const [uid, qid] = String(key).split('#'); let d = null; try { d = await X.unitData(uid); } catch (e) {} if (!d) return null;
    const q = (d.mcqs || []).find(x => x.id === qid); if (q) return { q, uid };
    for (const cs of d.cases || []) { const m = cs.mcqs.find(x => x.id === qid); if (m) return { q: m, uid, cs }; }
    return null;
  }
  const backBtn = (label, fn) => { const b = D.createElement('button'); b.className = 'back'; b.textContent = '← ' + label; b.onclick = fn; return b; };
  const toHub = () => (T() ? T().practiceHub() : Ca.home());
  async function drill() {
    const el = X.open('practice'); el.innerHTML = '<p class="ca-load">Loading your speed drill…</p>';
    const c = C(), keys = Object.keys(c.speed), found = [];
    for (const k of keys) { const f = await findQ(k); if (f) found.push({ k, ...f }); else delete c.speed[k]; }
    const names = {}; for (const f of found) { try { const x = X.findUnit(await X.structure(X.levelOf(f.uid)), f.uid); if (x) names[f.uid] = x; } catch (e) {} }
    el.innerHTML = ''; el.appendChild(backBtn('Practice', toHub));
    el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">⚡ Speed drill</h1>
      <div class="card"><p class="ca-p">${found.length ? `${found.length} question${found.length > 1 ? 's' : ''} you got right, but slower than the target. Beat the target and the question leaves this list.` : 'Nothing here yet. Questions you answer correctly but slower than the target (72 s, or the question\'s own target) appear here.'}</p>
        <p class="ca-note">Paper 3 and Paper 4 give you 2 hours for 100 MCQs — 72 seconds each. Open ⚡ Fast way on each question to learn the quick method.</p>
        ${found.length ? '<button class="btn" id="spDrillGo">Drill all ▶</button>' : '<button class="btn" id="spDrillTricks">💡 Learn shortcut tricks</button>'}</div>
      ${found.length ? `<div class="card"><ul class="ca-rvl">${found.map(f => { const s = c.speed[f.k]; const x = names[f.uid]; return `<li><span><b>${esc(f.q.q)}</b><small>${esc(x ? `${X.paperLabel(x.p)} · Ch ${x.c.n} · ${x.u.title}` : f.uid)} · your time <b>${s.s} s</b> · target ${s.t} s${s.n > 1 ? ` · slow ${s.n}×` : ''}</small></span><button class="ca-x" data-spk="${esc(f.k)}" aria-label="Remove from speed drill">✕</button></li>`; }).join('')}</ul></div>` : ''}`);
    const g = D.getElementById('spDrillGo');
    if (g) g.onclick = () => {
      const items = found.map(f => { const x = names[f.uid]; return { q: f.q, key: f.k, uid: f.uid, cs: f.cs, ch: chOf(f.k), chTitle: x ? `Ch ${x.c.n}: ${x.c.title}` : '' }; });
      if (T() && T().startSet) T().startSet(items, { mode: 'practice', perQ: 0, title: '⚡ Speed drill', again: drill, againLabel: 'Back to the speed drill' });
    };
    const tb = D.getElementById('spDrillTricks'); if (tb) tb.onclick = () => tricks();
    el.querySelectorAll('[data-spk]').forEach(b => b.onclick = () => { delete C().speed[b.dataset.spk]; save(); drill(); });
  }

  /* ================= 3. tricks screen ================= */
  async function tricks(focus, grp) {
    const el = X.open('practice'); const ft = focus && trickById(focus); grp = grp || 'all';
    let st = null; try { st = await X.structure('foundation'); } catch (e) {}
    const chName = {}, chUnit = {}; if (st) st.papers.forEach(p => p.chapters.forEach(ch => { chName[ch.id] = `${X.paperLabel(p).replace('Paper ', 'P')} Ch ${ch.n}: ${ch.title}`; const u = ch.units.find(u => u.status === 'built'); if (u) chUnit[ch.id] = u.id; }));
    const list = TRICKS.filter(t => grp === 'all' || t.s === grp);
    el.innerHTML = ''; el.appendChild(backBtn('Practice', toHub));
    el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">💡 Shortcut tricks</h1>
      <div class="card"><p class="ca-p">${TRICKS.length} quick methods for CA Foundation MCQs, each with a worked mini example. Learn one a day; use them in ⚡ Speed drill.</p>
        <div class="ca-chipsel" role="group" aria-label="Show tricks for">${[['all', 'All']].concat(GROUPS).map(([k, n]) => `<button type="button" class="ca-cs" aria-pressed="${grp === k}" data-spg="${k}">${esc(n)} <small>${k === 'all' ? TRICKS.length : TRICKS.filter(t => t.s === k).length}</small></button>`).join('')}</div></div>
      <div class="sp-tlist">${list.map(t => `<details class="card sp-trick" id="spT-${t.id}" ${ft && ft.id === t.id ? 'open' : ''}><summary><span class="sp-tg">${esc(GNAME[t.s])}</span><b>${esc(t.n)}</b><small>${esc(t.r.length > 90 ? t.r.slice(0, 87) + '…' : t.r)}</small></summary>
        <p class="ca-p">${esc(t.r)}</p>
        <div class="sp-ex"><span class="ca-k">Worked example</span><p class="ca-p"><b>${esc(t.ex[0])}</b></p><ol class="sp-ol">${t.ex[1].map(s => `<li>${esc(s)}</li>`).join('')}</ol><p class="sp-ans">Answer: <b>${esc(t.ex[2])}</b></p></div>
        ${t.ch.length ? `<div class="sp-rel"><span class="ca-note">Use it in:</span> ${t.ch.map(ch => chUnit[ch] ? `<button type="button" class="sp-tchip" data-spu="${chUnit[ch]}">${esc(chName[ch] || ch)} ▶</button>` : `<span class="sp-tchip off">${esc(chName[ch] || ch)}</span>`).join('')}</div>` : '<p class="ca-note">Works in every paper.</p>'}</details>`).join('')}</div>
      <p class="ca-note ca-onDark2">StudyVerse's own tricks and examples — check each rule's conditions before using it in the exam.</p>`);
    el.querySelectorAll('[data-spg]').forEach(b => b.onclick = () => { tap('tap'); tricks(null, b.dataset.spg); });
    el.querySelectorAll('[data-spu]').forEach(b => b.onclick = () => { tap('open'); Ca.unit(b.dataset.spu, 'mcq'); });
    if (ft) { const d = D.getElementById('spT-' + ft.id); if (d) setTimeout(() => { d.scrollIntoView({ block: 'start', behavior: reduced() ? 'auto' : 'smooth' }); const s = d.querySelector('summary'); if (s) s.focus({ preventScroll: true }); }, 60); }
  }

  /* ================= 4. calculator replay ================= */
  const KEYLAB = { '*': '×', '/': '÷', '-': '−', '+': '+', '=': '=', sqrt: '√', neg: '±', back: '⌫', '%': '%', AC: 'AC', C: 'C', sq: 'x²', pow: 'xʸ', recip: '1/x', pi: 'π', '(': '(', ')': ')' };
  let replaying = null;
  async function replay(q) {
    if (!window.Calc || !Calc.open) { toast('The calculator is not available'); return; }
    const keys = (q.keys || []).map(String).flatMap(k => (/^[\d.]+$/.test(k) && k.length > 1 && k !== '00' ? k.split('') : [k])), sci = q.keysMode === 'sci', n = keys.length; if (!n) return;   // "1.1" is typed key by key
    if (replaying) replaying.stop = true;
    const run = replaying = { stop: false };
    const wait = ms => new Promise(r => setTimeout(r, reduced() ? Math.min(ms, 250) : ms));
    try { Calc.open({ mode: sci ? 'sci' : 'basic' }); Calc.reset(); } catch (e) { toast('The calculator could not start'); return; }
    const coach = (i, msg, end) => {
      const c = Calc.coach(`<div class="cxc-top"><span>🧮 Key replay</span><span>${Math.min(i, n)}/${n}</span></div><div>${msg}</div>
        <div class="sp-cxkeys" aria-hidden="true">${keys.map((k, j) => `<i class="${j < i ? 'd' : j === i && !end ? 'c' : ''}">${esc(KEYLAB[k] || k)}</i>`).join('')}</div>
        <button type="button" class="cxc-hint" data-spstop>${end ? '🔁 Replay again' : '⏹ Stop'}</button>`);
      const b = c && c.querySelector('[data-spstop]'); if (b) b.onclick = () => { if (end) replay(q); else { run.stop = true; Calc.hint([]); Calc.coach(null); } };
    };
    say(`Calculator replay, ${n} keys`);
    for (let i = 0; i < n; i++) {
      if (run.stop) return;
      const k = keys[i]; coach(i, `Press <b>${esc(KEYLAB[k] || k)}</b>`); Calc.hint([k]);
      await wait(750); if (run.stop) return;
      try { sci ? Calc._sciPress(k) : Calc._press(k); } catch (e) {}
      await wait(300);
    }
    if (run.stop) return;
    Calc.hint([]); let v = ''; try { const s = Calc.state(); v = s && isFinite(s.value) ? (Calc.math && Calc.math.fmt ? Calc.math.fmt(s.value) : String(s.value)) : ''; } catch (e) {}
    coach(n, `Done${v ? ` — the display shows <b>${esc(v)}</b>` : ''}. Now try it yourself.`, true); say(`Replay done${v ? ', the display shows ' + v : ''}`);
    replaying = null;
  }

  /* ================= 5. 3-pass exam strategy ================= */
  const PASS1 = 45;
  function guideHTML(n) {
    return `<div class="card sp-guide"><span class="ca-k">3-pass mode · how it works</span><h2 class="ca-h2s">Answer in three passes</h2>
      <ol class="sp-passes"><li><b>Pass 1 — easy ones.</b> Answer if you can within about ${PASS1} s. If not, tap <b>🏷 Mark</b> and move on. Never get stuck.</li>
        <li><b>Pass 2 — marked ones.</b> Come back to the marked questions with the time you saved.</li>
        <li><b>Pass 3 — guess smartly.</b> Wrong answers cost ¼ mark. Guess only if you can cut at least 2 options; otherwise leave it blank.</li></ol>
      ${negTable()}
      <p class="ca-note">${n} questions · you can still jump to any question from the palette.</p></div>`;
  }
  function negTable() {
    return `<div class="ca-scroll" role="region" tabindex="0" aria-label="Value of a guess with −¼ marking"><table class="ca-t sp-neg"><thead><tr><th scope="col">Options you can cut</th><th scope="col">Chance of being right</th><th scope="col" class="n">Average marks from a guess</th></tr></thead>
      <tbody><tr><td>None (pure guess)</td><td>1 in 4</td><td class="n">+0.06</td></tr><tr><td>1 option</td><td>1 in 3</td><td class="n">+0.17</td></tr><tr class="sp-go"><td>2 options ✓ guess</td><td>1 in 2</td><td class="n">+0.38</td></tr></tbody></table></div>
      <p class="ca-note">A pure guess is almost worth nothing and is risky; the rule "cut 2, then guess" keeps the gain and cuts the risk.</p>`;
  }
  const PASSTIP = {
    1: `Pass 1 — answer the easy ones (about ${PASS1} s each). Not sure? Tap 🏷 Mark and move on.`,
    2: 'Pass 2 — your marked questions. Use the time you saved, but keep moving.',
    3: 'Pass 3 — left over. Guess only if you can cut at least 2 options; otherwise leave it blank (no penalty).',
  };
  /* res: [{ ok, skip, pass, ms, m (marks) }], neg: −¼ marking on */
  function breakdownHTML(res, neg) {
    const rows = [1, 2, 3].map(p => { const r = res.filter(x => !x.skip && x.pass === p); const ok = r.filter(x => x.ok).length, w = r.length - ok;
      const mk = r.reduce((a, x) => a + (x.ok ? x.m : neg ? -x.m / 4 : 0), 0), ms = res.reduce((a, x) => a + (x.pms ? x.pms[p] || 0 : 0), 0);
      return { p, n: r.length, ok, w, mk: Math.round(mk * 100) / 100, s: Math.round(ms / 1000) }; });
    const skip = res.filter(x => x.skip).length, p3 = rows[2];
    return `<div class="card sp-break"><h3 class="ca-h3">3-pass breakdown</h3><div class="ca-scroll" role="region" tabindex="0" aria-label="Results by pass"><table class="ca-t"><thead><tr><th scope="col">Pass</th><th scope="col" class="n">Answered</th><th scope="col" class="n">Right</th><th scope="col" class="n">Wrong</th><th scope="col" class="n">Marks</th><th scope="col" class="n">Time</th></tr></thead>
      <tbody>${rows.map(r => `<tr><td>${['', '1 · easy', '2 · marked', '3 · guesses'][r.p]}</td><td class="n">${r.n}</td><td class="n">${r.ok}</td><td class="n">${r.w}</td><td class="n">${r.mk > 0 ? '+' : ''}${r.mk}</td><td class="n">${Math.floor(r.s / 60)}:${String(r.s % 60).padStart(2, '0')}</td></tr>`).join('')}
      <tr><td>Left blank</td><td class="n">${skip}</td><td class="n">–</td><td class="n">–</td><td class="n">0</td><td class="n">–</td></tr></tbody></table></div>
      <p class="ca-p">${p3.n ? (p3.mk >= 0 ? `Your pass-3 guesses earned ${p3.mk} marks — smart guessing paid off.` : `Your pass-3 guesses lost ${-p3.mk} marks. Guess only after cutting 2 options.`) : 'No guesses in pass 3.'}${rows[0].n && rows[0].s / rows[0].n > PASS1 ? ` Pass 1 took ${Math.round(rows[0].s / rows[0].n)} s a question — mark sooner.` : ''}</p></div>`;
  }

  /* ================= 6. speed report card (CA dashboard) ================= */
  function speedData() {
    const c = C(), log = c.mlog.slice(-800), by = {};
    log.forEach(([m, key, ok, s]) => { const p = paperOf(key); if (!SUBJ[p] || !(s > 0)) return; const b = by[p] = by[p] || { n: 0, s: 0, ok: 0, ch: {} }; b.n++; b.s += s; if (ok) b.ok++;
      const ch = chOf(key), x = b.ch[ch] = b.ch[ch] || { n: 0, s: 0 }; x.n++; x.s += s; });
    const rows = Object.entries(by).map(([p, b]) => ({ p, key: SUBJ[p][0], name: SUBJ[p][1], n: b.n, avg: b.s / b.n, acc: b.ok / b.n, ch: b.ch })).sort((a, b) => a.p.localeCompare(b.p));
    const ready = rows.filter(r => r.n >= 5), slow = ready.slice().sort((a, b) => b.avg - a.avg)[0] || null;
    let top = [];
    if (slow) { const pool = TRICKS.filter(t => t.s === slow.key || (slow.key === 'qa' && t.s === 'calc'));
      const chAvg = id => { const x = slow.ch[id]; return x && x.n ? x.s / x.n : 0; };
      top = pool.map((t, i) => [t, Math.max(0, ...t.ch.map(chAvg)) - i * 0.01]).sort((a, b) => b[1] - a[1]).slice(0, 3).map(x => x[0]);
      if (top.length < 3) ['gen-est', 'gen-last', 'gen-odd'].forEach(id => { if (top.length < 3 && !top.includes(trickById(id))) top.push(trickById(id)); }); }
    return { rows, slow, top, speedN: Object.keys(c.speed).length };
  }
  function reportCard() {
    const d = speedData(), any = d.rows.some(r => r.n >= 1);
    const mx = Math.max(TARGET * 1.6, ...d.rows.map(r => r.avg));
    return `<section class="card ca-dcard sp-report" id="spReport"><h2 class="ca-h2s">⚡ Speed report card</h2>
      <p class="sub">Target: 72 s a question (Papers 3 and 4: 100 MCQs in 2 hours). For Papers 1 and 2 the MCQs are concept checks — the same pace is a good habit.</p>
      ${any ? `<div class="sp-rows">${d.rows.map(r => { const lost = (r.avg - TARGET) * 100 / 60, few = r.n < 5;
        return `<div class="sp-srow"><span class="sp-sname"><b>${esc(r.name)}</b><small>${r.n} answer${r.n === 1 ? '' : 's'} · ${Math.round(r.acc * 100)}% right${few ? ' · answer 5+ for a fair picture' : ''}</small></span>
          <span class="sp-sbar" aria-hidden="true"><i class="${r.avg > TARGET ? 'over' : 'ok'}" style="width:${Math.round(Math.min(1, r.avg / mx) * 100)}%"></i><em style="left:${Math.round(TARGET / mx * 100)}%"></em></span>
          <span class="sp-snum"><b>${Math.round(r.avg)} s</b><small class="${lost > 0 ? 'w' : 's'}">${lost > 0 ? `${Math.round(lost)} min lost` : `${Math.round(-lost)} min gained`} / 100 Qs</small></span></div>`; }).join('')}</div>
        ${d.slow ? `<h3 class="ca-h3">Top 3 tricks for ${esc(d.slow.name)} (your slowest)</h3><div class="sp-rel">${d.top.map(t => `<button type="button" class="sp-tchip" data-sptrick="${t.id}">💡 ${esc(t.n)}</button>`).join('')}</div>` : ''}`
      : '<p class="ca-p">Answer some MCQs — your average time per subject will appear here.</p>'}
      <div class="ca-btns"><button class="btn ghost" data-spgo="drill">⚡ Speed drill (${d.speedN})</button><button class="btn ghost" data-spgo="tricks">💡 Shortcut tricks</button></div>
      ${d.rows.length ? `<details class="ca-tview"><summary>Show as table</summary><div class="ca-scroll" role="region" tabindex="0" aria-label="Speed by subject"><table class="ca-t"><thead><tr><th scope="col">Subject</th><th scope="col" class="n">Answers</th><th scope="col" class="n">Avg seconds</th><th scope="col" class="n">Minutes over 100 Qs vs 72 s</th></tr></thead><tbody>${d.rows.map(r => `<tr><td>${esc(r.name)}</td><td class="n">${r.n}</td><td class="n">${Math.round(r.avg)}</td><td class="n">${Math.round((r.avg - TARGET) * 100 / 60)}</td></tr>`).join('')}</tbody></table></div></details>` : ''}</section>`;
  }
  function wireReport(host) {
    if (!host) return;
    host.querySelectorAll('#spReport [data-sptrick]').forEach(b => b.onclick = () => tricks(b.dataset.sptrick));
    host.querySelectorAll('#spReport [data-spgo]').forEach(b => b.onclick = () => (b.dataset.spgo === 'drill' ? drill() : tricks()));
  }

  /* ================= 7. 📌 Exam focus list — CA Foundation Paper 1 Accounting ================= */
  /* Chapters and units follow content/ca/foundation/structure.json (ICAI study material relevant for May 2027 onwards). */
  const FOCUS = [
    { t: 'Theoretical framework', u: 'fnd-p1-ch01-u02', ch: 'fnd-p1-ch01', more: [['fnd-p1-ch01-u03', 'Capital vs revenue'], ['fnd-p1-ch01-u04', 'Contingent items'], ['fnd-p1-ch01-u05', 'Accounting policies']],
      why: 'Short theory and true/false-with-reason questions come from here almost every time.', type: 'Theory (2–5 marks); classify an item as capital or revenue; true/false with reason.', hook: 'Assumptions hold up concepts; concepts hold up policies. Going concern, consistency, accrual — the three that are always assumed.' },
    { t: 'Journal, ledger and trial balance', u: 'fnd-p1-ch02-u01', ch: 'fnd-p1-ch02', more: [['fnd-p1-ch02-u02', 'Ledgers'], ['fnd-p1-ch02-u03', 'Trial balance'], ['fnd-p1-ch02-u05', 'Cash book']],
      why: 'The base of every other chapter, and journal entries are asked directly too (including GST entries).', type: 'Journal entries; post and balance accounts; cash book.', hook: 'Real: what comes in Dr. Personal: the receiver Dr. Nominal: expenses and losses Dr.' },
    { t: 'Rectification of errors', u: 'fnd-p1-ch02-u06', ch: 'fnd-p1-ch02',
      why: 'A regular 4–6 mark question, often with a suspense account.', type: 'Rectifying entries before and after the trial balance; suspense account.', hook: 'Cancel the wrong, then write the right — in one entry.' },
    { t: 'Bank reconciliation statement', u: 'fnd-p1-ch03-u01', ch: 'fnd-p1-ch03',
      why: 'Comes in most papers, 4–10 marks; marks go to the right add or less.', type: 'Prepare a BRS from given differences; amended cash book first, then BRS.', hook: 'Start from the book; if the bank is higher, add.' },
    { t: 'Inventories', u: 'fnd-p1-ch04-u01', ch: 'fnd-p1-ch04',
      why: 'Valuation rules are asked in theory and in final accounts.', type: 'FIFO / weighted average valuation; inventory on the balance sheet date; what to include in cost.', hook: 'Lower of cost and NRV — item by item. Selling costs stay out of cost.' },
    { t: 'Depreciation (SLM / WDV, change of method)', u: 'fnd-p1-ch05-u01', ch: 'fnd-p1-ch05',
      why: 'A machinery account with additions and a sale is a favourite 10-mark question.', type: 'Asset account over 3–4 years; profit or loss on sale; change in method or useful life.', hook: 'SLM = same amount; WDV = same rate. Sold asset: depreciate up to the date of sale first.' },
    { t: 'Bills of exchange and promissory notes', u: 'fnd-p1-ch06-u01', ch: 'fnd-p1-ch06',
      why: 'Appears often as a 5–8 mark entries question.', type: 'Entries in the books of drawer and drawee: discounting, dishonour, renewal, retirement.', hook: 'Draw the date line first: drawn → accepted → discounted → due (+3 days of grace).' },
    { t: 'Final accounts of sole proprietors', u: 'fnd-p1-ch07-u01', ch: 'fnd-p1-ch07', more: [['fnd-p1-ch07-u02', 'Manufacturing accounts']],
      why: 'A marks bank: every adjustment earns marks twice (P&L and balance sheet).', type: 'Trading and P&L account and balance sheet with 6–10 adjustments.', hook: 'Every adjustment touches two places — tick it twice.' },
    { t: 'Not-for-profit organisations', u: 'fnd-p1-ch08-u01', ch: 'fnd-p1-ch08',
      why: 'A 10–15 mark question appears often; marks are lost on capital vs revenue.', type: 'Receipts & payments → income & expenditure account and balance sheet; subscriptions.', hook: 'Receipts & payments = cash (all years). Income & expenditure = this year only.' },
    { t: 'Accounts from incomplete records', u: 'fnd-p1-ch09-u01', ch: 'fnd-p1-ch09',
      why: 'Step marks for each working note — even if the final figure is off.', type: 'Statement of affairs; find missing sales, purchases or stock with total accounts.', hook: 'Closing capital − opening capital + drawings − fresh capital = profit.' },
    { t: 'Partnership: goodwill and admission', u: 'fnd-p1-ch10-u03', ch: 'fnd-p1-ch10', more: [['fnd-p1-ch10-u01', 'P&L appropriation'], ['fnd-p1-ch10-u02', 'Goodwill']],
      why: 'Partnership is the biggest chapter by marks in ICAI model papers.', type: 'New ratio and sacrifice; goodwill; revaluation and capital accounts; balance sheet.', hook: 'Admission → sacrificing ratio (old − new).' },
    { t: 'Partnership: retirement and death', u: 'fnd-p1-ch10-u04', ch: 'fnd-p1-ch10', more: [['fnd-p1-ch10-u05', 'Death of a partner']],
      why: 'Asked as a full question with revaluation, goodwill and the amount due.', type: 'Gaining ratio; amount payable; joint life policy; executor\'s account.', hook: 'Retirement or death → gaining ratio (new − old).' },
    { t: 'Partnership: dissolution', u: 'fnd-p1-ch10-u06', ch: 'fnd-p1-ch10',
      why: 'A self-checking 10-mark question: bank and capital accounts must close at nil.', type: 'Realisation account, capital accounts and bank; insolvency of a partner; piecemeal payment.', hook: 'Assets out at book value, cash in at realised value; the difference is realisation profit or loss.' },
    { t: 'Company accounts: issue, forfeiture and re-issue of shares', u: 'fnd-p1-ch11-u02', ch: 'fnd-p1-ch11',
      why: 'One of the most frequent 10-mark questions in Paper 1.', type: 'Entries for application, allotment, calls; pro-rata; forfeiture and re-issue; capital reserve.', hook: 'Make the pro-rata table first. Forfeited amount − re-issue loss = capital reserve.' },
    { t: 'Company accounts: debentures, bonus and rights', u: 'fnd-p1-ch11-u03', ch: 'fnd-p1-ch11', more: [['fnd-p1-ch11-u04', 'Bonus and rights']],
      why: 'Entries and short computations; bonus from reserves is asked often.', type: 'Issue of debentures (par, premium, discount, collateral); bonus issue; value of a right.', hook: 'Debenture discount is a loss to write off; bonus uses reserves, not cash.' },
    { t: 'Company accounts: redemption (basics)', u: 'fnd-p1-ch11-u05', ch: 'fnd-p1-ch11', more: [['fnd-p1-ch11-u06', 'Redemption of debentures']],
      why: 'Redemption of preference shares and debentures — entries and the minimum fresh issue.', type: 'Fresh issue needed; transfer to capital redemption reserve; debenture redemption entries.', hook: 'Redeem from profits → CRR; redeem from fresh issue → no CRR for that part.' },
  ];
  async function focusList() {
    const el = X.open('world'); el.innerHTML = '<p class="ca-load">Loading the exam focus list…</p>';
    let st = null, wt = null; try { st = await X.structure('foundation'); } catch (e) {} try { wt = await loadJSON('content/ca/foundation/weightage.json'); } catch (e) {}
    const units = {}; if (st) st.papers.forEach(p => p.chapters.forEach(ch => ch.units.forEach(u => { units[u.id] = u; })));
    const w = wt && wt.papers && wt.papers['fnd-p1'];
    const live = id => units[id] && units[id].status === 'built';
    el.innerHTML = '';
    el.appendChild(backBtn('CA Journey', () => Ca.home()));
    el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">📌 Exam focus list</h1><p class="ca-onDark2">CA Foundation · Paper 1 Accounting — what to study first, and how it is asked.</p>
      <div class="card sp-as"><span class="ca-k">Accounting Standards at Foundation</span><h2 class="ca-h2s">Know the idea, not every standard</h2>
        <p class="ca-p">In the current Foundation Paper 1 study material, Accounting Standards are a topic of Chapter 1 (Unit 7): what standards are, their objectives and benefits, how they are made in India, and the list of standards — for awareness. Standard-by-standard study starts at CA Intermediate.</p>
        <p class="ca-p">Rules you will still use in Foundation sums: inventory at the lower of cost and net realisable value (Chapter 4); depreciation of fixed assets over their useful life (Chapter 5); only purchased goodwill is recorded (Chapter 10).</p>
        <div class="ca-btns">${live('fnd-p1-ch01-u07') ? '<button class="btn ghost" data-spfu="fnd-p1-ch01-u07">Practise now ▶</button>' : ''}${window.CaKeys ? '<button class="btn ghost" id="spKeys">📚 Key accounting rules — revise &amp; practise</button>' : ''}</div></div>
      ${FOCUS.map((f, i) => { const cw = w && w.chapters[f.ch];
        return `<article class="card sp-focus"><div class="sp-fhead"><span class="sp-fn">${i + 1}</span><div><h2 class="ca-h2s">${esc(f.t)}</h2>${cw ? `<span class="ca-chip">~${X.fmt(cw.avg_per_paper)} marks a paper · in ${cw.in_papers} of ${w.mtps} model papers</span>` : ''}</div></div>
          <dl class="sp-dl"><dt>Why it matters</dt><dd>${esc(f.why)}</dd><dt>Typical question</dt><dd>${esc(f.type)}</dd><dt>Memory hook</dt><dd class="sp-hook">💡 ${esc(f.hook)}</dd></dl>
          <div class="ca-btns">${live(f.u) ? `<button class="btn" data-spfu="${f.u}">Practise now ▶</button>` : '<span class="ca-soon">Coming soon</span>'}${(f.more || []).filter(([u]) => live(u)).map(([u, n]) => `<button class="btn ghost" data-spfu="${u}">${esc(n)} ▶</button>`).join('')}</div></article>`; }).join('')}
      <div class="card"><span class="ca-k">Not in your current syllabus</span><p class="ca-p">Consignment, sale or return, average due date and account current are not in the chapter list of the current Foundation Paper 1 study material (the one this app follows). Older books and coaching notes may still have them — skip them unless your syllabus changes.</p></div>
      <p class="ca-note ca-onDark2">${w ? `Marks per chapter: ${esc(wt.label)} ` : ''}Study order and hooks are StudyVerse guidance, not ICAI's.</p>`);
    el.querySelectorAll('[data-spfu]').forEach(b => b.onclick = () => { tap('open'); Ca.unit(b.dataset.spfu, 'mcq'); });
    const kb = D.getElementById('spKeys'); if (kb) kb.onclick = () => { tap('open'); CaKeys.open({ paper: 'fnd-p1', from: 'focus' }); };
  }

  /* ---------- styles (CA pro look: cream cards, gold accents; high-contrast and forced colours respected) ---------- */
  const CSS = `
.sp-row{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin:6px 0 8px}
.sp-pace{font-variant-numeric:tabular-nums;font-weight:700;font-size:13px;border-radius:999px;padding:5px 10px;background:#EEF6F0;color:#1d5c3a;border:1px solid #bfe0cb}
.sp-pace b{font-weight:800}.sp-pace.warn{background:#FFF6E0;color:#7a4b00;border-color:#f0d08a}.sp-pace.over{background:#FDE4E3;color:#8f1d1a;border-color:#f2b8b5}
.sp-verdict{font-size:12.5px;font-weight:800}.sp-verdict.slow{color:#8f1d1a}.sp-verdict.fast{color:#1d5c3a}
.sp-btn{position:relative;min-height:38px;border-radius:999px;border:1.5px solid var(--ca-gold,#C9A76A);background:#FBF4E4;color:#5B0F1B;font:inherit;font-size:13px;font-weight:800;padding:4px 12px;cursor:pointer}
.sp-btn::after{content:'';position:absolute;left:50%;top:50%;width:max(100%,44px);height:max(100%,44px);transform:translate(-50%,-50%)}
.sp-btn[aria-expanded=true]{background:#15161C;color:#E9D3A0;border-color:#15161C}
.sp-btn:focus-visible,.sp-tchip:focus-visible{outline:3px solid #C9A76A;outline-offset:2px}
.sp-fastbox{border-left:4px solid var(--ca-gold,#C9A76A);background:#FBF4E4;border-radius:8px;padding:10px 12px;margin:0 0 10px;color:#2B2D35}
.sp-fastin .ca-k{color:#74561F}.sp-p{margin:2px 0 6px;font-size:14.5px;line-height:1.45}.sp-ol{margin:4px 0 6px;padding-left:22px;font-size:14px;line-height:1.45}.sp-ol li{margin:2px 0}
.sp-tgt{margin:6px 0 4px;font-size:13px;color:#5B0F1B}
.sp-rel{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:6px}
.sp-tchip{position:relative;min-height:36px;border-radius:999px;border:1px solid #DDD3C0;background:#fff;color:#2B2D35;font:inherit;font-size:12.5px;font-weight:700;padding:4px 10px;cursor:pointer;text-align:left}
.sp-tchip.off{cursor:default;color:var(--muted)}
.sp-tlist{display:flex;flex-direction:column;gap:0}
.sp-trick summary{cursor:pointer;list-style:none;display:grid;grid-template-columns:auto 1fr;gap:2px 8px;align-items:baseline}
.sp-trick summary::-webkit-details-marker{display:none}
.sp-trick summary b{font-size:16px}.sp-trick summary small{grid-column:1/-1;color:var(--muted);font-size:13px;line-height:1.35}
.sp-trick summary{position:relative;padding-right:26px;min-height:44px}.sp-trick summary::after{content:'›';position:absolute;right:4px;top:-2px;font-size:24px;line-height:1;color:#74561F;transition:transform .2s}
.sp-trick[open] summary::after{transform:rotate(90deg)}.sp-trick[open] summary small{display:none}
@media (prefers-reduced-motion:reduce){.sp-trick summary::after{transition:none}}
.sp-tg{font-size:11px;font-weight:800;letter-spacing:.3px;text-transform:uppercase;color:#74561F;background:rgba(201,167,106,.18);border-radius:999px;padding:2px 8px}
.sp-ex{background:#F7F3EA;border-radius:8px;padding:8px 10px;margin:8px 0}.sp-ans{margin:4px 0 0;font-size:14px}
.sp-guide .sp-passes{padding-left:22px;line-height:1.5}.sp-guide .sp-passes li{margin:4px 0}
.sp-neg td,.sp-neg th{font-size:13px}.sp-neg .sp-go td{font-weight:800;color:#1d5c3a}
.sp-passbar{display:flex;align-items:flex-start;gap:8px;background:#15161C;color:#F4EAD8;border:1px solid rgba(201,167,106,.45);border-radius:10px;padding:8px 10px;margin:0 0 8px;font-size:13.5px;line-height:1.4}
.sp-passbar b{color:#E9D3A0;white-space:nowrap}
.sp-mark{min-height:40px}.sp-mark[aria-pressed=true]{background:#5B0F1B;color:#fff;border-color:#5B0F1B}
.ca-pal button.mk{box-shadow:inset 0 -4px 0 #B71C2C}
.sp-inter{text-align:left}
.sp-report .sp-srow{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(60px,1fr) auto;gap:8px;align-items:center;padding:6px 0;border-bottom:1px solid #EFE7D6}
.sp-sname b{display:block;font-size:14px}.sp-sname small,.sp-snum small{display:block;font-size:12px;color:var(--muted)}.sp-snum{text-align:right}.sp-snum b{font-size:15px}
.sp-snum small.w{color:#8f1d1a;font-weight:700}.sp-snum small.s{color:#1d5c3a;font-weight:700}
.sp-sbar{position:relative;height:10px;border-radius:99px;background:#EFE7D6;overflow:visible}.sp-sbar i{position:absolute;left:0;top:0;bottom:0;border-radius:99px}.sp-sbar i.ok{background:#23704A}.sp-sbar i.over{background:#B71C2C}
.sp-sbar em{position:absolute;top:-4px;bottom:-4px;width:2px;background:#15161C}
.sp-fhead{display:flex;gap:10px;align-items:flex-start}.sp-fn{flex:none;width:30px;height:30px;border-radius:50%;background:#15161C;color:#E9D3A0;font-weight:800;display:flex;align-items:center;justify-content:center}
.sp-fhead .ca-h2s{margin:2px 0 4px}
.sp-dl{margin:8px 0 6px}.sp-dl dt{font-size:11.5px;font-weight:800;letter-spacing:.3px;text-transform:uppercase;color:#74561F;margin-top:6px}.sp-dl dd{margin:2px 0 0;font-size:14.5px;line-height:1.45}
.sp-hook{background:#FBF4E4;border-radius:6px;padding:4px 8px}
.ca-duel{margin-top:10px}.ca-duelw{font-weight:800;color:#1d5c3a}
.sp-cxkeys{display:flex;flex-wrap:wrap;gap:4px;margin:6px 0 2px}.sp-cxkeys i{font-style:normal;min-width:26px;text-align:center;padding:2px 6px;border-radius:6px;background:#fff;border:1px solid #e0b400;font-weight:800;font-size:13px}
.sp-cxkeys i.d{background:#e7f3ea;border-color:#2E8B57;color:#1d5c3a}.sp-cxkeys i.c{background:#ffd54a}
html.sv-hc .sp-pace,html.sv-hc .sp-btn,html.sv-hc .sp-tchip,html.sv-hc .sp-fastbox,html.sv-hc .sp-hook,html.sv-hc .sp-ex{background:#fff;color:#000;border:2px solid #000}
html.sv-hc .sp-passbar{background:#000;color:#fff;border:2px solid #fff}
@media (forced-colors:active){.sp-pace,.sp-btn,.sp-tchip,.sp-fastbox{border:2px solid ButtonText}.sp-sbar i{background:CanvasText}}`;
  const st = D.createElement('style'); st.id = 'caSpeedCss'; st.textContent = CSS; D.head.appendChild(st);

  if (window.Nav) { drill = Nav.route('ca.speed', drill); tricks = Nav.route('ca.tricks', tricks); focusList = Nav.route('ca.focus', focusList); }
  window.CaSpeed = { TARGET, PASS1, target, kind, related, fastHTML, bar, wire, answered, note, drill, tricks, replay, focusList,
    guideHTML, negTable, PASSTIP, breakdownHTML, reportCard, wireReport, speedData, TRICKS, count: () => Object.keys(C().speed).length };
})();
