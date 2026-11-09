/* Knowtopia Concept Lab: simplemachines — levers, pulleys, ramps and energy (Grades 5-10).
 *
 *  lever  : drag the fulcrum, the load and the effort along a beam (or tap one, then tap the beam).
 *           The beam is level only when  load × load arm = effort × effort arm ; otherwise the heavier
 *           turning side goes down. Shows the class (1, 2, 3) and MA = load ÷ effort.
 *  pulley : choose a fixed pulley, a movable pulley or a block and tackle (n supporting ropes) and pull
 *           the rope hand over hand. Effort = load ÷ n, load rises (rope pulled ÷ n), work in = work out.
 *  ramp   : drag the foot of the ramp to make it longer/steeper, then push the box up.
 *           Effort = load × h ÷ L (no friction); work in E × L = work out W × h.
 *  energy : drag a ball on a U-shaped track (or a pendulum bob) to set its height and let go. Live bars
 *           show PE = mgh, KE = ½mv² and the total, which stays constant (no friction).
 *
 * PARAMS (all optional)
 *   mode       string  'lever' | 'pulley' | 'ramp' | 'energy'                         default 'lever'
 *   load       number  load in newtons (lever, pulley, ramp)       default lever 100, pulley 200, ramp 600
 *   effort     number  lever: starting effort in N (goal 'effort': the fixed effort you have)
 *                                                                  default load ÷ 2 (lever)
 *   arms       [loadArm, effortArm]  lever: starting arm lengths in m (multiples of 0.25)   default [1, 1]
 *   leverClass number  1 | 2 | 3 — keeps the parts in that order. 0 = free (class shown live)  default 1
 *   length     number  lever: beam length in m (2-8)                                  default 4
 *                      ramp: starting ramp length in m                                default 2 × height
 *   ropes      number  pulley: starting supporting ropes (1 = fixed, 2 = movable, 3-6 = block) default 1
 *   lockRopes  boolean pulley: hide the rope buttons (keep the given set-up)          default false
 *   height     number  pulley: shelf height in m (0.5-2.5) · ramp: platform height in m (0.5-3)
 *                      energy: starting height of the ball in m                    default 1.5 / 1 / 2
 *   mass       number  energy: mass of the ball in kg                                default 1
 *   g          number  gravity in m/s² (energy, and work shown in J)                  default 9.8
 *   shape      string  energy: 'track' (U-shaped track) | 'pendulum'                  default 'track'
 *   goal       string  lever : 'balance' | 'ma' (balance with MA = target) | 'effort' (balance using
 *                              exactly `effort` N — effort is fixed, move the parts)   default 'balance'
 *                      pulley: 'height' (lift to the shelf) | 'effort' (you can pull at most `target` N)
 *                              | 'ma' (use a set-up with MA = target, then lift)      default 'height'
 *                      ramp  : 'effort' (push with at most `target` N) | 'ma' (MA = L÷h = target)
 *                              | 'height' (just push the box up)                     default 'effort'
 *                      energy: 'height' (just reach the flag at `target` m on the other side)
 *                              | 'speed' (pass the bottom at `target` m/s)           default 'height'
 *   target     number  goal value (see goal)          default lever MA 2 · pulley effort load÷2 ·
 *                                                   ramp effort load÷3 · energy 1.5 m / 5 m/s
 *   challenge  string  challenge line                                         default generated
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = (v, d = 2) => { const r = Math.round(v * 10 ** d) / 10 ** d; return (Object.is(r, -0) ? 0 : r).toString(); };
  const num = (v, d) => (v != null && v !== '' && isFinite(+v) ? +v : d);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  Labs.register('simplemachines', {
    title: 'Simple machines',
    subjects: ['science', 'physics'],
    render(host, p, api) {
      const mode = ['lever', 'pulley', 'ramp', 'energy'].includes(p.mode) ? p.mode : 'lever';
      const g = num(p.g, 9.8) > 0 ? num(p.g, 9.8) : 9.8;
      host.innerHTML = `
<style>
.lb-simplemachines-w{color:#1b1f3a;font-size:14px}
.lb-simplemachines-ch{font-weight:800;font-size:14.5px;line-height:1.35;margin-bottom:7px}
.lb-simplemachines-svg{width:100%;height:auto;display:block;background:linear-gradient(#f4f7ff,#eaf0ff);border-radius:18px;touch-action:none;user-select:none;-webkit-user-select:none}
.lb-simplemachines-svg .lb-simplemachines-h{cursor:grab}
.lb-simplemachines-rd{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:6px}
.lb-simplemachines-rd div{background:#fff;border-radius:11px;padding:4px 8px;box-shadow:0 0 0 2px #e6e8f7 inset;font-size:12.5px;font-weight:700;line-height:1.3}
.lb-simplemachines-rd b{font-weight:900}
.lb-simplemachines-rd .lb-simplemachines-wd{grid-column:1/-1}
.lb-simplemachines-rd .lb-simplemachines-eq{background:#eafff7;box-shadow:0 0 0 2px #2ed3a5 inset}
.lb-simplemachines-rd .lb-simplemachines-ne{background:#fff4f4;box-shadow:0 0 0 2px #ffc2c2 inset}
.lb-simplemachines-ct{display:flex;gap:6px;margin-top:7px;align-items:center;flex-wrap:wrap}
.lb-simplemachines-b{flex:1;min-height:42px;min-width:44px;border:none;border-radius:13px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 8px}
.lb-simplemachines-b.lb-simplemachines-go{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-simplemachines-b.lb-simplemachines-on{background:#3b82f6;color:#fff;box-shadow:0 3px 0 #2563c9}
.lb-simplemachines-b.lb-simplemachines-sm{flex:0 0 44px;font-size:20px;padding:0}
.lb-simplemachines-b:active{transform:translateY(2px);box-shadow:none}
.lb-simplemachines-b:disabled{opacity:.4}
.lb-simplemachines-lab{font-size:12px;font-weight:800;color:#6b7090;white-space:nowrap}
.lb-simplemachines-val{min-width:74px;text-align:center;font-weight:900;font-size:16px;background:#fff;border-radius:11px;padding:8px 6px;box-shadow:0 0 0 2px #e3e0fb inset}
.lb-simplemachines-msg{font-size:13px;font-weight:700;color:#6b7090;margin:6px 2px 0;min-height:18px;line-height:1.35}
.lb-simplemachines-msg.good{color:#0f9b74}.lb-simplemachines-msg.bad{color:#e04848}
.lb-simplemachines-bars{margin-top:6px;display:flex;flex-direction:column;gap:4px}
.lb-simplemachines-bar{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:800}
.lb-simplemachines-bar>span:first-child{width:62px;flex:none}
.lb-simplemachines-bar .lb-simplemachines-tr{flex:1;height:16px;background:#eef0fb;border-radius:8px;overflow:hidden}
.lb-simplemachines-bar .lb-simplemachines-fl{height:100%;border-radius:8px;transition:width .05s linear}
.lb-simplemachines-bar>span:last-child{width:58px;text-align:right;flex:none;font-variant-numeric:tabular-nums}
</style>
<div class="lb-simplemachines-w">
  <div class="lb-simplemachines-ch"></div>
  <svg class="lb-simplemachines-svg" viewBox="0 0 360 220" role="img"></svg>
  <div class="lb-simplemachines-out"></div>
  <div class="lb-simplemachines-ct"></div>
  <div class="lb-simplemachines-msg" aria-live="polite"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const svg = $('.lb-simplemachines-svg'), out = $('.lb-simplemachines-out'), ctl = $('.lb-simplemachines-ct'), msgEl = $('.lb-simplemachines-msg'), chEl = $('.lb-simplemachines-ch');
      let won = false, raf = 0, timers = [];
      const say = (t, cls = '') => { msgEl.textContent = t; msgEl.className = 'lb-simplemachines-msg ' + cls; };
      const doWin = m => { if (won) return; won = true; say('🎉 ' + m, 'good'); api.sfx('correct'); api.speak(m); api.win(m); };
      const setCh = t => { chEl.textContent = '🎯 Challenge: ' + (p.challenge || t); };
      const toSvg = e => { const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY; const m = svg.getScreenCTM(); return m ? pt.matrixTransform(m.inverse()) : { x: 0, y: 0 }; };
      let drag = null;
      const H = {}; // per-mode handlers: down(e, el, pt), move(pt), up(moved), click(e)
      function onDown(e) {
        const el = e.target.closest('[data-h]'); const hit = e.target.closest('[data-hit]');
        if ((!el && !hit) || !svg.contains(e.target) || won && mode !== 'energy') return;
        e.preventDefault();
        drag = { el, hit, id: e.pointerId, x0: e.clientX, y0: e.clientY, moved: false };
        H.down && H.down(drag, toSvg(e));
      }
      function onMove(e) {
        if (!drag || e.pointerId !== drag.id) return;
        if (!drag.moved && Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) > 5) drag.moved = true;
        if (drag.moved) { e.preventDefault(); H.move && H.move(drag, toSvg(e)); }
      }
      function onUp(e) {
        if (!drag || e.pointerId !== drag.id) return;
        const d = drag; drag = null; H.up && H.up(d, toSvg(e));
      }
      svg.addEventListener('pointerdown', onDown);
      window.addEventListener('pointermove', onMove, { passive: false });
      window.addEventListener('pointerup', onUp); window.addEventListener('pointercancel', onUp);
      const onClick = e => H.click && H.click(e);
      ctl.addEventListener('click', onClick);
      const resetWin = () => { won = false; api.resetWin && api.resetWin(); };

      // ============================================================ LEVER
      if (mode === 'lever') {
        const load = Math.max(1, num(p.load, 100));
        const cls = [0, 1, 2, 3].includes(+p.leverClass) ? +p.leverClass : 1;
        const Lb = clamp(Math.round(num(p.length, 4) * 4) / 4, 2, 8);
        const goal = ['balance', 'ma', 'effort'].includes(p.goal) ? p.goal : 'balance';
        const target = num(p.target, 2);
        const step = load >= 200 ? 10 : load >= 50 ? 5 : 1;
        const lockE = goal === 'effort';
        let E0 = Math.max(1, Math.round(num(p.effort, lockE ? load / 2 : load / 2)));
        const arms = Array.isArray(p.arms) && p.arms.length === 2 ? p.arms.map(a => clamp(Math.round(num(a, 1) * 4) / 4, .25, Lb)) : [1, 1];
        const X0 = 30, X1 = 330, s = (X1 - X0) / Lb, PY = 132, GY = 184;
        svg.setAttribute('viewBox', '0 0 360 228');
        let st;
        function init() {
          let [la, ea] = arms; let f, l, e;
          if (cls === 2) { if (ea <= la) ea = Math.min(Lb, la + 1); f = 0; l = la; e = ea; }
          else if (cls === 3) { if (la <= ea) la = Math.min(Lb, ea + 1); f = 0; e = ea; l = la; }
          else { if (la + ea > Lb) { la = Lb / 2; ea = Lb / 2; } f = Math.round((la + (Lb - la - ea) / 2) * 4) / 4; l = f - la; e = f + ea; }
          st = { f, l, e, E: E0, ang: 0, va: 0, sel: null };
          if (!lockE && balanced()) st.E += step;
        }
        const cur = () => (st.f < Math.min(st.l, st.e) || st.f > Math.max(st.l, st.e)) ? (Math.abs(st.l - st.f) < Math.abs(st.e - st.f) ? 2 : 3) : 1;
        const effortDown = () => (st.l - st.f) * (st.e - st.f) < 0;
        const net = () => load * (st.l - st.f) + (effortDown() ? 1 : -1) * st.E * (st.e - st.f); // + = clockwise (right side down)
        const balanced = () => Math.abs(net()) < 1e-6 * load * Lb;
        function targetAng() {
          const n = net(); if (balanced()) return 0;
          const fx = X0 + st.f * s, dR = X1 - fx, dL = fx - X0, h = GY - PY - 6;
          const d = n > 0 ? dR : dL; const a = d > h ? Math.asin(h / d) * 180 / Math.PI : 30;
          return (n > 0 ? 1 : -1) * Math.min(14, a);
        }
        const CL = { 1: 'Class 1: fulcrum in the middle (see-saw, scissors)', 2: 'Class 2: load in the middle (nutcracker, wheelbarrow)', 3: 'Class 3: effort in the middle (tongs, fishing rod)' };
        function draw() {
          const fx = X0 + st.f * s, lx = X0 + st.l * s, ex = X0 + st.e * s, down = effortDown();
          const la = Math.abs(st.l - st.f), ea = Math.abs(st.e - st.f);
          let ticks = '';
          for (let m = 0; m <= Lb + 1e-9; m += .5) { const x = X0 + m * s; ticks += `<line x1="${x}" x2="${x}" y1="${PY - 4}" y2="${PY + (m % 1 ? 0 : 3)}" stroke="#fff" stroke-width="1" opacity=".8"/>`; if (m % 1 === 0) ticks += `<text x="${x}" y="${PY + 15}" font-size="8" text-anchor="middle" fill="#6b7090" font-weight="700">${m}</text>`; }
          const box = Math.min(42, 30 + load / 50);
          const sel = k => st.sel === k ? `stroke="#8b5cf6" stroke-width="3"` : '';
          const ar = (x1, x2, y, c, t) => `<line x1="${x1}" x2="${x2}" y1="${y}" y2="${y}" stroke="${c}" stroke-width="2.5"/><line x1="${x1}" x2="${x1}" y1="${y - 5}" y2="${y + 5}" stroke="${c}" stroke-width="2.5"/><line x1="${x2}" x2="${x2}" y1="${y - 5}" y2="${y + 5}" stroke="${c}" stroke-width="2.5"/><text x="${(x1 + x2) / 2}" y="${y + 13}" font-size="10.5" font-weight="900" fill="${c}" text-anchor="middle">${t}</text>`;
          svg.innerHTML = `
            <rect x="0" y="${GY}" width="360" height="70" fill="#d8f3e7"/><line x1="0" x2="360" y1="${GY}" y2="${GY}" stroke="#2ed3a5" stroke-width="3"/>
            <g transform="rotate(${st.ang} ${fx} ${PY})">
              <rect data-hit="beam" x="${X0 - 8}" y="${PY - 22}" width="${X1 - X0 + 16}" height="40" fill="transparent"/>
              <rect x="${X0 - 4}" y="${PY - 5}" width="${X1 - X0 + 8}" height="10" rx="5" fill="#8b5e3c"/>${ticks}
              <g class="lb-simplemachines-h" data-h="l" transform="translate(${lx} ${PY - 5})">
                <rect x="${-box / 2}" y="${-box}" width="${box}" height="${box}" rx="5" fill="#ff6b6b" ${sel('l') || 'stroke="#c94848" stroke-width="2"'}/>
                <text y="${-box / 2 + 4}" font-size="${box > 30 ? 11 : 9.5}" font-weight="900" fill="#fff" text-anchor="middle">${fmt(load)} N</text>
                <rect x="-24" y="${-box - 8}" width="48" height="${box + 14}" fill="transparent"/>
              </g>
              <g class="lb-simplemachines-h" data-h="e" transform="translate(${ex} ${down ? PY - 5 : PY + 5})">
                ${down ? `<path d="M0 0 L-7 -12 L-2.5 -12 L-2.5 -40 L2.5 -40 L2.5 -12 L7 -12 Z" fill="#3b82f6" ${sel('e')}/><text y="-46" font-size="11" font-weight="900" fill="#1d4ed8" text-anchor="middle">${fmt(st.E)} N</text><text y="-58" font-size="15" text-anchor="middle">✋</text>`
                       : `<path d="M0 0 L-7 12 L-2.5 12 L-2.5 34 L2.5 34 L2.5 12 L7 12 Z" fill="#3b82f6" ${sel('e')}/><text x="10" y="30" font-size="11" font-weight="900" fill="#1d4ed8">${fmt(st.E)} N ↑</text>`}
                <rect x="-20" y="${down ? -66 : 0}" width="40" height="66" fill="transparent"/>
              </g>
            </g>
            <g class="lb-simplemachines-h" data-h="f"><path d="M${fx} ${PY + 5} L${fx - 15} ${GY} L${fx + 15} ${GY} Z" fill="#ffc93c" ${sel('f') || 'stroke="#d9a300" stroke-width="2"'}/><rect x="${fx - 22}" y="${PY + 5}" width="44" height="${GY - PY}" fill="transparent"/></g>
            ${ar(Math.min(fx, lx), Math.max(fx, lx), GY + 9, '#e04848', `load arm ${fmt(la)} m`)}
            ${ar(Math.min(fx, ex), Math.max(fx, ex), GY + 27, '#2563eb', `effort arm ${fmt(ea)} m`)}
            <text x="180" y="18" font-size="11" font-weight="800" fill="#0f7a5c" text-anchor="middle">${CL[cur()]}</text>`;
        }
        function readout() {
          const la = Math.abs(st.l - st.f), ea = Math.abs(st.e - st.f), tL = load * la, tE = st.E * ea, b = balanced();
          const op = b ? '=' : tL > tE ? '>' : '<';
          out.innerHTML = `<div class="lb-simplemachines-rd">
            <div class="${b ? 'lb-simplemachines-eq' : 'lb-simplemachines-ne'}">Load × arm<br><b>${fmt(load)} × ${fmt(la)} = ${fmt(tL)} N·m</b></div>
            <div class="${b ? 'lb-simplemachines-eq' : 'lb-simplemachines-ne'}">Effort × arm<br><b>${fmt(st.E)} × ${fmt(ea)} = ${fmt(tE)} N·m</b></div>
            <div class="lb-simplemachines-wd">${b ? '⚖ Balanced' : `Not balanced (${fmt(tL)} ${op} ${fmt(tE)})`} · MA = load ÷ effort = <b>${fmt(load / st.E)}</b></div></div>`;
          ctl.innerHTML = lockE ? `<span class="lb-simplemachines-lab">Your effort: ${fmt(st.E)} N (fixed)</span><button class="lb-simplemachines-b" data-a="reset">↺ Reset</button>`
            : `<span class="lb-simplemachines-lab">Effort</span><button class="lb-simplemachines-b lb-simplemachines-sm" data-a="e-">−</button><span class="lb-simplemachines-val">${fmt(st.E)} N</span><button class="lb-simplemachines-b lb-simplemachines-sm" data-a="e+">+</button><button class="lb-simplemachines-b" data-a="reset">↺</button>`;
        }
        let last = 0;
        function tick(t) {
          const dt = Math.min(.05, last ? (t - last) / 1000 : .016); last = t;
          const ta = targetAng();
          st.va += ((ta - st.ang) * 60 - st.va * 9) * dt; st.ang += st.va * dt;
          if (Math.abs(ta - st.ang) < .03 && Math.abs(st.va) < .05) { st.ang = ta; st.va = 0; draw(); raf = 0; last = 0; return; }
          draw(); raf = requestAnimationFrame(tick);
        }
        const kick = () => { if (!raf) { last = 0; raf = requestAnimationFrame(tick); } };
        function check() {
          readout(); kick();
          if (won || !balanced()) return;
          const ma = load / st.E, c = cur();
          if (goal === 'balance') doWin(`Balanced! ${fmt(load)} × ${fmt(Math.abs(st.l - st.f))} = ${fmt(st.E)} × ${fmt(Math.abs(st.e - st.f))}. MA = ${fmt(ma)}.`);
          else if (goal === 'effort') doWin(`You balanced ${fmt(load)} N with only ${fmt(st.E)} N! A longer effort arm means less effort.`);
          else if (Math.abs(ma - target) < .01) doWin(`Balanced with MA = ${fmt(ma)}. Effort arm ÷ load arm = ${fmt(Math.abs(st.e - st.f))} ÷ ${fmt(Math.abs(st.l - st.f))} = ${fmt(ma)}.`);
          else say(`Balanced, but MA = ${fmt(ma)}. Make MA = ${fmt(target)}.`);
          if (!won && c && cls && c !== cls) say(`That is a class ${c} lever now.`);
        }
        function moveTo(k, xm) {
          xm = clamp(Math.round(xm * 4) / 4, 0, Lb);
          const o = { f: st.f, l: st.l, e: st.e }; o[k] = xm;
          const gap = .25;
          const ok = cls === 0 ? (o.f !== o.l && o.f !== o.e && o.l !== o.e) :
            cls === 1 ? (o.l + gap <= o.f && o.f + gap <= o.e) :
            cls === 2 ? (o.f + gap <= o.l && o.l + gap <= o.e) : (o.f + gap <= o.e && o.e + gap <= o.l);
          if (!ok) return false;
          if (o[k] === st[k]) return true;
          st[k] = xm; check(); return true;
        }
        let dk = null;
        H.down = (d) => { if (won) return; dk = d.el ? d.el.dataset.h : null; };
        H.move = (d, pt) => { if (dk) moveTo(dk, (pt.x - X0) / s); };
        H.up = (d, pt) => {
          if (won) return;
          if (d.moved) { if (dk) api.sfx('tap'); dk = null; return; }
          if (dk) { st.sel = st.sel === dk ? null : dk; dk = null; draw(); api.sfx('tap'); say(st.sel ? `Now tap the beam where the ${{ f: 'fulcrum', l: 'load', e: 'effort' }[st.sel]} should go.` : ''); return; }
          if (d.hit && st.sel) { const k = st.sel; if (!moveTo(k, (pt.x - X0) / s)) say(cls ? `That would not be a class ${cls} lever.` : 'Parts cannot share a spot.', 'bad'); else api.sfx('tap'); st.sel = null; draw(); }
        };
        H.click = e => {
          const a = e.target.closest('[data-a]'); if (!a) return;
          if (a.dataset.a === 'reset') { resetWin(); init(); draw(); check(); say(''); return; }
          if (won) return;
          st.E = clamp(st.E + (a.dataset.a === 'e+' ? step : -step), step, load * 4); api.sfx('tap'); check(); draw();
        };
        init();
        setCh(goal === 'balance' ? `Balance the ${fmt(load)} N load. Move the parts or change the effort.` : goal === 'ma' ? `Balance the lever with a mechanical advantage of ${fmt(target)}.` : `You can only push with ${fmt(E0)} N. Move the parts to balance ${fmt(load)} N.`);
        st.ang = targetAng(); draw(); readout();
        say('Drag the fulcrum ▲, the load or the effort arrow — or tap one, then tap the beam.');
      }

      // ============================================================ PULLEY
      if (mode === 'pulley') {
        const load = Math.max(1, num(p.load, 200));
        const goal = ['height', 'effort', 'ma'].includes(p.goal) ? p.goal : 'height';
        const shelf = clamp(num(p.height, goal === 'height' && p.target != null ? num(p.target, 1.5) : 1.5), .5, 2.5);
        const target = num(p.target, goal === 'ma' ? 4 : goal === 'effort' ? load / 2 : shelf);
        const OPTS = [1, 2, 3, 4, 6];
        let n0 = clamp(Math.round(num(p.ropes, 1)), 1, 6); if (n0 === 5) n0 = 4;
        const GY = 212, PX = 40, TOPB = 54, REST = 112, MAXH = 205;
        let n = n0, lift = 0, pulled = 0, hy = REST, gy0 = 0, hy0 = 0, stuck = false;
        const eff = () => load / n;
        const tooHeavy = () => goal === 'effort' && eff() > target + 1e-9;
        function draw() {
          const ly = GY - lift * PX; // load bottom
          const LH = 34, lbH = 18;
          const loadTop = ly - LH;
          let h = `<rect x="0" y="0" width="360" height="14" fill="#94a3b8"/>${Array.from({ length: 18 }, (_, i) => `<line x1="${i * 20}" y1="14" x2="${i * 20 + 10}" y2="0" stroke="#64748b" stroke-width="2"/>`).join('')}
            <rect x="0" y="${GY}" width="360" height="10" fill="#d8f3e7"/><line x1="0" x2="360" y1="${GY}" y2="${GY}" stroke="#2ed3a5" stroke-width="3"/>
            <rect x="8" y="${GY - shelf * PX}" width="100" height="7" rx="3" fill="#8b5e3c"/><text x="22" y="${GY - shelf * PX + 18}" font-size="10" font-weight="800" fill="#8b5e3c">shelf ${fmt(shelf)} m</text>
            <line x1="14" x2="14" y1="${GY - shelf * PX + 7}" y2="${GY}" stroke="#c6a27e" stroke-width="3"/>`;
          // ruler
          for (let m = 0; m <= 2.5; m += .5) h += `<line x1="350" x2="${m % 1 ? 345 : 340}" y1="${GY - m * PX}" y2="${GY - m * PX}" stroke="#6b7090" stroke-width="1.5"/>${m % 1 ? '' : `<text x="337" y="${GY - m * PX + 3}" font-size="9" text-anchor="end" fill="#6b7090" font-weight="700">${m} m</text>`}`;
          const cx = 150;
          let freeX;
          if (n === 1) {
            const r = 15, py = 36;
            h += `<line x1="${cx}" y1="14" x2="${cx}" y2="${py}" stroke="#475569" stroke-width="3"/>
              <line x1="${cx - r}" y1="${py}" x2="${cx - r}" y2="${loadTop}" stroke="#a16207" stroke-width="2.5"/>
              <path d="M${cx - r} ${py} A ${r} ${r} 0 0 1 ${cx + r} ${py}" fill="none" stroke="#a16207" stroke-width="2.5"/>
              <circle cx="${cx}" cy="${py}" r="${r - 2}" fill="#cbd5e1" stroke="#475569" stroke-width="2.5"/><circle cx="${cx}" cy="${py}" r="3" fill="#475569"/>`;
            freeX = cx + r;
            h += `<line x1="${freeX}" y1="${py}" x2="${freeX}" y2="${hy}" stroke="#a16207" stroke-width="2.5"/>`;
            h += `<rect x="${cx - r - 22}" y="${loadTop}" width="44" height="${LH}" rx="5" fill="#ff6b6b" stroke="#c94848" stroke-width="2"/><text x="${cx - r}" y="${loadTop + 21}" font-size="11" font-weight="900" fill="#fff" text-anchor="middle">${fmt(load)} N</text>`;
          } else {
            const gap = 13, xs = Array.from({ length: n }, (_, i) => cx + (i - (n - 1) / 2) * gap);
            const bw = (n - 1) * gap + 22, lbTop = loadTop - lbH - 6;
            h += `<line x1="${cx}" y1="14" x2="${cx}" y2="30" stroke="#475569" stroke-width="3"/>`;
            xs.forEach(x => { h += `<line x1="${x}" y1="${TOPB - 10}" x2="${x}" y2="${lbTop + 9}" stroke="#a16207" stroke-width="2.2"/>`; });
            h += `<rect x="${cx - bw / 2}" y="30" width="${bw}" height="${TOPB - 30}" rx="8" fill="#cbd5e1" stroke="#475569" stroke-width="2.5"/>`;
            h += `<rect x="${cx - bw / 2}" y="${lbTop}" width="${bw}" height="${lbH}" rx="7" fill="#e2e8f0" stroke="#475569" stroke-width="2.5"/>`;
            h += `<line x1="${cx}" y1="${lbTop + lbH}" x2="${cx}" y2="${loadTop}" stroke="#475569" stroke-width="3"/>`;
            freeX = cx + bw / 2 + 12;
            h += `<path d="M${xs[n - 1]} ${TOPB - 10} Q ${freeX} ${TOPB - 18} ${freeX} ${TOPB}" fill="none" stroke="#a16207" stroke-width="2.2"/><line x1="${freeX}" y1="${TOPB}" x2="${freeX}" y2="${hy}" stroke="#a16207" stroke-width="2.5"/>`;
            h += `<rect x="${cx - 26}" y="${loadTop}" width="52" height="${LH}" rx="5" fill="#ff6b6b" stroke="#c94848" stroke-width="2"/><text x="${cx}" y="${loadTop + 21}" font-size="11" font-weight="900" fill="#fff" text-anchor="middle">${fmt(load)} N</text>`;
            h += `<text x="${cx - bw / 2 - 6}" y="${(TOPB + lbTop) / 2 + 4}" font-size="11" font-weight="900" fill="#a16207" text-anchor="end">${n} ropes</text>`;
          }
          h += `<g class="lb-simplemachines-h" data-h="rope"><rect x="${freeX - 24}" y="${hy - 6}" width="48" height="40" fill="transparent"/><rect x="${freeX - 11}" y="${hy}" width="22" height="10" rx="5" fill="#3b82f6"/><text x="${freeX}" y="${hy + 29}" font-size="18" text-anchor="middle">✊</text>
            <text x="${freeX + 15}" y="${hy + 8}" font-size="10.5" font-weight="900" fill="#1d4ed8">${fmt(eff())} N ↓</text></g>`;
          if (hy === REST && !won && lift < shelf) h += `<text x="${freeX + 15}" y="${REST + 40}" font-size="9.5" font-weight="800" fill="#6b7090">pull ↓</text>`;
          svg.innerHTML = h;
        }
        function readout() {
          out.innerHTML = `<div class="lb-simplemachines-rd">
            <div>Effort = load ÷ ropes<br><b>${fmt(load)} ÷ ${n} = ${fmt(eff())} N</b></div>
            <div>Rope pulled / load lifted<br><b>${fmt(pulled)} m / ${fmt(lift)} m</b></div>
            <div class="lb-simplemachines-wd">MA = ${n} · Work in E×d = <b>${fmt(eff() * pulled)} J</b> · Work out W×h = <b>${fmt(load * lift)} J</b></div></div>`;
          ctl.innerHTML = (p.lockRopes ? '' : OPTS.map(k => `<button class="lb-simplemachines-b lb-simplemachines-sm${k === n ? ' lb-simplemachines-on' : ''}" data-n="${k}" aria-label="${k} supporting ropes" style="font-size:15px;flex-basis:40px;min-width:40px">${k}</button>`).join('')) +
            `<button class="lb-simplemachines-b lb-simplemachines-go" data-a="pull" style="white-space:nowrap">Pull ↓</button><button class="lb-simplemachines-b lb-simplemachines-sm" data-a="reset" aria-label="lower">↺</button>`;
        }
        function addPull(dm) {
          if (won || dm <= 0) return;
          if (tooHeavy()) { stuck = true; return; }
          const room = (shelf - lift) * n; dm = Math.min(dm, room);
          pulled += dm; lift = pulled / n;
          if (lift >= shelf - 1e-6) {
            lift = shelf;
            const msg = `${fmt(load)} N lifted ${fmt(shelf)} m by pulling ${fmt(pulled)} m of rope with ${fmt(eff())} N. Work in = work out = ${fmt(load * shelf)} J.`;
            if (goal === 'ma' && Math.abs(n - target) > 1e-9) say(`Lifted! But MA was ${n}. Lower it (↺) and use MA ${fmt(target)}.`, 'bad');
            else { readout(); draw(); doWin(msg); }
          }
        }
        H.down = (d, pt) => { if (won || !d.el) return; gy0 = pt.y; hy0 = hy; stuck = false; };
        H.move = (d, pt) => {
          if (won || !d.el) return;
          if (tooHeavy()) { if (!stuck) { stuck = true; api.sfx('wrong'); say(`Too heavy! You can pull only ${fmt(target)} N but need ${fmt(eff())} N. Use more ropes.`, 'bad'); } hy = REST + Math.sin(Date.now() / 30) * 2; draw(); return; }
          const ny = clamp(hy0 + (pt.y - gy0), REST, MAXH);
          if (ny > hy) addPull((ny - hy) / PX);
          hy = ny; draw(); readout();
        };
        H.up = (d) => {
          if (!d.el) return;
          if (!d.moved && !won) { say('Drag the rope handle down to pull, or press “Pull ↓” (0.5 m).'); }
          const from = hy; const t0 = performance.now();
          cancelAnimationFrame(raf);
          const back = t => { const k = Math.min(1, (t - t0) / 250); hy = from + (REST - from) * k; draw(); if (k < 1) raf = requestAnimationFrame(back); else raf = 0; };
          raf = requestAnimationFrame(back);
          if (!won && !stuck && lift < shelf && lift > 0) say(`Load at ${fmt(lift)} m. Grab the rope again and keep pulling.`);
        };
        H.click = e => {
          const b = e.target.closest('[data-n],[data-a]'); if (!b) return;
          if (b.dataset.a === 'reset' || b.dataset.n) {
            if (b.dataset.n) n = +b.dataset.n;
            resetWin(); lift = 0; pulled = 0; hy = REST; api.sfx('tap'); draw(); readout();
            say(n === 1 ? 'Fixed pulley: it only changes the direction. Effort = load.' : `${n} ropes hold the load, so each pull needs only 1/${n} of the load — but you pull ${n}× as much rope.`);
            return;
          }
          if (won) return;
          if (tooHeavy()) { api.sfx('wrong'); say(`Too heavy! You can pull only ${fmt(target)} N but need ${fmt(eff())} N. Use more ropes.`, 'bad'); return; }
          api.sfx('tap'); addPull(.5); hy = REST + 20; draw(); readout(); timers.push(setTimeout(() => { hy = REST; draw(); }, 180));
          if (!won && lift < shelf) say(`Load at ${fmt(lift)} m.`);
        };
        setCh(goal === 'height' ? `Lift the ${fmt(load)} N load up to the shelf (${fmt(shelf)} m).` : goal === 'effort' ? `You can pull with only ${fmt(target)} N. Pick a pulley set-up and lift ${fmt(load)} N to the shelf.` : `Use a pulley system with MA = ${fmt(target)} and lift the load to the shelf.`);
        draw(); readout();
        say('Pull the blue rope handle down (or press Pull). The 1-6 buttons set how many ropes hold the load.');
      }

      // ============================================================ RAMP
      if (mode === 'ramp') {
        const W = Math.max(1, num(p.load, 600));
        const h = clamp(num(p.height, 1), .5, 3);
        const goal = ['effort', 'ma', 'height'].includes(p.goal) ? p.goal : 'effort';
        const target = num(p.target, goal === 'ma' ? 3 : Math.round(W / 3));
        const Lmax = Math.max(4, Math.ceil(h * 4));
        let L = clamp(Math.round(num(p.length, 2 * h) * 4) / 4, h, Lmax), pos = 0, work = 0;
        if (goal === 'ma' && Math.abs(L / h - target) < .01) L = clamp(L + (L + 1 <= Lmax ? 1 : -1), h, Lmax);
        const GY = 196, PXR = 312;
        const sc = Math.min(270 / Math.sqrt(Lmax * Lmax - h * h), 120 / h);
        const E = () => W * h / L;
        const vy = Math.round(clamp(GY - h * sc - 56, 0, 90)); svg.setAttribute('viewBox', `0 ${vy} 360 ${222 - vy}`);
        const blocked = () => goal === 'effort' && E() > target + 1e-9;
        function draw() {
          const run = Math.sqrt(Math.max(0, L * L - h * h)), fx = PXR - run * sc, ty = GY - h * sc;
          const ang = Math.atan2(h, run), c = Math.cos(ang), s2 = Math.sin(ang);
          const bs = 32, half = Math.min(L / 2, (bs / 2 + 2) / sc), pv = half + pos * (L - 2 * half) / L;
          const bx = fx + pv * c * sc, by = GY - pv * s2 * sc;
          const deg = -ang * 180 / Math.PI;
          let gh = `<rect x="0" y="${GY}" width="360" height="24" fill="#d8f3e7"/><line x1="0" x2="360" y1="${GY}" y2="${GY}" stroke="#2ed3a5" stroke-width="3"/>
            <rect x="${PXR}" y="${ty}" width="48" height="${GY - ty}" fill="#a78bfa" stroke="#7c4dee" stroke-width="2"/><text x="${PXR + 24}" y="${ty + 15}" font-size="10" font-weight="900" fill="#fff" text-anchor="middle">h ${fmt(h)} m</text>
            <path d="M${fx} ${GY} L${PXR} ${ty} L${PXR} ${GY} Z" fill="#fde68a" stroke="#d9a300" stroke-width="2.5" stroke-linejoin="round"/>
            <text x="${(fx + PXR) / 2 - 10 * s2}" y="${(GY + ty) / 2 - 8 - 12 * c}" font-size="11" font-weight="900" fill="#a16207" text-anchor="middle" transform="rotate(${deg} ${(fx + PXR) / 2 - 10 * s2} ${(GY + ty) / 2 - 8 - 12 * c})">L = ${fmt(L)} m</text>
            ${run > .3 ? `<path d="M${fx + 26} ${GY} A 26 26 0 0 0 ${fx + 26 * c} ${GY - 26 * s2}" fill="none" stroke="#a16207" stroke-width="1.5"/><text x="${fx + 30}" y="${GY - 5}" font-size="9.5" font-weight="800" fill="#a16207">${fmt(ang * 180 / Math.PI, 0)}°</text>` : ''}
            <g class="lb-simplemachines-h" data-h="foot"><circle cx="${fx}" cy="${GY}" r="11" fill="#fff" stroke="#8b5cf6" stroke-width="3"/><path d="M${fx - 5} ${GY} l-4 0 m0 0 l3 -3 m-3 3 l3 3 M${fx + 5} ${GY} l4 0 m0 0 l-3 -3 m3 3 l-3 3" stroke="#8b5cf6" stroke-width="2" fill="none"/><rect x="${fx - 22}" y="${GY - 22}" width="44" height="44" fill="transparent"/></g>
            <g class="lb-simplemachines-h" data-h="box" transform="translate(${bx} ${by}) rotate(${deg})">
              <rect x="${-bs / 2}" y="${-bs - 1}" width="${bs}" height="${bs}" rx="4" fill="#ff6b6b" stroke="#c94848" stroke-width="2"/>
              <text x="0" y="${-bs / 2 + 3}" font-size="9.5" font-weight="900" fill="#fff" text-anchor="middle">${fmt(W)}N</text>
              <path d="M${-bs / 2 - 30} ${-bs / 2} L${-bs / 2 - 6} ${-bs / 2}" stroke="#3b82f6" stroke-width="4" stroke-linecap="round"/><path d="M${-bs / 2 - 2} ${-bs / 2} l-8 -5 l0 10 Z" fill="#3b82f6"/>
              <text x="${-bs / 2 - 18}" y="${-bs / 2 - 8}" font-size="10.5" font-weight="900" fill="#1d4ed8" text-anchor="middle">${fmt(E(), 1)} N</text>
              <rect x="${-bs / 2 - 36}" y="${-bs - 14}" width="${bs + 40}" height="${bs + 18}" fill="transparent"/>
            </g>`;
          if (pos > 0 || work > 0) gh += '';
          svg.innerHTML = gh;
        }
        function readout() {
          out.innerHTML = `<div class="lb-simplemachines-rd">
            <div>Effort = W × h ÷ L<br><b>${fmt(W)} × ${fmt(h)} ÷ ${fmt(L)} = ${fmt(E(), 1)} N</b></div>
            <div>MA = L ÷ h<br><b>${fmt(L)} ÷ ${fmt(h)} = ${fmt(L / h)}</b></div>
            <div class="lb-simplemachines-wd">Work in E×L = <b>${fmt(E() * L, 1)} J</b> · Work out W×h = <b>${fmt(W * h, 1)} J</b></div></div>`;
          ctl.innerHTML = `<span class="lb-simplemachines-lab">Ramp</span><button class="lb-simplemachines-b lb-simplemachines-sm" data-a="l-" aria-label="shorter">−</button><span class="lb-simplemachines-val">${fmt(L)} m</span><button class="lb-simplemachines-b lb-simplemachines-sm" data-a="l+" aria-label="longer">+</button><button class="lb-simplemachines-b lb-simplemachines-go" data-a="push">Push ▲</button>`;
        }
        function setL(v) { v = clamp(Math.round(v * 4) / 4, h, Lmax); if (v === L) return; L = v; pos = 0; work = 0; draw(); readout(); say(blocked() ? `Effort ${fmt(E(), 1)} N is more than your ${fmt(target)} N.` : `Effort is now ${fmt(E(), 1)} N.`); }
        function setPos(v) {
          if (won) return;
          if (blocked()) { api.sfx('wrong'); say(`Too steep! It needs ${fmt(E(), 1)} N but you can push only ${fmt(target)} N. Make the ramp longer.`, 'bad'); return; }
          v = clamp(v, 0, L); if (v > pos) work += E() * (v - pos); pos = v; draw(); readout();
          if (pos < L - 1e-6) say(`Pushed ${fmt(pos)} m of ${fmt(L)} m — work so far ${fmt(E() * pos, 1)} J.`);
          if (pos >= L - 1e-6) {
            if (goal === 'ma' && Math.abs(L / h - target) > .01) { say(`It is up, but MA = ${fmt(L / h)}. Make MA = ${fmt(target)}.`, 'bad'); return; }
            doWin(`Up! Effort ${fmt(E(), 1)} N over ${fmt(L)} m = ${fmt(E() * L, 1)} J, same as lifting ${fmt(W)} N by ${fmt(h)} m (${fmt(W * h, 1)} J).`);
          }
        }
        let k = null;
        H.down = d => { k = d.el ? d.el.dataset.h : null; };
        H.move = (d, pt) => {
          if (!k || won) return;
          if (k === 'foot') { const run = clamp((PXR - pt.x) / sc, 0, Math.sqrt(Lmax * Lmax - h * h)); setL(Math.sqrt(run * run + h * h)); }
          else {
            const run = Math.sqrt(Math.max(0, L * L - h * h)), fx = PXR - run * sc, ang = Math.atan2(h, run);
            setPos(((pt.x - fx) * Math.cos(ang) + (GY - pt.y) * Math.sin(ang)) / sc + .3);
          }
        };
        H.up = d => { if (!d.moved && k === 'box') setPos(pos + .5); k = null; };
        H.click = e => {
          const a = e.target.closest('[data-a]'); if (!a || won && a.dataset.a !== 'l-' && a.dataset.a !== 'l+') return;
          if (a.dataset.a === 'push') { api.sfx('tap'); setPos(pos + .5); return; }
          if (won) { resetWin(); }
          api.sfx('tap'); setL(L + (a.dataset.a === 'l+' ? .5 : -.5));
        };
        setCh(goal === 'effort' ? `You can push with only ${fmt(target)} N. Change the ramp, then push the ${fmt(W)} N box to the top.` : goal === 'ma' ? `Make a ramp with MA = ${fmt(target)}, then push the box up.` : `Push the ${fmt(W)} N box up the ramp.`);
        draw(); readout();
        say('Drag the purple circle to change the ramp. Drag the box (or press Push) to push it up.');
      }

      // ============================================================ ENERGY
      if (mode === 'energy') {
        const m = Math.max(.01, num(p.mass, 1));
        const pend = p.shape === 'pendulum';
        const goal = ['height', 'speed'].includes(p.goal) ? p.goal : 'height';
        const Hm = pend ? clamp(num(p.length, 2), .5, 5) : 3; // track max height or pendulum length
        const hMax = pend ? Hm * .95 : Hm * .95;
        const target = num(p.target, goal === 'speed' ? 5 : 1.5);
        let h0 = clamp(Math.round(num(p.height, 2) * 20) / 20, .05, hMax);
        if (pend && p.height == null) h0 = Math.min(h0, Hm * .5);
        const Xh = 4; // track half-width (m)
        // state: q (x for track, θ for pendulum), v (dq/dt)
        let q = 0, v = 0, running = false, last = 0, E0 = 0, peakDone = false, lastSign = 0, vb = null, side = -1, tRun = 0;
        const hOf = q => pend ? Hm * (1 - Math.cos(q)) : Hm * (q / Xh) ** 2;
        const qOf = h => pend ? -Math.acos(1 - h / Hm) : -Xh * Math.sqrt(h / Hm);
        const acc = (q, v) => {
          if (pend) return -(g / Hm) * Math.sin(q);
          const fp = 2 * Hm * q / (Xh * Xh), fpp = 2 * Hm / (Xh * Xh);
          return -(g * fp + fp * fpp * v * v) / (1 + fp * fp);
        };
        // drawing scale
        const CX = 180, BY = 186, sx = 150 / Xh, sy = 150 / Hm, ps = 150 / Hm, PY0 = 18;
        const P = q => pend ? { x: CX + Math.sin(q) * Hm * ps * .9, y: PY0 + Math.cos(q) * Hm * ps * .9 } : { x: CX + q * sx, y: BY - hOf(q) * sy };
        const hy = h => pend ? PY0 + (Hm - h) * ps * .9 : BY - h * sy; // screen y of a height
        let trackPath = '';
        if (!pend) { for (let i = 0; i <= 60; i++) { const x = -Xh + 2 * Xh * i / 60; const pt = P(x); trackPath += (i ? 'L' : 'M') + pt.x.toFixed(1) + ' ' + pt.y.toFixed(1); } }
        const groundY = pend ? hy(0) : BY;
        function draw() {
          const b = P(q), hh = hOf(q);
          let s = '';
          // height grid
          for (let k = 0; k <= Math.floor(hMax / .5) * .5 + 1e-9; k += .5) { const y = hy(k); s += `<line x1="16" x2="344" y1="${y}" y2="${y}" stroke="#d7def5" stroke-width="1" stroke-dasharray="3 4"/><text x="18" y="${y - 2}" font-size="8.5" fill="#6b7090" font-weight="700">${k} m</text>`; }
          if (goal === 'height') { const fy = hy(target), fx = pend ? CX + Math.sqrt(Math.max(0, (Hm * .9 * ps) ** 2 - (fy - PY0) ** 2)) : P(Xh * Math.sqrt(target / Hm)).x; s += `<line x1="${fx}" x2="${fx}" y1="${fy}" y2="${fy - 26}" stroke="#1b1f3a" stroke-width="2"/><path d="M${fx} ${fy - 26} l16 6 l-16 6 Z" fill="#ff6b6b"/><line x1="${fx - 30}" x2="${fx + 30}" y1="${fy}" y2="${fy}" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="4 3"/><text x="${fx + 4}" y="${fy - 30}" font-size="9.5" font-weight="900" fill="#e04848">${fmt(target)} m</text>`; }
          if (pend) s += `<rect x="${CX - 40}" y="${PY0 - 8}" width="80" height="8" fill="#94a3b8"/><line x1="${CX}" y1="${PY0}" x2="${b.x}" y2="${b.y}" stroke="#475569" stroke-width="2"/><circle cx="${CX}" cy="${PY0}" r="3.5" fill="#475569"/>`;
          else s += `<path d="${trackPath}" fill="none" stroke="#8b5cf6" stroke-width="7" stroke-linecap="round"/><path d="${trackPath}" fill="none" stroke="#c4b5fd" stroke-width="2" stroke-linecap="round"/>`;
          s += `<line x1="16" x2="344" y1="${groundY}" y2="${groundY}" stroke="#2ed3a5" stroke-width="2"/>`;
          if (!running) { const st = P(qOf(h0)); s += `<line x1="${st.x}" x2="${st.x}" y1="${st.y}" y2="${groundY}" stroke="#ffc93c" stroke-width="2" stroke-dasharray="3 3"/>`; }
          s += `<g class="lb-simplemachines-h" data-h="ball"><circle cx="${b.x}" cy="${b.y - (pend ? 0 : 10)}" r="11" fill="#ff6b6b" stroke="#c94848" stroke-width="2.5"/><circle cx="${b.x - 3}" cy="${b.y - (pend ? 3 : 13)}" r="3" fill="#fff" opacity=".7"/><circle cx="${b.x}" cy="${b.y - (pend ? 0 : 10)}" r="24" fill="transparent"/></g>
            <text x="${clamp(b.x, 34, 326)}" y="${b.y - (pend ? 18 : 28)}" font-size="10" font-weight="900" fill="#1b1f3a" text-anchor="middle">h ${fmt(hh)} m</text>`;
          svg.innerHTML = s;
        }
        function bars() {
          const hh = hOf(q), PE = m * g * hh, Et = running ? E0 : m * g * h0, KE = Math.max(0, Et - PE), sp = Math.sqrt(2 * KE / m), mx = m * g * hMax;
          const bar = (lab, val, c) => `<div class="lb-simplemachines-bar"><span>${lab}</span><div class="lb-simplemachines-tr"><div class="lb-simplemachines-fl" style="width:${clamp(val / mx * 100, 0, 100)}%;background:${c}"></div></div><span>${fmt(val, 1)} J</span></div>`;
          out.innerHTML = `<div class="lb-simplemachines-bars">${bar('PE mgh', PE, '#8b5cf6')}${bar('KE ½mv²', KE, '#2ed3a5')}${bar('Total', running ? Et : m * g * h0, '#ffc93c')}
            <div style="font-size:12px;font-weight:800;color:#6b7090;text-align:center">m = ${fmt(m)} kg · g = ${fmt(g)} m/s² · speed <b style="color:#1b1f3a">${fmt(running ? sp : 0, 2)} m/s</b>${vb != null ? ` · at bottom ${fmt(vb, 2)} m/s` : ''}</div></div>`;
        }
        function controls() {
          ctl.innerHTML = `<span class="lb-simplemachines-lab">Start</span><button class="lb-simplemachines-b lb-simplemachines-sm" data-a="h-" aria-label="lower">−</button><span class="lb-simplemachines-val">${fmt(h0)} m</span><button class="lb-simplemachines-b lb-simplemachines-sm" data-a="h+" aria-label="higher">+</button>
            <button class="lb-simplemachines-b ${running ? '' : 'lb-simplemachines-go'}" data-a="go">${running ? '■ Stop' : '▶ Let go'}</button>`;
        }
        function stop() { running = false; cancelAnimationFrame(raf); raf = 0; q = qOf(h0); v = 0; draw(); bars(); controls(); }
        function start() {
          if (running) return;
          q = qOf(h0); v = 0; E0 = m * g * h0; running = true; last = 0; vb = null; lastSign = Math.sign(q); peakDone = false; tRun = 0;
          controls(); raf = requestAnimationFrame(step);
          say(`Let go from ${fmt(h0)} m. Watch PE turn into KE and back.`);
        }
        function step(t) {
          const dt = Math.min(.04, last ? (t - last) / 1000 : .016); last = t; tRun += dt;
          const N = 12, h = dt / N;
          for (let i = 0; i < N; i++) {
            // RK4
            const k1v = acc(q, v), k1q = v;
            const k2v = acc(q + k1q * h / 2, v + k1v * h / 2), k2q = v + k1v * h / 2;
            const k3v = acc(q + k2q * h / 2, v + k2v * h / 2), k3q = v + k2v * h / 2;
            const k4v = acc(q + k3q * h, v + k3v * h), k4q = v + k3v * h;
            q += h * (k1q + 2 * k2q + 2 * k3q + k4q) / 6; v += h * (k1v + 2 * k2v + 2 * k3v + k4v) / 6;
          }
          const sg = Math.sign(q);
          if (sg && lastSign && sg !== lastSign && vb == null) {
            vb = Math.sqrt(2 * g * h0);
            if (goal === 'speed') {
              if (Math.abs(vb - target) <= .15) doWin(`${fmt(vb, 2)} m/s at the bottom! v = √(2gh) = √(2 × ${fmt(g)} × ${fmt(h0)}). All the PE became KE.`);
              else say(`${fmt(vb, 2)} m/s at the bottom — ${vb < target ? 'too slow: start higher' : 'too fast: start lower'}.`, 'bad');
            }
          }
          if (sg) lastSign = sg;
          // turning point on the far side (v changes sign while q > 0)
          if (!peakDone && q > 0 && v <= 0 && vb != null) {
            peakDone = true;
            if (goal === 'height') {
              if (Math.abs(h0 - target) <= .03) doWin(`It rose to ${fmt(h0)} m — exactly the height it started from. Total energy ${fmt(m * g * h0, 1)} J stayed the same!`);
              else say(`It rose to ${fmt(h0)} m on the other side — the same height it started from. The flag is at ${fmt(target)} m.`, h0 > target ? 'bad' : '');
            }
          }
          draw(); bars();
          if (tRun > 30) { stop(); return; }
          raf = requestAnimationFrame(step);
        }
        let dragging = false;
        H.down = d => { if (!d.el) return; if (running) stop(); dragging = true; };
        H.move = (d, pt) => {
          if (!dragging) return;
          let hh;
          if (pend) { const a = Math.atan2(pt.x - CX, pt.y - PY0); const aa = clamp(a, -Math.PI / 2, 0); hh = Hm * (1 - Math.cos(aa)); }
          else { const x = clamp((pt.x - CX) / sx, -Xh, 0); hh = hOf(x); }
          const nh = clamp(Math.round(hh * 20) / 20, .05, hMax);
          if (nh !== h0) { h0 = nh; if (won) resetWin(); q = qOf(h0); vb = null; draw(); bars(); controls(); }
        };
        H.up = d => { if (!dragging) return; dragging = false; if (d.moved) start(); };
        H.click = e => {
          const a = e.target.closest('[data-a]'); if (!a) return;
          if (a.dataset.a === 'go') { api.sfx('tap'); running ? stop() : start(); return; }
          if (running) stop();
          if (won) resetWin();
          h0 = clamp(Math.round((h0 + (a.dataset.a === 'h+' ? .05 : -.05)) * 20) / 20, .05, hMax); q = qOf(h0); vb = null; api.sfx('tap'); draw(); bars(); controls();
          say(`Start height ${fmt(h0)} m → PE = ${fmt(m)} × ${fmt(g)} × ${fmt(h0)} = ${fmt(m * g * h0, 1)} J.`);
        };
        q = qOf(h0);
        setCh(goal === 'height' ? `Let the ball go so it just reaches the flag (${fmt(target)} m) on the other side.` : `Make the ${pend ? 'bob' : 'ball'} pass the bottom at ${fmt(target)} m/s.`);
        draw(); bars(); controls();
        say(`Drag the ${pend ? 'bob' : 'ball'} up and let go (or use − + and ▶). No friction here.`);
      }

      return () => {
        cancelAnimationFrame(raf); timers.forEach(clearTimeout);
        svg.removeEventListener('pointerdown', onDown); ctl.removeEventListener('click', onClick);
        window.removeEventListener('pointermove', onMove); window.removeEventListener('pointerup', onUp); window.removeEventListener('pointercancel', onUp);
      };
    },
    example: { mode: 'lever', load: 100, effort: 50, arms: [1.5, 1.5], leverClass: 1, length: 4, goal: 'balance', challenge: 'Balance the 100 N rock using only 50 N of effort. Slide the fulcrum!' },
    examples: [
      { mode: 'pulley', load: 400, ropes: 1, goal: 'effort', target: 100, height: 1.5, challenge: 'You can pull only 100 N. Choose a pulley system and lift the 400 N load to the shelf.' },
      { mode: 'ramp', load: 600, height: 1, length: 1.5, goal: 'effort', target: 200, challenge: 'You can push only 200 N. Make the ramp long enough and push the 600 N box onto the truck.' },
      { mode: 'energy', shape: 'track', mass: 2, height: 2.5, goal: 'speed', target: 6, challenge: 'Make the ball pass the bottom of the track at 6 m/s. (v = √(2gh))' }
    ]
  });
})();
