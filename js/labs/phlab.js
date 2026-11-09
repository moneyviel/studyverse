/* Knowtopia Concept Lab: phlab — "Test-tube lab" (acids, bases, indicators, pH, neutralisation)
 *
 * PARAMS (all optional)
 *  mode        string  'test' (dip/drop indicators into substances) | 'neutralise' (add drops of
 *                      base/acid until neutral)                                                 default 'test'
 *  substances  array   test mode: ids from the built-in library or custom objects
 *                      {name, pH, emoji?, tint?}. Library ids: lemon, vinegar, hcl, naoh, soap,
 *                      bakingsoda, milk, water, antacid, orange, tomato, coffee, toothpaste,
 *                      limewater, ammonia, salt, sugar, curd, washingsoda, tamarind, gastric,
 *                      rain, sodawater                       default ['lemon','soap','water','bakingsoda','vinegar','antacid']
 *  indicators  array   ids: blueLitmus, redLitmus, turmeric, phenolphthalein, universal,
 *                      methylOrange, chinaRose                default ['blueLitmus','redLitmus','turmeric','phenolphthalein','universal']
 *  goal        object  test mode: {type:'sort'} classify every substance as acid/neutral/base;
 *                      {type:'find', nature:'acid'|'base'|'neutral', indicator?:id} find one;
 *                      {type:'testAll', indicator?:id} test every substance.                   default {type:'sort'}
 *  mystery     bool    hide names (Solution A, B, C…) — for "identify the unknown" questions    default false
 *  showPH      string  'universal' (pH pointer only when universal indicator is used) |
 *                      'always' | 'never'                                                       default 'universal'
 *  natureLabels object {acid, neutral, base} button words (e.g. Hindi)                          default Acid/Neutral/Base
 *  -- neutralise mode --
 *  acid        object  {name, formula?} acid in the dropper/tube (modelled as a strong acid)    default {name:'Dilute HCl'}
 *  base        object  {name} base (modelled as a strong base)                                 default {name:'Dilute NaOH'}
 *  start       string  'acid' | 'base' — what is in the tube at the start (10 mL)               default 'acid'
 *  indicator   string  indicator in the tube: universal | phenolphthalein | methylOrange | chinaRose default 'universal'
 *  dropsToNeutral number drops needed to neutralise exactly (sets the dropper concentration)   default 10
 *  equation    string  shown when neutral                                     default 'HCl + NaOH → NaCl + H₂O'
 *  challenge   string  challenge sentence (any language); a default is generated
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));
  const num = (v, d) => (v === null || v === undefined || v === '' || !Number.isFinite(+v)) ? d : +v;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const hex = h => { h = h.replace('#', ''); return [0, 2, 4].map(i => parseInt(h.substr(i, 2), 16)); };
  const toHex = a => '#' + a.map(v => Math.round(clamp(v, 0, 255)).toString(16).padStart(2, '0')).join('');
  const mix = (a, b, t) => { const A = hex(a), B = hex(b); return toHex(A.map((v, i) => v + (B[i] - v) * clamp(t, 0, 1))); };
  function ramp(stops, x) { // stops: [[x,color],...] sorted
    if (x <= stops[0][0]) return stops[0][1];
    for (let i = 1; i < stops.length; i++) if (x <= stops[i][0]) { const [x0, c0] = stops[i - 1], [x1, c1] = stops[i]; return mix(c0, c1, (x - x0) / (x1 - x0)); }
    return stops[stops.length - 1][1];
  }
  const UNI = [[0, '#c62828'], [1, '#e53935'], [2, '#f4511e'], [3, '#fb8c00'], [4, '#ffa726'], [5, '#fdd835'], [6, '#c0ca33'], [7, '#43a047'], [8, '#00897b'], [9, '#1e88e5'], [10, '#3949ab'], [11, '#5e35b1'], [12, '#7b1fa2'], [13, '#6a1b9a'], [14, '#4a148c']];
  const LIT = [[5, '#e53950'], [7, '#9a5fb8'], [8.3, '#3b6fe0']];
  const LIB = {
    lemon: ['Lemon juice', 2.2, '🍋', '#fff7a8'], vinegar: ['Vinegar', 2.9, '🫙', '#fffbe6'], hcl: ['Dilute HCl', 1.0, '🧪', '#f4f8ff'],
    naoh: ['Dilute NaOH', 13.0, '🧪', '#f4f8ff'], soap: ['Soap solution', 10.0, '🧼', '#eaf6ff'], bakingsoda: ['Baking soda solution', 8.3, '🥄', '#fafafa'],
    milk: ['Milk', 6.5, '🥛', '#ffffff'], water: ['Pure water', 7.0, '💧', '#eaf4ff'], antacid: ['Antacid (milk of magnesia)', 10.5, '💊', '#f7f7f7'],
    orange: ['Orange juice', 3.5, '🍊', '#ffd08a'], tomato: ['Tomato juice', 4.2, '🍅', '#ff9a8a'], coffee: ['Black coffee', 5.0, '☕', '#b08a72'],
    toothpaste: ['Toothpaste in water', 9.0, '🪥', '#effbff'], limewater: ['Lime water', 12.4, '⚪', '#f4f8ff'], ammonia: ['Ammonia solution', 11.6, '🧴', '#f4f8ff'],
    salt: ['Salt solution', 7.0, '🧂', '#f4f8ff'], sugar: ['Sugar solution', 7.0, '🍬', '#f4f8ff'], curd: ['Curd (dahi) water', 4.5, '🥣', '#fffdf3'],
    washingsoda: ['Washing soda solution', 11.5, '🧺', '#f4f8ff'], tamarind: ['Tamarind (imli) water', 3.0, '🌰', '#d9b99a'], gastric: ['Gastric juice', 1.5, '🫄', '#fbfbe8'],
    rain: ['Rain water', 5.6, '🌧️', '#eaf4ff'], sodawater: ['Soda water', 4.0, '🥤', '#eef7ff']
  };
  const nature = ph => ph < 6.8 ? 'acid' : ph > 7.2 ? 'base' : 'neutral';
  // indicator definitions: paper?, name, colour(pH)
  const IND = {
    blueLitmus: { name: 'Blue litmus', paper: true, base: '#3b6fe0', col: ph => ph < 7 ? ramp(LIT, ph) : '#3b6fe0' },
    redLitmus: { name: 'Red litmus', paper: true, base: '#e53950', col: ph => ph > 7 ? ramp(LIT, ph) : '#e53950' },
    turmeric: { name: 'Turmeric paper', paper: true, base: '#f6c21c', col: ph => ramp([[7.6, '#f6c21c'], [8.4, '#c0392b'], [11, '#a0281a']], ph) },
    phenolphthalein: { name: 'Phenolphthalein', paper: false, base: null, col: ph => ph < 8.2 ? null : ramp([[8.2, '#fbd3e9'], [9, '#f48fc0'], [10, '#e0218a']], ph) },
    universal: { name: 'Universal indicator', paper: false, base: '#43a047', col: ph => ramp(UNI, ph) },
    methylOrange: { name: 'Methyl orange', paper: false, base: '#fb8c00', col: ph => ramp([[3.1, '#e53935'], [3.8, '#fb8c00'], [4.4, '#fdd835']], ph) },
    chinaRose: { name: 'China rose', paper: false, base: '#a3477a', col: ph => ramp([[5, '#d81b60'], [7, '#a3477a'], [8.5, '#43a047']], ph) }
  };
  const colWord = c => { // rough colour name for observations
    if (!c) return 'colourless';
    const [r, g, b] = hex(c); const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
    if (mx - mn < 25) return mx > 200 ? 'colourless' : 'grey';
    let h; if (mx === r) h = ((g - b) / (mx - mn)) * 60; else if (mx === g) h = (2 + (b - r) / (mx - mn)) * 60; else h = (4 + (r - g) / (mx - mn)) * 60; if (h < 0) h += 360;
    if (h < 12 || h >= 345) return (r > 200 && g > 150) ? 'pink' : 'red';
    if (h < 30) return (r < 190) ? 'red-brown' : 'orange-red';
    if (h < 45) return 'orange'; if (h < 65) return 'yellow'; if (h < 85) return 'yellow-green'; if (h < 160) return 'green';
    if (h < 200) return 'blue-green'; if (h < 245) return 'blue'; if (h < 275) return 'violet'; if (h < 315) return 'purple'; return 'pink';
  };

  const CSS = `
  .lb-phlab{font-weight:700;color:#1b1f3a;user-select:none;-webkit-user-select:none}
  .lb-phlab-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:8px 11px;font-size:13.5px;line-height:1.3;margin-bottom:7px}
  .lb-phlab-sc{display:flex;gap:6px;overflow-x:auto;padding:2px 1px 5px;scrollbar-width:none}
  .lb-phlab-sc::-webkit-scrollbar{display:none}
  .lb-phlab-chip{flex:none;min-height:40px;border:2px solid #e3e6f6;background:#fff;border-radius:13px;padding:0 10px;font-family:inherit;font-weight:800;font-size:12.5px;color:#1b1f3a;cursor:pointer;display:flex;align-items:center;gap:5px}
  .lb-phlab-chip i{font-style:normal;width:14px;height:14px;border-radius:4px;display:inline-block;border:1px solid rgba(0,0,0,.12)}
  .lb-phlab-chip.on{border-color:#8b5cf6;background:#f1edff}
  .lb-phlab-chip.ok{background:#e3fbf3;border-color:#2ed3a5}
  .lb-phlab-stage{display:flex;gap:8px;align-items:stretch;margin:2px 0 4px}
  .lb-phlab-stage svg{flex:none;width:100px;height:144px}
  .lb-phlab-card{flex:1;background:#f7f8fd;border-radius:16px;padding:10px;font-size:12.5px;color:#6b7090;line-height:1.35;display:flex;flex-direction:column;gap:5px}
  .lb-phlab-card b{color:#1b1f3a}
  .lb-phlab-big{font-size:15px;color:#1b1f3a;font-weight:900;line-height:1.15}
  .lb-phlab-sw{display:inline-block;width:13px;height:13px;border-radius:4px;vertical-align:-2px;border:1px solid rgba(0,0,0,.15)}
  .lb-phlab-row{display:flex;gap:6px;align-items:center;margin-top:5px}
  .lb-phlab-btn{flex:1;min-height:42px;border:none;border-radius:13px;font-family:inherit;font-weight:800;font-size:13.5px;cursor:pointer;color:#fff;background:#8b5cf6;box-shadow:0 3px 0 #5b33c9}
  .lb-phlab-btn:active{transform:translateY(2px);box-shadow:none}
  .lb-phlab-btn:disabled{opacity:.35}
  .lb-phlab-btn.a{background:#ff6b6b;box-shadow:0 3px 0 #c94545}.lb-phlab-btn.n{background:#2ed3a5;box-shadow:0 3px 0 #1a9c78}.lb-phlab-btn.b{background:#3b82f6;box-shadow:0 3px 0 #2257b8}
  .lb-phlab-btn.g{background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;flex:0 0 auto;padding:0 12px}
  .lb-phlab-lbl{font-size:11.5px;color:#6b7090;margin:3px 0 2px}
  .lb-phlab-msg{font-size:12.5px;color:#6b7090;min-height:18px;margin-top:5px;text-align:center}
  .lb-phlab-msg.bad{color:#c94545}.lb-phlab-msg.good{color:#0f7a5c}
  .lb-phlab-liq{transition:fill .7s ease}
  @keyframes lb-phlab-drop{0%{transform:translateY(0);opacity:1}85%{opacity:1}100%{transform:translateY(64px);opacity:0}}
  .lb-phlab-dropping{animation:lb-phlab-drop .45s ease-in}
  @keyframes lb-phlab-dip{0%{transform:translateY(-40px)}100%{transform:translateY(0)}}
  .lb-phlab-dip{animation:lb-phlab-dip .45s ease-out}`;

  Labs.register('phlab', {
    title: 'Test-tube lab',
    subjects: ['science', 'chemistry'],
    render(host, p, api) {
      const mode = p.mode === 'neutralise' || p.mode === 'neutralize' ? 'neutralise' : 'test';
      const NL = Object.assign({ acid: 'Acid', neutral: 'Neutral', base: 'Base' }, (p.natureLabels && typeof p.natureLabels === 'object') ? p.natureLabels : {});
      const showPH = ['always', 'never'].includes(p.showPH) ? p.showPH : 'universal';
      let raf = 0, timers = [];
      const later = (f, ms) => timers.push(setTimeout(f, ms));
      let won = false; const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };

      // ---- pH scale SVG (shared) ----
      const uniStops = UNI.map(([x, c]) => `<stop offset="${(x / 14 * 100).toFixed(1)}%" stop-color="${c}"/>`).join('');
      const gid = 'lbph' + Math.random().toString(36).slice(2, 8);
      const phScale = `<svg class="lb-phlab-scale" viewBox="0 0 352 46" width="100%" style="display:block">
        <defs><linearGradient id="${gid}">${uniStops}</linearGradient></defs>
        <rect x="8" y="14" width="336" height="14" rx="7" fill="url(#${gid})"/>
        ${Array.from({ length: 15 }, (_, i) => `<text x="${8 + i * 24}" y="41" font-size="9.5" font-weight="800" text-anchor="middle" fill="${i === 7 ? '#1b1f3a' : '#9aa0c0'}">${i}</text>`).join('')}
        <text x="8" y="9" font-size="9" font-weight="800" fill="#e53935">◀ more acidic</text><text x="176" y="9" font-size="9" font-weight="800" text-anchor="middle" fill="#43a047">neutral</text><text x="344" y="9" font-size="9" font-weight="800" text-anchor="end" fill="#5e35b1">more basic ▶</text>
        <g class="lb-phlab-ptr" style="transition:transform .6s ease;opacity:0"><circle cx="0" cy="21" r="10" fill="none" stroke="#1b1f3a" stroke-width="3.5"/><circle cx="0" cy="21" r="12.5" fill="none" stroke="#fff" stroke-width="1.5"/></g>
        <text class="lb-phlab-q" x="176" y="25" font-size="11" font-weight="900" text-anchor="middle" fill="#fff"></text></svg>`;
      // ---- tube SVG ----
      const tubeSVG = `<svg viewBox="0 0 118 170" preserveAspectRatio="xMidYMid meet">
        <defs><clipPath id="${gid}c"><path d="M34 26 V140 a25 25 0 0 0 50 0 V26 Z"/></clipPath></defs>
        <rect x="14" y="150" width="90" height="10" rx="5" fill="#e3e6f6"/>
        <g clip-path="url(#${gid}c)"><rect class="lb-phlab-liq" x="30" y="70" width="60" height="110" fill="#eaf4ff"/>
          <rect class="lb-phlab-shine" x="40" y="26" width="6" height="130" fill="#fff" opacity=".5"/></g>
        <path d="M34 26 V140 a25 25 0 0 0 50 0 V26" fill="none" stroke="#9aa6d6" stroke-width="3"/>
        <rect x="29" y="20" width="60" height="7" rx="3.5" fill="#c9cde3"/>
        <g class="lb-phlab-paper" style="display:none"><rect x="52" y="4" width="14" height="118" rx="2" class="lb-phlab-ptop"/><rect x="52" y="76" width="14" height="46" rx="2" class="lb-phlab-pbot lb-phlab-liq"/></g>
        <g class="lb-phlab-dropper" style="display:none"><rect x="53" y="0" width="12" height="16" rx="4" fill="#ff8fa3"/><path d="M55 16 h8 l-2 8 h-4 z" fill="#c9cde3"/>
          <circle class="lb-phlab-drop" cx="59" cy="28" r="4" fill="#43a047" opacity="0"/></g>
</svg>`;

      // =================================================================== TEST MODE
      if (mode === 'test') {
        const subsIn = Array.isArray(p.substances) && p.substances.length ? p.substances : ['lemon', 'soap', 'water', 'bakingsoda', 'vinegar', 'antacid'];
        const S = subsIn.map((s, i) => {
          let o;
          if (typeof s === 'string') { const L = LIB[s] || LIB[s.toLowerCase()]; if (!L) return null; o = { id: s, name: L[0], pH: L[1], emoji: L[2], tint: L[3] }; }
          else if (s && typeof s === 'object' && Number.isFinite(+s.pH)) o = { id: 'c' + i, name: String(s.name || 'Solution'), pH: clamp(+s.pH, 0, 14), emoji: s.emoji || '🧪', tint: /^#[0-9a-f]{6}$/i.test(s.tint || '') ? s.tint : '#f4f8ff' };
          else return null;
          if (p.mystery) { o.real = o.name; o.name = 'Solution ' + String.fromCharCode(65 + i); o.emoji = '🧪'; }
          return o;
        }).filter(Boolean);
        const indIn = (Array.isArray(p.indicators) && p.indicators.length ? p.indicators : ['blueLitmus', 'redLitmus', 'turmeric', 'phenolphthalein', 'universal']).filter(k => IND[k]);
        if (!indIn.length) indIn.push('universal');
        const goal = (p.goal && typeof p.goal === 'object') ? p.goal : { type: 'sort' };
        const gtype = ['sort', 'find', 'testAll'].includes(goal.type) ? goal.type : 'sort';
        let challenge = p.challenge;
        if (!challenge) {
          if (gtype === 'sort') challenge = 'Test each liquid with indicators, then sort it: ' + NL.acid + ', ' + NL.neutral + ' or ' + NL.base + '.';
          else if (gtype === 'find') challenge = 'Find a liquid that is a' + (goal.nature === 'acid' ? 'n ' + NL.acid.toLowerCase() : ' ' + (NL[goal.nature] || NL.base).toLowerCase()) + (goal.indicator && IND[goal.indicator] ? ' using ' + IND[goal.indicator].name.toLowerCase() : '') + '.';
          else challenge = 'Test every liquid' + (goal.indicator && IND[goal.indicator] ? ' with ' + IND[goal.indicator].name.toLowerCase() : '') + ' and watch the colours.';
        }
        host.innerHTML = `<style>${CSS}</style><div class="lb-phlab">
          <div class="lb-phlab-ch">🎯 Challenge: ${esc(challenge)}</div>
          <div class="lb-phlab-sc lb-phlab-inds">${indIn.map(k => `<button class="lb-phlab-chip" data-i="${k}"><i style="background:${IND[k].base || '#ffffff'}"></i>${esc(IND[k].name)}</button>`).join('')}</div>
          <div class="lb-phlab-sc lb-phlab-subs">${S.map((s, i) => `<button class="lb-phlab-chip" data-s="${i}">${s.emoji} ${esc(s.name)}</button>`).join('')}</div>
          <div class="lb-phlab-stage">${tubeSVG}<div class="lb-phlab-card"></div></div>
          ${phScale}
          ${gtype === 'sort' ? `<div class="lb-phlab-row"><button class="lb-phlab-btn a" data-n="acid">${esc(NL.acid)}</button><button class="lb-phlab-btn n" data-n="neutral">${esc(NL.neutral)}</button><button class="lb-phlab-btn b" data-n="base">${esc(NL.base)}</button></div>` : ''}
          <div class="lb-phlab-msg"></div></div>`;
        const root = host.querySelector('.lb-phlab'), $ = s => root.querySelector(s), $$ = s => [...root.querySelectorAll(s)];
        const liq = $('rect.lb-phlab-liq'), paper = $('.lb-phlab-paper'), ptop = $('.lb-phlab-ptop'), pbot = $('.lb-phlab-pbot');
        const dropper = $('.lb-phlab-dropper'), dropEl = $('.lb-phlab-drop'), card = $('.lb-phlab-card'), msg = $('.lb-phlab-msg');
        const ptr = $('.lb-phlab-ptr'), q = $('.lb-phlab-q');
        let ind = indIn.includes(goal.indicator) ? goal.indicator : indIn[0], cur = -1;
        const sorted = {}, tested = S.map(() => new Set());
        const sortBtns = $$('.lb-phlab-btn[data-n]');
        function setMsg(t, cls) { msg.textContent = t; msg.className = 'lb-phlab-msg' + (cls ? ' ' + cls : ''); }
        function refreshChips() {
          $$('[data-i]').forEach(b => b.classList.toggle('on', b.dataset.i === ind));
          $$('[data-s]').forEach(b => { const i = +b.dataset.s; b.classList.toggle('on', i === cur); b.classList.toggle('ok', sorted[i] === true); });
          sortBtns.forEach(b => b.disabled = cur < 0 || sorted[cur] === true);
        }
        function showPtr(ph) {
          const vis = showPH === 'always' || (showPH === 'universal' && ind === 'universal');
          if (ph == null || showPH === 'never') { ptr.style.opacity = 0; q.textContent = ''; return; }
          if (vis) { ptr.style.opacity = 1; ptr.style.transform = `translate(${8 + ph / 14 * 336}px,0)`; q.textContent = ''; }
          else { ptr.style.opacity = 0; q.textContent = 'pH ? — use universal indicator'; }
        }
        function emptyCard() {
          card.innerHTML = `<div class="lb-phlab-big">Indicator: ${esc(IND[ind].name)}</div><div>${IND[ind].paper ? 'A strip of paper is dipped into the liquid.' : 'A few drops are added to the liquid.'}</div><div>👆 Pick an indicator (top row), then tap a liquid (second row) to test it.</div>`;
          liq.setAttribute('fill', '#f4f8ff'); liq.setAttribute('y', 150); paper.style.display = 'none'; dropper.style.display = 'none'; showPtr(null);
        }
        function test(i) {
          cur = i; const s = S[i], D = IND[ind]; tested[i].add(ind); api.sfx('tap');
          const after = D.col(s.pH);
          liq.style.transition = 'none'; liq.setAttribute('fill', s.tint); liq.setAttribute('y', 70); void liq.getBoundingClientRect(); liq.style.transition = '';
          let obs;
          if (D.paper) {
            dropper.style.display = 'none'; paper.style.display = '';
            ptop.setAttribute('fill', D.base); pbot.style.transition = 'none'; pbot.setAttribute('fill', D.base); void pbot.getBoundingClientRect(); pbot.style.transition = '';
            paper.classList.remove('lb-phlab-dip'); void paper.getBoundingClientRect(); paper.classList.add('lb-phlab-dip');
            later(() => pbot.setAttribute('fill', after), 450);
            const changed = mix(after, D.base, 0) !== D.base && colWord(after) !== colWord(D.base);
            obs = changed ? `${esc(D.name)} turned <b>${colWord(after)}</b> <span class="lb-phlab-sw" style="background:${after}"></span>` : `${esc(D.name)}: <b>no change</b> (stays ${colWord(D.base)})`;
          } else {
            paper.style.display = 'none'; dropper.style.display = '';
            const shown = after ? mix(after, s.tint, 0.18) : s.tint;
            dropEl.setAttribute('fill', D.base || '#f0f0f0'); dropEl.classList.remove('lb-phlab-dropping'); void dropEl.getBoundingClientRect();
            dropEl.setAttribute('opacity', 1); dropEl.classList.add('lb-phlab-dropping');
            later(() => { dropEl.setAttribute('opacity', 0); liq.setAttribute('fill', shown); }, 430);
            obs = after ? `Liquid turned <b>${colWord(after)}</b> <span class="lb-phlab-sw" style="background:${after}"></span>` : `Stays <b>colourless</b> — no change`;
          }
          const phTxt = (showPH === 'always' || (showPH === 'universal' && ind === 'universal')) ? `<div>pH ≈ <b>${s.pH}</b></div>` : '';
          card.innerHTML = `<div class="lb-phlab-big">${s.emoji} ${esc(s.name)}</div><div>+ ${esc(D.name)}</div><div>${obs}</div>${phTxt}`;
          later(() => showPtr(s.pH), 300);
          refreshChips();
          if (gtype === 'sort') setMsg(sorted[i] === true ? 'Already sorted ✓ — pick another liquid.' : 'Is it an ' + NL.acid.toLowerCase() + ', ' + NL.neutral.toLowerCase() + ' or ' + NL.base.toLowerCase() + '? Try more indicators if unsure.');
          else setMsg('');
          if (gtype === 'find' && nature(s.pH) === (goal.nature || 'base') && (!goal.indicator || goal.indicator === ind)) {
            later(() => winOnce(`${s.real || s.name} is ${nature(s.pH) === 'acid' ? 'an' : 'a'} ${NL[nature(s.pH)].toLowerCase()} — ${D.name} showed it!`), 600);
          }
          if (gtype === 'testAll') {
            const done = tested.filter(t => goal.indicator ? t.has(goal.indicator) : t.size > 0).length;
            setMsg(`Tested ${done} / ${S.length}`);
            if (done === S.length) later(() => winOnce('You tested every liquid! Acids, bases and neutral liquids give different colours.'), 600);
          }
        }
        $$('[data-i]').forEach(b => b.onclick = () => { ind = b.dataset.i; api.sfx('tap'); if (cur >= 0) test(cur); else { emptyCard(); refreshChips(); } });
        $$('[data-s]').forEach(b => b.onclick = () => test(+b.dataset.s));
        sortBtns.forEach(b => b.onclick = () => {
          if (cur < 0) return; const s = S[cur], right = nature(s.pH);
          if (b.dataset.n === right) {
            sorted[cur] = true; api.sfx('coin');
            const n = Object.values(sorted).filter(v => v === true).length;
            setMsg(`✓ ${s.real ? s.name + ' is ' + s.real : s.name} — ${NL[right]} (pH ${s.pH}). Sorted ${n} / ${S.length}`, 'good');
            refreshChips();
            if (n === S.length) winOnce('All sorted! Acids have pH below 7, bases above 7, neutral = 7.');
          } else {
            api.sfx('wrong');
            const hint = right === 'acid' ? 'Hint: acids turn blue litmus red.' : right === 'base' ? 'Hint: bases turn red litmus blue and turmeric red.' : 'Hint: neutral liquids change neither litmus.';
            setMsg('Not quite. ' + hint, 'bad');
          }
        });
        emptyCard(); refreshChips();
        return () => { timers.forEach(clearTimeout); cancelAnimationFrame(raf); };
      }

      // =================================================================== NEUTRALISE MODE
      const acid = Object.assign({ name: 'Dilute HCl' }, p.acid || {}), base = Object.assign({ name: 'Dilute NaOH' }, p.base || {});
      const startWith = p.start === 'base' ? 'base' : 'acid';
      const indK = ['universal', 'phenolphthalein', 'methylOrange', 'chinaRose'].includes(p.indicator) ? p.indicator : 'universal';
      const D = IND[indK];
      const NEQ = Math.max(2, Math.round(num(p.dropsToNeutral, 10)));
      const V0 = 10, dV = 0.5, n0 = 1.0, cT = n0 / (NEQ * dV); // mL, mL, mmol, mmol/mL (= M)
      const eq = String(p.equation || 'HCl + NaOH → NaCl + H₂O');
      const titrant = startWith === 'acid' ? base : acid, other = startWith === 'acid' ? acid : base;
      let challenge = p.challenge;
      if (!challenge) {
        if (indK === 'universal') challenge = `Add ${titrant.name} drop by drop until the ${other.name} turns green — pH 7, neutral!`;
        else challenge = `Add ${titrant.name} drop by drop. Stop as soon as ${D.name.toLowerCase()} changes colour!`;
      }
      host.innerHTML = `<style>${CSS}</style><div class="lb-phlab">
        <div class="lb-phlab-ch">🎯 Challenge: ${esc(challenge)}</div>
        <div class="lb-phlab-stage">${tubeSVG}<div class="lb-phlab-card"></div></div>
        ${phScale}
        <div class="lb-phlab-row"><button class="lb-phlab-btn ${startWith === 'acid' ? 'b' : 'a'} lb-phlab-add">💧 + 1 drop ${esc(titrant.name)}</button></div>
        <div class="lb-phlab-row"><button class="lb-phlab-btn ${startWith === 'acid' ? 'a' : 'b'} lb-phlab-back" style="font-size:12px">💧 + 1 drop ${esc(other.name)}</button><button class="lb-phlab-btn g lb-phlab-reset">↺ Reset</button></div>
        <div class="lb-phlab-msg"></div></div>`;
      const root = host.querySelector('.lb-phlab'), $ = s => root.querySelector(s);
      const liq = $('rect.lb-phlab-liq'), dropper = $('.lb-phlab-dropper'), dropEl = $('.lb-phlab-drop'), card = $('.lb-phlab-card'), msg = $('.lb-phlab-msg'), ptr = $('.lb-phlab-ptr');
      dropper.style.display = '';
      let nT = 0, nO = 0; // drops of titrant / of the other
      const tint = '#f4f8ff';
      function pH() {
        const V = V0 + (nT + nO) * dV; // mL
        // mmol of excess H+ (negative = excess OH-); both droppers have the same concentration cT
        const q = cT * dV; // mmol per drop
        const acidExcess = startWith === 'acid' ? n0 + (nO - nT) * q : (nT - nO) * q - n0;
        const x = acidExcess / V; // mol/L
        const h = (x + Math.sqrt(x * x + 4e-14)) / 2;
        return clamp(-Math.log10(h), 0, 14);
      }
      const startCol = D.col(pH()), startWord = colWord(startCol);
      function update(anim) {
        const ph = pH(), c = D.col(ph), shown = c ? mix(c, tint, 0.15) : tint;
        const V = V0 + (nT + nO) * dV;
        liq.setAttribute('y', 150 - V * 6.2);
        if (anim) later(() => liq.setAttribute('fill', shown), 380); else liq.setAttribute('fill', shown);
        ptr.style.opacity = showPH === 'never' ? 0 : 1; ptr.style.transform = `translate(${8 + ph / 14 * 336}px,0)`;
        const net = nT - nO; // titrant drops not cancelled by drops of the other liquid
        const nat = ph < 6.5 ? 'acidic' : ph > 7.5 ? 'basic' : 'neutral';
        card.innerHTML = `<div class="lb-phlab-big">${esc(other.name)} + ${esc(D.name)}</div>
          <div>Volume: <b>${V.toFixed(1)} mL</b></div><div>Drops of ${esc(titrant.name)}: <b>${nT}</b>${nO ? ` · extra ${esc(other.name)}: <b>${nO}</b>` : ''}</div>
          <div>Colour: <b>${colWord(c)}</b> <span class="lb-phlab-sw" style="background:${c || '#fff'}"></span></div>
          <div>${showPH === 'never' ? '' : `pH = <b>${ph.toFixed(1)}</b> · `}<b>${nat}</b></div>`;
        const excess = net - NEQ; // drops beyond exact neutralisation
        let ok;
        if (indK === 'universal') ok = Math.abs(ph - 7) <= 1;
        else ok = colWord(c) !== startWord && Math.abs(excess) <= 1;
        if (ok) {
          msg.className = 'lb-phlab-msg good';
          if (indK === 'universal') { msg.textContent = 'Neutralised! ' + eq; later(() => winOnce(`Neutral after ${nT} drops! Acid + base → salt + water: ${eq}`), 500); }
          else { msg.textContent = 'End point! ' + eq; later(() => winOnce(`End point after ${nT} drops: ${D.name} changed colour, so the ${other.name} is just used up. ${eq}`), 500); }
        }
        else if (Math.abs(excess) > 1 && excess > 0) { msg.className = 'lb-phlab-msg bad'; msg.textContent = 'Too much! Now it is ' + nat + '. Add a drop of ' + other.name + ' or Reset.'; }
        else { msg.className = 'lb-phlab-msg'; msg.textContent = nat === 'neutral' ? 'Neutral!' : 'Still ' + nat + '. Keep adding drop by drop.'; }
      }
      function drop(isT) {
        if (V0 + (nT + nO + 1) * dV > 20) { msg.className = 'lb-phlab-msg bad'; msg.textContent = 'The tube is full — press Reset.'; api.sfx('hmm'); return; }
        if (isT) nT++; else nO++;
        api.sfx('tap');
        dropEl.setAttribute('fill', '#cfe3ff'); dropEl.classList.remove('lb-phlab-dropping'); void dropEl.getBoundingClientRect();
        dropEl.setAttribute('opacity', 1); dropEl.classList.add('lb-phlab-dropping'); later(() => dropEl.setAttribute('opacity', 0), 430);
        update(true);
      }
      $('.lb-phlab-add').onclick = () => drop(true);
      $('.lb-phlab-back').onclick = () => drop(false);
      $('.lb-phlab-reset').onclick = () => { nT = nO = 0; api.sfx('tap'); update(false); if (won) { won = false; api.resetWin && api.resetWin(); } };
      update(false);
      return () => { timers.forEach(clearTimeout); };
    },
    example: {
      mode: 'test',
      substances: ['lemon', 'soap', 'water', 'bakingsoda', 'vinegar', 'antacid'],
      indicators: ['blueLitmus', 'redLitmus', 'turmeric', 'phenolphthalein', 'universal'],
      goal: { type: 'sort' }, showPH: 'universal'
    },
    examples: [
      { mode: 'test', substances: ['lemon', 'soap', 'tamarind', 'washingsoda', 'sugar'], indicators: ['turmeric', 'chinaRose', 'redLitmus'],
        goal: { type: 'find', nature: 'base', indicator: 'turmeric' }, showPH: 'never',
        challenge: 'Grade 7: Find a liquid that turns turmeric paper red. That liquid is a base!' },
      { mode: 'neutralise', start: 'acid', indicator: 'phenolphthalein', acid: { name: 'Dilute HCl' }, base: { name: 'Dilute NaOH' },
        dropsToNeutral: 8, equation: 'HCl + NaOH → NaCl + H₂O',
        challenge: 'Grade 10: Add NaOH drop by drop. Stop the moment phenolphthalein turns pink!' },
      { mode: 'test', mystery: true, substances: ['hcl', 'water', 'naoh'], indicators: ['blueLitmus', 'redLitmus', 'universal'], goal: { type: 'sort' },
        challenge: 'Grade 10: Three unknown solutions A, B, C. Use indicators to find which is acid, neutral and base.' }
    ]
  });
})();
