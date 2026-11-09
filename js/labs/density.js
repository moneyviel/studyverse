/* Knowtopia Concept Lab: density — sink or float in a tank of liquid.
 *
 * The child drags (or taps) objects from the shelf into the tank. Each object moves by real buoyancy:
 * it floats if its density is less than the liquid's, sinks if more, and a floating object rests with
 * the fraction ρ(object)/ρ(liquid) of itself under the surface (Archimedes). Changing the liquid makes
 * objects already in the tank rise or sink. Density = mass ÷ volume is shown for every object.
 * Tap an object in the tank to take it out.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   goal       string  'float' (make `target` float) | 'sink' (make `target` sink) | 'testall' (test every
 *                      object) | 'none'                                                default 'float'
 *   target     string  object name for goal float/sink                                  default 'Egg'
 *   challenge  string  challenge text (any language); default made from goal
 *   winText    string  optional win message
 *   objects    array   [{name, mass (g), volume (cm³), shape, color}]; shape one of block, nail, cube,
 *                      stone, coin, apple, egg, drop, ball (density = mass/volume)
 *                                                  default 9 everyday objects (wood, nail, ice, egg …)
 *   liquids    array   [{name, density (g/cm³), color}]          default Water 1.00, Salt water 1.20, Oil 0.92
 *   liquid     string  starting liquid name                                             default first
 *   showDensity boolean show each object's density on the info line before it is tested  default true
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fN = (v, d = 2) => (Math.round(v * Math.pow(10, d)) / Math.pow(10, d)).toFixed(d);
  const OBJS = [
    { name: 'Wood block', mass: 30, volume: 50, shape: 'block', color: '#c98a4b' },
    { name: 'Iron nail', mass: 7.9, volume: 1, shape: 'nail', color: '#8a94a6' },
    { name: 'Ice cube', mass: 18.2, volume: 20, shape: 'cube', color: '#bfe9ff' },
    { name: 'Egg', mass: 60, volume: 57, shape: 'egg', color: '#f6e3c4' },
    { name: 'Stone', mass: 26, volume: 10, shape: 'stone', color: '#9a9db0' },
    { name: 'Steel coin', mass: 3.9, volume: 0.5, shape: 'coin', color: '#c9ced8' },
    { name: 'Apple', mass: 160, volume: 200, shape: 'apple', color: '#ff6b6b' },
    { name: 'Plastic toy', mass: 9, volume: 10, shape: 'ball', color: '#8b5cf6' },
    { name: 'Oil drop', mass: 0.46, volume: 0.5, shape: 'drop', color: '#ffc93c' }
  ];
  const LIQS = [{ name: 'Water', density: 1.0, color: '#59b4ff' }, { name: 'Salt water', density: 1.2, color: '#3fd0c0' }, { name: 'Oil', density: 0.92, color: '#f2c94c' }];
  const SH = { block: [40, 26], nail: [40, 12], cube: [30, 30], stone: [36, 26], coin: [28, 10], apple: [32, 32], egg: [24, 32], drop: [20, 26], ball: [30, 30] };

  const CSS = `
.lb-density-w{font-size:14px;color:#1b1f3a;-webkit-user-select:none;user-select:none}
.lb-density-ch{font-weight:800;font-size:14px;margin-bottom:6px;line-height:1.25}
.lb-density-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:16px;touch-action:none}
.lb-density-row{display:flex;gap:6px;margin-top:6px}
.lb-density-b{flex:1 1 0;min-width:0;min-height:44px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:12.5px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 4px;line-height:1.1}
.lb-density-b small{display:block;font-size:10.5px;opacity:.8}
.lb-density-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-density-b.sm{flex:0 0 46px;font-size:16px}
.lb-density-b:active{transform:translateY(2px)}
.lb-density-out{background:#f6f4ff;border-radius:12px;padding:6px 10px;margin-top:6px;font-weight:800;font-size:13px;line-height:1.35;min-height:52px}
.lb-density-out i{font-style:normal;color:#6b7090;font-size:12px}
.lb-density-it{cursor:grab}
`;

  Labs.register('density', {
    title: 'Sink or float',
    subjects: ['science', 'physics'],
    render(host, p, api) {
      const ex = this.example || {};
      p = Object.assign({}, p);
      if (p.goal !== ex.goal || p.target !== ex.target) ['challenge', 'winText'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      const objs = (Array.isArray(p.objects) && p.objects.length ? p.objects : OBJS).filter(o => o && o.name && +o.mass > 0 && +o.volume > 0).slice(0, 9)
        .map((o, i) => ({ name: String(o.name), mass: +o.mass, volume: +o.volume, rho: +o.mass / +o.volume, shape: SH[o.shape] ? o.shape : 'ball', color: o.color || (OBJS.find(d => d.name === o.name) || OBJS.find(d => d.shape === o.shape) || OBJS[i % OBJS.length]).color, i }));
      const liqs = (Array.isArray(p.liquids) && p.liquids.length ? p.liquids : LIQS).filter(l => l && l.name && +l.density > 0).slice(0, 4)
        .map((l, i) => ({ name: String(l.name), rho: +l.density, color: l.color || LIQS[i % 3].color }));
      let li = Math.max(0, liqs.findIndex(l => l.name === p.liquid));
      const goal = ['float', 'sink', 'testall', 'none'].includes(p.goal) ? p.goal : 'float';
      const tIdx = Math.max(0, objs.findIndex(o => o.name === p.target));
      const showRho = p.showDensity !== false;
      const W = 360, H = 252, SHELF = 58, TX0 = 22, TX1 = 338, SURF = 104, BOT = 244, COLS = 6;
      const colX = c => TX0 + (TX1 - TX0) * (c + 0.5) / COLS;
      const G = 620;
      let won = false, raf = 0, last = performance.now(), msgObj = null;
      const tested = {}; // name -> verdict in liquid
      const items = []; // in tank: {o, col, y (centre), vy}
      const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(p.winText ? String(p.winText) : m); };
      const verdict = (o, l) => Math.abs(o.rho - l.rho) < 0.005 ? 'same' : o.rho < l.rho ? 'floats' : 'sinks';

      const tgtO = objs[tIdx];
      const DEFCH = {
        float: `Make the ${tgtO.name.toLowerCase()} FLOAT. (Hint: try a different liquid.)`,
        sink: `Make the ${tgtO.name.toLowerCase()} SINK. (Hint: try a different liquid.)`,
        testall: `Drop every object in the tank. Which ones float in ${liqs[li].name.toLowerCase()}?`,
        none: 'Drop things in the tank. Which float and which sink — and why?'
      };
      host.innerHTML = `<style>${CSS}</style><div class="lb-density-w">
  <div class="lb-density-ch">🎯 Challenge: ${esc(p.challenge ? String(p.challenge) : DEFCH[goal])}</div>
  <svg class="lb-density-svg" viewBox="0 0 ${W} ${H}"></svg>
  <div class="lb-density-row">${liqs.map((l, i) => `<button class="lb-density-b" data-l="${i}">${esc(l.name)}<small>${fN(l.rho)} g/cm³</small></button>`).join('')}<button class="lb-density-b sm" data-empty="1" aria-label="empty tank">↺</button></div>
  <div class="lb-density-out"></div></div>`;
      const sv = host.querySelector('svg'), out = host.querySelector('.lb-density-out');

      function shape(o, x, y, s = 1) {
        const [w, h] = SH[o.shape], c = esc(o.color);
        let g = '';
        switch (o.shape) {
          case 'block': g = `<rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="4" fill="${c}" stroke="#7a4d22" stroke-width="2"/><path d="M${-w / 2 + 5} -4 q10 -5 20 0 t14 0 M${-w / 2 + 6} 5 q12 4 24 0" fill="none" stroke="#7a4d22" stroke-width="1.3" opacity=".6"/>`; break;
          case 'nail': g = `<rect x="-16" y="-3" width="30" height="6" fill="${c}" stroke="#555c6c" stroke-width="1.5"/><path d="M14 -3 L21 0 L14 3Z" fill="${c}" stroke="#555c6c" stroke-width="1.5"/><rect x="-20" y="-6" width="5" height="12" rx="1.5" fill="${c}" stroke="#555c6c" stroke-width="1.5"/>`; break;
          case 'cube': g = `<rect x="-15" y="-15" width="30" height="30" rx="6" fill="${c}" stroke="#7cc0e8" stroke-width="2" opacity=".95"/><path d="M-9 -9 h8" stroke="#fff" stroke-width="3" stroke-linecap="round"/>`; break;
          case 'stone': g = `<path d="M-17 4 Q-18 -9 -4 -12 Q10 -14 16 -4 Q20 8 6 12 Q-12 14 -17 4Z" fill="${c}" stroke="#6b7090" stroke-width="2"/><circle cx="-4" cy="-2" r="2" fill="#7c8096"/>`; break;
          case 'coin': g = `<ellipse rx="14" ry="5" fill="${c}" stroke="#8a8f9e" stroke-width="2"/><ellipse rx="8" ry="2.2" fill="none" stroke="#8a8f9e" stroke-width="1"/>`; break;
          case 'apple': g = `<path d="M0 -10 C-14 -18 -20 2 -10 13 C-6 17 -2 15 0 13 C2 15 6 17 10 13 C20 2 14 -18 0 -10Z" fill="${c}" stroke="#c23b3b" stroke-width="2"/><path d="M0 -10 q1 -5 3 -7" stroke="#7a4d22" stroke-width="2" fill="none"/><path d="M2 -14 q7 -5 10 0 q-6 3 -10 0Z" fill="#2ed3a5"/>`; break;
          case 'egg': g = `<ellipse rx="12" ry="16" fill="${c}" stroke="#c9a77a" stroke-width="2"/><ellipse cx="-4" cy="-6" rx="3" ry="5" fill="#fff" opacity=".6"/>`; break;
          case 'drop': g = `<path d="M0 -13 C6 -4 10 1 10 5 A10 10 0 0 1 -10 5 C-10 1 -6 -4 0 -13Z" fill="${c}" stroke="#d9a400" stroke-width="2"/>`; break;
          default: g = `<circle r="15" fill="${c}" stroke="rgba(0,0,0,.25)" stroke-width="2"/><circle cx="-5" cy="-5" r="4" fill="#fff" opacity=".5"/>`;
        }
        return `<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${s})">${g}</g>`;
      }
      const inTank = o => items.find(it => it.o === o);
      const shelfX = i => 14 + (W - 28) * (i + 0.5) / objs.length;

      let drag = null; // {o, x, y, from:'shelf'|'tank', moved, sx, sy}
      function draw() {
        const l = liqs[li];
        let s = `<rect x="6" y="6" width="${W - 12}" height="${SHELF - 8}" rx="12" fill="#fff"/><rect x="6" y="${SHELF - 8}" width="${W - 12}" height="6" rx="3" fill="#d9a066"/>`;
        objs.forEach((o, i) => {
          if (inTank(o) || (drag && drag.o === o)) { s += `<circle cx="${shelfX(i)}" cy="${SHELF / 2}" r="4" fill="#e3e5f3"/>`; return; }
          s += `<g class="lb-density-it" data-o="${i}"><rect x="${shelfX(i) - 19}" y="8" width="38" height="${SHELF - 16}" fill="transparent"/>${shape(o, shelfX(i), SHELF / 2 + 1, objs.length > 7 ? 0.85 : 1)}` +
            (tested[o.name] ? `<text x="${shelfX(i)}" y="16" text-anchor="middle" font-size="9" font-weight="800" fill="${tested[o.name] === 'sinks' ? '#e04848' : '#14a37f'}">${tested[o.name] === 'sinks' ? '↓' : tested[o.name] === 'floats' ? '↑' : '='}</text>` : '') + '</g>';
        });
        // tank
        s += `<rect x="${TX0 - 4}" y="${SURF - 18}" width="${TX1 - TX0 + 8}" height="${BOT - SURF + 22}" rx="10" fill="#ffffff" opacity=".6" stroke="#9aa0c0" stroke-width="3"/>`;
        items.forEach((it, k) => { s += `<g class="lb-density-it" data-t="${k}"><rect x="${colX(it.col) - 22}" y="${it.y - 22}" width="44" height="44" fill="transparent"/>${shape(it.o, colX(it.col), it.y)}</g>`; });
        s += `<rect x="${TX0}" y="${SURF}" width="${TX1 - TX0}" height="${BOT - SURF}" fill="${esc(l.color)}" opacity=".3" pointer-events="none"/>`;
        s += `<path d="M${TX0} ${SURF} H${TX1}" stroke="${esc(l.color)}" stroke-width="3" pointer-events="none"/>`;
        s += `<text x="${TX1}" y="${SURF - 24}" text-anchor="end" font-size="12" font-weight="800" fill="#1b1f3a" opacity=".75" pointer-events="none">${esc(l.name)} · ${fN(l.rho)} g/cm³</text>`;
        if (drag && drag.moved) s += `<g pointer-events="none">${shape(drag.o, drag.x, drag.y, 1.15)}<text x="${drag.x}" y="${drag.y - 24}" text-anchor="middle" font-size="11" font-weight="800" fill="#1b1f3a" stroke="#fff" stroke-width="3" paint-order="stroke">${esc(drag.o.name)}</text></g>`;
        if (!items.length && !drag) s += `<text x="${W / 2}" y="${(SURF + BOT) / 2 + 4}" text-anchor="middle" font-size="13" font-weight="800" fill="#1b1f3a" opacity=".55" pointer-events="none">Drag or tap an object to drop it in</text>`;
        sv.innerHTML = s;
      }
      function info(o) {
        if (!o) { out.innerHTML = `Density = mass ÷ volume. Less dense than the liquid → floats.<br><i>Tap the liquids to change them.</i>`; return; }
        const l = liqs[li], v = verdict(o, l);
        const inT = inTank(o);
        out.innerHTML = `${esc(o.name)}: ρ = ${+o.mass.toFixed(2)} g ÷ ${+o.volume.toFixed(2)} cm³ = <span style="color:#8b5cf6">${showRho || inT ? fN(o.rho) : '?'} g/cm³</span><br>` +
          (inT ? (v === 'floats' ? `<span style="color:#14a37f">Floats</span> in ${esc(l.name.toLowerCase())} (${fN(l.rho)}) — ${Math.round(100 * o.rho / l.rho)}% of it is under the surface.`
            : v === 'sinks' ? `<span style="color:#e04848">Sinks</span> in ${esc(l.name.toLowerCase())} — it is denser (${fN(o.rho)} > ${fN(l.rho)}).`
              : `Same density as ${esc(l.name.toLowerCase())} — it stays wherever it is.`) : '<i>Drop it in the tank to test it.</i>');
      }
      function drop(o, x, y) {
        const used = items.map(it => it.col);
        let free = [...Array(COLS).keys()].filter(c => !used.includes(c));
        if (!free.length) { const old = items.shift(); free = [old.col]; }
        const col = x == null ? free[0] : free.reduce((b, c) => Math.abs(colX(c) - x) < Math.abs(colX(b) - x) ? c : b, free[0]);
        items.push({ o, col, y: Math.min(y == null ? SURF - 30 : y, SURF - 6), vy: 0 });
        tested[o.name] = verdict(o, liqs[li]);
        api.sfx('tap'); msgObj = o; info(o);
        checkTestAll();
      }
      function checkTestAll() {
        if (goal !== 'testall') return;
        if (objs.every(o => tested[o.name])) {
          const l = liqs[li];
          const fl = objs.filter(o => verdict(o, l) === 'floats').map(o => o.name), sk = objs.filter(o => verdict(o, l) === 'sinks').map(o => o.name);
          winOnce(`In ${l.name.toLowerCase()} (${fN(l.rho)} g/cm³) — float: ${fl.join(', ') || 'none'}; sink: ${sk.join(', ') || 'none'}. Less dense than the liquid → floats.`);
        }
      }
      function step(dt) {
        const l = liqs[li];
        items.forEach(it => {
          const h = SH[it.o.shape][1], bottom = it.y + h / 2;
          const sub = Math.max(0, Math.min(1, (bottom - SURF) / h));
          let ratio = l.rho / it.o.rho;
          if (Math.abs(it.o.rho - l.rho) < 0.005) ratio = 1;
          let a = G * (1 - ratio * sub);
          if (sub >= 1 && ratio !== 1) a = Math.sign(a) * Math.max(Math.abs(a), G * 0.3);
          const damp = sub > 0 ? 5.5 : 0.3;
          it.vy += (a - damp * it.vy) * dt;
          it.y += it.vy * dt;
          if (it.y + h / 2 > BOT - 1) { it.y = BOT - 1 - h / 2; if (it.vy > 0) it.vy = 0; }
          if (sub >= 1 && ratio === 1 && Math.abs(it.vy) < 2) it.vy = 0;
        });
        if (goal === 'float' || goal === 'sink') {
          const it = inTank(tgtO);
          if (it) {
            const v = verdict(tgtO, l), h = SH[tgtO.shape][1];
            if (goal === 'float' && v === 'floats' && Math.abs(it.vy) < 6 && it.y + h / 2 < BOT - 4 && it.y - h / 2 < SURF)
              winOnce(`The ${tgtO.name.toLowerCase()} (${fN(tgtO.rho)} g/cm³) floats in ${l.name.toLowerCase()} (${fN(l.rho)} g/cm³) because the liquid is denser.`);
            if (goal === 'sink' && v === 'sinks' && it.y + h / 2 >= BOT - 2)
              winOnce(`The ${tgtO.name.toLowerCase()} (${fN(tgtO.rho)} g/cm³) sinks in ${l.name.toLowerCase()} (${fN(l.rho)} g/cm³) because it is denser than the liquid.`);
          }
        }
      }
      function loop(now) {
        const dt = Math.min(0.033, (now - last) / 1000); last = now;
        step(dt); draw();
        raf = requestAnimationFrame(loop);
      }
      const pt = e => { const m = sv.getScreenCTM(); return m ? new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse()) : null; };
      const down = e => {
        const g = e.target.closest('[data-o],[data-t]'); if (!g) return;
        const q = pt(e); if (!q) return;
        if (g.dataset.o !== undefined) { const o = objs[+g.dataset.o]; drag = { o, from: 'shelf', x: q.x, y: q.y, sx: q.x, sy: q.y, moved: false }; msgObj = o; info(o); }
        else { const it = items[+g.dataset.t]; drag = { o: it.o, from: 'tank', it, x: q.x, y: q.y, sx: q.x, sy: q.y, moved: false }; msgObj = it.o; info(it.o); }
        sv.setPointerCapture && sv.setPointerCapture(e.pointerId);
      };
      const move = e => {
        if (!drag) return; const q = pt(e); if (!q) return;
        drag.x = q.x; drag.y = q.y;
        if (!drag.moved && Math.hypot(q.x - drag.sx, q.y - drag.sy) > 6) {
          drag.moved = true;
          if (drag.from === 'tank') items.splice(items.indexOf(drag.it), 1);
        }
      };
      const up = () => {
        if (!drag) return;
        const d = drag; drag = null;
        if (!d.moved) {
          if (d.from === 'shelf') drop(d.o, null, null);
          else { items.splice(items.indexOf(d.it), 1); api.sfx('tap'); info(d.o); }
          return;
        }
        if (d.x > TX0 - 10 && d.x < TX1 + 10 && d.y > SURF - 40) drop(d.o, d.x, d.y);
        else info(d.o);
      };
      sv.addEventListener('pointerdown', down); sv.addEventListener('pointermove', move); sv.addEventListener('pointerup', up); sv.addEventListener('pointercancel', up);
      const onClick = e => {
        const b = e.target.closest('button'); if (!b) return;
        if (b.dataset.l !== undefined) {
          li = +b.dataset.l; api.sfx('tap');
          items.forEach(it => { tested[it.o.name] = verdict(it.o, liqs[li]); });
          if (goal === 'testall') objs.forEach(o => { if (!inTank(o)) delete tested[o.name]; });
          ui(); info(msgObj); checkTestAll();
        } else if (b.dataset.empty) { items.length = 0; api.sfx('tap'); info(null); }
      };
      host.addEventListener('click', onClick);
      function ui() { host.querySelectorAll('[data-l]').forEach(b => b.classList.toggle('on', +b.dataset.l === li)); }
      ui(); info(null); draw(); raf = requestAnimationFrame(loop);
      return () => { cancelAnimationFrame(raf); sv.removeEventListener('pointerdown', down); sv.removeEventListener('pointermove', move); sv.removeEventListener('pointerup', up); sv.removeEventListener('pointercancel', up); host.removeEventListener('click', onClick); };
    },
    example: {
      goal: 'float', target: 'Egg',
      liquid: 'Water',
      challenge: 'An egg sinks in plain water. Can you make the egg FLOAT? Test the other objects too!'
    },
    examples: [
      { goal: 'testall', liquid: 'Water', challenge: 'Grade 6: Drop every object into water. Which ones float and which ones sink?' },
      {
        goal: 'sink', target: 'Ice cube', liquid: 'Water',
        liquids: [{ name: 'Water', density: 1.0, color: '#59b4ff' }, { name: 'Spirit (alcohol)', density: 0.79, color: '#c9b6ff' }, { name: 'Honey', density: 1.42, color: '#f0a020' }],
        objects: [
          { name: 'Ice cube', mass: 18.2, volume: 20, shape: 'cube' }, { name: 'Wood block', mass: 30, volume: 50, shape: 'block' },
          { name: 'Plastic toy', mass: 9, volume: 10, shape: 'ball', color: '#8b5cf6' }, { name: 'Grape', mass: 5.4, volume: 5, shape: 'ball', color: '#6bbf59' },
          { name: 'Stone', mass: 26, volume: 10, shape: 'stone' }
        ],
        challenge: 'Grade 8/9: Ice floats on water. Find a liquid that makes the ice cube SINK.'
      }
    ]
  });
})();
