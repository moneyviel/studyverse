/* StudyVerse Concept Lab: forces — friction & F = ma, pressure, and weight on different worlds.
 *
 * friction: the child pushes (or pulls) a box with a force slider on ice / wood / carpet. Static
 *   friction holds the box until F > μs·m·g; then kinetic friction μk·m·g acts, the net force gives
 *   a = (F − f)/m and the ground scrolls by as the box speeds up (or slows down if F < f).
 * pressure: the same force on different contact areas; P = F/A in N/m² (Pa); the sand dents deeper.
 * gravity: a mass hangs from a spring balance on Earth, Moon, Mars, Jupiter; W = m·g.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   mode       string  'friction' | 'pressure' | 'gravity'                              default 'friction'
 *   modes      array   modes offered as tabs                                            default [mode]
 *   goal       string  friction: 'move' (make it move) | 'least' (smallest force that moves it on
 *                      `surface`) | 'accel' (reach acceleration `target` m/s²);
 *                      pressure: 'pressure' (make P = target Pa); gravity: 'weight' (W = target N
 *                      on `body`) | 'compare' (weigh the same mass on 2 worlds); any: 'none'
 *                                                             default 'least' / 'pressure' / 'compare'
 *   target     number  target value (m/s², Pa or N, by goal)
 *   surface    string  surface name the goal is about (friction)                       default first
 *   body       string  world name the goal is about (gravity)                           default any
 *   challenge  string  challenge text (any language); default made from goal
 *   winText    string  optional win message
 *   mass       number  mass in kg                                                       default 5
 *   massRange  [min,max,step] show a mass slider (kg)                                  default none (friction),
 *                                                                                       [1,20,1] (gravity)
 *   force      number  starting force in N                                              default 10
 *   forceRange [min,max,step] force slider in N                         default [0,60,1] / [10,200,10]
 *   surfaces   array   [{name, mus, muk, color}] friction surfaces       default Ice .10/.05, Wood .40/.30, Carpet .70/.55
 *   faces      array   [{name, area (cm²), w, h (drawing size, cm)}]     default brick faces 200/100/50 cm²
 *   bodies     array   [{name, g}]                                       default Earth 9.8, Moon 1.62, Mars 3.7, Jupiter 24.8
 *   g          number  gravity used for friction and pressure modes                     default 9.8
 *   object     string  label for the box / thing                                        default 'Box'
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const f2 = v => { const r = Math.round(v * 100) / 100; return String(Object.is(r, -0) ? 0 : r).replace('-', '−'); };
  const f1 = v => { const r = Math.round(v * 10) / 10; return String(Object.is(r, -0) ? 0 : r).replace('-', '−'); };
  const big = v => Math.round(v).toLocaleString('en-IN');
  const rng = (a, def) => Array.isArray(a) && a.length >= 2 && +a[1] > +a[0] ? [+a[0], +a[1], +a[2] > 0 ? +a[2] : def[2]] : def;
  const SURF = [{ name: 'Ice', mus: 0.10, muk: 0.05, color: '#cfefff' }, { name: 'Wood', mus: 0.40, muk: 0.30, color: '#d9a066' }, { name: 'Carpet', mus: 0.70, muk: 0.55, color: '#e0607e' }];
  const FACES = [{ name: 'Lying flat', area: 200, w: 20, h: 5 }, { name: 'On its side', area: 100, w: 20, h: 10 }, { name: 'Standing up', area: 50, w: 10, h: 20 }];
  const BODIES = [{ name: 'Earth', g: 9.8 }, { name: 'Moon', g: 1.62 }, { name: 'Mars', g: 3.7 }, { name: 'Jupiter', g: 24.8 }];
  const SKY = { Earth: ['#bfe3ff', '#7cc46b'], Moon: ['#2b2f4a', '#b9bccb'], Mars: ['#f6c7a8', '#c8643c'], Jupiter: ['#f3dfc1', '#c99a6b'] };

  const CSS = `
.lb-forces-w{font-size:14px;color:#1b1f3a;-webkit-user-select:none;user-select:none}
.lb-forces-ch{font-weight:800;font-size:14px;margin-bottom:6px;line-height:1.25}
.lb-forces-svg{width:100%;height:auto;display:block;background:#f7f8ff;border-radius:16px}
.lb-forces-row{display:flex;gap:5px;margin-top:6px}
.lb-forces-b{flex:1 1 0;min-width:0;min-height:42px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:12.5px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 4px;line-height:1.1}
.lb-forces-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-forces-b.sm{flex:0 0 auto;padding:0 12px}
.lb-forces-b:active{transform:translateY(2px)}
.lb-forces-sl{display:flex;align-items:center;gap:8px;font-weight:800;font-size:13px;margin-top:2px}
.lb-forces-sl span{min-width:50px}
.lb-forces-sl input{flex:1;min-width:0;accent-color:#8b5cf6;height:36px}
.lb-forces-sl b{min-width:58px;text-align:right;color:#3b82f6;font-variant-numeric:tabular-nums}
.lb-forces-out{background:#f6f4ff;border-radius:12px;padding:6px 10px;margin-top:5px;font-weight:800;font-size:13px;line-height:1.35;min-height:36px}
.lb-forces-out i{font-style:normal;color:#6b7090;font-size:12px}
`;

  Labs.register('forces', {
    title: 'Forces lab',
    subjects: ['science', 'physics'],
    render(host, p, api) {
      const ex = this.example || {};
      const diffMode = p.mode !== undefined && p.mode !== ex.mode;
      p = Object.assign({}, p);
      if (diffMode) ['modes', 'goal', 'target', 'surface', 'body', 'force', 'forceRange', 'massRange', 'mass'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      if (diffMode || p.goal !== ex.goal || p.target !== ex.target) ['challenge', 'winText'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });

      const ALL = ['friction', 'pressure', 'gravity'];
      let mode = ALL.includes(p.mode) ? p.mode : 'friction';
      const modes = (Array.isArray(p.modes) ? p.modes : []).filter(m => ALL.includes(m));
      if (!modes.includes(mode)) modes.unshift(mode);
      const surfaces = (Array.isArray(p.surfaces) && p.surfaces.length ? p.surfaces : SURF).filter(s => s && s.name).map((s, i) => ({ name: String(s.name), mus: Math.max(0, +s.mus || 0), muk: Math.max(0, Math.min(+s.muk >= 0 ? +s.muk : (+s.mus || 0) * 0.75, +s.mus || 0)), color: s.color || SURF[i % 3].color }));
      const faces = (Array.isArray(p.faces) && p.faces.length ? p.faces : FACES).filter(f => f && +f.area > 0).map(f => ({ name: String(f.name || ''), area: +f.area, w: +f.w || Math.sqrt(+f.area), h: +f.h || 6 }));
      const bodies = (Array.isArray(p.bodies) && p.bodies.length ? p.bodies : BODIES).filter(b => b && +b.g > 0).map(b => ({ name: String(b.name), g: +b.g }));
      const G = +p.g > 0 ? +p.g : 9.8;
      const obj = String(p.object || 'Box');
      const goalDef = { friction: 'least', pressure: 'pressure', gravity: 'compare' };
      let won = false, raf = 0, last = 0;
      const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(p.winText ? String(p.winText) : m); };

      host.innerHTML = `<style>${CSS}</style><div class="lb-forces-w">
  <div class="lb-forces-ch"></div>
  ${modes.length > 1 ? `<div class="lb-forces-row" style="margin:0 0 6px">${modes.map(m => `<button class="lb-forces-b" data-mode="${m}">${{ friction: 'Friction', pressure: 'Pressure', gravity: 'Weight' }[m]}</button>`).join('')}</div>` : ''}
  <div class="lb-forces-body"></div></div>`;
      const chEl = host.querySelector('.lb-forces-ch'), body = host.querySelector('.lb-forces-body');
      let cleanupMode = () => { };

      function setup() {
        cleanupMode(); cancelAnimationFrame(raf);
        host.querySelectorAll('[data-mode]').forEach(b => b.classList.toggle('on', b.dataset.mode === mode));
        const goal = String(p.goal && (modes.length === 1 || goalFits(p.goal, mode)) ? p.goal : goalDef[mode]);
        if (mode === 'friction') cleanupMode = friction(goal);
        else if (mode === 'pressure') cleanupMode = pressure(goal);
        else cleanupMode = gravity(goal);
      }
      const goalFits = (g, m) => ({ friction: ['move', 'least', 'accel', 'none'], pressure: ['pressure', 'none'], gravity: ['weight', 'compare', 'none'] }[m] || []).includes(g);
      const setCh = t => { chEl.textContent = '🎯 Challenge: ' + (p.challenge && goalFits(p.goal || goalDef[mode], mode) ? String(p.challenge) : t); };

      // ================= FRICTION =================
      function friction(goal) {
        const fR = rng(p.forceRange, [0, 60, 1]);
        const mR = Array.isArray(p.massRange) ? rng(p.massRange, [1, 20, 1]) : null;
        let F = Math.min(fR[1], Math.max(fR[0], +p.force >= 0 ? +p.force : 10));
        let m = +p.mass > 0 ? +p.mass : 5;
        let si = Math.max(0, surfaces.findIndex(s => s.name === p.surface));
        const goalSurf = p.surface ? surfaces.findIndex(s => s.name === p.surface) : -1;
        const target = +p.target || 1;
        let v = 0, x = 0, pull = false, moving = false;
        const sName = goalSurf >= 0 ? surfaces[goalSurf].name.toLowerCase() : surfaces[si].name.toLowerCase();
        setCh({
          move: `Push the ${obj.toLowerCase()} hard enough to make it slide.`,
          least: `Find the smallest force that makes the ${obj.toLowerCase()} move on ${sName}.`,
          accel: `Make the ${obj.toLowerCase()} speed up at ${f2(target)} m/s²${goalSurf >= 0 ? ' on ' + sName : ''}.`,
          none: 'Push the box on each surface. Where is friction biggest?'
        }[goal] || '');
        body.innerHTML = `<svg class="lb-forces-svg" viewBox="0 0 360 170"></svg>
<div class="lb-forces-row">${surfaces.map((s, i) => `<button class="lb-forces-b" data-s="${i}">${esc(s.name)}</button>`).join('')}<button class="lb-forces-b sm" data-pull="1"></button></div>
<div class="lb-forces-sl"><span>Force</span><input type="range" class="lb-forces-f" min="${fR[0]}" max="${fR[1]}" step="${fR[2]}" value="${F}"><b></b></div>
${mR ? `<div class="lb-forces-sl"><span>Mass</span><input type="range" class="lb-forces-m" min="${mR[0]}" max="${mR[1]}" step="${mR[2]}" value="${m}"><b></b></div>` : ''}
<div class="lb-forces-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-forces-out'), fIn = body.querySelector('.lb-forces-f'), mIn = body.querySelector('.lb-forces-m');
        const N = () => m * G;
        function state() {
          const s = surfaces[si], fs = s.mus * N(), fk = s.muk * N();
          if (!moving) return F > fs + 1e-9 ? { fr: fk, net: F - fk, a: (F - fk) / m, start: true } : { fr: F, net: 0, a: 0, start: false, fs };
          return { fr: fk, net: F - fk, a: (F - fk) / m };
        }
        const halo = 'stroke="#fff" stroke-width="3.5" paint-order="stroke"';
        function arrow(x1, x2, y, col, lab, where) {
          if (Math.abs(x2 - x1) < 2) return '';
          const d = Math.sign(x2 - x1);
          const t = where === 'tail' ? `<text x="${x1 - 6 * d}" y="${y + 4}" text-anchor="${d > 0 ? 'end' : 'start'}"` :
            where === 'head' ? `<text x="${x2 + 6 * d}" y="${y + 4}" text-anchor="${d > 0 ? 'start' : 'end'}"` : `<text x="${(x1 + x2) / 2}" y="${y - 10}" text-anchor="middle"`;
          return `<line x1="${x1}" y1="${y}" x2="${x2 - d * 9}" y2="${y}" stroke="${col}" stroke-width="6" stroke-linecap="round"/><path d="M${x2} ${y} l${-d * 12} -9 v18z" fill="${col}"/>` +
            `${t} font-size="11.5" font-weight="800" fill="${col}" ${halo}>${lab}</text>`;
        }
        function draw(st) {
          const s = surfaces[si], gy = 118, bx = 168, bw = 64, bh = 54, k = Math.min(1.6, 95 / fR[1]);
          let o = `<rect x="0" y="0" width="360" height="${gy}" fill="#eef5ff"/><rect x="0" y="${gy}" width="360" height="52" fill="${esc(s.color)}"/>`;
          const off = -((x * 30) % 40 + 40) % 40;
          for (let gx = off; gx < 380; gx += 40) {
            if (s.name === 'Ice' || /ice|बर्फ/i.test(s.name)) o += `<path d="M${gx} ${gy + 14} l18 -6" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".9"/>`;
            else if (/carpet|दरी|कालीन/i.test(s.name)) { for (let j = 0; j < 4; j++) o += `<circle cx="${gx + j * 10 + 3}" cy="${gy + 8 + (j % 2) * 8}" r="2" fill="rgba(0,0,0,.18)"/>`; }
            else o += `<line x1="${gx}" y1="${gy}" x2="${gx}" y2="${gy + 52}" stroke="rgba(0,0,0,.15)" stroke-width="2"/><path d="M${gx + 6} ${gy + 20} q12 -6 24 0" fill="none" stroke="rgba(0,0,0,.12)" stroke-width="2"/>`;
          }
          o += `<line x1="0" y1="${gy}" x2="360" y2="${gy}" stroke="rgba(0,0,0,.25)" stroke-width="2"/>`;
          // box
          o += `<g transform="translate(${bx} ${gy - bh})"><rect width="${bw}" height="${bh}" rx="6" fill="#ffc93c" stroke="#c98a1b" stroke-width="3"/><path d="M6 6 L${bw - 6} ${bh - 6} M${bw - 6} 6 L6 ${bh - 6}" stroke="#e0a42a" stroke-width="3"/>` +
            `<text x="${bw / 2}" y="${bh / 2 + 5}" text-anchor="middle" font-size="13" font-weight="800" fill="#7a4d00">${f1(m)} kg</text></g>`;
          // applied force
          const len = F * k;
          if (pull) { o += `<line x1="${bx + bw}" y1="${gy - bh / 2}" x2="${bx + bw + 18 + len}" y2="${gy - bh / 2}" stroke="#9a6b3c" stroke-width="2.5"/>` + arrow(bx + bw + 18, bx + bw + 18 + len, gy - bh / 2 - 14, '#3b82f6', `Pull ${f1(F)} N`, 'mid'); }
          else o += arrow(bx - 8 - len, bx - 8, gy - bh / 2, '#3b82f6', `Push ${f1(F)} N`, 'tail');
          // friction (at the bottom, opposite)
          if (st.fr > 0.01) o += arrow(bx + bw / 2, bx + bw / 2 - st.fr * k, gy + 14, '#e04848', `Friction ${f1(st.fr)} N`, 'head');
          o += `<text x="10" y="20" font-size="12" font-weight="800" fill="#1b1f3a">Net force = ${f1(st.net)} N</text><text x="10" y="37" font-size="12" font-weight="800" fill="#8b5cf6">a = ${f2(st.a)} m/s²</text>`;
          o += `<text x="350" y="20" text-anchor="end" font-size="12" font-weight="800" fill="#ff6b6b">v = ${f1(v)} m/s</text><text x="350" y="37" text-anchor="end" font-size="11" font-weight="800" fill="#6b7090">${moving ? 'sliding 🏃' : 'not moving'}</text>`;
          sv.innerHTML = o;
        }
        function ui() {
          body.querySelectorAll('[data-s]').forEach(b => b.classList.toggle('on', +b.dataset.s === si));
          body.querySelector('[data-pull]').textContent = pull ? '🪢 Pull' : '✋ Push';
          fIn.nextElementSibling.textContent = `${f1(F)} N`;
          if (mIn) mIn.nextElementSibling.textContent = `${f1(m)} kg`;
        }
        function report(st) {
          const s = surfaces[si];
          if (!moving) out.innerHTML = `Friction balances your force (${f1(F)} N), so it stays still. <i>Max grip on ${esc(s.name)} = μ × m × g = ${f2(s.mus)} × ${f1(m)} × ${f1(G)} = ${f1(s.mus * N())} N</i>`;
          else out.innerHTML = `Sliding friction = ${f1(st.fr)} N. F = ma → a = (${f1(F)} − ${f1(st.fr)}) ÷ ${f1(m)} = ${f2(st.a)} m/s²${st.a < 0 ? ' (slowing down)' : ''}`;
        }
        function tick(now) {
          const dt = Math.min(0.05, (now - last) / 1000); last = now;
          let st = state();
          if (!moving && st.start) {
            moving = true; api.sfx('tap');
            if (goal === 'move') winOnce(`${f1(F)} N beat the friction grip of ${f1(st.fs || surfaces[si].mus * N())} N, so the ${obj.toLowerCase()} moves!`);
            if (goal === 'least' && (goalSurf < 0 || goalSurf === si) && F - surfaces[si].mus * N() <= fR[2] + 1e-9)
              winOnce(`About ${f1(surfaces[si].mus * N())} N is needed on ${surfaces[si].name} — friction = μ × m × g. Rougher surface → more friction.`);
            st = state();
          }
          if (moving) {
            v += st.a * dt;
            if (v <= 0) { v = 0; moving = false; st = state(); }
            x += v * dt;
            if (goal === 'accel' && moving && (goalSurf < 0 || goalSurf === si) && Math.abs(st.a - target) <= Math.max(0.05, 0.5 * fR[2] / m + 1e-9))
              winOnce(`a = (F − friction) ÷ m = (${f1(F)} − ${f1(st.fr)}) ÷ ${f1(m)} = ${f2(st.a)} m/s²`);
          }
          draw(st); report(st);
          raf = requestAnimationFrame(tick);
        }
        const stopBox = () => { v = 0; moving = false; };
        const onIn = e => { if (e.target === fIn) F = +fIn.value; else if (e.target === mIn) { m = +mIn.value; } ui(); };
        const onClick = e => {
          const b = e.target.closest('button'); if (!b || !body.contains(b)) return;
          if (b.dataset.s !== undefined) { si = +b.dataset.s; stopBox(); api.sfx('tap'); ui(); }
          else if (b.dataset.pull) { pull = !pull; api.sfx('tap'); ui(); }
        };
        body.addEventListener('input', onIn); body.addEventListener('click', onClick);
        ui(); last = performance.now(); raf = requestAnimationFrame(tick);
        return () => { cancelAnimationFrame(raf); body.removeEventListener('input', onIn); body.removeEventListener('click', onClick); };
      }

      // ================= PRESSURE =================
      function pressure(goal) {
        const fR = rng(p.forceRange, [10, 200, 10]);
        let F = Math.min(fR[1], Math.max(fR[0], +p.force > 0 ? +p.force : 50));
        let fi = 0;
        const target = +p.target || 10000;
        setCh(goal === 'pressure' ? `Make a pressure of ${big(target)} Pa (N/m²) on the sand.` : 'Same force, different area — which makes the deepest dent?');
        const Pmax = fR[1] / (Math.min(...faces.map(f => f.area)) / 1e4);
        body.innerHTML = `<svg class="lb-forces-svg" viewBox="0 0 360 190"></svg>
<div class="lb-forces-row">${faces.map((f, i) => `<button class="lb-forces-b" data-f="${i}">${esc(f.name)}<br><small>${f2(f.area)} cm²</small></button>`).join('')}</div>
<div class="lb-forces-sl"><span>Force</span><input type="range" min="${fR[0]}" max="${fR[1]}" step="${fR[2]}" value="${F}"><b></b></div>
<div class="lb-forces-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-forces-out'), fIn = body.querySelector('input');
        const maxDim = Math.max(...faces.map(f => Math.max(f.w, f.h)));
        let depth = 0, raf2 = 0;
        function draw() {
          const fc = faces[fi], A = fc.area / 1e4, P = F / A;
          const sc = Math.min(6, 120 / maxDim), w = fc.w * sc, h = fc.h * sc, sy = 150, cx = 180;
          let o = `<rect x="0" y="0" width="360" height="${sy}" fill="#eef5ff"/>`;
          const d = depth;
          o += `<path d="M0 ${sy} H${cx - w / 2 - 14} Q${cx - w / 2} ${sy} ${cx - w / 2} ${sy + d} H${cx + w / 2} Q${cx + w / 2} ${sy} ${cx + w / 2 + 14} ${sy} H360 V190 H0Z" fill="#f2d49b"/>`;
          for (let i = 0; i < 26; i++) o += `<circle cx="${(i * 53) % 350 + 6}" cy="${sy + 12 + (i * 17) % 26}" r="1.6" fill="#c9a25a"/>`;
          o += `<rect x="${cx - w / 2}" y="${sy + d - h}" width="${w}" height="${h}" rx="3" fill="#e2603f" stroke="#a63c22" stroke-width="2.5"/>`;
          for (let yy = sy + d - h + 10; yy < sy + d - 2; yy += 10) o += `<line x1="${cx - w / 2 + 2}" y1="${yy}" x2="${cx + w / 2 - 2}" y2="${yy}" stroke="#c44d30" stroke-width="1"/>`;
          const top = sy + d - h, al = 18 + 40 * F / fR[1];
          o += `<line x1="${cx}" y1="${top - al - 4}" x2="${cx}" y2="${top - 12}" stroke="#3b82f6" stroke-width="6" stroke-linecap="round"/><path d="M${cx} ${top - 2} l-9 -13 h18z" fill="#3b82f6"/>`;
          o += `<text x="${cx + 12}" y="${top - al / 2}" font-size="12" font-weight="800" fill="#3b82f6">F = ${f1(F)} N</text>`;
          o += `<text x="10" y="20" font-size="12" font-weight="800" fill="#1b1f3a">Area = ${f2(fc.area)} cm² = ${+(A).toPrecision(3)} m²</text>`;
          o += `<text x="10" y="38" font-size="13" font-weight="800" fill="#8b5cf6">Pressure = ${big(P)} Pa</text>`;
          sv.innerHTML = o;
          return P;
        }
        function anim() {
          const fc = faces[fi], P = F / (fc.area / 1e4), td = 4 + 30 * P / Pmax;
          depth += (td - depth) * 0.18;
          draw();
          if (Math.abs(td - depth) > 0.05) raf2 = requestAnimationFrame(anim); else { depth = td; draw(); }
        }
        function upd(user) {
          const fc = faces[fi], A = fc.area / 1e4, P = F / A;
          body.querySelectorAll('[data-f]').forEach(b => b.classList.toggle('on', +b.dataset.f === fi));
          fIn.nextElementSibling.textContent = `${f1(F)} N`;
          out.innerHTML = `P = F ÷ A = ${f1(F)} N ÷ ${+(A).toPrecision(3)} m² = ${big(P)} Pa <i>· smaller area → bigger pressure</i>`;
          cancelAnimationFrame(raf2); raf2 = requestAnimationFrame(anim);
          if (user && goal === 'pressure' && Math.abs(P - target) <= target * 0.01) winOnce(`P = F ÷ A = ${f1(F)} N ÷ ${+(A).toPrecision(3)} m² = ${big(P)} Pa`);
        }
        const onIn = () => { F = +fIn.value; upd(true); };
        const onClick = e => { const b = e.target.closest('[data-f]'); if (!b) return; fi = +b.dataset.f; api.sfx('tap'); upd(true); };
        body.addEventListener('input', onIn); body.addEventListener('click', onClick);
        if (Math.abs(F / (faces[0].area / 1e4) - target) <= target * 0.01) F = Math.min(fR[1], F + fR[2]);
        fIn.value = F; depth = 4; upd(false);
        return () => { cancelAnimationFrame(raf2); body.removeEventListener('input', onIn); body.removeEventListener('click', onClick); };
      }

      // ================= GRAVITY =================
      function gravity(goal) {
        const mR = rng(p.massRange, [1, 20, 1]);
        let m = Math.min(mR[1], Math.max(mR[0], +p.mass > 0 ? +p.mass : 5));
        let bi = 0;
        const target = +p.target || 16.2;
        const gb = p.body ? bodies.findIndex(b => b.name === p.body) : -1;
        const seen = {};
        setCh(goal === 'weight' ? `Find a mass that weighs ${f2(target)} N${gb >= 0 ? ' on ' + bodies[gb].name : ''}.` : goal === 'compare' ? 'Weigh the same mass on two different worlds. What changes?' : 'Change the mass and the world. Watch the weight.');
        const Wmax = mR[1] * Math.max(...bodies.map(b => b.g));
        body.innerHTML = `<svg class="lb-forces-svg" viewBox="0 0 360 200"></svg>
<div class="lb-forces-row">${bodies.map((b, i) => `<button class="lb-forces-b" data-b="${i}">${esc(b.name)}</button>`).join('')}</div>
<div class="lb-forces-sl"><span>Mass</span><input type="range" min="${mR[0]}" max="${mR[1]}" step="${mR[2]}" value="${m}"><b></b></div>
<div class="lb-forces-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-forces-out'), mIn = body.querySelector('input');
        let ext = 0, raf2 = 0;
        function draw() {
          const b = bodies[bi], W = m * b.g, col = SKY[b.name] || ['#e6ecff', '#9aa0c0'];
          let o = `<rect width="360" height="200" fill="${col[0]}"/><path d="M0 178 Q90 168 180 176 T360 172 V200 H0Z" fill="${col[1]}"/>`;
          if (b.name === 'Moon') o += '<circle cx="60" cy="188" r="6" fill="#9a9db0"/><circle cx="300" cy="186" r="8" fill="#9a9db0"/><circle cx="40" cy="30" r="2" fill="#fff"/><circle cx="320" cy="50" r="1.5" fill="#fff"/><circle cx="250" cy="22" r="2" fill="#fff"/>';
          // stand
          o += `<rect x="96" y="8" width="8" height="172" rx="3" fill="#6b7090"/><rect x="96" y="8" width="96" height="8" rx="3" fill="#6b7090"/>`;
          const sx = 168, top = 22, sl = 30 + ext;
          o += `<rect x="${sx - 16}" y="${top - 6}" width="32" height="${sl + 16}" rx="8" fill="#fff" stroke="#3b82f6" stroke-width="2.5" opacity=".9"/>`;
          let zz = `M${sx} ${top}`; const n = 10;
          for (let i = 1; i <= n; i++) zz += ` L${sx + (i % 2 ? 9 : -9)} ${top + sl * i / (n + 1)}`;
          zz += ` L${sx} ${top + sl}`;
          o += `<path d="${zz}" fill="none" stroke="#1b1f3a" stroke-width="2"/>`;
          o += `<line x1="${sx}" y1="${top + sl}" x2="${sx}" y2="${top + sl + 14}" stroke="#1b1f3a" stroke-width="2"/>`;
          const bs = 26 + 14 * Math.sqrt(m / mR[1]);
          o += `<rect x="${sx - bs / 2}" y="${top + sl + 14}" width="${bs}" height="${bs}" rx="5" fill="#8b5cf6"/><text x="${sx}" y="${top + sl + 18 + bs / 2}" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">${f1(m)} kg</text>`;
          // weight dial
          o += `<rect x="232" y="34" width="118" height="78" rx="14" fill="rgba(255,255,255,.92)"/>`;
          o += `<text x="291" y="56" text-anchor="middle" font-size="11.5" font-weight="800" fill="#6b7090">Weight on ${esc(b.name)}</text><text x="291" y="84" text-anchor="middle" font-size="22" font-weight="800" fill="#ff6b6b">${f1(W)} N</text><text x="291" y="103" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">g = ${f2(b.g)} m/s²</text>`;
          o += `<path d="M${sx} ${top + sl + 14 + bs + 4} v${12}" stroke="#ff6b6b" stroke-width="4"/><path d="M${sx} ${top + sl + 14 + bs + 24} l-7 -10 h14z" fill="#ff6b6b"/>`;
          sv.innerHTML = o;
        }
        function anim() {
          const W = m * bodies[bi].g, te = 96 * W / Wmax;
          ext += (te - ext) * 0.15; draw();
          if (Math.abs(te - ext) > 0.1) raf2 = requestAnimationFrame(anim); else { ext = te; draw(); }
        }
        function upd(user) {
          const b = bodies[bi], W = m * b.g;
          body.querySelectorAll('[data-b]').forEach(x => x.classList.toggle('on', +x.dataset.b === bi));
          mIn.nextElementSibling.textContent = `${f1(m)} kg`;
          out.innerHTML = `Mass ${f1(m)} kg (same everywhere) · W = m × g = ${f1(m)} × ${f2(b.g)} = ${f1(W)} N`;
          cancelAnimationFrame(raf2); raf2 = requestAnimationFrame(anim);
          if (!user) return;
          if (goal === 'weight' && (gb < 0 || gb === bi) && Math.abs(W - target) <= Math.max(0.05, target * 0.005)) winOnce(`W = m × g = ${f1(m)} kg × ${f2(b.g)} m/s² = ${f1(W)} N`);
          if (goal === 'compare') {
            const key = String(m); seen[key] = seen[key] || {}; seen[key][bi] = W;
            const ks = Object.keys(seen[key]);
            if (ks.length >= 2) winOnce(`Mass stays ${f1(m)} kg, but weight changes: ` + ks.map(k => `${bodies[k].name} ${f1(seen[key][k])} N`).join(', ') + '. Weight = m × g.');
          }
        }
        const onIn = () => { m = +mIn.value; upd(true); };
        const onClick = e => { const b = e.target.closest('[data-b]'); if (!b) return; bi = +b.dataset.b; api.sfx('tap'); upd(true); };
        body.addEventListener('input', onIn); body.addEventListener('click', onClick);
        ext = 96 * m * bodies[0].g / Wmax;
        const s0 = {}; s0[0] = m * bodies[0].g; seen[String(m)] = s0;
        upd(false);
        return () => { cancelAnimationFrame(raf2); body.removeEventListener('input', onIn); body.removeEventListener('click', onClick); };
      }

      const onTab = e => { const b = e.target.closest('[data-mode]'); if (!b) return; mode = b.dataset.mode; api.sfx('tap'); setup(); };
      host.addEventListener('click', onTab);
      setup();
      return () => { cleanupMode(); cancelAnimationFrame(raf); host.removeEventListener('click', onTab); };
    },
    example: {
      mode: 'friction',
      goal: 'least', surface: 'Carpet',
      mass: 5, force: 10, forceRange: [0, 60, 1],
      object: 'Box',
      challenge: 'Find the smallest push that makes the box move on carpet. Try ice and wood too!'
    },
    examples: [
      { mode: 'friction', goal: 'accel', target: 2, surface: 'Wood', mass: 5, force: 10, forceRange: [0, 60, 1], challenge: 'Grade 9: Make the box speed up at 2 m/s² on wood (F − friction = m × a).' },
      { mode: 'pressure', modes: ['pressure'], goal: 'pressure', target: 10000, force: 50, forceRange: [10, 200, 10], challenge: 'Grade 8: Make a pressure of 10,000 Pa on the sand. Try different faces of the brick.' },
      { mode: 'gravity', goal: 'weight', target: 16.2, body: 'Moon', mass: 4, massRange: [1, 20, 1], challenge: 'Grade 9: Which mass weighs 16.2 N on the Moon?' }
    ]
  });
})();
