/* StudyVerse Concept Lab: balance — balance scale for solving linear equations.
 *
 * The equation is  (lx)·x + lu  =  (rx)·x + ru   with whole-number counts (no negatives).
 * Mystery boxes (x) and unit weights (1) sit on two pans. The child removes things from one
 * side (the scale tilts) or from both sides (it stays level), divides both sides, and every
 * balanced step is written as an equation. Solve = one box alone on one side.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   left       [number, number]  [boxes, units] on the left pan  e.g. [2,3] = 2x + 3      default [2,3]
 *   right      [number, number]  [boxes, units] on the right pan e.g. [0,11] = 11         default [0,11]
 *              The solution x = (ru − lu)/(lx − rx) must be a positive number; otherwise
 *              the example equation is used. Keep units ≤ 20 per pan, boxes ≤ 6 per pan.
 *   letter     string   name of the unknown shown on boxes (x, y, n, क …)                 default 'x'
 *   unit       string   optional unit after the answer, e.g. 'kg' or 'g'                  default ''
 *   challenge  string   challenge text; default "Solve 2x + 3 = 11. Get x alone and keep the scale level!"
 *   winText    string   optional message when solved (default "x = 4. Check: …")
 *   hint       string   optional tip shown under the steps at the start
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };
  const fmtNum = v => Number.isInteger(v) ? String(v) : (Math.round(v * 100) / 100).toString();

  Labs.register('balance', {
    title: 'Balance the equation',
    subjects: ['maths'],
    render(host, p, api) {
      const ex = this.example;
      const okPair = a => Array.isArray(a) && a.length === 2 && a.every(n => Number.isInteger(+n) && +n >= 0) && +a[0] <= 6 && +a[1] <= 20;
      let L0 = okPair(p.left) ? p.left.map(Number) : ex.left.slice();
      let R0 = okPair(p.right) ? p.right.map(Number) : ex.right.slice();
      let xv = (R0[1] - L0[1]) / (L0[0] - R0[0]);
      if (!isFinite(xv) || xv <= 0) { L0 = ex.left.slice(); R0 = ex.right.slice(); xv = (R0[1] - L0[1]) / (L0[0] - R0[0]); }
      const X = String(p.letter || 'x');
      const unit = p.unit ? ' ' + p.unit : '';
      const gid = 'lbbal' + Math.random().toString(36).slice(2, 8);
      let L, R, steps, won = false, angle = 0, target = 0, raf = 0, msgTimer = 0;

      const term = (s) => {
        const parts = [];
        if (s.x) parts.push((s.x === 1 ? '' : s.x) + X);
        if (s.u || !s.x) parts.push(String(s.u));
        return parts.join(' + ');
      };
      const eqStr = () => `${term(L)} = ${term(R)}`;
      const weight = s => s.x * xv + s.u;
      const balanced = () => Math.abs(weight(L) - weight(R)) < 1e-9;
      const copy = s => ({ x: s.x, u: s.u });

      host.innerHTML = `
<style>
.lb-balance-w{font-size:14px;color:#1b1f3a}
.lb-balance-ch{font-weight:800;font-size:14px;margin-bottom:6px;line-height:1.25}
.lb-balance-eq{display:flex;align-items:center;justify-content:center;gap:8px;font-family:'Baloo 2',Nunito,sans-serif;font-weight:800;font-size:22px;line-height:1.1;min-height:30px;transition:color .2s}
.lb-balance-eq.off{color:#ff6b6b}
.lb-balance-eq small{font-family:Nunito,sans-serif;font-size:11px;font-weight:800;color:#fff;background:#2ed3a5;border-radius:999px;padding:2px 8px}
.lb-balance-eq.off small{background:#ff6b6b}
.lb-balance-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:18px;touch-action:manipulation}
.lb-balance-it{cursor:pointer}
.lb-balance-row{display:flex;gap:6px;margin-top:6px;align-items:center}
.lb-balance-side{flex:1;display:flex;gap:5px}
.lb-balance-b{flex:1;min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 4px}
.lb-balance-b:active{transform:translateY(2px);box-shadow:0 1px 0 #d3d7ef}
.lb-balance-b:disabled{opacity:.35;cursor:default}
.lb-balance-b.both{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-balance-b.div{background:#3b82f6;color:#fff;box-shadow:0 3px 0 #2563c9}
.lb-balance-b.ghost{flex:0 0 44px;font-size:17px}
.lb-balance-lab{font-size:11px;font-weight:800;color:#6b7090;text-transform:uppercase;letter-spacing:.4px;white-space:nowrap}
.lb-balance-steps{margin-top:7px;background:#f6f4ff;border-radius:12px;padding:6px 8px;display:flex;gap:4px;align-items:center;overflow-x:auto;white-space:nowrap;min-height:40px;scrollbar-width:thin}
.lb-balance-st{font-weight:800;font-size:13.5px;background:#fff;border-radius:9px;padding:3px 7px;box-shadow:0 1px 0 #e3e0fb}
.lb-balance-op{font-size:12.5px;font-weight:800;color:#8b5cf6}
.lb-balance-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:4px;min-height:17px}
</style>
<div class="lb-balance-w">
  <div class="lb-balance-ch">🎯 Challenge: ${esc(p.challenge || `Solve ${term({ x: L0[0], u: L0[1] })} = ${term({ x: R0[0], u: R0[1] })}. Get ${X} alone and keep the scale level!`)}</div>
  <div class="lb-balance-eq"><span class="lb-balance-eqt"></span><small class="lb-balance-tag">balanced</small></div>
  <svg class="lb-balance-svg" viewBox="0 0 360 236" role="img" aria-label="balance scale">
    <defs><linearGradient id="${gid}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#7c4dee"/></linearGradient></defs>
    <rect x="120" y="222" width="120" height="10" rx="5" fill="#d9dcf3"/>
    <path d="M180 52 L150 224 L210 224 Z" fill="#c9cdea"/>
    <path d="M180 52 L163 224 L197 224 Z" fill="#b5bae0"/>
    <g class="lb-balance-beam"><rect x="62" y="45" width="236" height="10" rx="5" fill="#6b7090"/><circle cx="180" cy="50" r="8" fill="#ffc93c" stroke="#1b1f3a" stroke-width="2"/></g>
    <g class="lb-balance-pl"></g><g class="lb-balance-pr"></g>
    <path class="lb-balance-needle" d="M180 50 L180 22" stroke="#ff6b6b" stroke-width="4" stroke-linecap="round"/>
  </svg>
  <div class="lb-balance-row">
    <div class="lb-balance-side"><button class="lb-balance-b" data-a="Lx">−${esc(X)}</button><button class="lb-balance-b" data-a="Lu">−1</button></div>
    <span class="lb-balance-lab">one side</span>
    <div class="lb-balance-side"><button class="lb-balance-b" data-a="Rx">−${esc(X)}</button><button class="lb-balance-b" data-a="Ru">−1</button></div>
  </div>
  <div class="lb-balance-row">
    <span class="lb-balance-lab">both</span>
    <button class="lb-balance-b both" data-a="Bx">−${esc(X)} both</button>
    <button class="lb-balance-b both" data-a="Bu">−1 both</button>
    <button class="lb-balance-b div" data-a="D">÷</button>
    <button class="lb-balance-b ghost" data-a="U" aria-label="undo">↶</button>
    <button class="lb-balance-b ghost" data-a="Z" aria-label="reset">⟲</button>
  </div>
  <div class="lb-balance-steps"></div>
  <div class="lb-balance-msg"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const svgEl = $('.lb-balance-svg'), beam = $('.lb-balance-beam'), needle = $('.lb-balance-needle');
      const PL = $('.lb-balance-pl'), PR = $('.lb-balance-pr');
      const eqT = $('.lb-balance-eqt'), eqBox = $('.lb-balance-eq'), tag = $('.lb-balance-tag');
      const stepsEl = $('.lb-balance-steps'), msgEl = $('.lb-balance-msg');
      const history = [];

      function say(t, keep) { msgEl.textContent = t; clearTimeout(msgTimer); if (!keep) msgTimer = setTimeout(() => { msgEl.textContent = ''; }, 3500); }

      function panItems(s, side) {
        // stack boxes then units on a plate centred at 0, plate top at y=0, items go upward (negative y)
        let out = '', y = 0;
        const bw = 24, bs = 27, per = 4;
        for (let i = 0; i < s.x; i++) {
          const row = Math.floor(i / per), col = i % per, inRow = Math.min(per, s.x - row * per);
          const x0 = -((inRow - 1) * bs) / 2 + col * bs;
          const yy = -bw - row * (bw + 3) - 1;
          out += `<g class="lb-balance-it" data-s="${side}" data-k="x"><rect x="${x0 - bw / 2}" y="${yy}" width="${bw}" height="${bw}" rx="6" fill="url(#${gid})" stroke="#5b33c9" stroke-width="1.5"/><text x="${x0}" y="${yy + 17}" text-anchor="middle" font-size="${won ? 11 : 15}" font-weight="800" fill="#fff">${esc(won ? fmtNum(xv) : X)}</text></g>`;
        }
        y = s.x ? -Math.ceil(s.x / per) * (bw + 3) - 2 : 0;
        const r = 8, us = 17.5, uper = 7;
        for (let i = 0; i < s.u; i++) {
          const row = Math.floor(i / uper), col = i % uper, inRow = Math.min(uper, s.u - row * uper);
          const x0 = -((inRow - 1) * us) / 2 + col * us;
          const yy = y - r - 1 - row * (2 * r + 1);
          out += `<g class="lb-balance-it" data-s="${side}" data-k="u"><circle cx="${x0}" cy="${yy}" r="${r}" fill="#ffc93c" stroke="#d99a00" stroke-width="1.5"/><text x="${x0}" y="${yy + 4}" text-anchor="middle" font-size="10" font-weight="800" fill="#7a5200">1</text></g>`;
        }
        return out;
      }
      function drawPans() {
        const plate = `<path d="M-62 0 L62 0 L52 10 L-52 10 Z" fill="#8b90b8"/>`;
        PL.innerHTML = `<g class="lb-balance-str"></g>${plate}${panItems(L, 'L')}`;
        PR.innerHTML = `<g class="lb-balance-str"></g>${plate}${panItems(R, 'R')}`;
      }
      const HALF = 115, PIV = { x: 180, y: 50 }, DROP = 112;
      function place() {
        const a = angle * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
        beam.setAttribute('transform', `rotate(${angle} ${PIV.x} ${PIV.y})`);
        needle.setAttribute('transform', `rotate(${angle} ${PIV.x} ${PIV.y})`);
        [[PL, -1], [PR, 1]].forEach(([g, d]) => {
          const hx = PIV.x + d * HALF * c, hy = PIV.y + d * HALF * s;
          g.setAttribute('transform', `translate(${hx} ${hy + DROP})`);
          const st = g.querySelector('.lb-balance-str');
          if (st) st.innerHTML = `<path d="M0 ${-DROP} L-58 0 M0 ${-DROP} L58 0" stroke="#9aa0c8" stroke-width="1.6" fill="none"/><circle cx="0" cy="${-DROP}" r="3.5" fill="#6b7090"/>`;
        });
      }
      function tick() {
        const d = target - angle;
        if (Math.abs(d) < 0.05) { angle = target; place(); raf = 0; return; }
        angle += d * 0.16; place(); raf = requestAnimationFrame(tick);
      }
      function setTilt() {
        const diff = weight(R) - weight(L);
        target = Math.max(-14, Math.min(14, diff * 2.2));
        if (Math.abs(diff) > 1e-9 && Math.abs(target) < 4) target = diff > 0 ? 4 : -4;
        if (Math.abs(diff) < 1e-9) target = 0;
        if (!raf) raf = requestAnimationFrame(tick);
      }
      function drawSteps() {
        stepsEl.innerHTML = steps.map((s, i) => (i ? `<span class="lb-balance-op">${esc(s.label)} →</span>` : '') + `<span class="lb-balance-st">${esc(s.eq)}</span>`).join('');
        stepsEl.scrollLeft = stepsEl.scrollWidth;
      }
      function opLabel(base, now) {
        const dLx = base.L.x - now.L.x, dLu = base.L.u - now.L.u, dRx = base.R.x - now.R.x, dRu = base.R.u - now.R.u;
        if (dLx === dRx && dLu === dRu && (dLx || dLu) && dLx >= 0 && dLu >= 0) {
          const t = term({ x: dLx, u: dLu });
          return { label: `−${(dLx && dLu) ? '(' + t + ')' : t}`, type: dLx && dLu ? 'm' : dLx ? 'x' : 'u' };
        }
        const k = base.L.x ? base.L.x / now.L.x : base.R.x ? base.R.x / now.R.x : 0;
        if (k > 1 && Number.isInteger(k) && ['L', 'R'].every(sd => base[sd].x === now[sd].x * k && base[sd].u === now[sd].u * k)) return { label: `÷${k}`, type: 'd' };
        return { label: 'swap equal weights', type: 'o' };
      }
      function logIfBalanced() {
        if (!balanced()) return;
        const now = { L: copy(L), R: copy(R) };
        const last = steps[steps.length - 1];
        if (last.L.x === L.x && last.L.u === L.u && last.R.x === R.x && last.R.u === R.u) return;
        let o = opLabel(last, now);
        if (steps.length > 1 && (o.type === 'u' || o.type === 'x') && last.type === o.type) {
          const o2 = opLabel(steps[steps.length - 2], now);
          if (o2.type === o.type) { steps.pop(); o = o2; }
        }
        steps.push({ eq: eqStr(), L: now.L, R: now.R, label: o.label + ' both', type: o.type });
        drawSteps();
      }
      function update() {
        const bal = balanced();
        eqT.textContent = bal ? eqStr() : `${term(L)} ≠ ${term(R)}`;
        eqBox.classList.toggle('off', !bal);
        tag.textContent = bal ? 'balanced' : (weight(L) > weight(R) ? 'left heavier' : 'right heavier');
        const g = gcd(gcd(L.x, L.u), gcd(R.x, R.u));
        const dBtn = $('[data-a="D"]');
        dBtn.disabled = !(g > 1 && (L.x || R.x) && bal);
        dBtn.textContent = g > 1 ? `÷${g} both` : '÷ both';
        $('[data-a="Lx"]').disabled = !L.x; $('[data-a="Lu"]').disabled = !L.u;
        $('[data-a="Rx"]').disabled = !R.x; $('[data-a="Ru"]').disabled = !R.u;
        $('[data-a="Bx"]').disabled = !(L.x && R.x); $('[data-a="Bu"]').disabled = !(L.u && R.u);
        $('[data-a="U"]').disabled = !history.length;
        drawPans(); place(); setTilt();
        logIfBalanced();
        checkWin();
      }
      function checkWin() {
        if (won || !balanced()) return;
        const solved = (L.x === 1 && L.u === 0 && R.x === 0) || (R.x === 1 && R.u === 0 && L.x === 0);
        if (!solved) return;
        won = true; drawPans(); place();
        const v = fmtNum(xv);
        const side = (s) => { const parts = []; if (s[0]) parts.push((s[0] === 1 ? '' : s[0] + '×') + v); if (s[1] || !s[0]) parts.push(s[1]); return parts.join(' + '); };
        const val = s => s[0] * xv + s[1];
        const msg = p.winText || `${X} = ${v}${unit}. Check: ${side(L0)} = ${fmtNum(val(L0))} and ${side(R0)} = ${fmtNum(val(R0))} ✓`;
        say(`Solved! ${X} = ${v}${unit}`, true);
        api.sfx('correct');
        api.win(msg);
      }
      function act(a) {
        if (a === 'Z') { reset(); api.sfx('tap'); return; }
        if (a === 'U') { if (!history.length) return; const h = history.pop(); L = h.L; R = h.R; steps = h.steps; drawSteps(); update(); api.sfx('tap'); return; }
        if (won) { say('Solved! Tap ⟲ to try again.'); return; }
        const snap = { L: copy(L), R: copy(R), steps: steps.slice() };
        const wasBal = balanced();
        if (a === 'Lx' && L.x) L.x--; else if (a === 'Lu' && L.u) L.u--;
        else if (a === 'Rx' && R.x) R.x--; else if (a === 'Ru' && R.u) R.u--;
        else if (a === 'Bx' && L.x && R.x) { L.x--; R.x--; }
        else if (a === 'Bu' && L.u && R.u) { L.u--; R.u--; }
        else if (a === 'D') {
          const g = gcd(gcd(L.x, L.u), gcd(R.x, R.u)); if (g < 2) return;
          L = { x: L.x / g, u: L.u / g }; R = { x: R.x / g, u: R.u / g };
        } else return;
        history.push(snap);
        update();
        if (wasBal && !balanced()) { api.sfx('wrong'); say('The scale tipped! Do the same to the other side.'); }
        else if (!wasBal && balanced()) { api.sfx('coin'); say('Level again 👍'); }
        else if (balanced()) api.sfx('tap');
      }
      function reset() {
        L = { x: L0[0], u: L0[1] }; R = { x: R0[0], u: R0[1] };
        steps = [{ eq: eqStr(), L: copy(L), R: copy(R), label: '', type: '' }];
        history.length = 0;
        if (won) { won = false; api.resetWin && api.resetWin(); }
        drawSteps(); update();
        say(p.hint || `Each box is the same mystery weight ${X}. Keep the scale level!`, true);
      }
      const onClick = e => { const b = e.target.closest('.lb-balance-b'); if (b && !b.disabled) act(b.dataset.a); };
      const onTap = e => { const it = e.target.closest('.lb-balance-it'); if (it) act(it.dataset.s + it.dataset.k); };
      host.addEventListener('click', onClick);
      svgEl.addEventListener('pointerdown', onTap);
      reset();
      return () => { cancelAnimationFrame(raf); clearTimeout(msgTimer); host.removeEventListener('click', onClick); svgEl.removeEventListener('pointerdown', onTap); };
    },
    example: { left: [2, 3], right: [0, 11], letter: 'x', unit: '' },
    examples: [
      { left: [1, 5], right: [0, 12], letter: 'n', challenge: 'A bag n and 5 marbles weigh as much as 12 marbles. Find n.' },
      { left: [3, 2], right: [1, 10], letter: 'x', challenge: 'Solve 3x + 2 = x + 10 (x on both sides!)' },
      { left: [4, 0], right: [0, 20], letter: 'y', unit: 'kg', challenge: '4 equal sacks weigh 20 kg. How heavy is one sack y?' }
    ]
  });
})();
