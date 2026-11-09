/* Knowtopia Concept Lab: photosynthesis — "Photosynthesis lab"
 *
 * PARAMS (all optional)
 *  mode       string  'rate'    : plant with sliders (light, CO₂, water, temperature); live rate meter,
 *                                 O₂ bubbles, limiting factor shown.
 *                     'bubbles' : water plant (Hydrilla) in a beaker under a lamp; count O₂ bubbles per minute.
 *                     'starch'  : starch test on a leaf (destarch → cover with black paper → sunlight →
 *                                 boil in alcohol → iodine); only the lit part turns blue-black.   default 'rate'
 *  factors    array   which sliders to show, from 'light','co2','water','temp'
 *                                         default rate: all four; bubbles: ['light','co2','temp']
 *  start      object  starting values {light, co2, water: 0–100 (%), temp: °C 0–50}  default {light:30,co2:50,water:80,temp:25}
 *  lightAs    string  bubbles mode: 'distance' (lamp distance 10–50 cm, light ∝ 1/d²) | 'intensity' default 'distance'
 *  goal       object  rate mode: {rate:n} reach a rate of at least n % |
 *                     {limit:'light'|'co2'|'water'|'temp', rate:n} reach n % while that factor is limiting
 *                     bubbles mode: {bpm:n} reach n bubbles per minute                       default {rate:80} / {bpm:40}
 *  equation   string  'word' | 'symbol' | 'both'                                             default 'both'
 *  variant    string  starch mode: 'paper' (black paper strip) | 'variegated' (white patches, no chlorophyll)
 *                                                                                             default 'paper'
 *  challenge  string  challenge sentence (any language); a default is generated
 *  Model: rate = 100 × min(f(light), f(CO₂), f(water)) × f(temperature)  (law of limiting factors);
 *  f rises and levels off (saturation); temperature has an optimum near 30–35 °C and falls above it (enzymes).
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));
  const num = (v, d) => (v === null || v === undefined || v === '' || !Number.isFinite(+v)) ? d : +v;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const sat = x => (1 - Math.exp(-x / 26)) / (1 - Math.exp(-100 / 26));
  const fTemp = T => T <= 0 ? 0 : T < 30 ? Math.sin(Math.PI / 2 * T / 30) : T <= 35 ? 1 : Math.max(0, 1 - Math.pow((T - 35) / 12, 2));
  const FN = { light: 'Light', co2: 'CO₂', water: 'Water', temp: 'Temperature' };
  const EQ = {
    word: 'carbon dioxide + water → glucose + oxygen  (light, chlorophyll)',
    symbol: '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂'
  };

  const CSS = `
  .lb-photosynthesis{font-weight:700;color:#1b1f3a;user-select:none;-webkit-user-select:none}
  .lb-photosynthesis-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:8px 11px;font-size:13.5px;line-height:1.3;margin-bottom:7px}
  .lb-photosynthesis svg{display:block;width:100%;height:auto;border-radius:16px}
  .lb-photosynthesis-eq{font-size:11.5px;text-align:center;color:#2b6a4f;background:#eafaf3;border-radius:10px;padding:4px 6px;margin-top:5px;line-height:1.3}
  .lb-photosynthesis-grid{display:grid;grid-template-columns:1fr 1fr;gap:2px 10px;margin-top:4px}
  .lb-photosynthesis-sl{display:flex;flex-direction:column}
  .lb-photosynthesis-sl label{display:flex;justify-content:space-between;font-size:12px;color:#6b7090}
  .lb-photosynthesis-sl label b{color:#1b1f3a}
  .lb-photosynthesis-sl.lim label{color:#c94545}
  .lb-photosynthesis input[type=range]{width:100%;height:34px;-webkit-appearance:none;appearance:none;background:transparent;margin:0}
  .lb-photosynthesis input[type=range]::-webkit-slider-runnable-track{height:9px;border-radius:99px;background:var(--tr,#e3e6f6)}
  .lb-photosynthesis input[type=range]::-moz-range-track{height:9px;border-radius:99px;background:var(--tr,#e3e6f6)}
  .lb-photosynthesis input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;border-radius:50%;background:#fff;border:4px solid #2ed3a5;margin-top:-8.5px;box-shadow:0 2px 5px rgba(0,0,0,.2)}
  .lb-photosynthesis input[type=range]::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:#fff;border:4px solid #2ed3a5}
  .lb-photosynthesis-steps{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px}
  .lb-photosynthesis-btn{min-height:42px;border:2px solid #e3e6f6;border-radius:13px;background:#fff;font-family:inherit;font-weight:800;font-size:12px;color:#1b1f3a;cursor:pointer;padding:3px 6px;line-height:1.15}
  .lb-photosynthesis-btn:active{transform:translateY(2px)}
  .lb-photosynthesis-btn.done{background:#e3fbf3;border-color:#2ed3a5;color:#0f7a5c}
  .lb-photosynthesis-btn.g{background:#eef0fb;border-color:#eef0fb}
  .lb-photosynthesis-msg{font-size:12.5px;color:#6b7090;margin-top:6px;line-height:1.3;min-height:32px}
  .lb-photosynthesis-msg.bad{color:#c94545}.lb-photosynthesis-msg.good{color:#0f7a5c}`;

  Labs.register('photosynthesis', {
    title: 'Photosynthesis lab',
    subjects: ['science', 'biology', 'evs'],
    render(host, p, api) {
      const mode = ['rate', 'bubbles', 'starch'].includes(p.mode) ? p.mode : 'rate';
      const st = Object.assign({ light: 30, co2: 50, water: 80, temp: 25 }, (p.start && typeof p.start === 'object') ? p.start : {});
      const V = { light: clamp(num(st.light, 30), 0, 100), co2: clamp(num(st.co2, 50), 0, 100), water: clamp(num(st.water, 80), 0, 100), temp: clamp(num(st.temp, 25), 0, 50) };
      const eqMode = ['word', 'symbol', 'both'].includes(p.equation) ? p.equation : 'both';
      const eqHTML = eqMode === 'both' ? `${EQ.word}<br><b>${EQ.symbol}</b>` : eqMode === 'word' ? EQ.word : `<b>${EQ.symbol}</b> <span style="opacity:.7">(light, chlorophyll)</span>`;
      let raf = 0, alive = true, timers = [];
      const later = (f, ms) => timers.push(setTimeout(f, ms));
      let won = false; const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };
      const NS = 'http://www.w3.org/2000/svg';
      const mk = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };

      // ===================================================================== STARCH
      if (mode === 'starch') {
        const varieg = p.variant === 'variegated';
        const challenge = p.challenge || (varieg ? 'Do the starch test on a variegated leaf. Which parts make starch?' : 'Do the starch test in the right order. Show that only the lit part makes starch!');
        const steps = varieg
          ? [['dark', '🌑 Keep in dark 2 days'], ['sun', '☀️ Sunlight 6 hours'], ['alcohol', '🔥 Boil in alcohol'], ['iodine', '🟤 Add iodine']]
          : [['dark', '🌑 Keep in dark 2 days'], ['sun', '☀️ Sunlight 6 hours'], ['alcohol', '🔥 Remove paper, boil in alcohol'], ['iodine', '🟤 Add iodine']];
        host.innerHTML = `<style>${CSS}</style><div class="lb-photosynthesis">
          <div class="lb-photosynthesis-ch">🎯 Challenge: ${esc(challenge)}</div>
          <svg viewBox="0 0 352 188" class="lb-photosynthesis-leaf" style="background:linear-gradient(#f3fbff,#eef8ef);touch-action:none"></svg>
          <div class="lb-photosynthesis-steps">${steps.map(([k, t]) => `<button class="lb-photosynthesis-btn" data-k="${k}">${t}</button>`).join('')}</div>
          <div class="lb-photosynthesis-steps" style="grid-template-columns:1fr auto"><div class="lb-photosynthesis-msg"></div><button class="lb-photosynthesis-btn g lb-photosynthesis-reset">↺ Reset</button></div></div>`;
        const root = host.querySelector('.lb-photosynthesis'), svg = root.querySelector('svg'), msg = root.querySelector('.lb-photosynthesis-msg');
        const setMsg = (t, c) => { msg.innerHTML = t; msg.className = 'lb-photosynthesis-msg' + (c ? ' ' + c : ''); };
        const COLS = 18, ROWS = 8, X0 = 36, Y0 = 22, CW = 16, CH = 17;
        const leafD = `M${X0 - 4} ${Y0 + ROWS * CH / 2} C ${X0 + 40} ${Y0 - 30}, ${X0 + 220} ${Y0 - 26}, ${X0 + COLS * CW + 8} ${Y0 + ROWS * CH / 2} C ${X0 + 220} ${Y0 + ROWS * CH + 26}, ${X0 + 40} ${Y0 + ROWS * CH + 30}, ${X0 - 4} ${Y0 + ROWS * CH / 2} Z`;
        const cid = 'lbps' + Math.random().toString(36).slice(2, 8);
        mk('clipPath', { id: cid }, mk('defs', {}, svg)).appendChild(mk('path', { d: leafD }));
        mk('path', { d: `M4 ${Y0 + ROWS * CH / 2} L${X0} ${Y0 + ROWS * CH / 2}`, stroke: '#6aa84f', 'stroke-width': 5, 'stroke-linecap': 'round' }, svg);
        const gCells = mk('g', { 'clip-path': `url(#${cid})` }, svg);
        const cells = [];
        const cxm = X0 + COLS * CW / 2, cym = Y0 + ROWS * CH / 2;
        for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
          const x = X0 + c * CW, y = Y0 + r * CH;
          const dx = (x + CW / 2 - cxm) / (COLS * CW / 2), dy = (y + CH / 2 - cym) / (ROWS * CH / 2 + 18);
          const white = varieg && (dx * dx + dy * dy > 0.42 || (Math.sin(c * 1.7 + r) > 0.85 && dx * dx + dy * dy > 0.25));
          cells.push({ c, r, white, starch: true, el: mk('rect', { x, y: y, width: CW + 0.6, height: CH + 0.6 }, gCells) });
        }
        mk('path', { d: `M${X0} ${cym} L${X0 + COLS * CW} ${cym}`, stroke: 'rgba(255,255,255,.55)', 'stroke-width': 2.5, fill: 'none', 'clip-path': `url(#${cid})` }, svg);
        for (let i = 1; i < 6; i++) { const x = X0 + i * COLS * CW / 6; mk('path', { d: `M${x} ${cym} Q ${x + 18} ${cym - 30} ${x + 30} ${cym - 52} M${x} ${cym} Q ${x + 18} ${cym + 30} ${x + 30} ${cym + 52}`, stroke: 'rgba(255,255,255,.4)', 'stroke-width': 1.5, fill: 'none', 'clip-path': `url(#${cid})` }, svg); }
        mk('path', { d: leafD, fill: 'none', stroke: 'rgba(30,80,40,.35)', 'stroke-width': 2 }, svg);
        // black paper strip (paper variant)
        let paperC = 7, paperW = 5; // columns covered: paperC .. paperC+paperW-1
        const paper = mk('g', { style: 'cursor:grab' }, svg);
        const pr = mk('rect', { y: 2, height: 160, rx: 4, fill: '#1b1f3a', opacity: .92 }, paper);
        const pt = mk('text', { y: 176, 'text-anchor': 'middle', 'font-size': 10.5, 'font-weight': 800, fill: '#1b1f3a' }, paper);
        const sun = mk('g', { opacity: 0, style: 'transition:opacity .5s' }, svg);
        mk('circle', { cx: 330, cy: 18, r: 13, fill: '#ffc93c' }, sun);
        for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; mk('line', { x1: 330 + Math.cos(a) * 17, y1: 18 + Math.sin(a) * 17, x2: 330 + Math.cos(a) * 23, y2: 18 + Math.sin(a) * 23, stroke: '#ffc93c', 'stroke-width': 3, 'stroke-linecap': 'round' }, sun); }
        const legend = mk('text', { x: 176, y: 184, 'text-anchor': 'middle', 'font-size': 10.5, 'font-weight': 800, fill: '#6b7090' }, svg);
        let done = [], paperOn = !varieg, chlorophyll = true, iodine = false;
        const covered = c => paperOn && c >= paperC && c < paperC + paperW;
        function paint() {
          for (const k of cells) {
            let col;
            if (iodine) {
              const hasGreen = chlorophyll && !k.white;
              col = k.starch ? (hasGreen ? '#1d2a3f' : '#16213d') : (hasGreen ? '#6f7d2d' : '#c98a2b');
            } else if (chlorophyll) col = k.white ? '#f2f6e8' : (k.r + k.c) % 2 ? '#3fae5a' : '#43b45f';
            else col = '#f3efcf';
            k.el.setAttribute('fill', col);
          }
          paper.style.display = paperOn ? '' : 'none';
          pr.setAttribute('x', X0 + paperC * CW - 2); pr.setAttribute('width', paperW * CW + 4);
          pt.setAttribute('x', X0 + (paperC + paperW / 2) * CW); pt.textContent = done.includes('sun') ? 'black paper' : '↔ drag paper';
          legend.textContent = iodine ? (chlorophyll ? 'Iodine on a green leaf — hard to see!' : 'Blue-black = starch present · brown = no starch') : !chlorophyll ? 'Leaf is now pale — ready for iodine' : '';
          root.querySelectorAll('[data-k]').forEach(b => b.classList.toggle('done', done.includes(b.dataset.k)));
        }
        // drag paper
        let drag = null;
        const toX = e => { const r = svg.getBoundingClientRect(); return (e.clientX - r.left) * 352 / r.width; };
        paper.addEventListener('pointerdown', e => { if (done.includes('sun')) { setMsg('The paper must stay in place now.', 'bad'); return; } drag = { x: toX(e), c: paperC }; paper.setPointerCapture && paper.setPointerCapture(e.pointerId); e.preventDefault(); });
        paper.addEventListener('pointermove', e => { if (!drag) return; paperC = clamp(Math.round(drag.c + (toX(e) - drag.x) / CW), 0, COLS - paperW); paint(); });
        const endDrag = () => { if (drag) { drag = null; api.sfx('tap'); } };
        paper.addEventListener('pointerup', endDrag); paper.addEventListener('pointercancel', endDrag);
        function step(k) {
          api.sfx('tap');
          if (iodine) { setMsg('Test finished. Press Reset to try again.'); return; }
          if (k === 'dark') {
            if (done.includes('sun')) { setMsg('Too late — keep it in the dark <b>before</b> sunlight.', 'bad'); api.sfx('wrong'); return; }
            cells.forEach(c => c.starch = false); done.push('dark'); setMsg('Starch used up. The leaf now has <b>no starch</b>.' + (varieg ? '' : ' Drag the black paper where you like.'));
          } else if (k === 'sun') {
            if (!chlorophyll) { setMsg('The leaf was boiled — it cannot make food now.', 'bad'); api.sfx('wrong'); return; }
            sun.setAttribute('opacity', 1); later(() => sun.setAttribute('opacity', 0), 1400);
            cells.forEach(c => { if (!covered(c.c) && !c.white) c.starch = true; }); if (!done.includes('sun')) done.push('sun');
            setMsg(varieg ? 'Green parts used sunlight to make starch.' : 'The leaf made food in sunlight… but not under the paper!');
          } else if (k === 'alcohol') {
            chlorophyll = false; paperOn = false; if (!done.includes('alcohol')) done.push('alcohol');
            setMsg('Alcohol removed the green chlorophyll, so the colour test is easy to see.');
          } else if (k === 'iodine') {
            iodine = true; done.push('iodine');
            if (chlorophyll) { setMsg('The green colour hides the result. Reset and boil in alcohol before iodine!', 'bad'); api.sfx('wrong'); }
            else if (!done.includes('dark')) { setMsg('Blue-black everywhere — the leaf already had old starch. Destarch it in the dark first!', 'bad'); api.sfx('wrong'); }
            else if (!done.includes('sun')) { setMsg('No starch anywhere — the leaf never got sunlight.', 'bad'); api.sfx('hmm'); }
            else {
              setMsg(varieg ? '✓ Only the parts that were green turned blue-black: <b>chlorophyll is needed</b>.' : '✓ Only the part that got light turned blue-black: <b>light is needed</b> for photosynthesis.', 'good');
              later(() => winOnce(varieg ? 'Starch formed only where there was chlorophyll!' : 'Starch formed only where light reached the leaf!'), 500);
            }
          }
          paint();
        }
        root.querySelectorAll('[data-k]').forEach(b => b.onclick = () => step(b.dataset.k));
        root.querySelector('.lb-photosynthesis-reset').onclick = () => {
          done = []; paperOn = !varieg; chlorophyll = true; iodine = false; cells.forEach(c => c.starch = true); api.sfx('tap'); paint();
          setMsg('Steps: tap them in the order you think is right.'); if (won) { won = false; api.resetWin && api.resetWin(); }
        };
        paint(); setMsg('Tap the steps in the order you think is right. Iodine turns <b>blue-black</b> with starch.');
        return () => { alive = false; timers.forEach(clearTimeout); };
      }

      // ===================================================================== RATE + BUBBLES
      const bubbles = mode === 'bubbles';
      const lightAs = bubbles && p.lightAs !== 'intensity' ? 'distance' : 'intensity';
      const facs = (Array.isArray(p.factors) && p.factors.length ? p.factors : bubbles ? ['light', 'co2', 'temp'] : ['light', 'co2', 'water', 'temp']).filter(f => FN[f] && !(bubbles && f === 'water'));
      if (bubbles) V.water = 100; // plant is under water
      let dist = clamp(num(st.distance, 40), 10, 50);
      const goal = (p.goal && typeof p.goal === 'object') ? p.goal : (bubbles ? { bpm: 40 } : { rate: 80 });
      const lightNow = () => lightAs === 'distance' ? clamp(Math.pow(10 / dist, 2) * 100, 0, 100) : V.light;
      const rateNow = () => { const f = { light: sat(lightNow()), co2: sat(V.co2), water: sat(V.water) }; const m = Math.min(f.light, f.co2, f.water); const t = fTemp(V.temp); return { r: 100 * m * t, f, t }; };
      function limiting(R) {
        const f = R.f; const ks = Object.keys(f).filter(k => facs.includes(k) || k === 'water' && !bubbles);
        let k = ks.reduce((a, b) => f[a] <= f[b] ? a : b, ks[0]);
        if (R.t < f[k] && R.t < 0.95) k = 'temp';
        return (k !== 'temp' && f[k] > 0.97) || (k === 'temp' && R.t > 0.97) ? null : k;
      }
      let challenge = p.challenge;
      if (!challenge) {
        if (bubbles) challenge = `Make the water plant give at least ${goal.bpm || 40} oxygen bubbles per minute.`;
        else if (goal.limit) challenge = `Make ${FN[goal.limit] || goal.limit} the limiting factor while the rate is ${goal.rate || 50}% or more.`;
        else challenge = `Get the rate of photosynthesis to ${goal.rate || 80}% or more.`;
      }
      const sliderHTML = facs.map(f => {
        if (f === 'light' && lightAs === 'distance') return `<div class="lb-photosynthesis-sl" data-f="light"><label>💡 Lamp distance <b class="v"></b></label><input type="range" min="10" max="50" step="1" value="${dist}" style="--tr:linear-gradient(90deg,#ffe28a,#e3e6f6)"></div>`;
        const ic = { light: '☀️ Light', co2: '🫧 CO₂', water: '💧 Water', temp: '🌡️ Temp' }[f];
        const tr = { light: 'linear-gradient(90deg,#e3e6f6,#ffc93c)', co2: 'linear-gradient(90deg,#e3e6f6,#9aa0c0)', water: 'linear-gradient(90deg,#e3e6f6,#3b82f6)', temp: 'linear-gradient(90deg,#7cc4ff,#2ed3a5 55%,#ff6b6b)' }[f];
        return `<div class="lb-photosynthesis-sl" data-f="${f}"><label>${ic} <b class="v"></b></label><input type="range" min="0" max="${f === 'temp' ? 50 : 100}" step="1" value="${V[f]}" style="--tr:${tr}"></div>`;
      }).join('');
      host.innerHTML = `<style>${CSS}</style><div class="lb-photosynthesis">
        <div class="lb-photosynthesis-ch">🎯 Challenge: ${esc(challenge)}</div>
        <svg viewBox="0 0 352 196"></svg>
        <div class="lb-photosynthesis-grid">${sliderHTML}</div>
        <div class="lb-photosynthesis-eq">${eqHTML}</div></div>`;
      const root = host.querySelector('.lb-photosynthesis'), svg = root.querySelector('svg');
      root.querySelectorAll('.lb-photosynthesis-sl').forEach(d => {
        const f = d.dataset.f, inp = d.querySelector('input');
        inp.oninput = () => { if (f === 'light' && lightAs === 'distance') dist = +inp.value; else V[f] = +inp.value; };
      });
      // ---------- static scene ----------
      const gid = 'lbpg' + Math.random().toString(36).slice(2, 8);
      const defs = mk('defs', {}, svg);
      const sky = mk('linearGradient', { id: gid + 's', x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
      const s1 = mk('stop', { offset: 0, 'stop-color': '#bfe6ff' }, sky); mk('stop', { offset: 1, 'stop-color': '#f4fbff' }, sky);
      mk('rect', { x: 0, y: 0, width: 352, height: 196, fill: `url(#${gid}s)` }, svg);
      const dim = mk('rect', { x: 0, y: 0, width: 352, height: 196, fill: '#1b1f3a', opacity: 0 }, svg);
      const PX = bubbles ? 150 : 130; // plant x
      let lamp, beam, sunG, soil, glassTop = 52;
      if (bubbles) {
        // beaker
        mk('rect', { x: 96, y: glassTop, width: 112, height: 132, rx: 10, fill: 'rgba(120,190,255,.35)', stroke: '#9aa6d6', 'stroke-width': 3 }, svg);
        mk('rect', { x: 96, y: glassTop - 4, width: 112, height: 8, rx: 4, fill: '#c9cde3' }, svg);
        // funnel + test tube
        mk('path', { d: `M112 170 L192 170 L160 128 L160 70 L144 70 L144 128 Z`, fill: 'rgba(255,255,255,.45)', stroke: '#9aa6d6', 'stroke-width': 2 }, svg);
        beam = mk('path', { d: '', fill: '#fff3b0', opacity: .5 }, svg);
        lamp = mk('g', {}, svg);
        mk('rect', { x: -10, y: -16, width: 30, height: 32, rx: 6, fill: '#6b7090' }, lamp);
        mk('circle', { cx: -10, cy: 0, r: 12, fill: '#ffe066' }, lamp);
        mk('text', { x: 5, y: 32, 'text-anchor': 'middle', 'font-size': 9.5, 'font-weight': 800, fill: '#6b7090', class: 'dl' }, lamp);
      } else {
        sunG = mk('g', {}, svg);
        mk('circle', { cx: 34, cy: 34, r: 18, fill: '#ffc93c' }, sunG);
        for (let i = 0; i < 10; i++) { const a = i * Math.PI / 5; mk('line', { x1: 34 + Math.cos(a) * 23, y1: 34 + Math.sin(a) * 23, x2: 34 + Math.cos(a) * 30, y2: 34 + Math.sin(a) * 30, stroke: '#ffc93c', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, sunG); }
        soil = mk('path', { d: `M${PX - 46} 160 L${PX + 46} 160 L${PX + 36} 194 L${PX - 36} 194 Z`, fill: '#c46a3b' }, svg);
        mk('rect', { x: PX - 50, y: 154, width: 100, height: 10, rx: 4, fill: '#a5532c' }, svg);
      }
      // plant
      const plant = mk('g', {}, svg);
      if (bubbles) {
        mk('path', { d: `M${PX} 182 C ${PX - 6} 150, ${PX + 6} 120, ${PX + 2} 92`, stroke: '#2f9e55', 'stroke-width': 4, fill: 'none' }, plant);
        for (let i = 0; i < 9; i++) { const y = 176 - i * 9.5, s = i % 2 ? 1 : -1; mk('ellipse', { cx: PX + s * 9, cy: y, rx: 9, ry: 3, fill: '#3fae5a', transform: `rotate(${s * -25} ${PX + s * 9} ${y})` }, plant); }
      } else {
        mk('path', { d: `M${PX} 156 C ${PX - 4} 120, ${PX + 6} 90, ${PX} 52`, stroke: '#2f9e55', 'stroke-width': 6, fill: 'none', 'stroke-linecap': 'round' }, plant);
        const leaves = [[PX - 30, 128, -30], [PX + 30, 112, 30], [PX - 30, 92, -25], [PX + 28, 72, 25], [PX, 46, 0]];
        leaves.forEach(([x, y, a]) => mk('path', { d: `M0 0 C 10 -14, 30 -14, 40 0 C 30 14, 10 14, 0 0 Z`, fill: '#43b45f', stroke: '#2f9e55', 'stroke-width': 1.5, transform: `translate(${a ? PX + (x < PX ? -2 : 2) : PX} ${a ? y : 54}) rotate(${a ? (x < PX ? 205 : -25) : -90})` }, plant));
      }
      const xyLeaves = bubbles ? [[PX + 2, 92]] : [[PX - 22, 118], [PX + 22, 102], [PX - 22, 82], [PX + 22, 62], [PX, 34]];
      const gMov = mk('g', {}, svg);
      // meter
      const MX = 300;
      mk('rect', { x: MX - 22, y: 16, width: 44, height: 150, rx: 12, fill: '#ffffff', stroke: '#e3e6f6', 'stroke-width': 2 }, svg);
      const mBar = mk('rect', { x: MX - 12, y: 156, width: 24, height: 0, rx: 6, fill: '#2ed3a5' }, svg);
      let goalLine = null;
      const gv = bubbles ? null : num(goal.rate, goal.limit ? 50 : 80);
      if (gv != null) { const gy = 156 - gv / 100 * 132; goalLine = mk('path', { d: `M${MX - 20} ${gy} L${MX + 20} ${gy}`, stroke: '#ff6b6b', 'stroke-width': 2, 'stroke-dasharray': '4 3' }, svg); mk('text', { x: MX - 24, y: gy + 3, 'text-anchor': 'end', 'font-size': 9, 'font-weight': 800, fill: '#ff6b6b' }, svg).textContent = 'goal'; }
      const mTxt = mk('text', { x: MX, y: 182, 'text-anchor': 'middle', 'font-size': 14, 'font-weight': 900, fill: '#1b1f3a' }, svg);
      const mLab = mk('text', { x: MX, y: 193, 'text-anchor': 'middle', 'font-size': 8.5, 'font-weight': 800, fill: '#6b7090' }, svg);
      mLab.textContent = bubbles ? 'bubbles / min' : 'rate';
      const limTxt = mk('text', { x: bubbles ? 240 : 236, y: 14, 'text-anchor': 'end', 'font-size': 10.5, 'font-weight': 800, fill: '#c94545' }, svg);
      if (bubbles) { mk('text', { x: 152, y: 66, 'text-anchor': 'middle', 'font-size': 9, 'font-weight': 800, fill: '#2f6b8f' }, svg).textContent = 'O₂ collects'; }
      const gasCol = bubbles ? mk('rect', { x: 146, y: 72, width: 12, height: 0, fill: 'rgba(255,255,255,.95)' }, svg) : null;

      const parts = []; let acc = 0, accC = 0, accW = 0, tAll = 0, gas = 0, holdT = 0;
      let last = performance.now();
      function frame(now) {
        if (!alive) return;
        const dt = clamp((now - last) / 1000, 0, 0.05); last = now; tAll += dt;
        const R = rateNow(), lim = limiting(R), L = lightNow();
        // labels
        root.querySelectorAll('.lb-photosynthesis-sl').forEach(d => {
          const f = d.dataset.f, v = d.querySelector('.v');
          const t = f === 'light' && lightAs === 'distance' ? dist + ' cm' : f === 'temp' ? V.temp + ' °C' : V[f] + '%';
          if (v.textContent !== t) v.textContent = t;
          d.classList.toggle('lim', lim === f);
        });
        // scene
        if (sunG) { sunG.setAttribute('opacity', (0.15 + 0.85 * L / 100).toFixed(2)); dim.setAttribute('opacity', ((1 - L / 100) * 0.28).toFixed(3)); s1.setAttribute('stop-color', L > 50 ? '#bfe6ff' : '#9fb7d6'); }
        if (soil) soil.setAttribute('fill', V.water < 25 ? '#d9a27a' : V.water < 60 ? '#b5683f' : '#8a4a2b');
        if (lamp) {
          const lx = 96 - 8 - (dist - 10) * 1.9; lamp.setAttribute('transform', `translate(${lx} 120)`); lamp.querySelector('.dl').textContent = dist + ' cm';
          beam.setAttribute('d', `M${lx - 4} 112 L96 ${100 - 10} L96 ${140 + 10} L${lx - 4} 128 Z`); beam.setAttribute('opacity', (0.15 + 0.6 * L / 100).toFixed(2));
          dim.setAttribute('opacity', ((1 - L / 100) * 0.18).toFixed(3));
        }
        // spawn particles
        const spawnRate = bubbles ? R.r * 0.6 / 60 : R.r / 100 * 6;
        acc += spawnRate * dt;
        while (acc >= 1) {
          acc -= 1; const [x, y] = xyLeaves[Math.floor(Math.random() * xyLeaves.length)];
          const e = mk('g', {}, gMov); mk('circle', { r: bubbles ? 3.5 : 6, fill: '#ffffff', stroke: '#7cc4ff', 'stroke-width': 1.5 }, e);
          if (!bubbles) { const t = mk('text', { y: 2.6, 'text-anchor': 'middle', 'font-size': 6, 'font-weight': 900, fill: '#3b82f6' }, e); t.textContent = 'O₂'; }
          parts.push({ e, x, y, vx: (Math.random() - .5) * 12, vy: bubbles ? -40 : -26, k: 'o' });
        }
        if (!bubbles) {
          accC += (V.co2 / 100) * 3.5 * dt;
          while (accC >= 1) { accC -= 1; const e = mk('g', {}, gMov); mk('circle', { r: 7, fill: '#e9ebf5', stroke: '#9aa0c0', 'stroke-width': 1 }, e); const t = mk('text', { y: 2.4, 'text-anchor': 'middle', 'font-size': 5.6, 'font-weight': 900, fill: '#6b7090' }, e); t.textContent = 'CO₂'; const [tx, ty] = xyLeaves[Math.floor(Math.random() * xyLeaves.length)]; parts.push({ e, x: 236 - Math.random() * 10, y: 30 + Math.random() * 120, tx, ty, k: 'c' }); }
          accW += (V.water / 100) * 3 * dt;
          while (accW >= 1) { accW -= 1; const e = mk('path', { d: 'M0 -4 C 3 0, 3 3, 0 3.5 C -3 3, -3 0, 0 -4 Z', fill: '#3b82f6' }, gMov); parts.push({ e, x: PX + (Math.random() - .5) * 3, y: 178, k: 'w' }); }
        }
        for (let i = parts.length - 1; i >= 0; i--) {
          const q = parts[i]; let dead = false;
          if (q.k === 'o') { q.x += q.vx * dt; q.y += q.vy * dt; if (bubbles) { if (q.y < 128 && q.x > 140 && q.x < 164) { q.x += (152 - q.x) * Math.min(1, dt * 8); } if (q.y < 74 + gas) { dead = true; gas = Math.min(50, gas + 0.12); } } else if (q.y < -8) dead = true; }
          else if (q.k === 'c') { q.x += (q.tx - q.x) * Math.min(1, dt * 1.1); q.y += (q.ty - q.y) * Math.min(1, dt * 1.1); if (Math.hypot(q.tx - q.x, q.ty - q.y) < 6) dead = true; }
          else { q.y -= 60 * dt; if (q.y < 120) dead = true; }
          if (dead) { q.e.remove(); parts.splice(i, 1); } else q.e.setAttribute('transform', `translate(${q.x.toFixed(1)} ${q.y.toFixed(1)})`);
        }
        if (gasCol) gasCol.setAttribute('height', gas.toFixed(1));
        // meter
        const shown = bubbles ? Math.round(R.r * 0.6) : Math.round(R.r);
        const frac = bubbles ? shown / 60 : R.r / 100;
        mBar.setAttribute('height', (frac * 132).toFixed(1)); mBar.setAttribute('y', (156 - frac * 132).toFixed(1));
        mBar.setAttribute('fill', frac > .66 ? '#2ed3a5' : frac > .33 ? '#ffc93c' : '#ff6b6b');
        mTxt.textContent = bubbles ? shown : shown + '%';
        limTxt.setAttribute('fill', R.r >= 1 && !lim ? '#0f7a5c' : '#c94545');
        limTxt.textContent = R.r < 1 ? (V.temp > 45 ? 'Too hot — enzymes damaged!' : 'No photosynthesis') : lim ? 'Limiting: ' + FN[lim] : 'Max rate!';
        // goal
        let ok;
        if (bubbles) ok = shown >= num(goal.bpm, 40);
        else if (goal.limit) ok = R.r >= num(goal.rate, 50) && lim === goal.limit;
        else ok = R.r >= num(goal.rate, 80);
        holdT = ok ? holdT + dt : 0;
        if (holdT > 0.8) winOnce(bubbles ? `${shown} bubbles per minute! More light = faster photosynthesis = more oxygen.` : goal.limit ? `${FN[goal.limit]} is limiting the rate — raising it would make the plant go faster.` : `Rate ${shown}%! Enough light, CO₂, water and a warm (not hot) temperature.`);
        raf = requestAnimationFrame(frame);
      }
      raf = requestAnimationFrame(frame);
      return () => { alive = false; cancelAnimationFrame(raf); timers.forEach(clearTimeout); };
    },
    example: { mode: 'rate', factors: ['light', 'co2', 'water', 'temp'], start: { light: 30, co2: 50, water: 80, temp: 25 }, equation: 'both' },
    examples: [
      { mode: 'bubbles', lightAs: 'distance', start: { distance: 45, co2: 60, temp: 25 }, goal: { bpm: 40 },
        challenge: 'Grade 10: Move the lamp to make Hydrilla give 40+ oxygen bubbles a minute.' },
      { mode: 'starch', variant: 'paper',
        challenge: 'Grade 7–10: Cover part of a leaf with black paper and do the starch test in the right order.' },
      { mode: 'rate', factors: ['light', 'co2', 'temp'], start: { light: 90, co2: 8, water: 100, temp: 25 }, goal: { limit: 'co2', rate: 40 }, equation: 'symbol',
        challenge: 'Grade 11: With bright light, make CO₂ the limiting factor while the rate is at least 40%.' }
    ]
  });
})();
