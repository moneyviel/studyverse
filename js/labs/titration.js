/* Knowtopia Concept Lab: titration — burette, conical flask, live pH / redox curve
 *
 * The child drags the burette TAP open (slow = dropwise, wide = fast stream) or adds single drops
 * (0.05 mL), watches the indicator and the curve, then presses "Record end point". The pH is found
 * exactly from the charge balance (Kw = 1.0 × 10⁻¹⁴, 298 K); weak acids/bases show the
 * Henderson–Hasselbalch buffer readout; redox mode uses KMnO₄ as self-indicator.
 *
 * PARAMS (all optional)
 *  mode        string  'acidbase' | 'redox'                                               default 'acidbase'
 *  analyte     string  in the flask. acidbase: 'HCl' | 'CH3COOH' | 'H2C2O4' (oxalic, diprotic) |
 *                      'NaOH' | 'NH3' (NH₄OH).  redox: 'Fe2+' (Mohr's salt) | 'H2C2O4'      default 'HCl' / 'Fe2+'
 *  titrant     string  in the burette. acidbase: 'NaOH' | 'HCl' (auto: opposite of analyte);
 *                      redox: always KMnO₄                                                  default auto
 *  Ca          number  analyte molarity (mol L⁻¹)        default 0.1 (oxalic 0.05); random 0.08–0.13 for goal 'molarity'
 *  Va          number  analyte volume pipetted into the flask, mL (5–50)                    default 20
 *  Ct          number  titrant molarity                                    default 0.1 (KMnO₄ 0.02)
 *  indicators  array   indicator chips: 'phenolphthalein','methylOrange','methylRed','bromothymolBlue','none'
 *                                                                default ['phenolphthalein','methylOrange']
 *  indicator   string  indicator selected at start                                         default first chip
 *  showPH      bool    show the pH-meter reading                                           default true
 *  goal        object  {type:'endpoint'}  record the end point within ±tol mL of equivalence
 *                      {type:'molarity'}  analyte molarity hidden; titrate, then type the molarity (±2 %)
 *                      {type:'halfeq'}    weak acid/base: stop at half-equivalence (pH = pKa) ±0.2 mL
 *                                                                                    default {type:'endpoint'}
 *  tol         number  allowed error for the end point, mL                                default 0.1
 *  labels      object  {analyte, titrant} display names (may be Hindi)                     default chemical names
 *  challenge   string  challenge sentence (else generated)
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const num = (v, d) => (Number.isFinite(+v) && v !== '' && v !== null ? +v : d);
  const KW = 1e-14, DROP = 0.05;
  // acid/base library: kind 'a' acid / 'b' base; pK = [] strong; n = protons (acid) or OH⁻ (base)
  const LIB = {
    HCl: { kind: 'a', pK: null, n: 1, name: 'HCl', long: 'Hydrochloric acid', f: 'HCl' },
    CH3COOH: { kind: 'a', pK: [4.76], n: 1, name: 'CH₃COOH', long: 'Ethanoic (acetic) acid', f: 'CH₃COOH' },
    H2C2O4: { kind: 'a', pK: [1.25, 4.27], n: 2, name: 'H₂C₂O₄', long: 'Oxalic acid', f: 'H₂C₂O₄' },
    NaOH: { kind: 'b', pK: null, n: 1, name: 'NaOH', long: 'Sodium hydroxide', f: 'NaOH' },
    NH3: { kind: 'b', pK: [4.75], n: 1, name: 'NH₄OH', long: 'Ammonium hydroxide (aq. NH₃)', f: 'NH₄OH' }
  };
  const EQN = {
    'HCl|NaOH': 'HCl + NaOH → NaCl + H₂O', 'CH3COOH|NaOH': 'CH₃COOH + NaOH → CH₃COONa + H₂O', 'H2C2O4|NaOH': 'H₂C₂O₄ + 2NaOH → Na₂C₂O₄ + 2H₂O',
    'NaOH|HCl': 'NaOH + HCl → NaCl + H₂O', 'NH3|HCl': 'NH₄OH + HCl → NH₄Cl + H₂O',
    'Fe2+': 'MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 'H2C2O4red': '2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O'
  };
  // indicators: [low pH, high pH], colours at each end
  const IND = {
    phenolphthalein: { name: 'Phenolphthalein', r: [8.2, 10.0], a: null, b: '#e0218a', words: ['colourless', 'pink'] },
    methylOrange: { name: 'Methyl orange', r: [3.1, 4.4], a: '#e53935', b: '#f9c80e', words: ['red', 'yellow'], mid: '#fb8c00' },
    methylRed: { name: 'Methyl red', r: [4.4, 6.2], a: '#e53935', b: '#f9c80e', words: ['red', 'yellow'], mid: '#fb8c00' },
    bromothymolBlue: { name: 'Bromothymol blue', r: [6.0, 7.6], a: '#f2d22e', b: '#2a6fdb', words: ['yellow', 'blue'], mid: '#3fae6a' },
    none: { name: 'pH meter only', r: null }
  };
  const hex = h => [1, 3, 5].map(i => parseInt(h.substr(i, 2), 16));
  const mix = (a, b, t) => { const A = hex(a), B = hex(b); t = clamp(t, 0, 1); return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, '0')).join(''); };
  function indColour(k, ph, base) {
    const D = IND[k]; if (!D || !D.r) return base;
    const t = clamp((ph - D.r[0]) / (D.r[1] - D.r[0]), 0, 1);
    if (!D.a) return mix(base, D.b, t * 0.85);
    const c = D.mid ? (t < 0.5 ? mix(D.a, D.mid, t * 2) : mix(D.mid, D.b, t * 2 - 1)) : mix(D.a, D.b, t);
    return mix(base, c, 0.7);
  }
  // charge from an acid (anions) or base (cations) of total conc C at [H+] = h
  function acidCharge(A, C, h) {
    if (!A.pK) return A.n * C;
    const K = A.pK.map(pk => Math.pow(10, -pk)), N = K.length; let num = 0, den = 0, prod = 1;
    for (let j = 0; j <= N; j++) { if (j > 0) prod *= K[j - 1]; const t = Math.pow(h, N - j) * prod; den += t; num += j * t; }
    return C * num / den;
  }
  function baseCharge(B, C, h) { if (!B.pK) return B.n * C; const Ka = KW / Math.pow(10, -B.pK[0]); return C * h / (h + Ka); }
  function solvePH(sp) { // sp: [{A, C}]
    let lo = -16, hi = 2;
    const f = lh => { const h = Math.pow(10, lh); let s = h - KW / h; sp.forEach(({ A, C }) => { s += A.kind === 'a' ? -acidCharge(A, C, h) : baseCharge(A, C, h); }); return s; };
    for (let i = 0; i < 70; i++) { const m = (lo + hi) / 2; if (f(m) > 0) hi = m; else lo = m; }
    return -(lo + hi) / 2;
  }
  const fx = (v, d) => (Math.round(v * Math.pow(10, d)) / Math.pow(10, d)).toFixed(d);

  const CSS = `
  .lb-titration{color:#1b1f3a;font-weight:700;user-select:none;-webkit-user-select:none}
  .lb-titration-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:6px 10px;font-size:12.5px;line-height:1.28;margin-bottom:5px}
  .lb-titration-stage{display:flex;gap:6px;align-items:flex-start}
  .lb-titration-app{flex:none;width:104px;height:228px;display:block}
  .lb-titration-side{flex:1;min-width:0;display:flex;flex-direction:column;gap:4px}
  .lb-titration-chips{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none}
  .lb-titration-chips::-webkit-scrollbar{display:none}
  .lb-titration-chip{flex:none;min-height:32px;padding:0 8px;border-radius:11px;border:2px solid #e3e6f6;background:#fff;font:inherit;font-size:11px;font-weight:800;color:#1b1f3a;cursor:pointer;display:flex;align-items:center;gap:4px}
  .lb-titration-chip i{width:10px;height:10px;border-radius:50%;display:inline-block;border:1px solid rgba(0,0,0,.15)}
  .lb-titration-chip.on{border-color:#8b5cf6;background:#f1edff}
  .lb-titration-meter{display:flex;gap:4px}
  .lb-titration-meter div{flex:1;background:#1b1f3a;color:#7dffcf;border-radius:10px;padding:3px 6px;font-size:10px;line-height:1.15;color:#aab0d0}
  .lb-titration-meter b{display:block;color:#7dffcf;font-size:16px;font-weight:900;font-variant-numeric:tabular-nums}
  .lb-titration-graph{width:100%;height:auto;display:block;background:#f7f8fd;border-radius:12px}
  .lb-titration-graph text{font-family:inherit}
  .lb-titration-note{font-size:10.5px;line-height:1.3;color:#6b7090;min-height:27px}
  .lb-titration-note b{color:#1b1f3a}
  .lb-titration-row{display:flex;gap:6px;align-items:center;margin-top:6px}
  .lb-titration-tap{flex:1;height:44px;border-radius:14px;background:#eef0fb;position:relative;touch-action:none;cursor:grab}
  .lb-titration-tap span{position:absolute;left:0;right:0;top:0;bottom:0;display:flex;align-items:center;justify-content:center;font-size:11px;color:#6b7090;pointer-events:none;padding-left:30px}
  .lb-titration-fill{position:absolute;left:0;top:0;bottom:0;border-radius:14px;background:linear-gradient(90deg,#c9f3e6,#2ed3a5);pointer-events:none}
  .lb-titration-knob{position:absolute;top:3px;width:38px;height:38px;border-radius:12px;background:#fff;box-shadow:0 2px 6px rgba(27,31,58,.25);pointer-events:none;display:flex;align-items:center;justify-content:center;font-size:17px}
  .lb-titration-btn{flex:none;min-height:44px;padding:0 12px;border:none;border-radius:13px;font:inherit;font-weight:800;font-size:12.5px;cursor:pointer;color:#fff;background:#8b5cf6;box-shadow:0 3px 0 #5b33c9}
  .lb-titration-btn:active{transform:translateY(2px);box-shadow:none}
  .lb-titration-btn.g{background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
  .lb-titration-btn.b{background:#3b82f6;box-shadow:0 3px 0 #2257b8}
  .lb-titration-btn.m{background:#2ed3a5;box-shadow:0 3px 0 #1a9c78}
  .lb-titration-btn:disabled{opacity:.4}
  .lb-titration-msg{font-size:12px;color:#6b7090;min-height:16px;margin-top:5px;line-height:1.3}
  .lb-titration-msg.good{color:#0f7a5c}.lb-titration-msg.bad{color:#c94545}
  .lb-titration-ans{display:none;gap:6px;align-items:center;margin-top:6px;font-size:12.5px}
  .lb-titration-ans input{width:92px;min-height:40px;border:2px solid #d9dcf0;border-radius:12px;font:inherit;font-size:15px;font-weight:800;text-align:center;color:#1b1f3a}
  .lb-titration-drop{transition:none}`;

  Labs.register('titration', {
    title: 'Titration lab',
    subjects: ['chemistry', 'science'],
    render(host, p, api) {
      const redox = p.mode === 'redox';
      const goal = (p.goal && typeof p.goal === 'object') ? p.goal : (typeof p.goal === 'string' ? { type: p.goal } : {});
      let gtype = ['endpoint', 'molarity', 'halfeq'].includes(goal.type) ? goal.type : 'endpoint';
      const tol = clamp(num(p.tol, 0.1), 0.05, 2);
      const L = (p.labels && typeof p.labels === 'object') ? p.labels : {};
      let A, T, eqn, nA, nT, ratioTxt, aName, tName, tColour, flaskBase;
      if (redox) {
        const ox = p.analyte === 'H2C2O4' || p.analyte === 'oxalic';
        A = { kind: 'r', ox }; aName = L.analyte || (ox ? 'Oxalic acid (H₂C₂O₄)' : 'Mohr\'s salt (Fe²⁺)'); tName = L.titrant || 'KMnO₄';
        eqn = ox ? EQN.H2C2O4red : EQN['Fe2+']; tColour = '#7b1fa2'; flaskBase = ox ? '#f4f8ff' : '#e8f4d9';
        // mol MnO4- : mol reductant = 1:5 (Fe2+) or 2:5 (C2O4 2-)
        nA = ox ? 2 : 1; nT = 5; ratioTxt = ox ? 'MnO₄⁻ : C₂O₄²⁻ = 2 : 5' : 'MnO₄⁻ : Fe²⁺ = 1 : 5';
        if (gtype === 'halfeq') gtype = 'endpoint';
      } else {
        A = LIB[p.analyte] || LIB[String(p.analyte || '').replace(/[^A-Za-z0-9]/g, '')] || LIB.HCl;
        const ak = Object.keys(LIB).find(k => LIB[k] === A);
        T = LIB[p.titrant] && LIB[p.titrant].kind !== A.kind && !LIB[p.titrant].pK ? LIB[p.titrant] : (A.kind === 'a' ? LIB.NaOH : LIB.HCl);
        const tk = Object.keys(LIB).find(k => LIB[k] === T);
        eqn = EQN[ak + '|' + tk] || ''; aName = L.analyte || A.name; tName = L.titrant || T.name; tColour = '#dbe9ff'; flaskBase = '#f4f8ff';
        nA = A.n; nT = T.n;
        if (gtype === 'halfeq' && !(A.pK && A.pK.length === 1)) gtype = 'endpoint';
      }
      const Va = clamp(num(p.Va, 20), 5, 50);
      const Ct = clamp(num(p.Ct, redox ? 0.02 : 0.1), 0.001, 5);
      const hidden = gtype === 'molarity';
      let Ca = num(p.Ca, NaN);
      if (!(Ca > 0)) Ca = hidden ? Math.round((0.08 + Math.random() * 0.05) * 2000) / 2000 * (redox && A.ox ? 0.5 : 1) : (redox ? (A.ox ? 0.05 : 0.1) : (A === LIB.H2C2O4 ? 0.05 : 0.1));
      Ca = clamp(Ca, 0.0005, 5);
      // equivalence volume: redox  n(MnO4-) = (nA/nT) n(red);   acid-base  nA·Ca·Va = nT·Ct·V
      const Veq = redox ? (nA / nT) * Ca * Va / Ct : nA * Ca * Va / (nT * Ct);
      const CAP = 50;
      const Vax = hidden ? 50 : Math.min(50, Math.max(10, Math.ceil(Math.min(50, Veq * 1.6) / 5) * 5));
      const indKeys = (Array.isArray(p.indicators) && p.indicators.length ? p.indicators : ['phenolphthalein', 'methylOrange']).filter(k => IND[k]);
      if (!indKeys.length) indKeys.push('phenolphthalein');
      let ind = redox ? null : (IND[p.indicator] && indKeys.includes(p.indicator) ? p.indicator : indKeys[0]);
      const showPH = !redox && p.showPH !== false;
      const pKa = !redox && A.pK && A.pK.length === 1 ? A.pK[0] : null;
      const ff = v => { const s = String(+v.toPrecision(3)); return s; };

      let challenge = p.challenge ? String(p.challenge) : '';
      if (!challenge) {
        if (gtype === 'molarity') challenge = `Titrate the ${aName} of unknown molarity with ${ff(Ct)} M ${tName}, record the end point and work out its molarity.`;
        else if (gtype === 'halfeq') challenge = `Stop exactly at half-neutralisation, where pH = pKa (±0.2 mL).`;
        else challenge = redox ? `Add ${tName} until the first permanent pale pink — record the end point within ±${tol} mL.` : `Choose a suitable indicator and record the end point within ±${tol} mL.`;
      }

      host.innerHTML = `<style>${CSS}</style><div class="lb-titration">
        <div class="lb-titration-ch">🎯 Challenge: ${esc(challenge)}</div>
        <div class="lb-titration-stage">
          <svg class="lb-titration-app" viewBox="0 0 104 228"></svg>
          <div class="lb-titration-side">
            ${redox ? '' : `<div class="lb-titration-chips">${indKeys.map(k => `<button class="lb-titration-chip" data-i="${k}"><i style="background:${k === 'none' ? '#fff' : k === 'phenolphthalein' ? '#e0218a' : IND[k].a}"></i>${IND[k].name}</button>`).join('')}</div>`}
            <div class="lb-titration-meter"><div>Burette reading<b class="lb-titration-v">0.00 mL</b></div><div>${showPH ? 'pH meter' : redox ? 'Flask colour' : 'Indicator'}<b class="lb-titration-ph">—</b></div></div>
            <svg class="lb-titration-graph" viewBox="0 0 240 120"></svg>
            <div class="lb-titration-note"></div>
          </div>
        </div>
        <div class="lb-titration-row"><div class="lb-titration-tap"><div class="lb-titration-fill"></div><span>closed — drag the tap ▶</span><div class="lb-titration-knob">🔧</div></div>
          <button class="lb-titration-btn b" data-a="drop">+1 drop</button></div>
        <div class="lb-titration-row"><button class="lb-titration-btn" data-a="rec" style="flex:1">📍 Record end point</button><button class="lb-titration-btn g" data-a="reset">↺ Refill</button></div>
        <div class="lb-titration-ans"><span>M(${esc(aName)}) =</span><input type="text" inputmode="decimal" placeholder="0.000"><span>M</span><button class="lb-titration-btn m" data-a="check">Check</button></div>
        <div class="lb-titration-msg"></div></div>`;
      const root = host.querySelector('.lb-titration'), $ = s => root.querySelector(s);
      const app = $('.lb-titration-app'), graph = $('.lb-titration-graph'), note = $('.lb-titration-note'), msg = $('.lb-titration-msg');
      const vEl = $('.lb-titration-v'), phEl = $('.lb-titration-ph'), tap = $('.lb-titration-tap'), knob = $('.lb-titration-knob'), fill = $('.lb-titration-fill'), tapTxt = tap.querySelector('span');
      const ansRow = $('.lb-titration-ans'), ansIn = ansRow.querySelector('input');
      const setMsg = (t, c) => { msg.innerHTML = t; msg.className = 'lb-titration-msg' + (c ? ' ' + c : ''); };
      let won = false; const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };

      // ---------- state ----------
      let drops = 0, open = 0, acc = 0, last = 0, raf = 0, hist = [], recorded = null, flashT = 0;
      const V = () => drops * DROP;
      function state(v) {
        const tot = Va + v;
        if (redox) {
          const nRed = Ca * Va, nMn = Ct * v, needMn = nRed * nA / nT; // mmol
          const left = Math.max(0, nRed - nMn * nT / nA), excess = Math.max(0, nMn - needMn);
          return { left, nRed, excessM: excess / tot, frac: Math.min(1, nMn / needMn) };
        }
        const ph = solvePH([{ A, C: Ca * Va / tot }, { A: T, C: Ct * v / tot }]);
        return { ph };
      }
      const eqState = state(Veq);
      // volume window over which an indicator changes colour (pH crosses its range) — for suitability
      const indWin = {};
      function indicatorWindow(k) {
        if (redox || !IND[k] || !IND[k].r) return null; if (indWin[k]) return indWin[k];
        const [a, b] = IND[k].r; let va = null, vb = null, prev = state(0).ph;
        for (let v = 0.01; v <= CAP; v += 0.01) {
          const ph = state(v).ph;
          if (va == null && (prev - a) * (ph - a) <= 0) va = v; if (vb == null && (prev - b) * (ph - b) <= 0) vb = v;
          if (va != null && vb != null) break; prev = ph;
        }
        if (va == null) va = state(0).ph > b || state(0).ph < a ? CAP : 0; if (vb == null) vb = va;
        return (indWin[k] = [Math.min(va, vb), Math.max(va, vb)]);
      }
      // ---------- apparatus drawing ----------
      const cid = 'lbtiF' + Math.random().toString(36).slice(2, 8);
      const BT = 10, BB = 132, scale = (BB - BT) / CAP; // burette 0 mL at top
      const fy0 = 168, fy1 = 222; // flask body
      const liqTop = vol => { const frac = clamp(0.14 + vol / 100 * 0.72, 0.1, 0.95); return fy1 - 2 - frac * (fy1 - fy0 - 4); };
      app.innerHTML = `
        <defs><clipPath id="${cid}"><path d="M44 152 V166 L18 219 Q16 224 22 224 H82 Q88 224 86 219 L60 166 V152 Z"/></clipPath></defs>
        <rect x="88" y="4" width="5" height="222" rx="2.5" fill="#d3d7ef"/><rect x="60" y="40" width="30" height="5" rx="2" fill="#c3c7da"/>
        <rect x="45" y="${BT}" width="14" height="${BB - BT}" rx="3" fill="#fff" stroke="#9aa6d6" stroke-width="1.5"/>
        <rect class="lb-titration-bliq" x="46.5" y="${BT}" width="11" height="${BB - BT}" fill="${tColour}" opacity="${redox ? .9 : .8}"/>
        ${Array.from({ length: 11 }, (_, i) => `<line x1="45" x2="${i % 2 ? 50 : 53}" y1="${BT + i * 5 * scale}" y2="${BT + i * 5 * scale}" stroke="#6b7090" stroke-width=".7"/><text x="42" y="${BT + i * 5 * scale + 2.5}" font-size="6.5" text-anchor="end" fill="#6b7090" font-weight="800">${i * 5}</text>`).join('')}
        <path d="M47 ${BB} L57 ${BB} L54 ${BB + 6} L50 ${BB + 6} Z" fill="#c9cde3"/>
        <g class="lb-titration-cock" style="transform-origin:52px ${BB + 9}px;transition:transform .1s"><rect x="40" y="${BB + 7}" width="24" height="5" rx="2.5" fill="#ff6b6b"/></g>
        <rect x="50.5" y="${BB + 12}" width="3" height="10" fill="#c9cde3"/>
        <g class="lb-titration-drops"></g>
        <g clip-path="url(#${cid})"><rect class="lb-titration-fliq" x="10" y="200" width="84" height="40" fill="${flaskBase}"/><ellipse class="lb-titration-splash" cx="52" cy="200" rx="0" ry="2" fill="#e0218a" opacity="0"/></g>
        <path d="M44 150 V166 L18 219 Q16 224 22 224 H82 Q88 224 86 219 L60 166 V150" fill="none" stroke="#9aa6d6" stroke-width="2"/>
        <rect x="41" y="148" width="22" height="4" rx="2" fill="#c3c7da"/>
        <rect x="8" y="225" width="88" height="3" rx="1.5" fill="#e3e6f6"/>`;
      const bliq = app.querySelector('.lb-titration-bliq'), fliq = app.querySelector('.lb-titration-fliq'), dropsG = app.querySelector('.lb-titration-drops'), cock = app.querySelector('.lb-titration-cock'), splash = app.querySelector('.lb-titration-splash');
      // ---------- graph ----------
      const GX0 = 24, GX1 = 234, GY0 = 7, GY1 = 101;
      let yMax = redox ? Ca * Va : 14;
      const gx = v => GX0 + v / Vax * (GX1 - GX0), gy = y => GY1 - y / yMax * (GY1 - GY0);
      function drawGraph(st) {
        let s = `<rect x="${GX0}" y="${GY0}" width="${GX1 - GX0}" height="${GY1 - GY0}" fill="#fff" rx="4"/>`;
        if (!redox && ind && IND[ind].r) { const [a, b] = IND[ind].r; s += `<rect x="${GX0}" y="${gy(b)}" width="${GX1 - GX0}" height="${gy(a) - gy(b)}" fill="${ind === 'phenolphthalein' ? '#fbd3e9' : '#ffe2b8'}" opacity=".75"/><text x="${GX1 - 2}" y="${gy(b) - 1.5}" font-size="6" text-anchor="end" fill="#b0547f" font-weight="800">${IND[ind].name} ${a}–${b}</text>`; }
        if (!redox && pKa != null) { // buffer region actually titrated so far (Henderson–Hasselbalch zone 10–90 %)
          const v0 = 0.1 * Veq, v1 = Math.min(0.9 * Veq, V()); if (v1 > v0) s += `<rect x="${gx(v0)}" y="${GY0}" width="${gx(v1) - gx(v0)}" height="${GY1 - GY0}" fill="#d8f7ec" opacity=".8"/><text x="${gx(v0) + 2}" y="${GY1 - 3}" font-size="6" fill="#0f7a5c" font-weight="800">buffer</text>`;
        }
        const ticksY = redox ? [0, yMax / 2, yMax] : [0, 2, 4, 6, 7, 8, 10, 12, 14];
        ticksY.forEach(t => s += `<line x1="${GX0}" x2="${GX1}" y1="${gy(t)}" y2="${gy(t)}" stroke="${t === 7 && !redox ? '#c9cde3' : '#eef0fb'}" stroke-width=".6"/>${!redox && t === 7 ? '' : `<text x="${GX0 - 3}" y="${gy(t) + 2}" font-size="6.5" text-anchor="end" fill="#9aa0c0" font-weight="800">${redox ? fx(t, 1) : t}</text>`}`);
        const stepX = Vax <= 10 ? 2 : Vax <= 30 ? 5 : 10;
        for (let v = 0; v <= Vax + 1e-9; v += stepX) s += `<text x="${gx(v)}" y="${GY1 + 8}" font-size="6.5" text-anchor="middle" fill="#9aa0c0" font-weight="800">${v}</text>`;
        s += `<text x="${GX1}" y="${GY1 + 17}" font-size="6.5" text-anchor="end" fill="#6b7090" font-weight="800">V(${esc(tName)}) / mL</text><text x="${GX0 + 4}" y="${GY0 + 8}" font-size="7" fill="#6b7090" font-weight="900">${redox ? (A.ox ? 'C₂O₄²⁻' : 'Fe²⁺') + ' left / mmol' : 'pH'}</text>`;
        if (recorded != null) s += `<line x1="${gx(recorded)}" x2="${gx(recorded)}" y1="${GY0}" y2="${GY1}" stroke="#8b5cf6" stroke-dasharray="3 2" stroke-width="1"/>`;
        if (hist.length > 1) s += `<polyline points="${hist.map(([v, y]) => gx(Math.min(v, Vax)).toFixed(1) + ',' + gy(clamp(y, 0, yMax)).toFixed(1)).join(' ')}" fill="none" stroke="${redox ? '#7b1fa2' : '#3b82f6'}" stroke-width="2" stroke-linejoin="round"/>`;
        const cy = redox ? st.left : st.ph;
        s += `<circle cx="${gx(Math.min(V(), Vax))}" cy="${gy(clamp(cy, 0, yMax))}" r="3.2" fill="#ff6b6b" stroke="#fff" stroke-width="1.2"/>`;
        graph.innerHTML = s;
      }
      // ---------- update ----------
      function update() {
        const v = V(), st = state(v);
        bliq.setAttribute('y', BT + v * scale); bliq.setAttribute('height', Math.max(0, BB - BT - v * scale));
        fliq.setAttribute('y', liqTop(Va + v));
        let col, word;
        if (redox) {
          const pink = clamp(st.excessM / 2.5e-4, 0, 1);
          const base = A.ox ? flaskBase : mix(flaskBase, '#f6efc4', st.frac); // Fe2+ pale green → Fe3+ pale yellow
          col = pink > 0 ? mix(base, '#c2185b', 0.15 + pink * 0.55) : base;
          word = pink > 0.02 ? (pink > 0.45 ? 'pink-purple' : 'pale pink') : (A.ox ? 'colourless' : st.frac > 0.5 ? 'pale yellow' : 'pale green');
        } else {
          col = indColour(ind, st.ph, flaskBase);
          const D = IND[ind]; word = !D.r ? '—' : st.ph <= D.r[0] ? D.words[0] : st.ph >= D.r[1] ? D.words[1] : (D.a ? 'orange/changing' : 'pale pink');
          if (ind === 'bromothymolBlue' && st.ph > D.r[0] && st.ph < D.r[1]) word = 'green';
        }
        fliq.setAttribute('fill', col);
        vEl.textContent = fx(v, 2) + ' mL';
        phEl.textContent = showPH ? fx(st.ph, 2) : word;
        if (!redox) { hist.push([v, st.ph]); } else hist.push([v, st.left]);
        if (hist.length > 1600) hist = hist.filter((_, i) => i % 2 === 0);
        drawGraph(st);
        // notes
        let n = '';
        if (redox) {
          n = `<b>${eqn}</b><br>${ratioTxt}. ${A.ox ? 'Flask warmed to 60 °C; ' : ''}KMnO₄ is its own indicator.`;
        } else {
          const nAm = Ca * Va, nTm = Ct * v; // mmol
          if (pKa != null && nTm * nT > 0 && nTm * nT < nAm * nA) {
            const conj = nTm * nT, weak = nAm - conj, hh = pKa + Math.log10(conj / weak);
            n = A.kind === 'a' ? `H–H: pH = pK<sub>a</sub> + log([A⁻]/[HA]) = ${pKa} + log(${fx(conj, 2)}/${fx(weak, 2)}) = <b>${fx(hh, 2)}</b>`
              : `H–H: pOH = pK<sub>b</sub> + log([NH₄⁺]/[NH₄OH]) = ${pKa} + log(${fx(conj, 2)}/${fx(weak, 2)}) → pH <b>${fx(14 - hh, 2)}</b>`;
          } else n = `<b>${eqn}</b>`;
          if (recorded != null || v >= Veq) n += `<br>pH at equivalence = <b>${fx(eqState.ph, 2)}</b>${Math.abs(eqState.ph - 7) < 0.05 ? ' (neutral salt)' : eqState.ph > 7 ? ' (salt of weak acid → basic)' : ' (salt of weak base → acidic)'}`;
          else n += `<br>${pKa != null ? (A.kind === 'a' ? 'pK<sub>a</sub>' : 'pK<sub>b</sub>') + ' = ' + pKa + ' · ' : ''}${esc(aName)}: ${Va} mL, ${hidden ? '? M' : ff(Ca) + ' M'} · ${esc(tName)}: ${ff(Ct)} M`;
        }
        note.innerHTML = n;
        if (v >= CAP - 1e-9) { open = 0; setTap(0); setMsg('Burette empty — press Refill.', 'bad'); }
      }
      function dropAnim(n) {
        if (dropsG.childNodes.length > 6) return;
        const d = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
        d.setAttribute('cx', 52); d.setAttribute('cy', BB + 24); d.setAttribute('rx', 1.8); d.setAttribute('ry', 2.4); d.setAttribute('fill', redox ? tColour : '#9cc3ff');
        dropsG.appendChild(d); const t0 = performance.now(), yEnd = liqTop(Va + V());
        const step = t => { const k = (t - t0) / 260; if (k >= 1 || !d.isConnected) { d.remove(); return; } d.setAttribute('cy', BB + 24 + (yEnd - BB - 24) * k * k); requestAnimationFrame(step); };
        requestAnimationFrame(step);
        if (redox) { splash.setAttribute('cy', yEnd + 2); splash.setAttribute('rx', 12); splash.setAttribute('opacity', '.55'); flashT = performance.now(); }
      }
      function addDrops(k) {
        k = Math.min(k, Math.round((CAP - V()) / DROP)); if (k <= 0) return;
        drops += k; dropAnim(k); update();
      }
      // ---------- tap (stopcock) ----------
      function setTap(t) {
        open = clamp(t, 0, 1); const w = tap.clientWidth || 200;
        knob.style.left = (3 + open * (w - 44)) + 'px'; fill.style.width = (open > 0 ? 22 + open * (w - 44) : 0) + 'px';
        cock.style.transform = `rotate(${open * 90}deg)`;
        tapTxt.textContent = open < 0.04 ? 'closed — drag the tap ▶' : open < 0.35 ? 'open: dropwise' : open < 0.7 ? 'open: fast drops' : 'wide open: stream!';
      }
      const rate = () => open < 0.04 ? 0 : 0.1 + 2.9 * open * open; // mL s⁻¹
      let tapDrag = false;
      const tapPos = e => { const r = tap.getBoundingClientRect(); return (e.clientX - r.left - 22) / Math.max(1, r.width - 44); };
      const tDown = e => { tapDrag = true; try { tap.setPointerCapture(e.pointerId); } catch (x) {} setTap(tapPos(e)); };
      const tMove = e => { if (tapDrag) setTap(tapPos(e)); };
      const tUp = () => { tapDrag = false; if (open < 0.04) setTap(0); };
      tap.addEventListener('pointerdown', tDown); tap.addEventListener('pointermove', tMove); tap.addEventListener('pointerup', tUp); tap.addEventListener('pointercancel', tUp);
      function loop(t) {
        const dt = last ? Math.min(0.1, (t - last) / 1000) : 0; last = t;
        const r = rate();
        if (r > 0 && V() < CAP) { acc += r * dt; const k = Math.floor(acc / DROP + 1e-9); if (k > 0) { acc -= k * DROP; addDrops(k); } }
        else acc = 0;
        if (flashT && t - flashT > 350) { splash.setAttribute('opacity', 0); flashT = 0; }
        raf = requestAnimationFrame(loop);
      }
      raf = requestAnimationFrame(loop);

      // ---------- buttons ----------
      function reset() {
        drops = 0; acc = 0; hist = []; recorded = null; setTap(0); ansRow.style.display = 'none'; ansIn.value = ''; setMsg('Flask refilled: ' + Va + ' mL ' + aName + (redox ? ' + dil. H₂SO₄' : '') + '.');
        if (won) { won = false; api.resetWin && api.resetWin(); }
        update();
      }
      function record() {
        const v = V(); setTap(0);
        if (v <= 0) { setMsg('Add titrant first — drag the tap open.', 'bad'); api.sfx('hmm'); return; }
        recorded = v; update();
        const err = v - Veq;
        const calcTxt = redox ? `M = ${nT / nA === 2.5 ? '(5/2)' : '5'} × ${ff(Ct)} × ${fx(v, 2)} / ${Va}` : `${nA > 1 ? nA + ' × ' : ''}M × ${Va} = ${nT > 1 ? nT + ' × ' : ''}${ff(Ct)} × ${fx(v, 2)}`;
        const Mfrom = redox ? (nT / nA) * Ct * v / Va : nT * Ct * v / (nA * Va);
        if (gtype === 'halfeq') {
          const e2 = v - Veq / 2;
          if (Math.abs(e2) <= 0.2) { api.sfx('coin'); setMsg(`✓ Half-neutralised at ${fx(v, 2)} mL: pH = ${fx(state(v).ph, 2)} ≈ pK = ${pKa}.`, 'good'); winOnce(`At half-equivalence [salt] = [${A.kind === 'a' ? 'acid' : 'base'}], so log 1 = 0 and ${A.kind === 'a' ? 'pH = pKa' : 'pOH = pKb'} = ${pKa}.`); }
          else { api.sfx('wrong'); setMsg(`✗ ${fx(v, 2)} mL is ${e2 > 0 ? 'past' : 'before'} the half-way point (pH ${fx(state(v).ph, 2)}). Watch for pH = ${A.kind === 'a' ? pKa : fx(14 - pKa, 2)}. Refill and retry.`, 'bad'); }
          return;
        }
        const iw = indicatorWindow(ind);
        if (Math.abs(err) <= tol + 1e-9 && iw && (iw[1] < Veq - tol || iw[0] > Veq + tol)) {
          api.sfx('hmm');
          setMsg(`Reading ${fx(v, 2)} mL is right, but ${IND[ind].name} (pH ${IND[ind].r[0]}–${IND[ind].r[1]}) changes colour at about ${fx(iw[0], 1)}–${fx(iw[1], 1)} mL, not at equivalence (pH ${fx(eqState.ph, 2)}). Pick an indicator whose range lies on the steep jump.`, 'bad');
          return;
        }
        if (Math.abs(err) <= tol + 1e-9) {
          api.sfx('coin');
          if (gtype === 'molarity') { setMsg(`✓ Good end point: ${fx(v, 2)} mL. Now use ${calcTxt.replace('M', 'M(' + aName + ')')} and type the molarity.`, 'good'); ansRow.style.display = 'flex'; try { ansIn.focus({ preventScroll: true }); } catch (x) {} }
          else { setMsg(`✓ End point ${fx(v, 2)} mL (equivalence ${fx(Veq, 2)} mL). ${calcTxt} ⇒ M = ${fx(Mfrom, 4)} M`, 'good'); winOnce(`End point at ${fx(v, 2)} mL! ${redox ? ratioTxt : 'n₁M₁V₁ = n₂M₂V₂'} gives M(${aName}) = ${fx(Mfrom, 4)} M.`); }
        } else {
          api.sfx('wrong');
          let why = err > 0 ? `Overshot by ${fx(err, 2)} mL.` : `Too early by ${fx(-err, 2)} mL.`;
          if (iw && (iw[1] < Veq - tol || iw[0] > Veq + tol)) {
            const [a, b] = IND[ind].r, eph = eqState.ph;
            why += ` ${IND[ind].name} changes at pH ${a}–${b}, but the equivalence pH is ${fx(eph, 2)} — the jump there does not pass through its range. Choose a better indicator.`;
          }
          if (gtype === 'molarity') { why += ' Refill and titrate again.'; }
          setMsg('✗ ' + why + ' Press Refill.', 'bad');
        }
      }
      function check() {
        const m = parseFloat(String(ansIn.value).replace(',', '.').replace(/[^\d.]/g, ''));
        if (!(m > 0)) { setMsg('Type a number like 0.105', 'bad'); return; }
        if (Math.abs(m - Ca) / Ca <= 0.02) { api.sfx('coin'); setMsg(`✓ Correct: ${fx(Ca, 4)} M.`, 'good'); winOnce(`Unknown molarity = ${fx(Ca, 4)} M (you found ${m}). End point ${fx(recorded, 2)} mL.`); }
        else { api.sfx('wrong'); setMsg(`✗ Not quite. ${redox ? ratioTxt + ': moles of reductant = ' + (nT / nA) + ' × moles of MnO₄⁻.' : 'Use n₁M₁V₁ = n₂M₂V₂ (n = ' + nA + ' for ' + aName + ', ' + nT + ' for ' + tName + ').'} Volumes in mL cancel.`, 'bad'); }
      }
      root.querySelectorAll('[data-i]').forEach(b => b.onclick = () => { ind = b.dataset.i; api.sfx('tap'); root.querySelectorAll('[data-i]').forEach(x => x.classList.toggle('on', x === b)); reset(); setMsg('Fresh flask with ' + IND[ind].name + '.'); });
      root.querySelectorAll('[data-i]').forEach(x => x.classList.toggle('on', x.dataset.i === ind));
      root.querySelector('[data-a=drop]').onclick = () => { api.sfx('tap'); addDrops(1); };
      root.querySelector('[data-a=rec]').onclick = record;
      root.querySelector('[data-a=reset]').onclick = () => { api.sfx('tap'); reset(); };
      root.querySelector('[data-a=check]').onclick = check;
      const onKey = e => { if (e.key === 'Enter') check(); }; ansIn.addEventListener('keydown', onKey);
      const onResize = () => setTap(open); window.addEventListener('resize', onResize);
      reset(); setMsg(redox ? 'Drag the tap to add KMnO₄. Each purple drop decolourises until the end point.' : 'Drag the tap open; slow to dropwise near the end point.');
      requestAnimationFrame(() => setTap(open));
      return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', onResize); tap.removeEventListener('pointerdown', tDown); tap.removeEventListener('pointermove', tMove); tap.removeEventListener('pointerup', tUp); tap.removeEventListener('pointercancel', tUp); };
    },
    example: {
      mode: 'acidbase', analyte: 'CH3COOH', titrant: 'NaOH', Ca: 0.1, Va: 20, Ct: 0.1,
      indicators: ['phenolphthalein', 'methylOrange', 'bromothymolBlue'], indicator: 'methylOrange', goal: { type: 'endpoint' }, tol: 0.1,
      challenge: 'Class 11 · Weak acid vs strong base: pick the right indicator and record the end point within ±0.1 mL.'
    },
    examples: [
      { mode: 'acidbase', analyte: 'H2C2O4', titrant: 'NaOH', Va: 10, Ct: 0.1, indicators: ['phenolphthalein'], goal: { type: 'molarity' },
        challenge: 'CBSE practical: titrate 10 mL oxalic acid (unknown M) with 0.1 M NaOH using phenolphthalein, then find its molarity.' },
      { mode: 'redox', analyte: 'Fe2+', Ca: 0.1, Va: 20, Ct: 0.02, goal: { type: 'endpoint' }, tol: 0.1,
        challenge: 'Class 12 · Mohr\'s salt vs KMnO₄ (1 : 5): stop at the first permanent pale pink.' },
      { mode: 'acidbase', analyte: 'CH3COOH', Ca: 0.1, Va: 20, Ct: 0.1, indicators: ['none', 'phenolphthalein'], indicator: 'none', goal: { type: 'halfeq' },
        challenge: 'Henderson–Hasselbalch: using the pH meter, stop at half-neutralisation where pH = pKa = 4.76.' }
    ]
  });
})();
