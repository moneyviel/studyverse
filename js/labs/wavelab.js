/* StudyVerse Concept Lab: wavelab — oscillations and waves (Class 11 Physics ch. 13–14, NCERT notation).
 *
 * mode 'shm'        : a block on a spring, x(t) = A cos(ωt + φ). Slide A, ω and φ; the block, the scrolling
 *                     x–t, v–t, a–t graphs and the KE / PE / E bars all stay in sync. v = −ωA sin(ωt + φ),
 *                     a = −ω²x, k = mω², E = ½ m ω² A².
 * mode 'travelling' : y(x, t) = A sin(kx − ωt) on a long string. Slide A, λ and f (or tension T and mass per
 *                     length μ, v = √(T/μ)); a marked particle only moves up and down while the crest (and
 *                     energy) travels at v = fλ = ω/k. Direction and slow-motion buttons.
 * mode 'standing'   : tune a vibrator's frequency f for a string fixed at both ends, or a speaker at an air
 *                     column (pipe open at both ends / closed at one end). At a natural frequency the amplitude
 *                     builds up (resonance): string / open pipe fₙ = n v / 2L, closed pipe f = (2n − 1) v / 4L
 *                     (odd harmonics only). Nodes N and antinodes A are marked; air-column particles move along
 *                     the pipe (longitudinal). Motion is shown slowed down.
 * mode 'beats'      : two sources f₁ and f₂; the resultant's loudness rises and falls |f₁ − f₂| times a second.
 *                     The zoom window shows the two waves drifting in and out of step. 🔊 plays them.
 *
 * PARAMS (all optional)
 *   mode         'shm' | 'travelling' | 'standing' | 'beats'                                     default 'shm'
 *   — shm —
 *   A, omega, phi  start values: amplitude (cm), angular frequency (rad/s), phase (degrees)     default 4, 2, 0
 *   ARange, omegaRange  [min,max,step] sliders                                  default [1,8,0.5], [0.5,6,0.5]
 *   mass         number kg (for k and energies)                                                default 0.5
 *   — travelling —
 *   A, lambda, f   start values: amplitude (cm), wavelength (m), frequency (Hz)                 default 3, 1, 2
 *   lambdaRange, fRange  [min,max,step]                                          default [0.25,2,0.25], [0.5,5,0.5] (with T, μ: [2,20,1])
 *   T, mu        if both given: tension (N) and μ (kg/m) sliders replace λ (λ = v / f)
 *   TRange, muRange      [min,max,step]                                          default [10,160,10], [0.01,0.1,0.01]
 *   dir          1 (towards +x) | −1                                                             default 1
 *   L            length of string shown, m                                          default 4 (with T, μ: 20)
 *   — standing —
 *   medium       'string' | 'open' | 'closed'                                                     default 'string'
 *   L            length in m                                              default 1 (string) / 0.5 (pipes)
 *   v            wave speed m/s                                           default 100 (string) / 340 (pipes)
 *   T, mu        string: v = √(T/μ) instead of v
 *   control      'f' (tune a slider) | 'n' (tap a harmonic)                                       default 'f'
 *   f            starting frequency (Hz)                                                          default 0.6 f₁
 *   — beats —
 *   f1, f2       start frequencies (Hz)                                                           default 256, 250
 *   fRange       [min,max] for both sliders (step 1 Hz)                                           default [240,272]
 *   lock1        boolean: f₁ fixed (a standard tuning fork)                                       default true
 * Challenge (one target; if none is given a sensible one is generated):
 *   target       shm:        {A, omega, phi} match the dashed x–t graph | {vmax} cm/s | {amax} cm/s² | {T} s
 *                travelling: {v} m/s | {lambda} m | {k} rad/m
 *                standing:   {harmonic:n} (closed pipe: odd n) | {f} Hz resonance at that frequency
 *                beats:      {beat} beats per second | {beat:0} tune until the beats vanish
 *   challenge    string  challenge sentence (may be Hindi); else generated
 *   winText      string  optional win message
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const minus = s => String(s).replace(/-/g, '−');
  const fmt = (v, dp = 2) => { if (!isFinite(v)) return '—'; let s = (+(+v).toFixed(dp)).toString(); if (s === '-0') s = '0'; return minus(s); };
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const rad = d => d * Math.PI / 180;
  const rng = (r, d) => Array.isArray(r) && r.length >= 2 && isFinite(+r[0]) && isFinite(+r[1]) && +r[0] < +r[1] ? [+r[0], +r[1], r[2] > 0 ? +r[2] : d[2]] : d;
  const ORD = n => n + (n % 10 === 1 && n % 100 !== 11 ? 'st' : n % 10 === 2 && n % 100 !== 12 ? 'nd' : n % 10 === 3 && n % 100 !== 13 ? 'rd' : 'th');
  function phiText(d) { // degrees → multiple of π
    const m = { 0: '0', 30: 'π/6', 45: 'π/4', 60: 'π/3', 90: 'π/2', 120: '2π/3', 135: '3π/4', 150: '5π/6', 180: 'π' };
    const a = Math.abs(d); return m[a] != null ? (d < 0 && a ? '−' : '') + m[a] : fmt(rad(d), 2);
  }
  const W = 360;

  Labs.register('wavelab', {
    title: 'Wave lab',
    subjects: ['physics'],
    render(host, p, api) {
      const mode = ['shm', 'travelling', 'standing', 'beats'].includes(p.mode) ? p.mode : 'shm';
      let won = false, touched = false, raf = 0, customRound = false, audio = null;
      const listeners = [];
      const on = (el, ev, fn) => { el.addEventListener(ev, fn); listeners.push([el, ev, fn]); };
      const stopAudio = () => { if (audio) { try { audio.ctx.close(); } catch (e) {} audio = null; } };
      const cleanup = () => { cancelAnimationFrame(raf); stopAudio(); listeners.forEach(([el, ev, fn]) => el.removeEventListener(ev, fn)); };
      const css = `
.lb-wavelab-w{font-size:13.5px;color:#1b1f3a}
.lb-wavelab-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.3}
.lb-wavelab-svg{width:100%;height:auto;display:block;background:#fbfbff;border:1.5px solid #e6e8f7;border-radius:16px;user-select:none;-webkit-user-select:none;box-sizing:border-box}
.lb-wavelab-chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}
.lb-wavelab-chip{flex:1 1 auto;border-radius:10px;padding:3px 6px;font-weight:800;font-size:12.5px;text-align:center;background:#f1f2fb;white-space:nowrap}
.lb-wavelab-chip b{font-size:13.5px}
.lb-wavelab-row{display:flex;gap:5px;margin-top:5px;align-items:center}
.lb-wavelab-b{flex:1;min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 6px;white-space:nowrap}
.lb-wavelab-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-wavelab-b.go{background:#2ed3a5;color:#08372a;box-shadow:0 3px 0 #1ea383}
.lb-wavelab-b:active{transform:translateY(2px)}
.lb-wavelab-sl{display:flex;align-items:center;gap:7px;font-weight:800;font-size:13px}
.lb-wavelab-sl span{min-width:92px;white-space:nowrap}
.lb-wavelab-sl input{flex:1;min-width:0;-webkit-appearance:none;appearance:none;height:32px;background:transparent;cursor:pointer}
.lb-wavelab-sl input::-webkit-slider-runnable-track{height:8px;border-radius:8px;background:#e3e6f6}
.lb-wavelab-sl input::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;border-radius:50%;background:#8b5cf6;margin-top:-9px;border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3)}
.lb-wavelab-sl input::-moz-range-track{height:8px;border-radius:8px;background:#e3e6f6}
.lb-wavelab-sl input::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:#8b5cf6;border:3px solid #fff}
.lb-wavelab-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:4px;min-height:16px;text-align:center;line-height:1.3}`;
      function shell(H, controls) {
        host.innerHTML = `<style>${css}</style><div class="lb-wavelab-w"><div class="lb-wavelab-ch">🎯 Challenge: <span class="lb-wavelab-cht"></span></div><svg class="lb-wavelab-svg" viewBox="0 0 ${W} ${H}"><g class="lb-wavelab-bg"></g><g class="lb-wavelab-dyn"></g></svg>${controls}<div class="lb-wavelab-msg"></div></div>`;
      }
      const $ = s => host.querySelector(s);
      const setCh = t => { $('.lb-wavelab-cht').textContent = t; };
      const msg = t => { $('.lb-wavelab-msg').innerHTML = t; };
      const out = (k, v) => { const el = host.querySelector(`[data-o="${k}"]`); if (el) el.innerHTML = v; };
      function win(t) { if (won) return; won = true; api.sfx('correct'); api.win(p.winText && !customRound ? p.winText : t); }
      const slider = (key, label, r, val) => `<label class="lb-wavelab-sl"><span>${label} <b data-o="${key}"></b></span><input type="range" data-k="${key}" min="${r[0]}" max="${r[1]}" step="${r[2]}" value="${val}"></label>`;
      const txt = (x, y, t, col, size = 11, anchor = 'middle') => `<text x="${x}" y="${y}" font-size="${size}" font-weight="900" fill="${col}" text-anchor="${anchor}" paint-order="stroke" stroke="#fbfbff" stroke-width="3" stroke-linejoin="round">${t}</text>`;
      const snapR = (v, r) => clamp(Math.round((v - r[0]) / r[2]) * r[2] + r[0], r[0], r[1]);
      const eq = (a, b) => Math.abs(a - b) < 1e-9;
      function loop(fn) { let last = performance.now(); const f = now => { const dt = Math.min(0.05, (now - last) / 1000); last = now; fn(dt, now); raf = requestAnimationFrame(f); }; raf = requestAnimationFrame(f); }
      function onSliders(fn) { on(host, 'input', e => { const k = e.target.dataset && e.target.dataset.k; if (!k) return; touched = true; fn(k, +e.target.value); }); }

      if (mode === 'travelling') return travelling();
      if (mode === 'standing') return standing();
      if (mode === 'beats') return beats();
      return shm();

      // ================= SHM =================
      function shm() {
        const H = 236, Ar = rng(p.ARange, [1, 8, 0.5]), wr = rng(p.omegaRange, [0.5, 6, 0.5]), m = +p.mass > 0 ? +p.mass : 0.5;
        let A = snapR(isFinite(+p.A) ? +p.A : 4, Ar), w = snapR(isFinite(+p.omega) ? +p.omega : 2, wr), ph = clamp(Math.round((isFinite(+p.phi) ? +p.phi : 0) / 15) * 15, -180, 180);
        const tg = p.target || {};
        let target = isFinite(+tg.A) && isFinite(+tg.omega) ? { A: snapR(+tg.A, Ar), omega: snapR(+tg.omega, wr), phi: clamp(Math.round((+tg.phi || 0) / 15) * 15, -180, 180) } : isFinite(+tg.vmax) ? { vmax: +tg.vmax } : isFinite(+tg.amax) ? { amax: +tg.amax } : isFinite(+tg.T) ? { T: +tg.T } : { A: 6, omega: 3, phi: 90 };
        if (target.A != null && eq(target.A, A) && eq(target.omega, w) && target.phi === ph) A = snapR(A === Ar[0] ? A + 2 : A - 1, Ar);
        const genText = () => target.A != null ? 'Match the dashed x–t graph: find A, ω and φ.' : target.vmax != null ? `Make the maximum speed v_max = Aω = ${fmt(target.vmax)} cm/s.` : target.amax != null ? `Make the maximum acceleration a_max = Aω² = ${fmt(target.amax)} cm/s².` : `Make the period T = 2π/ω equal to ${fmt(target.T)} s.`;
        let t = 0, playing = true;
        shell(H, `<div class="lb-wavelab-chips"><div class="lb-wavelab-chip" style="background:#e0ecff;color:#2f6fd6">T = 2π/ω = <b data-o="T"></b></div><div class="lb-wavelab-chip" style="background:#f3edff;color:#5b33c9">k = mω² = <b data-o="k"></b></div><div class="lb-wavelab-chip" style="background:#d9f7ee;color:#0f7a5c">E = <b data-o="E"></b></div></div>
<div class="lb-wavelab-row" style="gap:8px;margin-top:2px"><div style="flex:1">${slider('A', 'A =', Ar, A)}${slider('w', 'ω =', wr, w)}${slider('ph', 'φ =', [-180, 180, 15], ph)}</div><button class="lb-wavelab-b" data-a="play" style="flex:0 0 58px;min-height:88px;font-size:20px">⏸</button></div>`);
        setCh(p.challenge || genText());
        const dyn = $('.lb-wavelab-dyn');
        const PL = 30, PR = 354, WIN = 8; // graph x-range px, seconds shown
        const strips = [{ y: 92, k: 'x', col: '#8b5cf6' }, { y: 152, k: 'v', col: '#3b82f6' }, { y: 210, k: 'a', col: '#ff6b6b' }];
        let bg = `<line x1="0" y1="62" x2="${W}" y2="62" stroke="#e6e8f7" stroke-width="1.5"/><rect x="8" y="10" width="7" height="44" fill="#c7cbe3" rx="2"/><line x1="0" y1="54" x2="250" y2="54" stroke="#c7cbe3" stroke-width="2"/>`;
        strips.forEach(s => { bg += `<line x1="${PL}" y1="${s.y}" x2="${PR}" y2="${s.y}" stroke="#d6d9ee"/><line x1="${PL}" y1="${s.y - 25}" x2="${PL}" y2="${s.y + 25}" stroke="#d6d9ee"/>` + txt(14, s.y + 4, s.k, s.col, 14); });
        bg += txt(PR, H - 2, 't →', '#8a8fae', 9.5, 'end');
        $('.lb-wavelab-bg').innerHTML = bg;
        const EQX = 140, SX = 100 / Ar[1]; // px per cm for the block
        function curve(fn, y0, sc, tEnd, dash, col, wdt) {
          let d = '';
          for (let i = 0; i <= 160; i++) { const tt = tEnd - WIN + WIN * i / 160, px = PL + (PR - PL) * i / 160; d += (i ? 'L' : 'M') + px.toFixed(1) + ' ' + (y0 - fn(tt) * sc).toFixed(1); }
          return `<path d="${d}" fill="none" stroke="${col}" stroke-width="${wdt}" ${dash ? 'stroke-dasharray="5 4"' : ''} stroke-linecap="round"/>`;
        }
        function draw() {
          const P = rad(ph), x = A * Math.cos(w * t + P), v = -w * A * Math.sin(w * t + P), a = -w * w * x;
          let g = '';
          // spring + block
          const bx = EQX + x * SX - 18, coils = 12, sx0 = 15, sx1 = bx; let sp = `M${sx0} 32`;
          for (let i = 1; i <= coils * 2; i++) sp += `L${sx0 + (sx1 - sx0) * i / (coils * 2 + 1)} ${32 + (i % 2 ? -8 : 8)}`;
          sp += `L${sx1} 32`;
          g += `<line x1="${EQX}" y1="6" x2="${EQX}" y2="58" stroke="#8a8fae" stroke-dasharray="3 3"/><line x1="${EQX - A * SX}" y1="10" x2="${EQX - A * SX}" y2="56" stroke="#ffc93c" stroke-width="1.5"/><line x1="${EQX + A * SX}" y1="10" x2="${EQX + A * SX}" y2="56" stroke="#ffc93c" stroke-width="1.5"/>`;
          g += txt(EQX, 8, 'x = 0', '#8a8fae', 9) + txt(EQX + A * SX, 8, '+A', '#b8860b', 9) + txt(EQX - A * SX, 8, '−A', '#b8860b', 9);
          g += `<path d="${sp}" fill="none" stroke="#6b7090" stroke-width="2.2" stroke-linejoin="round"/><rect x="${bx}" y="17" width="36" height="34" rx="7" fill="#8b5cf6" stroke="#5b33c9" stroke-width="2"/><text x="${bx + 18}" y="38" font-size="10.5" font-weight="900" fill="#fff" text-anchor="middle">${fmt(m, 2)} kg</text>`;
          // energy bars
          const E = 0.5 * m * w * w * A * A / 1e4, KE = 0.5 * m * v * v / 1e4, PE = 0.5 * m * w * w * x * x / 1e4; // J (cm → m)
          [[KE, 'KE', '#2ed3a5'], [PE, 'PE', '#ffc93c'], [E, 'E', '#8b5cf6']].forEach(([val, lb, col], i) => { const bx2 = 270 + i * 30, h = E > 0 ? 34 * val / E : 0; g += `<rect x="${bx2}" y="6" width="20" height="34" rx="4" fill="#eef0fb"/><rect x="${bx2}" y="${40 - h}" width="20" height="${h}" rx="4" fill="${col}"/>` + txt(bx2 + 10, 52, lb, '#1b1f3a', 9.5); });
          // graphs
          const At = target.A != null ? target.A : 0, wt = target.omega || 0;
          const sx = 22 / Math.max(A, At), sv = 22 / Math.max(A * w, At * wt), sa = 22 / Math.max(A * w * w, At * wt * wt);
          if (target.A != null) g += curve(tt => At * Math.cos(wt * tt + rad(target.phi)), strips[0].y, sx, t, true, '#ff6b6b', 2);
          g += curve(tt => A * Math.cos(w * tt + P), strips[0].y, sx, t, false, '#8b5cf6', 2.6);
          g += curve(tt => -w * A * Math.sin(w * tt + P), strips[1].y, sv, t, false, '#3b82f6', 2.6);
          g += curve(tt => -w * w * A * Math.cos(w * tt + P), strips[2].y, sa, t, false, '#ff6b6b', 2.6);
          [[x, sx, 0], [v, sv, 1], [a, sa, 2]].forEach(([val, sc, i]) => { g += `<circle cx="${PR}" cy="${strips[i].y - val * sc}" r="4.5" fill="${strips[i].col}" stroke="#fff" stroke-width="2"/>`; });
          g += txt(PR - 4, strips[0].y - 27, `x = A cos(ωt + φ), A = ${fmt(A, 1)} cm`, '#5b33c9', 10, 'end');
          g += txt(PR - 4, strips[1].y - 27, `v = −ωA sin(ωt + φ), v_max = Aω = ${fmt(A * w, 1)} cm/s`, '#2f6fd6', 10, 'end');
          g += txt(PR - 4, strips[2].y - 27 + 4, `a = −ω²x, a_max = Aω² = ${fmt(A * w * w, 1)} cm/s²`, '#d64545', 10, 'end');
          if (target.A != null) g += txt(PL + 4, strips[0].y + 24, 'dashed = target', '#d64545', 9.5, 'start');
          dyn.innerHTML = g;
          out('A', fmt(A, 1) + ' cm'); out('w', fmt(w, 1) + ' rad/s'); out('ph', phiText(ph));
          out('T', fmt(2 * Math.PI / w) + ' s'); out('k', fmt(m * w * w) + ' N/m'); out('E', fmt(E * 1000, 2) + ' mJ');
        }
        function check() {
          if (!touched || won) return;
          let ok = false, why = '';
          if (target.A != null) { ok = eq(A, target.A) && eq(w, target.omega) && (ph === target.phi || Math.abs(ph - target.phi) === 360); why = `x = ${fmt(A, 1)} cos(${fmt(w, 1)}t + ${phiText(ph)}) cm — A = ${fmt(A, 1)} cm, ω = ${fmt(w, 1)} rad/s (T = ${fmt(2 * Math.PI / w)} s), φ = ${phiText(ph)}`; }
          else if (target.vmax != null) { ok = Math.abs(A * w - target.vmax) < 1e-9; why = `v_max = Aω = ${fmt(A, 1)} × ${fmt(w, 1)} = ${fmt(A * w)} cm/s`; }
          else if (target.amax != null) { ok = Math.abs(A * w * w - target.amax) < 1e-9; why = `a_max = Aω² = ${fmt(A, 1)} × ${fmt(w * w)} = ${fmt(A * w * w)} cm/s²`; }
          else { ok = Math.abs(2 * Math.PI / w - target.T) <= 0.005 * target.T; why = `T = 2π/ω = 2π/${fmt(w, 1)} = ${fmt(2 * Math.PI / w)} s`; }
          if (ok) { msg('✔ ' + why); win(why); } else if (target.A != null) { const bits = [eq(A, target.A) ? 'A ✔' : 'A ✗', eq(w, target.omega) ? 'ω ✔' : 'ω ✗', ph === target.phi ? 'φ ✔' : 'φ ✗']; msg(bits.join(' · ')); }
        }
        onSliders((k, val) => { if (k === 'A') A = val; else if (k === 'w') w = val; else ph = val; check(); if (!playing) draw(); });
        on(host, 'click', e => { const b = e.target.closest('[data-a="play"]'); if (!b) return; playing = !playing; b.textContent = playing ? '⏸' : '▶'; api.sfx('tap'); });
        loop(dt => { if (playing) { t += dt; draw(); } });
        draw(); msg(target.A != null ? 'Slide A, ω and φ until the solid curve sits on the dashed one' : 'Slide A, ω and φ');
        return cleanup;
      }

      // ================= travelling =================
      function travelling() {
        const H = 176, useT = isFinite(+p.T) && isFinite(+p.mu) && +p.T > 0 && +p.mu > 0;
        const Ar = rng(p.ARange, [1, 6, 0.5]), lr = rng(p.lambdaRange, [0.25, 2, 0.25]), fr = rng(p.fRange, useT ? [2, 20, 1] : [0.5, 5, 0.5]), Tr = rng(p.TRange, [10, 160, 10]), mr = rng(p.muRange, [0.01, 0.1, 0.01]);
        let A = snapR(isFinite(+p.A) ? +p.A : 3, Ar), lam = snapR(isFinite(+p.lambda) ? +p.lambda : 1, lr), f = snapR(isFinite(+p.f) ? +p.f : 2, fr);
        let Ten = useT ? snapR(+p.T, Tr) : 0, mu = useT ? snapR(+p.mu, mr) : 0, dir = +p.dir === -1 ? -1 : 1, slow = false;
        const L = +p.L > 0 ? +p.L : (useT ? 20 : 4);
        const vel = () => useT ? Math.sqrt(Ten / mu) : f * lam;
        const lamNow = () => useT ? vel() / f : lam;
        const tg = p.target || {};
        let target = isFinite(+tg.v) ? { v: +tg.v } : isFinite(+tg.lambda) ? { lambda: +tg.lambda } : isFinite(+tg.k) ? { k: +tg.k } : { v: useT ? 40 : 3 };
        const genText = () => target.v != null ? `Make the wave travel at v = ${fmt(target.v)} m/s.` : target.lambda != null ? `Make the wavelength λ = ${fmt(target.lambda)} m.` : `Make the wave number k = 2π/λ = ${fmt(target.k)} rad/m.`;
        shell(H, `<div class="lb-wavelab-chips"><div class="lb-wavelab-chip" style="background:#f3edff;color:#5b33c9">k = 2π/λ = <b data-o="k"></b></div><div class="lb-wavelab-chip" style="background:#e0ecff;color:#2f6fd6">ω = 2πf = <b data-o="om"></b></div><div class="lb-wavelab-chip" style="background:#d9f7ee;color:#0f7a5c">v = <b data-o="v"></b></div></div>
<div style="margin-top:2px">${useT ? slider('f', 'f =', fr, f) + slider('T', 'T =', Tr, Ten) + slider('mu', 'μ =', mr, mu) : slider('A', 'A =', Ar, A) + slider('lam', 'λ =', lr, lam) + slider('f', 'f =', fr, f)}</div>
<div class="lb-wavelab-row"><button class="lb-wavelab-b" data-a="dir"></button><button class="lb-wavelab-b" data-a="slow">🐢 Slow motion</button></div>`);
        setCh(p.challenge || genText());
        const dyn = $('.lb-wavelab-dyn'), X0 = 16, X1 = 344, Y0 = 92, sy = 7; // px per cm
        $('.lb-wavelab-bg').innerHTML = `<line x1="${X0}" y1="${Y0}" x2="${X1}" y2="${Y0}" stroke="#d6d9ee" stroke-dasharray="4 4"/>` + (() => { const st = L <= 5 ? 1 : L <= 10 ? 2 : L <= 25 ? 5 : 10, n = Math.floor(L / st); return Array.from({ length: n + 1 }, (_, i) => `<line x1="${X0 + (X1 - X0) * i * st / L}" y1="${H - 16}" x2="${X0 + (X1 - X0) * i * st / L}" y2="${H - 11}" stroke="#8a8fae"/>` + txt(X0 + (X1 - X0) * i * st / L, H - 2, i * st + (i === n ? ' m' : ''), '#8a8fae', 9.5)).join(''); })() + `<line x1="${X0}" y1="${H - 16}" x2="${X1}" y2="${H - 16}" stroke="#c7cbe3"/>`;
        let t = 0;
        function draw() {
          const lm = lamNow(), k = 2 * Math.PI / lm, om = 2 * Math.PI * f, v = om / k, Ap = useT ? 3 : A;
          const Y = x => Ap * Math.sin(k * x - dir * om * t);
          const P = x => X0 + (X1 - X0) * x / L;
          let d = ''; for (let i = 0; i <= 240; i++) { const x = L * i / 240; d += (i ? 'L' : 'M') + P(x).toFixed(1) + ' ' + (Y0 - Y(x) * sy).toFixed(1); }
          let g = `<path d="${d}" fill="none" stroke="#8b5cf6" stroke-width="3.2" stroke-linecap="round"/>`;
          // crest positions: k x − ω t dir = π/2 + 2πm
          const crests = []; for (let mm = -200; mm <= 200 && crests.length < 40; mm++) { const x = (Math.PI / 2 + 2 * Math.PI * mm + dir * om * t) / k; if (x >= 0 && x <= L) crests.push(x); }
          crests.sort((a, b) => a - b);
          const c0 = crests.find(x => x + lm <= L);
          if (c0 != null) { const yb = Y0 - Ap * sy - 12; g += `<path d="M${P(c0)} ${yb + 5}V${yb}H${P(c0 + lm)}V${yb + 5}" fill="none" stroke="#ffc93c" stroke-width="2.2"/>` + txt((P(c0) + P(c0 + lm)) / 2, yb - 4, `λ = ${fmt(lm)} m`, '#9a6a00', 10.5); }
          if (crests.length) { const cx = crests[Math.floor(crests.length / 2)]; g += `<path d="M${P(cx)} ${Y0 - Ap * sy - 3}l-5 -8h10z" fill="#3b82f6"/>`; }
          // marked particle at L/4
          const xp = L / 4 + lm / 8; g += `<line x1="${P(xp)}" y1="${Y0 - Ap * sy}" x2="${P(xp)}" y2="${Y0 + Ap * sy}" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="2 3"/><circle cx="${P(xp)}" cy="${Y0 - Y(xp) * sy}" r="6" fill="#ff6b6b" stroke="#fff" stroke-width="2"/>`;
          g += txt(P(xp) + 9, Y0 + Ap * sy + 13, 'particle: only up & down', '#d64545', 9.5, 'start');
          g += txt(dir > 0 ? X1 : X0, 14, dir > 0 ? `wave → v = ${fmt(v)} m/s` : `← v = ${fmt(v)} m/s`, '#2f6fd6', 11, dir > 0 ? 'end' : 'start');
          g += txt(dir > 0 ? X0 : X1, 14, `y = A sin(kx ${dir > 0 ? '−' : '+'} ωt)`, '#5b33c9', 11, dir > 0 ? 'start' : 'end');
          dyn.innerHTML = g;
          out('A', fmt(A, 1) + ' cm'); out('lam', fmt(lam) + ' m'); out('f', fmt(f, 1) + ' Hz'); out('T', fmt(Ten, 0) + ' N'); out('mu', fmt(mu, 2) + ' kg/m');
          out('k', fmt(k) + ' rad/m'); out('om', fmt(om) + ' rad/s'); out('v', useT ? `√(T/μ) = ${fmt(v)} m/s` : `fλ = ${fmt(v)} m/s`);
        }
        function check() {
          if (!touched || won) return;
          const lm = lamNow(), v = vel(), k = 2 * Math.PI / lm;
          let ok = false;
          if (target.v != null) ok = Math.abs(v - target.v) <= (useT ? 0.01 * target.v : 1e-9);
          else if (target.lambda != null) ok = Math.abs(lm - target.lambda) <= (useT ? 0.01 * target.lambda : 1e-9);
          else ok = Math.abs(k - target.k) <= 0.01 * target.k;
          if (ok) { const why = useT ? `v = √(T/μ) = √(${fmt(Ten, 0)}/${fmt(mu, 2)}) = ${fmt(v)} m/s, λ = v/f = ${fmt(lm)} m` : `v = fλ = ${fmt(f, 1)} × ${fmt(lam)} = ${fmt(v)} m/s, k = 2π/λ = ${fmt(k)} rad/m`; msg('✔ ' + why); win(why); }
        }
        onSliders((k, val) => { if (k === 'A') A = val; else if (k === 'lam') lam = val; else if (k === 'f') f = val; else if (k === 'T') Ten = val; else mu = val; check(); });
        const setDir = () => { host.querySelector('[data-a="dir"]').textContent = dir > 0 ? 'Direction: → (+x)' : 'Direction: ← (−x)'; };
        on(host, 'click', e => { const b = e.target.closest('[data-a]'); if (!b) return; api.sfx('tap'); if (b.dataset.a === 'dir') { dir = -dir; setDir(); } else { slow = !slow; b.classList.toggle('on', slow); } });
        setDir();
        loop(dt => { t += dt * (slow ? 0.2 : 1); draw(); });
        msg('Slide λ and f (watch the red particle and the blue crest)');
        return cleanup;
      }

      // ================= standing =================
      function standing() {
        const med = ['string', 'open', 'closed'].includes(p.medium) ? p.medium : 'string';
        const H = 168, L = +p.L > 0 ? +p.L : (med === 'string' ? 1 : 0.5);
        const useT = med === 'string' && +p.T > 0 && +p.mu > 0;
        const v = useT ? Math.sqrt(+p.T / +p.mu) : (+p.v > 0 ? +p.v : med === 'string' ? 100 : 340);
        const base = med === 'closed' ? v / (4 * L) : v / (2 * L); // lowest natural frequency
        const harmOf = f => med === 'closed' ? f / base : f / base; // harmonic number (closed: odd)
        const isNat = f => { const h = harmOf(f); return Math.abs(h - Math.round(h)) < 1e-6 && Math.round(h) >= 1 && (med !== 'closed' || Math.round(h) % 2 === 1); };
        const step = base / 10, fMax = base * (med === 'closed' ? 11.5 : 6.5);
        const ctl = p.control === 'n' ? 'n' : 'f';
        let f = isFinite(+p.f) && +p.f > 0 ? clamp(Math.round(+p.f / step) * step, step, fMax) : Math.round(0.6 * 10) * step;
        const tg = p.target || {};
        let target = isFinite(+tg.harmonic) && +tg.harmonic >= 1 ? { n: Math.round(+tg.harmonic) } : isFinite(+tg.f) ? { f: +tg.f } : { n: 3 };
        if (target.n && med === 'closed' && target.n % 2 === 0) target.n += 1;
        if (target.n && target.n * base > fMax) target.n = med === 'closed' ? 3 : 2;
        const what = med === 'string' ? `string (L = ${fmt(L)} m, v = ${fmt(v, 1)} m/s)` : `pipe ${med === 'open' ? 'open at both ends' : 'closed at one end'} (L = ${fmt(L)} m, v = ${fmt(v, 0)} m/s)`;
        const genText = () => target.n ? `Find the ${ORD(target.n)} harmonic of the ${what}.` : `Make the ${what} resonate at ${fmt(target.f, 1)} Hz.`;
        const fdp = Math.abs(step - Math.round(step)) < 1e-9 ? 0 : 1;
        shell(H, `<div class="lb-wavelab-chips"><div class="lb-wavelab-chip" style="background:#f3edff;color:#5b33c9">f = <b data-o="f"></b></div><div class="lb-wavelab-chip" style="background:#fff5d6;color:#9a6a00">λ = v/f = <b data-o="lam"></b></div><div class="lb-wavelab-chip" style="background:#e0ecff;color:#2f6fd6">${med === 'closed' ? 'v/4L' : 'v/2L'} = <b>${fmt(base, 1)} Hz</b></div></div>
<div class="lb-wavelab-chip" data-o="state" style="margin-top:4px;display:block;white-space:normal"></div>
${ctl === 'f' ? `<div class="lb-wavelab-row"><button class="lb-wavelab-b" data-a="m" style="flex:0 0 46px">◀</button><div style="flex:1">${slider('f', 'vibrator', [step, +fMax.toFixed(6), step], f)}</div><button class="lb-wavelab-b" data-a="p" style="flex:0 0 46px">▶</button></div>`
            : `<div class="lb-wavelab-row">${Array.from({ length: 6 }, (_, i) => med === 'closed' ? 2 * i + 1 : i + 1).map(n => `<button class="lb-wavelab-b" data-n="${n}">${med === 'closed' ? 'f×' + n : 'n=' + n}</button>`).join('')}</div>`}`);
        setCh(p.challenge || genText());
        const dyn = $('.lb-wavelab-dyn'), X0 = 34, X1 = 340, Y0 = 82, AMAX = 46, DELTA = 0.04, a0 = AMAX * DELTA;
        let bg = '';
        if (med === 'string') bg += `<rect x="${X1}" y="${Y0 - 40}" width="10" height="80" rx="3" fill="#c7cbe3"/><rect x="8" y="${Y0 - 22}" width="22" height="44" rx="6" fill="#6b7090"/>` + txt(19, Y0 + 36, 'vibrator', '#6b7090', 9);
        else {
          bg += `<rect x="${X0}" y="${Y0 - 50}" width="${X1 - X0}" height="100" fill="#eef6ff" stroke="#9cbbe6" stroke-width="2"/>`;
          if (med === 'closed') bg += `<rect x="${X1}" y="${Y0 - 54}" width="10" height="108" rx="3" fill="#6b7090"/>`;
          bg += `<path d="M${X0 - 4} ${Y0 - 16}h-12l-12 -14v60l12 -14h12z" fill="#6b7090"/>` + txt(3, Y0 + 44, 'speaker', '#6b7090', 9, 'start');
        }
        bg += txt((X0 + X1) / 2, H - 4, `L = ${fmt(L)} m · motion slowed down`, '#8a8fae', 9.5);
        $('.lb-wavelab-bg').innerHTML = bg;
        let t = 0;
        const kOf = f => 2 * Math.PI * f / v;
        function shapeAmp(f) {
          const k = kOf(f), D = med === 'closed' ? Math.cos(k * L) : Math.sin(k * L);
          const amp = a0 / Math.max(Math.abs(D), DELTA);
          const shape = med === 'open' ? (x => Math.cos(k * x)) : (x => Math.sin(k * (L - x)));
          return { amp, shape, k };
        }
        function draw() {
          const { amp, shape, k } = shapeAmp(f), ph = Math.cos(2 * Math.PI * 1.1 * t);
          const P = x => X0 + (X1 - X0) * x / L;
          const res = isNat(f), n = Math.round(harmOf(f));
          let g = '';
          if (med === 'string') {
            let d = '', e1 = '', e2 = '';
            for (let i = 0; i <= 200; i++) { const x = L * i / 200, s = shape(x); d += (i ? 'L' : 'M') + P(x).toFixed(1) + ' ' + (Y0 - amp * s * ph).toFixed(1); e1 += (i ? 'L' : 'M') + P(x).toFixed(1) + ' ' + (Y0 - amp * s).toFixed(1); e2 += (i ? 'L' : 'M') + P(x).toFixed(1) + ' ' + (Y0 + amp * s).toFixed(1); }
            g += `<path d="${e1}" fill="none" stroke="#c4b5fd" stroke-width="1.5" stroke-dasharray="3 3"/><path d="${e2}" fill="none" stroke="#c4b5fd" stroke-width="1.5" stroke-dasharray="3 3"/><path d="${d}" fill="none" stroke="#8b5cf6" stroke-width="3.2" stroke-linecap="round"/>`;
          } else {
                        for (let i = 0; i <= 44; i++) for (let j = 0; j < 5; j++) { const x0 = L * (i + 0.5) / 45, s = amp * shape(x0) * ph * 0.35; const px = clamp(P(x0) + s, X0 + 2, X1 - 2); g += `<circle cx="${px.toFixed(1)}" cy="${Y0 - 36 + j * 18 + (i % 2) * 9}" r="2.4" fill="#3b82f6" opacity=".75"/>`; }
            let e1 = '', e2 = '';
            for (let i = 0; i <= 200; i++) { const x = L * i / 200, s = amp * Math.abs(shape(x)) * 0.95; e1 += (i ? 'L' : 'M') + P(x).toFixed(1) + ' ' + (Y0 - s).toFixed(1); e2 += (i ? 'L' : 'M') + P(x).toFixed(1) + ' ' + (Y0 + s).toFixed(1); }
            g += `<path d="${e1}" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="5 3"/><path d="${e2}" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="5 3"/>`;
          }
          if (res) {
            const lam = v / f;
            const nodes = [], anti = [];
            for (let i = 0; i <= 400; i++) { const x = L * i / 400; if (Math.abs(shape(x)) < 0.016) nodes.push(x); if (Math.abs(Math.abs(shape(x)) - 1) < 1.3e-4) anti.push(x); }
            const dedup = arr => arr.filter((x, i) => i === 0 || x - arr[i - 1] > lam / 8);
            const yy = med === 'string' ? Y0 + 15 : Y0 + 63;
            dedup(nodes).forEach(x => { g += txt(P(x), yy, 'N', '#d64545', 11); if (med === 'string') g += `<circle cx="${P(x)}" cy="${Y0}" r="3.5" fill="#ff6b6b"/>`; });
            dedup(anti).forEach(x => { g += txt(P(x), med === 'string' ? Y0 - AMAX - 6 : Y0 - 56, 'A', '#0f7a5c', 11); });
          }
          dyn.innerHTML = g;
          out('f', fmt(f, fdp) + ' Hz'); out('lam', fmt(v / f) + ' m');
          const st = host.querySelector('[data-o="state"]');
          if (res) { st.style.background = '#d9f7ee'; st.style.color = '#0f7a5c'; st.innerHTML = `Resonance! ${ORD(n)} harmonic: f = ${n} × ${med === 'closed' ? 'v/4L' : 'v/2L'} = <b>${fmt(f, fdp)} Hz</b>, L = ${med === 'closed' ? `${n}λ/4` : `${n}λ/2`}`; }
          else { st.style.background = '#f1f2fb'; st.style.color = '#6b7090'; st.innerHTML = `Not a natural frequency — tiny amplitude. ${med === 'closed' ? 'Closed pipe: f = (2n − 1) v/4L, odd harmonics only' : 'Natural frequencies: fₙ = n v/2L'}`; }
          void k;
        }
        function check() {
          if (!touched || won || !isNat(f)) return;
          const n = Math.round(harmOf(f));
          const ok = target.n ? n === target.n : Math.abs(f - target.f) <= step / 2;
          if (ok) { const why = `${ORD(n)} harmonic at f = ${fmt(f, fdp)} Hz: λ = v/f = ${fmt(v / f)} m, ${med === 'closed' ? `L = ${n}λ/4 (closed end a node, open end an antinode)` : med === 'open' ? `L = ${n}λ/2 (antinodes at both open ends)` : `L = ${n}λ/2 (nodes at both fixed ends, ${n} loop${n > 1 ? 's' : ''})`}`; msg('✔ ' + why); win(why); }
          else msg(`That's the ${ORD(n)} harmonic — keep going`);
        }
        const sl = host.querySelector('input[data-k="f"]');
        onSliders((k, val) => { f = clean(val); check(); });
        on(host, 'click', e => {
          const b = e.target.closest('[data-a],[data-n]'); if (!b) return; touched = true; api.sfx('tap');
          if (b.dataset.n) { f = +b.dataset.n * base; host.querySelectorAll('[data-n]').forEach(x => x.classList.toggle('on', x === b)); }
          else { f = clamp(Math.round(f / step) * step + (b.dataset.a === 'p' ? step : -step), step, fMax); if (sl) sl.value = f; }
          f = clean(f); check();
        });
        loop(dt => { t += dt; draw(); });
        msg(ctl === 'f' ? 'Tune the frequency: watch for a big standing wave' : 'Tap a frequency');
        return cleanup;
      }
      function clean(v) { return +(+v).toFixed(9); }

      // ================= beats =================
      function beats() {
        const H = 196, fr = rng(p.fRange, [240, 272, 1]); fr[2] = 1;
        let f1 = clamp(Math.round(isFinite(+p.f1) ? +p.f1 : 256), fr[0], fr[1]), f2 = clamp(Math.round(isFinite(+p.f2) ? +p.f2 : 250), fr[0], fr[1]);
        const lock1 = p.lock1 !== false;
        const tg = p.target || {};
        let target = isFinite(+tg.beat) ? { beat: Math.abs(Math.round(+tg.beat)) } : { beat: 3 };
        if (Math.abs(f1 - f2) === target.beat) f2 = clamp(f2 + (f2 > fr[0] + 6 ? -5 : 5), fr[0], fr[1]);
        const genText = () => target.beat === 0 ? `Tune fork B until the beats disappear (f₁ = ${f1} Hz).` : `Tune fork B so that you hear ${target.beat} beats per second (f₁ = ${f1} Hz).`;
        shell(H, `<div class="lb-wavelab-chips"><div class="lb-wavelab-chip" style="background:#f3edff;color:#5b33c9">beats = |f₁ − f₂| = <b data-o="b"></b></div><div class="lb-wavelab-chip" style="background:#e0ecff;color:#2f6fd6">beat period = <b data-o="bp"></b></div></div>
<div style="margin-top:2px">${lock1 ? `<div class="lb-wavelab-sl" style="min-height:32px"><span>fork A f₁ =</span><b>${f1} Hz</b></div>` : slider('f1', 'fork A f₁ =', fr, f1)}${slider('f2', 'fork B f₂ =', fr, f2)}</div>
<div class="lb-wavelab-row"><button class="lb-wavelab-b" data-a="m">◀ 1 Hz</button><button class="lb-wavelab-b go" data-a="snd">🔊 Listen</button><button class="lb-wavelab-b" data-a="p">1 Hz ▶</button></div>`);
        setCh(p.challenge || genText());
        const dyn = $('.lb-wavelab-dyn'), X0 = 12, X1 = 348, YS = 54, YZ = 146;
        $('.lb-wavelab-bg').innerHTML = `<line x1="${X0}" y1="${YS}" x2="${X1}" y2="${YS}" stroke="#d6d9ee"/><line x1="${X0}" y1="${YZ}" x2="${X1}" y2="${YZ}" stroke="#d6d9ee"/><line x1="0" y1="100" x2="${W}" y2="100" stroke="#e6e8f7" stroke-width="1.5"/>`;
        let t = 0;
        function draw() {
          const fb = Math.abs(f1 - f2), win1 = 1; // top: 1 s of the resultant
          const tc = t % win1;
          // top: envelope band 2A|cos(π Δf t)| and the dense carrier
          let up = '', dn = '';
          for (let i = 0; i <= 220; i++) { const tt = win1 * i / 220, e = 40 * Math.abs(Math.cos(Math.PI * fb * tt)); const x = X0 + (X1 - X0) * i / 220; up += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + (YS - e).toFixed(1); dn = 'L' + x.toFixed(1) + ' ' + (YS + e).toFixed(1) + dn; }
          let g = `<path d="${up}${dn}Z" fill="#8b5cf6" fill-opacity=".22" stroke="#8b5cf6" stroke-width="1.6"/>`;
          g += `<text x="${X0}" y="12" font-size="10.5" font-weight="900" fill="#5b33c9">y₁ + y₂ over 1 s (loudness ∝ envelope²)</text>`;
          const cx = X0 + (X1 - X0) * tc / win1; g += `<line x1="${cx}" y1="10" x2="${cx}" y2="98" stroke="#ffc93c" stroke-width="2.5"/>`;
          // zoom: 20 ms around the cursor
          const Z = 0.02; let z1 = '', z2 = '', zs = '';
          for (let i = 0; i <= 200; i++) { const tt = tc + Z * (i / 200 - 0.5), x = X0 + (X1 - X0) * i / 200, a = Math.sin(2 * Math.PI * f1 * tt), b = Math.sin(2 * Math.PI * f2 * tt); z1 += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + (YZ - a * 18).toFixed(1); z2 += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + (YZ - b * 18).toFixed(1); zs += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + (YZ - (a + b) * 18).toFixed(1); }
          g += `<path d="${zs}" fill="none" stroke="#8b5cf6" stroke-width="2.6" opacity=".9"/><path d="${z1}" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4 2"/><path d="${z2}" fill="none" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="2 2"/>`;
          const inPhase = Math.cos(Math.PI * fb * tc) ** 2;
          g += `<text x="${X0}" y="112" font-size="10.5" font-weight="900" fill="#6b7090">zoom: 20 ms at the yellow line — <tspan fill="#2f6fd6">y₁</tspan>, <tspan fill="#e04848">y₂</tspan>, <tspan fill="#5b33c9">sum</tspan></text>`;
          g += txt(X1, H - 4, inPhase > 0.8 ? 'in step → LOUD' : inPhase < 0.2 ? 'out of step → soft' : '', inPhase > 0.8 ? '#0f7a5c' : '#d64545', 11, 'end');
          dyn.innerHTML = g;
          out('f1', f1 + ' Hz'); out('f2', f2 + ' Hz'); out('b', fb + ' s⁻¹'); out('bp', fb ? fmt(1 / fb, 3) + ' s' : '∞ (no beats)');
          if (audio) { audio.o1.frequency.value = f1; audio.o2.frequency.value = f2; }
        }
        function check() {
          if (!touched || won) return;
          const fb = Math.abs(f1 - f2);
          if (fb === target.beat) { const why = target.beat === 0 ? `f₂ = f₁ = ${f1} Hz: the beats vanish (unison)` : `f₂ = ${f2} Hz: beat frequency |${f1} − ${f2}| = ${fb} per second (f₂ could also be ${2 * f1 - f2} Hz)`; msg('✔ ' + why); win(why); }
        }
        const sync = () => { host.querySelectorAll('input[data-k]').forEach(i => { i.value = i.dataset.k === 'f1' ? f1 : f2; }); };
        onSliders((k, val) => { if (k === 'f1') f1 = val; else f2 = val; check(); });
        on(host, 'click', e => {
          const b = e.target.closest('[data-a]'); if (!b) return;
          if (b.dataset.a === 'snd') {
            if (audio) { stopAudio(); b.textContent = '🔊 Listen'; return; }
            try {
              const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
              const ctx = new AC(), gN = ctx.createGain(); gN.gain.value = 0.12; gN.connect(ctx.destination);
              const o1 = ctx.createOscillator(), o2 = ctx.createOscillator(); o1.frequency.value = f1; o2.frequency.value = f2; o1.connect(gN); o2.connect(gN); o1.start(); o2.start();
              audio = { ctx, o1, o2 }; b.textContent = '🔇 Stop';
            } catch (err) { audio = null; }
            return;
          }
          touched = true; api.sfx('tap'); f2 = clamp(f2 + (b.dataset.a === 'p' ? 1 : -1), fr[0], fr[1]); sync(); check();
        });
        loop(dt => { t += dt; draw(); });
        msg('Change f₂ — watch (or listen to) the loudness rise and fall');
        return cleanup;
      }
    },
    example: { mode: 'standing', medium: 'string', L: 1, v: 100, target: { harmonic: 3 }, challenge: 'A 1 m string carries waves at 100 m/s. Tune the vibrator to get the 3rd harmonic.' },
    examples: [
      { mode: 'shm', A: 4, omega: 2, phi: 0, mass: 0.5, target: { A: 6, omega: 3, phi: 90 }, challenge: 'Match the dashed x–t graph by setting A, ω and φ.' },
      { mode: 'travelling', A: 3, lambda: 1, f: 2, L: 4, target: { v: 3 }, challenge: 'तरंग की चाल v = 3 m/s कीजिए (v = fλ)।' },
      { mode: 'beats', f1: 256, f2: 250, target: { beat: 4 }, challenge: 'A 256 Hz fork and fork B give 4 beats per second. Tune fork B to show it.' }
    ]
  });
})();
