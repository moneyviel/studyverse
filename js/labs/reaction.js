/* Knowtopia Concept Lab: reaction — "Equation balancer" (balancing chemical equations + types of reactions)
 *
 * PARAMS (all optional)
 *  equations  array   list of equations, each either a string 'H2 + O2 -> H2O' (or with →) or an object
 *                     {r:['H2','O2'], p:['H2O'], type:'combination' | [types], hint?:'…'}.
 *                     Formulas may use brackets and hydrates: Ca(OH)2, Al2(SO4)3, CuSO4·5H2O, and state
 *                     symbols (s) (l) (g) (aq) which are shown but ignored for counting.
 *                     default: 5 Class-10 equations (one of each type)
 *  mode       string  'both' (balance, then pick the reaction type) | 'balance' (only balance) |
 *                     'type' (equations shown already balanced; pick the type)                 default 'both'
 *  types      array   type choices offered: from 'combination','decomposition','displacement',
 *                     'double displacement','combustion','neutralisation','redox'
 *                     default the first five
 *  typeNames  object  type id → display word (e.g. Hindi)                                    default English
 *  max        number  largest coefficient allowed                                            default 12
 *  challenge  string  challenge sentence (any language); a default is generated
 *  Win: every equation solved (balanced with the smallest whole numbers and/or type chosen correctly).
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));
  const num = (v, d) => (v === null || v === undefined || v === '' || !Number.isFinite(+v)) ? d : +v;
  const STATE = /\s*\((s|l|g|aq)\)\s*$/i;
  function parse(f) { // -> {El: n}
    const out = {};
    const parts = String(f).replace(STATE, '').split(/[·.*]/);
    for (let part of parts) {
      let mult = 1; const m = part.match(/^(\d+)(.*)$/); if (m) { mult = +m[1]; part = m[2]; }
      const stack = [{}]; let i = 0;
      while (i < part.length) {
        const ch = part[i];
        if (ch === '(' || ch === '[') { stack.push({}); i++; }
        else if (ch === ')' || ch === ']') {
          i++; let n = ''; while (i < part.length && /\d/.test(part[i])) n += part[i++];
          const top = stack.pop(), k = n ? +n : 1; const t = stack[stack.length - 1];
          for (const e in top) t[e] = (t[e] || 0) + top[e] * k;
        } else if (/[A-Z]/.test(ch)) {
          let el = ch; i++; while (i < part.length && /[a-z]/.test(part[i])) el += part[i++];
          let n = ''; while (i < part.length && /\d/.test(part[i])) n += part[i++];
          const t = stack[stack.length - 1]; t[el] = (t[el] || 0) + (n ? +n : 1);
        } else i++;
      }
      const t = stack[0]; for (const e in t) out[e] = (out[e] || 0) + t[e] * mult;
    }
    return out;
  }
  function fHTML(f) {
    const st = String(f).match(STATE); let body = String(f).replace(STATE, '');
    body = body.split(/[·.*]/).map((part, i) => {
      const m = part.match(/^(\d+)(.*)$/); let lead = ''; if (m && i > 0) { lead = m[1]; part = m[2]; }
      return lead + esc(part).replace(/([A-Za-z\)\]])(\d+)/g, '$1<sub>$2</sub>');
    }).join('·');
    return body + (st ? `<small>(${esc(st[1])})</small>` : '');
  }
  const gcd = (a, b) => b ? gcd(b, a % b) : a;
  const COL = { H: '#e9ebf5', O: '#ff6b6b', C: '#3a3f5c', N: '#3b82f6', Na: '#a78bfa', Cl: '#2ed3a5', Fe: '#c0703a', Cu: '#d4864a', S: '#ffc93c', Ca: '#9aa0c0', Mg: '#8fd694', Al: '#b8c2d6', Zn: '#7fa7c9', K: '#8b5cf6', Ba: '#5fb7a0', Pb: '#6b7090', Ag: '#cfd6e6', P: '#ff9f43', Si: '#c9a26b', I: '#8e44ad', Br: '#a0522d', F: '#9be15d', Li: '#ff8fb1', Mn: '#9b6bd1', Cr: '#4f9d69', Hg: '#a0a7c0' };
  const TYPES = { combination: 'Combination', decomposition: 'Decomposition', displacement: 'Displacement', 'double displacement': 'Double displacement', combustion: 'Combustion', neutralisation: 'Neutralisation', redox: 'Redox' };
  const THINT = {
    combination: 'Two or more substances join to make ONE product.',
    decomposition: 'ONE substance breaks down into two or more products.',
    displacement: 'A more reactive element pushes another element out of its compound.',
    'double displacement': 'Two compounds swap partners (ions) — often a precipitate forms.',
    combustion: 'A fuel burns in oxygen, giving carbon dioxide and water (and heat).',
    neutralisation: 'An acid and a base react to give salt and water.',
    redox: 'One substance is oxidised while another is reduced.'
  };

  const CSS = `
  .lb-reaction{font-weight:700;color:#1b1f3a;user-select:none;-webkit-user-select:none}
  .lb-reaction-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:8px 11px;font-size:13.5px;line-height:1.3;margin-bottom:7px}
  .lb-reaction-top{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:#6b7090;margin-bottom:4px}
  .lb-reaction-dots{display:flex;gap:4px}.lb-reaction-dots i{width:10px;height:10px;border-radius:50%;background:#e3e6f6}.lb-reaction-dots i.d{background:#2ed3a5}.lb-reaction-dots i.c{background:#8b5cf6}
  .lb-reaction-eq{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:2px 3px;background:#f7f8fd;border-radius:16px;padding:6px 4px;min-height:112px}
  .lb-reaction-eq.ok{background:#e3fbf3}
  .lb-reaction-sp{display:flex;flex-direction:column;align-items:center}
  .lb-reaction-sp button{width:44px;height:30px;border:none;border-radius:10px;background:#fff;box-shadow:0 2px 0 #d3d7ef;font-family:inherit;font-weight:900;font-size:17px;color:#8b5cf6;cursor:pointer;line-height:1}
  .lb-reaction-sp button:active{transform:translateY(2px);box-shadow:none}
  .lb-reaction-sp button:disabled{opacity:.3}
  .lb-reaction-f{display:flex;align-items:baseline;gap:2px;padding:3px 2px;font-size:16px;white-space:nowrap}
  .lb-reaction-f b{font-size:19px;color:#8b5cf6;min-width:12px;text-align:right}
  .lb-reaction-f b.one{color:#c9cde3}
  .lb-reaction-f sub{font-size:11px}.lb-reaction-f small{font-size:10px;color:#6b7090;margin-left:1px}
  .lb-reaction-op{font-size:18px;color:#6b7090;padding:0 1px}
  .lb-reaction-tab{width:100%;border-collapse:separate;border-spacing:0 3px;margin-top:5px;font-size:12.5px}
  .lb-reaction-tab td{padding:3px 6px;background:#fff6f0}
  .lb-reaction-tab tr.ok td{background:#e3fbf3}
  .lb-reaction-tab td:first-child{border-radius:10px 0 0 10px;font-weight:900;width:34px;text-align:center}
  .lb-reaction-tab td:last-child{border-radius:0 10px 10px 0;width:26px;text-align:center}
  .lb-reaction-tab .n{font-weight:900;font-size:14px;width:26px;text-align:center}
  .lb-reaction-balls{display:flex;flex-wrap:wrap;gap:2px;align-items:center;min-height:12px}
  .lb-reaction-balls i{width:9px;height:9px;border-radius:50%;border:1px solid rgba(0,0,0,.18)}
  .lb-reaction-balls em{font-style:normal;font-size:10px;color:#6b7090}
  .lb-reaction-head td{background:none!important;font-size:10.5px;color:#9aa0c0;padding:0 6px}
  .lb-reaction-types{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px}
  .lb-reaction-tb{min-height:42px;border:2px solid #e3e6f6;background:#fff;border-radius:13px;font-family:inherit;font-weight:800;font-size:13px;color:#1b1f3a;cursor:pointer}
  .lb-reaction-tb.ok{background:#e3fbf3;border-color:#2ed3a5;color:#0f7a5c}
  .lb-reaction-tb.no{background:#fff0f0;border-color:#ff6b6b;color:#c94545}
  .lb-reaction-row{display:flex;gap:6px;align-items:center;margin-top:6px}
  .lb-reaction-msg{flex:1;font-size:12.5px;color:#6b7090;line-height:1.3;min-height:34px}
  .lb-reaction-msg.good{color:#0f7a5c}.lb-reaction-msg.bad{color:#c94545}
  .lb-reaction-btn{min-height:40px;border:none;border-radius:12px;padding:0 12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;white-space:nowrap}
  .lb-reaction-btn.go{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
  .lb-reaction-btn:active{transform:translateY(2px);box-shadow:none}`;

  Labs.register('reaction', {
    title: 'Equation balancer',
    subjects: ['science', 'chemistry'],
    render(host, p, api) {
      const mode = ['both', 'balance', 'type'].includes(p.mode) ? p.mode : 'both';
      const MAX = Math.max(4, Math.min(20, Math.round(num(p.max, 12))));
      const typeList = (Array.isArray(p.types) && p.types.length ? p.types : ['combination', 'decomposition', 'displacement', 'double displacement', 'combustion']).filter(t => TYPES[t]);
      const tName = t => String((p.typeNames && p.typeNames[t]) || TYPES[t] || t);
      const raw = Array.isArray(p.equations) && p.equations.length ? p.equations : [];
      const EQS = raw.map(e => {
        let r, pr, type, hint;
        if (typeof e === 'string') { const [a, b] = e.split(/->|→|=/); if (!b) return null; r = a.split('+'); pr = b.split('+'); }
        else if (e && Array.isArray(e.r) && Array.isArray(e.p)) { r = e.r; pr = e.p; type = e.type; hint = e.hint; }
        else return null;
        r = r.map(s => String(s).trim()).filter(Boolean); pr = pr.map(s => String(s).trim()).filter(Boolean);
        if (!r.length || !pr.length) return null;
        const sp = r.concat(pr).map(parse), nR = r.length;
        const els = []; sp.forEach(m => Object.keys(m).forEach(k => { if (!els.includes(k)) els.push(k); }));
        // smallest balancing coefficients (brute force, small numbers)
        const n = sp.length, lim = n <= 4 ? MAX : n === 5 ? 10 : 6; let best = null, bestSum = 1e9; const c = new Array(n).fill(1);
        const ok = () => els.every(el => { let s = 0; for (let i = 0; i < n; i++) s += (i < nR ? 1 : -1) * c[i] * (sp[i][el] || 0); return s === 0; });
        (function rec(i, sum) { if (sum >= bestSum) return; if (i === n) { if (ok()) { best = c.slice(); bestSum = sum; } return; } for (let v = 1; v <= lim; v++) { c[i] = v; rec(i + 1, sum + v); } c[i] = 1; })(0, 0);
        const types = (Array.isArray(type) ? type : type ? [type] : []).map(String).filter(t => TYPES[t]);
        return { r, p: pr, sp, nR, els, best, types, hint };
      }).filter(e => e && e.best);
      if (!EQS.length && p.equations !== Labs.registry.reaction.example.equations) return Labs.registry.reaction.render(host, Object.assign({}, p, { equations: Labs.registry.reaction.example.equations }), api);
      if (!EQS.length) { host.textContent = 'No valid equations.'; return () => {}; }
      const needType = mode !== 'balance';
      const challenge = p.challenge || (mode === 'balance' ? `Balance all ${EQS.length} equations: make the atoms on both sides equal.` : mode === 'type' ? `Name the type of each of the ${EQS.length} reactions.` : `Balance each equation, then name its type (${EQS.length} equations).`);
      host.innerHTML = `<style>${CSS}</style><div class="lb-reaction">
        <div class="lb-reaction-ch">🎯 Challenge: ${esc(challenge)}</div>
        <div class="lb-reaction-top"><span class="lb-reaction-cnt"></span><span class="lb-reaction-dots">${EQS.map(() => '<i></i>').join('')}</span></div>
        <div class="lb-reaction-eq"></div>
        <div class="lb-reaction-mid"></div>
        <div class="lb-reaction-row"><div class="lb-reaction-msg"></div><button class="lb-reaction-btn lb-reaction-hint">💡 Hint</button><button class="lb-reaction-btn go lb-reaction-next" style="display:none">Next →</button></div></div>`;
      const root = host.querySelector('.lb-reaction'), $ = s => root.querySelector(s);
      const eqEl = $('.lb-reaction-eq'), mid = $('.lb-reaction-mid'), msg = $('.lb-reaction-msg'), nextB = $('.lb-reaction-next'), hintB = $('.lb-reaction-hint');
      let k = 0, coef = [], balanced = false, typed = false, solved = new Set(), won = false;
      const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };
      const setMsg = (t, c) => { msg.innerHTML = t; msg.className = 'lb-reaction-msg' + (c ? ' ' + c : ''); };
      const E = () => EQS[k];
      function counts() {
        const e = E(), L = {}, R = {};
        e.els.forEach(el => { L[el] = 0; R[el] = 0; });
        e.sp.forEach((m, i) => { for (const el in m) (i < e.nR ? L : R)[el] += coef[i] * m[el]; });
        return { L, R };
      }
      function load(i) {
        k = i; const e = E(); typed = false;
        coef = mode === 'type' ? e.best.slice() : e.sp.map(() => 1);
        balanced = mode === 'type';
        nextB.style.display = 'none'; hintB.style.display = mode === 'type' ? 'none' : '';
        $('.lb-reaction-cnt').textContent = `Equation ${k + 1} of ${EQS.length}`;
        root.querySelectorAll('.lb-reaction-dots i').forEach((d, j) => { d.className = solved.has(j) ? 'd' : j === k ? 'c' : ''; });
        if (mode !== 'type') { const { L, R } = counts(); if (e.els.every(el => L[el] === R[el])) { afterChange(); setMsg('Count the atoms: this one is <b>already balanced</b>! ' + (needType ? 'What type of reaction is it?' : ''), 'good'); return; } }
        drawEq(); drawMid();
        setMsg(mode === 'type' ? 'Look at the reactants and products. What kind of reaction is it?' : 'Use ▲ ▼ to change the numbers in front. Never change the small numbers!');
      }
      function drawEq() {
        const e = E(); let h = '';
        e.sp.forEach((_, i) => {
          if (i > 0) h += `<span class="lb-reaction-op">${i === e.nR ? '→' : '+'}</span>`;
          const f = i < e.nR ? e.r[i] : e.p[i - e.nR];
          const lock = mode === 'type' || (balanced && solvedBal());
          h += `<div class="lb-reaction-sp">${lock ? '' : `<button data-i="${i}" data-d="1" aria-label="more" ${coef[i] >= MAX ? 'disabled' : ''}>▲</button>`}
            <div class="lb-reaction-f"><b class="${coef[i] === 1 ? 'one' : ''}">${coef[i]}</b><span>${fHTML(f)}</span></div>
            ${lock ? '' : `<button data-i="${i}" data-d="-1" aria-label="less" ${coef[i] <= 1 ? 'disabled' : ''}>▼</button>`}</div>`;
        });
        eqEl.innerHTML = h; eqEl.classList.toggle('ok', solvedBal());
        eqEl.querySelectorAll('button[data-i]').forEach(b => b.onclick = () => { const i = +b.dataset.i; coef[i] = Math.max(1, Math.min(MAX, coef[i] + +b.dataset.d)); api.sfx('tap'); afterChange(); });
      }
      const solvedBal = () => balanced && coef.reduce((a, b) => gcd(a, b)) === 1;
      function table() {
        const { L, R } = counts(); const e = E();
        const balls = (n, c) => n <= 14 ? Array.from({ length: n }, () => `<i style="background:${c}"></i>`).join('') : Array.from({ length: 10 }, () => `<i style="background:${c}"></i>`).join('') + `<em>+${n - 10}</em>`;
        return `<table class="lb-reaction-tab"><tr class="lb-reaction-head"><td>atom</td><td style="text-align:right">left side</td><td></td><td></td><td>right side</td><td></td></tr>
          ${e.els.map(el => { const ok = L[el] === R[el], c = COL[el] || '#c4b5fd'; return `<tr class="${ok ? 'ok' : ''}"><td>${esc(el)}</td>
            <td><div class="lb-reaction-balls" style="justify-content:flex-end">${balls(L[el], c)}</div></td><td class="n">${L[el]}</td>
            <td class="n">${R[el]}</td><td><div class="lb-reaction-balls">${balls(R[el], c)}</div></td><td>${ok ? '✅' : '⚖️'}</td></tr>`; }).join('')}</table>`;
      }
      function drawMid() {
        if (mode !== 'type' && !(balanced && needType)) { mid.innerHTML = table(); return; }
        if (!needType) { mid.innerHTML = table(); return; }
        mid.innerHTML = `<div class="lb-reaction-types">${typeList.map(t => `<button class="lb-reaction-tb" data-t="${esc(t)}">${esc(tName(t))}</button>`).join('')}</div>`;
        mid.querySelectorAll('[data-t]').forEach(b => b.onclick = () => pickType(b));
      }
      function afterChange() {
        const { L, R } = counts(); const e = E();
        balanced = e.els.every(el => L[el] === R[el]);
        if (balanced && coef.reduce((a, b) => gcd(a, b)) !== 1) {
          drawEq(); mid.innerHTML = table();
          setMsg('Balanced — but every number can be divided. Use the <b>smallest</b> whole numbers!', 'bad'); api.sfx('hmm'); return;
        }
        drawEq();
        hintB.style.display = balanced || solved.has(k) ? 'none' : '';
        if (balanced) {
          api.sfx('coin');
          if (needType) { setMsg('⚖️ Balanced! Now: what <b>type</b> of reaction is this?', 'good'); drawMid(); }
          else { mid.innerHTML = table(); done('⚖️ Balanced! Atoms are neither created nor destroyed.'); }
        } else { mid.innerHTML = table(); const bad = e.els.filter(el => L[el] !== R[el]); setMsg(`Not balanced yet: check <b>${bad.map(esc).join(', ')}</b>.`); }
      }
      function pickType(b) {
        if (typed) return; const e = E(), t = b.dataset.t;
        const right = e.types.length ? e.types : null;
        if (!right || right.includes(t)) {
          typed = true; b.classList.add('ok'); api.sfx('coin');
          done(`✓ ${esc(tName(t))}: ${esc(THINT[t] || '')}`);
        } else {
          b.classList.add('no'); api.sfx('wrong');
          setMsg(`Not ${esc(tName(t).toLowerCase())}. ${e.hint ? esc(e.hint) : 'Hint: ' + esc(THINT[right[0]] || '')}`, 'bad');
        }
      }
      function done(text) {
        solved.add(k); setMsg(text, 'good'); hintB.style.display = 'none';
        root.querySelectorAll('.lb-reaction-dots i').forEach((d, j) => { d.className = solved.has(j) ? 'd' : j === k ? 'c' : ''; });
        if (solved.size === EQS.length) { setTimeout(() => winOnce(`All ${EQS.length} equations solved! ${mode !== 'type' ? 'Atoms balanced on both sides.' : ''}`), 400); nextB.style.display = EQS.length > 1 ? '' : 'none'; nextB.textContent = '↺ Again'; }
        else { nextB.style.display = ''; nextB.textContent = 'Next →'; }
      }
      nextB.onclick = () => {
        api.sfx('tap');
        if (solved.size === EQS.length) { solved.clear(); load(0); return; }
        let j = (k + 1) % EQS.length; while (solved.has(j)) j = (j + 1) % EQS.length; load(j);
      };
      hintB.onclick = () => {
        const e = E(); const i = coef.findIndex((c, j) => c !== e.best[j]);
        if (i < 0) return; coef[i] = e.best[i]; api.sfx('hmm'); afterChange();
        if (!balanced) setMsg(`Hint: the number in front of ${fHTML(i < e.nR ? e.r[i] : e.p[i - e.nR])} is <b>${e.best[i]}</b>.`);
      };
      load(0);
      return () => {};
    },
    example: {
      mode: 'both',
      equations: [
        { r: ['H2', 'O2'], p: ['H2O'], type: 'combination' },
        { r: ['CaCO3'], p: ['CaO', 'CO2'], type: 'decomposition', hint: 'Only ONE reactant here…' },
        { r: ['Fe', 'CuSO4'], p: ['FeSO4', 'Cu'], type: 'displacement' },
        { r: ['Na2SO4', 'BaCl2'], p: ['BaSO4', 'NaCl'], type: 'double displacement' },
        { r: ['CH4', 'O2'], p: ['CO2', 'H2O'], type: 'combustion' }
      ],
      types: ['combination', 'decomposition', 'displacement', 'double displacement', 'combustion']
    },
    examples: [
      { mode: 'balance', equations: ['Mg + O2 -> MgO', 'N2 + H2 -> NH3', 'Al + O2 -> Al2O3', 'Fe + H2O -> Fe3O4 + H2'],
        challenge: 'Grade 9–10: Balance these 4 equations using the smallest whole numbers.' },
      { mode: 'type', equations: [
          { r: ['Pb(NO3)2(s)'], p: ['PbO(s)', 'NO2(g)', 'O2(g)'], type: 'decomposition' },
          { r: ['Zn(s)', 'CuSO4(aq)'], p: ['ZnSO4(aq)', 'Cu(s)'], type: 'displacement' },
          { r: ['CaO(s)', 'H2O(l)'], p: ['Ca(OH)2(aq)'], type: 'combination' },
          { r: ['AgNO3(aq)', 'NaCl(aq)'], p: ['AgCl(s)', 'NaNO3(aq)'], type: 'double displacement' }],
        challenge: 'Grade 10: Name the type of each reaction (Chapter 1).' },
      { mode: 'both', equations: [
          { r: ['HCl', 'NaOH'], p: ['NaCl', 'H2O'], type: ['neutralisation', 'double displacement'] },
          { r: ['C3H8', 'O2'], p: ['CO2', 'H2O'], type: 'combustion' },
          { r: ['KClO3'], p: ['KCl', 'O2'], type: 'decomposition' }],
        types: ['combination', 'decomposition', 'neutralisation', 'combustion'],
        challenge: 'Grade 10–11: Balance and classify — watch the propane!' }
    ]
  });
})();
