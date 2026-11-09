/* Knowtopia Concept Lab: arraygrid — "Array builder & fair sharing"
 * Multiplication as rows × columns of objects (drag the corner to resize), times tables as growing rows,
 * and division as sharing objects equally into groups (with remainders).
 *
 * PARAMS (all optional)
 *  name        type            meaning                                                               default
 *  mode        string          'array' : drag to build rows × columns                                 'array'
 *                              'table' : a times table — columns fixed at `table`, drag rows 1-10
 *                              'share' : share `total` objects equally among `groups` plates
 *  rows, cols  number          starting size of the array                                             2, 3
 *  maxRows     number          largest rows allowed (≤ 12)                                             10
 *  maxCols     number          largest columns allowed (≤ 12)                                          10
 *  ask         string          array mode goal: 'exact' (make target "3x4"), 'product' (any array whose
 *                              product is `target`), 'factors' (find every array for `target`)         'exact'
 *  target      string|number   'exact': "3x4" (rows x cols); 'product' / 'factors' / 'table': a number  "3x4"
 *  table       number          table mode: the times table (columns)                                   7
 *  minSide     number          'product' mode: smallest rows/cols allowed (2 = no 1-row arrays)         1
 *  total       number          share mode: objects to share (≤ 40)                                      13
 *  groups      number          share mode: number of plates (≤ 10)                                      4
 *  lockGroups  boolean         share mode: hide the − / + for the number of plates                       true
 *  groupLabels array           share mode: names under plates, e.g. ["Riya","Aman"] (any language)       none
 *  item        string          object: 'apple' | 'star' | 'ball' | 'flower' | 'sweet' | 'mango' | emoji  'apple' (share: 'sweet')
 *  itemName    string          word for the objects in messages (any language)                          from item
 *  newChallenge boolean        show the "New" button                                                     true
 *  challenge   string          challenge text (any language); default generated                          auto
 */
