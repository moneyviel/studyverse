/* StudyVerse Concept Lab: motion — a car on a track with live distance–time and speed–time graphs,
 * plus a simple pendulum mode.
 *
 * Track: the child sets the starting speed (and, for non-uniform motion, the acceleration), presses
 * Go and watches the car. A dot is dropped every second (like ticker tape): equal gaps = uniform
 * motion, growing gaps = speeding up. Both graphs are drawn live. Uses v = u + at, s = ut + ½at².
 * Pendulum: the child sets the string length, presses Start and the lab counts oscillations with a
 * stopwatch; time period T = total time ÷ oscillations (the physics uses T = 2π√(L/g)).
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   mode         string  'track' | 'pendulum'                                            default 'track'
 *   motion       string  'uniform' | 'accelerated' | 'both' (both = acceleration slider that
 *                        includes 0, so the child can compare uniform and non-uniform)      default 'uniform'
 *   speed        number  starting speed u in m/s                                         default 4
 *   speedRange   [min,max,step] speed slider in m/s                                     default [0,15,0.5]
 *   accel        number  starting acceleration a in m/s²                                  default 1
 *   accelRange   [min,max,step] acceleration slider in m/s²                             default [-2,3,0.5]
 *   duration     number  run time in seconds                                             default 10
 *   trackLength  number  length of the track in metres                                   default 150
 *   timeScale    number  how much faster than real time the run plays                    default 2
 *   goal         string  'distance' (cover `target` m in `duration` s) | 'time' (reach the end of
 *                        the track in `target` s) | 'match' (match the dashed target graphs) |
 *                        'period' (pendulum T = target s) | 'measure' (measure any T) | 'none'
 *                                                                default 'distance' (track) / 'period'
 *   target       number|object  number for distance/time/period, or {speed, accel} for match  default 60
 *   challenge    string  challenge text (any language); default made from goal
 *   winText      string  optional win message
 *   object       string  label for the moving thing                                      default 'Car'
 *   length       number  pendulum: starting length in cm                                 default 40
 *   lengthRange  [min,max,step] pendulum length slider in cm                            default [10,150,1]
 *   count        number  pendulum: oscillations to time                                  default 10
 *   g            number  gravity in m/s² (e.g. 1.62 on the Moon)                         default 9.8
 *   showFormula  boolean pendulum: show T = 2π√(L/g)                                      default false
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = (v, d = 1) => { const r = Math.round(v * Math.pow(10, d)) / Math.pow(10, d); return (Object.is(r, -0) ? 0 : r).toFixed(d).replace('-', '−'); };
  const fmtN = v => { const r = Math.round(v * 100) / 100; return String(r).replace('-', '−'); };
  const rng = (a, def) => Array.isArray(a) && a.length >= 2 && +a[1] > +a[0] ? [+a[0], +a[1], +a[2] > 0 ? +a[2] : def[2]] : def;
  const nice = v => { const p = Math.pow(10, Math.floor(Math.log10(v))); const m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; };

  const CSS = `
.lb-motion-w{font-size:14px;color:#1b1f3a;-webkit-user-select:none;user-select:none}
.lb-motion-ch{font-weight:800;font-size:14px;margin-bottom:6px;line-height:1.25}
.lb-motion-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:16px}
.lb-motion-g{margin-top:5px}
.lb-motion-row{display:flex;gap:6px;margin-top:6px;align-items:center}
.lb-motion-b{flex:1 1 0;min-height:42px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:13.5px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 8px}
.lb-motion-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-motion-b.go{background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1a9c78}
.lb-motion-b:active{transform:translateY(2px)}
.lb-motion-b:disabled{opacity:.45}
.lb-motion-sl{display:flex;align-items:center;gap:8px;font-weight:800;font-size:13px;margin-top:2px}
.lb-motion-sl span{min-width:62px}
.lb-motion-sl input{flex:1;min-width:0;accent-color:#8b5cf6;height:34px}
.lb-motion-sl b{min-width:66px;text-align:right;color:#3b82f6;font-variant-numeric:tabular-nums}
.lb-motion-ctl{display:flex;gap:8px;align-items:center;margin-top:4px}
.lb-motion-sls{flex:1;min-width:0}
.lb-motion-btns{display:flex;flex-direction:column;gap:6px;flex:0 0 86px}
.lb-motion-btns .lb-motion-b{flex:0 0 auto;min-height:40px}
.lb-motion-sl span{min-width:56px}
.lb-motion-sl b{min-width:58px}
.lb-motion-out{background:#f6f4ff;border-radius:12px;padding:6px 10px;margin-top:5px;font-weight:800;font-size:13px;line-height:1.35;min-height:34px}
`;

  Labs.register('motion', {
    title: 'Motion lab',
    subjects: ['science', 'physics'],
    render(host, p, api) {
      const ex = this.example || {};
      const diffMode = p.mode !== undefined && p.mode !== ex.mode;
      p = Object.assign({}, p);
      if (diffMode) ['goal', 'target', 'motion'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      if (diffMode || p.goal !== ex.goal || p.target !== ex.target) ['challenge', 'winText'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });

      const mode = p.mode === 'pendulum' ? 'pendulum' : 'track';
      const g = +p.g > 0 ? +p.g : 9.8;
      const goal = String(p.goal || (mode === 'pendulum' ? 'period' : 'distance'));
      let won = false, raf = 0, last = 0;
      const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(p.winText ? String(p.winText) : m); };

      host.innerHTML = `<style>${CSS}</style><div class="lb-motion-w"><div class="lb-motion-ch"></div><div class="lb-motion-body"></div></div>`;
      const chEl = host.querySelector('.lb-motion-ch'), body = host.querySelector('.lb-motion-body');

      // =================== TRACK ===================
      if (mode === 'track') {
        const sR = rng(p.speedRange, [0, 15, 0.5]), aR = rng(p.accelRange, [-2, 3, 0.5]);
        const T = +p.duration > 0 ? +p.duration : 10, L = +p.trackLength > 0 ? +p.trackLength : 150;
        const scale = +p.timeScale > 0 ? +p.timeScale : 2;
        const mopt = ['uniform', 'accelerated', 'both'].includes(p.motion) ? p.motion : 'uniform';
        const accelOn = mopt !== 'uniform';
        const snap = (v, r) => Math.min(r[1], Math.max(r[0], Math.round((v - r[0]) / r[2]) * r[2] + r[0]));
        let u = snap(+p.speed >= 0 ? +p.speed : 4, sR), a = snap(p.accel !== undefined ? +p.accel || 0 : 1, aR);
        const tgt = p.target && typeof p.target === 'object' ? { speed: +p.target.speed || 0, accel: +p.target.accel || 0 } : null;
        const tnum = typeof p.target === 'number' || typeof p.target === 'string' ? +p.target : (goal === 'time' ? 10 : 60);
        const obj = String(p.object || 'Car');
        const DEFCH = {
          distance: `Set the speed so the ${obj.toLowerCase()} covers ${fmtN(tnum)} m in ${fmtN(T)} s.`,
          time: `Set the speed so the ${obj.toLowerCase()} reaches the ${fmtN(L)} m finish in ${fmtN(tnum)} s.`,
          match: 'Make your graphs match the dashed target graphs, then press Go.',
          none: 'Change the speed, press Go and watch the graphs.'
        };
        chEl.textContent = '🎯 Challenge: ' + (p.challenge ? String(p.challenge) : (DEFCH[goal] || DEFCH.none));

        // axes maxima (fixed, so runs can be compared)
        const vTop = nice(Math.max(1, sR[1] + Math.max(0, aR[1]) * (mopt === 'uniform' ? 0 : T), tgt ? tgt.speed + Math.max(0, tgt.accel) * T : 0));
        const run = { t: 0, on: false, done: false, dots: [], path: [] };
        const pos = (t, uu = u, aa = accelOn ? a : 0) => {
          if (aa < 0) { const ts = -uu / aa; if (t > ts) t = ts; }
          return { d: uu * t + 0.5 * aa * t * t, v: Math.max(0, uu + aa * t) };
        };

        body.innerHTML = `
<svg class="lb-motion-svg lb-motion-tr" viewBox="0 0 360 92"></svg>
<svg class="lb-motion-svg lb-motion-g" viewBox="0 0 360 112"></svg>
<div class="lb-motion-ctl"><div class="lb-motion-sls">
<div class="lb-motion-sl"><span>Speed u</span><input type="range" class="lb-motion-u" min="${sR[0]}" max="${sR[1]}" step="${sR[2]}" value="${u}"><b class="lb-motion-uv"></b></div>
<div class="lb-motion-sl lb-motion-arow"><span>Accel. a</span><input type="range" class="lb-motion-a" min="${aR[0]}" max="${aR[1]}" step="${aR[2]}" value="${a}"><b class="lb-motion-av"></b></div>
</div><div class="lb-motion-btns"><button class="lb-motion-b go" data-go="1">▶ Go</button><button class="lb-motion-b" data-reset="1">↺ Reset</button></div></div>
<div class="lb-motion-out"></div>`;
        const tr = body.querySelector('.lb-motion-tr'), gr = body.querySelector('.lb-motion-g'), out = body.querySelector('.lb-motion-out');
        const uIn = body.querySelector('.lb-motion-u'), aIn = body.querySelector('.lb-motion-a'), goBtn = body.querySelector('[data-go]');
        const X0 = 22, X1 = 336, xOf = d => X0 + (X1 - X0) * Math.min(1, d / L);

        // static graph frame
        const G = [{ x: 34, w: 136, max: L, lab: 'd (m)', key: 'd' }, { x: 214, w: 136, max: vTop, lab: 'v (m/s)', key: 'v' }];
        const gy0 = 92, gh = 74;
        const gx = (G0, t) => G0.x + G0.w * t / T, gyv = (G0, val) => gy0 - gh * Math.min(1.05, val / G0.max);
        function drawGraphs() {
          let s = '';
          G.forEach(G0 => {
            s += `<rect x="${G0.x}" y="${gy0 - gh}" width="${G0.w}" height="${gh}" fill="#fff" rx="4"/>`;
            for (let k = 1; k <= 4; k++) s += `<line x1="${G0.x}" x2="${G0.x + G0.w}" y1="${gy0 - gh * k / 4}" y2="${gy0 - gh * k / 4}" stroke="#eceefa"/>`;
            s += `<line x1="${G0.x}" y1="${gy0}" x2="${G0.x + G0.w}" y2="${gy0}" stroke="#1b1f3a" stroke-width="1.5"/><line x1="${G0.x}" y1="${gy0}" x2="${G0.x}" y2="${gy0 - gh - 4}" stroke="#1b1f3a" stroke-width="1.5"/>`;
            s += `<text x="${G0.x - 3}" y="${gy0 - gh + 4}" text-anchor="end" font-size="9" font-weight="700" fill="#6b7090">${fmtN(G0.max)}</text><text x="${G0.x - 3}" y="${gy0 + 3}" text-anchor="end" font-size="9" font-weight="700" fill="#6b7090">0</text>`;
            s += `<text x="${G0.x + 4}" y="${gy0 - gh - 6}" font-size="10.5" font-weight="800" fill="#1b1f3a">${G0.lab}</text>`;
            s += `<text x="${G0.x + G0.w}" y="${gy0 + 13}" text-anchor="end" font-size="10" font-weight="800" fill="#6b7090">t (s) → ${fmtN(T)}</text>`;
            if (tgt) {
              let pts = [];
              for (let i = 0; i <= 40; i++) { const t = T * i / 40, q = pos(t, tgt.speed, tgt.accel); pts.push(`${gx(G0, t).toFixed(1)},${gyv(G0, q[G0.key]).toFixed(1)}`); }
              s += `<polyline points="${pts.join(' ')}" fill="none" stroke="#2ed3a5" stroke-width="3" stroke-dasharray="5 4" opacity=".9"/>`;
            }
            if (run.path.length > 1) s += `<polyline points="${run.path.map(q => `${gx(G0, q.t).toFixed(1)},${gyv(G0, q[G0.key]).toFixed(1)}`).join(' ')}" fill="none" stroke="${G0.key === 'd' ? '#8b5cf6' : '#ff6b6b'}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>`;
            if (run.path.length) { const q = run.path[run.path.length - 1]; s += `<circle cx="${gx(G0, q.t)}" cy="${gyv(G0, q[G0.key])}" r="4" fill="${G0.key === 'd' ? '#8b5cf6' : '#ff6b6b'}"/>`; }
          });
          gr.innerHTML = s;
        }
        function drawTrack(q) {
          let s = `<rect x="8" y="40" width="344" height="30" rx="8" fill="#5d6378"/><line x1="12" y1="55" x2="348" y2="55" stroke="#fff" stroke-width="2" stroke-dasharray="10 8" opacity=".7"/>`;
          for (let k = 0; k <= 5; k++) { const x = X0 + (X1 - X0) * k / 5; s += `<line x1="${x}" y1="70" x2="${x}" y2="76" stroke="#6b7090" stroke-width="1.5"/><text x="${x}" y="87" text-anchor="middle" font-size="9.5" font-weight="700" fill="#6b7090">${fmtN(L * k / 5)}${k === 5 ? ' m' : ''}</text>`; }
          s += `<path d="M${X1} 40 V18" stroke="#1b1f3a" stroke-width="2"/><path d="M${X1} 18 h14 v8 h-14z" fill="#ff6b6b"/>`;
          run.dots.forEach((d, i) => { s += `<circle cx="${xOf(d)}" cy="64" r="3.2" fill="#ffc93c" stroke="#1b1f3a" stroke-width="1"/>`; if (i) s += ''; });
          const cx = xOf(q.d);
          s += `<g transform="translate(${cx} 50)"><rect x="-17" y="-9" width="30" height="12" rx="5" fill="#3b82f6"/><path d="M-11 -9 L-7 -16 H5 L10 -9Z" fill="#7cc0ff" stroke="#3b82f6" stroke-width="2"/><circle cx="-9" cy="4" r="4.5" fill="#1b1f3a"/><circle cx="6" cy="4" r="4.5" fill="#1b1f3a"/><rect x="11" y="-7" width="4" height="4" rx="1" fill="#ffc93c"/></g>`;
          s += `<text x="12" y="16" font-size="12" font-weight="800" fill="#1b1f3a">t = ${fmt(run.t)} s</text><text x="92" y="16" font-size="12" font-weight="800" fill="#8b5cf6">d = ${fmt(q.d)} m</text><text x="182" y="16" font-size="12" font-weight="800" fill="#ff6b6b">v = ${fmt(q.v)} m/s</text>`;
          s += `<text x="326" y="32" text-anchor="end" font-size="10" font-weight="700" fill="#6b7090">● = position every 1 s${scale !== 1 ? ` · plays ${fmtN(scale)}× fast` : ''}</text>`;
          tr.innerHTML = s;
        }
        function controls() {
          body.querySelector('.lb-motion-uv').textContent = `${fmtN(u)} m/s`;
          body.querySelector('.lb-motion-av').textContent = `${fmtN(a)} m/s²`;
          body.querySelector('.lb-motion-arow').style.display = accelOn ? 'flex' : 'none';
            uIn.disabled = aIn.disabled = run.on;
          goBtn.disabled = run.on;
        }
        function summary() {
          const q = pos(run.t);
          if (!run.done) { out.textContent = accelOn ? `v = u + at · d = ut + ½at²` : `Uniform motion: d = speed × time = ${fmtN(u)} × t`; return; }
          const eq = !accelOn || a === 0;
          out.innerHTML = `${run.reached ? `Reached ${fmtN(L)} m at t = ${fmt(run.t, 2)} s.` : `In ${fmtN(T)} s: d = ${fmt(q.d)} m.`} ` +
            (eq ? '<span style="color:#14a37f">Equal gaps → uniform motion (straight d–t line).</span>' : `<span style="color:#e04848">Gaps ${a > 0 ? 'grow' : 'shrink'} → non-uniform motion (curved d–t line).</span>`);
        }
        function reset() { cancelAnimationFrame(raf); run.t = 0; run.on = false; run.done = false; run.reached = false; run.dots = []; run.path = [{ t: 0, d: 0, v: u }]; drawTrack(pos(0)); drawGraphs(); controls(); summary(); }
        function finish() {
          run.on = false; run.done = true; controls(); summary();
          const q = pos(run.t);
          if (goal === 'distance' && !run.reached && Math.abs(q.d - tnum) <= 0.5) winOnce(`Speed × time = ${fmtN(u)} m/s × ${fmtN(T)} s = ${fmt(q.d)} m`);
          else if (goal === 'time' && run.reached && Math.abs(run.t - tnum) <= 0.15) winOnce(`Speed = distance ÷ time = ${fmtN(L)} m ÷ ${fmt(run.t, 2)} s = ${fmt(L / run.t, 2)} m/s`);
          else if (goal === 'match' && tgt && Math.abs(u - tgt.speed) < 1e-6 && Math.abs((accelOn ? a : 0) - tgt.accel) < 1e-6) winOnce(`Graphs match! u = ${fmtN(u)} m/s, a = ${fmtN(accelOn ? a : 0)} m/s².`);
          else if (goal !== 'none') api.sfx('hmm');
        }
        function frame(now) {
          const dt = Math.min(0.05, (now - last) / 1000) * scale; last = now;
          let t = run.t + dt;
          let q = pos(t);
          if (q.d >= L) {
            const aa = accelOn ? a : 0;
            t = aa === 0 ? L / u : (-u + Math.sqrt(u * u + 2 * aa * L)) / aa;
            q = pos(t); run.reached = true;
          }
          if (t >= T && !run.reached) { t = T; q = pos(t); }
          for (let k = Math.floor(run.t) + 1; k <= Math.floor(t + 1e-9); k++) run.dots.push(pos(k).d);
          run.t = t; run.path.push({ t, d: q.d, v: q.v });
          drawTrack(q); drawGraphs();
          if (run.reached || t >= T - 1e-9) { finish(); return; }
          raf = requestAnimationFrame(frame);
        }
        function go() {
          if (run.on) return;
          if (u === 0 && (!accelOn || a <= 0)) { out.textContent = 'Speed is 0 — the car will not move. Increase the speed.'; api.sfx('hmm'); return; }
          reset(); run.on = true; run.dots = [0]; controls(); api.sfx('tap');
          last = performance.now(); raf = requestAnimationFrame(frame);
        }
        const onIn = e => {
          if (e.target === uIn) u = +uIn.value; else if (e.target === aIn) a = +aIn.value; else return;
          reset();
        };
        const onClick = e => {
          const b = e.target.closest('button'); if (!b) return;
          if (b.dataset.go) go();
          else if (b.dataset.reset) reset();
        };
        body.addEventListener('input', onIn); body.addEventListener('click', onClick);
        reset();
        return () => { cancelAnimationFrame(raf); body.removeEventListener('input', onIn); body.removeEventListener('click', onClick); };
      }

      // =================== PENDULUM ===================
      const lR = rng(p.lengthRange, [10, 150, 1]);
      let len = Math.min(lR[1], Math.max(lR[0], +p.length || 40));
      const N = Math.max(1, Math.round(+p.count || 10));
      const target = +p.target > 0 ? +p.target : 2;
      const period = () => 2 * Math.PI * Math.sqrt(len / 100 / g);
      const DEFCH = {
        period: `Change the length so the pendulum's time period is ${fmtN(target)} s. Time ${N} oscillations to check.`,
        measure: `Press Start and time ${N} oscillations. What is the time period?`
      };
      chEl.textContent = '🎯 Challenge: ' + (p.challenge ? String(p.challenge) : (DEFCH[goal] || DEFCH.measure));
      body.innerHTML = `
<svg class="lb-motion-svg" viewBox="0 0 360 210"></svg>
<div class="lb-motion-sl"><span>Length</span><input type="range" class="lb-motion-l" min="${lR[0]}" max="${lR[1]}" step="${lR[2]}" value="${len}"><b class="lb-motion-lv"></b></div>
<div class="lb-motion-row"><button class="lb-motion-b go" data-go="1">▶ Start</button><button class="lb-motion-b" data-reset="1">■ Stop</button></div>
<div class="lb-motion-out"></div>`;
      const sv = body.querySelector('svg'), out = body.querySelector('.lb-motion-out'), lIn = body.querySelector('.lb-motion-l'), goBtn = body.querySelector('[data-go]');
      const st = { on: false, t: 0, done: false };
      const PX = 112, PY = 16, pxPerCm = 168 / lR[1], th0 = 12 * Math.PI / 180;
      function draw() {
        const Tp = period(), lp = len * pxPerCm;
        const th = st.on || st.done ? th0 * Math.cos(2 * Math.PI * st.t / Tp) : th0;
        const bx = PX + lp * Math.sin(th), by = PY + lp * Math.cos(th);
        const osc = Math.min(N, Math.floor(st.t / Tp + 1e-9));
        let s = `<rect x="40" y="6" width="144" height="10" rx="4" fill="#9aa0c0"/>`;
        // swing guide
        const gx1 = PX + lp * Math.sin(-th0), gy1 = PY + lp * Math.cos(th0), gx2 = PX + lp * Math.sin(th0);
        s += `<path d="M${gx1} ${gy1} A${lp} ${lp} 0 0 0 ${gx2} ${gy1}" fill="none" stroke="#d3d7ef" stroke-width="2" stroke-dasharray="4 4"/>`;
        s += `<line x1="${PX}" y1="${PY}" x2="${PX}" y2="${PY + lp + 18}" stroke="#d3d7ef" stroke-width="1.5" stroke-dasharray="3 4"/>`;
        s += `<line x1="${PX}" y1="${PY}" x2="${bx}" y2="${by}" stroke="#1b1f3a" stroke-width="2"/><circle cx="${PX}" cy="${PY}" r="4" fill="#1b1f3a"/>`;
        s += `<circle cx="${bx}" cy="${by}" r="13" fill="#ff6b6b" stroke="#c23b3b" stroke-width="2"/><circle cx="${bx - 4}" cy="${by - 4}" r="4" fill="#fff" opacity=".6"/>`;
        // length marker
        s += `<line x1="${PX - 30}" y1="${PY}" x2="${PX - 30}" y2="${PY + lp}" stroke="#8b5cf6" stroke-width="2"/><line x1="${PX - 36}" y1="${PY + lp}" x2="${PX - 24}" y2="${PY + lp}" stroke="#8b5cf6" stroke-width="2"/>`;
        s += `<text x="${PX - 36}" y="${PY + lp / 2 + 4}" text-anchor="end" font-size="11.5" font-weight="800" fill="#8b5cf6">${fmtN(len)} cm</text>`;
        // stopwatch
        s += `<circle cx="282" cy="72" r="46" fill="#fff" stroke="#3b82f6" stroke-width="4"/><rect x="274" y="18" width="16" height="9" rx="3" fill="#3b82f6"/>`;
        const hand = 2 * Math.PI * (st.t % 60) / 60;
        s += `<line x1="282" y1="72" x2="${282 + 34 * Math.sin(hand)}" y2="${72 - 34 * Math.cos(hand)}" stroke="#ff6b6b" stroke-width="2.5" stroke-linecap="round"/><circle cx="282" cy="72" r="3.5" fill="#1b1f3a"/>`;
        s += `<text x="282" y="104" text-anchor="middle" font-size="14" font-weight="800" fill="#1b1f3a" style="font-variant-numeric:tabular-nums">${fmt(st.t)} s</text>`;
        s += `<text x="282" y="144" text-anchor="middle" font-size="12" font-weight="800" fill="#6b7090">Oscillations</text><text x="282" y="170" text-anchor="middle" font-size="22" font-weight="800" fill="#8b5cf6">${osc} / ${N}</text>`;
        if (g !== 9.8) s += `<text x="282" y="196" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">g = ${fmtN(g)} m/s²</text>`;
        sv.innerHTML = s;
        body.querySelector('.lb-motion-lv').textContent = `${fmtN(len)} cm`;
      }
      function info() {
        if (st.done) {
          const tot = N * period(), Tm = Math.round(tot * 10) / 10 / N;
          out.innerHTML = `${N} oscillations in ${fmt(tot)} s → T = ${fmt(tot)} ÷ ${N} = <span style="color:#8b5cf6">${fmt(Tm, 2)} s</span>${p.showFormula ? `<br><span style="color:#6b7090;font-size:12px">T = 2π√(L/g) = 2π√(${fmtN(len / 100)} ÷ ${fmtN(g)}) = ${fmt(period(), 2)} s</span>` : ''}`;
        } else if (st.on) out.textContent = 'One oscillation = from one end to the other end and back.';
        else out.textContent = 'Set the length, then press Start. Longer string → slower swing.';
      }
      function frame(now) {
        st.t += Math.min(0.05, (now - last) / 1000); last = now;
        const tot = N * period();
        if (st.t >= tot) {
          st.t = tot; st.on = false; st.done = true; draw(); info(); goBtn.disabled = false; lIn.disabled = false;
          const Tm = Math.round(tot * 10) / 10 / N;
          if (goal === 'period') { if (Math.abs(Tm - target) <= 0.03) winOnce(`T = ${fmt(Tm, 2)} s with a ${fmtN(len)} cm string. Longer string → longer period.`); else api.sfx('hmm'); }
          else if (goal === 'measure') winOnce(`${N} oscillations took ${fmt(tot)} s, so T = ${fmt(Tm, 2)} s.`);
          return;
        }
        draw(); raf = requestAnimationFrame(frame);
      }
      function stop() { cancelAnimationFrame(raf); st.on = false; st.done = false; st.t = 0; goBtn.disabled = false; lIn.disabled = false; draw(); info(); }
      const onClick = e => {
        const b = e.target.closest('button'); if (!b) return;
        if (b.dataset.go && !st.on) { stop(); st.on = true; goBtn.disabled = true; lIn.disabled = true; api.sfx('tap'); info(); last = performance.now(); raf = requestAnimationFrame(frame); }
        else if (b.dataset.reset) stop();
      };
      const onIn = () => { len = +lIn.value; stop(); };
      body.addEventListener('click', onClick); lIn.addEventListener('input', onIn);
      stop();
      return () => { cancelAnimationFrame(raf); body.removeEventListener('click', onClick); lIn.removeEventListener('input', onIn); };
    },
    example: {
      mode: 'track',
      motion: 'uniform',
      speed: 4, speedRange: [0, 15, 0.5],
      duration: 10, trackLength: 150,
      goal: 'distance', target: 60,
      object: 'Car',
      challenge: 'Set the speed so the car covers 60 m in 10 s.'
    },
    examples: [
      { mode: 'track', motion: 'both', speed: 1, accel: 0, accelRange: [-1, 2, 0.5], goal: 'match', target: { speed: 3, accel: 1 }, challenge: 'Grade 9: Make your d–t and v–t graphs match the dashed ones (u = ?, a = ?).' },
      { mode: 'pendulum', length: 40, lengthRange: [10, 150, 1], count: 10, goal: 'period', target: 2, challenge: 'Grade 7: Make a pendulum whose time period is 2 s. Time 10 oscillations.' }
    ]
  });
})();
