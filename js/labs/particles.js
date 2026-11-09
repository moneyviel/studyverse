/* Knowtopia Concept Lab: particles — "Particle box" (states of matter, diffusion, evaporation)
 *
 * PARAMS (all optional; missing ones fall back to sensible defaults)
 *  mode       string   'states' | 'diffusion' | 'evaporation'                          default 'states'
 *             states      : solid/liquid/gas particle box with heater + thermometer (melting & boiling points).
 *             diffusion   : a drop of dye spreads through water (or a smell through air); hotter = faster.
 *             evaporation : liquid in an open dish; surface particles escape; a lid makes vapour condense back.
 *  substance  string   name of the substance shown                                     default 'Water'
 *  melt       number   melting / freezing point in °C                                  default 0
 *  boil       number   boiling point in °C                                             default 100
 *  range      [n,n]    thermometer range in °C [min,max] (states mode)                 default [-30,130]
 *  start      number   starting temperature in °C (clamped to a sensible value per mode) default -20
 *  control    string   'heater' (slider = burner power, temperature rises over time and
 *                      PAUSES at melting/boiling points = latent heat) | 'temp' (slider sets
 *                      the target temperature directly; still pauses while changing state) default 'heater'
 *  labels     object   names of the three states {solid,liquid,gas} e.g. {solid:'बर्फ़'} default Ice/Water/Steam for water, else Solid/Liquid/Gas
 *  color      string   particle colour (CSS)                                           default '#3b82f6'
 *  goals      array    states mode: states to reach IN ORDER, from 'solid','liquid','gas',
 *                      'melting','boiling','freezing','condensing'                     default ['liquid','gas']
 *  medium     string   diffusion mode: 'water' (dye in water) | 'air' (smell in air)   default 'water'
 *  dyeName    string   diffusion mode: name of what spreads                            default 'Dye' / 'Perfume'
 *  dyeTime    number   diffusion goal: spread fully in under this many seconds          default 10
 *  evaporate  number   evaporation goal: % of the liquid to evaporate                  default 50
 *  drops      number   evaporation goal (overrides evaporate): drops condensed on the lid default — (unset)
 *  challenge  string   the challenge sentence (any language); a default is generated from the params
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));
  const num = (v, d) => (v === null || v === undefined || v === '' || !Number.isFinite(+v)) ? d : +v;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const fmtT = t => (Math.round(t) < 0 ? '−' + Math.abs(Math.round(t)) : Math.round(t)) + ' °C';
  function gauss() { let u = 0; while (!u) u = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * Math.random()); }

  const CSS = `
  .lb-particles{font-weight:700;color:#1b1f3a;user-select:none;-webkit-user-select:none}
  .lb-particles-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:8px 11px;font-size:13.5px;line-height:1.3;margin-bottom:8px}
  .lb-particles canvas{display:block;width:100%;height:auto;border-radius:16px;background:#fbfcff}
  .lb-particles-row{display:flex;align-items:center;gap:8px;margin-top:8px}
  .lb-particles-row .lb-particles-lab{font-size:12px;color:#6b7090;min-width:44px;text-align:center;line-height:1.1}
  .lb-particles input[type=range]{flex:1;height:40px;-webkit-appearance:none;appearance:none;background:transparent;margin:0}
  .lb-particles input[type=range]::-webkit-slider-runnable-track{height:12px;border-radius:99px;background:var(--lb-particles-track)}
  .lb-particles input[type=range]::-moz-range-track{height:12px;border-radius:99px;background:var(--lb-particles-track)}
  .lb-particles input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:30px;height:30px;border-radius:50%;background:#fff;border:4px solid #8b5cf6;margin-top:-9px;box-shadow:0 2px 6px rgba(0,0,0,.2)}
  .lb-particles input[type=range]::-moz-range-thumb{width:22px;height:22px;border-radius:50%;background:#fff;border:4px solid #8b5cf6}
  .lb-particles-btn{min-height:40px;border:none;border-radius:12px;padding:0 12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;white-space:nowrap}
  .lb-particles-btn:active{transform:translateY(2px);box-shadow:0 1px 0 #d3d7ef}
  .lb-particles-btn.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
  .lb-particles-btn.mint{background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1a9c78}
  .lb-particles-info{flex:1;font-size:12.5px;color:#6b7090;line-height:1.25}
  .lb-particles-info b{color:#1b1f3a}
  .lb-particles-leg{font-size:11.5px;color:#6b7090;margin-top:5px;text-align:center}.lb-particles-leg i{font-style:normal}
  .lb-particles-goals{display:flex;gap:5px;flex-wrap:wrap;margin-top:7px}
  .lb-particles-goals span{font-size:12px;border-radius:99px;padding:4px 9px;background:#f1f2f8;color:#6b7090}
  .lb-particles-goals span.done{background:#e3fbf3;color:#0f7a5c}
  .lb-particles-goals span.next{background:#fff6dc;color:#9a6a00;outline:2px solid #ffc93c}`;

  Labs.register('particles', {
    title: 'Particle box',
    subjects: ['science', 'evs', 'chemistry', 'physics'],
    render(host, p, api) {
      const mode = ['states', 'diffusion', 'evaporation'].includes(p.mode) ? p.mode : 'states';
      const sub = String(p.substance || 'Water');
      let melt = num(p.melt, 0), boil = num(p.boil, 100);
      if (boil <= melt + 5) boil = melt + 100;
      const isWater = /^water$/i.test(sub.trim()) && melt === 0 && boil === 100;
      const L0 = isWater ? { solid: 'Ice', liquid: 'Water', gas: 'Steam' } : { solid: 'Solid', liquid: 'Liquid', gas: 'Gas' };
      const LB = Object.assign({}, L0, (p.labels && typeof p.labels === 'object') ? p.labels : {});
      const color = String(p.color || '#3b82f6');
      const medium = p.medium === 'air' ? 'air' : 'water';
      const dyeName = String(p.dyeName || (medium === 'air' ? 'Perfume' : 'Dye'));

      // temperature range per mode
      let Tmin, Tmax;
      if (mode === 'states') {
        const r = Array.isArray(p.range) ? p.range : [];
        Tmin = num(r[0], Math.min(melt - 30, -30)); Tmax = num(r[1], boil + 30);
        if (Tmin > melt - 10) Tmin = melt - 10; if (Tmax < boil + 10) Tmax = boil + 10;
      } else if (mode === 'diffusion') {
        if (medium === 'air') { Tmin = 0; Tmax = 50; } else { Tmin = melt + 5; Tmax = boil - 5; }
      } else { Tmin = melt + 10; Tmax = boil; }
      const span = Tmax - Tmin;

      // ---------- default challenge ----------
      const goals = (Array.isArray(p.goals) && p.goals.length ? p.goals : ['liquid', 'gas']).map(String)
        .filter(g => ['solid', 'liquid', 'gas', 'melting', 'boiling', 'freezing', 'condensing'].includes(g));
      const gName = g => ({ solid: LB.solid, liquid: LB.liquid, gas: LB.gas, melting: 'Melting', boiling: 'Boiling', freezing: 'Freezing', condensing: 'Condensing' }[g]);
      const dyeTime = num(p.dyeTime, 10);
      const evapGoal = clamp(num(p.evaporate, 50), 5, 100);
      const dropGoal = p.drops != null && num(p.drops, 0) > 0 ? Math.round(num(p.drops, 10)) : 0;
      let challenge = p.challenge;
      if (!challenge) {
        if (mode === 'states') challenge = 'Change the ' + sub.toLowerCase() + ': ' + goals.map(gName).join(' → ') + '. Watch the thermometer!';
        else if (mode === 'diffusion') challenge = 'Make the ' + dyeName.toLowerCase() + ' spread through the whole box in under ' + dyeTime + ' s.';
        else challenge = dropGoal ? 'Put the lid on and collect ' + dropGoal + ' drops of condensed ' + sub.toLowerCase() + '.' : 'Evaporate ' + evapGoal + '% of the ' + sub.toLowerCase() + '.';
      }

      // ---------- DOM ----------
      const W = 352, H = mode === 'states' ? 222 : 216;
      const ctlStates = `
        <div class="lb-particles-row"><span class="lb-particles-lab">${p.control === 'temp' ? 'Set<br>temp' : '❄️<br>Cool'}</span>
        <input type="range" class="lb-particles-s" aria-label="heater">
        <span class="lb-particles-lab">${p.control === 'temp' ? '<b class="lb-particles-sv"></b>' : '🔥<br>Heat'}</span></div>
        <div class="lb-particles-row"><div class="lb-particles-info"></div><button class="lb-particles-btn lb-particles-reset">↺ Reset</button></div>
        <div class="lb-particles-goals"></div>`;
      const ctlDiff = `
        <div class="lb-particles-row"><span class="lb-particles-lab">❄️<br>Cold</span><input type="range" class="lb-particles-s" aria-label="temperature"><span class="lb-particles-lab">🔥<br>Hot</span></div>
        <div class="lb-particles-row"><div class="lb-particles-info"></div><button class="lb-particles-btn mint lb-particles-drop">💧 Drop ${esc(dyeName.toLowerCase())}</button></div>
        <div class="lb-particles-goals"></div>`;
      const ctlEvap = `
        <div class="lb-particles-row"><span class="lb-particles-lab">❄️<br>Cool</span><input type="range" class="lb-particles-s" aria-label="temperature"><span class="lb-particles-lab">🔥<br>Hot</span></div>
        <div class="lb-particles-row"><button class="lb-particles-btn lb-particles-lid">Lid: off</button><button class="lb-particles-btn lb-particles-dish">Dish: narrow</button><div class="lb-particles-info"></div></div>
        <div class="lb-particles-row"><button class="lb-particles-btn lb-particles-reset">↺ Refill</button><div class="lb-particles-info lb-particles-info2"></div></div>`;
      host.innerHTML = `<style>${CSS}</style><div class="lb-particles" style="--lb-particles-track:${mode === 'states' && p.control !== 'temp' ? 'linear-gradient(90deg,#7cc4ff,#e6e9f5 45%,#e6e9f5 55%,#ff9a6b)' : 'linear-gradient(90deg,#7cc4ff,#ffd27a,#ff6b6b)'}">
        <div class="lb-particles-ch">🎯 Challenge: ${esc(challenge)}</div>
        <canvas width="${W * 2}" height="${H * 2}"></canvas>
        ${mode !== 'diffusion' ? `<div class="lb-particles-leg">${mode === 'states' ? `<i style="color:#3b82f6">▶</i> MP = melting point <b>${fmtT(melt)}</b> &nbsp; ` : ''}<i style="color:#ff6b6b">▶</i> BP = boiling point <b>${fmtT(boil)}</b></div>` : ''}
        ${mode === 'states' ? ctlStates : mode === 'diffusion' ? ctlDiff : ctlEvap}</div>`;
      const root = host.querySelector('.lb-particles');
      const cv = root.querySelector('canvas'), ctx = cv.getContext('2d');
      ctx.setTransform(2, 0, 0, 2, 0, 0);
      const slider = root.querySelector('.lb-particles-s');
      const info = root.querySelector('.lb-particles-info');
      const goalsEl = root.querySelector('.lb-particles-goals');
      const $ = s => root.querySelector(s);

      // geometry
      const bx0 = 66, bx1 = W - 8, by0 = 10, by1 = H - 10;
      let raf = 0, last = 0, tAll = 0, won = false, alive = true;
      const winOnce = msg => { if (won) return; won = true; api.sfx('correct'); api.win(msg); };

      // ---------- thermometer ----------
      const ty0 = 22, ty1 = H - 40;
      const tY = T => ty1 - (clamp(T, Tmin, Tmax) - Tmin) / span * (ty1 - ty0);
      function niceStep(s) { for (const st of [5, 10, 20, 25, 50, 100, 200, 250, 500]) if (s / st <= 7) return st; return 1000; }
      function drawThermo(T, marks) {
        const x = 40;
        ctx.save();
        ctx.fillStyle = '#ffffff'; ctx.strokeStyle = '#c9cde3'; ctx.lineWidth = 2;
        rr(x - 7, ty0 - 10, 14, ty1 - ty0 + 22, 7); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.arc(x, ty1 + 16, 12, 0, Math.PI * 2); ctx.fillStyle = '#ff6b6b'; ctx.fill();
        ctx.fillStyle = '#ff6b6b'; rr(x - 3.5, tY(T), 7, ty1 + 10 - tY(T), 3.5); ctx.fill();
        ctx.font = '800 9px Nunito, sans-serif'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
        const st = niceStep(span);
        for (let v = Math.ceil(Tmin / st) * st; v <= Tmax; v += st) {
          const y = tY(v); ctx.fillStyle = '#9aa0c0'; ctx.fillRect(x - 7, y - 0.5, 4, 1);
          ctx.fillText(v < 0 ? '−' + (-v) : v, x - 10, y);
        }
        for (const m of marks) {
          const y = tY(m.t); ctx.fillStyle = m.c; ctx.fillRect(x + 3, y - 1.5, 13, 3);
          ctx.beginPath(); ctx.moveTo(x + 16, y - 5); ctx.lineTo(x + 22, y); ctx.lineTo(x + 16, y + 5); ctx.fill();
          if (m.l) { ctx.font = '900 8.5px Nunito, sans-serif'; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.fillText(m.l, x + 6, y - 5); }
        }
        ctx.restore();
      }
      function rr(x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
      function ball(x, y, r, c, alpha) {
        ctx.globalAlpha = alpha == null ? 1 : alpha;
        const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .15, x, y, r);
        g.addColorStop(0, '#ffffff'); g.addColorStop(.35, c); g.addColorStop(1, c);
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
        ctx.globalAlpha = 1;
      }
      function pill(text, x, y, bg, fg, align) {
        ctx.font = '800 12px Nunito, sans-serif';
        const w = ctx.measureText(text).width + 16; const xx = align === 'right' ? x - w : x;
        ctx.fillStyle = bg; rr(xx, y, w, 22, 11); ctx.fill();
        ctx.fillStyle = fg; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(text, xx + 8, y + 11.5);
      }
      function boxBg(heat) {
        ctx.fillStyle = '#f4f7ff'; ctx.strokeStyle = '#c9cde3'; ctx.lineWidth = 2;
        rr(bx0, by0, bx1 - bx0, by1 - by0, 14); ctx.fill(); ctx.stroke();
        if (heat) {
          const g = ctx.createLinearGradient(0, by1 - 40, 0, by1);
          g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, heat > 0 ? `rgba(255,130,60,${.35 * Math.min(1, heat)})` : `rgba(90,180,255,${.4 * Math.min(1, -heat)})`);
          ctx.fillStyle = g; rr(bx0 + 1, by1 - 40, bx1 - bx0 - 2, 39, 13); ctx.fill();
        }
      }

      // ======================================================================
      // STATES MODE
      // ======================================================================
      if (mode === 'states') {
        const heater = p.control !== 'temp';
        const Lm = Math.max(25, span * 0.22), Lb = Math.max(35, span * 0.32); // latent heat in "°C worth" of energy (scaled to keep it quick)
        const eAt = T => T < melt ? T - Tmin : T < boil ? (melt - Tmin) + Lm + (T - melt) : (melt - Tmin) + Lm + (boil - melt) + Lb + (T - boil);
        const Emax = eAt(Tmax);
        function stateOf(E) {
          const e1 = melt - Tmin, e2 = e1 + Lm, e3 = e2 + (boil - melt), e4 = e3 + Lb;
          if (E < e1) return { T: Tmin + E, fs: 1, fg: 0 };
          if (E < e2) return { T: melt, fs: 1 - (E - e1) / Lm, fg: 0 };
          if (E < e3) return { T: melt + (E - e2), fs: 0, fg: 0 };
          if (E < e4) return { T: boil, fs: 0, fg: (E - e3) / Lb };
          return { T: boil + (E - e4), fs: 0, fg: 1 };
        }
        let start = clamp(num(p.start, -20), Tmin, Tmax);
        let E = eAt(start), power = 0, target = start, prevE = E;
        if (heater) { slider.min = -3; slider.max = 3; slider.step = 0.5; slider.value = 0; }
        else { slider.min = Math.ceil(Tmin); slider.max = Math.floor(Tmax); slider.step = 1; slider.value = Math.round(start); }
        const sv = $('.lb-particles-sv');
        const N = 40, R = 7, COLS = 8, SP = 15.5;
        const cx = (bx0 + bx1) / 2;
        const P = [];
        for (let i = 0; i < N; i++) {
          const c = i % COLS, row = Math.floor(i / COLS);
          const hx = cx - (COLS - 1) * SP / 2 + c * SP, hy = by1 - R - 2 - row * SP;
          P.push({ hx, hy, x: hx, y: hy, vx: 0, vy: 0, st: 's', ph1: Math.random() * 6.28, ph2: Math.random() * 6.28, w: 22 + Math.random() * 14 });
        }
        let gi = 0; // goal index
        function phaseName(s, dE) {
          if (s.fs === 1) return 'solid';
          if (s.fg === 1) return 'gas';
          if (s.fs > 0) return dE < 0 ? 'freezing' : 'melting';
          if (s.fg > 0) return dE < 0 ? 'condensing' : 'boiling';
          return 'liquid';
        }
        function renderGoals() {
          goalsEl.innerHTML = goals.map((g, i) => `<span class="${i < gi ? 'done' : i === gi ? 'next' : ''}">${i < gi ? '✓ ' : (i + 1) + '. '}${esc(gName(g))}</span>`).join('');
        }
        renderGoals();
        $('.lb-particles-reset').onclick = () => {
          E = eAt(start); power = 0; target = start; gi = 0; renderGoals(); api.sfx('tap');
          if (heater) slider.value = 0; else slider.value = Math.round(start);
          if (won) { won = false; api.resetWin && api.resetWin(); }
          for (const q of P) { q.x = q.hx; q.y = q.hy; q.vx = q.vy = 0; q.st = 's'; }
        };
        slider.oninput = () => { if (heater) power = +slider.value; else target = +slider.value; };
        let dEsm = 0;
        function step(dt) {
          prevE = E;
          if (heater) E += power * 9 * dt;
          else { const tE = eAt(target); const d = tE - E; E += Math.sign(d) * Math.min(Math.abs(d), 36 * dt); }
          E = clamp(E, 0, Emax);
          const dE = (E - prevE) / dt; dEsm += (dE - dEsm) * Math.min(1, dt * 6);
          const s = stateOf(E);
          const TK = s.T + 273.15;
          const nS = Math.round(N * s.fs), nG = Math.round(N * s.fg);
          for (let i = 0; i < N; i++) {
            const q = P[i]; const want = i < nS ? 's' : i >= N - nG ? 'g' : 'l';
            if (want !== q.st) {
              if (want === 'g') { const a = -Math.PI / 2 + (Math.random() - .5) * 1.6; q.vx = Math.cos(a) * 150; q.vy = Math.sin(a) * 150; }
              if (want === 'l' && q.st === 's') { q.vx = (Math.random() - .5) * 40; q.vy = -20; }
              q.st = want;
            }
          }
          const vib = 0.6 + 2.4 * clamp((s.T - Tmin) / Math.max(1, melt - Tmin), 0, 1);
          const kick = 2400 * Math.sqrt(TK / 300), gas = 120 * Math.sqrt(TK / 373);
          for (const q of P) {
            if (q.st === 's') {
              const tx = q.hx + vib * Math.sin(tAll * q.w + q.ph1), ty = q.hy + vib * Math.cos(tAll * q.w * 1.13 + q.ph2);
              const k = Math.min(1, dt * 8); q.x += (tx - q.x) * k; q.y += (ty - q.y) * k; q.vx = q.vy = 0;
            } else if (q.st === 'l') {
              q.vx += (Math.random() - .5) * kick * dt; q.vy += (Math.random() - .5) * kick * dt + 500 * dt;
              const damp = Math.max(0, 1 - 3.2 * dt); q.vx *= damp; q.vy *= damp;
              const sp = Math.hypot(q.vx, q.vy), cap = 150; if (sp > cap) { q.vx *= cap / sp; q.vy *= cap / sp; }
              q.x += q.vx * dt; q.y += q.vy * dt;
            } else {
              const sp = Math.hypot(q.vx, q.vy) || 1; q.vx *= gas / sp; q.vy *= gas / sp;
              q.x += q.vx * dt; q.y += q.vy * dt;
            }
          }
          // collisions
          for (let it = 0; it < 2; it++) for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
            const a = P[i], b = P[j]; const dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy, md = 2 * R;
            if (d2 < md * md && d2 > 0.0001) {
              const d = Math.sqrt(d2), o = (md - d), nx = dx / d, ny = dy / d;
              const ma = a.st === 's' ? 0 : 1, mb = b.st === 's' ? 0 : 1; if (!ma && !mb) continue;
              const sa = ma / (ma + mb), sb = mb / (ma + mb);
              a.x -= nx * o * sa; a.y -= ny * o * sa; b.x += nx * o * sb; b.y += ny * o * sb;
              if (a.st === 'g') { const vn = a.vx * nx + a.vy * ny; if (vn > 0) { a.vx -= 2 * vn * nx; a.vy -= 2 * vn * ny; } }
              if (b.st === 'g') { const vn = b.vx * nx + b.vy * ny; if (vn < 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; } }
            }
          }
          for (const q of P) {
            if (q.st === 's') continue;
            if (q.x < bx0 + R + 2) { q.x = bx0 + R + 2; q.vx = Math.abs(q.vx); }
            if (q.x > bx1 - R - 2) { q.x = bx1 - R - 2; q.vx = -Math.abs(q.vx); }
            if (q.y < by0 + R + 2) { q.y = by0 + R + 2; q.vy = Math.abs(q.vy); }
            if (q.y > by1 - R - 2) { q.y = by1 - R - 2; q.vy = -Math.abs(q.vy) * (q.st === 'l' ? 0.3 : 1); }
          }
          // ---- UI ----
          const ph = phaseName(s, dEsm < -0.5 ? -1 : dEsm > 0.5 ? 1 : 0);
          if (gi < goals.length) {
            const g = goals[gi];
            const ok = g === ph;
            if (ok) {
              gi++; renderGoals(); api.sfx(gi >= goals.length ? 'coin' : 'tap');
              if (gi >= goals.length) winOnce('You did it: ' + goals.map(gName).join(' → ') + '! While changing state the temperature stayed fixed (at ' + fmtT(melt) + ' or ' + fmtT(boil) + ').');
            }
          }
          const nm = { solid: LB.solid + ' (solid)', liquid: LB.liquid + ' (liquid)', gas: LB.gas + ' (gas)', melting: 'Melting…', freezing: 'Freezing…', boiling: 'Boiling…', condensing: 'Condensing…' }[ph];
          let msg;
          if (ph === 'melting' || ph === 'freezing') msg = `<b>${ph === 'melting' ? 'Melting' : 'Freezing'}!</b> Temperature stays at <b>${fmtT(melt)}</b> until all particles change.`;
          else if (ph === 'boiling' || ph === 'condensing') msg = `<b>${ph === 'boiling' ? 'Boiling' : 'Condensing'}!</b> Temperature stays at <b>${fmtT(boil)}</b> until all particles change.`;
          else if (ph === 'solid') msg = `<b>Solid:</b> particles packed in fixed places, only vibrating.`;
          else if (ph === 'liquid') msg = `<b>Liquid:</b> particles close together but sliding past each other.`;
          else msg = `<b>Gas:</b> particles far apart, moving fast in all directions.`;
          if (info._m !== msg) { info.innerHTML = msg; info._m = msg; }
          if (sv) sv.textContent = fmtT(target);
          // ---- draw ----
          ctx.clearRect(0, 0, W, H);
          drawThermo(s.T, [{ t: melt, c: '#3b82f6', l: 'MP' }, { t: boil, c: '#ff6b6b', l: 'BP' }]);
          const heat = heater ? power / 3 : clamp(dEsm / 30, -1, 1);
          boxBg(heat);
          // bonds between solid neighbours
          ctx.strokeStyle = 'rgba(80,90,160,.35)'; ctx.lineWidth = 2;
          for (let i = 0; i < N; i++) {
            const a = P[i]; if (a.st !== 's') continue;
            const nb = [i + 1, i + COLS]; for (const j of nb) {
              if (j >= N || (j === i + 1 && (i % COLS) === COLS - 1)) continue; const b = P[j]; if (b.st !== 's') continue;
              ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
            }
          }
          for (const q of P) {
            if (q.st === 'g') { ctx.strokeStyle = 'rgba(59,130,246,.18)'; ctx.lineWidth = 6; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(q.x, q.y); ctx.lineTo(q.x - q.vx * 0.09, q.y - q.vy * 0.09); ctx.stroke(); }
            ball(q.x, q.y, R, color);
          }
          pill(fmtT(s.T), bx0 + 8, by0 + 7, '#1b1f3a', '#fff');
          const pc = ph === 'solid' ? '#e8f1ff' : ph === 'gas' ? '#fff0ec' : ph === 'liquid' ? '#e6f9f3' : '#fff6dc';
          pill(nm, bx1 - 8, by0 + 7, pc, '#1b1f3a', 'right');
        }
        startLoop(step);
      }

      // ======================================================================
      // DIFFUSION MODE
      // ======================================================================
      if (mode === 'diffusion') {
        let T = clamp(num(p.start, 20), Tmin, Tmax);
        slider.min = Math.ceil(Tmin); slider.max = Math.floor(Tmax); slider.step = 1; slider.value = Math.round(T);
        slider.oninput = () => { T = +slider.value; };
        const Drel = () => medium === 'air' ? Math.pow((T + 273.15) / 293, 1.75) : ((T + 273.15) / 293) / Math.exp(-0.0163 * (T - 20));
        const KD = medium === 'air' ? 30 : 28;
        const M = 46, ND = 150;
        const bg = []; for (let i = 0; i < M; i++) bg.push({ x: bx0 + 8 + Math.random() * (bx1 - bx0 - 16), y: by0 + 8 + Math.random() * (by1 - by0 - 16), a: Math.random() * 6.28 });
        let dye = [], tRun = 0, done = false, results = [];
        const dyeCol = medium === 'air' ? '#ff6b9a' : '#8b5cf6';
        function drop() {
          dye = []; for (let i = 0; i < ND; i++) { const a = Math.random() * 6.28, r = Math.sqrt(Math.random()) * 13; dye.push({ x: bx0 + 30 + Math.cos(a) * r, y: by0 + 32 + Math.sin(a) * r }); }
          tRun = 0; done = false; api.sfx('tap');
        }
        $('.lb-particles-drop').onclick = drop;
        drop();
        function spread() {
          const c = [0, 0, 0, 0, 0, 0], cw = (bx1 - bx0) / 3, ch = (by1 - by0) / 2;
          for (const q of dye) { const i = Math.min(2, Math.max(0, Math.floor((q.x - bx0) / cw))), j = Math.min(1, Math.max(0, Math.floor((q.y - by0) / ch))); c[j * 3 + i]++; }
          let s = 0; for (const x of c) s += Math.min(1, x / (0.6 * ND / 6)); return s / 6;
        }
        function renderRes() {
          goalsEl.innerHTML = results.length ? results.slice(-3).map(r => `<span class="${r.t <= dyeTime ? 'done' : ''}">${fmtT(r.T)}: ${r.t.toFixed(1)} s</span>`).join('') : '<span>Results will appear here</span>';
        }
        renderRes();
        function step(dt) {
          const D = Drel(), s = KD * Math.sqrt(D * dt);
          for (const q of dye) {
            q.x += gauss() * s; q.y += gauss() * s;
            const lo = bx0 + 4, hi = bx1 - 4, lo2 = by0 + 4, hi2 = by1 - 4;
            if (q.x < lo) q.x = 2 * lo - q.x; if (q.x > hi) q.x = 2 * hi - q.x; if (q.y < lo2) q.y = 2 * lo2 - q.y; if (q.y > hi2) q.y = 2 * hi2 - q.y;
            q.x = clamp(q.x, lo, hi); q.y = clamp(q.y, lo2, hi2);
          }
          const vs = 40 * Math.sqrt(D);
          for (const q of bg) {
            q.a += gauss() * 3 * dt * 4; q.x += Math.cos(q.a) * vs * dt; q.y += Math.sin(q.a) * vs * dt;
            if (q.x < bx0 + 5 || q.x > bx1 - 5) { q.a = Math.PI - q.a; q.x = clamp(q.x, bx0 + 5, bx1 - 5); }
            if (q.y < by0 + 5 || q.y > by1 - 5) { q.a = -q.a; q.y = clamp(q.y, by0 + 5, by1 - 5); }
          }
          const sp = spread();
          if (!done) {
            tRun += dt;
            if (sp >= 0.999) {
              done = true; const avgT = T; results.push({ T: avgT, t: tRun }); renderRes();
              if (tRun <= dyeTime) winOnce(`Spread fully in ${tRun.toFixed(1)} s at ${fmtT(avgT)}! Hot particles move faster, so diffusion is faster.`);
              else { api.sfx('hmm'); }
            }
          }
          const msg = done ? `<b>Fully spread</b> in ${results[results.length - 1].t.toFixed(1)} s. ${won ? '' : 'Try another temperature!'}` : `<b>Spread: ${Math.round(sp * 100)}%</b> · time ${tRun.toFixed(1)} s`;
          if (info._m !== msg) { info.innerHTML = msg; info._m = msg; }
          ctx.clearRect(0, 0, W, H);
          drawThermo(T, []);
          boxBg(0);
          ctx.fillStyle = medium === 'air' ? 'rgba(200,220,255,.0)' : 'rgba(120,180,255,.10)'; rr(bx0 + 1, by0 + 1, bx1 - bx0 - 2, by1 - by0 - 2, 13); ctx.fill();
          for (const q of bg) ball(q.x, q.y, 3.6, medium === 'air' ? '#c9cde3' : '#9cc9ff', .8);
          for (const q of dye) ball(q.x, q.y, 3.3, dyeCol, .9);
          ctx.setLineDash([4, 5]); ctx.strokeStyle = 'rgba(107,112,144,.25)'; ctx.lineWidth = 1;
          ctx.beginPath(); for (let i = 1; i < 3; i++) { const x = bx0 + (bx1 - bx0) * i / 3; ctx.moveTo(x, by0 + 4); ctx.lineTo(x, by1 - 4); }
          ctx.moveTo(bx0 + 4, (by0 + by1) / 2); ctx.lineTo(bx1 - 4, (by0 + by1) / 2); ctx.stroke(); ctx.setLineDash([]);
          pill(fmtT(T), bx0 + 8, by1 - 29, '#1b1f3a', '#fff');
          pill((medium === 'air' ? '🌬️ ' + dyeName + ' in air' : '💧 ' + dyeName + ' in ' + sub.toLowerCase()), bx1 - 8, by1 - 29, 'rgba(255,255,255,.9)', '#1b1f3a', 'right');
        }
        startLoop(step);
      }

      // ======================================================================
      // EVAPORATION MODE
      // ======================================================================
      if (mode === 'evaporation') {
        let T = clamp(num(p.start, 30), Tmin, Tmax);
        if (!Number.isFinite(+p.start) || +p.start < Tmin) T = clamp(30, Tmin, Tmax);
        slider.min = Math.ceil(Tmin); slider.max = Math.floor(Tmax); slider.step = 1; slider.value = Math.round(T);
        slider.oninput = () => { T = +slider.value; };
        const N = 64, R = 6;
        let lid = false, wide = false, P = [], lost = 0, caught = 0;
        const lidY = by0 + 6;
        const walls = () => wide ? [bx0 + 6, bx1 - 6] : [(bx0 + bx1) / 2 - 62, (bx0 + bx1) / 2 + 62];
        function fill() {
          P = []; lost = 0; caught = 0; const [a, b] = walls(); const per = Math.floor((b - a) / (2 * R + 1));
          for (let i = 0; i < N; i++) { const c = i % per, r = Math.floor(i / per); P.push({ x: a + R + 1 + c * (2 * R + 1), y: by1 - R - 2 - r * (2 * R + 1), vx: 0, vy: 0, st: 'l', t: 0 }); }
        }
        fill();
        const lidB = $('.lb-particles-lid'), dishB = $('.lb-particles-dish'), info2 = $('.lb-particles-info2');
        lidB.onclick = () => { lid = !lid; lidB.textContent = 'Lid: ' + (lid ? 'on' : 'off'); lidB.classList.toggle('on', lid); api.sfx('tap'); };
        dishB.onclick = () => { wide = !wide; dishB.textContent = 'Dish: ' + (wide ? 'wide' : 'narrow'); dishB.classList.toggle('on', wide); api.sfx('tap'); };
        $('.lb-particles-reset').onclick = () => { fill(); api.sfx('tap'); if (won) { won = false; api.resetWin && api.resetWin(); } };
        function step(dt) {
          const TK = T + 273.15, boiling = T >= boil - 0.5;
          const [wa, wb] = walls();
          const liq = P.filter(q => q.st === 'l');
          const perRow = Math.max(1, Math.floor((wb - wa) / (2 * R + 1)));
          const surfSet = new Set(liq.slice().sort((a, b) => a.y - b.y).slice(0, perRow));
          const rate = 0.012 * Math.exp(0.045 * (T - 20));
          for (const q of liq) {
            const surf = surfSet.has(q);
            if ((surf && Math.random() < rate * dt) || (boiling && Math.random() < 0.6 * dt)) {
              q.st = 'g'; const a = -Math.PI / 2 + (Math.random() - .5) * 1.4; q.vx = Math.cos(a) * 110; q.vy = Math.sin(a) * 110;
            }
          }
          const kick = 1500 * Math.sqrt(TK / 300), gs = 105 * Math.sqrt(TK / 373);
          for (const q of P) {
            if (q.st === 'l') {
              q.vx += (Math.random() - .5) * kick * dt; q.vy += (Math.random() - .5) * kick * dt + 500 * dt;
              const damp = Math.max(0, 1 - 3.2 * dt); q.vx *= damp; q.vy *= damp; q.x += q.vx * dt; q.y += q.vy * dt;
            } else if (q.st === 'g') {
              q.vy -= 25 * dt; // warm vapour drifts up
              const sp = Math.hypot(q.vx, q.vy) || 1; q.vx *= gs / sp; q.vy *= gs / sp; q.x += q.vx * dt; q.y += q.vy * dt;
              if (q.y < lidY + R + 1) {
                if (lid) { q.st = 'd'; q.t = 1.2 + Math.random() * .8; q.y = lidY + R + 1; caught++; api.sfx('tap'); }
                else { q.st = 'x'; lost++; }
              }
            } else if (q.st === 'd') { q.t -= dt; if (!lid) { q.st = 'g'; q.vy = -50; } else if (q.t <= 0) { q.st = 'l'; q.vx = 0; q.vy = 30; } }
          }
          // collisions (liquid + vapour)
          const act = P.filter(q => q.st === 'l' || q.st === 'g');
          for (let it = 0; it < 2; it++) for (let i = 0; i < act.length; i++) for (let j = i + 1; j < act.length; j++) {
            const a = act[i], b = act[j]; const dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy, md = 2 * R;
            if (d2 < md * md && d2 > 0.0001) { const d = Math.sqrt(d2), o = (md - d) / 2, nx = dx / d, ny = dy / d; a.x -= nx * o; a.y -= ny * o; b.x += nx * o; b.y += ny * o; }
          }
          for (const q of act) {
            const inDish = q.y > by0 + 40 || q.st === 'l';
            const L = inDish ? wa : bx0 + 2, Rr = inDish ? wb : bx1 - 2;
            if (q.x < L + R) { q.x = L + R; q.vx = Math.abs(q.vx); }
            if (q.x > Rr - R) { q.x = Rr - R; q.vx = -Math.abs(q.vx); }
            if (q.y > by1 - R - 2) { q.y = by1 - R - 2; q.vy = -Math.abs(q.vy) * (q.st === 'l' ? .3 : 1); }
            if (q.y < by0 + R) { q.y = by0 + R; q.vy = Math.abs(q.vy); }
          }
          const left = Math.round((N - lost) / N * 100), evap = 100 - left;
          if (!won) {
            if (dropGoal && caught >= dropGoal) winOnce(`${caught} drops collected! The cool lid turned vapour back into liquid — condensation.`);
            if (!dropGoal && evap >= evapGoal) winOnce(`${evap}% evaporated! Heat and a wide surface make evaporation faster.`);
          }
          const nSurf = surfSet.size;
          const msg = `<b>${esc(sub)} left: ${left}%</b><br>${boiling ? 'Boiling!' : 'Surface particles: ' + nSurf}`;
          if (info._m !== msg) { info.innerHTML = msg; info._m = msg; }
          const m2 = lid ? `Drops on lid: <b>${caught}</b> — vapour condensing` : `Escaped to air: <b>${lost}</b> particles`;
          if (info2._m !== m2) { info2.innerHTML = m2; info2._m = m2; }
          // draw
          ctx.clearRect(0, 0, W, H);
          drawThermo(T, [{ t: boil, c: '#ff6b6b', l: 'BP' }]);
          ctx.fillStyle = '#eef6ff'; rr(bx0, by0, bx1 - bx0, by1 - by0, 14); ctx.fill();
          // dish
          ctx.fillStyle = 'rgba(255,255,255,.9)'; ctx.strokeStyle = '#9aa6d6'; ctx.lineWidth = 3;
          ctx.beginPath(); ctx.moveTo(wa - 2, by0 + 40); ctx.lineTo(wa - 2, by1 - 1); ctx.lineTo(wb + 2, by1 - 1); ctx.lineTo(wb + 2, by0 + 40); ctx.stroke();
          const hg = ctx.createLinearGradient(0, by1 - 30, 0, by1); const hk = (T - Tmin) / (Tmax - Tmin);
          hg.addColorStop(0, 'rgba(0,0,0,0)'); hg.addColorStop(1, `rgba(255,120,60,${.1 + .4 * hk})`); ctx.fillStyle = hg; ctx.fillRect(wa, by1 - 30, wb - wa, 29);
          if (lid) { ctx.fillStyle = '#c9cde3'; rr(bx0 + 4, by0 + 1, bx1 - bx0 - 8, 6, 3); ctx.fill(); ctx.fillStyle = '#6b7090'; ctx.font = '800 9px Nunito,sans-serif'; ctx.textAlign = 'center'; ctx.fillText('cool lid', (bx0 + bx1) / 2, by0 + 18); }
          for (const q of P) {
            if (q.st === 'x') continue;
            if (q.st === 'd') { ctx.fillStyle = color; ctx.globalAlpha = .85; ctx.beginPath(); ctx.ellipse(q.x, q.y, R * .8, R * 1.05, 0, 0, Math.PI * 2); ctx.fill(); ctx.globalAlpha = 1; continue; }
            if (q.st === 'g') { ctx.strokeStyle = 'rgba(59,130,246,.18)'; ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(q.x, q.y); ctx.lineTo(q.x - q.vx * .08, q.y - q.vy * .08); ctx.stroke(); }
            ball(q.x, q.y, R, color, q.st === 'g' ? .75 : 1);
          }
          pill(fmtT(T), bx0 + 8, by0 + (lid ? 24 : 10), '#1b1f3a', '#fff');
        }
        startLoop(step);
      }

      function startLoop(step) {
        last = performance.now();
        const loop = now => {
          if (!alive) return;
          const dt = clamp((now - last) / 1000, 0, 0.05); last = now; tAll += dt;
          if (host.isConnected === false) { alive = false; return; }
          step(dt || 0.016);
          raf = requestAnimationFrame(loop);
        };
        raf = requestAnimationFrame(loop);
      }
      return () => { alive = false; cancelAnimationFrame(raf); };
    },
    example: {
      mode: 'states', substance: 'Water', melt: 0, boil: 100, range: [-30, 130], start: -20,
      control: 'heater', labels: { solid: 'Ice', liquid: 'Water', gas: 'Steam' }, color: '#3b82f6',
      goals: ['melting', 'liquid', 'boiling', 'gas']
    },
    examples: [
      { mode: 'states', substance: 'Wax', melt: 60, boil: 370, range: [20, 400], start: 25, control: 'temp', color: '#ff9f43',
        labels: { solid: 'Solid wax', liquid: 'Liquid wax', gas: 'Wax vapour' }, goals: ['liquid', 'solid'],
        challenge: 'Grade 6: Melt the candle wax, then let it cool so it freezes again.' },
      { mode: 'diffusion', medium: 'water', dyeName: 'Ink', start: 20, dyeTime: 10,
        challenge: 'Grade 8–9: Drop ink in water. Make it spread fully in under 10 s — what must you change?' },
      { mode: 'evaporation', substance: 'Water', start: 30, evaporate: 50, color: '#2ed3a5',
        challenge: 'Grade 6–9: Dry half the water quickly. Try heat and a wide dish. Then use the lid to see condensation!' }
    ]
  });
})();