(function () {
  const T = 'arraygrid';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const ITEMS = {
    apple: '<circle cx="12" cy="14" r="9" fill="#ff6b6b"/><circle cx="8.5" cy="11" r="2.4" fill="#fff" opacity=".45"/><path d="M12 6q1-4 4-4" stroke="#7a4a1f" stroke-width="1.8" fill="none"/><path d="M13 5q4-3 7 0q-4 3-7 0" fill="#2ed3a5"/>',
    mango: '<path d="M5 15q0-10 10-10q6 1 6 8q-1 9-9 9q-7-1-7-7z" fill="#ffc93c" stroke="#f0a020" stroke-width="1.4"/><path d="M14 5q2-3 5-2q-2 3-5 2z" fill="#2ed3a5"/>',
    star: '<path d="M12 2l3 6.5 7 .8-5.2 4.8 1.5 7-6.3-3.6-6.3 3.6 1.5-7L2 9.3l7-.8z" fill="#ffc93c" stroke="#e0a400" stroke-width="1.2" stroke-linejoin="round"/>',
    ball: '<circle cx="12" cy="12" r="9.5" fill="#3b82f6"/><path d="M2.6 11q9.4 4 18.8 0M12 2.5q-4 9.5 0 19" stroke="#fff" stroke-width="1.6" fill="none"/>',
    flower: '<g fill="#ff8fb3"><circle cx="12" cy="6" r="4"/><circle cx="18" cy="11" r="4"/><circle cx="15.5" cy="18" r="4"/><circle cx="8.5" cy="18" r="4"/><circle cx="6" cy="11" r="4"/></g><circle cx="12" cy="12.5" r="3.6" fill="#ffc93c"/>',
    sweet: '<path d="M2 12l4-4v8zM22 12l-4-4v8z" fill="#ff6b6b"/><ellipse cx="12" cy="12" rx="7" ry="6" fill="#8b5cf6"/><path d="M8 9q4 6 8 0" stroke="#fff" stroke-width="1.5" fill="none" opacity=".6"/>'
  };
  const WORD = { apple: 'apples', mango: 'mangoes', star: 'stars', ball: 'balls', flower: 'flowers', sweet: 'sweets' };
  // item drawn inside an SVG at (x,y) size s
  const itemAt = (it, x, y, s) => ITEMS[it] ? `<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${(s / 24).toFixed(3)})">${ITEMS[it]}</g>` : `<text x="${(x + s / 2).toFixed(1)}" y="${(y + s * .82).toFixed(1)}" font-size="${(s * .85).toFixed(1)}" text-anchor="middle">${esc(it)}</text>`;
  const itemHTML = (it, s) => ITEMS[it] ? `<svg width="${s}" height="${s}" viewBox="0 0 24 24" aria-hidden="true">${ITEMS[it]}</svg>` : `<span style="font-size:${s - 4}px;line-height:${s}px;display:inline-block;width:${s}px;text-align:center">${esc(it)}</span>`;

  const CSS = `
  .lb-arraygrid-w{user-select:none;-webkit-user-select:none}
  .lb-arraygrid-ch{font-weight:800;font-size:14.5px;line-height:1.3;color:#1b1f3a;background:#f4f0ff;border-radius:14px;padding:9px 12px;margin-bottom:8px}
  .lb-arraygrid-stage{background:#fbfbff;border-radius:18px;box-shadow:inset 0 0 0 2px #eceefa;padding:4px}
  .lb-arraygrid-svg{display:block;width:100%;height:auto;touch-action:none;cursor:nwse-resize}
  .lb-arraygrid-eq{margin:8px 0 0;text-align:center;font-weight:800;font-size:24px;color:#1b1f3a;min-height:34px}
  .lb-arraygrid-eq .r{color:#8b5cf6}.lb-arraygrid-eq .c{color:#3b82f6}.lb-arraygrid-eq .a{color:#14a37f}
  .lb-arraygrid-sub{text-align:center;color:#6b7090;font-weight:700;font-size:13px;min-height:18px;overflow-wrap:anywhere}
  .lb-arraygrid-hint{text-align:center;font-weight:800;font-size:13.5px;color:#7c4ddb;min-height:20px;margin:4px 0 6px}
  .lb-arraygrid-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;align-items:center}
  .lb-arraygrid-s{height:44px;min-width:44px;border:none;border-radius:14px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 4px 0 #d3d7ef;padding:0 12px}
  .lb-arraygrid-s:active{transform:translateY(3px);box-shadow:0 1px 0 #d3d7ef}
  .lb-arraygrid-s.go{background:#2ed3a5;color:#fff;box-shadow:0 4px 0 #1a9c78}
  .lb-arraygrid-s.go:active{box-shadow:0 1px 0 #1a9c78}
  .lb-arraygrid-sl{display:flex;align-items:center;gap:4px;border-radius:16px;padding:3px 5px;font-weight:800;font-size:13px}
  .lb-arraygrid-sl .lb-arraygrid-s{height:40px;min-width:40px;font-size:20px;background:#fff;padding:0}
  .lb-arraygrid-sl output{min-width:22px;text-align:center;font-size:17px}
  .lb-arraygrid-chips{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;margin:4px 0;min-height:26px}
  .lb-arraygrid-chip{background:#e3fbf3;color:#0f7a5c;border-radius:999px;padding:3px 10px;font-weight:800;font-size:13px}
  .lb-arraygrid-chip.no{background:#f2f3f9;color:#b0b4cc}
  .lb-arraygrid-pile{display:flex;flex-wrap:wrap;justify-content:center;gap:2px;min-height:40px;padding:6px;border-radius:14px;background:#fff7e0;box-shadow:inset 0 0 0 2px #ffe6a6;margin:2px 2px 8px}
  .lb-arraygrid-pile .lbl{width:100%;text-align:center;font-weight:800;font-size:12px;color:#b07d00}
  .lb-arraygrid-plates{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding:2px 2px 4px}
  .lb-arraygrid-plate{width:74px;min-height:86px;border-radius:50%/42%;background:radial-gradient(circle at 50% 45%,#fff 0 55%,#eef0fb 56%);box-shadow:0 3px 0 #d3d7ef,inset 0 0 0 2px #dfe2f3;display:flex;flex-wrap:wrap;align-content:center;justify-content:center;gap:0;padding:10px 8px;cursor:pointer;position:relative;transition:transform .12s}
  .lb-arraygrid-plate:active{transform:scale(.95)}
  .lb-arraygrid-plate b{position:absolute;bottom:-20px;left:0;right:0;text-align:center;font-size:12px;color:#6b7090;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .lb-arraygrid-pw{display:flex;flex-direction:column;align-items:center;margin-bottom:18px}
  .lb-arraygrid-plate.full{box-shadow:0 3px 0 #9ee9d3,inset 0 0 0 2.5px #2ed3a5}
  `;

  Labs.register(T, {
    title: 'Arrays & sharing',
    subjects: ['maths'],
    render(host, p, api) {
      const mode = ['array', 'table', 'share'].includes(p.mode) ? p.mode : 'array';
      const int = (v, d, lo, hi) => { const x = Math.round(+v); return isFinite(x) && x >= lo ? Math.min(hi, x) : d; };
      let maxR = int(p.maxRows, 10, 1, 12), maxC = int(p.maxCols, 10, 1, 12);
      const item = p.item || (mode === 'share' ? 'sweet' : 'apple');
      const word = p.itemName || WORD[item] || 'objects';
      let ask = ['exact', 'product', 'factors'].includes(p.ask) ? p.ask : 'exact';
      let table = int(p.table, 7, 1, 12);
      if (mode === 'table') { maxC = table; maxR = 10; }
      let rows = int(p.rows, 2, 1, maxR), cols = mode === 'table' ? table : int(p.cols, 3, 1, maxC);
      if (mode === 'table') rows = int(p.rows, 1, 1, 10);
      const minSide = int(p.minSide, 1, 1, 12);
      let customText = p.challenge ? String(p.challenge) : '';

      // targets
      let tR = 0, tC = 0, tP = 0;
      function parseTarget() {
        const t = p.target;
        if (mode === 'array' && ask === 'exact') {
          const m = String(t == null ? '' : t).match(/(\d+)\s*[x×*]\s*(\d+)/i);
          if (m) { tR = Math.min(maxR, +m[1]); tC = Math.min(maxC, +m[2]); } else { tR = Math.min(3, maxR); tC = Math.min(4, maxC); }
        } else if (mode === 'array') {
          tP = int(t, 12, 1, maxR * maxC); if (pairs(tP).length === 0) tP = 12;
        } else if (mode === 'table') {
          tP = int(t, table * 6, 1, 1000); if (tP % table || tP / table > 10) tP = table * 6;
        }
      }
      function pairs(n) { const out = []; for (let r = 1; r <= maxR; r++) if (n % r === 0 && n / r <= maxC && r >= minSide && n / r >= minSide) out.push([r, n / r]); return out; }
      function unordered(n) { const s = new Set(); pairs(n).forEach(([a, b]) => s.add(Math.min(a, b) + '×' + Math.max(a, b))); return [...s]; }
      parseTarget();
      let found = new Set();

      // share state
      let total = int(p.total, 13, 1, 40), groups = int(p.groups, 4, 1, 10);
      let plates, pile, history;
      const resetShare = () => { plates = new Array(groups).fill(0); pile = total; history = []; };
      resetShare();

      function defaultText() {
        if (mode === 'share') return `Share ${total} ${word} equally among ${groups}. How many each? How many left over?`;
        if (mode === 'table') return `${table} × ? = ${tP}. Drag down to grow the rows of ${table} until you reach ${tP}`;
        if (ask === 'exact') return `Make an array with ${tR} rows of ${tC}. How many ${word} in all?`;
        if (ask === 'product') return `Make an array of exactly ${tP} ${word}${minSide > 1 ? ' (no single rows!)' : ''}`;
        return `Find all the different arrays you can make with ${tP} ${word}`;
      }

      host.innerHTML = `<style>${CSS}</style><div class="lb-arraygrid-w">
        <div class="lb-arraygrid-ch"></div>
        <div class="lb-arraygrid-stage"></div>
        <div class="lb-arraygrid-eq"></div>
        <div class="lb-arraygrid-sub"></div>
        <div class="lb-arraygrid-chips"></div>
        <div class="lb-arraygrid-hint"></div>
        <div class="lb-arraygrid-row"></div></div>`;
      const $ = s => host.querySelector(s);
      const stage = $('.lb-arraygrid-stage'), eqEl = $('.lb-arraygrid-eq'), subEl = $('.lb-arraygrid-sub'), chipsEl = $('.lb-arraygrid-chips'), hintEl = $('.lb-arraygrid-hint'), rowEl = $('.lb-arraygrid-row'), chEl = $('.lb-arraygrid-ch');
      const hint = t => { hintEl.textContent = t || ''; };
      const setText = () => { chEl.textContent = '🎯 Challenge: ' + (customText || defaultText()); };

      // ---------- array / table drawing ----------
      const W = 360, LM = 30, TM = 26;
      let cell = 30, svg = null;
      function layout() { cell = Math.min(40, (W - LM - 10) / maxC, 280 / maxR); }
      function drawGrid() {
        layout();
        const H = TM + maxR * cell + 10;
        let s = '';
        // active block background
        s += `<rect x="${LM - 3}" y="${TM - 3}" width="${cols * cell + 6}" height="${rows * cell + 6}" rx="10" fill="#f1ebff" stroke="#c9b5ff" stroke-width="2"/>`;
        for (let r = 0; r < maxR; r++) for (let c = 0; c < maxC; c++) {
          const x = LM + c * cell, y = TM + r * cell;
          if (r < rows && c < cols) s += itemAt(item, x + cell * .1, y + cell * .1, cell * .8);
          else s += `<circle cx="${x + cell / 2}" cy="${y + cell / 2}" r="${Math.max(2, cell * .09)}" fill="#d6d9ec"/>`;
        }
        // row labels and column labels
        for (let r = 0; r < rows; r++) s += `<text x="${LM - 9}" y="${TM + r * cell + cell / 2 + 4.5}" text-anchor="end" font-size="12" font-weight="800" fill="#8b5cf6">${r + 1}</text>`;
        for (let c = 0; c < cols; c++) s += `<text x="${LM + c * cell + cell / 2}" y="${TM - 9}" text-anchor="middle" font-size="12" font-weight="800" fill="#3b82f6">${c + 1}</text>`;
        // handle
        const hx = LM + cols * cell, hy = TM + rows * cell;
        if (mode === 'array' || mode === 'table') s += `<g pointer-events="none"><circle cx="${hx}" cy="${hy}" r="13" fill="#8b5cf6" stroke="#fff" stroke-width="3"/><path d="M${hx - 5} ${hy - 1}l4 4M${hx - 5} ${hy - 1}v-4h4" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" transform="rotate(${mode === 'table' ? 45 : 0} ${hx} ${hy})"/><path d="M${hx + 5} ${hy + 1}l-4 -4M${hx + 5} ${hy + 1}v4h-4" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" transform="rotate(${mode === 'table' ? 45 : 0} ${hx} ${hy})"/></g>`;
        if (!svg || !stage.contains(svg)) {
          stage.innerHTML = `<svg class="lb-arraygrid-svg" ${mode === 'table' ? 'style="cursor:ns-resize"' : ''}></svg>`;
          svg = stage.querySelector('svg'); bindDrag();
        }
        svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
        svg.innerHTML = s;
      }
      function readArray() {
        const n = rows * cols;
        const rep = rows <= 6 ? Array(rows).fill(cols).join(' + ') + ' = ' + n : `${cols} + ${cols} + … (${rows} times) = ${n}`;
        if (mode === 'table') {
          eqEl.innerHTML = `<span class="c">${table}</span> × <span class="r">${rows}</span> = <span class="a">${n}</span>`;
          subEl.textContent = Array.from({ length: rows }, (_, i) => table * (i + 1)).join(', ');
        } else {
          eqEl.innerHTML = `<span class="r">${rows}</span> × <span class="c">${cols}</span> = <span class="a">${n}</span>`;
          subEl.textContent = `${rows} row${rows > 1 ? 's' : ''} of ${cols}: ${rep}`;
        }
        if (mode === 'array' && ask === 'factors') {
          const all = unordered(tP);
          chipsEl.innerHTML = all.map(k => `<span class="lb-arraygrid-chip${found.has(k) ? '' : ' no'}">${found.has(k) ? k.replace('×', ' × ') : '? × ?'}</span>`).join('');
        } else chipsEl.innerHTML = '';
        chipsEl.style.display = chipsEl.innerHTML ? '' : 'none';
      }

      // ---------- share drawing ----------
      function drawShare() {
        const isz = total > 24 ? 18 : 22;
        let s = `<div class="lb-arraygrid-pile"><div class="lbl">${pile ? `${pile} to share — tap a plate` : 'All shared!'}</div>`;
        for (let i = 0; i < pile; i++) s += itemHTML(item, isz);
        s += '</div><div class="lb-arraygrid-plates">';
        const mx = Math.max(...plates);
        const labels = Array.isArray(p.groupLabels) ? p.groupLabels : [];
        const pw = groups > 6 ? 62 : 74;
        plates.forEach((k, g) => {
          s += `<div class="lb-arraygrid-pw"><div class="lb-arraygrid-plate${k && plates.every(x => x === k) ? ' full' : ''}" data-g="${g}" style="width:${pw}px">`;
          for (let i = 0; i < k; i++) s += itemHTML(item, k > 6 ? 15 : 19);
          s += `<b>${labels[g] != null ? esc(labels[g]) + ': ' : ''}${k}</b></div></div>`;
        });
        stage.innerHTML = s + '</div>';
        const q = Math.floor(total / groups), r = total % groups;
        const fair = plates.every(x => x === plates[0]);
        if (pile < groups && fair) {
          eqEl.innerHTML = `<span class="a">${total}</span> ÷ <span class="r">${groups}</span> = <span class="c">${plates[0]}</span>${pile ? ` <span style="font-size:.7em">rem</span> <span style="color:#ff6b6b">${pile}</span>` : ''}`;
          subEl.textContent = `${groups} × ${plates[0]}${pile ? ' + ' + pile : ''} = ${total}`;
        } else {
          eqEl.innerHTML = `<span class="a">${total}</span> ÷ <span class="r">${groups}</span> = <span style="color:#c0c4dc">?</span>`;
          subEl.textContent = `On plates: ${plates.join(', ')} · left: ${pile}`;
        }
        chipsEl.style.display = 'none';
      }

      function buildRow() {
        let s = '';
        const step = (lab, key, v, col) => `<div class="lb-arraygrid-sl" style="background:${col}1f;color:${col}"><span>${lab}</span><button class="lb-arraygrid-s" data-act="${key}-">−</button><output>${v}</output><button class="lb-arraygrid-s" data-act="${key}+">+</button></div>`;
        if (mode === 'array') { s += step('Rows', 'r', rows, '#8b5cf6') + step('Cols', 'c', cols, '#3b82f6'); s += `<button class="lb-arraygrid-s" data-act="turn">↻ Turn</button>`; }
        else if (mode === 'table') s += step('Rows', 'r', rows, '#8b5cf6');
        else {
          s += `<button class="lb-arraygrid-s go" data-act="deal">Deal 1 each</button><button class="lb-arraygrid-s" data-act="undo">↩ Undo</button>`;
          if (p.lockGroups === false) s += step('Plates', 'g', groups, '#8b5cf6');
        }
        s += `<button class="lb-arraygrid-s" data-act="reset">↺</button>`;
        if (p.newChallenge !== false) s += `<button class="lb-arraygrid-s" data-act="new">✨ New</button>`;
        rowEl.innerHTML = s;
      }
      function refresh() { if (mode === 'share') drawShare(); else { drawGrid(); readArray(); } buildRow(); }

      // ---------- win logic ----------
      let won = false;
      function win(msg) { if (won) return; won = true; api.sfx('correct'); hint('⭐ Super!'); api.win(msg); }
      function check(final) {
        if (won) return;
        const n = rows * cols;
        if (mode === 'table') { if (n === tP) win(`${table} × ${rows} = ${tP}`); return; }
        if (mode === 'array') {
          if (ask === 'exact') { if (rows === tR && cols === tC) win(`${tR} rows of ${tC} = ${tR} × ${tC} = ${tR * tC} ${word}`); else if (final && rows === tC && cols === tR && tR !== tC) hint(`That is ${rows} rows of ${cols}. Turn it!`); }
          else if (ask === 'product') { if (n === tP && rows >= minSide && cols >= minSide) win(`${rows} × ${cols} = ${tP}`); }
          else if (final && n === tP) {
            const k = Math.min(rows, cols) + '×' + Math.max(rows, cols);
            if (!found.has(k)) { found.add(k); api.sfx('coin'); hint(`Found ${rows} × ${cols}!`); readArray(); }
            else hint('You found that one already. Try another!');
            const all = unordered(tP);
            if (all.every(x => found.has(x))) win(`All arrays of ${tP}: ${all.map(x => x.replace('×', ' × ')).join(', ')}`);
          }
        }
        if (mode === 'share') {
          const fair = plates.every(x => x === plates[0]);
          if (pile < groups && fair) { const q = plates[0]; win(`${total} ÷ ${groups} = ${q}${pile ? ` remainder ${pile}` : ''} — ${q} each${pile ? `, ${pile} left over` : ''}`); }
          else if (pile < groups && pile >= 0 && !fair) { api.sfx('hmm'); hint('Not fair yet — every plate must have the same!'); }
        }
      }

      // ---------- dragging the array ----------
      let dragging = false;
      function cellAt(ev) {
        const r = svg.getBoundingClientRect(), sc = W / r.width;
        const x = (ev.clientX - r.left) * sc, y = (ev.clientY - r.top) * sc;
        return { c: Math.max(1, Math.min(maxC, Math.ceil((x - LM) / cell))), r: Math.max(1, Math.min(maxR, Math.ceil((y - TM) / cell))) };
      }
      function setSize(r2, c2) {
        if (mode === 'table') c2 = table;
        if (r2 === rows && c2 === cols) return;
        rows = r2; cols = c2; api.sfx('tap'); hint('');
        drawGrid(); readArray(); buildRow();
        if (mode === 'table' || ask !== 'factors') check(false);
      }
      function bindDrag() {
        svg.addEventListener('pointerdown', ev => { dragging = true; try { svg.setPointerCapture(ev.pointerId); } catch (e) { } const k = cellAt(ev); setSize(k.r, k.c); ev.preventDefault(); });
        svg.addEventListener('pointermove', ev => { if (!dragging) return; const k = cellAt(ev); setSize(k.r, k.c); });
        const up = () => { if (!dragging) return; dragging = false; check(true); };
        svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
      }

      // ---------- buttons & plate taps ----------
      stage.addEventListener('click', e => {
        if (mode !== 'share') return;
        const pl = e.target.closest('[data-g]'); if (!pl) return;
        if (!pile) { api.sfx('hmm'); hint('Nothing left to share!'); return; }
        const g = +pl.dataset.g; plates[g]++; pile--; history.push([g]); api.sfx('tap'); hint('');
        drawShare(); check(true);
      });
      rowEl.addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b) return; const a = b.dataset.act;
        if (a === 'r-' || a === 'r+') { const r2 = rows + (a === 'r+' ? 1 : -1); if (r2 < 1 || r2 > maxR) { api.sfx('wrong'); return; } setSize(r2, cols); check(true); return; }
        if (a === 'c-' || a === 'c+') { const c2 = cols + (a === 'c+' ? 1 : -1); if (c2 < 1 || c2 > maxC) { api.sfx('wrong'); return; } setSize(rows, c2); check(true); return; }
        if (a === 'turn') { if (cols > maxR || rows > maxC) { api.sfx('wrong'); hint('Too big to turn here'); return; } setSize(cols, rows); hint(`${cols} × ${rows} = ${rows} × ${cols} — same total!`); check(true); return; }
        if (a === 'deal') {
          if (pile < groups) { api.sfx('hmm'); hint(pile ? `Only ${pile} left — not enough for everyone!` : 'Nothing left to share!'); check(true); return; }
          for (let g = 0; g < groups; g++) plates[g]++; pile -= groups; history.push(plates.map((_, g) => g)); api.sfx('coin'); hint(''); drawShare(); check(true); return;
        }
        if (a === 'undo') { const h = history.pop(); if (!h) return; h.forEach(g => { plates[g]--; pile++; }); api.sfx('tap'); hint(''); drawShare(); return; }
        if (a === 'g-' || a === 'g+') { const g2 = groups + (a === 'g+' ? 1 : -1); if (g2 < 1 || g2 > 10) return; groups = g2; resetShare(); setText(); refresh(); return; }
        if (a === 'reset') { if (mode === 'share') resetShare(); else { rows = mode === 'table' ? 1 : int(p.rows, 2, 1, maxR); cols = mode === 'table' ? table : int(p.cols, 3, 1, maxC); found = new Set(); } hint(''); refresh(); api.sfx('tap'); return; }
        if (a === 'new') newChallenge();
      });
      function newChallenge() {
        const r = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
        if (mode === 'share') { const g = r(2, Math.min(6, 10)); groups = p.lockGroups === false ? groups : g; total = r(groups * 2, Math.min(40, groups * 6)); resetShare(); }
        else if (mode === 'table') { let t; do { t = table * r(2, 10); } while (t === tP); tP = t; rows = 1; }
        else if (ask === 'exact') { let a, b; do { a = r(2, Math.min(maxR, 6)); b = r(2, Math.min(maxC, 8)); } while (a === tR && b === tC); tR = a; tC = b; }
        else { const cands = [6, 8, 10, 12, 16, 18, 20, 24, 30, 36].filter(n => n !== tP && unordered(n).length >= 2 && (ask !== 'product' || pairs(n).length)); tP = cands[Math.floor(Math.random() * cands.length)] || 12; found = new Set(); }
        customText = ''; if (won) { won = false; api.resetWin && api.resetWin(); }
        setText(); hint(''); refresh(); api.sfx('tap');
      }

      setText(); refresh();
      return () => { dragging = false; };
    },
    example: { mode: 'array', ask: 'exact', target: '3x5', rows: 2, cols: 2, maxRows: 8, maxCols: 8, item: 'apple' },
    examples: [
      { mode: 'array', ask: 'factors', target: 12, maxRows: 12, maxCols: 12, item: 'star', challenge: 'Find every rectangle array of 12 stars. These are the factor pairs of 12!' },
      { mode: 'table', table: 6, target: 42, item: 'flower', challenge: '6 × ? = 42. Grow rows of 6 flowers until you have 42.' },
      { mode: 'share', total: 14, groups: 4, item: 'sweet', groupLabels: ['Riya', 'Aman', 'Zoya', 'Kabir'], challenge: 'Share 14 laddoos fairly among 4 friends. How many each? Any left over?' }
    ]
  });
})();
