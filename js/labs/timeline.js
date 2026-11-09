/* Knowtopia Concept Lab: timeline — scrollable timeline with era bands, scrubbing and an
   ordering / "which came first?" challenge.

   PARAMS (all optional — missing ones fall back to `example`)
   ─────────────────────────────────────────────────────────────────────────────────────────
   title     string   Heading text.                                              'Timeline'
   events    object[] {year:number, label, emoji?, info?, approx?}. BCE years are NEGATIVE
                      (-326 = 326 BCE). With format 'ago' give positive "years ago".
                      approx: true → the date is approximate: shown as "c. 760 CE" (or
                      "लगभग 760 CE" when the event label is in Devanagari), and gaps read
                      "about … years". Ordering / "which came first" use the year as usual.
   eras      object[] Coloured bands {from, to, label, color?} (same year units).     []
   format    string   'bce'  → 326 BCE / 1526 CE (no year 0, gaps across 1 BCE→1 CE are correct)
                      'plain'→ 1947           'ago' → 65 + suffix (older = left).  'bce' if any year < 0 else 'plain'
   suffix    string   Text after numbers in 'ago' format.                         'years ago'
   spacing   string   'linear' (true scale) | 'even' (events equally spaced).     'linear'
   range     number[] [start, end] of the axis (default: events/eras with padding).
   task      string   Challenge: 'order' (drag events into order) | 'first' (which came first?). 'order'
   count     number   order: how many events to sort.                             min(5, events)
   rounds    number   first: correct answers needed.                              3
   challenge string   Challenge text (else generated).

   What the child does: drags the year slider (or taps an event) to travel through time; the card
   shows the event, its era and how many years since the previous event. Challenge tab: drag the
   shuffled cards into time order (oldest on top) and press Check, or pick which came first.
*/
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const COLS = ['#ffe8a3', '#d9ccff', '#c8f4e6', '#ffd0d0', '#cfe3ff', '#ffe0c2'];
  const DCOL = ['#e0a800', '#7c4ddb', '#1a9c78', '#e04848', '#2f6fd6', '#e07a1f'];
  Labs.register('timeline', {
    title: 'Timeline', subjects: ['history', 'social', 'science', 'evs'],
    render(host, p, api) {
      const ex = this.example || {};
      const evRaw = (Array.isArray(p.events) && p.events.length ? p.events : ex.events).filter(e => e && isFinite(+e.year));
      const fmtKind = ['bce', 'plain', 'ago'].includes(p.format) ? p.format : (evRaw.some(e => +e.year < 0) ? 'bce' : 'plain');
      const ago = fmtKind === 'ago', suffix = p.suffix || 'years ago';
      const V = y => ago ? -(+y) : +y;                              /* internal value: bigger = later */
      const ev = evRaw.map((e, i) => ({ ...e, i, v: V(e.year) })).sort((a, b) => a.v - b.v);
      const eras = (Array.isArray(p.eras) && !(p.eras === ex.eras && p.events !== ex.events) ? p.eras : []).filter(e => e && isFinite(+e.from) && isFinite(+e.to)).map((e, i) => { const a = V(e.from), b = V(e.to); return { ...e, a: Math.min(a, b), b: Math.max(a, b), col: e.color || COLS[i % COLS.length], dcol: DCOL[i % DCOL.length] }; });
      const nf = n => Math.abs(n) >= 10000 ? Math.round(n).toLocaleString('en-IN') : (Math.abs(n) < 10 && Math.abs(n - Math.round(n)) > 0.05 ? String(+Math.abs(n).toFixed(1) * Math.sign(n)) : String(Math.round(n)));
      const fmtS = v => ago ? nf(-v) : fmt(v);
      const fmt = v => { if (ago) return `${nf(-v)} ${suffix}`; if (fmtKind === 'bce') return v < 0 ? `${nf(-v)} BCE` : `${nf(v)} CE`; return nf(v); };
      const DEVA = /[\u0900-\u097F]/;
      const isApprox = e => !!e && (e.approx === true || e.approx === 1 || e.approx === 'true');
      const fmtE = e => (isApprox(e) ? (DEVA.test(String(e.label || '') + String(p.title || '')) ? 'लगभग ' : 'c. ') : '') + fmt(e.v);   /* event date */
      const fmtSE = e => (isApprox(e) ? (DEVA.test(String(e.label || '') + String(p.title || '')) ? 'लगभग ' : 'c. ') : '') + fmtS(e.v);
      const unitW = ago ? suffix.replace(/\s*ago\s*$/i, '') || 'years' : 'years';
      const span = (a, b) => { let d = b - a; if (fmtKind === 'bce' && a < 0 && b > 0) d -= 1; return d; }; /* no year zero */
      let lo = ev.length ? ev[0].v : 0, hi = ev.length ? ev[ev.length - 1].v : 100;
      eras.forEach(e => { lo = Math.min(lo, e.a); hi = Math.max(hi, e.b); });
      if (Array.isArray(p.range) && p.range.length === 2) { const a = V(p.range[0]), b = V(p.range[1]); lo = Math.min(a, b); hi = Math.max(a, b); }
      else { const pad = (hi - lo || 10) * 0.04; lo -= pad; hi += pad; }
      const even = p.spacing === 'even' && ev.length > 1;
      const task = p.task === 'first' ? 'first' : 'order';
      const count = Math.max(2, Math.min(+p.count || 5, ev.length));
      const rounds = Math.max(1, +p.rounds || 3);

      host.innerHTML = `<div class="lb-timeline-w"><style>
.lb-timeline-w{font-size:14px;color:#1b1f3a;user-select:none;-webkit-user-select:none}
.lb-timeline-ch{font-weight:800;font-size:14px;line-height:1.3;margin-bottom:6px}
.lb-timeline-tabs{display:flex;gap:6px;margin-bottom:6px}
.lb-timeline-tabs button{flex:1;min-height:40px;border:none;border-radius:12px;background:#eef0fb;color:#1b1f3a;font:inherit;font-weight:800;font-size:13px;cursor:pointer}
.lb-timeline-tabs button.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-timeline-strip{overflow-x:auto;overflow-y:hidden;border-radius:16px;background:linear-gradient(180deg,#f7f8ff,#eef1ff);scrollbar-width:thin;scroll-behavior:auto}
.lb-timeline-strip svg{display:block}
.lb-timeline-ev{cursor:pointer}
.lb-timeline-ev .em{font-size:17px}
.lb-timeline-ev .d{fill:#fff;stroke:#8b5cf6;stroke-width:2.5;transition:all .2s}
.lb-timeline-ev.on .d{fill:#ffc93c;stroke:#1b1f3a}
.lb-timeline-ev .yr{font-size:9.5px;font-weight:800;fill:#6b7090}
.lb-timeline-tk{font-size:9.5px;font-weight:700;fill:#6b7090}
.lb-timeline-era{font-size:10px;font-weight:800}
.lb-timeline-sl{display:flex;align-items:center;gap:8px;margin-top:6px}
.lb-timeline-sl input{flex:1;accent-color:#8b5cf6;height:34px}
.lb-timeline-yr{min-width:92px;text-align:right;font-weight:800;font-size:15px;color:#8b5cf6}
.lb-timeline-card{display:flex;gap:10px;align-items:flex-start;background:#fff;border:2px solid #eef0fb;border-radius:14px;padding:8px 10px;min-height:74px;margin-top:4px}
.lb-timeline-card .e{font-size:30px;line-height:1}
.lb-timeline-card b{font-size:14.5px;display:block}
.lb-timeline-card .m{color:#6b7090;font-weight:700;font-size:12px}
.lb-timeline-card .tx{font-size:13px;line-height:1.3}
.lb-timeline-tag{display:inline-block;border-radius:999px;padding:1px 8px;font-size:11px;font-weight:800;margin-right:4px}
.lb-timeline-list{position:relative;touch-action:none;margin-top:2px}
.lb-timeline-row{position:absolute;left:0;right:0;height:40px;display:flex;align-items:center;gap:8px;background:#fff;border:2px solid #e3e6f7;border-radius:12px;padding:0 10px;font-weight:800;font-size:13.5px;transition:top .18s ease,border-color .2s,background .2s;cursor:grab;box-shadow:0 2px 0 #e3e6f7}
.lb-timeline-row.drag{transition:none;z-index:3;box-shadow:0 8px 20px rgba(27,31,58,.2);cursor:grabbing;border-color:#8b5cf6}
.lb-timeline-row .h{color:#b6bad6;font-size:16px}
.lb-timeline-row .l{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lb-timeline-row .y{color:#6b7090;font-size:12px}
.lb-timeline-row.ok{border-color:#2ed3a5;background:#effcf7}
.lb-timeline-row.bad{border-color:#ff6b6b;background:#fff3f3}
.lb-timeline-ends{display:flex;justify-content:space-between;color:#6b7090;font-weight:800;font-size:11.5px;margin:2px 2px 4px}
.lb-timeline-bar{display:flex;align-items:center;gap:8px;margin-top:8px;min-height:40px}
.lb-timeline-msg{flex:1;font-weight:800;font-size:13.5px;line-height:1.25}
.lb-timeline-bar button,.lb-timeline-pick button{border:none;border-radius:12px;font:inherit;font-weight:800;cursor:pointer}
.lb-timeline-bar button{min-height:40px;padding:0 14px;background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1a9c78}
.lb-timeline-bar button.g{background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
.lb-timeline-pick{display:flex;gap:8px;margin-top:6px}
.lb-timeline-pick button{flex:1;min-height:120px;background:#fff;border:2px solid #e3e6f7;box-shadow:0 3px 0 #e3e6f7;padding:8px;font-size:13.5px;line-height:1.25;transition:all .2s}
.lb-timeline-pick button .e{display:block;font-size:34px;margin-bottom:4px}
.lb-timeline-pick button.ok{border-color:#2ed3a5;background:#effcf7}
.lb-timeline-pick button.bad{border-color:#ff6b6b;background:#fff3f3}
.lb-timeline-pick button .y{display:block;color:#6b7090;font-size:12px;margin-top:4px;min-height:15px}
</style>
<div class="lb-timeline-ch"></div>
<div class="lb-timeline-tabs"><button data-t="x" class="on">🕰️ Travel</button><button data-t="c">🎯 Challenge</button></div>
<div class="lb-timeline-x"><div class="lb-timeline-strip"></div>
<div class="lb-timeline-sl"><input type="range" min="0" max="1000" step="1"><div class="lb-timeline-yr"></div></div>
<div class="lb-timeline-card"></div></div>
<div class="lb-timeline-c" style="display:none"></div></div>`;
      const $ = s => host.querySelector(s);
      const strip = $('.lb-timeline-strip'), slider = $('.lb-timeline-sl input'), yrEl = $('.lb-timeline-yr'), card = $('.lb-timeline-card'), cBox = $('.lb-timeline-c');
      $('.lb-timeline-ch').textContent = '🎯 Challenge: ' + (p.challenge || (task === 'order' ? `Put ${count} events in time order — oldest first` : `Pick which came first — get ${rounds} right`));
      const timers = []; let won = false, cur = null;

      /* ---- scale ---- */
      const SH = 150, PAD = 34;
      let SW = 360;
      const knots = even ? [...new Set(ev.map(e => e.v))] : null;
      function xOf(v) {
        if (!even) return PAD + (v - lo) / (hi - lo || 1) * (SW - 2 * PAD);
        const n = knots.length, step = (SW - 2 * PAD) / (n - 1);
        if (v <= knots[0]) return PAD; if (v >= knots[n - 1]) return SW - PAD;
        for (let i = 0; i < n - 1; i++) if (v <= knots[i + 1]) return PAD + step * (i + (v - knots[i]) / (knots[i + 1] - knots[i]));
        return SW - PAD;
      }
      function vOf(x) {
        if (!even) return lo + (x - PAD) / (SW - 2 * PAD) * (hi - lo);
        const n = knots.length, step = (SW - 2 * PAD) / (n - 1), f = Math.max(0, Math.min(n - 1, (x - PAD) / step)), i = Math.min(n - 2, Math.floor(f));
        return knots[i] + (f - i) * (knots[i + 1] - knots[i]);
      }
      function niceStep(range, n) { const raw = range / n, m = Math.pow(10, Math.floor(Math.log10(raw))); return [1, 2, 5, 10].map(k => k * m).find(s => s >= raw) || 10 * m; }
      function drawStrip() {
        const cw = strip.clientWidth || 360;
        SW = Math.max(cw, ev.length * 62 + 2 * PAD);
        let s = `<svg width="${SW}" height="${SH}" viewBox="0 0 ${SW} ${SH}">`;
        eras.forEach(e => { const a = xOf(e.a), b = xOf(e.b); s += `<rect x="${a}" y="6" width="${Math.max(2, b - a)}" height="${SH - 12}" rx="10" fill="${e.col}" opacity=".55"/><text class="lb-timeline-era" x="${(a + b) / 2}" y="19" text-anchor="middle" fill="${e.dcol}">${esc(e.label)}</text>`; });
        const AY = 102;
        s += `<line x1="${PAD - 14}" x2="${SW - PAD + 14}" y1="${AY}" y2="${AY}" stroke="#1b1f3a" stroke-width="3" stroke-linecap="round"/><path d="M${SW - PAD + 16} ${AY} l-8 -5 v10z" fill="#1b1f3a"/>`;
        if (!even) {
          const st = niceStep(hi - lo, Math.max(3, Math.floor(SW / 85)));
          for (let t = Math.ceil(lo / st) * st; t <= hi; t += st) { if (fmtKind === 'bce' && t === 0) continue; const x = xOf(t); s += `<line x1="${x}" x2="${x}" y1="${AY - 4}" y2="${AY + 4}" stroke="#1b1f3a" stroke-width="1.5"/><text class="lb-timeline-tk" x="${x}" y="${AY + 38}" text-anchor="middle">${esc(fmtS(t))}</text>`; }
        }
        ev.forEach((e, k) => {
          const x = xOf(e.v), up = [44, 62, 78][k % 3];
          s += `<g class="lb-timeline-ev" data-k="${k}"><line x1="${x}" x2="${x}" y1="${up + 6}" y2="${AY}" stroke="#c9c2f5" stroke-width="1.5"/><text class="em" x="${x}" y="${up}" text-anchor="middle">${esc(e.emoji || '⭐')}</text><circle class="d" cx="${x}" cy="${AY}" r="7"/>${even ? `<text class="yr" x="${x}" y="${AY + (k % 2 ? 36 : 22)}" text-anchor="middle">${esc(fmtSE(e))}</text>` : ''}<rect x="${x - 20}" y="${up - 20}" width="40" height="${AY - up + 30}" fill="transparent"/></g>`;
        });
        if (ago) s += `<text class="lb-timeline-tk" x="${SW - PAD}" y="${SH - 4}" text-anchor="end">(${esc(suffix)})</text>`;
        s += `<g class="cur" style="pointer-events:none"><line y1="4" y2="${SH - 4}" stroke="#ff6b6b" stroke-width="2.5"/><circle cy="${AY}" r="4" fill="#ff6b6b"/></g></svg>`;
        strip.innerHTML = s;
        strip.querySelectorAll('.lb-timeline-ev').forEach(g => g.addEventListener('click', () => { const e = ev[+g.dataset.k]; api.sfx('tap'); setX(xOf(e.v), true); }));
      }
      function setX(x, center) {
        x = Math.max(PAD, Math.min(SW - PAD, x));
        slider.value = Math.round((x - PAD) / (SW - 2 * PAD) * 1000);
        const v = vOf(x), c = strip.querySelector('.cur'); if (c) c.setAttribute('transform', `translate(${x},0)`);
        yrEl.textContent = fmt(fmtKind === 'bce' && Math.round(v) === 0 ? 1 : v);
        if (center !== false) strip.scrollLeft = x - strip.clientWidth / 2;
        /* nearest event to cursor */
        let best = null, bd = 1e9; ev.forEach((e, k) => { const d = Math.abs(xOf(e.v) - x); if (d < bd) { bd = d; best = k; } });
        if (best == null) { card.innerHTML = '<div class="tx">No events.</div>'; return; }
        strip.querySelectorAll('.lb-timeline-ev').forEach(g => g.classList.toggle('on', +g.dataset.k === best));
        if (best !== cur) {
          cur = best; const e = ev[best], prev = ev[best - 1], era = eras.find(r => e.v >= r.a && e.v <= r.b);
          const gap = prev ? span(prev.v, e.v) : null;
          card.innerHTML = `<div class="e">${esc(e.emoji || '⭐')}</div><div><b>${esc(e.label)}</b><div class="m">${era ? `<span class="lb-timeline-tag" style="background:${era.col};color:${era.dcol}">${esc(era.label)}</span>` : ''}${esc(fmtE(e))}${gap != null ? ` · ${isApprox(e) || isApprox(prev) ? 'about ' : ''}${nf(gap)} ${esc(unitW)} after “${esc(prev.label)}”` : ''}</div>${e.info ? `<div class="tx">${esc(e.info)}</div>` : ''}</div>`;
        }
      }
      slider.addEventListener('input', () => setX(PAD + slider.value / 1000 * (SW - 2 * PAD)));
      slider.addEventListener('change', () => { if (cur != null) api.speak(ev[cur].label); });

      /* ---- challenge: order ---- */
      let order = [], pick = [], checked = false, streak = 0, asked = 0;
      const ROW = 46;
      function startOrder() {
        checked = false;
        pick = ev.slice().sort(() => Math.random() - .5).slice(0, count);
        /* make sure no two picked events share a year, and it is not already sorted */
        const seenV = new Set(); pick = pick.filter(e => !seenV.has(e.v) && seenV.add(e.v));
        order = pick.slice(); for (let t = 0; t < 5 && order.every((e, i) => !i || order[i - 1].v <= e.v); t++) order.sort(() => Math.random() - .5);
        cBox.innerHTML = `<div class="lb-timeline-ends"><span>⬆️ Oldest</span><span>drag ↕ to sort</span></div><div class="lb-timeline-list" style="height:${order.length * ROW}px"></div><div class="lb-timeline-ends"><span>⬇️ Newest</span><span></span></div>
<div class="lb-timeline-bar"><div class="lb-timeline-msg">Drag the cards, then press Check.</div><button class="g sh">🔀</button><button class="ck">✔ Check</button></div>`;
        const list = cBox.querySelector('.lb-timeline-list');
        order.forEach(e => { const r = document.createElement('div'); r.className = 'lb-timeline-row'; r.innerHTML = `<span class="h">⋮⋮</span><span>${esc(e.emoji || '⭐')}</span><span class="l">${esc(e.label)}</span><span class="y"></span>`; r._e = e; list.appendChild(r); });
        layout();
        let drag = null;
        list.addEventListener('pointerdown', ev0 => {
          const r = ev0.target.closest('.lb-timeline-row'); if (!r) return;
          drag = { r, y0: ev0.clientY, top: order.indexOf(r._e) * ROW }; r.classList.add('drag'); list.setPointerCapture && list.setPointerCapture(ev0.pointerId);
          if (checked) { checked = false; list.querySelectorAll('.lb-timeline-row').forEach(x => { x.classList.remove('ok', 'bad'); x.querySelector('.y').textContent = ''; }); }
        });
        list.addEventListener('pointermove', e2 => {
          if (!drag) return;
          const top = Math.max(-6, Math.min((order.length - 1) * ROW + 6, drag.top + e2.clientY - drag.y0)); drag.r.style.top = top + 'px';
          const want = Math.max(0, Math.min(order.length - 1, Math.round(top / ROW))), at = order.indexOf(drag.r._e);
          if (want !== at) { order.splice(at, 1); order.splice(want, 0, drag.r._e); layout(drag.r); api.sfx('tap'); }
        });
        const end = () => { if (!drag) return; drag.r.classList.remove('drag'); drag = null; layout(); };
        list.addEventListener('pointerup', end); list.addEventListener('pointercancel', end);
        cBox.querySelector('.sh').addEventListener('click', () => { api.sfx('tap'); startOrder(); });
        cBox.querySelector('.ck').addEventListener('click', check);
      }
      function layout(skip) { cBox.querySelectorAll('.lb-timeline-row').forEach(r => { if (r !== skip) r.style.top = order.indexOf(r._e) * ROW + 'px'; }); }
      function check() {
        const sorted = order.slice().sort((a, b) => a.v - b.v); let ok = 0; checked = true;
        cBox.querySelectorAll('.lb-timeline-row').forEach(r => { const i = order.indexOf(r._e), good = sorted[i].v === r._e.v; ok += good; r.classList.toggle('ok', good); r.classList.toggle('bad', !good); r.querySelector('.y').textContent = good ? fmtE(r._e) : ''; });
        const m = cBox.querySelector('.lb-timeline-msg');
        if (ok === order.length) { api.sfx('correct'); m.textContent = 'Perfect order! 🎉'; if (!won) { won = true; api.win(`You put ${order.length} events in the right time order!`); } }
        else { api.sfx('wrong'); m.textContent = `${ok} of ${order.length} in the right place. Move the red ones!`; }
      }
      /* ---- challenge: which came first ---- */
      function startFirst() {
        streak = 0; asked = 0;
        cBox.innerHTML = `<div style="font-weight:800;margin:2px 0 2px">Which came first? 🤔</div><div class="lb-timeline-pick"><button></button><button></button></div><div class="lb-timeline-bar"><div class="lb-timeline-msg"></div></div>`;
        const bs = cBox.querySelectorAll('.lb-timeline-pick button');
        let pair = null, lock = false;
        function ask() {
          lock = false;
          const pool = ev.slice(); let a, b, t = 0;
          do { a = pool[Math.floor(Math.random() * pool.length)]; b = pool[Math.floor(Math.random() * pool.length)]; } while ((a === b || a.v === b.v) && ++t < 50);
          pair = [a, b]; bs.forEach((bt, i) => { bt.className = ''; bt.innerHTML = `<span class="e">${esc(pair[i].emoji || '⭐')}</span>${esc(pair[i].label)}<span class="y"></span>`; });
          cBox.querySelector('.lb-timeline-msg').textContent = `✅ ${streak} / ${rounds} correct`;
        }
        bs.forEach((bt, i) => bt.addEventListener('click', () => {
          if (lock || !pair) return; lock = true;
          const first = pair[0].v < pair[1].v ? 0 : 1, good = i === first;
          bs.forEach((x, j) => { x.classList.add(j === first ? 'ok' : 'bad'); x.querySelector('.y').textContent = fmtE(pair[j]); });
          const m = cBox.querySelector('.lb-timeline-msg');
          if (good) { streak++; api.sfx('correct'); } else api.sfx('wrong');
          m.textContent = (good ? 'Yes! ' : 'Oops! ') + `${isApprox(pair[0]) || isApprox(pair[1]) ? 'about ' : ''}${nf(span(pair[first].v, pair[1 - first].v))} ${unitW} apart · ✅ ${streak} / ${rounds}`;
          if (streak >= rounds) { if (!won) { won = true; api.win(`You got ${rounds} right — great sense of time!`); } m.textContent += ' 🎉'; return; }
          timers.push(setTimeout(ask, 1700));
        }));
        ask();
      }
      function tab(t) {
        host.querySelectorAll('.lb-timeline-tabs button').forEach(b => b.classList.toggle('on', b.dataset.t === t));
        $('.lb-timeline-x').style.display = t === 'x' ? '' : 'none'; cBox.style.display = t === 'c' ? '' : 'none';
        if (t === 'c') (task === 'order' ? startOrder : startFirst)();
        else { drawStrip(); setX(PAD + slider.value / 1000 * (SW - 2 * PAD)); }
      }
      host.querySelectorAll('.lb-timeline-tabs button').forEach(b => b.addEventListener('click', () => { api.sfx('tap'); tab(b.dataset.t); }));
      drawStrip();
      setX(ev.length ? xOf(ev[0].v) : PAD);
      const onResize = () => { if ($('.lb-timeline-x').style.display !== 'none') { const f = slider.value / 1000; drawStrip(); setX(PAD + f * (SW - 2 * PAD)); } };
      window.addEventListener('resize', onResize);
      return () => { timers.forEach(clearTimeout); window.removeEventListener('resize', onResize); };
    },
    example: {
      title: 'Ancient to modern India', format: 'bce', spacing: 'even', task: 'order', count: 5,
      challenge: 'Drag the 5 events into time order — oldest on top',
      eras: [{ from: -3300, to: -1700, label: 'Harappan' }, { from: -1500, to: -500, label: 'Vedic' }, { from: -322, to: -185, label: 'Mauryan' },
        { from: 320, to: 550, label: 'Gupta' }, { from: 1526, to: 1857, label: 'Mughal' }, { from: 1858, to: 1947, label: 'British rule' }],
      events: [
        { year: -2600, label: 'Mohenjo-daro city is built', emoji: '🧱', info: 'Planned streets, drains and the Great Bath.' },
        { year: -1500, label: 'Rigveda is composed', emoji: '📜', info: 'The oldest of the Vedas, passed on by memory.' },
        { year: -563, label: 'Gautama Buddha is born', emoji: '☸️', info: 'Born at Lumbini; taught the Middle Path.' },
        { year: -268, label: 'Ashoka becomes emperor', emoji: '🦁', info: 'After Kalinga he spread dhamma. His lion capital is our national emblem.' },
        { year: 499, label: 'Aryabhata writes Aryabhatiya', emoji: '🔭', info: 'Explained that the Earth spins on its axis.' },
        { year: 760, approx: true, label: 'Kailasa temple at Ellora is carved', emoji: '🛕', info: 'Cut from a single rock under the Rashtrakuta kings.' },
        { year: 1526, label: 'First Battle of Panipat', emoji: '⚔️', info: 'Babur defeats Ibrahim Lodi; the Mughal Empire begins.' },
        { year: 1857, label: 'Revolt of 1857', emoji: '🔥', info: 'First big uprising against the East India Company.' },
        { year: 1947, label: 'India becomes independent', emoji: '🇮🇳', info: '15 August 1947.' }
      ]
    },
    examples: [
      { title: 'Freedom struggle (Class 8)', format: 'plain', spacing: 'linear', task: 'first', rounds: 3, range: [1880, 1952],
        challenge: 'Which came first? Get 3 right',
        eras: [{ from: 1885, to: 1905, label: 'Moderates' }, { from: 1905, to: 1919, label: 'Extremists' }, { from: 1919, to: 1947, label: 'Gandhian era' }],
        events: [{ year: 1885, label: 'Indian National Congress founded', emoji: '🏛️' }, { year: 1905, label: 'Partition of Bengal', emoji: '✂️' },
          { year: 1919, label: 'Jallianwala Bagh massacre', emoji: '🕯️' }, { year: 1920, label: 'Non-Cooperation Movement', emoji: '🧵' },
          { year: 1930, label: 'Dandi March (Salt Satyagraha)', emoji: '🧂', info: 'Gandhiji walked 240 miles to make salt.' }, { year: 1942, label: 'Quit India Movement', emoji: '📢' },
          { year: 1947, label: 'Independence', emoji: '🇮🇳' }, { year: 1950, label: 'Constitution comes into force', emoji: '📘', info: '26 January 1950 — Republic Day.' }] },
      { title: 'Life on Earth (Class 4-5)', format: 'ago', suffix: 'million years ago', spacing: 'even', task: 'order', count: 4,
        challenge: 'Sort these 4 from oldest to newest',
        eras: [{ from: 540, to: 252, label: 'Old life' }, { from: 252, to: 66, label: 'Dinosaur age' }, { from: 66, to: 0, label: 'Mammal age' }],
        events: [{ year: 500, label: 'Fish appear in the sea', emoji: '🐟' }, { year: 375, label: 'Animals walk onto land', emoji: '🦎' },
          { year: 230, label: 'First dinosaurs', emoji: '🦕' }, { year: 150, label: 'First birds', emoji: '🐦' },
          { year: 66, label: 'Dinosaurs die out', emoji: '☄️' }, { year: 0.3, label: 'Modern humans appear', emoji: '🧍' }] },
      { title: 'भारत का इतिहास', format: 'bce', spacing: 'even', task: 'order', count: 4, challenge: 'चारों घटनाओं को समय के क्रम में लगाओ — सबसे पुरानी ऊपर',
        events: [{ year: -2600, approx: true, label: 'मोहनजोदड़ो नगर', emoji: '🧱' }, { year: -268, label: 'अशोक सम्राट बने', emoji: '🦁' },
          { year: 760, approx: true, label: 'एलोरा का कैलाश मंदिर', emoji: '🛕' }, { year: 1947, label: 'भारत स्वतंत्र हुआ', emoji: '🇮🇳' }] }
    ]
  });
})();
