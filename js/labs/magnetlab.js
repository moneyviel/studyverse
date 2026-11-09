/* Knowtopia Concept Lab: magnetlab — magnetic field of a bar magnet, attraction/repulsion of poles,
 * and an electromagnet that picks up paperclips.
 *
 * field:   drag compass needles around a bar magnet; each needle turns to point along the field
 *          (worked out from the two poles: lines leave N and enter S). Toggle iron filings to see the
 *          field pattern. Goal 'findN' hides the pole labels — use the compasses to find the N pole.
 * poles:   drag the right-hand magnet towards the fixed one; tap it to flip it. Like poles repel,
 *          unlike poles attract (the magnet slides away or snaps on).
 * electro: a coil on a nail with a cell; change the current, number of turns and the core. Strength
 *          grows with turns × current (iron core makes it far stronger) and more paperclips hang on.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   mode        string  'field' | 'poles' | 'electro'                                    default 'field'
 *   modes       array   modes offered as tabs                                            default [mode]
 *   goal        string  field: 'findN' | 'none'; poles: 'attract' | 'repel';
 *                       electro: 'clips' (pick up `target` clips) | 'none'   default 'findN'/'attract'/'clips'
 *   target      number  electro: number of paperclips to pick up                         default 6
 *   exact       boolean electro: must be exactly `target` (false = at least)             default true
 *   challenge   string  challenge text (any language); default made from goal
 *   winText     string  optional win message
 *   filings     boolean field: start with iron filings shown                             default false
 *   compasses   number  field: number of compasses (1–4)                                 default 3
 *   labels      object  pole letters, e.g. {N:'N', S:'S'} or {N:'उ', S:'द'}                default {N:'N',S:'S'}
 *   current     number  electro: starting current in A                                   default 1
 *   currentRange [min,max,step] electro current slider in A                             default [0,3,0.5]
 *   turns       array   electro: choices for number of turns                             default [10,20,50]
 *   perClip     number  electro: turns × amperes needed per paperclip                    default 10
 *   maxClips    number  electro: paperclips available                                    default 10
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fN = (v, d = 1) => { const r = Math.round(v * Math.pow(10, d)) / Math.pow(10, d); return String(Object.is(r, -0) ? 0 : r); };
  const rng = (a, def) => Array.isArray(a) && a.length >= 2 && +a[1] > +a[0] ? [+a[0], +a[1], +a[2] > 0 ? +a[2] : def[2]] : def;
  const RED = '#ff6b6b', BLUE = '#3b82f6';

  const CSS = `
.lb-magnetlab-w{font-size:14px;color:#1b1f3a;-webkit-user-select:none;user-select:none}
.lb-magnetlab-ch{font-weight:800;font-size:14px;margin-bottom:6px;line-height:1.25}
.lb-magnetlab-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:16px;touch-action:none}
.lb-magnetlab-row{display:flex;gap:6px;margin-top:6px;align-items:center}
.lb-magnetlab-b{flex:1 1 0;min-width:0;min-height:42px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 6px;line-height:1.1}
.lb-magnetlab-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-magnetlab-b:active{transform:translateY(2px)}
.lb-magnetlab-lab{font-size:11px;font-weight:800;color:#6b7090;text-transform:uppercase;letter-spacing:.3px;min-width:44px}
.lb-magnetlab-sl{display:flex;align-items:center;gap:8px;font-weight:800;font-size:13px;margin-top:2px}
.lb-magnetlab-sl input{flex:1;min-width:0;accent-color:#8b5cf6;height:34px}
.lb-magnetlab-sl b{min-width:52px;text-align:right;color:#3b82f6}
.lb-magnetlab-out{background:#f6f4ff;border-radius:12px;padding:6px 10px;margin-top:5px;font-weight:800;font-size:13px;line-height:1.35;min-height:36px}
.lb-magnetlab-out.bad{background:#ffecec;color:#c23b3b}.lb-magnetlab-out.ok{background:#e3fbf3;color:#0f7a5c}
.lb-magnetlab-out i{font-style:normal;color:#6b7090;font-size:12px}
.lb-magnetlab-drag{cursor:grab}
`;

  Labs.register('magnetlab', {
    title: 'Magnet lab',
    subjects: ['science', 'physics'],
    render(host, p, api) {
      const ex = this.example || {};
      const diffMode = p.mode !== undefined && p.mode !== ex.mode;
      p = Object.assign({}, p);
      if (diffMode) ['modes', 'goal', 'target'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      if (diffMode || p.goal !== ex.goal || p.target !== ex.target) ['challenge', 'winText'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });

      const ALL = ['field', 'poles', 'electro'];
      let mode = ALL.includes(p.mode) ? p.mode : 'field';
      const startMode = mode;
      const modes = (Array.isArray(p.modes) ? p.modes : []).filter(m => ALL.includes(m));
      if (!modes.includes(mode)) modes.unshift(mode);
      const GOALS = { field: ['findN', 'none'], poles: ['attract', 'repel'], electro: ['clips', 'none'] };
      const GDEF = { field: 'findN', poles: 'attract', electro: 'clips' };
      const LN = esc((p.labels && p.labels.N) || 'N'), LS = esc((p.labels && p.labels.S) || 'S');
      let won = false, raf = 0;
      const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(p.winText ? String(p.winText) : m); };
      const goalFor = m => (p.goal && GOALS[m].includes(p.goal)) ? p.goal : GDEF[m];
      const setCh = (m, def) => { chEl.textContent = '🎯 Challenge: ' + (p.challenge && m === startMode && (!p.goal || GOALS[m].includes(p.goal)) ? String(p.challenge) : def); };

      host.innerHTML = `<style>${CSS}</style><div class="lb-magnetlab-w">
  <div class="lb-magnetlab-ch"></div>
  ${modes.length > 1 ? `<div class="lb-magnetlab-row" style="margin:0 0 6px">${modes.map(m => `<button class="lb-magnetlab-b" data-mode="${m}">${{ field: '🧭 Field', poles: '🧲 Poles', electro: '⚡ Electromagnet' }[m]}</button>`).join('')}</div>` : ''}
  <div class="lb-magnetlab-body"></div></div>`;
      const chEl = host.querySelector('.lb-magnetlab-ch'), body = host.querySelector('.lb-magnetlab-body');
      let cleanupMode = () => { };
      const svgPt = (sv, e) => { const m = sv.getScreenCTM(); if (!m) return null; return new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse()); };

      function barMagnet(cx, cy, len, h, nRight, hidden, extra = '') {
        const l = cx - len / 2, half = len / 2;
        const cR = nRight ? RED : BLUE, cL = nRight ? BLUE : RED;
        const tL = nRight ? LS : LN, tR = nRight ? LN : LS;
        if (hidden) return `<g ${extra}><rect x="${l}" y="${cy - h / 2}" width="${len}" height="${h}" rx="8" fill="#9aa0c0" stroke="#6b7090" stroke-width="2.5"/><text x="${l + 18}" y="${cy + 6}" text-anchor="middle" font-size="17" font-weight="800" fill="#fff">?</text><text x="${l + len - 18}" y="${cy + 6}" text-anchor="middle" font-size="17" font-weight="800" fill="#fff">?</text></g>`;
        return `<g ${extra}><rect x="${l}" y="${cy - h / 2}" width="${half}" height="${h}" rx="8" fill="${cL}"/><rect x="${cx - 8}" y="${cy - h / 2}" width="16" height="${h}" fill="${cR}"/><rect x="${cx}" y="${cy - h / 2}" width="${half}" height="${h}" rx="8" fill="${cR}"/><rect x="${cx - 8}" y="${cy - h / 2}" width="8" height="${h}" fill="${cL}"/>` +
          `<rect x="${l}" y="${cy - h / 2}" width="${len}" height="${h}" rx="8" fill="none" stroke="#1b1f3a" stroke-width="2.5"/>` +
          `<text x="${l + 16}" y="${cy + 6}" text-anchor="middle" font-size="17" font-weight="800" fill="#fff">${tL}</text><text x="${l + len - 16}" y="${cy + 6}" text-anchor="middle" font-size="17" font-weight="800" fill="#fff">${tR}</text></g>`;
      }

      function setup() {
        cleanupMode(); cancelAnimationFrame(raf);
        host.querySelectorAll('[data-mode]').forEach(b => b.classList.toggle('on', b.dataset.mode === mode));
        cleanupMode = mode === 'field' ? field(goalFor('field')) : mode === 'poles' ? poles(goalFor('poles')) : electro(goalFor('electro'));
      }

      // ================= FIELD =================
      function field(goal) {
        const W = 360, H = 220, MX = 180, MY = 110, ML = 140, MH = 34;
        let nRight = goal === 'findN' ? Math.random() < 0.5 : true;
        let filings = !!p.filings, answered = false;
        const nc = Math.min(4, Math.max(1, Math.round(+p.compasses || 3)));
        const start = [[52, 46], [300, 182], [180, 40], [70, 186]];
        const comps = start.slice(0, nc).map(([x, y]) => ({ x, y, ang: -90, tgt: 0 }));
        setCh('field', goal === 'findN' ? 'The labels are hidden! Drag the compasses around, then tap the end you think is the N pole.' : 'Drag the compasses around the magnet. Which way do the needles point?');
        body.innerHTML = `<svg class="lb-magnetlab-svg" viewBox="0 0 ${W} ${H}"></svg>
<div class="lb-magnetlab-row"><button class="lb-magnetlab-b" data-fil="1">✨ Iron filings</button>${goal === 'findN' ? '' : '<button class="lb-magnetlab-b" data-flip="1">🔄 Flip magnet</button>'}</div>
<div class="lb-magnetlab-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-magnetlab-out');
        const poleN = () => [MX + (nRight ? 1 : -1) * (ML / 2 - 14), MY], poleS = () => [MX - (nRight ? 1 : -1) * (ML / 2 - 14), MY];
        function B(x, y) {
          let bx = 0, by = 0;
          [[poleN(), 1], [poleS(), -1]].forEach(([q, s]) => { const dx = x - q[0], dy = y - q[1], r2 = dx * dx + dy * dy + 30, r3 = r2 * Math.sqrt(r2); bx += s * dx / r3; by += s * dy / r3; });
          return [bx, by];
        }
        const inMag = (x, y, pad = 0) => Math.abs(x - MX) < ML / 2 + pad && Math.abs(y - MY) < MH / 2 + pad;
        function pushOut(c) {
          const pad = 22;
          if (inMag(c.x, c.y, pad)) { const dyTop = (MY - MH / 2 - pad) - c.y, dyBot = (MY + MH / 2 + pad) - c.y; c.y += Math.abs(dyTop) < Math.abs(dyBot) ? dyTop : dyBot; }
          c.x = Math.max(20, Math.min(W - 20, c.x)); c.y = Math.max(20, Math.min(H - 20, c.y));
        }
        let filingsSVG = '';
        function buildFilings() {
          let o = '';
          for (let y = 9; y < H; y += 15) for (let x = 9 + ((y / 15) % 2) * 7; x < W; x += 14) {
            if (inMag(x, y, 4)) continue;
            const [bx, by] = B(x, y), m = Math.hypot(bx, by); if (!m) continue;
            const ux = bx / m, uy = by / m, op = Math.max(0.18, Math.min(0.85, 0.35 + Math.log10(m * 4e4) * 0.25));
            o += `<line x1="${(x - ux * 5).toFixed(1)}" y1="${(y - uy * 5).toFixed(1)}" x2="${(x + ux * 5).toFixed(1)}" y2="${(y + uy * 5).toFixed(1)}" stroke="#4b4f5c" stroke-width="1.6" stroke-linecap="round" opacity="${op.toFixed(2)}"/>`;
          }
          filingsSVG = o;
        }
        function draw() {
          let o = filings ? filingsSVG : '';
          o += barMagnet(MX, MY, ML, MH, nRight, goal === 'findN' && !answered);
          if (goal === 'findN' && !answered) {
            o += `<rect data-end="L" x="${MX - ML / 2 - 6}" y="${MY - MH / 2 - 8}" width="56" height="${MH + 16}" rx="12" fill="rgba(139,92,246,.08)" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="5 4" style="cursor:pointer"/>`;
            o += `<rect data-end="R" x="${MX + ML / 2 - 50}" y="${MY - MH / 2 - 8}" width="56" height="${MH + 16}" rx="12" fill="rgba(139,92,246,.08)" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="5 4" style="cursor:pointer"/>`;
          }
          comps.forEach((c, i) => {
            o += `<g class="lb-magnetlab-drag" data-c="${i}" transform="translate(${c.x.toFixed(1)} ${c.y.toFixed(1)})"><circle r="22" fill="#fff" stroke="#1b1f3a" stroke-width="2.5"/><text y="-12" text-anchor="middle" font-size="7" font-weight="800" fill="#9aa0c0">·</text>` +
              `<g transform="rotate(${c.ang.toFixed(1)})"><path d="M0 -5.5 L18 0 L0 5.5Z" fill="${RED}"/><path d="M0 -5.5 L-18 0 L0 5.5Z" fill="#b8bdd6"/></g><circle r="2.5" fill="#1b1f3a"/></g>`;
          });
          sv.innerHTML = o;
        }
        function aim() { comps.forEach(c => { const [bx, by] = B(c.x, c.y); c.tgt = Math.atan2(by, bx) * 180 / Math.PI; }); }
        let last = performance.now();
        function loop(now) {
          const dt = Math.min(0.05, (now - last) / 1000); last = now;
          let moving = false;
          comps.forEach(c => { let d = ((c.tgt - c.ang + 540) % 360) - 180; if (Math.abs(d) > 0.3) { c.ang += d * Math.min(1, dt * 10); moving = true; } else c.ang = c.tgt; });
          draw();
          raf = moving || drag ? requestAnimationFrame(loop) : 0;
        }
        const kick = () => { if (!raf) { last = performance.now(); raf = requestAnimationFrame(loop); } };
        function info(msg, cls) {
          out.className = 'lb-magnetlab-out ' + (cls || '');
          out.innerHTML = msg || `The red end of each needle points along the field: <span style="color:${RED}">away from N</span>, <span style="color:${BLUE}">towards S</span>.`;
        }
        let drag = null;
        const down = e => {
          const g = e.target.closest('[data-c]'), end = e.target.closest('[data-end]');
          if (end) {
            const right = end.dataset.end === 'R';
            if (right === nRight) {
              answered = true; info(`Yes! That end is the N pole — compass needles point away from it.`, 'ok'); draw();
              winOnce('Compass needles point away from the N pole and towards the S pole — field lines go from N to S.');
            } else { api.sfx('wrong'); info('Not that one. Look: do the red needle tips point towards or away from that end?', 'bad'); }
            return;
          }
          if (!g) return;
          const q = svgPt(sv, e); if (!q) return;
          const c = comps[+g.dataset.c]; drag = { c, dx: c.x - q.x, dy: c.y - q.y };
          sv.setPointerCapture && sv.setPointerCapture(e.pointerId); kick();
        };
        const move = e => { if (!drag) return; const q = svgPt(sv, e); if (!q) return; drag.c.x = q.x + drag.dx; drag.c.y = q.y + drag.dy; pushOut(drag.c); aim(); kick(); };
        const up = () => { drag = null; };
        sv.addEventListener('pointerdown', down); sv.addEventListener('pointermove', move); sv.addEventListener('pointerup', up); sv.addEventListener('pointercancel', up);
        const onClick = e => {
          const b = e.target.closest('button'); if (!b) return;
          if (b.dataset.fil) { filings = !filings; b.classList.toggle('on', filings); api.sfx('tap'); draw(); }
          if (b.dataset.flip) { nRight = !nRight; buildFilings(); aim(); api.sfx('tap'); kick(); }
        };
        body.addEventListener('click', onClick);
        body.querySelector('[data-fil]').classList.toggle('on', filings);
        buildFilings(); aim(); comps.forEach(c => { c.ang = c.tgt + 60; }); info(); kick();
        return () => { cancelAnimationFrame(raf); raf = 0; sv.removeEventListener('pointerdown', down); sv.removeEventListener('pointermove', move); sv.removeEventListener('pointerup', up); sv.removeEventListener('pointercancel', up); body.removeEventListener('click', onClick); };
      }

      // ================= POLES =================
      function poles(goal) {
        const W = 360, H = 170, MY = 86, ML = 104, MH = 36, RANGE = 90;
        const LX = 70; // fixed magnet centre (its right end is N)
        const leftEnd = LX + ML / 2;
        const touchX = leftEnd + ML / 2; // right magnet centre when touching
        let x = 290, flipped = goal !== 'attract'; // flipped=true → right magnet drawn S…N, so its S faces the fixed magnet's N
        let vx = 0, dragging = null, everClose = false;
        setCh('poles', goal === 'attract' ? 'Make the two magnets pull together and stick. (Tap a magnet to flip it.)' : 'Bring the magnets close so they PUSH each other away. (Tap a magnet to flip it.)');
        body.innerHTML = `<svg class="lb-magnetlab-svg" viewBox="0 0 ${W} ${H}"></svg>
<div class="lb-magnetlab-row"><button class="lb-magnetlab-b" data-flip="1">🔄 Flip right magnet</button><button class="lb-magnetlab-b" data-reset="1">↺ Reset</button></div>
<div class="lb-magnetlab-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-magnetlab-out');
        const facing = () => flipped ? 'S' : 'N'; // pole of right magnet facing the fixed magnet's N
        const like = () => facing() === 'N';
        function draw() {
          const gap = x - ML / 2 - leftEnd;
          let o = `<rect x="0" y="${MY + MH / 2 + 2}" width="${W}" height="${H - MY - MH / 2 - 2}" fill="#e7e9f7"/>`;
          o += barMagnet(LX, MY, ML, MH, true, false);
          o += barMagnet(x, MY, ML, MH, flipped, false, `class="lb-magnetlab-drag" data-m="1"`);
          o += `<text x="${x}" y="${MY - MH / 2 - 8}" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">↔ drag · tap to flip</text>`;
          if (gap < RANGE && gap > 1) {
            const col = like() ? RED : '#14a37f', mid = leftEnd + gap / 2;
            const strength = Math.min(1, 26 / (gap + 10));
            o += like() ? `<path d="M${mid - 6} ${MY} h${-14 - 18 * strength} M${mid + 6} ${MY} h${14 + 18 * strength}" stroke="${col}" stroke-width="4" stroke-linecap="round"/><path d="M${mid - 22 - 18 * strength} ${MY} l8 -6 v12z M${mid + 22 + 18 * strength} ${MY} l-8 -6 v12z" fill="${col}"/>`
              : `<path d="M${mid - 24} ${MY} h12 M${mid + 24} ${MY} h-12" stroke="${col}" stroke-width="4" stroke-linecap="round"/><path d="M${mid - 6} ${MY} l-8 -6 v12z M${mid + 6} ${MY} l8 -6 v12z" fill="${col}"/>`;
          }
          sv.innerHTML = o;
          const fp = facing() === 'N' ? LN : LS;
          if (gap <= 1) { out.className = 'lb-magnetlab-out ok'; out.innerHTML = `${LN} and ${LS} stuck together — unlike poles attract!`; }
          else if (gap < RANGE) { out.className = 'lb-magnetlab-out ' + (like() ? 'bad' : 'ok'); out.innerHTML = like() ? `${LN} faces ${fp}: like poles repel — pushed away!` : `${LN} faces ${fp}: unlike poles attract — pulled in!`; }
          else { out.className = 'lb-magnetlab-out'; out.innerHTML = `${LN} faces ${fp}. Bring them closer… <i>(the force gets weaker with distance)</i>`; }
        }
        let last = performance.now();
        function loop(now) {
          const dt = Math.min(0.04, (now - last) / 1000); last = now;
          const gap = x - ML / 2 - leftEnd;
          if (!dragging) {
            if (gap < RANGE && gap > 0.5) {
              const F = 9000 / Math.pow(gap + 12, 2);
              vx += (like() ? F : -F) * dt * 60;
            }
            vx *= Math.pow(0.04, dt);
            x += vx * dt;
            if (x <= touchX) { x = touchX; vx = 0; if (!like()) { if (goal === 'attract') winOnce('Unlike poles (N and S) attract each other — the magnets snapped together!'); } else { vx = 40; } }
            if (x > W - ML / 2 - 4) { x = W - ML / 2 - 4; vx = 0; }
            if (goal === 'repel' && like() && everClose && x - ML / 2 - leftEnd > 70) winOnce('Like poles (N and N, or S and S) repel each other — the magnet was pushed away!');
          } else if (x - ML / 2 - leftEnd < 40 && like()) everClose = true;
          draw();
          raf = requestAnimationFrame(loop);
        }
        const down = e => {
          if (!e.target.closest('[data-m]')) return;
          const q = svgPt(sv, e); if (!q) return;
          dragging = { dx: x - q.x, sx: q.x, moved: false }; vx = 0;
          sv.setPointerCapture && sv.setPointerCapture(e.pointerId);
        };
        const move = e => {
          if (!dragging) return; const q = svgPt(sv, e); if (!q) return;
          if (Math.abs(q.x - dragging.sx) > 4) dragging.moved = true;
          x = Math.max(touchX, Math.min(W - ML / 2 - 4, q.x + dragging.dx));
          if (like() && x - ML / 2 - leftEnd < 40) everClose = true;
        };
        const up = () => { if (!dragging) return; if (!dragging.moved) { flipped = !flipped; api.sfx('tap'); if (x <= touchX + 0.5) x = touchX + 2; } dragging = null; };
        sv.addEventListener('pointerdown', down); sv.addEventListener('pointermove', move); sv.addEventListener('pointerup', up); sv.addEventListener('pointercancel', up);
        const onClick = e => {
          const b = e.target.closest('button'); if (!b) return;
          if (b.dataset.flip) { flipped = !flipped; if (x <= touchX + 0.5) x = touchX + 2; api.sfx('tap'); }
          if (b.dataset.reset) { x = 290; vx = 0; flipped = goal !== 'attract'; everClose = false; api.sfx('tap'); }
        };
        body.addEventListener('click', onClick);
        raf = requestAnimationFrame(loop);
        return () => { cancelAnimationFrame(raf); sv.removeEventListener('pointerdown', down); sv.removeEventListener('pointermove', move); sv.removeEventListener('pointerup', up); sv.removeEventListener('pointercancel', up); body.removeEventListener('click', onClick); };
      }

      // ================= ELECTRO =================
      function electro(goal) {
        const iR = rng(p.currentRange, [0, 3, 0.5]);
        const turnsList = (Array.isArray(p.turns) && p.turns.length ? p.turns : [10, 20, 50]).map(Number).filter(n => n > 0);
        const per = +p.perClip > 0 ? +p.perClip : 10, maxC = Math.max(1, Math.round(+p.maxClips || 10));
        const target = Math.min(maxC, Math.max(1, Math.round(+p.target || 6)));
        const exact = p.exact !== false;
        let I = Math.min(iR[1], Math.max(iR[0], +p.current >= 0 ? +p.current : 1)), ti = 0, iron = true;
        let shown = 0, raf2 = 0, touched = false;
        const clipsFor = () => Math.min(maxC, Math.floor(turnsList[ti] * I * (iron ? 1 : 0.1) / per + 1e-9));
        setCh('electro', goal === 'clips' ? `Make the electromagnet pick up ${exact ? 'exactly' : 'at least'} ${target} paperclips.` : 'Change the current, turns and core. How many clips can it lift?');
        body.innerHTML = `<svg class="lb-magnetlab-svg" viewBox="0 0 360 200" style="touch-action:manipulation"></svg>
<div class="lb-magnetlab-sl"><span class="lb-magnetlab-lab">Current</span><input type="range" min="${iR[0]}" max="${iR[1]}" step="${iR[2]}" value="${I}"><b></b></div>
<div class="lb-magnetlab-row"><span class="lb-magnetlab-lab">Turns</span>${turnsList.map((n, i) => `<button class="lb-magnetlab-b" data-t="${i}">${n}</button>`).join('')}</div>
<div class="lb-magnetlab-row"><span class="lb-magnetlab-lab">Core</span><button class="lb-magnetlab-b" data-core="1">Iron nail</button><button class="lb-magnetlab-b" data-core="0">None (air)</button></div>
<div class="lb-magnetlab-out"></div>`;
        const sv = body.querySelector('svg'), out = body.querySelector('.lb-magnetlab-out'), iIn = body.querySelector('input');
        function clip(x, y, rot, col) {
          return `<g transform="translate(${x} ${y}) rotate(${rot})"><path d="M-3 -9 V7 a3 3 0 0 0 6 0 V-7 a2 2 0 0 0 -4 0 V5" fill="none" stroke="${col}" stroke-width="2" stroke-linecap="round"/></g>`;
        }
        function draw() {
          const n = turnsList[ti], on = I > 0, str = turnsList[ti] * I * (iron ? 1 : 0.1);
          let o = `<rect x="0" y="176" width="360" height="24" fill="#e7e9f7"/>`;
          // battery and wires
          o += `<rect x="16" y="120" width="48" height="26" rx="6" fill="#1b1f3a"/><rect x="44" y="120" width="20" height="26" fill="#ffc93c"/><rect x="64" y="127" width="5" height="12" rx="2" fill="#9aa0c0"/><text x="38" y="160" text-anchor="middle" font-size="10.5" font-weight="800" fill="#6b7090">${fN(I)} A</text>`;
          const cx0 = 120, cx1 = 260, ny = 70;
          o += `<path d="M16 133 H8 V${ny} H${cx0}" fill="none" stroke="${on ? '#ff9f1c' : '#9aa0c0'}" stroke-width="3"/><path d="M69 133 H${cx1 - 4} V${ny + 12}" fill="none" stroke="${on ? '#ff9f1c' : '#9aa0c0'}" stroke-width="3"/>`;
          // field glow
          if (on) { const g = Math.min(1, str / (per * maxC)); o += `<ellipse cx="${(cx0 + cx1) / 2 + 20}" cy="${ny}" rx="${110 + 30 * g}" ry="${26 + 22 * g}" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="4 5" opacity="${0.15 + 0.6 * g}"/><ellipse cx="${(cx0 + cx1) / 2 + 20}" cy="${ny}" rx="${90 + 20 * g}" ry="${18 + 12 * g}" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="4 5" opacity="${0.1 + 0.5 * g}"/>`; }
          // nail (core)
          if (iron) o += `<rect x="${cx0 - 16}" y="${ny - 7}" width="${cx1 - cx0 + 50}" height="14" rx="3" fill="#9aa4b5" stroke="#6b7090" stroke-width="2"/><path d="M${cx1 + 34} ${ny - 7} L${cx1 + 52} ${ny} L${cx1 + 34} ${ny + 7}Z" fill="#9aa4b5" stroke="#6b7090" stroke-width="2"/><rect x="${cx0 - 22}" y="${ny - 13}" width="7" height="26" rx="2" fill="#9aa4b5" stroke="#6b7090" stroke-width="2"/>`;
          else o += `<rect x="${cx0 - 16}" y="${ny - 7}" width="${cx1 - cx0 + 50}" height="14" rx="7" fill="none" stroke="#c4c8e0" stroke-width="2" stroke-dasharray="4 4"/><text x="${cx1 + 40}" y="${ny - 14}" font-size="10" font-weight="800" fill="#6b7090">air</text>`;
          // coil turns
          const shownTurns = Math.min(28, Math.max(4, Math.round(n / 2)));
          for (let k = 0; k < shownTurns; k++) { const xx = cx0 + (cx1 - cx0) * (k + 0.5) / shownTurns; o += `<ellipse cx="${xx}" cy="${ny}" rx="2.6" ry="11" fill="none" stroke="${on ? '#e8890c' : '#c98a4b'}" stroke-width="2.4"/>`; }
          o += `<text x="${(cx0 + cx1) / 2}" y="${ny - 18}" text-anchor="middle" font-size="11" font-weight="800" fill="#c06a00">${n} turns</text>`;
          // clips: hanging chain from nail tip, others on table
          const tipX = cx1 + 44, k = Math.round(shown);
          for (let j = 0; j < k; j++) o += clip(tipX + (j % 2 ? 2 : -2), ny + 16 + j * 11, j % 2 ? 8 : -8, '#3b82f6');
          for (let j = k; j < maxC; j++) o += clip(150 + (j - k) * 18 - (maxC - k) * 0 + 0, 186, 90, '#6b7090');
          o += `<text x="350" y="20" text-anchor="end" font-size="13" font-weight="800" fill="#3b82f6">📎 ${k} picked up</text>`;
          sv.innerHTML = o;
        }
        function anim() { const t = clipsFor(); shown += Math.sign(t - shown) * Math.min(Math.abs(t - shown), 0.25); draw(); if (Math.abs(t - shown) > 1e-3) raf2 = requestAnimationFrame(anim); }
        function upd() {
          iIn.nextElementSibling.textContent = `${fN(I)} A`;
          body.querySelectorAll('[data-t]').forEach(b => b.classList.toggle('on', +b.dataset.t === ti));
          body.querySelectorAll('[data-core]').forEach(b => b.classList.toggle('on', (b.dataset.core === '1') === iron));
          const c = clipsFor(), prod = turnsList[ti] * I;
          out.className = 'lb-magnetlab-out';
          out.innerHTML = I === 0 ? 'No current → no magnetism. The clips drop off!' : `Turns × current = ${turnsList[ti]} × ${fN(I)} = ${fN(prod)} → ${c} clip${c === 1 ? '' : 's'}${iron ? '' : ' <i>(no iron core: much weaker)</i>'}<br><i>More turns, more current, iron core → stronger magnet</i>`;
          cancelAnimationFrame(raf2); raf2 = requestAnimationFrame(anim);
          if (touched && goal === 'clips' && (exact ? c === target : c >= target)) winOnce(`${turnsList[ti]} turns × ${fN(I)} A${iron ? ' with an iron core' : ''} lifts ${c} paperclips. More current or more turns = stronger electromagnet.`);
        }
        const onIn = () => { I = +iIn.value; touched = true; upd(); };
        const onClick = e => {
          const b = e.target.closest('button'); if (!b) return;
          if (b.dataset.t !== undefined) { ti = +b.dataset.t; touched = true; api.sfx('tap'); upd(); }
          if (b.dataset.core !== undefined) { iron = b.dataset.core === '1'; touched = true; api.sfx('tap'); upd(); }
        };
        body.addEventListener('input', onIn); body.addEventListener('click', onClick);
        shown = clipsFor(); upd();
        return () => { cancelAnimationFrame(raf2); body.removeEventListener('input', onIn); body.removeEventListener('click', onClick); };
      }

      const onTab = e => { const b = e.target.closest('[data-mode]'); if (!b) return; mode = b.dataset.mode; api.sfx('tap'); setup(); };
      host.addEventListener('click', onTab);
      setup();
      return () => { cleanupMode(); cancelAnimationFrame(raf); host.removeEventListener('click', onTab); };
    },
    example: {
      mode: 'field',
      modes: ['field', 'poles'],
      goal: 'findN',
      compasses: 3, filings: false,
      challenge: 'The pole labels are hidden! Move the compasses, then tap the end you think is the North pole.'
    },
    examples: [
      { mode: 'poles', modes: ['poles'], goal: 'attract', challenge: 'Grade 6: Make the two magnets stick together. Which poles must face each other?' },
      { mode: 'electro', modes: ['electro'], goal: 'clips', target: 6, exact: true, current: 1, turns: [10, 20, 50], challenge: 'Grade 7/10: Make the electromagnet lift exactly 6 paperclips.' },
      { mode: 'field', modes: ['field'], goal: 'none', filings: true, compasses: 2, challenge: 'Grade 10: Sprinkle iron filings and move the compasses. Where is the field strongest?' }
    ]
  });
})();
