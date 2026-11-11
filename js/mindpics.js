/* ================= 🖼️ Mind Gym picture puzzles (js/mindpics.js) =================
   Draws the picture-reasoning questions of content/mind/pics.json (made by tools/mind/gen_pics.py) as
   colourful SVG, with playful touches:
     • pictures bounce in, wiggle when tapped, dice wobble, paper-folding plays as a little story (↻ replay)
     • after answering, "▶ Show me" animates the reason: the picture flips in the mirror or the lake, the
       series turns once more, the odd one flips, the paper unfolds hole by hole, shapes are counted one by one,
       the missing tile drops in.
   The shapes and colours come from the same JSON the generator used to check every answer.
   window.MindPics = { init(data), stem(q), opt(q, k), isBig(q), show(q, host) } */
(function () {
  'use strict';
  let SH = {}, COL = [];
  const PT = {};
  const pts = s => PT[s] || (PT[s] = (SH[s] || []).map(p => p.join(',')).join(' '));

  function init(d) { SH = d.shapes || {}; COL = d.colors || []; }

  /* ---------- figures made of shapes ---------- */
  const shp = e => `<polygon points="${pts(e.s)}" fill="${COL[e.c] || '#888'}" stroke="rgba(0,0,0,.28)" stroke-width="${(1.1 / e.z).toFixed(3)}" stroke-linejoin="round" transform="translate(${e.x} ${e.y}) rotate(${e.r}) scale(${e.fx * e.z} ${e.fy * e.z})"/>`;
  const fig = (F, cls) => `<svg class="mp-fig ${cls || ''}" viewBox="0 0 100 100" aria-hidden="true"><rect x="2" y="2" width="96" height="96" rx="12" class="mp-bg"/>${F.map(shp).join('')}</svg>`;

  /* ---------- paper ---------- */
  const G = 4, CS = 100 / G;
  function region(folds) {
    let c = []; for (let r = 0; r < G; r++) for (let k = 0; k < G; k++) c.push([r, k]);
    folds.forEach(f => { c = c.filter(([r, k]) => f === 'v' ? k >= G / 2 : f === 'h' ? r >= G / 2 : r >= k); });
    return c;
  }
  function paper(cells, holes, extra) {
    const full = cells == null;
    const cellSet = full ? null : new Set(cells.map(x => x.join()));
    let s = '';
    if (!full) s += `<rect x="3" y="3" width="94" height="94" rx="4" class="mp-ghost"/>`;
    for (let r = 0; r < G; r++) for (let k = 0; k < G; k++) {
      if (full || cellSet.has(r + ',' + k)) {
        const diagHalf = !full && extra && extra.diag && r === k;
        s += diagHalf ? `<polygon points="${k * CS},${r * CS} ${k * CS},${(r + 1) * CS} ${(k + 1) * CS},${(r + 1) * CS}" class="mp-paper"/>` : `<rect x="${k * CS}" y="${r * CS}" width="${CS}" height="${CS}" class="mp-paper"/>`;
      }
    }
    s += `<g class="mp-gridl">${[1, 2, 3].map(i => `<line x1="${i * CS}" y1="0" x2="${i * CS}" y2="100"/><line x1="0" y1="${i * CS}" x2="100" y2="${i * CS}"/>`).join('')}</g>`;
    (holes || []).forEach(([r, k], i) => { s += `<circle cx="${k * CS + CS / 2}" cy="${r * CS + CS / 2}" r="6.5" class="mp-hole" style="animation-delay:${(extra && extra.delay ? extra.delay : 0) + i * 0.15}s"/>`; });
    if (extra && extra.line) s += extra.line;
    return `<svg class="mp-fig mp-pap" viewBox="-4 -4 108 108" aria-hidden="true">${s}</svg>`;
  }
  const FOLDLINE = { v: '<line x1="50" y1="-2" x2="50" y2="102" class="mp-fold"/><path d="M22 50 q28 -26 52 0" class="mp-arw" marker-end="url(#mpA)"/>',
    h: '<line x1="-2" y1="50" x2="102" y2="50" class="mp-fold"/><path d="M50 22 q-26 28 0 52" class="mp-arw" marker-end="url(#mpA)"/>',
    d: '<line x1="-2" y1="-2" x2="102" y2="102" class="mp-fold"/><path d="M76 24 q-6 50 -52 52" class="mp-arw" marker-end="url(#mpA)"/>' };
  const ARROWDEF = '<defs><marker id="mpA" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#ff5a5f"/></marker></defs>';
  function paperStory(q) {
    const steps = [];
    q.folds.forEach((f, i) => steps.push({ t: `${i + 1}. Fold`, svg: paper(i ? region(q.folds.slice(0, i)) : null, [], { line: ARROWDEF + FOLDLINE[f], diag: false }) }));
    steps.push({ t: `${q.folds.length + 1}. Punch!`, svg: paper(region(q.folds), q.holes, { diag: q.folds.includes('d'), delay: 0.2 }) });
    return `<div class="mp-story">${steps.map((s, i) => `<div class="mp-step" style="animation-delay:${i * 0.55}s"><b>${s.t}</b>${s.svg}</div>`).join('<span class="mp-then" aria-hidden="true">→</span>')}</div>`;
  }

  /* ---------- counting ---------- */
  function countSvg(q, hi) {
    let s = '';
    if (q.grid) {
      const [w, h] = q.grid, c = 84 / Math.max(w, h), ox = 50 - w * c / 2, oy = 50 - h * c / 2;
      s += `<rect x="${ox}" y="${oy}" width="${w * c}" height="${h * c}" class="mp-cfill"/>`;
      for (let i = 0; i <= w; i++) s += `<line x1="${ox + i * c}" y1="${oy}" x2="${ox + i * c}" y2="${oy + h * c}" class="mp-cl"/>`;
      for (let i = 0; i <= h; i++) s += `<line x1="${ox}" y1="${oy + i * c}" x2="${ox + w * c}" y2="${oy + i * c}" class="mp-cl"/>`;
      if (hi) { const [x, y, ww, hh] = hi; s += `<rect x="${ox + x * c + 1.2}" y="${oy + y * c + 1.2}" width="${ww * c - 2.4}" height="${hh * c - 2.4}" class="mp-hi"/>`; }
    } else {
      const [m, hl] = q.fan, P = (t, L) => [50 + (10 + 80 * t - 50) * L, 10 + 80 * L];
      s += `<polygon points="50,10 90,90 10,90" class="mp-cfill"/>`;
      for (let i = 0; i <= m; i++) { const [x, y] = P(i / m, 1); s += `<line x1="50" y1="10" x2="${x}" y2="${y}" class="mp-cl"/>`; }
      for (let l = 1; l <= hl + 1; l++) { const L = l / (hl + 1), [x1, y] = P(0, L), [x2] = P(1, L); s += `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" class="mp-cl"/>`; }
      if (hi) { const [a, b, L] = hi, A = P(a, L), B = P(b, L); s += `<polygon points="50,10 ${A.join(',')} ${B.join(',')}" class="mp-hi"/>`; }
    }
    return `<svg class="mp-fig mp-count" viewBox="0 0 100 100" aria-hidden="true">${s}</svg>`;
  }

  /* ---------- dice ---------- */
  const PIPS = { 1: [[.5, .5]], 2: [[.27, .27], [.73, .73]], 3: [[.25, .25], [.5, .5], [.75, .75]], 4: [[.27, .27], [.73, .27], [.27, .73], [.73, .73]],
    5: [[.25, .25], [.75, .25], [.5, .5], [.25, .75], [.75, .75]], 6: [[.28, .22], [.28, .5], [.28, .78], [.72, .22], [.72, .5], [.72, .78]] };
  const FACE = { top: [[50, 14], [30, 14], [-30, 14]], front: [[20, 28], [30, 14], [0, 36]], right: [[50, 42], [30, -14], [0, 36]] };
  function face(name, n, mark) {
    const [[ox, oy], [ux, uy], [vx, vy]] = FACE[name];
    const poly = [[ox, oy], [ox + ux, oy + uy], [ox + ux + vx, oy + uy + vy], [ox + vx, oy + vy]].map(p => p.join(',')).join(' ');
    return `<polygon points="${poly}" class="mp-df mp-df-${name}${mark ? ' mk' : ''}"/><g transform="matrix(${ux} ${uy} ${vx} ${vy} ${ox} ${oy})">${(PIPS[n] || []).map(([a, b]) => `<circle cx="${a}" cy="${b}" r=".085" class="mp-pip"/>`).join('')}</g>`;
  }
  const die = (v, mark) => `<svg class="mp-fig mp-die" viewBox="8 8 84 84" aria-hidden="true">${face('top', v[0], mark === v[0])}${face('front', v[1], mark === v[1])}${face('right', v[2], mark === v[2])}</svg>`;

  /* ---------- matrix and symmetry tiles ---------- */
  function cell(x) {
    if (!x) return `<svg class="mp-cell q" viewBox="0 0 100 100" aria-hidden="true"><rect x="4" y="4" width="92" height="92" rx="14" class="mp-qbox"/><text x="50" y="66" text-anchor="middle" class="mp-qm">?</text></svg>`;
    const L = { 1: [[50, 50, 24]], 2: [[30, 50, 17], [70, 50, 17]], 3: [[20, 50, 13], [50, 50, 13], [80, 50, 13]] }[x.n] || [];
    return `<svg class="mp-cell" viewBox="0 0 100 100" aria-hidden="true"><rect x="4" y="4" width="92" height="92" rx="14" class="mp-bg"/>${L.map(([cx, cy, z]) => shp({ s: x.s, x: cx, y: cy, z, r: 0, c: x.c, fx: 1, fy: 1 })).join('')}</svg>`;
  }
  function tile(t, hole, fill) {
    const n = t.length, c = 100 / n; let s = '';
    for (let r = 0; r < n; r++) for (let k = 0; k < n; k++) {
      let v = t[r][k], inHole = hole && r >= hole[0] && r < hole[0] + 3 && k >= hole[1] && k < hole[1] + 3;
      if (inHole && fill) v = fill[r - hole[0]][k - hole[1]];
      if (inHole && !fill) continue;
      s += `<rect x="${k * c + .8}" y="${r * c + .8}" width="${c - 1.6}" height="${c - 1.6}" rx="3" fill="${v === -1 || v == null ? '#fff' : COL[v]}" class="mp-tc${inHole ? ' in' : ''}"/>`;
    }
    if (hole && !fill) s += `<rect x="${hole[1] * c + 1}" y="${hole[0] * c + 1}" width="${3 * c - 2}" height="${3 * c - 2}" rx="6" class="mp-qbox"/><text x="${hole[1] * c + 1.5 * c}" y="${hole[0] * c + 1.5 * c + 9}" text-anchor="middle" class="mp-qm">?</text>`;
    if (hole) s += `<line x1="50" y1="0" x2="50" y2="100" class="mp-mid"/><line x1="0" y1="50" x2="100" y2="50" class="mp-mid"/>`;
    return `<svg class="mp-fig mp-tile" viewBox="-2 -2 104 104" aria-hidden="true">${s}</svg>`;
  }

  /* ---------- question picture ---------- */
  const box = (inner, cls) => `<div class="mp-stem ${cls || ''}">${inner}</div>`;
  function stem(q) {
    switch (q.k) {
      case 'mirror': return box(`<div class="mp-pair"><span class="mp-tap">${fig(q.stem || [])}</span><span class="mp-mirror" aria-hidden="true"></span><span class="mp-ghostq" aria-hidden="true">?</span></div>`);
      case 'water': return box(`<div class="mp-col"><span class="mp-tap">${fig(q.stem || [])}</span><span class="mp-lake" aria-hidden="true"></span><span class="mp-ghostq" aria-hidden="true">?</span></div>`);
      case 'series': return box(`<div class="mp-row">${q.stem.map((F, i) => `<span class="mp-tap mp-pop" style="animation-delay:${i * .12}s">${fig(F, 'sm')}</span>`).join('')}<span class="mp-ghostq sm" aria-hidden="true">?</span></div>`);
      case 'analogy': return box(`<div class="mp-row">${`<span class="mp-tap">${fig(q.stem[0], 'sm')}</span><b class="mp-to">→</b><span class="mp-tap">${fig(q.stem[1], 'sm')}</span><b class="mp-as">as</b><span class="mp-tap">${fig(q.stem[2], 'sm')}</span><b class="mp-to">→</b><span class="mp-ghostq sm">?</span>`}</div>`);
      case 'paper': return box(paperStory(q) + '<button type="button" class="mp-replay">↻ Replay</button>', 'mp-paperbox');
      case 'count': return box(`<span class="mp-tap">${countSvg(q)}</span>`);
      case 'dice': return box(`<div class="mp-row">${q.views.map(v => `<span class="mp-tap mp-wob">${die(v)}</span>`).join('')}</div>`);
      case 'matrix': return box(`<div class="mp-grid3">${q.grid.flat().map(x => cell(x)).join('')}</div>`);
      case 'symmetry': return box(tile(q.tile, q.hole));
      default: return '';
    }
  }
  const isPic = q => !!q && ['mirror', 'water', 'series', 'odd', 'analogy', 'paper', 'count', 'dice', 'matrix', 'symmetry'].includes(q.k) && Array.isArray(q.o);
  const textOpts = q => q.k === 'count' || q.k === 'dice';
  function opt(q, k) {
    const o = q.o[k];
    if (textOpts(q)) return `<span class="mp-num">${o}</span>`;
    if (q.k === 'paper') return paper(null, o);
    if (q.k === 'matrix') return cell(o);
    if (q.k === 'symmetry') return tile(o);
    return fig(o);
  }

  /* ---------- "Show me" animations ---------- */
  function show(q, host) {
    const a = q.o[q.a]; let html = '';
    if (q.k === 'mirror' || q.k === 'water') html = `<div class="mp-row"><span>${fig(q.stem)}</span><b class="mp-to">→</b><span class="mp-flip ${q.k}">${fig(q.stem)}</span></div>`;
    else if (q.k === 'series') html = `<div class="mp-row">${q.stem.map(F => fig(F, 'sm')).join('')}<span class="mp-turn" style="--t:${q.turn}deg">${fig(q.stem[q.stem.length - 1], 'sm')}</span></div>`;
    else if (q.k === 'odd') html = `<div class="mp-row"><span class="mp-flip mirror">${fig(a)}</span></div><p class="mp-cap">Watch it flip: it only matches as a mirror image.</p>`;
    else if (q.k === 'analogy') html = `<div class="mp-row">${fig(q.stem[0], 'sm')}<b class="mp-to">→</b>${fig(q.stem[1], 'sm')}<b class="mp-as">as</b>${fig(q.stem[2], 'sm')}<b class="mp-to">→</b><span class="mp-drop">${fig(a, 'sm')}</span></div>`;
    else if (q.k === 'paper') {
      let hs = q.holes.map(h => h.slice()); const frames = [paper(region(q.folds), hs, { diag: q.folds.includes('d') })];
      q.folds.slice().reverse().forEach((f, i) => {
        const add = hs.map(([r, c]) => f === 'v' ? [r, G - 1 - c] : f === 'h' ? [G - 1 - r, c] : [c, r]);
        add.forEach(x => { if (!hs.some(y => y[0] === x[0] && y[1] === x[1])) hs.push(x); });
        frames.push(paper(region(q.folds.slice(0, q.folds.length - 1 - i)), hs.slice(), { line: FOLDLINE[f].split('<path')[0], diag: q.folds.slice(0, q.folds.length - 1 - i).includes('d') }));
      });
      html = `<div class="mp-story">${frames.map((s, i) => `<div class="mp-step" style="animation-delay:${i * .7}s"><b>${i ? 'Unfold' : 'Folded'}</b>${s}</div>`).join('<span class="mp-then">→</span>')}</div>`;
    }
    else if (q.k === 'count') { html = `<div class="mp-row"><span class="mp-cbox">${countSvg(q)}</span><b class="mp-counter">0</b></div>`; }
    else if (q.k === 'dice') html = `<div class="mp-row">${q.views.map(v => `<span class="mp-wob">${die(v, +q.q.match(/opposite (\d)/)[1])}</span>`).join('')}</div>`;
    else if (q.k === 'matrix') html = `<div class="mp-grid3">${q.grid.flat().map(x => x ? cell(x) : `<span class="mp-drop">${cell(a)}</span>`).join('')}</div>`;
    else if (q.k === 'symmetry') html = `<div class="mp-drop2">${tile(q.tile, q.hole, a)}</div>`;
    host.innerHTML = `<div class="mp-show">${html}</div>`;
    if (q.k === 'count') {
      const items = q.items || [], b = host.querySelector('.mp-cbox'), n = host.querySelector('.mp-counter'); let i = 0;
      const step = Math.max(120, Math.min(600, 9000 / Math.max(1, items.length)));
      const t = setInterval(() => { if (!host.isConnected || i >= items.length) { clearInterval(t); if (host.isConnected) { b.innerHTML = countSvg(q); n.textContent = items.length + ' ✓'; } return; } b.innerHTML = countSvg(q, items[i]); n.textContent = ++i; }, step);
    }
  }

  /* ---------- playful touches ---------- */
  function wire(root) {
    root.querySelectorAll('.mp-tap').forEach(x => x.addEventListener('click', () => { x.classList.remove('wig'); void x.offsetWidth; x.classList.add('wig'); try { sfx && sfx('tap'); } catch (e) {} }));
    const rp = root.querySelector('.mp-replay');
    if (rp) rp.onclick = () => { const s = root.querySelector('.mp-story'); if (s) { const c = s.cloneNode(true); s.replaceWith(c); } };
  }

  let css = false;
  function style() {
    if (css) return; css = true;
    document.head.insertAdjacentHTML('beforeend', `<style id="mpCss">
      .mp-stem{display:flex;flex-direction:column;align-items:center;gap:8px;margin:6px 0 14px;padding:12px;border-radius:18px;background:linear-gradient(160deg,#fff7e6,#eaf6ff);box-shadow:inset 0 0 0 2px rgba(0,0,0,.04)}
      .mp-fig{width:132px;height:132px;display:block;filter:drop-shadow(0 3px 4px rgba(0,0,0,.12))}.mp-fig.sm{width:56px;height:56px}
      .mp-bg{fill:#fff;stroke:#e3e6f0;stroke-width:1.2}
      .mp-pair,.mp-col,.mp-row{display:flex;align-items:center;justify-content:center;gap:6px;flex-wrap:wrap}.mp-col{flex-direction:column;gap:2px}
      .mp-mirror{width:12px;height:128px;border-radius:6px;background:linear-gradient(90deg,#9ad7ff,#e8f7ff 40%,#7cc4f2);box-shadow:0 0 0 2px #5aa9d6,0 0 14px #9ad7ff;animation:mpShine 2.2s infinite}
      .mp-lake{width:140px;height:14px;border-radius:9px;background:repeating-linear-gradient(90deg,#4fb3ff 0 14px,#8fd0ff 14px 28px);animation:mpWave 1.6s linear infinite}
      .mp-ghostq{width:70px;height:70px;border:3px dashed #b9a7ff;border-radius:14px;display:grid;place-items:center;font-weight:900;font-size:34px;line-height:1;color:#9b5cff;animation:mpPulse 1.4s infinite}.mp-ghostq.sm{width:52px;height:52px;font-size:26px}
      .mp-to,.mp-as{font-size:20px;color:#7b6cff}.mp-as{font-size:14px;text-transform:uppercase}
      .mp-pop{animation:mpPop .45s both}.mp-tap{cursor:pointer;display:inline-block}.mp-tap.wig{animation:mpWig .5s}
      .mp-wob{display:inline-block;animation:mpWob 3s ease-in-out infinite}.mp-wob:nth-child(2){animation-delay:1.5s}
      .mp-die{width:118px;height:118px}.mp-df{stroke:#3a3f55;stroke-width:1.4;stroke-linejoin:round}.mp-df-top{fill:#fff}.mp-df-front{fill:#f1f3fb}.mp-df-right{fill:#dde2f2}.mp-df.mk{fill:#ffe27a}
      .mp-pip{fill:#e5334b}
      .mp-paper{fill:#fff4c9;stroke:#e0b84a;stroke-width:1.2}.mp-ghost{fill:none;stroke:#cdbf91;stroke-dasharray:3 3}.mp-gridl line{stroke:rgba(160,130,40,.25);stroke-width:.7}
      .mp-hole{fill:#2a2350;stroke:#fff;stroke-width:1.6;transform-box:fill-box;transform-origin:center;animation:mpPunch .35s both}
      .mp-fold{stroke:#ff5a5f;stroke-width:2;stroke-dasharray:5 4}.mp-arw{fill:none;stroke:#ff5a5f;stroke-width:2.4}
      .mp-story{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:4px}.mp-step{display:flex;flex-direction:column;align-items:center;gap:2px;animation:mpPop .5s both}
      .mp-step b{font-size:12px;color:#8a6d00}.mp-step .mp-fig{width:86px;height:86px}.mp-then{color:#c9a400;font-weight:900}
      .mp-replay{border:0;background:#ffe9a8;color:#7a5b00;font-weight:800;font-size:13px;font-family:inherit;border-radius:999px;padding:5px 12px;cursor:pointer}
      .mp-count{width:170px;height:170px}.mp-cfill{fill:#eef7ff;stroke:none}.mp-cl{stroke:#2b5ea8;stroke-width:1.6;stroke-linecap:round}.mp-hi{fill:rgba(255,196,61,.55);stroke:#ff8a1f;stroke-width:2;animation:mpFlash .3s}
      .mp-counter{font-weight:900;font-size:34px;color:#ff8a1f;min-width:70px;text-align:center}
      .mp-grid3{display:grid;grid-template-columns:repeat(3,66px);gap:6px}.mp-cell{width:66px;height:66px;display:block}
      .mp-qbox{fill:#f5f0ff;stroke:#9b5cff;stroke-width:2.2;stroke-dasharray:6 4}.mp-qm{font:900 34px sans-serif;fill:#9b5cff}
      .mp-tile{width:170px;height:170px}.mp-tc{stroke:rgba(0,0,0,.08);stroke-width:.6}.mp-tc.in{animation:mpPop .5s both}.mp-mid{stroke:#7b6cff;stroke-width:1.2;stroke-dasharray:3 3}
      .mg-o.pic{display:flex;justify-content:center;align-items:center;padding:8px}.mg-o.pic .mp-fig{width:100%;height:auto;max-width:120px;aspect-ratio:1}
      .mg-o.pic .mp-cell{width:76px;height:76px}.mp-num{font-weight:900;font-size:30px;display:block;text-align:center;width:100%}
      .mg-opts.picg{grid-template-columns:1fr 1fr}
      .mp-show{margin:10px 0 4px;padding:10px;border-radius:16px;background:#f7f4ff}.mp-cap{text-align:center;font-size:13px;margin:6px 0 0}
      .mp-flip svg{animation:mpFlipX 1.4s ease-in-out both}.mp-flip.water svg{animation-name:mpFlipY}.mp-flip.mirror svg{animation-name:mpFlipX}
      .mp-turn svg{animation:mpTurn 1.2s .4s ease-in-out both}
      .mp-drop{display:inline-block;animation:mpDrop .7s cubic-bezier(.3,1.6,.5,1) both}.mp-drop2 .mp-tc.in{animation:mpDrop .7s both}
      @keyframes mpPop{from{transform:scale(.4);opacity:0}to{transform:none;opacity:1}}
      @keyframes mpWig{25%{transform:rotate(-8deg) scale(1.06)}50%{transform:rotate(7deg)}75%{transform:rotate(-3deg)}}
      @keyframes mpWob{0%,100%{transform:rotate(0)}50%{transform:rotate(-6deg) translateY(-3px)}}
      @keyframes mpPulse{50%{transform:scale(1.07);border-color:#ff8a1f;color:#ff8a1f}}
      @keyframes mpShine{50%{box-shadow:0 0 0 2px #5aa9d6,0 0 24px #c7ecff}}
      @keyframes mpWave{to{background-position:28px 0}}
      @keyframes mpPunch{0%{transform:scale(0)}70%{transform:scale(1.3)}100%{transform:scale(1)}}
      @keyframes mpFlash{from{opacity:0}}
      @keyframes mpFlipX{0%,15%{transform:scaleX(1)}55%{transform:scaleX(.02)}85%,100%{transform:scaleX(-1)}}
      @keyframes mpFlipY{0%,15%{transform:scaleY(1)}55%{transform:scaleY(.02)}85%,100%{transform:scaleY(-1)}}
      @keyframes mpTurn{from{transform:rotate(0)}to{transform:rotate(var(--t))}}
      @keyframes mpDrop{0%{transform:translateY(-60px) scale(.6);opacity:0}100%{transform:none;opacity:1}}
      @media (prefers-reduced-motion:reduce){.mp-stem *,.mp-show *{animation-duration:.01s!important;animation-iteration-count:1!important}}
    </style>`);
  }
  window.MindPics = { init, stem: q => (style(), stem(q)), opt, isPic, textOpts, show: (q, h) => (style(), show(q, h)), wire };
})();
