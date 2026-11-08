/* Calculator Academy — content (missions, levels, badges). Used by js/calc-acad.js.
   Step types ("do"):
     info   — a short card; tap Next
     press  — press one of keys[] on the real calculator (optional mode)
     result — finish a calculation (=, %, GT, √ …) whose answer is value (keys[] limits which key finishes it)
     value  — the number on the screen becomes value (after any key; keys[] optional)
     mem    — the calculator's memory (M+ / M−) becomes value
     mode   — switch the calculator to Basic / Scientific / Financial
     angle  — switch DEG / RAD
     tool   — pick a financial tool
     fin    — a financial tool (tool) gives value with "Find …" button solve; tol = allowed difference
     quiz   — "Spot the mistake" style question: q, opts (first = right answer, shown shuffled), why
   hl = keys that glow when the student asks for a hint (data-k of the key, 'mode:sci', 'tool:emi', 'act:FV', 'grp', 'BGN').
   rewind = step index to go back to after a wrong finished attempt (e.g. GT already holds a wrong bill). */
window.CXA_DATA = {
  levels: [
    { id: 'basic', name: 'Desk calculator', emoji: '🧾', minGrade: 1, blurb: 'The 12-digit calculator shopkeepers and CA students use: GT, memory, %, constant mode and quick tricks.' },
    { id: 'sci', name: 'Scientific calculator', emoji: '🔬', minGrade: 8, blurb: 'Brackets and BODMAS, powers and roots, logs, sin/cos/tan in DEG and RAD, and EXP for giant numbers.' },
    { id: 'fin', name: 'Financial calculator', emoji: '💰', minGrade: 11, blurb: 'TVM and the sign rule, EMI, SIP growth, NPV and IRR, CAGR, depreciation, GST and margins.' },
  ],
  badges: {
    gt: ['🧾', 'GT Guru'], mem: ['🧠', 'Memory Master'], pct: ['💯', 'Percent Pro'], const: ['🔁', 'Repeat Ranger'], recip: ['🔄', 'Flip Wizard'], lakh: ['🪙', 'Lakh Legend'],
    spot: ['🔍', 'Mistake Detective'], speed: ['⚡', 'Speed Demon'], root: ['🌱', 'Root Ranger'], angle: ['📐', 'Angle Ace'], exp: ['🌌', 'Exponent Explorer'],
    tvm: ['⏳', 'Time Traveller'], emi: ['🛵', 'EMI Expert'], sip: ['🌟', 'SIP Star'], irr: ['🎯', 'IRR Hunter'], grow: ['📊', 'Growth Guru'], diwali: ['🪔', 'Diwali Dealer'], grad: ['🎓', 'Academy Graduate'],
  },
  missions: [
    /* ---------------- Desk calculator ---------------- */
    { id: 'b1', level: 'basic', mode: 'basic', emoji: '🧾', title: 'Kirana bill with GT', badge: 'gt',
      story: 'Raju bhaiya’s kirana shop is busy before Diwali. Help him total a customer’s bill without writing anything down.',
      steps: [
        { do: 'info', say: 'GT means Grand Total. Every time you press =, the answer is quietly added to GT. Press GT at the end and you get the total of all your answers!' },
        { do: 'result', say: 'Biscuits: 3 packets at ₹45. Type 3 × 45 =', value: 135, keys: ['='], hl: ['3', '*', '4', '5', '='], hint: 'Press 3, then ×, then 4 and 5, then =.' },
        { do: 'result', say: 'Sugar: 2 kg at ₹48 a kg. Type 2 × 48 =', value: 96, keys: ['='], hl: ['2', '*', '4', '8', '='] },
        { do: 'result', say: 'Tea packet ₹64 plus a matchbox ₹25. Type 64 + 25 =', value: 89, keys: ['='], hl: ['+', '='] },
        { do: 'result', say: 'Now press GT to see the grand total of all three.', value: 320, keys: ['GT'], hl: ['GT'], rewind: 1, hint: 'GT is in the top row. It shows the total and then empties itself.' },
      ], done: 'The GT key did all the adding for you. Shopkeepers total a whole day of bills this way!' },
    { id: 'b2', level: 'basic', mode: 'basic', emoji: '🧠', title: 'Diwali shopping memory', badge: 'mem',
      story: 'Priya’s family is shopping for Diwali. Keep a running total in the calculator’s memory while you work out each item.',
      steps: [
        { do: 'info', say: 'M+ adds the number on the screen to a hidden memory. M− takes it away. MR (memory recall) shows what is in memory. A small M on the screen means memory is not empty.' },
        { do: 'mem', say: '3 kurtas at ₹450 each: type 3 × 450 and press M+ (no need to press =).', value: 1350, hl: ['M+'], hint: 'Type 3 × 450, then press M+. M+ finishes the sum by itself.' },
        { do: 'mem', say: '2 boxes of diyas at ₹60: type 2 × 60, then M+.', value: 1470, hl: ['M+'] },
        { do: 'mem', say: 'A ₹100 discount coupon: type 100, then M− to take it away.', value: 1370, hl: ['M-'] },
        { do: 'value', say: 'Press MR to see the final bill.', value: 1370, keys: ['MR'], hl: ['MR'] },
        { do: 'quiz', q: 'Before the next customer, which key empties the memory?', opts: ['MC (memory clear)', 'AC', 'MR', 'C'], why: 'MC clears the memory. AC clears the screen but NOT the memory — that is a common exam slip!' },
      ], done: 'You kept a running total in memory. Tip: press MC before every new problem.' },
    { id: 'b3', level: 'basic', mode: 'basic', emoji: '💯', title: 'Percent power at Meena’s shop', badge: 'pct',
      story: 'Meena sells Diwali lamps. Work out GST, the price with GST, a sale price and a CA-style margin trick — all with the % key.',
      steps: [
        { do: 'info', say: 'On a desk calculator, % works with the sign you pressed before it: × % finds a part, + % adds it on, − % takes it off, and ÷ % divides by a percent.' },
        { do: 'result', say: '18% GST on a ₹2,500 lamp: type 2500 × 18 %', value: 450, keys: ['%'], hl: ['*', '%'], hint: 'No = needed. The % key gives the answer.' },
        { do: 'result', say: 'Price with GST: type 2500 + 18 %', value: 2950, keys: ['%'], hl: ['+', '%'] },
        { do: 'result', say: 'Diwali sale, 10% off: type 2500 − 10 %', value: 2250, keys: ['%'], hl: ['-', '%'] },
        { do: 'result', say: 'CA trick: a gift costs ₹800 and Meena wants a 20% margin on the selling price. Type 800 ÷ 80 % (because 100 − 20 = 80).', value: 1000, keys: ['%'], hl: ['/', '%'] },
      ], done: 'a ÷ b % is the fastest way to find a price for a margin. Many CA students use it in the exam hall.' },
    { id: 'b4', level: 'basic', mode: 'basic', emoji: '🔁', title: 'Constant mode piggy bank', badge: 'const',
      story: 'Arjun’s ₹1,000 grows by 10% every year. Watch it grow by pressing just one key again and again.',
      steps: [
        { do: 'info', say: 'Press = again and a desk calculator repeats the last operation. This is called constant mode — great for growth, tables and repeated discounts.' },
        { do: 'result', say: 'Year 1: type 1000 × 1.1 = (× 1.1 means +10%)', value: 1100, keys: ['='], hl: ['*', '.', '='] },
        { do: 'result', say: 'Year 2: just press = again!', value: 1210, keys: ['='], hl: ['='], hint: 'Only the = key. The calculator remembers × 1.1.' },
        { do: 'result', say: 'Year 3: press = once more.', value: 1331, keys: ['='], hl: ['='] },
        { do: 'quiz', q: 'What does 5 + 5 = = = show?', opts: ['20', '15', '10', '25'], why: '5 + 5 = 10, then each extra = adds 5 again: 15, then 20.' },
      ], done: 'Constant mode turns long repeated sums into a few taps.' },
    { id: 'b5', level: 'basic', mode: 'basic', emoji: '🔄', title: 'Reciprocal tricks', badge: 'recip',
      story: 'CA exams need discount factors like 1 ÷ 1.1. A desk calculator has a secret shortcut for them.',
      steps: [
        { do: 'info', say: 'Type a number, press ÷ and then = straight away: you get 1 ÷ that number (its reciprocal).' },
        { do: 'result', say: 'Find 1 ÷ 8: type 8 ÷ =', value: 0.125, keys: ['='], hl: ['8', '/', '='] },
        { do: 'result', say: 'Find 1 ÷ 25 the same way.', value: 0.04, keys: ['='], hl: ['/', '='] },
        { do: 'result', say: 'Discount factor for one year at 10%: type 1.1 ÷ =', value: 0.909090909, tol: 0.000001, keys: ['='], hl: ['/', '='] },
        { do: 'result', say: 'Press = again for year 2’s factor (1 ÷ 1.1 ÷ 1.1).', value: 0.826446281, tol: 0.000001, keys: ['='], hl: ['='] },
      ], done: 'Each extra = divides by 1.1 again — a whole table of discount factors in seconds!' },
    { id: 'b6', level: 'basic', mode: 'basic', emoji: '🪙', title: 'Lakhs, crores and the 00 key', badge: 'lakh',
      story: 'Big Indian numbers have lots of zeros. The 00 key and Indian commas make them easy to type and read.',
      steps: [
        { do: 'info', say: 'The 00 key types two zeros at once. The 1,00,000 button at the top switches between Indian commas (lakh, crore) and international commas.' },
        { do: 'press', say: 'Start typing 5 lakh: press 5, then 00.', keys: ['00'], hl: ['5', '00'] },
        { do: 'value', say: 'Finish it: press 00 again, then 0, to make 5,00,000.', value: 500000, hl: ['00', '0'], hint: '5 → 00 → 00 → 0 gives 5,00,000.' },
        { do: 'press', say: 'Tap the 1,00,000 button at the top to see the international style (500,000). Tap it again to come back if you like.', keys: ['grp'], hl: ['grp'] },
        { do: 'result', say: 'A salary of 5,00,000 a month for 12 months: press × 12 =', value: 6000000, keys: ['='], hl: ['*', '1', '2', '='] },
      ], done: '60,00,000 — sixty lakh! With Indian commas you can read big numbers aloud at a glance.' },
    { id: 'b7', level: 'basic', kind: 'spot', emoji: '🔍', title: 'Spot the mistake: desk calculator', badge: 'spot',
      story: 'Five students made calculator slips. Can you find what went wrong each time?',
      steps: [
        { do: 'quiz', q: 'Ravi typed 2500 + 18 % and wrote “GST = ₹2,950”. What went wrong?', opts: ['₹2,950 is the price WITH GST. GST alone is 2500 × 18 % = ₹450', 'He should have pressed − instead of +', 'The % key always adds 18', 'Nothing — it is correct'], why: '+ % adds the percent on. To find just the GST, use × %.' },
        { do: 'quiz', q: 'Sana pressed AC to start a new bill, but MR still showed an old number. Why?', opts: ['AC does not clear memory — she needed MC', 'MR is broken', 'She pressed GT by mistake', 'AC clears memory, so this cannot happen'], why: 'Memory survives AC. Press MC to empty it.' },
        { do: 'quiz', q: 'Kabir pressed = after each of his 10 bills, then GT — and the total was far too big. What did he forget?', opts: ['GT still held answers from earlier sums — press GT once before starting to empty it', 'GT multiplies the answers', 'He should have used × instead of +', 'He forgot to press AC after each bill'], why: 'GT adds every = answer since it was last shown. Pressing GT shows and empties it, so start clean.' },
        { do: 'quiz', q: 'For a 25% mark-up on a cost of ₹800, Neha typed 800 × 25 % and said the selling price is ₹200.', opts: ['₹200 is only the mark-up. Selling price = 800 + 25 % = ₹1,000', 'She should divide by 25', 'The answer should be ₹825', 'Nothing — ₹200 is right'], why: '× % gives the part (the mark-up). + % gives cost plus mark-up.' },
        { do: 'quiz', q: 'Isha typed 12 + 3 × 2 = on a desk calculator and got 30, but her maths book says 18. Who is right?', opts: ['Both: a desk calculator works left to right ((12 + 3) × 2). BODMAS gives 18 — use a scientific calculator or press × first', 'The calculator is broken', 'The book is wrong', 'Neither — the answer is 24'], why: 'Desk calculators do each step as you press it. Scientific calculators follow BODMAS.' },
      ], done: 'Great detective work! These are exactly the slips that cost marks in exams.' },
    { id: 'clock', level: 'basic', kind: 'speed', mode: 'basic', emoji: '⚡', title: 'Beat the clock', badge: 'speed',
      story: 'How many shop sums can you finish in 60 seconds? Type each one on the calculator and finish with = (or %).', steps: [], done: '' },

    /* ---------------- Scientific calculator ---------------- */
    { id: 's1', level: 'sci', mode: 'sci', emoji: '🧮', title: 'Brackets first (BODMAS)',
      story: 'Scientific calculators follow BODMAS, just like your maths book. Let us see the difference brackets make.',
      steps: [
        { do: 'mode', say: 'Tap “Scientific” at the top of the calculator.', mode: 'sci', hl: ['mode:sci'] },
        { do: 'info', say: 'Here you type the whole sum first and press = at the end. The calculator does Brackets, then powers (Orders), then ÷ and ×, then + and −.' },
        { do: 'result', say: 'Type 2 + 3 × 4 =  (× is done first)', value: 14, keys: ['='], hl: ['+', '*', '='] },
        { do: 'result', say: 'Now with brackets: ( 2 + 3 ) × 4 =', value: 20, keys: ['='], hl: ['(', ')', '='] },
        { do: 'result', say: 'Careful one: 10 − 4 ÷ 2 × 4 =', value: 2, keys: ['='], hl: ['-', '/', '*', '='], hint: '÷ and × go left to right: 4 ÷ 2 = 2, 2 × 4 = 8, then 10 − 8.' },
        { do: 'quiz', q: 'On a desk calculator 2 + 3 × 4 = shows 20, not 14. Why?', opts: ['A desk calculator works left to right: 2 + 3 = 5, then × 4', 'It is broken', 'It always does × first', 'It adds brackets by itself'], why: 'Desk calculators do each step as you press it. For BODMAS sums use the scientific mode, or brackets.' },
      ], done: 'Brackets put you in charge of the order. When in doubt, add brackets!' },
    { id: 's2', level: 'sci', mode: 'sci', emoji: '🌱', title: 'Powers and roots', badge: 'root',
      story: 'Squares, cubes, roots and factorials pop up everywhere — from area to probability.',
      steps: [
        { do: 'result', say: '2 to the power 10: type 2 xʸ 10 =', value: 1024, keys: ['='], hl: ['pow'] },
        { do: 'result', say: '12 squared: type 12 x² =', value: 144, keys: ['='], hl: ['sq'] },
        { do: 'result', say: 'Square root of 144: type √ 144 =', value: 12, keys: ['='], hl: ['sqrt'], hint: 'The calculator closes the bracket for you when you press =.' },
        { do: 'result', say: 'Cube root of 27: type ∛ 27 =', value: 3, keys: ['='], hl: ['cbrt'] },
        { do: 'result', say: '5 factorial (5 × 4 × 3 × 2 × 1): type 5 n! =', value: 120, keys: ['='], hl: ['fact'] },
        { do: 'result', say: 'Reciprocal: type 4 1/x =', value: 0.25, keys: ['='], hl: ['recip'] },
      ], done: 'You can now power up and root down any number!' },
    { id: 's3', level: 'sci', mode: 'sci', emoji: '📐', title: 'DEG or RAD?', badge: 'angle',
      story: 'Trigonometry answers change completely if the calculator is in the wrong angle unit. Learn to check it every time.',
      steps: [
        { do: 'info', say: 'Angles can be in degrees (DEG: a full turn is 360) or radians (RAD: a full turn is 2π). The small DEG or RAD on the screen tells you which one is on.' },
        { do: 'angle', say: 'Make sure the screen says DEG. If it says RAD, tap the DEG/RAD key.', unit: 'deg', hl: ['angle'] },
        { do: 'result', say: 'sin 30°: type sin 30 =', value: 0.5, keys: ['='], hl: ['sin'] },
        { do: 'result', say: 'tan 45°: type tan 45 =', value: 1, keys: ['='], hl: ['tan'] },
        { do: 'angle', say: 'Now tap the DEG/RAD key to switch to RAD.', unit: 'rad', hl: ['angle'] },
        { do: 'result', say: 'In radians, 30° is π ÷ 6. Type sin π ÷ 6 ) =', value: 0.5, keys: ['='], hl: ['sin', 'pi', '/'] },
        { do: 'quiz', q: 'Riya typed sin 30 and got −0.988. What happened?', opts: ['The calculator was in RAD mode, so it found sin of 30 radians', 'sin 30 really is −0.988', 'She pressed INV', 'The battery was low'], why: 'Always check DEG/RAD before trigonometry. School and CA sums use degrees.' },
        { do: 'angle', say: 'Switch back to DEG for school maths.', unit: 'deg', hl: ['angle'] },
        { do: 'result', say: 'INV turns sin back into an angle. Type INV sin 0.5 =', value: 30, keys: ['='], hl: ['inv', 'sin'] },
      ], done: 'Check DEG/RAD before every trigonometry sum — it is the number one exam slip.' },
    { id: 's4', level: 'sci', mode: 'sci', emoji: '🌌', title: 'Logs and giant numbers', badge: 'exp',
      story: 'Scientists write huge and tiny numbers with powers of 10. Logs undo powers. Let us try both.',
      steps: [
        { do: 'result', say: 'log 1000 asks “10 to what power is 1000?” Type log 1000 =', value: 3, keys: ['='], hl: ['log'] },
        { do: 'result', say: 'ln uses e (2.718…) instead of 10. Type ln e =', value: 1, keys: ['='], hl: ['ln', 'e'] },
        { do: 'result', say: 'INV log gives 10 to a power. Type INV log 2 =', value: 100, keys: ['='], hl: ['inv', 'log'] },
        { do: 'result', say: 'Avogadro’s number is 6.02 × 10²³. Type 6.02 EXP 23, then × 2 =', value: 1.204e24, keys: ['='], hl: ['exp', '*'], hint: 'EXP means “× 10 to the power”. Do not press × before EXP.' },
        { do: 'quiz', q: 'What does 3.5 EXP 4 mean?', opts: ['3.5 × 10⁴ = 35,000', '3.5 to the power 4', '3.5 × 4', '35 + 4'], why: 'EXP is short for exponent of 10.' },
      ], done: 'Logs and EXP let you handle numbers from atoms to galaxies.' },
    { id: 's5', level: 'sci', kind: 'spot', emoji: '🔎', title: 'Spot the mistake: scientific', badge: 'spot',
      story: 'Four scientific-calculator slips. Find the cause each time.',
      steps: [
        { do: 'quiz', q: 'Aman typed 1 ÷ 2 × 3 and wanted 1/6. He got 1.5. Why?', opts: ['÷ and × go left to right: (1 ÷ 2) × 3. For 1/6 type 1 ÷ ( 2 × 3 )', 'The calculator rounds badly', '× is always done first', 'He was in RAD mode'], why: 'Use brackets around the whole bottom part of a fraction.' },
        { do: 'quiz', q: 'Zoya typed −3 x² and got −9 instead of 9.', opts: ['The square is done before the minus. Type ( −3 ) x² to get 9', 'Squares are always negative', 'She needed x³', 'The calculator is wrong'], why: 'Powers come before the minus sign, so put negative numbers in brackets.' },
        { do: 'quiz', q: 'Dev got Math ERROR for log −10.', opts: ['Log of zero or a negative number is not defined', 'He forgot to press =', 'log needs RAD mode', 'The number was too small'], why: '10 to any power is always positive, so log only works for numbers above 0.' },
        { do: 'quiz', q: 'Kiran got Math ERROR for tan 90°.', opts: ['tan 90° is undefined — the line goes straight up and never meets the base', 'He should use RAD', 'tan 90° = 0', 'He typed 90 wrongly'], why: 'tan = sin ÷ cos, and cos 90° = 0. You cannot divide by 0.' },
      ], done: 'Brackets, signs and domains — you have spotted the classic traps!' },

    /* ---------------- Financial calculator ---------------- */
    { id: 'f1', level: 'fin', mode: 'fin', emoji: '⏳', title: 'TVM time machine', badge: 'tvm',
      story: 'Money today grows into more money later. The TVM keys move money through time — forwards and backwards.',
      steps: [
        { do: 'mode', say: 'Tap “Financial” at the top of the calculator.', mode: 'fin', hl: ['mode:fin'] },
        { do: 'info', say: 'TVM links five things: N (number of periods), I/Y (interest % a year), PV (money now), PMT (a regular payment) and FV (money later). Sign rule: money you pay out is minus (−), money you get back is plus (+).' },
        { do: 'fin', say: 'You put ₹1,000 in a bank FD for 5 years at 10%. In TVM type N 5, I/Y 10, PV −1000, PMT 0, P/Y 1, then tap Find FV.', tool: 'tvm', solve: 'FV', value: 1610.51, tol: 0.01, hl: ['tool:tvm', 'act:FV'], hint: 'PV is −1000 because you pay it to the bank.' },
        { do: 'fin', say: 'How much must you put in today to have ₹1,00,000 after 5 years at 10%? Change FV to 100000 (PMT 0), then tap Find PV.', tool: 'tvm', solve: 'PV', value: -62092.13, tol: 0.01, hl: ['act:PV'] },
        { do: 'quiz', q: 'Why is the PV answer negative (−62,092.13)?', opts: ['It is money you pay out today, so it carries a minus sign', 'It is a mistake', 'The interest rate is negative', 'The bank owes you that money'], why: 'Out is minus, in is plus. FV is +1,00,000 (you get it), so PV comes out minus.' },
      ], done: 'You moved money through time! FD maturity values and present values are now one tap away.' },
    { id: 'f2', level: 'fin', mode: 'fin', emoji: '🛵', title: 'Scooter on EMI', badge: 'emi',
      story: 'Anjali wants a ₹90,000 scooter on a loan at 10.5% a year for 24 months. What will she pay each month?',
      steps: [
        { do: 'tool', say: 'Pick the EMI tool.', tool: 'emi', hl: ['tool:emi'] },
        { do: 'fin', say: 'Type loan 90000, rate 10.5, tenure 24, then tap Find EMI.', tool: 'emi', solve: 'EMI', value: 4173.84, tol: 0.01, hl: ['act:EMI'] },
        { do: 'quiz', q: 'How much interest does Anjali pay in total? (Look under the answer.)', opts: ['₹10,172.25', '₹4,173.84', '₹9,450', '₹90,000'], why: 'Total paid = EMI × 24 = ₹1,00,172.25. Interest = total paid − loan.' },
        { do: 'fin', say: 'Check it with TVM: N 24, I/Y 10.5, PV 90000, FV 0, P/Y 12, END — then Find PMT. (It is minus: Anjali pays it.)', tool: 'tvm', solve: 'PMT', value: -4173.84, tol: 0.01, hl: ['tool:tvm', 'act:PMT'], hint: 'P/Y must be 12 because she pays every month.' },
      ], done: 'EMI tool and TVM agree. Banks use exactly this formula.' },
    { id: 'f3', level: 'fin', mode: 'fin', emoji: '🌟', title: 'SIP growth', badge: 'sip',
      story: 'Rahul starts a SIP of ₹2,000 a month for 10 years. If it earns 12% a year, how much will he have?',
      steps: [
        { do: 'fin', say: 'In TVM type N 120, I/Y 12, PV 0, PMT −2000, P/Y 12, keep END, then tap Find FV.', tool: 'tvm', solve: 'FV', value: 460077.38, tol: 0.01, hl: ['tool:tvm', 'act:FV'], hint: '10 years × 12 months = 120 payments. PMT is − because Rahul pays in.' },
        { do: 'press', say: 'Many SIPs go in at the START of each month. Tap BEGIN.', keys: ['BGN'], mode: 'fin', hl: ['BGN'] },
        { do: 'fin', say: 'Tap Find FV again.', tool: 'tvm', solve: 'FV', value: 464678.15, tol: 0.01, hl: ['act:FV'] },
        { do: 'quiz', q: 'Why is FV bigger in BEGIN mode?', opts: ['Each payment earns interest for one extra month', 'BEGIN adds a bonus', 'The rate becomes higher', 'There is one more payment'], why: 'Same 120 payments, but each one is invested a month earlier.' },
      ], done: 'He paid in ₹2,40,000 and could get about ₹4.6 lakh. That is the power of compounding!' },
    { id: 'f4', level: 'fin', mode: 'fin', emoji: '🎯', title: 'IRR hunter', badge: 'irr',
      story: 'A CA checks if a project is worth it. NPV says how much money it adds; IRR says what return it earns.',
      steps: [
        { do: 'tool', say: 'Pick the NPV · IRR tool.', tool: 'npv', hl: ['tool:npv'] },
        { do: 'info', say: 'Project A costs ₹1,000 today and pays ₹500 at the end of each of the next 3 years. CF0 is today (minus: you pay). CF1, CF2, CF3 come back to you (plus).' },
        { do: 'fin', say: 'Type rate 10, CF0 −1000, CF1 500, CF2 500, CF3 500, then tap Find NPV.', tool: 'npv', solve: 'NPV', value: 243.43, tol: 0.01, hl: ['act:NPV'] },
        { do: 'quiz', q: 'NPV at 10% is +₹243.43. What does that mean?', opts: ['The project earns more than 10%, so accept it', 'Reject it', 'It loses ₹243.43', 'NPV must always be 0'], why: 'A positive NPV means the project adds value at the given rate.' },
        { do: 'fin', say: 'Project B: CF0 −1000, CF1 300, CF2 400, CF3 500. Tap Find IRR.', tool: 'npv', solve: 'IRR', value: 8.8963, tol: 0.01, hl: ['act:IRR'], hint: 'IRR does not need the rate box — it finds the rate itself.' },
        { do: 'quiz', q: 'Your cost of money is 10%. Is Project B (IRR 8.90%) a good idea?', opts: ['No — its IRR is below 10%, so its NPV at 10% is negative', 'Yes, any IRR is good', 'IRR does not matter', 'Only if CF0 is positive'], why: 'Accept when IRR is above the cost of money; reject when it is below.' },
      ], done: 'IRR hunted! In the exam you find it by trial; here the calculator does the trials for you.' },
    { id: 'f5', level: 'fin', mode: 'fin', emoji: '📊', title: 'Growth and wear', badge: 'grow',
      story: 'Sales grow, machines wear out. CAGR measures smooth yearly growth; depreciation spreads a machine’s cost over its life.',
      steps: [
        { do: 'tool', say: 'Pick CAGR.', tool: 'cagr', hl: ['tool:cagr'] },
        { do: 'fin', say: 'Sales grew from 1,00,000 to 1,61,051 in 5 years. Type them, then Find CAGR.', tool: 'cagr', solve: 'CAGR', value: 10, tol: 0.01, hl: ['act:CAGR'] },
        { do: 'tool', say: 'Now pick Depreciation.', tool: 'dep', hl: ['tool:dep'] },
        { do: 'fin', say: 'A machine costs 1,00,000, scrap value 10,000, life 5 years. Tap Straight line (SLM).', tool: 'dep', solve: 'SLM', value: 18000, tol: 0.01, hl: ['act:SLM'] },
        { do: 'fin', say: 'Type a WDV rate of 20, then tap Written down (WDV).', tool: 'dep', solve: 'WDV', value: 20000, tol: 0.01, hl: ['act:WDV'] },
        { do: 'quiz', q: 'Which method gives more depreciation in year 1 here?', opts: ['WDV (₹20,000) — it is higher in the early years', 'SLM (₹18,000)', 'Both are the same', 'Neither — year 1 has no depreciation'], why: 'WDV charges a % of a shrinking value: big at first, smaller later. SLM is the same every year.' },
      ], done: 'CAGR and depreciation, done in seconds — with the formula shown so you can write it in the exam.' },
    { id: 'f6', level: 'fin', mode: 'fin', emoji: '🪔', title: 'Diwali GST and profit', badge: 'diwali',
      story: 'Back at Meena’s shop: add GST, take GST out of a price, and check her profit.',
      steps: [
        { do: 'tool', say: 'Pick GST.', tool: 'gst', hl: ['tool:gst'] },
        { do: 'fin', say: 'A ₹2,500 lamp with 18% GST: type 2500, tap 18%, then Add GST.', tool: 'gst', solve: 'ADD', value: 2950, tol: 0.01, hl: ['act:ADD'] },
        { do: 'fin', say: 'A gift box costs ₹1,180 including 18% GST. Type 1180, then Remove GST.', tool: 'gst', solve: 'REM', value: 1000, tol: 0.01, hl: ['act:REM'] },
        { do: 'tool', say: 'Pick Mark-up · margin.', tool: 'mark', hl: ['tool:mark'] },
        { do: 'fin', say: 'Meena bought the lamp for ₹2,000 and sells it for ₹2,500. Type both and tap Mark-up & margin.', tool: 'mark', solve: 'MM', value: 25, tol: 0.01, hl: ['act:MM'] },
        { do: 'quiz', q: 'Mark-up is 25% but margin is 20%. Why are they different?', opts: ['Mark-up is profit ÷ cost (2,000); margin is profit ÷ selling price (2,500)', 'One of them is wrong', 'GST changes the margin', 'Margin includes rent'], why: 'Same ₹500 profit, divided by different bases.' },
      ], done: 'Meena’s accounts are sorted. Happy Diwali! 🪔' },
    { id: 'f7', level: 'fin', kind: 'spot', emoji: '🕵️', title: 'Spot the mistake: financial', badge: 'spot',
      story: 'Four money-maths slips that CA students often make. Catch them!',
      steps: [
        { do: 'quiz', q: 'Tara typed PV 1000 and FV 1610.51 (both plus) and asked for I/Y. She got “No answer”. Why?', opts: ['PV and FV need opposite signs — money out is −, money in is +', 'I/Y cannot be found', 'N must be 0', 'She needed BEGIN mode'], why: 'With both plus, no interest rate can make them balance.' },
        { do: 'quiz', q: 'Arjun used P/Y = 1 for a monthly EMI with N = 24. His PMT came out far too big.', opts: ['For monthly payments set P/Y = 12, so the rate is split into months', 'N should be 2', 'He needed BEGIN mode', 'PMT is always big'], why: 'P/Y tells TVM how many payments happen in a year.' },
        { do: 'quiz', q: 'A ₹5,00,000 loan at 9% for 60 months came out as an EMI of ₹45,000.', opts: ['The rate was used as 9% a month. Use 9 ÷ 12 ÷ 100 a month — the right EMI is ₹10,379.18', '₹45,000 is right', 'Tenure must be in years', 'EMI ignores interest'], why: 'Monthly EMI uses the monthly rate.' },
        { do: 'quiz', q: 'Project A has IRR 15%, Project B has IRR 12% but a bigger NPV at the firm’s 10% rate. Only one can be chosen.', opts: ['Usually B — NPV shows how much money is added at the firm’s own rate', 'Always A — higher IRR always wins', 'Neither', 'Pick at random'], why: 'When NPV and IRR disagree for one-or-the-other projects, CA texts prefer NPV.' },
      ], done: 'Sign rule, P/Y, monthly rates, NPV vs IRR — you have nailed the classic traps.' },
  ],
};
