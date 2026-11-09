/* Knowtopia Concept Lab: patterns — growing patterns and number sequences (AP, GP, squares, triangles).
 *
 * The child steps the pattern forward/back (n = 1, 2, 3 …) and sees the figure grow (new tiles in
 * a new colour), the term strip with the jump between terms, the rule, the nth-term formula and the
 * sum of the first n terms. Optional sliders change a and d (or r). Challenge: predict a far term,
 * a sum, or which term has a given value — too far to just count, so the rule must be used.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   kind      'ap' | 'gp' | 'square' | 'triangular'   type of sequence                          default 'ap'
 *   a         number   first term                                                               default 3
 *   d         number   common difference (ap; may be negative)                                   default 2
 *   r         number   common ratio (gp; integer 2–5 draws best)                                 default 2
 *   visual    'tiles' | 'dots' | 'numbers'   how a term is drawn ('numbers' = number line style)  default 'tiles'
 *   label     string   what is being counted, e.g. 'tiles', 'matchsticks', 'रुपये'               default 'tiles'
 *   n         number   starting term number shown                                               default 3
 *   maxN      number   largest term the stepper reaches (keep below the asked term)              default 6
 *   editable  boolean  show sliders for a and d / r                                              default false
 *   aRange, dRange, rRange  [min,max]  slider limits                         default [1,9], [-5,6], [2,4]
 *   ask       {term:k} | {sum:k} | {which:value}   the challenge question                       default {term:10}
 *   challenge string   challenge sentence (else generated from ask)
 *   showSum   boolean  show Sₙ (sum of first n terms) line                                       default true
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = v => (Number.isInteger(v) ? v : Math.round(v * 100) / 100).toLocaleString('en-IN').replace('-', '−');
  const sub = n => String(n).split('').map(ch => (ch === 'n' ? 'ₙ' : '₀₁₂₃₄₅₆₇₈₉'[+ch]) || ch).join('');

  Labs.register('patterns', {
    title: 'Pattern explorer',
    subjects: ['maths'],
    render(host, p, api) {
      const kind = ['ap', 'gp', 'square', 'triangular'].includes(p.kind) ? p.kind : 'ap';
      const pr = (r, d) => Array.isArray(r) && r.length === 2 && +r[0] <= +r[1] ? r.map(Number) : d;
      const aR = pr(p.aRange, [1, 9]), dR = pr(p.dRange, [-5, 6]), rR = pr(p.rRange, [2, 4]);
      let a = isFinite(+p.a) ? +p.a : 3, d = isFinite(+p.d) ? +p.d : 2, r = isFinite(+p.r) && +p.r !== 0 ? +p.r : 2;
      if (kind === 'gp' && r === 1) r = 2;
      const maxN = Math.max(3, Math.min(10, +p.maxN || 6));
      let n = Math.max(1, Math.min(maxN, +p.n || 3));
      const label = String(p.label || 'tiles');
      const visual = ['tiles', 'dots', 'numbers'].includes(p.visual) ? p.visual : 'tiles';
      const showSum = p.showSum !== false;
      let won = false, ask, choices = [], picked = null;

      const T = k => kind === 'ap' ? a + (k - 1) * d : kind === 'gp' ? a * Math.pow(r, k - 1) : kind === 'square' ? k * k : k * (k + 1) / 2;
      const S = k => { let s = 0; for (let i = 1; i <= k; i++) s += T(i); return s; };
      const jump = k => kind === 'gp' ? `×${fmt(r)}` : (T(k + 1) - T(k) >= 0 ? '+' : '') + fmt(T(k + 1) - T(k));

      function ruleText() {
        if (kind === 'ap') return { rule: `Start at ${fmt(a)}, ${d >= 0 ? 'add ' + fmt(d) : 'subtract ' + fmt(-d)} each time`, nth: `a${sub('n')} = a + (n − 1)d = ${lin(d, a - d)}`, sum: `S${sub('n')} = n/2 [2a + (n − 1)d]` };
        if (kind === 'gp') return { rule: `Start at ${fmt(a)}, multiply by ${fmt(r)} each time`, nth: `a${sub('n')} = a·r${sup('n−1')} = ${fmt(a) === '1' ? '' : fmt(a) + '·'}${fmt(r)}${sup('n−1')}`, sum: `S${sub('n')} = a(r${sup('n')} − 1)/(r − 1)` };
        if (kind === 'square') return { rule: 'Add the next odd number: +3, +5, +7 …', nth: `a${sub('n')} = n × n = n²`, sum: `S${sub('n')} = n(n + 1)(2n + 1)/6` };
        return { rule: 'Add one more each time: +2, +3, +4 …', nth: `a${sub('n')} = n(n + 1)/2`, sum: `S${sub('n')} = n(n + 1)(n + 2)/6` };
      }
      function sup(t) { return String(t).split('').map(ch => ({ n: 'ⁿ', '−': '⁻', '1': '¹', '2': '²' }[ch] || ch)).join(''); }
      function lin(k, c) { // k·n + c
        let s = k === 0 ? '' : (k === 1 ? 'n' : k === -1 ? '−n' : fmt(k) + 'n');
        if (c) s += s ? (c > 0 ? ' + ' : ' − ') + fmt(Math.abs(c)) : fmt(c);
        return s || '0';
      }

      function makeAsk(fresh) {
        let q = (!fresh && p.ask && typeof p.ask === 'object') ? p.ask : null;
        if (q && 'which' in q) {
          const v = +q.which;
          const k = kind === 'ap' && d ? (v - a) / d + 1 : null;
          if (!(Number.isInteger(k) && k > 0)) q = null;
        }
        if (!q) {
          const lo = maxN + 2, hi = kind === 'gp' ? maxN + 4 : maxN + 14;
          q = { term: lo + Math.floor(Math.random() * (hi - lo + 1)) };
          if (fresh && kind === 'ap' && Math.random() < 0.35) q = d ? { which: T(q.term) } : q;
          if (fresh && Math.random() < 0.2 && kind !== 'gp') q = { sum: 5 + Math.floor(Math.random() * 8) };
          if (!fresh) q = { term: kind === 'gp' ? maxN + 2 : 10 };
        }
        ask = q;
        let ans, opts;
        if ('sum' in q) { const k = +q.sum; ans = S(k); opts = [ans, S(k - 1), S(k + 1)]; }
        else if ('which' in q) { const k = (+q.which - a) / d + 1; ans = k; opts = [k, k + 1, k - 1]; }
        else { const k = +q.term; ans = T(k); opts = kind === 'square' ? [ans, (k + 1) * (k + 1), 2 * k] : kind === 'triangular' ? [ans, T(k + 1), k * k] : [ans, T(k + 1), T(k - 1)]; }
        const seen = new Set();
        opts = opts.map(o => { while (seen.has(o)) o += 1; seen.add(o); return o; });
        choices = opts.sort(() => Math.random() - 0.5).map(o => ({ v: o, ok: o === ans }));
        picked = null;
      }
      function askText() {
        if (p.challenge && !ask._fresh) return p.challenge;
        if ('sum' in ask) return `What is the sum of the first ${ask.sum} terms?`;
        if ('which' in ask) return `Which term number is ${fmt(+ask.which)}?`;
        return `How many ${label} in term ${ask.term}? Use the rule!`;
      }

      host.innerHTML = `
<style>
.lb-patterns-w input[type=range]{-webkit-appearance:none;appearance:none;height:32px;background:transparent;cursor:pointer}.lb-patterns-w input[type=range]::-webkit-slider-runnable-track{height:8px;border-radius:8px;background:#e3e6f6}.lb-patterns-w input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;border-radius:50%;background:var(--c,#8b5cf6);margin-top:-8px;border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3)}.lb-patterns-w input[type=range]::-moz-range-track{height:8px;border-radius:8px;background:#e3e6f6}.lb-patterns-w input[type=range]::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:var(--c,#8b5cf6);border:3px solid #fff}
.lb-patterns-w{font-size:14px;color:#1b1f3a}
.lb-patterns-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.25}
.lb-patterns-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:16px}
.lb-patterns-nav{display:flex;align-items:center;gap:8px;margin-top:6px}
.lb-patterns-b{min-width:44px;min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:16px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
.lb-patterns-b:active{transform:translateY(2px);box-shadow:0 1px 0 #d3d7ef}
.lb-patterns-b:disabled{opacity:.35}
.lb-patterns-now{flex:1;text-align:center;font-family:'Baloo 2',Nunito,sans-serif;font-weight:800;font-size:18px;line-height:1.1}
.lb-patterns-now small{display:block;font-family:Nunito,sans-serif;font-size:11.5px;color:#6b7090}
.lb-patterns-strip{display:flex;align-items:center;gap:1px;overflow-x:auto;margin-top:6px;padding:2px 0 4px;scrollbar-width:thin}
.lb-patterns-t{min-width:33px;flex-shrink:0;text-align:center;background:#fff;border:2px solid #e3e6f6;border-radius:10px;padding:2px 3px;font-weight:800;font-size:14px;cursor:pointer;line-height:1.1}
.lb-patterns-t small{display:block;font-size:9.5px;color:#6b7090}
.lb-patterns-t.on{border-color:#8b5cf6;background:#f1ecff}
.lb-patterns-t.q{border-style:dashed;border-color:#ffc93c;background:#fff8e1;cursor:default}
.lb-patterns-j{font-size:10px;font-weight:800;color:#ff6b6b;min-width:16px;flex-shrink:0;text-align:center}
.lb-patterns-rule{background:#f6f4ff;border-radius:12px;padding:5px 9px;margin-top:4px;font-size:12.5px;font-weight:700;line-height:1.45}
.lb-patterns-rule b{color:#8b5cf6}
.lb-patterns-sl{display:flex;gap:10px;margin-top:4px}
.lb-patterns-sl label{flex:1;display:flex;align-items:center;gap:6px;font-weight:800;min-height:38px;min-width:0}
.lb-patterns-sl input{flex:1;min-width:0;--c:#8b5cf6}
.lb-patterns-ask{display:flex;gap:6px;margin-top:6px}
.lb-patterns-c{flex:1;min-height:44px;border:none;border-radius:12px;font-family:'Baloo 2',Nunito,sans-serif;font-weight:800;font-size:18px;cursor:pointer;background:#ffc93c;color:#1b1f3a;box-shadow:0 3px 0 #d99a00}
.lb-patterns-c.bad{background:#ffd6d6;box-shadow:0 3px 0 #ffb0b0;color:#c23b3b}
.lb-patterns-c.good{background:#2ed3a5;box-shadow:0 3px 0 #1a9c78;color:#fff}
.lb-patterns-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:4px;min-height:16px}
.lb-patterns-new{min-height:44px;padding:0 10px;font-size:13px}
</style>
<div class="lb-patterns-w">
  <div class="lb-patterns-ch"></div>
  <svg class="lb-patterns-svg" viewBox="0 0 360 150"></svg>
  <div class="lb-patterns-nav">
    <button class="lb-patterns-b" data-a="prev" aria-label="previous term">◀</button>
    <div class="lb-patterns-now"></div>
    <button class="lb-patterns-b" data-a="next" aria-label="next term">▶</button>
  </div>
  <div class="lb-patterns-strip"></div>
  <div class="lb-patterns-rule"></div>
  ${p.editable ? `<div class="lb-patterns-sl"><label>a <input type="range" data-k="a" min="${aR[0]}" max="${aR[1]}" step="1" value="${a}"><span data-v="a"></span></label>
    <label>${kind === 'gp' ? 'r' : 'd'} <input type="range" data-k="${kind === 'gp' ? 'r' : 'd'}" min="${kind === 'gp' ? rR[0] : dR[0]}" max="${kind === 'gp' ? rR[1] : dR[1]}" step="1" value="${kind === 'gp' ? r : d}"><span data-v="${kind === 'gp' ? 'r' : 'd'}"></span></label></div>` : ''}
  <div class="lb-patterns-ask"></div>
  <div class="lb-patterns-msg"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const svg = $('.lb-patterns-svg'), now = $('.lb-patterns-now'), strip = $('.lb-patterns-strip'), rule = $('.lb-patterns-rule'), askEl = $('.lb-patterns-ask'), msg = $('.lb-patterns-msg'), chEl = $('.lb-patterns-ch');
      if (kind !== 'ap' && kind !== 'gp' && p.editable) $('.lb-patterns-sl').style.display = 'none';

      function figure() {
        const t = T(n), prev = n > 1 ? T(n - 1) : 0, W = 360, H = 150;
        const NEW = '#ff6b6b', OLD = visual === 'dots' ? '#3b82f6' : '#2ed3a5';
        let g = '';
        const shape = (x, y, s, col, delay) => visual === 'dots'
          ? `<circle class="lb-patterns-pop" style="animation-delay:${delay}ms" cx="${x + s / 2}" cy="${y + s / 2}" r="${s * 0.4}" fill="${col}"/>`
          : `<rect class="lb-patterns-pop" style="animation-delay:${delay}ms" x="${x + 1}" y="${y + 1}" width="${s - 2}" height="${s - 2}" rx="${s * 0.22}" fill="${col}"/>`;
        const drawable = visual !== 'numbers' && Number.isInteger(t) && t >= 0 && t <= 220 && (kind !== 'ap' || (a > 0 && d >= 0));
        if (!drawable) {
          // number-line style: show previous and current values as bars
          const vals = []; for (let k = Math.max(1, n - 4); k <= n; k++) vals.push([k, T(k)]);
          const mx = Math.max(1, ...vals.map(q => Math.abs(q[1])));
          const bw = 52, gap = (W - vals.length * bw) / (vals.length + 1), base = H - 24, hh = 100;
          vals.forEach(([k, v], i) => {
            const x = gap + i * (bw + gap), h = Math.max(3, Math.abs(v) / mx * hh), y = v >= 0 ? base - h : base;
            g += `<rect x="${x}" y="${v >= 0 ? y : base - 3}" width="${bw}" height="${v >= 0 ? h : 3}" rx="8" fill="${k === n ? NEW : '#c4b5fd'}"/><text x="${x + bw / 2}" y="${(v >= 0 ? y : base) - 5}" text-anchor="middle" font-size="13" font-weight="800" fill="#1b1f3a">${fmt(v)}</text><text x="${x + bw / 2}" y="${base + 16}" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">a${sub(k)}</text>`;
          });
          g += `<line x1="8" x2="${W - 8}" y1="${base}" y2="${base}" stroke="#1b1f3a" stroke-width="1.5"/>`;
          if (visual !== 'numbers' && Math.abs(t) > 220) g += `<text x="${W / 2}" y="16" text-anchor="middle" font-size="12" font-weight="800" fill="#6b7090">Too many ${esc(label)} to draw — bars instead!</text>`;
          return g;
        }
        let cells = []; // [col,row,isNew]
        if (kind === 'ap') {
          for (let i = 0; i < a; i++) cells.push([0, i, n === 1]);
          for (let c = 1; c < n; c++) for (let i = 0; i < d; i++) cells.push([c, i, c === n - 1]);
        } else if (kind === 'square') {
          for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) cells.push([i, j, i === n - 1 || j === n - 1]);
        } else if (kind === 'triangular') {
          for (let i = 0; i < n; i++) for (let j = 0; j <= i; j++) cells.push([i, j, i === n - 1]);
        } else { // gp: blocks of previous figure, near square layout
          const cols = Math.ceil(Math.sqrt(t * 1.8));
          for (let i = 0; i < t; i++) cells.push([i % cols, Math.floor(i / cols), i >= prev]);
          if (n === 1) cells.forEach(c => { c[2] = true; });
        }
        const nc = Math.max(1, ...cells.map(c => c[0] + 1)), nr = Math.max(1, ...cells.map(c => c[1] + 1));
        const s = Math.min(30, (W - 30) / nc, (H - 38) / nr);
        const x0 = (W - nc * s) / 2, y0 = H - 12 - nr * s;
        cells.forEach((c, i) => { g += shape(x0 + c[0] * s, y0 + (nr - 1 - c[1]) * s, s, c[2] ? NEW : OLD, c[2] ? Math.min(400, i * 12) : 0); });
        g += `<text x="10" y="18" font-size="12" font-weight="800" fill="#6b7090">Term ${n}</text>`;
        if (n > 1) g += `<text x="${W - 10}" y="18" text-anchor="end" font-size="12" font-weight="800" fill="${NEW}">new: ${fmt(t - prev)} ${esc(label)}</text>`;
        return g;
      }
      function draw() {
        svg.innerHTML = `<style>.lb-patterns-pop{animation:lbpatpop .35s cubic-bezier(.2,1.5,.4,1) both;transform-box:fill-box;transform-origin:center}@keyframes lbpatpop{from{transform:scale(.2);opacity:0}}</style>` + figure();
        const t = T(n);
        now.innerHTML = `a${sub(n)} = ${fmt(t)}<small>term ${n} · ${fmt(t)} ${esc(label)}${showSum ? ` · S${sub(n)} = ${fmt(S(n))}` : ''}</small>`;
        let st = '';
        const last = Math.max(maxN, 5);
        for (let k = 1; k <= last; k++) {
          st += `<div class="lb-patterns-t ${k === n ? 'on' : ''}" data-n="${k <= maxN ? k : ''}"><small>a${sub(k)}</small>${fmt(T(k))}</div>`;
          if (k < last) st += `<span class="lb-patterns-j">${jump(k)}</span>`;
        }
        const qk = 'term' in ask ? ask.term : 'sum' in ask ? null : null;
        st += `<span class="lb-patterns-j">…</span><div class="lb-patterns-t q"><small>${qk ? 'a' + sub(qk) : 'sum' in ask ? 'S' + sub(ask.sum) : 'n'}</small>?</div>`;
        strip.innerHTML = st;
        const on = strip.querySelector('.on'); if (on) strip.scrollLeft = Math.max(0, on.offsetLeft - strip.offsetLeft - 120);
        const R = ruleText();
        rule.innerHTML = `<b>Rule:</b> ${esc(R.rule)}<br><b>nth term:</b> ${esc(R.nth)}${showSum ? `<br><b>Sum:</b> ${esc(R.sum)}` : ''}`;
        host.querySelector('[data-a="prev"]').disabled = n <= 1;
        host.querySelector('[data-a="next"]').disabled = n >= maxN;
        host.querySelectorAll('[data-v]').forEach(e => { e.textContent = fmt(e.dataset.v === 'a' ? a : e.dataset.v === 'r' ? r : d); });
      }
      function drawAsk() {
        chEl.textContent = '🎯 Challenge: ' + askText();
        askEl.innerHTML = choices.map((c, i) => `<button class="lb-patterns-c" data-c="${i}">${fmt(c.v)}</button>`).join('') + `<button class="lb-patterns-b lb-patterns-new" data-a="new">New ↻</button>`;
      }
      function newAsk(fresh) { makeAsk(fresh); if (fresh) ask._fresh = true; drawAsk(); draw(); }
      function onClick(e) {
        const b = e.target.closest('button,[data-n]');
        if (!b || b.disabled) return;
        if (b.dataset.a === 'prev' && n > 1) { n--; api.sfx('tap'); draw(); }
        else if (b.dataset.a === 'next' && n < maxN) { n++; api.sfx('tap'); draw(); }
        else if (b.dataset.a === 'new') { msg.textContent = ''; newAsk(true); api.sfx('tap'); }
        else if (b.dataset.n) { n = +b.dataset.n; api.sfx('tap'); draw(); }
        else if (b.dataset.c != null) {
          const c = choices[+b.dataset.c];
          if (c.ok) {
            b.classList.add('good'); api.sfx('correct');
            const R = ruleText();
            const why = 'sum' in ask ? `S${sub(ask.sum)} = ${fmt(c.v)}` : 'which' in ask ? `${fmt(+ask.which)} is term ${c.v}` : `a${sub(ask.term)} = ${fmt(c.v)}`;
            msg.textContent = `Yes! ${why}. ${R.nth}`;
            if (!won) { won = true; api.win(`${why} — you used the rule ${R.nth}`); }
          } else {
            b.classList.add('bad'); api.sfx('wrong');
            msg.textContent = kind === 'ap' && 'term' in ask ? `Careful: from a₁ to a${sub(ask.term)} there are ${ask.term - 1} jumps, not ${ask.term}.` : 'Not quite — check with the nth-term rule above.';
          }
        }
      }
      function onInput(e) {
        const k = e.target.dataset && e.target.dataset.k; if (!k) return;
        if (k === 'a') a = +e.target.value; else if (k === 'd') d = +e.target.value; else r = +e.target.value;
        msg.textContent = '';
        const keep = ask; makeAsk(!!ask._fresh || !p.ask); if (keep._fresh) ask._fresh = true;
        drawAsk(); draw();
      }
      host.addEventListener('click', onClick);
      host.addEventListener('input', onInput);
      makeAsk(false); drawAsk(); draw();
      return () => { host.removeEventListener('click', onClick); host.removeEventListener('input', onInput); };
    },
    example: { kind: 'ap', a: 3, d: 2, visual: 'tiles', label: 'tiles', n: 3, maxN: 6, editable: false, showSum: true },
    examples: [
      { kind: 'ap', a: 2, d: 2, visual: 'dots', label: 'dots', n: 2, maxN: 5, showSum: false, ask: { term: 10 }, challenge: 'Skip-count by 2s! How many dots in pattern 10?' },
      { kind: 'square', visual: 'tiles', label: 'tiles', n: 4, maxN: 6, ask: { term: 12 }, challenge: 'Square numbers: how many tiles in square 12?' },
      { kind: 'gp', a: 1, r: 2, visual: 'dots', label: 'bacteria', n: 4, maxN: 6, editable: true, ask: { term: 9 }, challenge: 'Bacteria double every hour. How many after term 9?' }
    ]
  });
})();
